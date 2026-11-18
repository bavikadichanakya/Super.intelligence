"""
SUPER.INTELLIGENCEEE — Phase 4.3.2B Multi-Engine Rendering Dispatcher
BaseEngineAdapter abstract interface for all rendering engine adapters.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

from core.universal_scene_contract import RenderingEngine, UniversalSceneContract
from rendering.engine_errors import AdapterPreflightError, ArtifactValidationError
from rendering.execution_context import ExecutionContext
from rendering.render_artifact import RenderArtifact
from rendering.resource_guard import ResourceGuard

logger = logging.getLogger("super_intelligence.base_adapter")


class BaseEngineAdapter(ABC):
    """
    Abstract interface for rendering engine adapters.
    Coordinates scene validation, resource estimation, asset preparation,
    execution under ResourceGuard, and artifact verification.
    """

    def __init__(self, resource_guard: Optional[ResourceGuard] = None):
        self.guard = resource_guard or ResourceGuard()

    @property
    @abstractmethod
    def engine_name(self) -> RenderingEngine:
        """The canonical RenderingEngine enum value represented by this adapter."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Checks if the required binary, runtime, or dependencies are available on the host."""
        pass

    @abstractmethod
    def get_version(self) -> str:
        """Returns the version string of the underlying engine."""
        pass

    @abstractmethod
    def validate_scene(self, scene: UniversalSceneContract) -> bool:
        """
        Validates whether the scene contract satisfies all requirements for this engine.
        Raises AdapterPreflightError if validation fails.
        """
        pass

    def estimate_resources(self, scene: UniversalSceneContract) -> Dict[str, float]:
        """
        Returns estimated resource requirements for this scene.
        Default estimate: 500 MB RAM, 100 MB disk, scene.timeout_seconds or 180s.
        """
        duration = scene.actual_duration_seconds or scene.narration_duration_seconds or 5.0
        return {
            "ram_mb": 600.0,
            "disk_mb": 150.0,
            "estimated_render_seconds": round(duration * 12.0, 1),
            "timeout_seconds": scene.timeout_seconds or 180.0,
        }

    @abstractmethod
    def prepare(self, scene: UniversalSceneContract, context: ExecutionContext) -> Dict[str, Any]:
        """
        Prepares scene scripts, markup, configurations, and assets in the context's scratch directory.
        Returns a dictionary of prepared paths and command arguments.
        """
        pass

    @abstractmethod
    def render(self, scene: UniversalSceneContract, context: ExecutionContext) -> RenderArtifact:
        """
        Executes rendering under ResourceGuard isolation and returns a verified RenderArtifact.
        """
        pass

    def verify_output(
        self,
        output_path: Path | str,
        scene: UniversalSceneContract,
        render_time_seconds: float = 0.0,
        peak_ram_mb: float = 0.0,
    ) -> RenderArtifact:
        """
        Inspects output video against contract requirements (resolution, fps, duration).
        """
        w, h = scene.output_resolution
        fps = float(scene.frame_rate)
        expected_dur = scene.actual_duration_seconds or scene.narration_duration_seconds

        return RenderArtifact.from_output_file(
            scene_id=scene.scene_id,
            engine_name=self.engine_name.value,
            output_path=output_path,
            render_time_seconds=render_time_seconds,
            peak_ram_mb=peak_ram_mb,
            expected_width=w,
            expected_height=h,
            expected_fps=fps,
            expected_duration_seconds=expected_dur,
        )

    def get_fallback_engine(self, scene: UniversalSceneContract) -> Optional[RenderingEngine]:
        """
        Returns the declared fallback engine from the scene contract,
        or a sensible engine-specific default (typically HYPERFRAMES).
        """
        if scene.fallback_engine:
            return scene.fallback_engine
        if self.engine_name != RenderingEngine.HYPERFRAMES:
            return RenderingEngine.HYPERFRAMES
        return None

    def cleanup(self, context: ExecutionContext) -> None:
        """Performs post-render cleanup for this adapter."""
        context.cleanup()
