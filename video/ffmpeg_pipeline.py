"""
SUPER.INTELLIGENCEEE — FFmpeg Video Pipeline Module
Handles muxing, subtitle burning (libass), encoding (H.264 / AAC), and final MP4 export.
Strict zero-budget processing with full Windows compatibility.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import get_config

logger = logging.getLogger("super_intelligence.ffmpeg_pipeline")


class FFmpegPipelineError(Exception):
    """Raised when FFmpeg post-processing fails."""


class FFmpegVideoPipeline:
    """Post-processes rendered video: audio muxing, subtitle overlay, H.264/AAC encoding."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.ffmpeg_cmd = "ffmpeg"
        self.ffprobe_cmd = "ffprobe"

    def compose_final_reel(
        self,
        video_input: Path | str,
        audio_input: Path | str,
        output_path: Path | str,
        captions_ass: Optional[Path | str] = None,
        burn_captions: bool = True,
    ) -> Path:
        """
        Combines visual track with master audio, optionally burns yellow punch captions,
        and encodes to high-quality Instagram standard MP4.
        """
        v_in = Path(video_input).resolve()
        a_in = Path(audio_input).resolve()
        out_path = Path(output_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if not v_in.exists():
            raise FFmpegPipelineError(f"Video input does not exist: {v_in}")
        if not a_in.exists():
            raise FFmpegPipelineError(f"Audio input does not exist: {a_in}")

        cmd = [
            self.ffmpeg_cmd, "-y",
            "-i", str(v_in),
            "-i", str(a_in),
        ]

        # Handle subtitle burning via libass
        vf_filters = []
        ass_temp = None

        if burn_captions and captions_ass and Path(captions_ass).exists():
            ass_path = Path(captions_ass).resolve()
            # Windows FFmpeg subtitle filter escaping workaround:
            # Copy ASS to out_path.parent so it's a relative simple name
            ass_temp = out_path.parent / f"temp_{ass_path.name}"
            shutil.copyfile(ass_path, ass_temp)
            # Use forward slashes and escape colon
            escaped_ass = str(ass_temp).replace("\\", "/").replace(":", "\\:")
            vf_filters.append(f"ass='{escaped_ass}'")

        if vf_filters:
            cmd.extend(["-vf", ",".join(vf_filters)])

        cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "medium",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            "-shortest",
            str(out_path),
        ])

        logger.info(f"Encoding final Reel to {out_path.name}...")
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                logger.warning(f"FFmpeg mux with subtitles failed: {res.stderr[:300]}. Retrying without subtitle filter...")
                # Fallback: simple mux without subtitle filter
                fallback_cmd = [
                    self.ffmpeg_cmd, "-y",
                    "-i", str(v_in),
                    "-i", str(a_in),
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-shortest",
                    str(out_path),
                ]
                f_res = subprocess.run(fallback_cmd, capture_output=True, text=True)
                if f_res.returncode != 0:
                    raise FFmpegPipelineError(f"FFmpeg final mux failed: {f_res.stderr}")

            logger.info(f"Final Reel exported successfully: {out_path.name} ({out_path.stat().st_size} bytes)")
            return out_path
        finally:
            if ass_temp and ass_temp.exists():
                try:
                    ass_temp.unlink()
                except Exception:
                    pass

