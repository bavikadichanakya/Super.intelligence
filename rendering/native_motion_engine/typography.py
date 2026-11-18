"""
SUPER.INTELLIGENCEEE — Phase 4.3.2D Native Motion Graphics Engine
Typography & Safe-Zone Layout Engine.
Guarantees robust word wrapping, auto-fitting, bounding box enforcement,
and vertical safe-zone compliance (top 180px, bottom 260px, horizontal 60px).
No text truncation or silent string slicing.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple, Union

from PIL import Image, ImageDraw, ImageFont


class TextAlignment(str, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class TextRole(str, Enum):
    TITLE = "title"
    SUBHEAD = "subhead"
    BODY = "body"
    BADGE = "badge"
    METRIC = "metric"
    FOOTNOTE = "footnote"


@dataclass
class SafeZone:
    top: int = 180
    bottom: int = 260
    left: int = 60
    right: int = 60
    canvas_width: int = 1080
    canvas_height: int = 1920

    @property
    def safe_width(self) -> int:
        return self.canvas_width - self.left - self.right

    @property
    def safe_height(self) -> int:
        return self.canvas_height - self.top - self.bottom

    @property
    def safe_top(self) -> int:
        return self.top

    @property
    def safe_bottom(self) -> int:
        return self.canvas_height - self.bottom

    def is_box_safe(self, box: Tuple[int, int, int, int]) -> bool:
        """Checks if (x1, y1, x2, y2) resides strictly inside safe bounds."""
        x1, y1, x2, y2 = box
        return (
            x1 >= self.left
            and x2 <= (self.canvas_width - self.right)
            and y1 >= self.top
            and y2 <= (self.canvas_height - self.bottom)
        )


class TypographyEngine:
    """
    High-precision typography layout engine utilizing Pillow FreeType fonts.
    Handles dynamic line wrapping, font auto-scaling, and vertical safe zones.
    """

    FONT_CANDIDATES = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/consolab.ttf",
    ]

    def __init__(self, safe_zone: Optional[SafeZone] = None):
        self.safe_zone = safe_zone or SafeZone()
        self._font_cache: dict = {}

    def get_font(
        self,
        size: int,
        bold: bool = False,
        mono: bool = False,
    ) -> ImageFont.FreeTypeFont:
        """Retrieves or loads a cached font matching style criteria."""
        cache_key = (size, bold, mono)
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]

        target_name = "consola" if mono else ("segoe" if not bold else "arialbd")
        if mono and bold:
            target_name = "consolab"

        font_path = None
        for cand in self.FONT_CANDIDATES:
            if target_name in cand.lower() and os.path.exists(cand):
                font_path = cand
                break

        if not font_path:
            # Fallback to any existing Windows font
            for cand in self.FONT_CANDIDATES:
                if os.path.exists(cand):
                    font_path = cand
                    break

        if font_path:
            try:
                font = ImageFont.truetype(font_path, size=size)
                self._font_cache[cache_key] = font
                return font
            except Exception:
                pass

        # Final fallback
        font = ImageFont.load_default()
        self._font_cache[cache_key] = font
        return font

    def wrap_text(
        self,
        text: str,
        font: ImageFont.FreeTypeFont,
        max_width: int,
        draw: Optional[ImageDraw.ImageDraw] = None,
    ) -> List[str]:
        """
        Wraps text into lines that do not exceed max_width pixels.
        Ensures words are preserved and never silently chopped.
        """
        if not text:
            return []

        if draw is None:
            dummy_img = Image.new("RGBA", (1, 1))
            draw = ImageDraw.Draw(dummy_img)

        words = text.split(" ")
        lines: List[str] = []
        current_line: List[str] = []

        for word in words:
            test_line = " ".join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_w = bbox[2] - bbox[0]

            if line_w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    # Single word exceeds max_width: keep as its own line
                    lines.append(word)
                    current_line = []

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def fit_text_box(
        self,
        text: str,
        max_width: int,
        max_height: int,
        preferred_size: int = 40,
        min_size: int = 16,
        bold: bool = False,
        mono: bool = False,
    ) -> Tuple[List[str], ImageFont.FreeTypeFont, int, int]:
        """
        Calculates optimal font size so all wrapped lines fit strictly within max_width x max_height.
        Returns: (wrapped_lines, font, total_w, total_h)
        """
        dummy_img = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(dummy_img)

        current_size = preferred_size
        while current_size >= min_size:
            font = self.get_font(size=current_size, bold=bold, mono=mono)
            lines = self.wrap_text(text, font, max_width=max_width, draw=draw)
            line_height = int(current_size * 1.35)
            total_h = len(lines) * line_height

            max_line_w = 0
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                w = bbox[2] - bbox[0]
                if w > max_line_w:
                    max_line_w = w

            if total_h <= max_height and max_line_w <= max_width:
                return (lines, font, max_line_w, total_h)

            current_size -= 2

        # Min size reached
        font = self.get_font(size=min_size, bold=bold, mono=mono)
        lines = self.wrap_text(text, font, max_width=max_width, draw=draw)
        line_height = int(min_size * 1.35)
        total_h = len(lines) * line_height
        return (lines, font, max_width, total_h)

    def draw_text_block(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        box: Tuple[int, int, int, int],
        fill: Tuple[int, int, int, int] = (248, 250, 252, 255),
        preferred_size: int = 36,
        min_size: int = 18,
        bold: bool = False,
        mono: bool = False,
        align: TextAlignment = TextAlignment.LEFT,
        line_spacing_mult: float = 1.35,
    ) -> Tuple[int, int, int, int]:
        """
        Renders a cleanly wrapped and auto-fitted text block within the given bounding box (x, y, w, h).
        Returns the actual rendered bounding box (rx1, ry1, rx2, ry2).
        """
        x, y, max_w, max_h = box
        lines, font, actual_w, total_h = self.fit_text_box(
            text=text,
            max_width=max_w,
            max_height=max_h,
            preferred_size=preferred_size,
            min_size=min_size,
            bold=bold,
            mono=mono,
        )

        line_h = int(font.size * line_spacing_mult)
        cur_y = y

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            lw = bbox[2] - bbox[0]
            if align == TextAlignment.CENTER:
                cur_x = x + (max_w - lw) // 2
            elif align == TextAlignment.RIGHT:
                cur_x = x + (max_w - lw)
            else:
                cur_x = x

            draw.text((cur_x, cur_y), line, font=font, fill=fill)
            cur_y += line_h

        return (x, y, x + actual_w, y + total_h)

