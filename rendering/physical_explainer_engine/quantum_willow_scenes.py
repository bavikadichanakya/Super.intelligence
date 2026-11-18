"""
SUPER.INTELLIGENCEEE — Phase 8 Flagship Visual Production
Google Willow: Real-Time Quantum Error Correction
Physical Explainer Scene Compositions

Bespoke physical and spatial visual architectures:
1. Scene 1: The Quantum Fragility Paradox & Cryostat (Obsidian Studio)
2. Scene 2: 2D Surface Code 105-Qubit Checkerboard Lattice (Warm Ivory Studio)
3. Scene 3: Dynamic Syndrome Detection & Real-Time Error Healing (Warm Ivory Studio)
4. Scene 4: The Historic Below-Threshold Scaling Curve (Nature Paper Re-creation)
5. Scene 5: The 10-Septillion-Year Calculation (Willow vs Frontier Supercomputer)
6. Scene 6: Fault-Tolerant Horizon & Seamless Loop (Obsidian Studio)
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

from core.universal_scene_contract import UniversalSceneContract
from creative.visual_intelligence.camera_director import CameraDirector
from rendering.physical_explainer_engine.composition_base_physical import BasePhysicalExplainerComposition


# ==============================================================================
# SCENE 1: CRYOSTAT HOOK (OBSIDIAN STUDIO VOID)
# ==============================================================================
class Scene1CryostatHookComposition(BasePhysicalExplainerComposition):
    """
    Scene 1: The Quantum Fragility Paradox & Cryostat.
    High-contrast dark obsidian canvas with golden dilution refrigerator chandelier
    descending into 10 mK cryogenic void.
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.bg_color = (10, 13, 20)          # #0A0D14
        self.text_primary = (255, 255, 255)   # Crisp white
        self.text_secondary = (148, 163, 184) # Muted slate #94A3B8
        self.accent_gold = (234, 179, 8)      # #EAB308
        self.accent_cyan = (56, 189, 248)     # #38BDF8

    def render_frame(self, t: float) -> Image.Image:
        canvas = Image.new("RGBA", (self.width, self.height), self.bg_color + (255,))
        draw = ImageDraw.Draw(canvas, "RGBA")

        # 1. Cryogenic Cold Gradient Lighting (10 mK ambient glow at bottom)
        cx, cy = self.width // 2, self.height - 200
        for r in range(800, 200, -100):
            alpha = int((1.0 - r / 800.0) * 28)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(14, 116, 144, alpha))

        # 2. Golden Dilution Refrigerator Chandelier
        self._render_cryostat_chandelier(draw, t)

        # 3. Delicate Thermal / Quantum Wave Noise
        self._render_quantum_noise_waves(draw, t)

        # 4. Editorial Typography & Cold Readout
        self._render_editorial_header(draw, t)

        return canvas

    def _render_cryostat_chandelier(self, draw: ImageDraw.Draw, t: float):
        progress = min(1.0, t / 2.5)
        ease = 3 * progress**2 - 2 * progress**3
        drop_y = int(-180 + ease * 260)  # Descends into frame
        cx = self.width // 2

        # Draw 4 Golden Thermal Stages (Plates from top to bottom: 50K, 4K, 100mK, 10mK)
        stages = [
            (560, 32, drop_y + 380, "50K STAGE"),
            (460, 28, drop_y + 540, "4K STAGE"),
            (360, 24, drop_y + 700, "100 mK STAGE"),
            (260, 20, drop_y + 860, "10 mK COLD FINGER"),
        ]

        # Draw Helical Superconducting Cables between stages
        for i in range(len(stages) - 1):
            y_top = stages[i][2] + stages[i][1]
            y_bot = stages[i + 1][2]
            w_top = stages[i][0]
            w_bot = stages[i + 1][0]
            for strand in [-0.35, -0.15, 0.0, 0.15, 0.35]:
                x1 = int(cx + w_top * strand)
                x2 = int(cx + w_bot * strand)
                draw.line([(x1, y_top), (x2, y_bot)], fill=(217, 119, 6, 200), width=4)

        # Draw Gilded Golden Plates with Specular Highlights
        for w, h, y, label in stages:
            rx = cx - w // 2
            # Plate shadow
            draw.rounded_rectangle([rx - 6, y + 4, rx + w + 6, y + h + 8], radius=8, fill=(0, 0, 0, 120))
            # Golden base plate
            draw.rounded_rectangle([rx, y, rx + w, y + h], radius=6, fill=(202, 138, 4))
            # Top specular gold edge
            draw.line([(rx + 4, y + 2), (rx + w - 4, y + 2)], fill=(254, 240, 138, 220), width=3)
            # Stage micro-label
            draw.text((cx - 50, y + 4), label, fill=(15, 23, 42), font=self.font_mono)

        # The Willow Quantum Chip at the base of the Cold Finger (Y ~ drop_y + 940)
        chip_y = drop_y + 920
        chip_w, chip_h = 160, 160
        chip_rx = cx - chip_w // 2

        # Glowing quantum chip core
        glow_pulse = int(25 + 15 * math.sin(t * 3.5))
        draw.ellipse([cx - 140, chip_y - 40, cx + 140, chip_y + 200], fill=(56, 189, 248, glow_pulse))

        # Chip package
        draw.rounded_rectangle([chip_rx, chip_y, chip_rx + chip_w, chip_y + chip_h], radius=12, fill=(15, 23, 42))
        draw.rounded_rectangle([chip_rx, chip_y, chip_rx + chip_w, chip_y + chip_h], radius=12, outline=self.accent_gold, width=3)
        # Gold wire bonds
        for offset in [-50, -25, 0, 25, 50]:
            draw.line([(cx + offset, chip_y), (cx + offset * 1.3, chip_y - 30)], fill=self.accent_gold, width=2)
            draw.line([(cx + offset, chip_y + chip_h), (cx + offset * 1.3, chip_y + chip_h + 30)], fill=self.accent_gold, width=2)

        # Silicon Die center
        draw.rectangle([cx - 45, chip_y + 35, cx + 45, chip_y + 125], fill=(30, 41, 59))
        draw.text((cx - 36, chip_y + 68), "WILLOW", fill=self.accent_cyan, font=self.font_mono_bold)

    def _render_quantum_noise_waves(self, draw: ImageDraw.Draw, t: float):
        """Draws subtle quantum interference ripples around the chip."""
        cx, cy = self.width // 2, 1280
        for wave_idx in range(4):
            radius = int(120 + wave_idx * 70 + (t * 40) % 70)
            alpha = max(0, int(40 - (radius - 120) * 0.15))
            draw.ellipse([cx - radius, cy - radius // 2, cx + radius, cy + radius // 2], outline=(56, 189, 248, alpha), width=2)

    def _render_editorial_header(self, draw: ImageDraw.Draw, t: float):
        top_y = 150
        left_x = 90

        # Category Chip
        draw.rounded_rectangle([left_x, top_y, left_x + 380, top_y + 44], radius=22, fill=(30, 41, 59))
        draw.text((left_x + 18, top_y + 8), "QUANTUM HARDWARE MILESTONE", fill=self.accent_cyan, font=self.font_mono_bold)

        # Hero Title (80pt)
        draw.text((left_x, top_y + 64), "THE FRAGILITY", fill=self.text_primary, font=self.font_hero)
        draw.text((left_x, top_y + 154), "PARADOX", fill=self.accent_gold, font=self.font_hero)

        # Subtitle
        draw.text((left_x, top_y + 260), "Adding more qubits made them exponentially more fragile.", fill=self.text_secondary, font=self.font_subtitle)

        # Cryogenic Metric Badge (Y=1440)
        card_y = 1440
        draw.rounded_rectangle([90, card_y, self.width - 90, card_y + 90], radius=16, fill=(15, 23, 42, 230), outline=(51, 65, 85), width=2)
        draw.text((120, card_y + 18), "10 mK (-273.14°C)", fill=self.accent_cyan, font=self.font_title)
        draw.text((120, card_y + 58), "Near absolute zero — required to preserve quantum coherence", fill=self.text_secondary, font=self.font_label)


# ==============================================================================
# SCENE 2: 2D SURFACE CODE LATTICE (WARM IVORY STUDIO)
# ==============================================================================
class Scene2SurfaceCodeLatticeComposition(BasePhysicalExplainerComposition):
    """
    Scene 2: 2D Surface Code 105-Qubit Checkerboard Lattice.
    Warm ivory studio floor (#F5F3ED).
    2.5D dimensional silicon quantum chip reveals the 105 physical qubit checkerboard grid:
    Data Qubits (Cobalt Blue Spheres) + Syndrome Sentinels (Emerald Green Diamonds).
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.headline = "THE SURFACE CODE"
        self.subheadline = "105 Physical Superconducting Transmon Qubits"
        self.accent_data = (37, 99, 235)      # Cobalt Blue #2563EB
        self.accent_syndrome = (5, 150, 105)  # Emerald Green #059669

    def render_physical_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        progress = min(1.0, t / 2.0)
        ease = 3 * progress**2 - 2 * progress**3

        cx = self.width // 2
        cy = 880

        # 1. 2.5D Silicon Die Base Carrier with Soft Contact Shadow
        chip_w, chip_h = 860, 860
        rx = cx - chip_w // 2
        ry = cy - chip_h // 2

        # Multi-layer ground contact shadow
        self.draw_contact_shadow(draw, rx + 20, ry + 30, chip_w - 40, chip_h - 40, blur_steps=10)

        # Dimensional Silicon Die (Dark Slate #1E293B with Bevel)
        draw.rounded_rectangle([rx, ry + 16, rx + chip_w, ry + chip_h + 16], radius=24, fill=(30, 41, 59))  # Depth extrusion
        draw.rounded_rectangle([rx, ry, rx + chip_w, ry + chip_h], radius=24, fill=(15, 23, 42))             # Top face
        draw.rounded_rectangle([rx, ry, rx + chip_w, ry + chip_h], radius=24, outline=(71, 85, 105), width=3)

        # Gold perimeter bond pads
        for i in range(12):
            px = rx + 60 + i * 62
            draw.rectangle([px, ry + 12, px + 36, ry + 32], fill=(217, 119, 6))
            draw.rectangle([px, ry + chip_h - 32, px + 36, ry + chip_h - 12], fill=(217, 119, 6))

        # 2. 7x7 Checkerboard Qubit Lattice Grid (Total 49 visible central qubits of the 105 array)
        grid_dim = 7
        cell_size = 94
        grid_start_x = cx - (grid_dim - 1) * cell_size // 2
        grid_start_y = cy - (grid_dim - 1) * cell_size // 2 + 10

        # Draw Coupler Resonator Waveguides (thin silver interconnect lines)
        for row in range(grid_dim):
            for col in range(grid_dim):
                qx = grid_start_x + col * cell_size
                qy = grid_start_y + row * cell_size
                if col < grid_dim - 1:
                    draw.line([(qx, qy), (qx + cell_size, qy)], fill=(71, 85, 105, 180), width=3)
                if row < grid_dim - 1:
                    draw.line([(qx, qy), (qx, qy + cell_size)], fill=(71, 85, 105, 180), width=3)

        # Draw Qubit Nodes (Alternating: Data Qubits = Circle, Syndrome Qubits = Diamond)
        for row in range(grid_dim):
            for col in range(grid_dim):
                qx = grid_start_x + col * cell_size
                qy = grid_start_y + row * cell_size
                node_idx = row * grid_dim + col

                # Staggered pop-in animation
                node_delay = (row + col) * 0.05
                node_prog = max(0.0, min(1.0, (t - node_delay) / 0.5))
                if node_prog <= 0:
                    continue

                node_ease = 1 + 2.70158 * (node_prog - 1)**3 + 1.70158 * (node_prog - 1)**2
                rad = int(18 * max(0.0, node_ease))

                is_data = (row + col) % 2 == 0
                if is_data:
                    # Data Qubit: Cobalt Blue Sphere
                    draw.ellipse([qx - rad, qy - rad, qx + rad, qy + rad], fill=self.accent_data)
                    # Specular highlight
                    draw.ellipse([qx - rad // 2, qy - rad // 2, qx, qy], fill=(147, 197, 253, 220))
                else:
                    # Syndrome Measurement Sentinel: Emerald Diamond
                    pts = [(qx, qy - rad), (qx + rad, qy), (qx, qy + rad), (qx - rad, qy)]
                    draw.polygon(pts, fill=self.accent_syndrome)
                    # Core highlight
                    inner = rad // 2
                    draw.polygon([(qx, qy - inner), (qx + inner, qy), (qx, qy + inner), (qx - inner, qy)], fill=(167, 243, 208, 220))

        # 3. Legend & Architecture Callout Card (Bottom safe zone Y=1380)
        card_y = 1380
        draw.rounded_rectangle([90, card_y, self.width - 90, card_y + 110], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        # Data Qubit key
        draw.ellipse([130, card_y + 35, 160, card_y + 65], fill=self.accent_data)
        draw.text((175, card_y + 36), "DATA QUBITS: Hold Superposition State", fill=self.text_primary, font=self.font_label)
        # Syndrome Qubit key
        pts_key = [(580, card_y + 35), (595, card_y + 50), (580, card_y + 65), (565, card_y + 50)]
        draw.polygon(pts_key, fill=self.accent_syndrome)
        draw.text((615, card_y + 36), "SYNDROME SENTINELS: Check Parity", fill=self.text_primary, font=self.font_label)


# ==============================================================================
# SCENE 3: REAL-TIME ERROR HEALING (WARM IVORY STUDIO)
# ==============================================================================
class Scene3ErrorHealingPlaquetteComposition(BasePhysicalExplainerComposition):
    """
    Scene 3: Dynamic Syndrome Detection & Real-Time Error Healing.
    Warm ivory studio floor.
    Demonstrates a cosmic ray / thermal bit-flip on a data qubit (turns crimson),
    triggering laser stabilizer plaquette checks, correcting the error in < 1 microsecond!
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.headline = "REAL-TIME SYNDROME HEALING"
        self.subheadline = "Detecting Errors Without Collapsing Quantum States"
        self.accent_data = (37, 99, 235)
        self.accent_syndrome = (5, 150, 105)
        self.accent_error = (239, 68, 68)     # Crimson Red #EF4444

    def render_physical_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        cx = self.width // 2
        cy = 880

        # Studio Ground Shadow
        self.draw_contact_shadow(draw, cx - 440, cy - 380, 880, 760, blur_steps=8)

        # Main 2.5D Carrier Card
        draw.rounded_rectangle([cx - 440, cy - 370, cx + 440, cy + 390], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

        # 3x3 Zoomed Plaquette Layout (Center is Target Data Qubit)
        scale = 190
        coords = [
            (-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1)
        ]

        # Determine Error Lifecycle:
        # Phase 1: t in [0.0, 2.2] -> Stable Quantum State (Coherent Blue)
        # Phase 2: t in [2.2, 5.0] -> Cosmic Ray Hit! Bit-flip Error (Red Alert + Laser Links)
        # Phase 3: t in [5.0, end] -> Real-Time Correction Applied! State Restored!
        has_error = (2.2 <= t < 5.2)
        is_healed = (t >= 5.2)

        # Draw Plaquette Shaded Stabilizer Tiles (X-plaquette and Z-plaquette)
        if has_error:
            # Active Syndrome Stabilizer Glow (Yellow/Amber Parity Alert)
            glow_alpha = int(45 + 25 * math.sin(t * 8.0))
            draw.polygon([
                (cx, cy - scale), (cx + scale, cy), (cx, cy + scale), (cx - scale, cy)
            ], fill=(245, 158, 11, glow_alpha), outline=(217, 119, 6, 180))

            # Laser Stabilizer Detection Links
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                draw.line([(cx, cy), (cx + dx * scale, cy + dy * scale)], fill=(239, 68, 68, 220), width=5)

        # Draw Superconducting Resonator Interconnects
        for x_idx, y_idx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            draw.line([(cx, cy), (cx + x_idx * scale, cy + y_idx * scale)], fill=(148, 163, 184), width=4)

        # Draw Surrounding Sentinels & Data Qubits
        for dx, dy in coords:
            qx = cx + dx * scale
            qy = cy + dy * scale
            is_center = (dx == 0 and dy == 0)
            is_syndrome = (abs(dx) + abs(dy)) % 2 == 1

            if is_center:
                # The Target Data Qubit
                if has_error:
                    # Crimson Error State (Bit-Flip X Error)
                    rad = 34
                    draw.ellipse([qx - rad, qy - rad, qx + rad, qy + rad], fill=self.accent_error)
                    draw.ellipse([qx - 14, qy - 14, qx + 14, qy + 14], fill=(254, 202, 202))
                    draw.text((qx - 40, qy + 45), "BIT-FLIP (X)", fill=self.accent_error, font=self.font_mono_bold)
                elif is_healed:
                    # Restored Coherent State with Emerald Healing Halo
                    rad = 32
                    draw.ellipse([qx - 48, qy - 48, qx + 48, qy + 48], outline=(16, 185, 129, 200), width=4)
                    draw.ellipse([qx - rad, qy - rad, qx + rad, qy + rad], fill=self.accent_data)
                    draw.text((qx - 36, qy + 45), "RESTORED", fill=(16, 185, 129), font=self.font_mono_bold)
                else:
                    rad = 30
                    draw.ellipse([qx - rad, qy - rad, qx + rad, qy + rad], fill=self.accent_data)
                    draw.text((qx - 32, qy + 45), "DATA |ψ⟩", fill=self.text_secondary, font=self.font_mono)
            elif is_syndrome:
                # Syndrome Measurement Sentinel (Diamond)
                rad = 28
                pts = [(qx, qy - rad), (qx + rad, qy), (qx, qy + rad), (qx - rad, qy)]
                draw.polygon(pts, fill=self.accent_syndrome)
                draw.text((qx - 20, qy + 36), "SENTINEL", fill=self.text_secondary, font=self.font_mono)
            else:
                # Other Data Qubits
                rad = 24
                draw.ellipse([qx - rad, qy - rad, qx + rad, qy + rad], fill=self.accent_data)

        # Real-Time Mathematical Status Banner (Bottom Y=1380)
        card_y = 1380
        draw.rounded_rectangle([90, card_y, self.width - 90, card_y + 110], radius=16, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
        if has_error:
            draw.text((120, card_y + 20), "ALERT: Parity Eigenvalue Flipped from +1 to -1", fill=(248, 113, 113), font=self.font_title)
            draw.text((120, card_y + 64), "Syndrome Sentinels isolate error location without measuring |ψ⟩", fill=(203, 213, 225), font=self.font_label)
        elif is_healed:
            draw.text((120, card_y + 20), "CORRECTION COMPLETE: < 1 µs Correction Time", fill=(52, 211, 153), font=self.font_title)
            draw.text((120, card_y + 64), "Quantum superposition preserved continuously without collapse", fill=(203, 213, 225), font=self.font_label)
        else:
            draw.text((120, card_y + 20), "CONTINUOUS SURFACE CODE MONITORING", fill=(56, 189, 248), font=self.font_title)
            draw.text((120, card_y + 64), "Non-destructive entanglement measurements cycling at 1 MHz", fill=(203, 213, 225), font=self.font_label)


# ==============================================================================
# SCENE 4: BELOW-THRESHOLD SCALING CURVE (NATURE PAPER RE-CREATION)
# ==============================================================================
class Scene4BelowThresholdCurveComposition(BasePhysicalExplainerComposition):
    """
    Scene 4: The Historic Below-Threshold Scaling Curve.
    Authentic physical re-creation of Google Quantum AI's Nature Dec 2024 paper:
    'Quantum error correction below the surface code threshold'.
    Animates the historic empirical plot showing error dropping exponentially as code distance d increases!
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.headline = "CROSSING THE THRESHOLD"
        self.subheadline = "First Experimental Proof: Larger Distance = Lower Error"

    def render_physical_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        cx = self.width // 2
        cy = 900

        # Studio Ground Shadow
        self.draw_contact_shadow(draw, cx - 440, cy - 400, 880, 800, blur_steps=10)

        # 1. 2.5D Nature Research Paper Card
        card_w, card_h = 880, 800
        rx = cx - card_w // 2
        ry = cy - card_h // 2
        draw.rounded_rectangle([rx, ry + 12, rx + card_w, ry + card_h + 12], radius=20, fill=(212, 208, 197))
        draw.rounded_rectangle([rx, ry, rx + card_w, ry + card_h], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

        # Paper Header: Nature Stamp & Article Meta
        draw.text((rx + 48, ry + 36), "nature", fill=(194, 65, 12), font=self.font_hero)
        draw.text((rx + 290, ry + 56), "| ARTICLE | PUBLISHED 11 DECEMBER 2024", fill=(100, 116, 139), font=self.font_mono)

        paper_title = "Quantum error correction below the surface code threshold"
        draw.text((rx + 48, ry + 130), paper_title, fill=self.text_primary, font=self.font_title)
        draw.text((rx + 48, ry + 185), "Google Quantum AI & Collaborators (Nature Vol 636)", fill=(71, 85, 105), font=self.font_label)

        draw.line([(rx + 48, ry + 225), (rx + card_w - 48, ry + 225)], fill=(226, 232, 240), width=2)

        # 2. Historic Empirical Scaling Graph (Y: Logical Error Rate, X: Code Distance d=3, d=5, d=7)
        graph_x = rx + 140
        graph_y = ry + 280
        gw = 620
        gh = 360

        # Axes
        draw.line([(graph_x, graph_y), (graph_x, graph_y + gh)], fill=(15, 23, 42), width=3)
        draw.line([(graph_x, graph_y + gh), (graph_x + gw, graph_y + gh)], fill=(15, 23, 42), width=3)

        # Y-Axis Labels (Log scale: 10^-2, 10^-3, 10^-4)
        draw.text((graph_x - 90, graph_y + 20), "10⁻²", fill=(71, 85, 105), font=self.font_mono_bold)
        draw.text((graph_x - 90, graph_y + 160), "10⁻³", fill=(71, 85, 105), font=self.font_mono_bold)
        draw.text((graph_x - 90, graph_y + 300), "10⁻⁴", fill=(71, 85, 105), font=self.font_mono_bold)

        # The Red Dashed "Break-Even Threshold" Line (Horizontal at Y=100)
        thresh_y = graph_y + 100
        for x_step in range(graph_x, graph_x + gw, 24):
            draw.line([(x_step, thresh_y), (x_step + 14, thresh_y)], fill=(239, 68, 68), width=3)
        draw.text((graph_x + gw - 220, thresh_y - 28), "THRESHOLD (Λ = 1.0)", fill=(239, 68, 68), font=self.font_mono_bold)

        # The Historic Willow Experimental Data Points (d=3, d=5, d=7)
        points = [
            (graph_x + 100, graph_y + 130, "d = 3", "1.5 × 10⁻³"),
            (graph_x + 310, graph_y + 220, "d = 5", "8.2 × 10⁻⁴"),
            (graph_x + 520, graph_y + 320, "d = 7", "4.1 × 10⁻⁴"),
        ]

        # Draw animated green trend curve
        anim_progress = min(1.0, max(0.0, (t - 1.0) / 2.5))
        curve_pts = []
        for i, (px, py, lbl, val) in enumerate(points):
            draw.text((px - 30, graph_y + gh + 14), lbl, fill=self.text_primary, font=self.font_title)
            if anim_progress >= (i + 1) / 3.0:
                curve_pts.append((px, py))
                # Data Point Marker
                draw.ellipse([px - 14, py - 14, px + 14, py + 14], fill=(5, 150, 105))
                draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(255, 255, 255))
                draw.text((px - 45, py - 38), val, fill=(5, 150, 105), font=self.font_mono_bold)

        if len(curve_pts) > 1:
            draw.line(curve_pts, fill=(5, 150, 105), width=6)

        # Summary Badge (Bottom Y=1400)
        card_y = 1400
        draw.rounded_rectangle([90, card_y, self.width - 90, card_y + 100], radius=16, fill=(240, 253, 244), outline=(187, 247, 208), width=2)
        draw.text((120, card_y + 16), "SUPPRESSION FACTOR Λ = 1.14 ± 0.02", fill=(21, 128, 61), font=self.font_title)
        draw.text((120, card_y + 58), "Each code distance expansion halves the logical error rate.", fill=(22, 101, 52), font=self.font_label)


# ==============================================================================
# SCENE 5: SEPTILLION-YEAR CALCULATION (WILLOW VS FRONTIER)
# ==============================================================================
class Scene5SupercomputerComparisonComposition(BasePhysicalExplainerComposition):
    """
    Scene 5: The 10-Septillion-Year Calculation (Willow vs Frontier Supercomputer).
    Dual-column architectural comparison:
    Left: Frontier Supercomputer (10^25 years to simulate).
    Right: Willow Quantum Chip (solved in 5 minutes / 300 seconds).
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.headline = "BENCHMARK PERFORMANCE"
        self.subheadline = "Random Circuit Sampling: Quantum vs World's #1 Supercomputer"

    def render_physical_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        cx = self.width // 2
        cy = 900
        col_w = 420
        col_h = 740

        left_x = 90
        right_x = cx + 30

        # Ground Shadows
        self.draw_contact_shadow(draw, left_x, cy - col_h // 2, col_w, col_h, blur_steps=8)
        self.draw_contact_shadow(draw, right_x, cy - col_h // 2, col_w, col_h, blur_steps=8)

        # ----------------------------------------------------------------------
        # LEFT COLUMN: FRONTIER SUPERCOMPUTER (Oak Ridge National Lab)
        # ----------------------------------------------------------------------
        ly = cy - col_h // 2
        draw.rounded_rectangle([left_x, ly + 10, left_x + col_w, ly + col_h + 10], radius=20, fill=(212, 208, 197))
        draw.rounded_rectangle([left_x, ly, left_x + col_w, ly + col_h], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

        draw.text((left_x + 32, ly + 36), "FRONTIER", fill=(220, 38, 38), font=self.font_title)
        draw.text((left_x + 32, ly + 92), "World's #1 Supercomputer", fill=(100, 116, 139), font=self.font_label)

        # Supercomputer visual: 4 stacked server blade bays
        for i in range(4):
            by = ly + 140 + i * 85
            draw.rounded_rectangle([left_x + 32, by, left_x + col_w - 32, by + 70], radius=8, fill=(30, 41, 59))
            # Blinking LED indicators
            for led in range(6):
                draw.ellipse([left_x + 50 + led * 28, by + 28, left_x + 62 + led * 28, by + 40], fill=(239, 68, 68))
            draw.text((left_x + 240, by + 26), "9,472 CPUS", fill=(148, 163, 184), font=self.font_mono)

        # Astronomical Time Card
        time_y = ly + 500
        draw.rounded_rectangle([left_x + 24, time_y, left_x + col_w - 24, time_y + 190], radius=14, fill=(254, 242, 242), outline=(254, 202, 202), width=2)
        draw.text((left_x + 38, time_y + 18), "REQUIRED TIME:", fill=(185, 28, 28), font=self.font_label)
        draw.text((left_x + 38, time_y + 54), "10²⁵ YEARS", fill=(220, 38, 38), font=self.font_hero)
        draw.text((left_x + 38, time_y + 142), "10 Septillion Years (Exceeds Universe Age)", fill=(153, 27, 27), font=self.font_mono)

        # ----------------------------------------------------------------------
        # RIGHT COLUMN: GOOGLE WILLOW QUANTUM PROCESSOR
        # ----------------------------------------------------------------------
        ry = cy - col_h // 2
        draw.rounded_rectangle([right_x, ry + 10, right_x + col_w, ry + col_h + 10], radius=20, fill=(212, 208, 197))
        draw.rounded_rectangle([right_x, ry, right_x + col_w, ry + col_h], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

        draw.text((right_x + 32, ry + 36), "WILLOW", fill=(5, 150, 105), font=self.font_title)
        draw.text((right_x + 32, ry + 92), "105-Qubit Quantum Processor", fill=(100, 116, 139), font=self.font_label)

        # Willow Chip Visual: Central Silicon Die in Cryo Mount
        die_cy = ry + 290
        glow_pulse = int(35 + 20 * math.sin(t * 4.0))
        draw.ellipse([right_x + col_w // 2 - 120, die_cy - 120, right_x + col_w // 2 + 120, die_cy + 120], fill=(16, 185, 129, glow_pulse))

        draw.rounded_rectangle([right_x + col_w // 2 - 90, die_cy - 90, right_x + col_w // 2 + 90, die_cy + 90], radius=16, fill=(15, 23, 42), outline=(5, 150, 105), width=3)
        draw.text((right_x + col_w // 2 - 58, die_cy - 16), "105 QUBITS", fill=(52, 211, 153), font=self.font_mono_bold)

        # Willow Measured Time Card
        time_y = ry + 500
        draw.rounded_rectangle([right_x + 24, time_y, right_x + col_w - 24, time_y + 190], radius=14, fill=(240, 253, 244), outline=(187, 247, 208), width=2)
        draw.text((right_x + 38, time_y + 18), "MEASURED TIME:", fill=(21, 128, 61), font=self.font_label)
        draw.text((right_x + 38, time_y + 54), "< 5 MINS", fill=(5, 150, 105), font=self.font_hero)
        draw.text((right_x + 38, time_y + 142), "Exact Random Circuit Sampling", fill=(22, 101, 52), font=self.font_mono)


# ==============================================================================
# SCENE 6: FAULT-TOLERANT HORIZON LOOP (OBSIDIAN STUDIO VOID)
# ==============================================================================
class Scene6LoopConclusionComposition(BasePhysicalExplainerComposition):
    """
    Scene 6: Fault-Tolerant Horizon & Seamless Loop Outro.
    Obsidian studio void (#0A0D14), matching Scene 1 to create an infinite loop.
    The golden quantum monolith glows with fault-tolerant coherence.
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.bg_color = (10, 13, 20)
        self.text_primary = (255, 255, 255)
        self.text_secondary = (148, 163, 184)
        self.accent_gold = (234, 179, 8)
        self.accent_emerald = (16, 185, 129)

    def render_frame(self, t: float) -> Image.Image:
        canvas = Image.new("RGBA", (self.width, self.height), self.bg_color + (255,))
        draw = ImageDraw.Draw(canvas, "RGBA")

        cx = self.width // 2
        cy = self.height // 2

        # 1. Radiant Ambient Quantum Core Bloom
        pulse = 0.5 + 0.5 * math.sin(t * 3.0)
        for r in range(650, 150, -80):
            alpha = int((1.0 - r / 650.0) * (30 + pulse * 20))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(16, 185, 129, alpha))

        # 2. Central Fault-Tolerant Logical Qubit Hexagon Monolith
        rad = 220
        pts = []
        for i in range(6):
            angle = math.radians(60 * i + t * 15)
            pts.append((cx + int(rad * math.cos(angle)), cy + int(rad * math.sin(angle))))

        draw.polygon(pts, fill=(15, 23, 42))
        draw.polygon(pts, outline=self.accent_gold, width=4)

        # Inner Glowing Core
        draw.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], fill=(5, 150, 105, 220))
        draw.text((cx - 68, cy - 16), "|LOGICAL ψ⟩", fill=(255, 255, 255), font=self.font_mono_bold)

        # 3. Editorial Typography (Closing Hook & Loop)
        top_y = 180
        draw.text((cx - 280, top_y), "THE ERA OF SELF-HEALING", fill=self.text_primary, font=self.font_title)
        draw.text((cx - 160, top_y + 70), "QUBITS HAS BEGUN", fill=self.accent_gold, font=self.font_title)

        bot_y = 1420
        draw.text((cx - 320, bot_y), "Unlocking practical materials science, chemistry, and AI.", fill=self.text_secondary, font=self.font_subtitle)

        return canvas
