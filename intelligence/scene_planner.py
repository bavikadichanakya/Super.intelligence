from typing import Dict, Any, List

class ScenePlanner:
    """Converts a 7-section structured script into an executable 7-scene production storyboard."""

    @classmethod
    def plan_scenes(cls, script_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        title = script_data.get("title", "AI Milestone")
        publisher = script_data.get("publisher", "Primary Source")
        category = script_data.get("category", "Artificial Intelligence News")

        hook = script_data.get("hook", "")
        context = script_data.get("context", "")
        development = script_data.get("development", "")
        explanation = script_data.get("explanation", "")
        implications = script_data.get("implications", "")
        limitations = script_data.get("limitations", "")
        takeaway = script_data.get("takeaway", "")

        def calc_duration(text: str, min_sec: float = 3.5) -> float:
            words = len(text.split())
            return max(min_sec, round(words / 2.5, 1))

        scenes = [
            {
                "scene_number": 1,
                "name": "Opening Hook",
                "narration": hook,
                "visual_type": "hook_card",
                "badge": "BREAKTHROUGH REPORT",
                "headline": title[:48] + ("..." if len(title) > 48 else ""),
                "subtext": "SUPER.INTELLIGENCEEE EXCLUSIVE",
                "duration_est": calc_duration(hook, 4.0),
                "transition": "fade"
            },
            {
                "scene_number": 2,
                "name": "Context & Provenance",
                "narration": context,
                "visual_type": "editorial_headline",
                "badge": f"SOURCE: {publisher.upper()}",
                "headline": "VERIFIED ARCHITECTURE",
                "subtext": "BENCHMARK VALIDATION",
                "duration_est": calc_duration(context, 4.0),
                "transition": "wipeleft"
            },
            {
                "scene_number": 3,
                "name": "The Core Development",
                "narration": development,
                "visual_type": "data_card",
                "badge": "PERFORMANCE METRIC",
                "headline": "NEXT-GEN CAPABILITY",
                "subtext": "FRONTIER EFFICIENCY GAIN",
                "duration_est": calc_duration(development, 4.5),
                "transition": "slideright"
            },
            {
                "scene_number": 4,
                "name": "Technical Architecture",
                "narration": explanation,
                "visual_type": "system_diagram",
                "badge": "SYSTEM DESIGN",
                "headline": "HOW IT OPERATES",
                "subtext": "ALGORITHMIC REFINEMENT",
                "duration_est": calc_duration(explanation, 4.5),
                "transition": "slideup"
            },
            {
                "scene_number": 5,
                "name": "Practical Impact",
                "narration": implications,
                "visual_type": "impact_card",
                "badge": "INDUSTRY DEPLOYMENT",
                "headline": "PRODUCTION IMPACT",
                "subtext": "LOWER INFERENCE OVERHEAD",
                "duration_est": calc_duration(implications, 4.0),
                "transition": "fade"
            },
            {
                "scene_number": 6,
                "name": "Limitations & Caveats",
                "narration": limitations,
                "visual_type": "critical_card",
                "badge": "CRITICAL PERSPECTIVE",
                "headline": "REALITY CHECK",
                "subtext": "PRODUCTION UNCERTAINTIES",
                "duration_est": calc_duration(limitations, 4.0),
                "transition": "wipeleft"
            },
            {
                "scene_number": 7,
                "name": "Brand Closing",
                "narration": takeaway,
                "visual_type": "brand_closing",
                "badge": "SUPER.INTELLIGENCEEE",
                "headline": "AUTONOMOUS INTELLIGENCE",
                "subtext": "FOLLOW FOR NEXT-GEN DEEP TECH",
                "duration_est": calc_duration(takeaway, 4.0),
                "transition": "fade"
            }
        ]

        return scenes
