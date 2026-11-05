import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from core.database import get_db
from core.logger import get_logger
from core.config_manager import get_config
from analytics.performance_tracker import PerformanceTracker

logger = get_logger("WeeklyReport")

class WeeklyReport:
    """Generates comprehensive weekly media performance digests and tactical recommendations."""

    def __init__(self):
        self.db = get_db()
        self.config = get_config()
        self.tracker = PerformanceTracker()
        self.reports_dir = self.config.resolve_path(Path("output") / "reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(self) -> Dict[str, Any]:
        stats = self.db.get_dashboard_stats()
        summary = self.tracker.get_summary()
        records = summary.get("records", [])

        # Categorize top performers if analytics exist
        top_by_views = sorted(records, key=lambda x: x.get("views", 0), reverse=True)[:3]
        top_by_saves = sorted(records, key=lambda x: x.get("saves", 0), reverse=True)[:3]

        report_date = datetime.utcnow().strftime("%Y-%m-%d")
        report_filename = f"weekly_report_{report_date}.md"
        report_path = self.reports_dir / report_filename

        # Formulate tactical insights
        insights = [
            "Maintain technical precision in Opening Hooks; viewers respond strongest to specific architectural metrics over generalized hype.",
            "Visual scenes displaying architecture flowcharts consistently generate higher save rates.",
            "Ensure source publication name is clearly featured in Scene 2 to solidify journalistic credibility.",
            "Target weekly quota of 5 Reels on Mon/Tue/Wed/Thu/Fri maintains optimal algorithmic distribution."
        ]

        markdown_body = f"""# SUPER.INTELLIGENCEEE — WEEKLY MEDIA REPORT
**Date:** {report_date}  
**System Status:** Operational | **Target:** 5 Reels/Week  

---

## 1. Executive Summary & KPIs
- **Total Topics Discovered:** {stats['discovered_topics']}
- **Verified Editorial Stories:** {stats['verified_topics']}
- **Scripts Prepared:** {stats['scripts_draft'] + stats['scripts_approved']}
- **Reels Rendered (Completed):** {stats['rendered_videos']}
- **Reels Queued for Publishing:** {stats['queued_videos']}
- **Reels Published:** {stats['published_videos']}

## 2. Audience Engagement Analytics
- **Total Tracked Views:** {summary['total_views']:,}
- **Total Accounts Reached:** {summary['total_reach']:,}
- **Total Saves:** {summary['total_saves']:,}
- **Total Shares:** {summary['total_shares']:,}
- **Average Engagement Rate:** {summary['avg_engagement_rate']}%
- **Average Save Rate:** {summary['avg_save_rate']}%

## 3. High-Performing Content Highlights
"""
        if top_by_saves:
            for i, r in enumerate(top_by_saves, 1):
                markdown_body += f"- **#{i} Most Saved:** *{r['reel_title']}* — {r.get('saves', 0)} saves ({r.get('views', 0)} views)\n"
        else:
            markdown_body += "*No published analytics recorded yet for this weekly cycle. Analytics populate once published Reels metrics are tracked.*\n"

        markdown_body += f"""
## 4. Editorial Recommendations for Next 5-Reel Production Cycle
"""
        for rec in insights:
            markdown_body += f"- {rec}\n"

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(markdown_body)

        logger.info(f"Generated weekly report: {report_path}")

        return {
            "report_date": report_date,
            "report_file": str(report_path),
            "stats": stats,
            "summary": summary,
            "top_by_views": top_by_views,
            "top_by_saves": top_by_saves,
            "recommendations": insights,
            "markdown_content": markdown_body
        }

