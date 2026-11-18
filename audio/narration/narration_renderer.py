"""
SUPER.INTELLIGENCEEE — Narration Renderer Module
Renders directed script segments, stitches audio with smooth crossfades,
normalizes loudness, prevents clipping and dead-air gaps, and produces
a detailed transcript-to-audio timing manifest.
"""

from __future__ import annotations

import dataclasses
import json
import logging
import math
import wave
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from core.config import get_config
from audio.narration.voice_director import DirectedScript, NarrationSegment, VoiceDirector
from audio.narration.narration_service import NarrationService

logger = logging.getLogger("super_intelligence.narration_renderer")


@dataclasses.dataclass
class SegmentTiming:
    """Precise timing marker for a rendered speech segment."""
    segment_index: int
    text: str
    start_seconds: float
    end_seconds: float
    duration_seconds: float
    audio_path: str


@dataclasses.dataclass
class RenderedNarrationResult:
    """Complete narration render product with timing manifest."""
    master_audio_path: Path
    timing_manifest_path: Path
    total_duration_seconds: float
    sample_rate: int
    segment_count: int
    timings: List[SegmentTiming]
    engine_used: str
    voice_used: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "master_audio_path": str(self.master_audio_path),
            "timing_manifest_path": str(self.timing_manifest_path),
            "total_duration_seconds": self.total_duration_seconds,
            "sample_rate": self.sample_rate,
            "segment_count": self.segment_count,
            "engine_used": self.engine_used,
            "voice_used": self.voice_used,
            "segments": [
                {
                    "segment_index": t.segment_index,
                    "text": t.text,
                    "start_seconds": t.start_seconds,
                    "end_seconds": t.end_seconds,
                    "duration_seconds": t.duration_seconds,
                    "audio_path": t.audio_path,
                }
                for t in self.timings
            ],
        }


class NarrationRenderer:
    """
    Renders directed scripts into broadcast-grade continuous voiceover tracks
    with crossfading, gap minimization, and transcript synchronization.
    """

    def __init__(
        self,
        narration_service: Optional[NarrationService] = None,
        voice_director: Optional[VoiceDirector] = None,
        config: Optional[Any] = None,
    ):
        self.config = config or get_config()
        self.service = narration_service or NarrationService(config=self.config)
        self.director = voice_director or VoiceDirector()

    def _read_wav_numpy(self, wav_path: Path | str) -> Tuple[np.ndarray, int]:
        """Reads a WAV file into float32 numpy array and sample rate."""
        with wave.open(str(wav_path), "rb") as wf:
            channels = wf.getnchannels()
            sample_rate = wf.getframerate()
            sampwidth = wf.getsampwidth()
            n_frames = wf.getnframes()
            raw_bytes = wf.readframes(n_frames)

        if sampwidth == 2:  # 16-bit PCM
            data = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        elif sampwidth == 4:  # 32-bit float or int
            data = np.frombuffer(raw_bytes, dtype=np.float32)
        else:
            data = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0

        if channels > 1:
            data = data.reshape(-1, channels).mean(axis=1)

        return data, sample_rate

    def _write_wav_numpy(self, wav_path: Path | str, audio: np.ndarray, sample_rate: int) -> None:
        """Writes float32 numpy array to 16-bit mono PCM WAV."""
        # Clip to [-1.0, 1.0] to prevent clipping distortion
        clipped = np.clip(audio, -1.0, 1.0)
        pcm16 = (clipped * 32767.0).astype(np.int16)

        with wave.open(str(wav_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(pcm16.tobytes())

    def _trim_silence(self, audio: np.ndarray, threshold: float = 0.015) -> np.ndarray:
        """Trims leading and trailing silence beyond natural margins."""
        non_zero = np.where(np.abs(audio) > threshold)[0]
        if len(non_zero) == 0:
            return audio

        start_idx = max(0, non_zero[0] - 800)  # ~35ms head margin
        end_idx = min(len(audio), non_zero[-1] + 1200)  # ~50ms tail margin
        return audio[start_idx:end_idx]

    def _apply_crossfade(
        self,
        audio_a: np.ndarray,
        audio_b: np.ndarray,
        crossfade_samples: int,
    ) -> np.ndarray:
        """Applies gentle equal-power / linear crossfade between two audio buffers."""
        if crossfade_samples <= 0 or len(audio_a) < crossfade_samples or len(audio_b) < crossfade_samples:
            return np.concatenate([audio_a, audio_b])

        overlap_a = audio_a[-crossfade_samples:]
        overlap_b = audio_b[:crossfade_samples]

        t = np.linspace(0.0, 1.0, crossfade_samples, dtype=np.float32)
        fade_out = np.cos(t * (np.pi / 2.0))
        fade_in = np.sin(t * (np.pi / 2.0))

        blended = (overlap_a * fade_out) + (overlap_b * fade_in)
        return np.concatenate([audio_a[:-crossfade_samples], blended, audio_b[crossfade_samples:]])

    def render_directed_script(
        self,
        directed_script: DirectedScript,
        output_master_path: Path | str,
        voice_id: Optional[str] = None,
        engine: Optional[str] = None,
        crossfade_ms: int = 60,
    ) -> RenderedNarrationResult:
        """
        Renders all segments of a DirectedScript, seamlessly concatenates them
        with crossfades and natural cadence pauses, and generates a timing manifest.
        """
        master_p = Path(output_master_path)
        master_p.parent.mkdir(parents=True, exist_ok=True)
        seg_dir = master_p.parent / f"{master_p.stem}_segments"
        seg_dir.mkdir(parents=True, exist_ok=True)

        timings: List[SegmentTiming] = []
        assembled_audio = np.array([], dtype=np.float32)
        target_sample_rate = 24000
        current_time = 0.0
        engine_used_rec = "unknown"
        voice_used_rec = "unknown"

        logger.info(
            f"Rendering directed narration ({len(directed_script.segments)} segments, "
            f"Tone: {directed_script.tone.value}, Engine: {directed_script.target_engine})..."
        )

        for seg in directed_script.segments:
            seg_wav_name = f"seg_{seg.segment_index:03d}.wav"
            seg_wav_path = seg_dir / seg_wav_name

            # Synthesize segment speech
            res = self.service.synthesize_speech(
                text=seg.spoken_text,
                output_filename=str(seg_wav_path),
                voice_id=voice_id,
                engine=engine or directed_script.target_engine,
            )

            if not res["success"] or not seg_wav_path.exists():
                logger.error(f"Failed to render segment #{seg.segment_index}: {seg.spoken_text}")
                continue

            engine_used_rec = res.get("engine", engine_used_rec)
            voice_used_rec = res.get("voice", voice_used_rec)

            audio_data, sr = self._read_wav_numpy(seg_wav_path)
            target_sample_rate = sr

            # Trim excessive silence
            trimmed = self._trim_silence(audio_data)

            # Insert pause buffer after segment (based on tone cadence)
            pause_samples = int((seg.pause_after_ms / 1000.0) * target_sample_rate)
            pause_buf = np.zeros(pause_samples, dtype=np.float32)
            seg_with_pause = np.concatenate([trimmed, pause_buf])

            seg_duration = len(seg_with_pause) / float(target_sample_rate)

            # Record timing manifest entry
            timings.append(
                SegmentTiming(
                    segment_index=seg.segment_index,
                    text=seg.raw_text,
                    start_seconds=round(current_time, 3),
                    end_seconds=round(current_time + seg_duration, 3),
                    duration_seconds=round(seg_duration, 3),
                    audio_path=str(seg_wav_path),
                )
            )
            current_time += seg_duration

            # Stitch with previous audio
            if len(assembled_audio) == 0:
                assembled_audio = seg_with_pause
            else:
                cf_samples = int((crossfade_ms / 1000.0) * target_sample_rate)
                assembled_audio = self._apply_crossfade(assembled_audio, seg_with_pause, cf_samples)

        # Normalize final master audio to peak -1.0 dBFS
        peak = np.max(np.abs(assembled_audio)) if len(assembled_audio) > 0 else 1.0
        if peak > 0.001:
            target_peak = 0.89  # ~ -1.0 dBFS
            assembled_audio = (assembled_audio / peak) * target_peak

        # Write master WAV
        self._write_wav_numpy(master_p, assembled_audio, target_sample_rate)
        total_duration = len(assembled_audio) / float(target_sample_rate)

        # Write timing manifest JSON
        manifest_path = master_p.parent / f"{master_p.stem}_timing_manifest.json"
        res_obj = RenderedNarrationResult(
            master_audio_path=master_p,
            timing_manifest_path=manifest_path,
            total_duration_seconds=round(total_duration, 3),
            sample_rate=target_sample_rate,
            segment_count=len(timings),
            timings=timings,
            engine_used=engine_used_rec,
            voice_used=voice_used_rec,
        )

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(res_obj.to_dict(), f, indent=2)

        logger.info(
            f"Narration rendering complete: {master_p.name} ({total_duration:.2f}s, "
            f"{len(timings)} segments) | Manifest: {manifest_path.name}"
        )
        return res_obj

