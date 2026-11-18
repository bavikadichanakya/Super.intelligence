"""
SUPER.INTELLIGENCEEE — Phase 4.3.2A Scene Contract Compatibility & Adapter Tests
Validates:
- Round-trip lossless conversion: DynamicScene <-> UniversalSceneContract
- Round-trip lossless conversion: UniversalScene <-> UniversalSceneContract
- DynamicScenePlan <-> VideoStoryboardContract
- Legacy dictionary generation (.to_legacy_dict()) for SQLite compatibility
- Schema migration from legacy v1 dictionary to v3.0.0
"""

import pytest
from core.creative_contracts import (
    DynamicScene,
    DynamicScenePlan,
    SceneType as CCSceneType,
    AssetRequirement,
    AudioCue,
    CreativeFormatType,
    NarrativeStructureType,
)
from core.schemas import UniversalScene, VisualArchetype, SceneProps, CaptionConfig
from core.universal_scene_contract import (
    UniversalSceneContract,
    VideoStoryboardContract,
    RenderingEngine,
    SceneType,
)


def test_dynamic_scene_round_trip():
    # 1. Create a fully populated DynamicScene
    original_ds = DynamicScene(
        scene_id="scene_dyn_01",
        sequence=1,
        narration="Memory capacity scales with context window.",
        scene_objective="Establish the core compute bottleneck",
        scene_type=CCSceneType.TECHNICAL_DIAGRAM,
        visual_concept="Accelerator memory hierarchy",
        visual_description="3D stack of HBM memory modules with bandwidth indicators",
        asset_requirements=[
            AssetRequirement(
                asset_id="asset_hbm_svg",
                asset_type="diagram_svg",
                description="HBM module vector diagram",
                source_suggestion="local_procedural",
                is_mandatory=True,
                license_preference="Editorial Generated",
            )
        ],
        camera_direction="push_in_slow",
        motion_direction="stack_reveal",
        on_screen_text="HBM3e Memory Bandwidth",
        transition_in="fade",
        transition_out="cross_dissolve",
        estimated_duration=5.0,
        actual_duration=5.2,
        audio_cues=[
            AudioCue(
                cue_id="cue_whoosh_01",
                cue_type="sfx_transition",
                timestamp_offset_seconds=0.2,
                asset_name="whoosh.mp3",
                volume_gain=0.25,
            )
        ],
        evidence_references=["claim_ref_001"],
        production_complexity="cinematic",
    )

    # 2. Convert to UniversalSceneContract
    contract = original_ds.to_contract()
    assert isinstance(contract, UniversalSceneContract)
    assert contract.scene_id == original_ds.scene_id
    assert contract.sequence_number == original_ds.sequence
    assert contract.narration_text == original_ds.narration
    assert contract.duration_seconds == original_ds.duration_seconds
    assert contract.camera_instructions == original_ds.camera_direction
    assert contract.motion_instructions == original_ds.motion_direction
    assert len(contract.asset_requirements) == 1
    assert contract.asset_requirements[0].asset_id == "asset_hbm_svg"
    assert len(contract.audio_cues) == 1
    assert contract.audio_cues[0].cue_id == "cue_whoosh_01"
    assert contract.evidence_items[0].claim_id == "claim_ref_001"

    # 3. Convert back to DynamicScene
    reconstructed_ds = contract.to_dynamic_scene()
    assert isinstance(reconstructed_ds, DynamicScene)
    assert reconstructed_ds.scene_id == original_ds.scene_id
    assert reconstructed_ds.sequence == original_ds.sequence
    assert reconstructed_ds.narration == original_ds.narration
    assert reconstructed_ds.scene_objective == original_ds.scene_objective
    assert reconstructed_ds.scene_type == original_ds.scene_type
    assert reconstructed_ds.visual_concept == original_ds.visual_concept
    assert reconstructed_ds.visual_description == original_ds.visual_description
    assert reconstructed_ds.duration_seconds == original_ds.duration_seconds
    assert reconstructed_ds.camera_direction == original_ds.camera_direction
    assert reconstructed_ds.motion_direction == original_ds.motion_direction
    assert len(reconstructed_ds.asset_requirements) == len(original_ds.asset_requirements)
    assert len(reconstructed_ds.audio_cues) == len(original_ds.audio_cues)
    assert reconstructed_ds.evidence_references == original_ds.evidence_references


def test_universal_scene_round_trip():
    # 1. Create a UniversalScene
    original_us = UniversalScene(
        scene_id="scene_univ_01",
        scene_index=2,
        duration_seconds=4.5,
        narrative_role="CONTEXT_ESTABLISHMENT",
        visual_archetype=VisualArchetype.MOTION_DIAGRAM,
        narration_text="Neural network layers propagate activation matrices.",
        on_screen_text="Activation Flow: Layer 0 to 12",
        visual_props=SceneProps(
            headline="Activation Flow",
            hero_word="FLOW",
            motion_preset="draw_reveal",
            evidence_ids=["ev_source_042"],
        ),
        captions=CaptionConfig(
            enabled=True,
            safe_margin_bottom=320,
        ),
        badge="SCENE 2",
        transition="fade",
    )

    # 2. Convert to UniversalSceneContract
    contract = original_us.to_contract()
    assert isinstance(contract, UniversalSceneContract)
    assert contract.scene_id == original_us.scene_id
    assert contract.sequence_number == original_us.scene_index
    assert contract.duration_seconds == original_us.duration_seconds
    assert contract.narration_text == original_us.narration_text
    assert contract.evidence_items[0].claim_id == "ev_source_042"

    # 3. Convert back to UniversalScene
    reconstructed_us = contract.to_universal_scene()
    assert isinstance(reconstructed_us, UniversalScene)
    assert reconstructed_us.scene_id == original_us.scene_id
    assert reconstructed_us.scene_index == original_us.scene_index
    assert reconstructed_us.duration_seconds == original_us.duration_seconds
    assert reconstructed_us.narration_text == original_us.narration_text
    assert reconstructed_us.visual_archetype == original_us.visual_archetype
    assert reconstructed_us.visual_props.evidence_ids == original_us.visual_props.evidence_ids


def test_dynamic_scene_plan_to_storyboard_contract():
    ds1 = DynamicScene(
        scene_id="s1", sequence=1, narration="First beat.", scene_objective="Hook",
        scene_type=CCSceneType.KINETIC_TYPOGRAPHY, visual_concept="Title Hook",
        visual_description="Big kinetic words", estimated_duration=4.0
    )
    ds2 = DynamicScene(
        scene_id="s2", sequence=2, narration="Second beat.", scene_objective="Mechanism",
        scene_type=CCSceneType.DATA_VISUALIZATION, visual_concept="Scaling Chart",
        visual_description="Curve drawing", estimated_duration=6.0
    )
    plan = DynamicScenePlan(
        plan_id="plan_001",
        topic_id="scaling_breakthrough",
        creative_format=CreativeFormatType.TECH_DOCUMENTARY,
        narrative_structure=NarrativeStructureType.DISCOVERY_EXPLANATION_IMPLICATIONS,
        total_target_duration=10.0,
        scenes=[ds1, ds2],
    )

    # Convert to VideoStoryboardContract
    vsc = plan.to_storyboard_contract()
    assert isinstance(vsc, VideoStoryboardContract)
    assert vsc.video_id == "plan_001"
    assert vsc.total_duration_seconds == 10.0
    assert len(vsc.scenes) == 2

    # Reconstruct back
    reconstructed_plan = DynamicScenePlan.from_storyboard_contract(vsc)
    assert isinstance(reconstructed_plan, DynamicScenePlan)
    assert reconstructed_plan.plan_id == plan.plan_id
    assert len(reconstructed_plan.scenes) == 2


def test_legacy_dict_conversion_matches_sqlite_schema():
    contract = UniversalSceneContract(
        scene_id="scene_legacy_test",
        sequence_number=3,
        scene_type=SceneType.ANIMATED_PROCESS,
        narrative_purpose="Demonstrate token flow",
        audience_takeaway="Tokens pass through linear kernel",
        narration_text="Tokens flow into the linear projection.",
        narration_duration_seconds=5.0,
        visual_concept="Token Packet Stream",
        mechanism_description="Particles move along Bezier curve",
        camera_instructions="push_in_slow",
        motion_instructions="vector_flow",
    )

    legacy_dict = contract.to_legacy_dict()
    
    # Must contain exact keys required by SQLite storyboards table
    required_sqlite_keys = {
        "scene_number",
        "name",
        "narration",
        "on_screen_text",
        "visual_type",
        "instructions",
        "transition",
        "duration",
        "created_at",
    }
    assert required_sqlite_keys.issubset(legacy_dict.keys())
    assert legacy_dict["scene_number"] == 3
    assert legacy_dict["name"] == "scene_legacy_test"
    assert legacy_dict["duration"] == 5.0


def test_schema_migration_from_legacy_v1_dictionary():
    legacy_data = {
        "scene_number": 1,
        "name": "Intro Hook",
        "narration": "Artificial intelligence compute has hit a scaling wall.",
        "on_screen_text": "COMPUTE BOTTLENECK",
        "visual_type": "editorial_hud",
        "duration": 4.5,
        "transition": "fade",
        "instructions": "Zoom slow",
    }

    # Reconstruct into v3.0.0 contract
    contract = UniversalSceneContract.from_dict(legacy_data)
    assert contract.schema_version.value == "3.0.0"
    assert contract.sequence_number == 1
    assert contract.scene_id == "Intro Hook"
    assert contract.narration_text == legacy_data["narration"]
    assert contract.duration_seconds == 4.5
    assert contract.preferred_engine == RenderingEngine.HYPERFRAMES
    assert contract.qa_record.schema_validation is True

