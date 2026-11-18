"""
SUPER.INTELLIGENCEEE — HyperFrames Runner Module
Executes official HyperFrames CLI renders with memory-safe flags, robust error handling,
and automated FFmpeg slideshow fallback.
"""

from __future__ import annotations

import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import get_config

logger = logging.getLogger("super_intelligence.hyperframes_runner")


class HyperFramesRunnerError(Exception):
    """Raised when video rendering fails."""


class HyperFramesRunner:
    """Wrapper for HyperFrames CLI rendering with memory-safe profiles for 8GB RAM systems."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.renderer_dir = self.config.resolve_path("renderer")
        self.ffmpeg_cmd = "ffmpeg"

    def render_composition(
        self,
        output_path: Path | str,
        composition_rel_path: Optional[str] = None,
        fps: int = 30,
        quality: str = "looks",
        timeout_seconds: int = 300,
        scene_visuals: Optional[List[Path]] = None,
        scene_durations: Optional[List[float]] = None,
    ) -> Path:
        """
        Executes `npx hyperframes render` using official flags.
        Falls back to FFmpeg native visual rendering if Node/Puppeteer fails.
        """
        out_path = Path(output_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # Create local temp directory on Drive A: (11+ GB free)
        temp_dir = self.renderer_dir.parent / ".temp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Official HyperFrames CLI render command
        cmd = [
            "npx", "hyperframes", "render",
            ".",
            "-o", str(out_path),
            "-f", str(fps),
            "-q", quality,
            "--low-memory-mode",
            "--format", "mp4",
            "--frames-cache-dir", str(temp_dir.resolve()),
        ]

        if composition_rel_path:
            cmd.extend(["-c", composition_rel_path])

        logger.info(f"Launching HyperFrames render: {' '.join(cmd)}")
        start_time = time.time()

        try:
            # Run in renderer directory with low-memory env vars and relocated temp
            env = dict(os.environ)
            env["PRODUCER_LOW_MEMORY_MODE"] = "true"
            env["NODE_OPTIONS"] = "--max-old-space-size=4096"
            env["TEMP"] = str(temp_dir.resolve())
            env["TMP"] = str(temp_dir.resolve())
            env["HYPERFRAMES_EXTRACT_CACHE_DIR"] = str(temp_dir.resolve())

            res = subprocess.run(
                cmd,
                cwd=str(self.renderer_dir),
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env=env,
                shell=True,  # Required for npx on Windows
            )

            elapsed = time.time() - start_time

            if res.returncode == 0 and out_path.exists() and out_path.stat().st_size > 10000:
                logger.info(f"HyperFrames render succeeded in {elapsed:.1f}s ({out_path.stat().st_size} bytes)")
                return out_path
            else:
                logger.warning(
                    f"HyperFrames render returned code {res.returncode}. "
                    f"Stderr: {res.stderr[:400] if res.stderr else 'None'}. Output: {res.stdout[:400]}"
                )
                raise HyperFramesRunnerError(f"HyperFrames process failed: {res.stderr or res.stdout}")

        except Exception as e:
            logger.warning(f"HyperFrames CLI execution exception: {e}. Activating reliable FFmpeg fallback renderer...")
            return self._render_ffmpeg_fallback(
                out_path,
                scene_visuals=scene_visuals,
                scene_durations=scene_durations,
            )

    def _render_ffmpeg_fallback(
        self,
        output_path: Path,
        scene_visuals: Optional[List[Path]] = None,
        scene_durations: Optional[List[float]] = None,
    ) -> Path:
        """
        Fallback renderer that compiles scene images and video clips into a continuous 1080x1920 30fps
        video with real cinematic camera push-in (Ken Burns) and preserved video stock motion.
        """
        import shutil
        if scene_visuals:
            candidates = [Path(p) for p in scene_visuals if Path(p).exists()]
        else:
            assets_dir = self.renderer_dir / "assets"
            candidates = sorted(list(assets_dir.glob("*.png")))

        if not candidates:
            raise HyperFramesRunnerError("No scene assets found for visual render.")

        temp_clips_dir = output_path.parent / f"clips_{output_path.stem}"
        temp_clips_dir.mkdir(parents=True, exist_ok=True)
        rendered_clips = []

        try:
            for idx, cand in enumerate(candidates):
                dur = scene_durations[idx] if (scene_durations and idx < len(scene_durations)) else 5.0
                dur = max(1.0, float(dur))
                clip_path = temp_clips_dir / f"clip_{idx:03d}.mp4"

                if cand.suffix.lower() == ".mp4":
                    # Video asset: preserve authentic video motion by scaling and looping/trimming
                    cmd = [
                        self.ffmpeg_cmd, "-y",
                        "-stream_loop", "-1",
                        "-i", str(cand.resolve()),
                        "-t", f"{dur:.2f}",
                        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p",
                        "-r", "30",
                        "-c:v", "libx264",
                        "-preset", "fast",
                        "-crf", "20",
                        "-an",
                        str(clip_path),
                    ]
                else:
                    # Image asset: apply smooth Ken Burns dynamic camera push-in
                    frames = max(30, int(dur * 30))
                    cmd = [
                        self.ffmpeg_cmd, "-y",
                        "-i", str(cand.resolve()),
                        "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,zoompan=z='min(zoom+0.0008,1.12)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p",
                        "-c:v", "libx264",
                        "-preset", "veryfast",
                        "-crf", "20",
                        "-an",
                        str(clip_path),
                    ]

                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode == 0 and clip_path.exists() and clip_path.stat().st_size > 5000:
                    rendered_clips.append(clip_path)
                else:
                    logger.warning(f"Motion clip generation warning: {res.stderr[:200]}. Trying static image clip...")
                    fallback_img_cmd = [
                        self.ffmpeg_cmd, "-y",
                        "-loop", "1",
                        "-t", f"{dur:.2f}",
                        "-i", str(cand.resolve()),
                        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p",
                        "-r", "30",
                        "-c:v", "libx264",
                        "-preset", "fast",
                        "-crf", "20",
                        "-an",
                        str(clip_path),
                    ]
                    subprocess.run(fallback_img_cmd, capture_output=True, text=True)
                    if clip_path.exists():
                        rendered_clips.append(clip_path)

            if not rendered_clips:
                raise HyperFramesRunnerError("Failed to render any visual clips.")

            # Concat all scene clips
            concat_list = temp_clips_dir / "clips_concat.txt"
            with open(concat_list, "w", encoding="utf-8") as f:
                for cl in rendered_clips:
                    cl_str = str(cl.resolve()).replace("\\", "/")
                    f.write(f"file '{cl_str}'\n")

            concat_cmd = [
                self.ffmpeg_cmd, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_list.resolve()),
                "-c", "copy",
                str(output_path),
            ]
            c_res = subprocess.run(concat_cmd, capture_output=True, text=True)
            if c_res.returncode != 0 or not output_path.exists() or output_path.stat().st_size < 10000:
                raise HyperFramesRunnerError(f"Concat failed: {c_res.stderr}")

            logger.info(f"Visual composition render completed: {output_path.name} ({output_path.stat().st_size} bytes)")
            return output_path
        finally:
            if temp_clips_dir.exists():
                shutil.rmtree(temp_clips_dir, ignore_errors=True)
