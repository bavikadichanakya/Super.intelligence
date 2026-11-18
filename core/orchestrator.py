"""
SUPER.INTELLIGENCEEE — Central Governance Orchestrator (NEXUS Engine)
Single authoritative coordinator for the multi-agent social media operating system.
Enforces the 9-stage lifecycle:
Signal Collection -> Policy Validation -> Opportunity Scoring -> Task Planning ->
Brief Generation -> Agent Dispatch -> Result Verification -> Approval Routing -> Execution Report.
"""

from __future__ import annotations

import datetime
import logging
import uuid
from typing import Any, Dict, List, Optional

from core.activity_logger import ActivityLogger, get_activity_logger
from core.brand_os import BrandOS, get_brand_os
from core.database import Database, get_db
from core.departments import DepartmentRegistry, get_department_registry
from core.kill_switch import KillSwitch, get_kill_switch
from core.owner_config import OwnerConfig, get_owner_config
from core.task_brief import (
    TaskBrief,
    TaskBriefStore,
    TaskLifecycleStatus,
    TaskPriority,
)
from intelligence.opportunity_scorer import OpportunityScore, OpportunityScorer

logger = logging.getLogger("super_intelligence.orchestrator")


class OrchestratorError(Exception):
    """Raised when the central orchestrator encounters a fatal execution block."""


class NexusOrchestrator:
    """Central governing orchestrator coordinating all 9 department agents."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NexusOrchestrator, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db: Optional[Database] = None):
        if self._initialized:
            return
        self.db = db or get_db()
        self.owner_config = get_owner_config()
        self.kill_switch = get_kill_switch()
        self.brand_os = get_brand_os()
        self.brief_store = TaskBriefStore(self.db)
        self.activity_logger = get_activity_logger()
        self.departments = get_department_registry(self.db)
        self.opportunity_scorer = OpportunityScorer(self.db)
        self._initialized = True

    # -------------------------------------------------------------
    # Stage 1: Signal Collection
    # -------------------------------------------------------------
    def stage_collect_signals(self) -> List[Dict[str, Any]]:
        """Collects fresh signals from research feeds and Brand OS."""
        self.kill_switch.assert_not_active("Stage:CollectSignals")
        logger.info("[Orchestrator:Stage1] Collecting fresh intelligence signals...")
        research_dept = self.departments.get_department("research_agent")

        brief = TaskBrief(
            task_id=f"TASK-SIG-{str(uuid.uuid4())[:6].upper()}",
            agent="research_agent",
            objective="Harvest latest research and technology signals from public feeds.",
            priority=TaskPriority.NORMAL,
        )
        self.brief_store.save_brief(brief)
        res = research_dept.run_brief(brief)
        self.activity_logger.log(
            task_id=brief.task_id,
            agent_id="research_agent",
            action="COLLECT_SIGNALS",
            result=f"Collected {res.get('collected_count', 0)} signals",
        )
        # Fetch pending topics from DB
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM topics WHERE score > 0 OR status = 'DISCOVERED' ORDER BY id DESC LIMIT 10")
            return [dict(r) for r in cursor.fetchall()]

    # -------------------------------------------------------------
    # Stage 2: Policy Validation
    # -------------------------------------------------------------
    def stage_validate_policies(self) -> Dict[str, Any]:
        """Validates that owner configuration is present, complete, and unbreached."""
        self.kill_switch.assert_not_active("Stage:ValidatePolicies")
        logger.info("[Orchestrator:Stage2] Validating owner policies and budget boundaries...")
        self.owner_config.reload()
        summary = self.owner_config.get_policy_summary()

        # Enforce zero-budget verification
        if not self.owner_config.check_financial_action(0.0):
            raise OrchestratorError("Budget policy check failed.")

        return summary

    # -------------------------------------------------------------
    # Stage 3: Opportunity Scoring
    # -------------------------------------------------------------
    def stage_score_opportunities(
        self, candidate_topics: List[Dict[str, Any]]
    ) -> OpportunityScore:
        """Evaluates candidates using the 7-factor opportunity scoring matrix."""
        self.kill_switch.assert_not_active("Stage:ScoreOpportunities")
        logger.info(f"[Orchestrator:Stage3] Scoring {len(candidate_topics)} candidate opportunities...")

        if not candidate_topics:
            # Fallback benchmark topic if database is empty
            candidate_topics = [{
                "id": 1,
                "title": "NEURAL MEMORY SCALING BREAKTHROUGH",
                "summary": "AI researchers demonstrated linear memory scaling across million-token contexts, unlocking real-time inference on consumer hardware with zero accuracy degradation.",
                "category": "Artificial Intelligence",
                "url": "https://super.intelligenceee.local/memory-scaling",
                "publisher": "Super Intelligence Lab",
            }]

        scored_list: List[OpportunityScore] = []
        for top in candidate_topics:
            score = self.opportunity_scorer.evaluate_opportunity(top)
            if score.eligible:
                scored_list.append(score)

        if not scored_list:
            raise OrchestratorError("No candidate topics met the mandatory primary evidence threshold.")

        # Select highest-scoring eligible opportunity
        best = max(scored_list, key=lambda s: s.overall_score)
        logger.info(f"[Orchestrator:Stage3] Selected top opportunity: '{best.title}' (Score: {best.overall_score}/100)")
        return best

    # -------------------------------------------------------------
    # Stage 4 & 5: Task Planning & Brief Generation
    # -------------------------------------------------------------
    def stage_plan_and_generate_briefs(
        self, opportunity: OpportunityScore
    ) -> List[TaskBrief]:
        """Formulates the cross-department task pipeline and generates structured briefs."""
        self.kill_switch.assert_not_active("Stage:PlanAndGenerateBriefs")
        wf_id = str(uuid.uuid4())[:6].upper()
        logger.info(f"[Orchestrator:Stage4-5] Generating task briefs for Workflow [{wf_id}]...")

        # 1. Content Engine Brief
        brief_content = TaskBrief(
            task_id=f"TASK-SCRIPT-{wf_id}",
            agent="content_engine",
            objective=f"Draft 7-section verified script for '{opportunity.title}'.",
            priority=TaskPriority.HIGH,
            evidence_refs=opportunity.evidence_refs,
            expected_output="script_data",
        )

        # 2. Creative Director Brief
        brief_creative = TaskBrief(
            task_id=f"TASK-STORYBOARD-{wf_id}",
            agent="creative_director",
            objective="Construct 7-scene storyboard with 3+ distinct visual archetypes.",
            priority=TaskPriority.HIGH,
            input_refs=[brief_content.task_id],
            expected_output="storyboard",
        )

        # 3. Production Agent Brief
        brief_production = TaskBrief(
            task_id=f"TASK-PROD-{wf_id}",
            agent="production_agent",
            objective="Synthesize Piper audio, normalize loudnorm, and render 1080x1920 MP4 video.",
            priority=TaskPriority.HIGH,
            input_refs=[brief_creative.task_id],
            expected_output="video_path",
        )

        # 4. Quality Assurance Brief
        brief_qa = TaskBrief(
            task_id=f"TASK-QA-{wf_id}",
            agent="quality_assurance",
            objective="Audit factual claims grounding and execute FFprobe technical check.",
            priority=TaskPriority.URGENT,
            input_refs=[brief_production.task_id],
            expected_output="qa_report",
        )

        # 5. Distribution Agent Brief
        brief_dist = TaskBrief(
            task_id=f"TASK-DIST-{wf_id}",
            agent="distribution_agent",
            objective="Package reel for channels and submit to Human Approval Queue.",
            priority=TaskPriority.NORMAL,
            input_refs=[brief_qa.task_id],
            expected_output="approval_entry",
        )

        briefs = [brief_content, brief_creative, brief_production, brief_qa, brief_dist]
        for b in briefs:
            b.transition_to(TaskLifecycleStatus.PLANNED, "Planned by Central Orchestrator")
            self.brief_store.save_brief(b)

        return briefs

    # -------------------------------------------------------------
    # Stage 6: Agent Dispatch & Execution
    # -------------------------------------------------------------
    def stage_dispatch_agents(
        self, briefs: List[TaskBrief], opportunity: OpportunityScore
    ) -> Dict[str, Any]:
        """Dispatches briefs sequentially across departments, passing verified intermediate outputs."""
        self.kill_switch.assert_not_active("Stage:DispatchAgents")
        logger.info("[Orchestrator:Stage6] Dispatching tasks across department agents...")

        # 1. Content Engine
        b_content = briefs[0]
        dept_content = self.departments.get_department("content_engine")
        b_content.result = {
            "title": opportunity.title,
            "summary": opportunity.reasoning,
            "url": opportunity.evidence_refs[0] if opportunity.evidence_refs else "https://super.intelligenceee.local",
            "publisher": "Primary Lab Documentation",
            "category": "Artificial Intelligence",
        }
        res_content = dept_content.run_brief(b_content)
        self.brief_store.save_brief(b_content)

        # 2. Creative Director
        b_creative = briefs[1]
        dept_creative = self.departments.get_department("creative_director")
        b_creative.result = res_content
        res_creative = dept_creative.run_brief(b_creative)
        self.brief_store.save_brief(b_creative)

        # 3. Production Agent
        b_prod = briefs[2]
        dept_prod = self.departments.get_department("production_agent")
        b_prod.result = {**res_content, **res_creative, "topic_id": opportunity.topic_id}
        res_prod = dept_prod.run_brief(b_prod)
        self.brief_store.save_brief(b_prod)

        return {
            "content": res_content,
            "creative": res_creative,
            "production": res_prod,
        }

    # -------------------------------------------------------------
    # Stage 7: Result Verification
    # -------------------------------------------------------------
    def stage_verify_results(
        self, brief_qa: TaskBrief, dispatch_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Dispatches QA department to evaluate claim evidence grounding and FFprobe video specs."""
        self.kill_switch.assert_not_active("Stage:VerifyResults")
        logger.info("[Orchestrator:Stage7] Dispatched Quality Assurance department for verification...")

        dept_qa = self.departments.get_department("quality_assurance")
        brief_qa.result = {
            "script_data": dispatch_results["content"].get("script_data"),
            "video_path": dispatch_results["production"].get("video_path"),
        }
        res_qa = dept_qa.run_brief(brief_qa)
        self.brief_store.save_brief(brief_qa)

        if not res_qa.get("passed", False):
            raise OrchestratorError("Quality Assurance gate failed verification.")

        return res_qa

    # -------------------------------------------------------------
    # Stage 8: Approval Routing
    # -------------------------------------------------------------
    def stage_route_approvals(
        self, brief_dist: TaskBrief, dispatch_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enforces the Owner Approval Bar and routes the finished reel to Human Review."""
        self.kill_switch.assert_not_active("Stage:RouteApprovals")
        logger.info("[Orchestrator:Stage8] Routing to Human Approval Queue per owner approval bar...")

        dept_dist = self.departments.get_department("distribution_agent")
        brief_dist.result = {
            "production_job_id": dispatch_results["production"].get("production_job_id"),
        }
        res_dist = dept_dist.run_brief(brief_dist)
        brief_dist.transition_to(TaskLifecycleStatus.AWAITING_APPROVAL, "Awaiting owner authorization in queue")
        self.brief_store.save_brief(brief_dist)

        return res_dist

    # -------------------------------------------------------------
    # Stage 9: Execution Report
    # -------------------------------------------------------------
    def stage_execution_report(
        self, workflow_id: str, briefs: List[TaskBrief], overall_status: str = "SUCCESS"
    ) -> Dict[str, Any]:
        """Compiles final structured execution audit report."""
        logger.info(f"[Orchestrator:Stage9] Compiling execution report for {workflow_id}...")
        report = self.activity_logger.generate_execution_report(
            workflow_id=workflow_id,
            tasks=briefs,
            overall_status=overall_status,
        )
        return report

    # -------------------------------------------------------------
    # Master Workflow Execution
    # -------------------------------------------------------------
    def execute_workflow(self, topic_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Executes one complete end-to-end governed workflow across all 9 stages:
        Signal Collection -> Policy Validation -> Opportunity Scoring -> Task Planning ->
        Brief Generation -> Agent Dispatch -> Result Verification -> Approval Routing -> Execution Report.
        """
        wf_id = f"WF-{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"=== Starting Governed Multi-Agent Workflow: {wf_id} ===")

        # Stage 1: Signals
        signals = self.stage_collect_signals()

        # Stage 2: Policies
        self.stage_validate_policies()

        # Stage 3: Opportunity Scoring
        if topic_id:
            with self.db.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
                row = cursor.fetchone()
                candidates = [dict(row)] if row else []
        else:
            candidates = signals

        opportunity = self.stage_score_opportunities(candidates)

        # Stage 4 & 5: Planning & Briefs
        briefs = self.stage_plan_and_generate_briefs(opportunity)

        try:
            # Stage 6: Dispatch Agents
            dispatch_results = self.stage_dispatch_agents(briefs, opportunity)

            # Stage 7: QA Verification
            self.stage_verify_results(briefs[3], dispatch_results)

            # Stage 8: Approval Routing
            dist_res = self.stage_route_approvals(briefs[4], dispatch_results)

            # Stage 9: Execution Report
            exec_report = self.stage_execution_report(wf_id, briefs, overall_status="SUCCESS")

            logger.info(f"=== Governed Workflow {wf_id} COMPLETED. Job placed in Human Approval Queue. ===")

            return {
                "workflow_id": wf_id,
                "status": "AWAITING_APPROVAL",
                "opportunity": opportunity.to_dict(),
                "production_job_id": dispatch_results["production"].get("production_job_id"),
                "video_path": dispatch_results["production"].get("video_path"),
                "duration": dispatch_results["production"].get("duration"),
                "distribution": dist_res,
                "execution_report": exec_report,
                "briefs": [b.to_dict() for b in briefs],
            }

        except Exception as e:
            logger.error(f"Governed Workflow {wf_id} FAILED: {e}", exc_info=True)
            self.stage_execution_report(wf_id, briefs, overall_status=f"FAILED: {e}")
            raise


def get_orchestrator(db: Optional[Database] = None) -> NexusOrchestrator:
    return NexusOrchestrator(db)
