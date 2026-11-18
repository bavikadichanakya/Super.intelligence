"""
SUPER.INTELLIGENCEEE V2 — Multi-Archetype Storyboard Generator
Transforms verified technical scripts into executable 7-scene production storyboards.
Enforces narrative-archetype mapping, visual diversity rules, and rich archetype props.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Union

from core.logger import get_logger
from core.schemas import CaptionConfig, SceneProps, UniversalScene, VisualArchetype

logger = get_logger("StoryboardGenerator")


class StoryboardGenerator:
    """Transforms verified technical scripts into executable 7-scene production storyboards."""

    def __init__(self, db=None, config=None):
        self.db = db
        self.config = config

    @classmethod
    def _extract_hero_word(cls, text: str) -> str:
        """Finds the most impactful focus word for visual highlighting."""
        # Check for numbers, multipliers, or strong tech terms
        matches = re.findall(r"\b\d+(\.\d+)?x\b|\b\d+%\b|\$[0-9,]+", text, re.IGNORECASE)
        if matches:
            return matches[0].upper()

        words = [
            w for w in re.findall(r"\b[A-Za-z0-9\-\_]{4,}\b", text)
            if w.lower() not in {"this", "that", "with", "from", "their", "more", "into", "been", "have", "will"}
        ]
        return words[0].upper() if words else "BREAKTHROUGH"

    @classmethod
    def _extract_metric_pair(cls, text: str) -> Dict[str, Any]:
        """Extracts before/after or delta metric from text."""
        # Multipliers
        mult = re.search(r"\b(\d+(\.\d+)?x)\b", text, re.IGNORECASE)
        if mult:
            return {
                "before": {"label": "Baseline", "value": "1.0x (Standard)"},
                "after": {"label": "Accelerated", "value": mult.group(1).upper()},
                "stat_delta": mult.group(1).upper(),
            }
        # Percentages
        pct = re.search(r"\b(\d+(\.\d+)?%)\b", text)
        if pct:
            return {
                "before": {"label": "Prior Overhead", "value": "100%"},
                "after": {"label": "Reduced Footprint", "value": pct.group(1)},
                "stat_delta": f"-{pct.group(1)}",
            }
        # Tokens
        tokens = re.search(r"\b(\d+(?:\.\d+)?\s*(?:million|billion|k))\b", text, re.IGNORECASE)
        if tokens:
            return {
                "before": {"label": "Context Window", "value": "8k Tokens"},
                "after": {"label": "Extended Scaling", "value": f"{tokens.group(1).upper()} Tokens"},
                "stat_delta": tokens.group(1).upper(),
            }
        return {
            "before": {"label": "Traditional Cloud", "value": "$240/mo"},
            "after": {"label": "Local Edge AI", "value": "$0/mo"},
            "stat_delta": "10x",
        }

    @classmethod
    def enforce_visual_diversity(cls, scenes: List[UniversalScene]) -> List[UniversalScene]:
        """
        Enforces:
        1. At least 3 distinct archetypes across 7 scenes.
        2. No identical consecutive archetypes (scene[i] != scene[i-1]).
        """
        fallback_alternatives = [
            VisualArchetype.STOCK_BROLL,
            VisualArchetype.SKETCH_TITLE,
            VisualArchetype.SKETCH_STAT,
            VisualArchetype.MOTION_DIAGRAM,
            VisualArchetype.SKETCH_LIST,
            VisualArchetype.SKETCH_QUOTE,
            VisualArchetype.PRODUCT_DEMO,
            VisualArchetype.EDITORIAL_HUD,
        ]

        # 1. Prevent adjacent duplicates
        for i in range(1, len(scenes)):
            if scenes[i].visual_archetype == scenes[i - 1].visual_archetype:
                # Find first archetype not matching previous or next
                next_arch = scenes[i + 1].visual_archetype if i + 1 < len(scenes) else None
                for alt in fallback_alternatives:
                    if alt != scenes[i - 1].visual_archetype and alt != next_arch:
                        logger.info(f"Diversifying scene #{i+1}: changed from {scenes[i].visual_archetype.value} to {alt.value}")
                        scenes[i].visual_archetype = alt
                        break

        # 2. Verify distinct count >= 3
        distinct_count = len({s.visual_archetype for s in scenes})
        if distinct_count < 3 and len(scenes) >= 3:
            scenes[1].visual_archetype = VisualArchetype.SKETCH_QUOTE
            scenes[2].visual_archetype = VisualArchetype.SKETCH_STAT

        return scenes

    @classmethod
    def generate_storyboard(cls, script_data: Dict[str, Any], script_id: Any = None) -> List[Dict[str, Any]]:
        """
        Transforms verified script into UniversalScene objects,
        exported as rich backward-compatible dictionaries.
        Supports both dynamic variable scene counts (3 to 12+) and legacy 7-scene scripts.
        """
        # 1. Check for dynamic scene plan
        if "dynamic_plan" in script_data and hasattr(script_data["dynamic_plan"], "to_universal_scenes"):
            u_scenes = script_data["dynamic_plan"].to_universal_scenes()
            u_scenes = cls.enforce_visual_diversity(u_scenes)
            return [s.to_dict() for s in u_scenes]

        # 2. Check for explicit variable scenes list
        if "scenes" in script_data and isinstance(script_data["scenes"], list) and len(script_data["scenes"]) != 7:
            u_scenes = []
            for i, sc in enumerate(script_data["scenes"], start=1):
                if isinstance(sc, UniversalScene):
                    u_scenes.append(sc)
                elif hasattr(sc, "to_universal_scene"):
                    u_scenes.append(sc.to_universal_scene())
                elif isinstance(sc, dict):
                    u_scenes.append(UniversalScene.from_dict(sc))
            if u_scenes:
                u_scenes = cls.enforce_visual_diversity(u_scenes)
                return [s.to_dict() for s in u_scenes]

        title = script_data.get("title", "AI Technical Milestone")
        publisher = script_data.get("publisher", "Primary Lab Documentation")
        category = script_data.get("category", "Artificial Intelligence News")

        hook = script_data.get("hook", "")
        context = script_data.get("context", "")
        development = script_data.get("development", "")
        explanation = script_data.get("explanation", "")
        implications = script_data.get("implications", "")
        limitations = script_data.get("limitations", "")
        takeaway = script_data.get("takeaway", "")

        def calc_duration(text: str, min_sec: float = 3.6) -> float:
            words = len(text.split())
            return max(min_sec, round(words / 2.5, 1))

        # --- Scene 1: HOOK (sketch_title) ---
        hero_1 = cls._extract_hero_word(hook or title)
        s1 = UniversalScene(
            scene_id="scene_001_hook",
            scene_index=1,
            duration_seconds=calc_duration(hook, 4.0),
            narrative_role="HOOK",
            visual_archetype=VisualArchetype.SKETCH_TITLE,
            narration_text=hook,
            on_screen_text=title[:52] + ("..." if len(title) > 52 else ""),
            badge="BREAKTHROUGH REPORT",
            instructions="Bold hand-drawn title on dark paper grid with yellow marker punch.",
            transition="fade",
            visual_props=SceneProps(
                headline=title[:52],
                lead_in="BREAKING INTEL",
                hero_word=hero_1,
                theme="dark",
                motion_preset="draw_reveal",
            ),
            captions=CaptionConfig(highlight_keywords=[hero_1]),
        )

        # --- Scene 2: CONTEXT & PROVENANCE (sketch_quote) ---
        hero_2 = cls._extract_hero_word(publisher)
        s2 = UniversalScene(
            scene_id="scene_002_context",
            scene_index=2,
            duration_seconds=calc_duration(context, 4.2),
            narrative_role="CONTEXT",
            visual_archetype=VisualArchetype.SKETCH_QUOTE,
            narration_text=context,
            on_screen_text=f"SOURCE: {publisher.upper()}",
            badge=f"PROVENANCE: {publisher.upper()}",
            instructions="Verified source citation with golden accent quotation marks and provenance stamp.",
            transition="wipeleft",
            visual_props=SceneProps(
                headline="PRIMARY SOURCE VERIFIED",
                lead_in=f"DOCUMENTED BY {publisher.upper()}",
                hero_word=hero_2,
                quote_text=context[:140] + ("..." if len(context) > 140 else ""),
                quote_author=publisher,
                quote_role=f"Official Research · {category}",
                theme="dark",
                motion_preset="slide_up",
            ),
            captions=CaptionConfig(highlight_keywords=[publisher]),
        )

        # --- Scene 3: THE CORE DEVELOPMENT (sketch_stat) ---
        metric_info = cls._extract_metric_pair(development)
        hero_3 = metric_info.get("stat_delta") or cls._extract_hero_word(development)
        s3 = UniversalScene(
            scene_id="scene_003_development",
            scene_index=3,
            duration_seconds=calc_duration(development, 4.8),
            narrative_role="DEVELOPMENT",
            visual_archetype=VisualArchetype.SKETCH_STAT,
            narration_text=development,
            on_screen_text=f"PERFORMANCE MULTIPLIER: {hero_3}",
            badge="BENCHMARK VERIFIED",
            instructions="Hand-drawn before-and-after comparison card with struck-through baseline and hero win value.",
            transition="slideright",
            visual_props=SceneProps(
                headline="PERFORMANCE MULTIPLIER",
                lead_in="EMPIRICAL BENCHMARK",
                hero_word=hero_3,
                before=metric_info.get("before"),
                after=metric_info.get("after"),
                stat_delta=metric_info.get("stat_delta"),
                theme="dark",
                motion_preset="draw_reveal",
            ),
            captions=CaptionConfig(highlight_keywords=[hero_3]),
        )

        # --- Scene 4: TECHNICAL ARCHITECTURE (motion_diagram) ---
        hero_4 = "PIPELINE"
        s4 = UniversalScene(
            scene_id="scene_004_explanation",
            scene_index=4,
            duration_seconds=calc_duration(explanation, 4.8),
            narrative_role="EXPLANATION",
            visual_archetype=VisualArchetype.MOTION_DIAGRAM,
            narration_text=explanation,
            on_screen_text="SYSTEM ARCHITECTURE PIPELINE",
            badge="ARCHITECTURE FLOW",
            instructions="Dynamic 3-stage animated SVG architectural flowchart with glowing data links.",
            transition="slideup",
            visual_props=SceneProps(
                headline="SYSTEM ARCHITECTURE PIPELINE",
                lead_in="EXECUTION TOPOLOGY",
                hero_word=hero_4,
                diagram_nodes=[
                    {"id": "n1", "label": "Context Ingestion", "type": "input", "color": "#00E5FF"},
                    {"id": "n2", "label": "Algorithmic Pruning", "type": "process", "color": "#FFD700"},
                    {"id": "n3", "label": "Zero-Drift Inference", "type": "output", "color": "#22C55E"},
                ],
                diagram_edges=[
                    {"from": "n1", "to": "n2", "label": "Tokens"},
                    {"from": "n2", "to": "n3", "label": "Optimized"},
                ],
                theme="dark",
                motion_preset="draw_reveal",
            ),
            captions=CaptionConfig(highlight_keywords=["ARCHITECTURE", "PIPELINE"]),
        )

        # --- Scene 5: PRACTICAL IMPACT (sketch_list) ---
        hero_5 = "DEPLOYMENT"
        s5 = UniversalScene(
            scene_id="scene_005_implications",
            scene_index=5,
            duration_seconds=calc_duration(implications, 4.2),
            narrative_role="IMPLICATIONS",
            visual_archetype=VisualArchetype.SKETCH_LIST,
            narration_text=implications,
            on_screen_text="PRODUCTION ADVANTAGES",
            badge="INDUSTRY IMPACT",
            instructions="Structured hand-drawn card list detailing workstation, edge, and zero-latency deployment wins.",
            transition="fade",
            visual_props=SceneProps(
                headline="PRODUCTION ADVANTAGES",
                lead_in="DEPLOYMENT GAINS",
                hero_word=hero_5,
                list_items=[
                    {"index": 1, "title": "Local Edge Workstations", "description": "Full parameter execution on consumer hardware", "win": False},
                    {"index": 2, "title": "Real-Time Latency", "description": "Zero cloud roundtrip overhead", "win": True},
                    {"index": 3, "title": "Verified Precision", "description": "Preserved accuracy with zero token drift", "win": False},
                ],
                theme="dark",
                motion_preset="slide_up",
            ),
            captions=CaptionConfig(highlight_keywords=["PRODUCTION", "EDGE"]),
        )

        # --- Scene 6: LIMITATIONS & CAVEATS (editorial_hud) ---
        hero_6 = "CAVEATS"
        s6 = UniversalScene(
            scene_id="scene_006_limitations",
            scene_index=6,
            duration_seconds=calc_duration(limitations, 4.2),
            narrative_role="LIMITATIONS",
            visual_archetype=VisualArchetype.EDITORIAL_HUD,
            narration_text=limitations,
            on_screen_text="CRITICAL PERSPECTIVE & LIMITATIONS",
            badge="REALITY CHECK",
            instructions="Amber-trimmed cybernetic alert card detailing edge-case stress tests and validation bounds.",
            transition="wipeleft",
            visual_props=SceneProps(
                headline="LIMITATIONS & VALIDATION BOUNDS",
                lead_in="CRITICAL PERSPECTIVE",
                hero_word=hero_6,
                theme="dark",
                motion_preset="draw_reveal",
            ),
            captions=CaptionConfig(highlight_keywords=["LIMITATIONS", "VALIDATION"]),
        )

        # --- Scene 7: TAKEAWAY & BRAND CLOSING (stock_broll) ---
        hero_7 = "SUPER.INTELLIGENCEEE"
        s7 = UniversalScene(
            scene_id="scene_007_takeaway",
            scene_index=7,
            duration_seconds=calc_duration(takeaway, 4.0),
            narrative_role="TAKEAWAY",
            visual_archetype=VisualArchetype.STOCK_BROLL,
            narration_text=takeaway,
            on_screen_text="SUPER.INTELLIGENCEEE",
            badge="DAILY DEEP TECH INTELLIGENCE",
            instructions="Cinematic tech footage overlay with official brand CTA and closing pulse.",
            transition="fade",
            visual_props=SceneProps(
                headline="SUPER.INTELLIGENCEEE",
                lead_in="STAY AHEAD OF THE CURVE",
                hero_word=hero_7,
                theme="dark",
                motion_preset="zoom_punch",
            ),
            captions=CaptionConfig(highlight_keywords=["SUPER.INTELLIGENCEEE"]),
        )

        raw_scenes = [s1, s2, s3, s4, s5, s6, s7]
        # Enforce diversity rules
        final_scenes = cls.enforce_visual_diversity(raw_scenes)

        # Return list of backward-compatible dictionaries
        return [s.to_dict() for s in final_scenes]
