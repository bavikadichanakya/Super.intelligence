"""
SUPER.INTELLIGENCEEE — Storytelling Engine: Browser-Use Narrative Compositions
7 distinct, explanation-driven scene compositions explaining 'browser-use':
1. BrowserUseHookComposition (Dark Theme, Full-bleed Glowing Browser, Cursor Click)
2. BrowserUseProblemScraperComposition (Light Theme, Brittle Raw HTML DOM Failure)
3. BrowserUseVisionTaggingComposition (Light Theme, Vision Bounding Boxes [1], [2], [3])
4. BrowserUseCDPConduitComposition (Light Theme, Chrome DevTools Protocol WebSocket Bus)
5. BrowserUsePythonREPLComposition (Light Theme, Python Code-As-Actions Execution)
6. BrowserUseBenchmarkEvidenceComposition (Light Theme, Authentic Acquired Benchmark Chart)
7. BrowserUseLoopConclusionComposition (Dark Theme, Booking Complete & Seamless Loop)
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from core.universal_scene_contract import UniversalSceneContract
from rendering.native_motion_engine.compositions import BaseMotionComposition
from rendering.reference_visual_engine.kinetic_typography import (
    KineticWord,
    ReferenceKineticTypography,
)
from rendering.storytelling_engine.browser_viewport import (
    BrowserViewport,
    InteractiveElementBox,
)
from rendering.storytelling_engine.cdp_protocol_bus import CDPProtocolBus
from rendering.storytelling_engine.evidence_figure_viewer import EvidenceFigureViewer
from rendering.storytelling_engine.repl_code_terminal import REPLCodeTerminal
from rendering.subtitle_layout import BoundingBox


# =============================================================================
# 1. SCENE 1: HOOK (Dark Theme, Glowing Browser, Autonomous Cursor Glide & Click)
# =============================================================================
class BrowserUseHookComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 576, height: int = 1024):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.browser = BrowserViewport()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=30, y0=60, x1=546, y1=210, label="kinetic_headline"),
            BoundingBox(x0=36, y0=220, x1=540, y1=660, label="hero_browser_viewport"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (10, 13, 20, 255))
        draw = ImageDraw.Draw(img)

        # 1. Subtle dark grid
        grid_step = 36
        for gx in range(0, self.width, grid_step):
            draw.line([(gx, 0), (gx, self.height)], fill=(20, 30, 45, 100), width=1)
        for gy in range(0, self.height, grid_step):
            draw.line([(0, gy), (self.width, gy)], fill=(20, 30, 45, 100), width=1)

        # 2. Central blue radial glow
        draw.ellipse([100, 260, 476, 640], fill=(2, 132, 199, 30))

        # 3. Kinetic Headline: "AI can now control your entire [web browser]"
        words = [
            KineticWord("AI can now", is_bold=True),
            KineticWord("control", is_serif_italic=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=self.width // 2, top_y=75, t=t, is_dark_theme=True)

        if t > 1.2:
            words2 = [
                KineticWord("your entire", is_bold=True),
                KineticWord("web browser", is_bold=True, is_highlight_box=True),
            ]
            self.kinetics.render_headline(draw, words2, center_x=self.width // 2, top_y=130, t=t - 1.2, is_dark_theme=True)

        # 4. Animate Cursor: Glides from (120, 300) to Search Button (288, 460)
        flight_btn_pos = (288.0, 455.0)
        if t < 1.0:
            cursor_pos = (120.0, 300.0)
            is_clicking = False
            click_prog = 0.0
        elif t < 2.5:
            move_prog = (t - 1.0) / 1.5
            smooth_prog = 0.5 - 0.5 * math.cos(move_prog * math.pi)
            cx = 120.0 + smooth_prog * (flight_btn_pos[0] - 120.0)
            cy = 300.0 + smooth_prog * (flight_btn_pos[1] - 300.0)
            cursor_pos = (cx, cy)
            is_clicking = False
            click_prog = 0.0
        else:
            cursor_pos = flight_btn_pos
            is_clicking = True
            click_prog = min(1.0, (t - 2.5) * 2.0)

        # 5. Render Browser Viewport
        self.browser.render(
            draw=draw,
            bounds=(36, 220, 540, 640),
            url="https://booking.com/flights",
            is_dark_theme=True,
            show_vision_tags=(t > 2.0),
            active_tag_id=3 if (t > 2.5) else None,
            cursor_pos=cursor_pos,
            is_clicking=is_clicking,
            click_progress=click_prog,
        )

        return img


# =============================================================================
# 2. SCENE 2: THE PROBLEM (Light Theme, Brittle HTML DOM Failure)
# =============================================================================
class BrowserUseProblemScraperComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 576, height: int = 1024):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        try:
            self.font_code = ImageFont.truetype("consola.ttf", 11)
            self.font_alert = ImageFont.truetype("arialbd.ttf", 13)
        except Exception:
            self.font_code = ImageFont.load_default()
            self.font_alert = ImageFont.load_default()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=30, y0=60, x1=546, y1=210, label="kinetic_headline"),
            BoundingBox(x0=36, y0=220, x1=540, y1=660, label="raw_dom_wall"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        # Warm light ivory background
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)

        # Kinetic Headline: "Traditional scrapers break on messy, raw [HTML DOMs]"
        words = [
            KineticWord("Traditional scrapers", is_bold=True),
            KineticWord("break", is_serif_italic=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=self.width // 2, top_y=75, t=t, is_dark_theme=False)

        if t > 1.2:
            words2 = [
                KineticWord("on messy, raw", is_bold=True),
                KineticWord("HTML DOMs", is_bold=True, is_highlight_box=True),
            ]
            self.kinetics.render_headline(draw, words2, center_x=self.width // 2, top_y=130, t=t - 1.2, is_dark_theme=False)

        # Raw HTML DOM Wall (Simulating overwhelming brittle tags)
        box_x0, box_y0, box_x1, box_y1 = 36, 220, 540, 640
        draw.rounded_rectangle([box_x0, box_y0, box_x1, box_y1], radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=2)

        # Titlebar
        draw.rounded_rectangle([box_x0, box_y0, box_x1, box_y0 + 34], radius=12, fill=(241, 245, 249))
        draw.rectangle([box_x0, box_y0 + 10, box_x1, box_y0 + 34], fill=(241, 245, 249))
        draw.text((box_x0 + 16, box_y0 + 10), "⚠ RAW DOM SCRAPING — 42,000 TOKENS", fill=(220, 38, 38), font=self.font_alert)

        # Brittle HTML Lines
        html_lines = [
            "<div class=\"_29xfk_wrapper dynamic-v3-obscured-7182\">",
            "  <section id=\"async-mount-root-987\" data-qa=\"bypass\">",
            "    <div class=\"c-btn-flyout__inner--obfuscated-js\">",
            "      <span data-cookie-consent=\"deny-all-trackers\">...</span>",
            "      <iframe src=\"https://auth-cdn.service/v2/challenge\">",
            "        <input type=\"hidden\" name=\"csrf_token\" value=\"9a8f...\" />",
            "      </iframe>",
            "      <button disabled class=\"btn-cta-v4_disabled-auto\">",
            "        <!-- ERROR: XPath '#submit-booking' not found -->",
            "        <span>Confirm Flight Reservation</span>",
            "      </button>",
            "    </div>",
            "  </section>",
            "</div>",
        ]

        ly = box_y0 + 44
        for l in html_lines:
            col = (220, 38, 38) if "ERROR" in l or "obfuscated" in l else (100, 116, 139)
            draw.text((box_x0 + 16, ly), l, fill=col, font=self.font_code)
            ly += 18

        # Red Failure Stamped Badge across the center
        if t > 1.8:
            stamp_w, stamp_h = 320, 60
            scx = (box_x0 + box_x1) // 2
            scy = (box_y0 + box_y1) // 2 + 30
            draw.rounded_rectangle([scx - stamp_w // 2, scy - stamp_h // 2, scx + stamp_w // 2, scy + stamp_h // 2], radius=8, fill=(254, 242, 242), outline=(220, 38, 38), width=3)
            draw.text((scx - 130, scy - 12), "✖ CONTEXT WINDOW EXHAUSTED", fill=(220, 38, 38), font=self.font_alert)

        return img


# =============================================================================
# 3. SCENE 3: THE BREAKTHROUGH (Light Theme, Vision Bounding Boxes [1], [2], [3])
# =============================================================================
class BrowserUseVisionTaggingComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 576, height: int = 1024):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.browser = BrowserViewport()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=30, y0=60, x1=546, y1=210, label="kinetic_headline"),
            BoundingBox(x0=36, y0=220, x1=540, y1=660, label="vision_tagged_browser"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)

        # Kinetic Headline: "browser-use tags every interactive button with [visual boxes]"
        words = [
            KineticWord("browser-use tags", is_bold=True),
            KineticWord("every", is_serif_italic=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=self.width // 2, top_y=75, t=t, is_dark_theme=False)

        if t > 1.2:
            words2 = [
                KineticWord("interactive button with", is_bold=True),
                KineticWord("visual boxes", is_bold=True, is_highlight_box=True),
            ]
            self.kinetics.render_headline(draw, words2, center_x=self.width // 2, top_y=130, t=t - 1.2, is_dark_theme=False)

        # Highlight tag 3 (Submit Button) with pulse
        active_id = 3 if ((t * 3.0) % 2.0 > 1.0) else None

        self.browser.render(
            draw=draw,
            bounds=(36, 220, 540, 640),
            url="https://booking.com/flights",
            is_dark_theme=False,
            show_vision_tags=True,
            active_tag_id=active_id,
            cursor_pos=(288, 455) if t > 2.0 else None,
            is_clicking=(t > 2.5),
            click_progress=min(1.0, (t - 2.5) * 2.0) if t > 2.5 else 0.0,
        )

        return img


# =============================================================================
# 4. SCENE 4: PROTOCOL ENGINE (Light Theme, CDP WebSocket Bus)
# =============================================================================
class BrowserUseCDPConduitComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 576, height: int = 1024):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.bus = CDPProtocolBus()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=30, y0=60, x1=546, y1=210, label="kinetic_headline"),
            BoundingBox(x0=36, y0=240, x1=540, y1=660, label="cdp_protocol_bus"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)

        # Kinetic Headline: "Direct control via native [Chrome DevTools Protocol]"
        words = [
            KineticWord("Direct control via", is_bold=True),
            KineticWord("native", is_serif_italic=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=self.width // 2, top_y=75, t=t, is_dark_theme=False)

        if t > 1.2:
            words2 = [
                KineticWord("Chrome DevTools", is_bold=True),
                KineticWord("Protocol", is_bold=True, is_highlight_box=True),
            ]
            self.kinetics.render_headline(draw, words2, center_x=self.width // 2, top_y=130, t=t - 1.2, is_dark_theme=False)

        # Render CDP Protocol Conduit
        self.bus.render(draw, t=t, center_y=440, width=self.width)

        return img


# =============================================================================
# 5. SCENE 5: CODE AS ACTIONS (Light Theme, Python REPL Terminal)
# =============================================================================
class BrowserUsePythonREPLComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 576, height: int = 1024):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.terminal = REPLCodeTerminal()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=30, y0=60, x1=546, y1=210, label="kinetic_headline"),
            BoundingBox(x0=36, y0=220, x1=540, y1=660, label="repl_terminal"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)

        # Kinetic Headline: "The agent writes pure multi-step [Python code]"
        words = [
            KineticWord("The agent writes", is_bold=True),
            KineticWord("pure", is_serif_italic=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=self.width // 2, top_y=75, t=t, is_dark_theme=False)

        if t > 1.2:
            words2 = [
                KineticWord("multi-step", is_bold=True),
                KineticWord("Python code", is_bold=True, is_highlight_box=True),
            ]
            self.kinetics.render_headline(draw, words2, center_x=self.width // 2, top_y=130, t=t - 1.2, is_dark_theme=False)

        # Render Python REPL Terminal
        self.terminal.render(draw, t=t, bounds=(36, 220, 540, 640))

        return img


# =============================================================================
# 6. SCENE 6: BENCHMARK EVIDENCE (Light Theme, Authentic Acquired PNG Chart)
# =============================================================================
class BrowserUseBenchmarkEvidenceComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 576, height: int = 1024):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.viewer = EvidenceFigureViewer()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=30, y0=60, x1=546, y1=210, label="kinetic_headline"),
            BoundingBox(x0=36, y0=220, x1=540, y1=660, label="benchmark_evidence_figure"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)

        # Kinetic Headline: "Crushing benchmarks on real [live websites]"
        words = [
            KineticWord("Crushing benchmarks on", is_bold=True),
            KineticWord("real", is_serif_italic=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=self.width // 2, top_y=75, t=t, is_dark_theme=False)

        if t > 1.2:
            words2 = [
                KineticWord("unseen", is_bold=True),
                KineticWord("live websites", is_bold=True, is_highlight_box=True),
            ]
            self.kinetics.render_headline(draw, words2, center_x=self.width // 2, top_y=130, t=t - 1.2, is_dark_theme=False)

        # Render Authentic Primary Diagram
        self.viewer.render(
            draw=draw,
            base_canvas=img,
            t=t,
            image_path="assets/acquired/browser_use/accuracy_by_model_light.png",
            center=(self.width // 2, 430),
            max_width=490,
            max_height=360,
            source_label="accuracy_by_model_light.png",
        )

        return img


# =============================================================================
# 7. SCENE 7: LOOP CONCLUSION (Dark Theme, Booking Completed, Seamless Loop)
# =============================================================================
class BrowserUseLoopConclusionComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 576, height: int = 1024):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        try:
            self.font_title = ImageFont.truetype("arialbd.ttf", 16)
            self.font_sub = ImageFont.truetype("arial.ttf", 13)
            self.font_check = ImageFont.truetype("arialbd.ttf", 28)
        except Exception:
            self.font_title = ImageFont.load_default()
            self.font_sub = ImageFont.load_default()
            self.font_check = ImageFont.load_default()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=30, y0=60, x1=546, y1=210, label="kinetic_headline"),
            BoundingBox(x0=36, y0=220, x1=540, y1=660, label="loop_conclusion_card"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (10, 13, 20, 255))
        draw = ImageDraw.Draw(img)

        # Subtle dark grid
        grid_step = 36
        for gx in range(0, self.width, grid_step):
            draw.line([(gx, 0), (gx, self.height)], fill=(20, 30, 45, 100), width=1)
        for gy in range(0, self.height, grid_step):
            draw.line([(0, gy), (self.width, gy)], fill=(20, 30, 45, 100), width=1)

        # Central emerald radial glow
        draw.ellipse([100, 260, 476, 640], fill=(16, 185, 129, 25))

        # Kinetic Headline: "Web automation is now solved and completely [open source]"
        words = [
            KineticWord("Web automation is now", is_bold=True),
            KineticWord("solved", is_serif_italic=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=self.width // 2, top_y=75, t=t, is_dark_theme=True)

        if t > 1.2:
            words2 = [
                KineticWord("and completely", is_bold=True),
                KineticWord("open source", is_bold=True, is_highlight_box=True),
            ]
            self.kinetics.render_headline(draw, words2, center_x=self.width // 2, top_y=130, t=t - 1.2, is_dark_theme=True)

        # Booking Confirmation Card
        box_x0, box_y0, box_x1, box_y1 = 44, 250, 532, 600
        draw.rounded_rectangle([box_x0, box_y0, box_x1, box_y1], radius=16, fill=(19, 24, 36), outline=(30, 41, 59), width=2)

        # Big Emerald Checkmark Circle
        ccx, ccy = self.width // 2, box_y0 + 70
        draw.ellipse([ccx - 36, ccy - 36, ccx + 36, ccy + 36], fill=(16, 185, 129))
        draw.text((ccx - 14, ccy - 18), "✓", fill=(255, 255, 255), font=self.font_check)

        # Confirmation Text
        draw.text((self.width // 2 - 120, ccy + 52), "Flight Reservation Confirmed", fill=(241, 245, 249), font=self.font_title)
        draw.text((self.width // 2 - 140, ccy + 80), "Booking #BU-94812 • SFO to NRT (Direct)", fill=(148, 163, 184), font=self.font_sub)
        draw.text((self.width // 2 - 110, ccy + 102), "Total: $642 USD • PDF Exported", fill=(52, 211, 153), font=self.font_sub)

        # Bottom GitHub Repo Pill
        pill_y = box_y1 - 50
        draw.rounded_rectangle([box_x0 + 20, pill_y, box_x1 - 20, pill_y + 36], radius=8, fill=(15, 23, 42), outline=(2, 132, 199), width=1)
        draw.text((box_x0 + 36, pill_y + 9), "★ github.com/browser-use/browser-use (121k stars)", fill=(56, 189, 248), font=self.font_sub)

        return img
