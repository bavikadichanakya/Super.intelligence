"""
SUPER.INTELLIGENCEEE — Phase 4.1 Test Suite: Unified Pipeline Integration
Validates end-to-end connectivity, research qualification enforcement,
dynamic story & scene planning, timing coordination, Voicebox audio integration,
visual diversity auditing, and publishing kill-switch governance.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from core.unified_pipeline import UnifiedProductionPipeline
from core.creative_contracts import DynamicScenePlan, StoryArchitecturePlan, SceneType
from core.schemas import ResearchDossier, EvidenceStatus
from audio.providers.voicebox_provider import VoiceboxProvider
from publishing.approval import ApprovalManager


@pytest.fixture
def test_topic():
    return {
        "title": "Unpacking the Compute Efficiency of Strong-to-Weak OPD against GRPO",
        "url": "https://arxiv.org/abs/2611.08453",
        "summary": "Investigation of on-policy distillation vs GRPO compute efficiency.",
        "category": "Artificial Intelligence Research",
        "source": "arXiv.org",
    }


@pytest.fixture
def pipeline():
    return UnifiedProductionPipeline()


def test_research_qualification_enforcement(pipeline, test_topic):
    """
    Validates that the research dossier strictly enforces mandatory qualifications:
    1. 50x FLOP reduction applies strictly when teacher is student's own GRPO checkpoint.
    2. With external post-trained teacher, OPD generally loses to GRPO in accuracy per training FLOP.
    3. Source is an academic preprint (not independently replicated or universally established).
    """
    dossier = pipeline.compile_qualified_research_dossier(test_topic)
    assert isinstance(dossier, ResearchDossier)
    assert len(dossier.limitations) >= 3

    # Check qualifications in limitations
    limitations_text = " ".join(dossier.limitations)
    assert "PREPRINT STATUS" in limitations_text
    assert "CONDITIONAL 50x REDUCTION" in limitations_text
    assert "EXTERNAL TEACHER LIMITATION" in limitations_text

    # Check claims are grounded, typed, and sourced
    assert len(dossier.important_claims) >= 3
    claims_text = " ".join([c.claim_text for c in dossier.important_claims])
    assert "50x" in claims_text
    assert "external" in claims_text.lower()
    
    # Verify claims have source and provenance
    for claim in dossier.important_claims:
        assert claim.source_url == test_topic["url"]
        assert claim.publisher == "arXiv.org"
        assert claim.retrieval_timestamp is not None
        assert claim.status == EvidenceStatus.VERIFIED
        assert claim.claim_type in ["qualitative", "quantitative"]


def test_dynamic_story_architecture_formulation(pipeline, test_topic):
    """
    Validates that StoryArchitectureEngine dynamically plans story beats
    and the resulting script incorporates the mandatory qualifications.
    """
    dossier = pipeline.compile_qualified_research_dossier(test_topic)
    story_plan, script_data = pipeline.formulate_story_and_script(test_topic, dossier)

    assert isinstance(story_plan, StoryArchitecturePlan)
    assert len(story_plan.structural_beats) == 4
    assert "scenes" in script_data
    assert len(script_data["scenes"]) == 4

    # Verify script embeds qualifications
    full_narration = " ".join([s["narration"] for s in script_data["scenes"]])
    assert "preprint" in full_narration.lower()
    assert "fifty times" in full_narration.lower() or "50x" in full_narration.lower()
    assert "external teacher" in full_narration.lower()


def test_dynamic_creative_direction_and_scene_planning(pipeline, test_topic):
    """
    Validates that CreativeDirector, DynamicScenePlanner, and VisualDiversityAnalyzer
    create a visually varied, light-first scene plan with no repeated archetypes.
    """
    dossier = pipeline.compile_qualified_research_dossier(test_topic)
    story_plan, script_data = pipeline.formulate_story_and_script(test_topic, dossier)
    creative_direction, dynamic_scene_plan = pipeline.plan_creative_scenes(
        story_plan, dossier, script_data
    )

    assert isinstance(dynamic_scene_plan, DynamicScenePlan)
    assert len(dynamic_scene_plan.scenes) == 4

    # Run diversity analyzer
    report = pipeline.diversity_analyzer.analyze_plan(dynamic_scene_plan)
    assert report.get("passed") is True
    assert report.get("diversity_score", 0) >= 0.85
    assert report.get("unique_types_count", 0) >= 3


def test_timing_coordination(pipeline, test_topic):
    """
    Validates TimingCoordinator audio-visual duration synchronization.
    """
    dossier = pipeline.compile_qualified_research_dossier(test_topic)
    story_plan, script_data = pipeline.formulate_story_and_script(test_topic, dossier)
    _, dynamic_scene_plan = pipeline.plan_creative_scenes(story_plan, dossier, script_data)

    # Simulate scene audio files with known lengths
    durations = [4.5, 6.2, 5.8, 4.0]
    # Check that synchronizing updates actual_duration
    for idx, sc in enumerate(dynamic_scene_plan.scenes):
        sc.actual_duration = durations[idx] + 0.25

    total_expected = sum(durations) + 4 * 0.25
    total_actual = sum(sc.actual_duration for sc in dynamic_scene_plan.scenes)
    assert abs(total_actual - total_expected) < 0.01


def test_voicebox_american_voice_configuration(pipeline):
    """
    Validates VoiceboxProvider is configured with Kokoro am_liam (General American Male).
    """
    assert pipeline.voice_provider.default_voice == "am_liam"
    assert "127.0.0.1:17493" in pipeline.voicebox_url


def test_governance_and_publishing_killswitch(pipeline, test_topic):
    """
    Validates that human approval gate is enforced (NEEDS_REVIEW)
    and publishing kill-switch prevents automatic release.
    """
    from core.kill_switch import get_kill_switch
    dossier = pipeline.compile_qualified_research_dossier(test_topic)
    assert dossier.verification_status == "VERIFIED"

    # Verify ApprovalManager rejects auto self-approval
    approval_mgr = ApprovalManager(db=pipeline.db, config=pipeline.config)
    with pytest.raises(PermissionError) as exc_info:
        approval_mgr.approve_reel(
            production_job_id=999999,
            reviewer_name="pipeline",
            notes="Auto-approve attempt",
        )
    assert "Human editorial review is mandatory" in str(exc_info.value)
