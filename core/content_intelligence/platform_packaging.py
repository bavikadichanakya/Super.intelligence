"""
Platform-Specific Packaging & Metadata Optimization Engine
Generates tailored, platform-native packaging for YouTube Shorts and Instagram Reels.
Never copies generic cross-posted copy across platforms.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformPackage:
    platform: str                  # "youtube_shorts" or "instagram_reels"
    title_or_headline: str
    first_frame_spec: str
    on_screen_text: str
    caption_body: str
    caption_first_line: str        # Front-loaded line before UI truncates
    hashtags: List[str]
    call_to_action: str
    pinned_comment: Optional[str]
    seo_keywords: List[str]
    cover_image_spec: str


class PlatformPackagingEngine:
    """Builds differentiated, platform-native metadata packages."""

    def package_for_instagram_reels(
        self,
        topic: str,
        core_insight: str,
        first_frame_action: str,
        target_persona: str,
        breakthrough_bullets: List[str],
        niche_tags: List[str],
    ) -> PlatformPackage:
        """Packages Reel for maximum sends, saves, and search indexability."""
        first_line = f"How {topic} broke the GPU memory wall without cloud APIs."
        
        bullets_text = "\n".join(f"• {b}" for b in breakthrough_bullets)
        caption_full = (
            f"{first_line}\n\n"
            f"Here is the exact systems breakdown:\n"
            f"{bullets_text}\n\n"
            f"Full technical breakdown of open weights and architecture on our channel.\n\n"
            f"Send this to an {target_persona} who needs to see this."
        )

        clean_tags = [f"#{t.replace('#', '').strip()}" for t in niche_tags[:4]]
        if "#SuperIntelligence" not in clean_tags:
            clean_tags.append("#SuperIntelligence")

        return PlatformPackage(
            platform="instagram_reels",
            title_or_headline=f"{topic} Architecture Deep Dive",
            first_frame_spec=f"High-contrast visual: {first_frame_action}. Zero title card clutter.",
            on_screen_text=f"{topic.upper()} EXPLAINED",
            caption_body=caption_full,
            caption_first_line=first_line,
            hashtags=clean_tags,
            call_to_action=f"Send this to an {target_persona} building with open weights.",
            pinned_comment=(
                f"Which open-source architecture should we break down next? "
                f"Drop the GitHub repository in the comments."
            ),
            seo_keywords=[topic, "Open Source AI", "LLM Architecture", "GPU Optimization", "Deep Learning"],
            cover_image_spec="High-contrast split visual: 93% memory drop graph with clean obsidian typography.",
        )

    def package_for_youtube_shorts(
        self,
        topic: str,
        hook_headline: str,
        first_frame_action: str,
        breakthrough_summary: str,
        niche_tags: List[str],
        related_longform_link: Optional[str] = None,
    ) -> PlatformPackage:
        """Packages Short for Shorts Feed retention and search discoverability."""
        title = f"{hook_headline} ({topic})"
        if len(title) > 60:
            title = f"{hook_headline[:55]}..."

        description_lines = [
            f"How {topic} achieved state-of-the-art reasoning through pure reinforcement learning and latent compression.",
            "",
            "Key Mechanisms Covered:",
            breakthrough_summary,
            "",
            "Subscribe to SUPER.INTELLIGENCEEE for daily engineering breakdowns of the world's most powerful open-source repositories.",
            "",
            # First tag MUST be #Shorts per YouTube Shorts feed ranking standards
            f"#Shorts " + " ".join(f"#{t.replace('#', '').strip()}" for t in niche_tags[:3]),
        ]

        if related_longform_link:
            description_lines.insert(4, f"Full Deep Dive Documentary: {related_longform_link}")

        return PlatformPackage(
            platform="youtube_shorts",
            title_or_headline=title,
            first_frame_spec=f"Immediate motion demonstration: {first_frame_action}. Subtitles start on frame 1.",
            on_screen_text=hook_headline.upper(),
            caption_body="\n".join(description_lines),
            caption_first_line=title,
            hashtags=["#Shorts"] + [f"#{t.replace('#', '').strip()}" for t in niche_tags[:3]],
            call_to_action="Subscribe to SUPER.INTELLIGENCEEE for daily open-source AI breakdowns.",
            pinned_comment=(
                "We break down breakthrough open-source AI repositories and hardware physics daily. "
                "Subscribe to build sovereign AI without cloud vendor lock-in."
            ),
            seo_keywords=[topic, "YouTube Shorts", "AI Research", "Computer Science", "Coding"],
            cover_image_spec="Vertical frame snapshot showing high-contrast benchmark leaderboard.",
        )
