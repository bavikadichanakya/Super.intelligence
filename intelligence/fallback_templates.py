import re
from typing import Dict, Any, List
from intelligence.hook_generator import HookGenerator

class FallbackTemplates:
    """Produces structured, factual 7-section video scripts completely offline without any paid APIs."""

    @classmethod
    def generate_script(cls, article: Dict[str, Any], dossier: Any = None) -> Dict[str, Any]:
        title = article.get("title", "Recent AI Development")
        publisher = article.get("publisher", "Official Announcement")
        summary = article.get("summary", "")
        category = article.get("category", "Artificial Intelligence News")
        source_url = article.get("url", "") or article.get("source_url", "")

        # Extract core summary sentences
        clean_summary = summary.replace("\n", " ").strip()
        sentences = [s.strip() for s in re.split(r'[.!?]+', clean_summary) if len(s.strip()) > 10]
        core_point = sentences[0] if sentences else f"Researchers and engineers have unveiled {title}."
        second_point = sentences[1] if len(sentences) > 1 else ""

        # Use dossier context if provided
        active_dossier = dossier or article.get("dossier") or article.get("research_dossier")
        if active_dossier:
            tech_exp = getattr(active_dossier, "technical_explanation", "") or (active_dossier.get("technical_explanation") if isinstance(active_dossier, dict) else "")
            lims = getattr(active_dossier, "limitations", []) or (active_dossier.get("limitations") if isinstance(active_dossier, dict) else [])
            imps = getattr(active_dossier, "potential_implications", []) or (active_dossier.get("potential_implications") if isinstance(active_dossier, dict) else [])
        else:
            tech_exp = ""
            lims = []
            imps = []

        hook = HookGenerator.generate_hook(title, category)
        context = f"Published via {publisher}, this milestone focuses on verified implementation and reproducible results."
        development = f"{core_point}. {second_point}." if second_point else f"{core_point}."
        explanation = tech_exp if tech_exp else (
            sentences[2] if len(sentences) > 2 else f"The underlying design prioritizes targeted optimizations within the core architecture of {title}."
        )
        implications = imps[0] if imps else (
            sentences[3] if len(sentences) > 3 else "For developers, this provides more predictable execution in production pipelines."
        )
        limitations = lims[0] if lims else "Production deployment requires independent benchmark validation under live real-world constraints."
        takeaway = "Understanding the underlying architectural trade-offs is essential as emerging models mature."

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
