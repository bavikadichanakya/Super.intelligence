"""
SUPER.INTELLIGENCEEE — Phase 4.3.2D Multi-Engine Rendering Dispatcher
NativeMotionAdapter: Adapter for the lightweight, CPU-efficient Native 2D Motion Graphics Engine.
Renders node networks, hardware topologies, architectural conclusions, and kinetic typography
directly to MP4 stems with zero headless browser overhead.
"""

from __future__ import annotations

import logging
import shutil
import time
from pathlib import Path
from typing import Any, Dict, Optional

import PIL

from core.universal_scene_contract import RenderingEngine, UniversalSceneContract
from rendering.adapters.base_adapter import BaseEngineAdapter
from rendering.engine_errors import (
    AdapterPreflightError,
    ArtifactValidationError,
    EngineUnavailableError,
    RenderExecutionError,
    RenderTimeoutError,
)
from rendering.execution_context import ExecutionContext
from rendering.native_motion_engine.renderer import NativeMotionRenderer
from rendering.render_artifact import RenderArtifact
from rendering.resource_guard import ResourceGuard

logger = logging.getLogger("super_intelligence.native_motion_adapter")


class NativeMotionAdapter(BaseEngineAdapter):
    """
    Adapter for the Native 2D Motion Graphics Engine.
    Executes in-process frame composition using Pillow/Cairo and pipes raw RGBA frames
    directly to FFmpeg.
    """

    def __init__(
        self,
        ffmpeg_bin: Optional[str] = None,
        resource_guard: Optional[ResourceGuard] = None,
    ):
        super().__init__(resource_guard=resource_guard)
        self.ffmpeg_bin = ffmpeg_bin or "ffmpeg"
        self.renderer = NativeMotionRenderer(ffmpeg_bin=self.ffmpeg_bin)
        self._cached_version: Optional[str] = None

    @property
    def engine_name(self) -> RenderingEngine:
        return RenderingEngine.NATIVE_MOTION

    def is_available(self) -> bool:
        """Verifies that Pillow and FFmpeg are available."""
        has_pillow = hasattr(PIL, "__version__")
        has_ffmpeg = shutil.which(self.ffmpeg_bin) is not None
        return has_pillow and has_ffmpeg

    def get_version(self) -> str:
        """Returns the version description."""
        if self._cached_version:
            return self._cached_version
        pil_ver = getattr(PIL, "__version__", "unknown")
        self._cached_version = f"NativeMotionEngine v1.0.0 (Pillow {pil_ver} + FFmpeg)"
        return self._cached_version

    def validate_scene(self, scene: UniversalSceneContract) -> bool:
        """Validates that the scene contract is well-formed for 2D motion rendering."""
        if not self.is_available():
            raise EngineUnavailableError("NativeMotionEngine dependencies (Pillow / FFmpeg) are not satisfied.")

        w, h = scene.output_resolution
        if w <= 0 or h <= 0:
            raise AdapterPreflightError(f"Invalid resolution for scene {scene.scene_id}: {scene.output_resolution}")

        duration = scene.actual_duration_seconds or scene.narration_duration_seconds or 0.0
        if duration <= 0.0:
            raise AdapterPreflightError(f"Invalid duration for scene {scene.scene_id}: {duration}s")

        return True

    def estimate_resources(self, scene: UniversalSceneContract) -> Dict[str, float]:
        """Native motion engine has very low memory and disk requirements."""
        duration = scene.actual_duration_seconds or scene.narration_duration_seconds or 5.0
        return {
            "ram_mb": 120.0,
            "disk_mb": 20.0,
            "estimated_render_seconds": round(duration * 0.35, 1),
            "timeout_seconds": scene.timeout_seconds or 60.0,
        }

    def prepare(self, scene: UniversalSceneContract, context: ExecutionContext) -> Dict[str, Any]:
        """Prepares target paths for the native render."""
        self.validate_scene(scene)
        target_output = context.get_output_stem_path(".mp4")
        return {
            "output_path": target_output,
            "duration": float(scene.actual_duration_seconds or scene.narration_duration_seconds or 5.0),
        }

    def render(self, scene: UniversalSceneContract, context: ExecutionContext) -> RenderArtifact:
        """
        Renders the scene via NativeMotionRenderer under ResourceGuard preflight safety.
        """
        prep = self.prepare(scene, context)
        target_output = prep["output_path"]
        log_file = context.log_file

        timeout = scene.timeout_seconds or 120.0
        start_time = time.time()

        try:
            # Preflight safety check
            self.guard.check_preflight_safety()

            # Execute direct pipe rendering
            metrics = self.renderer.render_scene(
                scene=scene,
                output_path=target_output,
                log_file=log_file,
                timeout_seconds=timeout,
            )

        except Exception as e:
            raise RenderExecutionError(f"NativeMotionAdapter rendering failed: {e}", log_path=str(log_file))

        render_time = time.time() - start_time
        logger.info(
            f"NativeMotionAdapter successfully rendered '{scene.scene_id}' to {target_output} "
            f"in {render_time:.2f}s."
        )

        return self.verify_output(
            output_path=target_output,
            scene=scene,
            render_time_seconds=render_time,
            peak_ram_mb=65.0,  # Peak RAM is minimal (~65 MB)
        )

