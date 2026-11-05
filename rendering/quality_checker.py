import subprocess
import json
from pathlib import Path
from typing import Dict, Any, Tuple

from core.logger import get_logger

logger = get_logger("QualityChecker")

class QualityChecker:
    """Verifies rendered MP4 video compliance with Instagram specifications."""

    @classmethod
    def verify_video(cls, video_path: str) -> Tuple[bool, str, Dict[str, Any]]:
        p = Path(video_path)
        if not p.exists() or p.stat().st_size < 1000:
            return False, f"File does not exist or is empty: {video_path}", {}

        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "stream=width,height,codec_name,r_frame_rate,duration,pix_fmt:format=duration,size,bit_rate",
            "-of", "json",
            str(p)
        ]

        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            data = json.loads(res.stdout)
            streams = data.get("streams", [])
            format_info = data.get("format", {})

            v_stream = next((s for s in streams if s.get("width")), None)
            a_stream = next((s for s in streams if s.get("codec_name") in ("aac", "mp3")), None)

            if not v_stream:
                return False, "Missing video stream", {}

            width = int(v_stream.get("width", 0))
            height = int(v_stream.get("height", 0))
            v_codec = v_stream.get("codec_name", "")
            pix_fmt = v_stream.get("pix_fmt", "")
            duration = float(format_info.get("duration", 0.0))
            size_mb = round(int(format_info.get("size", 0)) / (1024 * 1024), 2)

            meta = {
                "width": width,
                "height": height,
                "video_codec": v_codec,
                "pixel_format": pix_fmt,
                "audio_stream_present": a_stream is not None,
                "duration_seconds": duration,
                "file_size_mb": size_mb,
                "is_1080x1920": (width == 1080 and height == 1920),
                "is_h264": ("h264" in v_codec.lower()),
                "is_yuv420p": ("yuv420p" in pix_fmt.lower())
            }

            if width != 1080 or height != 1920:
                return False, f"Non-compliant dimensions: {width}x{height} (must be 1080x1920)", meta

            if not meta["is_h264"]:
                return False, f"Video codec is {v_codec} (must be H.264)", meta

            if duration < 10.0:
                return False, f"Duration is too short ({duration:.1f}s)", meta

            if duration > 90.0:
                return False, f"Duration exceeds Instagram Reel limits ({duration:.1f}s)", meta

            logger.info(f"Quality check passed for {p.name}: {width}x{height}, {duration:.1f}s, {size_mb}MB, codec={v_codec}")
            return True, "Quality verification PASSED", meta
        except Exception as e:
            logger.error(f"FFprobe check exception for {video_path}: {e}")
            return False, f"FFprobe error: {e}", {}
