from typing import Dict, Any, Tuple
from core.database import get_db
from core.logger import get_logger

logger = get_logger("FactChecking")

VALID_STATUSES = [
    "DISCOVERED",
    "SHORTLISTED",
    "RESEARCHED",
    "VERIFIED",
    "SCRIPT_READY",
    "APPROVED",
    "REJECTED"
]

class FactChecker:
    """Manages the verification state machine and human editorial safeguards."""

    def __init__(self):
        self.db = get_db()

    @staticmethod
    def validate_transition(current_status: str, target_status: str) -> Tuple[bool, str]:
        if target_status not in VALID_STATUSES:
            return False, f"Invalid status: {target_status}. Allowed: {VALID_STATUSES}"
        
        # Human rejection is allowed from any stage
        if target_status == "REJECTED":
            return True, "Article rejected."

        # Strict progression rules
        hierarchy = {
            "DISCOVERED": 0,
            "SHORTLISTED": 1,
            "RESEARCHED": 2,
            "VERIFIED": 3,
            "SCRIPT_READY": 4,
            "APPROVED": 5
        }

        current_level = hierarchy.get(current_status, -1)
        target_level = hierarchy.get(target_status, -1)

        # Allow moving forward or backward in editorial workflow
        if target_status == "VERIFIED" and current_level < hierarchy["SHORTLISTED"]:
            return False, "Articles must be SHORTLISTED and RESEARCHED before being marked VERIFIED."

        return True, "Transition authorized."

    def update_status(self, article_id: int, target_status: str, notes: str = "") -> Tuple[bool, str]:
        articles = self.db.get_articles(limit=1000)
        target_art = next((a for a in articles if a["id"] == article_id), None)
        if not target_art:
            return False, f"Article ID {article_id} not found."

        current_status = target_art["status"]
        valid, msg = self.validate_transition(current_status, target_status)
        if not valid:
            logger.warning(f"Blocked invalid status transition for article {article_id}: {msg}")
            return False, msg

        success = self.db.update_article_status(article_id, target_status, notes=notes if notes else target_art.get("notes"))
        if success:
            logger.info(f"Article {article_id} transitioned from {current_status} -> {target_status}")
            return True, f"Successfully moved to {target_status}"
        return False, "Database update failed."

    def verify_article(self, article_id: int, source_verified: bool, facts_checked: bool, reviewer_notes: str) -> Tuple[bool, str]:
        """Verify an article after affirmative source check and editorial sanity review."""
        if not source_verified or not facts_checked:
            return False, "Cannot verify story without affirmative source URL verification and fact checking."

        notes_entry = f"Verified: {reviewer_notes.strip()}"
        return self.update_status(article_id, "VERIFIED", notes=notes_entry)
