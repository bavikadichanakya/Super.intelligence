"""
Unit Tests for Publishing Telegram Bridge
Tests unconfigured states, mocked API delivery, and remote approval action callbacks.
"""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from core.database import Database
from publishing.telegram_bridge import TelegramBridge


@pytest.fixture
def test_db(tmp_path):
    db_file = tmp_path / "test_telegram.db"
    return Database(str(db_file))


def test_telegram_unconfigured(test_db):
    bridge = TelegramBridge(bot_token="", chat_id="", db=test_db)
    assert bridge.is_configured() is False

    res = bridge.send_notification("Test notification")
    assert res["success"] is False
    assert res["status"] == "NOT_CONFIGURED"

    video_res = bridge.send_reel_for_review(1, "fake.mp4", "Fake Title")
    assert video_res["success"] is False
    assert video_res["status"] == "NOT_CONFIGURED"


@patch("requests.post")
def test_telegram_send_notification_mock(mock_post, test_db):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"ok": True, "result": {"message_id": 9991}}
    mock_post.return_value = mock_resp

    bridge = TelegramBridge(bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11", chat_id="12345678", db=test_db)
    assert bridge.is_configured() is True

    res = bridge.send_notification("🚨 Autonomous Reel Rendered Successfully!")
    assert res["success"] is True
    assert res["status"] == "DELIVERED"
    assert res["message_id"] == 9991


def test_telegram_callback_approval(test_db, tmp_path):
    # Setup test draft video in DB
    dummy_video = tmp_path / "draft_reel.mp4"
    dummy_video.write_bytes(b"dummy mp4 video bytes")

    with test_db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO production_jobs (title, status, output_video_path)
            VALUES ('Telegram Test Reel', 'NEEDS_REVIEW', ?)
            """,
            (str(dummy_video),)
        )
        job_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO approvals (entity_type, entity_id, production_job_id, decision, status)
            VALUES ('video', ?, ?, 'PENDING', 'PENDING_REVIEW')
            """,
            (job_id, job_id)
        )

    bridge = TelegramBridge(bot_token="test_token", chat_id="test_chat", db=test_db)

    # Simulate Telegram inline button callback
    action_res = bridge.handle_callback_action(f"approve_{job_id}", reviewer="Alice Editor")
    if not action_res.get("success"):
        pytest.fail(f"action_res failed: {action_res}")
    assert action_res["success"] is True
    assert action_res["action"] == "APPROVED"

    # Verify DB state
    with test_db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM production_jobs WHERE id = ?", (job_id,))
        p_row = cursor.fetchone()
        assert p_row["status"] == "APPROVED"

        cursor.execute("SELECT status, decision, reviewer FROM approvals WHERE production_job_id = ?", (job_id,))
        a_row = cursor.fetchone()
        assert a_row["status"] == "APPROVED"
        assert a_row["decision"] == "APPROVED"
        assert a_row["reviewer"] == "Alice Editor"

