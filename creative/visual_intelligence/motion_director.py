"""
SUPER.INTELLIGENCEEE — Motion Director
Provides mathematical animation curves, pulse oscillators, kinetic typography
word reveal schedulers, and selection box geometry calculation.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple


class MotionDirector:
    """
    Manages kinetic animation curves, element reveals, and timing choreography.
    """

    @staticmethod
    def ease_out_back(x: float, c1: float = 1.70158) -> float:
        """Standard overshoot ease-out for snapping UI elements into view."""
        c3 = c1 + 1.0
        x = max(0.0, min(1.0, x))
        return 1.0 + c3 * math.pow(x - 1.0, 3.0) + c1 * math.pow(x - 1.0, 2.0)

    @staticmethod
    def ease_out_cubic(x: float) -> float:
        x = max(0.0, min(1.0, x))
        return 1.0 - math.pow(1.0 - x, 3.0)

    @staticmethod
    def ease_in_out_quad(x: float) -> float:
        x = max(0.0, min(1.0, x))
        return 2.0 * x * x if x < 0.5 else 1.0 - math.pow(-2.0 * x + 2.0, 2.0) / 2.0

    @staticmethod
    def pulse_sin(t: float, freq: float = 2.0, min_val: float = 0.8, max_val: float = 1.0) -> float:
        """Oscillates between min_val and max_val at frequency freq (Hz)."""
        mid = (max_val + min_val) / 2.0
        amp = (max_val - min_val) / 2.0
        return mid + amp * math.sin(t * 2.0 * math.pi * freq)

    @classmethod
    def schedule_kinetic_typography(
        cls,
        text: str,
        duration: float,
        focus_noun: str = "",
        italic_keyword: str = "",
    ) -> List[Dict[str, Any]]:
        """
        Calculates word-by-word timestamps and formatting for kinetic typography.
        """
        words = text.strip().split()
        if not words:
            return []

        word_count = len(words)
        # Allocate speaking time leaving a 0.5s settle window at end
        active_time = max(duration - 0.5, 1.0)
        time_per_word = active_time / word_count

        scheduled = []
        for i, w in enumerate(words):
            start_t = i * time_per_word
            clean_w = w.strip(".,!?:;\"'()[]")
            is_focus = focus_noun and (focus_noun.lower().strip("[]") in clean_w.lower() or clean_w.lower() in focus_noun.lower().strip("[]"))
            is_italic = italic_keyword and (italic_keyword.lower() in clean_w.lower())

            scheduled.append({
                "word": w,
                "clean_word": clean_w,
                "start_time": start_t,
                "is_focus_noun": is_focus,
                "is_italic_keyword": is_italic,
                "highlight_box": is_focus,
            })

        return scheduled
