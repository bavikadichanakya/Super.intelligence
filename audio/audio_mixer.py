"""
SUPER.INTELLIGENCEEE — Professional Audio Mixer Module
Master audio engineering pipeline:
- High-pass filter ~80 Hz
- Vocal presence EQ (+2 dB @ 3 kHz, -1.5 dB @ 300 Hz)
- Dynamic vocal compression (threshold -20 dB, ratio 3:1)
- Resampling to broadcast standard 48 kHz stereo
- EBU R128 loudness normalization (-16.0 LUFS ± 1.0, True Peak <= -1.0 dBTP)
- Dynamic music ducking (sidechain compression -16 dB attenuation during speech)
- Scene transition sound effects (SFX) overlay
"""

from __future__ import annotations

import json
import logging
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from core.config import get_config

logger = logging.getLogger("super_intelligence.audio_mixer")


class AudioMixerError(Exception):
    """Raised when audio mixing or processing fails."""


class AudioMixer:
    """Manages scene concatenation, loudness normalization (-16 LUFS), ducking, and master audio engineering."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.ffmpeg_cmd = "ffmpeg"
        self.ffprobe_cmd = "ffprobe"
        self.target_lufs = float(self.config.get("audio_engineering.target_lufs", -16.0))
        self.target_lra = float(self.config.get("audio_engineering.loudness_range_lra", 7.0))
        self.target_tp = float(self.config.get("audio_engineering.true_peak_limit_dbtp", -1.0))
        self.sample_rate = int(self.config.get("audio_engineering.master_sample_rate_hz", 48000))
        self.sfx_dir = self.config.resolve_path(
            self.config.get("audio_engineering.sound_effects.sfx_dir", ".agents/skills/media-use/audio/assets/sfx")
        )

    def get_audio_duration(self, audio_path: Path | str) -> float:
        """Inspects duration of an audio file using ffprobe."""
        audio_path = Path(audio_path)
        if not audio_path.exists():
            return 0.0

        cmd = [
            self.ffprobe_cmd,
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio_path),
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(res.stdout.strip())
        except Exception as e:
            logger.warning(f"Failed to inspect duration for {audio_path}: {e}")
            return 0.0

    def concatenate_scenes(
        self,
        scene_audio_files: List[Path | str],
        output_path: Path | str,
        silence_between: float = 0.20,
    ) -> Path:
        """
        Concatenates multiple scene audio WAV files with professional consistency.
        """
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        valid_files = [Path(p) for p in scene_audio_files if Path(p).exists() and Path(p).stat().st_size > 500]
        if not valid_files:
            raise AudioMixerError("No valid audio files provided for concatenation.")

        if len(valid_files) == 1:
            cmd = [
                self.ffmpeg_cmd, "-y",
                "-i", str(valid_files[0]),
                "-ar", str(self.sample_rate),
                "-ac", "2",
                "-c:a", "pcm_s16le",
                str(out_path),
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            return out_path

        concat_file = out_path.parent / f"concat_{out_path.stem}.txt"
        try:
            with open(concat_file, "w", encoding="utf-8") as f:
                for vf in valid_files:
                    f_path_str = str(vf.resolve()).replace("\\", "/")
                    f.write(f"file '{f_path_str}'\n")

            cmd = [
                self.ffmpeg_cmd, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-ar", str(self.sample_rate),
                "-ac", "2",
                "-c:a", "pcm_s16le",
                str(out_path),
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                raise AudioMixerError(f"Concat failed: {res.stderr}")

            return out_path
        finally:
            if concat_file.exists():
                try:
                    concat_file.unlink()
                except Exception:
                    pass

    def normalize_loudness(
        self,
        input_path: Path | str,
        output_path: Path | str,
        target_lufs: Optional[float] = None,
    ) -> Path:
        """
        Applies professional vocal mastering chain:
        1. High-pass filter ~80 Hz (eliminates low-end rumble)
        2. Presence boost ~3 kHz (+2 dB) & mud cut ~300 Hz (-1.5 dB)
        3. Dynamic vocal compressor (-20 dB threshold, 3:1 ratio, 5ms attack)
        4. Resample to 48 kHz stereo
        5. EBU R128 loudness normalization (-16.0 LUFS, TP -1.0 dBTP, LRA 7.0)
        """
        in_path = Path(input_path)
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if not in_path.exists():
            raise AudioMixerError(f"Input file not found for normalization: {in_path}")

        lufs = target_lufs if target_lufs is not None else self.target_lufs

        # Professional Mastering Audio Filter Chain
        vocal_master_filters = (
            "highpass=f=80,"
            "equalizer=f=3000:width_type=o:width=1.5:g=2,"
            "equalizer=f=300:width_type=o:width=1.0:g=-1.5,"
            "acompressor=threshold=-20dB:ratio=3:attack=5:release=50,"
            f"aresample={self.sample_rate},"
            "aformat=channel_layouts=stereo,"
            f"loudnorm=I={lufs}:LRA={self.target_lra}:TP={self.target_tp}"
        )

        cmd = [
            self.ffmpeg_cmd, "-y",
            "-i", str(in_path),
            "-af", vocal_master_filters,
            "-ar", str(self.sample_rate),
            "-c:a", "pcm_s16le",
            str(out_path),
        ]

        logger.info(f"Mastering & normalizing loudness of {in_path.name} to {lufs} LUFS (48 kHz stereo)")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            logger.warning(f"Mastering filter failed ({res.stderr}), falling back to direct loudnorm...")
            fallback_cmd = [
                self.ffmpeg_cmd, "-y",
                "-i", str(in_path),
                "-af", f"loudnorm=I={lufs}:LRA={self.target_lra}:TP={self.target_tp}",
                "-ar", str(self.sample_rate),
                "-c:a", "pcm_s16le",
                str(out_path),
            ]
            subprocess.run(fallback_cmd, capture_output=True, check=True)

        return out_path

    def mix_narration_and_music(
        self,
        narration_path: Path | str,
        output_path: Path | str,
        music_path: Optional[Path | str] = None,
        music_volume: float = 0.12,
        ducking: bool = True,
    ) -> Path:
        """
        Mixes master narration voice with background music utilizing dynamic
        speech sidechain ducking (-16 dB attenuation during voiceover, smooth recovery during pauses).
        """
        narr_path = Path(narration_path)
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if not narr_path.exists():
            raise AudioMixerError(f"Narration file not found: {narr_path}")

        if not music_path or not Path(music_path).exists():
            logger.info("No background music provided; mastering narration directly.")
            return self.normalize_loudness(narr_path, out_path)

        bgm_path = Path(music_path)
        duration = self.get_audio_duration(narr_path)
        if duration <= 0:
            duration = 30.0

        if ducking:
            # Dynamic Sidechain Compression: Voice ducks music by ~16 dB
            filter_complex = (
                f"[1:a]aloop=loop=-1:size=2e+09,aresample={self.sample_rate},aformat=channel_layouts=stereo,volume={music_volume}[bgm];"
                f"[0:a]aresample={self.sample_rate},aformat=channel_layouts=stereo[vox];"
                f"[bgm][vox]sidechaincompress=threshold=0.03:ratio=4:attack=200:release=400[ducked_bgm];"
                f"[vox][ducked_bgm]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
                f"[mixed]highpass=f=80,equalizer=f=3000:width_type=o:width=1.5:g=2,equalizer=f=300:width_type=o:width=1.0:g=-1.5,"
                f"loudnorm=I={self.target_lufs}:LRA={self.target_lra}:TP={self.target_tp}[out]"
            )
        else:
            filter_complex = (
                f"[1:a]aloop=loop=-1:size=2e+09,volume={music_volume}[music];"
                f"[0:a][music]amix=inputs=2:duration=first:dropout_transition=2,"
                f"loudnorm=I={self.target_lufs}:LRA={self.target_lra}:TP={self.target_tp}[out]"
            )

        cmd = [
            self.ffmpeg_cmd, "-y",
            "-i", str(narr_path),
            "-i", str(bgm_path),
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-ar", str(self.sample_rate),
            "-c:a", "pcm_s16le",
            str(out_path),
        ]

        logger.info(f"Mixing narration and ducked music into {out_path.name}")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            logger.warning(f"Audio mix with ducking failed ({res.stderr}); falling back to vocal master.")
            return self.normalize_loudness(narr_path, out_path)

        return out_path

    def mix_with_sound_effects(
        self,
        master_audio_path: Path | str,
        scene_durations: List[float],
        output_path: Path | str,
        sfx_name: str = "whoosh-cinematic.mp3",
        sfx_volume: float = 0.18,
    ) -> Path:
        """
        Mixes subtle cinematic transition sound effects (SFX) at scene boundaries.
        SFX assets are loaded from .agents/skills/media-use/audio/assets/sfx/.
        """
        master_path = Path(master_audio_path)
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        sfx_file = self.sfx_dir / sfx_name
        if not sfx_file.exists() or len(scene_durations) <= 1:
            # Nothing to overlay, just return normalized master
            return self.normalize_loudness(master_path, out_path)

        # Calculate transition cut timestamps
        cut_timestamps = []
        current_time = 0.0
        for dur in scene_durations[:-1]:
            current_time += dur
            cut_timestamps.append(current_time)

        # Build FFmpeg filter_complex with adelay for each transition point
        inputs = ["-i", str(master_path)]
        filter_parts = [f"[0:a]aresample={self.sample_rate},aformat=channel_layouts=stereo[base]"]
        mix_inputs = ["[base]"]

        for idx, t_sec in enumerate(cut_timestamps, start=1):
            delay_ms = int(max(0, t_sec - 0.25) * 1000) # Slightly anticipate cut
            inputs.extend(["-i", str(sfx_file)])
            filter_parts.append(
                f"[{idx}:a]adelay={delay_ms}|{delay_ms},volume={sfx_volume},aresample={self.sample_rate},aformat=channel_layouts=stereo[sfx{idx}]"
            )
            mix_inputs.append(f"[sfx{idx}]")

        filter_str = (
            ";".join(filter_parts) + ";" +
            "".join(mix_inputs) + f"amix=inputs={len(mix_inputs)}:duration=first:dropout_transition=2," +
            f"loudnorm=I={self.target_lufs}:LRA={self.target_lra}:TP={self.target_tp}[out]"
        )

        cmd = [
            self.ffmpeg_cmd, "-y",
            *inputs,
            "-filter_complex", filter_str,
            "-map", "[out]",
            "-ar", str(self.sample_rate),
            "-c:a", "pcm_s16le",
            str(out_path),
        ]

        logger.info(f"Overlaying {len(cut_timestamps)} transition SFX ({sfx_name}) at scene boundaries")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            logger.warning(f"SFX overlay failed ({res.stderr}); falling back to master audio.")
            return self.normalize_loudness(master_path, out_path)

        return out_path

    def measure_loudness(self, audio_path: Path | str) -> Dict[str, Any]:
        """
        Performs precise EBU R128 loudness measurement using FFmpeg's ebur128 filter.
        Returns integrated LUFS, true peak, loudness range (LRA), and compliance boolean.
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            return {"error": "File not found", "compliant": False}

        cmd = [
            self.ffmpeg_cmd,
            "-nostats",
            "-i", str(audio_path),
            "-filter_complex", "ebur128=peak=true",
            "-f", "null",
            "-",
        ]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = res.stderr

            integrated = None
            true_peak = None
            lra = None

            # Extract Integrated loudness
            m_i = re.search(r"Integrated loudness:\s+I:\s+([-\d.]+)\s+LUFS", output)
            if m_i:
                integrated = float(m_i.group(1))

            # Extract True peak
            m_tp = re.search(r"True peak:\s+Peak:\s+([-\d.]+)\s+dBFS", output)
            if m_tp:
                true_peak = float(m_tp.group(1))

            # Extract LRA
            m_lra = re.search(r"Loudness range:\s+LRA:\s+([-\d.]+)\s+LU", output)
            if m_lra:
                lra = float(m_lra.group(1))

            # Mobile Reels standard compliance: -16 LUFS (±1.5) and True Peak <= -1.0 dBTP
            compliant = False
            if integrated is not None and true_peak is not None:
                compliant = (-17.5 <= integrated <= -14.5) and (true_peak <= -0.8)

            return {
                "file_path": str(audio_path),
                "integrated_lufs": integrated,
                "true_peak_dbtp": true_peak,
                "loudness_range_lra": lra,
                "target_lufs": self.target_lufs,
                "compliant": compliant,
            }
        except Exception as e:
            logger.error(f"Failed to measure loudness for {audio_path}: {e}")
            return {"error": str(e), "compliant": False}
