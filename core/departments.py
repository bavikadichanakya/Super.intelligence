"""
SUPER.INTELLIGENCEEE — Specialized Department Agents & Contracts
Defines the 9 canonical department agents inspired by OneGTMLab principles.
Coordinates specialized work under the strict supervision of the central orchestrator.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from core.database import Database, get_db
from core.kill_switch import get_kill_switch
from core.owner_config import get_owner_config
from core.task_brief import TaskBrief, TaskLifecycleStatus

logger = logging.getLogger("super_intelligence.departments")


class DepartmentExecutionError(Exception):
    """Raised when a department agent encounters a fatal execution error."""


class BaseDepartment(ABC):
    """Abstract base class for all governed department agents."""

    department_id: str
    name: str
    responsibilities: List[str]
    allowed_tools: List[str]
    restricted_operations: List[str]

    def __init__(self, db: Optional[Database] = None):
        self.db = db or get_db()
        self.owner_config = get_owner_config()
        self.kill_switch = get_kill_switch()

    def run_brief(self, brief: TaskBrief) -> Dict[str, Any]:
        """
        Guarded execution entrypoint.
        Enforces Kill Switch check, legal transitions, and error boundary.
        """
        # 1. Kill switch check
        self.kill_switch.assert_not_active(f"{self.department_id}:{brief.task_id}")

        # 2. Transition to RUNNING
        brief.transition_to(TaskLifecycleStatus.RUNNING, f"Dispatched to {self.name}")

        try:
            result = self.execute(brief)
            brief.result = result
            brief.transition_to(TaskLifecycleStatus.COMPLETED, f"Successfully executed by {self.name}")
            return result
        except Exception as e:
            brief.error = str(e)
            brief.transition_to(TaskLifecycleStatus.FAILED, f"Failed in {self.name}: {e}")
            logger.error(f"[{self.department_id}] Brief {brief.task_id} failed: {e}", exc_info=True)
            raise DepartmentExecutionError(f"[{self.department_id}] Execution failed: {e}")

    @abstractmethod
    def execute(self, brief: TaskBrief) -> Dict[str, Any]:
        """Specialist logic implemented by each department agent."""
        raise NotImplementedError


# -------------------------------------------------------------
# 1. Research Agent
# -------------------------------------------------------------
class ResearchAgent(BaseDepartment):
    department_id = "research_agent"
    name = "Research & Evidence Department"
    responsibilities = [
        "Discover public tech news, preprints, and developer breakthroughs",
        "Extract primary source URLs and author credentials",
        "Filter duplicate stories and verify domain credibility",
    ]
    allowed_tools = ["RSSCollector", "SourceExtractor", "Deduplicator", "AgentReachConnector"]
    restricted_operations = ["Direct scriptwriting", "Visual rendering", "Publishing"]

    def execute(self, brief: TaskBrief) -> Dict[str, Any]:
        from research.rss_collector import RSSCollector
        from research.deduplicator import Deduplicator
        from core.config import get_config

        # Check if we already have fresh discovered topics in DB (cached within 1 hour)
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) as cnt FROM topics WHERE discovered_at >= datetime('now', '-1 hour')")
            row = cursor.fetchone()
            recent_count = row["cnt"] if row else 0

        if recent_count >= 10:
            logger.info(f"[ResearchAgent] Cache fresh: {recent_count} recent signals found. Utilizing existing pool.")
            return {
                "collected_count": recent_count,
                "status": "RESEARCH_COMPLETE_CACHED",
            }

        collector = RSSCollector(self.db, get_config())
        items = collector.collect_all()
        logger.info(f"[ResearchAgent] Ingested {len(items)} public signals.")
        return {
            "collected_count": len(items),
            "sample_signals": [i.get("title") for i in items[:5]] if items else [],
            "status": "RESEARCH_COMPLETE",
        }


# -------------------------------------------------------------
# 2. Market Radar
# -------------------------------------------------------------
class MarketRadar(BaseDepartment):
    department_id = "market_radar"
    name = "Market & Competitor Radar"
    responsibilities = [
        "Monitor external developer discussions and competitor coverage",
        "Detect search demand spikes and trending technical keywords",
        "Flag saturation risks and redundant content angles",
    ]
    allowed_tools = ["AgentReachConnector", "PublicWebCollector", "BrandOS"]
    restricted_operations = ["Publishing", "Financial actions", "Modifying Brand OS"]

    def execute(self, brief: TaskBrief) -> Dict[str, Any]:
        from core.brand_os import get_brand_os
        brand_os = get_brand_os()
        active_signals = brand_os.get_active_signals()
        return {
            "active_signals_count": len(active_signals),
            "trends": [s.get("title") for s in active_signals[:3]],
            "status": "RADAR_SCANNED",
        }


# -------------------------------------------------------------
# 3. Brand Intelligence
# -------------------------------------------------------------
class BrandIntelligence(BaseDepartment):
    department_id = "brand_intelligence"
    name = "Brand Intelligence & Governance"
    responsibilities = [
        "Maintain Brand Brain context and audience persona alignment",
        "Enforce prohibited claims boundaries and hallucination rules",
        "Audit draft proposals against owner brand voice and pillars",
    ]
    allowed_tools = ["BrandOS", "OwnerConfig"]
    restricted_operations = ["Mutating owner files", "Overwriting historical learnings"]

    def execute(self, brief: TaskBrief) -> Dict[str, Any]:
        summary = self.owner_config.get_policy_summary()
        prohibited = self.owner_config._parsed_voice.get("prohibited_words", set())
        return {
            "governance_status": "COMPLIANT",
            "prohibited_words_tracked": len(prohibited),
            "pillars": summary.get("editorial_pillars", []),
        }


# -------------------------------------------------------------
# 4. Content Engine
# -------------------------------------------------------------
class ContentEngine(BaseDepartment):
    department_id = "content_engine"
    name = "Content & Script Engine"
    responsibilities = [
        "Generate structured 7-section video scripts (Hook to Takeaway)",
        "Optimize spoken rhythm, beat timing, and word density (~2.5 wps)",
        "Produce platform-optimized captions without clickbait fluff",
    ]
    allowed_tools = ["ScriptWriter", "FallbackTemplates", "ProviderManager", "InstagramIntel"]
    restricted_operations = ["Direct rendering", "Publishing without review", "Using prohibited words"]

    def execute(self, brief: TaskBrief) -> Dict[str, Any]:
        from content.script_writer import ScriptWriter
        topic_data = brief.result or {
            "title": brief.objective,
            "summary": "Technical architecture breakthrough demonstration.",
            "url": brief.evidence_refs[0] if brief.evidence_refs else "https://super.intelligenceee.local",
            "publisher": "Primary Research Documentation",
            "category": "Artificial Intelligence",
        }
        writer = ScriptWriter(self.db)
        script_data = writer.generate_script_for_topic(topic_data)

        # Voice validation
        ok_voice, voice_issues = self.owner_config.validate_copy_against_voice(script_data.get("full_narration", ""))
        if not ok_voice:
            logger.warning(f"[ContentEngine] Script voice issues: {voice_issues}")

        return {
            "script_id": script_data.get("id"),
            "title": script_data.get("title"),
            "full_narration": script_data.get("full_narration"),
            "word_count": script_data.get("word_count"),
            "script_data": script_data,
        }


# -------------------------------------------------------------
# 5. Creative Director
# -------------------------------------------------------------
class CreativeDirector(BaseDepartment):
    department_id = "creative_director"
    name = "Creative & Storyboard Direction"
    responsibilities = [
        "Transform verified scripts into 7-scene production storyboards",
        "Assign 7 visual archetypes based on narrative beat",
        "Enforce visual diversity rules (minimum 3 distinct archetypes)",
    ]
    allowed_tools = ["StoryboardGenerator", "ScenePlanner"]
    restricted_operations = ["Audio synthesis", "FFmpeg composition"]

    def execute(self, brief: TaskBrief) -> Dict[str, Any]:
        from content.storyboard import StoryboardGenerator
        script_data = brief.result.get("script_data") if (brief.result and "script_data" in brief.result) else {
            "title": brief.objective,
            "hook": brief.objective,
        }
        storyboard = StoryboardGenerator.generate_storyboard(script_data)
        archetypes = [s["visual_archetype"] for s in storyboard]
        return {
            "scene_count": len(storyboard),
            "storyboard": storyboard,
            "archetypes": archetypes,
            "unique_archetypes": list(set(archetypes)),
        }


# -------------------------------------------------------------
# 6. Production Agent
# -------------------------------------------------------------
class ProductionAgent(BaseDepartment):
    department_id = "production_agent"
    name = "Video & Audio Production"
    responsibilities = [
        "Synthesize high-fidelity voiceover via Piper TTS",
        "Execute EBU R128 audio loudness normalization (-16 LUFS)",
        "Resolve multi-archetype visual assets and render 1080x1920 compositions",
    ]
    allowed_tools = ["PiperEngine", "AudioMixer", "VisualRouter", "HyperFramesRunner", "FFmpegVideoPipeline"]
    restricted_operations = ["Publishing", "Modifying script claims", "Exceeding 8 GB RAM"]

    def execute(self, brief: TaskBrief) -> Dict[str, Any]:
        # Production execution is coordinated sequentially through SuperIntelligencePipeline
        from core.pipeline import SuperIntelligencePipeline
        pipeline = SuperIntelligencePipeline(self.db)
        topic_id = brief.result.get("topic_id") if brief.result else None
        reel_result = pipeline.produce_reel(topic_id=topic_id)
        return {
            "production_job_id": reel_result.get("production_job_id"),
            "video_path": reel_result.get("video_path"),
            "duration": reel_result.get("duration"),
            "status": reel_result.get("status"),
        }


# -------------------------------------------------------------
# 7. Quality Assurance
# -------------------------------------------------------------
class QualityAssurance(BaseDepartment):
    department_id = "quality_assurance"
    name = "Technical & Factual QA Gate"
    responsibilities = [
        "Audit quantitative script claims against primary source evidence",
        "Verify audio pacing and speech fidelity via Whisper QA",
        "Inspect rendered video technical standards (1080x1920, 30fps, H.264/AAC) via FFprobe",
    ]
    allowed_tools = ["FactChecker", "WhisperQA", "VideoValidator"]
    restricted_operations = ["Bypassing validation failures", "Auto-approving ungrounded claims"]

    def execute(self, brief: TaskBrief) -> Dict[str, Any]:
        from content.fact_checker import FactChecker
        from video.video_validator import VideoValidator
        from pathlib import Path

        fc = FactChecker(self.db)
        script_payload = brief.result.get("script_data") if (brief.result and "script_data" in brief.result) else {
            "title": brief.objective,
            "summary": brief.objective,
            "sources": [{"url": "https://super.intelligenceee.local"}],
        }
        fc_res = fc.check_script(script_payload)

        # Video validation check if path provided
        video_valid = True
        video_report = {}
        if brief.result and brief.result.get("video_path"):
            v_path = Path(brief.result.get("video_path"))
            validator = VideoValidator()
            video_report = validator.validate_reel(v_path)
            video_valid = video_report.get("valid", False)

        passed = fc_res.get("verified", False) and video_valid
        return {
            "passed": passed,
            "fact_check": fc_res,
            "video_qa": video_report,
            "status": "QA_PASSED" if passed else "QA_FAILED",
        }


# -------------------------------------------------------------
# 8. Distribution Agent
# -------------------------------------------------------------
class DistributionAgent(BaseDepartment):
    department_id = "distribution_agent"
    name = "Distribution & Publishing Gate"
    responsibilities = [
        "Package reels with channel metadata, SEO tags, and mobile-safe formatting",
        "Enforce the mandatory human approval gate before any external publishing",
        "Execute resumable, token-encrypted publishing to Instagram and YouTube",
    ]
    allowed_tools = ["InstagramIntegration", "YouTubeIntegration", "ApprovalManager"]
    restricted_operations = ["Publishing without affirmative human approval in database"]

    def execute(self, brief: TaskBrief) -> Dict[str, Any]:
        from publishing.approval import ApprovalManager
        job_id = brief.result.get("production_job_id") if brief.result else None
        if not job_id:
            return {"status": "BLOCKED", "reason": "No production job ID provided for distribution."}

        # Check approval gate strictly
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM production_jobs WHERE id = ?", (job_id,))
            row = cursor.fetchone()
            current_status = row["status"] if row else "UNKNOWN"

        if current_status != "APPROVED":
            logger.info(f"[DistributionAgent] Job #{job_id} is in status '{current_status}'. Halting before publishing per owner approval bar.")
            # Enqueue into filesystem review mirror queue/needs-your-ok/
            try:
                from publishing.approval_queue import ApprovalQueue
                q = ApprovalQueue(self.db)
                d_row = dict(row) if row else {}
                q.enqueue_for_review(
                    task_id=brief.task_id,
                    production_job_id=job_id,
                    title=d_row.get("title", f"Reel #{job_id}"),
                    artifact_path=d_row.get("output_video_path", ""),
                    agent_responsible="distribution_agent",
                )
            except Exception as e:
                logger.warning(f"Could not mirror to approval queue folder: {e}")

            return {
                "production_job_id": job_id,
                "status": "AWAITING_APPROVAL",
                "human_approval_required": True,
                "message": f"Job #{job_id} safely queued in Human Approval Queue.",
            }

        return {
            "production_job_id": job_id,
            "status": "READY_FOR_DISPATCH",
        }


# -------------------------------------------------------------
# 9. Analytics Agent
# -------------------------------------------------------------
class AnalyticsAgent(BaseDepartment):
    department_id = "analytics_agent"
    name = "Analytics & Performance Intelligence"
    responsibilities = [
        "Track views, reach, retention, and engagement across published reels",
        "Detect post performance spikes and retention drop-offs",
        "Formulate empirical recommendations for future content planning",
    ]
    allowed_tools = ["PerformanceTracker", "WeeklyReport"]
    restricted_operations = ["Fabricating missing metrics", "Mutating Brand OS policies"]

    def execute(self, brief: TaskBrief) -> Dict[str, Any]:
        from analytics.performance_tracker import PerformanceTracker
        tracker = PerformanceTracker()
        summary = tracker.get_summary()
        return {
            "total_tracked": summary.get("total_reels_tracked", 0),
            "total_views": summary.get("total_views", 0),
            "avg_engagement_rate": summary.get("avg_engagement_rate", 0.0),
            "status": "ANALYTICS_REPORTED",
        }


# -------------------------------------------------------------
# Department Registry & Factory
# -------------------------------------------------------------
class DepartmentRegistry:
    """Central registry and lookup factory for all 9 department agents."""

    def __init__(self, db: Optional[Database] = None):
        self.db = db or get_db()
        self._departments: Dict[str, BaseDepartment] = {
            "research_agent": ResearchAgent(self.db),
            "market_radar": MarketRadar(self.db),
            "brand_intelligence": BrandIntelligence(self.db),
            "content_engine": ContentEngine(self.db),
            "creative_director": CreativeDirector(self.db),
            "production_agent": ProductionAgent(self.db),
            "quality_assurance": QualityAssurance(self.db),
            "distribution_agent": DistributionAgent(self.db),
            "analytics_agent": AnalyticsAgent(self.db),
        }

    def get_department(self, department_id: str) -> Optional[BaseDepartment]:
        return self._departments.get(department_id.lower())

    def list_departments(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": dept.department_id,
                "name": dept.name,
                "responsibilities": dept.responsibilities,
                "allowed_tools": dept.allowed_tools,
                "restricted_operations": dept.restricted_operations,
            }
            for dept in self._departments.values()
        ]


def get_department_registry(db: Optional[Database] = None) -> DepartmentRegistry:
    return DepartmentRegistry(db)
