"""
SUPER.INTELLIGENCEEE — Phase 5 Charts, Telemetry & Timer Engine
Reference-style technical data visualizers:
1. LollipopChart: Horizontal lollipop chart comparing binary sizes in KB
2. FlatlineTelemetryCard: Real-time flatline RAM curve with 'stays flat' status badge
3. DigitalStopwatchTimer: Giant digital timer (1:54, 4:00) with animated progress blocks
4. MoEExpertGrid: Dense 896-expert grid with 16 active red nodes and bezier streaming connectors
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from rendering.native_motion_engine.primitives import (
    clamp,
    ease_out_back,
    ease_out_cubic,
    get_progress,
)


class LollipopChart:
    """
    Renders a horizontal lollipop chart comparing file/binary sizes.
    One target bar is highlighted in bright green with an active focus rectangle.
    """

    def __init__(self):
        try:
            self.font_title = ImageFont.truetype("arialbd.ttf", 22)
            self.font_body = ImageFont.truetype("arial.ttf", 16)
            self.font_mono = ImageFont.truetype("consola.ttf", 14)
        except Exception:
            self.font_title = ImageFont.load_default()
            self.font_body = ImageFont.load_default()
            self.font_mono = ImageFont.load_default()

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        t: float = 1.0,
        center_y: int = 720,
    ):
        cx0, cy0 = 60, center_y - 280
        cx1, cy1 = 1020, center_y + 280

        # Background white card
        draw.rounded_rectangle([cx0 + 6, cy0 + 8, cx1 + 6, cy1 + 8], radius=20, fill=(210, 218, 225, 110))
        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

        # Title
        draw.text((cx0 + 40, cy0 + 30), "A 176 KB binary that runs a 1.56 TB model", font=self.font_title, fill=(15, 23, 42))

        # Chart items: (label, kb_val, is_target)
        items = [
            ("k3_run", 176, True),     # Target highlighted in green
            ("fast_ops", 95, False),
            ("c_model", 87, False),
            ("table_test", 70, False),
            ("kv_cache", 60, False),
            ("context_st", 55, False),
            ("test_cfg", 47, False),
        ]

        chart_x0 = cx0 + 160
        chart_x1 = cx1 - 60
        chart_w = chart_x1 - chart_x0
        max_kb = 200

        # Vertical grid lines
        for kb_tick in [0, 25, 50, 75, 100, 125, 150, 175, 200]:
            tx = chart_x0 + int((kb_tick / max_kb) * chart_w)
            draw.line([(tx, cy0 + 80), (tx, cy1 - 50)], fill=(241, 245, 249), width=1)
            draw.text((tx - 10, cy1 - 40), str(kb_tick), font=self.font_mono, fill=(148, 163, 184))

        draw.text((chart_x0 + chart_w // 2 - 30, cy1 - 20), "kilobytes", font=self.font_mono, fill=(100, 116, 139))

        # Draw lollipop bars
        row_h = 44
        start_y = cy0 + 95

        for i, (name, kb, is_target) in enumerate(items):
            ry = start_y + i * row_h
            p = get_progress(t, 0.2 + i * 0.08, 0.5, "ease_out_cubic")
            cur_kb = kb * p

            cur_end_x = chart_x0 + int((cur_kb / max_kb) * chart_w)

            # Name label
            draw.text((chart_x0 - 120, ry - 8), name, font=self.font_mono, fill=(71, 85, 105))

            if is_target:
                # Highlighted Green Line
                draw.line([(chart_x0, ry), (cur_end_x, ry)], fill=(34, 197, 94), width=4)
                draw.circle((cur_end_x, ry), radius=10, fill=(34, 197, 94))
                draw.text((cur_end_x + 16, ry - 8), f"{kb} KB", font=self.font_title, fill=(22, 101, 52))

                # Focus bounding box around top line
                if t > 0.6:
                    bx0 = chart_x0 - 130
                    by0 = ry - 16
                    bx1 = cur_end_x + 120
                    by1 = ry + 16
                    draw.rectangle([bx0, by0, bx1, by1], outline=(2, 132, 199), width=2)
                    for dx, dy in [(bx0, by0), (bx1, by0), (bx0, by1), (bx1, by1)]:
                        draw.rectangle([dx - 3, dy - 3, dx + 3, dy + 3], fill=(255, 255, 255), outline=(2, 132, 199), width=1)
            else:
                # Standard Gray Line
                draw.line([(chart_x0, ry), (cur_end_x, ry)], fill=(71, 85, 105), width=2)
                draw.circle((cur_end_x, ry), radius=8, fill=(71, 85, 105))
                draw.text((cur_end_x + 14, ry - 7), f"{kb} KB", font=self.font_mono, fill=(71, 85, 105))


class FlatlineTelemetryCard:
    """
    Renders 'RAM use while layers stream' with a flatline green curve and status badge.
    """

    def __init__(self):
        try:
            self.font_title = ImageFont.truetype("arialbd.ttf", 20)
            self.font_badge = ImageFont.truetype("arialbd.ttf", 14)
            self.font_mono = ImageFont.truetype("consola.ttf", 13)
        except Exception:
            self.font_title = ImageFont.load_default()
            self.font_badge = ImageFont.load_default()
            self.font_mono = ImageFont.load_default()

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        t: float = 1.0,
        center_y: int = 1260,
    ):
        cx0, cy0 = 60, center_y - 100
        cx1, cy1 = 1020, center_y + 100

        draw.rounded_rectangle([cx0 + 6, cy0 + 8, cx1 + 6, cy1 + 8], radius=18, fill=(210, 218, 225, 110))
        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

        # Title
        draw.text((cx0 + 30, cy0 + 20), "RAM use while layers stream", font=self.font_title, fill=(15, 23, 42))

        # Status badge: ✓ stays flat
        bw = 140
        bx = cx1 - 30 - bw
        by = cy0 + 16
        draw.rounded_rectangle([bx, by, bx + bw, by + 32], radius=6, fill=(240, 253, 244), outline=(34, 197, 94), width=1)
        draw.text((bx + 16, by + 7), "✓  stays flat", font=self.font_badge, fill=(22, 101, 52))

        # Flatline telemetry trace
        line_x0 = cx0 + 30
        line_x1 = cx1 - 30
        line_y = cy0 + 120
        line_w = line_x1 - line_x0

        p = get_progress(t, 0.2, 1.2, "ease_out_cubic")
        cur_w = int(line_w * p)

        # Gray base track
        draw.line([(line_x0, line_y), (line_x1, line_y)], fill=(241, 245, 249), width=4)
        # Green active flatline
        draw.line([(line_x0, line_y), (line_x0 + cur_w, line_y)], fill=(34, 197, 94), width=4)
        # Leading pulse circle
        draw.circle((line_x0 + cur_w, line_y), radius=7, fill=(34, 197, 94))


class DigitalStopwatchTimer:
    """
    Renders a giant digital timer (1:54, 4:00) with prompt and horizontal progress blocks.
    """

    def __init__(self):
        try:
            self.font_timer = ImageFont.truetype("arialbd.ttf", 84)
            self.font_title = ImageFont.truetype("arialbd.ttf", 24)
            self.font_mono = ImageFont.truetype("consola.ttf", 15)
            self.font_badge = ImageFont.truetype("arialbd.ttf", 13)
        except Exception:
            self.font_timer = ImageFont.load_default()
            self.font_title = ImageFont.load_default()
            self.font_mono = ImageFont.load_default()
            self.font_badge = ImageFont.load_default()

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        t: float = 1.0,
        center_y: int = 740,
        prompt_text: str = "The capital of France is",
        time_display: str = "1:54",
    ):
        # Header Badges: [EXAMPLE RUN · FROM THE README]  [💻 LAPTOP PRESET]
        b1_x0 = 60
        b1_y0 = center_y - 280
        draw.rounded_rectangle([b1_x0, b1_y0, b1_x0 + 320, b1_y0 + 32], radius=6, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
        draw.text((b1_x0 + 14, b1_y0 + 7), "EXAMPLE RUN · FROM THE README", font=self.font_badge, fill=(180, 83, 9))

        b2_x0 = 1080 - 60 - 200
        draw.rounded_rectangle([b2_x0, b1_y0, b2_x0 + 200, b1_y0 + 32], radius=6, fill=(15, 23, 42))
        draw.text((b2_x0 + 16, b1_y0 + 7), "💻 LAPTOP PRESET", font=self.font_badge, fill=(255, 255, 255))

        # Prompt Box Card
        cx0 = 60
        cx1 = 1020
        cy0 = center_y - 220
        cy1 = center_y - 120
        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.text((cx0 + 24, cy0 + 14), "PROMPT", font=self.font_mono, fill=(100, 116, 139))
        draw.text((cx0 + 24, cy0 + 44), prompt_text, font=self.font_title, fill=(15, 23, 42))

        # Giant Stopwatch Timer: ⏱ 1:54
        timer_text = time_display
        tw = draw.textlength(timer_text, font=self.font_timer)
        tx = 540 - int(tw / 2) + 20
        ty = center_y - 30

        # Clock icon
        draw.circle((tx - 40, ty + 45), radius=22, outline=(220, 38, 38), width=3)
        draw.line([(tx - 40, ty + 45), (tx - 40, ty + 30)], fill=(220, 38, 38), width=3)
        draw.line([(tx - 40, ty + 45), (tx - 28, ty + 45)], fill=(220, 38, 38), width=3)

        draw.text((tx, ty), timer_text, font=self.font_timer, fill=(15, 23, 42))

        # Horizontal progress blocks
        block_w = 80
        block_h = 70
        spacing = 24
        total_bw = 7 * block_w + 6 * spacing
        bx_start = 540 - total_bw // 2
        by = center_y + 110

        p_blocks = min(7, int(t * 3.5))
        for i in range(7):
            bx = bx_start + i * (block_w + spacing)
            is_filled = i < p_blocks
            b_col = (185, 28, 28) if is_filled else (226, 232, 240)
            draw.rounded_rectangle([bx, by, bx + block_w, by + block_h], radius=10, fill=b_col)


class MoEExpertGrid:
    """
    Renders the 896-expert dense grid with 16 active red nodes and bezier streaming conduits.
    """

    def __init__(self):
        try:
            self.font_badge = ImageFont.truetype("arialbd.ttf", 13)
            self.font_mono = ImageFont.truetype("consola.ttf", 13)
        except Exception:
            self.font_badge = ImageFont.load_default()
            self.font_mono = ImageFont.load_default()

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        t: float = 1.0,
        center_y: int = 680,
    ):
        cx0 = 60
        cx1 = 1020
        cy0 = center_y - 360
        cy1 = center_y + 360

        # Base white card
        draw.rounded_rectangle([cx0 + 6, cy0 + 8, cx1 + 6, cy1 + 8], radius=24, fill=(210, 218, 225, 110))
        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

        # Header: [LAYER 1] of 93, each with its own set     [16 awake] [880 asleep]
        draw.rounded_rectangle([cx0 + 30, cy0 + 24, cx0 + 150, cy0 + 58], radius=6, fill=(15, 23, 42))
        draw.text((cx0 + 44, cy0 + 31), "⬡ LAYER 1", font=self.font_badge, fill=(255, 255, 255))
        draw.text((cx0 + 165, cy0 + 31), "of 93, each with its own set", font=self.font_mono, fill=(100, 116, 139))

        # Awake / Asleep badges
        draw.rounded_rectangle([cx1 - 280, cy0 + 24, cx1 - 170, cy0 + 58], radius=6, fill=(220, 38, 38))
        draw.text((cx1 - 268, cy0 + 31), "16 awake", font=self.font_badge, fill=(255, 255, 255))

        draw.rounded_rectangle([cx1 - 160, cy0 + 24, cx1 - 30, cy0 + 58], radius=6, fill=(241, 245, 249))
        draw.text((cx1 - 148, cy0 + 31), "880 asleep", font=self.font_badge, fill=(100, 116, 139))

        # Dense Grid: 28 cols x 32 rows = 896 dots
        grid_cols = 28
        grid_rows = 32
        cell_size = 18
        cell_gap = 10
        grid_w = grid_cols * (cell_size + cell_gap) - cell_gap
        gx_start = 540 - grid_w // 2
        gy_start = cy0 + 80

        # Fixed set of 16 active indexes (pseudo-randomly distributed)
        active_indices = {45, 112, 198, 245, 310, 380, 425, 490, 560, 615, 680, 725, 790, 815, 850, 885}
        active_coords = []

        for r in range(grid_rows):
            for c in range(grid_cols):
                idx = r * grid_cols + c
                cell_x = gx_start + c * (cell_size + cell_gap)
                cell_y = gy_start + r * (cell_size + cell_gap)

                if idx in active_indices and t > 0.4:
                    # Active Red Node
                    draw.rounded_rectangle([cell_x, cell_y, cell_x + cell_size, cell_y + cell_size], radius=4, fill=(220, 38, 38))
                    active_coords.append((cell_x + cell_size // 2, cell_y + cell_size // 2))
                else:
                    # Inactive Gray Node
                    draw.rounded_rectangle([cell_x, cell_y, cell_x + cell_size, cell_y + cell_size], radius=4, fill=(226, 232, 240))

        # Bezier connector lines streaming up from lower SSD
        if t > 0.8:
            ssd_source = (540, cy1 - 40)
            p_stream = min(1.0, (t - 0.8) * 1.5)
            for target in active_coords:
                # Dotted bezier curve
                for step in range(12):
                    u = (step / 12.0) * p_stream
                    bx = (1 - u) * ssd_source[0] + u * target[0]
                    by = (1 - u) * ssd_source[1] + u * target[1]
                    draw.circle((int(bx), int(by)), radius=2, fill=(220, 38, 38))
