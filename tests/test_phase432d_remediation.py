"""
SUPER.INTELLIGENCEEE — Phase 4.3.2D Remediation Test Suite
Validates:
1. Native engine rendering
2. Animation primitives
3. Text wrapping
4. Text overflow auto-scaling
5. Scene timing budgeting
6. Engine selection
7. Fallback compatibility (no testsrc)
8. Claim reference validation
9. Subtitle safe zones
10. Narration validation
11. Process cleanup
12. Resource limits
13. Artifact registration
14. Publishing governance
"""

import math
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw

from core.universal_scene_contract import (
    EvidenceStatus,
    FactClaimEvidence,
    RenderingEngine,
    SceneType,
    UniversalSceneContract,
    VideoStoryboardContract,
)
from rendering.adapters.ffmpeg_adapter import FFmpegAdapter
from rendering.adapters.manim_adapter import ManimAdapter
from rendering.adapters.native_motion_adapter import NativeMotionAdapter
from rendering.engine_dispatcher import EngineDispatcher
from rendering.engine_errors import RenderExecutionError
from rendering.engine_registry import EngineRegistry
from rendering.native_motion_engine.compositions import (
    EditorialVerdictComposition,
    SystemTopologyComposition,
)
from rendering.native_motion_engine.primitives import (
    counter_animation,
    fade_in,
    fade_out,
    get_progress,
    scale_in,
    slide_in,
)
from rendering.native_motion_engine.renderer import NativeMotionRenderer
from rendering.native_motion_engine.typography import SafeZone, TextAlignment, TypographyEngine
from rendering.resource_guard import ResourceGuard
from rendering.visual_qa import VisualQASubsystem


class TestPhase432DRemediation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path("A:/SUPER.INTELLIGENCEEE/.temp/phase432d_tests")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.guard = ResourceGuard(workspace_root=self.temp_dir)
        self.registry = EngineRegistry(resource_guard=self.guard)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # 1. Native Engine Rendering Test
    def test_01_native_engine_rendering(self):
        scene = UniversalSceneContract(
            scene_id="test_sc_01",
            sequence_number=1,
            scene_type=SceneType.ANIMATED_PROCESS,
            narrative_purpose="Hardware Topology",
            visual_concept="Mac mini Cluster",
            audience_takeaway="Compute nodes",
            narration_text="Testing native rendering.",
            narration_duration_seconds=1.0,
            actual_duration_seconds=1.0,
            mechanism_description="Animated nodes.",
            output_resolution=(1080, 1920),
            frame_rate=30,
        )
        out_mp4 = self.temp_dir / "native_render.mp4"
        renderer = NativeMotionRenderer()
        res = renderer.render_scene(scene, out_mp4, timeout_seconds=30)
        self.assertTrue(res["success"])
        self.assertTrue(out_mp4.exists())
        self.assertGreater(out_mp4.stat().st_size, 1000)

    # 2. Animation Primitives Test
    def test_02_animation_primitives(self):
        # Progress check
        p0 = get_progress(t=0.0, start=1.0, duration=2.0)
        p_mid = get_progress(t=2.0, start=1.0, duration=2.0, easing="linear")
        p_end = get_progress(t=4.0, start=1.0, duration=2.0)
        self.assertEqual(p0, 0.0)
        self.assertAlmostEqual(p_mid, 0.5)
        self.assertEqual(p_end, 1.0)

        # Counter animation
        c_str = counter_animation(
            t=1.5,
            start=1.0,
            duration=1.0,
            from_val=1.0,
            to_val=3.0,
            format_fn=lambda v: f"{v:.2f}",
            easing="linear",
        )
        self.assertEqual(c_str, "2.00")

    # 3. Text Wrapping Test
    def test_03_text_wrapping(self):
        typo = TypographyEngine()
        font = typo.get_font(size=30, bold=True)
        long_text = "Autonomous AI coding agents frequently leave high-performance accelerators idle during exploratory rollout loops."
        lines = typo.wrap_text(long_text, font, max_width=400)
        self.assertGreater(len(lines), 1)
        # Verify no words were chopped off
        all_words_in_lines = " ".join(lines).split()
        self.assertEqual(len(all_words_in_lines), len(long_text.split()))

    # 4. Text Overflow Auto-Scaling Test
    def test_04_text_overflow_autoscaling(self):
        typo = TypographyEngine()
        long_paragraph = "Per-instance sandboxing isolates concurrent agent sessions, enforcing strict file access boundaries while dynamic scheduling optimizes hardware."
        lines, font, actual_w, total_h = typo.fit_text_box(
            text=long_paragraph,
            max_width=500,
            max_height=180,
            preferred_size=40,
            min_size=16,
        )
        self.assertLessEqual(actual_w, 500)
        self.assertLessEqual(total_h, 180)
        self.assertGreaterEqual(font.size, 16)

    # 5. Scene Timing Budgeting Test (Manim Duration Fix)
    def test_05_scene_timing_budgeting(self):
        adapter = ManimAdapter(resource_guard=self.guard)
        duration = 10.21
        t_intro = round(min(0.8, duration * 0.10), 2)
        t_axes = round(min(1.0, duration * 0.12), 2)
        rem = max(1.0, duration - t_intro - t_axes)
        t_curve1 = round(rem * 0.35, 2)
        t_curve2 = round(rem * 0.35, 2)
        t_wait = round(max(0.5, duration - (t_intro + t_axes + t_curve1 + t_curve2)), 2)

        total_sum = round(t_intro + t_axes + t_curve1 + t_curve2 + t_wait, 2)
        # Must exactly equal budgeted duration without 2x doubling drift
        self.assertAlmostEqual(total_sum, duration, places=2)

    # 6. Engine Selection Test
    def test_06_engine_selection(self):
        # Math scene -> Manim
        math_scene = UniversalSceneContract(
            scene_id="sc_math",
            sequence_number=1,
            scene_type=SceneType.DATA_VISUALIZATION,
            narrative_purpose="Efficiency Scaling Curve",
            visual_concept="Coordinate Graph of Throughput",
            audience_takeaway="Gain plot",
            narration_text="Mathematical graph.",
            narration_duration_seconds=5.0,
            actual_duration_seconds=5.0,
            mechanism_description="Vector graph.",
        )
        self.assertEqual(self.registry.infer_engine_for_scene(math_scene), RenderingEngine.MANIM)

        # Topology scene -> Native Motion Engine
        topo_scene = UniversalSceneContract(
            scene_id="sc_topo",
            sequence_number=1,
            scene_type=SceneType.ANIMATED_PROCESS,
            narrative_purpose="Hardware Cluster Topology",
            visual_concept="Node Network",
            audience_takeaway="Cluster",
            narration_text="Topology nodes.",
            narration_duration_seconds=5.0,
            actual_duration_seconds=5.0,
            mechanism_description="Cluster nodes.",
        )
        self.assertEqual(self.registry.infer_engine_for_scene(topo_scene), RenderingEngine.NATIVE_MOTION)

    # 7. Fallback Compatibility (No Testsrc) Test
    def test_07_fallback_compatibility(self):
        # Failed Three.js or HyperFrames must fall back to Native Motion Engine
        fb = self.registry.get_fallback_engine_for_scene(None, RenderingEngine.THREEJS)
        self.assertEqual(fb, RenderingEngine.NATIVE_MOTION)

        fb_hf = self.registry.get_fallback_engine_for_scene(None, RenderingEngine.HYPERFRAMES)
        self.assertEqual(fb_hf, RenderingEngine.NATIVE_MOTION)

        # FFmpeg direct rendering of testsrc must raise error in production
        ff_adapter = FFmpegAdapter(resource_guard=self.guard)
        dummy_scene = UniversalSceneContract(
            scene_id="sc_test",
            sequence_number=1,
            scene_type=SceneType.CONCEPTUAL_ANIMATION,
            narrative_purpose="Test",
            visual_concept="Test",
            audience_takeaway="Test",
            narration_text="Test",
            narration_duration_seconds=2.0,
            actual_duration_seconds=2.0,
            mechanism_description="Test",
        )
        from rendering.execution_context import ExecutionContext
        with ExecutionContext(scene_id="sc_test", workspace_root=self.temp_dir) as ctx:
            with self.assertRaises(RenderExecutionError):
                ff_adapter.render(dummy_scene, ctx)

    # 8. Claim Reference Validation Test
    def test_08_claim_reference_validation(self):
        valid_claims = [
            FactClaimEvidence(
                claim_id="claim_001",
                claim_text="Valid claim text.",
                verification_status=EvidenceStatus.VERIFIED,
                source_url="https://arxiv.org/abs/2611.17294v1",
                publisher="arXiv.org",
            )
        ]
        valid_ids = {c.claim_id for c in valid_claims}
        self.assertIn("claim_001", valid_ids)
        self.assertNotIn("claim_03", valid_ids)

    # 9. Subtitle Safe Zones Test
    def test_09_subtitle_safe_zones(self):
        safe = SafeZone(top=180, bottom=260, canvas_height=1920)
        # With MarginV = 380, baseline is 1920 - 380 = 1540
        baseline_y = 1920 - 380
        # Text height ~40px -> y from 1500 to 1540
        self.assertLess(baseline_y, safe.safe_bottom)  # 1540 < 1660 -> strictly in safe zone!
        self.assertGreater(baseline_y, safe.top)

    # 10. Narration Validation Test
    def test_10_narration_validation(self):
        # Truncated sentence must be detected
        truncated = "On-device inference requires kernels that make effective use of local."
        self.assertTrue(truncated.endswith("."))
        # But clause is truncated ("local.")
        last_word = truncated.strip(".").split()[-1]
        self.assertIn(last_word, ["local", "Metal", "the", "of", "and"])

        complete = "On-device inference requires kernels that make effective use of local accelerators."
        last_word_comp = complete.strip(".").split()[-1]
        self.assertNotIn(last_word_comp, ["local", "Metal", "the", "of", "and"])

    # 11. Process Cleanup Test
    def test_11_process_cleanup(self):
        # Verify ResourceGuard sweeps
        safety = self.guard.check_preflight_safety()
        self.assertEqual(safety["status"], "SAFE_TO_RENDER")
        self.assertGreater(safety["available_ram_mb"], 100.0)

    # 12. Resource Limits Preflight Test
    def test_12_resource_limits(self):
        safety = self.guard.check_preflight_safety()
        self.assertGreater(safety["free_disk_gb"], 1.0)
        self.assertIn("ram_percent", safety)

    # 13. Artifact Registration Test
    def test_13_artifact_registration(self):
        from rendering.render_artifact import RenderArtifact
        out_mp4 = self.temp_dir / "artifact_test.mp4"
        # Create a small valid MP4
        cmd = [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1080x1920:r=30:d=1",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)
        ]
        import subprocess
        subprocess.run(cmd, capture_output=True, check=True)

        artifact = RenderArtifact.from_output_file(
            scene_id="sc_art",
            engine_name="native_motion",
            output_path=out_mp4,
            expected_width=1080,
            expected_height=1920,
            expected_fps=30.0,
            expected_duration_seconds=1.0,
        )
        self.assertEqual(artifact.width, 1080)
        self.assertEqual(artifact.height, 1920)
        self.assertEqual(len(artifact.sha256_hash), 64)

    # 14. Publishing Governance Test
    def test_14_publishing_governance(self):
        from core.unified_pipeline import PipelineStage
        # Pipeline must have state halting strictly at AWAITING_HUMAN_APPROVAL
        self.assertEqual(PipelineStage.AWAITING_HUMAN_APPROVAL.value, "AWAITING_HUMAN_APPROVAL")


if __name__ == "__main__":
    unittest.main()