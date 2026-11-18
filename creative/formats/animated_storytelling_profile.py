"""
SUPER.INTELLIGENCEEE — Animated Storytelling Creative Format Profile
Planning interface for original technology stories, conceptual explanations, and character-driven narratives.
Establishes continuity schemas for character identity, environment consistency, and camera direction.
"""

from __future__ import annotations

from typing import Any, Dict, List
from core.creative_contracts import (
    CreativeFormatType,
    NarrativeStructureType,
    SceneType,
)


class AnimatedStorytellingProfile:
    """Specification and planning contracts for Animated Storytelling content."""

    format_type = CreativeFormatType.ANIMATED_STORYTELLING
    primary_priority = False

    default_narrative_structures = [
        NarrativeStructureType.HISTORICAL_BREAKTHROUGH_CURRENT_FUTURE,
        NarrativeStructureType.PROBLEM_MECHANISM_SOLUTION_LIMITATIONS,
    ]

    supported_scene_types = [
        SceneType.CONCEPTUAL_ANIMATION,
        SceneType.ANIMATED_PROCESS,
        SceneType.TECHNICAL_DIAGRAM,
        SceneType.NARRATIVE_SCENE,
    ]

    target_duration_range = (50.0, 90.0)
    typical_scene_count_range = (4, 8)

    visual_style_guidelines = {
        "theme": "Geometric Vector Storytelling & World Continuity",
        "background": "#0b0e14",
        "character_continuity": "Consistent non-copyrighted robotic / engineering avatar geometry across scenes",
        "environment_continuity": "Cohesive spatial world (server laboratory, silicon cleanroom, abstract matrix)",
        "camera_motion": "Smooth cinematic 2.5D parallax drift, rotational camera pivots",
        "sound_design": "Warm melodic ambient synths, synchronized character foley, resolving cadence",
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

