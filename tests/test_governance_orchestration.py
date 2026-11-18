"""
SUPER.INTELLIGENCEEE — Governance, Orchestration & Multi-Agent Test Suite
Tests Owner Governance, Global Kill Switch, Task Briefs, Department Registry,
Opportunity Scoring, Event Playbooks, Approval Queue, and Central Orchestration.
"""

import pytest
import shutil
from pathlib import Path

from core.database import Database
from core.owner_config import (
    OwnerConfig,
    OwnerConfigProtectionError,
    OwnerPolicyError,
    get_owner_config,
)
from core.kill_switch import KillSwitch, KillSwitchActiveError, get_kill_switch
from core.brand_os import BrandOS, get_brand_os
from core.task_brief import (
    TaskBrief,
    TaskBriefStore,
    TaskLifecycleStatus,
    TaskPriority,
)
from core.departments import DepartmentRegistry, get_department_registry
from intelligence.opportunity_scorer import OpportunityScorer
from core.playbooks import PlaybookEngine, PlaybookEventType
from publishing.approval_queue import ApprovalQueue, ApprovalSelfCheckError
from core.orchestrator import NexusOrchestrator


# -------------------------------------------------------------
# 1. Owner Governance & Immutability Tests
# -------------------------------------------------------------
def test_owner_config_reading_and_validation():
    cfg = get_owner_config()
    summary = cfg.get_policy_summary()
    assert summary["zero_budget_cap"] == "₹0.00 / $0.00"
    assert summary["human_approval_mandatory"] is True
    assert len(summary["editorial_pillars"]) >= 4


def test_owner_config_buzzword_and_hashtag_validation():
    cfg = get_owner_config()
    
    # Unacceptable hype copy
    bad_copy = "Stop scrolling! This insane breakthrough will mindblowingly change everything! #viral #fyp"
    ok, issues = cfg.validate_copy_against_voice(bad_copy)
    assert ok is False
    assert len(issues) >= 3
    assert any("insane" in i for i in issues)
    assert any("#viral" in i for i in issues)

    # Approved technical copy
    good_copy = "Engineers benchmarked algorithmic pruning achieving 3.8x inference throughput across million-token contexts. #AI #MachineLearning"
    ok, issues = cfg.validate_copy_against_voice(good_copy)
    assert ok is True
    assert len(issues) == 0


def test_owner_config_budget_enforcement():
    cfg = get_owner_config()
    # Zero cost is authorized
    assert cfg.check_financial_action(0.0) is True
    # Any positive expenditure without owner token is rejected
    assert cfg.check_financial_action(10.0, category="cloud_gpu") is False


def test_owner_config_immutability_protection():
    cfg = get_owner_config()
    with pytest.raises(OwnerConfigProtectionError):
        cfg.protect_file_mutation(caller="ContentEngine")


# -------------------------------------------------------------
# 2. Global Kill Switch Tests
# -------------------------------------------------------------
def test_kill_switch_lifecycle(tmp_path):
    stop_file = tmp_path / "STOP"
    ks = KillSwitch(stop_file=stop_file)

    try:
        # Default: inactive
        assert ks.is_active() is False
        ks.assert_not_active("TestInitial")

        # Activate
        ks.activate(reason="Test safety alert")
        assert ks.is_active() is True
        assert stop_file.exists()

        # Blocked operations raise KillSwitchActiveError
        with pytest.raises(KillSwitchActiveError):
            ks.assert_not_active("TestBlockedOperation")

        # Deactivate
        ks.deactivate()
        assert ks.is_active() is False
        ks.assert_not_active("TestResumed")
    finally:
        ks.deactivate()
        from core.config import get_config
        ks.stop_file = get_config().resolve_path("owner/STOP").resolve()


# -------------------------------------------------------------
# 3. Brand OS & Time-Stamped Signals Tests
# -------------------------------------------------------------
def test_brand_os_signal_lifecycle(tmp_path):
    bos = BrandOS(root_dir=tmp_path / "brand-os")
    assert "SUPER.INTELLIGENCEEE" in bos.get_brand_profile()
    
    # Add active signal
    sig = bos.add_signal(
        category="research",
        title="Sub-Quadratic Quantization Milestone",
        source_url="https://arxiv.org/abs/2026.0001",
        content="Engineers proved sub-quadratic quantization bounds.",
        ttl_hours=48,
    )
    assert sig["status"] == "ACTIVE"

    # Query active signals
    active = bos.get_active_signals(category="research")
    assert len(active) >= 1
    assert active[0]["title"] == "Sub-Quadratic Quantization Milestone"


# -------------------------------------------------------------
# 4. Structured Task Brief State Machine Tests
# -------------------------------------------------------------
def test_task_brief_lifecycle_and_transitions():
    brief = TaskBrief(
        task_id="TASK-TEST-001",
        agent="content_engine",
        objective="Draft technical script",
    )
    assert brief.execution_status == TaskLifecycleStatus.PENDING

    # Legal progression
    brief.transition_to(TaskLifecycleStatus.PLANNED)
    brief.transition_to(TaskLifecycleStatus.DISPATCHED)
    brief.transition_to(TaskLifecycleStatus.RUNNING)
    brief.transition_to(TaskLifecycleStatus.COMPLETED)
    brief.transition_to(TaskLifecycleStatus.QUALITY_CHECK)
    brief.transition_to(TaskLifecycleStatus.AWAITING_APPROVAL)
    brief.transition_to(TaskLifecycleStatus.APPROVED)
    brief.transition_to(TaskLifecycleStatus.PUBLISHED)
    assert brief.execution_status == TaskLifecycleStatus.PUBLISHED

    # Illegal transition: cannot move directly from PENDING to PUBLISHED
    invalid_brief = TaskBrief(task_id="TASK-INV", agent="test", objective="test")
    with pytest.raises(ValueError):
        invalid_brief.transition_to(TaskLifecycleStatus.PUBLISHED)


def test_task_brief_persistence_in_sqlite(tmp_path):
    db = Database(str(tmp_path / "test_tb.db"))
    store = TaskBriefStore(db)

    brief = TaskBrief(
        task_id="TASK-PERSIST-100",
        agent="creative_director",
        objective="Prepare storyboard",
        priority=TaskPriority.HIGH,
    )
    store.save_brief(brief)

    loaded = store.get_brief("TASK-PERSIST-100")
    assert loaded is not None
    assert loaded.agent == "creative_director"
    assert loaded.priority == TaskPriority.HIGH
    assert loaded.execution_status == TaskLifecycleStatus.PENDING


# -------------------------------------------------------------
# 5. Opportunity Scoring & Hard Evidence Gating Tests
# -------------------------------------------------------------
def test_opportunity_scoring_with_hard_evidence_gate(tmp_path):
    db = Database(str(tmp_path / "test_opp.db"))
    scorer = OpportunityScorer(db)

    # 1. High-evidence candidate
    grounded_candidate = {
        "title": "Autonomous Neural Pruning at 3.8x Speed",
        "summary": "AI researchers demonstrated linear memory scaling across million-token contexts on consumer hardware.",
        "category": "Artificial Intelligence",
        "url": "https://arxiv.org/abs/2601.12345",
        "publisher": "ArXiv Research",
    }
    score = scorer.evaluate_opportunity(grounded_candidate)
    assert score.eligible is True
    assert score.overall_score >= 65.0
    assert score.factors["evidence_quality"] == 10.0

    # 2. Fabricated candidate with missing URL
    fake_candidate = {
        "title": "Ungrounded Hype Story",
        "summary": "Rumors of massive speedups with zero links.",
        "category": "AI",
        "url": "",
    }
    zero_score = scorer.evaluate_opportunity(fake_candidate)
    assert zero_score.eligible is False
    assert zero_score.overall_score == 0.0
    assert "DISQUALIFIED" in zero_score.reasoning


# -------------------------------------------------------------
# 6. Event-Driven Playbooks & Idempotency Tests
# -------------------------------------------------------------
def test_playbook_idempotent_execution(tmp_path):
    db = Database(str(tmp_path / "test_pb.db"))
    engine = PlaybookEngine(db)

    payload = {"keyword": "Attention Scaling", "growth_pct": "+140%"}
    # Trigger event first time
    evt1 = engine.trigger_event(PlaybookEventType.SEARCH_DEMAND_SPIKE, payload)
    assert evt1.status == "COMPLETED"
    assert evt1.result["action"] == "RESEARCH_DISPATCHED"

    # Trigger identical event second time: must return cached idempotent record without duplicate tasks
    evt2 = engine.trigger_event(PlaybookEventType.SEARCH_DEMAND_SPIKE, payload)
    assert evt2.event_id == evt1.event_id
    assert evt2.status == "COMPLETED"


def test_playbook_negative_review_escalation(tmp_path):
    db = Database(str(tmp_path / "test_pb2.db"))
    engine = PlaybookEngine(db)

    payload = {"feedback": "The benchmark in scene 3 did not match the cited paper page 4."}
    evt = engine.trigger_event(PlaybookEventType.NEGATIVE_REVIEW, payload)
    assert evt.status == "ESCALATED"
    assert evt.escalation_required is True
    assert evt.result["requires_human_review"] is True


# -------------------------------------------------------------
# 7. Centralized Approval Queue Tests
# -------------------------------------------------------------
def test_approval_queue_decisions_and_self_approval_block(tmp_path):
    db = Database(str(tmp_path / "test_aq.db"))
    queue = ApprovalQueue(db)

    # 1. Enqueue item
    item = queue.enqueue_for_review(
        task_id="TASK-REV-01",
        production_job_id=99,
        title="Test Reel #99",
        artifact_path="output/drafts/test.mp4",
        agent_responsible="production_agent",
    )
    assert item.owner_decision == "PENDING"
    assert len(queue.list_pending_approvals()) >= 1

    # 2. Block agent self-approval
    with pytest.raises(ApprovalSelfCheckError):
        queue.decide(99, decision="APPROVE", reviewer_name="production_agent")

    # 3. Request revision
    rev_res = queue.decide(99, decision="REQUEST_REVISION", reviewer_name="Lead Editor", notes="Adjust lower margin")
    assert rev_res["status"] == "NEEDS_REVISION"


# -------------------------------------------------------------
# 8. Department Registry Completeness Test
# -------------------------------------------------------------
def test_department_registry_all_nine_agents():
    reg = get_department_registry()
    depts = reg.list_departments()
    assert len(depts) == 9
    expected_ids = {
        "research_agent", "market_radar", "brand_intelligence", "content_engine",
        "creative_director", "production_agent", "quality_assurance",
        "distribution_agent", "analytics_agent"
    }
    actual_ids = {d["id"] for d in depts}
    assert expected_ids == actual_ids


# -------------------------------------------------------------
# 9. Nexus Orchestrator Multi-Stage Governance Workflow Test
# -------------------------------------------------------------
def test_orchestrator_multi_stage_governance_flow(tmp_path, monkeypatch):
    db = Database(str(tmp_path / "test_orch.db"))
    orch = NexusOrchestrator(db=db)

    # Mock research agent execution to keep unit test hermetic and fast
    res_dept = orch.departments.get_department("research_agent")
    monkeypatch.setattr(res_dept, "execute", lambda brief: {"collected_count": 3, "status": "COMPLETED"})

    # 1. Stage 1: Collect signals
    signals = orch.stage_collect_signals()
    assert isinstance(signals, list)

    # 2. Stage 2: Validate policies
    policies = orch.stage_validate_policies()
    assert policies["human_approval_mandatory"] is True

    # 3. Stage 3: Opportunity scoring
    test_cand = [{
        "id": 101,
        "title": "Sub-Quadratic Quantization Milestone",
        "summary": "AI researchers demonstrated linear memory scaling across million-token contexts on consumer hardware.",
        "category": "Artificial Intelligence",
        "url": "https://arxiv.org/abs/2601.12345",
        "publisher": "ArXiv Research",
    }]
    opp = orch.stage_score_opportunities(test_cand)
    assert opp.eligible is True
    assert opp.overall_score >= 60.0

    # 4. Stage 4 & 5: Task planning & brief generation
    briefs = orch.stage_plan_and_generate_briefs(opp)
    assert len(briefs) == 5
    assert [b.agent for b in briefs] == [
        "content_engine", "creative_director", "production_agent", "quality_assurance", "distribution_agent"
    ]

    # Mock production agent execution to keep unit test fast
    prod_dept = orch.departments.get_department("production_agent")
    monkeypatch.setattr(
        prod_dept,
        "execute",
        lambda brief: {
            "production_job_id": 101,
            "video_path": "output/drafts/mock_video.mp4",
            "duration": 45.0,
            "status": "NEEDS_REVIEW",
        }
    )

    # Mock QA department execution
    qa_dept = orch.departments.get_department("quality_assurance")
    monkeypatch.setattr(
        qa_dept,
        "execute",
        lambda brief: {
            "passed": True,
            "fact_check": {"verified": True},
            "video_qa": {"valid": True},
            "status": "QA_PASSED",
        }
    )

    # 5. Stage 6: Dispatch agents
    res = orch.stage_dispatch_agents(briefs, opp)
    assert "content" in res
    assert "creative" in res
    assert "production" in res
    assert res["production"]["production_job_id"] == 101

    # 6. Stage 7: QA Verification
    qa_res = orch.stage_verify_results(briefs[3], res)
    assert qa_res["passed"] is True

    # 7. Stage 8: Approval routing
    dist_res = orch.stage_route_approvals(briefs[4], res)
    assert dist_res["status"] == "AWAITING_APPROVAL"
    assert briefs[4].execution_status == TaskLifecycleStatus.AWAITING_APPROVAL

    # 8. Stage 9: Execution report
    report = orch.stage_execution_report("WF-TEST-001", briefs)
    assert report["status"] == "SUCCESS"
    assert report["step_count"] == 5
    assert "WORKFLOW EXECUTION REPORT" in report["markdown_report"]

