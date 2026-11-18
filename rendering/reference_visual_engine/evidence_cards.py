"""
SUPER.INTELLIGENCEEE — Phase 5 Evidence & Screenshot Cards
Authentic primary source presentation components:
1. GitHubRepoCard: Floating repository card with real stars, license, language breakdown, and topics
2. DocumentationFigureViewer: Displays genuine repo figures (docs/images/*) with focus zoom & badges
3. SideBySideComparisonCard: Determinism comparison (laptop vs workstation, 0 chars different)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from rendering.native_motion_engine.primitives import (
    clamp,
    ease_out_back,
    ease_out_cubic,
    get_progress,
    scale_in,
)


class GitHubRepoCard:
    """
    Renders an authentic, floating GitHub repository card (like FareedKhan-dev / kimi-k3-in-c in Scene 3).
    """

    def __init__(self):
        try:
            self.font_title = ImageFont.truetype("arialbd.ttf", 26)
            self.font_body = ImageFont.truetype("arial.ttf", 18)
            self.font_mono = ImageFont.truetype("consola.ttf", 15)
            self.font_badge = ImageFont.truetype("arialbd.ttf", 13)
        except Exception:
            self.font_title = ImageFont.load_default()
            self.font_body = ImageFont.load_default()
            self.font_mono = ImageFont.load_default()
            self.font_badge = ImageFont.load_default()

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        repo_name: str = "FareedKhan-dev / kimi-k3-in-c",
        description: str = "A 2.78-trillion-parameter Kimi K3 running inference on a single CPU in 8.24 GB of RAM. Portable C99: no BLAS, no framework, no GPU.",
        topics: Optional[List[str]] = None,
        language: str = "C 71.5%",
        license_name: str = "Apache-2.0 license",
        version: str = "v1.1.0",
        top_y: int = 340,
        t: float = 1.0,
    ) -> Tuple[int, int, int, int]:
        cx0, cy0 = 60, top_y
        cx1, cy1 = 1020, top_y + 440

        # Scale in animation
        s = scale_in(t, 0.1, 0.45)
        if s <= 0.01:
            return (cx0, cy0, cx1, cy1)

        # Drop shadow
        draw.rounded_rectangle([cx0 + 8, cy0 + 10, cx1 + 8, cy1 + 10], radius=24, fill=(200, 208, 218, 120))
        # Card body (clean white)
        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

        # Octocat icon circle
        draw.circle((cx0 + 52, cy0 + 54), radius=22, fill=(15, 23, 42))
        draw.text((cx0 + 44, cy0 + 42), "🐙", font=self.font_title)

        # Repo title
        draw.text((cx0 + 88, cy0 + 40), repo_name, font=self.font_title, fill=(15, 23, 42))

        # 'Public' pill badge
        title_w = draw.textlength(repo_name, font=self.font_title)
        bx = cx0 + 96 + int(title_w)
        draw.rounded_rectangle([bx, cy0 + 42, bx + 64, cy0 + 68], radius=6, outline=(203, 213, 225), width=1)
        draw.text((bx + 10, cy0 + 46), "Public", font=self.font_badge, fill=(100, 116, 139))

        # Description text
        desc_lines = [
            description[:68],
            description[68:136],
            description[136:200],
        ]
        for i, line in enumerate(desc_lines):
            if line:
                draw.text((cx0 + 36, cy0 + 96 + i * 28), line.strip(), font=self.font_body, fill=(51, 65, 85))

        # Topic tag pills
        tag_list = topics or ["avx2", "c99", "cpu-inference", "from-scratch", "inference-engine", "kimi-k3", "mixture-of-experts"]
        tx = cx0 + 36
        ty = cy0 + 195
        for tag in tag_list[:8]:
            tag_text = tag
            tw = draw.textlength(tag_text, font=self.font_badge)
            pw = int(tw + 20)
            if tx + pw > cx1 - 36:
                tx = cx0 + 36
                ty += 40
            draw.rounded_rectangle([tx, ty, tx + pw, ty + 32], radius=16, fill=(241, 245, 249))
            draw.text((tx + 10, ty + 7), tag_text, font=self.font_badge, fill=(2, 132, 199))
            tx += pw + 10

        # Footer divider line
        draw.line([(cx0 + 36, cy1 - 56), (cx1 - 36, cy1 - 56)], fill=(226, 232, 240), width=1)

        # Footer: Language dot, License, Version
        # C language dot (dark gray/blue)
        draw.circle((cx0 + 44, cy1 - 34), radius=6, fill=(85, 85, 85))
        draw.text((cx0 + 56, cy1 - 42), language, font=self.font_mono, fill=(71, 85, 105))

        # License
        draw.text((cx0 + 220, cy1 - 42), f"⚖ {license_name}", font=self.font_mono, fill=(71, 85, 105))

        # Version tag
        draw.text((cx1 - 140, cy1 - 42), f"🏷 {version}", font=self.font_mono, fill=(100, 116, 139))

        return (cx0, cy0, cx1, cy1)


class DocumentationFigureViewer:
    """
    Displays genuine repository documentation figures (e.g. binary_sizes.png or bytes_census.png).
    Features a top 'FROM THE REPO' pill badge and an animated focus selection rectangle.
    """

    def __init__(self):
        try:
            self.font_badge = ImageFont.truetype("arialbd.ttf", 13)
            self.font_mono = ImageFont.truetype("consola.ttf", 14)
        except Exception:
            self.font_badge = ImageFont.load_default()
            self.font_mono = ImageFont.load_default()

    def render(
        self,
        base_img: Image.Image,
        figure_path: Path,
        repo_subpath: str = "docs/images/binary_sizes.png",
        center_y: int = 700,
        focus_rect: Optional[Tuple[int, int, int, int]] = None,
        t: float = 1.0,
    ):
        draw = ImageDraw.Draw(base_img)

        # Top Source Badge: [FROM THE REPO] docs/images/...
        bx = 60
        by = center_y - 330
        draw.rounded_rectangle([bx, by, bx + 160, by + 32], radius=6, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
        draw.text((bx + 12, by + 7), "FROM THE REPO", font=self.font_badge, fill=(180, 83, 9))
        draw.text((bx + 175, by + 7), repo_subpath, font=self.font_mono, fill=(71, 85, 105))

        if not figure_path.exists():
            return

        # Load and scale figure to width ~960px
        with Image.open(figure_path) as fig:
            target_w = 960
            aspect = fig.height / fig.width
            target_h = int(target_w * aspect)

            # Cap height to prevent intrusion into caption territory
            if target_h > 620:
                target_h = 620
                target_w = int(target_h / aspect)

            fig_resized = fig.resize((target_w, target_h), Image.Resampling.LANCZOS)
            px = (1080 - target_w) // 2
            py = center_y - target_h // 2 + 20

            # Subtle drop shadow
            draw.rounded_rectangle([px - 4, py - 4, px + target_w + 4, py + target_h + 4], radius=16, fill=(210, 218, 225, 120))
            base_img.paste(fig_resized, (px, py))
            draw.rounded_rectangle([px, py, px + target_w, py + target_h], radius=12, outline=(203, 213, 225), width=2)

            # Animated Focus Selection Box if provided
            if focus_rect and t > 0.4:
                p_focus = get_progress(t, 0.4, 0.4, "ease_out_back")
                fx0, fy0, fx1, fy1 = focus_rect
                # Scale relative to placed image
                abs_fx0 = px + int(fx0 * (target_w / fig.width))
                abs_fy0 = py + int(fy0 * (target_h / fig.height))
                abs_fx1 = px + int(fx1 * (target_w / fig.width))
                abs_fy1 = py + int(fy1 * (target_h / fig.height))

                cx = (abs_fx0 + abs_fx1) / 2.0
                cy = (abs_fy0 + abs_fy1) / 2.0
                hw = ((abs_fx1 - abs_fx0) / 2.0) * p_focus
                hh = ((abs_fy1 - abs_fy0) / 2.0) * p_focus

                draw.rectangle([cx - hw, cy - hh, cx + hw, cy + hh], outline=(2, 132, 199), width=3)
                # Corner dots
                for dx, dy in [(cx - hw, cy - hh), (cx + hw, cy - hh), (cx - hw, cy + hh), (cx + hw, cy + hh)]:
                    draw.rectangle([dx - 4, dy - 4, dx + 4, dy + 4], fill=(255, 255, 255), outline=(2, 132, 199), width=1)


class SideBySideComparisonCard:
    """
    Renders laptop vs workstation determinism cards with green equality badge.
    """

    def __init__(self):
        try:
            self.font_header = ImageFont.truetype("arialbd.ttf", 20)
            self.font_code = ImageFont.truetype("consola.ttf", 18)
            self.font_badge = ImageFont.truetype("arialbd.ttf", 14)
            self.font_mono = ImageFont.truetype("consola.ttf", 13)
        except Exception:
            self.font_header = ImageFont.load_default()
            self.font_code = ImageFont.load_default()
            self.font_badge = ImageFont.load_default()
            self.font_mono = ImageFont.load_default()

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        t: float = 1.0,
        center_y: int = 760,
    ):
        card_w = 440
        card_h = 420
        c1_x0 = 60
        c2_x0 = 580

        # Top Verification Pill: ✓ 0 characters different
        pill_w = 260
        px = 540 - pill_w // 2
        py = center_y - 280
        draw.rounded_rectangle([px, py, px + pill_w, py + 40], radius=8, fill=(15, 23, 42))
        draw.text((px + 24, py + 10), "✓  0 characters different", font=self.font_badge, fill=(255, 255, 255))

        # Left Card: Laptop
        draw.rounded_rectangle([c1_x0 + 6, center_y - 220 + 8, c1_x0 + card_w + 6, center_y - 220 + card_h + 8], radius=20, fill=(210, 218, 225, 110))
        draw.rounded_rectangle([c1_x0, center_y - 220, c1_x0 + card_w, center_y - 220 + card_h], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

        draw.text((c1_x0 + 30, center_y - 190), "💻 laptop", font=self.font_header, fill=(15, 23, 42))
        draw.text((c1_x0 + 30, center_y - 160), "smallest preset · 1 RAM DIMM", font=self.font_mono, fill=(100, 116, 139))

        # Output Box
        draw.rounded_rectangle([c1_x0 + 20, center_y - 80, c1_x0 + card_w - 20, center_y + 160], radius=12, fill=(248, 250, 252), outline=(34, 197, 94), width=2)
        draw.text((c1_x0 + 36, center_y - 65), "OUTPUT", font=self.font_mono, fill=(71, 85, 105))
        draw.text((c1_x0 + 36, center_y - 30), "if n <= 1:\n    return n", font=self.font_code, fill=(22, 101, 52))
        draw.circle((c1_x0 + card_w - 45, center_y - 60), radius=12, fill=(34, 197, 94))
        draw.text((c1_x0 + card_w - 51, center_y - 68), "✓", fill=(255, 255, 255))

        # Right Card: Workstation
        draw.rounded_rectangle([c2_x0 + 6, center_y - 220 + 8, c2_x0 + card_w + 6, center_y - 220 + card_h + 8], radius=20, fill=(210, 218, 225, 110))
        draw.rounded_rectangle([c2_x0, center_y - 220, c2_x0 + card_w, center_y - 220 + card_h], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

        draw.text((c2_x0 + 30, center_y - 190), "🖥 workstation", font=self.font_header, fill=(15, 23, 42))
        draw.text((c2_x0 + 30, center_y - 160), "128 GB of RAM · 16 DIMMs", font=self.font_mono, fill=(100, 116, 139))

        # Output Box
        draw.rounded_rectangle([c2_x0 + 20, center_y - 80, c2_x0 + card_w - 20, center_y + 160], radius=12, fill=(248, 250, 252), outline=(34, 197, 94), width=2)
        draw.text((c2_x0 + 36, center_y - 65), "OUTPUT", font=self.font_mono, fill=(71, 85, 105))
        draw.text((c2_x0 + 36, center_y - 30), "if n <= 1:\n    return n", font=self.font_code, fill=(22, 101, 52))
        draw.circle((c2_x0 + card_w - 45, center_y - 60), radius=12, fill=(34, 197, 94))
        draw.text((c2_x0 + card_w - 51, center_y - 68), "✓", fill=(255, 255, 255))

        # Center Equality Circle Badge: =
        draw.circle((540, center_y + 40), radius=28, fill=(34, 197, 94))
        draw.text((531, center_y + 24), "=", font=self.font_header, fill=(255, 255, 255))
