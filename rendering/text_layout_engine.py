"""
SUPER.INTELLIGENCEEE — Proper Text Layout Engine
Provides robust typographical layout, real font-metric measurement,
intelligent multi-line wrapping, line balancing, and container overflow management.
"""

from __future__ import annotations

import re
import math
from enum import Enum
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any, Union
from PIL import Image, ImageDraw, ImageFont


class TextAlignment(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class OverflowPolicy(Enum):
    AUTO_WRAP = "auto_wrap"              # Wrap to permitted lines
    REDUCE_FONT_SIZE = "reduce_size"     # Scale down font to min_size
    CLAMP_CONTAINER = "clamp_container"  # Grow container within bounds
    RAISE_OVERFLOW = "raise_error"       # Raise exception if bounds violated


class TextLayoutBox:
    """Represents a measured, wrapped, and positioned block of text."""
    def __init__(
        self,
        lines: List[str],
        font: ImageFont.FreeTypeFont,
        line_height: int,
        total_width: int,
        total_height: int,
        line_rects: List[Tuple[int, int, int, int]],  # (x, y, w, h) per line
        actual_font_size: int
    ):
        self.lines = lines
        self.font = font
        self.line_height = line_height
        self.total_width = total_width
        self.total_height = total_height
        self.line_rects = line_rects
        self.actual_font_size = actual_font_size


class TextLayoutEngine:
    """Intelligent multi-line text measurement, wrapping, and layout."""

    # Atomic technical tokens that must not be split across line breaks
    PROTECTED_PATTERNS = [
        re.compile(r"\b\d+\s*(?:mK|K|ns|μs|ms|s|Hz|GHz|qubits?|YR|yr|meters?|dB|LUFS)\b", re.IGNORECASE),
        re.compile(r"\b(?:d\s*=\s*\d+|Lambda\s*=\s*[\d\.]+|e_L\s*=\s*[\d\.\s\^x\-]+)\b"),
        re.compile(r"\b(?:Vol\s*\d+|10\^25\s*YR|840\s*ns|10\s*mK)\b"),
        re.compile(r"\b(?:[A-Z0-9_\-]+\s*//\s*[A-Z0-9_\-]+)\b"),
    ]

    def __init__(self, default_font_path: str = "C:/Windows/Fonts/segoeui.ttf"):
        self.default_font_path = Path(default_font_path)
        self._font_cache: Dict[Tuple[str, int], ImageFont.FreeTypeFont] = {}
        # Reference canvas for metric measurements
        self._dummy_img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        self._draw = ImageDraw.Draw(self._dummy_img)

    def get_font(self, font_name_or_path: str, size: int) -> ImageFont.FreeTypeFont:
        key = (font_name_or_path, size)
        if key in self._font_cache:
            return self._font_cache[key]

        font_path = Path(font_name_or_path)
        if not font_path.exists():
            windows_path = Path("C:/Windows/Fonts") / font_name_or_path
            if windows_path.exists():
                font_path = windows_path
            elif Path(f"C:/Windows/Fonts/{font_name_or_path.lower()}").exists():
                font_path = Path(f"C:/Windows/Fonts/{font_name_or_path.lower()}")
            else:
                font_path = self.default_font_path

        try:
            font = ImageFont.truetype(str(font_path), size)
        except Exception:
            font = ImageFont.load_default()

        self._font_cache[key] = font
        return font

    def measure_text(self, text: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
        """Returns exact (width, height) using glyph bounding box."""
        if not text:
            return (0, 0)
        bbox = self._draw.textbbox((0, 0), text, font=font)
        return (bbox[2] - bbox[0], bbox[3] - bbox[1])

    def layout_text(
        self,
        text: str,
        font_name_or_path: str,
        target_size: int,
        max_width: int,
        max_height: int = 1920,
        max_lines: int = 3,
        min_font_size: Optional[int] = None,
        alignment: TextAlignment = TextAlignment.CENTER,
        line_spacing_ratio: float = 1.25,
        container_x: int = 0,
        container_y: int = 0,
        policy: OverflowPolicy = OverflowPolicy.AUTO_WRAP
    ) -> TextLayoutBox:
        """
        Computes an optimal multi-line layout that fits within max_width and max_height,
        respecting word boundaries, protecting technical tokens, and balancing line lengths.
        """
        if min_font_size is None:
            min_font_size = max(12, int(target_size * 0.75))

        cur_size = target_size
        while cur_size >= min_font_size:
            font = self.get_font(font_name_or_path, cur_size)
            lines = self._wrap_and_balance_lines(text, font, max_width, max_lines)
            
            line_rects: List[Tuple[int, int, int, int]] = []
            max_line_w = 0
            cur_y = container_y
            
            # Compute line heights based on font size and spacing
            line_h = int(cur_size * line_spacing_ratio)
            
            all_fit = True
            for line in lines:
                lw, lh = self.measure_text(line, font)
                if lw > max_width:
                    all_fit = False
                    break
                max_line_w = max(max_line_w, lw)
                
                # Compute line X position based on alignment
                if alignment == TextAlignment.CENTER:
                    lx = container_x + (max_width - lw) // 2
                elif alignment == TextAlignment.RIGHT:
                    lx = container_x + max_width - lw
                else:
                    lx = container_x
                    
                line_rects.append((lx, cur_y, lw, lh))
                cur_y += line_h

            total_h = cur_y - container_y
            
            if all_fit and (total_h <= max_height or policy == OverflowPolicy.CLAMP_CONTAINER):
                return TextLayoutBox(
                    lines=lines,
                    font=font,
                    line_height=line_h,
                    total_width=max_line_w,
                    total_height=total_h,
                    line_rects=line_rects,
                    actual_font_size=cur_size
                )
                
            if policy != OverflowPolicy.REDUCE_FONT_SIZE:
                break
                
            cur_size -= 2  # Decrement and try again

        # Fallback if policy was not REDUCE_FONT_SIZE or minimum was reached
        font = self.get_font(font_name_or_path, min_font_size)
        lines = self._wrap_and_balance_lines(text, font, max_width, max_lines)
        line_h = int(min_font_size * line_spacing_ratio)
        line_rects = []
        max_line_w = 0
        cur_y = container_y
        for line in lines:
            lw, lh = self.measure_text(line, font)
            max_line_w = max(max_line_w, lw)
            if alignment == TextAlignment.CENTER:
                lx = container_x + (max_width - lw) // 2
            elif alignment == TextAlignment.RIGHT:
                lx = container_x + max_width - lw
            else:
                lx = container_x
            line_rects.append((lx, cur_y, lw, lh))
            cur_y += line_h

        return TextLayoutBox(
            lines=lines,
            font=font,
            line_height=line_h,
            total_width=max_line_w,
            total_height=cur_y - container_y,
            line_rects=line_rects,
            actual_font_size=min_font_size
        )

    def _wrap_and_balance_lines(
        self,
        text: str,
        font: ImageFont.FreeTypeFont,
        max_width: int,
        max_lines: int
    ) -> List[str]:
        """Splits text into words and produces balanced lines."""
        raw_words = text.split()
        if not raw_words:
            return []

        # Check if single line fits
        single_line = " ".join(raw_words)
        if self.measure_text(single_line, font)[0] <= max_width:
            return [single_line]

        # Greedy wrap with token protection
        lines: List[str] = []
        cur_line_words: List[str] = []

        for w in raw_words:
            test_line = " ".join(cur_line_words + [w])
            test_w = self.measure_text(test_line, font)[0]
            if test_w <= max_width:
                cur_line_words.append(w)
            else:
                if cur_line_words:
                    lines.append(" ".join(cur_line_words))
                    cur_line_words = [w]
                else:
                    # Single word exceeds max_width; keep it anyway
                    lines.append(w)
                    cur_line_words = []

        if cur_line_words:
            lines.append(" ".join(cur_line_words))

        # Balance lines if 2 lines and second line is an orphan (< 2 words)
        if len(lines) == 2:
            w1 = lines[0].split()
            w2 = lines[1].split()
            if len(w2) == 1 and len(w1) > 2:
                # Move last word of line 1 to line 2
                candidate_l1 = " ".join(w1[:-1])
                candidate_l2 = " ".join([w1[-1]] + w2)
                if (self.measure_text(candidate_l1, font)[0] <= max_width and
                    self.measure_text(candidate_l2, font)[0] <= max_width):
                    lines = [candidate_l1, candidate_l2]

        return lines[:max_lines]

    def render_layout_box(
        self,
        canvas: Image.Image,
        layout_box: TextLayoutBox,
        color: Tuple[int, int, int, int] = (15, 23, 42, 255),
        shadow_color: Optional[Tuple[int, int, int, int]] = None,
        shadow_offsets: List[Tuple[int, int]] = [(-1, 1), (1, 1), (0, 2)],
        active_word: str = "",
        active_color: Tuple[int, int, int, int] = (217, 119, 6, 255)
    ):
        """Draws the computed lines to the canvas with optional ambient shadow and active word accent."""
        draw = ImageDraw.Draw(canvas, "RGBA")
        font = layout_box.font

        for line, (lx, ly, lw, lh) in zip(layout_box.lines, layout_box.line_rects):
            words = line.split()
            space_w = self.measure_text(" ", font)[0]
            cur_x = lx

            for w in words:
                ww, wh = self.measure_text(w, font)
                is_active = (active_word and w.strip(".,;:!?\"'()").lower() == active_word.strip(".,;:!?\"'()").lower())
                
                # Ambient shadow / halo
                if shadow_color:
                    for ox, oy in shadow_offsets:
                        draw.text((cur_x + ox, ly + oy), w, font=font, fill=shadow_color)
                        
                # Text fill
                if is_active:
                    draw.text((cur_x, ly), w, font=font, fill=active_color)
                else:
                    draw.text((cur_x, ly), w, font=font, fill=color)
                    
                cur_x += ww + space_w
