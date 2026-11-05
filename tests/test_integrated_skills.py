"""
SUPER.INTELLIGENCEEE — Quality Verification Suite for Integrated Skills & Repositories
Tests:
- Hook scoring (Instagram & YouTube)
- Spoken beat timing & pacing flags
- Caption validation & 125-char truncation simulation
- AI slop detection & humanization
- Agent Reach multi-source retrieval, policy guards & DB ingestion
- YouTube title/thumbnail packaging linter
- YouTube Studio retention curve CSV analysis
- Transcript dead-air / EDL cuts
- YouTube chapter generation adhering to official rules
- SEO metadata package builder
- Approval gate preservation on publishing
"""

import os
import json
import pytest
from pathlib import Path

from core.database import Database
from intelligence.instagram_intel import (
    score_instagram_hook,
    rank_instagram_hooks,
    analyze_spoken_beats,
    lint_instagram_caption,
    detect_ai_slop,
    humanize_text,
)
from intelligence.youtube_intel import (
    check_youtube_title_thumbnail,
    score_youtube_hook,
    analyze_retention_csv,
    generate_deadair_edl,
    generate_youtube_chapters,
    build_youtube_seo_package,
)
from research.agent_reach_connector import AgentReachConnector, BLOCKED_CHANNELS
from publishing.youtube_integration import YouTubeIntegration


@pytest.fixture
def test_db(tmp_path):
    db_file = tmp_path / "test_integrated.db"
    return Database(str(db_file))


# ---------------------------------------------------------------------------
# 1. Hook Scoring Tests
# ---------------------------------------------------------------------------
def test_instagram_hook_scoring():
    # Strong hook with numbers, stakes, and brevity
    strong = "Engineers benchmarked a 3.8x speedup in neural pruning."
    s_res = score_instagram_hook(strong)
    assert s_res["score"] >= 70.0
    assert s_res["word_count"] <= 9
    assert len(s_res["dealbreakers"]) == 0
    assert s_res["subscores"]["concreteness"] >= 75.0

    # Bad hook triggering dealbreaker
    bad = "Stop scrolling! In this video today I wanted to tell you something crazy."
    b_res = score_instagram_hook(bad)
    assert b_res["score"] <= 30.0
    assert len(b_res["dealbreakers"]) > 0
    assert any("stop scrolling" in d.lower() for d in b_res["dealbreakers"])


def test_youtube_hook_scoring():
    yt_hook = "Why did researchers discard standard pruning models for this 3.8x technique?"
    h_res = score_youtube_hook(yt_hook)
    assert h_res["score"] >= 75.0
    assert h_res["has_question"] is True
    assert h_res["has_concrete"] is True


# ---------------------------------------------------------------------------
# 2. Spoken Beat Timing & Pacing Flags
# ---------------------------------------------------------------------------
def test_spoken_beat_timing():
    script = (
        "Engineers benchmarked a 3.8x inference speedup in neural pruning.\n"
        "This is an extraordinarily long sentence crafted deliberately to exceed the four second continuous speaking threshold on screen without any visual transition cut or pause.\n"
        "Final takeaway for your stack."
    )
    res = analyze_spoken_beats(script, wpm=165, target_seconds=30.0)
    assert res["beat_count"] >= 3
    assert res["total_duration_seconds"] > 0
    # Beat 2 is very long, should be flagged
    assert any("BEAT LONG" in str(b.get("flag")) for b in res["beats"])


# ---------------------------------------------------------------------------
# 3. Caption Validation & Truncation Simulation
# ---------------------------------------------------------------------------
def test_caption_validation():
    caption = (
        "Neural pruning reaches 3.8x throughput with zero accuracy loss! "
        "Engineers eliminated 60% of idle weights in transformer layers. "
        "Comment PRUNE below to get the full benchmark codebase.\n\n"
        "#AI #MachineLearning #TechNews #Innovation #NeuralNets"
    )
    res = lint_instagram_caption(caption)
    assert res["passed"] is True
    assert res["quality_score"] >= 80.0
    assert res["tag_count"] == 5
    assert len(res["asks"]) > 0
    assert res["truncated_at_feed"] is True
    assert "... more" in res["feed_preview_box"]


def test_caption_excessive_hashtags_and_filler():
    spam_caption = (
        "Check this out! #viral #fyp #explore #explorepage #foryou #foryoupage #tech #ai #innovation"
    )
    res = lint_instagram_caption(spam_caption)
    # Exceeds official 5 hashtag cap
    assert any(c["check"] == "HASHTAG_LIMIT" and c["status"] == "WARN" for c in res["checks"])
    # Contains filler tags
    assert any(c["check"] == "FILLER_TAGS" and c["status"] == "WARN" for c in res["checks"])


# ---------------------------------------------------------------------------
# 4. AI Slop Detection & Humanization
# ---------------------------------------------------------------------------
def test_ai_slop_detection_and_humanization():
    robotic = "In today's fast-paced digital landscape, we delve into the tapestry of cutting-edge AI breakthroughs."
    audit = detect_ai_slop(robotic)
    assert audit["human_score"] < 60.0
    assert audit["slop_hits_count"] >= 2
    assert "delve into" in audit["slop_hits"] or "delve" in audit["slop_hits"]
    assert "tapestry" in audit["slop_hits"]

    humanized, applied = humanize_text(robotic)
    assert len(applied) >= 2
    assert "delve" not in humanized.lower()
    assert "tapestry" not in humanized.lower()


# ---------------------------------------------------------------------------
# 5. Agent Reach Connector & Policy Safety
# ---------------------------------------------------------------------------
def test_agent_reach_blocked_channels(test_db):
    conn = AgentReachConnector(db=test_db)
    for blocked in BLOCKED_CHANNELS:
        res = conn._run_reach([blocked, "search", "test"])
        assert res["ok"] is False
        assert res["error"]["code"] == "POLICY_BLOCKED"


def test_agent_reach_ingestion_into_database(test_db):
    conn = AgentReachConnector(db=test_db)
    sample_items = [
        {
            "title": "vllm-project/vllm: High-throughput LLM serving",
            "url": "https://github.com/vllm-project/vllm",
            "source": "GitHub",
            "description": "High-throughput and memory-efficient LLM serving engine with PagedAttention.",
        },
        {
            "title": "FlashAttention-3 Released for Hopper GPUs",
            "url": "https://github.com/Dao-AILab/flash-attention",
            "source": "GitHub",
            "description": "Fast and memory-efficient exact attention with FP8 support.",
        }
    ]
    ids = conn.ingest_research_to_topics(sample_items, category="Technology Experiments")
    assert len(ids) == 2

    # Verify topics in database
    topics = test_db.get_topics()
    assert any(t["id"] in ids and "vllm" in t["title"].lower() for t in topics)
    assert any(t["id"] in ids and "flashattention" in t["title"].lower() for t in topics)


# ---------------------------------------------------------------------------
# 6. YouTube Title & Thumbnail Linter
# ---------------------------------------------------------------------------
def test_youtube_title_thumbnail_linter():
    # Good pairing
    good = check_youtube_title_thumbnail("Engineers Achieved 3.8x Neural Pruning in 2026", "3.8X FASTER")
    assert good["score"] >= 80.0
    assert good["is_optimal"] is True

    # Bad pairing: repeats words, shouting all caps, vague clickbait
    bad = check_youtube_title_thumbnail("INSANE CRAZY MASSIVE BREAKTHROUGH", "CRAZY BREAKTHROUGH")
    assert bad["is_optimal"] is False
    assert bad["score"] < 65.0
    assert any(i["category"] == "shouting" for i in bad["issues"])
    assert any(i["category"] == "vague" for i in bad["issues"])
    assert any(i["category"] == "duplicate" for i in bad["issues"])


# ---------------------------------------------------------------------------
# 7. Retention CSV Processing
# ---------------------------------------------------------------------------
def test_retention_csv_processing():
    csv_sample = """0,100
10,88
20,80
30,76
45,64
60,60
90,56
120,52"""
    res = analyze_retention_csv(csv_sample, duration_seconds=120)
    assert res["ok"] is True
    assert res["points_count"] == 8
    assert res["hook_leak_percent"] == 24.0
    assert res["verdict"] == "healthy"  # under 25% is healthy


# ---------------------------------------------------------------------------
# 8. Dead-Air & EDL Cuts
# ---------------------------------------------------------------------------
def test_transcript_deadair_edl():
    srt = """1
00:00:00,000 --> 00:00:03,000
Engineers achieved an autonomous 3.8x speedup.

2
00:00:04,500 --> 00:00:06,500
Um, basically.

3
00:00:07,000 --> 00:00:10,000
The architecture reduces memory overhead.
"""
    res = generate_deadair_edl(srt, floor_seconds=0.45)
    assert res["ok"] is True
    assert res["cut_count"] >= 2  # dead pause between cue 1 and 2, plus filler cue 2
    assert res["removed_seconds"] > 0
    assert res["projected_duration_seconds"] < res["original_duration_seconds"]


# ---------------------------------------------------------------------------
# 9. YouTube Chapters Generator
# ---------------------------------------------------------------------------
def test_youtube_chapter_generation():
    scenes = [
        {"duration": 12.0, "name": "Introduction & Hook"},
        {"duration": 15.0, "name": "Technical Mechanism"},
        {"duration": 14.0, "name": "Benchmark Results"},
        {"duration": 11.0, "name": "Future Outlook"},
    ]
    res = generate_youtube_chapters(scenes)
    assert res["ok"] is True
    assert res["valid_for_youtube"] is True
    assert res["chapter_count"] == 4
    assert res["chapters"][0]["start_seconds"] == 0.0
    assert "0:00 Introduction & Hook" in res["formatted_block"]


# ---------------------------------------------------------------------------
# 10. YouTube Shorts & SEO Package
# ---------------------------------------------------------------------------
def test_youtube_seo_package():
    pkg = build_youtube_seo_package(
        title="Autonomous AI Pruning Benchmarked at 3.8x Speed",
        summary="Engineers demonstrated dynamic layer pruning running on consumer hardware.",
        tags=["AI", "NeuralNets", "MachineLearning"],
    )
    assert len(pkg["title"]) <= 100
    assert "Subscribe to SUPER.INTELLIGENCEEE" in pkg["description"]
    assert "NeuralNets" in pkg["tags"]
    assert pkg["privacy_status"] == "private"


# ---------------------------------------------------------------------------
# 11. Approval Gate Preservation in Publishing
# ---------------------------------------------------------------------------
def test_youtube_publishing_approval_gate_preservation(test_db, tmp_path):
    yt = YouTubeIntegration(db=test_db)
    dummy_video = tmp_path / "test_unapproved.mp4"
    dummy_video.write_bytes(b"dummy video data")

    # Insert unapproved job
    with test_db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO production_jobs (title, status, output_video_path)
            VALUES ('Unapproved Draft Reel', 'NEEDS_REVIEW', ?)
            """,
            (str(dummy_video),)
        )
        job_id = cursor.lastrowid

    # Attempt to upload unapproved job
    res = yt.upload_video(
        video_path=dummy_video,
        title="Unapproved Draft",
        description="Testing approval gate",
        production_job_id=job_id,
    )

    # Must be blocked by approval gate
    assert res["ok"] is False
    assert "APPROVAL_GATE_BLOCKED" in res["error"]
