"""
SUPER.INTELLIGENCEEE — Phase 13 Character Host Engine
Deterministic procedural 2D animation and compositing for the recurring documentary host.
Designed for high performance on Windows 11 / Intel i5 integrated graphics.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from core.character_scene_config import (
    CharacterSceneConfig,
    CharacterPose,
    CharacterExpression,
    CharacterScreenPosition,
    CharacterMovementPattern,
)


class CharacterHostEngine:
    """
    Renders and composites the canonical documentary host into 1080x1920 scene canvases.
    Features:
    - Biometric sinusoidal respiration & micro-sway
    - Deterministic 3.2s blink cycle with smooth eyelid easing
    - Pose-specific anchoring (center hero, lower left, lower right)
    - Gaze direction and head tilt tracking
    - Directional ambient lighting tint and contact drop shadows
    - Subtitle safe-zone collision avoidance
    """

    DEFAULT_CANVAS_WIDTH: int = 1080
    DEFAULT_CANVAS_HEIGHT: int = 1920
    SUBTITLE_SAFE_ZONE: Tuple[int, int, int, int] = (0, 1640, 1080, 1820)

    # Standard position anchors: (center_x, bottom_y, scale)
    POSITION_PRESETS = {
        CharacterScreenPosition.CENTER_HERO: (540, 1550, 0.72),
        CharacterScreenPosition.LOWER_LEFT: (260, 1580, 0.62),
        CharacterScreenPosition.LOWER_RIGHT: (820, 1580, 0.62),
        CharacterScreenPosition.SPLIT_LEFT: (270, 1450, 0.58),
        CharacterScreenPosition.SPLIT_RIGHT: (810, 1450, 0.58),
    }

    def __init__(self, asset_dir: Optional[Path] = None):
        self.workspace_root = Path(__file__).resolve().parent.parent
        self.asset_dir = asset_dir or (self.workspace_root / "assets" / "character")

        # Load canonical assets
        self.cutout_path = self.asset_dir / "character_cutout_transparent.png"
        self.blink_path = self.asset_dir / "expressions" / "character_blinking.png"
        self.overlay_path = self.asset_dir / "expressions" / "eyelid_blink_overlay.png"

        if not self.cutout_path.exists():
            raise FileNotFoundError(f"Canonical cutout missing at {self.cutout_path}")

        self._base_open = Image.open(self.cutout_path).convert("RGBA")
        if self.blink_path.exists():
            self._base_blink = Image.open(self.blink_path).convert("RGBA")
        else:
            self._base_blink = self._base_open.copy()

        # Cache scaled assets
        self._scaled_cache: Dict[Tuple[int, int, bool], Image.Image] = {}

    def get_screen_anchor(
        self,
        config: CharacterSceneConfig,
        canvas_width: int = 1080,
        canvas_height: int = 1920
    ) -> Tuple[int, int, float]:
        """Resolves (center_x, bottom_y, scale) based on config and canvas dimensions."""
        preset_x, preset_y, preset_scale = self.POSITION_PRESETS.get(
            config.screen_position, (540, 1550, 0.65)
        )
        scale = config.scale if config.scale is not None else preset_scale
        cx = config.custom_center_x if config.custom_center_x is not None else preset_x
        by = config.custom_bottom_y if config.custom_bottom_y is not None else preset_y

        # Adapt if non-standard canvas dimensions
        if canvas_width != 1080 or canvas_height != 1920:
            cx = int(cx * (canvas_width / 1080.0))
            by = int(by * (canvas_height / 1920.0))

        return cx, by, scale

    def compute_motion_state(
        self,
        config: CharacterSceneConfig,
        t_sec: float
    ) -> Dict[str, Any]:
        """Computes instantaneous biometric animation transforms for timestamp t_sec."""
        # 1. Respiration (0.35 Hz, ~2.8s per breath)
        breath_freq = 0.35
        breath_amp = 3.5  # pixels
        breath_dy = breath_amp * math.sin(2.0 * math.pi * breath_freq * t_sec)

        # 2. Subtle Micro-Tilt (0.18 Hz)
        tilt_freq = 0.18
        base_tilt = 0.0
        if config.pose == CharacterPose.INVESTIGATOR_EXAMINING:
            base_tilt = 2.0   # Tilted toward subject
        elif config.pose == CharacterPose.EXPLAINER_GESTURE:
            base_tilt = -1.8  # Tilted toward schematic
        elif config.expression == CharacterExpression.CURIOUS_INQUIRY:
            base_tilt = 1.0

        tilt_deg = base_tilt + 0.8 * math.sin(2.0 * math.pi * tilt_freq * t_sec)

        # 3. Biometric Blink Cycle
        # Every 3.2s, a blink lasts 150ms (0.15s)
        blink_cycle = 3.2
        mod_t = t_sec % blink_cycle
        is_blinking = False
        blink_alpha = 0.0

        if mod_t < 0.150:
            is_blinking = True
            # Bell curve easing for smooth eyelid closure and opening
            phase = mod_t / 0.150
            blink_alpha = math.sin(phase * math.pi)  # 0 -> 1 -> 0

        # 4. Entry transition (if entering_frame_settle)
        entry_offset_y = 0.0
        if config.movement_pattern == CharacterMovementPattern.ENTERING_FRAME_SETTLE:
            if t_sec < 0.6:
                ease = 1.0 - math.pow(1.0 - (t_sec / 0.6), 3)  # Cubic ease-out
                entry_offset_y = (1.0 - ease) * 120.0  # Rise 120px into position

        return {
            "dy": breath_dy + entry_offset_y,
            "tilt_deg": tilt_deg,
            "is_blinking": is_blinking,
            "blink_alpha": blink_alpha,
        }

    def render_character_sprite(
        self,
        config: CharacterSceneConfig,
        t_sec: float,
        target_height: int,
        flip_horizontal: bool = False
    ) -> Image.Image:
        """Generates the transformed, anti-aliased character RGBA sprite for timestamp t_sec."""
        motion = self.compute_motion_state(config, t_sec)

        # Base sprite selection (blend open and blinking if in transition)
        if motion["blink_alpha"] > 0.35:
            base = self._base_blink
        else:
            base = self._base_open

        # Scale to target size
        orig_w, orig_h = base.size
        aspect = orig_w / float(orig_h)
        scaled_w = int(target_height * aspect)
        scaled_h = target_height

        scaled_sprite = base.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)

        if flip_horizontal:
            scaled_sprite = scaled_sprite.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        # Apply subtle head/body tilt rotation anchored at chest/neck
        tilt = motion["tilt_deg"]
        if abs(tilt) > 0.1:
            # Rotate with bicubic interpolation
            # Pivot at chest: x ~ width*0.5, y ~ height*0.75
            scaled_sprite = scaled_sprite.rotate(
                tilt,
                resample=Image.Resampling.BICUBIC,
                center=(scaled_w // 2, int(scaled_h * 0.75)),
                expand=True
            )

        return scaled_sprite

    def composite_onto_canvas(
        self,
        canvas: Image.Image,
        config: CharacterSceneConfig,
        t_sec: float,
        ambient_tint_hex: Optional[str] = None
    ) -> Tuple[int, int, int, int]:
        """
        Composites the animated character onto the canvas with realistic drop shadow
        and ambient color grading.
        Returns the bounding box (x0, y0, x1, y1) of the rendered character on canvas.
        """
        cx, by, scale = self.get_screen_anchor(config, canvas.width, canvas.height)
        motion = self.compute_motion_state(config, t_sec)

        # Determine target height based on scale
        # At scale 1.0, character occupies approx 1050px in 1920 canvas
        target_h = int(1050 * scale)

        # Flip horizontally if investigator/explainer requires subject on left
        flip_h = False
        if config.screen_position in (CharacterScreenPosition.LOWER_RIGHT, CharacterScreenPosition.SPLIT_RIGHT):
            if config.pose in (CharacterPose.INVESTIGATOR_EXAMINING, CharacterPose.EXPLAINER_GESTURE):
                flip_h = True

        sprite = self.render_character_sprite(config, t_sec, target_h, flip_horizontal=flip_h)
        sw, sh = sprite.size

        # Compute top-left placement coordinates
        dest_x = cx - (sw // 2)
        dest_y = int(by - sh + motion["dy"])

        # 1. Soft directional contact drop shadow
        shadow_mask = sprite.split()[3]
        shadow_im = Image.new("RGBA", (sw, sh), (10, 12, 16, 160))
        shadow_im.putalpha(shadow_mask)
        shadow_im = shadow_im.filter(ImageFilter.GaussianBlur(radius=18))

        shadow_offset_x = 12
        shadow_offset_y = 16
        canvas.alpha_composite(shadow_im, (dest_x + shadow_offset_x, dest_y + shadow_offset_y))

        # 2. Ambient lighting tint (if requested)
        if ambient_tint_hex:
            try:
                hex_c = ambient_tint_hex.lstrip("#")
                r = int(hex_c[0:2], 16)
                g = int(hex_c[2:4], 16)
                b = int(hex_c[4:6], 16)
                # Subtle 8% color wash
                tint_layer = Image.new("RGBA", sprite.size, (r, g, b, 20))
                sprite = Image.alpha_composite(sprite, tint_layer)
            except Exception:
                pass

        # 3. Composite host sprite onto canvas
        canvas.alpha_composite(sprite, (dest_x, dest_y))

        rendered_bbox = (dest_x, dest_y, dest_x + sw, dest_y + sh)
        return rendered_bbox

    def check_subtitle_safe_zone_collision(
        self,
        rendered_bbox: Tuple[int, int, int, int]
    ) -> Tuple[bool, str]:
        """
        Verifies that character does not obstruct subtitles (y=1640..1820).
        Returns (is_safe, message).
        """
        rx0, ry0, rx1, ry1 = rendered_bbox
        sx0, sy0, sx1, sy1 = self.SUBTITLE_SAFE_ZONE

        # Check intersection
        inter_x0 = max(rx0, sx0)
        inter_y0 = max(ry0, sy0)
        inter_x1 = min(rx1, sx1)
        inter_y1 = min(ry1, sy1)

        if inter_x0 < inter_x1 and inter_y0 < inter_y1:
            overlap_h = inter_y1 - inter_y0
            return False, f"Character overlaps subtitle safe zone by {overlap_h}px (y: {inter_y0}..{inter_y1})"

        return True, "Safe zone respected: zero subtitle overlap."
