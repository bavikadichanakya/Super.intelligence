"""
SUPER.INTELLIGENCEEE — Shared Creative Contracts & Dynamic Scene Models
Defines strictly-typed data contracts for story architecture, creative direction,
and dynamic scene planning across Tech Documentary, Trend Short-Form, and Animated Storytelling.
Provides lossless bi-directional adapters with UniversalScene and legacy storyboard dicts.
"""

from __future__ import annotations

import datetime
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from core.schemas import CaptionConfig, SceneProps, UniversalScene, VisualArchetype


class SceneType(str, Enum):
    """Canonical scene types across all creative formats."""
    SCREEN_DEMONSTRATION = "screen_demonstration"
    PRODUCT_DEMONSTRATION = "product_demonstration"
    TECHNICAL_DIAGRAM = "technical_diagram"
    ANIMATED_PROCESS = "animated_process"
    CINEMATIC_BROLL = "cinematic_broll"
    KINETIC_TYPOGRAPHY = "kinetic_typography"
    DATA_VISUALIZATION = "data_visualization"
    COMPARISON = "comparison"
    UI_CLOSEUP = "ui_closeup"
    CONCEPTUAL_ANIMATION = "conceptual_animation"
    NARRATIVE_SCENE = "narrative_scene"

    def to_visual_archetype(self) -> VisualArchetype:
        """Maps dynamic scene type to renderer visual archetype."""
        mapping = {
            SceneType.SCREEN_DEMONSTRATION: VisualArchetype.PRODUCT_DEMO,
            SceneType.PRODUCT_DEMONSTRATION: VisualArchetype.PRODUCT_DEMO,
            SceneType.TECHNICAL_DIAGRAM: VisualArchetype.MOTION_DIAGRAM,
            SceneType.ANIMATED_PROCESS: VisualArchetype.MOTION_DIAGRAM,
            SceneType.CINEMATIC_BROLL: VisualArchetype.STOCK_BROLL,
            SceneType.KINETIC_TYPOGRAPHY: VisualArchetype.SKETCH_TITLE,
            SceneType.DATA_VISUALIZATION: VisualArchetype.SKETCH_STAT,
            SceneType.COMPARISON: VisualArchetype.SKETCH_STAT,
            SceneType.UI_CLOSEUP: VisualArchetype.PRODUCT_DEMO,
            SceneType.CONCEPTUAL_ANIMATION: VisualArchetype.MOTION_DIAGRAM,
            SceneType.NARRATIVE_SCENE: VisualArchetype.EDITORIAL_HUD,
        }
        return mapping.get(self, VisualArchetype.EDITORIAL_HUD)

    @classmethod
    def from_str(cls, val: Union[str, SceneType]) -> SceneType:
        if isinstance(val, SceneType):
            return val
        s = str(val).lower().strip()
        for member in cls:
            if member.value == s or member.name.lower() == s:
                return member
        if "demo" in s or "screen" in s or "code" in s:
            return cls.SCREEN_DEMONSTRATION
        if "diagram" in s or "arch" in s or "system" in s:
            return cls.TECHNICAL_DIAGRAM
        if "broll" in s or "b_roll" in s or "stock" in s:
            return cls.CINEMATIC_BROLL
        if "stat" in s or "data" in s or "chart" in s:
            return cls.DATA_VISUALIZATION
        if "type" in s or "title" in s or "text" in s:
            return cls.KINETIC_TYPOGRAPHY
        if "comp" in s or "vs" in s or "diff" in s:
            return cls.COMPARISON
        return cls.NARRATIVE_SCENE


class NarrativeStructureType(str, Enum):
    """Available narrative structures for technology storytelling."""
    DISCOVERY_EXPLANATION_IMPLICATIONS = "discovery_explanation_implications"
    PROBLEM_MECHANISM_SOLUTION_LIMITATIONS = "problem_mechanism_solution_limitations"
    QUESTION_INVESTIGATION_EVIDENCE_CONCLUSION = "question_investigation_evidence_conclusion"
    DEMONSTRATION_BREAKDOWN_EVALUATION = "demonstration_breakdown_evaluation"
    COMPARISON_TESTING_RESULTS_VERDICT = "comparison_testing_results_verdict"
    HISTORICAL_BREAKTHROUGH_CURRENT_FUTURE = "historical_breakthrough_current_future"


class CreativeFormatType(str, Enum):
    """The three specialized creative production engines."""
    TECH_DOCUMENTARY = "tech_documentary"
    TREND_SHORTFORM = "trend_shortform"
    ANIMATED_STORYTELLING = "animated_storytelling"


@dataclass
class AssetRequirement:
    """Specific visual or audio asset required for a scene."""
    asset_id: str
    asset_type: str                   # footage_mp4, diagram_svg, screenshot_png, sound_sfx
    description: str
    source_suggestion: str = "local_editorial"
    is_mandatory: bool = True
    license_preference: str = "Editorial Generated"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AudioCue:
    """Explicit audio synchronization instruction for narration and sound design."""
    cue_id: str
    cue_type: str                     # sfx_transition, music_duck, narration_pause, riser
    timestamp_offset_seconds: float = 0.0
    asset_name: str = "whoosh-cinematic.mp3"
    volume_gain: float = 0.18

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DynamicScene:
    """
    Canonical Dynamic Scene Model.
    Decoupled from fixed scene count assumptions; supports variable duration and diverse compositions.
    """
    scene_id: str
    sequence: int
    narration: str
    scene_objective: str
    scene_type: SceneType
    visual_concept: str
    visual_description: str
    asset_requirements: List[AssetRequirement] = field(default_factory=list)
    camera_direction: str = "push_in_slow"
    motion_direction: str = "draw_reveal"
    on_screen_text: str = ""
    transition_in: str = "fade"
    transition_out: str = "cross_dissolve"
    estimated_duration: float = 5.0
    actual_duration: Optional[float] = None
    audio_cues: List[AudioCue] = field(default_factory=list)
    evidence_references: List[str] = field(default_factory=list)
    production_complexity: str = "standard" # standard, high, cinematic

    @property
    def duration_seconds(self) -> float:
        """Returns actual audio duration if set, otherwise estimated duration."""
        return self.actual_duration if self.actual_duration is not None and self.actual_duration > 0.1 else self.estimated_duration

    def validate(self) -> Tuple[bool, List[str]]:
        """Strict validation of scene contract."""
        errors: List[str] = []
        if not self.scene_id:
            errors.append("scene_id must be non-empty.")
        if self.sequence < 1:
            errors.append(f"sequence must be >= 1 (got {self.sequence}).")
        if not self.narration.strip():
            errors.append(f"Scene #{self.sequence} has empty narration text.")
        if not self.scene_objective.strip():
            errors.append(f"Scene #{self.sequence} has empty scene_objective.")
        if not self.visual_concept.strip():
            errors.append(f"Scene #{self.sequence} has empty visual_concept.")
        if self.duration_seconds <= 0:
            errors.append(f"Scene #{self.sequence} has non-positive duration ({self.duration_seconds}s).")
        return len(errors) == 0, errors

    def to_universal_scene(self) -> UniversalScene:
        """Converts to UniversalScene for seamless compatibility with existing render pipeline."""
        archetype = self.scene_type.to_visual_archetype()
        props = SceneProps(
            headline=self.on_screen_text or self.visual_concept[:48],
            hero_word=self.visual_concept.split()[0].upper() if self.visual_concept.split() else "SYSTEM",
            motion_preset=self.motion_direction,
            evidence_ids=self.evidence_references,
            quote_text=self.narration if archetype == VisualArchetype.SKETCH_QUOTE else "",
        )
        return UniversalScene(
            scene_id=self.scene_id,
            scene_index=self.sequence,
            duration_seconds=self.duration_seconds,
            narrative_role=f"BEAT_{self.sequence}",
            visual_archetype=archetype,
            narration_text=self.narration,
            on_screen_text=self.on_screen_text or self.visual_concept[:48],
            visual_props=props,
            captions=CaptionConfig(),
            badge=f"SCENE {self.sequence}",
            transition=self.transition_in,
        )

    def to_contract(self) -> Any:
        """Losslessly converts DynamicScene to UniversalSceneContract (v3.0.0)."""
        from core.universal_scene_contract import UniversalSceneContract
        return UniversalSceneContract.from_dynamic_scene(self)

    @classmethod
    def from_contract(cls, contract: Any) -> "DynamicScene":
        """Reconstructs DynamicScene from UniversalSceneContract."""
        return contract.to_dynamic_scene()

    def to_dict(self) -> Dict[str, Any]:
        """Outputs rich dictionary compatible with legacy and modern modules."""
        dur = self.duration_seconds
        return {
            "scene_id": self.scene_id,
            "sequence": self.sequence,
            "scene_number": self.sequence,                 # legacy alias
            "narration": self.narration,
            "narration_text": self.narration,              # legacy alias
            "scene_objective": self.scene_objective,
            "scene_type": self.scene_type.value,
            "visual_type": self.scene_type.to_visual_archetype().value, # renderer alias
            "visual_archetype": self.scene_type.to_visual_archetype().value,
            "visual_concept": self.visual_concept,
            "visual_description": self.visual_description,
            "asset_requirements": [a.to_dict() for a in self.asset_requirements],
            "camera_direction": self.camera_direction,
            "motion_direction": self.motion_direction,
            "on_screen_text": self.on_screen_text,
            "headline": self.on_screen_text,               # legacy template alias
            "transition_in": self.transition_in,
            "transition_out": self.transition_out,
            "transition": self.transition_in,              # legacy alias
            "estimated_duration": self.estimated_duration,
            "actual_duration": self.actual_duration,
            "duration_seconds": dur,                       # modern pipeline alias
            "duration": dur,                               # legacy renderer alias
            "duration_est": self.estimated_duration,       # scene_planner alias
            "audio_cues": [c.to_dict() for c in self.audio_cues],
            "evidence_references": self.evidence_references,
            "production_complexity": self.production_complexity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DynamicScene:
        seq = int(data.get("sequence") or data.get("scene_number") or 1)
        s_id = str(data.get("scene_id") or f"scene_{seq:03d}")
        narr = str(data.get("narration") or data.get("narration_text") or "").strip()
        s_type = SceneType.from_str(data.get("scene_type") or data.get("visual_type") or "narrative_scene")
        obj = str(data.get("scene_objective") or data.get("narrative_purpose") or f"Communicate beat {seq}")
        concept = str(data.get("visual_concept") or data.get("visual_metaphor") or data.get("headline") or f"Visual Beat {seq}")
        desc = str(data.get("visual_description") or data.get("visual_action") or concept)
        on_text = str(data.get("on_screen_text") or data.get("headline") or "")

        est_dur = float(data.get("estimated_duration") or data.get("duration_est") or data.get("duration") or 5.0)
        act_dur = float(data["actual_duration"]) if data.get("actual_duration") is not None else None

        assets = [AssetRequirement(**a) if isinstance(a, dict) else a for a in data.get("asset_requirements", [])]
        cues = [AudioCue(**c) if isinstance(c, dict) else c for c in data.get("audio_cues", [])]
        ev_refs = data.get("evidence_references", [])

        return cls(
            scene_id=s_id,
            sequence=seq,
            narration=narr,
            scene_objective=obj,
            scene_type=s_type,
            visual_concept=concept,
            visual_description=desc,
            asset_requirements=assets,
            camera_direction=data.get("camera_direction", "push_in_slow"),
            motion_direction=data.get("motion_direction", "draw_reveal"),
            on_screen_text=on_text,
            transition_in=data.get("transition_in", "fade"),
            transition_out=data.get("transition_out", "cross_dissolve"),
            estimated_duration=est_dur,
            actual_duration=act_dur,
            audio_cues=cues,
            evidence_references=ev_refs,
            production_complexity=data.get("production_complexity", "standard"),
        )


@dataclass
class StoryArchitecturePlan:
    """Master narrative architecture formulated for a specific topic."""
    architecture_id: str
    topic_id: str
    topic_title: str
    narrative_structure: NarrativeStructureType
    selected_creative_format: CreativeFormatType
    recommended_scene_count: int
    target_duration_seconds: float
    structural_beats: List[Dict[str, Any]]
    rationale: str
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["narrative_structure"] = self.narrative_structure.value
        d["selected_creative_format"] = self.selected_creative_format.value
        return d


@dataclass
class CreativeDirectionPlan:
    """Production-ready creative direction produced by the Creative Director."""
    direction_id: str
    topic_id: str
    visual_theme: str
    color_palette: Dict[str, str]
    editorial_emphasis_claims: List[str]
    screen_demo_sections: List[int]
    diagram_sections: List[int]
    broll_sections: List[int]
    sound_design_strategy: str
    ending_resolution: str
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DynamicScenePlan:
    """Complete executable scene plan linking narrative architecture to video rendering."""
    plan_id: str
    topic_id: str
    creative_format: CreativeFormatType
    narrative_structure: NarrativeStructureType
    total_target_duration: float
    scenes: List[DynamicScene]
    architecture_plan: Optional[StoryArchitecturePlan] = None
    direction_plan: Optional[CreativeDirectionPlan] = None
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    @property
    def total_duration(self) -> float:
        return round(sum(s.duration_seconds for s in self.scenes), 2)

    def validate(self) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        if not self.scenes:
            errors.append("DynamicScenePlan must contain at least 1 scene.")
        for s in self.scenes:
            ok, s_errs = s.validate()
            if not ok:
                errors.extend(s_errs)
        return len(errors) == 0, errors

    def to_universal_scenes(self) -> List[UniversalScene]:
        """Losslessly converts all dynamic scenes to UniversalScene objects."""
        return [s.to_universal_scene() for s in self.scenes]

    def to_storyboard_contract(self) -> Any:
        """Converts DynamicScenePlan to VideoStoryboardContract."""
        from core.universal_scene_contract import UniversalSceneContract, VideoStoryboardContract
        contracts = [s.to_contract() for s in self.scenes]
        return VideoStoryboardContract(
            video_id=self.plan_id,
            title=f"Reel: {self.topic_id}",
            target_duration_seconds=self.total_target_duration,
            scenes=contracts,
        )

    @classmethod
    def from_storyboard_contract(cls, vsc: Any) -> "DynamicScenePlan":
        """Reconstructs DynamicScenePlan from VideoStoryboardContract."""
        dynamic_scenes = [s.to_dynamic_scene() for s in vsc.scenes]
        return cls(
            plan_id=vsc.video_id,
            topic_id=vsc.title.replace("Reel: ", "").strip(),
            creative_format=CreativeFormatType.TECH_DOCUMENTARY,
            narrative_structure=NarrativeStructureType.DISCOVERY_EXPLANATION_IMPLICATIONS,
            total_target_duration=vsc.target_duration_seconds,
            scenes=dynamic_scenes,
        )

    def to_legacy_storyboard_dict(self) -> Dict[str, Any]:
        """Provides backward-compatible dictionary for existing template builder and pipeline."""
        return {
            "plan_id": self.plan_id,
            "topic_id": self.topic_id,
            "total_duration": self.total_duration,
            "scenes": [s.to_dict() for s in self.scenes],
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "topic_id": self.topic_id,
            "creative_format": self.creative_format.value,
            "narrative_structure": self.narrative_structure.value,
            "total_target_duration": self.total_target_duration,
            "total_duration": self.total_duration,
            "scenes": [s.to_dict() for s in self.scenes],
            "architecture_plan": self.architecture_plan.to_dict() if self.architecture_plan else None,
            "direction_plan": self.direction_plan.to_dict() if self.direction_plan else None,
            "created_at": self.created_at,
        }


# ---------------------------------------------------------------------------
# Re-exports for Phase 4.3.2A Universal Scene Contract
# ---------------------------------------------------------------------------
from core.universal_scene_contract import (
    UniversalSceneContract,
    VideoStoryboardContract,
    RenderingEngine,
    TimingReference,
    VisualEvent,
    AssetProvenance,
    FactClaimEvidence,
    AudioProductionConfig,
    QualityAssuranceRecord,
    QAStatus,
)


