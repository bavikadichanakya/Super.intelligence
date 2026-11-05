"""
Tests for Core Foundation: config, database schema, provenance, task status, and job manager.
"""

import pytest
from pathlib import Path
from core.config import get_config
from core.database import Database
from core.provenance import LegalProvenanceRecord, LicenseType
from core.task_status import JobStatus, ScriptStatus
from core.job_manager import JobManager

def test_config_loader():
    cfg = get_config()
    assert cfg.get("project.name") == "SUPER.INTELLIGENCEEE"
    assert cfg.get("video.width") == 1080
    assert cfg.get("video.height") == 1920
    assert cfg.get("video.fps") == 30

def test_database_tables():
    db = Database()
    with db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}

    expected_tables = {
        "topics", "sources", "scripts", "storyboards", "assets",
        "narration_jobs", "caption_jobs", "render_jobs", "production_jobs",
        "approvals", "publishing_queue", "analytics", "application_settings"
    }
    for t in expected_tables:
        assert t in tables, f"Missing expected table: {t}"

def test_provenance_validation():
    prov = LegalProvenanceRecord(
        license_type=LicenseType.EDITORIAL_GENERATED,
        source_url="https://super.intelligenceee.local",
        author_or_creator="SUPER.INTELLIGENCEEE Engine",
        verification_notes="Locally synthesized graphic asset"
    )
    assert prov.is_legally_cleared() is True

    uncit = LegalProvenanceRecord(
        license_type=LicenseType.CC_BY,
        source_url="",
        author_or_creator=""
    )
    assert uncit.is_legally_cleared() is False

def test_job_manager_sequential():
    import time
    jm = JobManager(max_workers=1)
    def simple_task(job):
        return 42 * 2
    job_id = jm.submit_job("test_task", simple_task)
    assert job_id is not None
    # Wait briefly for execution
    for _ in range(20):
        info = jm.get_job(job_id)
        if info and info["status"] == "COMPLETED":
            break
        time.sleep(0.05)
    assert jm.get_job(job_id)["status"] == "COMPLETED"
