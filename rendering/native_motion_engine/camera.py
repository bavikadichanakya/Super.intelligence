"""
SUPER.INTELLIGENCEEE — Phase 4.3.3.2 Cinematic Camera & Spatial Composition Engine
Provides 2D/2.5D virtual camera operations:
- Push-in / Pull-out (smooth focal zoom)
- Panning / Tracking (following moving entities)
- Layered Parallax (foreground / background depth)
- Coordinate transformations (world space -> screen space)
Pure Python / NumPy / Pillow. Zero external 3D runtime dependencies.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Tuple

from rendering.native_motion_engine.primitives import (
    clamp,
    ease_in_out_cubic,
    ease_out_cubic,
    get_progress,
)


@dataclass
class CameraKeyframe:
    timestamp: float
    target_x: float
    target_y: float
    zoom: float = 1.0
    easing: str = "ease_in_out_cubic"


class CinematicCamera:
    """
    Virtual camera for 2D/2.5D motion graphics.
    Maintains focal target and zoom, mapping world coordinates to 1080x1920 screen space.
    """

    def __init__(
        self,
        viewport_width: int = 1080,
        viewport_height: int = 1920,
        initial_x: float = 540.0,
        initial_y: float = 960.0,
        initial_zoom: float = 1.0,
    ):
        self.vw = viewport_width
        self.vh = viewport_height
        self.cx = self.vw / 2.0
        self.cy = self.vh / 2.0

        # Current camera state
        self.x = initial_x
        self.y = initial_y
        self.zoom = initial_zoom

        # Keyframe track for scripted camera motions
        self.keyframes: List[CameraKeyframe] = []

    def set_position(self, x: float, y: float, zoom: float = 1.0):
        """Directly sets camera target and zoom."""
        self.x = x
        self.y = y
        self.zoom = max(0.2, min(5.0, zoom))

    def add_keyframe(
        self,
        timestamp: float,
        target_x: float,
        target_y: float,
        zoom: float = 1.0,
        easing: str = "ease_in_out_cubic",
    ):
        """Appends a camera keyframe."""
        self.keyframes.append(
            CameraKeyframe(
                timestamp=timestamp,
                target_x=target_x,
                target_y=target_y,
                zoom=zoom,
                easing=easing,
            )
        )
        self.keyframes.sort(key=lambda k: k.timestamp)

    def update_for_time(self, t: float):
        """Updates camera position and zoom based on keyframe track."""
        if not self.keyframes:
            return

        if t <= self.keyframes[0].timestamp:
            k = self.keyframes[0]
            self.x, self.y, self.zoom = k.target_x, k.target_y, k.zoom
            return

        if t >= self.keyframes[-1].timestamp:
            k = self.keyframes[-1]
            self.x, self.y, self.zoom = k.target_x, k.target_y, k.zoom
            return

        # Find enclosing keyframe segment
        for i in range(len(self.keyframes) - 1):
            k0 = self.keyframes[i]
            k1 = self.keyframes[i + 1]
            if k0.timestamp <= t <= k1.timestamp:
                dur = k1.timestamp - k0.timestamp
                p = get_progress(t, k0.timestamp, dur, k1.easing)
                self.x = k0.target_x + (k1.target_x - k0.target_x) * p
                self.y = k0.target_y + (k1.target_y - k0.target_y) * p
                self.zoom = k0.zoom + (k1.zoom - k0.zoom) * p
                return

    def to_screen(
        self,
        world_x: float,
        world_y: float,
        parallax_depth: float = 1.0,
    ) -> Tuple[float, float]:
        """
        Transforms world coordinates into screen coordinates.
        parallax_depth: 1.0 = standard focal plane; < 1.0 = distant background; > 1.0 = close foreground.
        """
        eff_zoom = 1.0 + (self.zoom - 1.0) * parallax_depth
        dx = (world_x - self.x) * parallax_depth
        dy = (world_y - self.y) * parallax_depth

        sx = self.cx + dx * eff_zoom
        sy = self.cy + dy * eff_zoom
        return (sx, sy)

    def to_screen_rect(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        parallax_depth: float = 1.0,
    ) -> Tuple[float, float, float, float]:
        """Transforms an unrotated bounding box to screen coordinates."""
        sx0, sy0 = self.to_screen(x0, y0, parallax_depth)
        sx1, sy1 = self.to_screen(x1, y1, parallax_depth)
        return (min(sx0, sx1), min(sy0, sy1), max(sx0, sx1), max(sy0, sy1))

    def scale_length(self, length: float, parallax_depth: float = 1.0) -> float:
        """Scales a scalar length by current camera zoom."""
        eff_zoom = 1.0 + (self.zoom - 1.0) * parallax_depth
        return length * eff_zoom

    def push_in_transition(
        self,
        t: float,
        start: float,
        duration: float,
        from_zoom: float = 1.0,
        to_zoom: float = 1.35,
        target: Optional[Tuple[float, float]] = None,
        easing: str = "ease_in_out_cubic",
    ):
        """Executes a dynamic push-in zoom into a specific target focal point."""
        p = get_progress(t, start, duration, easing)
        self.zoom = from_zoom + (to_zoom - from_zoom) * p
        if target:
            self.x += (target[0] - self.x) * p * 0.5
            self.y += (target[1] - self.y) * p * 0.5

    def pull_out_transition(
        self,
        t: float,
        start: float,
        duration: float,
        from_zoom: float = 1.35,
        to_zoom: float = 1.0,
        target: Optional[Tuple[float, float]] = None,
        easing: str = "ease_in_out_cubic",
    ):
        """Executes a dynamic pull-out revealing the broader architecture."""
        p = get_progress(t, start, duration, easing)
        self.zoom = from_zoom + (to_zoom - from_zoom) * p
        if target:
            self.x += (target[0] - self.x) * p * 0.5
            self.y += (target[1] - self.y) * p * 0.5
