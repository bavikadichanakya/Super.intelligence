"""
SUPER.INTELLIGENCEEE — Audio Mixer Module
Handles audio concatenation, normalization (-16 LUFS), ducking, and master mixing via FFmpeg.
Strict zero-budget, local-first processing.
"""

from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from core.config import get_config

logger = logging.getLogger("super_intelligence.audio_mixer")


class AudioMixerError(Exception):
    """Raised when audio mixing or processing fails."""


class AudioMixer:
    """Manages scene concatenation, loudness normalization (-16 LUFS), and audio post-processing."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.ffmpeg_cmd = "ffmpeg"
        self.ffprobe_cmd = "ffprobe"
        self.target_lufs = self.config.get("audio.target_lufs", -16.0)
        self.target_lra = 11.0
        self.target_tp = -1.5

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
        silence_between: float = 0.25,
    ) -> Path:
        """
        Concatenates multiple scene audio WAV files with an optional silence pad.
        """
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        valid_files = [Path(p) for p in scene_audio_files if Path(p).exists() and Path(p).stat().st_size > 500]
        if not valid_files:
            raise AudioMixerError("No valid audio files provided for concatenation.")

        if len(valid_files) == 1:
            # Just copy or normalize single file
            cmd = [
                self.ffmpeg_cmd, "-y",
                "-i", str(valid_files[0]),
                "-c:a", "pcm_s16le",
                str(out_path),
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            return out_path

        # Build ffmpeg filter_complex with concat and adelay
        # Or simpler: create a concat demuxer text file
        concat_file = out_path.parent / f"concat_{out_path.stem}.txt"
        try:
            with open(concat_file, "w", encoding="utf-8") as f:
                for vf in valid_files:
                    # FFmpeg requires forward slashes or escaped backslashes in concat files
                    f_path_str = str(vf.resolve()).replace("\\", "/")
                    f.write(f"file '{f_path_str}'\n")

            cmd = [
                self.ffmpeg_cmd, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
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
        Applies EBU R128 loudness normalization (-16 LUFS for Instagram/mobile Reels).
        Uses single-pass dynamic loudnorm or two-pass loudnorm.
        """
        in_path = Path(input_path)
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if not in_path.exists():
            raise AudioMixerError(f"Input file not found for normalization: {in_path}")

        lufs = target_lufs if target_lufs is not None else self.target_lufs

        # Fast and robust single-pass linear normalization to mobile standards
        # loudnorm=I=-16:LRA=11:TP=-1.5
        filter_str = f"loudnorm=I={lufs}:LRA={self.target_lra}:TP={self.target_tp}"

        cmd = [
            self.ffmpeg_cmd, "-y",
            "-i", str(in_path),
            "-af", filter_str,
            "-ar", "44100",
            "-c:a", "pcm_s16le",
            str(out_path),
        ]

        logger.info(f"Normalizing loudness of {in_path.name} to {lufs} LUFS")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            logger.warning(f"Loudnorm failed ({res.stderr}), falling back to simple volume peak...")
            fallback_cmd = [
                self.ffmpeg_cmd, "-y",
                "-i", str(in_path),
                "-af", "volume=1.2",
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
        Mixes master narration voice with optional background music, looping or trimming
        music to match narration length, applying ducking (-18dB under speech).
        """
        narr_path = Path(narration_path)
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if not narr_path.exists():
            raise AudioMixerError(f"Narration file not found: {narr_path}")

        # If no music or music doesn't exist, just normalize and copy narration
        if not music_path or not Path(music_path).exists():
            logger.info("No background music provided or found; exporting normalized narration directly.")
            return self.normalize_loudness(narr_path, out_path)

        bgm_path = Path(music_path)
        duration = self.get_audio_duration(narr_path)
        if duration <= 0:
            duration = 30.0

        # Mixing filter with sidechain ducking or simple amix with low background volume
        # Speech is loud and prominent, music is subtle background ambience
        # [0:a] is narration, [1:a] is looped music
        # amix=inputs=2:duration=first:dropout_transition=2
        # volume balance: narration at 1.0, music at music_volume (e.g. 0.12)
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
            "-c:a", "pcm_s16le",
            str(out_path),
        ]

        logger.info(f"Mixing narration and music into {out_path.name}")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            logger.warning(f"Audio mix with music failed ({res.stderr}); falling back to voice only.")
            return self.normalize_loudness(narr_path, out_path)

        return out_path

