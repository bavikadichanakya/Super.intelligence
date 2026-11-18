"""
SUPER.INTELLIGENCEEE — Phase 9 Master Visual Research & Proof-of-Concept Engine
Produces:
1. Subtitle Direction Comparison Frame & Artifacts (Direction 1, 2, 3)
2. Prototype A: Physical Technology (Dilution Refrigerator matching user reference)
3. Prototype B: Abstract Technical Concept (Quantum Surface Code & Error Healing)
4. Prototype C: Real-World Documentary (Nature Paper, Threshold Curve, Supercomputer)
5. Multi-Track Audio (Kokoro-82M speech + procedural sound design + EBU R128)
6. High-Resolution Contact Sheets & Telemetry Benchmarks
"""

from __future__ import annotations

import os
import sys
import time
import math
import json
import hashlib
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Tuple
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_ROOT = Path("A:/SUPER.INTELLIGENCEEE").resolve()
sys.path.insert(0, str(WORKSPACE_ROOT))

from audio.providers.kokoro_direct import KokoroDirectRunner
from rendering.resource_guard import ResourceGuard

PROTOTYPES_DIR = WORKSPACE_ROOT / "output" / "drafts" / "phase9_prototypes"
SUBTITLES_DIR = PROTOTYPES_DIR / "subtitles"
FRAMES_DIR = PROTOTYPES_DIR / "frames"
USER_REFERENCE_IMG = WORKSPACE_ROOT / "output" / "reference_assets" / "user_reference_cryostat.jpg"

PROTOTYPES_DIR.mkdir(parents=True, exist_ok=True)
SUBTITLES_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

# Font Resolver
def get_font(name: str, size: int):
    candidates = [
        Path(f"C:/Windows/Fonts/{name}"),
        Path(f"C:/Windows/Fonts/{name.lower()}"),
        Path(f"C:/Windows/Fonts/{name.upper()}"),
    ]
    for c in candidates:
        if c.exists():
            try:
                return ImageFont.truetype(str(c), size)
            except Exception:
                pass
    return ImageFont.load_default()

FONT_HERO = get_font("ariblk.ttf", 64)
FONT_TITLE = get_font("arialbd.ttf", 46)
FONT_SUBTITLE = get_font("segoeui.ttf", 34)
FONT_LABEL = get_font("arialbd.ttf", 26)
FONT_MONO = get_font("consolab.ttf", 26)
FONT_MONO_SM = get_font("consola.ttf", 20)
FONT_SUBTITLE_D1 = get_font("ariblk.ttf", 48)
FONT_SUBTITLE_D2 = get_font("arialbd.ttf", 46)
FONT_SUBTITLE_D3 = get_font("consolab.ttf", 42)


# ==============================================================================
# SUBTITLE DIRECTION GENERATORS
# ==============================================================================

def draw_subtitle_direction_1(canvas: Image.Image, text: str, active_word_idx: int, cy: int = 1420):
    """
    Direction 1: Kinetic Word-Highlight Editorial (The Master Explainer)
    Dynamic pill capsule with frosted glass, active word in golden amber with spring bounce.
    """
    draw = ImageDraw.Draw(canvas, "RGBA")
    words = text.split()
    font = FONT_SUBTITLE_D1
    
    # Measure word widths
    word_widths = [draw.textbbox((0, 0), w, font=font)[2] for w in words]
    space_w = draw.textbbox((0, 0), " ", font=font)[2]
    total_w = sum(word_widths) + space_w * (len(words) - 1)
    
    pill_padding_x = 36
    pill_padding_y = 20
    pill_x0 = (canvas.width - total_w) // 2 - pill_padding_x
    pill_x1 = (canvas.width + total_w) // 2 + pill_padding_x
    pill_y0 = cy - 30 - pill_padding_y
    pill_y1 = cy + 30 + pill_padding_y
    
    # Frosted dark pill background with subtle golden edge
    draw.rounded_rectangle([pill_x0, pill_y0, pill_x1, pill_y1], radius=24, fill=(10, 15, 26, 215), outline=(212, 175, 55, 90), width=2)
    
    # Draw words
    cur_x = (canvas.width - total_w) // 2
    for idx, (word, w_len) in enumerate(zip(words, word_widths)):
        if idx == active_word_idx:
            # Active word: Golden Amber (#FCD34D) with subtle glow
            draw.text((cur_x - 1, cy - 26), word, font=font, fill=(252, 211, 77, 180))
            draw.text((cur_x + 1, cy - 24), word, font=font, fill=(252, 211, 77, 180))
            draw.text((cur_x, cy - 25), word, font=font, fill=(252, 211, 77, 255))
        else:
            # Inactive words: Crisp white at 75% opacity
            draw.text((cur_x, cy - 25), word, font=font, fill=(240, 243, 246, 190))
        cur_x += w_len + space_w


def draw_subtitle_direction_2(canvas: Image.Image, text: str, active_word_idx: int, cy: int = 1420):
    """
    Direction 2: Clean Phrase-Group Dynamic Lower-Third (The BBC / Vox Editorial)
    Zero background box. Dual-pass soft drop shadow for clean contrast. Active word in electric cyan.
    """
    draw = ImageDraw.Draw(canvas, "RGBA")
    words = text.split()
    font = FONT_SUBTITLE_D2
    
    word_widths = [draw.textbbox((0, 0), w, font=font)[2] for w in words]
    space_w = draw.textbbox((0, 0), " ", font=font)[2]
    total_w = sum(word_widths) + space_w * (len(words) - 1)
    
    cur_x = (canvas.width - total_w) // 2
    for idx, (word, w_len) in enumerate(zip(words, word_widths)):
        # Multi-pass shadow
        for ox, oy in [(-2, 2), (2, 2), (0, 3), (0, -2)]:
            draw.text((cur_x + ox, cy - 24 + oy), word, font=font, fill=(0, 0, 0, 160))
            
        if idx == active_word_idx:
            # Active word: Electric Cyan (#38BDF8)
            draw.text((cur_x, cy - 24), word, font=font, fill=(56, 189, 248, 255))
            # Underline stroke
            draw.line([cur_x, cy + 28, cur_x + w_len, cy + 28], fill=(56, 189, 248, 255), width=3)
        else:
            # Clean pure white
            draw.text((cur_x, cy - 24), word, font=font, fill=(255, 255, 255, 240))
        cur_x += w_len + space_w


def draw_subtitle_direction_3(canvas: Image.Image, text: str, active_word_idx: int, cy: int = 1420):
    """
    Direction 3: Floating Dimensional Contextual Capsule (The Apple / Modernist AR)
    Glassmorphic floating capsule, monospace tabular typography, active word in soft mint green.
    """
    draw = ImageDraw.Draw(canvas, "RGBA")
    words = text.split()
    font = FONT_SUBTITLE_D3
    
    word_widths = [draw.textbbox((0, 0), w, font=font)[2] for w in words]
    space_w = draw.textbbox((0, 0), " ", font=font)[2]
    total_w = sum(word_widths) + space_w * (len(words) - 1)
    
    pill_padding_x = 44
    pill_padding_y = 16
    pill_x0 = (canvas.width - total_w) // 2 - pill_padding_x
    pill_x1 = (canvas.width + total_w) // 2 + pill_padding_x
    pill_y0 = cy - 26 - pill_padding_y
    pill_y1 = cy + 26 + pill_padding_y
    
    # Translucent glassmorphic border and fill
    draw.rounded_rectangle([pill_x0, pill_y0, pill_x1, pill_y1], radius=16, fill=(15, 23, 42, 190), outline=(56, 189, 248, 120), width=1)
    # Subtle top edge reflection highlight
    draw.line([pill_x0 + 16, pill_y0 + 1, pill_x1 - 16, pill_y0 + 1], fill=(255, 255, 255, 80), width=1)
    
    cur_x = (canvas.width - total_w) // 2
    for idx, (word, w_len) in enumerate(zip(words, word_widths)):
        if idx == active_word_idx:
            # Active word: Mint Green (#34D399) with glowing outline
            draw.text((cur_x, cy - 22), word, font=font, fill=(52, 211, 153, 255))
        else:
            draw.text((cur_x, cy - 22), word, font=font, fill=(203, 213, 225, 200))
        cur_x += w_len + space_w


# ==============================================================================
# PROTOTYPE RENDER ENGINES
# ==============================================================================

class PrototypeAPhysicalTechnology:
    """
    Prototype A: Dilution Refrigerator Physical Technology.
    Direct realization of user-uploaded reference image:
    - Deep indigo/violet background with ambient molecular network
    - Grey cylindrical top stage
    - Tapered titanium structural support struts
    - 4 gold stages with realistic metallic gradients & highlights
    - Dense bundles of vertical RF coaxial cables with stress-relief coils
    - Cold finger and dual gold amplifier cans
    - Continuous 1.04x camera push-in and slow crane down
    - Subtitle: Direction 1 Kinetic Word-Highlight Editorial
    """
    def __init__(self, duration: float = 9.0, width: int = 1080, height: int = 1920):
        self.duration = duration
        self.width = width
        self.height = height
        self.subtitle_chunks = [
            ("To protect fragile qubits", 0.0, 2.5),
            ("from room-temperature noise,", 2.5, 5.0),
            ("Willow is suspended inside", 5.0, 7.0),
            ("a multi-stage dilution refrigerator.", 7.0, 9.0)
        ]

    def render_frame(self, t: float) -> Image.Image:
        canvas = Image.new("RGBA", (self.width, self.height), (8, 4, 26, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # 1. Background Radial Vignette (Deep indigo to violet center)
        cx, cy = self.width // 2, self.height // 2 - 100
        for r in range(1000, 200, -120):
            alpha = int((1.0 - r / 1000.0) * 35)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(24, 14, 65, alpha))
            
        # 2. Ambient Molecular / Hexagonal Bond Lattice (Reference Match)
        self._draw_ambient_molecules(draw, t)
        
        # 3. Virtual Camera Motion (Continuous push-in + slow crane down)
        cam_zoom = 1.0 + 0.04 * (t / self.duration)
        cam_pan_y = int(30 * (t / self.duration))
        
        # 4. Dilution Refrigerator Physical Assembly
        self._draw_cryostat_assembly(draw, canvas, t, cam_zoom, cam_pan_y)
        
        # 5. Cryogenic Mist Floating Particles
        self._draw_cryogenic_mist(draw, t)
        
        # 6. Editorial Header & Temperature Readout
        self._draw_editorial_hud(draw, t)
        
        # 7. Subtitles: Direction 1 (Kinetic Word-Highlight)
        self._draw_subtitles(canvas, t)
        
        return canvas

    def _draw_ambient_molecules(self, draw: ImageDraw.Draw, t: float):
        """Draws faint chemical ring structures on left and right borders like the reference image."""
        drift_y = (t * 8) % 200
        mol_color = (40, 50, 110, 50)
        bond_color = (35, 45, 95, 40)
        
        # Left molecular cluster
        left_centers = [(140, 360 + drift_y), (220, 500 + drift_y), (100, 640 + drift_y), (180, 1100 - drift_y), (120, 1260 - drift_y)]
        for x, y in left_centers:
            draw.ellipse([x - 22, y - 22, x + 22, y + 22], fill=mol_color)
            draw.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(15, 20, 50, 120))
        # Bonds
        for i in range(len(left_centers) - 1):
            p1, p2 = left_centers[i], left_centers[i+1]
            draw.line([p1[0], p1[1], p2[0], p2[1]], fill=bond_color, width=4)
            
        # Right molecular cluster
        right_centers = [(940, 320 - drift_y), (860, 460 - drift_y), (980, 600 - drift_y), (900, 1150 + drift_y), (960, 1300 + drift_y)]
        for x, y in right_centers:
            draw.ellipse([x - 22, y - 22, x + 22, y + 22], fill=mol_color)
            draw.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(15, 20, 50, 120))
        for i in range(len(right_centers) - 1):
            p1, p2 = right_centers[i], right_centers[i+1]
            draw.line([p1[0], p1[1], p2[0], p2[1]], fill=bond_color, width=4)

    def _draw_cryostat_assembly(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float, zoom: float, pan_y: int):
        cx = self.width // 2
        base_y = int(240 * zoom + pan_y)
        
        # Stage positions relative to base_y
        top_flange_y = base_y
        stage_50k_y = base_y + int(340 * zoom)
        stage_4k_y = base_y + int(520 * zoom)
        stage_100mk_y = base_y + int(690 * zoom)
        stage_15mk_y = base_y + int(860 * zoom)
        cold_finger_y = stage_15mk_y + int(140 * zoom)
        
        # --- A. Tapered Structural Struts (Top Collar to 50K) ---
        strut_color = (220, 226, 235, 220)
        strut_shadow = (140, 150, 165, 180)
        # 4 struts
        strut_coords = [
            # Top attachment -> Bottom attachment
            ((cx - int(240 * zoom), top_flange_y + int(120 * zoom)), (cx - int(210 * zoom), stage_50k_y)),
            ((cx - int(120 * zoom), top_flange_y + int(120 * zoom)), (cx - int(90 * zoom), stage_50k_y)),
            ((cx + int(120 * zoom), top_flange_y + int(120 * zoom)), (cx + int(90 * zoom), stage_50k_y)),
            ((cx + int(240 * zoom), top_flange_y + int(120 * zoom)), (cx + int(210 * zoom), stage_50k_y)),
        ]
        for p_top, p_bot in strut_coords:
            # Draw strut with 3D width
            draw.polygon([
                (p_top[0] - 6, p_top[1]), (p_top[0] + 6, p_top[1]),
                (p_bot[0] + 4, p_bot[1]), (p_bot[0] - 4, p_bot[1])
            ], fill=strut_color)
            draw.line([p_top[0] + 4, p_top[1], p_bot[0] + 3, p_bot[1]], fill=strut_shadow, width=2)
            
        # --- B. Vertical Coaxial RF Cable Bundles ---
        # Stage 0 to 1 (Top to 50K)
        self._draw_cable_loom(draw, cx - int(160 * zoom), cx - int(40 * zoom), top_flange_y + int(120 * zoom), stage_50k_y, num_cables=10, zoom=zoom)
        self._draw_cable_loom(draw, cx + int(40 * zoom), cx + int(160 * zoom), top_flange_y + int(120 * zoom), stage_50k_y, num_cables=10, zoom=zoom)
        
        # Stage 1 to 2 (50K to 4K)
        self._draw_cable_loom(draw, cx - int(200 * zoom), cx - int(50 * zoom), stage_50k_y + int(24 * zoom), stage_4k_y, num_cables=14, with_loops=True, zoom=zoom)
        self._draw_cable_loom(draw, cx + int(50 * zoom), cx + int(200 * zoom), stage_50k_y + int(24 * zoom), stage_4k_y, num_cables=14, with_loops=True, zoom=zoom)
        
        # Stage 2 to 3 (4K to 100mK)
        self._draw_cable_loom(draw, cx - int(180 * zoom), cx - int(40 * zoom), stage_4k_y + int(22 * zoom), stage_100mk_y, num_cables=12, with_loops=True, zoom=zoom)
        self._draw_cable_loom(draw, cx + int(40 * zoom), cx + int(180 * zoom), stage_4k_y + int(22 * zoom), stage_100mk_y, num_cables=12, with_loops=True, zoom=zoom)
        
        # Stage 3 to 4 (100mK to 15mK)
        self._draw_cable_loom(draw, cx - int(150 * zoom), cx - int(30 * zoom), stage_100mk_y + int(20 * zoom), stage_15mk_y, num_cables=10, with_loops=True, zoom=zoom)
        self._draw_cable_loom(draw, cx + int(30 * zoom), cx + int(150 * zoom), stage_100mk_y + int(20 * zoom), stage_15mk_y, num_cables=10, with_loops=True, zoom=zoom)
        
        # --- C. Central Thermal Structural Column ---
        col_w = int(24 * zoom)
        draw.rectangle([cx - col_w, top_flange_y + int(120 * zoom), cx + col_w, cold_finger_y], fill=(225, 230, 240, 240))
        draw.line([cx - col_w, top_flange_y + int(120 * zoom), cx - col_w, cold_finger_y], fill=(160, 170, 185, 255), width=2)
        # Attenuator blocks on center column
        for att_y in [stage_50k_y + int(70 * zoom), stage_4k_y + int(80 * zoom), stage_100mk_y + int(70 * zoom)]:
            draw.rectangle([cx - int(20 * zoom), att_y - int(18 * zoom), cx + int(20 * zoom), att_y + int(18 * zoom)], fill=(212, 175, 55, 255), outline=(255, 235, 140, 255), width=2)

        # --- D. Gold Thermal Stage Disks (With 3D Metallic Shading) ---
        self._draw_gold_stage_plate(draw, cx, stage_50k_y, width=int(540 * zoom), height=int(26 * zoom), label="50 KELVIN STAGE")
        self._draw_gold_stage_plate(draw, cx, stage_4k_y, width=int(460 * zoom), height=int(24 * zoom), label="4 KELVIN STILL")
        self._draw_gold_stage_plate(draw, cx, stage_100mk_y, width=int(380 * zoom), height=int(22 * zoom), label="100 mK COLD STAGE")
        self._draw_gold_stage_plate(draw, cx, stage_15mk_y, width=int(330 * zoom), height=int(20 * zoom), label="15 mK MIXING FLANGE")
        
        # --- E. Top Cylindrical Vacuum Stage (Grey Metal Gradient) ---
        top_w = int(520 * zoom)
        top_h = int(120 * zoom)
        # Top lip
        draw.rectangle([cx - top_w // 2 - int(20 * zoom), top_flange_y, cx + top_w // 2 + int(20 * zoom), top_flange_y + int(22 * zoom)], fill=(230, 235, 242, 255))
        # Main cylindrical body with horizontal lighting gradient
        for step in range(top_w):
            norm_u = step / top_w
            # Cosine lighting with specular highlight around u = 0.45
            light = 0.55 + 0.35 * math.cos((norm_u - 0.45) * math.pi)
            grey_val = int(min(255, 150 + light * 90))
            draw.line([cx - top_w // 2 + step, top_flange_y + int(22 * zoom), cx - top_w // 2 + step, top_flange_y + top_h], fill=(grey_val, grey_val, int(grey_val * 1.05), 255), width=1)
        # Bottom rim lip
        draw.rectangle([cx - top_w // 2 - int(10 * zoom), top_flange_y + top_h, cx + top_w // 2 + int(10 * zoom), top_flange_y + top_h + int(14 * zoom)], fill=(200, 205, 215, 255))
        
        # --- F. Bottom RF Amplifier Cans & Cold Finger (Reference Match) ---
        # Dual gold amplifier cans flanking the center
        can_w = int(58 * zoom)
        can_h = int(110 * zoom)
        for offset_x in [-int(85 * zoom), int(85 * zoom)]:
            can_x0 = cx + offset_x - can_w // 2
            can_x1 = cx + offset_x + can_w // 2
            can_y0 = stage_15mk_y + int(24 * zoom)
            can_y1 = can_y0 + can_h
            # Draw can body
            draw.rectangle([can_x0, can_y0, can_x1, can_y1], fill=(212, 160, 40, 255), outline=(255, 225, 120, 255), width=2)
            # Ribbed horizontal ridges
            for ridge_y in range(can_y0 + 10, can_y1 - 10, int(14 * zoom)):
                draw.line([can_x0 + 4, ridge_y, can_x1 - 4, ridge_y], fill=(160, 110, 20, 255), width=2)
                
        # Central Cold Finger (Nickel-Plated Copper)
        cf_w = int(46 * zoom)
        cf_h = int(140 * zoom)
        draw.rectangle([cx - cf_w // 2, stage_15mk_y + int(20 * zoom), cx + cf_w // 2, stage_15mk_y + int(20 * zoom) + cf_h], fill=(120, 128, 138, 255), outline=(210, 220, 230, 255), width=2)
        
        # Willow Qubit Processor Enclosure at tip
        willow_box_w = int(76 * zoom)
        willow_box_h = int(40 * zoom)
        willow_y0 = stage_15mk_y + int(20 * zoom) + cf_h
        draw.rounded_rectangle([cx - willow_box_w // 2, willow_y0, cx + willow_box_w // 2, willow_y0 + willow_box_h], radius=6, fill=(24, 28, 38, 255), outline=(56, 189, 248, 255), width=2)
        # Glowing cyan chip die inside
        draw.rectangle([cx - int(18 * zoom), willow_y0 + int(10 * zoom), cx + int(18 * zoom), willow_y0 + int(30 * zoom)], fill=(56, 189, 248, 255))

    def _draw_cable_loom(self, draw: ImageDraw.Draw, x0: int, x1: int, y0: int, y1: int, num_cables: int, with_loops: bool = False, zoom: float = 1.0):
        """Draws dense vertical silver coaxial cables with optional stress-relief loops."""
        step = (x1 - x0) / max(1, num_cables - 1)
        cable_color = (235, 240, 248, 230)
        cable_shade = (160, 170, 185, 180)
        for i in range(num_cables):
            x = x0 + i * step
            if with_loops and (i % 2 == 0):
                # Stress relief loop coil
                loop_y = y0 + (y1 - y0) * 0.5
                draw.line([x, y0, x, loop_y - int(12 * zoom)], fill=cable_color, width=2)
                draw.arc([x - int(8 * zoom), loop_y - int(14 * zoom), x + int(8 * zoom), loop_y + int(14 * zoom)], start=0, end=360, fill=(212, 175, 55, 230), width=2)
                draw.line([x, loop_y + int(12 * zoom), x, y1], fill=cable_color, width=2)
            else:
                draw.line([x, y0, x, y1], fill=cable_color, width=2)
                draw.line([x + 1, y0, x + 1, y1], fill=cable_shade, width=1)

    def _draw_gold_stage_plate(self, draw: ImageDraw.Draw, cx: int, cy: int, width: int, height: int, label: str):
        """Draws a gilded copper stage plate with top specular highlight and 3D bevel."""
        x0 = cx - width // 2
        x1 = cx + width // 2
        y0 = cy
        y1 = cy + height
        
        # 1. Base Warm Gold Gradient
        draw.rectangle([x0, y0, x1, y1], fill=(212, 175, 55, 255))
        # 2. Top Specular Reflection Strip
        draw.rectangle([x0, y0, x1, y0 + 4], fill=(255, 248, 200, 255))
        # 3. Bottom Ambient Occlusion Shadow Lip
        draw.rectangle([x0, y1 - 4, x1, y1], fill=(130, 85, 18, 255))
        # 4. Gold edge borders
        draw.line([x0, y0, x0, y1], fill=(255, 235, 140, 255), width=2)
        draw.line([x1, y0, x1, y1], fill=(130, 85, 18, 255), width=2)
        
        # Stage label on the right side
        draw.text((x1 + 16, y0 - 2), label, font=FONT_LABEL, fill=(212, 175, 55, 220))
        draw.line([x1 + 4, y0 + height // 2, x1 + 12, y0 + height // 2], fill=(212, 175, 55, 180), width=2)

    def _draw_cryogenic_mist(self, draw: ImageDraw.Draw, t: float):
        for i in range(35):
            px = 300 + (i * 47 + int(math.sin(t * 1.5 + i) * 60)) % 480
            py = 1450 - ((int(t * 60) + i * 40) % 900)
            alpha = int(max(0, min(140, 140 * math.sin((1450 - py) / 900.0 * math.pi))))
            draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(180, 230, 255, alpha))

    def _draw_editorial_hud(self, draw: ImageDraw.Draw, t: float):
        # Top Header
        draw.text((54, 80), "PHYSICAL INSTRUMENTATION // 01", font=FONT_LABEL, fill=(212, 175, 55, 255))
        draw.text((54, 114), "DILUTION REFRIGERATOR", font=FONT_TITLE, fill=(255, 255, 255, 255))
        draw.text((54, 168), "Cooling Willow processor to 10 mK — colder than deep space", font=FONT_SUBTITLE, fill=(148, 163, 184, 230))
        
        # Bottom Right Metric Readout
        draw.text((760, 1260), "STAGE 4 TEMP", font=FONT_MONO_SM, fill=(148, 163, 184, 200))
        draw.text((760, 1286), "0.010 KELVIN", font=FONT_MONO, fill=(56, 189, 248, 255))
        draw.text((760, 1318), "VACUUM: 10^-8 MBAR", font=FONT_MONO_SM, fill=(148, 163, 184, 180))

    def _draw_subtitles(self, canvas: Image.Image, t: float):
        # Find active chunk
        active_chunk = None
        for chunk, t0, t1 in self.subtitle_chunks:
            if t0 <= t < t1:
                active_chunk = (chunk, t0, t1)
                break
        if not active_chunk:
            active_chunk = self.subtitle_chunks[-1]
            
        text, t0, t1 = active_chunk
        words = text.split()
        dur = max(0.1, t1 - t0)
        word_dur = dur / len(words)
        active_idx = min(len(words) - 1, int((t - t0) / word_dur))
        
        # Direction 1: Kinetic Word-Highlight Editorial
        draw_subtitle_direction_1(canvas, text, active_idx, cy=1480)


# ==============================================================================
# PROTOTYPE B: ABSTRACT TECHNICAL CONCEPT (SURFACE CODE & ERROR HEALING)
# ==============================================================================

class PrototypeBAbstractConcept:
    """
    Prototype B: Quantum Surface Code Lattice & Topological Error Healing.
    - 2.5D perspective silicon die with gold wire bonds
    - Checkerboard array of data qubits (cyan circles) and syndrome ancillas (diamonds)
    - Interactive error event: data qubit flashes red at t = 2.8s
    - Topological stabilizer parity check wave pulses outward
    - Cyan laser healing beam restores quantum phase coherence at t = 5.2s
    - Camera smoothly zooms in from 1.0x to 1.35x into the failing plaquette
    - Subtitle: Direction 2 Clean Phrase-Group Dynamic Lower-Third
    """
    def __init__(self, duration: float = 8.5, width: int = 1080, height: int = 1920):
        self.duration = duration
        self.width = width
        self.height = height
        self.subtitle_chunks = [
            ("When thermal decoherence flips", 0.0, 2.5),
            ("a physical data qubit,", 2.5, 4.5),
            ("topological syndrome checks", 4.5, 6.5),
            ("instantly heal the disturbance.", 6.5, 8.5)
        ]

    def render_frame(self, t: float) -> Image.Image:
        canvas = Image.new("RGBA", (self.width, self.height), (10, 14, 26, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # 1. Background Grid & Ambient Quantum Waves
        self._draw_quantum_field_background(draw, t)
        
        # 2. Camera Zoom & Pan tracking the error node
        # Zoom from 1.0x to 1.32x starting at t=2.5s
        zoom_prog = max(0.0, min(1.0, (t - 2.0) / 2.5))
        ease_zoom = 3 * zoom_prog**2 - 2 * zoom_prog**3
        cam_zoom = 1.0 + 0.32 * ease_zoom
        cam_offset_x = int(-40 * ease_zoom)
        cam_offset_y = int(-60 * ease_zoom)
        
        # 3. 2.5D Silicon Processor Package Base
        self._draw_chip_carrier(draw, t, cam_zoom, cam_offset_x, cam_offset_y)
        
        # 4. Surface Code Checkerboard Lattice (Data + Syndrome Qubits)
        self._draw_surface_code_lattice(draw, t, cam_zoom, cam_offset_x, cam_offset_y)
        
        # 5. Editorial Header & Live Telemetry HUD
        self._draw_hud_telemetry(draw, t)
        
        # 6. Subtitles: Direction 2 (Clean Phrase-Group Lower-Third)
        self._draw_subtitles(canvas, t)
        
        return canvas

    def _draw_quantum_field_background(self, draw: ImageDraw.Draw, t: float):
        cx, cy = self.width // 2, self.height // 2
        for r in range(900, 200, -140):
            alpha = int((1.0 - r / 900.0) * 25)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(16, 36, 75, alpha))
            
    def _draw_chip_carrier(self, draw: ImageDraw.Draw, t: float, zoom: float, off_x: int, off_y: int):
        cx = self.width // 2 + off_x
        cy = 820 + off_y
        card_w = int(720 * zoom)
        card_h = int(720 * zoom)
        x0, y0 = cx - card_w // 2, cy - card_h // 2
        x1, y1 = cx + card_w // 2, cy + card_h // 2
        
        # Silicon Die Shadow
        draw.rounded_rectangle([x0 + 10, y0 + 16, x1 + 10, y1 + 16], radius=24, fill=(0, 0, 0, 90))
        # Silicon Package Ground Plane
        draw.rounded_rectangle([x0, y0, x1, y1], radius=24, fill=(18, 24, 38, 255), outline=(45, 60, 90, 255), width=3)
        # Gold Wire Bonds around perimeter
        for bx in range(x0 + 60, x1 - 50, 40):
            draw.line([bx, y0, bx, y0 - 30], fill=(212, 175, 55, 200), width=2)
            draw.line([bx, y1, bx, y1 + 30], fill=(212, 175, 55, 200), width=2)
        for by in range(y0 + 60, y1 - 50, 40):
            draw.line([x0, by, x0 - 30, by], fill=(212, 175, 55, 200), width=2)
            draw.line([x1, by, x1 + 30, by], fill=(212, 175, 55, 200), width=2)

    def _draw_surface_code_lattice(self, draw: ImageDraw.Draw, t: float, zoom: float, off_x: int, off_y: int):
        cx = self.width // 2 + off_x
        cy = 820 + off_y
        grid_n = 4
        spacing = int(120 * zoom)
        start_x = cx - int((grid_n - 1) * spacing / 2)
        start_y = cy - int((grid_n - 1) * spacing / 2)
        
        error_t = 2.8
        heal_t = 5.2
        error_active = (t >= error_t)
        healed = (t >= heal_t)
        
        # 1. Plaquettes (Z-type and X-type error stabilizers)
        for r in range(grid_n - 1):
            for c in range(grid_n - 1):
                px0 = start_x + c * spacing
                py0 = start_y + r * spacing
                px1 = px0 + spacing
                py1 = py0 + spacing
                
                is_z = ((r + c) % 2 == 0)
                is_error_plaq = (r == 1 and c == 1)
                
                if is_error_plaq and error_active and not healed:
                    # Flashing alarm plaquette
                    pulse = math.sin((t - error_t) * 12) * 0.5 + 0.5
                    fill_c = (239, 68, 68, int(40 + pulse * 60))
                    edge_c = (239, 68, 68, int(140 + pulse * 100))
                elif is_z:
                    fill_c = (56, 189, 248, 25)
                    edge_c = (56, 189, 248, 70)
                else:
                    fill_c = (129, 140, 248, 25)
                    edge_c = (129, 140, 248, 70)
                    
                draw.rectangle([px0, py0, px1, py1], fill=fill_c, outline=edge_c, width=2)
                
                # Central syndrome ancilla diamond
                anc_x = (px0 + px1) // 2
                anc_y = (py0 + py1) // 2
                rad = int(14 * zoom)
                
                if is_error_plaq and error_active and not healed:
                    # Ancilla flags syndrome in amber/yellow
                    anc_fill = (252, 211, 77, 255)
                    # Expanding detection ripple wave
                    wave_r = int((t - error_t) * 90 * zoom) % int(spacing * 1.5)
                    draw.ellipse([anc_x - wave_r, anc_y - wave_r, anc_x + wave_r, anc_y + wave_r], outline=(252, 211, 77, max(0, 200 - wave_r * 2)), width=3)
                else:
                    anc_fill = (129, 140, 248, 220)
                    
                draw.polygon([
                    (anc_x, anc_y - rad), (anc_x + rad, anc_y),
                    (anc_x, anc_y + rad), (anc_x - rad, anc_y)
                ], fill=anc_fill)

        # 2. Resonator Coupler Bus Lines
        for r in range(grid_n):
            for c in range(grid_n):
                x = start_x + c * spacing
                y = start_y + r * spacing
                if c < grid_n - 1:
                    draw.line([x, y, x + spacing, y], fill=(70, 90, 130, 140), width=3)
                if r < grid_n - 1:
                    draw.line([x, y, x, y + spacing], fill=(70, 90, 130, 140), width=3)

        # 3. Data Qubits (Circular Nodes)
        for r in range(grid_n):
            for c in range(grid_n):
                x = start_x + c * spacing
                y = start_y + r * spacing
                q_rad = int(18 * zoom)
                
                # Targeted error node at (r=1, c=1)
                if r == 1 and c == 1:
                    if error_active and not healed:
                        # Crimson Red Decoherence Error Flare
                        pulse = math.sin((t - error_t) * 16) * 0.5 + 0.5
                        draw.ellipse([x - q_rad - 8, y - q_rad - 8, x + q_rad + 8, y + q_rad + 8], fill=(239, 68, 68, int(80 + pulse * 120)))
                        draw.ellipse([x - q_rad, y - q_rad, x + q_rad, y + q_rad], fill=(239, 68, 68, 255), outline=(255, 200, 200, 255), width=3)
                        # Error label
                        draw.text((x + q_rad + 8, y - 16), "BIT-FLIP ERROR", font=FONT_LABEL, fill=(239, 68, 68, 255))
                    elif healed:
                        # Restored Coherence Burst
                        heal_prog = min(1.0, (t - heal_t) / 1.0)
                        burst_r = int(q_rad + heal_prog * 40)
                        draw.ellipse([x - burst_r, y - burst_r, x + burst_r, y + burst_r], outline=(56, 189, 248, int(255 * (1.0 - heal_prog))), width=3)
                        draw.ellipse([x - q_rad, y - q_rad, x + q_rad, y + q_rad], fill=(56, 189, 248, 255), outline=(255, 255, 255, 255), width=3)
                        draw.text((x + q_rad + 8, y - 16), "RESTORED", font=FONT_LABEL, fill=(56, 189, 248, 255))
                    else:
                        draw.ellipse([x - q_rad, y - q_rad, x + q_rad, y + q_rad], fill=(56, 189, 248, 255), outline=(255, 255, 255, 255), width=2)
                else:
                    # Normal Coherent Data Qubit
                    draw.ellipse([x - q_rad, y - q_rad, x + q_rad, y + q_rad], fill=(56, 189, 248, 240), outline=(200, 240, 255, 220), width=2)
                    
        # 4. Laser Stabilizer Healing Beam ($t \in [4.5, 5.5]$)
        if 4.2 <= t <= 5.4:
            anc_x = start_x + int(0.5 * spacing)
            anc_y = start_y + int(0.5 * spacing)
            target_x = start_x + spacing
            target_y = start_y + spacing
            beam_alpha = int(240 * math.sin((t - 4.2) / 1.2 * math.pi))
            draw.line([anc_x, anc_y, target_x, target_y], fill=(56, 189, 248, beam_alpha), width=6)
            draw.line([anc_x, anc_y, target_x, target_y], fill=(255, 255, 255, beam_alpha), width=2)

    def _draw_hud_telemetry(self, draw: ImageDraw.Draw, t: float):
        # Header
        draw.text((54, 80), "QUANTUM STABILIZER DYNAMICS // 02", font=FONT_LABEL, fill=(56, 189, 248, 255))
        draw.text((54, 114), "SURFACE CODE LATTICE", font=FONT_TITLE, fill=(255, 255, 255, 255))
        draw.text((54, 168), "Autonomous syndrome measurement & real-time topological healing", font=FONT_SUBTITLE, fill=(148, 163, 184, 230))
        
        # Status Card Bottom
        if t < 2.8:
            status_txt = "LATTICE COHERENCE: 99.98%"
            status_col = (56, 189, 248, 255)
        elif t < 5.2:
            status_txt = "ALERT: DECOHERENCE SYNDROME AT (1,1)"
            status_col = (239, 68, 68, 255)
        else:
            status_txt = "CORRECTION APPLIED // CYCLE TIME: 840 ns"
            status_col = (52, 211, 153, 255)
            
        draw.text((54, 1260), "REAL-TIME DIAGNOSTIC", font=FONT_MONO_SM, fill=(148, 163, 184, 200))
        draw.text((54, 1288), status_txt, font=FONT_MONO, fill=status_col)

    def _draw_subtitles(self, canvas: Image.Image, t: float):
        active_chunk = None
        for chunk, t0, t1 in self.subtitle_chunks:
            if t0 <= t < t1:
                active_chunk = (chunk, t0, t1)
                break
        if not active_chunk:
            active_chunk = self.subtitle_chunks[-1]
            
        text, t0, t1 = active_chunk
        words = text.split()
        dur = max(0.1, t1 - t0)
        word_dur = dur / len(words)
        active_idx = min(len(words) - 1, int((t - t0) / word_dur))
        
        # Direction 2: Clean Phrase-Group Dynamic Lower-Third
        draw_subtitle_direction_2(canvas, text, active_idx, cy=1480)


# ==============================================================================
# PROTOTYPE C: REAL-WORLD DOCUMENTARY (NATURE PAPER & SCALE CONTRAST)
# ==============================================================================

class PrototypeCDocumentaryReality:
    """
    Prototype C: Real-World Documentary Reality.
    - Authentic Nature publication card with editorial paper texture
    - Animated exponential threshold scaling curve drawing dynamically
    - Threshold boundary indicating break-even
    - Split-scale comparison: Frontier Supercomputer (10 septillion years) vs Willow (<5 minutes)
    - Subtitle: Direction 3 Floating Dimensional Contextual Capsule
    """
    def __init__(self, duration: float = 9.5, width: int = 1080, height: int = 1920):
        self.duration = duration
        self.width = width
        self.height = height
        self.subtitle_chunks = [
            ("Published in Nature, Willow crossed", 0.0, 2.5),
            ("the historic error threshold:", 2.5, 4.5),
            ("exponentially suppressing noise,", 4.5, 7.0),
            ("finishing in five minutes what takes septillions of years.", 7.0, 9.5)
        ]

    def render_frame(self, t: float) -> Image.Image:
        canvas = Image.new("RGBA", (self.width, self.height), (12, 16, 28, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # 1. Background Lighting
        cx = self.width // 2
        for r in range(950, 300, -150):
            alpha = int((1.0 - r / 950.0) * 22)
            draw.ellipse([cx - r, 700 - r, cx + r, 700 + r], fill=(20, 35, 70, alpha))
            
        # 2. Upper Third: Nature Publication Manuscript Card
        self._draw_nature_paper_card(draw, t)
        
        # 3. Middle Section: Exponential Scaling Curve (Draws dynamically)
        self._draw_threshold_scaling_curve(draw, t)
        
        # 4. Lower Third: The 10-Septillion-Year Split Comparison
        self._draw_split_supercomputer_comparison(draw, t)
        
        # 5. Editorial Header
        draw.text((54, 80), "HISTORIC BREAKTHROUGH // 03", font=FONT_LABEL, fill=(212, 175, 55, 255))
        draw.text((54, 114), "BELOW-THRESHOLD SCALING", font=FONT_TITLE, fill=(255, 255, 255, 255))
        
        # 6. Subtitles: Direction 3 (Floating Dimensional Contextual Capsule)
        self._draw_subtitles(canvas, t)
        
        return canvas

    def _draw_nature_paper_card(self, draw: ImageDraw.Draw, t: float):
        cx = self.width // 2
        card_w, card_h = 970, 220
        x0, y0 = cx - card_w // 2, 180
        x1, y1 = x0 + card_w, y0 + card_h
        
        # Textured paper card
        draw.rounded_rectangle([x0 + 6, y0 + 10, x1 + 6, y1 + 10], radius=16, fill=(0, 0, 0, 95))
        draw.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=(248, 247, 244, 255), outline=(220, 218, 210, 255), width=2)
        
        # Nature Banner
        draw.text((x0 + 36, y0 + 24), "nature", font=FONT_TITLE, fill=(200, 30, 30, 255))
        draw.text((x0 + 190, y0 + 32), "|  VOL 636  |  9 DECEMBER 2024  |  ACCELERATED ARTICLE", font=FONT_LABEL, fill=(80, 85, 95, 255))
        draw.line([x0 + 36, y0 + 82, x1 - 36, y0 + 82], fill=(220, 215, 205, 255), width=2)
        
        # Paper Title
        draw.text((x0 + 36, y0 + 100), "Quantum error correction below the surface code threshold", font=FONT_TITLE, fill=(15, 23, 42, 255))
        draw.text((x0 + 36, y0 + 160), "Google Quantum AI Collaborative  *  Achieving Lambda = 2.14 > 1.0", font=FONT_SUBTITLE, fill=(71, 85, 105, 255))

    def _draw_threshold_scaling_curve(self, draw: ImageDraw.Draw, t: float):
        cx = self.width // 2
        plot_w, plot_h = 970, 360
        x0, y0 = cx - plot_w // 2, 440
        x1, y1 = x0 + plot_w, y0 + plot_h
        
        # Blueprint Plot Background
        draw.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=(16, 22, 36, 255), outline=(40, 55, 80, 255), width=2)
        
        # Axes
        ax_x0, ax_y0 = x0 + 120, y1 - 60
        ax_x1, ax_y1 = x1 - 60, y0 + 40
        draw.line([ax_x0, ax_y0, ax_x1, ax_y0], fill=(100, 115, 140, 255), width=2) # X axis
        draw.line([ax_x0, ax_y0, ax_x0, ax_y1], fill=(100, 115, 140, 255), width=2) # Y axis
        
        # Axis Labels
        draw.text((ax_x1 - 180, ax_y0 + 16), "CODE DISTANCE (d)", font=FONT_MONO_SM, fill=(148, 163, 184, 255))
        draw.text((x0 + 20, y0 + 20), "LOGICAL ERROR RATE", font=FONT_MONO_SM, fill=(148, 163, 184, 255))
        
        # Code distance ticks: d=3, d=5, d=7
        d_ticks = [(ax_x0 + 160, "d = 3"), (ax_x0 + 400, "d = 5"), (ax_x0 + 640, "d = 7")]
        for tx, tlabel in d_ticks:
            draw.line([tx, ax_y0 - 6, tx, ax_y0 + 6], fill=(148, 163, 184, 255), width=2)
            draw.text((tx - 24, ax_y0 + 12), tlabel, font=FONT_MONO, fill=(220, 230, 245, 255))
            
        # Threshold line at Y = midpoint
        thresh_y = y0 + 140
        draw.line([ax_x0, thresh_y, ax_x1, thresh_y], fill=(239, 68, 68, 160), width=2)
        draw.text((ax_x1 - 260, thresh_y - 28), "THRESHOLD (Lambda = 1.0)", font=FONT_MONO_SM, fill=(239, 68, 68, 220))
        
        # Dynamic Curve Drawing (Starts at t=1.0s, finishes at t=5.0s)
        curve_prog = max(0.0, min(1.0, (t - 1.0) / 4.0))
        ease_curve = 3 * curve_prog**2 - 2 * curve_prog**3
        
        pts = [
            (ax_x0 + 160, thresh_y + 30),   # d=3: just above threshold
            (ax_x0 + 400, thresh_y + 110),  # d=5: lower error
            (ax_x0 + 640, thresh_y + 180),  # d=7: drastically lower
        ]
        
        max_idx = int(ease_curve * (len(pts) - 1))
        frac = (ease_curve * (len(pts) - 1)) - max_idx
        
        drawn_pts = []
        for i in range(max_idx + 1):
            drawn_pts.append(pts[i])
        if max_idx < len(pts) - 1 and frac > 0.0:
            interp_x = pts[max_idx][0] + (pts[max_idx + 1][0] - pts[max_idx][0]) * frac
            interp_y = pts[max_idx][1] + (pts[max_idx + 1][1] - pts[max_idx][1]) * frac
            drawn_pts.append((interp_x, interp_y))
            
        # Draw curve segments with glowing cyan stroke
        for i in range(len(drawn_pts) - 1):
            p1, p2 = drawn_pts[i], drawn_pts[i + 1]
            draw.line([p1[0], p1[1], p2[0], p2[1]], fill=(56, 189, 248, 120), width=8)
            draw.line([p1[0], p1[1], p2[0], p2[1]], fill=(255, 255, 255, 255), width=3)
            
        # Glowing head at leading point
        if drawn_pts:
            hx, hy = drawn_pts[-1]
            draw.ellipse([hx - 10, hy - 10, hx + 10, hy + 10], fill=(56, 189, 248, 255))
            draw.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=(255, 255, 255, 255))
            
        # Milestone badge at d=7 if drawn
        if curve_prog > 0.85:
            draw.text((pts[2][0] - 60, pts[2][1] - 44), "LAMBDA = 2.14", font=FONT_LABEL, fill=(52, 211, 153, 255))

    def _draw_split_supercomputer_comparison(self, draw: ImageDraw.Draw, t: float):
        cx = self.width // 2
        y0 = 840
        w, h = 970, 420
        x0, y1 = cx - w // 2, y0 + h
        x1 = x0 + w
        mid_x = cx
        
        # Container
        draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=(16, 20, 32, 255), outline=(40, 50, 75, 255), width=2)
        draw.line([mid_x, y0 + 20, mid_x, y1 - 20], fill=(40, 50, 75, 255), width=2)
        
        # Left Side: Classical Supercomputer (Frontier)
        draw.text((x0 + 40, y0 + 30), "CLASSICAL SUPERCOMPUTER", font=FONT_MONO_SM, fill=(239, 68, 68, 255))
        draw.text((x0 + 40, y0 + 64), "FRONTIER (OAK RIDGE)", font=FONT_TITLE, fill=(240, 240, 245, 255))
        
        # Accelerating counter
        draw.text((x0 + 40, y0 + 150), "TIME TO COMPUTE:", font=FONT_MONO_SM, fill=(148, 163, 184, 220))
        draw.text((x0 + 40, y0 + 190), "10 SEPTILLION", font=FONT_HERO, fill=(239, 68, 68, 255))
        draw.text((x0 + 40, y0 + 270), "YEARS (10^25 YR)", font=FONT_TITLE, fill=(239, 68, 68, 220))
        draw.text((x0 + 40, y0 + 330), "* Exceeds age of the known universe", font=FONT_SUBTITLE, fill=(148, 163, 184, 180))
        
        # Right Side: Google Willow Quantum Processor
        draw.text((mid_x + 40, y0 + 30), "QUANTUM PROCESSOR", font=FONT_MONO_SM, fill=(52, 211, 153, 255))
        draw.text((mid_x + 40, y0 + 64), "GOOGLE WILLOW", font=FONT_TITLE, fill=(240, 240, 245, 255))
        
        draw.text((mid_x + 40, y0 + 150), "TIME TO COMPUTE:", font=FONT_MONO_SM, fill=(148, 163, 184, 220))
        draw.text((mid_x + 40, y0 + 190), "< 5 MINUTES", font=FONT_HERO, fill=(52, 211, 153, 255))
        draw.text((mid_x + 40, y0 + 270), "(UNDER 300 SECONDS)", font=FONT_TITLE, fill=(52, 211, 153, 220))
        
        # Progress bar resolving
        bar_prog = min(1.0, max(0.0, (t - 2.0) / 4.0))
        bar_w = 400
        draw.rectangle([mid_x + 40, y0 + 335, mid_x + 40 + bar_w, y0 + 355], fill=(30, 40, 60, 255))
        draw.rectangle([mid_x + 40, y0 + 335, mid_x + 40 + int(bar_w * bar_prog), y0 + 355], fill=(52, 211, 153, 255))

    def _draw_subtitles(self, canvas: Image.Image, t: float):
        active_chunk = None
        for chunk, t0, t1 in self.subtitle_chunks:
            if t0 <= t < t1:
                active_chunk = (chunk, t0, t1)
                break
        if not active_chunk:
            active_chunk = self.subtitle_chunks[-1]
            
        text, t0, t1 = active_chunk
        words = text.split()
        dur = max(0.1, t1 - t0)
        word_dur = dur / len(words)
        active_idx = min(len(words) - 1, int((t - t0) / word_dur))
        
        # Direction 3: Floating Dimensional Contextual Capsule
        draw_subtitle_direction_3(canvas, text, active_idx, cy=1480)


# ==============================================================================
# SUBTITLE DIRECTIONS COMPARISON RENDERER
# ==============================================================================

def render_subtitle_directions_comparison():
    """Renders a 3-panel side-by-side composite demonstrating Direction 1, 2, and 3."""
    print("\n[SUBTITLES] Rendering 3-Direction Subtitle Comparison Frame...")
    comp_a = PrototypeAPhysicalTechnology()
    base_frame = comp_a.render_frame(t=4.0)
    
    # 1. Direction 1 Frame
    frame_d1 = base_frame.copy()
    draw_subtitle_direction_1(frame_d1, "Willow is suspended inside a dilution refrigerator.", active_word_idx=4, cy=1450)
    d = ImageDraw.Draw(frame_d1)
    d.text((54, 1340), "DIRECTION 1: KINETIC WORD-HIGHLIGHT EDITORIAL", font=FONT_LABEL, fill=(252, 211, 77, 255))
    d1_path = SUBTITLES_DIR / "direction_1_word_highlight.png"
    frame_d1.save(d1_path)
    
    # 2. Direction 2 Frame
    frame_d2 = base_frame.copy()
    draw_subtitle_direction_2(frame_d2, "Willow is suspended inside a dilution refrigerator.", active_word_idx=4, cy=1450)
    d = ImageDraw.Draw(frame_d2)
    d.text((54, 1340), "DIRECTION 2: CLEAN PHRASE-GROUP DYNAMIC LOWER-THIRD", font=FONT_LABEL, fill=(56, 189, 248, 255))
    d2_path = SUBTITLES_DIR / "direction_2_phrase_group.png"
    frame_d2.save(d2_path)
    
    # 3. Direction 3 Frame
    frame_d3 = base_frame.copy()
    draw_subtitle_direction_3(frame_d3, "Willow is suspended inside a dilution refrigerator.", active_word_idx=4, cy=1450)
    d = ImageDraw.Draw(frame_d3)
    d.text((54, 1340), "DIRECTION 3: FLOATING CONTEXTUAL CAPSULE", font=FONT_LABEL, fill=(52, 211, 153, 255))
    d3_path = SUBTITLES_DIR / "direction_3_contextual_capsule.png"
    frame_d3.save(d3_path)
    
    # Composite Comparison Image (1920x1080 horizontal layout showing 3 cropped lower-thirds)
    comp_w, comp_h = 1920, 1080
    composite = Image.new("RGBA", (comp_w, comp_h), (10, 14, 24, 255))
    crop_box = (0, 1150, 1080, 1650) # Crop lower third
    
    c1 = frame_d1.crop(crop_box).resize((620, 287), Image.Resampling.LANCZOS)
    c2 = frame_d2.crop(crop_box).resize((620, 287), Image.Resampling.LANCZOS)
    c3 = frame_d3.crop(crop_box).resize((620, 287), Image.Resampling.LANCZOS)
    
    cdraw = ImageDraw.Draw(composite)
    cdraw.text((60, 40), "SUPER.INTELLIGENCEEE // PHASE 9 SUBTITLE ARCHITECTURE EVALUATION", font=FONT_LABEL, fill=(212, 175, 55, 255))
    cdraw.text((60, 75), "Three Distinct Kinetic Typography Directions (Safe Zone Compliant MarginV >= 440px)", font=FONT_TITLE, fill=(255, 255, 255, 255))
    
    # Panel 1
    composite.paste(c1, (60, 160))
    cdraw.rectangle([60, 160, 680, 447], outline=(252, 211, 77, 200), width=2)
    cdraw.text((60, 460), "DIRECTION 1: KINETIC WORD-HIGHLIGHT EDITORIAL", font=FONT_LABEL, fill=(252, 211, 77, 255))
    cdraw.text((60, 495), "- High-contrast pill capsule with golden active word bounce", font=FONT_SUBTITLE, fill=(180, 190, 205, 255))
    cdraw.text((60, 530), "- Maximizes mobile engagement; eliminates dead reading pauses", font=FONT_SUBTITLE, fill=(180, 190, 205, 255))
    
    # Panel 2
    composite.paste(c2, (60, 580))
    cdraw.rectangle([60, 580, 680, 867], outline=(56, 189, 248, 200), width=2)
    cdraw.text((60, 880), "DIRECTION 2: CLEAN PHRASE-GROUP DYNAMIC LOWER-THIRD", font=FONT_LABEL, fill=(56, 189, 248, 255))
    cdraw.text((60, 915), "- Zero background box; dual-pass shadow with electric cyan tag", font=FONT_SUBTITLE, fill=(180, 190, 205, 255))
    cdraw.text((60, 950), "- Clean BBC / Vox documentary authority; unobstructed visuals", font=FONT_SUBTITLE, fill=(180, 190, 205, 255))
    
    # Panel 3
    composite.paste(c3, (740, 160))
    cdraw.rectangle([740, 160, 1360, 447], outline=(52, 211, 153, 200), width=2)
    cdraw.text((740, 460), "DIRECTION 3: FLOATING CONTEXTUAL CAPSULE", font=FONT_LABEL, fill=(52, 211, 153, 255))
    cdraw.text((740, 495), "- Glassmorphic backdrop with mint tabular monospace typography", font=FONT_SUBTITLE, fill=(180, 190, 205, 255))
    cdraw.text((740, 530), "- Modernist Apple / AR aesthetic; moves dynamically around UI", font=FONT_SUBTITLE, fill=(180, 190, 205, 255))
    
    # Right Column: User Reference Image Comparison Thumbnail
    if USER_REFERENCE_IMG.exists():
        ref_im = Image.open(USER_REFERENCE_IMG).resize((480, 252), Image.Resampling.LANCZOS)
        composite.paste(ref_im, (1380, 160))
        cdraw.rectangle([1380, 160, 1860, 412], outline=(212, 175, 55, 200), width=2)
        cdraw.text((1380, 430), "USER REFERENCE TARGET (media_...0f3853b5.jpg)", font=FONT_LABEL, fill=(212, 175, 55, 255))
        cdraw.text((1380, 465), "Cryostat chandelier physical benchmark", font=FONT_SUBTITLE, fill=(180, 190, 205, 255))

    comp_path = SUBTITLES_DIR / "subtitle_directions_comparison.png"
    composite.save(comp_path)
    print(f"[SUBTITLES] Saved comparison composite to: {comp_path}")
    return comp_path


# ==============================================================================
# AUDIO & SOUND DESIGN SYNTHESIS
# ==============================================================================

def generate_prototype_audio(proto_id: str, narration_text: str, duration: float, sfx_type: str) -> Path:
    """Generates Kokoro-82M speech + procedural sound design stems + mastered audio."""
    audio_dir = PROTOTYPES_DIR / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    speech_wav = audio_dir / f"{proto_id}_speech.wav"
    sfx_wav = audio_dir / f"{proto_id}_sfx.wav"
    master_wav = audio_dir / f"{proto_id}_master.wav"
    
    print(f"\n[AUDIO] Preparing speech for {proto_id}...")
    if speech_wav.exists() and speech_wav.stat().st_size > 10000:
        print(f"  Reusing existing synthesized speech: {speech_wav.name}")
        import wave
        with wave.open(str(speech_wav), "rb") as wf:
            actual_speech_dur = wf.getnframes() / float(wf.getframerate())
    else:
        runner = KokoroDirectRunner(workspace_root=WORKSPACE_ROOT)
        ok, meta = runner.generate(narration_text, speech_wav, voice_id="am_liam", speed=1.0)
        if not ok:
            raise RuntimeError(f"Speech synthesis failed for {proto_id}")
        actual_speech_dur = meta.get("duration", duration)
        
    target_dur = max(actual_speech_dur + 0.5, duration)
    
    # Synthesize procedural ambient drone + SFX via lavfi (No commas to prevent FFmpeg filtergraph splitting)
    if sfx_type == "cryostat":
        # Deep cryogenic hum (65Hz + 110Hz + mist hiss)
        expr = "0.07*sin(2*PI*65*t)+0.04*sin(2*PI*110*t)+0.02*sin(2*PI*195*t)+0.015*random(0)"
    elif sfx_type == "quantum_stabilizer":
        # Quantum hum + pulsating stabilizer frequency
        expr = "0.05*sin(2*PI*120*t)+0.03*sin(2*PI*240*t)+0.025*sin(2*PI*440*t)*sin(PI*t/8.5)+0.02*sin(2*PI*880*t)*sin(2*PI*t/8.5)"
    else: # documentary
        # Warm harmonic chords + acoustic drone
        expr = "0.05*sin(2*PI*130.81*t)+0.04*sin(2*PI*164.81*t)+0.03*sin(2*PI*196.00*t)+0.02*sin(2*PI*261.63*t)"
        
    sfx_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"aevalsrc={expr}:s=48000:d={target_dur:.2f}",
        "-af", "lowpass=f=2500,volume=0.6",
        str(sfx_wav)
    ]
    subprocess.run(sfx_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Master audio: voice + ducked sfx + EBU R128 (-16 LUFS)
    filter_complex = (
        "[1:a]volume=0.35[bg];"
        "[bg][0:a]sidechaincompress=threshold=0.08:ratio=4:attack=20:release=250[ducked_bg];"
        "[0:a]highpass=f=80,equalizer=f=3000:t=q:w=1.5:g=2.0[voice];"
        "[voice][ducked_bg]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
        "[mixed]loudnorm=I=-16:TP=-1.0:LRA=6[out]"
    )
    master_cmd = [
        "ffmpeg", "-y",
        "-i", str(speech_wav),
        "-i", str(sfx_wav),
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-ar", "48000",
        "-c:a", "pcm_s16le",
        str(master_wav)
    ]
    subprocess.run(master_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[AUDIO] Mastered audio produced at: {master_wav}")
    return master_wav


# ==============================================================================
# VIDEO RENDERING & COMPOSITING
# ==============================================================================

def render_prototype_video(comp, audio_wav: Path, output_mp4: Path, fps: float = 30.0) -> None:
    """Renders composition frames directly into FFmpeg stdin with deadlock-free pipe."""
    print(f"\n[RENDER] Rendering {output_mp4.name} (Duration: {comp.duration:.1f}s @ {fps}fps)...")
    total_frames = int(comp.duration * fps)
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{comp.width}x{comp.height}",
        "-pix_fmt", "rgba",
        "-r", str(fps),
        "-i", "-",
        "-i", str(audio_wav),
        "-c:v", "libx264",
        "-profile:v", "high",
        "-level", "4.2",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_mp4)
    ]
    
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        bufsize=10**7
    )
    
    t_start = time.time()
    try:
        for idx in range(total_frames):
            t = idx / fps
            frame = comp.render_frame(t)
            proc.stdin.write(frame.tobytes())
            if idx % 60 == 0:
                print(f"  Frame {idx}/{total_frames} ({idx/total_frames*100:.1f}%) | {(idx+1)/(time.time()-t_start):.1f} fps")
        proc.stdin.close()
        proc.wait()
    except Exception as e:
        proc.kill()
        raise RuntimeError(f"Rendering failed: {e}")
        
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg returned code {proc.returncode}")
        
    dur = time.time() - t_start
    print(f"[RENDER] Completed {output_mp4.name} in {dur:.1f}s ({total_frames/dur:.1f} fps)")


def extract_contact_sheet(video_mp4: Path, output_sheet: Path, rows: int = 2, cols: int = 3) -> None:
    """Extracts a grid contact sheet from rendered video."""
    num_frames = rows * cols
    temp_pattern = FRAMES_DIR / f"{video_mp4.stem}_f%02d.png"
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_mp4),
        "-vf", f"select=not(mod(n\\,{30*int(9/num_frames)})),scale=360:640",
        "-vframes", str(num_frames),
        str(temp_pattern)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    frame_files = sorted(FRAMES_DIR.glob(f"{video_mp4.stem}_f*.png"))[:num_frames]
    if not frame_files:
        return
        
    fw, fh = Image.open(frame_files[0]).size
    sheet = Image.new("RGBA", (fw * cols + (cols + 1) * 20, fh * rows + (rows + 1) * 20 + 80), (10, 14, 24, 255))
    sdraw = ImageDraw.Draw(sheet)
    sdraw.text((24, 20), f"CONTACT SHEET: {video_mp4.name.upper()}", font=FONT_LABEL, fill=(212, 175, 55, 255))
    
    for idx, ff in enumerate(frame_files):
        r = idx // cols
        c = idx % cols
        x = 20 + c * (fw + 20)
        y = 80 + r * (fh + 20)
        im = Image.open(ff)
        sheet.paste(im, (x, y))
        sdraw.rectangle([x, y, x + fw, y + fh], outline=(60, 75, 100, 255), width=2)
        sdraw.text((x + 10, y + 10), f"FRAME {idx+1}", font=FONT_MONO_SM, fill=(255, 255, 255, 220))
        
    sheet.save(output_sheet)
    print(f"[CONTACT SHEET] Saved to: {output_sheet}")


# ==============================================================================
# MAIN ORCHESTRATION PIPELINE
# ==============================================================================

def main():
    guard = ResourceGuard()
    guard.configure_environment()
    
    print("================================================================================")
    print("PHASE 9: VISUAL RESEARCH & PROOF-OF-CONCEPT PROTOTYPE PRODUCTION")
    print("================================================================================")
    
    # Step 1: Subtitle Directions Comparison Frame
    render_subtitle_directions_comparison()
    
    # Step 2: Prototype A (Physical Technology - Dilution Refrigerator)
    print("\n--------------------------------------------------------------------------------")
    print("[1/3] PROTOTYPE A: PHYSICAL TECHNOLOGY (DILUTION REFRIGERATOR)")
    print("--------------------------------------------------------------------------------")
    proto_a = PrototypeAPhysicalTechnology(duration=9.0)
    mp4_a = PROTOTYPES_DIR / "prototype_a_physical_technology.mp4"
    sheet_a = PROTOTYPES_DIR / "prototype_a_contact_sheet.png"
    if mp4_a.exists() and mp4_a.stat().st_size > 500000 and sheet_a.exists():
        print(f"  Prototype A already successfully rendered: {mp4_a.name}")
    else:
        audio_a = generate_prototype_audio(
            "proto_a",
            "To protect fragile qubits from room-temperature noise, Willow is suspended inside a multi-stage dilution refrigerator, cooling superconducting circuits down to ten millikelvin.",
            duration=9.0,
            sfx_type="cryostat"
        )
        render_prototype_video(proto_a, audio_a, mp4_a, fps=30.0)
        extract_contact_sheet(mp4_a, sheet_a)
    
    # Step 3: Prototype B (Abstract Concept - Quantum Surface Code)
    print("\n--------------------------------------------------------------------------------")
    print("[2/3] PROTOTYPE B: ABSTRACT TECHNICAL CONCEPT (SURFACE CODE LATTICE)")
    print("--------------------------------------------------------------------------------")
    proto_b = PrototypeBAbstractConcept(duration=8.5)
    audio_b = generate_prototype_audio(
        "proto_b",
        "When thermal decoherence flips a physical data qubit, real-time topological syndrome checks instantly pinpoint the disturbance, firing correction lasers before information leaks.",
        duration=8.5,
        sfx_type="quantum_stabilizer"
    )
    mp4_b = PROTOTYPES_DIR / "prototype_b_abstract_concept.mp4"
    render_prototype_video(proto_b, audio_b, mp4_b, fps=30.0)
    sheet_b = PROTOTYPES_DIR / "prototype_b_contact_sheet.png"
    extract_contact_sheet(mp4_b, sheet_b)
    
    # Step 4: Prototype C (Documentary Reality - Nature Paper & Supercomputer)
    print("\n--------------------------------------------------------------------------------")
    print("[3/3] PROTOTYPE C: REAL-WORLD DOCUMENTARY (NATURE MILESTONE & SCALE)")
    print("--------------------------------------------------------------------------------")
    proto_c = PrototypeCDocumentaryReality(duration=9.5)
    audio_c = generate_prototype_audio(
        "proto_c",
        "Published in Nature, Willow crossed the historic threshold: scaling physical qubits now exponentially suppresses error rates, finishing in five minutes what takes septillions of years.",
        duration=9.5,
        sfx_type="documentary"
    )
    mp4_c = PROTOTYPES_DIR / "prototype_c_documentary_reality.mp4"
    render_prototype_video(proto_c, audio_c, mp4_c, fps=30.0)
    sheet_c = PROTOTYPES_DIR / "prototype_c_contact_sheet.png"
    extract_contact_sheet(mp4_c, sheet_c)
    
    # Step 5: Master 3-Prototype Side-by-Side Sheet
    print("\n[MASTER SHEET] Assembling Master 3-Prototype Comparison Sheet...")
    master_w, master_h = 1920, 1080
    master_sheet = Image.new("RGBA", (master_w, master_h), (8, 12, 20, 255))
    mdraw = ImageDraw.Draw(master_sheet)
    mdraw.text((60, 30), "SUPER.INTELLIGENCEEE // PHASE 9 MASTER VISUAL PROTOTYPES", font=FONT_LABEL, fill=(212, 175, 55, 255))
    mdraw.text((60, 65), "Three Proof-of-Concept Productions Demonstrating High-Fidelity Technical Storytelling", font=FONT_TITLE, fill=(255, 255, 255, 255))
    
    # Paste sample frames from A, B, C side-by-side
    fa = proto_a.render_frame(t=4.5).resize((560, 995), Image.Resampling.LANCZOS)
    fb = proto_b.render_frame(t=3.8).resize((560, 995), Image.Resampling.LANCZOS)
    fc = proto_c.render_frame(t=4.0).resize((560, 995), Image.Resampling.LANCZOS)
    
    # Crop to 560x860 each
    crop_h = 860
    fa_c = fa.crop((0, 60, 560, 60 + crop_h))
    fb_c = fb.crop((0, 60, 560, 60 + crop_h))
    fc_c = fc.crop((0, 60, 560, 60 + crop_h))
    
    master_sheet.paste(fa_c, (60, 140))
    mdraw.rectangle([60, 140, 620, 140 + crop_h], outline=(212, 175, 55, 220), width=3)
    mdraw.text((75, 155), "PROTOTYPE A: PHYSICAL TECH", font=FONT_LABEL, fill=(212, 175, 55, 255))
    
    master_sheet.paste(fb_c, (680, 140))
    mdraw.rectangle([680, 140, 1240, 140 + crop_h], outline=(56, 189, 248, 220), width=3)
    mdraw.text((695, 155), "PROTOTYPE B: ABSTRACT CONCEPT", font=FONT_LABEL, fill=(56, 189, 248, 255))
    
    master_sheet.paste(fc_c, (1300, 140))
    mdraw.rectangle([1300, 140, 1860, 140 + crop_h], outline=(52, 211, 153, 220), width=3)
    mdraw.text((1315, 155), "PROTOTYPE C: DOCUMENTARY REALITY", font=FONT_LABEL, fill=(52, 211, 153, 255))
    
    master_sheet_path = PROTOTYPES_DIR / "phase9_master_prototypes_contact_sheet.png"
    master_sheet.save(master_sheet_path)
    print(f"[MASTER SHEET] Saved to: {master_sheet_path}")
    
    # Telemetry report
    print("\n================================================================================")
    print("PHASE 9 PROTOTYPES COMPLETED SUCCESSFULLY!")
    print(f"1. Subtitles: {SUBTITLES_DIR / 'subtitle_directions_comparison.png'}")
    print(f"2. Proto A:   {mp4_a}")
    print(f"3. Proto B:   {mp4_b}")
    print(f"4. Proto C:   {mp4_c}")
    print(f"5. Master:    {master_sheet_path}")
    print("================================================================================")

if __name__ == "__main__":
    main()
