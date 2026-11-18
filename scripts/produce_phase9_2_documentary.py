"""
SUPER.INTELLIGENCEEE — Phase 9.2 Complete Autonomous Documentary Production Engine
Flagship Masterpiece: "Google Willow: Real-Time Quantum Error Correction Below Threshold"
Duration: 55.0 seconds | Resolution: 1080x1920 @ 30fps
Features:
- 6 Continuous Storytelling Scenes with Dynamic Camera Choreography.
- Smart Composition & BoundingBox Alignment via SmartCompositionValidator.
- Collision-Free Elbow Leader Annotations.
- Both Clean Archival Master & Captioned Review Master.
- 40+ Frame Forensic Contact Sheet & Diagnostic Composition Overlays.
"""

from __future__ import annotations

import os
import sys
import time
import math
import wave
import json
import hashlib
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Tuple
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_ROOT = Path("A:/SUPER.INTELLIGENCEEE").resolve()
sys.path.insert(0, str(WORKSPACE_ROOT))

from rendering.composition_engine_v2 import (
    CANVAS_WIDTH, CANVAS_HEIGHT, MARGIN_X, USABLE_WIDTH,
    GRID_LEFT, GRID_RIGHT, GRID_CENTER_X,
    FONT_DISPLAY_HERO, FONT_DISPLAY_TITLE, FONT_DISPLAY_SUB,
    FONT_BADGE_TITLE, FONT_BADGE_METRIC, FONT_MONO_LABEL,
    LeaderAnnotation, CinematicCameraDirectorV2,
    render_subtitle_direction_a, render_subtitle_direction_b, render_subtitle_direction_c,
    draw_editorial_scene_header
)
from rendering.smart_composition_engine import (
    BoundingBox, SmartCompositionValidator, SmartAnnotationRouter
)
from rendering.resource_guard import ResourceGuard

PROD_DIR = WORKSPACE_ROOT / "output" / "productions" / "phase9_2_documentary"
AUDIO_DIR = PROD_DIR / "audio"
FRAMES_DIR = PROD_DIR / "frames"
OVERLAYS_DIR = PROD_DIR / "overlays"
SUBTITLES_DIR = PROD_DIR / "subtitles"
REPORTS_DIR = WORKSPACE_ROOT / "reports" / "phase9_2"

PROD_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)
OVERLAYS_DIR.mkdir(parents=True, exist_ok=True)
SUBTITLES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# SCENE 1: CRYOSTAT CHANDELIER (OBSIDIAN CRYOGENIC VOID)
# ==============================================================================
class Scene1CryostatChandelier:
    """Scene 1: 0.0s - 9.0s (The Cryogenic Fortress)."""
    def __init__(self, duration: float = 9.0):
        self.duration = duration
        self.camera = CinematicCameraDirectorV2([
            (0.0, 540.0, 780.0, 1.00),
            (2.2, 540.0, 720.0, 1.05),
            (3.4, 520.0, 600.0, 1.38),
            (5.0, 500.0, 720.0, 1.62),
            (6.8, 540.0, 940.0, 1.48),
            (8.2, 540.0, 1080.0, 1.80),
            (9.0, 540.0, 1100.0, 1.85),
        ])
        self.subtitles = [
            ("To protect fragile qubits", "qubits", 0.0, 2.5),
            ("from room-temperature noise,", "noise", 2.5, 5.0),
            ("Willow is suspended inside", "suspended", 5.0, 7.0),
            ("a multi-stage dilution refrigerator.", "refrigerator", 7.0, 9.0),
        ]

    def render_frame(self, t: float, with_subtitles: bool = True, validator: Optional[SmartCompositionValidator] = None) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (6, 4, 20, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # Radial lighting
        cx, cy = GRID_CENTER_X, 850
        for r in range(1100, 250, -140):
            alpha = int((1.0 - r / 1100.0) * 32)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(22, 12, 56, alpha))
            
        cam_cx, cam_cy, zoom = self.camera.get_state(t)
        
        # Render physical refrigerator
        self._draw_cryostat(draw, t, cam_cx, cam_cy, zoom, validator)
        
        # Annotations
        self._draw_annotations(draw, t, cam_cx, cam_cy, zoom, validator)
        
        # Header
        draw_editorial_scene_header(draw, "PHYSICAL HARDWARE // 01", "DILUTION REFRIGERATOR", "Cooling Willow circuits down to ten millikelvin", (212, 175, 55))
        if validator:
            validator.register("HEADER", BoundingBox(GRID_LEFT, 90, GRID_RIGHT, 230), "TEXT")
            
        # Subtitle
        if with_subtitles:
            self._draw_subtitles(canvas, t, validator)
            
        return canvas

    def _draw_cryostat(self, draw: ImageDraw.Draw, t: float, cx: float, cy: float, zoom: float, validator: Optional[SmartCompositionValidator]):
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))
            
        wx = 540.0
        y_top_flange, y_50k, y_4k, y_100mk, y_15mk, y_cf = 340.0, 540.0, 720.0, 890.0, 1050.0, 1200.0
        
        # Struts
        for p_top, p_bot in [((wx - 260, y_top_flange + 120), (wx - 220, y_50k)), ((wx - 130, y_top_flange + 120), (wx - 100, y_50k)), ((wx + 130, y_top_flange + 120), (wx + 100, y_50k)), ((wx + 260, y_top_flange + 120), (wx + 220, y_50k))]:
            vt, vb = tf(p_top[0], p_top[1]), tf(p_bot[0], p_bot[1])
            draw.polygon([(vt[0] - int(7 * zoom), vt[1]), (vt[0] + int(7 * zoom), vt[1]), (vb[0] + int(5 * zoom), vb[1]), (vb[0] - int(5 * zoom), vb[1])], fill=(225, 230, 240, 230))
            draw.line([vt[0] + int(5 * zoom), vt[1], vb[0] + int(4 * zoom), vb[1]], fill=(140, 150, 170, 200), width=2)
            
        # Cable looms
        for x0, x1, y0, y1, nc, wl in [(wx - 200, wx - 50, y_top_flange + 120, y_50k, 10, False), (wx + 50, wx + 200, y_top_flange + 120, y_50k, 10, False), (wx - 220, wx - 50, y_50k + 26, y_4k, 12, True), (wx + 50, wx + 220, y_50k + 26, y_4k, 12, True), (wx - 190, wx - 40, y_4k + 24, y_100mk, 12, True), (wx + 40, wx + 190, y_4k + 24, y_100mk, 12, True), (wx - 160, wx - 30, y_100mk + 22, y_15mk, 10, True), (wx + 30, wx + 160, y_100mk + 22, y_15mk, 10, True)]:
            step = (x1 - x0) / max(1, nc - 1)
            for i in range(nc):
                x = x0 + i * step
                pt, pb = tf(x, y0), tf(x, y1)
                if wl and (i % 2 == 0):
                    p_loop = tf(x, y0 + (y1 - y0) * 0.5)
                    draw.line([pt[0], pt[1], pt[0], p_loop[1] - int(10 * zoom)], fill=(235, 240, 248, 220), width=2)
                    draw.arc([pt[0] - int(7 * zoom), p_loop[1] - int(10 * zoom), pt[0] + int(7 * zoom), p_loop[1] + int(10 * zoom)], start=0, end=360, fill=(212, 175, 55, 230), width=2)
                    draw.line([pt[0], p_loop[1] + int(10 * zoom), pt[0], pb[1]], fill=(235, 240, 248, 220), width=2)
                else:
                    draw.line([pt[0], pt[1], pb[0], pb[1]], fill=(235, 240, 248, 220), width=2)
                    
        # Central column & attenuators
        vt_c0, vt_c1 = tf(wx - 26, y_top_flange + 120), tf(wx + 26, y_cf)
        draw.rectangle([vt_c0[0], vt_c0[1], vt_c1[0], vt_c1[1]], fill=(220, 226, 238, 255))
        for att_y in [y_50k + 80, y_4k + 75, y_100mk + 70]:
            at0, at1 = tf(wx - 22, att_y - 18), tf(wx + 22, att_y + 18)
            draw.rectangle([at0[0], at0[1], at1[0], at1[1]], fill=(212, 175, 55, 255), outline=(255, 240, 150, 255), width=2)
            
        # Gold plates
        for wy, w, h in [(y_50k, 640, 30), (y_4k, 540, 28), (y_100mk, 440, 26), (y_15mk, 380, 24)]:
            p0, p1 = tf(wx - w / 2, wy), tf(wx + w / 2, wy + h)
            draw.rectangle([p0[0], p0[1], p1[0], p1[1]], fill=(212, 175, 55, 255))
            hs = max(2, int(4 * zoom))
            draw.rectangle([p0[0], p0[1], p1[0], p0[1] + hs], fill=(255, 248, 200, 255))
            draw.rectangle([p0[0], p1[1] - hs, p1[0], p1[1]], fill=(130, 85, 18, 255))
            
        # Top collar
        v_top0, v_top1 = tf(wx - 320, y_top_flange), tf(wx + 320, y_top_flange + 120)
        v_lip0, v_lip1 = tf(wx - 340, y_top_flange), tf(wx + 340, y_top_flange + 24)
        draw.rectangle([v_lip0[0], v_lip0[1], v_lip1[0], v_lip1[1]], fill=(230, 235, 245, 255))
        top_w = v_top1[0] - v_top0[0]
        if top_w > 0:
            for step in range(top_w):
                nu = step / top_w
                light = 0.55 + 0.35 * math.cos((nu - 0.45) * math.pi)
                gv = int(min(255, 150 + light * 90))
                draw.line([v_top0[0] + step, v_lip1[1], v_top0[0] + step, v_top1[1]], fill=(gv, gv, int(gv * 1.05), 255), width=1)
                
        # Cold finger & Willow chip package
        for off_x in [-100.0, 100.0]:
            can0, can1 = tf(wx + off_x - 32, y_15mk + 26), tf(wx + off_x + 32, y_15mk + 150)
            draw.rectangle([can0[0], can0[1], can1[0], can1[1]], fill=(212, 160, 40, 255), outline=(255, 230, 130, 255), width=2)
        cf0, cf1 = tf(wx - 26, y_15mk + 24), tf(wx + 26, y_cf)
        draw.rectangle([cf0[0], cf0[1], cf1[0], cf1[1]], fill=(130, 138, 150, 255), outline=(220, 230, 242, 255), width=2)
        wp0, wp1 = tf(wx - 52, y_cf), tf(wx + 52, y_cf + 50)
        draw.rounded_rectangle([wp0[0], wp0[1], wp1[0], wp1[1]], radius=8, fill=(20, 25, 36, 255), outline=(56, 189, 248, 255), width=3)
        wd0, wd1 = tf(wx - 18, y_cf + 12), tf(wx + 18, y_cf + 38)
        draw.rectangle([wd0[0], wd0[1], wd1[0], wd1[1]], fill=(56, 189, 248, 255))
        
        if validator:
            hero_box = BoundingBox(v_lip0[0], v_top0[1], v_lip1[0], wp1[1])
            validator.register("HERO_CRYOSTAT", hero_box, "HERO", visual_weight=2.0)

    def _draw_annotations(self, draw: ImageDraw.Draw, t: float, cx: float, cy: float, zoom: float, validator: Optional[SmartCompositionValidator]):
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))
        wx = 540.0
        if 1.8 <= t <= 5.0:
            op = min(1.0, (t - 1.8) / 0.5) if t < 4.5 else max(0.0, (5.0 - t) / 0.5)
            tgt = tf(wx + 270, 540.0)
            la = LeaderAnnotation(tgt[0], tgt[1], GRID_RIGHT - 360, tgt[1] - 40, "50K THERMAL FLANGE", "First-stage heat rejection", (212, 175, 55), "right")
            la.draw(draw, op)
            if validator and op > 0.5:
                validator.register("ANN_50K", BoundingBox(GRID_RIGHT - 360, tgt[1] - 80, GRID_RIGHT, tgt[1]), "ANNOTATION")
        if 4.0 <= t <= 7.0:
            op = min(1.0, (t - 4.0) / 0.5) if t < 6.5 else max(0.0, (7.0 - t) / 0.5)
            tgt = tf(wx - 130, 800.0)
            la = LeaderAnnotation(tgt[0], tgt[1], GRID_LEFT + 360, tgt[1] + 30, "COAXIAL RF LOOM", "NbTi superconducting wiring", (56, 189, 248), "left")
            la.draw(draw, op)
            if validator and op > 0.5:
                validator.register("ANN_COAX", BoundingBox(GRID_LEFT, tgt[1] - 10, GRID_LEFT + 360, tgt[1] + 70), "ANNOTATION")
        if t >= 6.8:
            op = min(1.0, (t - 6.8) / 0.5)
            tgt = tf(wx + 54, 1220.0)
            la = LeaderAnnotation(tgt[0], tgt[1], GRID_RIGHT - 380, tgt[1] - 30, "PROTECTED WILLOW DIE", "10 mK Base Environment", (52, 211, 153), "right")
            la.draw(draw, op)
            if validator and op > 0.5:
                validator.register("ANN_DIE", BoundingBox(GRID_RIGHT - 380, tgt[1] - 70, GRID_RIGHT, tgt[1] + 10), "ANNOTATION")

    def _draw_subtitles(self, canvas: Image.Image, t: float, validator: Optional[SmartCompositionValidator]):
        active_chunk = None
        for text, word, t0, t1 in self.subtitles:
            if t0 <= t < t1:
                active_chunk = (text, word)
                break
        if not active_chunk:
            active_chunk = self.subtitles[-1][:2]
        render_subtitle_direction_a(canvas, active_chunk[0], active_word=active_chunk[1], y_center=1460)
        if validator:
            validator.register("SUBTITLE", BoundingBox(GRID_LEFT, 1420, GRID_RIGHT, 1505), "SUBTITLE")


# ==============================================================================
# SCENE 2: 105-QUBIT QUANTUM ARCHITECTURE (ARCHITECTURAL WARM STUDIO)
# ==============================================================================
class Scene2QuantumArchitecture:
    """Scene 2: 9.0s - 18.0s (105-Qubit Checkerboard Lattice on Warm Stone Canvas)."""
    def __init__(self, duration: float = 9.0):
        self.duration = duration
        self.camera = CinematicCameraDirectorV2([
            (0.0, 540.0, 820.0, 1.00),
            (4.0, 540.0, 820.0, 1.05),
            (9.0, 540.0, 820.0, 1.10),
        ])
        self.subtitles = [
            ("Beneath the gold thermal stages", "thermal", 0.0, 2.5),
            ("sits the processor:", "processor", 2.5, 4.5),
            ("105 physical qubits arranged in", "qubits", 4.5, 7.0),
            ("an alternating checkerboard lattice.", "checkerboard", 7.0, 9.0),
        ]

    def render_frame(self, t: float, with_subtitles: bool = True, validator: Optional[SmartCompositionValidator] = None) -> Image.Image:
        # Architectural warm stone background as seen in the reference video!
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (236, 234, 228, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # Soft studio contact vignette
        for r in range(950, 300, -150):
            alpha = int((1.0 - r / 950.0) * 20)
            draw.ellipse([540 - r, 820 - r, 540 + r, 820 + r], fill=(210, 206, 198, alpha))
            
        cam_cx, cam_cy, zoom = self.camera.get_state(t)
        
        # Render silicon die carrier (spans 900px width)
        self._draw_die_carrier(draw, cam_cx, cam_cy, zoom, validator)
        
        # Render 5x5 checkerboard surface code lattice
        self._draw_lattice(draw, t, cam_cx, cam_cy, zoom, validator)
        
        # Header (Dark slate editorial typography)
        draw_editorial_scene_header(draw, "Quantum Architecture // 02", "105-QUBIT PROCESSOR", "Surface code checkerboard of data and syndrome ancillas", (180, 130, 20))
        if validator:
            validator.register("HEADER", BoundingBox(GRID_LEFT, 90, GRID_RIGHT, 230), "TEXT")
            
        # Subtitle
        if with_subtitles:
            self._draw_subtitles(canvas, t, validator)
            
        return canvas

    def _draw_die_carrier(self, draw: ImageDraw.Draw, cx: float, cy: float, zoom: float, validator: Optional[SmartCompositionValidator]):
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))
        p0, p1 = tf(540 - 450, 820 - 450), tf(540 + 450, 820 + 450)
        # Soft ground contact shadow
        draw.rounded_rectangle([p0[0] + 12, p0[1] + 16, p1[0] + 12, p1[1] + 16], radius=24, fill=(180, 175, 165, 140))
        # Dark silicon die package
        draw.rounded_rectangle([p0[0], p0[1], p1[0], p1[1]], radius=24, fill=(30, 34, 46, 255), outline=(70, 80, 105, 255), width=3)
        # Gold wire bonds
        for bx in range(540 - 400, 540 + 400, 48):
            t0, t1 = tf(bx, 820 - 450), tf(bx, 820 - 490)
            draw.line([t0[0], t0[1], t1[0], t1[1]], fill=(212, 175, 55, 220), width=2)
            b0, b1 = tf(bx, 820 + 450), tf(bx, 820 + 490)
            draw.line([b0[0], b0[1], b1[0], b1[1]], fill=(212, 175, 55, 220), width=2)
        if validator:
            validator.register("HERO_DIE", BoundingBox(p0[0], p0[1], p1[0], p1[1]), "HERO", visual_weight=2.0)

    def _draw_lattice(self, draw: ImageDraw.Draw, t: float, cx: float, cy: float, zoom: float, validator: Optional[SmartCompositionValidator]):
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))
        grid_n = 4
        spacing = 180.0
        start_x, start_y = 540.0 - (grid_n - 1) * spacing / 2.0, 820.0 - (grid_n - 1) * spacing / 2.0
        
        # Plaquettes
        for r in range(grid_n - 1):
            for c in range(grid_n - 1):
                v0, v1 = tf(start_x + c * spacing, start_y + r * spacing), tf(start_x + (c+1)*spacing, start_y + (r+1)*spacing)
                is_z = ((r + c) % 2 == 0)
                fill_c = (56, 189, 248, 30) if is_z else (129, 140, 248, 30)
                edge_c = (56, 189, 248, 90) if is_z else (129, 140, 248, 90)
                draw.rectangle([v0[0], v0[1], v1[0], v1[1]], fill=fill_c, outline=edge_c, width=2)
                # Ancilla diamond
                av = tf(start_x + (c + 0.5) * spacing, start_y + (r + 0.5) * spacing)
                rad = int(18 * zoom)
                draw.polygon([(av[0], av[1] - rad), (av[0] + rad, av[1]), (av[0], av[1] + rad), (av[0] - rad, av[1])], fill=(129, 140, 248, 230))
                
        # Resonator buses & data qubits
        for r in range(grid_n):
            for c in range(grid_n):
                p_cur = tf(start_x + c * spacing, start_y + r * spacing)
                if c < grid_n - 1:
                    p_next = tf(start_x + (c+1)*spacing, start_y + r * spacing)
                    draw.line([p_cur[0], p_cur[1], p_next[0], p_next[1]], fill=(70, 90, 130, 180), width=max(2, int(3 * zoom)))
                if r < grid_n - 1:
                    p_down = tf(start_x + c * spacing, start_y + (r+1)*spacing)
                    draw.line([p_cur[0], p_cur[1], p_down[0], p_down[1]], fill=(70, 90, 130, 180), width=max(2, int(3 * zoom)))
                q_rad = int(22 * zoom)
                draw.ellipse([p_cur[0] - q_rad, p_cur[1] - q_rad, p_cur[0] + q_rad, p_cur[1] + q_rad], fill=(56, 189, 248, 255), outline=(230, 245, 255, 255), width=3)
                
        # Annotation callout
        if t >= 2.0:
            p_node = tf(start_x + 2 * spacing, start_y + spacing)
            la = LeaderAnnotation(p_node[0], p_node[1], GRID_RIGHT - 360, p_node[1] - 60, "DATA & SYNDROME QUBITS", "105-qubit planar connectivity", (180, 130, 20), "right")
            la.draw(draw, opacity=min(1.0, (t - 2.0) / 0.6))

    def _draw_subtitles(self, canvas: Image.Image, t: float, validator: Optional[SmartCompositionValidator]):
        active_chunk = None
        for text, word, t0, t1 in self.subtitles:
            if t0 <= t < t1:
                active_chunk = (text, word)
                break
        if not active_chunk:
            active_chunk = self.subtitles[-1][:2]
        render_subtitle_direction_a(canvas, active_chunk[0], active_word=active_chunk[1], y_center=1460)
        if validator:
            validator.register("SUBTITLE", BoundingBox(GRID_LEFT, 1420, GRID_RIGHT, 1505), "SUBTITLE")


# ==============================================================================
# SCENE 3: REAL-TIME ERROR HEALING (MACRO PLUNGE & TOPOLOGICAL LASER)
# ==============================================================================
class Scene3ErrorHealing:
    """Scene 3: 18.0s - 27.5s (The Quantum Battle: Bit-Flip, Parity Ripple, Laser Healing)."""
    def __init__(self, duration: float = 9.5):
        self.duration = duration
        self.camera = CinematicCameraDirectorV2([
            (0.0, 540.0, 820.0, 1.05),
            (2.2, 540.0, 820.0, 1.10),
            (3.8, 480.0, 760.0, 1.95),  # Macro plunge to failing qubit
            (6.2, 480.0, 760.0, 2.10),  # Stabilizer laser close-up
            (8.0, 540.0, 820.0, 1.20),  # Pullback
            (9.5, 540.0, 820.0, 1.15),
        ])
        self.subtitles = [
            ("When thermal decoherence flips", "decoherence", 0.0, 2.5),
            ("a physical data qubit,", "qubit", 2.5, 4.5),
            ("adjacent detectors pinpoint the disturbance,", "disturbance", 4.5, 7.0),
            ("firing a correction pulse in 840 nanoseconds.", "840", 7.0, 9.5),
        ]

    def render_frame(self, t: float, with_subtitles: bool = True, validator: Optional[SmartCompositionValidator] = None) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (236, 234, 228, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        cam_cx, cam_cy, zoom = self.camera.get_state(t)
        
        # Silicon Die Ground
        self._draw_die_carrier(draw, cam_cx, cam_cy, zoom, validator)
        
        # Lattice with error dynamics
        self._draw_error_dynamics(draw, t, cam_cx, cam_cy, zoom, validator)
        
        # Header
        draw_editorial_scene_header(draw, "Quantum Stabilizer Dynamics // 03", "TOPOLOGICAL HEALING", "Real-time syndrome extraction and laser phase correction", (2, 132, 199))
        if validator:
            validator.register("HEADER", BoundingBox(GRID_LEFT, 90, GRID_RIGHT, 230), "TEXT")
            
        # Subtitle
        if with_subtitles:
            self._draw_subtitles(canvas, t, validator)
            
        return canvas

    def _draw_die_carrier(self, draw: ImageDraw.Draw, cx: float, cy: float, zoom: float, validator: Optional[SmartCompositionValidator]):
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))
        p0, p1 = tf(540 - 450, 820 - 450), tf(540 + 450, 820 + 450)
        draw.rounded_rectangle([p0[0] + 12, p0[1] + 16, p1[0] + 12, p1[1] + 16], radius=24, fill=(180, 175, 165, 140))
        draw.rounded_rectangle([p0[0], p0[1], p1[0], p1[1]], radius=24, fill=(30, 34, 46, 255), outline=(70, 80, 105, 255), width=3)
        if validator:
            validator.register("HERO_DIE", BoundingBox(p0[0], p0[1], p1[0], p1[1]), "HERO", visual_weight=2.0)

    def _draw_error_dynamics(self, draw: ImageDraw.Draw, t: float, cx: float, cy: float, zoom: float, validator: Optional[SmartCompositionValidator]):
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))
        grid_n = 4
        spacing = 180.0
        start_x, start_y = 540.0 - (grid_n - 1) * spacing / 2.0, 820.0 - (grid_n - 1) * spacing / 2.0
        
        err_t, heal_t = 2.4, 5.2
        is_err = (t >= err_t)
        is_healed = (t >= heal_t)
        dim = 0.35 if (is_err and not is_healed) else 1.0
        
        # Plaquettes
        for r in range(grid_n - 1):
            for c in range(grid_n - 1):
                v0, v1 = tf(start_x + c * spacing, start_y + r * spacing), tf(start_x + (c+1)*spacing, start_y + (r+1)*spacing)
                is_target = (r == 1 and c == 1)
                is_z = ((r + c) % 2 == 0)
                if is_target and is_err and not is_healed:
                    pulse = math.sin((t - err_t) * 14) * 0.5 + 0.5
                    draw.rectangle([v0[0], v0[1], v1[0], v1[1]], fill=(239, 68, 68, int(45 + pulse * 65)), outline=(239, 68, 68, int(160 + pulse * 95)), width=3)
                else:
                    fc = (56, 189, 248, int(30 * dim)) if is_z else (129, 140, 248, int(30 * dim))
                    draw.rectangle([v0[0], v0[1], v1[0], v1[1]], fill=fc, outline=(70, 90, 130, int(90 * dim)), width=2)
                    
                av = tf(start_x + (c + 0.5) * spacing, start_y + (r + 0.5) * spacing)
                rad = int(18 * zoom)
                if is_target and is_err and not is_healed:
                    draw.polygon([(av[0], av[1] - rad), (av[0] + rad, av[1]), (av[0], av[1] + rad), (av[0] - rad, av[1])], fill=(252, 211, 77, 255))
                    wr = int(((t - err_t) * 120 * zoom) % (spacing * zoom * 1.5))
                    draw.ellipse([av[0] - wr, av[1] - wr, av[0] + wr, av[1] + wr], outline=(252, 211, 77, max(0, 210 - wr * 2)), width=3)
                else:
                    draw.polygon([(av[0], av[1] - rad), (av[0] + rad, av[1]), (av[0], av[1] + rad), (av[0] - rad, av[1])], fill=(129, 140, 248, int(220 * dim)))

        # Buses & Qubits
        for r in range(grid_n):
            for c in range(grid_n):
                p_cur = tf(start_x + c * spacing, start_y + r * spacing)
                if c < grid_n - 1:
                    p_next = tf(start_x + (c+1)*spacing, start_y + r * spacing)
                    draw.line([p_cur[0], p_cur[1], p_next[0], p_next[1]], fill=(70, 90, 130, int(150 * dim)), width=max(2, int(3 * zoom)))
                if r < grid_n - 1:
                    p_down = tf(start_x + c * spacing, start_y + (r+1)*spacing)
                    draw.line([p_cur[0], p_cur[1], p_down[0], p_down[1]], fill=(70, 90, 130, int(150 * dim)), width=max(2, int(3 * zoom)))
                q_rad = int(22 * zoom)
                if r == 1 and c == 1:
                    if is_err and not is_healed:
                        pulse = math.sin((t - err_t) * 16) * 0.5 + 0.5
                        draw.ellipse([p_cur[0] - q_rad - 12, p_cur[1] - q_rad - 12, p_cur[0] + q_rad + 12, p_cur[1] + q_rad + 12], fill=(239, 68, 68, int(80 + pulse * 140)))
                        draw.ellipse([p_cur[0] - q_rad, p_cur[1] - q_rad, p_cur[0] + q_rad, p_cur[1] + q_rad], fill=(239, 68, 68, 255), outline=(255, 220, 220, 255), width=3)
                        LeaderAnnotation(p_cur[0], p_cur[1], p_cur[0] + 120, p_cur[1] - 80, "PHASE-FLIP ERROR", "Parity inverted at Node (1,1)", (239, 68, 68), "right").draw(draw, 1.0)
                    elif is_healed:
                        bp = min(1.0, (t - heal_t) / 1.0)
                        br = int(q_rad + bp * 60)
                        draw.ellipse([p_cur[0] - br, p_cur[1] - br, p_cur[0] + br, p_cur[1] + br], outline=(56, 189, 248, int(255 * (1.0 - bp))), width=3)
                        draw.ellipse([p_cur[0] - q_rad, p_cur[1] - q_rad, p_cur[0] + q_rad, p_cur[1] + q_rad], fill=(56, 189, 248, 255), outline=(255, 255, 255, 255), width=3)
                        LeaderAnnotation(p_cur[0], p_cur[1], p_cur[0] + 120, p_cur[1] - 80, "STABILIZER RESTORED", "Cycle complete in 840 ns", (52, 211, 153), "right").draw(draw, max(0.0, 1.0 - (t - heal_t - 1.2)))
                    else:
                        draw.ellipse([p_cur[0] - q_rad, p_cur[1] - q_rad, p_cur[0] + q_rad, p_cur[1] + q_rad], fill=(56, 189, 248, 255), outline=(255, 255, 255, 255), width=3)
                else:
                    draw.ellipse([p_cur[0] - q_rad, p_cur[1] - q_rad, p_cur[0] + q_rad, p_cur[1] + q_rad], fill=(56, 189, 248, int(240 * dim)), outline=(210, 245, 255, int(220 * dim)), width=2)
                    
        # Laser beam
        if 4.4 <= t <= 5.4:
            av = tf(start_x + 0.5 * spacing, start_y + 0.5 * spacing)
            nv = tf(start_x + spacing, start_y + spacing)
            ba = int(255 * math.sin((t - 4.4) / 1.0 * math.pi))
            draw.line([av[0], av[1], nv[0], nv[1]], fill=(56, 189, 248, ba), width=max(4, int(8 * zoom)))
            draw.line([av[0], av[1], nv[0], nv[1]], fill=(255, 255, 255, ba), width=max(2, int(3 * zoom)))

    def _draw_subtitles(self, canvas: Image.Image, t: float, validator: Optional[SmartCompositionValidator]):
        active_chunk = None
        for text, word, t0, t1 in self.subtitles:
            if t0 <= t < t1:
                active_chunk = (text, word)
                break
        if not active_chunk:
            active_chunk = self.subtitles[-1][:2]
        render_subtitle_direction_a(canvas, active_chunk[0], active_word=active_chunk[1], y_center=1460)
        if validator:
            validator.register("SUBTITLE", BoundingBox(GRID_LEFT, 1420, GRID_RIGHT, 1505), "SUBTITLE")


# ==============================================================================
# SCENE 4: NATURE PUBLICATION & SCALING CURVE (THREE-ACT EDITORIAL)
# ==============================================================================
class Scene4NatureScaling:
    """Scene 4: 27.5s - 37.0s (Nature Journal Reveal + Dedicated 740px Scaling Graph)."""
    def __init__(self, duration: float = 9.5):
        self.duration = duration
        self.subtitles = [
            ("Published in Nature, Willow crossed", "Nature", 0.0, 2.5),
            ("the historic error threshold:", "threshold", 2.5, 4.5),
            ("scaling physical qubits now", "qubits", 4.5, 7.0),
            ("exponentially suppresses error rates.", "exponentially", 7.0, 9.5),
        ]

    def render_frame(self, t: float, with_subtitles: bool = True, validator: Optional[SmartCompositionValidator] = None) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (236, 234, 228, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # Header
        draw_editorial_scene_header(draw, "Empirical Evidence // 04", "BELOW-THRESHOLD SCALING", "Verified error suppression across distance 3, 5, and 7", (180, 130, 20))
        if validator:
            validator.register("HEADER", BoundingBox(GRID_LEFT, 90, GRID_RIGHT, 230), "TEXT")
            
        if t < 3.2:
            self._draw_nature_card(draw, t, validator)
        else:
            self._draw_scaling_plot(draw, t, validator)
            
        if with_subtitles:
            self._draw_subtitles(canvas, t, validator)
            
        return canvas

    def _draw_nature_card(self, draw: ImageDraw.Draw, t: float, validator: Optional[SmartCompositionValidator]):
        x0, y0, w, h = GRID_LEFT, 340, USABLE_WIDTH, 660
        x1, y1 = x0 + w, y0 + h
        draw.rounded_rectangle([x0 + 8, y0 + 12, x1 + 8, y1 + 12], radius=20, fill=(180, 175, 165, 140))
        draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=(248, 247, 244, 255), outline=(215, 212, 205, 255), width=2)
        
        draw.text((x0 + 48, y0 + 40), "nature", font=FONT_DISPLAY_HERO, fill=(200, 30, 30, 255))
        draw.text((x0 + 290, y0 + 58), "|  VOL 636  |  9 DECEMBER 2024  |  ARTICLE", font=FONT_MONO_LABEL, fill=(80, 85, 95, 255))
        draw.line([x0 + 48, y0 + 130, x1 - 48, y0 + 130], fill=(215, 210, 200, 255), width=2)
        
        draw.text((x0 + 48, y0 + 160), "Quantum error correction below the", font=FONT_DISPLAY_TITLE, fill=(15, 23, 42, 255))
        draw.text((x0 + 48, y0 + 220), "surface code threshold", font=FONT_DISPLAY_TITLE, fill=(15, 23, 42, 255))
        draw.text((x0 + 48, y0 + 290), "Google Quantum AI Collaborative  *  Peer-Reviewed Milestone", font=FONT_DISPLAY_SUB, fill=(71, 85, 105, 255))
        
        draw.rounded_rectangle([x0 + 48, y0 + 380, x0 + 480, y0 + 460], radius=14, fill=(240, 253, 244, 255), outline=(34, 197, 94, 255), width=2)
        draw.text((x0 + 72, y0 + 405), "EXPERIMENTAL MILESTONE ACHIEVED", font=FONT_BADGE_TITLE, fill=(22, 101, 52, 255))
        draw.text((x0 + 48, y0 + 490), "Physical hardware: 105 superconducting qubits at 10 millikelvin", font=FONT_DISPLAY_SUB, fill=(50, 60, 75, 255))
        draw.text((x0 + 48, y0 + 536), "Proving logical qubit error rates decrease as system size expands", font=FONT_BADGE_METRIC, fill=(100, 115, 130, 255))
        if validator:
            validator.register("HERO_NATURE_CARD", BoundingBox(x0, y0, x1, y1), "HERO", visual_weight=2.0)

    def _draw_scaling_plot(self, draw: ImageDraw.Draw, t: float, validator: Optional[SmartCompositionValidator]):
        x0, y0, w, h = GRID_LEFT, 320, USABLE_WIDTH, 760
        x1, y1 = x0 + w, y0 + h
        draw.rounded_rectangle([x0 + 8, y0 + 12, x1 + 8, y1 + 12], radius=20, fill=(180, 175, 165, 140))
        draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=(24, 32, 48, 255), outline=(55, 70, 95, 255), width=2)
        
        draw.text((x0 + 40, y0 + 36), "LOGICAL ERROR RATE VS CODE DISTANCE", font=FONT_BADGE_TITLE, fill=(240, 244, 250, 255))
        draw.text((x0 + 40, y0 + 74), "Experimental scaling across Distance 3, 5, and 7 surface code patches", font=FONT_BADGE_METRIC, fill=(148, 163, 184, 255))
        
        ax_x0, ax_y0, ax_x1, ax_y1 = x0 + 120, y1 - 90, x1 - 60, y0 + 140
        draw.line([ax_x0, ax_y0, ax_x1, ax_y0], fill=(100, 115, 140, 255), width=3)
        draw.line([ax_x0, ax_y0, ax_x0, ax_y1], fill=(100, 115, 140, 255), width=3)
        draw.text((ax_x1 - 220, ax_y0 + 24), "CODE DISTANCE (d)", font=FONT_MONO_LABEL, fill=(148, 163, 184, 255))
        draw.text((x0 + 30, ax_y1 - 10), "LOGICAL ERROR", font=FONT_MONO_LABEL, fill=(148, 163, 184, 255))
        
        d_ticks = [(ax_x0 + 180, "d = 3"), (ax_x0 + 440, "d = 5"), (ax_x0 + 700, "d = 7")]
        for tx, tlabel in d_ticks:
            draw.line([tx, ax_y0 - 8, tx, ax_y0 + 8], fill=(148, 163, 184, 255), width=2)
            draw.text((tx - 30, ax_y0 + 18), tlabel, font=FONT_DISPLAY_SUB, fill=(240, 244, 250, 255))
            
        thresh_y = y0 + 280
        draw.line([ax_x0, thresh_y, ax_x1, thresh_y], fill=(239, 68, 68, 180), width=2)
        draw.text((ax_x1 - 320, thresh_y - 34), "THRESHOLD LIMIT (Lambda = 1.0)", font=FONT_MONO_LABEL, fill=(239, 68, 68, 240))
        
        curve_prog = max(0.0, min(1.0, (t - 3.4) / 2.8))
        ease = 3 * curve_prog**2 - 2 * curve_prog**3
        pts = [(ax_x0 + 180, thresh_y + 40), (ax_x0 + 440, thresh_y + 160), (ax_x0 + 700, thresh_y + 260)]
        max_idx = int(ease * (len(pts) - 1))
        frac = (ease * (len(pts) - 1)) - max_idx
        drawn_pts = [pts[i] for i in range(max_idx + 1)]
        if max_idx < len(pts) - 1 and frac > 0.0:
            drawn_pts.append((pts[max_idx][0] + (pts[max_idx + 1][0] - pts[max_idx][0]) * frac, pts[max_idx][1] + (pts[max_idx + 1][1] - pts[max_idx][1]) * frac))
        for i in range(len(drawn_pts) - 1):
            draw.line([drawn_pts[i][0], drawn_pts[i][1], drawn_pts[i+1][0], drawn_pts[i+1][1]], fill=(56, 189, 248, 120), width=10)
            draw.line([drawn_pts[i][0], drawn_pts[i][1], drawn_pts[i+1][0], drawn_pts[i+1][1]], fill=(255, 255, 255, 255), width=4)
        if drawn_pts:
            hx, hy = drawn_pts[-1]
            draw.ellipse([hx - 12, hy - 12, hx + 12, hy + 12], fill=(56, 189, 248, 255))
        if curve_prog > 0.8:
            LeaderAnnotation(pts[2][0], pts[2][1], pts[2][0] - 260, pts[2][1] - 80, "LAMBDA = 2.14", "Exponential error suppression", (52, 211, 153), "left").draw(draw, 1.0)
        if validator:
            validator.register("HERO_GRAPH", BoundingBox(x0, y0, x1, y1), "HERO", visual_weight=2.0)

    def _draw_subtitles(self, canvas: Image.Image, t: float, validator: Optional[SmartCompositionValidator]):
        active_chunk = None
        for text, word, t0, t1 in self.subtitles:
            if t0 <= t < t1:
                active_chunk = (text, word)
                break
        if not active_chunk:
            active_chunk = self.subtitles[-1][:2]
        render_subtitle_direction_a(canvas, active_chunk[0], active_word=active_chunk[1], y_center=1460)
        if validator:
            validator.register("SUBTITLE", BoundingBox(GRID_LEFT, 1420, GRID_RIGHT, 1505), "SUBTITLE")


# ==============================================================================
# SCENE 5: SUPREMACY CONTRAST (FRONTIER VS WILLOW)
# ==============================================================================
class Scene5SupremacyContrast:
    """Scene 5: 37.0s - 46.0s (10 Septillion Years vs < 5 Minutes)."""
    def __init__(self, duration: float = 9.0):
        self.duration = duration
        self.subtitles = [
            ("In standard benchmarks, Willow completes", "Willow", 0.0, 2.5),
            ("in under five minutes a calculation", "minutes", 2.5, 4.5),
            ("that would take the fastest supercomputer", "supercomputer", 4.5, 7.0),
            ("ten septillion years.", "septillion", 7.0, 9.0),
        ]

    def render_frame(self, t: float, with_subtitles: bool = True, validator: Optional[SmartCompositionValidator] = None) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (12, 16, 28, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        draw_editorial_scene_header(draw, "Computational Supremacy // 05", "SUPREMACY BENCHMARK", "Random circuit sampling: classical supercomputer vs Willow", (52, 211, 153))
        if validator:
            validator.register("HEADER", BoundingBox(GRID_LEFT, 90, GRID_RIGHT, 230), "TEXT")
            
        x0, y0, w, h = GRID_LEFT, 320, USABLE_WIDTH, 760
        x1, y1 = x0 + w, y0 + h
        mid_x = CANVAS_WIDTH // 2
        
        draw.rounded_rectangle([x0 + 8, y0 + 12, x1 + 8, y1 + 12], radius=20, fill=(0, 0, 0, 95))
        draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=(16, 22, 38, 255), outline=(45, 60, 90, 255), width=2)
        draw.line([mid_x, y0 + 30, mid_x, y1 - 30], fill=(45, 60, 90, 255), width=2)
        
        # Left: Frontier
        draw.text((x0 + 40, y0 + 40), "CLASSICAL BENCHMARK", font=FONT_MONO_LABEL, fill=(239, 68, 68, 255))
        draw.text((x0 + 40, y0 + 76), "FRONTIER (OAK RIDGE)", font=FONT_DISPLAY_TITLE, fill=(240, 244, 250, 255))
        draw.text((x0 + 40, y0 + 130), "World's fastest supercomputer", font=FONT_BADGE_METRIC, fill=(148, 163, 184, 255))
        draw.text((x0 + 40, y0 + 220), "TIME REQUIRED:", font=FONT_MONO_LABEL, fill=(148, 163, 184, 220))
        draw.text((x0 + 40, y0 + 260), "10 SEPTILLION", font=FONT_DISPLAY_HERO, fill=(239, 68, 68, 255))
        draw.text((x0 + 40, y0 + 340), "YEARS (10^25 YR)", font=FONT_DISPLAY_TITLE, fill=(239, 68, 68, 220))
        draw.text((x0 + 40, y0 + 440), "* Classical runtime exceeds", font=FONT_DISPLAY_SUB, fill=(148, 163, 184, 200))
        draw.text((x0 + 40, y0 + 480), "  the age of the known universe", font=FONT_DISPLAY_SUB, fill=(148, 163, 184, 200))
        
        # Right: Willow
        draw.text((mid_x + 40, y0 + 40), "QUANTUM BENCHMARK", font=FONT_MONO_LABEL, fill=(52, 211, 153, 255))
        draw.text((mid_x + 40, y0 + 76), "GOOGLE WILLOW", font=FONT_DISPLAY_TITLE, fill=(240, 244, 250, 255))
        draw.text((mid_x + 40, y0 + 130), "105-Qubit Quantum Processor", font=FONT_BADGE_METRIC, fill=(148, 163, 184, 255))
        draw.text((mid_x + 40, y0 + 220), "TIME REQUIRED:", font=FONT_MONO_LABEL, fill=(148, 163, 184, 220))
        draw.text((mid_x + 40, y0 + 260), "< 5 MINUTES", font=FONT_DISPLAY_HERO, fill=(52, 211, 153, 255))
        draw.text((mid_x + 40, y0 + 340), "(UNDER 300 SECONDS)", font=FONT_DISPLAY_TITLE, fill=(52, 211, 153, 220))
        
        bar_w = 380
        bar_prog = min(1.0, max(0.0, (t - 1.5) / 3.0))
        draw.rectangle([mid_x + 40, y0 + 440, mid_x + 40 + bar_w, y0 + 470], fill=(25, 35, 55, 255))
        draw.rectangle([mid_x + 40, y0 + 440, mid_x + 40 + int(bar_w * bar_prog), y0 + 470], fill=(52, 211, 153, 255))
        draw.text((mid_x + 40, y0 + 490), "TASK COMPLETE // VERIFIED", font=FONT_MONO_LABEL, fill=(52, 211, 153, 255))
        
        if validator:
            validator.register("HERO_COMPARISON", BoundingBox(x0, y0, x1, y1), "HERO", visual_weight=2.0)
            
        if with_subtitles:
            self._draw_subtitles(canvas, t, validator)
            
        return canvas

    def _draw_subtitles(self, canvas: Image.Image, t: float, validator: Optional[SmartCompositionValidator]):
        active_chunk = None
        for text, word, t0, t1 in self.subtitles:
            if t0 <= t < t1:
                active_chunk = (text, word)
                break
        if not active_chunk:
            active_chunk = self.subtitles[-1][:2]
        render_subtitle_direction_a(canvas, active_chunk[0], active_word=active_chunk[1], y_center=1460)
        if validator:
            validator.register("SUBTITLE", BoundingBox(GRID_LEFT, 1420, GRID_RIGHT, 1505), "SUBTITLE")


# ==============================================================================
# SCENE 6: CONCLUSION & INFINITE LOOP (OBSIDIAN VOID)
# ==============================================================================
class Scene6ConclusionLoop:
    """Scene 6: 46.0s - 55.0s (Fault-Tolerant Era & Seamless Loop to Opening Frame)."""
    def __init__(self, duration: float = 9.0):
        self.duration = duration
        self.camera = CinematicCameraDirectorV2([
            (0.0, 540.0, 1100.0, 1.85), # Starts close on the Willow processor
            (3.0, 540.0, 960.0, 1.45),
            (6.5, 540.0, 780.0, 1.05),
            (9.0, 540.0, 780.0, 1.00),  # Pulls back to exact opening establishing framing!
        ])
        self.subtitles = [
            ("Practical quantum computing is no longer", "computing", 0.0, 2.5),
            ("a distant theoretical dream:", "theoretical", 2.5, 4.5),
            ("it is an operating machine,", "machine", 4.5, 7.0),
            ("protected forever in the cold.", "cold", 7.0, 9.0),
        ]

    def render_frame(self, t: float, with_subtitles: bool = True, validator: Optional[SmartCompositionValidator] = None) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (6, 4, 20, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        cx, cy = GRID_CENTER_X, 850
        for r in range(1100, 250, -140):
            alpha = int((1.0 - r / 1100.0) * 32)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(22, 12, 56, alpha))
            
        cam_cx, cam_cy, zoom = self.camera.get_state(t)
        
        # Render cryostat
        s1 = Scene1CryostatChandelier(duration=9.0)
        s1._draw_cryostat(draw, t, cam_cx, cam_cy, zoom, validator)
        
        # Header
        draw_editorial_scene_header(draw, "The Horizon // 06", "FAULT-TOLERANT ERA", "The threshold crossed: quantum supremacy made permanent", (212, 175, 55))
        if validator:
            validator.register("HEADER", BoundingBox(GRID_LEFT, 90, GRID_RIGHT, 230), "TEXT")
            
        # Final Callout
        if t >= 4.0:
            la = LeaderAnnotation(GRID_CENTER_X, 1200, GRID_RIGHT - 360, 1160, "FAULT-TOLERANT CORE", "105 Qubits / Continuous Operation", (52, 211, 153), "right")
            la.draw(draw, opacity=min(1.0, (t - 4.0) / 0.8))
            
        if with_subtitles:
            self._draw_subtitles(canvas, t, validator)
            
        return canvas

    def _draw_subtitles(self, canvas: Image.Image, t: float, validator: Optional[SmartCompositionValidator]):
        active_chunk = None
        for text, word, t0, t1 in self.subtitles:
            if t0 <= t < t1:
                active_chunk = (text, word)
                break
        if not active_chunk:
            active_chunk = self.subtitles[-1][:2]
        render_subtitle_direction_a(canvas, active_chunk[0], active_word=active_chunk[1], y_center=1460)
        if validator:
            validator.register("SUBTITLE", BoundingBox(GRID_LEFT, 1420, GRID_RIGHT, 1505), "SUBTITLE")


# ==============================================================================
# SUBTITLE V2 EVALUATION SHEET GENERATOR
# ==============================================================================
def render_subtitle_comparison_sheet():
    print("\n[SUBTITLES] Generating Subtitle V2 Comparison Sheet...")
    s1 = Scene1CryostatChandelier()
    base_frame = s1.render_frame(t=3.8, with_subtitles=False)
    
    fa = base_frame.copy()
    render_subtitle_direction_a(fa, "Willow is suspended inside a dilution refrigerator.", active_word="refrigerator", y_center=1460)
    
    fb = base_frame.copy()
    render_subtitle_direction_b(fb, "Willow is suspended inside a dilution refrigerator.", active_word="refrigerator", y_center=1460)
    
    fc = base_frame.copy()
    render_subtitle_direction_c(fc, "Willow is suspended inside a dilution refrigerator.", active_word="refrigerator", y_center=1460)
    
    comp = Image.new("RGBA", (1920, 1080), (10, 14, 24, 255))
    crop_box = (0, 1180, 1080, 1620)
    c1 = fa.crop(crop_box).resize((580, 240), Image.Resampling.LANCZOS)
    c2 = fb.crop(crop_box).resize((580, 240), Image.Resampling.LANCZOS)
    c3 = fc.crop(crop_box).resize((580, 240), Image.Resampling.LANCZOS)
    
    cdraw = ImageDraw.Draw(comp)
    cdraw.text((60, 40), "SUPER.INTELLIGENCEEE // SUBTITLE ARCHITECTURE EVALUATION", font=FONT_BADGE_TITLE, fill=(212, 175, 55, 255))
    cdraw.text((60, 80), "Three Distinct Subtitle Styles Tested on Actual Flagship Footage", font=FONT_DISPLAY_TITLE, fill=(255, 255, 255, 255))
    
    comp.paste(c1, (60, 180))
    cdraw.rectangle([60, 180, 640, 420], outline=(252, 211, 77, 220), width=2)
    cdraw.text((60, 435), "STYLE A: CLEAN EDITORIAL PHRASE-GROUP (WINNER)", font=FONT_BADGE_TITLE, fill=(252, 211, 77, 255))
    cdraw.text((60, 475), "- Zero background box; subtle soft vignette; luminous gold active word", font=FONT_DISPLAY_SUB, fill=(180, 190, 205, 255))
    
    comp.paste(c2, (680, 180))
    cdraw.rectangle([680, 180, 1260, 420], outline=(56, 189, 248, 220), width=2)
    cdraw.text((680, 435), "STYLE B: RESTRAINED KINETIC WORD EMPHASIS", font=FONT_BADGE_TITLE, fill=(56, 189, 248, 255))
    cdraw.text((680, 475), "- Frosted glass capsule with cyan active word and underline", font=FONT_DISPLAY_SUB, fill=(180, 190, 205, 255))
    
    comp.paste(c3, (1300, 180))
    cdraw.rectangle([1300, 180, 1880, 420], outline=(52, 211, 153, 220), width=2)
    cdraw.text((1300, 435), "STYLE C: MINIMAL DOCUMENTARY CAPTIONS", font=FONT_BADGE_TITLE, fill=(52, 211, 153, 255))
    cdraw.text((1300, 475), "- Pure floating typography; active word in soft emerald mint (#34D399)", font=FONT_DISPLAY_SUB, fill=(180, 190, 205, 255))
    
    out_sheet = SUBTITLES_DIR / "subtitle_comparison_sheet.png"
    comp.save(out_sheet)
    print(f"[SUBTITLES] Saved comparison sheet: {out_sheet}")


# ==============================================================================
# MAIN FLAGSHIP PRODUCTION ORCHESTRATION
# ==============================================================================
def main():
    guard = ResourceGuard()
    guard.configure_environment()
    
    print("=" * 80)
    print("PHASE 9.2: COMPLETE FLAGSHIP DOCUMENTARY PRODUCTION (55.0 SECONDS)")
    print("=" * 80)
    
    # 1. Subtitle Comparison
    render_subtitle_comparison_sheet()
    
    scenes = [
        ("scene1_cryostat", Scene1CryostatChandelier(duration=9.0)),
        ("scene2_architecture", Scene2QuantumArchitecture(duration=9.0)),
        ("scene3_error_healing", Scene3ErrorHealing(duration=9.5)),
        ("scene4_nature_scaling", Scene4NatureScaling(duration=9.5)),
        ("scene5_supremacy_contrast", Scene5SupremacyContrast(duration=9.0)),
        ("scene6_conclusion_loop", Scene6ConclusionLoop(duration=9.0)),
    ]
    
    total_duration = sum(s[1].duration for s in scenes)
    print(f"\n[ORCHESTRATION] Assembling 6 Scenes. Total Planned Duration: {total_duration:.1f}s")
    
    # Audio Soundtrack
    master_audio = AUDIO_DIR / "master_documentary_soundtrack.wav"
    if not master_audio.exists():
        raise RuntimeError("Master audio soundtrack not found. Run synthesize_phase9_2_audio.py first.")
        
    # Output Videos
    clean_master_mp4 = PROD_DIR / "willow_quantum_flagship_clean_master.mp4"
    review_master_mp4 = PROD_DIR / "willow_quantum_flagship_captioned_review.mp4"
    fps = 30.0
    
    print(f"\n[RENDER] Spawning Dual FFmpeg Pipes for Clean & Captioned Masters...")
    cmd_clean = [
        "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}", "-pix_fmt", "rgba",
        "-r", str(fps), "-i", "-",
        "-i", str(master_audio),
        "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
        "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(clean_master_mp4)
    ]
    proc_clean = subprocess.Popen(cmd_clean, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, bufsize=10**7)
    
    cmd_review = [
        "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}", "-pix_fmt", "rgba",
        "-r", str(fps), "-i", "-",
        "-i", str(master_audio),
        "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
        "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(review_master_mp4)
    ]
    proc_review = subprocess.Popen(cmd_review, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, bufsize=10**7)
    
    validator = SmartCompositionValidator(CANVAS_WIDTH, CANVAS_HEIGHT)
    diagnostic_overlays_saved = 0
    t_start = time.time()
    total_rendered_frames = 0
    global_frame_idx = 0
    
    try:
        for s_idx, (s_name, s_comp) in enumerate(scenes):
            scene_frames = int(s_comp.duration * fps)
            print(f"\n[SCENE {s_idx+1}/6] Rendering {s_name} ({s_comp.duration:.1f}s, {scene_frames} frames)...")
            
            for f_idx in range(scene_frames):
                t = f_idx / fps
                validator.clear()
                
                # Render clean frame
                frame_clean = s_comp.render_frame(t, with_subtitles=False, validator=None)
                proc_clean.stdin.write(frame_clean.tobytes())
                
                # Render captioned frame with validation
                frame_review = s_comp.render_frame(t, with_subtitles=True, validator=validator)
                proc_review.stdin.write(frame_review.tobytes())
                
                # Diagnostic overlay capture for 2 keyframes per scene
                if f_idx in [int(scene_frames * 0.3), int(scene_frames * 0.7)]:
                    diag_im = validator.draw_diagnostic_overlay(frame_review)
                    diag_path = OVERLAYS_DIR / f"{s_name}_diag_f{f_idx:03d}.png"
                    diag_im.save(diag_path)
                    diagnostic_overlays_saved += 1
                    
                total_rendered_frames += 1
                global_frame_idx += 1
                if global_frame_idx % 90 == 0:
                    el = time.time() - t_start
                    fps_live = (global_frame_idx * 2) / max(0.001, el)
                    print(f"  Frame {global_frame_idx}/{int(total_duration*fps)} ({global_frame_idx/(total_duration*fps)*100:.1f}%) | {fps_live:.1f} dual-fps")
                    
        proc_clean.stdin.close()
        proc_clean.wait()
        proc_review.stdin.close()
        proc_review.wait()
    except Exception as e:
        proc_clean.kill()
        proc_review.kill()
        raise RuntimeError(f"Rendering failed: {e}")
        
    dur = time.time() - t_start
    print(f"\n[RENDER COMPLETE] Finished dual masters in {dur:.1f}s ({total_rendered_frames*2/dur:.1f} fps)")
    print(f"  Clean Master:    {clean_master_mp4} ({clean_master_mp4.stat().st_size} bytes)")
    print(f"  Review Master:   {review_master_mp4} ({review_master_mp4.stat().st_size} bytes)")
    
    # 40+ Frame Forensic Contact Sheet Extraction
    print("\n[CONTACT SHEET] Extracting 42 evenly distributed frames across the full 55s video...")
    num_contact_frames = 42 # 6 rows x 7 cols
    cols = 7
    rows = 6
    step_t = total_duration / num_contact_frames
    
    extracted_frames = []
    for i in range(num_contact_frames):
        tf = i * step_t
        out_f = FRAMES_DIR / f"frame_{i:02d}_{tf:.2f}s.png"
        cmd_ext = [
            "ffmpeg", "-y",
            "-ss", f"{tf:.3f}",
            "-i", str(review_master_mp4),
            "-vframes", "1",
            "-q:v", "2",
            str(out_f)
        ]
        subprocess.run(cmd_ext, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        extracted_frames.append(out_f)
        
    # Build 7x6 High-Resolution Contact Sheet
    tw, th = 260, 462
    pad = 12
    sheet_w = cols * tw + (cols + 1) * pad
    sheet_h = rows * th + (rows + 1) * pad + 70
    
    sheet = Image.new("RGB", (sheet_w, sheet_h), (12, 16, 26))
    sdraw = ImageDraw.Draw(sheet)
    sdraw.text((pad, 20), "GOOGLE WILLOW: REAL-TIME QUANTUM ERROR CORRECTION // 42-FRAME FORENSIC CONTACT SHEET", font=FONT_BADGE_TITLE, fill=(212, 175, 55))
    
    for idx, ff in enumerate(extracted_frames):
        r = idx // cols
        c = idx % cols
        x = pad + c * (tw + pad)
        y = 70 + pad + r * (th + pad)
        im = Image.open(ff).resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        sdraw.rectangle([x, y, x + tw, y + th], outline=(55, 70, 95), width=2)
        sdraw.text((x + 8, y + 8), f"#{idx+1:02d} ({idx*step_t:.1f}s)", font=FONT_MONO_LABEL, fill=(255, 255, 255))
        
    sheet_path = PROD_DIR / "phase9_2_40frame_contact_sheet.png"
    sheet.save(sheet_path)
    print(f"[CONTACT SHEET] Saved 42-frame sheet: {sheet_path}")
    
    # Manifest Generation
    manifest = {
        "production_id": "willow_quantum_flagship_v9_2",
        "title": "Google Willow: Real-Time Quantum Error Correction Below Threshold",
        "topic": "Google Quantum AI December 2024 Breakthrough (Nature Vol 636)",
        "duration_seconds": total_duration,
        "resolution": "1080x1920",
        "frame_rate": 30.0,
        "voice": "Kokoro-82M am_liam (General American)",
        "clean_master": str(clean_master_mp4),
        "review_master": str(review_master_mp4),
        "contact_sheet": str(sheet_path),
        "diagnostic_overlays": diagnostic_overlays_saved,
        "governance_status": "AWAITING_HUMAN_APPROVAL",
        "publishing_kill_switch_armed": True,
        "scenes": [s[0] for s in scenes]
    }
    manifest_path = PROD_DIR / "willow_quantum_flagship_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"[MANIFEST] Production manifest saved: {manifest_path}")

if __name__ == "__main__":
    main()

