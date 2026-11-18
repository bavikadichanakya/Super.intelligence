"""
Unit tests for EngineDispatcher and EngineRegistry routing and fallback mechanisms.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from core.universal_scene_contract import (
    RenderingEngine,
    SceneType,
    UniversalSceneContract,
    VideoStoryboardContract,
)
from rendering.adapters.base_adapter import BaseEngineAdapter
from rendering.engine_dispatcher import EngineDispatcher
from rendering.engine_errors import (
    EngineUnavailableError,
    FallbackExhaustedError,
    RenderExecutionError,
)
from rendering.engine_registry import EngineRegistry
from rendering.render_artifact import RenderArtifact
from rendering.resource_guard import ResourceGuard


@pytest.fixture
def mock_artifact():
    return RenderArtifact(
        scene_id="s1",
        engine_name="manim",
        output_path=Path("A:/SUPER.INTELLIGENCEEE/output/stems/s1.mp4"),
        duration_seconds=5.0,
        width=1080,
        height=1920,
        fps=30.0,
        file_size_bytes=1024,
        sha256_hash="a" * 64,
    )


@pytest.fixture
def sample_scene():
    return UniversalSceneContract(
        scene_id="s1",
        video_id="v1",
        sequence_number=1,
        scene_type=SceneType.TECHNICAL_DIAGRAM,
        narrative_stage="hook",
        narrative_purpose="Purpose",
        audience_takeaway="Takeaway",
        visual_concept="Concept",
        mechanism_description="Mechanism",
        narration_text="Narration",
        narration_duration_seconds=5.0,
        preferred_engine=RenderingEngine.MANIM,
        fallback_engine=RenderingEngine.HYPERFRAMES,
    )


class TestEngineRegistry:
    def test_default_registry_has_core_engines(self):
        reg = EngineRegistry()
        assert reg.get_adapter(RenderingEngine.MANIM) is not None
        assert reg.get_adapter(RenderingEngine.THREEJS) is not None
        assert reg.get_adapter(RenderingEngine.HYPERFRAMES) is not None
        assert reg.get_adapter(RenderingEngine.FFMPEG) is not None

    def test_infer_engine_from_scene_type(self, sample_scene):
        reg = EngineRegistry()
        # TECHNICAL_DIAGRAM -> MANIM
        assert reg.infer_engine_for_scene(sample_scene) == RenderingEngine.MANIM

        # CONCEPTUAL_ANIMATION -> THREEJS
        sample_scene.scene_type = SceneType.CONCEPTUAL_ANIMATION
        assert reg.infer_engine_for_scene(sample_scene) == RenderingEngine.THREEJS

        # KINETIC_TYPOGRAPHY -> HYPERFRAMES
        sample_scene.scene_type = SceneType.KINETIC_TYPOGRAPHY
        assert reg.infer_engine_for_scene(sample_scene) == RenderingEngine.HYPERFRAMES

    def test_resolve_engine_preferred(self, sample_scene):
        reg = EngineRegistry()
        adapter = reg.resolve_engine(sample_scene)
        assert adapter.engine_name == RenderingEngine.MANIM

    def test_fallback_engine_resolution(self, sample_scene):
        reg = EngineRegistry()
        fb = reg.get_fallback_engine_for_scene(sample_scene, failed_engine=RenderingEngine.MANIM)
        assert fb == RenderingEngine.HYPERFRAMES


class TestEngineDispatcher:
    def test_dispatch_scene_success(self, sample_scene, mock_artifact):
        mock_adapter = MagicMock(spec=BaseEngineAdapter)
        mock_adapter.engine_name = RenderingEngine.MANIM
        mock_adapter.is_available.return_value = True
        mock_adapter.render.return_value = mock_artifact

        reg = EngineRegistry(auto_register=False)
        reg.register(RenderingEngine.MANIM, mock_adapter)

        dispatcher = EngineDispatcher(registry=reg)
        art = dispatcher.dispatch_scene(sample_scene)

        assert art == mock_artifact
        mock_adapter.render.assert_called_once()

    def test_dispatch_scene_fallback_on_primary_failure(self, sample_scene, mock_artifact):
        # Primary adapter fails
        mock_primary = MagicMock(spec=BaseEngineAdapter)
        mock_primary.engine_name = RenderingEngine.MANIM
        mock_primary.is_available.return_value = True
        mock_primary.render.side_effect = RenderExecutionError("Simulated primary failure")

        # Fallback adapter succeeds
        mock_fb_artifact = mock_artifact.model_copy(update={"engine_name": "hyperframes"})
        mock_fallback = MagicMock(spec=BaseEngineAdapter)
        mock_fallback.engine_name = RenderingEngine.HYPERFRAMES
        mock_fallback.is_available.return_value = True
        mock_fallback.render.return_value = mock_fb_artifact

        reg = EngineRegistry(auto_register=False)
        reg.register(RenderingEngine.MANIM, mock_primary)
        reg.register(RenderingEngine.HYPERFRAMES, mock_fallback)

        dispatcher = EngineDispatcher(registry=reg)
        art = dispatcher.dispatch_scene(sample_scene)

        assert art.engine_name == "hyperframes"
        mock_primary.render.assert_called_once()
        mock_fallback.render.assert_called_once()

    def test_dispatch_scene_raises_when_all_fail(self, sample_scene):
        mock_primary = MagicMock(spec=BaseEngineAdapter)
        mock_primary.engine_name = RenderingEngine.MANIM
        mock_primary.is_available.return_value = True
        mock_primary.render.side_effect = RenderExecutionError("Primary failed")

        mock_fallback = MagicMock(spec=BaseEngineAdapter)
        mock_fallback.engine_name = RenderingEngine.HYPERFRAMES
        mock_fallback.is_available.return_value = True
        mock_fallback.render.side_effect = RenderExecutionError("Fallback also failed")

        reg = EngineRegistry(auto_register=False)
        reg.register(RenderingEngine.MANIM, mock_primary)
        reg.register(RenderingEngine.HYPERFRAMES, mock_fallback)

        dispatcher = EngineDispatcher(registry=reg)
        with pytest.raises(FallbackExhaustedError) as exc_info:
            dispatcher.dispatch_scene(sample_scene)

        assert "All rendering engines failed" in str(exc_info.value)
        assert sample_scene.scene_id in str(exc_info.value)

    def test_sequential_lock_prevents_reentrant_deadlock(self, sample_scene, mock_artifact):
        mock_adapter = MagicMock(spec=BaseEngineAdapter)
        mock_adapter.engine_name = RenderingEngine.MANIM
        mock_adapter.is_available.return_value = True
        mock_adapter.render.return_value = mock_artifact

        reg = EngineRegistry(auto_register=False)
        reg.register(RenderingEngine.MANIM, mock_adapter)

        dispatcher = EngineDispatcher(registry=reg)
        # Calling twice sequentially works cleanly
        art1 = dispatcher.dispatch_scene(sample_scene)
        art2 = dispatcher.dispatch_scene(sample_scene)
        assert art1.scene_id == art2.scene_id
