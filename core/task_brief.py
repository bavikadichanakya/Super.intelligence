"""
SUPER.INTELLIGENCEEE — Structured Task Brief & Lifecycle State Machine
Canonical task contract coordinating inter-agent work briefs across departments.
Enforces strict legal state transitions and persistent SQLite execution history.
"""

from __future__ import annotations

import datetime
import json
import logging
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from core.database import Database, get_db

logger = logging.getLogger("super_intelligence.task_brief")


class TaskLifecycleStatus(str, Enum):
    """Canonical task state machine states."""
    PENDING = "PENDING"
    PLANNED = "PLANNED"
    DISPATCHED = "DISPATCHED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    QUALITY_CHECK = "QUALITY_CHECK"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    NEEDS_REVISION = "NEEDS_REVISION"
    EXPIRED = "EXPIRED"


class TaskPriority(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"


# Valid forward and backward state transitions
VALID_TRANSITIONS: Dict[TaskLifecycleStatus, Set[TaskLifecycleStatus]] = {
    TaskLifecycleStatus.PENDING: {
        TaskLifecycleStatus.PLANNED,
        TaskLifecycleStatus.DISPATCHED,
        TaskLifecycleStatus.RUNNING,
        TaskLifecycleStatus.BLOCKED,
        TaskLifecycleStatus.CANCELLED,
    },
    TaskLifecycleStatus.PLANNED: {
        TaskLifecycleStatus.DISPATCHED,
        TaskLifecycleStatus.RUNNING,
        TaskLifecycleStatus.CANCELLED,
        TaskLifecycleStatus.BLOCKED,
    },
    TaskLifecycleStatus.DISPATCHED: {
        TaskLifecycleStatus.RUNNING,
        TaskLifecycleStatus.CANCELLED,
        TaskLifecycleStatus.FAILED,
    },
    TaskLifecycleStatus.RUNNING: {
        TaskLifecycleStatus.COMPLETED,
        TaskLifecycleStatus.FAILED,
        TaskLifecycleStatus.CANCELLED,
        TaskLifecycleStatus.BLOCKED,
    },
    TaskLifecycleStatus.COMPLETED: {
        TaskLifecycleStatus.QUALITY_CHECK,
        TaskLifecycleStatus.AWAITING_APPROVAL,
        TaskLifecycleStatus.NEEDS_REVISION,
    },
    TaskLifecycleStatus.QUALITY_CHECK: {
        TaskLifecycleStatus.AWAITING_APPROVAL,
        TaskLifecycleStatus.NEEDS_REVISION,
        TaskLifecycleStatus.FAILED,
    },
    TaskLifecycleStatus.AWAITING_APPROVAL: {
        TaskLifecycleStatus.APPROVED,
        TaskLifecycleStatus.REJECTED,
        TaskLifecycleStatus.NEEDS_REVISION,
        TaskLifecycleStatus.CANCELLED,
    },
    TaskLifecycleStatus.APPROVED: {
        TaskLifecycleStatus.PUBLISHED,
        TaskLifecycleStatus.CANCELLED,
        TaskLifecycleStatus.FAILED,
    },
    TaskLifecycleStatus.NEEDS_REVISION: {
        TaskLifecycleStatus.PLANNED,
        TaskLifecycleStatus.DISPATCHED,
        TaskLifecycleStatus.CANCELLED,
    },
    TaskLifecycleStatus.PUBLISHED: set(),  # Terminal state
    TaskLifecycleStatus.FAILED: {TaskLifecycleStatus.PLANNED, TaskLifecycleStatus.CANCELLED}, # Allow retry
    TaskLifecycleStatus.REJECTED: set(),
    TaskLifecycleStatus.CANCELLED: set(),
    TaskLifecycleStatus.BLOCKED: {TaskLifecycleStatus.PLANNED, TaskLifecycleStatus.CANCELLED},
    TaskLifecycleStatus.EXPIRED: set(),
}


@dataclass
class TaskBrief:
    """Canonical task contract coordinating inter-agent work briefs."""
    task_id: str
    agent: str                                # Department identifier
    objective: str                            # Plain-text assignment statement
    priority: TaskPriority = TaskPriority.NORMAL
    channel: str = "instagram"                # instagram, youtube, multi
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    input_refs: List[str] = field(default_factory=list)
    evidence_refs: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=lambda: {
        "budget": 0.0,
        "human_approval_required": True,
        "zero_cost_mode": True,
    })
    expected_output: str = "result.json"
    approval_status: str = "PENDING"          # PENDING, APPROVED, REJECTED
    execution_status: TaskLifecycleStatus = TaskLifecycleStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    updated_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def transition_to(self, target_status: TaskLifecycleStatus, reason: str = "") -> bool:
        """Enforces legal state transitions and updates timestamps."""
        allowed = VALID_TRANSITIONS.get(self.execution_status, set())
        # Global emergency cancellation is always permissible
        if target_status == TaskLifecycleStatus.CANCELLED or target_status in allowed:
            logger.info(f"Task [{self.task_id}] transition: {self.execution_status.value} -> {target_status.value} ({reason})")
            self.execution_status = target_status
            self.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
            return True

        err_msg = f"Illegal task transition: cannot move {self.task_id} from {self.execution_status.value} to {target_status.value}"
        logger.error(err_msg)
        raise ValueError(err_msg)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["priority"] = self.priority.value if hasattr(self.priority, "value") else str(self.priority)
        d["execution_status"] = self.execution_status.value if hasattr(self.execution_status, "value") else str(self.execution_status)
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TaskBrief:
        p_raw = data.get("priority", "NORMAL")
        priority = TaskPriority(p_raw) if p_raw in TaskPriority.__members__ else TaskPriority.NORMAL

        s_raw = data.get("execution_status", "PENDING")
        status = TaskLifecycleStatus(s_raw) if s_raw in TaskLifecycleStatus.__members__ else TaskLifecycleStatus.PENDING

        return cls(
            task_id=str(data.get("task_id", f"TASK-{str(uuid.uuid4())[:8]}").upper()),
            agent=str(data.get("agent", "content_engine")),
            objective=str(data.get("objective", "Execute video workflow")),
            priority=priority,
            channel=str(data.get("channel", "instagram")),
            created_at=str(data.get("created_at", datetime.datetime.now(datetime.timezone.utc).isoformat())),
            input_refs=data.get("input_refs", []),
            evidence_refs=data.get("evidence_refs", []),
            constraints=data.get("constraints", {"budget": 0.0, "human_approval_required": True}),
            expected_output=str(data.get("expected_output", "result.json")),
            approval_status=str(data.get("approval_status", "PENDING")),
            execution_status=status,
            result=data.get("result"),
            error=data.get("error"),
            updated_at=str(data.get("updated_at", datetime.datetime.now(datetime.timezone.utc).isoformat())),
        )


class TaskBriefStore:
    """Persists structured task briefs into SQLite for cross-session durability."""

    def __init__(self, db: Optional[Database] = None):
        self.db = db or get_db()
        self._ensure_table()

    def _ensure_table(self):
        with self.db.transaction() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS task_briefs (
                    task_id TEXT PRIMARY KEY,
                    agent TEXT NOT NULL,
                    objective TEXT NOT NULL,
                    priority TEXT DEFAULT 'NORMAL',
                    channel TEXT DEFAULT 'instagram',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    input_refs TEXT,
                    evidence_refs TEXT,
                    constraints TEXT,
                    expected_output TEXT,
                    approval_status TEXT DEFAULT 'PENDING',
                    execution_status TEXT DEFAULT 'PENDING',
                    result TEXT,
                    error TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

    def save_brief(self, brief: TaskBrief) -> str:
        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO task_briefs (
                    task_id, agent, objective, priority, channel, created_at,
                    input_refs, evidence_refs, constraints, expected_output,
                    approval_status, execution_status, result, error, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    brief.task_id,
                    brief.agent,
                    brief.objective,
                    brief.priority.value,
                    brief.channel,
                    brief.created_at,
                    json.dumps(brief.input_refs),
                    json.dumps(brief.evidence_refs),
                    json.dumps(brief.constraints),
                    brief.expected_output,
                    brief.approval_status,
                    brief.execution_status.value,
                    json.dumps(brief.result) if brief.result else None,
                    brief.error,
                    brief.updated_at,
                ),
            )
        return brief.task_id

    def get_brief(self, task_id: str) -> Optional[TaskBrief]:
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM task_briefs WHERE task_id = ?", (task_id,))
            row = cursor.fetchone()
            if not row:
                return None
            d = dict(row)
            d["input_refs"] = json.loads(d["input_refs"]) if d.get("input_refs") else []
            d["evidence_refs"] = json.loads(d["evidence_refs"]) if d.get("evidence_refs") else []
            d["constraints"] = json.loads(d["constraints"]) if d.get("constraints") else {}
            d["result"] = json.loads(d["result"]) if d.get("result") else None
            return TaskBrief.from_dict(d)

    def list_briefs(self, status: Optional[str] = None, limit: int = 50) -> List[TaskBrief]:
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute(
                    "SELECT * FROM task_briefs WHERE execution_status = ? ORDER BY created_at DESC LIMIT ?",
                    (status, limit),
                )
            else:
                cursor.execute(
                    "SELECT * FROM task_briefs ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                )
            rows = cursor.fetchall()
            briefs = []
            for r in rows:
                d = dict(r)
                d["input_refs"] = json.loads(d["input_refs"]) if d.get("input_refs") else []
                d["evidence_refs"] = json.loads(d["evidence_refs"]) if d.get("evidence_refs") else []
                d["constraints"] = json.loads(d["constraints"]) if d.get("constraints") else {}
                d["result"] = json.loads(d["result"]) if d.get("result") else None
                briefs.append(TaskBrief.from_dict(d))
            return briefs

