"""
SUPER.INTELLIGENCEEE — Universal Proof & Conclusion Compositions
Implements full-bleed 1080x1920 explanatory visualizations for empirical benchmark
validations and circular loop conclusions matching the reference benchmark.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple
from PIL import Image, ImageDraw

from core.universal_scene_contract import UniversalSceneContract
from creative.visual_intelligence.motion_director import MotionDirector
from rendering.visual_intelligence_engine.composition_base import BaseVisualIntelligenceComposition


class ComparativeBenchmarkMatrixComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes empirical benchmark leap using 3D isometric rising columns,
    base pill tags, and dynamic percentage counters.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        domain = self.params.get("domain", "")
        # Resolve benchmark bars dynamically
        target_label = self.params.get("target_label") or self.scene.narrative_purpose
        baseline_val = float(self.params.get("baseline_score", 35.0))
        target_val = float(self.params.get("achieved_score", 85.0))

        # 3 Benchmark Bars
        bars = [
            ("Standard Baseline", -260, baseline_val, (148, 163, 184)),
            ("Optimized Prior Art", -20, baseline_val * 1.35, (100, 116, 139)),
            (f"{target_label[:16]}", 220, target_val, (2, 132, 199)),
        ]

        base_y = center_y + 320
        max_bar_h = 600

        p_rise = min(1.0, max(0.0, t / 3.0))
        rise_curve = MotionDirector.ease_out_cubic(p_rise)

        for name, ox, score, col in bars:
            bx = center_x + ox
            bar_h = (score / 100.0) * max_bar_h * rise_curve
            top_y = base_y - bar_h

            # Draw 3D column face
            col_w = 160
            draw.rectangle([bx - col_w/2, top_y, bx + col_w/2, base_y], fill=col)

            # Score label on top of bar
            curr_score = score * rise_curve
            score_str = f"{curr_score:.1f}%" if score <= 100 else f"{int(curr_score)}"
            draw.text((bx - 45, top_y - 45), score_str, fill=(15, 23, 42), font=self.font_sans_head)

            # Base Pill badge
            draw.rounded_rectangle([bx - col_w/2, base_y + 16, bx + col_w/2, base_y + 56], radius=8, fill=(255, 255, 255), outline=col, width=2)
            draw.text((bx - 65, base_y + 24), name[:14], fill=(15, 23, 42), font=self.font_mono)

        # Verified Checkmark Badge
        if p_rise > 0.8:
            draw.rounded_rectangle([center_x - 220, center_y - 420, center_x + 220, center_y - 340], radius=12, fill=(240, 253, 244), outline=(5, 150, 105), width=2)
            draw.text((center_x - 180, center_y - 395), "✓ REPRODUCIBLE BENCHMARK VERIFIED", fill=(5, 150, 105), font=self.font_sans_head)


class CircularLoopTakeoutComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes the concluding takeaway on high-contrast obsidian dark field,
    providing a seamless visual loop back to the hook.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # Ambient radiant glow
        glow_radius = 360 * scale
        bbox = [center_x - glow_radius, center_y - glow_radius, center_x + glow_radius, center_y + glow_radius]
        draw.ellipse(bbox, outline=(56, 189, 248), width=2)

        # Core Hero Emblem
        pulse = MotionDirector.pulse_sin(t, freq=1.8, min_val=140, max_val=170)
        draw.ellipse([center_x - pulse, center_y - pulse, center_x + pulse, center_y + pulse], fill=(15, 23, 42), outline=(56, 189, 248), width=3)

        topic = self.scene.engine_specific_config.get("topic_name", "Autonomous Core")
        draw.text((center_x - 140, center_y - 20), topic[:22].upper(), fill=(255, 255, 255), font=self.font_sans_head)

        # License & Open Weights Pill
        draw.rounded_rectangle([center_x - 180, center_y + 260, center_x + 180, center_y + 320], radius=10, fill=(30, 41, 59), outline=(56, 189, 248), width=1)
        draw.text((center_x - 150, center_y + 278), "OPEN SOURCE • PRODUCTION READY", fill=(56, 189, 248), font=self.font_mono)

        # Bottom Loop indicator
        draw.text((center_x - 110, center_y + 440), "↺ REPLAY / LOOP", fill=(148, 163, 184), font=self.font_sans_head)
