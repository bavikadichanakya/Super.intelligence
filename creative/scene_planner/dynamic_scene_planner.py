"""
SUPER.INTELLIGENCEEE — Dynamic Scene Planner
Synthesizes StoryArchitecturePlans and CreativeDirectionPlans into fully populated,
validated DynamicScenePlans with explicit camera movements, motion directions, and asset requirements.
"""

from __future__ import annotations

import logging
import re
import uuid
from typing import Any, Dict, List, Optional

from core.creative_contracts import (
    AssetRequirement,
    AudioCue,
    CreativeDirectionPlan,
    CreativeFormatType,
    DynamicScene,
    DynamicScenePlan,
    NarrativeStructureType,
    SceneType,
    StoryArchitecturePlan,
)
from core.schemas import ResearchDossier

logger = logging.getLogger("super_intelligence.dynamic_scene_planner")


class DynamicScenePlanner:
    """Produces validated, production-ready DynamicScenePlans with variable scene counts."""

    def __init__(self, config=None):
        self.config = config

    def _determine_scene_type(
        self,
        sequence: int,
        total_scenes: int,
        beat_role: str,
        direction_plan: CreativeDirectionPlan,
    ) -> SceneType:
        """Assigns the specific scene type based on creative direction and narrative role."""
        if sequence in direction_plan.screen_demo_sections:
            return SceneType.SCREEN_DEMONSTRATION
        elif sequence in direction_plan.diagram_sections:
            return SceneType.TECHNICAL_DIAGRAM
        elif sequence in direction_plan.broll_sections:
            return SceneType.CINEMATIC_BROLL

        # Role-based fallback
        role = beat_role.upper()
        if "HOOK" in role or sequence == 1:
            return SceneType.KINETIC_TYPOGRAPHY
        elif "BENCHMARK" in role or "RESULT" in role or "STAT" in role:
            return SceneType.DATA_VISUALIZATION
        elif "COMPARE" in role or "VS" in role:
            return SceneType.COMPARISON
        elif "MECHANISM" in role or "ARCH" in role:
            return SceneType.TECHNICAL_DIAGRAM
        elif "DEMO" in role or "TOOL" in role:
            return SceneType.PRODUCT_DEMONSTRATION
        elif sequence == total_scenes:
            return SceneType.NARRATIVE_SCENE
        else:
            return SceneType.ANIMATED_PROCESS

    def _determine_camera_motion(self, scene_type: SceneType) -> str:
        """Assigns dynamic camera movement tailored to the visual payload."""
        if scene_type in (SceneType.TECHNICAL_DIAGRAM, SceneType.DATA_VISUALIZATION):
            return "static_locked"  # Hold locked for diagram readability
        elif scene_type in (SceneType.SCREEN_DEMONSTRATION, SceneType.PRODUCT_DEMONSTRATION):
            return "push_in_slow"   # Slow focus on UI
        elif scene_type == SceneType.CINEMATIC_BROLL:
            return "drift_subtle"   # Subtle floating motion
        elif scene_type == SceneType.KINETIC_TYPOGRAPHY:
            return "snap_zoom"      # Punch on key words
        else:
            return "push_in_slow"

    def _determine_motion_preset(self, scene_type: SceneType) -> str:
        """Assigns rendering motion preset."""
        if scene_type == SceneType.TECHNICAL_DIAGRAM:
            return "draw_reveal"
        elif scene_type == SceneType.DATA_VISUALIZATION:
            return "slide_up"
        elif scene_type == SceneType.KINETIC_TYPOGRAPHY:
            return "zoom_punch"
        else:
            return "ken_burns"

    def plan_scenes(
        self,
        architecture_plan: StoryArchitecturePlan,
        direction_plan: CreativeDirectionPlan,
        script_data: Optional[Dict[str, Any]] = None,
        dossier: Optional[ResearchDossier] = None,
    ) -> DynamicScenePlan:
        """
        Synthesizes the complete DynamicScenePlan.
        Distributes narration text across beats and populates visual concepts.
        """
        topic_id = architecture_plan.topic_id
        title = architecture_plan.topic_title
        beats = architecture_plan.structural_beats
        total_scenes = len(beats)

        # Extract available narration snippets
        raw_script = script_data or {}
        narration_pool: List[str] = []

        # Check if full_narration or section keys exist
        if "scenes" in raw_script and isinstance(raw_script["scenes"], list):
            narration_pool = [s.get("narration_text", s.get("narration", "")) for s in raw_script["scenes"]]
        elif "full_narration" in raw_script and raw_script["full_narration"]:
            # Split full narration into matching number of sentences/chunks
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", raw_script["full_narration"]) if len(s.strip()) > 10]
            if len(sentences) >= total_scenes:
                # Distribute sentences across beats
                chunk_size = max(1, len(sentences) // total_scenes)
                for b_i in range(total_scenes):
                    start = b_i * chunk_size
                    end = (b_i + 1) * chunk_size if b_i < total_scenes - 1 else len(sentences)
                    narration_pool.append(" ".join(sentences[start:end]))
            else:
                narration_pool = sentences
        else:
            # Fallback sections
            for k in ["hook", "problem", "context", "development", "mechanism", "explanation", "results", "implications", "limitations", "takeaway", "verdict"]:
                if raw_script.get(k):
                    narration_pool.append(raw_script[k])

        dynamic_scenes: List[DynamicScene] = []
        target_total_dur = architecture_plan.target_duration_seconds

        for idx, beat in enumerate(beats, start=1):
            s_id = f"scene_{idx:03d}_{beat.get('role', 'beat').lower()[:12]}"
            beat_name = beat.get("beat_name", f"Beat #{idx}")
            objective = beat.get("objective", f"Deliver narrative beat #{idx}")
            pct = beat.get("target_pct", 1.0 / total_scenes)
            est_dur = round(max(3.5, target_total_dur * pct), 1)

            # Assign narration
            if idx - 1 < len(narration_pool) and narration_pool[idx - 1]:
                narr_text = narration_pool[idx - 1]
            else:
                narr_text = f"{beat_name}: Examining key technical principles of {title}."

            scene_type = self._determine_scene_type(idx, total_scenes, beat.get("role", ""), direction_plan)
            cam_motion = self._determine_camera_motion(scene_type)
            motion_dir = self._determine_motion_preset(scene_type)

            # Formulate visual concept and description
            if scene_type == SceneType.KINETIC_TYPOGRAPHY:
                vis_concept = f"PUNCH HOOK // {title.upper()[:36]}"
                vis_desc = "High-contrast bold kinetic typography pulsing over a dark neural mesh grid."
                on_text = title[:48]
            elif scene_type == SceneType.TECHNICAL_DIAGRAM:
                vis_concept = f"SYSTEM ARCHITECTURE // {beat_name.upper()}"
                vis_desc = "Schematic architectural flow showing decoupled tensor pipelines and memory allocation."
                on_text = f"ARCH: {beat_name.upper()}"
            elif scene_type == SceneType.DATA_VISUALIZATION:
                vis_concept = "VERIFIED BENCHMARK TELEMETRY"
                vis_desc = "Side-by-side comparative metric cards displaying throughput multiplier and memory delta."
                on_text = "EMPIRICAL PERFORMANCE GAIN"
            elif scene_type == SceneType.SCREEN_DEMONSTRATION:
                vis_concept = "TERMINAL CLI & INTERACTION"
                vis_desc = "Live terminal screen showing rapid inference execution with sub-second response times."
                on_text = "LOCAL RUNTIME EXECUTION"
            elif scene_type == SceneType.CINEMATIC_BROLL:
                vis_concept = "HARDWARE & SILICON FOOTAGE"
                vis_desc = "Cinematic slow-drift macro footage of microchip circuits and high-density server racks."
                on_text = "ENTERPRISE INFRASTRUCTURE"
            elif scene_type == SceneType.COMPARISON:
                vis_concept = "HEAD-TO-HEAD LATENCY COMPARISON"
                vis_desc = "Split-screen performance comparison measuring prior baseline vs current breakthrough."
                on_text = "BENCHMARK DELTA"
            else:
                vis_concept = f"EDITORIAL INSIGHT // {beat_name.upper()}"
                vis_desc = "HUD layout displaying summary synthesis with animated corner brackets and badges."
                on_text = beat_name.upper()

            # Asset Requirements
            asset_reqs = [
                AssetRequirement(
                    asset_id=f"ast_{s_id}_bg",
                    asset_type="image_png" if scene_type != SceneType.CINEMATIC_BROLL else "footage_mp4",
                    description=f"Visual asset for {scene_type.value}: {vis_concept}",
                )
            ]

            # Audio Cues
            audio_cues = []
            if idx > 1:
                audio_cues.append(
                    AudioCue(
                        cue_id=f"cue_{s_id}_trans",
                        cue_type="sfx_transition",
                        timestamp_offset_seconds=0.0,
                        asset_name="whoosh-cinematic.mp3",
                        volume_gain=0.18,
                    )
                )

            # Evidence references
            ev_refs = []
            if dossier and dossier.important_claims and idx <= len(dossier.important_claims):
                ev_refs.append(dossier.important_claims[idx - 1].claim_id)

            sc = DynamicScene(
                scene_id=s_id,
                sequence=idx,
                narration=narr_text,
                scene_objective=objective,
                scene_type=scene_type,
                visual_concept=vis_concept,
                visual_description=vis_desc,
                asset_requirements=asset_reqs,
                camera_direction=cam_motion,
                motion_direction=motion_dir,
                on_screen_text=on_text,
                transition_in="fade" if idx == 1 else "wipeleft" if idx % 2 == 0 else "cross_dissolve",
                transition_out="cross_dissolve",
                estimated_duration=est_dur,
                actual_duration=None,
                audio_cues=audio_cues,
                evidence_references=ev_refs,
                production_complexity="cinematic" if scene_type in (SceneType.TECHNICAL_DIAGRAM, SceneType.SCREEN_DEMONSTRATION) else "standard",
            )
            dynamic_scenes.append(sc)

        plan = DynamicScenePlan(
            plan_id=f"dplan_{str(uuid.uuid4())[:8]}",
            topic_id=topic_id,
            creative_format=architecture_plan.selected_creative_format,
            narrative_structure=architecture_plan.narrative_structure,
            total_target_duration=target_total_dur,
            scenes=dynamic_scenes,
            architecture_plan=architecture_plan,
            direction_plan=direction_plan,
        )

        logger.info(f"Generated DynamicScenePlan [{plan.plan_id}] with {len(dynamic_scenes)} dynamic scenes.")
        return plan

