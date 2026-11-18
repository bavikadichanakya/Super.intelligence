"""
SUPER.INTELLIGENCEEE V2 — Comprehensive Visual Engine & Quality Gate Test Suite
Tests UniversalScene schema, multi-archetype assignment, visual diversity,
visual routing, claim-level fact checking, and quality gate enforcement.
"""

import pytest
from pathlib import Path
from PIL import Image

from core.database import Database
from core.schemas import (
    ClaimEvidence,
    EvidenceStatus,
    SceneProps,
    UniversalScene,
    VisualArchetype,
)
from content.storyboard import StoryboardGenerator
from content.fact_checker import FactChecker
from visuals.visual_router import VisualRouter
from visuals.stock_provider import StockProvider
from video.video_validator import VideoValidator


# -------------------------------------------------------------
# 1. Universal Scene Schema Tests
# -------------------------------------------------------------
def test_universal_scene_schema_valid():
    scene = UniversalScene(
        scene_id="sc_001",
        scene_index=1,
        duration_seconds=4.5,
        narrative_role="HOOK",
        visual_archetype=VisualArchetype.SKETCH_TITLE,
        narration_text="Neural memory scaling breakthrough demonstrated.",
        on_screen_text="10X CONTEXT EXPANSION",
        visual_props=SceneProps(headline="10X CONTEXT EXPANSION", hero_word="10X"),
    )
    ok, errors = scene.validate()
    assert ok is True
    assert len(errors) == 0

    # Test legacy aliases
    assert scene.narration == "Neural memory scaling breakthrough demonstrated."
    assert scene.visual_type == "sketch_title"
    assert scene.scene_number == 1
    assert scene.duration == 4.5

    # Test export dictionary compatibility
    d = scene.to_dict()
    assert d["scene_index"] == 1
    assert d["scene_number"] == 1
    assert d["narration_text"] == scene.narration_text
    assert d["narration"] == scene.narration_text
    assert d["visual_archetype"] == "sketch_title"
    assert d["visual_type"] == "sketch_title"
    assert d["scene_type"] == "sketch_title"


def test_universal_scene_schema_validation_failures():
    # Empty scene_id and invalid duration
    invalid_scene = UniversalScene(
        scene_id="",
        scene_index=0,
        duration_seconds=-1.0,
        narrative_role="HOOK",
        visual_archetype=VisualArchetype.SKETCH_TITLE,
        narration_text="",
        on_screen_text="",
    )
    ok, errors = invalid_scene.validate()
    assert ok is False
    assert len(errors) >= 4
    assert any("scene_id" in e for e in errors)
    assert any("scene_index" in e for e in errors)
    assert any("duration" in e for e in errors)
    assert any("narration_text" in e for e in errors)


def test_universal_scene_from_legacy_dict():
    legacy_data = {
        "scene_number": 3,
        "name": "The Core Development",
        "narration": "Engineers achieved 3.8x inference throughput.",
        "on_screen_text": "3.8X SPEEDUP",
        "badge": "PERFORMANCE",
        "visual_type": "data_card",
        "duration": 4.8,
    }
    scene = UniversalScene.from_dict(legacy_data)
    assert scene.scene_index == 3
    assert scene.narration_text == "Engineers achieved 3.8x inference throughput."
    assert scene.duration_seconds == 4.8
    assert scene.visual_archetype == VisualArchetype.SKETCH_STAT
    assert scene.visual_props.hero_word != ""


# -------------------------------------------------------------
# 2. Storyboard Multi-Archetype Assignment & Diversity
# -------------------------------------------------------------
def test_storyboard_multi_archetype_assignment():
    test_script = {
        "title": "Autonomous Neural Pruning at 3.8x Speed",
        "publisher": "Synthetic AI Research Lab",
        "category": "Artificial Intelligence",
        "hook": "Engineers benchmarked an autonomous algorithmic pruning technique achieving 3.8x inference throughput.",
        "context": "Published via Synthetic AI Research Lab, this milestone solves peak VRAM allocation.",
        "development": "The architecture reduces peak VRAM allocation while preserving output fidelity.",
        "explanation": "Architecturally, this advance leverages refined algorithmic optimizations and focused data pipelines.",
        "implications": "For engineers and builders, this unlocks more efficient inference and reduced operational latency.",
        "limitations": "However, researchers note that edge-case stress testing is still underway.",
        "takeaway": "As frontier models evolve, efficiency and verified execution are becoming the real competitive moats.",
    }

    storyboard = StoryboardGenerator.generate_storyboard(test_script)
    assert len(storyboard) == 7

    archetypes = [s["visual_archetype"] for s in storyboard]
    unique_archetypes = set(archetypes)

    # 1. Must have at least 3 distinct archetypes
    assert len(unique_archetypes) >= 3, f"Insufficient diversity: {unique_archetypes}"

    # 2. No identical consecutive archetypes
    for i in range(1, len(archetypes)):
        assert archetypes[i] != archetypes[i - 1], f"Duplicate consecutive archetype at scene #{i+1}: {archetypes[i]}"

    # 3. Check props population
    stat_scene = next(s for s in storyboard if s["visual_archetype"] == "sketch_stat")
    assert "before" in stat_scene["visual_props"]
    assert "after" in stat_scene["visual_props"]

    diagram_scene = next(s for s in storyboard if s["visual_archetype"] == "motion_diagram")
    assert len(diagram_scene["visual_props"]["diagram_nodes"]) >= 3


# -------------------------------------------------------------
# 3. Claim-Level Fact Checking Tests
# -------------------------------------------------------------
def test_fact_checker_grounded_claims():
    fc = FactChecker()
    grounded_script = {
        "title": "Autonomous Neural Pruning at 3.8x Speed",
        "summary": "Engineers benchmarked an autonomous algorithmic pruning technique achieving 3.8x inference throughput.",
        "publisher": "Synthetic AI Research Lab",
        "source_url": "https://example.org/pruning",
        "hook": "Engineers benchmarked an autonomous algorithmic pruning technique achieving 3.8x inference throughput.",
        "sources": [{"publisher": "Synthetic Lab", "url": "https://example.org/pruning"}],
    }
    report = fc.check_script(grounded_script)
    assert report["verified"] is True
    assert len(report["issues"]) == 0
    assert report["evidence_summary"]["total_claims"] >= 1
    assert report["evidence_summary"]["verified"] >= 1
    assert report["evidence_summary"]["unsupported"] == 0


def test_fact_checker_unsupported_quantitative_metric():
    fc = FactChecker()
    unsupported_script = {
        "title": "Autonomous Neural Pruning at 3.8x Speed",
        "summary": "Engineers benchmarked an autonomous algorithmic pruning technique achieving 3.8x inference throughput.",
        "publisher": "Synthetic AI Research Lab",
        "source_url": "https://example.org/pruning",
        "hook": "Engineers achieved an unbelievable 99x inference throughput reduction.",
        "sources": [{"publisher": "Synthetic Lab", "url": "https://example.org/pruning"}],
    }
    report = fc.check_script(unsupported_script)
    assert report["verified"] is False
    assert any("99x" in issue for issue in report["issues"])
    assert report["evidence_summary"]["unsupported"] >= 1


def test_fact_checker_missing_source_url():
    fc = FactChecker()
    missing_source_script = {
        "title": "General AI Progress Report",
        "summary": "No source url provided.",
        "hook": "AI models are improving gradually.",
        "sources": [],
    }
    report = fc.check_script(missing_source_script)
    assert report["verified"] is False
    assert any("Missing primary source URL" in issue for issue in report["issues"])


# -------------------------------------------------------------
# 4. Visual Router & Stock Provider Dispatch Tests
# -------------------------------------------------------------
def test_visual_router_archetype_synthesis(tmp_path):
    db = Database(str(tmp_path / "test_vr.db"))
    router = VisualRouter(db=db)

    # 1. Sketch Title
    s_title = UniversalScene(
        scene_id="s1",
        scene_index=1,
        duration_seconds=4.0,
        narrative_role="HOOK",
        visual_archetype=VisualArchetype.SKETCH_TITLE,
        narration_text="Title narration",
        on_screen_text="AUTONOMOUS INFERENCE",
        visual_props=SceneProps(headline="AUTONOMOUS INFERENCE", hero_word="AUTONOMOUS"),
    )
    p1 = router.prepare_scene_visual(s_title, 1, 7, "vr_test")
    assert p1.exists()
    assert p1.suffix == ".png"
    with Image.open(p1) as im:
        assert im.size == (1080, 1920)

    # 2. Sketch Stat
    s_stat = UniversalScene(
        scene_id="s3",
        scene_index=3,
        duration_seconds=4.5,
        narrative_role="DEVELOPMENT",
        visual_archetype=VisualArchetype.SKETCH_STAT,
        narration_text="Stat narration",
        on_screen_text="3.8X SPEEDUP",
        visual_props=SceneProps(headline="3.8X SPEEDUP", stat_delta="3.8X"),
    )
    p3 = router.prepare_scene_visual(s_stat, 3, 7, "vr_test")
    assert p3.exists()

    # 3. Motion Diagram
    s_diag = UniversalScene(
        scene_id="s4",
        scene_index=4,
        duration_seconds=4.5,
        narrative_role="EXPLANATION",
        visual_archetype=VisualArchetype.MOTION_DIAGRAM,
        narration_text="Diagram narration",
        on_screen_text="PIPELINE FLOW",
    )
    p4 = router.prepare_scene_visual(s_diag, 4, 7, "vr_test")
    assert p4.exists()

    # Verify assets were registered in SQLite database
    assets = db.get_assets()
    assert len(assets) >= 3


# -------------------------------------------------------------
# 5. Technical Quality Gate Enforcement
# -------------------------------------------------------------
def test_video_validator_corrupt_file_rejection(tmp_path):
    validator = VideoValidator()
    fake_video = tmp_path / "corrupt.mp4"
    fake_video.write_bytes(b"NOT_A_REAL_MP4_HEADER")

    report = validator.validate_reel(fake_video)
    assert report["valid"] is False
    assert len(report["issues"]) > 0

