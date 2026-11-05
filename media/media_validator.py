import os
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, Tuple
from PIL import Image

from core.logger import get_logger

logger = get_logger("MediaValidator")

class MediaValidator:
    """Verifies image and video dimensions, aspect ratios, and format standards."""

    TARGET_WIDTH = 1080
    TARGET_HEIGHT = 1920
    TARGET_ASPECT = 9 / 16  # 0.5625

    @classmethod
    def validate_image(cls, file_path: str) -> Tuple[bool, str, Dict[str, Any]]:
        p = Path(file_path)
        if not p.exists():
            return False, f"File does not exist: {file_path}", {}

        try:
            with Image.open(p) as img:
                w, h = img.size
                format_name = img.format
                aspect = round(w / h, 4)
                
                # Check for standard 9:16 or acceptable vertical resolution
                is_vertical = h >= w
                matches_target = (w == cls.TARGET_WIDTH and h == cls.TARGET_HEIGHT)

                meta = {
                    "width": w,
                    "height": h,
                    "aspect_ratio": aspect,
                    "format": format_name,
                    "is_exact_9_16": matches_target,
                    "is_vertical": is_vertical
                }

                if not is_vertical:
                    return False, f"Image {p.name} is horizontal ({w}x{h}). Vertical (9:16) required.", meta

                return True, "Valid vertical image", meta
        except Exception as e:
            return False, f"Corrupted or invalid image: {e}", {}

    @classmethod
    def validate_video(cls, file_path: str) -> Tuple[bool, str, Dict[str, Any]]:
        p = Path(file_path)
        if not p.exists():
            return False, f"Video does not exist: {file_path}", {}

        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "stream=width,height,codec_name,r_frame_rate,duration:format=duration,size,bit_rate",
            "-of", "json",
            str(p)
        ]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            data = json.loads(res.stdout)
            streams = data.get("streams", [])
            video_stream = next((s for s in streams if s.get("width")), None)

            if not video_stream:
                return False, "No valid video stream detected", {}

            w = int(video_stream.get("width", 0))
            h = int(video_stream.get("height", 0))
            duration = float(data.get("format", {}).get("duration", 0.0))
            size_mb = round(int(data.get("format", {}).get("size", 0)) / (1024 * 1024), 2)
            codec = video_stream.get("codec_name", "")

            meta = {
                "width": w,
                "height": h,
                "duration": duration,
                "size_mb": size_mb,
                "codec": codec,
                "is_1080x1920": (w == 1080 and h == 1920)
            }

            if duration < 5.0:
                return False, f"Video duration too short ({duration}s).", meta

            return True, "Video verified", meta
        except Exception as e:
            return False, f"FFprobe analysis failed: {e}", {}
