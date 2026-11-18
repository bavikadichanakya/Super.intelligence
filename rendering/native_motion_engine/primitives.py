"""
SUPER.INTELLIGENCEEE — Phase 4.3.2D Native Motion Graphics Engine
Animation Primitives & Parametric Easing Functions.
Deterministic, pure mathematical interpolation with zero external runtime dependencies.
"""

from __future__ import annotations

import math
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


# ==============================================================================
# 1. PARAMETRIC EASING FUNCTIONS
# ==============================================================================

def clamp(val: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Clamps a floating point value to [min_val, max_val]."""
    return max(min_val, min(max_val, val))


def linear(p: float) -> float:
    return clamp(p)


def ease_in_quad(p: float) -> float:
    p = clamp(p)
    return p * p


def ease_out_quad(p: float) -> float:
    p = clamp(p)
    return p * (2.0 - p)


def ease_in_out_quad(p: float) -> float:
    p = clamp(p)
    return 2.0 * p * p if p < 0.5 else -1.0 + (4.0 - 2.0 * p) * p


def ease_in_cubic(p: float) -> float:
    p = clamp(p)
    return p * p * p


def ease_out_cubic(p: float) -> float:
    p = clamp(p)
    p -= 1.0
    return p * p * p + 1.0


def ease_in_out_cubic(p: float) -> float:
    p = clamp(p)
    return 4.0 * p * p * p if p < 0.5 else (p - 1.0) * (2.0 * p - 2.0) * (2.0 * p - 2.0) + 1.0


def ease_out_back(p: float, s: float = 1.70158) -> float:
    p = clamp(p) - 1.0
    return p * p * ((s + 1.0) * p + s) + 1.0


def ease_out_elastic(p: float) -> float:
    p = clamp(p)
    if p == 0.0 or p == 1.0:
        return p
    return math.pow(2.0, -10.0 * p) * math.sin((p - 0.075) * (2.0 * math.pi) / 0.3) + 1.0


EASING_MAP: Dict[str, Callable[[float], float]] = {
    "linear": linear,
    "ease_in": ease_in_quad,
    "ease_out": ease_out_quad,
    "ease_in_out": ease_in_out_quad,
    "ease_in_cubic": ease_in_cubic,
    "ease_out_cubic": ease_out_cubic,
    "ease_in_out_cubic": ease_in_out_cubic,
    "ease_out_back": ease_out_back,
    "ease_out_elastic": ease_out_elastic,
}


def get_progress(t: float, start: float, duration: float, easing: str = "ease_out_cubic") -> float:
    """Computes eased progress [0.0, 1.0] for timestamp t."""
    if duration <= 0.0:
        return 1.0 if t >= start else 0.0
    raw = clamp((t - start) / duration)
    ease_fn = EASING_MAP.get(easing, ease_out_cubic)
    return ease_fn(raw)


# ==============================================================================
# 2. ANIMATION PRIMITIVES
# ==============================================================================

def fade_in(t: float, start: float, duration: float, easing: str = "ease_out_quad") -> float:
    """Returns opacity [0.0, 1.0] over [start, start + duration]."""
    return get_progress(t, start, duration, easing)


def fade_out(t: float, start: float, duration: float, easing: str = "ease_in_quad") -> float:
    """Returns opacity [1.0, 0.0] over [start, start + duration]."""
    return 1.0 - get_progress(t, start, duration, easing)


def slide_in(
    t: float,
    start: float,
    duration: float,
    start_pos: Tuple[float, float],
    end_pos: Tuple[float, float],
    easing: str = "ease_out_cubic",
) -> Tuple[float, float]:
    """Interpolates position from start_pos to end_pos."""
    p = get_progress(t, start, duration, easing)
    x = start_pos[0] + (end_pos[0] - start_pos[0]) * p
    y = start_pos[1] + (end_pos[1] - start_pos[1]) * p
    return (x, y)


def slide_out(
    t: float,
    start: float,
    duration: float,
    current_pos: Tuple[float, float],
    exit_pos: Tuple[float, float],
    easing: str = "ease_in_cubic",
) -> Tuple[float, float]:
    """Interpolates exit position from current_pos to exit_pos."""
    p = get_progress(t, start, duration, easing)
    x = current_pos[0] + (exit_pos[0] - current_pos[0]) * p
    y = current_pos[1] + (exit_pos[1] - current_pos[1]) * p
    return (x, y)


def scale_in(
    t: float,
    start: float,
    duration: float,
    from_scale: float = 0.0,
    to_scale: float = 1.0,
    easing: str = "ease_out_back",
) -> float:
    """Interpolates scaling factor [from_scale, to_scale]."""
    p = get_progress(t, start, duration, easing)
    return from_scale + (to_scale - from_scale) * p


def scale_out(
    t: float,
    start: float,
    duration: float,
    from_scale: float = 1.0,
    to_scale: float = 0.0,
    easing: str = "ease_in_quad",
) -> float:
    """Interpolates scale down from from_scale to to_scale."""
    p = get_progress(t, start, duration, easing)
    return from_scale + (to_scale - from_scale) * p


def draw_line(
    t: float,
    start: float,
    duration: float,
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    easing: str = "linear",
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Returns the visible segment ((x1, y1), (x_current, y_current)) of a line drawing animation."""
    p = get_progress(t, start, duration, easing)
    current_x = p1[0] + (p2[0] - p1[0]) * p
    current_y = p1[1] + (p2[1] - p1[1]) * p
    return (p1, (current_x, current_y))


def draw_path(
    t: float,
    start: float,
    duration: float,
    points: List[Tuple[float, float]],
    easing: str = "linear",
) -> List[Tuple[float, float]]:
    """Progressively reveals a polygonal/path route of points."""
    if not points:
        return []
    if len(points) == 1:
        return [points[0]]

    p = get_progress(t, start, duration, easing)
    total_segments = len(points) - 1
    segment_idx = int(p * total_segments)
    if segment_idx >= total_segments:
        return list(points)

    revealed = list(points[: segment_idx + 1])
    seg_p = (p * total_segments) - segment_idx
    p_a = points[segment_idx]
    p_b = points[segment_idx + 1]
    inter_x = p_a[0] + (p_b[0] - p_a[0]) * seg_p
    inter_y = p_a[1] + (p_b[1] - p_a[1]) * seg_p
    revealed.append((inter_x, inter_y))
    return revealed


def move_object(
    t: float,
    start: float,
    duration: float,
    from_pos: Tuple[float, float],
    to_pos: Tuple[float, float],
    easing: str = "ease_in_out_cubic",
) -> Tuple[float, float]:
    """Moves an object smoothly between two coordinates."""
    p = get_progress(t, start, duration, easing)
    return (
        from_pos[0] + (to_pos[0] - from_pos[0]) * p,
        from_pos[1] + (to_pos[1] - from_pos[1]) * p,
    )


def rotate_object(
    t: float,
    start: float,
    duration: float,
    from_deg: float = 0.0,
    to_deg: float = 360.0,
    easing: str = "linear",
) -> float:
    """Returns angle in degrees at timestamp t."""
    p = get_progress(t, start, duration, easing)
    return from_deg + (to_deg - from_deg) * p


def highlight_region(
    t: float,
    start: float,
    duration: float,
    max_intensity: float = 1.0,
    pulse_freq: float = 2.0,
) -> float:
    """Generates a pulsating highlight intensity [0.0, max_intensity]."""
    if t < start or t > start + duration:
        return 0.0
    elapsed = t - start
    pulse = (math.sin(elapsed * math.pi * 2.0 * pulse_freq) + 1.0) / 2.0
    envelope = math.sin((elapsed / duration) * math.pi)
    return max_intensity * pulse * envelope


def reveal_text(
    t: float,
    start: float,
    duration: float,
    text: str,
    method: str = "character",
) -> str:
    """Typewriter or word-by-word progressive text reveal."""
    if not text:
        return ""
    p = get_progress(t, start, duration, "linear")
    if p >= 1.0:
        return text

    if method == "word":
        words = text.split(" ")
        num_words = max(1, int(len(words) * p))
        return " ".join(words[:num_words])
    else:  # character
        num_chars = int(len(text) * p)
        return text[:num_chars]


def counter_animation(
    t: float,
    start: float,
    duration: float,
    from_val: float,
    to_val: float,
    format_fn: Optional[Callable[[float], str]] = None,
    easing: str = "ease_out_cubic",
) -> str:
    """Smooth numeric counter animation with customizable formatting."""
    p = get_progress(t, start, duration, easing)
    current_val = from_val + (to_val - from_val) * p
    if format_fn:
        return format_fn(current_val)
    if isinstance(to_val, int) or (to_val - int(to_val) == 0 and from_val - int(from_val) == 0):
        return str(int(round(current_val)))
    return f"{current_val:.2f}"


def camera_pan(
    t: float,
    start: float,
    duration: float,
    dx: float,
    dy: float,
    easing: str = "ease_in_out_quad",
) -> Tuple[float, float]:
    """Generates virtual camera translation offsets (offset_x, offset_y)."""
    p = get_progress(t, start, duration, easing)
    return (dx * p, dy * p)


def camera_zoom(
    t: float,
    start: float,
    duration: float,
    from_zoom: float = 1.0,
    to_zoom: float = 1.15,
    easing: str = "ease_in_out_quad",
) -> float:
    """Returns virtual camera scale factor."""
    p = get_progress(t, start, duration, easing)
    return from_zoom + (to_zoom - from_zoom) * p


def parallax(
    t: float,
    start: float,
    duration: float,
    depth_factor: float = 0.5,
    max_offset: float = 40.0,
) -> float:
    """Generates continuous slow parallax shift offset."""
    if t < start:
        return 0.0
    elapsed = t - start
    return math.sin(elapsed * 0.4) * max_offset * depth_factor


def particle_motion(
    t: float,
    seed: int,
    bounds: Tuple[float, float, float, float],
    speed: float = 15.0,
) -> Tuple[float, float, float]:
    """Computes pseudo-random procedural particle position (x, y, opacity)."""
    min_x, min_y, max_x, max_y = bounds
    w = max_x - min_x
    h = max_y - min_y
    if w <= 0: w = 1.0
    if h <= 0: h = 1.0

    offset_x = (seed * 197.3) % w
    offset_y = (seed * 349.7) % h
    dir_x = math.cos(seed * 1.7)
    dir_y = math.sin(seed * 2.3)

    cur_x = min_x + (offset_x + dir_x * speed * t) % w
    cur_y = min_y + (offset_y + dir_y * speed * t) % h
    alpha = (math.sin(t * 1.5 + seed) + 1.0) / 2.0 * 0.4 + 0.1
    return (cur_x, cur_y, alpha)

