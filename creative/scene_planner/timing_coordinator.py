"""
SUPER.INTELLIGENCEEE — Timing Coordinator & Audio-Visual Synchronization Planner
Coordinates scene durations with actual narration WAV files, allocates visual hold times,
prevents static frame stagnation, and eliminates timing mismatches prior to rendering.
"""

from __future__ import annotations

import logging
import wave
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.creative_contracts import DynamicScene, DynamicScenePlan

logger = logging.getLogger("super_intelligence.timing_coordinator")


class TimingCoordinator:
    """Plans and synchronizes scene display durations against speech audio."""

    def __init__(self, target_wps: float = 2.5, min_scene_hold: float = 3.2):
        self.target_wps = target_wps
        self.min_scene_hold = min_scene_hold

    def estimate_narration_duration(self, text: str) -> float:
        """Estimates spoken duration based on word count (~2.5 words per second)."""
        words = len(text.strip().split())
        if words == 0:
            return self.min_scene_hold
        est = words / self.target_wps
        return max(self.min_scene_hold, round(est, 2))

    def measure_wav_duration(self, wav_path: Path | str) -> float:
        """Reads exact duration in seconds directly from a RIFF WAV header."""
        path = Path(wav_path)
        if not path.exists():
            return 0.0
        try:
            with wave.open(str(path), "rb") as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                if rate > 0:
                    return round(frames / float(rate), 3)
        except Exception as e:
            logger.warning(f"Could not read WAV duration from {path.name}: {e}")
        return 0.0

    def synchronize_with_audio(
        self,
        scene_plan: DynamicScenePlan,
        scene_audio_files: List[Path | str],
        visual_hold_padding_seconds: float = 0.25,
    ) -> DynamicScenePlan:
        """
        Updates each scene's actual_duration from real synthesized WAV audio.
        Applies subtle visual hold padding to prevent abrupt cuts between scenes.
        """
        scenes = scene_plan.scenes
        if len(scene_audio_files) != len(scenes):
            logger.warning(
                f"Audio file count ({len(scene_audio_files)}) does not match scene count ({len(scenes)}). "
                f"Synchronizing available subset."
            )

        for i, sc in enumerate(scenes):
            if i < len(scene_audio_files):
                f_path = scene_audio_files[i]
                real_dur = self.measure_wav_duration(f_path)
                if real_dur > 0.5:
                    # Allocate subtle visual hold padding on scene exit
                    padded_dur = round(real_dur + visual_hold_padding_seconds, 2)
                    sc.actual_duration = padded_dur
                    logger.info(f"Scene #{sc.sequence} audio synchronized: {real_dur:.2f}s (Padded: {padded_dur:.2f}s)")
                else:
                    # Fallback to estimated duration
                    sc.actual_duration = sc.estimated_duration

        return scene_plan

    def audit_timing_profile(self, scene_plan: DynamicScenePlan) -> Dict[str, Any]:
        """
        Audits the timing distribution across all scenes.
        Detects rushed scenes (< 2.5s), excessively long static scenes (> 14s),
        and overall video pacing.
        """
        scenes = scene_plan.scenes
        issues: List[str] = []
        rushed_scenes: List[int] = []
        stagnant_scenes: List[int] = []

        total_duration = 0.0
        for s in scenes:
            dur = s.duration_seconds
            total_duration += dur
            word_count = len(s.narration.split())
            wps = word_count / dur if dur > 0 else 0

            if dur < 2.5:
                rushed_scenes.append(s.sequence)
                issues.append(f"Scene #{s.sequence} duration is too short ({dur:.1f}s). Minimum is 2.5s.")

            if dur > 15.0:
                stagnant_scenes.append(s.sequence)
                issues.append(
                    f"Scene #{s.sequence} duration is excessively long ({dur:.1f}s). "
                    f"Subdivide into multiple visual beats to prevent visual stagnation."
                )

            if wps > 3.8:
                issues.append(f"Scene #{s.sequence} speech rate is rushed ({wps:.1f} wps). Target is ~2.5 wps.")

        passed = len(rushed_scenes) == 0 and len(stagnant_scenes) == 0

        return {
            "passed": passed,
            "total_duration_seconds": round(total_duration, 2),
            "scene_count": len(scenes),
            "avg_scene_duration": round(total_duration / max(1, len(scenes)), 2),
            "rushed_scenes": rushed_scenes,
            "stagnant_scenes": stagnant_scenes,
            "issues": issues,
        }

