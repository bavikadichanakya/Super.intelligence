"""
SUPER.INTELLIGENCEEE — Phase 13 Character Quality & Consistency Validator
Automated validation ensuring reference asset integrity, aspect ratio preservation,
safe-zone non-interference, and collision prevention across documentary scenes.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image

from core.character_scene_config import CharacterSceneConfig


class CharacterQualityValidator:
    """
    Automated QA validator enforcing strict character integrity and layout rules.
    """

    EXPECTED_CANONICAL_SHA256: str = "d17de5c978e153a8ef8b332849e4ea653eb7e9fddf7d03b5dbdaf02daac96fde"
    EXPECTED_CANONICAL_DIMS: Tuple[int, int] = (2048, 2048)
    SUBTITLE_SAFE_ZONE: Tuple[int, int, int, int] = (0, 1640, 1080, 1820)
    HEADER_SAFE_ZONE: Tuple[int, int, int, int] = (0, 0, 1080, 240)

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent
        self.char_dir = self.workspace_root / "assets" / "character"

    def validate_reference_asset_integrity(self) -> Dict[str, Any]:
        """Validates that canonical reference image exists and matches exact SHA-256 hash."""
        ref_file = self.workspace_root / "character.me.png"
        mirrored_file = self.char_dir / "character.me.png"

        violations: List[str] = []

        if not ref_file.exists():
            violations.append(f"Canonical master reference missing at {ref_file}")
            return {"passed": False, "violations": violations}

        with open(ref_file, "rb") as f:
            ref_hash = hashlib.sha256(f.read()).hexdigest()

        if ref_hash != self.EXPECTED_CANONICAL_SHA256:
            violations.append(
                f"Canonical image hash mismatch! Expected {self.EXPECTED_CANONICAL_SHA256}, got {ref_hash}."
            )

        with Image.open(ref_file) as im:
            if im.size != self.EXPECTED_CANONICAL_DIMS:
                violations.append(
                    f"Canonical dimensions mismatch! Expected {self.EXPECTED_CANONICAL_DIMS}, got {im.size}."
                )

        if not mirrored_file.exists():
            violations.append(f"Mirrored asset missing at {mirrored_file}")

        # Check required derived assets
        cutout = self.char_dir / "character_cutout_transparent.png"
        if not cutout.exists():
            violations.append(f"Transparent cutout asset missing at {cutout}")

        manifest = self.char_dir / "character_reference_manifest.json"
        if not manifest.exists():
            violations.append(f"Character manifest missing at {manifest}")

        profile = self.char_dir / "character_profile.json"
        if not profile.exists():
            violations.append(f"Character profile missing at {profile}")

        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "sha256": ref_hash,
            "path": str(ref_file),
        }

    def validate_aspect_ratio_and_distortion(
        self,
        rendered_width: int,
        rendered_height: int,
        base_aspect: float = 1610 / 1755.0,
        tolerance: float = 0.05
    ) -> Tuple[bool, Optional[str]]:
        """Verifies that character has not been stretched or squashed."""
        current_aspect = rendered_width / float(rendered_height)
        diff = abs(current_aspect - base_aspect)
        if diff > tolerance:
            return False, f"Aspect ratio distortion detected: {current_aspect:.3f} vs base {base_aspect:.3f} (diff {diff:.3f} > {tolerance})"
        return True, None

    def validate_scene_layout_safety(
        self,
        rendered_bbox: Tuple[int, int, int, int],
        canvas_width: int = 1080,
        canvas_height: int = 1920,
        primary_subject_bbox: Optional[Tuple[int, int, int, int]] = None
    ) -> Dict[str, Any]:
        """
        Validates character placement against:
        1. Subtitle safe-zone clearance (y=1640..1820)
        2. Top header / title safe-zone clearance (y=0..240)
        3. Canvas edge clipping
        4. Primary technical subject occlusion
        """
        rx0, ry0, rx1, ry1 = rendered_bbox
        violations: List[str] = []

        # 1. Subtitle collision check
        sx0, sy0, sx1, sy1 = self.SUBTITLE_SAFE_ZONE
        ix0, iy0 = max(rx0, sx0), max(ry0, sy0)
        ix1, iy1 = min(rx1, sx1), min(ry1, sy1)
        if ix0 < ix1 and iy0 < iy1:
            violations.append(
                f"Collision: Character overlaps subtitle safe-zone by {iy1 - iy0}px in y: [{iy0}..{iy1}]."
            )

        # 2. Header collision check
        hx0, hy0, hx1, hy1 = self.HEADER_SAFE_ZONE
        hx_i0, hy_i0 = max(rx0, hx0), max(ry0, hy0)
        hx_i1, hy_i1 = min(rx1, hx1), min(ry1, hy1)
        if hx_i0 < hx_i1 and hy_i0 < hy_i1:
            violations.append(
                f"Collision: Character overlaps header banner safe-zone by {hy_i1 - hy_i0}px."
            )

        # 3. Canvas boundary clipping
        if rx0 < -20:
            violations.append(f"Character severely clipped off left edge: x0={rx0} < -20")
        if rx1 > canvas_width + 20:
            violations.append(f"Character severely clipped off right edge: x1={rx1} > {canvas_width + 20}")
        if ry0 < 0:
            violations.append(f"Character clipped above top canvas boundary: y0={ry0} < 0")

        # 4. Primary subject occlusion check
        if primary_subject_bbox is not None:
            px0, py0, px1, py1 = primary_subject_bbox
            pix0, piy0 = max(rx0, px0), max(ry0, py0)
            pix1, piy1 = min(rx1, px1), min(ry1, py1)
            if pix0 < pix1 and piy0 < piy1:
                overlap_area = (pix1 - pix0) * (piy1 - piy0)
                subject_area = max(1, (px1 - px0) * (py1 - py0))
                occlusion_ratio = overlap_area / float(subject_area)
                if occlusion_ratio > 0.15:
                    violations.append(
                        f"Occlusion: Character covers {occlusion_ratio*100:.1f}% of primary technical subject."
                    )

        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "rendered_bbox": rendered_bbox,
        }

    def validate_scene_character_count(
        self,
        character_configs: List[CharacterSceneConfig]
    ) -> Tuple[bool, Optional[str]]:
        """Ensures that no scene accidentally duplicates the host."""
        active_hosts = [c for c in character_configs if c.appears]
        if len(active_hosts) > 1:
            return False, f"Unexpected character duplication! Found {len(active_hosts)} active hosts in scene."
        return True, None
