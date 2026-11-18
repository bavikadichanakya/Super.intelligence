"""
SUPER.INTELLIGENCEEE — Centralized Approval Queue & Governance Interface
Maintains human review files under queue/ synchronized with SQLite approvals table.
Supports APPROVE, REJECT, REQUEST_REVISION, and HOLD decisions.
"""

from __future__ import annotations

import datetime
import json
import logging
import shutil
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import get_config
from core.database import Database, get_db
from publishing.approval import ApprovalManager

logger = logging.getLogger("super_intelligence.approval_queue")


class ApprovalSelfCheckError(PermissionError):
    """Raised when an agent attempts to approve its own work."""


@dataclass
class ApprovalItem:
    """Standardized human review submission packet."""
    task_id: str
    production_job_id: int
    title: str
    artifact_path: str
    agent_responsible: str
    evidence_refs: List[str]
    quality_check_results: Dict[str, Any]
    reason_approval_required: str = "Mandatory owner approval before social media distribution."
    owner_decision: str = "PENDING"       # PENDING, APPROVED, REJECTED, REQUEST_REVISION, HOLD
    reviewer: Optional[str] = None
    reviewer_notes: Optional[str] = None
    submitted_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    decision_timestamp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ApprovalQueue:
    """Manages filesystem queue mirroring and enforces single authoritative state."""

    def __init__(self, db: Optional[Database] = None, config=None):
        self.config = config or get_config()
        self.db = db or get_db()
        self.mgr = ApprovalManager(self.db, self.config)

        self.root_queue_dir = self.config.resolve_path("queue")
        self.needs_ok_dir = self.root_queue_dir / "needs-your-ok"
        self.needs_rev_dir = self.root_queue_dir / "needs-revision"
        self.rejected_dir = self.root_queue_dir / "rejected"
        self.completed_dir = self.root_queue_dir / "completed"

        for d in [self.needs_ok_dir, self.needs_rev_dir, self.rejected_dir, self.completed_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def enqueue_for_review(
        self,
        task_id: str,
        production_job_id: int,
        title: str,
        artifact_path: str,
        agent_responsible: str = "production_agent",
        evidence_refs: Optional[List[str]] = None,
        quality_check_results: Optional[Dict[str, Any]] = None,
    ) -> ApprovalItem:
        """Creates review item and writes to queue/needs-your-ok/."""
        item = ApprovalItem(
            task_id=task_id,
            production_job_id=production_job_id,
            title=title,
            artifact_path=artifact_path,
            agent_responsible=agent_responsible,
            evidence_refs=evidence_refs or [],
            quality_check_results=quality_check_results or {"qa_passed": True},
        )

        # Write to queue/needs-your-ok/<job_id>.json
        q_file = self.needs_ok_dir / f"job_{production_job_id}.json"
        q_file.write_text(json.dumps(item.to_dict(), indent=2), encoding="utf-8")
        logger.info(f"Queued job #{production_job_id} into {q_file.name}")
        return item

    def decide(
        self,
        production_job_id: int,
        decision: str,                        # APPROVE, REJECT, REQUEST_REVISION, HOLD
        reviewer_name: str = "Human Owner",
        notes: str = "",
    ) -> Dict[str, Any]:
        """
        Processes human owner decision.
        Prevents agent self-approval and moves review packet to appropriate folder.
        """
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        src_file = self.needs_ok_dir / f"job_{production_job_id}.json"

        # Load existing item if file exists
        if src_file.exists():
            item_data = json.loads(src_file.read_text(encoding="utf-8"))
            # Prevent agent self-approval
            if reviewer_name.lower() == item_data.get("agent_responsible", "").lower():
                raise ApprovalSelfCheckError(f"Agent '{reviewer_name}' cannot approve its own work.")
        else:
            item_data = {
                "production_job_id": production_job_id,
                "title": f"Job #{production_job_id}",
                "artifact_path": "",
                "agent_responsible": "production_agent",
            }

        item_data["owner_decision"] = decision.upper()
        item_data["reviewer"] = reviewer_name
        item_data["reviewer_notes"] = notes
        item_data["decision_timestamp"] = now

        decision_upper = decision.upper()

        if decision_upper == "APPROVE":
            # Delegate to existing ApprovalManager
            mgr_res = self.mgr.approve_reel(production_job_id, reviewer_name=reviewer_name, notes=notes)
            dest = self.completed_dir / f"job_{production_job_id}.json"
            dest.write_text(json.dumps(item_data, indent=2), encoding="utf-8")
            if src_file.exists():
                src_file.unlink()
            return {"status": "APPROVED", "mgr_result": mgr_res, "reviewer": reviewer_name, "notes": notes}

        elif decision_upper == "REJECT":
            mgr_res = self.mgr.reject_reel(production_job_id, reviewer_name=reviewer_name, reason=notes)
            dest = self.rejected_dir / f"job_{production_job_id}.json"
            dest.write_text(json.dumps(item_data, indent=2), encoding="utf-8")
            if src_file.exists():
                src_file.unlink()
            return {"status": "REJECTED", "mgr_result": mgr_res, "reviewer": reviewer_name, "notes": notes}

        elif decision_upper == "REQUEST_REVISION":
            with self.db.transaction() as conn:
                conn.execute(
                    "UPDATE production_jobs SET status = 'NEEDS_REVISION', updated_at = ? WHERE id = ?",
                    (now, production_job_id),
                )
                conn.execute(
                    "UPDATE approvals SET status = 'NEEDS_REVISION', decision = 'REQUEST_REVISION', reviewer = ?, reviewer_notes = ?, reviewed_at = ? WHERE production_job_id = ?",
                    (reviewer_name, notes, now, production_job_id),
                )
            dest = self.needs_rev_dir / f"job_{production_job_id}.json"
            dest.write_text(json.dumps(item_data, indent=2), encoding="utf-8")
            if src_file.exists():
                src_file.unlink()
            return {"status": "NEEDS_REVISION", "notes": notes}

        elif decision_upper == "HOLD":
            dest = self.needs_ok_dir / f"job_{production_job_id}.json"
            dest.write_text(json.dumps(item_data, indent=2), encoding="utf-8")
            return {"status": "HOLD", "notes": notes}

        raise ValueError(f"Unknown decision: {decision}. Allowed: APPROVE, REJECT, REQUEST_REVISION, HOLD")

    def list_pending_approvals(self) -> List[Dict[str, Any]]:
        """Lists all items in queue/needs-your-ok/."""
        items = []
        for f in self.needs_ok_dir.glob("*.json"):
            try:
                items.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                continue
        return items

    def list_completed_approvals(self) -> List[Dict[str, Any]]:
        """Lists all items in queue/completed/."""
        items = []
        for f in self.completed_dir.glob("*.json"):
            try:
                items.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                continue
        return items

    def list_needs_revision(self) -> List[Dict[str, Any]]:
        """Lists all items in queue/needs-revision/."""
        items = []
        for f in self.needs_rev_dir.glob("*.json"):
            try:
                items.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                continue
        return items

    def list_rejected(self) -> List[Dict[str, Any]]:
        """Lists all items in queue/rejected/."""
        items = []
        for f in self.rejected_dir.glob("*.json"):
            try:
                items.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                continue
        return items


def get_approval_queue(db: Optional[Database] = None) -> ApprovalQueue:
    return ApprovalQueue(db)

