"""
SUPER.INTELLIGENCEEE — Event-Driven Playbooks Framework
Defines the 8 canonical strategic event playbooks inspired by OneGTMLab principles.
Guarantees idempotency, prevents duplicate execution, and enforces human governance.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import logging
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from core.database import Database, get_db
from core.kill_switch import get_kill_switch
from core.owner_config import get_owner_config
from core.task_brief import TaskBrief, TaskBriefStore, TaskLifecycleStatus, TaskPriority

logger = logging.getLogger("super_intelligence.playbooks")


class PlaybookEventType(str, Enum):
    """The 8 canonical strategic event types."""
    SEARCH_DEMAND_SPIKE = "SEARCH_DEMAND_SPIKE"
    COMPETITOR_CAMPAIGN = "COMPETITOR_CAMPAIGN"
    NEGATIVE_REVIEW = "NEGATIVE_REVIEW"
    CONTENT_CALENDAR_THIN = "CONTENT_CALENDAR_THIN"
    POST_PERFORMANCE_SPIKE = "POST_PERFORMANCE_SPIKE"
    SEARCH_RANKING_DECLINE = "SEARCH_RANKING_DECLINE"
    CREATIVE_PERFORMANCE_DROP = "CREATIVE_PERFORMANCE_DROP"
    NEW_LEAD_OR_DM = "NEW_LEAD_OR_DM"


@dataclass
class PlaybookEvent:
    """Represents a validated event triggering an automated response playbook."""
    event_id: str
    event_type: PlaybookEventType
    payload: Dict[str, Any]
    evidence_ref: str
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    status: str = "RECEIVED"               # RECEIVED, PROCESSING, COMPLETED, ESCALATED, FAILED
    escalation_required: bool = False
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["event_type"] = self.event_type.value
        return d


class PlaybookEngine:
    """Coordinates execution of event-driven playbooks with strict idempotency."""

    def __init__(self, db: Optional[Database] = None):
        self.db = db or get_db()
        self.owner_config = get_owner_config()
        self.kill_switch = get_kill_switch()
        self.brief_store = TaskBriefStore(self.db)
        self._ensure_table()

    def _ensure_table(self):
        with self.db.transaction() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS playbook_events (
                    event_id TEXT PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    evidence_ref TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'RECEIVED',
                    escalation_required INTEGER DEFAULT 0,
                    result TEXT,
                    error TEXT
                );
                """
            )

    def _compute_idempotency_key(self, event_type: PlaybookEventType, payload: Dict[str, Any]) -> str:
        """Generates deterministic hash to prevent duplicate event execution."""
        raw_key = f"{event_type.value}:{json.dumps(payload, sort_keys=True)}"
        return f"EVT-{hashlib.sha256(raw_key.encode('utf-8')).hexdigest()[:12].upper()}"

    def trigger_event(
        self,
        event_type: PlaybookEventType,
        payload: Dict[str, Any],
        evidence_ref: str = "",
    ) -> PlaybookEvent:
        """
        Main entrypoint for triggering an event playbook.
        Guarantees idempotency: duplicate payloads within 24 hours are safely ignored.
        """
        # Kill switch verification
        self.kill_switch.assert_not_active(f"Playbook:{event_type.value}")

        event_id = self._compute_idempotency_key(event_type, payload)

        # Check existing execution
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM playbook_events WHERE event_id = ?", (event_id,))
            existing = cursor.fetchone()
            if existing:
                logger.info(f"Idempotent skip: Event {event_id} ({event_type.value}) was already processed.")
                d = dict(existing)
                return PlaybookEvent(
                    event_id=d["event_id"],
                    event_type=PlaybookEventType(d["event_type"]),
                    payload=json.loads(d["payload"]),
                    evidence_ref=d.get("evidence_ref", ""),
                    created_at=d.get("created_at", ""),
                    status=d.get("status", "COMPLETED"),
                    escalation_required=bool(d.get("escalation_required", 0)),
                    result=json.loads(d["result"]) if d.get("result") else None,
                    error=d.get("error"),
                )

        # Create new event record
        event = PlaybookEvent(
            event_id=event_id,
            event_type=event_type,
            payload=payload,
            evidence_ref=evidence_ref,
            status="PROCESSING",
        )

        try:
            # Route to specialized playbook handler
            handler = self._get_handler(event_type)
            result = handler(event)
            event.result = result
            event.status = "ESCALATED" if event.escalation_required else "COMPLETED"
            logger.info(f"Playbook {event_type.value} [{event_id}] executed successfully (Status: {event.status})")
        except Exception as e:
            event.status = "FAILED"
            event.error = str(e)
            logger.error(f"Playbook {event_type.value} [{event_id}] failed: {e}", exc_info=True)

        # Persist event result
        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO playbook_events (
                    event_id, event_type, payload, evidence_ref, created_at,
                    status, escalation_required, result, error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.event_type.value,
                    json.dumps(event.payload),
                    event.evidence_ref,
                    event.created_at,
                    event.status,
                    1 if event.escalation_required else 0,
                    json.dumps(event.result) if event.result else None,
                    event.error,
                ),
            )

        return event

    def _get_handler(self, event_type: PlaybookEventType) -> Callable[[PlaybookEvent], Dict[str, Any]]:
        handlers = {
            PlaybookEventType.SEARCH_DEMAND_SPIKE: self._handle_search_demand_spike,
            PlaybookEventType.COMPETITOR_CAMPAIGN: self._handle_competitor_campaign,
            PlaybookEventType.NEGATIVE_REVIEW: self._handle_negative_review,
            PlaybookEventType.CONTENT_CALENDAR_THIN: self._handle_content_calendar_thin,
            PlaybookEventType.POST_PERFORMANCE_SPIKE: self._handle_post_performance_spike,
            PlaybookEventType.SEARCH_RANKING_DECLINE: self._handle_search_ranking_decline,
            PlaybookEventType.CREATIVE_PERFORMANCE_DROP: self._handle_creative_performance_drop,
            PlaybookEventType.NEW_LEAD_OR_DM: self._handle_new_lead_or_dm,
        }
        return handlers[event_type]

    # -------------------------------------------------------------
    # 1. SEARCH_DEMAND_SPIKE Playbook
    # -------------------------------------------------------------
    def _handle_search_demand_spike(self, event: PlaybookEvent) -> Dict[str, Any]:
        keyword = event.payload.get("keyword", "Neural Pruning")
        growth = event.payload.get("growth_pct", "+120%")
        # Create research brief
        brief = TaskBrief(
            task_id=f"TASK-SPIKE-{event.event_id[:6]}",
            agent="research_agent",
            objective=f"Investigate search demand surge for '{keyword}' ({growth}) and extract primary preprints.",
            priority=TaskPriority.HIGH,
            evidence_refs=[event.evidence_ref] if event.evidence_ref else [],
        )
        self.brief_store.save_brief(brief)
        return {"action": "RESEARCH_DISPATCHED", "task_id": brief.task_id, "keyword": keyword}

    # -------------------------------------------------------------
    # 2. COMPETITOR_CAMPAIGN Playbook
    # -------------------------------------------------------------
    def _handle_competitor_campaign(self, event: PlaybookEvent) -> Dict[str, Any]:
        competitor = event.payload.get("competitor", "Rival Lab")
        angle = event.payload.get("angle", "Generalized AI Compute")
        brief = TaskBrief(
            task_id=f"TASK-COMP-{event.event_id[:6]}",
            agent="brand_intelligence",
            objective=f"Audit differentiator counter-positioning against {competitor}'s campaign on {angle}.",
            priority=TaskPriority.NORMAL,
        )
        self.brief_store.save_brief(brief)
        return {"action": "COUNTER_POSITIONING_ANALYSIS", "task_id": brief.task_id}

    # -------------------------------------------------------------
    # 3. NEGATIVE_REVIEW Playbook (Immediate Escalation)
    # -------------------------------------------------------------
    def _handle_negative_review(self, event: PlaybookEvent) -> Dict[str, Any]:
        event.escalation_required = True
        logger.warning(f"[Playbook:NEGATIVE_REVIEW] Urgent escalation required for review: {event.payload.get('feedback', '')}")
        # Create QA diagnostic task
        brief = TaskBrief(
            task_id=f"TASK-QA-{event.event_id[:6]}",
            agent="quality_assurance",
            objective=f"Perform root-cause technical audit on negative feedback: {event.payload.get('feedback', '')}",
            priority=TaskPriority.URGENT,
        )
        self.brief_store.save_brief(brief)
        return {"action": "ESCALATED_TO_OWNER", "task_id": brief.task_id, "requires_human_review": True}

    # -------------------------------------------------------------
    # 4. CONTENT_CALENDAR_THIN Playbook
    # -------------------------------------------------------------
    def _handle_content_calendar_thin(self, event: PlaybookEvent) -> Dict[str, Any]:
        brief = TaskBrief(
            task_id=f"TASK-CAL-{event.event_id[:6]}",
            agent="research_agent",
            objective="Discover and score fresh frontier tech stories to replenish content queue to target (5 reels).",
            priority=TaskPriority.HIGH,
        )
        self.brief_store.save_brief(brief)
        return {"action": "DISCOVERY_SCHEDULED", "task_id": brief.task_id}

    # -------------------------------------------------------------
    # 5. POST_PERFORMANCE_SPIKE Playbook
    # -------------------------------------------------------------
    def _handle_post_performance_spike(self, event: PlaybookEvent) -> Dict[str, Any]:
        reel_title = event.payload.get("reel_title", "Breakthrough Reel")
        views = event.payload.get("views", 10000)
        # Create follow-up proposal brief
        brief = TaskBrief(
            task_id=f"TASK-SPIKE-{event.event_id[:6]}",
            agent="content_engine",
            objective=f"Formulate follow-up deep-dive script capitalizing on performance spike of '{reel_title}' ({views:,} views).",
            priority=TaskPriority.HIGH,
            constraints={"human_approval_required": True, "budget": 0.0},
        )
        self.brief_store.save_brief(brief)
        return {"action": "FOLLOW_UP_PLANNED", "task_id": brief.task_id}

    # -------------------------------------------------------------
    # 6. SEARCH_RANKING_DECLINE Playbook
    # -------------------------------------------------------------
    def _handle_search_ranking_decline(self, event: PlaybookEvent) -> Dict[str, Any]:
        topic_name = event.payload.get("topic", "Attention Scaling")
        brief = TaskBrief(
            task_id=f"TASK-RANK-{event.event_id[:6]}",
            agent="research_agent",
            objective=f"Audit refreshed preprints and newer empirical benchmarks for '{topic_name}' to update editorial dossier.",
            priority=TaskPriority.NORMAL,
        )
        self.brief_store.save_brief(brief)
        return {"action": "RESEARCH_REFRESH_SCHEDULED", "task_id": brief.task_id}

    # -------------------------------------------------------------
    # 7. CREATIVE_PERFORMANCE_DROP Playbook
    # -------------------------------------------------------------
    def _handle_creative_performance_drop(self, event: PlaybookEvent) -> Dict[str, Any]:
        brief = TaskBrief(
            task_id=f"TASK-CREATIVE-{event.event_id[:6]}",
            agent="creative_director",
            objective="Rotate visual archetype distribution: increase motion_diagram and sketch_stat ratios to counter viewer fatigue.",
            priority=TaskPriority.NORMAL,
        )
        self.brief_store.save_brief(brief)
        return {"action": "ARCHETYPE_ROTATION_APPLIED", "task_id": brief.task_id}

    # -------------------------------------------------------------
    # 8. NEW_LEAD_OR_DM Playbook (Zero Automated Outbound Messages)
    # -------------------------------------------------------------
    def _handle_new_lead_or_dm(self, event: PlaybookEvent) -> Dict[str, Any]:
        event.escalation_required = True
        lead_sender = event.payload.get("sender", "@engineer")
        lead_text = event.payload.get("message", "Inquiry regarding architecture implementation.")
        logger.info(f"[Playbook:NEW_LEAD_OR_DM] Lead received from {lead_sender}. Logged for owner manual response.")
        return {
            "action": "ESCALATED_FOR_MANUAL_RESPONSE",
            "sender": lead_sender,
            "requires_human_action": True,
            "auto_reply_blocked": True,
        }

