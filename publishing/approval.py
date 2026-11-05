"""
SUPER.INTELLIGENCEEE — Human-in-the-Loop Review & Approval Module
Enforces editorial verification before videos move to approved state or publishing queue.
"""

from __future__ import annotations

import datetime
import logging
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import get_config
from core.database import Database
from publishing.queue import PublishingQueue

logger = logging.getLogger("super_intelligence.approval")


class ApprovalManager:
    """Manages video review, revision requests, and promotional publishing approval."""

    def __init__(self, db: Optional[Database] = None, config=None):
        self.config = config or get_config()
        self.db = db or Database()
        self.queue = PublishingQueue(self.db, self.config)
        self.approved_dir = self.config.resolve_path("output/approved")
        self.failed_dir = self.config.resolve_path("output/failed")
        self.approved_dir.mkdir(parents=True, exist_ok=True)
        self.failed_dir.mkdir(parents=True, exist_ok=True)

    def record_submission(self, production_job_id: int) -> int:
        """Records a new production job into the pending approval table."""
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO approvals (
                    entity_type, entity_id, production_job_id, decision, status, submitted_at
                ) VALUES ('video', ?, ?, 'PENDING', 'PENDING_REVIEW', ?)
                """,
                (production_job_id, production_job_id, datetime.datetime.now().isoformat()),
            )
            return cursor.lastrowid

    def approve_reel(
        self,
        production_job_id: int,
        reviewer_name: str = "Lead Editor",
        notes: str = "Verified technical quality, factual accuracy, and audio synchronization.",
    ) -> Dict[str, Any]:
        """
        Approves a reel: moves file to output/approved/, updates database, and enqueues to weekly queue.
        """
        now = datetime.datetime.now().isoformat()

        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM production_jobs WHERE id = ?", (production_job_id,)
            )
            p_job = cursor.fetchone()
            if not p_job:
                raise ValueError(f"Production job #{production_job_id} not found.")

            draft_path = Path(p_job["output_video_path"]) if p_job["output_video_path"] else None
            approved_path = None

            if draft_path and draft_path.exists():
                approved_path = self.approved_dir / draft_path.name
                shutil.copyfile(draft_path, approved_path)

            # Update production_jobs
            cursor.execute(
                """
                UPDATE production_jobs 
                SET status = 'APPROVED', updated_at = ?, output_video_path = ?
                WHERE id = ?
                """,
                (now, str(approved_path or draft_path), production_job_id),
            )

            # Update approvals
            cursor.execute(
                """
                UPDATE approvals 
                SET status = 'APPROVED', decision = 'APPROVED', reviewer = ?, reviewer_notes = ?, reviewed_at = ?
                WHERE production_job_id = ? OR entity_id = ?
                """,
                (reviewer_name, notes, now, production_job_id, production_job_id),
            )

        # Enqueue into weekly publishing queue after transaction commit to avoid SQLite nested connection locks
        q_id = None
        if approved_path:
            q_id = self.queue.enqueue_reel(
                production_job_id=production_job_id,
                title=f"Reel #{production_job_id}",
                video_path=approved_path,
                caption_text="Autonomous AI & tech intelligence briefing. #AI #Tech #Innovation",
                hashtags=["AI", "ArtificialIntelligence", "TechNews", "FutureTech"],
            )

        logger.info(f"Reel #{production_job_id} APPROVED by {reviewer_name}")
        return {
            "production_job_id": production_job_id,
            "status": "APPROVED",
            "approved_path": str(approved_path or draft_path),
            "queue_id": q_id,
        }

    def reject_reel(
        self,
        production_job_id: int,
        reviewer_name: str = "Lead Editor",
        reason: str = "Quality standards not met.",
    ) -> Dict[str, Any]:
        """Rejects a reel, moving it to output/failed/ and logging reason."""
        now = datetime.datetime.now().isoformat()

        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM production_jobs WHERE id = ?", (production_job_id,)
            )
            p_job = cursor.fetchone()

            if p_job and p_job["output_video_path"]:
                draft_path = Path(p_job["output_video_path"])
                if draft_path.exists():
                    failed_path = self.failed_dir / draft_path.name
                    shutil.move(draft_path, failed_path)

            cursor.execute(
                "UPDATE production_jobs SET status = 'FAILED', updated_at = ? WHERE id = ?",
                (now, production_job_id),
            )
            cursor.execute(
                """
                UPDATE approvals 
                SET status = 'REJECTED', decision = 'REJECTED', reviewer = ?, reviewer_notes = ?, reviewed_at = ?
                WHERE production_job_id = ? OR entity_id = ?
                """,
                (reviewer_name, reason, now, production_job_id, production_job_id),
            )

            logger.info(f"Reel #{production_job_id} REJECTED by {reviewer_name}: {reason}")
            return {
                "production_job_id": production_job_id,
                "status": "REJECTED",
                "reason": reason,
            }
