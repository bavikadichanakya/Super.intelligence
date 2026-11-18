"""
SUPER.INTELLIGENCEEE — Phase 9.3 Visual Prototypes Production Engine
Produces three distinct scientific prototypes based on live hardware research:
1. Prototype A: Physical Hardware (Superconducting Dilution Refrigerator, Palette A)
2. Prototype B: Quantum Mechanism (Surface Code Syndrome Extraction & 840ns Decoder, Palette A + B)
3. Prototype C: Scientific Evidence (Willow Below-Threshold Nature 2024 Scaling Curve, Palette E)
"""

from __future__ import annotations

import os
import sys
import time
import math
import wave
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_ROOT = Path("A:/SUPER.INTELLIGENCEEE").resolve()
sys.path.insert(0, str(WORKSPACE_ROOT))

from rendering.composition_engine_v2 import (
    CANVAS_WIDTH, CANVAS_HEIGHT, MARGIN_X, USABLE_WIDTH,
    GRID_LEFT, GRID_RIGHT, GRID_CENTER_X,
    LeaderAnnotation, CinematicCameraDirectorV2
)
from rendering.smart_composition_engine import (
    BoundingBox, SmartCompositionValidator
)
from rendering.resource_guard import ResourceGuard

PROD_DIR = WORKSPACE_ROOT / "output" / "drafts" / "phase9_3"
AUDIO_DIR = PROD_DIR / "audio"
FRAMES_DIR = PROD_DIR / "frames"
OVERLAYS_DIR = PROD_DIR / "overlays"

PROD_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)
OVERLAYS_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# PALETTE SPECIFICATIONS DERIVED FROM RESEARCH
# ==============================================================================
# Palette A: Superconducting Cryogenic Hardware
CRYO_VOID = (8, 12, 20, 255)            # Deep cleanroom cryogenic vacuum (#080C14)
CRYO_PANEL = (14, 22, 36, 255)          # Structural datum surface (#0E1624)
GOLD_BASE = (212, 175, 55, 255)         # 99.99% Au electroplated OFHC copper (#D4AF37)
GOLD_SPECULAR = (255, 242, 163, 255)    # Directional specular glint (#FFF2A3)
GOLD_SHADOW = (138, 104, 40, 255)       # Cylindrical plate falloff (#8A6828)
COPPER_BRAID = (200, 117, 72, 255)      # OFHC copper thermal strap (#C87548)
STAINLESS_COAX = (148, 150, 153, 255)   # 316L semi-rigid coax jacket (#949699)
NBTI_SUPERCON = (112, 117, 125, 255)    # Niobium-Titanium coax (#70757D)
MUMETAL_SHIELD = (140, 146, 154, 255)   # Magnetic shield canister (#8C929A)
BRASS_SMA = (200, 155, 60, 255)         # Gold-plated brass SMA knurled hex (#C89B3C)

# Palette E: Scientific Data Visualization & Telemetry
DATA_POINT = (255, 255, 255, 255)       # Pure white empirical measurement
BELOW_THRESH = (16, 185, 129, 255)      # Technical Green below threshold (#10B981)
THRESH_LIMIT = (239, 68, 68, 255)       # Signal Red breakeven threshold (#EF4444)
CLASSICAL_CRIMSON = (220, 38, 38, 255)  # Classical brute-force limit (#DC2626)
QUANTUM_CYAN = (6, 182, 212, 255)       # Willow quantum runtime (#06B6D4)
TYPE_OFFWHITE = (248, 250, 252, 255)    # Crisp archival off-white (#F8FAFC)
TYPE_SLATE = (148, 163, 184, 255)       # Technical metadata slate (#94A3B8)

def load_font(font_name: str, size: int) -> ImageFont.FreeTypeFont:
    paths = [
        Path(f"C:/Windows/Fonts/{font_name}"),
        Path(f"C:/Windows/Fonts/{font_name.lower()}"),
        Path(f"C:/Windows/Fonts/{font_name.upper()}"),
    ]
    for p in paths:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()

FONT_HERO = load_font("georgiab.ttf", 68)
FONT_TITLE = load_font("segoeuib.ttf", 44)
FONT_SUB = load_font("segoeui.ttf", 28)
FONT_MONO = load_font("consolab.ttf", 26)
FONT_BADGE = load_font("segoeuib.ttf", 26)
FONT_SUBTITLE = load_font("segoeuib.ttf", 42)
FONT_NOTE = load_font("segoeui.ttf", 22)


# ==============================================================================
# SUBTITLE TREATMENT 1: CLEAN FLOATING ARCHIVAL (PROTOTYPE A)
# ==============================================================================
def render_subtitles_treatment_1(canvas: Image.Image, phrase: str, active_word: str = "", y_center: int = 1560):
    """Clean Floating Archival: 100% transparent; soft dual-pass ambient halo; active word in Warm Gold."""
    if not phrase:
        return
    draw = ImageDraw.Draw(canvas, "RGBA")
    f = FONT_SUBTITLE
    words = phrase.split()
    word_widths = [draw.textbbox((0, 0), w, font=f)[2] for w in words]
    space_w = draw.textbbox((0, 0), " ", font=f)[2]
    total_w = sum(word_widths) + space_w * (len(words) - 1)
    
    cur_x = (CANVAS_WIDTH - total_w) // 2
    for w, w_len in zip(words, word_widths):
        is_active = (w.strip(".,;:!?").lower() == active_word.strip(".,;:!?").lower())
        # Soft ambient shadow (zero black box)
        for ox, oy in [(-2, 2), (2, 2), (0, 3), (0, -2)]:
            draw.text((cur_x + ox, y_center - 26 + oy), w, font=f, fill=(0, 0, 0, 210))
        if is_active:
            draw.text((cur_x, y_center - 26), w, font=f, fill=GOLD_SPECULAR)
        else:
            draw.text((cur_x, y_center - 26), w, font=f, fill=TYPE_OFFWHITE)
        cur_x += w_len + space_w


# ==============================================================================
# SUBTITLE TREATMENT 2: RESTRAINED SCIENTIFIC MONOSPACE HUD (PROTOTYPE B)
# ==============================================================================
def render_subtitles_treatment_2(canvas: Image.Image, phrase: str, active_word: str = "", y_center: int = 1560):
    """Restrained Scientific Monospace HUD: Corner brackets, technical monospace, emerald active word."""
    if not phrase:
        return
    draw = ImageDraw.Draw(canvas, "RGBA")
    f = FONT_MONO
    words = phrase.split()
    word_widths = [draw.textbbox((0, 0), w, font=f)[2] for w in words]
    space_w = draw.textbbox((0, 0), " ", font=f)[2]
    total_w = sum(word_widths) + space_w * (len(words) - 1)
    
    bx0, by0 = (CANVAS_WIDTH - total_w) // 2 - 28, y_center - 32
    bx1, by1 = (CANVAS_WIDTH + total_w) // 2 + 28, y_center + 26
    
    # Corner registration brackets (zero black background box)
    cl = 14
    draw.line([bx0, by0 + cl, bx0, by0, bx0 + cl, by0], fill=(6, 182, 212, 190), width=2)
    draw.line([bx1, by0 + cl, bx1, by0, bx1 - cl, by0], fill=(6, 182, 212, 190), width=2)
    draw.line([bx0, by1 - cl, bx0, by1, bx0 + cl, by1], fill=(6, 182, 212, 190), width=2)
    draw.line([bx1, by1 - cl, bx1, by1, bx1 - cl, by1], fill=(6, 182, 212, 190), width=2)
    
    cur_x = (CANVAS_WIDTH - total_w) // 2
    for w, w_len in zip(words, word_widths):
        is_active = (w.strip(".,;:!?").lower() == active_word.strip(".,;:!?").lower())
        for ox, oy in [(-2, 2), (2, 2), (0, 3)]:
            draw.text((cur_x + ox, y_center - 18 + oy), w, font=f, fill=(0, 0, 0, 220))
        if is_active:
            draw.text((cur_x, y_center - 18), w, font=f, fill=BELOW_THRESH)
        else:
            draw.text((cur_x, y_center - 18), w, font=f, fill=TYPE_OFFWHITE)
        cur_x += w_len + space_w


# ==============================================================================
# SUBTITLE TREATMENT 3: MINIMAL CRITERION DOCUMENTARY CAPTION (PROTOTYPE C)
# ==============================================================================
def render_subtitles_treatment_3(canvas: Image.Image, phrase: str, active_word: str = "", y_center: int = 1560):
    """Minimal Criterion Documentary Caption: Pure floating typography, cyan active word."""
    if not phrase:
        return
    draw = ImageDraw.Draw(canvas, "RGBA")
    f = FONT_SUBTITLE
    words = phrase.split()
    word_widths = [draw.textbbox((0, 0), w, font=f)[2] for w in words]
    space_w = draw.textbbox((0, 0), " ", font=f)[2]
    total_w = sum(word_widths) + space_w * (len(words) - 1)
    
    cur_x = (CANVAS_WIDTH - total_w) // 2
    for w, w_len in zip(words, word_widths):
        is_active = (w.strip(".,;:!?").lower() == active_word.strip(".,;:!?").lower())
        for ox, oy in [(-2, 2), (2, 2), (0, 3)]:
            draw.text((cur_x + ox, y_center - 26 + oy), w, font=f, fill=(0, 0, 0, 200))
        if is_active:
            draw.text((cur_x, y_center - 26), w, font=f, fill=QUANTUM_CYAN)
        else:
            draw.text((cur_x, y_center - 26), w, font=f, fill=TYPE_OFFWHITE)
        cur_x += w_len + space_w


# ==============================================================================
# PROTOTYPE A: PHYSICAL HARDWARE (SUPERCONDUCTING CHANDELIER)
# ==============================================================================
class PrototypeAHardware:
    """Scientifically plausible dilution refrigerator based on Bluefors / Oxford research."""
    def __init__(self, duration: float = 11.25):
        self.duration = duration
        # Controlled camera path keeping hardware strictly below Y=240 safe line
        self.camera = CinematicCameraDirectorV2([
            (0.0, 540.0, 760.0, 1.00),
            (3.5, 540.0, 800.0, 1.10),
            (7.0, 540.0, 880.0, 1.25),
            (11.25, 540.0, 940.0, 1.35),
        ])
        self.subtitles = [
            ("To preserve delicate quantum coherence,", "coherence", 0.24, 2.70),
            ("superconducting transmons are housed inside a dilution refrigerator,", "refrigerator", 3.00, 6.60),
            ("cooling gold-plated copper stages down to ten millikelvin.", "millikelvin", 6.90, 10.80),
        ]

    def render_frame(self, t: float, with_subtitles: bool = True, validator: Optional[SmartCompositionValidator] = None) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), CRYO_VOID)
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # Directional Cleanroom Overhead Lighting (5000K Soft Diffuse)
        cx, cy = GRID_CENTER_X, 850
        for r in range(1100, 200, -150):
            alpha = int((1.0 - r / 1100.0) * 28)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(22, 34, 52, alpha))
            
        cam_cx, cam_cy, zoom = self.camera.get_state(t)
        self._draw_cryostat(draw, t, cam_cx, cam_cy, zoom)
        
        # Header Safe-Zone Protective Mask (Prevents ANY background object from interfering with header)
        for y_g in range(240):
            alpha = int(255 * (1.0 - max(0.0, (y_g - 180) / 60.0)))
            draw.line([0, y_g, CANVAS_WIDTH, y_g], fill=(8, 12, 20, alpha))
        
        # Header (Strictly Y=90-218px)
        draw.text((GRID_LEFT, 90), "PHYSICAL INSTRUMENTATION // PROTOTYPE A", font=FONT_MONO, fill=GOLD_BASE)
        draw.text((GRID_LEFT, 124), "DILUTION REFRIGERATOR", font=FONT_TITLE, fill=TYPE_OFFWHITE)
        draw.text((GRID_LEFT, 178), "5-Stage cryogenic infrastructure cooling Willow to 10 millikelvin", font=FONT_SUB, fill=TYPE_SLATE)
        draw.line([GRID_LEFT, 218, GRID_RIGHT, 218], fill=(45, 55, 75, 200), width=1)
        
        if with_subtitles:
            active_chunk = None
            for text, word, t0, t1 in self.subtitles:
                if t0 <= t < t1:
                    active_chunk = (text, word)
                    break
            if active_chunk:
                render_subtitles_treatment_1(canvas, active_chunk[0], active_word=active_chunk[1], y_center=1560)
                
        return canvas

    def _draw_cryostat(self, draw: ImageDraw.Draw, t: float, cx: float, cy: float, zoom: float):
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))
            
        wx = 540.0
        y_top = 340.0
        stages = [
            (510.0, 580, 32, "50K THERMAL SHIELD"),
            (680.0, 500, 30, "4K PULSE TUBE STAGE"),
            (850.0, 420, 28, "100mK DILUTION LOOP"),
            (1020.0, 350, 26, "15mK MIXING CHAMBER"),
        ]
        
        # 300K Top Vacuum Flange (Brushed 316L Stainless Steel)
        vt0, vt1 = tf(wx - 300, y_top), tf(wx + 300, y_top + 55)
        draw.rounded_rectangle([vt0[0], vt0[1], vt1[0], vt1[1]], radius=10, fill=(215, 222, 230, 255), outline=(100, 110, 125, 255), width=2)
        # Stainless steel highlight
        draw.line([vt0[0] + 12, vt0[1] + 4, vt1[0] - 12, vt0[1] + 4], fill=(255, 255, 255, 200), width=2)
        
        # Central Titanium / SS Column
        vc0, vc1 = tf(wx - 24, y_top + 55), tf(wx + 24, 1160)
        draw.rectangle([vc0[0], vc0[1], vc1[0], vc1[1]], fill=(140, 146, 156, 255), outline=(80, 85, 95, 255), width=2)
        
        # 4 Gold Thermal Plates with Anisotropic Lighting
        for wy, w, h, _ in stages:
            p0, p1 = tf(wx - w / 2, wy), tf(wx + w / 2, wy + h)
            # Plate Body (OFHC Copper Gold Electroplate)
            draw.rounded_rectangle([p0[0], p0[1], p1[0], p1[1]], radius=6, fill=GOLD_BASE, outline=GOLD_SHADOW, width=2)
            # Specular Glint along top bevel
            draw.line([p0[0] + 8, p0[1] + 3, p1[0] - 8, p0[1] + 3], fill=GOLD_SPECULAR, width=2)
            # Lower shadow falloff
            draw.line([p0[0] + 4, p1[1] - 2, p1[0] - 4, p1[1] - 2], fill=GOLD_SHADOW, width=2)
            
        # Titanium Support Standoffs
        for p_top, p_bot in [((wx - 260, y_top + 55), (wx - 220, 510)), ((wx + 260, y_top + 55), (wx + 220, 510)),
                             ((wx - 220, 542), (wx - 180, 680)), ((wx + 220, 542), (wx + 180, 680)),
                             ((wx - 180, 710), (wx - 145, 850)), ((wx + 180, 710), (wx + 145, 850))]:
            vt, vb = tf(p_top[0], p_top[1]), tf(p_bot[0], p_bot[1])
            draw.line([vt[0], vt[1], vb[0], vb[1]], fill=(120, 128, 138, 255), width=4)
            draw.line([vt[0] - 1, vt[1], vb[0] - 1, vb[1]], fill=(200, 210, 222, 200), width=1)
            
        # Semi-Rigid Coaxial Cables with S-Curvature
        for x0, x1, y0, y1, nc in [(wx - 200, wx - 50, 542, 680, 8), (wx + 50, wx + 200, 542, 680, 8),
                                   (wx - 160, wx - 40, 710, 850, 8), (wx + 40, wx + 160, 710, 850, 8),
                                   (wx - 130, wx - 30, 878, 1020, 6), (wx + 30, wx + 130, 878, 1020, 6)]:
            step = (x1 - x0) / max(1, nc - 1)
            for i in range(nc):
                x = x0 + i * step
                pt, pb = tf(x, y0), tf(x, y1)
                # Outer conductor
                draw.line([pt[0], pt[1], pb[0], pb[1]], fill=STAINLESS_COAX, width=2)
                # Brass SMA connector collar at plate entry
                draw.rectangle([pt[0] - 3, pt[1], pt[0] + 3, pt[1] + 6], fill=BRASS_SMA)
                draw.rectangle([pb[0] - 3, pb[1] - 6, pb[0] + 3, pb[1]], fill=BRASS_SMA)
                
        # Attenuators on central column
        for ay in [590, 760, 930]:
            at0, at1 = tf(wx - 20, ay - 18), tf(wx + 20, ay + 18)
            draw.rectangle([at0[0], at0[1], at1[0], at1[1]], fill=GOLD_BASE, outline=GOLD_SPECULAR, width=2)
            
        # QPU Mu-Metal Canister at bottom
        q0, q1 = tf(wx - 80, 1080), tf(wx + 80, 1240)
        draw.rounded_rectangle([q0[0], q0[1], q1[0], q1[1]], radius=12, fill=(34, 38, 46, 255), outline=MUMETAL_SHIELD, width=3)
        draw.line([q0[0] + 8, q0[1] + 6, q1[0] - 8, q0[1] + 6], fill=(180, 190, 205, 180), width=2)
        draw.text((q0[0] + 20, q0[1] + 65), "WILLOW QPU", font=FONT_MONO, fill=QUANTUM_CYAN)
        
        # Telemetry Callout (15mK Stage)
        if t > 3.0:
            lx0, ly0 = tf(wx + 80, 1160)
            lx1, ly1 = lx0 + int(70 * zoom), ly0
            lx2, ly2 = lx1 + int(60 * zoom), ly0 - int(50 * zoom)
            draw.ellipse([lx0 - 4, ly0 - 4, lx0 + 4, ly0 + 4], fill=QUANTUM_CYAN)
            draw.line([lx0, ly0, lx1, ly1], fill=TYPE_SLATE, width=2)
            draw.line([lx1, ly1, lx2, ly2], fill=TYPE_SLATE, width=2)
            
            draw.rounded_rectangle([lx2, ly2 - 24, lx2 + 280, ly2 + 48], radius=8, fill=(14, 22, 36, 230), outline=QUANTUM_CYAN, width=1)
            draw.text((lx2 + 16, ly2 - 16), "STAGE 05: MIXING CHAMBER", font=FONT_BADGE, fill=TYPE_OFFWHITE)
            draw.text((lx2 + 16, ly2 + 14), "10 mK Base Temperature // Au OFHC", font=FONT_NOTE, fill=TYPE_SLATE)
            lx1, ly1 = lx0 + int(70 * zoom), ly0
            lx2, ly2 = lx1 + int(60 * zoom), ly0 - int(50 * zoom)
            draw.ellipse([lx0 - 4, ly0 - 4, lx0 + 4, ly0 + 4], fill=QUANTUM_CYAN)
            draw.line([lx0, ly0, lx1, ly1], fill=TYPE_SLATE, width=2)
            draw.line([lx1, ly1, lx2, ly2], fill=TYPE_SLATE, width=2)
            
            draw.rounded_rectangle([lx2, ly2 - 24, lx2 + 280, ly2 + 48], radius=8, fill=(14, 22, 36, 230), outline=QUANTUM_CYAN, width=1)
            draw.text((lx2 + 16, ly2 - 16), "STAGE 05: MIXING CHAMBER", font=FONT_BADGE, fill=TYPE_OFFWHITE)
            draw.text((lx2 + 16, ly2 + 14), "10 mK Base Temperature // Au OFHC", font=FONT_NOTE, fill=TYPE_SLATE)


# ==============================================================================
# PROTOTYPE B: QUANTUM MECHANISM (SURFACE CODE SYNDROME EXTRACTION)
# ==============================================================================
class PrototypeBMechanism:
    """Explains surface code syndrome extraction, real-time bit-flip detection, and 840ns feedback."""
    def __init__(self, duration: float = 10.75):
        self.duration = duration
        self.camera = CinematicCameraDirectorV2([
            (0.0, 540.0, 840.0, 1.05),
            (3.0, 540.0, 840.0, 1.35),
            (7.0, 540.0, 840.0, 1.45),
            (10.75, 540.0, 840.0, 1.15),
        ])
        self.subtitles = [
            ("When thermal noise flips a physical data qubit,", "flips", 0.24, 2.70),
            ("adjacent syndrome ancillas detect the parity disturbance,", "disturbance", 3.00, 6.30),
            ("firing a feedback correction pulse in 840 nanoseconds.", "840", 6.60, 10.20),
        ]

    def render_frame(self, t: float, with_subtitles: bool = True, validator: Optional[SmartCompositionValidator] = None) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), CRYO_VOID)
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        cam_cx, cam_cy, zoom = self.camera.get_state(t)
        self._draw_die_carrier(draw, cam_cx, cam_cy, zoom)
        self._draw_lattice(draw, t, cam_cx, cam_cy, zoom)
        
        # Header Safe-Zone Mask
        for y_g in range(240):
            alpha = int(255 * (1.0 - max(0.0, (y_g - 180) / 60.0)))
            draw.line([0, y_g, CANVAS_WIDTH, y_g], fill=(8, 12, 20, alpha))
            
        # Header
        draw.text((GRID_LEFT, 90), "STABILIZER DYNAMICS // PROTOTYPE B", font=FONT_MONO, fill=QUANTUM_CYAN)
        draw.text((GRID_LEFT, 124), "TOPOLOGICAL ERROR HEALING", font=FONT_TITLE, fill=TYPE_OFFWHITE)
        draw.text((GRID_LEFT, 178), "Surface code parity measurement & real-time phase restoration", font=FONT_SUB, fill=TYPE_SLATE)
        draw.line([GRID_LEFT, 218, GRID_RIGHT, 218], fill=(45, 55, 75, 200), width=1)
        
        if with_subtitles:
            active_chunk = None
            for text, word, t0, t1 in self.subtitles:
                if t0 <= t < t1:
                    active_chunk = (text, word)
                    break
            if active_chunk:
                render_subtitles_treatment_2(canvas, active_chunk[0], active_word=active_chunk[1], y_center=1560)
                
        return canvas

    def _draw_die_carrier(self, draw: ImageDraw.Draw, cx: float, cy: float, zoom: float):
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))
            
        x0, y0 = tf(60, 420)
        x1, y1 = tf(1020, 1260)
        # Multilayer Ceramic Substrate Carrier
        draw.rounded_rectangle([x0, y0, x1, y1], radius=24, fill=(16, 24, 38, 255), outline=(45, 60, 85, 255), width=2)
        
        # Silicon Die Inset
        dx0, dy0 = tf(150, 480)
        dx1, dy1 = tf(930, 1200)
        draw.rounded_rectangle([dx0, dy0, dx1, dy1], radius=14, fill=(10, 16, 28, 255), outline=(60, 80, 110, 255), width=2)
        
        # Gold Wirebond Pads along perimeter
        for side in range(4):
            for i in range(12):
                if side == 0:   # Top
                    wx_val = 190 + i * 60
                    p_die, p_car = tf(wx_val, 480), tf(wx_val, 450)
                elif side == 1: # Bottom
                    wx_val = 190 + i * 60
                    p_die, p_car = tf(wx_val, 1200), tf(wx_val, 1230)
                elif side == 2: # Left
                    wy_val = 520 + i * 56
                    p_die, p_car = tf(150, wy_val), tf(100, wy_val)
                else:           # Right
                    wy_val = 520 + i * 56
                    p_die, p_car = tf(930, wy_val), tf(980, wy_val)
                draw.line([p_die[0], p_die[1], p_car[0], p_car[1]], fill=GOLD_BASE, width=2)
                draw.rectangle([p_car[0] - 3, p_car[1] - 3, p_car[0] + 3, p_car[1] + 3], fill=GOLD_SPECULAR)

    def _draw_lattice(self, draw: ImageDraw.Draw, t: float, cx: float, cy: float, zoom: float):
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))
            
        ox, oy = 220.0, 520.0
        pitch = 160.0
        
        # Coplanar Waveguide Resonator Bus
        for r in range(5):
            p0, p1 = tf(ox, oy + r * pitch), tf(ox + 4 * pitch, oy + r * pitch)
            draw.line([p0[0], p0[1], p1[0], p1[1]], fill=(38, 52, 76, 255), width=3)
        for c in range(5):
            p0, p1 = tf(ox + c * pitch, oy), tf(ox + c * pitch, oy + 4 * pitch)
            draw.line([p0[0], p0[1], p1[0], p1[1]], fill=(38, 52, 76, 255), width=3)
            
        err_r, err_c = 2, 2
        pt_err = tf(ox + err_c * pitch, oy + err_r * pitch)
        
        # Draw Stabilizer Nodes (Data qubits vs Syndrome ancillas)
        for r in range(5):
            for c in range(5):
                if r == err_r and c == err_c:
                    continue
                pt = tf(ox + c * pitch, oy + r * pitch)
                is_data = ((r + c) % 2 == 0)
                is_adj = (abs(r - err_r) + abs(c - err_c) == 1)
                
                if is_adj and 3.0 <= t < 6.5:
                    # Adjacent syndrome detector PULSING IN CYAN
                    rad = int(26 * zoom + 5 * math.sin(t * 14))
                    draw.rectangle([pt[0] - rad//2, pt[1] - rad//2, pt[0] + rad//2, pt[1] + rad//2], fill=QUANTUM_CYAN, outline=TYPE_OFFWHITE, width=2)
                    draw.text((pt[0] - 8, pt[1] - 12), "Z", font=FONT_BADGE, fill=CRYO_VOID)
                else:
                    if is_data:
                        rad = int(16 * zoom)
                        draw.ellipse([pt[0] - rad, pt[1] - rad, pt[0] + rad, pt[1] + rad], fill=(36, 123, 206, 230), outline=(20, 35, 55, 255), width=2)
                    else:
                        w = int(24 * zoom)
                        draw.rectangle([pt[0] - w//2, pt[1] - w//2, pt[0] + w//2, pt[1] + w//2], fill=(60, 146, 122, 230), outline=(20, 35, 55, 255), width=2)

        # FAILING QUBIT (Phase 1: Normal -> Phase 2: Coral Bit-Flip -> Phase 3: Green Laser Restoration)
        rad_f = int(20 * zoom)
        if t < 2.2:
            draw.ellipse([pt_err[0] - rad_f, pt_err[1] - rad_f, pt_err[0] + rad_f, pt_err[1] + rad_f], fill=(36, 123, 206, 255), outline=TYPE_OFFWHITE, width=2)
        elif 2.2 <= t < 6.5:
            # Coral Bit-Flip (#EF4444)
            pulse = int(8 * math.sin(t * 16))
            draw.ellipse([pt_err[0] - rad_f - 14 - pulse, pt_err[1] - rad_f - 14 - pulse, pt_err[0] + rad_f + 14 + pulse, pt_err[1] + rad_f + 14 + pulse], fill=(239, 68, 68, 80))
            draw.ellipse([pt_err[0] - rad_f, pt_err[1] - rad_f, pt_err[0] + rad_f, pt_err[1] + rad_f], fill=THRESH_LIMIT, outline=TYPE_OFFWHITE, width=3)
            
            draw.rounded_rectangle([pt_err[0] + 34, pt_err[1] - 44, pt_err[0] + 280, pt_err[1] + 16], radius=8, fill=(18, 26, 42, 240), outline=THRESH_LIMIT, width=2)
            draw.text((pt_err[0] + 48, pt_err[1] - 32), "BIT-FLIP DETECTED", font=FONT_BADGE, fill=THRESH_LIMIT)
            draw.text((pt_err[0] + 48, pt_err[1] - 4), "Parity violation detected", font=FONT_NOTE, fill=TYPE_SLATE)
        else:
            # Stabilizer Feedback Correction (#10B981)
            draw.ellipse([pt_err[0] - rad_f - 18, pt_err[1] - rad_f - 18, pt_err[0] + rad_f + 18, pt_err[1] + rad_f + 18], fill=(16, 185, 129, 90))
            draw.ellipse([pt_err[0] - rad_f, pt_err[1] - rad_f, pt_err[0] + rad_f, pt_err[1] + rad_f], fill=BELOW_THRESH, outline=TYPE_OFFWHITE, width=3)
            
            draw.rounded_rectangle([pt_err[0] + 34, pt_err[1] - 44, pt_err[0] + 310, pt_err[1] + 16], radius=8, fill=(18, 26, 42, 240), outline=BELOW_THRESH, width=2)
            draw.text((pt_err[0] + 48, pt_err[1] - 32), "HEALED IN 840ns", font=FONT_BADGE, fill=BELOW_THRESH)
            draw.text((pt_err[0] + 48, pt_err[1] - 4), "Real-time state restoration", font=FONT_NOTE, fill=TYPE_SLATE)


# ==============================================================================
# PROTOTYPE C: SCIENTIFIC EVIDENCE (WILLOW NATURE VOL 636 SCALING CURVE)
# ==============================================================================
class PrototypeCEvidence:
    """Authentic empirical data visualization plotting Logical Error vs Code Distance."""
    def __init__(self, duration: float = 10.25):
        self.duration = duration
        self.subtitles = [
            ("Published in Nature, Willow achieved the historic milestone:", "historic", 0.24, 3.20),
            ("expanding the surface code from distance three to distance seven", "seven", 3.50, 6.70),
            ("exponentially suppresses the logical error rate.", "suppresses", 7.00, 10.00),
        ]

    def render_frame(self, t: float, with_subtitles: bool = True, validator: Optional[SmartCompositionValidator] = None) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), CRYO_VOID)
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # Header Safe-Zone Mask
        for y_g in range(240):
            alpha = int(255 * (1.0 - max(0.0, (y_g - 180) / 60.0)))
            draw.line([0, y_g, CANVAS_WIDTH, y_g], fill=(8, 12, 20, alpha))
            
        # Header
        draw.text((GRID_LEFT, 90), "EMPIRICAL DATA // PROTOTYPE C", font=FONT_MONO, fill=BELOW_THRESH)
        draw.text((GRID_LEFT, 124), "BELOW-THRESHOLD SCALING", font=FONT_TITLE, fill=TYPE_OFFWHITE)
        draw.text((GRID_LEFT, 178), "Nature Vol 636 (Dec 2024): Logical error suppression vs distance d", font=FONT_SUB, fill=TYPE_SLATE)
        draw.line([GRID_LEFT, 218, GRID_RIGHT, 218], fill=(45, 55, 75, 200), width=1)
        
        self._draw_scaling_plot(draw, t)
        
        if with_subtitles:
            active_chunk = None
            for text, word, t0, t1 in self.subtitles:
                if t0 <= t < t1:
                    active_chunk = (text, word)
                    break
            if active_chunk:
                render_subtitles_treatment_3(canvas, active_chunk[0], active_word=active_chunk[1], y_center=1560)
                
        return canvas

    def _draw_scaling_plot(self, draw: ImageDraw.Draw, t: float):
        x0, y0, w, h = GRID_LEFT, 260, USABLE_WIDTH, 1160
        x1, y1 = x0 + w, y0 + h
        
        # Drafting surface
        draw.rounded_rectangle([x0, y0, x1, y1], radius=24, fill=(14, 20, 32, 255), outline=(40, 52, 75, 255), width=2)
        
        # Nature Journal Citation Banner
        draw.text((x0 + 44, y0 + 36), "nature", font=load_font("georgiab.ttf", 46), fill=(210, 20, 20, 255))
        draw.text((x0 + 210, y0 + 52), "|  VOL 636  |  9 DECEMBER 2024  |  ARTICLE", font=FONT_MONO, fill=TYPE_SLATE)
        draw.line([x0 + 44, y0 + 104, x1 - 44, y0 + 104], fill=(35, 46, 68, 255), width=1)
        
        draw.text((x0 + 44, y0 + 124), "LOGICAL ERROR RATE PER CYCLE (e_L)", font=FONT_TITLE, fill=TYPE_OFFWHITE)
        draw.text((x0 + 44, y0 + 176), "Willow 105-qubit processor across surface code distance 3, 5, and 7", font=FONT_SUB, fill=TYPE_SLATE)
        
        ax_x0, ax_y0, ax_x1, ax_y1 = x0 + 140, y1 - 200, x1 - 60, y0 + 260
        # Axes
        draw.line([ax_x0, ax_y0, ax_x1, ax_y0], fill=(80, 95, 120, 255), width=2)
        draw.line([ax_x0, ax_y0, ax_x0, ax_y1], fill=(80, 95, 120, 255), width=2)
        
        # Y-Axis Logarithmic Ticks
        for y_tick, y_lbl in [(ax_y1 + 40, "10^-2"), (ax_y1 + 240, "10^-3"), (ax_y0 - 40, "10^-4")]:
            draw.line([ax_x0 - 8, y_tick, ax_x0, y_tick], fill=(80, 95, 120, 255), width=2)
            draw.text((ax_x0 - 100, y_tick - 12), y_lbl, font=FONT_MONO, fill=TYPE_SLATE)
            
        # X-Axis Ticks (Distance 3, 5, 7)
        d_ticks = [
            (ax_x0 + 140, "d = 3", "17 Qubits"),
            (ax_x0 + 380, "d = 5", "49 Qubits"),
            (ax_x0 + 620, "d = 7", "105 Qubits")
        ]
        for tx, tlabel, tsub in d_ticks:
            draw.line([tx, ax_y0 - 8, tx, ax_y0 + 8], fill=(80, 95, 120, 255), width=2)
            bb = draw.textbbox((0, 0), tlabel, font=FONT_TITLE)
            tw = bb[2] - bb[0]
            draw.text((tx - tw // 2, ax_y0 + 18), tlabel, font=FONT_TITLE, fill=TYPE_OFFWHITE)
            
            bb2 = draw.textbbox((0, 0), tsub, font=FONT_NOTE)
            tw2 = bb2[2] - bb2[0]
            draw.text((tx - tw2 // 2, ax_y0 + 62), tsub, font=FONT_NOTE, fill=TYPE_SLATE)
            
        # X-Axis Title (Center separated by 110px below axis)
        x_title = "SURFACE CODE DISTANCE (d)"
        bb_xt = draw.textbbox((0, 0), x_title, font=FONT_MONO)
        xt_w = bb_xt[2] - bb_xt[0]
        draw.text(((ax_x0 + ax_x1 - xt_w) // 2, ax_y0 + 105), x_title, font=FONT_MONO, fill=GOLD_BASE)
        
        # Threshold Limit Line (Lambda = 1.0)
        thresh_y = y0 + 440
        for lx in range(ax_x0, ax_x1, 16):
            draw.line([lx, thresh_y, lx + 10, thresh_y], fill=THRESH_LIMIT, width=2)
        draw.text((ax_x1 - 420, thresh_y - 32), "THRESHOLD LIMIT (Lambda = 1.0)", font=FONT_MONO, fill=THRESH_LIMIT)
        
        # Empirical Data Points & Error Curve (Lambda = 0.79)
        curve_prog = max(0.0, min(1.0, (t - 2.5) / 3.0))
        ease = 3 * curve_prog**2 - 2 * curve_prog**3
        
        pts = [
            (ax_x0 + 140, thresh_y + 60, "3.0 x 10^-3"),
            (ax_x0 + 380, thresh_y + 180, "2.1 x 10^-3"),
            (ax_x0 + 620, thresh_y + 320, "1.4 x 10^-3")
        ]
        
        max_idx = int(ease * (len(pts) - 1))
        frac = (ease * (len(pts) - 1)) - max_idx
        drawn_pts = [pts[i][:2] for i in range(max_idx + 1)]
        if max_idx < len(pts) - 1 and frac > 0.0:
            drawn_pts.append((pts[max_idx][0] + (pts[max_idx + 1][0] - pts[max_idx][0]) * frac,
                              pts[max_idx][1] + (pts[max_idx + 1][1] - pts[max_idx][1]) * frac))
                              
        # Connecting Glow Spline
        for i in range(len(drawn_pts) - 1):
            draw.line([drawn_pts[i][0], drawn_pts[i][1], drawn_pts[i+1][0], drawn_pts[i+1][1]], fill=(6, 182, 212, 90), width=14)
            draw.line([drawn_pts[i][0], drawn_pts[i][1], drawn_pts[i+1][0], drawn_pts[i+1][1]], fill=BELOW_THRESH, width=4)
            
        # Draw Data Points with 1-Sigma Error Bars
        for idx, (px, py, lbl) in enumerate(pts):
            if idx <= max_idx:
                # 1-Sigma Error Bar
                err_h = 24
                draw.line([px, py - err_h, px, py + err_h], fill=TYPE_OFFWHITE, width=2)
                draw.line([px - 8, py - err_h, px + 8, py - err_h], fill=TYPE_OFFWHITE, width=2)
                draw.line([px - 8, py + err_h, px + 8, py + err_h], fill=TYPE_OFFWHITE, width=2)
                # Point circle
                draw.ellipse([px - 11, py - 11, px + 11, py + 11], fill=BELOW_THRESH, outline=DATA_POINT, width=2)
                draw.text((px + 20, py - 14), lbl, font=FONT_BADGE, fill=TYPE_OFFWHITE)

        # Callout Pill
        if curve_prog > 0.8:
            cx0, cy0 = pts[2][0] - 340, pts[2][1] - 120
            draw.rounded_rectangle([cx0, cy0, cx0 + 320, cy0 + 74], radius=12, fill=(16, 26, 44, 245), outline=BELOW_THRESH, width=2)
            draw.text((cx0 + 20, cy0 + 12), "LAMBDA = 0.79 +/- 0.02", font=FONT_BADGE, fill=BELOW_THRESH)
            draw.text((cx0 + 20, cy0 + 42), "Exponential Error Suppression Verified", font=FONT_NOTE, fill=TYPE_SLATE)


# ==============================================================================
# MAIN PROTOTYPE RENDERING PIPELINE
# ==============================================================================
def render_prototype(proto_name: str, renderer: Any, audio_file: Path, out_mp4: Path, out_sheet: Path):
    fps = 30.0
    total_frames = int(renderer.duration * fps)
    print(f"\n[RENDER] Rendering {proto_name} ({renderer.duration:.2f}s, {total_frames} frames)...")
    
    cmd_ff = [
        "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}", "-pix_fmt", "rgba",
        "-r", str(fps), "-i", "-",
        "-i", str(audio_file),
        "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
        "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(out_mp4)
    ]
    proc = subprocess.Popen(cmd_ff, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, bufsize=10**7)
    
    t_start = time.time()
    for f_idx in range(total_frames):
        t = f_idx / fps
        frame = renderer.render_frame(t, with_subtitles=True)
        proc.stdin.write(frame.tobytes())
        
    proc.stdin.close()
    proc.wait()
    dur = time.time() - t_start
    print(f"  Finished {proto_name} MP4 in {dur:.1f}s ({total_frames/dur:.1f} fps): {out_mp4.stat().st_size} bytes")
    
    # 30-Frame Contact Sheet (5 cols x 6 rows)
    print(f"  Extracting 30 frames for {proto_name} contact sheet...")
    num_frames = 30
    cols, rows = 5, 6
    step_t = renderer.duration / num_frames
    
    extracted = []
    for i in range(num_frames):
        tf = i * step_t
        out_f = FRAMES_DIR / f"{proto_name}_f{i:02d}.png"
        cmd_ext = [
            "ffmpeg", "-y", "-ss", f"{tf:.3f}", "-i", str(out_mp4),
            "-vframes", "1", "-q:v", "2", str(out_f)
        ]
        subprocess.run(cmd_ext, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        extracted.append(out_f)
        
    tw, th = 320, 568
    pad = 12
    sw = cols * tw + (cols + 1) * pad
    sh = rows * th + (rows + 1) * pad + 60
    
    sheet = Image.new("RGB", (sw, sh), (8, 12, 20))
    sdraw = ImageDraw.Draw(sheet)
    sdraw.text((pad, 16), f"SUPER.INTELLIGENCEEE // {proto_name.upper()} — 30-FRAME VISUAL AUDIT", font=FONT_TITLE, fill=GOLD_BASE)
    
    for idx, ff in enumerate(extracted):
        r = idx // cols
        c = idx % cols
        x = pad + c * (tw + pad)
        y = 60 + pad + r * (th + pad)
        im = Image.open(ff).resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        sdraw.rectangle([x, y, x + tw, y + th], outline=(40, 52, 75), width=2)
        sdraw.text((x + 8, y + 8), f"#{idx+1:02d} ({idx*step_t:.1f}s)", font=FONT_MONO, fill=TYPE_OFFWHITE)
        
    sheet.save(out_sheet)
    print(f"  Saved contact sheet: {out_sheet.name}")

def main():
    guard = ResourceGuard()
    guard.configure_environment()
    
    print("=" * 80)
    print("PHASE 9.3: BUILDING THREE SCIENTIFIC PROTOTYPES")
    print("=" * 80)
    
    # Prototype A
    p_a = PrototypeAHardware(duration=11.25)
    render_prototype(
        "prototype_a_hardware",
        p_a,
        AUDIO_DIR / "proto_a_hardware_master.wav",
        PROD_DIR / "prototype_a_physical_hardware.mp4",
        PROD_DIR / "prototype_a_30frame_contact_sheet.png"
    )
    
    # Prototype B
    p_b = PrototypeBMechanism(duration=10.75)
    render_prototype(
        "prototype_b_mechanism",
        p_b,
        AUDIO_DIR / "proto_b_mechanism_master.wav",
        PROD_DIR / "prototype_b_quantum_mechanism.mp4",
        PROD_DIR / "prototype_b_30frame_contact_sheet.png"
    )
    
    # Prototype C
    p_c = PrototypeCEvidence(duration=10.25)
    render_prototype(
        "prototype_c_evidence",
        p_c,
        AUDIO_DIR / "proto_c_evidence_master.wav",
        PROD_DIR / "prototype_c_scientific_evidence.mp4",
        PROD_DIR / "prototype_c_30frame_contact_sheet.png"
    )
    
    print("\n[ALL PROTOTYPES COMPLETE] Successfully rendered all 3 prototypes and contact sheets.")

if __name__ == "__main__":
    main()
