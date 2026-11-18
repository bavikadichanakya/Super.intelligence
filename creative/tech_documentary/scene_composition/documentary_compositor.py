"""
SUPER.INTELLIGENCEEE — Phase 3.5 Scene Compositor & Dispatcher
Dispatches planned scene blueprints to specialized full-screen motion graphic engines:
- Family A: Full-Bleed Cinematic Footage & Hardware Silicon Matrix (AssetResolver)
- Family B: Systems & Mathematical Vector Flow (VectorDiagramEngine)
- Family C: Real Developer CLI Demonstration (TerminalAnimator)
- Family D: Full-Bleed Editorial Kinetic Typography (KineticTypographyEngine)
- Family E: Content-Driven Comparative Benchmark Data Graphics (HUDTelemetryEngine)
- Scene 6: Distinct Executive Verdict & Synthesis Plate (VerdictEngine)
All engines strictly adhere to light-first theme and continuous active motion (zero static holds).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from core.creative_contracts import DynamicScene, SceneType
from core.config import get_config
from creative.tech_documentary.cinematic_assets.asset_resolver import AssetResolver
from creative.tech_documentary.kinetic_typography.kinetic_engine import KineticTypographyEngine
from creative.tech_documentary.motion_graphics.hud_telemetry import HUDTelemetryEngine
from creative.tech_documentary.screen_demonstration.terminal_animator import TerminalAnimator
from creative.tech_documentary.technical_diagrams.vector_diagram_engine import VectorDiagramEngine
from creative.tech_documentary.verdict.verdict_engine import VerdictEngine

logger = logging.getLogger("super_intelligence.documentary_compositor")


class DocumentaryCompositor:
    """Dispatches scene blueprints to specialized full-screen rendering engines."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.output_dir = self.config.resolve_path("output/drafts/scenes")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.asset_resolver = AssetResolver(config=self.config)
        self.diagram_engine = VectorDiagramEngine()
        self.terminal_animator = TerminalAnimator()
        self.hud_engine = HUDTelemetryEngine()
        self.kinetic_engine = KineticTypographyEngine()
        self.verdict_engine = VerdictEngine()

    def render_scene(
        self,
        scene: Union[DynamicScene, Dict[str, Any]],
        scene_index: int,
        reel_slug: str,
        topic_title: str = "Technology Breakthrough",
    ) -> Path:
        """Renders an individual scene clip using the appropriate visual archetype engine."""
        if isinstance(scene, DynamicScene):
            st = scene.scene_type
            dur = float(scene.duration_seconds or 5.0)
            headline = scene.on_screen_text or topic_title
            desc = scene.visual_description
            role = getattr(scene, "narrative_role", getattr(scene, "scene_objective", "SCENE"))
            narration = getattr(scene, "narration", "")
            cmd_override = getattr(scene, "command", None)
            stat_override = getattr(scene, "stat_number", None)
            hl_override = getattr(scene, "highlight_keyword", None)
            cit_override = getattr(scene, "citation", None)
            telem_override = getattr(scene, "telemetry", None)
            sub_override = getattr(scene, "sub_header", None)
        else:
            raw_st = scene.get("scene_type", scene.get("visual_archetype", "SCREEN_DEMONSTRATION"))
            try:
                st = SceneType(raw_st) if isinstance(raw_st, str) else raw_st
            except ValueError:
                st = SceneType.SCREEN_DEMONSTRATION
            dur = float(scene.get("duration_seconds", scene.get("duration", 5.0)))
            headline = scene.get("on_screen_text", scene.get("headline", scene.get("title", topic_title)))
            desc = scene.get("visual_description", scene.get("description", ""))
            role = scene.get("narrative_role", f"SCENE_{scene_index}")
            narration = scene.get("narration_text", scene.get("narration", ""))
            cmd_override = scene.get("command")
            stat_override = scene.get("stat_number")
            hl_override = scene.get("highlight_keyword")
            cit_override = scene.get("citation")
            telem_override = scene.get("telemetry")
            sub_override = scene.get("sub_header")

        dur = max(2.5, dur)
        clip_path = self.output_dir / f"{reel_slug}_scene_{scene_index:02d}_{role.lower()}.mp4"

        logger.info(f"Composing Phase 3.5 Scene #{scene_index} [{st.value}] ({dur:.2f}s) -> {clip_path.name}")

        # 1. Family C: Real Developer CLI Demonstration
        if st in (SceneType.SCREEN_DEMONSTRATION, SceneType.PRODUCT_DEMONSTRATION):
            cmd = cmd_override or "vllm serve Llama-3-70b --speculative-model Llama-3-8b --spec-tokens 4"
            return self.terminal_animator.render_terminal_clip(
                output_path=clip_path,
                command=cmd,
                duration_seconds=dur,
                topic_header=headline[:36] or "LIVE INFERENCE VERIFICATION",
                sub_header=sub_override or desc[:56] or "vLLM Speculative Engine on NVIDIA A100-SXM4-80GB",
                telemetry=telem_override or "CUDA 12.4 | A100-80GB | ACCEPTANCE RATE 78.4% | FP16 PARITY",
            )

        # 2. Family B: Full-Screen Systems Vector Diagram
        elif st in (SceneType.TECHNICAL_DIAGRAM, SceneType.ANIMATED_PROCESS):
            return self.diagram_engine.render_diagram_clip(
                output_path=clip_path,
                duration_seconds=dur,
                topic_header=headline[:36] or "SPECULATIVE VERIFICATION TREE",
                sub_header=sub_override or desc[:56] or "Draft Model Emits K=4 Tokens; Target Model Verifies in 1 Parallel Pass",
                telemetry=telem_override or "REJECTION SAMPLING: min(1, p/q) // EXACT PROBABILITY MATCH // P=1.0",
            )

        # 3. Family E: Content-Driven Comparative Benchmark Data Graphics
        elif st in (SceneType.DATA_VISUALIZATION,):
            return self.hud_engine.render_metric_hud_clip(
                output_path=clip_path,
                topic_header=headline[:36] or "EMPIRICAL INFERENCE BENCHMARKS",
                sub_header=sub_override or desc[:56] or "Llama-3-70B Target + 1B Draft: Standard vs Speculative Decoding",
                duration_seconds=dur,
                telemetry=telem_override or "BENCHMARK SUITE: NVIDIA A100 80GB // 100% REASONING PARITY",
            )

        # 4. Family D: Full-Bleed Editorial Kinetic Typography (Hook / Breakthrough)
        elif st in (SceneType.KINETIC_TYPOGRAPHY,):
            return self.kinetic_engine.render_kinetic_clip(
                output_path=clip_path,
                primary_text=headline or "SPECULATIVE DECODING ACCELERATION",
                highlight_keyword=hl_override or "SPECULATIVE",
                stat_number=stat_override or "3.2x",
                sub_text=desc[:90] or "Draft verifier models break autoregressive memory latency without quality loss.",
                category="SYSTEMS ARCHITECTURE",
                citation=cit_override or "SOURCE: LEVIATHAN ET AL. // FAST INFERENCE VIA SPECULATIVE DECODING",
                duration_seconds=dur,
            )

        # 5. Family A: Full-Bleed Cinematic Footage & Hardware Matrix
        elif st in (SceneType.CINEMATIC_BROLL, SceneType.UI_CLOSEUP):
            broll_info = self.asset_resolver.resolve_broll_clip(
                duration_seconds=dur,
                topic="GPU ARITHMETIC INTENSITY ROOFLINE",
                output_path=clip_path,
            )
            return Path(broll_info["path"])

        # 6. Scene 6 (Verdict & Conclusion): Distinct Full-Screen Executive Verdict Plate (Never repeats Scene 1)
        else:
            return self.verdict_engine.render_verdict_clip(
                output_path=clip_path,
                topic_header=headline[:36] or "THE SPECULATIVE INFERENCE VERDICT",
                sub_header=sub_override or desc[:60] or "Architectural Synthesis on Draft-Verifier Decoding",
                duration_seconds=dur,
                telemetry=telem_override or "SYSTEMS SUMMARY: EXACT TARGET DISTRIBUTION // 3.2X SPEEDUP",
            )
