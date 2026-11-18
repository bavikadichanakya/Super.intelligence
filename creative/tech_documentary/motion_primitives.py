"""
SUPER.INTELLIGENCEEE — Motion Graphics Primitives Engine
Provides reusable mathematical easing, camera tracking, vector morphing,
bezier paths, and typography clearance utilities for broadcast-grade documentary rendering.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple
from PIL import ImageDraw, ImageFont


def harmonic_spring(
    progress: float,
    zeta: float = 0.65,
    omega: float = 7.5,
    damping: Optional[float] = None,
    frequency: Optional[float] = None,
) -> float:
    """
    Damped harmonic oscillator spring easing.
    Produces physical, elastic arrival without artificial bounces.
    """
    if damping is not None:
        zeta = damping if damping < 2.0 else 0.70
    if frequency is not None:
        omega = frequency if frequency < 15.0 else 7.5

    if progress <= 0.0:
        return 0.0
    if progress >= 1.0:
        return 1.0
    return 1.0 - math.exp(-zeta * omega * progress) * math.cos(omega * math.sqrt(max(0.01, 1.0 - zeta**2)) * progress)


def cubic_ease_out(progress: float) -> float:
    """Cubic ease-out for smooth natural deceleration."""
    p = max(0.0, min(1.0, progress))
    return 1.0 - math.pow(1.0 - p, 3)


def cubic_ease_in_out(progress: float) -> float:
    """Cubic ease-in-out for smooth transitions."""
    p = max(0.0, min(1.0, progress))
    if p < 0.5:
        return 4.0 * p * p * p
    return 1.0 - math.pow(-2.0 * p + 2.0, 3) / 2.0


def smooth_step(progress: float) -> float:
    """Hermite smoothstep interpolation."""
    p = max(0.0, min(1.0, progress))
    return p * p * (3.0 - 2.0 * p)


def bezier_point(
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    p3: Tuple[float, float],
    t: float,
) -> Tuple[float, float]:
    """Evaluates a 2D cubic bezier curve at parameter t in [0, 1]."""
    t = max(0.0, min(1.0, t))
    u = 1.0 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t

    x = uuu * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + ttt * p3[0]
    y = uuu * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + ttt * p3[1]
    return (x, y)


def draw_hud_brackets(
    draw: ImageDraw.ImageDraw,
    box: Tuple[int, int, int, int],
    color: Tuple[int, int, int] = (49, 92, 255),
    length: int = 20,
    width: int = 2,
    bracket_len: Optional[int] = None,
) -> None:
    """Draws clean, open architectural HUD corner brackets without enclosing cards."""
    if bracket_len is not None:
        length = bracket_len
    x1, y1, x2, y2 = box
    draw.line([(x1, y1), (x1 + length, y1)], fill=color, width=width)
    draw.line([(x1, y1), (x1, y1 + length)], fill=color, width=width)
    draw.line([(x2 - length, y1), (x2, y1)], fill=color, width=width)
    draw.line([(x2, y1), (x2, y1 + length)], fill=color, width=width)
    draw.line([(x1, y2 - length), (x1, y2)], fill=color, width=width)
    draw.line([(x1, y2), (x1 + length, y2)], fill=color, width=width)
    draw.line([(x2 - length, y2), (x2, y2)], fill=color, width=width)
    draw.line([(x2, y2 - length), (x2, y2)], fill=color, width=width)


def draw_open_hairline(
    draw: ImageDraw.ImageDraw,
    arg1: Any,
    arg2: Any = 80,
    arg3: Any = 1000,
    color: Tuple[int, int, int] = (225, 225, 220),
    width: int = 1,
    label: Optional[str] = None,
    font: Optional[Any] = None,
    label_color: Optional[Tuple[int, int, int]] = None,
) -> None:
    """
    Draws a subtle architectural layout hairline.
    Supports both:
    - (draw, (x1, y1), (x2, y2), color, width)
    - (draw, y, x1, x2, color, width, label)
    """
    if isinstance(arg1, (tuple, list)):
        pt1 = arg1
        pt2 = arg2
        c = arg3 if isinstance(arg3, tuple) else color
        w = color if isinstance(color, int) else width
        draw.line([pt1, pt2], fill=c, width=w)
    else:
        y = int(arg1)
        x1 = int(arg2)
        x2 = int(arg3)
        draw.line([(x1, y), (x2, y)], fill=color, width=width)
        if label:
            lbl_col = label_color or color
            try:
                from PIL import ImageFont
                lbl_font = font or ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 18)
            except Exception:
                from PIL import ImageFont
                lbl_font = font or ImageFont.load_default()
            draw.text((x1, y - 24), label, font=lbl_font, fill=lbl_col)


def check_safe_zone(
    bbox: Tuple[int, int, int, int],
    safe_left: int = 80,
    safe_right: int = 1000,
    safe_top: int = 140,
    safe_bottom: int = 1780,
) -> bool:
    """Verifies that an element bounding box resides strictly inside the 9:16 safe area."""
    x1, y1, x2, y2 = bbox
    return (x1 >= safe_left) and (x2 <= safe_right) and (y1 >= safe_top) and (y2 <= safe_bottom)

