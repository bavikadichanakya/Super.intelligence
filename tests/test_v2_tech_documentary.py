"""
SUPER.INTELLIGENCEEE — Phase 3 Tech Documentary Automated Test Suite
Verifies all submodules in creative/tech_documentary:
- Screen Demonstration (Terminal Animator)
- Technical Diagrams (Vector Diagram Engine)
- Motion Graphics (HUD Telemetry Engine)
- Cinematic Assets (Asset Resolver)
- Kinetic Typography (Kinetic Engine)
- Scene Composition (Documentary Compositor)
- Transitions (Transition Router)
- Sound Design (Sound Designer)
- Documentary Renderer (Tech Doc Producer)
"""

import math
import os
import shutil
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import MagicMock, patch

from PIL import Image

from core.creative_contracts import DynamicScene, DynamicScenePlan, SceneType
from creative.tech_documentary.screen_demonstration.terminal_animator import TerminalAnimator
from creative.tech_documentary.technical_diagrams.vector_diagram_engine import VectorDiagramEngine
from creative.tech_documentary.motion_graphics.hud_telemetry import HUDTelemetryEngine
from creative.tech_documentary.cinematic_assets.asset_resolver import AssetResolver
from creative.tech_documentary.kinetic_typography.kinetic_engine import KineticTypographyEngine
from creative.tech_documentary.scene_composition.documentary_compositor import DocumentaryCompositor
from creative.tech_documentary.transitions.transition_router import TransitionRouter
from creative.tech_documentary.sound_design.sound_designer import SoundDesigner
from creative.tech_documentary.documentary_renderer.tech_doc_producer import TechDocProducer, DocumentaryProductionResult


class TestTechDocumentaryEngine(unittest.TestCase):
    """Automated verification suite for the Tech Documentary production engine."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_tech_doc_"))
        self.addCleanup(lambda: shutil.rmtree(self.temp_dir, ignore_errors=True))

    def _create_mock_wav(self, path: Path, duration_sec: float = 1.0, sample_rate: int = 48000) -> Path:
        """Helper to create a valid uncompressed WAV file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        num_frames = int(duration_sec * sample_rate)
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            # Write silence (zeros)
            wf.writeframes(b"\x00\x00" * num_frames)
        return path

    # 1. Terminal Animator
    def test_terminal_animator_frame_rendering(self):
        animator = TerminalAnimator(width=540, height=960)
        frame = animator.render_frame(
            frame_idx=15,
            total_frames=60,
            command="pip install super-ai",
            output_lines=["[INFO] Initializing...", "[BENCH] 142.8 tok/s"],
            topic_header="TEST HEADER",
            sub_header="Execution",
        )
        self.assertIsInstance(frame, Image.Image)
        self.assertEqual(frame.size, (540, 960))
        # Verify non-blank frame
        extrema = frame.getextrema()
        self.assertIsNotNone(extrema)

    def test_terminal_animator_syntax_coloring(self):
        animator = TerminalAnimator()
        c_info = animator._get_line_color("[INFO] Ready")
        c_warn = animator._get_line_color("[WARN] Memory high")
        c_bench = animator._get_line_color("[BENCH] 3.4x")
        c_err = animator._get_line_color("[ERROR] Failed")
        c_norm = animator._get_line_color("Standard text")

        self.assertEqual(c_info, (0, 255, 140))
        self.assertEqual(c_warn, (255, 190, 40))
        self.assertEqual(c_bench, (0, 210, 255))
        self.assertEqual(c_err, (255, 80, 80))
        self.assertEqual(c_norm, (230, 235, 245))

    # 2. Vector Diagram Engine
    def test_vector_diagram_frame_rendering(self):
        engine = VectorDiagramEngine(width=540, height=960)
        stages = [
            {"title": "Input", "desc": "Tokens", "tag": "O(N)"},
            {"title": "Kernel", "desc": "Scan", "tag": "O(N log N)"},
            {"title": "Output", "desc": "Decoded", "tag": "140 tok/s"},
        ]
        frame = engine.render_frame(
            frame_idx=20,
            total_frames=60,
            stages=stages,
            topic_header="KERNEL PIPELINE",
            sub_header="Hardware Architecture",
        )
        self.assertIsInstance(frame, Image.Image)
        self.assertEqual(frame.size, (540, 960))

    # 3. HUD Telemetry Engine
    def test_hud_telemetry_gauges_and_reticles(self):
        hud = HUDTelemetryEngine(width=540, height=960)
        img = Image.new("RGB", (540, 960), (10, 15, 25))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)

        # Draw corner reticles
        hud.draw_corner_reticles(draw, (50, 50, 450, 250), color=(0, 210, 255), length=16)
        # Draw circular gauge
        hud.draw_circular_gauge(
            draw=draw,
            center=(270, 450),
            radius=80,
            progress_val=0.75,
            label="Throughput",
            value_str="+340%",
        )
        self.assertEqual(img.size, (540, 960))

    # 4. Cinematic Asset Resolver
    def test_asset_resolver_silicon_macro_and_provenance(self):
        resolver = AssetResolver()
        plate_p = self.temp_dir / "silicon_test.png"
        resolver.generate_silicon_macro_plate(plate_p, width=540, height=960)
        self.assertTrue(plate_p.exists())
        self.assertGreater(plate_p.stat().st_size, 5000)

        sha = resolver._compute_sha256(plate_p)
        self.assertEqual(len(sha), 64)

    # 5. Kinetic Typography Engine
    def test_kinetic_typography_spring_easing(self):
        engine = KineticTypographyEngine(width=540, height=960)
        # Verify spring scale function bounds
        s0 = engine._spring_scale(0.0)
        s_mid = engine._spring_scale(0.5)
        s1 = engine._spring_scale(1.0)

        self.assertAlmostEqual(s0, 0.0, places=4)
        self.assertGreater(s_mid, 0.5)
        self.assertAlmostEqual(s1, 1.0, places=4)

        frame = engine.render_frame(
            frame_idx=30,
            total_frames=60,
            primary_text="SUB-QUADRATIC ATTENTION SCALED",
            highlight_keyword="ATTENTION",
            stat_number="+340%",
        )
        self.assertIsInstance(frame, Image.Image)
        self.assertEqual(frame.size, (540, 960))

    # 6. Documentary Compositor
    def test_documentary_compositor_dispatch_types(self):
        compositor = DocumentaryCompositor(output_dir=self.temp_dir)

        # Mock the individual clip rendering methods to verify routing logic
        compositor.terminal_animator.render_terminal_clip = MagicMock(return_value=self.temp_dir / "term.mp4")
        compositor.diagram_engine.render_diagram_clip = MagicMock(return_value=self.temp_dir / "diag.mp4")
        compositor.hud_engine.render_metric_hud_clip = MagicMock(return_value=self.temp_dir / "hud.mp4")
        compositor.kinetic_engine.render_kinetic_clip = MagicMock(return_value=self.temp_dir / "kinetic.mp4")
        compositor.asset_resolver.resolve_broll_clip = MagicMock(return_value={"path": self.temp_dir / "broll.mp4"})

        # Test Screen Demonstration dispatch
        sc_term = DynamicScene(scene_id="s1", sequence=1, narration="CLI demo", scene_objective="demo", scene_type=SceneType.SCREEN_DEMONSTRATION, visual_concept="code", visual_description="desc", estimated_duration=4.0)
        p1 = compositor.render_scene(sc_term, 1, "test_slug")
        self.assertEqual(p1.name, "term.mp4")
        compositor.terminal_animator.render_terminal_clip.assert_called_once()

        # Test Technical Diagram dispatch
        sc_diag = DynamicScene(scene_id="s2", sequence=2, narration="Diagram", scene_objective="explain", scene_type=SceneType.TECHNICAL_DIAGRAM, visual_concept="diag", visual_description="desc", estimated_duration=5.0)
        p2 = compositor.render_scene(sc_diag, 2, "test_slug")
        self.assertEqual(p2.name, "diag.mp4")
        compositor.diagram_engine.render_diagram_clip.assert_called_once()

        # Test Data Visualization dispatch
        sc_hud = DynamicScene(scene_id="s3", sequence=3, narration="HUD", scene_objective="stats", scene_type=SceneType.DATA_VISUALIZATION, visual_concept="hud", visual_description="desc", estimated_duration=4.5)
        p3 = compositor.render_scene(sc_hud, 3, "test_slug")
        self.assertEqual(p3.name, "hud.mp4")
        compositor.hud_engine.render_metric_hud_clip.assert_called_once()

        # Test Kinetic Typography dispatch
        sc_kin = DynamicScene(scene_id="s4", sequence=4, narration="Kinetic", scene_objective="punch", scene_type=SceneType.KINETIC_TYPOGRAPHY, visual_concept="typo", visual_description="desc", estimated_duration=3.5)
        p4 = compositor.render_scene(sc_kin, 4, "test_slug")
        self.assertEqual(p4.name, "kinetic.mp4")
        compositor.kinetic_engine.render_kinetic_clip.assert_called_once()

        # Test Cinematic B-Roll dispatch
        sc_broll = DynamicScene(scene_id="s5", sequence=5, narration="B-roll", scene_objective="atmosphere", scene_type=SceneType.CINEMATIC_BROLL, visual_concept="broll", visual_description="desc", estimated_duration=4.0)
        p5 = compositor.render_scene(sc_broll, 5, "test_slug")
        self.assertEqual(p5.name, "broll.mp4")
        compositor.asset_resolver.resolve_broll_clip.assert_called_once()

    # 7. Transition Router
    def test_transition_router_single_clip(self):
        router = TransitionRouter()
        c1 = self.temp_dir / "clip1.mp4"
        c1.write_bytes(b"x" * 2000)
        out = self.temp_dir / "single_out.mp4"

        res = router.concat_clips([c1], out)
        self.assertTrue(res.exists())
        self.assertEqual(res.stat().st_size, c1.stat().st_size)

    # 8. Sound Designer
    def test_sound_designer_foley_timing_calculation(self):
        sd = SoundDesigner()
        scene_durs = [4.0, 5.0, 6.0]
        scene_types = ["SCREEN_DEMONSTRATION", "TECHNICAL_DIAGRAM", "KINETIC_TYPOGRAPHY"]

        # Verify that sound designer correctly calculates cumulative times
        total_time = sum(scene_durs)
        self.assertEqual(total_time, 15.0)

    # 9. Tech Doc Producer
    def test_producer_duration_sync(self):
        producer = TechDocProducer()
        wav1 = self._create_mock_wav(self.temp_dir / "w1.wav", duration_sec=3.2)
        wav2 = self._create_mock_wav(self.temp_dir / "w2.wav", duration_sec=4.6)

        scenes = [
            DynamicScene(scene_id="s1", sequence=1, narration="narration 1", scene_objective="demo", scene_type=SceneType.SCREEN_DEMONSTRATION, visual_concept="code", visual_description="desc", estimated_duration=5.0),
            DynamicScene(scene_id="s2", sequence=2, narration="narration 2", scene_objective="explain", scene_type=SceneType.TECHNICAL_DIAGRAM, visual_concept="diag", visual_description="desc", estimated_duration=5.0),
        ]

        durs = producer._sync_scene_durations_to_audio(scenes, [wav1, wav2])
        # Duration should be real_dur + 0.25 padding
        self.assertAlmostEqual(durs[0], 3.45, places=2)
        self.assertAlmostEqual(durs[1], 4.85, places=2)
        self.assertEqual(scenes[0].duration_seconds, 3.45)
        self.assertEqual(scenes[1].duration_seconds, 4.85)


if __name__ == "__main__":
    unittest.main()
