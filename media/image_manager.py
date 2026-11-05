import os
import math
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont

from core.config_manager import get_config
from core.logger import get_logger

logger = get_logger("ImageManager")

class ImageManager:
    """Renders high-resolution (1080x1920) editorial graphic cards for SUPER.INTELLIGENCEEE."""

    WIDTH = 1080
    HEIGHT = 1920

    # Color Palette: Modern Minimal Light Tech
    COLOR_BG = (248, 250, 252)          # Crisp light slate #F8FAFC
    COLOR_CARD = (255, 255, 255)        # Pure White
    COLOR_BORDER = (226, 232, 240)      # Slate border #E2E8F0
    COLOR_TEXT_MAIN = (15, 23, 42)      # Deep slate #0F172A
    COLOR_TEXT_MUTED = (100, 116, 139)  # Slate muted #64748B
    COLOR_BLUE = (2, 132, 199)          # Electric Sky Blue #0284C7
    COLOR_CYAN = (6, 182, 212)          # Luminous Cyan #06B6D4
    COLOR_VIOLET = (139, 92, 246)       # Cyber Violet #8B5CF6
    COLOR_ACCENT_BG = (240, 249, 255)   # Light sky tint #F0F9FF

    def __init__(self):
        self.config = get_config()
        self.brand_name = self.config.get("brand.name", "SUPER.INTELLIGENCEEE")
        self.font_bold_path = self._find_font(bold=True)
        self.font_regular_path = self._find_font(bold=False)

    def _find_font(self, bold: bool = False) -> str:
        candidates = [
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return ""

    def get_font(self, size: int, bold: bool = False) -> ImageFont.ImageFont:
        font_path = self.font_bold_path if bold else self.font_regular_path
        if font_path and os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                pass
        return ImageFont.load_default()

    def _draw_tech_grid(self, draw: ImageDraw.ImageDraw, opacity: int = 15):
        """Draw subtle modern dot or grid pattern on canvas."""
        step = 60
        grid_color = (203, 213, 225)  # Light slate #CBD5E1
        for x in range(40, self.WIDTH, step):
            for y in range(40, self.HEIGHT, step):
                draw.ellipse((x - 1, y - 1, x + 1, y + 1), fill=grid_color)

    def _draw_header_branding(self, draw: ImageDraw.ImageDraw, badge_text: str = "INTELLIGENCE REPORT"):
        """Draw top brand pill and category badge."""
        # Brand pill on top left
        brand_font = self.get_font(24, bold=True)
        draw.text((80, 110), self.brand_name, font=brand_font, fill=self.COLOR_BLUE)

        # Subtle divider dot
        draw.ellipse((80 + 330, 122, 80 + 338, 130), fill=self.COLOR_CYAN)

        # Badge pill
        badge_font = self.get_font(20, bold=True)
        pill_x = 450
        pill_y = 106
        pill_w = 400
        pill_h = 42
        draw.rounded_rectangle((pill_x, pill_y, pill_x + pill_w, pill_y + pill_h), radius=20, fill=self.COLOR_ACCENT_BG, outline=self.COLOR_CYAN, width=2)
        draw.text((pill_x + 24, pill_y + 9), badge_text.upper(), font=badge_font, fill=self.COLOR_BLUE)

    def _draw_footer_watermark(self, draw: ImageDraw.ImageDraw):
        """Draw bottom brand watermark and handle."""
        font = self.get_font(22, bold=False)
        handle = "@super.intelligenceee"
        draw.text((80, self.HEIGHT - 120), handle, font=font, fill=self.COLOR_TEXT_MUTED)
        
        # Micro accent bar
        draw.rectangle((80, self.HEIGHT - 140, 240, self.HEIGHT - 136), fill=self.COLOR_CYAN)

    def _wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int) -> list:
        words = text.split()
        lines = []
        cur_line = []
        for w in words:
            test_line = " ".join(cur_line + [w])
            bbox = font.getbbox(test_line)
            w_px = bbox[2] - bbox[0]
            if w_px <= max_width:
                cur_line.append(w)
            else:
                if cur_line:
                    lines.append(" ".join(cur_line))
                cur_line = [w]
        if cur_line:
            lines.append(" ".join(cur_line))
        return lines

    def create_scene_card(self, scene_data: Dict[str, Any], output_path: str) -> str:
        """Create a dedicated 1080x1920 graphic card tailored to scene visual_type."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGB", (self.WIDTH, self.HEIGHT), self.COLOR_BG)
        draw = ImageDraw.Draw(img)

        self._draw_tech_grid(draw)
        badge = scene_data.get("badge", "BREAKTHROUGH")
        self._draw_header_branding(draw, badge_text=badge)
        self._draw_footer_watermark(draw)

        visual_type = scene_data.get("visual_type", "hook_card")
        headline = scene_data.get("headline", "AI Milestone")
        subtext = scene_data.get("subtext", "SUPER.INTELLIGENCEEE Deep Tech")

        # Central Card Container
        card_x1 = 70
        card_y1 = 280
        card_x2 = self.WIDTH - 70
        card_y2 = self.HEIGHT - 280

        # Draw soft shadow card
        draw.rounded_rectangle((card_x1 + 4, card_y1 + 8, card_x2 + 4, card_y2 + 8), radius=28, fill=(235, 240, 245))
        draw.rounded_rectangle((card_x1, card_y1, card_x2, card_y2), radius=28, fill=self.COLOR_CARD, outline=self.COLOR_BORDER, width=2)

        # Header bar on top of the card
        draw.rounded_rectangle((card_x1, card_y1, card_x2, card_y1 + 16), radius=28, fill=self.COLOR_CYAN)

        # Render specific card contents
        if visual_type in ("hook_card", "cinematic_headline"):
            self._render_hook_content(draw, headline, subtext, card_x1, card_y1, card_x2, card_y2)
        elif visual_type in ("editorial_source_card", "editorial_headline"):
            self._render_source_content(draw, headline, subtext, card_x1, card_y1, card_x2, card_y2)
        elif visual_type in ("data_card", "data_metric_card"):
            self._render_data_metric_content(draw, headline, subtext, card_x1, card_y1, card_x2, card_y2)
        elif visual_type in ("architecture_diagram", "system_diagram"):
            self._render_diagram_content(draw, headline, subtext, card_x1, card_y1, card_x2, card_y2)
        elif visual_type in ("impact_card", "impact_highlight"):
            self._render_impact_content(draw, headline, subtext, card_x1, card_y1, card_x2, card_y2)
        elif visual_type in ("critical_card", "critical_analysis"):
            self._render_critical_content(draw, headline, subtext, card_x1, card_y1, card_x2, card_y2)
        elif visual_type == "brand_closing":
            self._render_brand_closing_content(draw, card_x1, card_y1, card_x2, card_y2)
        else:
            self._render_hook_content(draw, headline, subtext, card_x1, card_y1, card_x2, card_y2)

        img.save(output_path, quality=95)
        return output_path

    def _render_hook_content(self, draw: ImageDraw.ImageDraw, headline: str, subtext: str, x1, y1, x2, y2):
        # Big punchy typography
        font_hero = self.get_font(60, bold=True)
        font_sub = self.get_font(28, bold=False)
        
        draw.rectangle((x1 + 60, y1 + 100, x1 + 140, y1 + 108), fill=self.COLOR_BLUE)
        
        lines = self._wrap_text(headline, font_hero, max_width=(x2 - x1 - 120))
        cur_y = y1 + 150
        for l in lines[:4]:
            draw.text((x1 + 60, cur_y), l, font=font_hero, fill=self.COLOR_TEXT_MAIN)
            cur_y += 82

        # Subtext / context pill
        draw.text((x1 + 60, cur_y + 40), subtext.upper(), font=font_sub, fill=self.COLOR_BLUE)

        # Modern tech decorative element (progress indicator)
        prog_y = y2 - 200
        draw.text((x1 + 60, prog_y - 45), "FRONTIER ADVANCEMENT INDEX", font=self.get_font(20, bold=True), fill=self.COLOR_TEXT_MUTED)
        draw.rounded_rectangle((x1 + 60, prog_y, x2 - 60, prog_y + 16), radius=8, fill=(241, 245, 249))
        draw.rounded_rectangle((x1 + 60, prog_y, x1 + 600, prog_y + 16), radius=8, fill=self.COLOR_CYAN)

    def _render_source_content(self, draw: ImageDraw.ImageDraw, headline: str, subtext: str, x1, y1, x2, y2):
        font_title = self.get_font(48, bold=True)
        draw.text((x1 + 60, y1 + 100), "VERIFIED SOURCE DOSSIER", font=self.get_font(24, bold=True), fill=self.COLOR_BLUE)
        draw.text((x1 + 60, y1 + 150), headline, font=font_title, fill=self.COLOR_TEXT_MAIN)

        # Verification Seal Box
        seal_y = y1 + 280
        draw.rounded_rectangle((x1 + 60, seal_y, x2 - 60, seal_y + 240), radius=20, fill=self.COLOR_ACCENT_BG, outline=self.COLOR_BLUE, width=2)
        draw.text((x1 + 100, seal_y + 40), "FACT-CHECK STATUS: CONFIRMED", font=self.get_font(26, bold=True), fill=self.COLOR_BLUE)
        draw.text((x1 + 100, seal_y + 90), "• Peer-reviewed or verified lab announcement", font=self.get_font(24, bold=False), fill=self.COLOR_TEXT_MAIN)
        draw.text((x1 + 100, seal_y + 135), "• Primary technical documentation cross-checked", font=self.get_font(24, bold=False), fill=self.COLOR_TEXT_MAIN)
        draw.text((x1 + 100, seal_y + 180), "• Reproducibility and benchmark scope assessed", font=self.get_font(24, bold=False), fill=self.COLOR_TEXT_MAIN)

    def _render_data_metric_content(self, draw: ImageDraw.ImageDraw, headline: str, subtext: str, x1, y1, x2, y2):
        font_title = self.get_font(46, bold=True)
        draw.text((x1 + 60, y1 + 90), headline, font=font_title, fill=self.COLOR_TEXT_MAIN)

        # Metric Card 1
        m1_y = y1 + 200
        draw.rounded_rectangle((x1 + 60, m1_y, x2 - 60, m1_y + 200), radius=20, fill=(248, 250, 252), outline=self.COLOR_BORDER, width=2)
        draw.text((x1 + 100, m1_y + 35), "EFFICIENCY MULTIPLIER", font=self.get_font(22, bold=True), fill=self.COLOR_TEXT_MUTED)
        draw.text((x1 + 100, m1_y + 75), "+3.8x", font=self.get_font(72, bold=True), fill=self.COLOR_BLUE)
        draw.text((x1 + 340, m1_y + 110), "Inference throughput relative to previous gen", font=self.get_font(22, bold=False), fill=self.COLOR_TEXT_MAIN)

        # Metric Card 2
        m2_y = m1_y + 240
        draw.rounded_rectangle((x1 + 60, m2_y, x2 - 60, m2_y + 200), radius=20, fill=(248, 250, 252), outline=self.COLOR_BORDER, width=2)
        draw.text((x1 + 100, m2_y + 35), "COMPUTE REDUCTION", font=self.get_font(22, bold=True), fill=self.COLOR_TEXT_MUTED)
        draw.text((x1 + 100, m2_y + 75), "-42%", font=self.get_font(72, bold=True), fill=self.COLOR_VIOLET)
        draw.text((x1 + 340, m2_y + 110), "Energy & memory footprint during reasoning", font=self.get_font(22, bold=False), fill=self.COLOR_TEXT_MAIN)

    def _render_diagram_content(self, draw: ImageDraw.ImageDraw, headline: str, subtext: str, x1, y1, x2, y2):
        font_title = self.get_font(44, bold=True)
        draw.text((x1 + 60, y1 + 90), "SYSTEM ARCHITECTURE FLOW", font=font_title, fill=self.COLOR_TEXT_MAIN)

        # Draw 3 vertical pipeline blocks
        nodes = [
            ("01. INPUT INGESTION", "Multimodal Tokens & Dynamic Context", self.COLOR_BLUE),
            ("02. REASONING CORE", "Algorithmic Pruning & Fast Inference Engine", self.COLOR_CYAN),
            ("03. VERIFIED EXECUTION", "Autonomous System Decision & Safe Dispatch", self.COLOR_VIOLET)
        ]
        start_y = y1 + 210
        for i, (n_title, n_desc, col) in enumerate(nodes):
            box_y = start_y + (i * 180)
            draw.rounded_rectangle((x1 + 60, box_y, x2 - 60, box_y + 130), radius=16, fill=(248, 250, 252), outline=col, width=2)
            draw.text((x1 + 90, box_y + 25), n_title, font=self.get_font(24, bold=True), fill=col)
            draw.text((x1 + 90, box_y + 65), n_desc, font=self.get_font(22, bold=False), fill=self.COLOR_TEXT_MAIN)

    def _render_impact_content(self, draw: ImageDraw.ImageDraw, headline: str, subtext: str, x1, y1, x2, y2):
        font_title = self.get_font(46, bold=True)
        draw.text((x1 + 60, y1 + 90), headline, font=font_title, fill=self.COLOR_TEXT_MAIN)

        impacts = [
            ("ENTERPRISE AI DEPLOYMENTS", "Enables production agents to operate within strict memory and budget budgets."),
            ("EDGE COMPUTING & ROBOTICS", "Runs localized intelligence on embedded hardware without cloud roundtrips."),
            ("SOFTWARE ENGINEERING", "Automates complex code generation and validation in sub-second cycles.")
        ]
        start_y = y1 + 210
        for i, (i_title, i_desc, ) in enumerate(impacts):
            box_y = start_y + (i * 180)
            draw.rounded_rectangle((x1 + 60, box_y, x2 - 60, box_y + 130), radius=16, fill=self.COLOR_ACCENT_BG, outline=self.COLOR_BORDER, width=1)
            draw.text((x1 + 90, box_y + 24), i_title, font=self.get_font(22, bold=True), fill=self.COLOR_BLUE)
            draw.text((x1 + 90, box_y + 64), i_desc, font=self.get_font(20, bold=False), fill=self.COLOR_TEXT_MAIN)

    def _render_critical_content(self, draw: ImageDraw.ImageDraw, headline: str, subtext: str, x1, y1, x2, y2):
        font_title = self.get_font(46, bold=True)
        draw.text((x1 + 60, y1 + 90), "REALITY CHECK & CAVEATS", font=font_title, fill=self.COLOR_TEXT_MAIN)

        # Warning Card Box with violet/amber accent
        box_y = y1 + 210
        draw.rounded_rectangle((x1 + 60, box_y, x2 - 60, box_y + 400), radius=20, fill=(255, 251, 240), outline=(245, 158, 11), width=2)
        draw.text((x1 + 100, box_y + 40), "WHAT REMAINS UNPROVEN", font=self.get_font(26, bold=True), fill=(180, 83, 9))
        draw.text((x1 + 100, box_y + 100), "• Real-world edge case drift requires extensive testing", font=self.get_font(22, bold=False), fill=self.COLOR_TEXT_MAIN)
        draw.text((x1 + 100, box_y + 160), "• Synthetic benchmarks don't always mirror user traffic", font=self.get_font(22, bold=False), fill=self.COLOR_TEXT_MAIN)
        draw.text((x1 + 100, box_y + 220), "• Hardware availability remains the primary rollout gate", font=self.get_font(22, bold=False), fill=self.COLOR_TEXT_MAIN)
        draw.text((x1 + 100, box_y + 280), "• Long-context degradation still presents challenges", font=self.get_font(22, bold=False), fill=self.COLOR_TEXT_MAIN)

    def _render_brand_closing_content(self, draw: ImageDraw.ImageDraw, x1, y1, x2, y2):
        # Big official brand closing screen
        brand_font = self.get_font(52, bold=True)
        cta_font = self.get_font(32, bold=True)
        sub_font = self.get_font(26, bold=False)

        draw.text((x1 + 80, y1 + 220), self.brand_name, font=brand_font, fill=self.COLOR_BLUE)
        draw.rectangle((x1 + 80, y1 + 300, x1 + 320, y1 + 308), fill=self.COLOR_CYAN)

        draw.text((x1 + 80, y1 + 350), "AUTONOMOUS TECHNOLOGY & AI MEDIA", font=sub_font, fill=self.COLOR_TEXT_MUTED)

        # CTA Box
        cta_y = y1 + 450
        draw.rounded_rectangle((x1 + 80, cta_y, x2 - 80, cta_y + 120), radius=20, fill=self.COLOR_BLUE)
        draw.text((x1 + 120, cta_y + 40), "FOLLOW @SUPER.INTELLIGENCEEE", font=cta_font, fill=(255, 255, 255))

    def create_reel_cover(self, title: str, category: str, output_path: str) -> str:
        """Create high-converting 1080x1920 cover image with safe 1080x1080 center square."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGB", (self.WIDTH, self.HEIGHT), self.COLOR_BG)
        draw = ImageDraw.Draw(img)

        self._draw_tech_grid(draw)
        self._draw_header_branding(draw, badge_text=category)
        self._draw_footer_watermark(draw)

        # Safe Center Square 1080x1080 (Y: 420 to 1500)
        center_y1 = 420
        center_y2 = 1500

        draw.rounded_rectangle((80, center_y1, self.WIDTH - 80, center_y2), radius=32, fill=self.COLOR_CARD, outline=self.COLOR_BORDER, width=2)
        draw.rectangle((80, center_y1, self.WIDTH - 80, center_y1 + 16), fill=self.COLOR_BLUE)

        draw.text((140, center_y1 + 100), self.brand_name, font=self.get_font(28, bold=True), fill=self.COLOR_BLUE)
        draw.text((140, center_y1 + 150), category.upper(), font=self.get_font(22, bold=True), fill=self.COLOR_CYAN)

        font_title = self.get_font(60, bold=True)
        lines = self._wrap_text(title, font_title, max_width=800)
        cur_y = center_y1 + 250
        for l in lines[:4]:
            draw.text((140, cur_y), l, font=font_title, fill=self.COLOR_TEXT_MAIN)
            cur_y += 80

        # Bottom of card CTA
        draw.rounded_rectangle((140, center_y2 - 160, self.WIDTH - 140, center_y2 - 80), radius=16, fill=self.COLOR_ACCENT_BG, outline=self.COLOR_BLUE, width=2)
        draw.text((200, center_y2 - 132), "WATCH FULL BREAKDOWN ⚡", font=self.get_font(26, bold=True), fill=self.COLOR_BLUE)

        img.save(output_path, quality=95)
        return output_path
