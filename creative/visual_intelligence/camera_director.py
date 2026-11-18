"""
SUPER.INTELLIGENCEEE — Camera Director
Choreographs 2D/2.5D camera zoom, pan, dolly, and parallax paths across the 1080x1920 canvas.
Eliminates static, frozen camera states.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple


@dataclass
class CameraKeyframe:
    time_sec: float
    scale: float
    pan_x: float
    pan_y: float
    rotation_deg: float = 0.0


class CameraDirector:
    """
    Computes smooth camera transformations for a scene based on its movement profile.
    """

    def __init__(self, movement_type: str = "slow_zoom_in", duration: float = 6.0):
        self.movement_type = movement_type
        self.duration = max(duration, 0.1)

    def get_transform(self, t: float) -> Tuple[float, float, float, float]:
        """
        Returns (scale, pan_x, pan_y, rotation_deg) at time t.
        """
        progress = max(0.0, min(1.0, t / self.duration))

        if self.movement_type == "slow_zoom_in":
            # Gentle cinematic push-in (1.0 to 1.12)
            scale = 1.0 + 0.12 * self._ease_in_out(progress)
            pan_x = 0.0
            pan_y = -30.0 * progress
            rot = 0.0

        elif self.movement_type == "pan_right":
            # Smooth lateral pan tracking across the flow
            scale = 1.05
            pan_x = 60.0 - 120.0 * self._ease_in_out(progress)
            pan_y = 0.0
            rot = 0.0

        elif self.movement_type == "macro_isolate":
            # Fast zoom into point of interest with ease-out
            p_ease = self._ease_out_cubic(progress)
            scale = 1.0 + 0.28 * p_ease
            pan_x = -40.0 * p_ease
            pan_y = 50.0 * p_ease
            rot = -1.2 * p_ease

        elif self.movement_type == "parallax_tilt":
            # Subtle isometric depth oscillation
            scale = 1.08 + 0.04 * math.sin(progress * math.pi)
            pan_x = 20.0 * math.cos(progress * math.pi)
            pan_y = -20.0 * progress
            rot = 1.5 * math.sin(progress * 2 * math.pi)

        else:
            scale = 1.0
            pan_x = 0.0
            pan_y = 0.0
            rot = 0.0

        return scale, pan_x, pan_y, rot

    @staticmethod
    def _ease_in_out(p: float) -> float:
        return 0.5 * (1.0 - math.cos(p * math.pi))

    @staticmethod
    def _ease_out_cubic(p: float) -> float:
        return 1.0 - math.pow(1.0 - p, 3.0)
