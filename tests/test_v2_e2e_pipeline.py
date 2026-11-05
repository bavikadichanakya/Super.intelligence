"""
End-to-End Production Test for SUPER.INTELLIGENCEEE V2.
Produces a complete 7-scene vertical video and verifies it with FFprobe.
"""

import pytest
from pathlib import Path
from core.database import Database
from core.pipeline import SuperIntelligencePipeline
from video.video_validator import VideoValidator

def test_full_autonomous_production_pipeline():
    db = Database()
    pipeline = SuperIntelligencePipeline(db=db)
    
    # Run production for a test topic
    test_topic = {
        "title": "NEURAL MEMORY SCALING BREAKTHROUGH",
        "summary": "AI researchers demonstrated linear memory scaling across million-token contexts, unlocking real-time inference on consumer hardware with zero accuracy degradation.",
        "category": "Artificial Intelligence",
        "source_url": "https://super.intelligenceee.local/memory-scaling"
    }
    
    with db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO topics (title, url, publisher, summary, category, score, status)
            VALUES (?, ?, ?, ?, ?, 95.0, 'DISCOVERED')
            """,
            (
                test_topic["title"],
                test_topic["source_url"],
                "Super Intelligence Lab",
                test_topic["summary"],
                test_topic["category"]
            )
        )
        t_id = cursor.lastrowid
        
    result = pipeline.produce_reel(topic_id=t_id)
    assert result["status"] == "NEEDS_REVIEW"
    assert result["production_job_id"] is not None
    
    video_path = Path(result["video_path"])
    assert video_path.exists(), f"Video file was not created: {video_path}"
    assert video_path.stat().st_size > 100000, f"Video file too small: {video_path.stat().st_size} bytes"
    
    # FFprobe Technical QA Verification
    validator = VideoValidator()
    report = validator.validate_reel(video_path)
    
    assert report["valid"] is True, f"FFprobe validation failed with issues: {report['issues']}"
    assert report["width"] == 1080
    assert report["height"] == 1920
    assert report["fps"] == 30.0
    assert "h264" in report["video_codec"].lower()
    assert "aac" in report["audio_codec"].lower()
    assert report["duration"] >= 15.0
    
    print("\n" + "="*60)
    print("END-TO-END REEL PRODUCTION & FFPROBE QA TEST PASSED")
    print("="*60)
    print(f"Output Video: {video_path}")
    print(f"Dimensions:   {report['width']}x{report['height']} (9:16 Vertical)")
    print(f"Frame Rate:   {report['fps']} FPS")
    print(f"Duration:     {report['duration']} seconds")
    print(f"File Size:    {report['file_size_mb']} MB")
    print(f"Video Codec:  {report['video_codec']}")
    print(f"Audio Codec:  {report['audio_codec']}")
    print("="*60 + "\n")
