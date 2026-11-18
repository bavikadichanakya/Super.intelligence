import pytest
from pathlib import Path
import json

from core.content_intelligence.performance_diagnostics import (
    AccountBaselineCalculator,
    OFFICIAL_METRIC_DEFINITIONS,
    CAUSATION_DISCLAIMER
)
from core.content_intelligence.opening_quality_gate import (
    OpeningQualityGate,
    OpeningConcept,
    OpeningConceptType
)
from publishing.youtube_integration import (
    YouTubeVisibility,
    VISIBILITY_DESCRIPTIONS,
    validate_visibility_selection
)

def test_account_baseline_insufficient_data():
    # Less than 5 snapshots
    snapshots = [
        {"views": 100, "skip_rate": 0.60, "avg_watch_time": 4.5, "reach": 90, "duration": 45.0},
        {"views": 150, "skip_rate": 0.55, "avg_watch_time": 5.2, "reach": 130, "duration": 50.0},
    ]
    result = AccountBaselineCalculator.calculate_baselines(snapshots)
    assert result["status"] == "INSUFFICIENT_BASELINE_DATA"
    assert result["sample_size"] == 2
    assert result["required_minimum"] == 5
    assert "disclaimer" in result

def test_account_baseline_sufficient_data():
    snapshots = [
        {"views": 100, "skip_rate": 0.60, "avg_watch_time": 4.5, "reach": 90, "video_length": 45.0, "content_pillar": "deep_tech", "retention_pct": 50.0, "shares": 2},
        {"views": 150, "skip_rate": 0.55, "avg_watch_time": 5.2, "reach": 130, "video_length": 50.0, "content_pillar": "deep_tech", "retention_pct": 52.0, "shares": 5},
        {"views": 200, "skip_rate": 0.50, "avg_watch_time": 6.0, "reach": 180, "video_length": 40.0, "content_pillar": "agentic_ai", "retention_pct": 60.0, "shares": 10},
        {"views": 120, "skip_rate": 0.65, "avg_watch_time": 4.0, "reach": 110, "video_length": 60.0, "content_pillar": "deep_tech", "retention_pct": 45.0, "shares": 1},
        {"views": 180, "skip_rate": 0.52, "avg_watch_time": 5.8, "reach": 160, "video_length": 45.0, "content_pillar": "agentic_ai", "retention_pct": 55.0, "shares": 8},
    ]
    result = AccountBaselineCalculator.calculate_baselines(snapshots)
    assert result["status"] == "VALID_BASELINE"
    assert result["sample_size"] == 5
    assert result["metrics"]["views"]["median"] == 150
    assert result["metrics"]["skip_rate"]["median"] == 0.55
    assert "segmentation" in result
    assert "by_pillar_counts" in result["segmentation"]
    assert "deep_tech" in result["segmentation"]["by_pillar_counts"]

def test_official_metric_definitions_exist():
    assert "reels_skip_rate" in OFFICIAL_METRIC_DEFINITIONS
    assert "ig_reels_avg_watch_time" in OFFICIAL_METRIC_DEFINITIONS
    assert "views" in OFFICIAL_METRIC_DEFINITIONS
    assert "STATISTICAL INTEGRITY NOTICE" in CAUSATION_DISCLAIMER

def test_youtube_visibility_options():
    assert len(VISIBILITY_DESCRIPTIONS) == 4
    assert "private" in VISIBILITY_DESCRIPTIONS
    assert "unlisted" in VISIBILITY_DESCRIPTIONS
    assert "public" in VISIBILITY_DESCRIPTIONS
    assert "scheduled" in VISIBILITY_DESCRIPTIONS
    assert VISIBILITY_DESCRIPTIONS["private"]["enters_recommendations"] is False
    assert VISIBILITY_DESCRIPTIONS["public"]["enters_recommendations"] is True

def test_youtube_visibility_validation():
    # Private succeeds without explicit confirmation
    spec = validate_visibility_selection("private", explicit_owner_confirmation=False)
    assert spec["visibility"] == "private"

    # Public requires explicit confirmation
    with pytest.raises(PermissionError):
        validate_visibility_selection("public", explicit_owner_confirmation=False)

    spec_pub = validate_visibility_selection("public", explicit_owner_confirmation=True)
    assert spec_pub["visibility"] == "public"

    # Invalid visibility raises ValueError
    with pytest.raises(ValueError):
        validate_visibility_selection("invalid_mode")

def test_opening_quality_gate_linting():
    gate = OpeningQualityGate()
    
    # Passing hook concept
    valid_concept = OpeningConcept(
        concept_id="OP_TEST_1",
        concept_type=OpeningConceptType.RESULT_FIRST,
        headline="740 TFLOPS ON H100 SILICON",
        first_frame_visual="Split benchmark diagram with active GPU register telemetry",
        first_spoken_sentence="FlashAttention-3 unlocks 740 teraflops on H100 silicon.",
        on_screen_hook="740 TFLOPS ON H100",
        first_visual_action="Immediate dynamic counter jumps to 740 TFLOPs in 0.5 seconds",
        expected_audience_curiosity="How does attention achieve 75% hardware utilization?",
        promised_payoff="Understand asynchronous warp specialization by second 30",
        supporting_evidence="arXiv:2407.08608 Section 4 Hardware Benchmark"
    )
    passed, violations = gate.lint_opening_concept(valid_concept)
    assert passed is True
    assert len(violations) == 0

    # Failing hook with rhetorical question and static title card
    invalid_concept = OpeningConcept(
        concept_id="OP_TEST_2",
        concept_type=OpeningConceptType.RESULT_FIRST,
        headline="WHY GPUS ARE SLOW",
        first_frame_visual="Static title card with dark background",
        first_spoken_sentence="Have you ever heard why GPUs run out of memory?",
        on_screen_hook="WHY GPUS RUN OUT OF MEMORY FAST",
        first_visual_action="No movement for first 3 seconds",
        expected_audience_curiosity="None",
        promised_payoff="None",
        supporting_evidence=""
    )
    passed_bad, violations_bad = gate.lint_opening_concept(invalid_concept)
    assert passed_bad is False
    assert any("Rhetorical question opener" in v for v in violations_bad)
    assert any("Static title slides" in v for v in violations_bad)

def test_opening_quality_gate_alternatives_generation():
    gate = OpeningQualityGate()
    candidates = gate.generate_candidate_openings(
        topic="FlashAttention-3",
        hero_metric="740 TFLOPs/s",
        technical_mechanism="Asynchronous warp specialization",
        conventional_dogma="GPUs spend 80% of clock cycles waiting for memory",
        evidence_citation="arXiv:2407.08608 Shah et al. 2024"
    )
    
    assert len(candidates) == 3
    types = [c.concept_type for c in candidates]
    assert OpeningConceptType.RESULT_FIRST in types
    assert OpeningConceptType.MECHANISM_FIRST in types
    assert OpeningConceptType.UNEXPECTED_CONTRAST in types
    
    # All generated concepts must pass the linter
    for c in candidates:
        passed, violations = gate.lint_opening_concept(c)
        assert passed is True, f"Generated concept failed linter: {violations}"

def test_flashattention3_production_manifest_and_video():
    manifest_path = Path("output/drafts/flashattention3_documentary/publishing_manifest.json")
    assert manifest_path.exists(), "Production manifest must exist"
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    assert manifest["stable_topic_id"] == "flashattention3_hopper"
    assert manifest["selected_opening_concept"] == "OP_CONCEPT_A_RESULT"
    assert manifest["status"] == "AWAITING_HUMAN_APPROVAL"
    assert manifest["youtube_package"]["visibility_default"] == "private"
    assert len(manifest["opening_concepts_evaluated"]) == 3

    master_mp4 = Path(manifest["output_video_path"])
    assert master_mp4.exists(), "Master MP4 file must exist"
    assert master_mp4.stat().st_size > 500_000, "Master MP4 must be > 500KB"

    contact_sheet = Path("output/drafts/flashattention3_documentary/flashattention3_forensic_contact_sheet.png")
    assert contact_sheet.exists(), "Forensic contact sheet must exist"
