"""
SUPER.INTELLIGENCEEE — Publishing Queue Module
Manages weekly publishing slots (5 Reels/week: Mon-Fri) in SQLite.
"""

from __future__ import annotations

import datetime
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import get_config
from core.database import Database

logger = logging.getLogger("super_intelligence.publishing_queue")


class PublishingQueue:
    """Manages the 5-reel weekly publishing pipeline and slot scheduling."""

    def __init__(self, db: Optional[Database] = None, config=None):
        self.config = config or get_config()
        self.db = db or Database()
        self.weekly_target = self.config.get("publishing.weekly_target", 5)

    def get_next_available_slot(self) -> datetime.datetime:
        """Calculates next upcoming weekday slot (Monday through Friday at 09:00 AM)."""
        now = datetime.datetime.now()
        # Find next weekday
        candidate = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if candidate <= now:
            candidate += datetime.timedelta(days=1)

        # Skip weekends (Saturday=5, Sunday=6)
        while candidate.weekday() >= 5:
            candidate += datetime.timedelta(days=1)

        # Check existing queue for clashes
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT scheduled_time FROM publishing_queue WHERE status IN ('QUEUED', 'SCHEDULED') ORDER BY scheduled_time DESC LIMIT 1"
            )
            row = cursor.fetchone()
            if row and row["scheduled_time"]:
                try:
                    last_sched = datetime.datetime.fromisoformat(row["scheduled_time"])
                    if candidate <= last_sched:
                        candidate = last_sched + datetime.timedelta(days=1)
                        while candidate.weekday() >= 5:
                            candidate += datetime.timedelta(days=1)
                except Exception:
                    pass

        return candidate

    def enqueue_reel(
        self,
        production_job_id: int,
        title: str,
        video_path: Path | str,
        caption_text: str,
        hashtags: List[str],
        scheduled_time: Optional[datetime.datetime] = None,
    ) -> int:
        """Enqueues an approved reel into the weekly queue."""
        slot = scheduled_time or self.get_next_available_slot()
        path = str(Path(video_path).resolve())
        tag_str = " ".join([h if h.startswith("#") else f"#{h}" for h in hashtags])

        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO publishing_queue (
                    production_job_id, job_id, title, caption, caption_text,
                    scheduled_time, scheduled_for, status, video_path,
                    hashtags, retry_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'SCHEDULED', ?, ?, 0)
                """,
                (
                    production_job_id,
                    production_job_id,
                    title,
                    caption_text,
                    caption_text,
                    slot.isoformat(),
                    slot.isoformat(),
                    path,
                    tag_str,
                ),
            )
            queue_id = cursor.lastrowid
            logger.info(f"Enqueued Reel #{production_job_id} into slot {slot.strftime('%A, %b %d %I:%M %p')}")
            return queue_id

    def list_queue(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists items in the publishing queue."""
        query = "SELECT * FROM publishing_queue"
        params = []
        if status:
            query += " WHERE status = ?"
            params.append(status)
        query += " ORDER BY scheduled_time ASC"

        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

