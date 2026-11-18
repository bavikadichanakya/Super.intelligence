"""
SUPER.INTELLIGENCEEE — Phase 4.3.2B Multi-Engine Rendering Dispatcher
EngineDispatcher: Master orchestration layer routing UniversalSceneContracts to Manim, Three.js,
HyperFrames, and assembling final video through FFmpeg under strict single sequential execution locks.
"""

from __future__ import annotations

import logging
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.universal_scene_contract import (
    RenderingEngine,
    UniversalSceneContract,
    VideoStoryboardContract,
)
from rendering.adapters.ffmpeg_adapter import FFmpegAdapter
from rendering.engine_errors import (
    EngineError,
    FallbackExhaustedError,
    ResourceThresholdBreachedError,
)
from rendering.engine_registry import EngineRegistry
from rendering.execution_context import ExecutionContext
from rendering.render_artifact import RenderArtifact
from rendering.resource_guard import ResourceGuard, ResourceThresholdError

logger = logging.getLogger("super_intelligence.engine_dispatcher")


class EngineDispatcher:
    """
    Production-grade multi-engine rendering dispatcher.
    Guarantees:
    1. Single sequential execution lock (zero concurrent rendering processes on 8 GB RAM).
    2. Automatic engine routing based on scene archetype and contract specification.
    3. Resilient fallback degradation if preferred engine encounters errors.
    4. Cryptographic SHA-256 and ffprobe validation of all rendered video stems.
    5. Final assembly, broadcast loudness mastering (-16 LUFS), and safe-zone subtitles via FFmpeg.
    """

    def __init__(
        self,
        registry: Optional[EngineRegistry] = None,
        resource_guard: Optional[ResourceGuard] = None,
        workspace_root: Optional[Path | str] = None,
    ):
        self.workspace_root = Path(workspace_root or "A:/SUPER.INTELLIGENCEEE").resolve()
        self.guard = resource_guard or ResourceGuard(workspace_root=self.workspace_root)
        self.registry = registry or EngineRegistry(resource_guard=self.guard)
        self._lock = threading.Lock()

    def dispatch_scene(
        self,
        scene: UniversalSceneContract,
        output_dir: Optional[Path | str] = None,
        keep_scratch: bool = False,
    ) -> RenderArtifact:
        """
        Dispatches a single UniversalSceneContract to its designated rendering engine under sequential lock.
        Executes automatic fallback if the primary engine fails.
        """
        with self._lock:
            # 1. Preflight safety check
            try:
                safety = self.guard.check_preflight_safety()
                logger.info(
                    f"Preflight safety OK for scene '{scene.scene_id}': "
                    f"{safety['available_ram_mb']} MB RAM free, {safety['free_disk_gb']} GB disk free."
                )
            except ResourceThresholdError as e:
                raise ResourceThresholdBreachedError(str(e)) from e

            # 2. Resolve primary engine adapter
            primary_adapter = self.registry.resolve_engine(scene)
            primary_engine = primary_adapter.engine_name

            logger.info(
                f"Dispatching scene '{scene.scene_id}' to primary engine '{primary_engine.value}' "
                f"(SceneType: {scene.scene_type.value}, Target: {scene.actual_duration_seconds or scene.narration_duration_seconds}s)"
            )

            # 3. Attempt render with primary engine
            try:
                with ExecutionContext(
                    scene_id=scene.scene_id,
                    workspace_root=self.workspace_root,
                    output_dir=output_dir,
                    keep_scratch=keep_scratch,
                ) as ctx:
                    artifact = primary_adapter.render(scene, ctx)
                    return artifact

            except Exception as primary_err:
                logger.warning(
                    f"Primary engine '{primary_engine.value}' failed for scene '{scene.scene_id}': {primary_err}. "
                    "Checking fallback availability..."
                )

                # 4. Attempt fallback engine
                fallback_engine = self.registry.get_fallback_engine_for_scene(scene, primary_engine)
                if not fallback_engine:
                    raise FallbackExhaustedError(
                        scene_id=scene.scene_id,
                        preferred_err=str(primary_err),
                        fallback_err="No fallback engine declared or available.",
                    ) from primary_err

                fb_adapter = self.registry.get_adapter(fallback_engine)
                if not fb_adapter or not fb_adapter.is_available():
                    raise FallbackExhaustedError(
                        scene_id=scene.scene_id,
                        preferred_err=str(primary_err),
                        fallback_err=f"Fallback engine '{fallback_engine.value}' is unavailable.",
                    ) from primary_err

                logger.info(
                    f"Executing fallback render for scene '{scene.scene_id}' "
                    f"using engine '{fallback_engine.value}'..."
                )

                try:
                    with ExecutionContext(
                        scene_id=scene.scene_id,
                        workspace_root=self.workspace_root,
                        output_dir=output_dir,
                        keep_scratch=keep_scratch,
                    ) as fb_ctx:
                        artifact = fb_adapter.render(scene, fb_ctx)
                        logger.info(f"Fallback engine '{fallback_engine.value}' successfully rendered '{scene.scene_id}'.")
                        return artifact
                except Exception as fb_err:
                    logger.error(
                        f"Fallback engine '{fallback_engine.value}' also failed for scene '{scene.scene_id}': {fb_err}."
                    )
                    # Zero calibration pattern fallbacks in production. If both fail, fail cleanly.
                    raise FallbackExhaustedError(
                        scene_id=scene.scene_id,
                        preferred_err=str(primary_err),
                        fallback_err=f"Fallback engine '{fallback_engine.value}' failed: {fb_err}",
                    ) from fb_err

    def dispatch_storyboard(
        self,
        storyboard: VideoStoryboardContract,
        output_path: Optional[Path | str] = None,
        audio_stem: Optional[Path | str] = None,
        subtitles_ass: Optional[Path | str] = None,
        stems_dir: Optional[Path | str] = None,
        burn_subtitles: bool = True,
        keep_scratch: bool = False,
    ) -> Dict[str, Any]:
        """
        Sequentially renders all scenes in a VideoStoryboardContract and assembles them into
        a finalized master MP4 with safe-zone subtitles and broadcast loudness normalization (-16 LUFS).
        """
        start_time = time.time()
        logger.info(
            f"Beginning storyboard dispatch for '{storyboard.video_id}' "
            f"({len(storyboard.scenes)} scenes, target duration: {storyboard.target_duration_seconds}s)"
        )

        stem_artifacts: List[RenderArtifact] = []
        target_stems_dir = Path(stems_dir or (self.workspace_root / "output" / "stems")).resolve()
        target_stems_dir.mkdir(parents=True, exist_ok=True)

        target_master_path = Path(
            output_path or (self.workspace_root / "output" / f"{storyboard.video_id}_master.mp4")
        ).resolve()

        # Sequentially dispatch each scene
        for idx, scene in enumerate(storyboard.scenes, start=1):
            logger.info(f"Rendering scene {idx}/{len(storyboard.scenes)}: '{scene.scene_id}'...")
            artifact = self.dispatch_scene(
                scene=scene,
                output_dir=target_stems_dir,
                keep_scratch=keep_scratch,
            )
            stem_artifacts.append(artifact)

        # Assemble stems via FFmpeg
        ffmpeg_adapter = self.registry.get_adapter(RenderingEngine.FFMPEG)
        if not isinstance(ffmpeg_adapter, FFmpegAdapter):
            ffmpeg_adapter = FFmpegAdapter(resource_guard=self.guard)

        master_artifact = ffmpeg_adapter.assemble_storyboard(
            storyboard=storyboard,
            stem_artifacts=stem_artifacts,
            output_path=target_master_path,
            audio_stem=audio_stem,
            subtitles_ass=subtitles_ass,
            burn_subtitles=burn_subtitles,
        )

        total_wall_time = time.time() - start_time
        summary = {
            "video_id": storyboard.video_id,
            "title": storyboard.title,
            "master_artifact": master_artifact,
            "stem_artifacts": stem_artifacts,
            "scene_count": len(stem_artifacts),
            "total_render_duration_seconds": round(total_wall_time, 2),
            "master_output_path": str(master_artifact.output_path),
            "sha256": master_artifact.sha256_hash,
            "status": "COMPLETED",
        }

        logger.info(
            f"Storyboard dispatch complete for '{storyboard.video_id}' in {total_wall_time:.2f}s! "
            f"Master: {master_artifact.output_path} ({master_artifact.file_size_bytes / (1024**2):.2f} MB)"
        )

        return summary
