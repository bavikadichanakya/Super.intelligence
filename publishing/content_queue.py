from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

from core.database import get_db
from core.logger import get_logger
from core.config_manager import get_config

logger = get_logger("ContentQueue")

class ContentQueue:
    """Manages the 5-Reel weekly publishing calendar and queue lifecycle."""

    def __init__(self, db: Optional[Any] = None):
        self.db = db or get_db()
        self.config = get_config()

    def get_queue(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.db.get_publishing_queue(status=status)

    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        items = self.db.get_publishing_queue()
        return next((i for i in items if i["id"] == item_id), None)

    def update_schedule(self, item_id: int, new_datetime_str: str) -> bool:
        return self.db.update_publishing_item(item_id, {"scheduled_for": new_datetime_str})

    def update_status(self, item_id: int, new_status: str, notes: Optional[str] = None) -> bool:
        updates = {"status": new_status}
        if notes:
            updates["notes"] = notes
        if new_status == "PUBLISHED":
            updates["published_at"] = datetime.utcnow().isoformat()
        return self.db.update_publishing_item(item_id, updates)

    def assign_weekly_slots(self, week_start_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Takes up to 5 unassigned or queued items and schedules them evenly across
        Monday through Friday in the optimal engagement time slots.
        """
        start = week_start_date or datetime.utcnow()
        # Find next Monday
        days_ahead = (0 - start.weekday()) % 7
        if days_ahead == 0 and start.hour >= 18:
            days_ahead = 7
        monday = (start + timedelta(days=days_ahead)).replace(hour=11, minute=30, second=0, microsecond=0)

        posting_slots = [
            monday.replace(hour=11, minute=30),                     # Monday 11:30 AM
            (monday + timedelta(days=1)).replace(hour=15, minute=0),# Tuesday 3:00 PM
            (monday + timedelta(days=2)).replace(hour=18, minute=45),# Wednesday 6:45 PM
            (monday + timedelta(days=3)).replace(hour=11, minute=30),# Thursday 11:30 AM
            (monday + timedelta(days=4)).replace(hour=15, minute=0) # Friday 3:00 PM
        ]

        queued = self.db.get_publishing_queue(status="QUEUED")
        scheduled_count = 0
        scheduled_items = []

        for idx, item in enumerate(queued[:5]):
            slot = posting_slots[idx]
            slot_str = slot.strftime("%Y-%m-%d %H:%M:%S")
            self.db.update_publishing_item(item["id"], {
                "scheduled_for": slot_str,
                "status": "SCHEDULED"
            })
            item["scheduled_for"] = slot_str
            item["status"] = "SCHEDULED"
            scheduled_items.append(item)
            scheduled_count += 1

        logger.info(f"Assigned {scheduled_count} Reels to weekly schedule slots.")
        return scheduled_items

