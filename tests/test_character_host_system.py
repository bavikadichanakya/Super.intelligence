import pytest
from pathlib import Path
from PIL import Image

from core.character_scene_config import (
    CharacterSceneConfig,
    CharacterPose,
    CharacterExpression,
    CharacterScreenPosition,
    CharacterMovementPattern,
)
from core.character_quality_validator import CharacterQualityValidator
from core.universal_scene_contract import UniversalSceneContract, SchemaVersion
from rendering.character_host_engine import CharacterHostEngine


def test_canonical_reference_asset_integrity():
    validator = CharacterQualityValidator()
    res = validator.validate_reference_asset_integrity()
    assert res["passed"] is True, f"Integrity check failed: {res['violations']}"
    assert res["sha256"] == "d17de5c978e153a8ef8b332849e4ea653eb7e9fddf7d03b5dbdaf02daac96fde"


def test_character_scene_config_validation():
    # Valid presenter config
    valid_cfg = CharacterSceneConfig(
        appears=True,
        editorial_reason="Introduce the NVIDIA Hopper memory wall bottleneck",
        pose=CharacterPose.PRESENTER_DIRECT,
        expression=CharacterExpression.CURIOUS_INQUIRY,
        screen_position=CharacterScreenPosition.CENTER_HERO,
        movement_pattern=CharacterMovementPattern.NATURAL_BREATHING_AND_BLINK,
        scale=0.70,
    )
    assert valid_cfg.appears is True
    assert valid_cfg.pose == CharacterPose.PRESENTER_DIRECT

    # Collision with subtitle safe zone raises error
    with pytest.raises(ValueError, match="collides with the subtitle safe zone"):
        CharacterSceneConfig(
            appears=True,
            editorial_reason="Invalid placement testing",
            custom_bottom_y=1700,  # inside 1640..1820
        )


def test_universal_scene_contract_with_character():
    contract_data = {
        "scene_id": "scene_001_hook",
        "sequence_number": 1,
        "narrative_stage": "HOOK",
        "narrative_purpose": "Capture viewer attention with benchmark proof",
        "audience_takeaway": "Understand 740 TFLOPs throughput on H100",
        "narration_text": "FlashAttention-3 unlocks 740 teraflops on H100 silicon.",
        "narration_duration_seconds": 6.5,
        "visual_concept": "Host presenter beside benchmark comparison",
        "mechanism_description": "Live counter surging to 740 TFLOPs",
        "character_presence": {
            "appears": True,
            "editorial_reason": "Host introduces the hardware benchmark directly to audience",
            "pose": "presenter_direct",
            "expression": "curious_inquiry",
            "screen_position": "center_hero",
            "movement_pattern": "natural_breathing_and_blink",
            "scale": 0.72
        }
    }
    scene = UniversalSceneContract(**contract_data)
    assert scene.character_presence is not None
    assert scene.character_presence.appears is True
    assert scene.character_presence.pose == CharacterPose.PRESENTER_DIRECT
    assert scene.character_presence.scale == 0.72


def test_character_host_engine_rendering():
    engine = CharacterHostEngine()
    config = CharacterSceneConfig(
        appears=True,
        editorial_reason="Host test render",
        pose=CharacterPose.PRESENTER_DIRECT,
        expression=CharacterExpression.CURIOUS_INQUIRY,
        screen_position=CharacterScreenPosition.CENTER_HERO,
        scale=0.65
    )

    # 1. Test motion states
    state_0 = engine.compute_motion_state(config, 0.0)
    state_blink = engine.compute_motion_state(config, 0.05)  # within 0.150s blink window
    state_open = engine.compute_motion_state(config, 1.0)    # outside blink window

    assert state_blink["is_blinking"] is True
    assert state_open["is_blinking"] is False

    # 2. Test compositing onto 1080x1920 canvas
    canvas = Image.new("RGBA", (1080, 1920), (10, 14, 20, 255))
    bbox = engine.composite_onto_canvas(canvas, config, t_sec=1.5, ambient_tint_hex="#00e5ff")
    assert len(bbox) == 4
    x0, y0, x1, y1 = bbox
    assert x1 > x0
    assert y1 > y0

    # 3. Test subtitle safe zone collision check
    safe, msg = engine.check_subtitle_safe_zone_collision(bbox)
    assert safe is True, f"Default center hero anchor collided: {msg}"


def test_character_quality_validator_rules():
    validator = CharacterQualityValidator()

    # Aspect ratio check
    safe, msg = validator.validate_aspect_ratio_and_distortion(1610, 1755)
    assert safe is True

    distorted, msg = validator.validate_aspect_ratio_and_distortion(1200, 1900)
    assert distorted is False
    assert "Aspect ratio distortion detected" in msg

    # Subtitle safe zone collision
    bad_bbox = (200, 1650, 800, 1780)
    res = validator.validate_scene_layout_safety(bad_bbox)
    assert res["passed"] is False
    assert any("subtitle safe-zone" in v for v in res["violations"])

    # Duplication check
    cfg1 = CharacterSceneConfig(appears=True, editorial_reason="Host 1")
    cfg2 = CharacterSceneConfig(appears=True, editorial_reason="Host 2")
    single_ok, _ = validator.validate_scene_character_count([cfg1])
    assert single_ok is True

    dup_bad, dup_msg = validator.validate_scene_character_count([cfg1, cfg2])
    assert dup_bad is False
    assert "Unexpected character duplication" in dup_msg
