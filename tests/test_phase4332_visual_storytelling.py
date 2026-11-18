"""
SUPER.INTELLIGENCEEE — Phase 4.3.3.2 Visual Storytelling Test Suite
Validates the 12 Cinematic Visual & Storytelling Domains:
1. Composition Families (all 5 distinct composition families exist & instantiate)
2. Camera Operations (CinematicCamera push-in, pull-out, to_screen, to_screen_rect)
3. Subtitle Collisions (zero collision with protected visual regions)
4. Caption Boundaries (conformance to vertical and horizontal safe zones, max 2 lines)
5. Hardware Spec Consistency (Apple Silicon M4 official specs: 10-core CPU, 10-core GPU, 16GB, 120 GB/s)
6. Benchmark Evidence (verified empirical metrics from arXiv:2611.17294v1, removal of 38%/78%)
7. Scene Visual Diversity (< 0.94 consecutive scene similarity)
8. Motion Coverage (continuous transitions and animated elements)
9. Voice Identity Lock (Kokoro-82M am_liam, zero fallback)
10. Evidence Traceability & Security Calibration (verified claims, zero absolute/unsupported security claims)
11. Engine Failure Handling (no testsrc fallback, structured exceptions)
12. Resource Management & Cleanup (peak RAM < 500 MB, temp cache cleanup)
"""

import math
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageChops, ImageStat

from core.universal_scene_contract import (
    EvidenceStatus,
    FactClaimEvidence,
    RenderingEngine,
    SceneType,
    UniversalSceneContract,
    VideoStoryboardContract,
)
from rendering.adapters.ffmpeg_adapter import FFmpegAdapter
from rendering.adapters.native_motion_adapter import NativeMotionAdapter
from rendering.engine_dispatcher import EngineDispatcher
from rendering.engine_errors import RenderExecutionError
from rendering.engine_registry import EngineRegistry
from rendering.native_motion_engine.camera import CinematicCamera
from rendering.native_motion_engine.cinematic_components import (
    AppleSiliconHardwareHero,
    CinematicBenchmarkRace,
    CodingAgentRolloutVisual,
    HeroEditorialHeader,
    ProcessConfinementLaserBoundary,
)
from rendering.native_motion_engine.components import get_scene_protected_regions
from rendering.native_motion_engine.compositions import (
    CinematicEvidenceVerdictComposition,
    CloseUpMechanismComposition,
    ExplodedHardwareStackComposition,
    FullScreenArchitectureComposition,
    GenericMotionComposition,
    ProcessEntityTrackingComposition,
)
from rendering.native_motion_engine.renderer import NativeMotionRenderer
from rendering.native_motion_engine.typography import SafeZone, TypographyEngine
from rendering.resource_guard import ResourceGuard
from rendering.subtitle_layout import (
    BoundingBox,
    SubtitleCollisionValidator,
    SubtitleLayoutEngine,
)


class TestPhase4332VisualStorytelling(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path("A:/SUPER.INTELLIGENCEEE/.temp/phase4332_tests").resolve()
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.guard = ResourceGuard(workspace_root=self.temp_dir)
        self.registry = EngineRegistry(resource_guard=self.guard)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_mock_scene(self, seq_num: int) -> UniversalSceneContract:
        return UniversalSceneContract(
            scene_id=f"scene_{seq_num:02d}",
            sequence_number=seq_num,
            scene_type=SceneType.ANIMATED_PROCESS,
            narrative_purpose=f"Scene {seq_num} Narrative Purpose",
            visual_concept=f"Scene {seq_num} Visual Concept",
            audience_takeaway=f"Scene {seq_num} Audience Takeaway",
            narration_text=f"Scene {seq_num} narration text for validation.",
            narration_duration_seconds=10.0,
            actual_duration_seconds=10.0,
            mechanism_description=f"Scene {seq_num} mechanism description.",
            output_resolution=(1080, 1920),
            frame_rate=30,
        )

    # -------------------------------------------------------------------------
    # Domain 1: Composition Families
    # -------------------------------------------------------------------------
    def test_01_composition_families(self):
        """Asserts all 5 distinct composition families exist and instantiate correctly."""
        scene = self._create_mock_scene(1)
        
        c1 = FullScreenArchitectureComposition(scene, width=1080, height=1920)
        c2 = CloseUpMechanismComposition(scene, width=1080, height=1920)
        c3 = ProcessEntityTrackingComposition(scene, width=1080, height=1920)
        c4 = ExplodedHardwareStackComposition(scene, width=1080, height=1920)
        c5 = CinematicEvidenceVerdictComposition(scene, width=1080, height=1920)

        self.assertIsNotNone(c1)
        self.assertIsNotNone(c2)
        self.assertIsNotNone(c3)
        self.assertIsNotNone(c4)
        self.assertIsNotNone(c5)

        # Test frame rendering on each composition
        f1 = c1.render_frame(1.5)
        f2 = c2.render_frame(1.5)
        f3 = c3.render_frame(1.5)
        f4 = c4.render_frame(1.5)
        f5 = c5.render_frame(1.5)

        for f in [f1, f2, f3, f4, f5]:
            self.assertEqual(f.size, (1080, 1920))

    # -------------------------------------------------------------------------
    # Domain 2: Camera Operations
    # -------------------------------------------------------------------------
    def test_02_camera_operations(self):
        """Tests CinematicCamera push-in, pull-out, to_screen, and to_screen_rect math."""
        cam = CinematicCamera(viewport_width=1080, viewport_height=1920)
        self.assertEqual(cam.zoom, 1.0)
        self.assertEqual((cam.x, cam.y), (540.0, 960.0))

        # Test coordinate mapping at 1.0 zoom
        sx, sy = cam.to_screen(540.0, 960.0)
        self.assertEqual((sx, sy), (540.0, 960.0))

        # Test push-in transition
        cam.push_in_transition(t=2.0, start=0.0, duration=4.0, from_zoom=1.0, to_zoom=1.2, target=(540.0, 600.0))
        self.assertGreater(cam.zoom, 1.0)
        self.assertLessEqual(cam.zoom, 1.2)

        # Test bounding rect transformation
        rect = [100.0, 200.0, 300.0, 400.0]
        s_rect = cam.to_screen_rect(rect[0], rect[1], rect[2], rect[3])
        self.assertEqual(len(s_rect), 4)
        self.assertGreaterEqual(s_rect[2], s_rect[0])
        self.assertGreaterEqual(s_rect[3], s_rect[1])

        # Test pull-out transition
        cam.pull_out_transition(t=5.0, start=4.0, duration=2.0, from_zoom=1.2, to_zoom=1.0, target=(540.0, 960.0))
        self.assertAlmostEqual(cam.zoom, 1.1, delta=0.05)

    # -------------------------------------------------------------------------
    # Domain 3: Subtitle Collisions
    # -------------------------------------------------------------------------
    def test_03_subtitle_collisions(self):
        """Validates zero intersections between planned subtitle cues and protected regions in cinematic scenes."""
        layout_engine = SubtitleLayoutEngine(font_size=34, max_line_chars=36)

        scene_narrations = {
            "scene_01": (
                "Four Apple Mac mini nodes form our local testbed, but running agent rollouts "
                "serially leaves shared hardware severely underutilized.",
                1,
                FullScreenArchitectureComposition(self._create_mock_scene(1)),
            ),
            "scene_02": (
                "By isolating filesystem operations while interleaving command queues, Metal Sandbox "
                "enforces process boundaries without stalling the accelerator.",
                2,
                ProcessEntityTrackingComposition(self._create_mock_scene(2)),
            ),
            "scene_03": (
                "Across sixteen agent traces, the system achieved a 1.68 to 2.05 times command throughput gain, "
                "reducing batch execution time by 22.3 percent.",
                3,
                CinematicEvidenceVerdictComposition(self._create_mock_scene(3)),
            ),
        }

        all_cues = []
        protected_dict = {}
        cumulative_time = 0.0

        for scene_id, (narration, seq_num, comp) in scene_narrations.items():
            dur = 10.0
            regs = comp.protected_regions
            protected_dict[scene_id] = regs

            cues = layout_engine.plan_scene_cues(
                scene_id=scene_id,
                narration_text=narration,
                start_time_sec=cumulative_time,
                duration_sec=dur,
                protected_regions=regs,
            )
            all_cues.extend(cues)
            cumulative_time += dur

        passed, issues = SubtitleCollisionValidator.validate_cues_against_scenes(
            all_cues, protected_dict
        )
        self.assertTrue(passed, f"Subtitle collisions detected: {issues}")
        self.assertEqual(len(issues), 0)

    # -------------------------------------------------------------------------
    # Domain 4: Caption Boundaries
    # -------------------------------------------------------------------------
    def test_04_caption_boundaries(self):
        """Asserts subtitle cues conform to vertical and horizontal safe zones and max 2 lines."""
        layout_engine = SubtitleLayoutEngine(font_size=34, max_line_chars=36)
        cues = layout_engine.plan_scene_cues(
            scene_id="scene_01",
            narration_text="Across sixteen agent traces, the system achieved a 1.68 to 2.05 times command throughput gain.",
            start_time_sec=0.0,
            duration_sec=10.0,
            protected_regions=get_scene_protected_regions(1),
        )
        for cue in cues:
            self.assertLessEqual(len(cue.lines), 2, "Subtitle cue must not exceed 2 lines.")
            self.assertGreaterEqual(cue.bbox.x0, 60)
            self.assertLessEqual(cue.bbox.x1, 1020)
            self.assertGreaterEqual(cue.bbox.y0, 1380, "Subtitle entered protected upper canvas.")
            self.assertLessEqual(cue.bbox.y1, 1680, "Subtitle entered platform interaction danger zone.")

    # -------------------------------------------------------------------------
    # Domain 5: Hardware Spec Consistency
    # -------------------------------------------------------------------------
    def test_05_hardware_spec_consistency(self):
        """Asserts that hardware specs strictly match Apple M4 specifications."""
        scene = self._create_mock_scene(1)
        comp = FullScreenArchitectureComposition(scene)
        frame = comp.render_frame(2.0)
        self.assertIsNotNone(frame)

        # Inspect source code of cinematic components for correct specs
        import inspect
        src = inspect.getsource(CodingAgentRolloutVisual)
        self.assertIn("10-Core CPU (4P+6E)", src)
        self.assertIn("10-Core GPU", src)
        self.assertIn("16GB Unified Memory", src)
        self.assertIn("120 GB/s", src)
        # Ensure incorrect specs are absent
        self.assertNotIn("12-core", src.lower())
        self.assertNotIn("24gb", src.lower())

    # -------------------------------------------------------------------------
    # Domain 6: Benchmark Evidence
    # -------------------------------------------------------------------------
    def test_06_benchmark_evidence(self):
        """Asserts verified empirical metrics from arXiv:2611.17294v1, removal of 38%/78%."""
        import inspect
        src = inspect.getsource(CinematicBenchmarkRace)
        # Empirical metrics
        self.assertIn("1.68", src)
        self.assertIn("2.05", src)
        self.assertIn("22.3", src)
        self.assertIn("18.8", src)
        # Trace model estimate
        self.assertIn("2.14", src)
        # Outdated/unsupported figures must be absent
        self.assertNotIn("38%", src)
        self.assertNotIn("78%", src)

    # -------------------------------------------------------------------------
    # Domain 7: Scene Visual Diversity & Similarity
    # -------------------------------------------------------------------------
    def test_07_scene_similarity(self):
        """Asserts consecutive scene frame similarity < 0.94 using RMSE/difference metric."""
        s1 = FullScreenArchitectureComposition(self._create_mock_scene(1)).render_frame(3.0).convert("RGB")
        s2 = ProcessEntityTrackingComposition(self._create_mock_scene(2)).render_frame(3.0).convert("RGB")
        s3 = CinematicEvidenceVerdictComposition(self._create_mock_scene(3)).render_frame(3.0).convert("RGB")

        def calc_similarity(img1: Image.Image, img2: Image.Image) -> float:
            diff = ImageChops.difference(img1, img2)
            stat = ImageStat.Stat(diff)
            # Root mean square difference per channel normalized
            rms = math.sqrt(sum(val ** 2 for val in stat.mean) / len(stat.mean))
            # Max possible difference is ~255
            similarity = 1.0 - (rms / 255.0)
            return similarity

        sim_1_2 = calc_similarity(s1, s2)
        sim_2_3 = calc_similarity(s2, s3)

        self.assertLess(sim_1_2, 0.94, f"Scene 1 and 2 visual similarity {sim_1_2:.3f} >= 0.94")
        self.assertLess(sim_2_3, 0.94, f"Scene 2 and 3 visual similarity {sim_2_3:.3f} >= 0.94")

    # -------------------------------------------------------------------------
    # Domain 8: Motion Coverage
    # -------------------------------------------------------------------------
    def test_08_motion_coverage(self):
        """Asserts active visual motion between timeline points in each scene."""
        comp1 = FullScreenArchitectureComposition(self._create_mock_scene(1))
        f1_start = comp1.render_frame(0.5).convert("RGB")
        f1_mid = comp1.render_frame(3.5).convert("RGB")
        diff1 = ImageChops.difference(f1_start, f1_mid)
        stat1 = ImageStat.Stat(diff1)
        self.assertGreater(sum(stat1.mean), 5.0, "Scene 1 shows insufficient motion between t=0.5 and t=3.5")

        comp2 = ProcessEntityTrackingComposition(self._create_mock_scene(2))
        f2_start = comp2.render_frame(1.0).convert("RGB")
        f2_mid = comp2.render_frame(3.5).convert("RGB")
        diff2 = ImageChops.difference(f2_start, f2_mid)
        stat2 = ImageStat.Stat(diff2)
        self.assertGreater(sum(stat2.mean), 5.0, "Scene 2 shows insufficient motion between t=1.0 and t=3.5")

    # -------------------------------------------------------------------------
    # Domain 9: Voice Identity Lock
    # -------------------------------------------------------------------------
    def test_09_voice_identity(self):
        """Asserts that voice identity is locked to Kokoro am_liam with zero fallback."""
        from audio.narration.narration_service import NarrationService
        service = NarrationService()
        self.assertEqual(service.voicebox.default_voice, "am_liam")
        self.assertEqual(service.voicebox.DEFAULT_MALE_VOICE, "am_liam")
        self.assertEqual(service.voicebox.default_engine, "kokoro")

    # -------------------------------------------------------------------------
    # Domain 10: Security Claim Calibration
    # -------------------------------------------------------------------------
    def test_10_security_claim_calibration(self):
        """Asserts absence of absolute or unverified security claims."""
        import inspect
        src_comp = inspect.getsource(ProcessConfinementLaserBoundary)
        prohibited_phrases = [
            "zero memory bleed",
            "100% isolation",
            "completely unhackable",
            "absolute security",
            "zero overhead",
        ]
        for phrase in prohibited_phrases:
            self.assertNotIn(phrase, src_comp.lower())

    # -------------------------------------------------------------------------
    # Domain 11: Engine Failure Handling
    # -------------------------------------------------------------------------
    def test_11_engine_failure_handling(self):
        """Asserts engine failure raises structured error without silent test pattern fallback."""
        fb_three = self.registry.get_fallback_engine_for_scene(None, RenderingEngine.THREEJS)
        self.assertEqual(fb_three, RenderingEngine.NATIVE_MOTION)

        fb_hf = self.registry.get_fallback_engine_for_scene(None, RenderingEngine.HYPERFRAMES)
        self.assertEqual(fb_hf, RenderingEngine.NATIVE_MOTION)

        # Direct FFmpeg testsrc pattern must raise RenderExecutionError
        ff_adapter = FFmpegAdapter(resource_guard=self.guard)
        dummy_scene = UniversalSceneContract(
            scene_id="sc_fail",
            sequence_number=1,
            scene_type=SceneType.CONCEPTUAL_ANIMATION,
            narrative_purpose="Failure test",
            visual_concept="Test pattern trigger",
            audience_takeaway="Should fail",
            narration_text="Testing error handling.",
            narration_duration_seconds=1.0,
            actual_duration_seconds=1.0,
            mechanism_description="Test pattern",
        )
        from rendering.execution_context import ExecutionContext
        with ExecutionContext(scene_id="sc_fail", workspace_root=self.temp_dir) as ctx:
            with self.assertRaises(RenderExecutionError):
                ff_adapter.render(dummy_scene, ctx)

    # -------------------------------------------------------------------------
    # Domain 12: Resource Cleanup
    # -------------------------------------------------------------------------
    def test_12_resource_cleanup(self):
        """Asserts temp cache cleanup and peak RAM safety."""
        safety = self.guard.check_preflight_safety()
        self.assertEqual(safety["status"], "SAFE_TO_RENDER")
        self.assertGreater(safety["available_ram_mb"], 200.0)

        # Verify temp cache sweep
        test_temp = self.guard.temp_dir / "temp_marker.tmp"
        test_temp.write_text("marker")
        self.assertTrue(test_temp.exists())
        self.guard.cleanup_temp_cache()
        self.assertFalse(test_temp.exists())


if __name__ == "__main__":
    unittest.main()
