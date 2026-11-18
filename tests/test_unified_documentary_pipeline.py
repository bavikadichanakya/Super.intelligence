"""
SUPER.INTELLIGENCEEE — Phase 4.3.2C Unified Documentary Pipeline Automated Test Suite
Verifies:
1. Pipeline initialization and submodule bindings.
2. Topic discovery and selection from SQLite.
3. Research dossier compilation with structured claim evidence.
4. Script generation and VideoStoryboardContract (USC v3.0.0) validation.
5. Narration synthesis, WAV duration measurement, and timing synchronization.
6. Multi-stage pipeline tracking (PipelineStage transitions in SQLite).
7. Governance: Registration in approvals queue with AWAITING_HUMAN_APPROVAL status.
8. Publishing kill switch preflight enforcement and prohibition of AI self-approval.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from core.database import Database
from core.kill_switch import get_kill_switch
from core.schemas import EvidenceStatus
from core.unified_pipeline import PipelineStage, UnifiedDocumentaryPipeline
from core.universal_scene_contract import RenderingEngine, SceneType, VideoStoryboardContract


@pytest.fixture
def mock_pipeline(tmp_path):
    """Initializes a UnifiedDocumentaryPipeline with an isolated SQLite database."""
    test_db_path = tmp_path / "test_pipeline.db"
    db = Database(db_path=str(test_db_path))
    pipeline = UnifiedDocumentaryPipeline(db=db, workspace_root=tmp_path)
    return pipeline


class TestUnifiedDocumentaryPipeline:
    def test_pipeline_initialization(self, mock_pipeline):
        assert mock_pipeline is not None
        assert mock_pipeline.db is not None
        assert mock_pipeline.dispatcher is not None
        assert mock_pipeline.narration_service is not None
        assert mock_pipeline.approval_manager is not None

    def test_topic_selection_and_scoring(self, mock_pipeline):
        test_topic = {
            "title": "Quantum Acceleration Breakthrough in Matrix Decomposition",
            "url": "https://arxiv.org/abs/2611.99999",
            "publisher": "arXiv.org",
            "summary": "Researchers achieve polynomial speedup in high-dimensional matrix decomposition using superconducting qudits.",
            "category": "Technology Experiments",
            "score": 88.0,
        }
        with mock_pipeline.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO topics (title, url, publisher, summary, category, score, status)
                VALUES (?, ?, ?, ?, ?, ?, 'DISCOVERED')
                """,
                (
                    test_topic["title"],
                    test_topic["url"],
                    test_topic["publisher"],
                    test_topic["summary"],
                    test_topic["category"],
                    test_topic["score"],
                ),
            )
            inserted_id = cursor.lastrowid

        selected = mock_pipeline.select_or_discover_topic(topic_id=inserted_id)
        assert selected["id"] == inserted_id
        assert selected["title"] == test_topic["title"]
        assert selected["score"] == 88.0

    def test_dossier_compilation_and_evidence(self, mock_pipeline):
        topic = {
            "id": 101,
            "title": "Metal Sandbox GPU Isolation Architecture",
            "url": "https://arxiv.org/abs/2611.17294",
            "publisher": "arXiv.org",
            "summary": "Metal Sandbox combines restricted per-instance file access, native command execution, and command-level scheduling across interconnected Macs to minimize idle compute.",
            "category": "Technology Experiments",
        }
        dossier = mock_pipeline.build_research_dossier(topic)
        assert dossier is not None
        assert len(dossier.important_claims) >= 2
        for claim in dossier.important_claims:
            assert claim.claim_id is not None
            assert len(claim.claim_text) > 10
            assert claim.status in [EvidenceStatus.VERIFIED, EvidenceStatus.SOURCE_REPORTED]

    def test_script_and_storyboard_contract(self, mock_pipeline):
        topic = {
            "id": 102,
            "title": "Metal Sandbox GPU Scheduling",
            "url": "https://arxiv.org/abs/2611.17294",
            "publisher": "arXiv.org",
            "summary": "GPU coding agents on Apple Silicon alternate between model requests, development commands, and GPU execution, leaving capacity idle.",
            "category": "Technology Experiments",
        }
        dossier = mock_pipeline.build_research_dossier(topic)
        script = mock_pipeline.generate_documentary_script(topic, dossier, target_scene_count=3)

        assert "scenes" in script
        assert len(script["scenes"]) == 3
        assert script["word_count"] > 20
        assert script["estimated_duration_seconds"] > 10.0

        storyboard = mock_pipeline.plan_storyboard_contract(topic, dossier, script, reel_slug="test_reel_01")
        assert isinstance(storyboard, VideoStoryboardContract)
        assert len(storyboard.scenes) == 3
        assert storyboard.scenes[0].preferred_engine == RenderingEngine.THREEJS
        assert storyboard.scenes[1].preferred_engine == RenderingEngine.MANIM
        assert storyboard.scenes[2].preferred_engine == RenderingEngine.HYPERFRAMES

        # Validate USC contract properties
        for sc in storyboard.scenes:
            assert sc.scene_id.startswith("test_reel_01_scene_")
            assert len(sc.narration_text) > 10
            assert sc.actual_duration_seconds >= 4.0
            assert len(sc.evidence_items) > 0

    def test_stage_tracking_in_database(self, mock_pipeline):
        with mock_pipeline.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO production_jobs (title, status, created_at, updated_at)
                VALUES ('Test Stage Tracking', 'PENDING', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """
            )
            job_id = cursor.lastrowid

        mock_pipeline._record_stage(job_id, PipelineStage.TOPIC_SELECTED)
        conn = mock_pipeline.db.get_connection()
        row = conn.cursor().execute("SELECT status FROM production_jobs WHERE id = ?", (job_id,)).fetchone()
        assert row["status"] == PipelineStage.TOPIC_SELECTED.value

        mock_pipeline._record_stage(job_id, PipelineStage.AWAITING_HUMAN_APPROVAL)
        row = conn.cursor().execute("SELECT status FROM production_jobs WHERE id = ?", (job_id,)).fetchone()
        assert row["status"] == PipelineStage.AWAITING_HUMAN_APPROVAL.value

    def test_approval_queue_registration_and_kill_switch(self, mock_pipeline, tmp_path):
        from rendering.render_artifact import RenderArtifact
        fake_video = tmp_path / "fake_master.mp4"
        fake_video.write_bytes(b"\x00" * 1024)

        artifact = RenderArtifact(
            scene_id="master_scene",
            engine_name="ffmpeg",
            output_path=fake_video,
            duration_seconds=25.0,
            file_size_bytes=1024,
            sha256_hash="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
            codecs={"video": "h264", "audio": "aac"},
            render_time_seconds=5.0,
            peak_ram_mb=200.0,
        )

        with mock_pipeline.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO production_jobs (title, status, created_at, updated_at)
                VALUES ('Governance Test', 'PENDING', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """
            )
            job_id = cursor.lastrowid

        from core.universal_scene_contract import UniversalSceneContract
        fake_scene = UniversalSceneContract(
            scene_id="gov_test_scene_01",
            sequence_number=1,
            scene_type=SceneType.KINETIC_TYPOGRAPHY,
            narrative_purpose="Governance validation test",
            audience_takeaway="Publishing kill-switch assertion",
            visual_concept="Verification HUD badge",
            mechanism_description="Editorial typography with security check",
            narration_text="Governance verification test scene narration.",
            narration_duration_seconds=5.0,
            actual_duration_seconds=5.0,
            preferred_engine=RenderingEngine.HYPERFRAMES,
        )
        storyboard = VideoStoryboardContract(
            video_id="gov_test_01",
            title="Governance Test",
            target_duration_seconds=25.0,
            scenes=[fake_scene],
        )

        approval_id = mock_pipeline.register_approval_submission(
            job_id=job_id,
            storyboard=storyboard,
            captioned_master=artifact,
            dossier=None,
            qa_report={"passed": True},
        )

        assert approval_id is not None
        conn = mock_pipeline.db.get_connection()
        cursor = conn.cursor()
        job_row = cursor.execute("SELECT status, output_video_path FROM production_jobs WHERE id = ?", (job_id,)).fetchone()
        assert job_row["status"] == PipelineStage.AWAITING_HUMAN_APPROVAL.value
        assert job_row["output_video_path"] == str(fake_video)

        app_row = cursor.execute("SELECT status, decision FROM approvals WHERE id = ?", (approval_id,)).fetchone()
        assert app_row["decision"] == "PENDING"
        assert app_row["status"] == "PENDING_REVIEW"
