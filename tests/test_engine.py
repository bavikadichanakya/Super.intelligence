"""
SUPER.INTELLIGENCEEE — Automated Quality Assurance Test Suite
Tests every subsystem using controlled synthetic benchmark data.
"""

import os
import json
import pytest
from pathlib import Path

from core.config_manager import get_config
from core.database import Database
from core.logger import get_system_resources
from research.source_extractor import SourceExtractor
from research.deduplicator import Deduplicator
from research.topic_ranker import TopicRanker
from research.fact_checking import FactChecker
from intelligence.fallback_templates import FallbackTemplates
from intelligence.script_generator import ScriptGenerator
from media.image_manager import ImageManager
from media.video_manager import VideoManager
from media.asset_manager import AssetManager
from media.license_manager import LicenseManager
from media.media_validator import MediaValidator
from audio.tts_engine import TTSEngine
from audio.subtitle_generator import SubtitleGenerator
from audio.audio_processor import AudioProcessor
from rendering.quality_checker import QualityChecker
from rendering.video_renderer import VideoRenderer
from publishing.content_queue import ContentQueue
from publishing.caption_manager import CaptionManager
from publishing.instagram_integration import InstagramIntegration
from analytics.performance_tracker import PerformanceTracker

# -------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------
@pytest.fixture
def synthetic_article():
    return {
        "title": "SYNTHETIC TEST: Autonomous Neural Pruning Benchmarked at 3.8x Speed",
        "url": "https://synthetic-test.superintelligenceee.local/benchmark-2026",
        "publisher": "Synthetic AI Research Lab",
        "summary": "Engineers benchmarked an autonomous algorithmic pruning technique achieving 3.8x inference throughput. The architecture reduces peak VRAM allocation while preserving output fidelity.",
        "category": "Technology Experiments",
        "published_date": "2026-11-04T12:00:00Z"
    }

@pytest.fixture
def test_db(tmp_path):
    db_file = tmp_path / "test_super_intelligence.db"
    db = Database(str(db_file))
    return db

# -------------------------------------------------------------
# 1. Database Persistence Tests
# -------------------------------------------------------------
def test_database_persistence(test_db, synthetic_article):
    # Insert article
    art_id = test_db.insert_article(synthetic_article)
    assert art_id is not None
    articles = test_db.get_articles()
    assert any(a["id"] == art_id for a in articles)

    # Status update
    ok = test_db.update_article_status(art_id, "SHORTLISTED")
    assert ok is True
    updated = test_db.get_articles(status="SHORTLISTED")
    assert any(a["id"] == art_id for a in updated)

# -------------------------------------------------------------
# 2. Duplicate Detection Tests
# -------------------------------------------------------------
def test_duplicate_detection(synthetic_article):
    existing = [synthetic_article]
    candidates = [
        synthetic_article,  # Exact duplicate
        {
            "title": "SYNTHETIC TEST: Autonomous Neural Pruning Benchmarked at 3.8x Speed",  # Duplicate title
            "url": "https://other-url.org/test",
            "publisher": "Other"
        },
        {
            "title": "Completely Novel Hardware Architecture for Quantum Sensing",
            "url": "https://unique-story.org/quantum",
            "publisher": "Quantum Lab"
        }
    ]
    unique = Deduplicator.filter_duplicates(candidates, existing)
    assert len(unique) == 1
    assert "Quantum" in unique[0]["title"]

# -------------------------------------------------------------
# 3. Source Extraction & Missing Field Handling
# -------------------------------------------------------------
def test_missing_source_handling():
    # Incomplete RSS entry
    raw_entry = {"title": "Raw Story without link"}
    feed_cfg = {"publisher": "Test Publisher", "category": "AI"}
    processed = SourceExtractor.process_entry(raw_entry, feed_cfg)
    assert processed["title"] == "Raw Story without link"
    assert processed["publisher"] == "Test Publisher"
    assert processed["url"] == ""

# -------------------------------------------------------------
# 4. Fact-Checking Editorial Workflow State Machine
# -------------------------------------------------------------
def test_fact_checking_workflow():
    # Valid transitions
    ok, _ = FactChecker.validate_transition("DISCOVERED", "SHORTLISTED")
    assert ok is True

    # Invalid jump: DISCOVERED -> VERIFIED without being SHORTLISTED & RESEARCHED
    blocked, msg = FactChecker.validate_transition("DISCOVERED", "VERIFIED")
    assert blocked is False
    assert "SHORTLISTED" in msg

    # Rejection is always allowed
    rej_ok, _ = FactChecker.validate_transition("SHORTLISTED", "REJECTED")
    assert rej_ok is True

# -------------------------------------------------------------
# 5. Offline Fallback Script Generation & JSON Validation
# -------------------------------------------------------------
def test_offline_fallback_script(synthetic_article):
    script = FallbackTemplates.generate_script(synthetic_article)
    assert "hook" in script
    assert "context" in script
    assert "development" in script
    assert "explanation" in script
    assert "implications" in script
    assert "limitations" in script
    assert "takeaway" in script
    assert len(script["scenes"]) == 7

    # Validate with ScriptGenerator rules
    valid, msg = ScriptGenerator.validate_script(script)
    assert valid is True, msg

# -------------------------------------------------------------
# 6. Asset Licensing & Provenance Verification
# -------------------------------------------------------------
def test_asset_licensing():
    # Permitted license
    ok, _ = LicenseManager.validate_license("Editorial Generated")
    assert ok is True

    # Permitted with attribution
    ok_by, _ = LicenseManager.validate_license("CC-BY", attribution="MIT Open Courseware")
    assert ok_by is True

    # Failed attribution requirement
    bad_by, msg = LicenseManager.validate_license("CC-BY", attribution="")
    assert bad_by is False
    assert "requires explicit creator attribution" in msg

    # Disallowed license
    bad_lic, _ = LicenseManager.validate_license("All Rights Reserved Random Scraping")
    assert bad_lic is False

# -------------------------------------------------------------
# 7. Media Validator (9:16 Aspect Ratio)
# -------------------------------------------------------------
def test_media_validator(tmp_path):
    from PIL import Image
    # 1. Valid vertical 1080x1920
    vert_path = tmp_path / "valid_vertical.png"
    img_v = Image.new("RGB", (1080, 1920), color=(255, 255, 255))
    img_v.save(vert_path)
    ok_v, _, meta_v = MediaValidator.validate_image(str(vert_path))
    assert ok_v is True
    assert meta_v["is_exact_9_16"] is True

    # 2. Invalid horizontal image
    horiz_path = tmp_path / "invalid_horizontal.png"
    img_h = Image.new("RGB", (1920, 1080), color=(0, 0, 0))
    img_h.save(horiz_path)
    ok_h, msg_h, _ = MediaValidator.validate_image(str(horiz_path))
    assert ok_h is False
    assert "horizontal" in msg_h

# -------------------------------------------------------------
# 8. TTS Audio Generation & Durations
# -------------------------------------------------------------
def test_tts_audio_generation(tmp_path):
    tts = TTSEngine()
    out_audio = tmp_path / "test_synth.mp3"
    success, engine_name = tts.generate_speech("SUPER.INTELLIGENCEEE synthetic unit test narration.", str(out_audio))
    assert success is True
    assert engine_name in ("edge-tts", "pyttsx3")

    # Audio info inspection
    # Check either mp3 or wav
    actual_path = out_audio if out_audio.exists() else out_audio.with_suffix(".wav")
    assert actual_path.exists()
    info = AudioProcessor.get_audio_info(str(actual_path))
    assert info["duration"] > 0.5

# -------------------------------------------------------------
# 9. Subtitle Generation (SRT Timestamps & Line Wrapping)
# -------------------------------------------------------------
def test_subtitle_generation(tmp_path):
    scenes = [
        {"duration": 4.0, "narration": "First scene introducing breakthrough technology."},
        {"duration": 4.5, "narration": "Second scene detailing official laboratory benchmarks and metrics."}
    ]
    srt_out = tmp_path / "test.srt"
    SubtitleGenerator.generate_srt_from_scenes(scenes, str(srt_out))
    assert srt_out.exists()
    content = srt_out.read_text(encoding="utf-8")
    assert "00:00:00,000 -->" in content
    assert "FIRST SCENE" in content

# -------------------------------------------------------------
# 10. Image Manager Editorial Card Rendering (1080x1920)
# -------------------------------------------------------------
def test_editorial_card_rendering(tmp_path):
    im = ImageManager()
    card_path = tmp_path / "scene_card.png"
    scene_data = {
        "visual_type": "data_card",
        "badge": "BENCHMARK METRICS",
        "headline": "3.8x INFERENCE THROUGHPUT",
        "subtext": "SUPER.INTELLIGENCEEE LABS"
    }
    rendered_path = im.create_scene_card(scene_data, str(card_path))
    assert Path(rendered_path).exists()
    valid, _, meta = MediaValidator.validate_image(rendered_path)
    assert valid is True
    assert meta["width"] == 1080
    assert meta["height"] == 1920

# -------------------------------------------------------------
# 11. Ken Burns Motion Clip Generation (VideoManager)
# -------------------------------------------------------------
def test_video_motion_clip(tmp_path):
    im = ImageManager()
    card_path = tmp_path / "motion_source.png"
    im.create_scene_card({"headline": "MOTION CLIP TEST"}, str(card_path))

    clip_path = tmp_path / "test_motion.mp4"
    ok = VideoManager.create_motion_clip(str(card_path), str(clip_path), duration=2.0, motion_style="zoom_in")
    assert ok is True
    assert clip_path.exists()

# -------------------------------------------------------------
# 12. Quality Checker & FFprobe Compliance
# -------------------------------------------------------------
def test_quality_checker_ffprobe(tmp_path):
    # Non-existent file
    ok, msg, _ = QualityChecker.verify_video(str(tmp_path / "non_existent.mp4"))
    assert ok is False
    assert "does not exist" in msg

# -------------------------------------------------------------
# 13. Publishing Queue & Package Bundling
# -------------------------------------------------------------
def test_publishing_queue_and_package(test_db, tmp_path):
    queue = ContentQueue(db=test_db)
    # Create production job first to satisfy foreign key constraint
    job_id = test_db.create_production_job(None, "Synthetic AI Frontier Reel")
    assert job_id is not None

    # Add item
    item_id = test_db.add_to_publishing_queue({
        "job_id": job_id,
        "title": "Synthetic AI Frontier Reel",
        "caption": "Full test caption for Instagram #superintelligence",
        "hashtags": "#superintelligence #ai",
        "scheduled_for": "2026-11-05 11:30:00",
        "status": "QUEUED"
    })
    assert item_id is not None
    # Update status
    ok = queue.update_status(item_id, "SCHEDULED")
    assert ok is True

# -------------------------------------------------------------
# 14. Dashboard Flask Routes
# -------------------------------------------------------------
def test_dashboard_routes():
    from dashboard.app import create_app
    app = create_app()
    client = app.test_client()

    # Main dashboard view
    res = client.get("/")
    assert res.status_code == 200
    assert b"SUPER.INTELLIGENCEEE" in res.data

    # Telemetry API
    t_res = client.get("/api/telemetry")
    assert t_res.status_code == 200
    t_data = t_res.get_json()
    assert "resources" in t_data
    assert "ram_process_mb" in t_data["resources"]
