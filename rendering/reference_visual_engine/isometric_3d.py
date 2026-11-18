"""
SUPER.INTELLIGENCEEE — Phase 5 Procedural Isometric 3D Engine
Pure Python / NumPy / Pillow 3D projection engine:
1. IsometricVoxelCube: Floating multi-cell voxel model cube with floor shadow and glowing particles
2. IsometricBarChart: 3D column bars with highlighted target pillar and pill badges
3. IsometricHardwareModels: M.2 NVMe SSD (PCB, controller, NAND chips) and RAM DIMMs
4. IsometricLayerStack: 93-slab neural layer stack with sliding always-on slice
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


def iso_project(x: float, y: float, z: float, origin: Tuple[float, float], scale: float = 1.0) -> Tuple[float, float]:
    """
    Transforms 3D Cartesian coordinates into 2D isometric screen coordinates.
    Standard 30-degree isometric projection:
    screen_x = origin_x + (x - y) * cos(30 deg) * scale
    screen_y = origin_y + (x + y) * sin(30 deg) * scale - z * scale
    """
    cos30 = 0.8660254
    sin30 = 0.5000000
    sx = origin[0] + (x - y) * cos30 * scale
    sy = origin[1] + (x + y) * sin30 * scale - z * scale
    return (sx, sy)


class IsometricVoxelCube:
    """
    Renders an animated 3D voxel cube (e.g. representing model parameter count).
    Features subtle floating oscillation, multi-cell surface detailing, and soft floor shadow.
    """

    def __init__(self, font_mono: Optional[ImageFont.ImageFont] = None):
        try:
            self.font_mono = font_mono or ImageFont.truetype("consola.ttf", 14)
        except Exception:
            self.font_mono = ImageFont.load_default()

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        t: float,
        center: Tuple[int, int] = (540, 600),
        size: float = 180.0,
        grid_divisions: int = 5,
        is_dark_theme: bool = True,
    ):
        # 1. Subtle floating oscillation
        float_y = math.sin(t * 2.2) * 12.0
        cur_origin = (center[0], center[1] + float_y)

        # 2. Floor Shadow
        shadow_w = int(size * 1.5)
        shadow_h = int(size * 0.55)
        shadow_y = center[1] + int(size * 0.65)
        shadow_alpha = int(120 - float_y * 2)
        shadow_col = (0, 0, 0, max(20, min(180, shadow_alpha)))
        draw.ellipse(
            [
                center[0] - shadow_w // 2,
                shadow_y - shadow_h // 2,
                center[0] + shadow_w // 2,
                shadow_y + shadow_h // 2,
            ],
            fill=shadow_col,
        )

        # 3. Cube Geometry
        # Base colors (slate/blue hues matching reference)
        top_color = (96, 125, 158)      # Lightest top surface
        left_color = (68, 92, 122)     # Medium left surface
        right_color = (48, 68, 94)     # Darkest right surface
        edge_color = (120, 150, 185)   # Subtle edge highlight

        hs = size / 2.0

        # Define 8 cube vertices in local 3D space (-hs to +hs)
        v = {
            "top_front": (hs, hs, hs),
            "top_left": (-hs, hs, hs),
            "top_back": (-hs, -hs, hs),
            "top_right": (hs, -hs, hs),
            "bot_front": (hs, hs, -hs),
            "bot_left": (-hs, hs, -hs),
            "bot_back": (-hs, -hs, -hs),
            "bot_right": (hs, -hs, -hs),
        }

        # Project vertices to screen
        p = {k: iso_project(coords[0], coords[1], coords[2], cur_origin, scale=1.0) for k, coords in v.items()}

        # Top Face Polygon
        draw.polygon([p["top_back"], p["top_right"], p["top_front"], p["top_left"]], fill=top_color, outline=edge_color)
        # Left Face Polygon
        draw.polygon([p["top_left"], p["top_front"], p["bot_front"], p["bot_left"]], fill=left_color, outline=edge_color)
        # Right Face Polygon
        draw.polygon([p["top_front"], p["top_right"], p["bot_right"], p["bot_front"]], fill=right_color, outline=edge_color)

        # 4. Multi-cell grid subdivisions (voxel texture)
        for i in range(1, grid_divisions):
            frac = i / grid_divisions
            z_mid = -hs + (2 * hs * frac)
            # Left face horizontal lines
            p_lh0 = iso_project(-hs, hs, z_mid, cur_origin)
            p_lh1 = iso_project(hs, hs, z_mid, cur_origin)
            draw.line([p_lh0, p_lh1], fill=edge_color, width=1)

            # Right face horizontal lines
            p_rh0 = iso_project(hs, hs, z_mid, cur_origin)
            p_rh1 = iso_project(hs, -hs, z_mid, cur_origin)
            draw.line([p_rh0, p_rh1], fill=edge_color, width=1)

        # 5. Glowing Micro Particles around base
        for idx in range(6):
            p_ang = (t * 1.5 + idx * (math.pi / 3))
            px = center[0] + int(math.cos(p_ang) * (size * 0.75))
            py = shadow_y + int(math.sin(p_ang) * (shadow_h * 0.45))
            p_rad = 3 + int(math.sin(t * 3.0 + idx) * 1.5)
            draw.circle((px, py), radius=p_rad, fill=(56, 189, 248))


class IsometricBarChart:
    """
    Renders a 3D isometric comparative bar chart (e.g. 'open models, by size').
    One target pillar is highlighted with high contrast and a base label pill.
    """

    def __init__(self):
        try:
            self.font_title = ImageFont.truetype("arialbd.ttf", 16)
            self.font_mono = ImageFont.truetype("consola.ttf", 14)
        except Exception:
            self.font_title = ImageFont.load_default()
            self.font_mono = ImageFont.load_default()

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        t: float,
        center: Tuple[int, int] = (540, 680),
        highlight_idx: int = 2,
    ):
        # Header Badge: 'open models, by size'
        draw.text((center[0] - 280, center[1] - 380), "⬡ open models, by size", font=self.font_mono, fill=(180, 83, 9))

        bars = [
            ("Model A", 120, False),
            ("Model B", 220, False),
            ("Kimi K3", 520, True),   # Tall highlighted pillar
            ("Model C", 260, False),
            ("Model D", 170, False),
        ]

        bar_w = 42.0
        spacing = 90.0
        start_x = -((len(bars) - 1) * spacing) / 2.0

        # Floor ground ellipse
        draw.ellipse(
            [center[0] - 320, center[1] + 80, center[0] + 320, center[1] + 180],
            fill=(210, 215, 215, 160),
        )

        for i, (name, target_h, is_target) in enumerate(bars):
            bx = start_x + i * spacing
            grow_prog = get_progress(t, 0.2 + i * 0.1, 0.6, "ease_out_cubic")
            h = target_h * grow_prog

            b_orig = (center[0] + bx, center[1] + 120)

            # Colors
            if is_target:
                c_top = (70, 95, 130)
                c_left = (40, 65, 95)
                c_right = (25, 45, 75)
                edge_col = (90, 120, 160)
            else:
                c_top = (235, 235, 235)
                c_left = (210, 210, 210)
                c_right = (185, 185, 185)
                edge_col = (200, 200, 200)

            hw = bar_w / 2.0
            p_top_back = iso_project(-hw, -hw, h, b_orig)
            p_top_right = iso_project(hw, -hw, h, b_orig)
            p_top_front = iso_project(hw, hw, h, b_orig)
            p_top_left = iso_project(-hw, hw, h, b_orig)

            p_bot_left = iso_project(-hw, hw, 0, b_orig)
            p_bot_front = iso_project(hw, hw, 0, b_orig)
            p_bot_right = iso_project(hw, -hw, 0, b_orig)

            # Draw faces
            draw.polygon([p_top_back, p_top_right, p_top_front, p_top_left], fill=c_top, outline=edge_col)
            draw.polygon([p_top_left, p_top_front, p_bot_front, p_bot_left], fill=c_left, outline=edge_col)
            draw.polygon([p_top_front, p_top_right, p_bot_right, p_bot_front], fill=c_right, outline=edge_col)

            # Target Pillar Pill Badge
            if is_target and grow_prog > 0.8:
                pw, ph = 120, 36
                px0 = b_orig[0] - pw // 2
                py0 = b_orig[1] + 20
                draw.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], radius=8, fill=(15, 23, 42))
                draw.text((px0 + 20, py0 + 8), f"K  {name}", font=self.font_title, fill=(255, 255, 255))


class IsometricHardwareModels:
    """
    Renders realistic hardware components:
    1. M.2 NVMe SSD (PCB, controller, 4 NAND chips, PCIe contacts)
    2. RAM DIMM stick (Green PCB, DRAM chips, notch, gold pins)
    """

    def __init__(self):
        try:
            self.font_badge = ImageFont.truetype("arialbd.ttf", 14)
            self.font_mono = ImageFont.truetype("consola.ttf", 12)
        except Exception:
            self.font_badge = ImageFont.load_default()
            self.font_mono = ImageFont.load_default()

    def render_m2_ssd(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[int, int] = (540, 1150),
        scale: float = 1.0,
        t: float = 1.0,
    ):
        """Renders an isometric M.2 NVMe SSD drive with black NAND chips and badge."""
        orig = center

        # SSD PCB base: Length ~280, Width ~80, Thickness ~16
        pcb_len = 160.0
        pcb_w = 50.0
        pcb_thick = 14.0

        p0 = iso_project(-pcb_len, -pcb_w, pcb_thick, orig)
        p1 = iso_project(pcb_len, -pcb_w, pcb_thick, orig)
        p2 = iso_project(pcb_len, pcb_w, pcb_thick, orig)
        p3 = iso_project(-pcb_len, pcb_w, pcb_thick, orig)

        b0 = iso_project(-pcb_len, pcb_w, 0, orig)
        b1 = iso_project(pcb_len, pcb_w, 0, orig)
        b2 = iso_project(pcb_len, -pcb_w, 0, orig)

        # PCB colors (matte navy/slate PCB)
        draw.polygon([p0, p1, p2, p3], fill=(70, 95, 125), outline=(90, 115, 145))
        draw.polygon([p3, p2, b1, b0], fill=(45, 65, 90), outline=(90, 115, 145))
        draw.polygon([p2, p1, b2, b1], fill=(35, 50, 70), outline=(90, 115, 145))

        # 4 NAND Flash packages on top
        chip_len = 30.0
        chip_w = 34.0
        chip_thick = 5.0
        chip_spacing = 38.0

        for i in range(4):
            cx = -pcb_len + 45.0 + i * chip_spacing
            cp0 = iso_project(cx, -chip_w / 2, pcb_thick + chip_thick, orig)
            cp1 = iso_project(cx + chip_len, -chip_w / 2, pcb_thick + chip_thick, orig)
            cp2 = iso_project(cx + chip_len, chip_w / 2, pcb_thick + chip_thick, orig)
            cp3 = iso_project(cx, chip_w / 2, pcb_thick + chip_thick, orig)

            cb0 = iso_project(cx, chip_w / 2, pcb_thick, orig)
            cb1 = iso_project(cx + chip_len, chip_w / 2, pcb_thick, orig)

            # Dark NAND chip
            draw.polygon([cp0, cp1, cp2, cp3], fill=(30, 35, 42), outline=(50, 55, 65))
            draw.polygon([cp3, cp2, cb1, cb0], fill=(20, 22, 28))

        # SSD Pill Badge
        badge_x0 = center[0] + 160
        badge_y0 = center[1] - 40
        draw.rounded_rectangle([badge_x0, badge_y0, badge_x0 + 90, badge_y0 + 36], radius=6, fill=(15, 23, 42))
        draw.text((badge_x0 + 16, badge_y0 + 8), "🗄 SSD", font=self.font_badge, fill=(255, 255, 255))

    def render_ram_stick(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[int, int] = (540, 1050),
        label: str = "8 GB RAM",
    ):
        """Renders a stylized green RAM DIMM stick with gold contacts and white badge."""
        rw = 840
        rh = 140
        rx0 = center[0] - rw // 2
        ry0 = center[1] - rh // 2

        # Green PCB
        draw.rounded_rectangle([rx0, ry0, rx0 + rw, ry0 + rh], radius=12, fill=(20, 83, 45), outline=(22, 101, 52), width=3)

        # Gold PCIe pin contacts along bottom
        pin_step = 14
        pin_h = 30
        for px in range(rx0 + 24, rx0 + rw - 24, pin_step):
            # Center notch gap
            if abs(px - center[0]) < 18:
                continue
            draw.rectangle([px, ry0 + rh - pin_h, px + 8, ry0 + rh - 4], fill=(234, 179, 8))

        # 8 DRAM chips on PCB
        chip_w = 64
        chip_h = 60
        chip_y = ry0 + 20
        for i in range(8):
            cx = rx0 + 36 + i * (chip_w + 34)
            draw.rounded_rectangle([cx, chip_y, cx + chip_w, chip_y + chip_h], radius=6, fill=(24, 24, 27))

        # Central white badge: "8 GB RAM"
        bw = 240
        bh = 52
        bx0 = center[0] - bw // 2
        by0 = center[1] - bh // 2 - 10
        draw.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
        draw.text((bx0 + 28, by0 + 10), label, font=ImageFont.truetype("arialbd.ttf", 26) if hasattr(self, 'font_badge') else self.font_badge, fill=(15, 23, 42))


class IsometricLayerStack:
    """
    Renders 93 stacked neural network layers with the top layer sliding outward (Always-On part).
    """

    def __init__(self):
        try:
            self.font_badge = ImageFont.truetype("arialbd.ttf", 13)
            self.font_mono = ImageFont.truetype("consola.ttf", 12)
        except Exception:
            self.font_badge = ImageFont.load_default()
            self.font_mono = ImageFont.load_default()

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        t: float,
        center: Tuple[int, int] = (300, 750),
    ):
        num_visible_layers = 26
        layer_h = 8.0
        spacing = 11.0
        w = 90.0

        for i in range(num_visible_layers):
            z = i * spacing
            c_orig = (center[0], center[1])

            # Top layer slides outward
            is_top = (i == num_visible_layers - 1)
            slide_x = (math.sin(t * 1.8) * 35.0 + 40.0) if is_top else 0.0

            p0 = iso_project(-w + slide_x, -w, z + layer_h, c_orig)
            p1 = iso_project(w + slide_x, -w, z + layer_h, c_orig)
            p2 = iso_project(w + slide_x, w, z + layer_h, c_orig)
            p3 = iso_project(-w + slide_x, w, z + layer_h, c_orig)

            b0 = iso_project(-w + slide_x, w, z, c_orig)
            b1 = iso_project(w + slide_x, w, z, c_orig)

            c_top = (96, 125, 158) if is_top else (65, 85, 110)
            draw.polygon([p0, p1, p2, p3], fill=c_top, outline=(110, 135, 165))
            draw.polygon([p3, p2, b1, b0], fill=(45, 60, 80))

            if is_top:
                # Pill badge: ALWAYS-ON PART
                bx = p2[0] - 120
                by = p2[1] - 40
                draw.rounded_rectangle([bx, by, bx + 155, by + 28], radius=6, fill=(15, 23, 42))
                draw.text((bx + 10, by + 6), "✦ ALWAYS-ON PART", font=self.font_badge, fill=(255, 255, 255))

        # Bottom label
        draw.text((center[0] - 110, center[1] + 160), "93 layers · used for every word", font=self.font_mono, fill=(100, 116, 139))
