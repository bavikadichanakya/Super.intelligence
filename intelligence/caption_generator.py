from typing import Dict, Any, List
from core.config_manager import get_config

class CaptionGenerator:
    """Generates clean, professional Instagram captions and strategic hashtags."""

    @classmethod
    def generate_caption(cls, script_data: Dict[str, Any]) -> Dict[str, str]:
        config = get_config()
        title = script_data.get("title", "AI Development")
        publisher = script_data.get("publisher", "Official Release")
        source_url = script_data.get("source_url", "")
        hook = script_data.get("hook", "")
        takeaway = script_data.get("takeaway", "")
        category = script_data.get("category", "Artificial Intelligence News")

        default_tags = config.get("publishing.default_hashtags", [
            "#superintelligence", "#artificialintelligence", "#aimodels", "#futuretech"
        ])

        # Category specific hashtags
        cat_tags = []
        if "Cybersecurity" in category:
            cat_tags = ["#cybersecurity", "#infosec", "#zeroday", "#networksecurity"]
        elif "Robotics" in category:
            cat_tags = ["#robotics", "#humanoid", "#automation", "#hardware"]
        elif "New AI Models" in category:
            cat_tags = ["#deeplearning", "#llm", "#frontiermodels", "#openaialternative"]
        else:
            cat_tags = ["#techtrends", "#machinelearning", "#datascience", "#aiagents"]

        all_tags = list(dict.fromkeys(default_tags + cat_tags))[:15]
        hashtags_str = " ".join(all_tags)

        caption = f"""{title}

⚡ {hook}

Key Takeaways:
• Architecture & Scale: Engineered for optimized inference and real-world system reliability.
• Source & Verification: Formally reported via {publisher}.
• Big Picture: {takeaway}

🔗 Original Source: {source_url}

💬 How do you see this impacting current engineering pipelines? Share your thoughts below.

Follow @super.intelligenceee for daily breakdowns of frontier AI and deep tech.
"""
        return {
            "caption": caption.strip(),
            "hashtags": hashtags_str
        }
