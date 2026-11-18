"""
SUPER.INTELLIGENCEEE — Phase 4.3.2B Multi-Engine Rendering Dispatcher
RenderArtifact model with cryptographic integrity and ffprobe validation.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from pydantic import BaseModel, Field, field_validator

from rendering.engine_errors import ArtifactValidationError

logger = logging.getLogger("super_intelligence.render_artifact")


class RenderArtifact(BaseModel):
    """
    Immutable representation of a verified rendered video stem or composite.
    Guarantees integrity, resolution compliance, and metadata traceability.
    """
    scene_id: str = Field(..., description="Unique scene identifier or 'master' for assembled reel")
    engine_name: str = Field(..., description="Name of the engine that rendered this artifact (manim, threejs, hyperframes, ffmpeg)")
    output_path: Path = Field(..., description="Absolute path to the rendered video file")
    duration_seconds: float = Field(..., ge=0.0, description="Duration in seconds")
    width: int = Field(default=1080, ge=1, description="Pixel width")
    height: int = Field(default=1920, ge=1, description="Pixel height")
    fps: float = Field(default=30.0, gt=0.0, description="Frame rate")
    file_size_bytes: int = Field(..., ge=1, description="File size in bytes (must be > 0)")
    sha256_hash: str = Field(..., min_length=64, max_length=64, description="Cryptographic SHA-256 hash of output file")
    codecs: Dict[str, str] = Field(default_factory=dict, description="Detected stream codecs, e.g. {'video': 'h264', 'audio': 'aac'}")
    render_time_seconds: float = Field(default=0.0, ge=0.0, description="Wall-clock time taken to render in seconds")
    peak_ram_mb: float = Field(default=0.0, ge=0.0, description="Peak RAM consumed during render in MB")
    ffprobe_metadata: Dict[str, Any] = Field(default_factory=dict, description="Raw ffprobe output for provenance")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    @field_validator("output_path", mode="before")
    @classmethod
    def _coerce_path(cls, v: Any) -> Path:
        return Path(v).resolve()

    @staticmethod
    def compute_sha256(file_path: Path | str) -> str:
        """Calculates SHA-256 hash of a file on disk."""
        p = Path(file_path).resolve()
        if not p.is_file():
            raise ArtifactValidationError(f"File not found for hash calculation: {p}")
        h = hashlib.sha256()
        with open(p, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    @classmethod
    def from_output_file(
        cls,
        scene_id: str,
        engine_name: str,
        output_path: Path | str,
        render_time_seconds: float = 0.0,
        peak_ram_mb: float = 0.0,
        expected_width: int = 1080,
        expected_height: int = 1920,
        expected_fps: float = 30.0,
        duration_tolerance_sec: float = 1.0,
        expected_duration_seconds: Optional[float] = None,
    ) -> RenderArtifact:
        """
        Inspects an output video on disk using ffprobe, validates resolution and fps,
        calculates SHA-256, and returns a verified RenderArtifact.
        """
        p = Path(output_path).resolve()
        if not p.is_file():
            raise ArtifactValidationError(f"Render artifact missing on disk: {p}")

        file_size = p.stat().st_size
        if file_size == 0:
            raise ArtifactValidationError(f"Render artifact is zero bytes: {p}")

        # Compute SHA-256 hash
        sha256 = cls.compute_sha256(p)

        # Probe file with ffprobe
        probe_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "stream=width,height,r_frame_rate,nb_frames,duration,codec_name,codec_type",
            "-show_entries", "format=duration,size,bit_rate",
            "-of", "json",
            str(p)
        ]

        try:
            res = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
            probe_data = json.loads(res.stdout)
        except Exception as e:
            raise ArtifactValidationError(f"ffprobe failed to inspect {p}: {e}")

        streams = probe_data.get("streams", [])
        fmt = probe_data.get("format", {})

        video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
        if not video_stream:
            raise ArtifactValidationError(f"No video stream found in {p}")

        # Extract dimensions
        w = int(video_stream.get("width", 0))
        h = int(video_stream.get("height", 0))

        if w != expected_width or h != expected_height:
            raise ArtifactValidationError(
                f"Resolution mismatch in {p}: expected {expected_width}x{expected_height}, got {w}x{h}"
            )

        # Extract frame rate
        r_fps_str = video_stream.get("r_frame_rate", "30/1")
        try:
            if "/" in r_fps_str:
                num, den = r_fps_str.split("/")
                fps_val = float(num) / float(den)
            else:
                fps_val = float(r_fps_str)
        except Exception:
            fps_val = 30.0

        if abs(fps_val - expected_fps) > 1.0:
            raise ArtifactValidationError(
                f"Frame rate mismatch in {p}: expected {expected_fps} fps, got {fps_val:.2f} fps"
            )

        # Extract duration
        duration = float(fmt.get("duration") or video_stream.get("duration") or 0.0)
        if expected_duration_seconds is not None:
            if abs(duration - expected_duration_seconds) > duration_tolerance_sec:
                logger.warning(
                    f"Duration drift in {p}: expected ~{expected_duration_seconds:.2f}s, got {duration:.2f}s "
                    f"(tolerance: ±{duration_tolerance_sec}s)"
                )

        # Codecs
        codecs = {"video": video_stream.get("codec_name", "unknown")}
        audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
        if audio_stream:
            codecs["audio"] = audio_stream.get("codec_name", "unknown")

        return cls(
            scene_id=scene_id,
            engine_name=engine_name,
            output_path=p,
            duration_seconds=round(duration, 3),
            width=w,
            height=h,
            fps=round(fps_val, 2),
            file_size_bytes=file_size,
            sha256_hash=sha256,
            codecs=codecs,
            render_time_seconds=round(render_time_seconds, 2),
            peak_ram_mb=round(peak_ram_mb, 2),
            ffprobe_metadata=probe_data,
        )
