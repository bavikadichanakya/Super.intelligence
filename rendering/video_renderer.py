import os
import time
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from core.config_manager import get_config
from core.database import get_db
from core.logger import get_logger, get_system_resources
from core.task_manager import TaskManager
from media.image_manager import ImageManager
from media.video_manager import VideoManager
from media.asset_manager import AssetManager
from audio.tts_engine import TTSEngine
from audio.audio_processor import AudioProcessor
from audio.subtitle_generator import SubtitleGenerator
from rendering.transitions import Transitions
from rendering.motion_graphics import MotionGraphics
from rendering.quality_checker import QualityChecker
from rendering.ffmpeg_manager import FFmpegManager
from intelligence.scene_planner import ScenePlanner
from intelligence.caption_generator import CaptionGenerator

logger = get_logger("VideoRenderer")

class VideoRenderer:
    """
    Core production rendering engine for SUPER.INTELLIGENCEEE.
    Renders professional 1080x1920 30FPS H.264 vertical Instagram Reels sequentially
    with strict zero-budget operation and low RAM bounds (<8GB RAM target).
    """

    def __init__(self):
        self.config = get_config()
        self.db = get_db()
        self.image_manager = ImageManager()
        self.tts_engine = TTSEngine()
        self.asset_manager = AssetManager()
        self.task_manager = TaskManager()

        self.reels_dir = self.config.resolve_path(Path("output") / "reels")
        self.covers_dir = self.config.resolve_path(Path("output") / "covers")
        self.temp_dir = self.config.resolve_path(Path("output") / "temp")

        self.reels_dir.mkdir(parents=True, exist_ok=True)
        self.covers_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _slugify(text: str) -> str:
        s = re.sub(r'[^a-zA-Z0-9_\s-]', '', text).strip().lower()
        return re.sub(r'[-\s]+', '_', s)[:36]

    def render_reel(
        self,
        script_or_id: Any,
        job_id: Optional[int] = None,
        progress_callback: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Orchestrates sequential 7-scene video rendering:
        1. Resolve script data
        2. Audio generation & timing
        3. Editorial card generation
        4. Ken Burns motion clips
        5. Visual & audio assembly
        6. Subtitle & progress bar composite
        7. Cover image creation
        8. FFprobe quality verification
        9. Database registration
        """
        start_time = time.time()
        res_start = get_system_resources()
        logger.info(f"Initiating Reel render (Initial Process RAM: {res_start['ram_process_mb']} MB, System RAM: {res_start['ram_system_percent']}%)")

        if progress_callback:
            progress_callback(5, "Resolving script and initializing production job...")

        # 1. Resolve Script
        script_data = None
        script_id = None
        if isinstance(script_or_id, int):
            script_id = script_or_id
            script_data = self.db.get_script_by_id(script_id)
            if not script_data:
                raise ValueError(f"Script ID {script_id} not found in database.")
        elif isinstance(script_or_id, dict):
            script_data = script_or_id
            script_id = script_data.get("id")
        else:
            raise TypeError("script_or_id must be a script ID (int) or script dictionary.")

        title = script_data.get("title", "AI Frontier Milestone")
        slug = self._slugify(title)

        # 2. Database Job Record
        if not job_id:
            job_id = self.db.create_production_job(script_id=script_id, title=title)
        self.db.update_production_job(job_id, {"status": "RENDERING"})

        # Working directory for this job
        job_work_dir = self.temp_dir / f"job_{job_id}_{slug}"
        job_work_dir.mkdir(parents=True, exist_ok=True)

        try:
            # 3. Resolve 7 Scenes
            scenes = []
            script_json = script_data.get("script_json") or {}
            if isinstance(script_json, dict) and script_json.get("scenes") and len(script_json["scenes"]) == 7:
                scenes = script_json["scenes"]
            elif script_data.get("scenes") and len(script_data["scenes"]) == 7:
                scenes = script_data["scenes"]
            else:
                scenes = ScenePlanner.plan_scenes(script_data)

            total_scenes = len(scenes)
            logger.info(f"Job {job_id}: Processing {total_scenes} storyboard scenes for '{title}'")

            # 4. Generate Audio & Exact Scene Durations
            if progress_callback:
                progress_callback(15, "Synthesizing scene narrations and computing timing...")

            scene_audios = []
            scene_clips = []
            motion_styles = ["zoom_in", "pan_left", "zoom_in", "pan_right", "zoom_in", "pan_left", "zoom_in"]

            for idx, scene in enumerate(scenes):
                scene_num = idx + 1
                narration = scene.get("narration", "").strip()
                if not narration:
                    narration = f"Section {scene_num} overview."

                audio_file = job_work_dir / f"scene_{scene_num:02d}.mp3"
                tts_ok, engine_used = self.tts_engine.generate_speech(narration, str(audio_file))
                
                # Check for wav fallback if pyttsx3 used
                if not audio_file.exists():
                    wav_candidate = audio_file.with_suffix(".wav")
                    if wav_candidate.exists():
                        audio_file = wav_candidate

                audio_info = AudioProcessor.get_audio_info(str(audio_file))
                audio_dur = audio_info["duration"]
                # Give 0.35s natural breathing room after sentence
                scene_duration = max(3.4, round(audio_dur + 0.35, 2))
                scene["duration"] = scene_duration
                scene_audios.append(str(audio_file))

            # 5. Concatenate Audio into Master Audio Track
            if progress_callback:
                progress_callback(30, "Assembling master voiceover and normalizing audio...")

            raw_master_audio = job_work_dir / "master_audio_raw.mp3"
            audio_concat_txt = job_work_dir / "audio_concat.txt"
            Transitions.create_concat_file(scene_audios, str(audio_concat_txt))

            cmd_audio = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(audio_concat_txt),
                "-c:a", "libmp3lame",
                "-b:a", "192k",
                str(raw_master_audio)
            ]
            FFmpegManager.run_command(cmd_audio)

            # Loudness normalization to -16 LUFS
            master_audio = job_work_dir / "master_audio_norm.mp3"
            norm_ok = AudioProcessor.normalize_loudness(str(raw_master_audio), str(master_audio), target_lufs=-16.0)
            if not norm_ok or not master_audio.exists():
                master_audio = raw_master_audio

            master_info = AudioProcessor.get_audio_info(str(master_audio))
            total_audio_duration = master_info["duration"]
            logger.info(f"Master audio track generated: {total_audio_duration:.2f}s")

            # 6. Render Editorial Graphic Cards & Motion Clips
            for idx, scene in enumerate(scenes):
                scene_num = idx + 1
                if progress_callback:
                    pct = int(35 + (idx / total_scenes) * 35)
                    progress_callback(pct, f"Rendering Scene {scene_num}/{total_scenes} ({scene.get('name', 'Scene')})...")

                # A. Render Graphic Card
                card_png = job_work_dir / f"scene_{scene_num:02d}_card.png"
                self.image_manager.create_scene_card(scene, str(card_png))
                
                # Register in AssetManager with Editorial Generated license
                self.asset_manager.register_asset(
                    file_path=str(card_png),
                    asset_type="image",
                    license_type="Editorial Generated",
                    creator="SUPER.INTELLIGENCEEE",
                    source_url=script_data.get("source_url", "")
                )

                # B. Render Motion Clip (Ken Burns)
                clip_mp4 = job_work_dir / f"scene_{scene_num:02d}_clip.mp4"
                m_style = motion_styles[idx % len(motion_styles)]
                dur = scene.get("duration", 4.0)

                v_ok = VideoManager.create_motion_clip(
                    image_path=str(card_png),
                    output_clip_path=str(clip_mp4),
                    duration=dur,
                    motion_style=m_style
                )
                if not v_ok or not clip_mp4.exists():
                    raise RuntimeError(f"Failed to render video clip for Scene {scene_num}")

                scene_clips.append(str(clip_mp4))

            # 7. Concatenate Scene Video Tracks
            if progress_callback:
                progress_callback(75, "Joining visual scenes into unified sequence...")

            visual_concat_txt = job_work_dir / "visual_concat.txt"
            Transitions.create_concat_file(scene_clips, str(visual_concat_txt))

            merged_visual_mp4 = job_work_dir / "visual_merged.mp4"
            cmd_concat_v = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(visual_concat_txt),
                "-c:v", "copy",
                str(merged_visual_mp4)
            ]
            v_concat_ok, _ = FFmpegManager.run_command(cmd_concat_v)
            if not v_concat_ok or not merged_visual_mp4.exists():
                raise RuntimeError("Failed to concatenate scene video clips.")

            # 8. Generate Mobile Subtitles (SRT)
            if progress_callback:
                progress_callback(80, "Generating timed mobile subtitles...")

            srt_path = job_work_dir / f"{slug}_subtitles.srt"
            SubtitleGenerator.generate_srt_from_scenes(scenes, str(srt_path))

            # 9. Final Composite Pass: Visual + Audio + Progress Bar + Subtitles
            if progress_callback:
                progress_callback(85, "Executing final composite: subtitles, progress bar, audio sync...")

            final_video_name = f"reel_{job_id}_{slug}.mp4"
            final_video_path = self.reels_dir / final_video_name

            # Subtitles filter string: relative forward-slash path prevents Windows colon delimiter conflicts
            rel_srt = str(srt_path.resolve()).replace("\\", "/")
            # Use forward slashes relative to root or properly escaped path
            # In our earlier verified test: subtitles='path':force_style='...' works with forward slashes
            clean_srt = str(srt_path.relative_to(self.config.base_dir)).replace("\\", "/") if srt_path.is_relative_to(self.config.base_dir) else str(srt_path).replace("\\", "/")

            total_dur = max(total_audio_duration, sum(s.get("duration", 4.0) for s in scenes))
            prog_filter = MotionGraphics.get_progress_bar_filter(total_dur, height=12, color="0x06B6D4@1.0")
            
            # Combine filters
            # Style: bold white sans text with high contrast black outline & subtle backing
            sub_style = "FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H80000000,BorderStyle=4,Outline=1,Alignment=2,MarginV=260"
            filter_complex = f"subtitles={clean_srt}:force_style='{sub_style}',{prog_filter}"

            cmd_final = [
                "ffmpeg", "-y",
                "-i", str(merged_visual_mp4),
                "-i", str(master_audio),
                "-vf", filter_complex,
                "-c:v", "libx264",
                "-preset", self.config.get("rendering.ffmpeg_preset", "veryfast"),
                "-crf", str(self.config.get("rendering.crf", 22)),
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                str(final_video_path)
            ]

            comp_ok, comp_err = FFmpegManager.run_command(cmd_final, timeout_sec=400)
            if not comp_ok or not final_video_path.exists():
                logger.warning(f"Composite with burned-in subtitles failed ({comp_err[:200]}), attempting stream fallback...")
                # Fallback: mux audio and video directly with progress bar
                cmd_fallback = [
                    "ffmpeg", "-y",
                    "-i", str(merged_visual_mp4),
                    "-i", str(master_audio),
                    "-vf", prog_filter,
                    "-c:v", "libx264",
                    "-preset", "veryfast",
                    "-crf", "22",
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-shortest",
                    str(final_video_path)
                ]
                f_ok, f_err = FFmpegManager.run_command(cmd_fallback, timeout_sec=300)
                if not f_ok or not final_video_path.exists():
                    raise RuntimeError(f"Final video composite failed: {f_err}")

            # 10. Generate High-Converting Instagram Reel Cover Image
            if progress_callback:
                progress_callback(92, "Designing 1080x1920 Instagram cover image...")

            cover_name = f"cover_{job_id}_{slug}.jpg"
            cover_path = self.covers_dir / cover_name
            category = script_data.get("content_style") or script_data.get("category") or "AI Milestone"
            self.image_manager.create_reel_cover(title, category, str(cover_path))

            # 11. FFprobe Quality Verification
            if progress_callback:
                progress_callback(95, "Validating output against Instagram technical specifications...")

            is_valid, q_msg, meta = QualityChecker.verify_video(str(final_video_path))
            render_elapsed = round(time.time() - start_time, 2)
            file_size_mb = meta.get("file_size_mb", round(final_video_path.stat().st_size / (1024 * 1024), 2))

            # 12. Update Database Production Job
            self.db.update_production_job(job_id, {
                "status": "COMPLETED",
                "output_video_path": str(final_video_path),
                "cover_image_path": str(cover_path),
                "audio_path": str(master_audio),
                "subtitle_path": str(srt_path),
                "render_time_seconds": render_elapsed,
                "file_size_mb": file_size_mb,
                "completed_at": datetime.utcnow().isoformat()
            })

            # 13. Auto-Add to Publishing Queue
            pub_data = CaptionGenerator.generate_caption(script_data)
            self.db.add_to_publishing_queue({
                "job_id": job_id,
                "title": title,
                "caption": pub_data["caption"],
                "hashtags": pub_data["hashtags"],
                "scheduled_for": datetime.utcnow().strftime("%Y-%m-%d 11:30:00"),
                "status": "QUEUED",
                "export_path": str(final_video_path)
            })

            # 14. Optional Cleanup of Intermediate Scene Clips
            if self.config.get("rendering.cleanup_temp_files", True):
                try:
                    # Keep only final srt and audio in temp, remove frame clips
                    for clip in scene_clips:
                        Path(clip).unlink(missing_ok=True)
                    for c_img in job_work_dir.glob("*.png"):
                        c_img.unlink(missing_ok=True)
                    merged_visual_mp4.unlink(missing_ok=True)
                    logger.debug(f"Cleaned temporary intermediate clips for Job {job_id}")
                except Exception as e:
                    logger.warning(f"Cleanup non-fatal error: {e}")

            res_end = get_system_resources()
            logger.info(
                f"Production Job {job_id} successfully COMPLETED in {render_elapsed}s. "
                f"File: {final_video_name} ({file_size_mb} MB, {meta.get('duration_seconds', 0):.1f}s, "
                f"Peak RAM: {res_end['ram_process_mb']} MB)"
            )

            if progress_callback:
                progress_callback(100, f"Render complete: {final_video_name} ({file_size_mb} MB)")

            return {
                "success": True,
                "job_id": job_id,
                "title": title,
                "video_path": str(final_video_path),
                "cover_path": str(cover_path),
                "subtitle_path": str(srt_path),
                "duration_seconds": meta.get("duration_seconds", 0.0),
                "file_size_mb": file_size_mb,
                "render_time_seconds": render_elapsed,
                "quality_verified": is_valid,
                "quality_message": q_msg
            }

        except Exception as e:
            err_msg = str(e)
            logger.error(f"Render failed for Job {job_id}: {err_msg}", exc_info=True)
            self.db.update_production_job(job_id, {
                "status": "FAILED",
                "error_message": err_msg
            })
            if progress_callback:
                progress_callback(100, f"Render failed: {err_msg}")
            raise

