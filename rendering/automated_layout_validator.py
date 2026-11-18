"""
SUPER.INTELLIGENCEEE — Automated Layout & Typography Validator
Performs forensic mathematical verification of text layouts, safe areas,
collisions, and mobile readability across all documentary scenes.
"""

from __future__ import annotations

from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
from PIL import ImageFont

from rendering.text_layout_engine import TextLayoutBox, TextLayoutEngine


@dataclass
class LayoutElement:
    element_id: str
    element_type: str  # title, subtitle, annotation, data_label, footnote
    x: int
    y: int
    w: int
    h: int
    text: str
    font_size: int
    container_bounds: Optional[Tuple[int, int, int, int]] = None  # (cx, cy, cw, ch)


@dataclass
class ValidationIssue:
    severity: str  # ERROR, WARNING
    scene_id: str
    timestamp: float
    element_id: str
    rule_violated: str
    details: str
    measured_value: Any
    threshold_value: Any


class AutomatedLayoutValidator:
    """Forensic validator inspecting bounding geometry and mobile ergonomics."""

    def __init__(
        self,
        canvas_width: int = 1080,
        canvas_height: int = 1920,
        safe_margin_x: int = 60,
        safe_margin_y: int = 60
    ):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.safe_margin_x = safe_margin_x
        self.safe_margin_y = safe_margin_y
        self.issues: List[ValidationIssue] = []

    def clear(self):
        self.issues.clear()

    def validate_scene_layout(
        self,
        scene_id: str,
        timestamp: float,
        elements: List[LayoutElement],
        critical_geometry_regions: Optional[List[Tuple[int, int, int, int]]] = None
    ) -> List[ValidationIssue]:
        """Audits a complete frame's text elements against all layout constraints."""
        scene_issues: List[ValidationIssue] = []

        for elem in elements:
            # 1. Canvas Boundary Check
            if elem.x < self.safe_margin_x:
                scene_issues.append(ValidationIssue(
                    severity="ERROR",
                    scene_id=scene_id,
                    timestamp=timestamp,
                    element_id=elem.element_id,
                    rule_violated="LEFT_FRAME_OVERFLOW",
                    details=f"Element '{elem.element_id}' left edge ({elem.x}px) exceeds left safe margin ({self.safe_margin_x}px)",
                    measured_value=elem.x,
                    threshold_value=self.safe_margin_x
                ))
            if elem.x + elem.w > self.canvas_width - self.safe_margin_x:
                scene_issues.append(ValidationIssue(
                    severity="ERROR",
                    scene_id=scene_id,
                    timestamp=timestamp,
                    element_id=elem.element_id,
                    rule_violated="RIGHT_FRAME_OVERFLOW",
                    details=f"Element '{elem.element_id}' right edge ({elem.x + elem.w}px) exceeds right safe margin ({self.canvas_width - self.safe_margin_x}px)",
                    measured_value=elem.x + elem.w,
                    threshold_value=self.canvas_width - self.safe_margin_x
                ))
            if elem.y + elem.h > self.canvas_height - self.safe_margin_y:
                scene_issues.append(ValidationIssue(
                    severity="ERROR",
                    scene_id=scene_id,
                    timestamp=timestamp,
                    element_id=elem.element_id,
                    rule_violated="BOTTOM_FRAME_OVERFLOW",
                    details=f"Element '{elem.element_id}' bottom edge ({elem.y + elem.h}px) exceeds bottom margin ({self.canvas_height - self.safe_margin_y}px)",
                    measured_value=elem.y + elem.h,
                    threshold_value=self.canvas_height - self.safe_margin_y
                ))

            # 2. Container Bounds Check
            if elem.container_bounds:
                cx, cy, cw, ch = elem.container_bounds
                if elem.x < cx or elem.y < cy or (elem.x + elem.w) > (cx + cw) or (elem.y + elem.h) > (cy + ch):
                    scene_issues.append(ValidationIssue(
                        severity="ERROR",
                        scene_id=scene_id,
                        timestamp=timestamp,
                        element_id=elem.element_id,
                        rule_violated="CONTAINER_OVERFLOW",
                        details=f"Element '{elem.element_id}' escapes container ({cx}, {cy}, {cw}, {ch})",
                        measured_value=(elem.x, elem.y, elem.w, elem.h),
                        threshold_value=elem.container_bounds
                    ))

            # 3. Mobile Readability (Font Size)
            min_size = 20 if elem.element_type != "footnote" else 16
            if elem.font_size < min_size:
                scene_issues.append(ValidationIssue(
                    severity="WARNING",
                    scene_id=scene_id,
                    timestamp=timestamp,
                    element_id=elem.element_id,
                    rule_violated="INSUFFICIENT_FONT_SIZE",
                    details=f"Font size {elem.font_size}pt below mobile readability threshold ({min_size}pt)",
                    measured_value=elem.font_size,
                    threshold_value=min_size
                ))

        # 4. Text-on-Text Collision Detection
        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                e1, e2 = elements[i], elements[j]
                if self._check_rect_collision((e1.x, e1.y, e1.w, e1.h), (e2.x, e2.y, e2.w, e2.h)):
                    scene_issues.append(ValidationIssue(
                        severity="ERROR",
                        scene_id=scene_id,
                        timestamp=timestamp,
                        element_id=f"{e1.element_id}_vs_{e2.element_id}",
                        rule_violated="TEXT_COLLISION",
                        details=f"Text collision between '{e1.element_id}' and '{e2.element_id}'",
                        measured_value=(e1.x, e1.y, e1.w, e1.h),
                        threshold_value=(e2.x, e2.y, e2.w, e2.h)
                    ))

        # 5. Critical Geometry Collision Detection (e.g. text overlapping hardware)
        if critical_geometry_regions:
            for elem in elements:
                if elem.element_type == "subtitle":
                    for g_idx, geom in enumerate(critical_geometry_regions):
                        if self._check_rect_collision((elem.x, elem.y, elem.w, elem.h), geom):
                            scene_issues.append(ValidationIssue(
                                severity="ERROR",
                                scene_id=scene_id,
                                timestamp=timestamp,
                                element_id=elem.element_id,
                                rule_violated="SUBTITLE_GEOMETRY_COLLISION",
                                details=f"Subtitle '{elem.element_id}' overlaps critical hardware region #{g_idx}",
                                measured_value=(elem.x, elem.y, elem.w, elem.h),
                                threshold_value=geom
                            ))

        self.issues.extend(scene_issues)
        return scene_issues

    def _check_rect_collision(self, r1: Tuple[int, int, int, int], r2: Tuple[int, int, int, int]) -> bool:
        """Returns True if two rectangles (x, y, w, h) intersect with >0 area."""
        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2
        return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)
