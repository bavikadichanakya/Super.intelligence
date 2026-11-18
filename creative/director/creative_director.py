"""
SUPER.INTELLIGENCEEE — Creative Director Module
Translates narrative beats and research dossiers into an intentional, production-ready creative direction plan.
Decides what the viewer sees, when they see it, which concepts get diagrams or screen demos,
where visual pauses occur, and how the ending resolves.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, List, Optional

from core.creative_contracts import (
    CreativeDirectionPlan,
    CreativeFormatType,
    NarrativeStructureType,
    SceneType,
    StoryArchitecturePlan,
)
from core.schemas import ResearchDossier

logger = logging.getLogger("super_intelligence.creative_director")


class CreativeDirector:
    """Orchestrates high-level visual storytelling strategy and intentional scene treatments."""

    def __init__(self, config=None):
        self.config = config

    def formulate_creative_direction(
        self,
        architecture_plan: StoryArchitecturePlan,
        dossier: Optional[ResearchDossier] = None,
        custom_theme: Optional[str] = None,
    ) -> CreativeDirectionPlan:
        """
        Synthesizes visual theme, palette, and scene-by-scene creative visual requirements.
        Prevents slideshow monotony by allocating specific media treatments:
        - Screen demonstrations for developer tools & CLI
        - Animated technical diagrams for model architectures
        - Cinematic B-roll for real-world hardware & context
        - Kinetic typography for decisive punchlines
        """
        title = architecture_plan.topic_title
        fmt = architecture_plan.selected_creative_format
        beats = architecture_plan.structural_beats
        scene_count = len(beats)

        # 1. Visual Theme Formulation
        if custom_theme:
            visual_theme = custom_theme
        elif fmt == CreativeFormatType.TECH_DOCUMENTARY:
            visual_theme = "High-Fidelity Engineering Documentary: Dark Obsidian, Neon Telemetry, Diagrammatic Depth"
        elif fmt == CreativeFormatType.TREND_SHORTFORM:
            visual_theme = "High-Impact Breaking Tech: High-Contrast Yellow/Cyan Punch, Accelerated Kinetic Cuts"
        else:
            visual_theme = "Conceptual Tech Narrative: Geometric Continuity, Abstract Vector Storytelling"

        # 2. Dynamic Color Palette
        color_palette = {
            "background_primary": "#080b11",     # Deep space obsidian
            "panel_surface": "#111722",          # Elevated dark slate
            "grid_lines": "#1c2638",             # Structural technical grid
            "accent_cyan": "#00f0ff",            # Electric neural pulse
            "accent_amber": "#ffb703",           # High-visibility quantitative metric
            "accent_crimson": "#ff3366",         # Bottleneck or legacy ceiling indicator
            "accent_emerald": "#00e676",         # Verified performance gain
            "text_primary": "#f8fafc",           # Crisp white typography
            "text_secondary": "#94a3b8",         # Muted technical subtitle
        }

        # 3. Identify High-Value Information Beats for Visual Emphasis
        emphasis_claims: List[str] = []
        if dossier and dossier.important_claims:
            for c in dossier.important_claims[:3]:
                emphasis_claims.append(c.claim_text)
        else:
            emphasis_claims.append(title)

        # 4. Allocate Specific Visual Treatments across Scenes
        screen_demos: List[int] = []
        diagrams: List[int] = []
        broll_scenes: List[int] = []

        for idx, beat in enumerate(beats, start=1):
            role = beat.get("role", "")
            beat_name = beat.get("beat_name", "").lower()

            if any(k in role.lower() or k in beat_name for k in ["demo", "tool", "overview", "code"]):
                screen_demos.append(idx)
            elif any(k in role.lower() or k in beat_name for k in ["mechanism", "architecture", "breakdown", "investigation", "details"]):
                diagrams.append(idx)
            elif any(k in role.lower() or k in beat_name for k in ["context", "problem", "challenge", "origin", "future"]):
                broll_scenes.append(idx)

        # Ensure balanced visual distribution
        # If no diagrams were flagged, place one in the middle scene
        if not diagrams and scene_count >= 3:
            mid_scene = scene_count // 2 + 1
            diagrams.append(mid_scene)

        # If no B-roll was flagged, place in scene 2
        if not broll_scenes and scene_count >= 2:
            broll_scenes.append(2)

        # 5. Sound Design Strategy
        if fmt == CreativeFormatType.TREND_SHORTFORM:
            sound_strategy = "Aggressive sub-bass risers on hooks, swift whoosh transitions between beats, minimal ambient pad."
        elif fmt == CreativeFormatType.TECH_DOCUMENTARY:
            sound_strategy = "Subtle cinematic low-end drone, discrete mechanical clicks on diagram elements, 18% ducked transition whooshes."
        else:
            sound_strategy = "Ambient melodic synths synchronized to visual pacing, melodic resolve at concluding insight."

        # 6. Ending Resolution
        ending_resolution = (
            f"Frame #{scene_count} resolves with an authoritative takeaway on {title[:40]}, "
            f"dissolving into the official SUPER.INTELLIGENCEEE technical badge."
        )

        direction_plan = CreativeDirectionPlan(
            direction_id=f"dir_{str(uuid.uuid4())[:8]}",
            topic_id=architecture_plan.topic_id,
            visual_theme=visual_theme,
            color_palette=color_palette,
            editorial_emphasis_claims=emphasis_claims,
            screen_demo_sections=screen_demos,
            diagram_sections=diagrams,
            broll_sections=broll_scenes,
            sound_design_strategy=sound_strategy,
            ending_resolution=ending_resolution,
        )

        logger.info(
            f"Formulated CreativeDirectionPlan [{direction_plan.direction_id}]: "
            f"{len(diagrams)} diagrams, {len(screen_demos)} demos, {len(broll_scenes)} B-roll."
        )
        return direction_plan

