"""
SUPER.INTELLIGENCEEE — Phase 6 BitNet b1.58 Explanatory Motion Compositions
Implements full-bleed 1080x1920 explanatory visualizations for 1-bit LLMs,
ternary matrix quantization {-1, 0, +1}, silicon addition datapaths, and CPU inference.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Tuple
from PIL import Image, ImageDraw, ImageFont

from core.universal_scene_contract import UniversalSceneContract
from rendering.visual_intelligence_engine.composition_base import BaseVisualIntelligenceComposition


def draw_hud_reticle(draw: ImageDraw.Draw, x: float, y: float, w: float, h: float, t: float, color: tuple = (0, 229, 255)):
    """Draws an animated technical HUD bracket around the target area."""
    corner = 20
    pad = 6
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, outline=color, width=2)
    # Corner accents
    draw.line([(x - pad, y - pad), (x - pad + corner, y - pad)], fill=color, width=3)
    draw.line([(x - pad, y - pad), (x - pad, y - pad + corner)], fill=color, width=3)
    draw.line([(x + w + pad, y - pad), (x + w + pad - corner, y - pad)], fill=color, width=3)
    draw.line([(x + w + pad, y - pad), (x + w + pad, y - pad + corner)], fill=color, width=3)
    draw.line([(x - pad, y + h + pad), (x - pad + corner, y + h + pad)], fill=color, width=3)
    draw.line([(x - pad, y + h + pad), (x - pad, y + h + pad - corner)], fill=color, width=3)
    draw.line([(x + w + pad, y + h + pad), (x + w + pad - corner, y + h + pad)], fill=color, width=3)
    draw.line([(x + w + pad, y + h + pad), (x + w + pad, y + h + pad - corner)], fill=color, width=3)


class BitNetMultiplierObliterationComposition(BaseVisualIntelligenceComposition):
    """
    Scene 1: Multiplier Obliteration Hook.
    Visualizes the death of the floating-point multiplication symbol,
    shattering a 16-bit MAC equation into cyan particle sparks with a laser strike.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        cx = self.width / 2.0 + pan_x
        cy = 960.0 + pan_y

        # Floating FP16 equation in gold/white
        eq_y = cy - 80
        draw.text((cx - 360, eq_y - 120), "TRADITIONAL LLM GEMM", fill=(148, 163, 184), font=self.font_sans_head)
        
        # Draw equation text
        draw.text((cx - 380, eq_y - 20), "Y  =  W", fill=(255, 255, 255), font=self.font_sans_bold)
        draw.text((cx - 160, eq_y - 45), "[FP16]", fill=(245, 158, 11), font=self.font_mono)
        
        # Giant multiplication operator
        mult_x = cx - 30
        mult_y = eq_y - 20
        draw.text((mult_x, mult_y), "×", fill=(239, 68, 68), font=self.font_sans_bold)
        
        draw.text((mult_x + 90, eq_y - 20), "X", fill=(255, 255, 255), font=self.font_sans_bold)
        draw.text((mult_x + 150, eq_y - 45), "[FP16]", fill=(245, 158, 11), font=self.font_mono)

        # Silicon Energy Tag
        draw.text((cx - 160, eq_y + 80), "3.7 pJ per operation", fill=(239, 68, 68), font=self.font_mono_bold)

        # Laser strike animation at t >= 1.6s
        strike_progress = min(1.0, max(0.0, (t - 1.6) * 3.5))
        if strike_progress > 0:
            x1 = mult_x - 120
            y1 = eq_y - 90
            x2 = x1 + 280 * strike_progress
            y2 = y1 + 180 * strike_progress

            # Laser beam line
            draw.line([(x1, y1), (x2, y2)], fill=(255, 51, 102), width=10)
            draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255), width=4)

            # Impact shockwave ring
            if strike_progress > 0.5:
                ring_r = int((strike_progress - 0.5) * 220)
                draw.ellipse([mult_x + 20 - ring_r, mult_y + 30 - ring_r, mult_x + 20 + ring_r, mult_y + 30 + ring_r],
                             outline=(0, 229, 255), width=3)

            # Shattered cyan particle sparks
            for i in range(24):
                angle = (i / 24.0) * 2 * math.pi
                dist = strike_progress * (140 + (i % 5) * 35)
                px = mult_x + 20 + math.cos(angle) * dist
                py = mult_y + 30 + math.sin(angle) * dist
                draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(0, 229, 255))

        # Bottom Callout Badge
        if t > 2.8:
            badge_y = cy + 260
            draw_hud_reticle(draw, cx - 320, badge_y - 40, 640, 80, t, (0, 229, 255))
            draw.text((cx - 280, badge_y - 14), "MULTIPLIERS ELIMINATED", fill=(0, 229, 255), font=self.font_sans_head)


class BitNetMemoryWallComposition(BaseVisualIntelligenceComposition):
    """
    Scene 2: 2.5D Isometric GPU Memory Wall.
    Illustrates HBM memory bandwidth choking compute cores with 140 GB weight movement.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        cx = self.width / 2.0 + pan_x
        cy = 960.0 + pan_y

        # Top Node: HBM3 Memory Stack (80 GB)
        hbm_y = cy - 360
        draw.rounded_rectangle([cx - 280, hbm_y - 60, cx + 280, hbm_y + 60], radius=16, fill=(15, 23, 42), outline=(245, 158, 11), width=3)
        draw.text((cx - 220, hbm_y - 35), "HBM3 MEMORY STACK", fill=(255, 255, 255), font=self.font_sans_head)
        draw.text((cx - 140, hbm_y + 8), "140 GB Weight Bus (70B Model)", fill=(245, 158, 11), font=self.font_mono)

        # Bottom Node: Tensor Compute Cores
        core_y = cy + 280
        draw.rounded_rectangle([cx - 280, core_y - 60, cx + 280, core_y + 60], radius=16, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((cx - 200, core_y - 35), "GPU COMPUTE CORES", fill=(255, 255, 255), font=self.font_sans_head)
        draw.text((cx - 160, core_y + 8), "Waiting for Weights (Idle FLOPS)", fill=(148, 163, 184), font=self.font_mono)

        # Memory Bus Chasm with Traffic Jam Packets
        bus_top = hbm_y + 60
        bus_bottom = core_y - 60
        
        # Dual bus boundary rails
        draw.line([(cx - 120, bus_top), (cx - 120, bus_bottom)], fill=(71, 85, 105), width=2)
        draw.line([(cx + 120, bus_top), (cx + 120, bus_bottom)], fill=(71, 85, 105), width=2)

        # Jammed Amber Packets moving down slowly
        packet_count = 14
        for i in range(packet_count):
            p_prog = ((t * 0.4 + i / float(packet_count)) % 1.0)
            py = bus_top + p_prog * (bus_bottom - bus_top)
            px = cx + math.sin(i * 1.5) * 60
            draw.rounded_rectangle([px - 35, py - 15, px + 35, py + 15], radius=6, fill=(245, 158, 11), outline=(255, 255, 255), width=1)
            draw.text((px - 22, py - 8), "FP16", fill=(0, 0, 0), font=self.font_mono)

        # Thermal Warning Bar on Right Side
        gauge_x = cx + 360
        gauge_y = cy - 200
        draw.rectangle([gauge_x, gauge_y, gauge_x + 36, gauge_y + 400], fill=(30, 41, 59), outline=(148, 163, 184), width=2)
        
        # Dynamic Fill
        fill_h = min(400.0, 100.0 + t * 45.0)
        draw.rectangle([gauge_x + 2, gauge_y + 400 - fill_h, gauge_x + 34, gauge_y + 398], fill=(239, 68, 68))
        draw.text((gauge_x - 30, gauge_y - 35), "450W", fill=(239, 68, 68), font=self.font_mono_bold)
        draw.text((gauge_x - 80, gauge_y + 420), "MEMORY WALL", fill=(239, 68, 68), font=self.font_mono)


class BitNetTernaryMatrixComposition(BaseVisualIntelligenceComposition):
    """
    Scene 3: Ternary Matrix Transformation ({-1, 0, +1}).
    Visualizes high-density tensor weights flipping from continuous floats into discrete ternary states.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        cx = self.width / 2.0 + pan_x
        cy = 960.0 + pan_y

        # Center Matrix Grid (6 columns x 6 rows)
        grid_cols = 6
        grid_rows = 6
        cell_w = 110
        cell_h = 75
        start_x = cx - (grid_cols * cell_w) / 2.0
        start_y = cy - 280

        # Flip trigger at t >= 1.5s
        flip_t = max(0.0, t - 1.5)

        for r in range(grid_rows):
            for c in range(grid_cols):
                x = start_x + c * cell_w
                y = start_y + r * cell_h
                
                # Deterministic ternary value based on coordinate
                val_mod = (r * 7 + c * 3 + 1) % 3
                # 0 -> 0, 1 -> +1, 2 -> -1
                ternary_val = 1 if val_mod == 1 else (-1 if val_mod == 2 else 0)

                cell_progress = min(1.0, max(0.0, (flip_t * 2.5 - (r + c) * 0.1)))

                if cell_progress < 0.5:
                    # Floating point initial state
                    fill_c = (30, 41, 59)
                    outline_c = (71, 85, 105)
                    text_val = f"{0.12 * (r - c):+.2f}"
                    text_color = (148, 163, 184)
                else:
                    # Ternary final state
                    if ternary_val == 1:
                        fill_c = (14, 116, 144)      # Cyan tint
                        outline_c = (0, 229, 255)
                        text_val = "+1"
                        text_color = (0, 229, 255)
                    elif ternary_val == -1:
                        fill_c = (109, 40, 217)     # Violet tint
                        outline_c = (168, 85, 247)
                        text_val = "-1"
                        text_color = (216, 180, 254)
                    else:
                        fill_c = (15, 23, 42)       # Dim dark
                        outline_c = (51, 65, 85)
                        text_val = " 0"
                        text_color = (100, 116, 139)

                draw.rounded_rectangle([x + 4, y + 4, x + cell_w - 4, y + cell_h - 4], radius=8, fill=fill_c, outline=outline_c, width=2)
                draw.text((x + 24, y + 22), text_val, fill=text_color, font=self.font_mono_bold)

        # Big Stat Callout Below Matrix
        stat_y = cy + 240
        draw_hud_reticle(draw, cx - 340, stat_y - 20, 680, 130, t, (0, 229, 255))
        draw.text((cx - 240, stat_y), "1.58 BITS / WEIGHT", fill=(0, 229, 255), font=self.font_sans_bold)
        draw.text((cx - 180, stat_y + 65), "log₂(3) States: {-1, 0, +1}", fill=(241, 245, 249), font=self.font_mono)


class BitNetLogicMultiplexerComposition(BaseVisualIntelligenceComposition):
    """
    Scene 4: Silicon Datapath Logic Multiplexer.
    Deconstructs GEMM into conditional integer addition:
    +1 -> ADD (+x), -1 -> SUB (-x), 0 -> SKIP.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        cx = self.width / 2.0 + pan_x
        cy = 960.0 + pan_y

        # Left: Activation Input Vector x_j
        in_x = cx - 380
        in_y = cy - 20
        draw.rounded_rectangle([in_x - 60, in_y - 70, in_x + 60, in_y + 70], radius=14, fill=(30, 41, 59), outline=(56, 189, 248), width=3)
        draw.text((in_x - 45, in_y - 45), "INPUT", fill=(148, 163, 184), font=self.font_mono)
        draw.text((in_x - 30, in_y - 10), "x[j]", fill=(0, 229, 255), font=self.font_sans_head)
        draw.text((in_x - 40, in_y + 25), "INT8", fill=(245, 158, 11), font=self.font_mono)

        # Center: 3-Way Ternary Logic Multiplexer MUX
        mux_x = cx - 80
        mux_y = cy - 20
        draw.polygon([(mux_x - 60, mux_y - 120), (mux_x + 60, mux_y - 160), 
                      (mux_x + 60, mux_y + 160), (mux_x - 60, mux_y + 120)], 
                     fill=(15, 23, 42), outline=(0, 229, 255))
        draw.text((mux_x - 35, mux_y - 20), "MUX", fill=(0, 229, 255), font=self.font_sans_head)

        # Connection line from input to MUX
        draw.line([(in_x + 60, in_y), (mux_x - 60, mux_y)], fill=(0, 229, 255), width=4)

        # 3 Branch Paths from MUX
        out_x = cx + 220
        
        # Branch 1 (+1): ADD
        add_y = cy - 180
        draw.line([(mux_x + 60, mux_y - 80), (out_x - 80, add_y)], fill=(0, 229, 255), width=3)
        draw.rounded_rectangle([out_x - 80, add_y - 40, out_x + 140, add_y + 40], radius=10, fill=(14, 116, 144), outline=(0, 229, 255), width=2)
        draw.text((out_x - 60, add_y - 16), "W = +1 ➜ ADD (+x)", fill=(255, 255, 255), font=self.font_mono_bold)

        # Branch 2 (0): SKIP
        skip_y = cy - 20
        draw.line([(mux_x + 60, mux_y), (out_x - 80, skip_y)], fill=(100, 116, 139), width=3)
        draw.rounded_rectangle([out_x - 80, skip_y - 40, out_x + 140, skip_y + 40], radius=10, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
        draw.text((out_x - 60, skip_y - 16), "W =  0 ➜ ZERO (SKIP)", fill=(148, 163, 184), font=self.font_mono_bold)

        # Branch 3 (-1): SUB
        sub_y = cy + 140
        draw.line([(mux_x + 60, mux_y + 80), (out_x - 80, sub_y)], fill=(168, 85, 247), width=3)
        draw.rounded_rectangle([out_x - 80, sub_y - 40, out_x + 140, sub_y + 40], radius=10, fill=(109, 40, 217), outline=(168, 85, 247), width=2)
        draw.text((out_x - 60, sub_y - 16), "W = -1 ➜ SUB (-x)", fill=(255, 255, 255), font=self.font_mono_bold)

        # Animated Pulse Traversal along active branch
        pulse_phase = (t * 2.0) % 3.0
        if pulse_phase < 1.0:
            # Pulse along ADD branch
            px = (mux_x + 60) + pulse_phase * (out_x - 80 - (mux_x + 60))
            py = (mux_y - 80) + pulse_phase * (add_y - (mux_y - 80))
            draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(255, 255, 255))
        elif pulse_phase < 2.0:
            p_sub = pulse_phase - 1.0
            px = (mux_x + 60) + p_sub * (out_x - 80 - (mux_x + 60))
            py = (mux_y + 80) + p_sub * (sub_y - (mux_y + 80))
            draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(255, 255, 255))

        # Bottom Datapath Tag
        draw.text((cx - 220, cy + 260), "PURE CONDITIONAL INTEGER ADDITION", fill=(0, 229, 255), font=self.font_sans_head)


class BitNetBenchmarkExtrusionComposition(BaseVisualIntelligenceComposition):
    """
    Scene 5: 3D Comparative Benchmark Extrusion.
    Compares FP16 MAC Energy (3.7 pJ) vs BitNet Add Energy (0.1 pJ) -> 71.4x Savings.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        cx = self.width / 2.0 + pan_x
        cy = 960.0 + pan_y

        baseline_y = cy + 220
        bar_w = 220

        # Bar 1: FP16 MAC Unit (3.7 pJ)
        bar1_x = cx - 280
        bar1_h = 420
        draw.rounded_rectangle([bar1_x, baseline_y - bar1_h, bar1_x + bar_w, baseline_y], radius=12, fill=(185, 28, 28), outline=(239, 68, 68), width=3)
        draw.text((bar1_x + 25, baseline_y - bar1_h - 55), "3.7 pJ", fill=(239, 68, 68), font=self.font_sans_bold)
        draw.text((bar1_x + 35, baseline_y - bar1_h + 30), "FP16 MAC", fill=(255, 255, 255), font=self.font_mono_bold)
        draw.text((bar1_x + 20, baseline_y - bar1_h + 75), "Standard GPU", fill=(254, 202, 202), font=self.font_mono)

        # Bar 2: BitNet Integer Add (0.1 pJ)
        bar2_x = cx + 60
        # Dynamic rise
        rise = min(1.0, t * 1.5)
        bar2_h = int(12 + rise * 28)
        draw.rounded_rectangle([bar2_x, baseline_y - bar2_h, bar2_x + bar_w, baseline_y], radius=8, fill=(14, 116, 144), outline=(0, 229, 255), width=3)
        draw.text((bar2_x + 30, baseline_y - bar2_h - 55), "0.1 pJ", fill=(0, 229, 255), font=self.font_sans_bold)
        draw.text((bar2_x + 25, baseline_y + 25), "BITNET ADD", fill=(0, 229, 255), font=self.font_mono_bold)

        # Big Stat Counter
        mult_counter = min(71.4, 1.0 + t * 24.0)
        draw_hud_reticle(draw, cx - 360, cy - 380, 720, 140, t, (0, 229, 255))
        draw.text((cx - 280, cy - 360), f"{mult_counter:.1f}X LESS ENERGY", fill=(0, 229, 255), font=self.font_sans_bold)
        draw.text((cx - 220, cy - 290), "Arithmetic Energy Consumption on 7nm Silicon", fill=(148, 163, 184), font=self.font_mono)


class BitNetTerminalDemoComposition(BaseVisualIntelligenceComposition):
    """
    Scene 6: Real-World CPU Inference & Terminal Demonstration.
    Displays the authentic bitnet.cpp CLI inference benchmark asset.
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        # Load acquired terminal demo asset
        asset_path = Path("A:/SUPER.INTELLIGENCEEE/output/drafts/phase6_bitnet/assets/bitnet_terminal_execution_demo.png")
        if asset_path.exists():
            self.terminal_img = Image.open(asset_path).convert("RGBA")
        else:
            self.terminal_img = None

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        cx = self.width / 2.0 + pan_x
        cy = 960.0 + pan_y

        # Paste Terminal Asset if available
        if self.terminal_img:
            # Rescale slightly for frame
            tw, th = self.terminal_img.size
            dest_x = int(cx - tw // 2)
            dest_y = int(cy - th // 2 - 40)
            canvas.paste(self.terminal_img, (dest_x, dest_y), self.terminal_img)
            
            # Draw HUD frame around terminal
            draw_hud_reticle(draw, dest_x - 12, dest_y - 12, tw + 24, th + 24, t, (0, 229, 255))

        # Bottom Hardware Verification Pill
        pill_y = cy + 360
        draw.rounded_rectangle([cx - 340, pill_y - 35, cx + 340, pill_y + 35], radius=16, fill=(15, 23, 42), outline=(34, 197, 94), width=2)
        draw.text((cx - 310, pill_y - 14), "✓ 70B MODEL EXECUTING ON LOCAL CPU", fill=(34, 197, 94), font=self.font_sans_head)


class BitNetOutroComposition(BaseVisualIntelligenceComposition):
    """
    Scene 7: 1-Bit Computing Horizon & Outro.
    Radiant discrete logic core pulsating outwards with branding lockup.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        cx = self.width / 2.0 + pan_x
        cy = 960.0 + pan_y

        # Concentric glowing rings
        pulse = (t * 1.5) % 1.0
        for i in range(5):
            r = int(140 + i * 70 + pulse * 40)
            alpha = max(0, int(180 - i * 35))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 229, 255), width=2)

        # Center branding core
        core_r = 110
        draw.ellipse([cx - core_r, cy - core_r, cx + core_r, cy + core_r], fill=(15, 23, 42), outline=(0, 229, 255), width=4)
        draw.text((cx - 65, cy - 25), "{-1, 0, 1}", fill=(0, 229, 255), font=self.font_mono_bold)

        # Branding text
        out_y = cy + 280
        draw_hud_reticle(draw, cx - 340, out_y - 30, 680, 110, t, (0, 229, 255))
        draw.text((cx - 280, out_y - 10), "SUPER.INTELLIGENCEEE", fill=(255, 255, 255), font=self.font_sans_bold)
        draw.text((cx - 180, out_y + 45), "The Future of 1-Bit Computing", fill=(0, 229, 255), font=self.font_mono)
