"""
SUPER.INTELLIGENCEEE — Phase 4.3.2B Multi-Engine Rendering Dispatcher
EngineRegistry: Registers, queries, and resolves rendering engine adapters by capability and scene type.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from core.universal_scene_contract import RenderingEngine, SceneType, UniversalSceneContract
from rendering.adapters.base_adapter import BaseEngineAdapter
from rendering.adapters.ffmpeg_adapter import FFmpegAdapter
from rendering.adapters.hyperframes_adapter import HyperFramesAdapter
from rendering.adapters.manim_adapter import ManimAdapter
from rendering.adapters.native_motion_adapter import NativeMotionAdapter
from rendering.adapters.threejs_adapter import ThreeJsAdapter
from rendering.engine_errors import EngineUnavailableError
from rendering.resource_guard import ResourceGuard

logger = logging.getLogger("super_intelligence.engine_registry")


class EngineRegistry:
    """
    Central registry for multi-engine rendering adapters.
    Maintains adapter singletons, queries engine health, and resolves the best engine
    for each scene contract based on scene type, preferred engine, and system availability.
    """

    def __init__(self, resource_guard: Optional[ResourceGuard] = None, auto_register: bool = True):
        self.guard = resource_guard or ResourceGuard()
        self._adapters: Dict[RenderingEngine, BaseEngineAdapter] = {}

        if auto_register:
            self._register_default_adapters()

    def _register_default_adapters(self) -> None:
        """Instantiates and registers the production adapters."""
        self.register(RenderingEngine.NATIVE_MOTION, NativeMotionAdapter(resource_guard=self.guard))
        self.register(RenderingEngine.MANIM, ManimAdapter(resource_guard=self.guard))
        self.register(RenderingEngine.THREEJS, ThreeJsAdapter(resource_guard=self.guard))
        self.register(RenderingEngine.HYPERFRAMES, HyperFramesAdapter(resource_guard=self.guard))
        self.register(RenderingEngine.FFMPEG, FFmpegAdapter(resource_guard=self.guard))

    def register(self, engine: RenderingEngine, adapter: BaseEngineAdapter) -> None:
        """Registers an adapter for an engine type."""
        self._adapters[engine] = adapter
        logger.debug(f"Registered engine adapter for: {engine.value}")

    def get_adapter(self, engine: RenderingEngine) -> Optional[BaseEngineAdapter]:
        """Returns the registered adapter for the given engine enum."""
        return self._adapters.get(engine)

    def get_available_engines(self) -> List[RenderingEngine]:
        """Returns all registered engines whose runtimes/binaries are currently available."""
        available = []
        for engine, adapter in self._adapters.items():
            if adapter.is_available():
                available.append(engine)
        return available

    def infer_engine_for_scene(self, scene: UniversalSceneContract) -> RenderingEngine:
        """
        Determines the optimal engine based on scene archetype and narrative purpose.
        - Mathematics, formulas, coordinate scaling plots -> Manim
        - Topologies, architecture diagrams, HUDs, kinetic typography -> Native Motion Engine
        """
        st = scene.scene_type
        purpose = (scene.narrative_purpose or "").lower()
        concept = (scene.visual_concept or "").lower()

        # Check for mathematical or coordinate graphing intent
        math_keywords = ["math", "equation", "coordinate", "curve", "graph", "plot", "scaling", "duty cycle", "complexity"]
        is_math_oriented = any(k in purpose or k in concept for k in math_keywords)

        if st == SceneType.DATA_VISUALIZATION or is_math_oriented:
            return RenderingEngine.MANIM
        elif st in (SceneType.TECHNICAL_DIAGRAM, SceneType.CONCEPTUAL_ANIMATION, SceneType.ANIMATED_PROCESS):
            return RenderingEngine.NATIVE_MOTION
        elif st == SceneType.KINETIC_TYPOGRAPHY:
            return RenderingEngine.NATIVE_MOTION
        else:
            return RenderingEngine.NATIVE_MOTION

    def resolve_engine(self, scene: UniversalSceneContract) -> BaseEngineAdapter:
        """
        Resolves the appropriate adapter for a scene, adhering to preferred engine,
        archetype defaults, and runtime availability.
        """
        target_engine = scene.preferred_engine or self.infer_engine_for_scene(scene)

        adapter = self.get_adapter(target_engine)
        if adapter and adapter.is_available():
            return adapter

        logger.warning(
            f"Preferred engine '{target_engine.value}' is unavailable for scene '{scene.scene_id}'. "
            "Attempting fallback..."
        )

        # Try fallback engine declared in scene contract
        fallback_engine = self.get_fallback_engine_for_scene(scene, target_engine)
        if fallback_engine:
            fb_adapter = self.get_adapter(fallback_engine)
            if fb_adapter and fb_adapter.is_available():
                logger.info(f"Routed scene '{scene.scene_id}' to fallback engine '{fallback_engine.value}'.")
                return fb_adapter

        # Default reliable fallback: Native Motion Engine
        native_adapter = self.get_adapter(RenderingEngine.NATIVE_MOTION)
        if native_adapter and native_adapter.is_available():
            logger.info(f"Falling back to Native Motion Engine for scene '{scene.scene_id}'.")
            return native_adapter

        raise EngineUnavailableError(
            f"No suitable rendering engine available for scene '{scene.scene_id}' "
            f"(target: {target_engine.value}). Available engines: {[e.value for e in self.get_available_engines()]}"
        )

    def get_fallback_engine_for_scene(
        self,
        scene: Optional[UniversalSceneContract],
        failed_engine: RenderingEngine,
    ) -> Optional[RenderingEngine]:
        """
        Identifies a viable fallback engine distinct from the failed engine.
        Guarantees that fallbacks preserve scene intent and NEVER route to diagnostic test patterns.
        """
        if scene and scene.fallback_engine and scene.fallback_engine != failed_engine:
            return scene.fallback_engine

        # Defaults based on failed engine:
        # If 3D (Three.js) or HTML (HyperFrames) fails, fall back to Native Motion (2D vector/raster animation).
        if failed_engine in (RenderingEngine.THREEJS, RenderingEngine.HYPERFRAMES, RenderingEngine.MANIM):
            return RenderingEngine.NATIVE_MOTION

        return None
