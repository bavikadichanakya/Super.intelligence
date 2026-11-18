"""
SUPER.INTELLIGENCEEE — AI Model Architecture Compositions
Implements full-bleed 1080x1920 explanatory visualizations for AI reasoning models,
chain-of-thought expansion, pure RL self-correction, and test-time compute scaling.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple
from PIL import Image, ImageDraw

from core.universal_scene_contract import UniversalSceneContract
from creative.visual_intelligence.motion_director import MotionDirector
from rendering.visual_intelligence_engine.composition_base import BaseVisualIntelligenceComposition


class ReasoningChainExpansionComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes deep reasoning LLMs (e.g. DeepSeek-R1) generating a branching
    tree of thought tokens, exploring alternative proofs and self-reflecting.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # Draw root prompt node
        root_y = center_y - 420
        draw.rounded_rectangle(
            [center_x - 140, root_y - 40, center_x + 140, root_y + 40],
            radius=12,
            fill=(15, 23, 42, 220),
            outline=(56, 189, 248),
            width=2,
        )
        draw.text((center_x - 110, root_y - 14), "COMPLEX MATH PROMPT", fill=(241, 245, 249), font=self.font_sans_head)

        # 3 Branching Levels with Dynamic Expansion
        levels = [
            # Level 1: 3 initial exploration paths
            {"y": root_y + 180, "nodes": [(-240, "Hypothesis A"), (0, "Hypothesis B"), (240, "Hypothesis C")]},
            # Level 2: 5 step deduction paths
            {"y": root_y + 360, "nodes": [(-320, "Step 1.1"), (-120, "Step 1.2 [Backtrack]"), (80, "Step 2.1"), (240, "Step 3.1"), (380, "Step 3.2")]},
            # Level 3: Converging proof tokens
            {"y": root_y + 560, "nodes": [(-300, "Branch Verified"), (120, "Optimal Path [Q.E.D.]"), (320, "Discarded")]},
        ]

        # Connective conduits with animated flow pulses
        pulse_phase = (t * 2.5) % 1.0

        for l_idx, level in enumerate(levels):
            parent_y = root_y if l_idx == 0 else levels[l_idx - 1]["y"]
            parent_nodes = [(0, "")] if l_idx == 0 else levels[l_idx - 1]["nodes"]

            for n_x, label in level["nodes"]:
                actual_nx = center_x + n_x * scale
                actual_ny = level["y"] * scale

                # Draw conduits from nearest parent
                nearest_px = min(parent_nodes, key=lambda p: abs(p[0] - n_x))[0]
                actual_px = center_x + nearest_px * scale
                actual_py = parent_y * scale

                # Line with active glowing pulse
                is_optimal = "Optimal" in label or "Verified" in label
                line_color = (56, 189, 248, 180) if is_optimal else (71, 85, 105, 140)
                draw.line([(actual_px, actual_py + 30), (actual_nx, actual_ny - 30)], fill=line_color, width=2)

                # Traveling energy packet
                packet_t = (pulse_phase + (n_x % 100) * 0.01) % 1.0
                pack_x = actual_px + (actual_nx - actual_px) * packet_t
                pack_y = (actual_py + 30) + ((actual_ny - 30) - (actual_py + 30)) * packet_t
                glow_col = (56, 189, 248) if is_optimal else (148, 163, 184)
                draw.ellipse([pack_x - 5, pack_y - 5, pack_x + 5, pack_y + 5], fill=glow_col)

                # Draw node box
                box_w = 110
                box_h = 32
                if is_optimal:
                    fill_col = (14, 116, 144, 230)
                    border_col = (56, 189, 248)
                    text_col = (255, 255, 255)
                elif "Backtrack" in label or "Discarded" in label:
                    fill_col = (69, 10, 10, 200)
                    border_col = (239, 68, 68)
                    text_col = (248, 113, 113)
                else:
                    fill_col = (30, 41, 59, 200)
                    border_col = (100, 116, 139)
                    text_col = (203, 213, 225)

                draw.rounded_rectangle(
                    [actual_nx - box_w, actual_ny - box_h, actual_nx + box_w, actual_ny + box_h],
                    radius=8,
                    fill=fill_col,
                    outline=border_col,
                    width=2 if is_optimal else 1,
                )
                draw.text((actual_nx - box_w + 12, actual_ny - 10), label[:22], fill=text_col, font=self.font_mono)

        # Telemetry badge: Dynamic reasoning tokens generated
        tokens_gen = int(1200 + t * 450)
        draw.rounded_rectangle([center_x - 180, center_y + 440, center_x + 180, center_y + 510], radius=12, fill=(15, 23, 42, 240), outline=(56, 189, 248), width=2)
        draw.text((center_x - 150, center_y + 456), f"REASONING TOKENS: {tokens_gen:,}", fill=(56, 189, 248), font=self.font_sans_head)


class VerificationRewardLatticeComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes the limitation of imitation learning (SFT) hitting a plateau,
    contrasted with an algorithmic outcome verification oracle.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # SFT Human Plateau Ceiling
        ceiling_y = center_y - 200
        draw.line([(100, ceiling_y), (self.width - 100, ceiling_y)], fill=(239, 68, 68), width=3)
        draw.rectangle([center_x - 190, ceiling_y - 36, center_x + 190, ceiling_y], fill=(254, 226, 226), outline=(239, 68, 68), width=1)
        draw.text((center_x - 170, ceiling_y - 28), "HUMAN DEMONSTRATION CEILING", fill=(185, 28, 28), font=self.font_sans_head)

        # 4 Stalled SFT models flattening against the ceiling
        models = [
            ("Model SFT-A", -280, 0.58),
            ("Model SFT-B", -90, 0.62),
            ("Model SFT-C", 100, 0.64),
            ("Model SFT-D", 290, 0.65),
        ]

        for name, ox, cap in models:
            bx = center_x + ox
            by = ceiling_y + 40 + (1.0 - cap) * 500
            # Column
            draw.rectangle([bx - 60, by, bx + 60, center_y + 360], fill=(203, 213, 225), outline=(148, 163, 184), width=1)
            # Stalled indicator
            draw.text((bx - 50, by - 34), f"{int(cap*100)}%", fill=(71, 85, 105), font=self.font_mono_bold)
            draw.text((bx - 55, center_y + 375), name, fill=(51, 65, 85), font=self.font_mono)

        # Stamped Warning Badge
        p_stamp = min(1.0, max(0.0, (t - 1.2) / 0.4))
        if p_stamp > 0.0:
            stamp_w = 420 * MotionDirector.ease_out_back(p_stamp)
            stamp_h = 70 * MotionDirector.ease_out_back(p_stamp)
            sy1 = center_y - 320
            draw.rectangle(
                [center_x - stamp_w / 2, sy1, center_x + stamp_w / 2, sy1 + stamp_h],
                fill=(239, 68, 68),
                outline=(153, 27, 27),
                width=3,
            )
            draw.text((center_x - 180, sy1 + 18), "IMITATION CEILING REACHED", fill=(255, 255, 255), font=self.font_sans_head)


class NeuralTensorFlowComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes Pure RL Cold Start (DeepSeek-R1-Zero):
    Self-evolution without human supervision, discovering thinking strategies autonomously.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # Autonomous feedback loop
        loop_radius = 320 * scale
        bbox = [center_x - loop_radius, center_y - loop_radius, center_x + loop_radius, center_y + loop_radius]
        draw.ellipse(bbox, outline=(2, 132, 199), width=3)

        # 4 Core Reinforcement Learning Pillars around circumference
        pillars = [
            ("1. EXPLORATION", -math.pi / 2, "Generates Novel Paths"),
            ("2. REWARD VERIFIER", 0, "Checks Answer Accuracy"),
            ("3. BACKPROPAGATION", math.pi / 2, "Updates Policy Weights"),
            ("4. AHA MOMENT", math.pi, "Discovers Self-Reflection"),
        ]

        ang_offset = t * 0.8
        for name, base_ang, desc in pillars:
            a = base_ang + ang_offset
            px = center_x + loop_radius * math.cos(a)
            py = center_y + loop_radius * math.sin(a)

            # Pillar card
            cw, ch = 150, 45
            draw.rounded_rectangle([px - cw, py - ch, px + cw, py + ch], radius=10, fill=(255, 255, 255), outline=(2, 132, 199), width=2)
            draw.text((px - cw + 14, py - 20), name, fill=(2, 132, 199), font=self.font_mono_bold)
            draw.text((px - cw + 14, py + 8), desc, fill=(71, 85, 105), font=self.font_mono)

        # Center Self-Evolution Core
        pulse = MotionDirector.pulse_sin(t, freq=1.5, min_val=80, max_val=110)
        draw.ellipse([center_x - pulse, center_y - pulse, center_x + pulse, center_y + pulse], fill=(2, 132, 199, 40), outline=(2, 132, 199), width=2)
        draw.text((center_x - 70, center_y - 12), "R1-ZERO CORE", fill=(15, 23, 42), font=self.font_sans_head)


class KVCachePaginationComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes Test-Time Compute Scaling:
    Expanding token budget dynamically increases problem-solving capability.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # Logarithmic compute scaling curve
        ox, oy = center_x - 380, center_y + 260
        w, h = 760, 480

        # Axes
        draw.line([(ox, oy), (ox + w, oy)], fill=(15, 23, 42), width=2)
        draw.line([(ox, oy), (ox, oy - h)], fill=(15, 23, 42), width=2)

        draw.text((ox + w - 180, oy + 16), "INFERENCE COMPUTE (TOKENS)", fill=(71, 85, 105), font=self.font_mono)
        draw.text((ox - 40, oy - h - 36), "ACCURACY (%)", fill=(71, 85, 105), font=self.font_mono)

        # Draw dynamic logarithmic curve
        curve_pts = []
        progress_curve = min(1.0, max(0.1, t / 4.0))
        for step in range(int(100 * progress_curve)):
            px = step / 100.0
            # Logarithmic response curve
            py = math.log(1.0 + px * 9.0) / math.log(10.0)
            pt_x = ox + px * w
            pt_y = oy - py * h * 0.88
            curve_pts.append((pt_x, pt_y))

        if len(curve_pts) > 1:
            draw.line(curve_pts, fill=(2, 132, 199), width=4)

        # Current Token Allocation Marker
        if curve_pts:
            curr_x, curr_y = curve_pts[-1]
            draw.ellipse([curr_x - 10, curr_y - 10, curr_x + 10, curr_y + 10], fill=(2, 132, 199))
            token_val = int(512 * math.pow(2.0, progress_curve * 6.0))
            acc_val = int(22.0 + progress_curve * 68.0)

            draw.rounded_rectangle([curr_x - 120, curr_y - 65, curr_x + 120, curr_y - 15], radius=8, fill=(15, 23, 42), outline=(2, 132, 199), width=1)
            draw.text((curr_x - 105, curr_y - 55), f"{token_val:,} TOKENS -> {acc_val}%", fill=(255, 255, 255), font=self.font_mono)
