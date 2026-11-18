"""
SUPER.INTELLIGENCEEE — Phase 4.3.1 Resource Guard & Process Isolation
Enforces strict sequential rendering, RAM/disk safety thresholds, process timeouts,
and Windows-safe child process termination.
"""

from __future__ import annotations

import gc
import logging
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import psutil

logger = logging.getLogger("super_intelligence.resource_guard")


class ResourceThresholdError(Exception):
    """Raised when memory or disk headroom is below safe thresholds."""
    pass


class RenderProcessTimeoutError(Exception):
    """Raised when a rendering child process exceeds its allocated timeout."""
    pass


class ResourceGuard:
    """
    Guarantees hardware and memory safety for multi-engine rendering on 8 GB RAM workstations.
    """

    MIN_FREE_DISK_GB = 2.0
    MIN_FREE_RAM_MB = 200.0
    DEFAULT_TIMEOUT_SEC = 360.0

    def __init__(self, workspace_root: Optional[Path | str] = None):
        self.workspace_root = Path(workspace_root or "A:/SUPER.INTELLIGENCEEE").resolve()
        self.temp_dir = self.workspace_root / ".temp"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def configure_environment(self) -> Dict[str, str]:
        """
        Forces all child runtimes (Node, Chrome, FFmpeg, Python) to write scratch data to Drive A: .temp.
        """
        env = dict(os.environ)
        temp_str = str(self.temp_dir.resolve())
        env["TEMP"] = temp_str
        env["TMP"] = temp_str
        env["HYPERFRAMES_EXTRACT_CACHE_DIR"] = temp_str
        env["NODE_OPTIONS"] = "--max-old-space-size=2048"
        env["PRODUCER_LOW_MEMORY_MODE"] = "false"
        return env

    def check_preflight_safety(self) -> Dict[str, Any]:
        """
        Verifies that disk and memory thresholds are satisfied before launching an engine.
        """
        # Disk Check on A:
        disk_usage = psutil.disk_usage(str(self.temp_dir))
        free_disk_gb = disk_usage.free / (1024**3)
        if free_disk_gb < self.MIN_FREE_DISK_GB:
            raise ResourceThresholdError(
                f"Insufficient disk space on {self.temp_dir}: {free_disk_gb:.2f} GB free "
                f"(Minimum required: {self.MIN_FREE_DISK_GB} GB)."
            )

        # RAM Check
        mem = psutil.virtual_memory()
        available_ram_mb = mem.available / (1024**2)
        if available_ram_mb < self.MIN_FREE_RAM_MB:
            logger.warning(
                f"High memory pressure: {available_ram_mb:.1f} MB available (Minimum: {self.MIN_FREE_RAM_MB} MB). "
                "Triggering garbage collection before execution."
            )
            gc.collect()
            time.sleep(1.0)
            mem = psutil.virtual_memory()
            available_ram_mb = mem.available / (1024**2)
            if available_ram_mb < self.MIN_FREE_RAM_MB:
                raise ResourceThresholdError(
                    f"Memory starvation: Only {available_ram_mb:.1f} MB RAM available. "
                    f"Threshold of {self.MIN_FREE_RAM_MB} MB breached."
                )

        # Sweep orphaned headless browser workers if any linger from previous aborted jobs
        if os.name == "nt":
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", "chrome-headless-shell.exe"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                pass

        return {
            "free_disk_gb": round(free_disk_gb, 2),
            "available_ram_mb": round(available_ram_mb, 1),
            "total_ram_gb": round(mem.total / (1024**3), 2),
            "ram_percent": mem.percent,
            "status": "SAFE_TO_RENDER"
        }

    def execute_isolated_render(
        self,
        command: List[str] | str,
        cwd: Optional[Path | str] = None,
        timeout_seconds: Optional[float] = None,
        log_file: Optional[Path | str] = None,
    ) -> Dict[str, Any]:
        """
        Executes a rendering process under monitored, isolated sequential execution.
        Safely records peak RAM/CPU and guarantees tree termination on timeout or failure.
        """
        self.check_preflight_safety()
        timeout = timeout_seconds or self.DEFAULT_TIMEOUT_SEC
        working_dir = Path(cwd or self.workspace_root).resolve()
        env = self.configure_environment()

        log_path = Path(log_file or (self.temp_dir / f"render_{int(time.time())}.log")).resolve()
        log_path.parent.mkdir(parents=True, exist_ok=True)

        start_time = time.time()
        peak_ram_mb = 0.0
        peak_cpu_pct = 0.0

        with open(log_path, "w", encoding="utf-8") as out_fp:
            # On Windows, if command is a list and starts with npm/npx, ensure .cmd extension
            if isinstance(command, list) and os.name == "nt":
                if command[0] in ["npm", "npx"]:
                    command[0] = f"{command[0]}.cmd"

            proc = subprocess.Popen(
                command,
                cwd=str(working_dir),
                stdout=out_fp,
                stderr=subprocess.STDOUT,
                env=env,
                shell=False,
            )

            try:
                ps_proc = psutil.Process(proc.pid)
                while proc.poll() is None:
                    elapsed = time.time() - start_time
                    if elapsed > timeout:
                        self._terminate_process_tree(proc.pid)
                        raise RenderProcessTimeoutError(
                            f"Render process PID {proc.pid} exceeded timeout of {timeout}s."
                        )

                    try:
                        # Monitor process memory including children
                        children = ps_proc.children(recursive=True)
                        total_rss = ps_proc.memory_info().rss
                        for child in children:
                            total_rss += child.memory_info().rss
                        total_ram_mb = total_rss / (1024**2)
                        peak_ram_mb = max(peak_ram_mb, total_ram_mb)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

                    time.sleep(0.5)

                return_code = proc.returncode

            except RenderProcessTimeoutError:
                raise
            except Exception as e:
                self._terminate_process_tree(proc.pid)
                raise RuntimeError(f"Unexpected error during render execution: {e}")

        duration = time.time() - start_time

        # Post-execution cleanup & garbage collection
        gc.collect()

        # Sweep orphaned headless browser workers if any linger from previous aborted jobs
        if os.name == "nt":
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", "chrome-headless-shell.exe"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                pass

        return {
            "returncode": return_code,
            "duration_seconds": round(duration, 2),
            "peak_ram_mb": round(peak_ram_mb, 1),
            "log_path": str(log_path),
            "success": return_code == 0,
        }

    def cleanup_temp_cache(self, keep_latest: bool = True) -> int:
        """
        Purges temporary frame extractions and scratch files to keep Drive A: headroom healthy.
        """
        deleted_count = 0
        if not self.temp_dir.exists():
            return 0

        for item in self.temp_dir.iterdir():
            try:
                if item.is_file():
                    item.unlink()
                    deleted_count += 1
                elif item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                    deleted_count += 1
            except Exception as e:
                logger.warning(f"Failed to delete temp item {item}: {e}")

        logger.info(f"Cleaned up {deleted_count} temporary items from {self.temp_dir}")
        return deleted_count

    @staticmethod
    def _terminate_process_tree(pid: int):
        """Kills a process and all its children cleanly on Windows."""
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.kill()
                except Exception:
                    pass
            parent.kill()
        except Exception:
            pass
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            # Guarantee no orphaned headless browser workers linger
            subprocess.run(
                ["taskkill", "/F", "/IM", "chrome-headless-shell.exe"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

