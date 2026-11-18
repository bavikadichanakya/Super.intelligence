"""
SUPER.INTELLIGENCEEE — Phase 7 Physical Explainer Composition Base
Provides the light-first editorial studio canvas, directional lighting,
ground contact shadows, and high-contrast typography.
Completely banishes cyber grids, HUD corner reticles, and dark template boxes.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

from core.universal_scene_contract import UniversalSceneContract
from creative.visual_intelligence.camera_director import CameraDirector


class BasePhysicalExplainerComposition:
    """
    Physical Explainer Base Composition.
    Default surface: Warm ivory (#F5F3ED), soft white (#FAFAF8), or architectural grey (#E8E6E0).
    Hero objects command 65%-85% of canvas width with real soft contact shadows.
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        self.scene = scene
        self.width = width
        self.height = height
        self.duration = float(scene.actual_duration_seconds or scene.narration_duration_seconds or 5.0)

        cfg = getattr(scene, "engine_specific_config", None) or {}
        # Default to warm ivory studio surface
        self.surface_theme = cfg.get("surface_theme", "warm_ivory")
        self.camera_movement = cfg.get("camera_movement", "slow_zoom_in")
        self.headline = cfg.get("headline", "")
        self.subheadline = cfg.get("subheadline", "")
        self.camera = CameraDirector(movement_type=self.camera_movement, duration=self.duration)

        self._init_palette()
        self._init_fonts()

    def _init_palette(self):
        if self.surface_theme == "warm_ivory":
            self.bg_color = (245, 243, 237)      # #F5F3ED
            self.text_primary = (15, 23, 42)      # Deep slate #0F172A
            self.text_secondary = (71, 85, 105)   # Muted slate #475569
            self.accent_blue = (2, 132, 199)      # Architectural blue #0284C7
            self.accent_cyan = (14, 116, 144)     # Deep cyan
            self.shadow_color = (0, 0, 0, 32)     # Soft contact shadow
        elif self.surface_theme == "soft_white":
            self.bg_color = (250, 250, 248)      # #FAFAF8
            self.text_primary = (15, 23, 42)
            self.text_secondary = (100, 116, 139)
            self.accent_blue = (37, 99, 235)
            self.accent_cyan = (6, 182, 212)
            self.shadow_color = (0, 0, 0, 28)
        else: # architectural_grey
            self.bg_color = (232, 230, 224)      # #E8E6E0
            self.text_primary = (15, 23, 42)
            self.text_secondary = (71, 85, 105)
            self.accent_blue = (2, 132, 199)
            self.accent_cyan = (14, 116, 144)
            self.shadow_color = (0, 0, 0, 36)

    def _init_fonts(self):
        try:
            self.font_hero = ImageFont.truetype("arialbd.ttf", 80)
            self.font_title = ImageFont.truetype("arialbd.ttf", 52)
            self.font_subtitle = ImageFont.truetype("georgiai.ttf", 34)
            self.font_label = ImageFont.truetype("arialbd.ttf", 26)
            self.font_mono = ImageFont.truetype("consola.ttf", 24)
            self.font_mono_bold = ImageFont.truetype("consolab.ttf", 28)
            self.font_stat_num = ImageFont.truetype("arialbd.ttf", 110)
        except Exception:
            self.font_hero = self.font_title = self.font_subtitle = self.font_label = ImageFont.load_default()

    def render_frame(self, t: float) -> Image.Image:
        canvas = Image.new("RGBA", (self.width, self.height), self.bg_color + (255,))
        draw = ImageDraw.Draw(canvas, "RGBA")

        # 1. Soft Studio Vignette / Lighting
        self._render_studio_lighting(draw)

        # 2. Hero Physical Object Mechanism with Soft Contact Shadows
        self.render_physical_mechanism(draw, canvas, t)

        # 3. Clean Editorial Typography (Upper Third)
        self._render_editorial_typography(draw, t)

        return canvas

    def _render_studio_lighting(self, draw: ImageDraw.Draw):
        """Draws subtle, soft radial lighting falloff for physical studio depth."""
        # Top-left key light gradient simulation
        cx = int(self.width * 0.45)
        cy = int(self.height * 0.35)
        for r in range(900, 300, -120):
            alpha = int((1.0 - r / 900.0) * 14)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, alpha))

    def _render_editorial_typography(self, draw: ImageDraw.Draw, t: float):
        """Renders clean, large editorial title and subtitle in the upper safe region."""
        if not self.headline:
            return

        top_y = 140
        left_x = 90

        # Headline (Sans Bold 52pt)
        draw.text((left_x, top_y), self.headline.upper(), fill=self.text_primary, font=self.font_title)

        # Subtitle (Georgia Italic 34pt)
        if self.subheadline:
            draw.text((left_x, top_y + 68), self.subheadline, fill=self.accent_blue, font=self.font_subtitle)

    def draw_contact_shadow(self, draw: ImageDraw.Draw, x: float, y: float, w: float, h: float, blur_steps: int = 8):
        """Draws soft contact ambient occlusion shadow on the studio ground plane."""
        for step in range(blur_steps, 0, -1):
            pad = step * 6
            alpha = int(18 / step)
            draw.rounded_rectangle(
                [x - pad, y - pad // 2, x + w + pad, y + h + pad],
                radius=16 + pad,
                fill=(0, 0, 0, alpha)
            )

    def render_physical_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        """Subclasses implement bespoke physical visual objects."""
        pass
