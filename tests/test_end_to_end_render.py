"""
SUPER.INTELLIGENCEEE — End-to-End Reel Production Test
Renders a complete 7-scene synthetic Reel, measures execution telemetry,
and verifies output compliance with FFprobe.
"""

import os
import pytest
from pathlib import Path

from core.database import get_db
from core.logger import get_system_resources
from intelligence.fallback_templates import FallbackTemplates
from rendering.video_renderer import VideoRenderer
from rendering.quality_checker import QualityChecker

def test_full_reel_render_end_to_end():
    db = get_db()
    res_start = get_system_resources()

    synthetic_article = {
        "title": "SYNTHETIC BENCHMARK: Sub-Quadratic Attention Scaled to Million-Token Context",
        "url": "https://synthetic.superintelligenceee.local/attention-scaling",
        "publisher": "Frontier AI Benchmark Institute",
        "summary": "Researchers demonstrated a sub-quadratic attention mechanism maintaining linear memory scaling across one million tokens. Empirical tests show 4.2x faster inference with zero loss in retrieval precision.",
        "category": "New AI Models & Releases",
        "published_date": "2026-11-04T12:00:00Z"
    }

    # 1. Generate full 7-scene structured script
    script = FallbackTemplates.generate_script(synthetic_article)
    assert len(script["scenes"]) == 7

    # 2. Save script into DB
    script_id = db.insert_script({
        "title": script["title"],
        "content_style": script["category"],
        "hook": script["hook"],
        "context": script["context"],
        "development": script["development"],
        "explanation": script["explanation"],
        "implications": script["implications"],
        "limitations": script["limitations"],
        "takeaway": script["takeaway"],
        "script_json": script,
        "word_count": script["word_count"],
        "est_duration": script["est_duration"],
        "status": "APPROVED"
    })
    assert script_id is not None

    # 3. Render Reel sequentially
    renderer = VideoRenderer()
    result = renderer.render_reel(script_or_id=script_id)

    assert result["success"] is True
    assert Path(result["video_path"]).exists()
    assert Path(result["cover_path"]).exists()
    assert Path(result["subtitle_path"]).exists()

    # 4. Strict FFprobe validation
    is_valid, q_msg, meta = QualityChecker.verify_video(result["video_path"])
    assert is_valid is True, f"FFprobe validation failed: {q_msg}"
    assert meta["width"] == 1080
    assert meta["height"] == 1920
    assert meta["is_h264"] is True
    assert meta["is_yuv420p"] is True
    assert meta["audio_stream_present"] is True
    assert 20.0 <= meta["duration_seconds"] <= 90.0

    # 5. Check memory consumption stayed within 8 GB laptop limits
    res_end = get_system_resources()
    assert res_end["ram_process_mb"] < 1024, "Process RAM exceeded 1 GB during render!"

    print(f"\nEnd-to-End Render Test Succeeded!")
    print(f"  Output MP4: {result['video_path']}")
    print(f"  File Size: {result['file_size_mb']} MB")
    print(f"  Duration: {result['duration_seconds']:.1f}s")
    print(f"  Render Time: {result['render_time_seconds']}s")
    print(f"  RAM Peak: {res_end['ram_process_mb']} MB")
