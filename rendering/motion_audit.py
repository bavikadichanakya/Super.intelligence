"""
SUPER.INTELLIGENCEEE — Phase 3.5 Programmatic Motion Audit Subsystem
Evaluates frame deltas across video files at 0.5-second intervals to detect
static holds, freezes, lack of visual progression, and verify kinetic vitality.
Zero-dependency beyond FFmpeg, standard library, and NumPy.
"""

from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

logger = logging.getLogger("super_intelligence.motion_audit")


@dataclass
class MotionAuditResult:
    """Detailed programmatic motion audit findings."""
    video_path: str
    duration_seconds: float
    sample_interval_seconds: float
    total_samples: int
    mean_delta_pct: float
    min_delta_pct: float
    max_delta_pct: float
    static_hold_count: int
    static_hold_max_consecutive_seconds: float
    motion_pass: bool
    static_intervals: List[Dict[str, Any]] = field(default_factory=list)
    motion_timeline: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save_json(self, output_path: Path | str) -> Path:
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)
        logger.info(f"Saved MotionAuditResult to {out_p.name}")
        return out_p


class MotionAuditor:
    """Performs rigorous frame-by-frame temporal motion analysis on rendered documentary MP4s."""

    def __init__(self, ffmpeg_cmd: str = "ffmpeg", ffprobe_cmd: str = "ffprobe"):
        self.ffmpeg_cmd = ffmpeg_cmd
        self.ffprobe_cmd = ffprobe_cmd

    def get_duration(self, video_path: Path | str) -> float:
        """Inspects video container duration via ffprobe."""
        cmd = [
            self.ffprobe_cmd,
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(res.stdout.strip())
        except Exception as e:
            logger.warning(f"Failed to probe duration for {video_path}: {e}")
            return 0.0

    def audit_video(
        self,
        video_path: Path | str,
        sample_interval: float = 0.5,
        static_threshold_pct: float = 0.035,
        target_width: int = 540,
        target_height: int = 960,
    ) -> MotionAuditResult:
        """
        Samples the video at fixed intervals (default 0.5s) and calculates
        normalized mean pixel deltas across consecutive frames.
        Downscales during analysis to 540x960 for fast, memory-safe execution (< 100 MB RAM).
        """
        vid_p = Path(video_path).resolve()
        if not vid_p.exists():
            raise FileNotFoundError(f"Video file not found for motion audit: {vid_p}")

        duration = self.get_duration(vid_p)
        if duration <= 0.0:
            raise ValueError(f"Invalid or zero duration video: {vid_p}")

        fps_sample = 1.0 / sample_interval
        frame_bytes = target_width * target_height * 3

        # Stream downscaled raw frames via FFmpeg pipe
        cmd = [
            self.ffmpeg_cmd,
            "-v", "error",
            "-i", str(vid_p),
            "-vf", f"fps={fps_sample:.3f},scale={target_width}:{target_height}",
            "-f", "rawvideo",
            "-pix_fmt", "rgb24",
            "-",
        ]

        logger.info(f"Running motion audit on {vid_p.name} (interval={sample_interval}s, scale={target_width}x{target_height})...")
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        sample_idx = 0
        prev_frame: Optional[np.ndarray] = None
        deltas: List[float] = []
        timeline: List[Dict[str, Any]] = []
        static_intervals: List[Dict[str, Any]] = []

        consecutive_static = 0
        max_consecutive_static = 0

        while True:
            raw = proc.stdout.read(frame_bytes)
            if not raw or len(raw) < frame_bytes:
                break

            curr_frame = np.frombuffer(raw, dtype=np.uint8).astype(np.float32)
            timestamp = round(sample_idx * sample_interval, 2)

            if prev_frame is not None:
                # Calculate mean absolute pixel delta normalized as percentage (0 - 100%)
                diff = np.abs(curr_frame - prev_frame)
                delta_pct = float(np.mean(diff) / 255.0 * 100.0)
                deltas.append(delta_pct)

                is_static = delta_pct < static_threshold_pct
                if is_static:
                    consecutive_static += 1
                    max_consecutive_static = max(max_consecutive_static, consecutive_static)
                    static_intervals.append({
                        "timestamp_seconds": timestamp,
                        "delta_pct": round(delta_pct, 3),
                        "status": "STATIC_HOLD_DETECTED",
                    })
                else:
                    consecutive_static = 0

                timeline.append({
                    "sample_index": sample_idx,
                    "timestamp_seconds": timestamp,
                    "delta_pct": round(delta_pct, 3),
                    "is_static": is_static,
                })

            prev_frame = curr_frame
            sample_idx += 1

        proc.stdout.close()
        proc.wait()

        if not deltas:
            raise RuntimeError(f"Motion audit extracted zero valid delta samples from {vid_p.name}")

        mean_delta = float(np.mean(deltas))
        min_delta = float(np.min(deltas))
        max_delta = float(np.max(deltas))
        static_count = sum(1 for d in deltas if d < static_threshold_pct)
        max_static_sec = max_consecutive_static * sample_interval

        # Pass Criteria:
        # 1. Mean delta >= 0.40% (healthy continuous kinetic motion)
        # 2. Maximum consecutive static duration <= 1.0s (no frozen slides or dead holds)
        motion_pass = (mean_delta >= 0.40) and (max_static_sec <= 1.0)

        logger.info(
            f"Motion Audit complete for {vid_p.name}: Mean Delta={mean_delta:.2f}%, "
            f"Static Holds={static_count}, Max Frozen Duration={max_static_sec:.1f}s, Pass={motion_pass}"
        )

        return MotionAuditResult(
            video_path=str(vid_p),
            duration_seconds=duration,
            sample_interval_seconds=sample_interval,
            total_samples=len(deltas),
            mean_delta_pct=round(mean_delta, 3),
            min_delta_pct=round(min_delta, 3),
            max_delta_pct=round(max_delta, 3),
            static_hold_count=static_count,
            static_hold_max_consecutive_seconds=round(max_static_sec, 2),
            motion_pass=motion_pass,
            static_intervals=static_intervals,
            motion_timeline=timeline,
        )

