"""
SUPER.INTELLIGENCEEE — Storytelling Engine: Browser Viewport & Interactive DOM Tagging
Renders a pixel-crisp, procedural web browser interface with URL bar, interactive DOM elements,
vision-grounded bounding boxes, and an autonomous robotic cursor.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont


@dataclass
class InteractiveElementBox:
    element_id: int
    label: str
    rect: Tuple[int, int, int, int]  # (x0, y0, x1, y1)
    tag_color: Tuple[int, int, int] = (2, 132, 199)  # Tech Blue
    is_active: bool = False


class AutonomousCursor:
    """Animates a robotic agent pointer cursor with click ripples."""

    @staticmethod
    def render(
        draw: ImageDraw.ImageDraw,
        x: float,
        y: float,
        is_clicking: bool = False,
        click_progress: float = 0.0,
        color: Tuple[int, int, int] = (15, 23, 42),
    ) -> None:
        # Draw pointer cursor shape
        points = [
            (x, y),
            (x, y + 20),
            (x + 5, y + 16),
            (x + 10, y + 25),
            (x + 14, y + 23),
            (x + 9, y + 14),
            (x + 16, y + 14),
        ]
        draw.polygon(points, fill=color, outline=(255, 255, 255), width=2)

        # Click ripple effect
        if is_clicking and click_progress > 0.0:
            radius = int(8 + 24 * click_progress)
            alpha = int(255 * (1.0 - click_progress))
            ripple_color = (2, 132, 199, alpha)
            draw.ellipse(
                [x - radius, y - radius, x + radius, y + radius],
                outline=ripple_color,
                width=2,
            )


class BrowserViewport:
    """
    Renders an authentic, full-bleed or centered browser window with
    interactive page elements, address bar, and vision-bounding boxes.
    """

    def __init__(self, font_name: str = "arial.ttf"):
        try:
            self.font_url = ImageFont.truetype(font_name, 13)
            self.font_title = ImageFont.truetype(font_name, 16)
            self.font_body = ImageFont.truetype(font_name, 13)
            self.font_tag = ImageFont.truetype(font_name, 11)
            self.font_btn = ImageFont.truetype("arialbd.ttf", 13)
        except Exception:
            self.font_url = ImageFont.load_default()
            self.font_title = ImageFont.load_default()
            self.font_body = ImageFont.load_default()
            self.font_tag = ImageFont.load_default()
            self.font_btn = ImageFont.load_default()

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        bounds: Tuple[int, int, int, int],  # (x0, y0, x1, y1)
        url: str = "https://booking.com/flights",
        is_dark_theme: bool = False,
        show_vision_tags: bool = False,
        active_tag_id: Optional[int] = None,
        cursor_pos: Optional[Tuple[float, float]] = None,
        is_clicking: bool = False,
        click_progress: float = 0.0,
    ) -> List[InteractiveElementBox]:
        x0, y0, x1, y1 = bounds
        w = x1 - x0
        h = y1 - y0

        # Colors
        if is_dark_theme:
            win_bg = (19, 24, 36)
            win_border = (30, 41, 59)
            titlebar_bg = (15, 23, 42)
            url_bg = (10, 13, 20)
            url_text = (148, 163, 184)
            page_bg = (15, 23, 42)
            text_color = (241, 245, 249)
            subtext_color = (148, 163, 184)
            card_bg = (24, 32, 47)
            card_border = (40, 53, 75)
        else:
            win_bg = (255, 255, 255)
            win_border = (203, 213, 225)
            titlebar_bg = (241, 245, 249)
            url_bg = (226, 232, 240)
            url_text = (71, 85, 105)
            page_bg = (255, 255, 255)
            text_color = (15, 23, 42)
            subtext_color = (100, 116, 139)
            card_bg = (248, 250, 252)
            card_border = (226, 232, 240)

        # 1. Window Outline & Shadow
        draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=win_bg, outline=win_border, width=2)

        # 2. Titlebar & Tab
        tb_height = 42
        draw.rounded_rectangle([x0, y0, x1, y0 + tb_height], radius=14, fill=titlebar_bg)
        # Flatten bottom corners of titlebar
        draw.rectangle([x0, y0 + 14, x1, y0 + tb_height], fill=titlebar_bg)
        draw.line([(x0, y0 + tb_height), (x1, y0 + tb_height)], fill=win_border, width=1)

        # Traffic lights (macOS/Chrome window controls)
        draw.ellipse([x0 + 14, y0 + 15, x0 + 26, y0 + 27], fill=(239, 68, 68))    # Red
        draw.ellipse([x0 + 32, y0 + 15, x0 + 44, y0 + 27], fill=(245, 158, 11))   # Yellow
        draw.ellipse([x0 + 50, y0 + 15, x0 + 62, y0 + 27], fill=(16, 185, 129))   # Green

        # Active Tab
        tab_x0 = x0 + 72
        tab_x1 = x0 + 200
        draw.rounded_rectangle([tab_x0, y0 + 8, tab_x1, y0 + tb_height], radius=6, fill=win_bg)
        draw.text((tab_x0 + 10, y0 + 14), "✈ Flight Search", fill=text_color, font=self.font_url)

        # URL Address Bar
        url_bar_y0 = y0 + tb_height + 8
        url_bar_y1 = url_bar_y0 + 30
        draw.rounded_rectangle([x0 + 16, url_bar_y0, x1 - 16, url_bar_y1], radius=8, fill=url_bg)
        draw.text((x0 + 28, url_bar_y0 + 6), "🔒 " + url, fill=url_text, font=self.font_url)

        # Separator below URL bar
        header_bottom = url_bar_y1 + 8
        draw.line([(x0, header_bottom), (x1, header_bottom)], fill=win_border, width=1)

        # 3. Web Page Content
        content_top = header_bottom + 16
        draw.text((x0 + 24, content_top), "Find Flights Worldwide", fill=text_color, font=self.font_title)
        draw.text((x0 + 24, content_top + 22), "Compare 500+ airlines instantly", fill=subtext_color, font=self.font_body)

        # Booking Search Card
        card_top = content_top + 46
        card_bottom = card_top + 160
        draw.rounded_rectangle([x0 + 20, card_top, x1 - 20, card_bottom], radius=10, fill=card_bg, outline=card_border, width=1)

        # Inputs inside card
        input_w = (w - 70) // 2
        in1_rect = (x0 + 32, card_top + 16, x0 + 32 + input_w, card_top + 52)
        in2_rect = (x0 + 44 + input_w, card_top + 16, x1 - 32, card_top + 52)

        # Draw Input 1
        draw.rounded_rectangle(in1_rect, radius=6, fill=win_bg, outline=card_border, width=1)
        draw.text((in1_rect[0] + 8, in1_rect[1] + 10), "SFO (San Francisco)", fill=text_color, font=self.font_body)

        # Draw Input 2
        draw.rounded_rectangle(in2_rect, radius=6, fill=win_bg, outline=card_border, width=1)
        draw.text((in2_rect[0] + 8, in2_rect[1] + 10), "NRT (Tokyo)", fill=text_color, font=self.font_body)

        # Search Button
        btn_rect = (x0 + 32, card_top + 70, x1 - 32, card_top + 106)
        btn_color = (2, 132, 199) if not (active_tag_id == 3) else (14, 165, 233)
        draw.rounded_rectangle(btn_rect, radius=8, fill=btn_color)
        draw.text((btn_rect[0] + (btn_rect[2] - btn_rect[0]) // 2 - 45, btn_rect[1] + 10), "Search Flights →", fill=(255, 255, 255), font=self.font_btn)

        # Below Card: Simulated Result Row
        res_top = card_bottom + 16
        draw.rounded_rectangle([x0 + 20, res_top, x1 - 20, res_top + 60], radius=8, fill=win_bg, outline=card_border, width=1)
        draw.text((x0 + 32, res_top + 12), "Direct Flight • 11h 15m", fill=text_color, font=self.font_body)
        draw.text((x0 + 32, res_top + 32), "Departs 10:45 AM", fill=subtext_color, font=self.font_tag)
        draw.text((x1 - 100, res_top + 18), "$642 USD", fill=(16, 185, 129), font=self.font_btn)

        # Define Interactive Element Boxes
        interactive_elements = [
            InteractiveElementBox(element_id=1, label="Departure", rect=in1_rect),
            InteractiveElementBox(element_id=2, label="Destination", rect=in2_rect),
            InteractiveElementBox(element_id=3, label="Submit", rect=btn_rect, tag_color=(239, 68, 68)),
            InteractiveElementBox(element_id=4, label="Select Flight", rect=(x0 + 20, res_top, x1 - 20, res_top + 60), tag_color=(16, 185, 129)),
        ]

        # 4. Vision Bounding Boxes (The Browser-Use Hallmark)
        if show_vision_tags:
            for elem in interactive_elements:
                ex0, ey0, ex1, ey1 = elem.rect
                tag_col = elem.tag_color
                is_active = (active_tag_id == elem.element_id)

                # Draw high-contrast bounding box
                box_width = 3 if is_active else 2
                draw.rectangle([ex0 - 2, ey0 - 2, ex1 + 2, ey1 + 2], outline=tag_col, width=box_width)

                # Draw numeric badge pill at top-left
                badge_w = 22
                badge_h = 16
                badge_rect = [ex0 - 2, ey0 - badge_h - 2, ex0 - 2 + badge_w, ey0 - 2]
                draw.rectangle(badge_rect, fill=tag_col)
                draw.text((badge_rect[0] + 5, badge_rect[1] + 2), f"{elem.element_id}", fill=(255, 255, 255), font=self.font_tag)

        # 5. Cursor Overlay
        if cursor_pos is not None:
            cx, cy = cursor_pos
            cursor_col = (255, 255, 255) if is_dark_theme else (15, 23, 42)
            AutonomousCursor.render(
                draw=draw,
                x=cx,
                y=cy,
                is_clicking=is_clicking,
                click_progress=click_progress,
                color=cursor_col,
            )

        return interactive_elements
