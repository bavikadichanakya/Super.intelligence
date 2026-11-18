"""
SUPER.INTELLIGENCEEE — Trend-Driven Short-Form Creative Format Profile
Optimized for breaking news, rapid discoveries, timely launches, and fast-paced technical developments.
Prioritizes strong opening hooks, rapid context, vital metrics, and swift visual progression.
"""

from __future__ import annotations

from typing import Any, Dict, List
from core.creative_contracts import (
    CreativeFormatType,
    NarrativeStructureType,
    SceneType,
)


class TrendShortFormProfile:
    """Specification and composition rules for Trend-Driven Short-Form content."""

    format_type = CreativeFormatType.TREND_SHORTFORM
    primary_priority = False

    default_narrative_structures = [
        NarrativeStructureType.DISCOVERY_EXPLANATION_IMPLICATIONS,
        NarrativeStructureType.QUESTION_INVESTIGATION_EVIDENCE_CONCLUSION,
    ]

    supported_scene_types = [
        SceneType.KINETIC_TYPOGRAPHY,
        SceneType.DATA_VISUALIZATION,
        SceneType.SCREEN_DEMONSTRATION,
        SceneType.COMPARISON,
        SceneType.NARRATIVE_SCENE,
    ]

    target_duration_range = (25.0, 45.0)      # High-retention short duration
    typical_scene_count_range = (3, 5)

    visual_style_guidelines = {
        "theme": "High-Contrast Breaking Telemetry",
        "background": "#05070a",
        "typography": "Heavy Impact / Bold Sans-Serif (Yellow & Cyan punch)",
        "pacing": "Rapid scene transitions (every 2.5 to 4.5 seconds)",
        "camera_motion": "Snap zoom on hook emphasis words, quick lateral wipe transitions",
        "sound_design": "Sub-bass riser on hook, sharp transient transitions, accelerated tempo",
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

