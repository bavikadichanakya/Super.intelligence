"""
Unit tests for multi-engine rendering adapters, render artifacts, and execution context.
"""

import hashlib
import os
from pathlib import Path
import pytest

from core.universal_scene_contract import (
    CaptionSegment,
    RenderingEngine,
    SceneType,
    UniversalSceneContract,
    VideoStoryboardContract,
)
from rendering.adapters.base_adapter import BaseEngineAdapter
from rendering.adapters.ffmpeg_adapter import FFmpegAdapter
from rendering.adapters.hyperframes_adapter import HyperFramesAdapter
from rendering.adapters.manim_adapter import ManimAdapter
from rendering.adapters.threejs_adapter import ThreeJsAdapter
from rendering.engine_errors import (
    AdapterPreflightError,
    ArtifactValidationError,
    EngineUnavailableError,
)
from rendering.execution_context import ExecutionContext
from rendering.render_artifact import RenderArtifact
from rendering.resource_guard import ResourceGuard


@pytest.fixture
def sample_scene():
    return UniversalSceneContract(
        scene_id="test_scene_01",
        video_id="test_video_v1",
        sequence_number=1,
        scene_type=SceneType.TECHNICAL_DIAGRAM,
        narrative_stage="hook",
        narrative_purpose="Demonstrate algorithmic latency bottleneck",
        audience_takeaway="Linear attention cuts memory consumption by 8.4x",
        visual_concept="Quadratic vs Linear Attention Scaling Curve",
        mechanism_description="Comparison of memory matrix size as token count scales from 1k to 128k",
        narration_text="Traditional attention consumes quadratic memory, bottlenecking long-context reasoning.",
        narration_duration_seconds=4.5,
        preferred_engine=RenderingEngine.MANIM,
        fallback_engine=RenderingEngine.HYPERFRAMES,
    )


class TestRenderArtifact:
    def test_artifact_hash_calculation(self, tmp_path):
        dummy_file = tmp_path / "dummy.mp4"
        data = b"dummy video data for hash testing"
        dummy_file.write_bytes(data)

        h = RenderArtifact.compute_sha256(dummy_file)
        assert len(h) == 64
        assert h == hashlib.sha256(data).hexdigest()

    def test_missing_file_raises_validation_error(self, tmp_path):
        missing_path = tmp_path / "nonexistent.mp4"
        with pytest.raises(ArtifactValidationError):
            RenderArtifact.compute_sha256(missing_path)

    def test_artifact_model_validation(self, tmp_path):
        dummy_file = tmp_path / "stem.mp4"
        dummy_file.write_bytes(b"test data")
        h = RenderArtifact.compute_sha256(dummy_file)

        art = RenderArtifact(
            scene_id="s1",
            engine_name="manim",
            output_path=dummy_file,
            duration_seconds=5.0,
            width=1080,
            height=1920,
            fps=30.0,
            file_size_bytes=9,
            sha256_hash=h,
        )
        assert art.scene_id == "s1"
        assert art.engine_name == "manim"
        assert art.width == 1080
        assert art.height == 1920


class TestExecutionContext:
    def test_context_lifecycle_and_scratch(self):
        ctx = ExecutionContext(scene_id="ctx_test_01", keep_scratch=False)
        assert ctx.scratch_dir.exists()
        assert str(ctx.workspace_root) in str(ctx.scratch_dir)

        scratch_file = ctx.get_scratch_path("temp.txt")
        scratch_file.write_text("temporary scratch", encoding="utf-8")
        assert scratch_file.exists()

        # Context manager exit with cleanup
        with ctx:
            pass

        ctx.cleanup()
        assert not ctx.scratch_dir.exists()

    def test_environment_variable_overrides(self):
        ctx = ExecutionContext(scene_id="ctx_env_test")
        env = ctx.environment
        assert "TEMP" in env
        assert "TMP" in env
        assert "HYPERFRAMES_EXTRACT_CACHE_DIR" in env
        assert env["NODE_OPTIONS"] == "--max-old-space-size=2048"
        assert env["PRODUCER_LOW_MEMORY_MODE"] == "false"
        ctx.cleanup()


class TestManimAdapter:
    def test_adapter_availability(self):
        adapter = ManimAdapter()
        assert adapter.engine_name == RenderingEngine.MANIM
        assert adapter.is_available() is True
        ver = adapter.get_version()
        assert "Manim" in ver or "0." in ver

    def test_scene_validation(self, sample_scene):
        adapter = ManimAdapter()
        assert adapter.validate_scene(sample_scene) is True

    def test_prepare_generates_valid_script(self, sample_scene):
        adapter = ManimAdapter()
        with ExecutionContext(scene_id=sample_scene.scene_id) as ctx:
            prep = adapter.prepare(sample_scene, ctx)
            assert "script_path" in prep
            script_path = prep["script_path"]
            assert script_path.exists()
            content = script_path.read_text(encoding="utf-8")
            assert "config.pixel_width = 1080" in content
            assert "config.pixel_height = 1920" in content
            assert "class ManimScene_test_scene_01(Scene):" in content
            assert "Axes" in content


class TestThreeJsAdapter:
    def test_adapter_availability(self):
        adapter = ThreeJsAdapter()
        assert adapter.engine_name == RenderingEngine.THREEJS
        assert adapter.is_available() is True

    def test_prepare_generates_procedural_html(self, sample_scene):
        adapter = ThreeJsAdapter()
        with ExecutionContext(scene_id=sample_scene.scene_id) as ctx:
            prep = adapter.prepare(sample_scene, ctx)
            comp_file = prep["composition_file"]
            assert comp_file.exists()
            content = comp_file.read_text(encoding="utf-8")
            assert "three.min.js" in content
            assert "hf-seek" in content
            assert "renderAt" in content
            assert "1080" in content
            assert "1920" in content
            # Clean up
            comp_file.unlink()


class TestHyperFramesAdapter:
    def test_adapter_availability(self):
        adapter = HyperFramesAdapter()
        assert adapter.engine_name == RenderingEngine.HYPERFRAMES
        assert adapter.is_available() is True

    def test_prepare_generates_gsap_timeline(self, sample_scene):
        adapter = HyperFramesAdapter()
        with ExecutionContext(scene_id=sample_scene.scene_id) as ctx:
            prep = adapter.prepare(sample_scene, ctx)
            comp_file = prep["composition_file"]
            assert comp_file.exists()
            content = comp_file.read_text(encoding="utf-8")
            assert "gsap.timeline" in content
            assert "window.__timelines" in content
            assert "scanlines" in content
            comp_file.unlink()


class TestFFmpegAdapter:
    def test_adapter_availability(self):
        adapter = FFmpegAdapter()
        assert adapter.engine_name == RenderingEngine.FFMPEG
        assert adapter.is_available() is True
        ver = adapter.get_version()
        assert "ffmpeg" in ver.lower()

    def test_ass_subtitle_generation(self, sample_scene, tmp_path):
        adapter = FFmpegAdapter()
        sb = VideoStoryboardContract(
            video_id="test_video_v1",
            title="Subtitles Test Video",
            target_duration_seconds=5.0,
            scenes=[sample_scene],
        )
        ass_path = tmp_path / "test.ass"
        adapter.generate_ass_subtitles(sb, ass_path, safe_margin_bottom=340)
        assert ass_path.exists()
        content = ass_path.read_text(encoding="utf-8")
        assert "PlayResX: 1080" in content
        assert "PlayResY: 1920" in content
        assert "340" in content  # safe margin verified
        assert "Traditional attention consumes quadratic" in content
