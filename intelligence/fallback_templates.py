import re
from typing import Dict, Any, List
from intelligence.hook_generator import HookGenerator

class FallbackTemplates:
    """Produces structured, factual 7-section video scripts completely offline without any paid APIs."""

    @classmethod
    def generate_script(cls, article: Dict[str, Any]) -> Dict[str, Any]:
        title = article.get("title", "Recent AI Development")
        publisher = article.get("publisher", "Official Announcement")
        summary = article.get("summary", "")
        category = article.get("category", "Artificial Intelligence News")
        source_url = article.get("url", "")

        # Extract core summary sentence
        clean_summary = summary.replace("\n", " ").strip()
        sentences = [s.strip() for s in re.split(r'[.!?]+', clean_summary) if len(s.strip()) > 10]
        core_point = sentences[0] if sentences else f"Researchers and engineers have unveiled {title}."
        second_point = sentences[1] if len(sentences) > 1 else "Early evaluations demonstrate notable performance improvements across target tasks."

        hook = HookGenerator.generate_hook(title, category)
        context = f"Published via {publisher}, this milestone addresses persistent challenges in computational scalability and real-world system reliability."
        development = f"{core_point}. {second_point}."
        explanation = "Architecturally, this advance leverages refined algorithmic optimizations and focused data pipelines rather than just raw brute-force compute."
        implications = "For engineers and builders, this unlocks more efficient inference, reduced operational latency, and smarter autonomous workflows."
        limitations = "However, researchers note that edge-case validation and broader stress testing in complex production environments are still underway."
        takeaway = "As frontier models evolve, efficiency and verified execution are becoming the real competitive moats."

        # Compute word counts
        sections = [hook, context, development, explanation, implications, limitations, takeaway]
        total_text = " ".join(sections)
        word_count = len(total_text.split())
        est_duration = round(word_count / 2.6, 1)  # ~156 WPM / 2.6 words per second

        # 7-Scene visual storyboard breakdown
        scenes = [
            {
                "scene_number": 1,
                "name": "Opening Hook",
                "narration": hook,
                "visual_type": "cinematic_headline",
                "headline": title[:50] + ("..." if len(title) > 50 else ""),
                "badge": "AI BREAKING",
                "duration_est": round(len(hook.split()) / 2.6, 1)
            },
            {
                "scene_number": 2,
                "name": "Context & Source",
                "narration": context,
                "visual_type": "editorial_source_card",
                "headline": publisher.upper(),
                "badge": "SOURCE VERIFIED",
                "duration_est": round(len(context.split()) / 2.6, 1)
            },
            {
                "scene_number": 3,
                "name": "The Core Breakthrough",
                "narration": development,
                "visual_type": "data_metric_card",
                "headline": "KEY ADVANCEMENT",
                "badge": "TECHNICAL BRIEF",
                "duration_est": round(len(development.split()) / 2.6, 1)
            },
            {
                "scene_number": 4,
                "name": "How It Works",
                "narration": explanation,
                "visual_type": "architecture_diagram",
                "headline": "SYSTEM ARCHITECTURE",
                "badge": "DEEP DIVE",
                "duration_est": round(len(explanation.split()) / 2.6, 1)
            },
            {
                "scene_number": 5,
                "name": "Practical Impact",
                "narration": implications,
                "visual_type": "impact_highlight",
                "headline": "PRACTICAL IMPACT",
                "badge": "DEPLOYMENT",
                "duration_est": round(len(implications.split()) / 2.6, 1)
            },
            {
                "scene_number": 6,
                "name": "Limitations & Reality Check",
                "narration": limitations,
                "visual_type": "critical_analysis",
                "headline": "TECHNICAL LIMITS",
                "badge": "REALITY CHECK",
                "duration_est": round(len(limitations.split()) / 2.6, 1)
            },
            {
                "scene_number": 7,
                "name": "Takeaway & Brand Outro",
                "narration": takeaway,
                "visual_type": "brand_closing",
                "headline": "SUPER.INTELLIGENCEEE",
                "badge": "FOLLOW FOR MORE",
                "duration_est": round(len(takeaway.split()) / 2.6, 1)
            }
        ]

        return {
            "title": title,
            "publisher": publisher,
            "source_url": source_url,
            "category": category,
            "hook": hook,
            "context": context,
            "development": development,
            "explanation": explanation,
            "implications": implications,
            "limitations": limitations,
            "takeaway": takeaway,
            "word_count": word_count,
            "est_duration": est_duration,
            "full_narration": total_text,
            "scenes": scenes
        }
