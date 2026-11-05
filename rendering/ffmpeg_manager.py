import subprocess
import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

from core.logger import get_logger, get_system_resources
from core.config_manager import get_config

logger = get_logger("FFmpegManager")

class FFmpegManager:
    """Safely executes FFmpeg and FFprobe processes with memory monitoring and cleanup."""

    def __init__(self):
        self.config = get_config()
        self.preset = self.config.get("rendering.ffmpeg_preset", "veryfast")
        self.cleanup = self.config.get("rendering.cleanup_temp_files", True)

    @staticmethod
    def run_command(cmd: List[str], timeout_sec: int = 300) -> (bool, str):
        """Run an FFmpeg command with memory tracking and timeout protection."""
        logger.debug(f"Executing FFmpeg: {' '.join(cmd)}")
        res_before = get_system_resources()
        start_time = time.time()

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            stdout, stderr = process.communicate(timeout=timeout_sec)
            elapsed = round(time.time() - start_time, 2)
            res_after = get_system_resources()

            if process.returncode != 0:
                logger.error(f"FFmpeg exited with error code {process.returncode}: {stderr[-800:]}")
                return False, stderr

            logger.info(f"FFmpeg command finished in {elapsed}s (RAM: {res_after['ram_process_mb']}MB, CPU: {res_after['cpu_percent']}%)")
            return True, stdout
        except subprocess.TimeoutExpired:
            process.kill()
            logger.error(f"FFmpeg process timed out after {timeout_sec}s")
            return False, f"Timeout after {timeout_sec}s"
        except Exception as e:
            logger.error(f"FFmpeg execution failed: {e}")
            return False, str(e)

    @staticmethod
    def cleanup_files(file_paths: List[str]):
        """Remove temporary intermediate clips and files."""
        for p in file_paths:
            try:
                path_obj = Path(p)
                if path_obj.exists() and path_obj.is_file():
                    path_obj.unlink()
            except Exception as e:
                logger.warning(f"Could not remove temporary file {p}: {e}")
