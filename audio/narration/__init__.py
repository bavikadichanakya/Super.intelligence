"""
SUPER.INTELLIGENCEEE — Audio Narration Package
Provides unified offline TTS interfaces, structured narration direction,
and segmented audio rendering with timing manifests.
"""

from .narration_service import NarrationService
from .voice_director import VoiceDirector, NarrationTone, NarrationSegment, DirectedScript
from .narration_renderer import NarrationRenderer, RenderedNarrationResult, SegmentTiming

__all__ = [
    "NarrationService",
    "VoiceDirector",
    "NarrationTone",
    "NarrationSegment",
    "DirectedScript",
    "NarrationRenderer",
    "RenderedNarrationResult",
    "SegmentTiming",
]

