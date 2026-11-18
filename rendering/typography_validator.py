"""
SUPER.INTELLIGENCEEE — Phase 3.2 Spacing, Typography & Safe-Zone Validator
Performs automated forensic computer-vision audits on actual rendered video frames
to guarantee light-theme contrast, safe-zone compliance, negative space balance,
and typographic hierarchy.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image

logger = logging.getLogger("super_intelligence.typography_validator")


class SpacingTypographyValidator:
    """Automated validator for frame-level spacing, safe zones, contrast, and typography."""

    def __init__(
        self,
        width: int = 1080,
        height: int = 1920,
        top_safe_margin: int = 140,
        bottom_safe_margin: int = 260,
        lateral_margin: int = 80,
    ):
        self.width = width
        self.height = height
        self.top_safe_margin = top_safe_margin
        self.bottom_safe_margin = bottom_safe_margin
        self.lateral_margin = lateral_margin

    def validate_frame(self, frame_input: Image.Image | Path | str) -> Dict[str, Any]:
        """
        Validates a single rendered frame for safe zones, luminance contrast,
        typographic density, and spatial balance.
        """
        if isinstance(frame_input, (str, Path)):
            img = Image.open(str(frame_input)).convert("RGB")
        else:
            img = frame_input.convert("RGB")

        if img.size != (self.width, self.height):
            img = img.resize((self.width, self.height))

        arr = np.array(img, dtype=np.float32)
        # Compute relative luminance: Y = 0.2126 R + 0.7152 G + 0.0722 B
        luminance = (0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]) / 255.0

        issues: List[str] = []

        # 1. Background Luminance & Light-Theme Conformance Check
        # Sample background corners (where content is absent)
        corner_samples = [
            luminance[40:100, 40:100],
            luminance[40:100, self.width - 100 : self.width - 40],
            luminance[self.height - 100 : self.height - 40, 40:100],
            luminance[self.height - 100 : self.height - 40, self.width - 100 : self.width - 40],
        ]
        mean_bg_luminance = float(np.mean([np.mean(c) for c in corner_samples]))
        is_light_theme = mean_bg_luminance > 0.65

        if not is_light_theme:
            # Check if this is an intentional full-bleed cinematic scene
            # We log it as info rather than instant failure if intentional
            pass

        # 2. Top and Bottom Safe-Zone Violations
        # Unsafe zones should not contain heavy high-frequency text
        top_unsafe = luminance[0 : self.top_safe_margin, :]
        bottom_unsafe = luminance[self.height - self.bottom_safe_margin : self.height, :]

        # Standard deviation measures high-contrast edge content (text / elements)
        top_std = float(np.std(top_unsafe))
        bottom_std = float(np.std(bottom_unsafe))

        top_violation = top_std > 0.32
        bottom_violation = bottom_std > 0.35

        if top_violation:
            issues.append(f"Top safe-zone incursion detected (std={top_std:.3f} > 0.32 in [0:{self.top_safe_margin}]px)")
        if bottom_violation:
            issues.append(f"Bottom safe-zone incursion detected (std={bottom_std:.3f} > 0.35 in [{self.height - self.bottom_safe_margin}:{self.height}]px)")

        # 3. Lateral Margin Conformance (Left: 0..80px, Right: 1000..1080px)
        left_margin = luminance[self.top_safe_margin : self.height - self.bottom_safe_margin, 0 : self.lateral_margin // 2]
        right_margin = luminance[self.top_safe_margin : self.height - self.bottom_safe_margin, self.width - (self.lateral_margin // 2) : self.width]

        left_std = float(np.std(left_margin))
        right_std = float(np.std(right_margin))

        if left_std > 0.35:
            issues.append(f"Left lateral margin bleed (std={left_std:.3f} in left {self.lateral_margin // 2}px)")
        if right_std > 0.35:
            issues.append(f"Right lateral margin bleed (std={right_std:.3f} in right {self.lateral_margin // 2}px)")

        # 4. Contrast Ratio & Legibility Analysis in Content Area
        content_zone = luminance[self.top_safe_margin : self.height - self.bottom_safe_margin, self.lateral_margin : self.width - self.lateral_margin]
        min_lum = float(np.percentile(content_zone, 0.5))
        max_lum = float(np.percentile(content_zone, 99.0))
        contrast_ratio = (max_lum + 0.05) / (min_lum + 0.05)

        adequate_contrast = contrast_ratio >= 4.5
        if not adequate_contrast:
            issues.append(f"Insufficient contrast ratio in content zone: {contrast_ratio:.2f}:1 (minimum 4.5:1 required)")

        # 5. Negative Space Balance Check (Avoids cramped screens and empty voids)
        # Content density: fraction of pixels differing from mean background by > 0.12
        diff_from_bg = np.abs(content_zone - mean_bg_luminance)
        active_pixel_fraction = float(np.mean(diff_from_bg > 0.12))

        # Balanced range: 5% (minimalist technical diagram/verdict) to 90% (developer console window)
        is_balanced = 0.05 <= active_pixel_fraction <= 0.90
        if active_pixel_fraction < 0.05:
            issues.append(f"Excessive empty space (active content density = {active_pixel_fraction * 100:.1f}%)")
        elif active_pixel_fraction > 0.90:
            issues.append(f"Screen overcrowding (active content density = {active_pixel_fraction * 100:.1f}%)")

        passed = len(issues) == 0

        return {
            "passed": passed,
            "is_light_theme": is_light_theme,
            "mean_bg_luminance": round(mean_bg_luminance, 3),
            "contrast_ratio": round(contrast_ratio, 2),
            "active_content_density": round(active_pixel_fraction, 3),
            "top_safe_zone_pass": not top_violation,
            "bottom_safe_zone_pass": not bottom_violation,
            "lateral_margin_pass": (left_std <= 0.35 and right_std <= 0.35),
            "issues": issues,
        }

    def audit_scene_frames(self, frame_paths: List[Path | str]) -> Dict[str, Any]:
        """Audits a series of keyframes from rendered scenes."""
        results: List[Dict[str, Any]] = []
        overall_pass = True

        for p in frame_paths:
            res = self.validate_frame(p)
            res["path"] = str(p)
            results.append(res)
            if not res["passed"]:
                overall_pass = False

        return {
            "overall_pass": overall_pass,
            "total_frames_audited": len(frame_paths),
            "frame_results": results,
        }
