"""
SUPER.INTELLIGENCEEE — Tech Documentary Creative Format Profile
Primary production profile for technical explanations, software demos, AI research, and architecture breakdowns.
Combines screen demonstrations, animated system diagrams, cinematic B-roll, kinetic typography, and synchronized sound design.
"""

from __future__ import annotations

from typing import Any, Dict, List
from core.creative_contracts import (
    CreativeFormatType,
    NarrativeStructureType,
    SceneType,
)


class TechDocumentaryProfile:
    """Specification and default composition rules for the Tech Documentary production engine."""

    format_type = CreativeFormatType.TECH_DOCUMENTARY
    primary_priority = True

    default_narrative_structures = [
        NarrativeStructureType.PROBLEM_MECHANISM_SOLUTION_LIMITATIONS,
        NarrativeStructureType.DEMONSTRATION_BREAKDOWN_EVALUATION,
        NarrativeStructureType.COMPARISON_TESTING_RESULTS_VERDICT,
        NarrativeStructureType.HISTORICAL_BREAKTHROUGH_CURRENT_FUTURE,
    ]

    supported_scene_types = [
        SceneType.SCREEN_DEMONSTRATION,
        SceneType.TECHNICAL_DIAGRAM,
        SceneType.DATA_VISUALIZATION,
        SceneType.CINEMATIC_BROLL,
        SceneType.KINETIC_TYPOGRAPHY,
        SceneType.COMPARISON,
        SceneType.PRODUCT_DEMONSTRATION,
        SceneType.ANIMATED_PROCESS,
        SceneType.UI_CLOSEUP,
    ]

    target_duration_range = (45.0, 90.0)      # Optimal for deep-dive vertical tech reels
    typical_scene_count_range = (5, 9)

    visual_style_guidelines = {
        "theme": "Dark Obsidian & Neon Telemetry",
        "background": "#080b11",
        "typography": "Arial Black / Inter Bold (High Contrast, Left or Center Aligned)",
        "diagram_style": "Vector nodes, decoupled dataflow paths, glowing highlighted stages",
        "screen_demo_style": "Dark mode IDE or Terminal with highlighted command line inputs",
        "camera_motion": "Controlled subtle push-in (1.0 to 1.15x), locked on code or diagrams",
        "sound_design": "Subtle low-frequency atmospheric drone, mechanical clicks on diagram reveals, 18% ducked whoosh transitions",
    }

    @classmethod
    def get_profile_metadata(cls) -> Dict[str, Any]:
        return {
            "format_type": cls.format_type.value,
            "primary_priority": cls.primary_priority,
            "supported_scene_types": [s.value for s in cls.supported_scene_types],
            "target_duration_range": cls.target_duration_range,
            "typical_scene_count_range": cls.typical_scene_count_range,
            "visual_style_guidelines": cls.visual_style_guidelines,
        }

