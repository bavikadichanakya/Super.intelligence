from typing import Dict, Any, List, Optional
from datetime import datetime
from core.database import get_db
from core.logger import get_logger

logger = get_logger("PerformanceTracker")

class PerformanceTracker:
    """Tracks real audience metrics, engagement rates, and viral indicators for published Reels."""

    def __init__(self):
        self.db = get_db()

    def record_metrics(
        self,
        publishing_id: Optional[int],
        reel_title: str,
        views: int = 0,
        reach: int = 0,
        likes: int = 0,
        comments: int = 0,
        shares: int = 0,
        saves: int = 0,
        watch_time_avg: float = 0.0,
        followers_gained: int = 0
    ) -> int:
        entry = {
            "publishing_id": publishing_id,
            "reel_title": reel_title,
            "views": max(0, views),
            "reach": max(0, reach),
            "likes": max(0, likes),
            "comments": max(0, comments),
            "shares": max(0, shares),
            "saves": max(0, saves),
            "watch_time_avg": max(0.0, float(watch_time_avg)),
            "followers_gained": max(0, followers_gained)
        }
        entry_id = self.db.record_analytics(entry)
        logger.info(f"Recorded analytics for '{reel_title}': {views} views, {likes} likes, {saves} saves")
        return entry_id

    def get_summary(self) -> Dict[str, Any]:
        records = self.db.get_analytics(limit=200)
        if not records:
            return {
                "total_reels_tracked": 0,
                "total_views": 0,
                "total_reach": 0,
                "total_likes": 0,
                "total_shares": 0,
                "total_saves": 0,
                "avg_engagement_rate": 0.0,
                "avg_save_rate": 0.0,
                "records": []
            }

        total_views = sum(r.get("views", 0) for r in records)
        total_reach = sum(r.get("reach", 0) for r in records)
        total_likes = sum(r.get("likes", 0) for r in records)
        total_comments = sum(r.get("comments", 0) for r in records)
        total_shares = sum(r.get("shares", 0) for r in records)
        total_saves = sum(r.get("saves", 0) for r in records)

        interactions = total_likes + total_comments + total_shares + total_saves
        denom = total_reach if total_reach > 0 else (total_views if total_views > 0 else 1)
        avg_eng_rate = round((interactions / denom) * 100, 2)
        avg_save_rate = round((total_saves / (total_views or 1)) * 100, 2)

        # Enhance records with calculated rates
        for r in records:
            v = r.get("views", 0)
            rec_interactions = r.get("likes", 0) + r.get("comments", 0) + r.get("shares", 0) + r.get("saves", 0)
            r["engagement_rate"] = round((rec_interactions / max(v, 1)) * 100, 2)
            r["save_rate"] = round((r.get("saves", 0) / max(v, 1)) * 100, 2)

        return {
            "total_reels_tracked": len(records),
            "total_views": total_views,
            "total_reach": total_reach,
            "total_likes": total_likes,
            "total_shares": total_shares,
            "total_saves": total_saves,
            "avg_engagement_rate": avg_eng_rate,
            "avg_save_rate": avg_save_rate,
            "records": records
        }

