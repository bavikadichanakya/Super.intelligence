import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

from core.logger import get_logger

logger = get_logger("AudioProcessor")

class AudioProcessor:
    """Manages audio normalization, FFprobe duration metrics, and audio concatenation."""

    @staticmethod
    def get_audio_info(audio_path: str) -> Dict[str, Any]:
        """Extract duration and audio properties using ffprobe."""
        if not os.path.exists(audio_path):
            return {"duration": 0.0, "format": "none", "bitrate": 0}
        
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration,bit_rate:stream=sample_rate,channels",
            "-of", "json",
            str(audio_path)
        ]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            data = json.loads(res.stdout)
            duration = float(data.get("format", {}).get("duration", 0.0))
            bitrate = int(data.get("format", {}).get("bit_rate", 0))
            return {
                "duration": duration,
                "bitrate": bitrate,
                "valid": duration > 0.1
            }
        except Exception as e:
            logger.error(f"FFprobe audio inspection failed for {audio_path}: {e}")
            return {"duration": 0.0, "bitrate": 0, "valid": False}

    @staticmethod
    def normalize_loudness(input_path: str, output_path: str, target_lufs: float = -16.0) -> bool:
        """Normalize audio loudness to mobile social standard (-16 LUFS) via FFmpeg loudnorm filter."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(input_path),
            "-af", f"loudnorm=I={target_lufs}:LRA=11:TP=-1.5",
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            str(output_path)
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return os.path.exists(output_path) and os.path.getsize(output_path) > 100
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg audio normalization failed: {e.stderr.decode('utf-8', errors='ignore')}")
            return False

    @staticmethod
    def mix_background_music(voice_path: str, music_path: str, output_path: str, music_volume: float = 0.08) -> bool:
        """Mix ducked background ambient audio under primary voiceover."""
        if not os.path.exists(music_path):
            # If no music exists, copy or convert voice directly
            return AudioProcessor.normalize_loudness(voice_path, output_path)

        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(voice_path),
            "-stream_loop", "-1",
            "-i", str(music_path),
            "-filter_complex",
            f"[1:a]volume={music_volume}[music];[0:a][music]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "[aout]",
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            str(output_path)
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return os.path.exists(output_path) and os.path.getsize(output_path) > 100
        except Exception as e:
            logger.warning(f"Background music mix failed, falling back to clean voiceover: {e}")
            return AudioProcessor.normalize_loudness(voice_path, output_path)
