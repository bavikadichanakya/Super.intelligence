from typing import Dict, Any, List

class StoryboardGenerator:
    """Transforms verified technical scripts into executable 7-scene production storyboards."""

    def __init__(self, db=None, config=None):
        self.db = db
        self.config = config

    @classmethod
    def generate_storyboard(cls, script_data: Dict[str, Any], script_id: Any = None) -> Dict[str, Any]:
        title = script_data.get("title", "AI Technical Milestone")
        publisher = script_data.get("publisher", "Primary Lab Documentation")
        category = script_data.get("category", "Artificial Intelligence News")

        hook = script_data.get("hook", "")
        context = script_data.get("context", "")
        development = script_data.get("development", "")
        explanation = script_data.get("explanation", "")
        implications = script_data.get("implications", "")
        limitations = script_data.get("limitations", "")
        takeaway = script_data.get("takeaway", "")

        def calc_duration(text: str, min_sec: float = 3.6) -> float:
            words = len(text.split())
            return max(min_sec, round(words / 2.5, 1))

        scenes = [
            {
                "scene_number": 1,
                "name": "Opening Hook",
                "narration": hook,
                "on_screen_text": title[:48] + ("..." if len(title) > 48 else ""),
                "badge": "BREAKTHROUGH REPORT",
                "visual_type": "hook_card",
                "instructions": "Bold high-contrast headline card, subtle blue accent line, electric sky glow.",
                "transition": "fade",
                "duration": calc_duration(hook, 4.0)
            },
            {
                "scene_number": 2,
                "name": "Context & Provenance",
                "narration": context,
                "on_screen_text": "PRIMARY SOURCE VERIFIED",
                "badge": f"SOURCE: {publisher.upper()}",
                "visual_type": "editorial_headline",
                "instructions": "Source dossier card with verified fact-check seal and publication date.",
                "transition": "wipeleft",
                "duration": calc_duration(context, 4.2)
            },
            {
                "scene_number": 3,
                "name": "The Core Development",
                "narration": development,
                "on_screen_text": "TECHNICAL METRIC MULTIPLIER",
                "badge": "PERFORMANCE BENCHMARK",
                "visual_type": "data_card",
                "instructions": "Infographic metric cards highlighting efficiency gain and compute reduction.",
                "transition": "slideright",
                "duration": calc_duration(development, 4.8)
            },
            {
                "scene_number": 4,
                "name": "Technical Architecture",
                "narration": explanation,
                "on_screen_text": "SYSTEM PIPELINE FLOW",
                "badge": "SYSTEM DESIGN",
                "visual_type": "system_diagram",
                "instructions": "3-stage architectural pipeline showing ingestion, reasoning, and verified execution.",
                "transition": "slideup",
                "duration": calc_duration(explanation, 4.8)
            },
            {
                "scene_number": 5,
                "name": "Practical Impact",
                "narration": implications,
                "on_screen_text": "PRODUCTION DEPLOYMENT",
                "badge": "INDUSTRY IMPACT",
                "visual_type": "impact_card",
                "instructions": "Triple impact callout cards for enterprise agents, edge hardware, and engineering.",
                "transition": "fade",
                "duration": calc_duration(implications, 4.2)
            },
            {
                "scene_number": 6,
                "name": "Limitations & Caveats",
                "narration": limitations,
                "on_screen_text": "CRITICAL PERSPECTIVE & UNPROVEN EDGES",
                "badge": "REALITY CHECK",
                "visual_type": "critical_card",
                "instructions": "Amber/violet alert card detailing edge-case drift and hardware gating.",
                "transition": "wipeleft",
                "duration": calc_duration(limitations, 4.2)
            },
            {
                "scene_number": 7,
                "name": "Takeaway & Outro",
                "narration": takeaway,
                "on_screen_text": "SUPER.INTELLIGENCEEE",
                "badge": "FOLLOW FOR NEXT-GEN DEEP TECH",
                "visual_type": "brand_closing",
                "instructions": "Minimalist official brand closing screen with call to action.",
                "transition": "fade",
                "duration": calc_duration(takeaway, 4.0)
            }
        ]
        return scenes
