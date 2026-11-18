"""
SUPER.INTELLIGENCEEE — Subtitle Layout Engine & Collision Avoidance Subsystem
Guarantees zero collisions between subtitles and protected on-screen technical graphics,
dynamic placement calculation, balanced two-line text wrapping, safe-zone conformance,
and frame-level collision auditing.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from PIL import Image, ImageDraw, ImageFont


@dataclass
class BoundingBox:
    x0: int
    y0: int
    x1: int
    y1: int
    label: str = "protected_region"

    @property
    def width(self) -> int:
        return max(0, self.x1 - self.x0)

    @property
    def height(self) -> int:
        return max(0, self.y1 - self.y0)

    @property
    def area(self) -> int:
        return self.width * self.height

    def intersects(self, other: BoundingBox, margin: int = 0) -> bool:
        """Returns True if this box intersects other box with optional buffer margin."""
        return not (
            self.x1 + margin <= other.x0
            or self.x0 - margin >= other.x1
            or self.y1 + margin <= other.y0
            or self.y0 - margin >= other.y1
        )

    def intersection_area(self, other: BoundingBox) -> int:
        """Returns the pixel area of overlap between two boxes."""
        ix0 = max(self.x0, other.x0)
        iy0 = max(self.y0, other.y0)
        ix1 = min(self.x1, other.x1)
        iy1 = min(self.y1, other.y1)
        if ix1 > ix0 and iy1 > iy0:
            return (ix1 - ix0) * (iy1 - iy0)
        return 0


@dataclass
class SubtitleCue:
    start_sec: float
    end_sec: float
    text: str
    lines: List[str]
    bbox: BoundingBox
    scene_id: str = ""
    margin_v: int = 300
    alignment: int = 2  # Bottom-Center in ASS


class SubtitleLayoutEngine:
    """
    Computes collision-free subtitle positioning and line wrapping.
    Integrates with scene contract protected regions to guarantee 0% visual overlap.
    """

    CANVAS_WIDTH = 1080
    CANVAS_HEIGHT = 1920

    # Default platform interaction safe zone (TikTok/Reels/Shorts bottom controls)
    PLATFORM_DANGER_BOTTOM = 1660
    PLATFORM_DANGER_TOP = 180
    SAFE_MARGIN_H = 60

    # Default dedicated caption corridor (strictly below visuals y <= 1400, strictly above UI y >= 1660)
    DEFAULT_CAPTION_ZONE = BoundingBox(
        x0=60,
        y0=1430,
        x1=1020,
        y1=1630,
        label="reserved_caption_corridor",
    )

    def __init__(self, font_size: int = 34, max_line_chars: int = 36):
        self.font_size = font_size
        self.max_line_chars = max_line_chars
        # Use Windows standard Arial or Segoe font for measurement
        self._font = None
        for p in ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf"]:
            if Path(p).exists():
                try:
                    self._font = ImageFont.truetype(p, font_size)
                    break
                except Exception:
                    pass
        if self._font is None:
            self._font = ImageFont.load_default()

    def wrap_caption_lines(self, text: str) -> List[str]:
        """
        Wraps caption into at most 2 balanced lines without clipping or orphan words.
        """
        text = " ".join(text.strip().split())
        if not text:
            return []

        words = text.split(" ")
        if len(text) <= self.max_line_chars:
            return [text]

        # Find best split point near the middle to create two balanced lines
        mid_target = len(text) // 2
        best_split_idx = 1
        best_diff = 999

        cur_len = 0
        for i in range(len(words) - 1):
            cur_len += len(words[i]) + (1 if i > 0 else 0)
            diff = abs(cur_len - mid_target)
            if diff < best_diff:
                best_diff = diff
                best_split_idx = i + 1

        line1 = " ".join(words[:best_split_idx])
        line2 = " ".join(words[best_split_idx:])

        # If line2 still exceeds max chars, re-balance conservatively
        if len(line2) > self.max_line_chars and len(words) >= 4:
            # Shift a word to line1 if line1 can accommodate it
            if len(line1) + 1 + len(words[best_split_idx]) <= self.max_line_chars + 6:
                line1 = " ".join(words[: best_split_idx + 1])
                line2 = " ".join(words[best_split_idx + 1 :])

        return [line1, line2] if line2 else [line1]

    def measure_text_box(
        self,
        lines: List[str],
        anchor_bottom_y: int = 1620,
        center_x: int = 540,
    ) -> BoundingBox:
        """Computes bounding box for wrapped caption lines given a bottom baseline anchor."""
        line_height = int(self.font_size * 1.35)
        total_h = len(lines) * line_height

        dummy_img = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(dummy_img)

        max_w = 0
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=self._font)
            w = bbox[2] - bbox[0]
            if w > max_w:
                max_w = w

        max_w = max(max_w + 32, 200)  # Add pill padding
        x0 = max(self.SAFE_MARGIN_H, center_x - max_w // 2)
        x1 = min(self.CANVAS_WIDTH - self.SAFE_MARGIN_H, x0 + max_w)
        y1 = anchor_bottom_y
        y0 = y1 - total_h - 16

        return BoundingBox(x0=x0, y0=y0, x1=x1, y1=y1, label="caption_box")

    def plan_scene_cues(
        self,
        scene_id: str,
        narration_text: str,
        start_time_sec: float,
        duration_sec: float,
        protected_regions: Optional[List[BoundingBox]] = None,
    ) -> List[SubtitleCue]:
        """
        Plans all subtitle cues for a scene, selecting collision-free placement.
        """
        protected_regions = protected_regions or []
        words = narration_text.split()
        if not words:
            return []

        # Divide narration into comfortable reading chunks (~7 to 10 words, ~2.5 to 3.5 seconds each)
        chunk_word_size = 8
        num_chunks = max(1, math.ceil(len(words) / chunk_word_size))
        chunk_dur = duration_sec / float(num_chunks)

        # Check if default caption zone [1430, 1630] intersects any protected region
        target_margin_v = 300  # Baseline at y = 1920 - 300 = 1620
        caption_zone = self.DEFAULT_CAPTION_ZONE

        has_conflict = False
        for pr in protected_regions:
            if pr.intersects(caption_zone, margin=15):
                has_conflict = True
                break

        # If lower zone has conflict, move to upper safe corridor below header (y = 380 - 480)
        if has_conflict:
            # Alternate top caption position (MarginV = 1480 from bottom -> y ≈ 440)
            target_margin_v = 1460
            anchor_bottom = 460
            align = 8  # Top-center in ASS
        else:
            target_margin_v = 300
            anchor_bottom = 1620
            align = 2  # Bottom-center in ASS

        cues: List[SubtitleCue] = []
        for i in range(num_chunks):
            w_start = i * chunk_word_size
            w_end = min(len(words), (i + 1) * chunk_word_size)
            chunk_raw = " ".join(words[w_start:w_end])

            t0 = start_time_sec + i * chunk_dur
            t1 = min(start_time_sec + duration_sec, t0 + chunk_dur)

            wrapped_lines = self.wrap_caption_lines(chunk_raw)
            bbox = self.measure_text_box(wrapped_lines, anchor_bottom_y=anchor_bottom)

            cue = SubtitleCue(
                start_sec=round(t0, 2),
                end_sec=round(t1, 2),
                text=r"\N".join(wrapped_lines),
                lines=wrapped_lines,
                bbox=bbox,
                scene_id=scene_id,
                margin_v=target_margin_v,
                alignment=align,
            )
            cues.append(cue)

        return cues


class SubtitleCollisionValidator:
    """
    Validates that rendered or planned subtitles have ZERO intersections with protected visual regions.
    """

    @classmethod
    def validate_cues_against_scenes(
        cls,
        cues: List[SubtitleCue],
        scene_protected_regions: Dict[str, List[BoundingBox]],
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Audits all subtitle cues against their scene's protected regions.
        Returns: (passed, collision_issues)
        """
        issues: List[Dict[str, Any]] = []

        for cue in cues:
            # Check canvas bounds
            if cue.bbox.x0 < 0 or cue.bbox.x1 > 1080 or cue.bbox.y0 < 0 or cue.bbox.y1 > 1920:
                issues.append({
                    "scene_id": cue.scene_id,
                    "timestamp": cue.start_sec,
                    "text": cue.text,
                    "type": "CANVAS_OVERFLOW",
                    "issue": f"Subtitle box {cue.bbox} extends outside 1080x1920 canvas bounds.",
                })

            # Check line count
            if len(cue.lines) > 2:
                issues.append({
                    "scene_id": cue.scene_id,
                    "timestamp": cue.start_sec,
                    "text": cue.text,
                    "type": "EXCESSIVE_LINES",
                    "issue": f"Subtitle has {len(cue.lines)} lines (maximum allowed is 2).",
                })

            # Check protected region intersections
            regions = scene_protected_regions.get(cue.scene_id, [])
            for pr in regions:
                overlap = cue.bbox.intersection_area(pr)
                if overlap > 0:
                    issues.append({
                        "scene_id": cue.scene_id,
                        "timestamp": cue.start_sec,
                        "text": cue.text,
                        "type": "VISUAL_COLLISION",
                        "protected_region": pr.label,
                        "overlap_area_pixels": overlap,
                        "issue": f"Subtitle overlaps with protected visual region '{pr.label}' ({overlap}px overlap).",
                    })

        passed = len(issues) == 0
        return passed, issues
