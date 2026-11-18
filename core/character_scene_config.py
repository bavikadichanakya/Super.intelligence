"""
SUPER.INTELLIGENCEEE — Phase 13 Character Scene Configuration
Pydantic v2 data model integrating the recurring documentary host into the Universal Scene Contract.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field, model_validator


class CharacterPose(str, Enum):
    """Authoritative host poses for documentary scenes."""
    PRESENTER_DIRECT = "presenter_direct"               # Facing camera 3/4 turn, direct eye contact
    INVESTIGATOR_EXAMINING = "investigator_examining"   # Orienting body and gaze toward technical subject
    EXPLAINER_GESTURE = "explainer_gesture"             # Sidecar host gesturing toward schematic/diagram
    TRANSITION_GUIDE = "transition_guide"               # Leading viewer into subsequent technical section
    CLOSING_SUMMARY = "closing_summary"                 # Final takeaway framing


class CharacterExpression(str, Enum):
    """Allowed facial expressions adhering strictly to character profile."""
    CURIOUS_INQUIRY = "curious_inquiry"         # Slight head tilt, engaged, introducing paradox
    FOCUSED_ANALYSIS = "focused_analysis"       # Concentrated gaze on hardware/code detail
    AHA_REVELATION = "aha_revelation"           # Confident subtle smile, mechanism breakthrough
    TECHNICAL_CAUTION = "technical_caution"     # Thoughtful brow, hardware limits/bottlenecks


class CharacterScreenPosition(str, Enum):
    """Screen layout anchors in 1080x1920 vertical canvas."""
    CENTER_HERO = "center_hero"         # Centered horizontally, chest at mid-bottom (y=850..1600)
    LOWER_LEFT = "lower_left"           # Positioned on left column (x=40..460), subject on right
    LOWER_RIGHT = "lower_right"         # Positioned on right column (x=620..1040), schematic on left
    SPLIT_LEFT = "split_left"           # Left half host (x=0..520), technical visual right
    SPLIT_RIGHT = "split_right"         # Right half host (x=560..1080), technical visual left


class CharacterMovementPattern(str, Enum):
    """Biometric procedural animation behavior."""
    NATURAL_BREATHING_AND_BLINK = "natural_breathing_and_blink"     # Subtle respiration (3-5px) + 3.2s blink
    LOOK_AT_SUBJECT_AND_RETURN = "look_at_subject_and_return"       # Gaze shifts to subject, then back to viewer
    ENTERING_FRAME_SETTLE = "entering_frame_settle"                 # Smooth ease-in from lower border
    EXPLAINING_GESTURE_PULSE = "explaining_gesture_pulse"           # Subtle micro-nod & gesture pulse on narration sync


class CharacterSceneConfig(BaseModel):
    """
    Strongly-typed scene-level configuration for the recurring host.
    Specifies exact placement, movement, and relationship with technical evidence.
    """
    appears: bool = Field(True, description="Whether host appears in this scene")
    editorial_reason: str = Field(..., min_length=5, description="Why host presence enhances understanding")
    pose: CharacterPose = Field(CharacterPose.PRESENTER_DIRECT)
    expression: CharacterExpression = Field(CharacterExpression.CURIOUS_INQUIRY)
    screen_position: CharacterScreenPosition = Field(CharacterScreenPosition.CENTER_HERO)
    movement_pattern: CharacterMovementPattern = Field(CharacterMovementPattern.NATURAL_BREATHING_AND_BLINK)
    scale: float = Field(0.65, ge=0.30, le=1.0, description="Scale relative to 1080 canvas width")
    
    # Precise positioning (optional manual override in 1080x1920 space)
    custom_center_x: Optional[int] = Field(None, ge=0, le=1080)
    custom_bottom_y: Optional[int] = Field(None, ge=400, le=1700)
    
    # Timing and narration synchronization
    start_time_seconds: float = Field(0.0, ge=0.0)
    duration_seconds: Optional[float] = Field(None, gt=0.0, description="Duration of appearance in scene")
    gesture_trigger_word: Optional[str] = Field(None, description="Narration word triggering nod or gesture")
    transition_out: str = Field("fade_to_technical", description="Transition when host leaves the frame")
    
    # Safety validation
    respect_safe_zones: bool = Field(True, description="Enforce strict subtitle and UI clearance")

    @model_validator(mode="after")
    def validate_safe_positioning(self) -> "CharacterSceneConfig":
        if self.custom_bottom_y is not None:
            # Subtitle zone is 1640 to 1820
            if 1640 <= self.custom_bottom_y <= 1820:
                raise ValueError(
                    f"custom_bottom_y={self.custom_bottom_y} collides with the subtitle safe zone (1640..1820)."
                )
        return self
