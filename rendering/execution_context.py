"""
SUPER.INTELLIGENCEEE — Phase 4.3.2B Multi-Engine Rendering Dispatcher
ExecutionContext for isolated per-scene rendering environments, scratch management, and logging.
"""

from __future__ import annotations

import logging
import os
import shutil
import time
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger("super_intelligence.execution_context")


class ExecutionContext:
    """
    Manages an isolated working environment for a single scene render.
    Ensures all temporary files, cache writes, logs, and stems remain strictly confined to Drive A: .temp.
    """

    def __init__(
        self,
        scene_id: str,
        workspace_root: Optional[Path | str] = None,
        output_dir: Optional[Path | str] = None,
        keep_scratch: bool = False,
    ):
        self.scene_id = scene_id
        self.workspace_root = Path(workspace_root or "A:/SUPER.INTELLIGENCEEE").resolve()
        self.timestamp = int(time.time() * 1000)
        self.run_id = f"{scene_id}_{self.timestamp}"

        # Per-scene scratch directory inside Drive A: .temp
        self.temp_root = self.workspace_root / ".temp"
        self.scratch_dir = self.temp_root / "renders" / self.run_id
        self.scratch_dir.mkdir(parents=True, exist_ok=True)

        # Output stems directory
        self.output_dir = Path(output_dir or (self.workspace_root / "output" / "stems")).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Log path
        self.log_file = self.scratch_dir / f"{self.run_id}.log"
        self.keep_scratch = keep_scratch
        self.is_active = False

    @property
    def environment(self) -> Dict[str, str]:
        """Provides environment variables redirecting all temporary allocations to Drive A:."""
        env = dict(os.environ)
        scratch_str = str(self.scratch_dir.resolve())
        env["TEMP"] = scratch_str
        env["TMP"] = scratch_str
        env["HYPERFRAMES_EXTRACT_CACHE_DIR"] = scratch_str
        env["NODE_OPTIONS"] = "--max-old-space-size=2048"
        env["PRODUCER_LOW_MEMORY_MODE"] = "false"
        return env

    def get_output_stem_path(self, suffix: str = ".mp4") -> Path:
        """Returns the canonical output path for the rendered scene stem."""
        return self.output_dir / f"{self.scene_id}{suffix}"

    def get_scratch_path(self, filename: str) -> Path:
        """Returns a path within this scene's isolated scratch directory."""
        return self.scratch_dir / filename

    def cleanup(self, force: bool = False) -> None:
        """Purges scratch files unless keep_scratch is True."""
        if not force and self.keep_scratch:
            logger.info(f"Retaining scratch directory for debugging: {self.scratch_dir}")
            return

        if self.scratch_dir.exists():
            try:
                shutil.rmtree(self.scratch_dir, ignore_errors=True)
                logger.debug(f"Purged isolated scratch directory: {self.scratch_dir}")
            except Exception as e:
                logger.warning(f"Failed to cleanly delete scratch directory {self.scratch_dir}: {e}")

    def __enter__(self) -> ExecutionContext:
        self.is_active = True
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.is_active = False
        # If an error occurred, keep scratch files for post-mortem debugging unless forced
        if exc_type is not None:
            logger.error(f"Render failed in ExecutionContext {self.run_id}: {exc_val}. Scratch retained at {self.scratch_dir}")
        else:
            self.cleanup()
