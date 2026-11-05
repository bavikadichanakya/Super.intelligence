"""
SUPER.INTELLIGENCEEE — Editorial Graphics Generator Module
Generates high-aesthetic 1080x1920 vertical editorial technology cards using Pillow.
Zero external API costs; produces cinematic, brand-consistent visual assets.
"""

from __future__ import annotations

import logging
import math
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from core.config import get_config

logger = logging.getLogger("super_intelligence.graphics")


class EditorialGraphicsGenerator:
    """Generates 1080x1920 branded editorial visual cards for Instagram Reels."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.width = 1080
        self.height = 1920

        # Tech Brand Palette
        self.bg_dark = (10, 12, 18)        # #0A0C12
        self.bg_card = (20, 24, 38)        # #141826
        self.cyan = (0, 229, 255)          # #00E5FF
        self.purple = (139, 92, 246)       # #8B5CF6
        self.gold = (255, 215, 0)          # #FFD700
        self.white = (248, 250, 252)       # #F8FAFC
        self.muted = (148, 163, 184)       # #94A3B8
        self.grid_color = (25, 30, 48)     # subtle cyber lines

        # Font resolution
        self.fonts_dir = self.config.resolve_path(self.config.get("paths.fonts_dir", "assets/fonts"))
        self._load_fonts()

    def _load_fonts(self):
        """Loads available system or bundled fonts, falling back safely."""
        self.title_font = None
        self.stat_font = None
        self.body_font = None
        self.brand_font = None

        # Common Windows fonts
        font_candidates = [
            "arial.ttf",
            "arialbd.ttf",
            "seguiemj.ttf",
            "segoeui.ttf",
            "tahoma.ttf",
        ]

        def get_font(size: int, bold: bool = False):
            # Check custom fonts dir first
            for f in self.fonts_dir.glob("*.ttf"):
                try:
                    return ImageFont.truetype(str(f), size)
                except Exception:
                    pass

            # Check Windows system fonts
            sys_font_names = ["arialbd.ttf" if bold else "arial.ttf", "segoeui.ttf", "calibri.ttf"]
            for sfn in sys_font_names:
                try:
                    return ImageFont.truetype(sfn, size)
                except Exception:
                    continue

            return ImageFont.load_default()

        self.font_title = get_font(68, bold=True)
        self.font_stat = get_font(130, bold=True)
        self.font_body = get_font(42, bold=False)
        self.font_brand = get_font(28, bold=True)
        self.font_badge = get_font(32, bold=True)

    def _draw_gradient_background(self, draw: ImageDraw.ImageDraw):
        """Renders a sleek dark blue/purple tech radial or linear gradient."""
        # Simple vertical gradient interpolation
        top_color = (8, 10, 16)
        bottom_color = (18, 22, 36)
        for y in range(0, self.height, 4):
            factor = y / float(self.height)
            r = int(top_color[0] + factor * (bottom_color[0] - top_color[0]))
            g = int(top_color[1] + factor * (bottom_color[1] - top_color[1]))
            b = int(top_color[2] + factor * (bottom_color[2] - top_color[2]))
            draw.rectangle([(0, y), (self.width, y + 4)], fill=(r, g, b))

        # Render subtle cyber tech grid
        step = 120
        for x in range(0, self.width, step):
            draw.line([(x, 0), (x, self.height)], fill=(20, 26, 42), width=1)
        for y in range(0, self.height, step):
            draw.line([(0, y), (self.width, y)], fill=(20, 26, 42), width=1)

    def _draw_brand_header(self, draw: ImageDraw.ImageDraw, category: str = "AI NEWS"):
        """Draws top brand pill and tag (safely below top status bar)."""
        y_pos = 180
        badge_text = f"⚡ SUPER.INTELLIGENCEEE  //  {category.upper()}"

        # Pill background
        pill_w = 720
        pill_h = 56
        pill_x = (self.width - pill_w) // 2
        draw.rounded_rectangle(
            [(pill_x, y_pos), (pill_x + pill_w, y_pos + pill_h)],
            radius=28,
            fill=(18, 26, 44),
            outline=self.cyan,
            width=2,
        )

        draw.text(
            (self.width // 2, y_pos + pill_h // 2),
            badge_text,
            fill=self.cyan,
            font=self.font_brand,
            anchor="mm",
        )

    def _draw_corner_tech_brackets(self, draw: ImageDraw.ImageDraw):
        """Draws HUD-style decorative corner brackets."""
        b_len = 40
        b_pad = 60
        top = 120
        bottom = self.height - 180

        # Top-left
        draw.line([(b_pad, top), (b_pad + b_len, top)], fill=self.cyan, width=3)
        draw.line([(b_pad, top), (b_pad, top + b_len)], fill=self.cyan, width=3)

        # Top-right
        draw.line([(self.width - b_pad, top), (self.width - b_pad - b_len, top)], fill=self.cyan, width=3)
        draw.line([(self.width - b_pad, top), (self.width - b_pad, top + b_len)], fill=self.cyan, width=3)

        # Bottom-left
        draw.line([(b_pad, bottom), (b_pad + b_len, bottom)], fill=self.cyan, width=3)
        draw.line([(b_pad, bottom), (b_pad, bottom - b_len)], fill=self.cyan, width=3)

        # Bottom-right
        draw.line([(self.width - b_pad, bottom), (self.width - b_pad - b_len, bottom)], fill=self.cyan, width=3)
        draw.line([(self.width - b_pad, bottom), (self.width - b_pad, bottom - b_len)], fill=self.cyan, width=3)

    def _wrap_text(self, text: str, max_chars: int = 24) -> List[str]:
        """Wraps text into readable short lines for high-impact viewing."""
        words = text.split()
        lines = []
        current_line = []
        current_len = 0

        for w in words:
            if current_len + len(w) + 1 <= max_chars:
                current_line.append(w)
                current_len += len(w) + 1
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [w]
                current_len = len(w)

        if current_line:
            lines.append(" ".join(current_line))
        return lines

    def create_title_card(
        self,
        title: str,
        category: str = "ARTIFICIAL INTELLIGENCE",
        output_path: Path | str = "title_card.png",
    ) -> Path:
        """Creates the hero title hook card for Scene 1."""
        img = Image.new("RGB", (self.width, self.height), self.bg_dark)
        draw = ImageDraw.Draw(img)

        self._draw_gradient_background(draw)
        self._draw_corner_tech_brackets(draw)
        self._draw_brand_header(draw, category)

        # Center card container
        card_margin = 80
        card_top = 400
        card_bottom = 1400
        draw.rounded_rectangle(
            [(card_margin, card_top), (self.width - card_margin, card_bottom)],
            radius=32,
            fill=(14, 18, 30),
            outline=self.purple,
            width=3,
        )

        # Headline
        wrapped_title = self._wrap_text(title.upper(), max_chars=20)
        line_height = 80
        total_text_h = len(wrapped_title) * line_height
        start_y = card_top + (card_bottom - card_top - total_text_h) // 2

        for i, line in enumerate(wrapped_title):
            # Highlight first word or line in cyan
            color = self.cyan if i == 0 else self.white
            draw.text(
                (self.width // 2, start_y + i * line_height),
                line,
                fill=color,
                font=self.font_title,
                anchor="mm",
            )

        # Bottom hook pulse
        draw.text(
            (self.width // 2, 1460),
            "▶  BREAKING INTEL",
            fill=self.gold,
            font=self.font_badge,
            anchor="mm",
        )

        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(out_path, format="PNG")
        logger.info(f"Generated title card: {out_path.name}")
        return out_path

    def create_stat_card(
        self,
        headline: str,
        stat_number: str,
        context: str,
        output_path: Path | str = "stat_card.png",
    ) -> Path:
        """Creates a high-impact metric or statistic card."""
        img = Image.new("RGB", (self.width, self.height), self.bg_dark)
        draw = ImageDraw.Draw(img)

        self._draw_gradient_background(draw)
        self._draw_corner_tech_brackets(draw)
        self._draw_brand_header(draw, "METRICS & BENCHMARKS")

        # Container
        card_margin = 80
        draw.rounded_rectangle(
            [(card_margin, 460), (self.width - card_margin, 1360)],
            radius=32,
            fill=(14, 18, 32),
            outline=self.cyan,
            width=3,
        )

        # Section Headline
        draw.text(
            (self.width // 2, 580),
            headline.upper(),
            fill=self.muted,
            font=self.font_badge,
            anchor="mm",
        )

        # Giant Stat
        draw.text(
            (self.width // 2, 820),
            stat_number,
            fill=self.cyan,
            font=self.font_stat,
            anchor="mm",
        )

        # Context lines
        wrapped_context = self._wrap_text(context, max_chars=28)
        c_start_y = 1040
        for i, line in enumerate(wrapped_context):
            draw.text(
                (self.width // 2, c_start_y + i * 55),
                line,
                fill=self.white,
                font=self.font_body,
                anchor="mm",
            )

        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(out_path, format="PNG")
        return out_path

    def create_scene_card(
        self,
        scene: Dict[str, Any],
        scene_index: int,
        total_scenes: int,
        output_path: Path | str,
    ) -> Path:
        """Generates the appropriate styled card based on scene data."""
        scene_type = scene.get("scene_type", "tech_b_roll").lower()
        title = scene.get("on_screen_text", scene.get("narration_text", "AI Update"))
        text = scene.get("narration_text", "")

        # Route by scene type
        if scene_index == 1 or "hook" in scene_type:
            return self.create_title_card(title, category="AI BREAKTHROUGH", output_path=output_path)
        elif "stat" in scene_type or "metric" in scene_type:
            # Extract number or use 10x default
            words = text.split()
            found_num = next((w for w in words if any(c.isdigit() for c in w)), "10X")
            return self.create_stat_card("KEY PERFORMANCE METRIC", found_num, text[:120], output_path=output_path)
        elif scene_index == total_scenes or "outro" in scene_type:
            return self.create_outro_card("FOLLOW FOR DAILY AI BRIEFINGS", "@super.intelligenceee", output_path=output_path)
        else:
            # General editorial explanation card
            return self.create_explanation_card(title, text, f"SCENE 0{scene_index}", output_path=output_path)

    def create_explanation_card(
        self,
        headline: str,
        body_text: str,
        step_tag: str,
        output_path: Path | str,
    ) -> Path:
        """Creates an editorial insight card with bulleted or cleanly spaced breakdown."""
        img = Image.new("RGB", (self.width, self.height), self.bg_dark)
        draw = ImageDraw.Draw(img)

        self._draw_gradient_background(draw)
        self._draw_corner_tech_brackets(draw)
        self._draw_brand_header(draw, step_tag)

        # Card container
        card_margin = 80
        draw.rounded_rectangle(
            [(card_margin, 440), (self.width - card_margin, 1380)],
            radius=32,
            fill=(14, 18, 30),
            outline=(45, 55, 85),
            width=2,
        )

        # Headline
        wrapped_h = self._wrap_text(headline.upper(), max_chars=22)
        h_y = 560
        for i, line in enumerate(wrapped_h[:3]):
            draw.text(
                (self.width // 2, h_y + i * 70),
                line,
                fill=self.cyan,
                font=self.font_title,
                anchor="mm",
            )

        # Divider line
        div_y = h_y + len(wrapped_h[:3]) * 70 + 40
        draw.line([(180, div_y), (self.width - 180, div_y)], fill=(40, 50, 80), width=2)

        # Body narration takeaway
        wrapped_body = self._wrap_text(body_text, max_chars=26)
        b_y = div_y + 60
        for i, line in enumerate(wrapped_body[:6]):
            draw.text(
                (self.width // 2, b_y + i * 60),
                line,
                fill=self.white,
                font=self.font_body,
                anchor="mm",
            )

        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(out_path, format="PNG")
        return out_path

    def create_outro_card(
        self,
        call_to_action: str,
        handle: str = "@super.intelligenceee",
        output_path: Path | str = "outro_card.png",
    ) -> Path:
        """Creates the outro call-to-action card."""
        img = Image.new("RGB", (self.width, self.height), self.bg_dark)
        draw = ImageDraw.Draw(img)

        self._draw_gradient_background(draw)
        self._draw_corner_tech_brackets(draw)
        self._draw_brand_header(draw, "DAILY TECH PULSE")

        # Central CTA Box
        draw.rounded_rectangle(
            [(100, 500), (self.width - 100, 1340)],
            radius=36,
            fill=(16, 20, 34),
            outline=self.cyan,
            width=3,
        )

        draw.text(
            (self.width // 2, 650),
            "STAY AHEAD OF THE CURVE",
            fill=self.gold,
            font=self.font_badge,
            anchor="mm",
        )

        wrapped_cta = self._wrap_text(call_to_action.upper(), max_chars=20)
        c_y = 800
        for i, line in enumerate(wrapped_cta):
            draw.text(
                (self.width // 2, c_y + i * 75),
                line,
                fill=self.white,
                font=self.font_title,
                anchor="mm",
            )

        # Handle pill
        pill_w = 640
        pill_h = 70
        p_x = (self.width - pill_w) // 2
        p_y = 1120
        draw.rounded_rectangle(
            [(p_x, p_y), (p_x + pill_w, p_y + pill_h)],
            radius=35,
            fill=(0, 229, 255),
        )
        draw.text(
            (self.width // 2, p_y + pill_h // 2),
            handle.upper(),
            fill=(10, 12, 18),
            font=self.font_badge,
            anchor="mm",
        )

        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(out_path, format="PNG")
        return out_path

