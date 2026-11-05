from datetime import datetime, date, timedelta
from typing import Dict, Any, List

from core.database import get_db
from core.logger import get_logger

logger = get_logger("Scheduler")

WEEKLY_PLAN = {
    0: {
        "day": "Monday",
        "action": "Discovery & Ranking",
        "description": "Collect AI & deep-tech RSS stories, deduplicate, score, and shortlist top 5-10 candidates."
    },
    1: {
        "day": "Tuesday",
        "action": "Research & Scripting",
        "description": "Fact-check shortlisted topics, verify primary sources, generate 7-scene structured JSON scripts."
    },
    2: {
        "day": "Wednesday",
        "action": "Asset Prep & Batch Render Part 1",
        "description": "Generate editorial graphics, Ken Burns scenes, TTS narration, and render Reels 1 to 3."
    },
    3: {
        "day": "Thursday",
        "action": "Batch Render Part 2 & Review",
        "description": "Render Reels 4 and 5 sequentially, run FFprobe quality validation, review final drafts."
    },
    4: {
        "day": "Friday",
        "action": "Publishing Queue & Weekly Analytics",
        "description": "Finalize captions and hashtags, schedule 5 weekly Reels, and generate performance analytics."
    },
    5: {
        "day": "Saturday",
        "action": "Weekly Review",
        "description": "Review Instagram audience engagement and optimize upcoming hooks."
    },
    6: {
        "day": "Sunday",
        "action": "Topic Pipeline Curation",
        "description": "Curate watchlist of upcoming AI conferences, model drops, and open-source releases."
    }
}

class Scheduler:
    """Manages the 5-Reel weekly content calendar and production stages."""
    
    def __init__(self):
        self.db = get_db()

    def get_today_schedule(self) -> Dict[str, Any]:
        today_idx = datetime.utcnow().weekday()
        plan = WEEKLY_PLAN.get(today_idx, WEEKLY_PLAN[0])
        stats = self.db.get_dashboard_stats()
        
        return {
            "weekday_index": today_idx,
            "day_name": plan["day"],
            "recommended_action": plan["action"],
            "description": plan["description"],
            "current_status": {
                "discovered": stats["discovered_topics"],
                "scripts_approved": stats["scripts_approved"],
                "rendered": stats["rendered_videos"],
                "queued": stats["queued_videos"],
                "weekly_target": 5,
                "target_met": stats["rendered_videos"] >= 5
            }
        }

    def get_full_week_schedule(self) -> List[Dict[str, Any]]:
        today_idx = datetime.utcnow().weekday()
        schedule = []
        for idx in range(7):
            item = dict(WEEKLY_PLAN[idx])
            item["is_today"] = (idx == today_idx)
            schedule.append(item)
        return schedule
