"""
SUPER.INTELLIGENCEEE — Visual Intelligence Composition Base
Provides the foundational 1080x1920 rendering canvas, camera transforms,
dual-font kinetic typography, and animated selection bounding boxes.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

from core.universal_scene_contract import UniversalSceneContract
from creative.visual_intelligence.camera_director import CameraDirector
from creative.visual_intelligence.motion_director import MotionDirector


class BaseVisualIntelligenceComposition:
    """
    Base composition class for all 1080x1920 explanatory motion graphics.
    Strictly enforces full-bleed presentation (zero slide cards or dashboard borders).
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        self.scene = scene
        self.width = width
        self.height = height
        self.duration = float(scene.actual_duration_seconds or scene.narration_duration_seconds or 6.5)

        cfg = getattr(scene, "engine_specific_config", None) or {}
        self.theme_mode = cfg.get("theme_mode", "dark")
        self.camera_movement = cfg.get("camera_movement", "slow_zoom_in")
        self.kinetic_focus_noun = cfg.get("kinetic_focus_noun", "")
        self.kinetic_italic_keyword = cfg.get("kinetic_italic_keyword", "")
        self.headline = cfg.get("headline", "")
        self.color_accents = cfg.get("color_accents", {})
        self.params = cfg.get("parameters", {})

        self.camera = CameraDirector(movement_type=self.camera_movement, duration=self.duration)
        self.scheduled_words = MotionDirector.schedule_kinetic_typography(
            text=scene.narration_text or "",
            duration=self.duration,
            focus_noun=self.kinetic_focus_noun,
            italic_keyword=self.kinetic_italic_keyword,
        )

        # Setup standard system fonts
        self._init_fonts()

    def _init_fonts(self):
        """Initializes typography hierarchy with fallbacks."""
        try:
            self.font_sans_bold = ImageFont.truetype("arialbd.ttf", 46)
            self.font_sans_head = ImageFont.truetype("arialbd.ttf", 26)
            self.font_serif_italic = ImageFont.truetype("georgiai.ttf", 48)
            self.font_mono = ImageFont.truetype("consola.ttf", 24)
            self.font_mono_bold = ImageFont.truetype("consolab.ttf", 28)
            self.font_metric = ImageFont.truetype("arialbd.ttf", 72)
        except Exception:
            self.font_sans_bold = ImageFont.load_default()
            self.font_sans_head = ImageFont.load_default()
            self.font_serif_italic = ImageFont.load_default()
            self.font_mono = ImageFont.load_default()
            self.font_mono_bold = ImageFont.load_default()
            self.font_metric = ImageFont.load_default()

    def render_frame(self, t: float) -> Image.Image:
        """
        Renders a single 1080x1920 frame at time t.
        1. Draws background canvas with subtle ambient gradient / grid.
        2. Renders explanatory mechanism in central action zone (y = 350 to 1520).
        3. Applies camera transforms.
        4. Overlays dual-font kinetic typography in top safe zone (y = 120 to 320).
        """
        # Create base canvas
        bg_color = (10, 13, 20) if self.theme_mode == "dark" else (229, 229, 224)
        canvas = Image.new("RGBA", (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(canvas)

        # Draw background architectural lines / subtle grid
        self._render_background_grid(draw, t)

        # Draw domain-specific explanatory mechanism
        self.render_mechanism(draw, canvas, t)

        # Render top kinetic typography
        self._render_kinetic_typography(draw, t)

        return canvas

    def _render_background_grid(self, draw: ImageDraw.Draw, t: float):
        """Draws a subtle technical grid across the canvas."""
        grid_spacing = 80
        if self.theme_mode == "dark":
            line_color = (30, 41, 59, 120)
            dot_color = (56, 189, 248, 80)
        else:
            line_color = (214, 214, 208, 140)
            dot_color = (15, 23, 42, 60)

        # Subtle drift over time
        offset_y = int((t * 12.0) % grid_spacing)
        for y in range(offset_y, self.height, grid_spacing):
            draw.line([(0, y), (self.width, y)], fill=line_color, width=1)
        for x in range(0, self.width, grid_spacing):
            draw.line([(x, 0), (x, self.height)], fill=line_color, width=1)

    def _render_kinetic_typography(self, draw: ImageDraw.Draw, t: float):
        """
        Renders two-font kinetic typography in the upper safe region (y = 120 to 320).
        Uses Bold Grotesque Sans + Italic Serif + dynamic Figma-style selection bounding box.
        """
        top_y = 130
        left_margin = 80
        right_margin = self.width - 80
        max_w = right_margin - left_margin

        # 1. Headline category pill
        head_text = self.headline or "TECHNICAL EXPLAINER"
        pill_bg = (56, 189, 248, 30) if self.theme_mode == "dark" else (2, 132, 199, 25)
        pill_border = (56, 189, 248) if self.theme_mode == "dark" else (2, 132, 199)
        text_color_head = (56, 189, 248) if self.theme_mode == "dark" else (2, 132, 199)

        draw.rounded_rectangle([left_margin, top_y, left_margin + 260, top_y + 36], radius=8, fill=pill_bg, outline=pill_border, width=1)
        draw.text((left_margin + 16, top_y + 6), head_text[:24], fill=text_color_head, font=self.font_sans_head)

        # 2. Synchronized words
        revealed_words = [w for w in self.scheduled_words if w["start_time"] <= t]
        if not revealed_words:
            return

        cur_x = left_margin
        cur_y = top_y + 60
        line_height = 56

        text_obsidian = (241, 245, 249) if self.theme_mode == "dark" else (15, 23, 42)
        text_dim = (148, 163, 184) if self.theme_mode == "dark" else (100, 116, 139)
        blue_accent = (56, 189, 248) if self.theme_mode == "dark" else (2, 132, 199)

        for item in revealed_words:
            w_str = item["word"]
            is_focus = item["is_focus_noun"]
            is_italic = item["is_italic_keyword"]

            active_font = self.font_serif_italic if is_italic else self.font_sans_bold
            bbox = active_font.getbbox(w_str)
            w_width = bbox[2] - bbox[0] + 12

            if cur_x + w_width > right_margin:
                cur_x = left_margin
                cur_y += line_height
                if cur_y > 310:
                    break

            # Draw word
            word_color = blue_accent if is_focus else (text_obsidian if not is_italic else blue_accent)
            draw.text((cur_x, cur_y), w_str, fill=word_color, font=active_font)

            # If focus noun, draw animated selection bounding box
            if is_focus:
                p_box = min(1.0, max(0.0, (t - item["start_time"]) / 0.25))
                box_scale = MotionDirector.ease_out_back(p_box)
                pad_x = 6 * box_scale
                pad_y = 4 * box_scale
                b_x1 = cur_x - pad_x
                b_y1 = cur_y - pad_y
                b_x2 = cur_x + w_width - 8 + pad_x
                b_y2 = cur_y + line_height - 12 + pad_y

                draw.rectangle([b_x1, b_y1, b_x2, b_y2], outline=blue_accent, width=2)
                # Corner dots
                for pt in [(b_x1, b_y1), (b_x2, b_y1), (b_x1, b_y2), (b_x2, b_y2)]:
                    draw.rectangle([pt[0] - 3, pt[1] - 3, pt[0] + 3, pt[1] + 3], fill=blue_accent)

            cur_x += w_width

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        """Subclasses override this to implement domain-specific visual mechanism."""
        pass
