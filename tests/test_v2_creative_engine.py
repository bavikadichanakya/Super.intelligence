"""
SUPER.INTELLIGENCEEE V2 — Creative Engine Redesign Test Suite
Verifies:
1. SceneCreativeBrief data structures and serialization.
2. VisualIntelligenceEngine narrative-to-visual decoupled planning.
3. ProductionModeDispatcher rendering distinct 1080x1920 assets for all modes.
4. AssetProvenanceManifest cryptographic hashing and tracking.
5. VisualQASubsystem luminance, perceptual diversity, and contact sheet generation.
"""

import json
from pathlib import Path
import pytest
from PIL import Image

from core.creative_brief import (
    CameraMovement,
    CompositionLayout,
    ProductionMode,
    SceneCreativeBrief,
    ReelCreativePlan,
)
from core.provenance import (
    AssetProvenanceManifest,
    AssetProvenanceRecord,
    LicenseType,
)
from visuals.visual_intelligence import VisualIntelligenceEngine
from visuals.production_modes import ProductionModeDispatcher
from rendering.visual_qa import VisualQASubsystem


def test_creative_brief_serialization():
    brief = SceneCreativeBrief(
        scene_id="sc_001",
        scene_index=1,
        narrative_purpose="HOOK",
        intended_emotion="AWE",
        visual_metaphor="EXPANDING_HORIZON",
        primary_subject="NEURAL_CORE",
        visual_action="PULSING_LATTICE",
        production_mode=ProductionMode.ORIGINAL_MOTION_GRAPHICS,
        asset_requirements=["particles.mp4"],
        composition=CompositionLayout.MACRO_CENTER_HERO,
        camera_movement=CameraMovement.PUSH_IN_SLOW,
        animation_instructions="Slow continuous zoom",
        duration_seconds=5.2,
        on_screen_text="10X SPEEDUP",
        factual_claims_represented=["Claim 1"],
        visual_concept_rationale="Visually shows core",
    )
    d = brief.to_dict()
    assert d["production_mode"] == "original_motion_graphics"
    assert d["composition"] == "macro_center_hero"
    assert d["camera_movement"] == "push_in_slow"

    # Reconstitute
    reconstructed = SceneCreativeBrief.from_dict(d)
    assert reconstructed.production_mode == ProductionMode.ORIGINAL_MOTION_GRAPHICS
    assert reconstructed.composition == CompositionLayout.MACRO_CENTER_HERO
    assert reconstructed.duration_seconds == 5.2


def test_visual_intelligence_planning():
    engine = VisualIntelligenceEngine()
    topic = {
        "id": 99,
        "title": "Sub-Quadratic Attention Scaled to 1M Tokens",
        "category": "Artificial Intelligence",
        "summary": "Researchers achieve linear scaling across 1M context with 4.2x speedup.",
    }
    storyboard = {
        "scenes": [
            {"scene_index": 1, "narrative_role": "HOOK", "narration": "Million token context is now real."},
            {"scene_index": 2, "narrative_role": "CONTEXT", "narration": "Transformers hit O(N^2) memory bottlenecks."},
            {"scene_index": 3, "narrative_role": "DEVELOPMENT", "narration": "Sub-quadratic attention changes the game."},
            {"scene_index": 4, "narrative_role": "EXPLANATION", "narration": "Here is the internal kernel routing architecture."},
            {"scene_index": 5, "narrative_role": "IMPLICATIONS", "narration": "Running on a single consumer RTX 4090."},
            {"scene_index": 6, "narrative_role": "LIMITATIONS", "narration": "Only works on specialized sparse kernels currently."},
            {"scene_index": 7, "narrative_role": "TAKEAWAY", "narration": "Follow for more daily AI breakthroughs."},
        ]
    }
    plan = engine.plan_reel_creative(topic, storyboard)
    assert len(plan.scenes) == 7
    # Verify diversity of production modes: at least 3 distinct modes in 7 scenes
    distinct_modes = {s.production_mode for s in plan.scenes}
    assert len(distinct_modes) >= 3


def test_production_modes_dispatch_all_modes(tmp_path):
    dispatcher = ProductionModeDispatcher()
    manifest = AssetProvenanceManifest(manifest_id="test_manifest", reel_slug="test_reel")

    modes_to_test = [
        ProductionMode.ORIGINAL_MOTION_GRAPHICS,
        ProductionMode.SPLIT_SCREEN_COMPARISON,
        ProductionMode.DATA_VISUALIZATION,
        ProductionMode.ANIMATED_TECHNICAL_DIAGRAM,
        ProductionMode.INTERFACE_WALKTHROUGH,
        ProductionMode.EDITORIAL_TYPOGRAPHY,
    ]

    for idx, mode in enumerate(modes_to_test):
        brief = SceneCreativeBrief(
            scene_id=f"test_{idx}",
            scene_index=idx + 1,
            narrative_purpose="EXPLANATION",
            intended_emotion="CLARITY",
            visual_metaphor="BENCHMARK",
            primary_subject="NEURAL_SYSTEM",
            visual_action="DATA_FLOW",
            production_mode=mode,
            asset_requirements=[],
            composition=CompositionLayout.MACRO_CENTER_HERO,
            camera_movement=CameraMovement.PUSH_IN_SLOW,
            animation_instructions="",
            duration_seconds=5.0,
            on_screen_text=f"MODE {mode.value}",
        )
        out_img = tmp_path / f"mode_{idx}.png"
        res = dispatcher.dispatch_scene_visual(brief, out_img, manifest=manifest)
        assert res.exists()
        assert res.stat().st_size > 10000

        with Image.open(res) as im:
            assert im.size == (1080, 1920)

    # Verify manifest recorded all assets
    assert len(manifest.records) == len(modes_to_test)
    for rec in manifest.records:
        assert len(rec.sha256_hash) == 64
        assert rec.file_size_bytes > 10000


def test_visual_qa_subsystem_checks(tmp_path):
    qa = VisualQASubsystem()

    # 1. Create a pitch black dummy image and verify black frame check flags it
    black_img_path = tmp_path / "black.png"
    Image.new("RGB", (1080, 1920), (0, 0, 0)).save(black_img_path)

    bf_pass, bf_issues = qa.check_black_frames([(0.0, black_img_path)])
    assert bf_pass is False
    assert len(bf_issues) == 1
    assert "Solid black or near-zero luminance" in bf_issues[0]["issue"]

    # 2. Create normal bright high-aesthetic images and verify they pass
    normal_img_1 = tmp_path / "normal_1.png"
    normal_img_2 = tmp_path / "normal_2.png"
    im1 = Image.new("RGB", (1080, 1920), (30, 40, 60))
    im2 = Image.new("RGB", (1080, 1920), (180, 120, 40))
    im1.save(normal_img_1)
    im2.save(normal_img_2)

    bf_pass2, _ = qa.check_black_frames([(1.0, normal_img_1), (2.0, normal_img_2)])
    assert bf_pass2 is True

    # 3. Test perceptual diversity: identical frames should flag duplicate warning
    pd_fail, pd_issues = qa.check_perceptual_diversity([(1.0, normal_img_1), (2.0, normal_img_1)], max_similarity=0.95)
    assert pd_fail is False
    assert len(pd_issues) >= 1

    # Distinct frames should pass
    pd_pass, pd_issues_2 = qa.check_perceptual_diversity([(1.0, normal_img_1), (2.0, normal_img_2)])
    assert pd_pass is True

    # 4. Test contact sheet generation
    cs_out = tmp_path / "contact_sheet.png"
    cs_res = qa.generate_contact_sheet(
        frame_items=[(1.0, normal_img_1), (2.0, normal_img_2)],
        output_path=cs_out,
        title="TEST CONTACT SHEET",
        labels=["SCENE 1", "SCENE 2"]
    )
    assert cs_res.exists()
    assert cs_res.stat().st_size > 5000

