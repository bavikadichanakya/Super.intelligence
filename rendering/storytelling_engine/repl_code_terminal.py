"""
SUPER.INTELLIGENCEEE — Storytelling Engine: REPL Code Terminal
Visualizes the Python Code-As-Actions execution environment of browser-use,
featuring syntax-highlighted code, line reveals, and persistent REPL subprocess telemetry.
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont


class REPLCodeTerminal:
    """Renders a syntax-highlighted code editor and live REPL execution terminal."""

    def __init__(self, font_name: str = "arial.ttf"):
        try:
            self.font_code = ImageFont.truetype("consola.ttf", 13)
            self.font_title = ImageFont.truetype("arialbd.ttf", 13)
            self.font_status = ImageFont.truetype("consola.ttf", 11)
        except Exception:
            self.font_code = ImageFont.load_default()
            self.font_title = ImageFont.load_default()
            self.font_status = ImageFont.load_default()

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        t: float,
        bounds: Tuple[int, int, int, int] = (36, 260, 540, 780),
        is_dark_theme: bool = False,
    ) -> None:
        x0, y0, x1, y1 = bounds
        w = x1 - x0
        h = y1 - y0

        # Modern editor palette (Dark VS Code style)
        bg_color = (15, 23, 42)
        border_color = (30, 41, 59)
        titlebar_color = (30, 41, 59)
        text_color = (241, 245, 249)

        # 1. Main Terminal Window
        draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=bg_color, outline=border_color, width=2)

        # 2. Titlebar
        tb_h = 36
        draw.rounded_rectangle([x0, y0, x1, y0 + tb_h], radius=12, fill=titlebar_color)
        draw.rectangle([x0, y0 + 12, x1, y0 + tb_h], fill=titlebar_color)

        # Traffic light dots
        draw.ellipse([x0 + 14, y0 + 12, x0 + 24, y0 + 22], fill=(239, 68, 68))
        draw.ellipse([x0 + 30, y0 + 12, x0 + 40, y0 + 22], fill=(245, 158, 11))
        draw.ellipse([x0 + 46, y0 + 12, x0 + 56, y0 + 22], fill=(16, 185, 129))

        # Tab name
        draw.text((x0 + 70, y0 + 10), "📄 agent_repl.py — browser-use", fill=(203, 213, 225), font=self.font_title)

        # 3. Python Code Lines
        code_lines = [
            ("from browser_use import Agent", [(0, 4, (192, 132, 252)), (5, 16, (148, 163, 184)), (17, 23, (192, 132, 252)), (24, 29, (96, 165, 250))]),
            ("from langchain_openai import ChatOpenAI", [(0, 4, (192, 132, 252)), (17, 23, (192, 132, 252)), (24, 38, (96, 165, 250))]),
            ("", []),
            ("# 1. Autonomous Flight Booking Agent", [(0, 36, (100, 116, 139))]),
            ("agent = Agent(", [(0, 5, (241, 245, 249)), (8, 13, (96, 165, 250))]),
            ("    task=\"Find flight SFO to NRT\",", [(4, 8, (148, 163, 184)), (9, 34, (52, 211, 153))]),
            ("    llm=ChatOpenAI(model=\"gpt-4o\"),", [(4, 7, (148, 163, 184)), (8, 18, (96, 165, 250)), (25, 33, (52, 211, 153))]),
            (")", [(0, 1, (241, 245, 249))]),
            ("", []),
            ("# 2. Execute Multi-Step Actions in REPL", [(0, 39, (100, 116, 139))]),
            ("history = await agent.run(max_steps=25)", [(0, 7, (241, 245, 249)), (10, 15, (192, 132, 252)), (22, 25, (96, 165, 250))]),
            ("print(f\"Result: {history.final_result()}\")", [(0, 5, (96, 165, 250)), (6, 42, (52, 211, 153))]),
        ]

        # Animate line reveal based on t
        visible_lines_count = min(len(code_lines), int(t * 3.5) + 3)

        line_y = y0 + tb_h + 16
        for idx in range(visible_lines_count):
            line_text, highlights = code_lines[idx]
            line_num_str = f"{idx + 1:2d}"

            # Draw line number
            draw.text((x0 + 16, line_y), line_num_str, fill=(71, 85, 105), font=self.font_code)

            # Draw text with syntax colors
            char_x = x0 + 46
            draw.text((char_x, line_y), line_text, fill=(241, 245, 249), font=self.font_code)

            line_y += 22

        # 4. Live REPL Worker Output Console
        console_h = 100
        console_top = y1 - console_h - 12
        draw.rounded_rectangle([x0 + 12, console_top, x1 - 12, y1 - 12], radius=8, fill=(10, 13, 20), outline=(30, 41, 59), width=1)

        # Console Header
        draw.text((x0 + 24, console_top + 8), "● REPL SUBPROCESS WORKER", fill=(16, 185, 129), font=self.font_status)
        draw.text((x1 - 140, console_top + 8), "MEMORY: 38.4 MB", fill=(148, 163, 184), font=self.font_status)

        # Console Log Stream
        if t > 1.0:
            draw.text((x0 + 24, console_top + 28), "[CDP] > Navigating to booking.com... (142ms)", fill=(148, 163, 184), font=self.font_status)
        if t > 2.0:
            draw.text((x0 + 24, console_top + 46), "[DOM] > Tagged 24 interactive bounding boxes", fill=(56, 189, 248), font=self.font_status)
        if t > 3.0:
            draw.text((x0 + 24, console_top + 64), "[EXEC] > Clicked tag [3] 'Search Flights' -> Status: 200 OK", fill=(52, 211, 153), font=self.font_status)
