"""
SUPER.INTELLIGENCEEE — Phase 1 Editorial Intelligence Test Suite
Verifies:
1. 100-Point Transparent Topic Scoring Matrix
2. Structured ResearchDossier Compilation
3. RESEARCH_BLOCKED enforcement on ungrounded sources
4. Claim-Level Fact Verification against Primary Evidence
5. Anti-Self-Approval Enforcement
6. Unsupported Metric Hallucination Detection
7. Dossier Context Integration into Script Generation
8. Governed Editorial Workflow State Machine
"""

import pytest
from core.schemas import (
    ClaimEvidence,
    ContentBrief,
    EditorialWorkflowState,
    EvidenceStatus,
    ResearchDossier,
    Source,
    TopicScoreBreakdown,
)
from research.topic_scorer import TopicScorer
from research.research_analyst import ResearchAnalyst
from content.fact_checker import FactChecker
from intelligence.fallback_templates import FallbackTemplates


def test_100_point_scoring_matrix_criteria_and_thresholds():
    """Validates the 6 transparent scoring criteria and threshold decision boundaries."""
    # High-depth technical topic with primary paper
    high_topic = {
        "title": "Sub-Quadratic Attention Scaling with State Space Kernel Optimization",
        "summary": "AI researchers demonstrated linear memory scaling across million-token contexts, unlocking real-time inference on consumer hardware with zero accuracy degradation.",
        "url": "https://arxiv.org/abs/2405.12345",
        "publisher": "arXiv Preprint",
        "published_date": "2026-11-05",
        "category": "Artificial Intelligence",
    }
    scorer = TopicScorer()
    breakdown = scorer.score_100_points(high_topic)

    assert isinstance(breakdown, TopicScoreBreakdown)
    assert breakdown.information_value > 15.0, "High technical keyword density should score high info value"
    assert breakdown.evidence_quality == 20.0, "arXiv URLs must receive full 20 pts evidence quality"
    assert breakdown.total_score >= 80.0, f"Expected HIGH_PRIORITY >= 80, got {breakdown.total_score}"
    assert breakdown.decision == "HIGH_PRIORITY"

    # Shallow / speculative topic with low evidence
    low_topic = {
        "title": "This Insane AI Mind-Blowing Trick Could Change Everything",
        "summary": "You won't believe what happens next when you prompt this chatbot.",
        "url": "http://random-blog.xyz/post",
        "publisher": "Tech Gossip Blog",
        "category": "General Tech",
    }
    low_breakdown = scorer.score_100_points(low_topic)
    assert low_breakdown.total_score < 50.0, f"Expected REJECT < 50, got {low_breakdown.total_score}"
    assert low_breakdown.decision == "REJECT"


def test_research_analyst_builds_dossier():
    """Validates compiling a structured ResearchDossier from primary source documentation."""
    analyst = ResearchAnalyst()
    topic = {
        "id": "TOPIC_TEST_001",
        "title": "Quantized INT4 Kernel Accelerates Local Transformer Inference by 4.2x",
        "summary": "Engineers developed custom fused CUDA kernels enabling INT4 weight-only quantization. Across Llama-3 70B benchmarks, latency dropped by 65% with 4.2x throughput speedup on RTX 4090 GPUs.",
        "url": "https://github.com/super-intelligence/int4-fused-kernel",
        "publisher": "Open Source Labs",
        "published_date": "2026-11-06T10:00:00Z",
    }

    dossier = analyst.build_dossier(topic)
    assert isinstance(dossier, ResearchDossier)
    assert dossier.topic_id == "TOPIC_TEST_001"
    assert dossier.verification_status == "VERIFIED"
    assert len(dossier.primary_sources) >= 1
    assert len(dossier.important_claims) >= 1
    assert len(dossier.limitations) >= 1
    assert len(dossier.visual_opportunities) >= 1
    assert dossier.suggested_creative_format == "tech_documentary"

    # Check that claims contain extracted metrics
    claims_text = " ".join([c.claim_text for c in dossier.important_claims])
    assert "4.2x" in claims_text or "65%" in claims_text


def test_research_blocked_on_empty_or_unreachable_source():
    """Enforces that topics without accessible primary evidence enter RESEARCH_BLOCKED status."""
    analyst = ResearchAnalyst()
    empty_topic = {
        "id": "TOPIC_EMPTY",
        "title": "Unsubstantiated Rumor About Frontier Silicon",
        "summary": "",
        "url": "",  # Missing URL
    }

    dossier = analyst.build_dossier(empty_topic)
    assert dossier.verification_status == "RESEARCH_BLOCKED"
    assert "Research blocked" in dossier.original_angle


def test_fact_checker_evaluates_against_dossier():
    """Validates that FactChecker checks claims against the deep ResearchDossier."""
    analyst = ResearchAnalyst()
    topic = {
        "id": "TOPIC_FACT_001",
        "title": "Pruning Transformer Weights Reduces VRAM Footprint by 50%",
        "summary": "Structural pruning techniques demonstrated a 50% reduction in peak VRAM consumption on 24GB GPUs while preserving 98% accuracy on standard benchmarks.",
        "url": "https://super.intelligenceee.local/pruning",
        "publisher": "Benchmark Institute",
    }
    dossier = analyst.build_dossier(topic)

    # Legitimate grounded script
    script_data = {
        "title": topic["title"],
        "hook": "Engineers just cut model memory overhead in half.",
        "context": "Published by Benchmark Institute, this pruning milestone targets consumer deployment.",
        "development": "Tests show a 50% reduction in peak VRAM consumption while preserving 98% accuracy.",
        "explanation": "By structurally removing non-essential weight matrices, the model streamlines tensor calculations.",
        "implications": "For developers, this means running large models on consumer 24GB GPUs.",
        "limitations": "However, fine-tuning recovery steps are required after aggressive pruning passes.",
        "takeaway": "Weight efficiency is turning previously inaccessible models into practical local assets.",
        "source_url": topic["url"],
    }

    fc = FactChecker()
    res = fc.check_script(script_data, dossier=dossier)
    assert res["verified"] is True
    assert len(res["issues"]) == 0


def test_fact_checker_blocks_research_blocked_dossier():
    """Validates that a script referencing a RESEARCH_BLOCKED dossier is strictly rejected."""
    blocked_dossier = ResearchDossier(
        topic_id="BLOCKED_01",
        topic_title="Fake News Breakthrough",
        topic_description="Missing sources",
        original_angle="Blocked",
        verification_status="RESEARCH_BLOCKED",
    )

    script_data = {
        "title": "Fake News Breakthrough",
        "hook": "Everything is solved.",
        "source_url": "https://example.com/fake",
    }

    fc = FactChecker()
    res = fc.check_script(script_data, dossier=blocked_dossier)
    assert res["verified"] is False
    assert any("RESEARCH_BLOCKED" in issue for issue in res["issues"])


def test_fact_checker_rejects_self_approval():
    """Validates that script writer cannot self-verify claims."""
    script_data = {
        "title": "Autonomous Verification Bypass Attempt",
        "hook": "We verified ourselves without human review.",
        "source_url": "https://super.intelligenceee.local/test",
        "self_verified": True,  # Illicit self-approval flag
    }

    fc = FactChecker()
    res = fc.check_script(script_data)
    assert res["verified"] is False
    assert any("Script writer cannot mark its own claims as verified" in issue for issue in res["issues"])


def test_fact_checker_catches_unsupported_metrics():
    """Validates that hallucinated or unsubstantiated metrics are flagged as UNSUPPORTED."""
    topic = {
        "title": "Transformer Attention Optimization",
        "summary": "Researchers demonstrated algorithmic optimizations for attention layers.",
        "url": "https://super.intelligenceee.local/attention",
    }
    # Script invents a metric "99.9% faster" and "100x" not present in the topic
    script_data = {
        "title": topic["title"],
        "hook": "This model is 99.9% faster than any prior implementation.",
        "development": "Benchmarks show a massive 100x multiplier in processing speed.",
        "source_url": topic["url"],
    }

    fc = FactChecker()
    res = fc.check_script(script_data)
    assert res["verified"] is False
    assert any("Ungrounded quantitative claim" in issue for issue in res["issues"])
    unsupported_claims = [c for c in res["claims"] if c.get("status") == "UNSUPPORTED"]
    assert len(unsupported_claims) >= 1


def test_fallback_templates_uses_dossier_context():
    """Validates that FallbackTemplates incorporates research dossier insights instead of generic boilerplate."""
    dossier = ResearchDossier(
        topic_id="TOPIC_INT",
        topic_title="Sub-Quadratic Memory Scaling",
        topic_description="Linear attention mechanics",
        original_angle="Technical breakdown",
        technical_explanation="The architecture decouples key-value projection from sequence length using recurrent states.",
        limitations=["Recurrent state compression limits exact verbatim retrieval on needles."],
        potential_implications=["Enables million-token context processing on edge workstations with zero memory explosion."],
    )

    article = {
        "title": "Sub-Quadratic Memory Scaling",
        "summary": "Linear attention mechanics unlock long contexts.",
        "publisher": "Research Lab",
        "url": "https://arxiv.org/abs/2405.0001",
    }

    script = FallbackTemplates.generate_script(article, dossier=dossier)
    assert "recurrent states" in script["explanation"]
    assert "million-token context" in script["implications"]
    assert "needle" in script["limitations"].lower()


def test_editorial_workflow_state_enum():
    """Validates full state representation of the editorial operating system."""
    expected_states = {
        "DISCOVERED", "SCORING", "RESEARCHING", "RESEARCH_VERIFIED", "RESEARCH_BLOCKED",
        "BRIEF_APPROVED", "SCRIPT_READY", "CREATIVE_PLAN_READY", "ASSETS_READY",
        "ASSET_REQUIRED", "LICENSING_REVIEW", "PRODUCING", "QA_PENDING", "QA_FAILED",
        "NEEDS_REVIEW", "REVISION_REQUIRED", "HELD_BY_OWNER", "APPROVED", "PUBLISHED",
        "ANALYZED", "REJECTED"
    }
    actual_states = {s.value for s in EditorialWorkflowState}
    assert expected_states.issubset(actual_states)
