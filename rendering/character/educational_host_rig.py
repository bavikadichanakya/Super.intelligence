"""
SUPER.INTELLIGENCEEE — Phase 15 Educational Character Host Rig
Extends the canonical character rig with:
1. 5 distinct expressive states:
   - 'overwhelmed': Wide eyes, raised brows, sweat bead, tense mouth
   - 'smug_sarcastic': Asymmetrical smirk, arched brow, knowing squint
   - 'focused_insight': Concentrated analytical brow, downward analytical gaze
   - 'triumphant': Bright white catchlights, broad beaming smile, energetic posture
   - 'confident_host': Warm direct eye contact, natural friendly smile
2. Meaningful Prop Interactions:
   - 'task_stack': Balancing an overwhelming, trembling tower of glowing pixel calculation cubes
   - 'glowing_alu_core': Cradling a floating illuminated 3D ALU compute core in hand with directional lighting
   - 'simt_wand': Pencil acting as an ignition wand directing synchronous dataflow waves
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from rendering.animated_character_host import AnimatedCharacterHost


class EducationalCharacterHost(AnimatedCharacterHost):
    """
    Advanced character host for character-led educational entertainment.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        super().__init__(workspace_root=workspace_root)
        self._build_expression_assets()

    def _build_expression_assets(self) -> None:
        """Constructs parametric expression overlays seamlessly mapped to 2048 space."""
        # 1. Sweat drop for 'overwhelmed'
        sw = Image.new("RGBA", (80, 100), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(sw)
        # Teardrop shape: ellipse + triangle
        sdraw.ellipse([20, 40, 60, 80], fill=(0, 229, 255, 230), outline=(255, 255, 255, 255), width=2)
        sdraw.polygon([(40, 15), (22, 50), (58, 50)], fill=(0, 229, 255, 230))
        # Highlight catchlight
        sdraw.ellipse([30, 48, 38, 56], fill=(255, 255, 255, 240))
        self._sweat_drop = sw

        # 2. Glowing ALU Core prop
        cw, ch = 240, 240
        core = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        cdraw = ImageDraw.Draw(core)
        # Multi-layer outer glow
        for r in range(40, 10, -5):
            alpha = int(180 * (1.0 - r / 40.0))
            cdraw.rounded_rectangle([r, r, cw - r, ch - r], radius=16, fill=(16, 185, 129, alpha // 4), outline=(16, 185, 129, alpha), width=2)
        # Inner silicon die tile
        cdraw.rounded_rectangle([50, 50, cw - 50, ch - 50], radius=12, fill=(12, 36, 28, 255), outline=(52, 211, 153, 255), width=3)
        # ALU circuit lines inside core
        cdraw.line([(70, 90), (170, 90)], fill=(52, 211, 153, 255), width=2)
        cdraw.line([(70, 150), (170, 150)], fill=(52, 211, 153, 255), width=2)
        cdraw.line([(120, 70), (120, 170)], fill=(52, 211, 153, 255), width=2)
        cdraw.text((85, 108), "ALU", fill=(255, 255, 255, 255))
        self._alu_core_prop = core

    def apply_expression(
        self,
        canvas_body: Image.Image,
        expression_id: str,
        t_sec: float,
    ) -> None:
        """Applies distinct eye, brow, and prop accents in 2048 master space."""
        draw = ImageDraw.Draw(canvas_body)

        # Left eye: (881, 745), Right eye: (1207, 745)
        # Eyebrows: y ~ 680..725

        if expression_id == "overwhelmed":
            # 1. Wide shocked pupils: add white ring and tiny black contracted pupil
            # Left pupil wide shock
            draw.ellipse([865, 730, 897, 762], fill=(255, 255, 255, 240))
            draw.ellipse([874, 739, 888, 753], fill=(15, 15, 20, 255))
            # Right pupil wide shock
            draw.ellipse([1191, 730, 1223, 762], fill=(255, 255, 255, 240))
            draw.ellipse([1200, 739, 1214, 753], fill=(15, 15, 20, 255))

            # 2. Raised high arched stress eyebrows
            brow_stress_dy = -12 + int(2 * math.sin(t_sec * 8.0))
            draw.arc([820, 675 + brow_stress_dy, 940, 725 + brow_stress_dy], start=190, end=350, fill=(35, 25, 20, 255), width=8)
            draw.arc([1150, 675 + brow_stress_dy, 1270, 725 + brow_stress_dy], start=190, end=350, fill=(35, 25, 20, 255), width=8)

            # 3. Comical sweat bead on temple
            sweat_wobble = int(3 * math.sin(t_sec * 6.0))
            canvas_body.alpha_composite(self._sweat_drop, (1290, 740 + sweat_wobble))

        elif expression_id == "smug_sarcastic":
            # 1. Left brow arched high, right brow lower/skeptical
            draw.arc([820, 665, 940, 715], start=200, end=340, fill=(35, 25, 20, 255), width=9)
            draw.line([(1155, 715), (1265, 715)], fill=(35, 25, 20, 255), width=8)

            # 2. Amused knowing gaze: slight squint on right eye
            draw.line([(1185, 745), (1225, 745)], fill=(35, 25, 20, 255), width=5)

        elif expression_id == "focused_insight":
            # 1. Lowered analytical concentration brows
            draw.line([(830, 715), (935, 728)], fill=(35, 25, 20, 255), width=9)
            draw.line([(1160, 728), (1265, 715)], fill=(35, 25, 20, 255), width=9)

            # 2. Downward analytical gaze toward hand/prop: pupils shifted slightly down-right
            draw.ellipse([885, 744, 897, 756], fill=(15, 15, 20, 255))
            draw.ellipse([1211, 744, 1223, 756], fill=(15, 15, 20, 255))

        elif expression_id == "triumphant":
            # 1. Raised joyful brows
            draw.arc([825, 680, 935, 720], start=190, end=350, fill=(35, 25, 20, 255), width=8)
            draw.arc([1155, 680, 1265, 720], start=190, end=350, fill=(35, 25, 20, 255), width=8)

            # 2. Bright white catchlights in eyes
            draw.ellipse([876, 736, 886, 746], fill=(255, 255, 255, 255))
            draw.ellipse([1202, 736, 1212, 746], fill=(255, 255, 255, 255))

        elif expression_id == "confident_host":
            # Warm natural eye contact with clear catchlights
            draw.ellipse([878, 738, 885, 745], fill=(255, 255, 255, 255))
            draw.ellipse([1204, 738, 1211, 745], fill=(255, 255, 255, 255))

    def render_educational_sprite(
        self,
        t_sec: float,
        target_height: int,
        expression_id: str = "confident_host",
        is_speaking: bool = True,
        speech_intensity: float = 1.0,
        gesture_mode: str = "explaining",
        prop_mode: str = "none",
        target_xy: Optional[Tuple[int, int]] = None,
        flip_h: bool = False,
    ) -> Tuple[Image.Image, Dict[str, Any]]:
        """
        Renders the character with expression overlays, lip-sync visemes, and interactive props.
        """
        kin = self.compute_gestures(t_sec, gesture_mode=gesture_mode, is_speaking=is_speaking, target_xy=target_xy)

        # 1. Base body
        if kin["blink_alpha"] > 0.35 and expression_id != "overwhelmed":
            body = self._base_blink.copy()
        else:
            body = self._base_open.copy()

        # 2. Apply active facial expression
        self.apply_expression(body, expression_id, t_sec)

        # 3. Composite active mouth viseme
        viseme_img, viseme_name = self.compute_viseme(t_sec, is_speaking=is_speaking, speech_intensity=speech_intensity)
        body.paste(viseme_img, self.MOUTH_ORIGIN, self._mouth_mask)

        # 4. Composite dynamic arm and props
        if self._arm_layer:
            arm_w, arm_h = self._arm_layer.size
            rel_pivot_x = self.SHOULDER_PIVOT_2048[0] - self.ARM_BBOX_2048[0]
            rel_pivot_y = self.SHOULDER_PIVOT_2048[1] - self.ARM_BBOX_2048[1]

            rot_deg = kin["arm_rot_deg"]
            if expression_id == "overwhelmed":
                # Raise hands up defensively
                rot_deg = -24.0 + 3.0 * math.sin(t_sec * 8.0)
            elif prop_mode == "glowing_alu_core":
                # Bend arm to cradle the core in front of chest
                rot_deg = -18.0 + 1.0 * math.sin(t_sec * 2.0)

            rotated_arm = self._arm_layer.rotate(
                rot_deg,
                resample=Image.Resampling.BICUBIC,
                center=(rel_pivot_x, rel_pivot_y),
                expand=True
            )
            rw, rh = rotated_arm.size
            diff_x = (rw - arm_w) // 2
            diff_y = (rh - arm_h) // 2
            paste_x = self.ARM_BBOX_2048[0] - diff_x + int(kin["arm_dx"])
            paste_y = self.ARM_BBOX_2048[1] - diff_y + int(kin["arm_dy"])
            body.alpha_composite(rotated_arm, (paste_x, paste_y))

        # 5. Composite Prop if active
        if prop_mode == "glowing_alu_core":
            # Floating illuminated core levitating just above the right hand: around (900, 1100)
            core_float_dy = int(10 * math.sin(t_sec * 3.5))
            body.alpha_composite(self._alu_core_prop, (850, 1050 + core_float_dy))

        # 6. Scale to target height
        orig_w, orig_h = body.size
        aspect = orig_w / float(orig_h)
        scaled_w = int(target_height * aspect)
        scaled_h = target_height

        scaled_sprite = body.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
        if flip_h:
            scaled_sprite = scaled_sprite.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        return scaled_sprite, kin
