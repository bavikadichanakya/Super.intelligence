"""
SUPER.INTELLIGENCEEE — Storytelling Engine: Chrome DevTools Protocol (CDP) WebSocket Bus
Visualizes the bi-directional, high-throughput protocol pipeline between the
Python Agent Core and the Chromium Browser Engine.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont


class CDPProtocolBus:
    """
    Renders an animated hardware-style protocol bus showing JSON command packets
    traveling over Chrome DevTools Protocol (CDP) WebSocket connections.
    """

    def __init__(self, font_name: str = "arial.ttf"):
        try:
            self.font_title = ImageFont.truetype("arialbd.ttf", 15)
            self.font_mono = ImageFont.truetype("consola.ttf", 12)
            self.font_sub = ImageFont.truetype(font_name, 12)
            self.font_tag = ImageFont.truetype("arialbd.ttf", 11)
        except Exception:
            self.font_title = ImageFont.load_default()
            self.font_mono = ImageFont.load_default()
            self.font_sub = ImageFont.load_default()
            self.font_tag = ImageFont.load_default()

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        t: float,
        center_y: int = 560,
        width: int = 576,
    ) -> None:
        # Layout metrics
        margin_x = 36
        bus_w = width - margin_x * 2
        bus_h = 360
        top_y = center_y - bus_h // 2
        bottom_y = top_y + bus_h

        # Canvas styling: Technical light ivory/gray
        # Node Left: Python Agent (x: 40 to 190)
        # Node Right: Chromium Browser (x: 386 to 536)
        # Center Bus: x: 190 to 386

        left_x0, left_x1 = margin_x, margin_x + 150
        right_x0, right_x1 = width - margin_x - 150, width - margin_x
        center_x0, center_x1 = left_x1, right_x0

        # 1. Left Node: Python Agent REPL Controller
        draw.rounded_rectangle([left_x0, top_y + 30, left_x1, bottom_y - 30], radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
        # Top banner
        draw.rounded_rectangle([left_x0, top_y + 30, left_x1, top_y + 65], radius=12, fill=(15, 23, 42))
        draw.rectangle([left_x0, top_y + 55, left_x1, top_y + 65], fill=(15, 23, 42))
        draw.text((left_x0 + 16, top_y + 38), "AGENT REPL", fill=(255, 255, 255), font=self.font_title)

        draw.text((left_x0 + 14, top_y + 80), "Python 3.11", fill=(15, 23, 42), font=self.font_sub)
        draw.text((left_x0 + 14, top_y + 102), "• Pydantic AI Loop", fill=(71, 85, 105), font=self.font_sub)
        draw.text((left_x0 + 14, top_y + 124), "• DOM Parser", fill=(71, 85, 105), font=self.font_sub)
        draw.text((left_x0 + 14, top_y + 146), "• Code Generator", fill=(71, 85, 105), font=self.font_sub)

        # Pulse indicator
        pulse = 0.5 + 0.5 * math.sin(t * 6.0)
        pulse_col = (2, 132, 199) if pulse > 0.5 else (14, 165, 233)
        draw.ellipse([left_x0 + 16, bottom_y - 60, left_x0 + 26, bottom_y - 50], fill=pulse_col)
        draw.text((left_x0 + 32, bottom_y - 62), "ACTIVE REPL", fill=pulse_col, font=self.font_tag)

        # 2. Right Node: Chromium Browser Engine
        draw.rounded_rectangle([right_x0, top_y + 30, right_x1, bottom_y - 30], radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
        draw.rounded_rectangle([right_x0, top_y + 30, right_x1, top_y + 65], radius=12, fill=(15, 23, 42))
        draw.rectangle([right_x0, top_y + 55, right_x1, top_y + 65], fill=(15, 23, 42))
        draw.text((right_x0 + 14, top_y + 38), "CHROMIUM", fill=(255, 255, 255), font=self.font_title)

        draw.text((right_x0 + 14, top_y + 80), "Blink / V8 Engine", fill=(15, 23, 42), font=self.font_sub)
        draw.text((right_x0 + 14, top_y + 102), "• Live Render Tree", fill=(71, 85, 105), font=self.font_sub)
        draw.text((right_x0 + 14, top_y + 124), "• Accessibility Tree", fill=(71, 85, 105), font=self.font_sub)
        draw.text((right_x0 + 14, top_y + 146), "• Native Mouse / Keys", fill=(71, 85, 105), font=self.font_sub)

        draw.ellipse([right_x0 + 16, bottom_y - 60, right_x0 + 26, bottom_y - 50], fill=(16, 185, 129))
        draw.text((right_x0 + 32, bottom_y - 62), "PORT 9222", fill=(16, 185, 129), font=self.font_tag)

        # 3. Center Pipeline Tracks: Bi-Directional WebSocket
        track1_y = top_y + 100  # Outbound Commands (Agent -> Chromium)
        track2_y = top_y + 190  # Inbound Events (Chromium -> Agent)

        # Draw Conduit lines with arrows
        draw.line([(center_x0, track1_y), (center_x1, track1_y)], fill=(148, 163, 184), width=3)
        draw.line([(center_x0, track2_y), (center_x1, track2_y)], fill=(148, 163, 184), width=3)

        # Track Labels
        draw.text((center_x0 + 20, track1_y - 20), "CDP COMMANDS →", fill=(2, 132, 199), font=self.font_tag)
        draw.text((center_x0 + 20, track2_y - 20), "← ACCESSIBILITY EVENTS", fill=(16, 185, 129), font=self.font_tag)

        # 4. Animated Data Packets (Flying JSON Badges)
        # Outbound packet moves Left to Right
        p1_progress = (t * 1.2) % 1.0
        p1_x = center_x0 + p1_progress * (center_x1 - center_x0 - 90)
        draw.rounded_rectangle([p1_x, track1_y - 12, p1_x + 94, track1_y + 14], radius=6, fill=(2, 132, 199))
        draw.text((p1_x + 6, track1_y - 7), "Input.click()", fill=(255, 255, 255), font=self.font_mono)

        # Inbound packet moves Right to Left
        p2_progress = ((t + 0.4) * 0.9) % 1.0
        p2_x = center_x1 - 100 - p2_progress * (center_x1 - center_x0 - 100)
        draw.rounded_rectangle([p2_x, track2_y - 12, p2_x + 100, track2_y + 14], radius=6, fill=(16, 185, 129))
        draw.text((p2_x + 6, track2_y - 7), "DOM.NodeId: 14", fill=(255, 255, 255), font=self.font_mono)

        # Bottom Conduit Telemetry Banner
        banner_y = bottom_y - 10
        draw.rounded_rectangle([margin_x, banner_y, width - margin_x, banner_y + 36], radius=8, fill=(241, 245, 249), outline=(226, 232, 240), width=1)
        draw.text(
            (margin_x + 16, banner_y + 10),
            "⚡ ws://127.0.0.1:9222/devtools/page • Latency: 0.4ms • Zero Headless Lag",
            fill=(71, 85, 105),
            font=self.font_mono,
        )
