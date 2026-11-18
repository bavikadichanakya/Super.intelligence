"""
SUPER.INTELLIGENCEEE — Phase 4.3.2A Universal Scene Contract Unit Tests
Validates:
- Valid scene construction
- Missing required fields
- Invalid timestamps (negative, end < start, exceeding duration)
- Word timestamp ordering & synthetic fallback
- Asset licensing & verification status
- Scientific evidence & claim fact-checking
- Rendering engine validation
- JSON serialization & deserialization
- VideoStoryboardContract cross-scene validation (duplicate IDs, sequence gaps)
"""

import json
import pytest
from pydantic import ValidationError

from core.universal_scene_contract import (
    UniversalSceneContract,
    VideoStoryboardContract,
    RenderingEngine,
    SceneType,
    EvidenceStatus,
    QAStatus,
    TimingReference,
    SentenceTimestamp,
    CaptionSegment,
    VisualEvent,
    AssetProvenance,
    FactClaimEvidence,
    AudioCueConfig,
    AudioProductionConfig,
    QualityAssuranceRecord,
)


def create_valid_test_scene(seq: int = 1, scene_id: str = "scene_001") -> UniversalSceneContract:
    return UniversalSceneContract(
        scene_id=scene_id,
        sequence_number=seq,
        scene_type=SceneType.TECHNICAL_DIAGRAM,
        narrative_stage="MECHANISM",
        narrative_purpose="Explain quadratic attention bottleneck",
        audience_takeaway="Standard attention scales as O(N^2), saturating memory",
        learning_objective="Understand quadratic scaling",
        narration_text="Standard self attention computes token relationships across every pair, scaling memory quadratically.",
        narration_duration_seconds=5.0,
        visual_concept="Attention matrix expansion",
        mechanism_description="Token sequences cross-multiplied into N by N matrix",
        camera_instructions="push_in_slow",
        motion_instructions="matrix_expand",
        preferred_engine=RenderingEngine.MANIM,
        fallback_engine=RenderingEngine.HYPERFRAMES,
        word_timestamps=[
            TimingReference(word="Standard", start_sec=0.0, end_sec=0.5),
            TimingReference(word="self", start_sec=0.5, end_sec=0.9),
            TimingReference(word="attention", start_sec=0.9, end_sec=1.6),
            TimingReference(word="computes", start_sec=1.6, end_sec=2.2),
            TimingReference(word="token", start_sec=2.2, end_sec=2.8),
            TimingReference(word="relationships", start_sec=2.8, end_sec=3.6),
            TimingReference(word="quadratically", start_sec=3.6, end_sec=4.8),
        ],
        caption_segments=[
            CaptionSegment(
                segment_id="cap_01",
                start_sec=0.0,
                end_sec=4.9,
                text="Standard self-attention scales quadratically O(N^2)",
                safe_margin_bottom=340,
            )
        ],
        visual_events=[
            VisualEvent(
                event_id="ev_matrix_01",
                trigger_timestamp=0.5,
                duration=3.5,
                subject="Token Matrix",
                action="Grid expands from 4x4 to 128x128",
                intended_understanding="Observe exponential cell explosion",
            )
        ],
        asset_requirements=[
            AssetProvenance(
                asset_id="asset_matrix_svg",
                asset_type="diagram_svg",
                provider="local_procedural",
                creator="super_intelligence_engine",
                license_name="Editorial Generated",
                verification_status="INTERNAL_GENERATED",
            )
        ],
        evidence_items=[
            FactClaimEvidence(
                claim_id="claim_vaswani_2017",
                claim_text="Attention Is All You Need establishes O(N^2) memory complexity",
                source_url="https://arxiv.org/abs/1706.03762",
                publisher="NeurIPS",
                verification_status=EvidenceStatus.VERIFIED,
                confidence=1.0,
            )
        ],
    )


def test_valid_scene_construction():
    scene = create_valid_test_scene()
    assert scene.scene_id == "scene_001"
    assert scene.sequence_number == 1
    assert scene.duration_seconds == 5.0
    assert scene.preferred_engine == RenderingEngine.MANIM
    assert scene.qa_record.schema_validation is True
    assert len(scene.word_timestamps) == 7


def test_missing_required_fields_fails():
    with pytest.raises(ValidationError):
        # Empty scene_id
        UniversalSceneContract(
            scene_id="",
            sequence_number=1,
            narrative_purpose="Purpose",
            audience_takeaway="Takeaway",
            narration_text="Narration",
            narration_duration_seconds=5.0,
            visual_concept="Concept",
            mechanism_description="Desc",
        )

    with pytest.raises(ValidationError):
        # Non-positive duration
        UniversalSceneContract(
            scene_id="scene_001",
            sequence_number=1,
            narrative_purpose="Purpose",
            audience_takeaway="Takeaway",
            narration_text="Narration",
            narration_duration_seconds=-2.0,
            visual_concept="Concept",
            mechanism_description="Desc",
        )


def test_invalid_timestamps_rejected():
    # 1. Negative timestamp
    with pytest.raises(ValidationError):
        TimingReference(word="test", start_sec=-1.0, end_sec=1.0)

    # 2. End time before start time
    with pytest.raises(ValidationError):
        TimingReference(word="test", start_sec=2.0, end_sec=1.0)

    # 3. Caption segment end time exceeding scene duration
    with pytest.raises(ValidationError):
        scene = create_valid_test_scene()
        scene_dict = scene.to_dict()
        scene_dict["caption_segments"] = [
            {"segment_id": "c1", "start_sec": 0.0, "end_sec": 10.0, "text": "Exceeding duration"}
        ]
        scene_dict["narration_duration_seconds"] = 4.0
        UniversalSceneContract(**scene_dict)


def test_out_of_order_word_timestamps_rejected():
    scene_dict = create_valid_test_scene().to_dict()
    scene_dict["word_timestamps"] = [
        {"word": "first", "start_sec": 2.0, "end_sec": 2.5, "confidence": 1.0},
        {"word": "second", "start_sec": 1.0, "end_sec": 1.5, "confidence": 1.0},  # Out of order
    ]
    with pytest.raises(ValidationError):
        UniversalSceneContract(**scene_dict)


def test_synthetic_word_timings_fallback():
    # If no word timestamps provided, model synthesizes them linearly
    scene = UniversalSceneContract(
        scene_id="scene_synth",
        sequence_number=1,
        narrative_purpose="Test synthetic timing",
        audience_takeaway="Takeaway",
        narration_text="One two three four",
        narration_duration_seconds=4.0,
        visual_concept="Concept",
        mechanism_description="Desc",
    )
    assert len(scene.word_timestamps) == 4
    assert scene.word_timestamps[0].word == "One"
    assert scene.word_timestamps[0].start_sec == 0.0
    assert scene.word_timestamps[3].word == "four"
    assert scene.word_timestamps[3].end_sec == 4.0


def test_asset_licensing_verification():
    # Rejected asset status causes ValidationError
    with pytest.raises(ValidationError):
        AssetProvenance(
            asset_id="asset_bad",
            asset_type="footage_mp4",
            verification_status="REJECTED",
        )


def test_unverified_claim_evidence_recorded_in_qa():
    scene = create_valid_test_scene()
    scene_dict = scene.to_dict()
    scene_dict["evidence_items"] = [
        {
            "claim_id": "unverified_metric_01",
            "claim_text": "Unverified 100x speedup claim",
            "verification_status": "UNVERIFIED",
            "confidence": 0.2,
        }
    ]
    contract = UniversalSceneContract(**scene_dict)
    # Must record limitation in QA record failure reasons
    assert any("UNVERIFIED" in reason for reason in contract.qa_record.failure_reasons)


def test_json_serialization_and_deserialization():
    scene = create_valid_test_scene()
    json_str = scene.model_dump_json()
    assert isinstance(json_str, str)
    
    data = json.loads(json_str)
    reconstructed = UniversalSceneContract(**data)
    assert reconstructed.scene_id == scene.scene_id
    assert reconstructed.sequence_number == scene.sequence_number
    assert reconstructed.narration_duration_seconds == scene.narration_duration_seconds
    assert reconstructed.preferred_engine == scene.preferred_engine


def test_video_storyboard_contract_valid():
    s1 = create_valid_test_scene(seq=1, scene_id="scene_001")
    s2 = create_valid_test_scene(seq=2, scene_id="scene_002")
    
    board = VideoStoryboardContract(
        video_id="video_reel_001",
        title="Attention Scaling Breakthrough",
        target_duration_seconds=10.0,
        scenes=[s1, s2],
    )
    assert board.total_duration_seconds == 10.0
    assert len(board.scenes) == 2


def test_video_storyboard_duplicate_scenes_rejected():
    s1 = create_valid_test_scene(seq=1, scene_id="duplicate_id")
    s2 = create_valid_test_scene(seq=2, scene_id="duplicate_id")
    
    with pytest.raises(ValidationError):
        VideoStoryboardContract(
            video_id="video_fail",
            title="Duplicate Test",
            target_duration_seconds=10.0,
            scenes=[s1, s2],
        )


def test_video_storyboard_non_sequential_scenes_rejected():
    s1 = create_valid_test_scene(seq=1, scene_id="scene_001")
    s3 = create_valid_test_scene(seq=3, scene_id="scene_003")  # Missing seq 2
    
    with pytest.raises(ValidationError):
        VideoStoryboardContract(
            video_id="video_fail_seq",
            title="Non Sequential Test",
            target_duration_seconds=10.0,
            scenes=[s1, s3],
        )

