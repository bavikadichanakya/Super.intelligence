"""
SUPER.INTELLIGENCEEE — Advanced Scientific Subtitle Engine
Reconstructs the subtitle presentation layer:
- 100% transparent backing (zero black box)
- Mobile-safe 2-line intelligent wrapping (max width 900px, 90px margin left/right)
- Dual-pass ambient halo for high-contrast legibility over any background
- Kokoro acoustic word-level timestamp synchronization
"""

from __future__ import annotations

from typing import List, Tuple, Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont

from rendering.text_layout_engine import TextLayoutEngine, TextLayoutBox, TextAlignment, OverflowPolicy


class AdvancedSubtitleEngine:
    """Manages subtitle timing, multi-line wrapping, safe-area positioning, and rendering."""

    def __init__(self, layout_engine: Optional[TextLayoutEngine] = None):
        self.layout = layout_engine or TextLayoutEngine()
        self.font_sans = "segoeuib.ttf"
        self.font_mono = "consolab.ttf"
        self.font_size = 38
        self.max_width = 900       # 90px left/right margins on 1080px canvas
        self.container_x = 90      # Centered: (1080 - 900) // 2
        
        # Color palettes for light theme
        self.color_primary = (15, 23, 42, 255)         # Deep Obsidian Slate (#0F172A)
        self.color_halo = (255, 255, 255, 220)        # Soft Ambient Halo (#FFFFFF, 86% alpha)
        self.color_active_gold = (217, 119, 6, 255)   # Amber Gold (#D97706)
        self.color_active_green = (5, 150, 105, 255)  # Technical Emerald (#059669)
        self.color_active_cyan = (2, 132, 199, 255)   # Electric Sapphire (#0284C7)

    def compute_subtitle_layout(
        self,
        phrase: str,
        treatment: int = 1,
        y_center: int = 1680
    ) -> TextLayoutBox:
        """Calculates multi-line layout bounded strictly within the mobile safe area."""
        font_name = self.font_mono if treatment == 2 else self.font_sans
        target_size = 32 if treatment == 2 else self.font_size
        
        # Lay out text with maximum 2 lines
        box = self.layout.layout_text(
            text=phrase,
            font_name_or_path=font_name,
            target_size=target_size,
            max_width=self.max_width,
            max_height=140,
            max_lines=2,
            min_font_size=28,
            alignment=TextAlignment.CENTER,
            line_spacing_ratio=1.30,
            container_x=self.container_x,
            container_y=y_center - 40,
            policy=OverflowPolicy.AUTO_WRAP
        )
        return box

    def render_subtitle(
        self,
        canvas: Image.Image,
        phrase: str,
        active_word: str = "",
        treatment: int = 1,
        y_center: int = 1680
    ):
        """Renders 100% transparent subtitles with ambient halo and active word tracking."""
        if not phrase:
            return

        box = self.compute_subtitle_layout(phrase, treatment=treatment, y_center=y_center)
        
        # Choose active highlight color
        if treatment == 2:
            active_col = self.color_active_green
        elif treatment == 3:
            active_col = self.color_active_cyan
        else:
            active_col = self.color_active_gold

        draw = ImageDraw.Draw(canvas, "RGBA")

        # Treatment 2: Technical registration brackets
        if treatment == 2:
            bx0 = (1080 - box.total_width) // 2 - 24
            by0 = box.line_rects[0][1] - 12
            bx1 = (1080 + box.total_width) // 2 + 24
            by1 = box.line_rects[-1][1] + box.line_rects[-1][3] + 10
            cl = 12
            bracket_col = (2, 132, 199, 180)
            draw.line([bx0, by0 + cl, bx0, by0, bx0 + cl, by0], fill=bracket_col, width=2)
            draw.line([bx1, by0 + cl, bx1, by0, bx1 - cl, by0], fill=bracket_col, width=2)
            draw.line([bx0, by1 - cl, bx0, by1, bx0 + cl, by1], fill=bracket_col, width=2)
            draw.line([bx1, by1 - cl, bx1, by1, bx1 - cl, by1], fill=bracket_col, width=2)

        # Dual-pass halo rendering:
        # Pass 1: Multi-direction soft ambient halo (ensures legibility over any hardware)
        halo_offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, -1), (-1, 1), (1, 1)]
        self.layout.render_layout_box(
            canvas=canvas,
            layout_box=box,
            color=self.color_primary,
            shadow_color=self.color_halo,
            shadow_offsets=halo_offsets,
            active_word=active_word,
            active_color=active_col
        )

    def validate_safe_area(self, box: TextLayoutBox) -> Tuple[bool, List[str]]:
        """Verifies that all subtitle lines stay strictly within mobile safe margins."""
        violations = []
        for idx, (lx, ly, lw, lh) in enumerate(box.line_rects):
            if lx < 90:
                violations.append(f"Line {idx+1} left edge (x={lx}) violates left safe margin (x>=90)")
            if lx + lw > 990:
                violations.append(f"Line {idx+1} right edge (x={lx+lw}) violates right safe margin (x<=990)")
            if ly < 1200 or ly + lh > 1850:
                violations.append(f"Line {idx+1} vertical position (y={ly}) violates vertical safe range (1200..1850)")
        return (len(violations) == 0, violations)
