"""
SUPER.INTELLIGENCEEE — Phase 5 Reference Kinetic Typography Engine
Implements the narration-aware kinetic typography extracted from the reference benchmark:
- Dual-font pairing: Bold Modern Sans (Inter/Arial/Helvetica) + Italic Serif (Playfair/Georgia/Times)
- Focus selection bounding boxes with corner handle dots around key metrics ([8 gigs], [176], etc.)
- Word-level reveal and emphasis tracking
- Animated numeric counters with easing
- Pure Python / Pillow / TrueType font rendering.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from rendering.native_motion_engine.primitives import (
    clamp,
    ease_out_back,
    ease_out_cubic,
    get_progress,
)


@dataclass
class KineticWord:
    text: str
    is_serif_italic: bool = False
    is_highlight_box: bool = False
    is_bold: bool = True
    color: Optional[Tuple[int, int, int]] = None


class ReferenceKineticTypography:
    """
    Renders reference-style kinetic typography at the top of the vertical frame (y = 80 to 260).
    Features dual-font pairing (Sans + Serif Italic) and dynamic focus selection boxes.
    """

    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height
        self._load_fonts()

    def _load_fonts(self):
        # Sans fonts
        try:
            self.font_sans_hero = ImageFont.truetype("arialbd.ttf", 64)
            self.font_sans_title = ImageFont.truetype("arialbd.ttf", 44)
            self.font_sans_sub = ImageFont.truetype("arialbd.ttf", 32)
            self.font_sans_mono = ImageFont.truetype("consola.ttf", 20)
        except Exception:
            self.font_sans_hero = ImageFont.load_default()
            self.font_sans_title = ImageFont.load_default()
            self.font_sans_sub = ImageFont.load_default()
            self.font_sans_mono = ImageFont.load_default()

        # Serif Italic fonts (Georgia / Times New Roman italic)
        try:
            self.font_serif_italic = ImageFont.truetype("georgiai.ttf", 44)
            self.font_serif_hero_italic = ImageFont.truetype("georgiai.ttf", 64)
        except Exception:
            try:
                self.font_serif_italic = ImageFont.truetype("timesi.ttf", 44)
                self.font_serif_hero_italic = ImageFont.truetype("timesi.ttf", 64)
            except Exception:
                self.font_serif_italic = self.font_sans_title
                self.font_serif_hero_italic = self.font_sans_hero

    def render_headline(
        self,
        draw: ImageDraw.ImageDraw,
        words: List[KineticWord],
        center_x: int = 540,
        top_y: int = 120,
        t: float = 1.0,
        is_dark_theme: bool = False,
    ) -> Tuple[int, int, int, int]:
        """
        Renders a centered kinetic headline with mixed sans and serif italic words,
        supporting animated selection bounding boxes around designated keywords.
        Returns the bounding box (x0, y0, x1, y1) of the rendered headline.
        """
        base_color = (255, 255, 255) if is_dark_theme else (15, 23, 42)
        box_outline_color = (56, 189, 248) if is_dark_theme else (2, 132, 199)

        # 1. Measure words and total width
        word_measurements = []
        space_w = draw.textlength(" ", font=self.font_sans_title)
        total_w = 0.0

        for kw in words:
            font = self.font_serif_italic if kw.is_serif_italic else self.font_sans_title
            w = draw.textlength(kw.text, font=font)
            word_measurements.append((kw, font, w))
            total_w += w

        total_w += (len(words) - 1) * space_w
        start_x = center_x - (total_w / 2.0)

        # 2. Render each word
        cur_x = start_x
        min_y = top_y
        max_y = top_y + 55

        for kw, font, w in word_measurements:
            word_color = kw.color or base_color

            # Draw word text
            draw.text((cur_x, top_y), kw.text, font=font, fill=word_color)

            # Draw Selection Bounding Box with Corner Handles if flagged
            if kw.is_highlight_box:
                pad_x = 10
                pad_y = 6
                bx0 = cur_x - pad_x
                by0 = top_y - pad_y
                bx1 = cur_x + w + pad_x
                by1 = top_y + 52 + pad_y

                # Animate box snap scale
                box_prog = get_progress(t, 0.1, 0.4, "ease_out_back")
                if box_prog > 0.01:
                    cx = (bx0 + bx1) / 2.0
                    cy = (by0 + by1) / 2.0
                    hw = ((bx1 - bx0) / 2.0) * box_prog
                    hh = ((by1 - by0) / 2.0) * box_prog

                    cur_bx0 = cx - hw
                    cur_by0 = cy - hh
                    cur_bx1 = cx + hw
                    cur_by1 = cy + hh

                    # Thin selection rectangle
                    draw.rectangle([cur_bx0, cur_by0, cur_bx1, cur_by1], outline=box_outline_color, width=2)

                    # 4 Corner Handle Dots (design tool style)
                    dot_r = 3
                    corners = [
                        (cur_bx0, cur_by0),
                        (cur_bx1, cur_by0),
                        (cur_bx0, cur_by1),
                        (cur_bx1, cur_by1),
                    ]
                    for cx_dot, cy_dot in corners:
                        draw.rectangle(
                            [cx_dot - dot_r, cy_dot - dot_r, cx_dot + dot_r, cy_dot + dot_r],
                            fill=(255, 255, 255),
                            outline=box_outline_color,
                            width=1,
                        )

            cur_x += w + space_w

        return (int(start_x - 12), int(min_y - 10), int(start_x + total_w + 12), int(max_y + 10))

    def render_hero_stat(
        self,
        draw: ImageDraw.ImageDraw,
        number_str: str,
        unit_str: str,
        sub_label: str,
        center_x: int = 540,
        center_y: int = 240,
        t: float = 1.0,
        is_dark_theme: bool = True,
    ):
        """
        Renders giant hero parameter count typography (e.g. '2.78 T parameters').
        """
        num_color = (255, 255, 255) if is_dark_theme else (15, 23, 42)
        unit_color = (56, 189, 248) if is_dark_theme else (2, 132, 199)
        sub_color = (148, 163, 184) if is_dark_theme else (100, 116, 139)

        # Measure
        num_w = draw.textlength(number_str, font=self.font_sans_hero)
        unit_w = draw.textlength(f" {unit_str}", font=self.font_sans_hero)
        tot_w = num_w + unit_w

        sx = center_x - (tot_w / 2.0)
        draw.text((sx, center_y), number_str, font=self.font_sans_hero, fill=num_color)
        draw.text((sx + num_w, center_y), f" {unit_str}", font=self.font_sans_hero, fill=unit_color)

        # Sub-label
        sub_w = draw.textlength(sub_label, font=self.font_sans_mono)
        draw.text((center_x - (sub_w / 2.0), center_y + 80), sub_label, font=self.font_sans_mono, fill=sub_color)
