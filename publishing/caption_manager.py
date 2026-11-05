import re
from typing import Dict, Any, List, Tuple
from core.config_manager import get_config
from core.logger import get_logger

logger = get_logger("CaptionManager")

class CaptionManager:
    """Manages Instagram caption formatting, character limits, and strategic hashtag clusters."""

    MAX_CAPTION_CHARS = 2200
    RECOMMENDED_TAG_COUNT = 15

    @classmethod
    def format_caption(cls, script_data: Dict[str, Any]) -> Dict[str, Any]:
        config = get_config()
        brand_handle = config.get("brand.handle", "@super.intelligenceee")

        title = script_data.get("title", "Breakthrough Technology Announcement")
        hook = script_data.get("hook", "")
        context = script_data.get("context", "")
        implications = script_data.get("implications", "")
        takeaway = script_data.get("takeaway", "")
        publisher = script_data.get("publisher", "Official Technical Documentation")
        source_url = script_data.get("source_url", "")
        category = script_data.get("category", "Artificial Intelligence News")

        # Category-targeted hashtags
        base_tags = [
            "#superintelligence", "#artificialintelligence", "#aimodels",
            "#techreels", "#machinelearning", "#futuretech", "#deeptech"
        ]

        cat_lower = category.lower()
        if "cyber" in cat_lower or "threat" in cat_lower:
            spec_tags = ["#cybersecurity", "#infosec", "#zeroday", "#privacy", "#netsec"]
        elif "robot" in cat_lower or "auto" in cat_lower:
            spec_tags = ["#robotics", "#humanoid", "#automation", "#hardware", "#embeddedai"]
        elif "model" in cat_lower or "release" in cat_lower:
            spec_tags = ["#frontierai", "#llm", "#openweight", "#neuralnetworks", "#aiagents"]
        elif "experiment" in cat_lower or "tutorial" in cat_lower:
            spec_tags = ["#aiexperiment", "#computervision", "#python", "#buildinpublic"]
        else:
            spec_tags = ["#innovation", "#softwareengineering", "#techtrends", "#nextgenai"]

        all_tags = list(dict.fromkeys(base_tags + spec_tags))[:cls.RECOMMENDED_TAG_COUNT]
        hashtag_block = " ".join(all_tags)

        # Build clean editorial caption structure
        body = f"""{title}

⚡ {hook}

KEY BREAKDOWN:
• Context: {context}
• Practical Impact: {implications}
• Editorial Assessment: {takeaway}

📰 Source & Provenance: {publisher}
🔗 Full Story: {source_url}

💬 How do you evaluate the production viability of this update? Drop your thoughts below.

Follow {brand_handle} for daily autonomous technology intelligence.

{hashtag_block}"""

        char_count = len(body)
        is_compliant = char_count <= cls.MAX_CAPTION_CHARS

        return {
            "title": title,
            "caption": body.strip(),
            "hashtags": hashtag_block,
            "char_count": char_count,
            "is_compliant": is_compliant
        }

    @classmethod
    def validate_caption(cls, caption_text: str) -> Tuple[bool, str]:
        if not caption_text or len(caption_text.strip()) < 20:
            return False, "Caption is too short or empty."
        if len(caption_text) > cls.MAX_CAPTION_CHARS:
            return False, f"Caption exceeds Instagram character limit ({len(caption_text)}/{cls.MAX_CAPTION_CHARS})."
        
        tags = re.findall(r'#\w+', caption_text)
        if len(tags) > 30:
            return False, f"Too many hashtags ({len(tags)}). Instagram allows maximum 30."

        return True, "Caption is compliant."

