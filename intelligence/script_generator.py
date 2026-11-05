from typing import Dict, Any, Optional
from core.database import get_db
from core.logger import get_logger
from intelligence.provider_manager import ProviderManager
from intelligence.scene_planner import ScenePlanner

logger = get_logger("ScriptGenerator")

class ScriptGenerator:
    """Manages script creation, validation against 30-45s / 70-110 words requirements, and persistence."""

    def __init__(self):
        self.provider_manager = ProviderManager()
        self.db = get_db()

    def create_script_for_article(self, article: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        logger.info(f"Generating structured script for article: {article.get('title')}")
        raw_script = self.provider_manager.generate_script(article)
        
        # Attach planned 7 scenes
        scenes = ScenePlanner.plan_scenes(raw_script)
        raw_script["scenes"] = scenes

        # Validate script
        is_valid, validation_msg = self.validate_script(raw_script)
        if not is_valid:
            logger.warning(f"Script validation warning: {validation_msg}")

        # Persist into DB
        script_record = {
            "article_id": article.get("id"),
            "title": raw_script.get("title", article.get("title")),
            "content_style": article.get("category", "Breaking AI News"),
            "hook": raw_script.get("hook", ""),
            "context": raw_script.get("context", ""),
            "development": raw_script.get("development", ""),
            "explanation": raw_script.get("explanation", ""),
            "implications": raw_script.get("implications", ""),
            "limitations": raw_script.get("limitations", ""),
            "takeaway": raw_script.get("takeaway", ""),
            "script_json": raw_script,
            "word_count": raw_script.get("word_count", 0),
            "est_duration": raw_script.get("est_duration", 35.0),
            "status": "DRAFT"
        }

        script_id = self.db.insert_script(script_record)
        if script_id:
            raw_script["id"] = script_id
            logger.info(f"Script saved with ID {script_id} (Words: {raw_script['word_count']}, Est Duration: {raw_script['est_duration']}s)")
            # Update article status to SCRIPT_READY
            if article.get("id"):
                self.db.update_article_status(article["id"], "SCRIPT_READY")
            return raw_script

        return None

    @staticmethod
    def validate_script(script_data: Dict[str, Any]) -> (bool, str):
        required_fields = ["hook", "context", "development", "explanation", "implications", "limitations", "takeaway", "scenes"]
        for field in required_fields:
            if not script_data.get(field):
                return False, f"Missing required script field: {field}"

        word_count = script_data.get("word_count", 0)
        if word_count < 50 or word_count > 140:
            return False, f"Word count ({word_count}) is outside target bounds (70-110 words recommended)."

        scenes = script_data.get("scenes", [])
        if len(scenes) != 7:
            return False, f"Scene count ({len(scenes)}) must be exactly 7 scenes."

        return True, "Script validated successfully."
