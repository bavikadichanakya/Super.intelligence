"""
SUPER.INTELLIGENCEEE — Transitions: Transition Router
Applies cinematic FFmpeg xfade transitions (wipeleft, wiperight, dissolve, fade)
between documentary scene clips to maintain broadcast visual momentum.
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger("super_intelligence.transition_router")


class TransitionRouter:
    """Manages cinematic transition routing and seamless video concatenation."""

    def __init__(self, ffmpeg_cmd: str = "ffmpeg"):
        self.ffmpeg_cmd = ffmpeg_cmd

    def concat_clips(
        self,
        clip_paths: List[Path],
        output_path: Path | str,
        transition_type: str = "fade",
        transition_duration: float = 0.35,
    ) -> Path:
        """
        Concatenates video clips into a continuous MP4.
        Applies fast concat demuxer or FFmpeg xfade transition filter between consecutive clips.
        """
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        valid_clips = [Path(p).resolve() for p in clip_paths if Path(p).exists() and Path(p).stat().st_size > 1000]
        if not valid_clips:
            raise ValueError("No valid video clips provided for concatenation.")

        if len(valid_clips) == 1:
            import shutil
            shutil.copy2(valid_clips[0], out_p)
            return out_p

        # Attempt xfade transition pipeline if clip count <= 8 (optimal RAM/CPU efficiency)
        if len(valid_clips) <= 8 and transition_duration > 0.05:
            try:
                return self._concat_with_xfade(valid_clips, out_p, transition_type, transition_duration)
            except Exception as e:
                logger.warning(f"xfade transition warning ({e}). Falling back to fast concat demuxer...")

        return self._concat_fast_demuxer(valid_clips, out_p)

    def _concat_with_xfade(
        self,
        clips: List[Path],
        output_path: Path,
        transition_type: str = "fade",
        trans_dur: float = 0.35,
    ) -> Path:
        """Chains multiple inputs using FFmpeg xfade filter."""
        # Get durations of all clips via ffprobe
        durations = []
        for c in clips:
            cmd_dur = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(c),
            ]
            res = subprocess.run(cmd_dur, capture_output=True, text=True, check=True)
            durations.append(float(res.stdout.strip()))

        # Build FFmpeg command with filter_complex xfade chain
        cmd = [self.ffmpeg_cmd, "-y"]
        for c in clips:
            cmd.extend(["-i", str(c)])

        filter_parts = []
        current_offset = durations[0] - trans_dur
        prev_label = "[0:v]"

        # Available xfade transitions: wipeleft, wiperight, dissolve, fade, circleopen, smoothleft
        allowed_transitions = ["wipeleft", "wiperight", "dissolve", "fade", "circleopen", "smoothleft"]
        chosen_trans = transition_type if transition_type in allowed_transitions else "wipeleft"

        for i in range(1, len(clips)):
            next_in = f"[{i}:v]"
            out_label = f"[v{i}]" if i < len(clips) - 1 else "[vfinal]"
            filter_parts.append(
                f"{prev_label}{next_in}xfade=transition={chosen_trans}:duration={trans_dur:.2f}:offset={current_offset:.2f}{out_label}"
            )
            prev_label = out_label
            if i < len(clips) - 1:
                current_offset += durations[i] - trans_dur

        filter_str = ";".join(filter_parts)
        cmd.extend([
            "-filter_complex", filter_str,
            "-map", "[vfinal]",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output_path),
        ])

        logger.info(f"Applying xfade ({chosen_trans}, {trans_dur:.2f}s) across {len(clips)} scenes...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and output_path.exists() and output_path.stat().st_size > 10000:
            return output_path
        raise RuntimeError(f"xfade failed: {res.stderr[:300]}")

    def _concat_fast_demuxer(self, clips: List[Path], output_path: Path) -> Path:
        """Fast and reliable FFmpeg concat demuxer."""
        concat_txt = output_path.parent / f"concat_{output_path.stem}.txt"
        with open(concat_txt, "w", encoding="utf-8") as f:
            for c in clips:
                c_str = str(c.resolve()).replace("\\", "/")
                f.write(f"file '{c_str}'\n")

        cmd = [
            self.ffmpeg_cmd, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_txt.resolve()),
            "-c", "copy",
            str(output_path),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if concat_txt.exists():
            concat_txt.unlink(missing_ok=True)

        if res.returncode != 0 or not output_path.exists() or output_path.stat().st_size < 1000:
            raise RuntimeError(f"Concat demuxer failed: {res.stderr[:300]}")

        return output_path
