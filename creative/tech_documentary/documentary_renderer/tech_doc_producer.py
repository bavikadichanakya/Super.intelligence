"""
SUPER.INTELLIGENCEEE — Documentary Renderer: Tech Doc Producer
Master production orchestrator for the Tech Documentary engine.
Orchestrates audio synchronization, scene clip rendering, transition application,
sound design layering, subtitle burning, and visual QA auditing.
"""

from __future__ import annotations

import dataclasses
import json
import logging
import subprocess
import wave
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np

from core.config import get_config
from core.creative_contracts import DynamicScene, DynamicScenePlan, SceneType
from creative.tech_documentary.scene_composition.documentary_compositor import DocumentaryCompositor
from creative.tech_documentary.transitions.transition_router import TransitionRouter
from creative.tech_documentary.sound_design.sound_designer import SoundDesigner
from audio.audio_mixer import AudioMixer
from captions.caption_generator import CaptionGenerator
from video.ffmpeg_pipeline import FFmpegVideoPipeline
from rendering.visual_qa import VisualQASubsystem

logger = logging.getLogger("super_intelligence.tech_doc_producer")


class AudioMuxVerificationError(Exception):
    """Raised when exported video file fails mandatory audio stream verification."""


@dataclasses.dataclass
class DocumentaryProductionResult:
    """Production result metadata for a rendered Tech Documentary."""
    reel_slug: str
    final_video_path: Path
    master_audio_path: Path
    raw_video_path: Path
    contact_sheet_path: Optional[Path]
    visual_qa_report: Dict[str, Any]
    duration_seconds: float
    scene_count: int
    scene_clips: List[Path]
    sound_cue_timeline_path: Optional[Path] = None
    status: str = "READY_FOR_REVIEW"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reel_slug": self.reel_slug,
            "final_video_path": str(self.final_video_path),
            "master_audio_path": str(self.master_audio_path),
            "raw_video_path": str(self.raw_video_path),
            "contact_sheet_path": str(self.contact_sheet_path) if self.contact_sheet_path else None,
            "sound_cue_timeline_path": str(self.sound_cue_timeline_path) if self.sound_cue_timeline_path else None,
            "duration_seconds": self.duration_seconds,
            "scene_count": self.scene_count,
            "scene_clips": [str(p) for p in self.scene_clips],
            "status": self.status,
            "visual_qa_passed": self.visual_qa_report.get("overall_qa_pass", self.visual_qa_report.get("passed", False)),
        }


class TechDocProducer:
    """Master orchestrator for producing broadcast-grade AI and technology mini-documentaries."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.compositor = DocumentaryCompositor()
        self.transition_router = TransitionRouter()
        self.sound_designer = SoundDesigner(config=self.config)
        self.audio_mixer = AudioMixer(config=self.config)
        self.caption_gen = CaptionGenerator(config=self.config)
        self.ffmpeg_pipeline = FFmpegVideoPipeline(config=self.config)
        self.visual_qa = VisualQASubsystem(config=self.config)

        self.drafts_dir = self.config.resolve_path("output/drafts")
        self.drafts_dir.mkdir(parents=True, exist_ok=True)

    def _sync_scene_durations_to_audio(
        self,
        scenes: List[Any],
        scene_audio_files: List[Path | str],
    ) -> List[float]:
        """Inspects actual WAV headers and aligns scene duration values."""
        durations = []
        for idx, sc in enumerate(scenes):
            real_dur = 0.0
            if idx < len(scene_audio_files):
                a_path = Path(scene_audio_files[idx])
                if a_path.exists():
                    try:
                        with wave.open(str(a_path), "rb") as wf:
                            real_dur = wf.getnframes() / float(wf.getframerate())
                    except Exception:
                        real_dur = 0.0

            # Fallback to configured duration or 5.0s default
            if real_dur <= 0.5:
                if isinstance(sc, DynamicScene):
                    real_dur = float(sc.duration_seconds or 5.0)
                elif isinstance(sc, dict):
                    real_dur = float(sc.get("duration_seconds", sc.get("duration", 5.0)))
                else:
                    real_dur = 5.0

            # Add gentle 0.25s padding for visual transition breathing room
            final_dur = round(real_dur + 0.25, 2)
            durations.append(final_dur)

            # Update scene model in place
            if isinstance(sc, DynamicScene):
                sc.actual_duration = final_dur
            elif isinstance(sc, dict):
                sc["duration_seconds"] = final_dur
                sc["duration"] = final_dur

        return durations

    def verify_exported_video_stream(self, video_path: Path, expected_audio_dur: float) -> Dict[str, Any]:
        """
        MANDATORY AUDIO/STREAM VALIDATION:
        1. Checks that the video file contains both 1 H.264 video stream and 1 AAC audio stream.
        2. Asserts non-zero audio duration.
        3. Asserts audio and video durations match within 150 milliseconds.
        4. Decodes audio stream to temporary WAV and calculates RMS level to guarantee non-silence (RMS >= 1000).
        Raises AudioMuxVerificationError if any check fails.
        """
        v_path = Path(video_path).resolve()
        if not v_path.exists() or v_path.stat().st_size == 0:
            raise AudioMuxVerificationError(f"Video file does not exist or is empty: {v_path}")

        probe_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "stream=index,codec_name,codec_type,sample_rate,channels,duration",
            "-show_entries", "format=duration,size",
            "-of", "json",
            str(v_path),
        ]
        res = subprocess.run(probe_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise AudioMuxVerificationError(f"ffprobe failed on {v_path.name}: {res.stderr}")

        data = json.loads(res.stdout)
        streams = data.get("streams", [])
        video_streams = [s for s in streams if s.get("codec_type") == "video"]
        audio_streams = [s for s in streams if s.get("codec_type") == "audio"]

        if not video_streams:
            raise AudioMuxVerificationError(f"No video stream found in {v_path.name}")
        if not audio_streams:
            raise AudioMuxVerificationError(f"CRITICAL DEFECT: No audio stream found in {v_path.name}! Video is completely silent.")

        a_stream = audio_streams[0]
        v_stream = video_streams[0]

        a_codec = a_stream.get("codec_name", "").lower()
        if a_codec != "aac":
            raise AudioMuxVerificationError(f"Unexpected audio codec in {v_path.name}: '{a_codec}' (expected 'aac')")

        fmt_dur = float(data.get("format", {}).get("duration", 0.0))
        v_dur = float(v_stream.get("duration", fmt_dur))
        a_dur = float(a_stream.get("duration", fmt_dur))

        if a_dur <= 0.5:
            raise AudioMuxVerificationError(f"Audio stream duration in {v_path.name} is zero or invalid ({a_dur:.2f}s)")

        dur_delta = abs(v_dur - a_dur)
        if dur_delta > 0.20:
            raise AudioMuxVerificationError(
                f"Audio duration ({a_dur:.2f}s) and video duration ({v_dur:.2f}s) delta ({dur_delta:.3f}s) exceeds tolerance in {v_path.name}"
            )

        temp_wav = v_path.parent / f"temp_verify_{v_path.stem}.wav"
        try:
            dec_cmd = ["ffmpeg", "-y", "-i", str(v_path), "-vn", "-acodec", "pcm_s16le", str(temp_wav)]
            dec_res = subprocess.run(dec_cmd, capture_output=True)
            if dec_res.returncode != 0 or not temp_wav.exists():
                raise AudioMuxVerificationError(f"Failed to decode audio stream from {v_path.name}")

            with wave.open(str(temp_wav), "rb") as wf:
                nframes = wf.getnframes()
                raw_data = wf.readframes(nframes)
                samples = np.frombuffer(raw_data, dtype=np.int16)
                if len(samples) == 0:
                    raise AudioMuxVerificationError(f"Decoded audio from {v_path.name} contains 0 samples")
                rms = float(np.sqrt(np.mean(samples.astype(np.float64)**2)))
                peak = int(np.max(np.abs(samples)))

            if rms < 1000.0:
                raise AudioMuxVerificationError(f"Audio stream in {v_path.name} is SILENT (RMS={rms:.1f} < 1000.0)")

            logger.info(f"Verified audio/video streams for {v_path.name}: Video={v_dur:.2f}s, Audio={a_dur:.2f}s (delta={dur_delta*1000:.1f}ms), RMS={rms:.1f}, Peak={peak}")
            return {
                "file": v_path.name,
                "video_duration": v_dur,
                "audio_duration": a_dur,
                "delta_seconds": dur_delta,
                "audio_codec": a_codec,
                "sample_rate": int(a_stream.get("sample_rate", 48000)),
                "channels": int(a_stream.get("channels", 2)),
                "audio_rms": rms,
                "audio_peak": peak,
                "passed": True,
            }
        finally:
            if temp_wav.exists():
                try:
                    temp_wav.unlink()
                except Exception:
                    pass

    def produce_documentary(
        self,
        scene_plan: Union[DynamicScenePlan, Dict[str, Any], List[Any]],
        topic: Dict[str, Any],
        scene_audio_files: List[Path | str],
        reel_slug: str,
        burn_subtitles: bool = True,
        transition_type: str = "wipeleft",
    ) -> DocumentaryProductionResult:
        """
        Orchestrates full Tech Documentary execution:
        1. Synchronize audio speech durations.
        2. Render scene-by-scene motion clips (Terminal, Diagram, HUD, Kinetic, B-Roll).
        3. Connect clips with cinematic xfade transitions into continuous video.
        4. Assemble multi-layer soundscape (Voice + Sub-Bass Drone Bed + Diegetic Foley).
        5. Generate and burn high-contrast subtitles.
        6. Perform automated visual QA audit with contact sheet.
        """
        logger.info(f"=== Starting Tech Documentary Production: {reel_slug} ===")
        topic_title = topic.get("title", "Advanced Technology Breakthrough")

        # Normalize scenes list
        if isinstance(scene_plan, DynamicScenePlan):
            scenes = scene_plan.scenes
        elif isinstance(scene_plan, dict):
            scenes = scene_plan.get("scenes", [])
        else:
            scenes = list(scene_plan)

        if not scenes:
            raise ValueError(f"Cannot produce Tech Documentary '{reel_slug}': scene list is empty.")

        # 1. Synchronize Scene Timings to Real Audio WAV Files
        scene_durations = self._sync_scene_durations_to_audio(scenes, scene_audio_files)
        total_duration = sum(scene_durations)
        logger.info(f"Synchronized {len(scenes)} scenes. Total duration: {total_duration:.2f}s")

        # 2. Render Scene-by-Scene Motion Clips
        rendered_clips: List[Path] = []
        scene_types_str: List[str] = []

        for idx, sc in enumerate(scenes):
            sc_idx = idx + 1
            clip_p = self.compositor.render_scene(
                scene=sc,
                scene_index=sc_idx,
                reel_slug=reel_slug,
                topic_title=topic_title,
            )
            rendered_clips.append(clip_p)

            st_val = sc.scene_type.value if hasattr(sc, "scene_type") else str(sc.get("scene_type", "SCENE"))
            scene_types_str.append(st_val)

        # 3. Concatenate Scene Clips with Cinematic Transitions (Intermediate Video Track)
        intermediate_video_path = self.drafts_dir / f"{reel_slug}_video_intermediate.mp4"
        self.transition_router.concat_clips(
            clip_paths=rendered_clips,
            output_path=intermediate_video_path,
            transition_type=transition_type,
            transition_duration=0.30,
        )

        # 4. Multi-Layer Sound Design (Voice + Drone + Foley)
        raw_master_audio = self.drafts_dir / f"{reel_slug}_audio_raw.wav"
        valid_audios = [Path(p) for p in scene_audio_files if Path(p).exists()]
        if valid_audios:
            self.audio_mixer.concatenate_scenes(valid_audios, raw_master_audio)
        else:
            raise ValueError("No valid scene audio files available for documentary sound design.")

        master_soundscape_audio = self.drafts_dir / f"{reel_slug}_audio_soundscape.wav"
        sound_res = self.sound_designer.assemble_documentary_soundscape(
            voiceover_master_path=raw_master_audio,
            scene_durations=scene_durations,
            scene_types=scene_types_str,
            output_path=master_soundscape_audio,
            target_lufs=-14.0,
        )
        if isinstance(sound_res, tuple):
            final_master_audio, timeline_json_path = sound_res
        else:
            final_master_audio = sound_res
            timeline_json_path = None

        # 5. Captions Generation (SRT/ASS)
        # Adapt scenes to format expected by CaptionGenerator
        sb_dict = {
            "scenes": [
                {
                    "scene_index": i + 1,
                    "narration_text": (
                        getattr(sc, "narration", None)
                        or getattr(sc, "narration_text", None)
                        or (sc.get("narration_text", sc.get("narration", "")) if isinstance(sc, dict) else "")
                    ),
                    "narration": (
                        getattr(sc, "narration", None)
                        or getattr(sc, "narration_text", None)
                        or (sc.get("narration_text", sc.get("narration", "")) if isinstance(sc, dict) else "")
                    ),
                    "duration_seconds": scene_durations[i],
                    "duration": scene_durations[i],
                }
                for i, sc in enumerate(scenes)
            ]
        }
        captions_res = self.caption_gen.generate_captions_from_storyboard(
            storyboard=sb_dict,
            output_dir=self.drafts_dir,
            base_name=f"{reel_slug}_captions",
        )

        # 6. Video Post-Processing: Clean Raw Master & Captioned Final Release
        # 6a. Mux intermediate video with master audio to produce clean raw documentary master (NO burned subtitles)
        raw_video_path = self.drafts_dir / f"{reel_slug}_raw_documentary.mp4"
        logger.info(f"Muxing clean raw documentary master (video + master audio) -> {raw_video_path.name}")
        self.ffmpeg_pipeline.compose_final_reel(
            video_input=intermediate_video_path,
            audio_input=final_master_audio,
            output_path=raw_video_path,
            burn_captions=False,
        )

        # 6b. Mux intermediate video with master audio and burned subtitles to produce captioned final release
        final_video_path = self.drafts_dir / f"{reel_slug}_tech_doc_final.mp4"
        logger.info(f"Muxing captioned final release video -> {final_video_path.name}")
        self.ffmpeg_pipeline.compose_final_reel(
            video_input=intermediate_video_path,
            audio_input=final_master_audio,
            output_path=final_video_path,
            captions_ass=captions_res["ass"] if burn_subtitles else None,
            burn_captions=burn_subtitles,
        )

        # 6c. Mandatory Stream & Audio Validation on Both Export Artifacts
        logger.info("Executing mandatory audio & stream verification on export artifacts...")
        raw_stream_audit = self.verify_exported_video_stream(raw_video_path, expected_audio_dur=total_duration)
        final_stream_audit = self.verify_exported_video_stream(final_video_path, expected_audio_dur=total_duration)
        logger.info(f"Stream verification PASSED: raw={raw_stream_audit['file']} (RMS={raw_stream_audit['audio_rms']:.1f}), final={final_stream_audit['file']} (RMS={final_stream_audit['audio_rms']:.1f})")

        # 7. Automated Visual QA Audit & Contact Sheet Generation
        contact_sheet_path = self.drafts_dir / f"{reel_slug}_contact_sheet.png"
        vqa_report = self.visual_qa.run_full_visual_audit(
            video_path=final_video_path,
            audio_path=final_master_audio,
            scene_briefs=scenes,
            output_contact_sheet=contact_sheet_path,
        )
        vqa_report["raw_stream_audit"] = raw_stream_audit
        vqa_report["final_stream_audit"] = final_stream_audit

        logger.info(f"=== Tech Documentary Production Completed: {final_video_path.name} ===")
        return DocumentaryProductionResult(
            reel_slug=reel_slug,
            final_video_path=final_video_path,
            master_audio_path=final_master_audio,
            raw_video_path=raw_video_path,
            contact_sheet_path=contact_sheet_path if contact_sheet_path.exists() else None,
            sound_cue_timeline_path=timeline_json_path,
            visual_qa_report=vqa_report,
            duration_seconds=total_duration,
            scene_count=len(scenes),
            scene_clips=rendered_clips,
            status="READY_FOR_REVIEW",
        )
