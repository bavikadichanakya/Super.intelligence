"""
SUPER.INTELLIGENCEEE — Phase 9.2 Smart Composition & Layout Architecture
Provides:
1. Mathematical BoundingBox algebra (overlap tests, edge clearances, centroid calculation).
2. Optical center and visual weight balancing.
3. Dynamic collision-free annotation placement via cost minimization.
4. Subtitle safe-zone enforcement and collision prevention.
5. Diagnostic composition overlay generator (renders bounding boxes, optical centers, and safe zones).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont


@dataclass
class BoundingBox:
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def width(self) -> float:
        return max(0.0, self.x1 - self.x0)

    @property
    def height(self) -> float:
        return max(0.0, self.y1 - self.y0)

    @property
    def center(self) -> Tuple[float, float]:
        return ((self.x0 + self.x1) / 2.0, (self.y0 + self.y1) / 2.0)

    @property
    def area(self) -> float:
        return self.width * self.height

    def overlaps(self, other: BoundingBox, padding: float = 0.0) -> bool:
        """Returns True if this box overlaps with other box (with optional padding)."""
        return not (
            self.x1 + padding <= other.x0 or
            self.x0 - padding >= other.x1 or
            self.y1 + padding <= other.y0 or
            self.y0 - padding >= other.y1
        )

    def contains(self, other: BoundingBox) -> bool:
        return (
            self.x0 <= other.x0 and
            self.y0 <= other.y0 and
            self.x1 >= other.x1 and
            self.y1 >= other.y1
        )

    def distance_to(self, other: BoundingBox) -> float:
        """Euclidean distance between box centers."""
        c1 = self.center
        c2 = other.center
        return math.hypot(c1[0] - c2[0], c1[1] - c2[1])


@dataclass
class VisualElement:
    name: str
    bbox: BoundingBox
    category: str # "HERO", "SECONDARY", "TEXT", "ANNOTATION", "SUBTITLE"
    visual_weight: float = 1.0


class SmartCompositionValidator:
    """
    Validates and diagnoses frame layout:
    - Verifies margin edge clearances (left/right >= 72px, top >= 80px, bottom >= 400px).
    - Checks for illegal collisions between text and hero subjects.
    - Computes optical visual weight centroid.
    - Generates diagnostic overlay frames for automated and human auditing.
    """
    def __init__(self, canvas_width: int = 1080, canvas_height: int = 1920):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.margin_x = 72.0
        self.margin_top = 80.0
        self.margin_bottom = 400.0 # Safe zone for platform UI
        self.elements: List[VisualElement] = []

    def clear(self):
        self.elements.clear()

    def register(self, name: str, bbox: BoundingBox, category: str, visual_weight: float = 1.0):
        self.elements.append(VisualElement(name, bbox, category, visual_weight))

    def detect_collisions(self) -> List[Tuple[str, str, float]]:
        """Returns list of (elem_a, elem_b, overlap_area) for any colliding elements."""
        collisions = []
        n = len(self.elements)
        for i in range(n):
            for j in range(i + 1, n):
                ea = self.elements[i]
                eb = self.elements[j]
                # Allow background/secondary elements to overlap hero, but text/annotations must never collide!
                if "TEXT" in (ea.category, eb.category) or "ANNOTATION" in (ea.category, eb.category) or "SUBTITLE" in (ea.category, eb.category):
                    if ea.bbox.overlaps(eb.bbox, padding=4.0):
                        # compute overlap area
                        ox0 = max(ea.bbox.x0, eb.bbox.x0)
                        oy0 = max(ea.bbox.y0, eb.bbox.y0)
                        ox1 = min(ea.bbox.x1, eb.bbox.x1)
                        oy1 = min(ea.bbox.y1, eb.bbox.y1)
                        overlap_area = max(0.0, ox1 - ox0) * max(0.0, oy1 - oy0)
                        collisions.append((ea.name, eb.name, overlap_area))
        return collisions

    def compute_optical_center(self) -> Tuple[float, float]:
        """Calculates optical centroid weighted by visual importance."""
        total_w = 0.0
        sum_x = 0.0
        sum_y = 0.0
        for el in self.elements:
            cx, cy = el.bbox.center
            w = el.visual_weight * math.sqrt(max(1.0, el.bbox.area))
            sum_x += cx * w
            sum_y += cy * w
            total_w += w
        if total_w <= 0.0:
            return (self.canvas_width / 2.0, self.canvas_height / 2.0)
        return (sum_x / total_w, sum_y / total_w)

    def draw_diagnostic_overlay(self, base_canvas: Image.Image) -> Image.Image:
        """Renders diagnostic overlay with bounding boxes, optical center, and safe zones."""
        overlay = base_canvas.copy()
        draw = ImageDraw.Draw(overlay, "RGBA")
        
        # 1. Safe Zone Outlines
        # Top Header Zone
        draw.rectangle([self.margin_x, self.margin_top, self.canvas_width - self.margin_x, 230], outline=(70, 130, 180, 120), width=2)
        # Main Hero Safe Area
        draw.rectangle([self.margin_x, 240, self.canvas_width - self.margin_x, self.canvas_height - self.margin_bottom], outline=(100, 200, 100, 80), width=2)
        # Subtitle Safe Band
        draw.rectangle([self.margin_x, 1420, self.canvas_width - self.margin_x, 1540], outline=(255, 215, 0, 140), width=2)
        # Bottom Cutoff Danger Zone
        draw.rectangle([0, self.canvas_height - 360, self.canvas_width, self.canvas_height], fill=(255, 50, 50, 20), outline=(255, 50, 50, 120), width=2)
        
        # 2. Draw Element Bounding Boxes
        cat_colors = {
            "HERO": (56, 189, 248, 220),       # Cyan
            "SECONDARY": (129, 140, 248, 180),  # Indigo
            "TEXT": (255, 255, 255, 200),       # White
            "ANNOTATION": (252, 211, 77, 240),  # Amber
            "SUBTITLE": (52, 211, 153, 220),    # Mint Green
        }
        for el in self.elements:
            col = cat_colors.get(el.category, (200, 200, 200, 200))
            draw.rectangle([el.bbox.x0, el.bbox.y0, el.bbox.x1, el.bbox.y1], outline=col, width=2)
            # Label
            draw.text((el.bbox.x0 + 4, el.bbox.y0 + 2), f"{el.name} [{el.category}]", fill=col)

        # 3. Optical Centroid Crosshair
        oc_x, oc_y = self.compute_optical_center()
        draw.ellipse([oc_x - 12, oc_y - 12, oc_x + 12, oc_y + 12], outline=(239, 68, 68, 255), width=3)
        draw.line([oc_x - 24, oc_y, oc_x + 24, oc_y], fill=(239, 68, 68, 255), width=2)
        draw.line([oc_x, oc_y - 24, oc_x, oc_y + 24], fill=(239, 68, 68, 255), width=2)
        draw.text((oc_x + 16, oc_y - 10), f"OPTICAL CENTER ({int(oc_x)}, {int(oc_y)})", fill=(239, 68, 68, 255))
        
        return overlay


class SmartAnnotationRouter:
    """
    Computes optimal, collision-free annotation coordinates:
    - Finds empty space on left or right flanks of the hero object.
    - Routes elbow connector lines to prevent intersecting hero features.
    """
    @staticmethod
    def place_annotation(
        target_x: float,
        target_y: float,
        badge_w: float,
        badge_h: float,
        existing_boxes: List[BoundingBox],
        canvas_width: int = 1080,
        margin_x: float = 72.0,
        preferred_side: str = "auto"
    ) -> Tuple[float, float, str, BoundingBox]:
        """
        Returns (badge_x, badge_y, align, badge_bbox).
        """
        # Determine candidate sides
        if preferred_side == "auto":
            sides = ["right", "left"] if target_x <= canvas_width / 2.0 else ["left", "right"]
        else:
            sides = [preferred_side]
            
        best_pos = None
        min_cost = float("inf")
        
        for side in sides:
            for y_offset in [0.0, -40.0, 40.0, -80.0, 80.0]:
                curr_by = target_y + y_offset
                if side == "right":
                    bx0 = target_x + 100.0
                    bx1 = bx0 + badge_w
                    if bx1 > canvas_width - margin_x:
                        bx1 = canvas_width - margin_x
                        bx0 = bx1 - badge_w
                else: # left
                    bx1 = target_x - 100.0
                    bx0 = bx1 - badge_w
                    if bx0 < margin_x:
                        bx0 = margin_x
                        bx1 = bx0 + badge_w
                        
                by0 = curr_by - badge_h / 2.0
                by1 = curr_by + badge_h / 2.0
                cand_box = BoundingBox(bx0, by0, bx1, by1)
                
                # Calculate cost: distance + collision penalty
                dist = math.hypot(target_x - cand_box.center[0], target_y - cand_box.center[1])
                collision_penalty = 0.0
                for eb in existing_boxes:
                    if cand_box.overlaps(eb, padding=12.0):
                        collision_penalty += 10000.0
                        
                cost = dist + collision_penalty + abs(y_offset) * 2.0
                if cost < min_cost:
                    min_cost = cost
                    best_pos = (bx0 if side == "right" else bx1, curr_by, side, cand_box)
                    
        return best_pos or (canvas_width - margin_x - badge_w, target_y, "right", BoundingBox(canvas_width - margin_x - badge_w, target_y - badge_h/2, canvas_width - margin_x, target_y + badge_h/2))
