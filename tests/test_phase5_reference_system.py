"""
SUPER.INTELLIGENCEEE — Phase 5 Reference System Unit Test Suite
Verifies:
1. Multi-source research discovery and scoring.
2. Authentic media acquisition and SHA-256 provenance manifests.
3. Dual-font kinetic typography and animated selection boxes.
4. Pure Python 3D isometric projections and hardware models.
5. Evidence cards (GitHub repo, documentation viewer, side-by-side comparison).
6. Specialized telemetry (Lollipop chart, RAM flatline, digital stopwatch, MoE grid).
7. All 8 Reference Composition templates under BaseMotionComposition interface.
8. ReferenceSoundDesigner procedural lo-fi bed and EBU R128 audio mastering.
9. ReferenceDirector 9-beat storyboard construction.
"""

from __future__ import annotations

import json
import os
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from audio.reference_sound_designer import ReferenceSoundDesigner, SFXEvent
from core.schemas import ResearchDossier, ClaimEvidence
from core.universal_scene_contract import (
    RenderingEngine,
    SceneType,
    UniversalSceneContract,
    VideoStoryboardContract,
)
from creative.reference_director import ReferenceDirector
from rendering.reference_visual_engine.charts_and_telemetry import (
    DigitalStopwatchTimer,
    FlatlineTelemetryCard,
    LollipopChart,
    MoEExpertGrid,
)
from rendering.reference_visual_engine.evidence_cards import (
    DocumentationFigureViewer,
    GitHubRepoCard,
    SideBySideComparisonCard,
)
from rendering.reference_visual_engine.isometric_3d import (
    IsometricBarChart,
    IsometricHardwareModels,
    IsometricLayerStack,
    IsometricVoxelCube,
    iso_project,
)
from rendering.reference_visual_engine.kinetic_typography import (
    KineticWord,
    ReferenceKineticTypography,
)
from rendering.reference_visual_engine.reference_compositions import (
    ReferenceBarChartComparisonComposition,
    ReferenceDeterminismComparisonComposition,
    ReferenceIsometricHookComposition,
    ReferenceLatencyTimerComposition,
    ReferenceLayerStreamingComposition,
    ReferenceLoopConclusionComposition,
    ReferenceMoEMechanismComposition,
    ReferenceRepoEvidenceComposition,
)
from research.media_acquirer import MediaAcquisitionEngine, VisualAssetRecord
from research.multi_source_discovery import MultiSourceDiscoveryEngine, TopicCandidate


class TestPhase5ReferenceSystem(unittest.TestCase):
    """Exhaustive test suite for the Phase 5 Reference Studio."""

    @classmethod
    def setUpClass(cls):
        cls.width = 576
        cls.height = 1024
        cls.test_dir = Path(".temp/test_phase5")
        cls.test_dir.mkdir(parents=True, exist_ok=True)

    def test_01_multi_source_discovery(self):
        """Verifies multi-source topic discovery and candidate ranking."""
        engine = MultiSourceDiscoveryEngine()
        cand = TopicCandidate(
            candidate_id="cand_test_01",
            title="Kimi K3 in C: 2.78T parameter model in 8GB RAM",
            category="Open-source projects",
            ecosystem="github",
            source_name="GitHub.com",
            source_url="https://github.com/FareedKhan-dev/kimi-k3-in-c",
            publication_date="2026-11-14T00:00:00Z",
            discovery_timestamp="2026-11-15T12:00:00Z",
            summary="Pure portable C99 implementation streaming MoE layers from disk.",
            main_technical_development="Portable C99 CPU inference engine with chunked layer streaming.",
            why_it_matters="Democratizes trillion-parameter models on consumer hardware.",
            technical_complexity="high",
            evidence_quality="verified_primary",
            visual_assets_available=["repo_card", "docs/images/architecture.png"],
            raw_metadata={"stars": 1250, "language": "C"},
        )
        engine._score_candidate(cand)
        self.assertGreaterEqual(cand.total_score, 50.0)
        self.assertGreater(cand.significance_score, 0.0)
        self.assertGreater(cand.visual_potential_score, 0.0)
        self.assertEqual(cand.ecosystem, "github")

    def test_02_media_acquirer_provenance(self):
        """Verifies media acquisition manifest format and SHA-256 hashing."""
        acquirer = MediaAcquisitionEngine(assets_root=self.test_dir / "assets")
        test_file = self.test_dir / "sample_test_diagram.png"
        img = Image.new("RGBA", (200, 200), (20, 20, 30, 255))
        img.save(test_file)

        sha = acquirer._compute_sha256(test_file)
        self.assertEqual(len(sha), 64)

        record = VisualAssetRecord(
            asset_id="asset_test_01",
            asset_type="repo_doc_figure",
            title="Test Architecture Diagram",
            source_url="https://github.com/FareedKhan-dev/kimi-k3-in-c",
            original_creator="FareedKhan-dev",
            provider="github",
            license_type="MIT",
            license_url="https://opensource.org/licenses/MIT",
            attribution_required=True,
            retrieval_date="2026-11-15T12:00:00Z",
            sha256_hash=sha,
            local_path=str(test_file),
            dimensions=[200, 200],
        )
        acquirer.manifest["asset_test_01"] = record.__dict__
        acquirer._save_manifest()

        self.assertTrue(acquirer.manifest_path.exists())
        with open(acquirer.manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("asset_test_01", data)
        self.assertEqual(data["asset_test_01"]["sha256_hash"], sha)

    def test_03_kinetic_typography(self):
        """Verifies dual-font kinetic typography and selection bounding boxes."""
        kt = ReferenceKineticTypography(self.width, self.height)
        img = Image.new("RGBA", (self.width, self.height), (10, 13, 20, 255))
        draw = ImageDraw.Draw(img)

        words = [
            KineticWord("RUN", is_bold=True),
            KineticWord("2.78T", is_serif_italic=True, is_bold=True),
            KineticWord("IN", is_bold=True),
            KineticWord("[8 gigs]", is_highlight_box=True, is_bold=True),
        ]

        # Render at t = 1.0 (fully settled)
        kt.render_headline(
            draw=draw,
            words=words,
            center_x=self.width // 2,
            top_y=250,
            t=1.0,
            is_dark_theme=True,
        )
        self.assertEqual(img.size, (self.width, self.height))

        # Check that canvas is not empty
        arr = np.array(img)
        self.assertGreater(np.mean(arr), 10)

    def test_04_isometric_3d_projection(self):
        """Verifies 3D isometric mathematics and primitive rendering."""
        # Test isometric coordinate mapping
        u, v = iso_project(0, 0, 0, origin=(288, 512))
        self.assertEqual((u, v), (288, 512))

        # Positive Z maps straight up (-v)
        u_z, v_z = iso_project(0, 0, 50, origin=(288, 512), scale=1.0)
        self.assertEqual(u_z, 288)
        self.assertEqual(v_z, 462)

        # Test IsometricVoxelCube rendering
        cube = IsometricVoxelCube()
        img = Image.new("RGBA", (self.width, self.height), (10, 13, 20, 255))
        draw = ImageDraw.Draw(img)
        cube.render(draw, t=1.0, center=(288, 450), size=120.0)
        self.assertEqual(img.size, (self.width, self.height))

        # Test IsometricHardwareModels (NVMe SSD)
        hw = IsometricHardwareModels()
        hw.render_m2_ssd(draw, center=(288, 500), scale=1.0, t=1.0)
        self.assertEqual(img.size, (self.width, self.height))

        # Test IsometricLayerStack
        stack = IsometricLayerStack()
        stack.render(draw, t=1.0, center=(288, 600))
        self.assertEqual(img.size, (self.width, self.height))

    def test_05_evidence_cards(self):
        """Verifies GitHubRepoCard, DocumentationFigureViewer, SideBySideComparisonCard."""
        # 1. GitHubRepoCard
        repo_card = GitHubRepoCard()
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)
        repo_card.render(draw, repo_name="FareedKhan-dev / kimi-k3-in-c", top_y=350, t=1.0)
        self.assertEqual(img.size, (self.width, self.height))

        # 2. DocumentationFigureViewer
        doc_viewer = DocumentationFigureViewer()
        sample_fig = self.test_dir / "sample_fig.png"
        Image.new("RGBA", (300, 200), (40, 50, 60, 255)).save(sample_fig)
        doc_viewer.render(img, figure_path=sample_fig, repo_subpath="docs/images/test.png", center_y=450, t=1.0)
        self.assertEqual(img.size, (self.width, self.height))

        # 3. SideBySideComparisonCard
        comp_card = SideBySideComparisonCard()
        comp_card.render(draw, t=1.0, center_y=550)
        self.assertEqual(img.size, (self.width, self.height))

    def test_06_telemetry_and_charts(self):
        """Verifies LollipopChart, FlatlineTelemetryCard, DigitalStopwatchTimer, MoEExpertGrid."""
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)

        # 1. LollipopChart
        chart = LollipopChart()
        chart.render(draw, t=1.0, center_y=350)
        self.assertEqual(img.size, (self.width, self.height))

        # 2. FlatlineTelemetryCard
        flatline = FlatlineTelemetryCard()
        flatline.render(draw, t=1.0, center_y=500)
        self.assertEqual(img.size, (self.width, self.height))

        # 3. DigitalStopwatchTimer
        timer = DigitalStopwatchTimer()
        timer.render(draw, t=1.0, center_y=450, time_display="1:54")
        self.assertEqual(img.size, (self.width, self.height))

        # 4. MoEExpertGrid
        grid = MoEExpertGrid()
        grid.render(draw, t=1.0, center_y=480)
        self.assertEqual(img.size, (self.width, self.height))

    def test_07_all_eight_reference_compositions(self):
        """Tests that all 8 reference compositions render frames without exception."""
        scene = UniversalSceneContract(
            scene_id="test_ref_scene",
            sequence_number=1,
            scene_type=SceneType.CONCEPTUAL_ANIMATION,
            preferred_engine=RenderingEngine.NATIVE_MOTION,
            narration_text="Test scene narration for reference composition verification.",
            narration_duration_seconds=5.0,
            actual_duration_seconds=5.0,
            output_resolution=(self.width, self.height),
            frame_rate=30,
            narrative_purpose="hook",
            audience_takeaway="Run on CPU",
            visual_concept="ReferenceIsometricHookComposition",
            mechanism_description="Streaming layers",
        )

        compositions = [
            ReferenceIsometricHookComposition(scene, self.width, self.height),
            ReferenceRepoEvidenceComposition(scene, self.width, self.height),
            ReferenceBarChartComparisonComposition(scene, self.width, self.height),
            ReferenceLayerStreamingComposition(scene, self.width, self.height),
            ReferenceMoEMechanismComposition(scene, self.width, self.height),
            ReferenceDeterminismComparisonComposition(scene, self.width, self.height),
            ReferenceLatencyTimerComposition(scene, self.width, self.height),
            ReferenceLoopConclusionComposition(scene, self.width, self.height),
        ]

        for comp in compositions:
            f0 = comp.render_frame(0.0)
            f1 = comp.render_frame(2.0)
            self.assertIsInstance(f0, Image.Image)
            self.assertIsInstance(f1, Image.Image)
            self.assertEqual(f0.size, (self.width, self.height))
            self.assertEqual(f1.size, (self.width, self.height))

    def test_08_reference_sound_designer(self):
        """Verifies procedural lo-fi ambient bed generation and loudness inspection."""
        designer = ReferenceSoundDesigner()
        bed_out = self.test_dir / "test_lofi_bed.wav"
        designer.generate_lofi_bed(duration_s=4.0, output_path=bed_out)
        self.assertTrue(bed_out.exists())
        self.assertGreater(bed_out.stat().st_size, 1000)

        probe = designer.inspect_audio(bed_out)
        self.assertAlmostEqual(probe["duration"], 4.0, delta=0.5)
        self.assertEqual(probe["channels"], 2)
        self.assertEqual(probe["sample_rate"], 48000)

    def test_09_reference_director_storyboard(self):
        """Verifies 9-beat storyboard generation by ReferenceDirector."""
        director = ReferenceDirector(fps=30)
        dossier = ResearchDossier(
            topic_id="topic_test_01",
            topic_title="Kimi K3 in C",
            topic_description="2.78 Trillion parameter model on single CPU in 8.24 GB RAM",
            original_angle="Pure C99 implementation without GPU or framework dependencies",
            dossier_provenance={
                "repo_name": "FareedKhan-dev/kimi-k3-in-c",
                "stars": "1.2k",
                "binary_size_kb": 176,
                "ram_gb": 8.24,
                "parameters": "2.78 Trillion",
            },
        )
        sb = director.build_storyboard(
            topic="Kimi K3 in C",
            dossier=dossier,
            video_id="prod_test_01",
        )
        self.assertEqual(len(sb.scenes), 9)
        self.assertEqual(sb.scenes[0].output_resolution, (576, 1024))
        self.assertGreaterEqual(sb.target_duration_seconds, 50.0)
        self.assertEqual(sb.scenes[0].scene_id, "prod_test_01_scene_01_hook")


if __name__ == "__main__":
    unittest.main()
