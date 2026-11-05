"""
SUPER.INTELLIGENCEEE — Master Production Pipeline Coordinator
Orchestrates end-to-end production: Research -> Script -> Fact Check -> Narration -> Visuals -> Render -> QA -> Review.
Zero-budget, local-first execution.
"""

from __future__ import annotations

import datetime
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from audio.audio_mixer import AudioMixer
from audio.narration import NarrationService
from captions.caption_generator import CaptionGenerator
from captions.whisper_qa import WhisperQA
from content.fact_checker import FactChecker
from content.script_writer import ScriptWriter
from content.storyboard import StoryboardGenerator
from core.config import get_config
from core.database import Database
from core.task_status import JobStatus
from publishing.approval import ApprovalManager
from research.rss_collector import RSSCollector
from research.topic_scorer import TopicScorer
from video.ffmpeg_pipeline import FFmpegVideoPipeline
from video.hyperframes_runner import HyperFramesRunner
from video.template_builder import HyperFramesTemplateBuilder
from video.video_validator import VideoValidator
from visuals.stock_provider import StockProvider

logger = logging.getLogger("super_intelligence.pipeline")


class SuperIntelligencePipeline:
    """Master production engine coordinating all submodules sequentially."""

    def __init__(self, db: Optional[Database] = None, config=None):
        self.config = config or get_config()
        self.db = db or Database()

        # Initialize sub-services
        self.rss_collector = RSSCollector(self.db, self.config)
        self.topic_scorer = TopicScorer(self.db, self.config)
        self.script_writer = ScriptWriter(self.db, self.config)
        self.fact_checker = FactChecker(self.db, self.config)
        self.storyboard_gen = StoryboardGenerator(self.db, self.config)
        self.narration_service = NarrationService(self.db, self.config)
        self.audio_mixer = AudioMixer(self.config)
        self.caption_gen = CaptionGenerator(self.config)
        self.whisper_qa = WhisperQA()
        self.stock_provider = StockProvider(self.db, self.config)
        self.template_builder = HyperFramesTemplateBuilder(self.config)
        self.hyperframes_runner = HyperFramesRunner(self.config)
        self.ffmpeg_pipeline = FFmpegVideoPipeline(self.config)
        self.video_validator = VideoValidator(self.config)
        self.approval_mgr = ApprovalManager(self.db, self.config)

        self.drafts_dir = self.config.resolve_path("output/drafts")
        self.drafts_dir.mkdir(parents=True, exist_ok=True)

    def _slugify(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        return re.sub(r"[-\s]+", "_", text)[:40]

    def run_topic_research(self) -> List[Dict[str, Any]]:
        """Executes topic discovery and multi-dimensional scoring."""
        logger.info("Executing topic discovery and research...")
        collected = self.rss_collector.collect_all()
        logger.info(f"Collected {len(collected)} items from public tech feeds.")
        scored = self.topic_scorer.score_all_pending()
        logger.info(f"Scored {len(scored)} topics.")
        return scored

    def produce_reel(self, topic_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Executes complete production run for a specific topic or highest-scoring pending topic.
        """
        now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # 1. Select Topic
        topic = None
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            if topic_id:
                cursor.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
                row = cursor.fetchone()
                if row:
                    topic = dict(row)
            else:
                cursor.execute(
                    "SELECT * FROM topics WHERE score > 0 ORDER BY score DESC LIMIT 1"
                )
                row = cursor.fetchone()
                if row:
                    topic = dict(row)

        if not topic:
            # Fallback topic if database is empty
            topic = {
                "id": 1,
                "title": "Next-Generation Autonomous AI Systems Emerge",
                "summary": "Engineers deploy localized zero-latency AI production pipelines running completely offline on personal workstations.",
                "category": "Artificial Intelligence",
                "source_url": "https://super.intelligenceee.local",
            }

        reel_slug = f"reel_{now_str}_{self._slugify(topic['title'])}"
        logger.info(f"Starting production for: '{topic['title']}' (Slug: {reel_slug})")

        # Record production job in SQLite
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO production_jobs (topic_id, title, status, created_at, updated_at)
                VALUES (?, ?, 'IN_PROGRESS', ?, ?)
                """,
                (
                    topic.get("id"),
                    topic.get("title", "Autonomous Reel"),
                    datetime.datetime.now().isoformat(),
                    datetime.datetime.now().isoformat()
                ),
            )
            prod_job_id = cursor.lastrowid

        try:
            # 2. Generate Script
            script_data = self.script_writer.generate_script_for_topic(topic)
            script_id = self.script_writer.save_script(script_data, topic_id=topic.get("id"))

            # 3. Fact Checking & Verification
            fc_report = self.fact_checker.check_script(script_data, script_id=script_id)
            logger.info(f"Fact check passed: {fc_report['verified']}")

            # 4. Generate Storyboard
            raw_storyboard = self.storyboard_gen.generate_storyboard(script_data, script_id=script_id)
            scenes = raw_storyboard if isinstance(raw_storyboard, list) else raw_storyboard.get("scenes", [])
            storyboard = {"scenes": scenes}

            # 5. Synthesize Scene Narration via Piper TTS (with fallback)
            scene_audio_files = []
            for i, sc in enumerate(scenes):
                sc_idx = i + 1
                text = sc.get("narration_text", sc.get("narration", ""))
                audio_res = self.narration_service.synthesize_speech(
                    text=text,
                    output_filename=f"{reel_slug}_scene_{sc_idx}.wav",
                )
                scene_audio_files.append(audio_res["path"])

            # 6. Audio Mixing & Loudness Normalization (-16 LUFS)
            raw_master_audio = self.drafts_dir / f"{reel_slug}_audio_raw.wav"
            self.audio_mixer.concatenate_scenes(scene_audio_files, raw_master_audio)

            master_audio = self.drafts_dir / f"{reel_slug}_audio_master.wav"
            self.audio_mixer.normalize_loudness(raw_master_audio, master_audio, target_lufs=-16.0)

            # 7. Captions Generation (SRT, VTT, ASS, JSON)
            captions_res = self.caption_gen.generate_captions_from_storyboard(
                storyboard=storyboard,
                output_dir=self.drafts_dir,
                base_name=f"{reel_slug}_captions",
            )

            # 8. Visual Assets Preparation (Branded 1080x1920 Editorial Tech Cards)
            scene_visuals = []
            for i, sc in enumerate(scenes):
                sc_idx = i + 1
                visual_path = self.stock_provider.prepare_scene_visual(
                    scene=sc,
                    scene_index=sc_idx,
                    total_scenes=len(scenes),
                    reel_slug=reel_slug,
                )
                scene_visuals.append(visual_path)

            # 9. HyperFrames Composition & Visual Rendering
            comp_file = self.template_builder.build_reel_composition(
                storyboard=storyboard,
                scene_visuals=scene_visuals,
                reel_slug=reel_slug,
            )

            raw_video_path = self.drafts_dir / f"{reel_slug}_raw_visuals.mp4"
            self.hyperframes_runner.render_composition(
                output_path=raw_video_path,
                composition_rel_path=f"compositions/{comp_file.name}",
                fps=30,
                quality="looks",
            )

            # 10. Final FFmpeg Post-Processing (Muxing, Subtitle Burning, H.264/AAC Export)
            final_video_path = self.drafts_dir / f"{reel_slug}_final.mp4"
            self.ffmpeg_pipeline.compose_final_reel(
                video_input=raw_video_path,
                audio_input=master_audio,
                output_path=final_video_path,
                captions_ass=captions_res["ass"],
                burn_captions=True,
            )

            # 11. Technical Quality Assurance Inspection via FFprobe
            validation_report = self.video_validator.validate_reel(final_video_path)

            # 12. Submit for Human Review & Update Database
            self.approval_mgr.record_submission(prod_job_id)

            with self.db.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE production_jobs 
                    SET status = 'NEEDS_REVIEW', output_video_path = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (str(final_video_path), datetime.datetime.now().isoformat(), prod_job_id),
                )

            logger.info(f"Production SUCCESS for Reel #{prod_job_id}: {final_video_path.name}")

            return {
                "production_job_id": prod_job_id,
                "status": "NEEDS_REVIEW",
                "topic": topic["title"],
                "video_path": str(final_video_path),
                "duration": validation_report.get("duration", 0.0),
                "fps": validation_report.get("fps", 30),
                "dimensions": f"{validation_report.get('width', 1080)}x{validation_report.get('height', 1920)}",
                "validation": validation_report,
                "captions": {k: str(v) for k, v in captions_res.items()},
            }

        except Exception as e:
            logger.exception(f"Production FAILED for Reel #{prod_job_id}: {e}")
            with self.db.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE production_jobs 
                    SET status = 'FAILED', error_log = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (str(e), datetime.datetime.now().isoformat(), prod_job_id),
                )
            raise
