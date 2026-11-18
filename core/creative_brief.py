"""
SUPER.INTELLIGENCEEE — Visual Intelligence & Scene Creative Brief Architecture
Defines the creative contract separating visual storytelling concepts from narration text.
Every scene must have an independent visual concept explaining what the viewer sees and why.
"""

from __future__ import annotations

import datetime
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ProductionMode(str, Enum):
    """Canonical visual production modes for scenes."""
    CINEMATIC_STOCK = "cinematic_stock_footage"
    ORIGINAL_MOTION_GRAPHICS = "original_motion_graphics"
    ANIMATED_TECHNICAL_DIAGRAM = "animated_technical_diagram"
    SOFTWARE_DEMO = "software_demo"
    EDITORIAL_TYPOGRAPHY = "editorial_typography"
    SKETCH_EXPLANATION = "sketch_based_explanation"
    DATA_VISUALIZATION = "data_visualization"
    SPLIT_SCREEN_COMPARISON = "split_screen_comparison"
    INTERFACE_WALKTHROUGH = "interface_walkthrough"
    DOCUMENTARY_SEQUENCE = "documentary_sequence"


class CameraMovement(str, Enum):
    """Dynamic camera movement instructions."""
    PUSH_IN_SLOW = "push_in_slow"          # 1.0 -> 1.15x smooth Ken Burns zoom
    PAN_HORIZONTAL = "pan_horizontal"      # Smooth lateral drift across diagram
    DRIFT_SUBTLE = "drift_subtle"          # Handheld micro-orbit
    SNAP_ZOOM = "snap_zoom"                # Fast punch on emphasis beat
    STATIC_LOCKED = "static_locked"        # Deliberate locked-off frame for code/data readability


class CompositionLayout(str, Enum):
    """Scene framing and geometric composition."""
    FULL_BLEED_CINEMATIC = "full_bleed_cinematic"
    SPLIT_50_50_VERTICAL = "split_50_50_vertical"
    MACRO_CENTER_HERO = "macro_center_hero"
    TERMINAL_LOWER_THIRD = "terminal_lower_third"
    ASYMMETRIC_DIAGONAL = "asymmetric_diagonal"
    NETWORK_TOPOLOGY = "network_topology"


@dataclass
class SceneCreativeBrief:
    """
    Structured creative specification for a single video scene.
    Operates BEFORE rendering to decouple visual concepts from raw narration.
    """
    scene_id: str
    scene_index: int
    narrative_purpose: str                   # Why this scene exists in the narrative arc
    intended_emotion: str                    # Curiosity, skepticism, clarity, awe, conviction
    visual_metaphor: str                     # Visual symbolism (e.g., linear thread vs tangled matrix)
    primary_subject: str                     # The focal element the viewer's eye should track
    visual_action: str                       # What changes or moves in the frame
    production_mode: ProductionMode          # Which production mode executes this scene
    asset_requirements: List[str]            # Required visual/footage assets
    composition: CompositionLayout           # Framing layout
    camera_movement: CameraMovement          # Dynamic camera motion
    animation_instructions: str              # Object-level animation timing and behavior
    transition_in: str = "fade"              # In-transition
    transition_out: str = "fade"             # Out-transition
    on_screen_text: str = ""                 # Minimal text overlay (not full narration)
    duration_seconds: float = 5.0            # Synchronized exact audio duration
    factual_claims_represented: List[str] = field(default_factory=list)
    visual_concept_rationale: str = ""       # Why this visual was selected for this topic
    provenance_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["production_mode"] = self.production_mode.value if isinstance(self.production_mode, ProductionMode) else str(self.production_mode)
        d["camera_movement"] = self.camera_movement.value if isinstance(self.camera_movement, CameraMovement) else str(self.camera_movement)
        d["composition"] = self.composition.value if isinstance(self.composition, CompositionLayout) else str(self.composition)
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SceneCreativeBrief:
        d = dict(data)
        if "production_mode" in d and isinstance(d["production_mode"], str):
            d["production_mode"] = ProductionMode(d["production_mode"])
        if "camera_movement" in d and isinstance(d["camera_movement"], str):
            d["camera_movement"] = CameraMovement(d["camera_movement"])
        if "composition" in d and isinstance(d["composition"], str):
            d["composition"] = CompositionLayout(d["composition"])
        return cls(**d)


@dataclass
class ReelCreativePlan:
    """Master visual storytelling strategy for an entire video production."""
    topic_id: int
    title: str
    overall_visual_theme: str                # e.g., "Cyber-Industrial Hardware & Edge Neural Architecture"
    narrative_pacing_arc: str                # Hook hook -> Tension setup -> Mechanism breakdown -> Real-world impact
    color_palette: Dict[str, str]            # Narrative color mapping (primary, accent, danger, success)
    scenes: List[SceneCreativeBrief]
    total_duration_seconds: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic_id": self.topic_id,
            "title": self.title,
            "overall_visual_theme": self.overall_visual_theme,
            "narrative_pacing_arc": self.narrative_pacing_arc,
            "color_palette": self.color_palette,
            "total_duration_seconds": self.total_duration_seconds,
            "created_at": self.created_at,
            "scenes": [s.to_dict() for s in self.scenes],
        }

