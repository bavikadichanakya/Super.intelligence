"""
SUPER.INTELLIGENCEEE — Visual Diversity & Composition Analyzer
Analyzes DynamicScenePlans to detect repetitive compositions, excessive text density,
consecutive identical scene types, and static pacing before video rendering.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

from core.creative_contracts import DynamicScene, DynamicScenePlan, SceneType

logger = logging.getLogger("super_intelligence.visual_diversity_analyzer")


class VisualDiversityAnalyzer:
    """Evaluates semantic, compositional, and typographical variety across planned scenes."""

    def __init__(self, config=None):
        self.config = config

    def analyze_plan(self, scene_plan: DynamicScenePlan) -> Dict[str, Any]:
        """
        Executes comprehensive diversity and composition inspection.
        Returns score (0.0 to 1.0), issue list, and remediation suggestions.
        """
        scenes = scene_plan.scenes
        total_scenes = len(scenes)
        issues: List[str] = []

        if total_scenes < 2:
            return {
                "diversity_score": 1.0,
                "issues": [],
                "passed": True,
                "scene_count": total_scenes,
                "unique_types": 1,
            }

        # 1. Consecutive Scene Type Duplication Check
        consecutive_duplicates = 0
        for i in range(1, total_scenes):
            if scenes[i].scene_type == scenes[i - 1].scene_type:
                consecutive_duplicates += 1
                issues.append(
                    f"Consecutive identical scene types at Scene #{i} and #{i+1} ({scenes[i].scene_type.value}). "
                    f"Suggest varying visual treatment."
                )

        # 2. Scene-Type Distribution & Variety
        unique_types = len({s.scene_type for s in scenes})
        min_required_unique = 2 if total_scenes <= 3 else 3 if total_scenes <= 6 else 4
        if unique_types < min_required_unique:
            issues.append(
                f"Insufficient visual variety: only {unique_types} unique scene types across {total_scenes} scenes "
                f"(minimum recommended: {min_required_unique})."
            )

        # 3. Excessive On-Screen Text Density Check
        # On-screen text in video reels should be concise (< 12 words / < 70 chars) to prevent crowded slide appearance
        crowded_text_scenes: List[int] = []
        for s in scenes:
            word_count = len(s.on_screen_text.split())
            if word_count > 12 or len(s.on_screen_text) > 75:
                crowded_text_scenes.append(s.sequence)
                issues.append(
                    f"Scene #{s.sequence} has excessive on-screen text ({word_count} words, {len(s.on_screen_text)} chars). "
                    f"Videos must not look like presentation slides; condense on-screen headline."
                )

        # 4. Motion Preset Diversity Check
        unique_motions = len({s.motion_direction for s in scenes})
        if unique_motions < 2 and total_scenes >= 4:
            issues.append(
                f"Monotonous motion presets: all scenes use '{scenes[0].motion_direction}'. "
                f"Incorporate dynamic zoom punches, draw reveals, and slides."
            )

        # 5. Calculate Diversity Score (0.0 to 1.0)
        penalty = (consecutive_duplicates * 0.20) + (len(crowded_text_scenes) * 0.15)
        if unique_types < min_required_unique:
            penalty += 0.25

        score = max(0.1, round(1.0 - penalty, 2))
        passed = score >= 0.65 and consecutive_duplicates == 0 and len(crowded_text_scenes) == 0

        report = {
            "diversity_score": score,
            "passed": passed,
            "total_scenes": total_scenes,
            "unique_types_count": unique_types,
            "unique_types": [t.value for t in {s.scene_type for s in scenes}],
            "consecutive_duplicates_count": consecutive_duplicates,
            "crowded_text_scenes": crowded_text_scenes,
            "issues": issues,
        }

        logger.info(
            f"Visual Diversity Audit: score={score}, passed={passed}, "
            f"unique_types={unique_types}/{total_scenes}, issues={len(issues)}"
        )
        return report

    def remediate_diversity_issues(self, scene_plan: DynamicScenePlan) -> DynamicScenePlan:
        """
        Automatically resolves adjacent duplicates and excessive text length
        to ensure video complies with diversity standards.
        """
        scenes = scene_plan.scenes
        alternatives = [
            SceneType.TECHNICAL_DIAGRAM,
            SceneType.DATA_VISUALIZATION,
            SceneType.CINEMATIC_BROLL,
            SceneType.SCREEN_DEMONSTRATION,
            SceneType.COMPARISON,
            SceneType.KINETIC_TYPOGRAPHY,
            SceneType.ANIMATED_PROCESS,
        ]

        # 1. Resolve adjacent duplicates
        for i in range(1, len(scenes)):
            if scenes[i].scene_type == scenes[i - 1].scene_type:
                next_t = scenes[i + 1].scene_type if i + 1 < len(scenes) else None
                for alt in alternatives:
                    if alt != scenes[i - 1].scene_type and alt != next_t:
                        logger.info(f"Remediated scene #{i+1}: changed from {scenes[i].scene_type.value} to {alt.value}")
                        scenes[i].scene_type = alt
                        scenes[i].camera_direction = "push_in_slow" if alt != SceneType.TECHNICAL_DIAGRAM else "static_locked"
                        scenes[i].motion_direction = "draw_reveal" if alt == SceneType.TECHNICAL_DIAGRAM else "slide_up"
                        break

        # 2. Trim excessive on-screen text
        for s in scenes:
            if len(s.on_screen_text) > 65:
                words = s.on_screen_text.split()
                if len(words) > 8:
                    s.on_screen_text = " ".join(words[:8]) + "..."
                else:
                    s.on_screen_text = s.on_screen_text[:62] + "..."

        return scene_plan

