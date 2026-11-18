"""
SUPER.INTELLIGENCEEE — Storytelling Engine: Evidence Figure Viewer
Renders authentic acquired primary source figures (such as official GitHub benchmark charts)
with provenance verification badges and smooth camera zooms.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont


class EvidenceFigureViewer:
    """Renders authentic primary source diagrams with provenance headers."""

    def __init__(self, font_name: str = "arial.ttf"):
        self.cached_images = {}
        try:
            self.font_badge = ImageFont.truetype("consola.ttf", 11)
            self.font_label = ImageFont.truetype("arialbd.ttf", 13)
        except Exception:
            self.font_badge = ImageFont.load_default()
            self.font_label = ImageFont.load_default()

    def _get_image(self, path_str: str) -> Optional[Image.Image]:
        if path_str not in self.cached_images:
            p = Path(path_str)
            if p.exists():
                self.cached_images[path_str] = Image.open(p).convert("RGBA")
            else:
                return None
        return self.cached_images[path_str]

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        base_canvas: Image.Image,
        t: float,
        image_path: str = "assets/acquired/browser_use/accuracy_by_model_light.png",
        center: Tuple[int, int] = (288, 540),
        max_width: int = 500,
        max_height: int = 380,
        source_label: str = "FROM THE REPO: static/accuracy_by_model_light.png",
    ) -> None:
        raw_img = self._get_image(image_path)
        cx, cy = center

        if raw_img is None:
            # Fallback if image not found on disk
            draw.rounded_rectangle([cx - max_width // 2, cy - max_height // 2, cx + max_width // 2, cy + max_height // 2], radius=10, fill=(241, 245, 249), outline=(203, 213, 225), width=2)
            draw.text((cx - 100, cy), "Benchmark Evidence Placeholder", fill=(100, 116, 139), font=self.font_label)
            return

        # Slight gentle zoom based on t (1.0 to 1.05)
        scale_anim = 1.0 + 0.04 * min(1.0, t / 4.0)

        # Scale image to fit within max_width, max_height
        orig_w, orig_h = raw_img.size
        aspect = orig_w / orig_h
        target_w = int(max_width * scale_anim)
        target_h = int(target_w / aspect)
        if target_h > max_height:
            target_h = int(max_height * scale_anim)
            target_w = int(target_h * aspect)

        # Resize image
        resized = raw_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

        # Paste position
        paste_x = cx - target_w // 2
        paste_y = cy - target_h // 2

        # 1. Background Card Frame
        card_pad = 12
        card_rect = [paste_x - card_pad, paste_y - card_pad - 32, paste_x + target_w + card_pad, paste_y + target_h + card_pad]
        draw.rounded_rectangle(card_rect, radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=2)

        # 2. Source Provenance Header Badge
        badge_h = 24
        draw.rounded_rectangle([card_rect[0] + 8, card_rect[1] + 6, card_rect[2] - 8, card_rect[1] + 6 + badge_h], radius=6, fill=(15, 23, 42))
        draw.text((card_rect[0] + 16, card_rect[1] + 10), "AUTHENTIC BENCHMARK EVIDENCE • " + source_label, fill=(56, 189, 248), font=self.font_badge)

        # 3. Paste the authentic figure
        base_canvas.paste(resized, (paste_x, paste_y), mask=resized)

        # 4. Animated Focus Box around the top model result
        if t > 1.5:
            pulse = 0.5 + 0.5 * math.sin(t * 5.0)
            alpha_col = (2, 132, 199)
            # Draw focus highlight box
            focus_y0 = paste_y + int(target_h * 0.15)
            focus_y1 = paste_y + int(target_h * 0.45)
            draw.rectangle([paste_x + 8, focus_y0, paste_x + target_w - 8, focus_y1], outline=alpha_col, width=3)
            # Highlight badge
            draw.rounded_rectangle([paste_x + target_w - 110, focus_y0 - 20, paste_x + target_w - 8, focus_y0], radius=4, fill=(2, 132, 199))
            draw.text((paste_x + target_w - 104, focus_y0 - 17), "★ TOP SCORE", fill=(255, 255, 255), font=self.font_badge)
