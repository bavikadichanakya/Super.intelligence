"""
SUPER.INTELLIGENCEEE — Phase 4.3.2B Multi-Engine Rendering Dispatcher
FFmpegAdapter: Handles video stem concatenation, audio mixing, broadcast loudness normalization (-16 LUFS),
safe-zone ASS subtitle burning, and final MP4 mastering.
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.universal_scene_contract import (
    CaptionSegment,
    RenderingEngine,
    UniversalSceneContract,
    VideoStoryboardContract,
)
from rendering.adapters.base_adapter import BaseEngineAdapter
from rendering.engine_errors import (
    AdapterPreflightError,
    ArtifactValidationError,
    EngineUnavailableError,
    RenderExecutionError,
    RenderTimeoutError,
)
from rendering.execution_context import ExecutionContext
from rendering.render_artifact import RenderArtifact
from rendering.resource_guard import RenderProcessTimeoutError, ResourceGuard

logger = logging.getLogger("super_intelligence.ffmpeg_adapter")


class FFmpegAdapter(BaseEngineAdapter):
    """
    Adapter for FFmpeg video processing, stem concatenation, and final mastering.
    Enforces strict -16 LUFS loudness normalization and vertical mobile safe margins.
    """

    def __init__(
        self,
        ffmpeg_bin: Optional[str] = None,
        ffprobe_bin: Optional[str] = None,
        resource_guard: Optional[ResourceGuard] = None,
    ):
        super().__init__(resource_guard=resource_guard)
        self.ffmpeg_bin = ffmpeg_bin or "ffmpeg"
        self.ffprobe_bin = ffprobe_bin or "ffprobe"
        self._cached_version: Optional[str] = None

    @property
    def engine_name(self) -> RenderingEngine:
        return RenderingEngine.FFMPEG

    def is_available(self) -> bool:
        """Verifies that ffmpeg and ffprobe are available."""
        try:
            r1 = subprocess.run([self.ffmpeg_bin, "-version"], capture_output=True, text=True, timeout=5)
            r2 = subprocess.run([self.ffprobe_bin, "-version"], capture_output=True, text=True, timeout=5)
            return r1.returncode == 0 and r2.returncode == 0
        except Exception:
            return False

    def get_version(self) -> str:
        """Returns the FFmpeg version string."""
        if self._cached_version:
            return self._cached_version
        try:
            res = subprocess.run([self.ffmpeg_bin, "-version"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                first_line = res.stdout.splitlines()[0] if res.stdout else "FFmpeg"
                self._cached_version = first_line.strip()
                return self._cached_version
        except Exception as e:
            logger.warning(f"Failed to query FFmpeg version: {e}")
        return "FFmpeg (version unknown)"

    def validate_scene(self, scene: UniversalSceneContract) -> bool:
        """Validates scene contract for FFmpeg processing."""
        if not self.is_available():
            raise EngineUnavailableError("FFmpeg or ffprobe executable is not available on PATH.")
        return True

    def prepare(self, scene: UniversalSceneContract, context: ExecutionContext) -> Dict[str, Any]:
        """
        Prepares a standalone FFmpeg synthetic stem if routed directly.
        """
        self.validate_scene(scene)
        w, h = scene.output_resolution
        duration = float(scene.actual_duration_seconds or scene.narration_duration_seconds or 5.0)
        target_output = context.get_output_stem_path(".mp4")

        return {
            "output_path": target_output,
            "width": w,
            "height": h,
            "duration": duration,
        }

    def render(self, scene: UniversalSceneContract, context: ExecutionContext) -> RenderArtifact:
        """
        Renders a standalone technical test / backdrop stem via FFmpeg lavfi filters.
        Strictly disallowed in production to prevent calibration patterns from entering masters.
        """
        if os.environ.get("ALLOW_FFMPEG_TESTSRC") != "true" and not getattr(context, "is_diagnostic", False):
            raise RenderExecutionError(
                "FFmpeg testsrc calibration pattern is strictly prohibited in production pipelines. "
                "Scenes must be rendered by NativeMotionEngine or Manim.",
                log_path=str(context.log_file),
            )

        prep = self.prepare(scene, context)
        w = prep["width"]
        h = prep["height"]
        duration = prep["duration"]
        target_output = prep["output_path"]

        # Procedural test card / technical grid
        cmd = [
            self.ffmpeg_bin, "-y",
            "-f", "lavfi",
            "-i", f"testsrc=size={w}x{h}:rate=30:duration={duration}",
            "-f", "lavfi",
            "-i", f"sine=frequency=440:duration={duration}",
            "-c:v", "libx264",
            "-preset", "fast",
            "-profile:v", "high",
            "-b:v", "4500k",
            "-maxrate", "6000k",
            "-bufsize", "8000k",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-ar", "48000",
            "-b:a", "192k",
            str(target_output),
        ]

        timeout = scene.timeout_seconds or 120.0
        start_time = time.time()
        try:
            result = self.guard.execute_isolated_render(
                command=cmd,
                cwd=context.workspace_root,
                timeout_seconds=timeout,
                log_file=context.log_file,
            )
        except RenderProcessTimeoutError as e:
            raise RenderTimeoutError(str(e), timeout_seconds=timeout)
        except Exception as e:
            raise RenderExecutionError(f"FFmpeg render process failed: {e}", log_path=str(context.log_file))

        if not result["success"]:
            raise RenderExecutionError(
                f"FFmpeg render exited with code {result['returncode']}",
                exit_code=result["returncode"],
                log_path=result.get("log_path", ""),
            )

        render_time = time.time() - start_time
        return self.verify_output(
            output_path=target_output,
            scene=scene,
            render_time_seconds=render_time,
            peak_ram_mb=result.get("peak_ram_mb", 0.0),
        )

    def generate_ass_subtitles(
        self,
        storyboard: VideoStoryboardContract,
        ass_path: Path,
        safe_margin_bottom: int = 360,
    ) -> Path:
        """
        Generates an Advanced SubStation Alpha (.ass) subtitle file enforcing collision-free
        placement and vertical mobile safe zones via SubtitleLayoutEngine.
        """
        from rendering.subtitle_layout import SubtitleLayoutEngine

        ass_path = Path(ass_path).resolve()
        ass_path.parent.mkdir(parents=True, exist_ok=True)
        layout_engine = SubtitleLayoutEngine(font_size=34, max_line_chars=36)

        header = f"""[Script Info]
Title: {storyboard.title}
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,34,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,60,60,{safe_margin_bottom},1
Style: TopBanner,Arial,32,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,8,60,60,1460,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

        events: List[str] = []
        cumulative_time = 0.0

        for scene in storyboard.scenes:
            dur = scene.actual_duration_seconds or scene.narration_duration_seconds or 5.0
            scene_start = cumulative_time

            protected_regs = getattr(scene, "protected_regions", None)
            if not protected_regs:
                try:
                    from rendering.native_motion_engine.components import get_scene_protected_regions
                    seq_num = getattr(scene, "sequence_number", None)
                    if seq_num is not None:
                        protected_regs = get_scene_protected_regions(seq_num)
                except Exception:
                    protected_regs = []

            if scene.narration_text:
                cues = layout_engine.plan_scene_cues(
                    scene_id=scene.scene_id,
                    narration_text=scene.narration_text,
                    start_time_sec=scene_start,
                    duration_sec=dur,
                    protected_regions=protected_regs,
                )
                for cue in cues:
                    s_str = self._format_ass_timestamp(cue.start_sec)
                    e_str = self._format_ass_timestamp(cue.end_sec)
                    style_name = "TopBanner" if cue.alignment == 8 else "Default"
                    events.append(f"Dialogue: 0,{s_str},{e_str},{style_name},,60,60,{cue.margin_v},,{cue.text}")
            elif scene.caption_segments:
                for seg in scene.caption_segments:
                    s_t = scene_start + seg.start_sec
                    e_t = scene_start + seg.end_sec
                    s_str = self._format_ass_timestamp(s_t)
                    e_str = self._format_ass_timestamp(e_t)
                    text_clean = seg.text.replace("\n", r"\N").strip()
                    events.append(f"Dialogue: 0,{s_str},{e_str},Default,,60,60,{safe_margin_bottom},,{text_clean}")

            cumulative_time += dur

        with open(ass_path, "w", encoding="utf-8") as f:
            f.write(header + "\n".join(events) + "\n")

        return ass_path

    @staticmethod
    def _format_ass_timestamp(seconds: float) -> str:
        """Formats seconds into ASS timestamp H:MM:SS.CC."""
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centisecs = int(round((seconds - int(seconds)) * 100))
        if centisecs >= 100:
            centisecs = 99
        return f"{hrs}:{mins:02d}:{secs:02d}.{centisecs:02d}"

    def assemble_storyboard(
        self,
        storyboard: VideoStoryboardContract,
        stem_artifacts: List[RenderArtifact],
        output_path: Path | str,
        audio_stem: Optional[Path | str] = None,
        subtitles_ass: Optional[Path | str] = None,
        burn_subtitles: bool = True,
        log_file: Optional[Path | str] = None,
        timeout_seconds: float = 180.0,
    ) -> RenderArtifact:
        """
        Concatenates scene stems, masters audio to -16 LUFS, burns ASS subtitles if requested,
        and produces the upload-ready master video.
        """
        output_file = Path(output_path).resolve()
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if not stem_artifacts:
            raise ArtifactValidationError("Cannot assemble storyboard: zero stem artifacts provided.")

        scratch_dir = Path("A:/SUPER.INTELLIGENCEEE/.temp/assemble").resolve()
        scratch_dir.mkdir(parents=True, exist_ok=True)

        # 1. Concat demuxer list
        concat_file = scratch_dir / f"concat_{storyboard.video_id}.txt"
        with open(concat_file, "w", encoding="utf-8") as f:
            for art in stem_artifacts:
                posix_path = art.output_path.as_posix()
                f.write(f"file '{posix_path}'\n")

        # 2. Subtitles
        if burn_subtitles:
            if subtitles_ass is None:
                subtitles_ass = scratch_dir / f"subs_{storyboard.video_id}.ass"
                self.generate_ass_subtitles(storyboard, subtitles_ass)

            subtitles_ass_path = Path(subtitles_ass).resolve()
            ass_escaped = str(subtitles_ass_path).replace("\\", "/").replace(":", "\\:")
            video_filter = f"[0:v]subtitles='{ass_escaped}'[vout]"
        else:
            video_filter = "[0:v]null[vout]"

        # 3. Audio handling
        total_duration = sum(art.duration_seconds for art in stem_artifacts)
        audio_input_args: List[str] = []

        if audio_stem and Path(audio_stem).is_file():
            audio_input_args = ["-i", str(Path(audio_stem).resolve())]
            audio_filter = "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[aout]"
        else:
            # Synthetic background hum / tone if no external audio provided
            audio_input_args = ["-f", "lavfi", "-i", f"sine=frequency=220:duration={total_duration:.2f}"]
            audio_filter = "[1:a]volume=0.3,loudnorm=I=-16:TP=-1.5:LRA=11[aout]"

        filter_complex = f"{video_filter};{audio_filter}"

        cmd = [
            self.ffmpeg_bin, "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_file),
            *audio_input_args,
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-profile:v", "high",
            "-b:v", "4500k",
            "-maxrate", "6000k",
            "-bufsize", "8000k",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-ar", "48000",
            "-b:a", "192k",
            "-shortest",
            str(output_file),
        ]

        logger.info(f"Assembling storyboard '{storyboard.video_id}' ({len(stem_artifacts)} stems) with FFmpeg...")
        start_time = time.time()

        try:
            result = self.guard.execute_isolated_render(
                command=cmd,
                cwd="A:/SUPER.INTELLIGENCEEE",
                timeout_seconds=timeout_seconds,
                log_file=log_file or (scratch_dir / f"assemble_{storyboard.video_id}.log"),
            )
        except RenderProcessTimeoutError as e:
            raise RenderTimeoutError(str(e), timeout_seconds=timeout_seconds)
        except Exception as e:
            raise RenderExecutionError(f"FFmpeg assembly failed: {e}", log_path=str(log_file or ""))

        if not result["success"]:
            raise RenderExecutionError(
                f"FFmpeg assembly exited with code {result['returncode']}",
                exit_code=result["returncode"],
                log_path=result.get("log_path", ""),
            )

        render_time = time.time() - start_time
        logger.info(f"Master video assembled successfully in {render_time:.2f}s: {output_file}")

        target_w = storyboard.scenes[0].output_resolution[0] if storyboard.scenes else 1080
        target_h = storyboard.scenes[0].output_resolution[1] if storyboard.scenes else 1920

        return RenderArtifact.from_output_file(
            scene_id=f"master_{storyboard.video_id}",
            engine_name="ffmpeg",
            output_path=output_file,
            render_time_seconds=render_time,
            peak_ram_mb=result.get("peak_ram_mb", 0.0),
            expected_width=target_w,
            expected_height=target_h,
            expected_fps=30.0,
            expected_duration_seconds=total_duration,
            duration_tolerance_sec=2.0,
        )
