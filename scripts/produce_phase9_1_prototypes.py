"""
SUPER.INTELLIGENCEEE — Phase 9.1 Autonomous Visual Storytelling & Documentary Production Engine
Executes complete visual redesign:
1. Standardized 1080x1920 layout grid (72px margins, defined vertical zones).
2. Leader-line annotation system with pill badges and collision-free elbow connectors.
3. Purposeful narrative camera choreography (wide -> macro close-ups -> detail reveals).
4. Prototype A: High-fidelity dilution refrigerator with 5-stage camera narrative.
5. Prototype B: Surface code lattice with macro dive and topological error healing.
6. Prototype C: Three-act sequential documentary (Publication -> Scaling Graph -> Supremacy Contrast).
7. Subtitle Engine V2: Three refined directions (Style A, Style B, Style C).
8. Exports both Clean Archival Masters and Captioned Review Masters + 30-frame Contact Sheets.
"""

from __future__ import annotations

import os
import sys
import time
import math
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
from rendering.resource_guard import ResourceGuard

PHASE9_1_DIR = WORKSPACE_ROOT / "output" / "drafts" / "phase9_1"
FRAMES_DIR = PHASE9_1_DIR / "frames"
SUBTITLES_DIR = PHASE9_1_DIR / "subtitles"
MASTERS_DIR = PHASE9_1_DIR / "masters"
AUDIO_DIR = WORKSPACE_ROOT / "output" / "drafts" / "phase9_prototypes" / "audio"

PHASE9_1_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)
SUBTITLES_DIR.mkdir(parents=True, exist_ok=True)
MASTERS_DIR.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# PROTOTYPE A: PHYSICAL TECHNOLOGY (CRYOSTAT RECONSTRUCTION)
# ==============================================================================

class PrototypeARevised:
    """
    Revised Prototype A: Dilution Refrigerator.
    5-Stage Narrative Camera Arc:
    - 0.0s - 2.2s: Establishing wide shot of complete physical apparatus (760px wide).
    - 2.2s - 4.4s: Camera dives toward upper thermal stages (50K & 4K plates) with leader callouts.
    - 4.4s - 6.4s: Macro close-up on coaxial cable harness and central attenuator column.
    - 6.4s - 7.8s: Camera tracks down to the 15mK mixing flange and gold amplifier cans.
    - 7.8s - 9.0s: Final close-up reveals the thermally protected Willow qubit package.
    """
    def __init__(self, duration: float = 9.0):
        self.duration = duration
        self.width = CANVAS_WIDTH
        self.height = CANVAS_HEIGHT
        
        # 5 Keyframe Camera Arc: (t_sec, cam_center_x, cam_center_y, zoom)
        self.camera = CinematicCameraDirectorV2([
            (0.0, 540.0, 780.0, 1.00),  # Stage 1: Establishing Wide
            (2.2, 540.0, 720.0, 1.05),
            (3.4, 520.0, 600.0, 1.40),  # Stage 2: Upper Thermal Stages
            (5.0, 500.0, 720.0, 1.65),  # Stage 3: Coaxial Wire Loom Macro
            (6.8, 540.0, 940.0, 1.50),  # Stage 4: 15mK Mixing Base & Amps
            (8.2, 540.0, 1080.0, 1.85), # Stage 5: Protected Willow Chip
            (9.0, 540.0, 1100.0, 1.90),
        ])
        
        self.subtitles = [
            ("To protect fragile qubits", "qubits", 0.0, 2.5),
            ("from room-temperature noise,", "noise", 2.5, 5.0),
            ("Willow is suspended inside", "suspended", 5.0, 7.0),
            ("a multi-stage dilution refrigerator.", "refrigerator", 7.0, 9.0),
        ]

    def render_frame(self, t: float, with_subtitles: bool = True) -> Image.Image:
        canvas = Image.new("RGBA", (self.width, self.height), (6, 4, 20, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # 1. Background Radial Lighting (Atmospheric cryogenic void)
        cx, cy = CANVAS_WIDTH // 2, 850
        for r in range(1100, 250, -140):
            alpha = int((1.0 - r / 1100.0) * 32)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(22, 12, 56, alpha))
            
        # 2. Camera Transform Parameters
        cam_cx, cam_cy, zoom = self.camera.get_state(t)
        
        # 3. Render Dilution Refrigerator Physical Apparatus
        self._draw_cryostat(draw, canvas, t, cam_cx, cam_cy, zoom)
        
        # 4. Dynamic Editorial Leader Annotations
        self._draw_leader_annotations(draw, t, cam_cx, cam_cy, zoom)
        
        # 5. Standardized Editorial Header
        draw_editorial_scene_header(
            draw,
            category="Physical Instrumentation // 01",
            title="DILUTION REFRIGERATOR",
            subtitle="Cooling Willow processor to 10 mK — colder than deep space",
            accent_color=(212, 175, 55)
        )
        
        # 6. Subtitles: Direction A (Clean Editorial Phrase-Group Captions)
        if with_subtitles:
            self._draw_subtitles(canvas, t)
            
        return canvas

    def _draw_cryostat(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float, cx: float, cy: float, zoom: float):
        # Base world anchor: center at 540, base_y = 420
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))

        wx = 540.0
        # World Y coordinates of stages
        y_top_flange = 340.0
        y_stage_50k = 540.0
        y_stage_4k = 720.0
        y_stage_100mk = 890.0
        y_stage_15mk = 1050.0
        y_cold_finger = 1200.0
        
        # --- A. Tapered Structural Struts (Top Collar to 50K) ---
        strut_coords = [
            ((wx - 260, y_top_flange + 120), (wx - 220, y_stage_50k)),
            ((wx - 130, y_top_flange + 120), (wx - 100, y_stage_50k)),
            ((wx + 130, y_top_flange + 120), (wx + 100, y_stage_50k)),
            ((wx + 260, y_top_flange + 120), (wx + 220, y_stage_50k)),
        ]
        for p_top, p_bot in strut_coords:
            vt = tf(p_top[0], p_top[1])
            vb = tf(p_bot[0], p_bot[1])
            draw.polygon([
                (vt[0] - int(7 * zoom), vt[1]), (vt[0] + int(7 * zoom), vt[1]),
                (vb[0] + int(5 * zoom), vb[1]), (vb[0] - int(5 * zoom), vb[1])
            ], fill=(225, 230, 240, 230))
            draw.line([vt[0] + int(5 * zoom), vt[1], vb[0] + int(4 * zoom), vb[1]], fill=(140, 150, 170, 200), width=2)
            
        # --- B. Vertical Coaxial RF Cable Looms ---
        self._draw_cable_loom(draw, tf, wx - 200, wx - 50, y_top_flange + 120, y_stage_50k, 10, zoom=zoom)
        self._draw_cable_loom(draw, tf, wx + 50, wx + 200, y_top_flange + 120, y_stage_50k, 10, zoom=zoom)
        
        self._draw_cable_loom(draw, tf, wx - 220, wx - 50, y_stage_50k + 26, y_stage_4k, 12, with_loops=True, zoom=zoom)
        self._draw_cable_loom(draw, tf, wx + 50, wx + 220, y_stage_50k + 26, y_stage_4k, 12, with_loops=True, zoom=zoom)
        
        self._draw_cable_loom(draw, tf, wx - 190, wx - 40, y_stage_4k + 24, y_stage_100mk, 12, with_loops=True, zoom=zoom)
        self._draw_cable_loom(draw, tf, wx + 40, wx + 190, y_stage_4k + 24, y_stage_100mk, 12, with_loops=True, zoom=zoom)
        
        self._draw_cable_loom(draw, tf, wx - 160, wx - 30, y_stage_100mk + 22, y_stage_15mk, 10, with_loops=True, zoom=zoom)
        self._draw_cable_loom(draw, tf, wx + 30, wx + 160, y_stage_100mk + 22, y_stage_15mk, 10, with_loops=True, zoom=zoom)

        # --- C. Central Structural Column & Attenuators ---
        vt_c0 = tf(wx - 26, y_top_flange + 120)
        vt_c1 = tf(wx + 26, y_cold_finger)
        draw.rectangle([vt_c0[0], vt_c0[1], vt_c1[0], vt_c1[1]], fill=(220, 226, 238, 255))
        draw.line([vt_c0[0], vt_c0[1], vt_c0[0], vt_c1[1]], fill=(160, 170, 185, 255), width=2)
        
        for att_y in [y_stage_50k + 80, y_stage_4k + 75, y_stage_100mk + 70]:
            at0 = tf(wx - 22, att_y - 18)
            at1 = tf(wx + 22, att_y + 18)
            draw.rectangle([at0[0], at0[1], at1[0], at1[1]], fill=(212, 175, 55, 255), outline=(255, 240, 150, 255), width=2)

        # --- D. Gold Thermal Stage Disks (With 3D Metallic Shading) ---
        self._draw_gold_plate(draw, tf, wx, y_stage_50k, width=640, height=30, zoom=zoom)
        self._draw_gold_plate(draw, tf, wx, y_stage_4k, width=540, height=28, zoom=zoom)
        self._draw_gold_plate(draw, tf, wx, y_stage_100mk, width=440, height=26, zoom=zoom)
        self._draw_gold_plate(draw, tf, wx, y_stage_15mk, width=380, height=24, zoom=zoom)

        # --- E. Top Cylindrical Vacuum Collar ---
        v_top0 = tf(wx - 320, y_top_flange)
        v_top1 = tf(wx + 320, y_top_flange + 120)
        v_lip0 = tf(wx - 340, y_top_flange)
        v_lip1 = tf(wx + 340, y_top_flange + 24)
        
        draw.rectangle([v_lip0[0], v_lip0[1], v_lip1[0], v_lip1[1]], fill=(230, 235, 245, 255))
        top_w = v_top1[0] - v_top0[0]
        if top_w > 0:
            for step in range(top_w):
                norm_u = step / top_w
                light = 0.55 + 0.35 * math.cos((norm_u - 0.45) * math.pi)
                gv = int(min(255, 150 + light * 90))
                draw.line([v_top0[0] + step, v_lip1[1], v_top0[0] + step, v_top1[1]], fill=(gv, gv, int(gv * 1.05), 255), width=1)
        v_botlip0 = tf(wx - 330, y_top_flange + 120)
        v_botlip1 = tf(wx + 330, y_top_flange + 134)
        draw.rectangle([v_botlip0[0], v_botlip0[1], v_botlip1[0], v_botlip1[1]], fill=(200, 205, 218, 255))

        # --- F. Bottom RF Amplifier Cans & Cold Finger ---
        # Dual gold amplifier cans
        for off_x in [-100.0, 100.0]:
            can0 = tf(wx + off_x - 32, y_stage_15mk + 26)
            can1 = tf(wx + off_x + 32, y_stage_15mk + 150)
            draw.rectangle([can0[0], can0[1], can1[0], can1[1]], fill=(212, 160, 40, 255), outline=(255, 230, 130, 255), width=2)
            for ry in range(can0[1] + 12, can1[1] - 10, max(8, int(16 * zoom))):
                draw.line([can0[0] + 4, ry, can1[0] - 4, ry], fill=(160, 110, 20, 255), width=2)
                
        # Central Cold Finger (Nickel-Plated Copper)
        cf0 = tf(wx - 26, y_stage_15mk + 24)
        cf1 = tf(wx + 26, y_cold_finger)
        draw.rectangle([cf0[0], cf0[1], cf1[0], cf1[1]], fill=(130, 138, 150, 255), outline=(220, 230, 242, 255), width=2)
        
        # Willow Qubit Processor Package
        wp0 = tf(wx - 52, y_cold_finger)
        wp1 = tf(wx + 52, y_cold_finger + 50)
        draw.rounded_rectangle([wp0[0], wp0[1], wp1[0], wp1[1]], radius=8, fill=(20, 25, 36, 255), outline=(56, 189, 248, 255), width=3)
        # Glowing cyan quantum processor die
        wd0 = tf(wx - 18, y_cold_finger + 12)
        wd1 = tf(wx + 18, y_cold_finger + 38)
        draw.rectangle([wd0[0], wd0[1], wd1[0], wd1[1]], fill=(56, 189, 248, 255))

    def _draw_gold_plate(self, draw: ImageDraw.Draw, tf, wx: float, wy: float, width: float, height: float, zoom: float):
        p0 = tf(wx - width / 2, wy)
        p1 = tf(wx + width / 2, wy + height)
        # Body
        draw.rectangle([p0[0], p0[1], p1[0], p1[1]], fill=(212, 175, 55, 255))
        # Top specular highlight strip
        h_strip = max(2, int(4 * zoom))
        draw.rectangle([p0[0], p0[1], p1[0], p0[1] + h_strip], fill=(255, 248, 200, 255))
        # Bottom ambient occlusion shadow lip
        draw.rectangle([p0[0], p1[1] - h_strip, p1[0], p1[1]], fill=(130, 85, 18, 255))
        # Borders
        draw.line([p0[0], p0[1], p0[0], p1[1]], fill=(255, 235, 140, 255), width=2)
        draw.line([p1[0], p0[1], p1[0], p1[1]], fill=(130, 85, 18, 255), width=2)

    def _draw_cable_loom(self, draw: ImageDraw.Draw, tf, x0: float, x1: float, y0: float, y1: float, num_cables: int, with_loops: bool = False, zoom: float = 1.0):
        step = (x1 - x0) / max(1, num_cables - 1)
        cable_color = (235, 240, 248, 220)
        cable_shade = (160, 170, 185, 170)
        for i in range(num_cables):
            x = x0 + i * step
            p_top = tf(x, y0)
            p_bot = tf(x, y1)
            if with_loops and (i % 2 == 0):
                loop_wy = y0 + (y1 - y0) * 0.5
                p_loop = tf(x, loop_wy)
                draw.line([p_top[0], p_top[1], p_top[0], p_loop[1] - int(10 * zoom)], fill=cable_color, width=2)
                draw.arc([p_top[0] - int(7 * zoom), p_loop[1] - int(10 * zoom), p_top[0] + int(7 * zoom), p_loop[1] + int(10 * zoom)], start=0, end=360, fill=(212, 175, 55, 230), width=2)
                draw.line([p_top[0], p_loop[1] + int(10 * zoom), p_top[0], p_bot[1]], fill=cable_color, width=2)
            else:
                draw.line([p_top[0], p_top[1], p_bot[0], p_bot[1]], fill=cable_color, width=2)
                draw.line([p_top[0] + 1, p_top[1], p_bot[0] + 1, p_bot[1]], fill=cable_shade, width=1)

    def _draw_leader_annotations(self, draw: ImageDraw.Draw, t: float, cx: float, cy: float, zoom: float):
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))
            
        wx = 540.0
        # 1. Annotation for Upper Stages (Active t in [2.0, 5.0])
        if 1.8 <= t <= 5.2:
            op = min(1.0, (t - 1.8) / 0.5) if t < 4.7 else max(0.0, (5.2 - t) / 0.5)
            target = tf(wx + 270, 540.0)
            LeaderAnnotation(
                target_x=target[0], target_y=target[1],
                badge_x=GRID_RIGHT - 360, badge_y=target[1] - 40,
                title="50K THERMAL FLANGE",
                metric="First-stage heat rejection",
                color=(212, 175, 55),
                align="right"
            ).draw(draw, opacity=op)
            
        # 2. Annotation for Coaxial Loom (Active t in [4.2, 7.0])
        if 4.2 <= t <= 7.2:
            op = min(1.0, (t - 4.2) / 0.5) if t < 6.7 else max(0.0, (7.2 - t) / 0.5)
            target = tf(wx - 130, 800.0)
            LeaderAnnotation(
                target_x=target[0], target_y=target[1],
                badge_x=GRID_LEFT + 360, badge_y=target[1] + 30,
                title="COAXIAL RF LOOM",
                metric="NbTi superconducting wiring",
                color=(56, 189, 248),
                align="left"
            ).draw(draw, opacity=op)
            
        # 3. Annotation for Cold Finger & Protected Chip (Active t in [6.8, 9.0])
        if t >= 6.8:
            op = min(1.0, (t - 6.8) / 0.5)
            target = tf(wx + 54, 1220.0)
            LeaderAnnotation(
                target_x=target[0], target_y=target[1],
                badge_x=GRID_RIGHT - 380, badge_y=target[1] - 30,
                title="PROTECTED WILLOW DIE",
                metric="10 mK Base Environment",
                color=(52, 211, 153),
                align="right"
            ).draw(draw, opacity=op)

    def _draw_subtitles(self, canvas: Image.Image, t: float):
        active_chunk = None
        for text, word, t0, t1 in self.subtitles:
            if t0 <= t < t1:
                active_chunk = (text, word)
                break
        if not active_chunk:
            active_chunk = self.subtitles[-1][:2]
            
        text, word = active_chunk
        # Style A: Clean Editorial Phrase-Group Captions
        render_subtitle_direction_a(canvas, text, active_word=word, y_center=1460)


# ==============================================================================
# PROTOTYPE B: ABSTRACT TECHNICAL CONCEPT (SURFACE CODE RECONSTRUCTION)
# ==============================================================================

class PrototypeBRevised:
    """
    Revised Prototype B: Quantum Surface Code Lattice & Topological Healing.
    Key Improvements:
    - Lattice fills 85% of canvas width ($W = 920\text{px}$). No small card box.
    - Camera executes dramatic macro dive ($1.0\times \to 2.1\times$) directly into the error node.
    - Surrounding lattice dims to 25% opacity when the error occurs (Attentional Spotlight).
    - Clear distinction between Data Qubits (cyan spheres) and Syndrome Ancillas (amber/indigo diamonds).
    - Stabilizer laser restoration pulse sweeps across plaquette, resolving the parity check.
    - Subtitle: Style B (Restrained Kinetic Word Emphasis with Electric Cyan active word).
    """
    def __init__(self, duration: float = 8.5):
        self.duration = duration
        self.width = CANVAS_WIDTH
        self.height = CANVAS_HEIGHT
        
        # Camera Director: Wide Establishing -> Extreme Macro Dive -> Pullback Resolution
        self.camera = CinematicCameraDirectorV2([
            (0.0, 540.0, 820.0, 1.00),  # Wide establishing
            (2.2, 540.0, 820.0, 1.04),
            (3.8, 480.0, 760.0, 1.85),  # Macro dive centered on failing qubit at (1,1)
            (5.5, 480.0, 760.0, 2.05),  # Stabilizer laser close-up
            (7.2, 540.0, 820.0, 1.15),  # Pullback showing lattice healed
            (8.5, 540.0, 820.0, 1.10),
        ])
        
        self.subtitles = [
            ("When thermal decoherence flips", "decoherence", 0.0, 2.5),
            ("a physical data qubit,", "qubit", 2.5, 4.5),
            ("topological syndrome checks", "syndrome", 4.5, 6.5),
            ("instantly heal the disturbance.", "heal", 6.5, 8.5),
        ]

    def render_frame(self, t: float, with_subtitles: bool = True) -> Image.Image:
        canvas = Image.new("RGBA", (self.width, self.height), (10, 14, 28, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # 1. Background Ambient Radial Glow
        cx, cy = CANVAS_WIDTH // 2, 820
        for r in range(1000, 200, -150):
            alpha = int((1.0 - r / 1000.0) * 28)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(16, 32, 68, alpha))
            
        cam_cx, cam_cy, zoom = self.camera.get_state(t)
        
        # 2. Silicon Wafer Ground Plane (Canvas-Filling, No Box)
        self._draw_silicon_substrate(draw, t, cam_cx, cam_cy, zoom)
        
        # 3. Surface Code Checkerboard Lattice & Dynamics
        self._draw_lattice_dynamics(draw, t, cam_cx, cam_cy, zoom)
        
        # 4. Standardized Editorial Header
        draw_editorial_scene_header(
            draw,
            category="Quantum Stabilizer Dynamics // 02",
            title="SURFACE CODE LATTICE",
            subtitle="Autonomous syndrome measurement & real-time topological healing",
            accent_color=(56, 189, 248)
        )
        
        # 5. Subtitles: Direction B (Restrained Kinetic Word Emphasis)
        if with_subtitles:
            self._draw_subtitles(canvas, t)
            
        return canvas

    def _draw_silicon_substrate(self, draw: ImageDraw.Draw, t: float, cx: float, cy: float, zoom: float):
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))
            
        # Large substrate (900x900 in world space)
        p0 = tf(540 - 450, 820 - 450)
        p1 = tf(540 + 450, 820 + 450)
        
        # Dark silicon die with soft shadow
        draw.rounded_rectangle([p0[0] + 8, p0[1] + 12, p1[0] + 8, p1[1] + 12], radius=24, fill=(0, 0, 0, 95))
        draw.rounded_rectangle([p0[0], p0[1], p1[0], p1[1]], radius=24, fill=(18, 22, 36, 255), outline=(45, 58, 85, 255), width=3)
        
        # Gold wire bonds along perimeter
        for bx in range(540 - 400, 540 + 400, 50):
            t_b0 = tf(bx, 820 - 450)
            t_b1 = tf(bx, 820 - 490)
            draw.line([t_b0[0], t_b0[1], t_b1[0], t_b1[1]], fill=(212, 175, 55, 180), width=2)
            b_b0 = tf(bx, 820 + 450)
            b_b1 = tf(bx, 820 + 490)
            draw.line([b_b0[0], b_b0[1], b_b1[0], b_b1[1]], fill=(212, 175, 55, 180), width=2)

    def _draw_lattice_dynamics(self, draw: ImageDraw.Draw, t: float, cx: float, cy: float, zoom: float):
        def tf(x: float, y: float) -> Tuple[int, int]:
            vx = GRID_CENTER_X + (x - cx) * zoom
            vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
            return (int(vx), int(vy))
            
        grid_n = 4
        spacing = 180.0 # Generous 180px spacing in world space
        start_x = 540.0 - (grid_n - 1) * spacing / 2.0
        start_y = 820.0 - (grid_n - 1) * spacing / 2.0
        
        error_t = 2.6
        heal_t = 5.2
        is_error = (t >= error_t)
        is_healed = (t >= heal_t)
        
        # Attentional Focus Factor: When error occurs, dim background non-error elements to 30%
        focus_dim = 0.35 if (is_error and not is_healed) else 1.0
        
        # 1. Plaquettes (Z-type and X-type stabilizers)
        for r in range(grid_n - 1):
            for c in range(grid_n - 1):
                px0, py0 = start_x + c * spacing, start_y + r * spacing
                px1, py1 = px0 + spacing, py0 + spacing
                
                v0 = tf(px0, py0)
                v1 = tf(px1, py1)
                
                is_target_plaq = (r == 1 and c == 1)
                is_z = ((r + c) % 2 == 0)
                
                if is_target_plaq and is_error and not is_healed:
                    # Pulsing error alarm plaquette
                    pulse = math.sin((t - error_t) * 14) * 0.5 + 0.5
                    fill_c = (239, 68, 68, int(45 + pulse * 65))
                    edge_c = (239, 68, 68, int(160 + pulse * 95))
                elif is_z:
                    fill_c = (56, 189, 248, int(25 * focus_dim))
                    edge_c = (56, 189, 248, int(80 * focus_dim))
                else:
                    fill_c = (129, 140, 248, int(25 * focus_dim))
                    edge_c = (129, 140, 248, int(80 * focus_dim))
                    
                draw.rectangle([v0[0], v0[1], v1[0], v1[1]], fill=fill_c, outline=edge_c, width=2)
                
                # Syndrome Ancilla Diamond
                anc_x = (px0 + px1) / 2.0
                anc_y = (py0 + py1) / 2.0
                av = tf(anc_x, anc_y)
                rad = int(18 * zoom)
                
                if is_target_plaq and is_error and not is_healed:
                    anc_fill = (252, 211, 77, 255)
                    # Ripple wave
                    wave_r = int(((t - error_t) * 120 * zoom) % (spacing * zoom * 1.5))
                    draw.ellipse([av[0] - wave_r, av[1] - wave_r, av[0] + wave_r, av[1] + wave_r], outline=(252, 211, 77, max(0, 210 - wave_r * 2)), width=3)
                else:
                    anc_fill = (129, 140, 248, int(220 * focus_dim))
                    
                draw.polygon([
                    (av[0], av[1] - rad), (av[0] + rad, av[1]),
                    (av[0], av[1] + rad), (av[0] - rad, av[1])
                ], fill=anc_fill)

        # 2. Resonator Coupler Bus Lines
        for r in range(grid_n):
            for c in range(grid_n):
                x = start_x + c * spacing
                y = start_y + r * spacing
                p_cur = tf(x, y)
                if c < grid_n - 1:
                    p_next = tf(x + spacing, y)
                    draw.line([p_cur[0], p_cur[1], p_next[0], p_next[1]], fill=(70, 90, 130, int(150 * focus_dim)), width=max(2, int(3 * zoom)))
                if r < grid_n - 1:
                    p_down = tf(x, y + spacing)
                    draw.line([p_cur[0], p_cur[1], p_down[0], p_down[1]], fill=(70, 90, 130, int(150 * focus_dim)), width=max(2, int(3 * zoom)))

        # 3. Data Qubits (Spheres)
        for r in range(grid_n):
            for c in range(grid_n):
                x = start_x + c * spacing
                y = start_y + r * spacing
                qv = tf(x, y)
                q_rad = int(22 * zoom)
                
                is_error_node = (r == 1 and c == 1)
                
                if is_error_node:
                    if is_error and not is_healed:
                        # Crimson decoherence flare
                        pulse = math.sin((t - error_t) * 16) * 0.5 + 0.5
                        draw.ellipse([qv[0] - q_rad - 12, qv[1] - q_rad - 12, qv[0] + q_rad + 12, qv[1] + q_rad + 12], fill=(239, 68, 68, int(80 + pulse * 140)))
                        draw.ellipse([qv[0] - q_rad, qv[1] - q_rad, qv[0] + q_rad, qv[1] + q_rad], fill=(239, 68, 68, 255), outline=(255, 220, 220, 255), width=3)
                        # Leader Annotation for Error
                        LeaderAnnotation(
                            target_x=qv[0], target_y=qv[1],
                            badge_x=qv[0] + 120, badge_y=qv[1] - 80,
                            title="PHASE-FLIP ERROR",
                            metric="Parity inverted at Node (1,1)",
                            color=(239, 68, 68),
                            align="right"
                        ).draw(draw, opacity=1.0)
                    elif is_healed:
                        # Restored Coherence Burst
                        burst_prog = min(1.0, (t - heal_t) / 1.0)
                        br = int(q_rad + burst_prog * 60)
                        draw.ellipse([qv[0] - br, qv[1] - br, qv[0] + br, qv[1] + br], outline=(56, 189, 248, int(255 * (1.0 - burst_prog))), width=3)
                        draw.ellipse([qv[0] - q_rad, qv[1] - q_rad, qv[0] + q_rad, qv[1] + q_rad], fill=(56, 189, 248, 255), outline=(255, 255, 255, 255), width=3)
                        LeaderAnnotation(
                            target_x=qv[0], target_y=qv[1],
                            badge_x=qv[0] + 120, badge_y=qv[1] - 80,
                            title="STABILIZER RESTORED",
                            metric="Cycle complete in 840 ns",
                            color=(52, 211, 153),
                            align="right"
                        ).draw(draw, opacity=max(0.0, 1.0 - (t - heal_t - 1.2)))
                    else:
                        draw.ellipse([qv[0] - q_rad, qv[1] - q_rad, qv[0] + q_rad, qv[1] + q_rad], fill=(56, 189, 248, 255), outline=(255, 255, 255, 255), width=3)
                else:
                    # Inactive or background data qubit
                    draw.ellipse([qv[0] - q_rad, qv[1] - q_rad, qv[0] + q_rad, qv[1] + q_rad], fill=(56, 189, 248, int(240 * focus_dim)), outline=(210, 245, 255, int(220 * focus_dim)), width=2)

        # 4. Laser Stabilizer Beam ($t \in [4.4, 5.4]$)
        if 4.4 <= t <= 5.4:
            anc_v = tf(start_x + 0.5 * spacing, start_y + 0.5 * spacing)
            node_v = tf(start_x + spacing, start_y + spacing)
            beam_a = int(255 * math.sin((t - 4.4) / 1.0 * math.pi))
            draw.line([anc_v[0], anc_v[1], node_v[0], node_v[1]], fill=(56, 189, 248, beam_a), width=max(4, int(8 * zoom)))
            draw.line([anc_v[0], anc_v[1], node_v[0], node_v[1]], fill=(255, 255, 255, beam_a), width=max(2, int(3 * zoom)))

    def _draw_subtitles(self, canvas: Image.Image, t: float):
        active_chunk = None
        for text, word, t0, t1 in self.subtitles:
            if t0 <= t < t1:
                active_chunk = (text, word)
                break
        if not active_chunk:
            active_chunk = self.subtitles[-1][:2]
            
        text, word = active_chunk
        # Style B: Restrained Kinetic Word Emphasis
        render_subtitle_direction_b(canvas, text, active_word=word, y_center=1460)


# ==============================================================================
# PROTOTYPE C: REAL-WORLD DOCUMENTARY (SEQUENTIAL THREE-ACT RECONSTRUCTION)
# ==============================================================================

class PrototypeCRevised:
    """
    Revised Prototype C: Three-Act Sequential Documentary.
    Solves information crowding by breaking into distinct visual moments:
    - Act 1 (0.0s - 3.2s): Research Publication Reveal. Full-width Nature journal presentation.
    - Act 2 (3.2s - 6.8s): The Historic Scaling Curve. Large 680px blueprint graph with dynamic curve.
    - Act 3 (6.8s - 9.5s): Computational Supremacy Contrast. Frontier (10 septillion yr) vs Willow (<5 min).
    - Subtitle: Style C (Minimal Documentary Captions with soft mint green active word).
    """
    def __init__(self, duration: float = 9.5):
        self.duration = duration
        self.width = CANVAS_WIDTH
        self.height = CANVAS_HEIGHT
        
        self.subtitles = [
            ("Published in Nature, Willow crossed", "Nature", 0.0, 2.5),
            ("the historic error threshold:", "threshold", 2.5, 4.5),
            ("exponentially suppressing noise,", "exponentially", 4.5, 7.0),
            ("finishing in five minutes what takes septillions of years.", "septillions", 7.0, 9.5),
        ]

    def render_frame(self, t: float, with_subtitles: bool = True) -> Image.Image:
        canvas = Image.new("RGBA", (self.width, self.height), (12, 16, 28, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # 1. Background Gradient
        cx = CANVAS_WIDTH // 2
        for r in range(950, 300, -140):
            alpha = int((1.0 - r / 950.0) * 24)
            draw.ellipse([cx - r, 750 - r, cx + r, 750 + r], fill=(20, 36, 75, alpha))
            
        # 2. Standardized Scene Header
        draw_editorial_scene_header(
            draw,
            category="Historic Breakthrough // 03",
            title="BELOW-THRESHOLD SCALING",
            subtitle="Exponential suppression of error rates in quantum memory",
            accent_color=(212, 175, 55)
        )
        
        # 3. Three-Act Sequential Visual Logic
        if t < 3.2:
            # ACT 1: Dedicated Nature Publication Presentation
            self._draw_act1_nature_paper(draw, t)
        elif t < 6.8:
            # ACT 2: Dedicated Large Below-Threshold Scaling Graph
            self._draw_act2_scaling_curve(draw, t)
        else:
            # ACT 3: Dedicated Computational Supremacy Comparison
            self._draw_act3_supremacy_contrast(draw, t)
            
        # 4. Subtitles: Direction C (Minimal Documentary Captions)
        if with_subtitles:
            self._draw_subtitles(canvas, t)
            
        return canvas

    def _draw_act1_nature_paper(self, draw: ImageDraw.Draw, t: float):
        """Act 1: Generous, readable presentation of the Nature paper."""
        card_w = USABLE_WIDTH
        card_h = 680
        x0 = GRID_LEFT
        y0 = 360
        x1 = x0 + card_w
        y1 = y0 + card_h
        
        # Entrance slide-in
        prog = min(1.0, t / 0.8)
        ease = 3 * prog**2 - 2 * prog**3
        curr_y0 = int(y0 + (1.0 - ease) * 120)
        curr_y1 = curr_y0 + card_h
        
        # Card Body (Textured White Journal Page)
        draw.rounded_rectangle([x0 + 8, curr_y0 + 12, x1 + 8, curr_y1 + 12], radius=20, fill=(0, 0, 0, 95))
        draw.rounded_rectangle([x0, curr_y0, x1, curr_y1], radius=20, fill=(248, 247, 244, 255), outline=(220, 218, 210, 255), width=2)
        
        # Nature Masthead Banner
        draw.text((x0 + 48, curr_y0 + 40), "nature", font=FONT_DISPLAY_HERO, fill=(200, 30, 30, 255))
        draw.text((x0 + 290, curr_y0 + 58), "|  VOL 636  |  9 DECEMBER 2024  |  ACCELERATED ARTICLE", font=FONT_MONO_LABEL, fill=(80, 85, 95, 255))
        draw.line([x0 + 48, curr_y0 + 130, x1 - 48, curr_y0 + 130], fill=(215, 210, 200, 255), width=2)
        
        # Paper Title & Authors
        draw.text((x0 + 48, curr_y0 + 160), "Quantum error correction below the", font=FONT_DISPLAY_TITLE, fill=(15, 23, 42, 255))
        draw.text((x0 + 48, curr_y0 + 220), "surface code threshold", font=FONT_DISPLAY_TITLE, fill=(15, 23, 42, 255))
        draw.text((x0 + 48, curr_y0 + 290), "Google Quantum AI Collaborative  *  Published Peer-Reviewed Research", font=FONT_DISPLAY_SUB, fill=(71, 85, 105, 255))
        
        # Milestone Pill Badge inside Card
        draw.rounded_rectangle([x0 + 48, curr_y0 + 380, x0 + 480, curr_y0 + 460], radius=14, fill=(240, 253, 244, 255), outline=(34, 197, 94, 255), width=2)
        draw.text((x0 + 72, curr_y0 + 405), "EXPERIMENTAL MILESTONE ACHIEVED", font=FONT_BADGE_TITLE, fill=(22, 101, 52, 255))
        
        # Summary text
        draw.text((x0 + 48, curr_y0 + 500), "First physical demonstration that increasing qubit count suppresses errors", font=FONT_DISPLAY_SUB, fill=(50, 60, 75, 255))
        draw.text((x0 + 48, curr_y0 + 546), "Physical hardware: 105 superconducting qubits at 10 millikelvin", font=FONT_BADGE_METRIC, fill=(100, 115, 130, 255))

    def _draw_act2_scaling_curve(self, draw: ImageDraw.Draw, t: float):
        """Act 2: Dedicated Large Blueprint Scaling Graph (680px height)."""
        card_w = USABLE_WIDTH
        card_h = 760
        x0 = GRID_LEFT
        y0 = 320
        x1 = x0 + card_w
        y1 = y0 + card_h
        
        # Blueprint Card Background
        draw.rounded_rectangle([x0 + 8, y0 + 12, x1 + 8, y1 + 12], radius=20, fill=(0, 0, 0, 95))
        draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=(16, 24, 40, 255), outline=(45, 60, 90, 255), width=2)
        
        # Graph Header
        draw.text((x0 + 40, y0 + 36), "EMPIRICAL LOGICAL ERROR RATE VS CODE DISTANCE", font=FONT_BADGE_TITLE, fill=(240, 244, 250, 255))
        draw.text((x0 + 40, y0 + 74), "Measured performance across Distance 3, 5, and 7 surface code patches", font=FONT_BADGE_METRIC, fill=(148, 163, 184, 255))
        
        # Plot Axes
        ax_x0 = x0 + 120
        ax_y0 = y1 - 90
        ax_x1 = x1 - 60
        ax_y1 = y0 + 140
        
        draw.line([ax_x0, ax_y0, ax_x1, ax_y0], fill=(100, 115, 140, 255), width=3) # X Axis
        draw.line([ax_x0, ax_y0, ax_x0, ax_y1], fill=(100, 115, 140, 255), width=3) # Y Axis
        
        # Axis Labels
        draw.text((ax_x1 - 220, ax_y0 + 24), "CODE DISTANCE (d)", font=FONT_MONO_LABEL, fill=(148, 163, 184, 255))
        draw.text((x0 + 30, ax_y1 - 10), "LOGICAL ERROR", font=FONT_MONO_LABEL, fill=(148, 163, 184, 255))
        
        # Code distance ticks
        d_ticks = [(ax_x0 + 180, "d = 3"), (ax_x0 + 440, "d = 5"), (ax_x0 + 700, "d = 7")]
        for tx, tlabel in d_ticks:
            draw.line([tx, ax_y0 - 8, tx, ax_y0 + 8], fill=(148, 163, 184, 255), width=2)
            draw.text((tx - 30, ax_y0 + 18), tlabel, font=FONT_DISPLAY_SUB, fill=(240, 244, 250, 255))
            
        # Threshold line
        thresh_y = y0 + 280
        draw.line([ax_x0, thresh_y, ax_x1, thresh_y], fill=(239, 68, 68, 180), width=2)
        draw.text((ax_x1 - 320, thresh_y - 34), "THRESHOLD LIMIT (Lambda = 1.0)", font=FONT_MONO_LABEL, fill=(239, 68, 68, 240))
        
        # Dynamic Curve Drawing (Starts at t=3.4s, completes at t=6.2s)
        curve_prog = max(0.0, min(1.0, (t - 3.4) / 2.8))
        ease = 3 * curve_prog**2 - 2 * curve_prog**3
        
        pts = [
            (ax_x0 + 180, thresh_y + 40),   # d=3
            (ax_x0 + 440, thresh_y + 160),  # d=5
            (ax_x0 + 700, thresh_y + 260),  # d=7
        ]
        
        max_idx = int(ease * (len(pts) - 1))
        frac = (ease * (len(pts) - 1)) - max_idx
        drawn_pts = []
        for i in range(max_idx + 1):
            drawn_pts.append(pts[i])
        if max_idx < len(pts) - 1 and frac > 0.0:
            interp_x = pts[max_idx][0] + (pts[max_idx + 1][0] - pts[max_idx][0]) * frac
            interp_y = pts[max_idx][1] + (pts[max_idx + 1][1] - pts[max_idx][1]) * frac
            drawn_pts.append((interp_x, interp_y))
            
        # Draw glowing curve
        for i in range(len(drawn_pts) - 1):
            p1, p2 = drawn_pts[i], drawn_pts[i + 1]
            draw.line([p1[0], p1[1], p2[0], p2[1]], fill=(56, 189, 248, 120), width=10)
            draw.line([p1[0], p1[1], p2[0], p2[1]], fill=(255, 255, 255, 255), width=4)
            
        if drawn_pts:
            hx, hy = drawn_pts[-1]
            draw.ellipse([hx - 12, hy - 12, hx + 12, hy + 12], fill=(56, 189, 248, 255))
            draw.ellipse([hx - 6, hy - 6, hx + 6, hy + 6], fill=(255, 255, 255, 255))
            
        if curve_prog > 0.8:
            # High-Impact Milestone Callout
            LeaderAnnotation(
                target_x=pts[2][0], target_y=pts[2][1],
                badge_x=pts[2][0] - 260, badge_y=pts[2][1] - 80,
                title="LAMBDA = 2.14",
                metric="Exponential error suppression",
                color=(52, 211, 153),
                align="left"
            ).draw(draw, opacity=1.0)

    def _draw_act3_supremacy_contrast(self, draw: ImageDraw.Draw, t: float):
        """Act 3: Dedicated Computational Supremacy Comparison."""
        card_w = USABLE_WIDTH
        card_h = 760
        x0 = GRID_LEFT
        y0 = 320
        x1 = x0 + card_w
        y1 = y0 + card_h
        
        # Container
        draw.rounded_rectangle([x0 + 8, y0 + 12, x1 + 8, y1 + 12], radius=20, fill=(0, 0, 0, 95))
        draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=(16, 22, 38, 255), outline=(45, 60, 90, 255), width=2)
        
        # Central divider
        mid_x = CANVAS_WIDTH // 2
        draw.line([mid_x, y0 + 30, mid_x, y1 - 30], fill=(45, 60, 90, 255), width=2)
        
        # --- Left Side: Frontier Supercomputer ---
        draw.text((x0 + 40, y0 + 40), "CLASSICAL BENCHMARK", font=FONT_MONO_LABEL, fill=(239, 68, 68, 255))
        draw.text((x0 + 40, y0 + 76), "FRONTIER SUPERCOMPUTER", font=FONT_DISPLAY_TITLE, fill=(240, 244, 250, 255))
        draw.text((x0 + 40, y0 + 130), "Oak Ridge National Laboratory", font=FONT_BADGE_METRIC, fill=(148, 163, 184, 255))
        
        draw.text((x0 + 40, y0 + 220), "TIME REQUIRED:", font=FONT_MONO_LABEL, fill=(148, 163, 184, 220))
        draw.text((x0 + 40, y0 + 260), "10 SEPTILLION", font=FONT_DISPLAY_HERO, fill=(239, 68, 68, 255))
        draw.text((x0 + 40, y0 + 340), "YEARS (10^25 YR)", font=FONT_DISPLAY_TITLE, fill=(239, 68, 68, 220))
        
        draw.text((x0 + 40, y0 + 440), "* Classical runtime exceeds", font=FONT_DISPLAY_SUB, fill=(148, 163, 184, 200))
        draw.text((x0 + 40, y0 + 480), "  the age of the known universe", font=FONT_DISPLAY_SUB, fill=(148, 163, 184, 200))

        # --- Right Side: Google Willow ---
        draw.text((mid_x + 40, y0 + 40), "QUANTUM BENCHMARK", font=FONT_MONO_LABEL, fill=(52, 211, 153, 255))
        draw.text((mid_x + 40, y0 + 76), "GOOGLE WILLOW", font=FONT_DISPLAY_TITLE, fill=(240, 244, 250, 255))
        draw.text((mid_x + 40, y0 + 130), "105-Qubit Quantum Processor", font=FONT_BADGE_METRIC, fill=(148, 163, 184, 255))
        
        draw.text((mid_x + 40, y0 + 220), "TIME REQUIRED:", font=FONT_MONO_LABEL, fill=(148, 163, 184, 220))
        draw.text((mid_x + 40, y0 + 260), "< 5 MINUTES", font=FONT_DISPLAY_HERO, fill=(52, 211, 153, 255))
        draw.text((mid_x + 40, y0 + 340), "(UNDER 300 SECONDS)", font=FONT_DISPLAY_TITLE, fill=(52, 211, 153, 220))
        
        # Kinetic Progress Bar
        bar_w = 380
        bar_prog = min(1.0, (t - 6.8) / 2.0)
        draw.rectangle([mid_x + 40, y0 + 440, mid_x + 40 + bar_w, y0 + 470], fill=(25, 35, 55, 255))
        draw.rectangle([mid_x + 40, y0 + 440, mid_x + 40 + int(bar_w * bar_prog), y0 + 470], fill=(52, 211, 153, 255))
        draw.text((mid_x + 40, y0 + 490), "TASK COMPLETE // VERIFIED", font=FONT_MONO_LABEL, fill=(52, 211, 153, 255))

    def _draw_subtitles(self, canvas: Image.Image, t: float):
        active_chunk = None
        for text, word, t0, t1 in self.subtitles:
            if t0 <= t < t1:
                active_chunk = (text, word)
                break
        if not active_chunk:
            active_chunk = self.subtitles[-1][:2]
            
        text, word = active_chunk
        # Style C: Minimal Documentary Captions
        render_subtitle_direction_c(canvas, text, active_word=word, y_center=1460)


# ==============================================================================
# SUBTITLE COMPARISON RENDERER (ALL 3 DIRECTIONS ON PHASE 9.1 CANVAS)
# ==============================================================================

def render_subtitle_comparison_composite():
    print("\n[SUBTITLES] Rendering 3-Direction Subtitle Comparison Composite...")
    proto_a = PrototypeARevised()
    base_frame = proto_a.render_frame(t=3.8, with_subtitles=False)
    
    # 1. Style A Frame
    f_a = base_frame.copy()
    render_subtitle_direction_a(f_a, "Willow is suspended inside a dilution refrigerator.", active_word="refrigerator", y_center=1450)
    d = ImageDraw.Draw(f_a)
    d.text((GRID_LEFT, 1340), "STYLE A: CLEAN EDITORIAL PHRASE-GROUP CAPTIONS", font=FONT_BADGE_TITLE, fill=(252, 211, 77, 255))
    f_a.save(SUBTITLES_DIR / "style_a_clean_editorial.png")
    
    # 2. Style B Frame
    f_b = base_frame.copy()
    render_subtitle_direction_b(f_b, "Willow is suspended inside a dilution refrigerator.", active_word="refrigerator", y_center=1450)
    d = ImageDraw.Draw(f_b)
    d.text((GRID_LEFT, 1340), "STYLE B: RESTRAINED KINETIC WORD EMPHASIS", font=FONT_BADGE_TITLE, fill=(56, 189, 248, 255))
    f_b.save(SUBTITLES_DIR / "style_b_restrained_kinetic.png")
    
    # 3. Style C Frame
    f_c = base_frame.copy()
    render_subtitle_direction_c(f_c, "Willow is suspended inside a dilution refrigerator.", active_word="refrigerator", y_center=1450)
    d = ImageDraw.Draw(f_c)
    d.text((GRID_LEFT, 1340), "STYLE C: MINIMAL DOCUMENTARY CAPTIONS", font=FONT_BADGE_TITLE, fill=(52, 211, 153, 255))
    f_c.save(SUBTITLES_DIR / "style_c_minimal_documentary.png")
    
    # Composite Sheet
    comp = Image.new("RGBA", (1920, 1080), (10, 14, 24, 255))
    crop_box = (0, 1180, 1080, 1620) # 440px height crop
    
    c1 = f_a.crop(crop_box).resize((580, 240), Image.Resampling.LANCZOS)
    c2 = f_b.crop(crop_box).resize((580, 240), Image.Resampling.LANCZOS)
    c3 = f_c.crop(crop_box).resize((580, 240), Image.Resampling.LANCZOS)
    
    cdraw = ImageDraw.Draw(comp)
    cdraw.text((60, 40), "SUPER.INTELLIGENCEEE // PHASE 9.1 SUBTITLE REDESIGN EVALUATION", font=FONT_BADGE_TITLE, fill=(212, 175, 55, 255))
    cdraw.text((60, 80), "Three Genuinely Different Subtitle Directions (Mobile Safe Zone MarginV >= 440px)", font=FONT_DISPLAY_TITLE, fill=(255, 255, 255, 255))
    
    # Panel 1
    comp.paste(c1, (60, 180))
    cdraw.rectangle([60, 180, 640, 420], outline=(252, 211, 77, 220), width=2)
    cdraw.text((60, 435), "STYLE A: CLEAN EDITORIAL PHRASE-GROUP", font=FONT_BADGE_TITLE, fill=(252, 211, 77, 255))
    cdraw.text((60, 475), "- Zero background box; subtle bottom gradient for universal legibility", font=FONT_DISPLAY_SUB, fill=(180, 190, 205, 255))
    cdraw.text((60, 515), "- Highest documentary authority; perfectly centered phrase balance", font=FONT_DISPLAY_SUB, fill=(180, 190, 205, 255))
    
    # Panel 2
    comp.paste(c2, (680, 180))
    cdraw.rectangle([680, 180, 1260, 420], outline=(56, 189, 248, 220), width=2)
    cdraw.text((680, 435), "STYLE B: RESTRAINED KINETIC WORD EMPHASIS", font=FONT_BADGE_TITLE, fill=(56, 189, 248, 255))
    cdraw.text((680, 475), "- Frosted glass capsule with electric cyan active word and underline", font=FONT_DISPLAY_SUB, fill=(180, 190, 205, 255))
    cdraw.text((680, 515), "- Restrained modern motion; zero chaotic jumping or bouncy pop-in", font=FONT_DISPLAY_SUB, fill=(180, 190, 205, 255))
    
    # Panel 3
    comp.paste(c3, (1300, 180))
    cdraw.rectangle([1300, 180, 1880, 420], outline=(52, 211, 153, 220), width=2)
    cdraw.text((1300, 435), "STYLE C: MINIMAL DOCUMENTARY CAPTIONS", font=FONT_BADGE_TITLE, fill=(52, 211, 153, 255))
    cdraw.text((1300, 475), "- Pure floating typography; active word in soft emerald mint (#34D399)", font=FONT_DISPLAY_SUB, fill=(180, 190, 205, 255))
    cdraw.text((1300, 515), "- Criterion / cleanroom aesthetic; maximum respect for the visual image", font=FONT_DISPLAY_SUB, fill=(180, 190, 205, 255))
    
    comp_path = SUBTITLES_DIR / "subtitle_directions_comparison_v2.png"
    comp.save(comp_path)
    print(f"[SUBTITLES] Saved comparison composite to: {comp_path}")
    return comp_path


# ==============================================================================
# VIDEO RENDERING & 30-FRAME CONTACT SHEET GENERATOR
# ==============================================================================

def render_dual_masters(comp, audio_wav: Path, base_filename: str, fps: float = 30.0) -> Tuple[Path, Path]:
    """
    Renders BOTH:
    1. Clean Archival Master (without subtitles)
    2. Captioned Review Master (with subtitles)
    """
    clean_mp4 = MASTERS_DIR / f"{base_filename}_clean_master.mp4"
    captioned_mp4 = PHASE9_1_DIR / f"{base_filename}.mp4"
    total_frames = int(comp.duration * fps)
    
    print(f"\n[RENDER] Rendering {base_filename} Dual Masters (Duration: {comp.duration:.1f}s @ {fps}fps)...")
    
    # 1. Clean Master
    cmd_clean = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{comp.width}x{comp.height}", "-pix_fmt", "rgba",
        "-r", str(fps), "-i", "-",
        "-i", str(audio_wav),
        "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
        "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(clean_mp4)
    ]
    proc_clean = subprocess.Popen(cmd_clean, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, bufsize=10**7)
    
    # 2. Captioned Master
    cmd_cap = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{comp.width}x{comp.height}", "-pix_fmt", "rgba",
        "-r", str(fps), "-i", "-",
        "-i", str(audio_wav),
        "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
        "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(captioned_mp4)
    ]
    proc_cap = subprocess.Popen(cmd_cap, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, bufsize=10**7)
    
    t0 = time.time()
    try:
        for idx in range(total_frames):
            t = idx / fps
            # Clean frame
            frame_clean = comp.render_frame(t, with_subtitles=False)
            proc_clean.stdin.write(frame_clean.tobytes())
            
            # Captioned frame
            frame_cap = comp.render_frame(t, with_subtitles=True)
            proc_cap.stdin.write(frame_cap.tobytes())
            
            if idx % 60 == 0:
                elapsed = time.time() - t0
                fps_curr = (idx + 1) / max(0.001, elapsed)
                print(f"  Frame {idx}/{total_frames} ({idx/total_frames*100:.1f}%) | {fps_curr:.1f} fps")
                
        proc_clean.stdin.close()
        proc_clean.wait()
        proc_cap.stdin.close()
        proc_cap.wait()
    except Exception as e:
        proc_clean.kill()
        proc_cap.kill()
        raise RuntimeError(f"Rendering failed: {e}")
        
    dur = time.time() - t0
    print(f"[RENDER] Completed {base_filename} in {dur:.1f}s ({total_frames*2/dur:.1f} effective frame encoding fps)")
    return clean_mp4, captioned_mp4


def extract_30frame_contact_sheet(video_mp4: Path, output_sheet: Path) -> None:
    """Extracts 30 frames across the video duration and builds a 5x6 high-resolution contact sheet."""
    num_frames = 30
    cols = 6
    rows = 5
    v_frames_dir = FRAMES_DIR / video_mp4.stem
    v_frames_dir.mkdir(parents=True, exist_ok=True)
    
    temp_pattern = v_frames_dir / "f_%02d.png"
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_mp4),
        "-vf", "fps=30/9.0,scale=320:568", # 9/16 thumbnail
        "-vframes", str(num_frames),
        str(temp_pattern)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    frame_files = sorted(v_frames_dir.glob("f_*.png"))[:num_frames]
    if not frame_files:
        return
        
    tw, th = Image.open(frame_files[0]).size
    pad = 16
    sheet_w = cols * tw + (cols + 1) * pad
    sheet_h = rows * th + (rows + 1) * pad + 70
    
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (10, 14, 24, 255))
    sdraw = ImageDraw.Draw(sheet)
    sdraw.text((pad, 20), f"30-FRAME AUDIT CONTACT SHEET // {video_mp4.name.upper()}", font=FONT_BADGE_TITLE, fill=(212, 175, 55, 255))
    
    for idx, ff in enumerate(frame_files):
        r = idx // cols
        c = idx % cols
        x = pad + c * (tw + pad)
        y = 70 + pad + r * (th + pad)
        im = Image.open(ff)
        sheet.paste(im, (x, y))
        sdraw.rectangle([x, y, x + tw, y + th], outline=(50, 65, 90, 255), width=2)
        sdraw.text((x + 8, y + 8), f"#{idx+1:02d}", font=FONT_MONO_LABEL, fill=(255, 255, 255, 220))
        
    sheet.save(output_sheet)
    print(f"[CONTACT SHEET] Saved 30-frame sheet to: {output_sheet}")


# ==============================================================================
# MAIN PRODUCTION RUNNER
# ==============================================================================

def main():
    guard = ResourceGuard()
    guard.configure_environment()
    
    print("================================================================================")
    print("PHASE 9.1: VISUAL COMPOSITION, SPACING, GRAPHIC QUALITY & EDITORIAL RECONSTRUCTION")
    print("================================================================================")
    
    # 1. Render Subtitle Directions Comparison Composite
    render_subtitle_comparison_composite()
    
    # 2. Prototype A: Physical Technology (Dilution Refrigerator)
    print("\n--------------------------------------------------------------------------------")
    print("[1/3] REVISED PROTOTYPE A: PHYSICAL TECHNOLOGY (DILUTION REFRIGERATOR)")
    print("--------------------------------------------------------------------------------")
    proto_a = PrototypeARevised(duration=9.0)
    audio_a = AUDIO_DIR / "proto_a_master.wav"
    clean_a, cap_a = render_dual_masters(proto_a, audio_a, "prototype_a_physical_technology")
    extract_30frame_contact_sheet(cap_a, PHASE9_1_DIR / "prototype_a_contact_sheet_30frames.png")
    
    # 3. Prototype B: Abstract Concept (Quantum Surface Code Lattice)
    print("\n--------------------------------------------------------------------------------")
    print("[2/3] REVISED PROTOTYPE B: ABSTRACT TECHNICAL CONCEPT (SURFACE CODE)")
    print("--------------------------------------------------------------------------------")
    proto_b = PrototypeBRevised(duration=8.5)
    audio_b = AUDIO_DIR / "proto_b_master.wav"
    clean_b, cap_b = render_dual_masters(proto_b, audio_b, "prototype_b_abstract_concept")
    extract_30frame_contact_sheet(cap_b, PHASE9_1_DIR / "prototype_b_contact_sheet_30frames.png")
    
    # 4. Prototype C: Real-World Documentary (Sequential Three-Act)
    print("\n--------------------------------------------------------------------------------")
    print("[3/3] REVISED PROTOTYPE C: REAL-WORLD DOCUMENTARY (THREE-ACT EDITORIAL)")
    print("--------------------------------------------------------------------------------")
    proto_c = PrototypeCRevised(duration=9.5)
    audio_c = AUDIO_DIR / "proto_c_master.wav"
    clean_c, cap_c = render_dual_masters(proto_c, audio_c, "prototype_c_documentary_reality")
    extract_30frame_contact_sheet(cap_c, PHASE9_1_DIR / "prototype_c_contact_sheet_30frames.png")
    
    # 5. Master 3-Prototype Side-by-Side Comparison Sheet
    print("\n[MASTER SHEET] Assembling Master 3-Prototype Comparison Sheet...")
    master_w, master_h = 1920, 1080
    master_sheet = Image.new("RGBA", (master_w, master_h), (8, 12, 20, 255))
    mdraw = ImageDraw.Draw(master_sheet)
    mdraw.text((60, 30), "SUPER.INTELLIGENCEEE // PHASE 9.1 RECONSTRUCTED VISUAL MASTERWORKS", font=FONT_BADGE_TITLE, fill=(212, 175, 55, 255))
    mdraw.text((60, 68), "Three Production-Grade Prototypes with 1080x1920 Grid Alignment, Dynamic Leader Lines & Cinematic Pacing", font=FONT_DISPLAY_TITLE, fill=(255, 255, 255, 255))
    
    # Render keyframes from each
    fa = proto_a.render_frame(t=4.5, with_subtitles=True).resize((560, 995), Image.Resampling.LANCZOS)
    fb = proto_b.render_frame(t=4.0, with_subtitles=True).resize((560, 995), Image.Resampling.LANCZOS)
    fc = proto_c.render_frame(t=5.2, with_subtitles=True).resize((560, 995), Image.Resampling.LANCZOS)
    
    crop_h = 860
    fa_c = fa.crop((0, 60, 560, 60 + crop_h))
    fb_c = fb.crop((0, 60, 560, 60 + crop_h))
    fc_c = fc.crop((0, 60, 560, 60 + crop_h))
    
    master_sheet.paste(fa_c, (60, 140))
    mdraw.rectangle([60, 140, 620, 140 + crop_h], outline=(212, 175, 55, 220), width=3)
    mdraw.text((75, 155), "PROTOTYPE A: PHYSICAL TECH", font=FONT_BADGE_TITLE, fill=(212, 175, 55, 255))
    
    master_sheet.paste(fb_c, (680, 140))
    mdraw.rectangle([680, 140, 1240, 140 + crop_h], outline=(56, 189, 248, 220), width=3)
    mdraw.text((695, 155), "PROTOTYPE B: ABSTRACT CONCEPT", font=FONT_BADGE_TITLE, fill=(56, 189, 248, 255))
    
    master_sheet.paste(fc_c, (1300, 140))
    mdraw.rectangle([1300, 140, 1860, 140 + crop_h], outline=(52, 211, 153, 220), width=3)
    mdraw.text((1315, 155), "PROTOTYPE C: DOCUMENTARY REALITY", font=FONT_BADGE_TITLE, fill=(52, 211, 153, 255))
    
    master_sheet_path = PHASE9_1_DIR / "phase9_1_master_contact_sheet.png"
    master_sheet.save(master_sheet_path)
    print(f"[MASTER SHEET] Saved to: {master_sheet_path}")
    
    print("\n================================================================================")
    print("PHASE 9.1 PRODUCTION COMPLETED SUCCESSFULLY!")
    print(f"1. Subtitles: {SUBTITLES_DIR / 'subtitle_directions_comparison_v2.png'}")
    print(f"2. Proto A:   {cap_a} & {clean_a}")
    print(f"3. Proto B:   {cap_b} & {clean_b}")
    print(f"4. Proto C:   {cap_c} & {clean_c}")
    print(f"5. Master:    {master_sheet_path}")
    print("================================================================================")

if __name__ == "__main__":
    main()
