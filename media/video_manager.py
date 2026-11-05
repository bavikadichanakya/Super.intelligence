import subprocess
import os
from pathlib import Path
from typing import Dict, Any, List

from core.logger import get_logger

logger = get_logger("VideoManager")

class VideoManager:
    """Creates cinematic motion video clips (Ken Burns effect) from editorial image cards."""

    @staticmethod
    def create_motion_clip(image_path: str, output_clip_path: str, duration: float, motion_style: str = "zoom_in") -> bool:
        """
        Render a smooth 1080x1920 30FPS MP4 video clip with subtle motion from a static graphic card.
        Optimized for low RAM using veryfast preset.
        """
        Path(output_clip_path).parent.mkdir(parents=True, exist_ok=True)
        total_frames = int(duration * 30)

        # Subtle zoom rate calculation
        if motion_style == "zoom_in":
            vf = f"zoompan=z='min(zoom+0.0006,1.06)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        elif motion_style == "pan_left":
            vf = f"zoompan=z=1.04:d={total_frames}:x='if(lte(on,1),(iw-iw/zoom)/2,x-0.4)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        elif motion_style == "pan_right":
            vf = f"zoompan=z=1.04:d={total_frames}:x='if(lte(on,1),0,x+0.4)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        else:
            vf = f"zoompan=z='min(zoom+0.0005,1.05)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"

        cmd = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", str(image_path),
            "-vf", vf,
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            str(output_clip_path)
        ]

        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return os.path.exists(output_clip_path) and os.path.getsize(output_clip_path) > 1000
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create motion clip {output_clip_path}: {e.stderr.decode('utf-8', errors='ignore')}")
            return False
