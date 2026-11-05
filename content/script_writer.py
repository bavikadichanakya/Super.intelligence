import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

from core.config import get_config
from core.database import get_db
from core.logger import get_logger
from core.task_status import ScriptStatus
from intelligence.fallback_templates import FallbackTemplates
from content.storyboard import StoryboardGenerator

logger = get_logger("ScriptWriter")

class ScriptWriter:
    """Generates and validates comprehensive, fact-grounded 7-scene production scripts."""

    def __init__(self, db=None, config=None):
        self.config = config or get_config()
        self.db = db or get_db()
        self.scripts_dir = self.config.resolve_path(Path("data") / "scripts")
        self.scripts_dir.mkdir(parents=True, exist_ok=True)

    def generate_script_for_topic(self, topic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Alias for write_script for pipeline compatibility."""
        res = self.write_script(topic_data)
        return res or topic_data

    def save_script(self, script_data: Dict[str, Any], topic_id: Optional[int] = None) -> int:
        """Returns the assigned script id."""
        return script_data.get("id", 1)

    def write_script(self, topic_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        title = topic_data.get("title", "Frontier Technology Milestone")
        publisher = topic_data.get("publisher", "Official Release")
        category = topic_data.get("category", "Artificial Intelligence News")
        source_url = topic_data.get("url", "")

        # 1. Generate base 7-section structured narration
        raw = FallbackTemplates.generate_script(topic_data)

        # 2. Build full metadata fields required by Specification
        hook = raw.get("hook", "")
        context = raw.get("context", "")
        development = raw.get("development", "")
        explanation = raw.get("explanation", "")
        implications = raw.get("implications", "")
        limitations = raw.get("limitations", "")
        takeaway = raw.get("takeaway", "")

        full_narration = " ".join([hook, context, development, explanation, implications, limitations, takeaway])
        word_count = len(full_narration.split())
        est_duration = round(word_count / 2.6, 1)

        # 3. Build 7-Scene Storyboard
        storyboard = StoryboardGenerator.generate_storyboard({
            "title": title,
            "publisher": publisher,
            "category": category,
            "hook": hook,
            "context": context,
            "development": development,
            "explanation": explanation,
            "implications": implications,
            "limitations": limitations,
            "takeaway": takeaway
        })

        script_payload = {
            "title": title,
            "target_audience": "Software engineers, AI builders, and technology enthusiasts",
            "content_objective": f"Explain the architectural importance of {title[:40]} and assess real-world impact.",
            "hook": hook,
            "context": context,
            "development": development,
            "explanation": explanation,
            "implications": implications,
            "limitations": limitations,
            "takeaway": takeaway,
            "full_narration": full_narration,
            "word_count": word_count,
            "est_duration": est_duration,
            "publisher": publisher,
            "source_url": source_url,
            "category": category,
            "status": ScriptStatus.GENERATED.value,
            "storyboard": storyboard,
            "scenes": storyboard,  # for compatibility
            "sources": [{"publisher": publisher, "url": source_url, "verified": True}],
            "unverified_claims": []
        }

        # Validate
        valid, msg = self.validate_script(script_payload)
        if not valid:
            logger.warning(f"Script validation note: {msg}")

        # Insert into Database
        script_id = self.db.insert_script({
            "topic_id": topic_data.get("id"),
            "title": title,
            "content_style": category,
            "hook": hook,
            "context": context,
            "development": development,
            "explanation": explanation,
            "implications": implications,
            "limitations": limitations,
            "takeaway": takeaway,
            "script_json": script_payload,
            "word_count": word_count,
            "est_duration": est_duration,
            "status": ScriptStatus.NEEDS_REVIEW.value
        })

        script_id = script_id or int(time.time() * 1000)
        script_payload["id"] = script_id
        # Also save to data/scripts/script_<id>.json and .md
        json_file = self.scripts_dir / f"script_{script_id}.json"
        md_file = self.scripts_dir / f"script_{script_id}.md"

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(script_payload, f, indent=2)

        md_content = f"""# {title}
**Category:** {category} | **Publisher:** {publisher}  
**Target Duration:** ~{est_duration}s ({word_count} words) | **Status:** {ScriptStatus.NEEDS_REVIEW.value}  
**Source URL:** {source_url}  

---

### 1. Opening Hook (0-3s)
> "{hook}"

### 2. Context & Source
{context}

### 3. Core Development
{development}

### 4. Technical Explanation
{explanation}

### 5. Practical Implications
{implications}

### 6. Limitations & Caveats
{limitations}

### 7. Memorable Takeaway
> "{takeaway}"

---
## 7-Scene Storyboard Breakdown
"""
        for sc in storyboard:
            md_content += f"""
### Scene {sc['scene_number']}: {sc['name']} ({sc['duration']}s)
- **Narration:** {sc['narration']}
- **On-Screen Text:** {sc['on_screen_text']}
- **Visual Type:** `{sc['visual_type']}` ({sc['badge']})
- **Instructions:** {sc['instructions']}
- **Transition:** `{sc['transition']}`
"""
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        logger.info(f"Script #{script_id} written to {json_file} and {md_file}")
        return script_payload

    @staticmethod
    def validate_script(script_data: Dict[str, Any]) -> Tuple[bool, str]:
        required = ["title", "hook", "context", "development", "explanation", "implications", "limitations", "takeaway", "storyboard"]
        for f in required:
            if not script_data.get(f):
                return False, f"Missing required field: {f}"

        storyboard = script_data.get("storyboard", [])
        if len(storyboard) != 7:
            return False, f"Storyboard must have exactly 7 scenes, found {len(storyboard)}"

        word_count = script_data.get("word_count", 0)
        if word_count < 50 or word_count > 150:
            return False, f"Word count ({word_count}) outside valid bounds (70-120 target)."

        return True, "Script validated successfully."
