"""
SUPER.INTELLIGENCEEE — Visual Intelligence Engine
Generates pre-render creative visual strategies and scene creative briefs.
Ensures every scene has an authentic, independent visual concept, metaphor, and camera direction.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from core.creative_brief import (
    CameraMovement,
    CompositionLayout,
    ProductionMode,
    ReelCreativePlan,
    SceneCreativeBrief,
)

logger = logging.getLogger("super_intelligence.visual_intelligence")


class VisualIntelligenceEngine:
    """
    Transforms script text into an intentional visual storytelling strategy.
    Decouples visual ideas from mere narration text blitting.
    """

    def __init__(self, config=None):
        self.config = config

    def plan_reel_creative(
        self,
        topic: Dict[str, Any],
        script: Optional[Dict[str, Any]] = None,
        storyboard: Optional[Dict[str, Any]] = None,
        scene_audio_durations: Optional[List[float]] = None,
    ) -> ReelCreativePlan:
        """
        Formulates a comprehensive visual strategy with diverse production modes,
        dynamic camera movements, and audio-synchronized scene durations.
        """
        effective_script = script or storyboard or {}
        title = topic.get("title", "AI Systems Milestone")
        topic_id = topic.get("id", 1)
        category = topic.get("category", "Artificial Intelligence")
        scenes_data = effective_script.get("scenes", [])
        if not scenes_data:
            # Fallback if raw 7 sections passed
            sections = ["hook", "context", "development", "explanation", "implications", "limitations", "takeaway"]
            scenes_data = [{"name": s.title(), "narration_text": script.get(s, "")} for s in sections if script.get(s)]

        color_palette = {
            "background": "#0c0f12",       # Deep charcoal obsidian
            "panel": "#141920",            # Elevated dark slate
            "grid": "#222a36",             # Subtle geometric grid
            "cyan_pulse": "#00f0ff",       # Electric neural telemetry
            "amber_gold": "#ffd23f",       # High-contrast insight highlight
            "crimson_alert": "#ff3860",    # Baseline bottleneck strike
            "emerald_gain": "#00e676",     # Verified efficiency gain
            "text_primary": "#ffffff",
            "text_muted": "#8899a6",
        }

        creative_scenes: List[SceneCreativeBrief] = []
        total_duration = 0.0

        # Map each narrative section to a tailored visual concept
        for i, sc in enumerate(scenes_data):
            idx = i + 1
            narr_text = sc.get("narration_text", sc.get("narration", ""))
            dur = scene_audio_durations[i] if (scene_audio_durations and i < len(scene_audio_durations)) else float(sc.get("duration", sc.get("duration_seconds", 6.0)))
            total_duration += dur

            if idx == 1:
                # 1. HOOK: Arrest attention with kinetic visual energy
                brief = SceneCreativeBrief(
                    scene_id=f"scene_{idx:03d}_hook",
                    scene_index=idx,
                    narrative_purpose="Stop the infinite feed scroll within 0.8s; challenge assumption of cloud compute dependency.",
                    intended_emotion="Immediate technical curiosity and urgency.",
                    visual_metaphor="Macro zoom into silicon wafer interconnects pulsing with high-frequency data packets.",
                    primary_subject="High-contrast hardware architecture badge with electric particle drift.",
                    visual_action="Camera executes a slow, deliberate cinematic push-in while particles orbit the core claim.",
                    production_mode=ProductionMode.ORIGINAL_MOTION_GRAPHICS,
                    asset_requirements=["procedural_neural_matrix", "kinetic_headline_overlay"],
                    composition=CompositionLayout.MACRO_CENTER_HERO,
                    camera_movement=CameraMovement.PUSH_IN_SLOW,
                    animation_instructions="Layer 0: slow ambient grid drift; Layer 1: glowing cyan core pulse; Layer 2: bold punch title.",
                    transition_in="fade",
                    transition_out="cross_dissolve",
                    on_screen_text=f"BREAKTHROUGH // {title.upper()[:36]}",
                    duration_seconds=round(dur, 2),
                    factual_claims_represented=[sc.get("on_screen_text", title)],
                    visual_concept_rationale="Establishes immediate high-production value, signaling technical depth without fluff.",
                )

            elif idx == 2:
                # 2. CONTEXT: Establish the real-world engineering bottleneck
                brief = SceneCreativeBrief(
                    scene_id=f"scene_{idx:03d}_context",
                    scene_index=idx,
                    narrative_purpose="Expose the critical pain point: runaway memory growth and infrastructure costs.",
                    intended_emotion="Skepticism turning into analytical engagement.",
                    visual_metaphor="Splitscreen visual bottleneck: server racks burning cloud budget vs lightweight local edge footprint.",
                    primary_subject="Dual-channel comparison matrix highlighting computational complexity curves.",
                    visual_action="Side-by-side vertical split; left channel displays red warning metric, right channel highlights blue edge target.",
                    production_mode=ProductionMode.SPLIT_SCREEN_COMPARISON,
                    asset_requirements=["split_comparison_layout", "cloud_vs_edge_metrics"],
                    composition=CompositionLayout.SPLIT_50_50_VERTICAL,
                    camera_movement=CameraMovement.PAN_HORIZONTAL,
                    animation_instructions="Left pane slides in from left with red boundary; right pane slides in from right with cyan glow.",
                    transition_in="wipe_left",
                    transition_out="cross_dissolve",
                    on_screen_text="THE BOTTLENECK: CLOUD MEMORY SCALING",
                    duration_seconds=round(dur, 2),
                    factual_claims_represented=["Published milestone addresses memory scaling bottlenecks"],
                    visual_concept_rationale="Visualizes the engineering conflict directly so the audience understands the problem stakes.",
                )

            elif idx == 3:
                # 3. DEVELOPMENT: Reveal the breakthrough mechanism
                brief = SceneCreativeBrief(
                    scene_id=f"scene_{idx:03d}_development",
                    scene_index=idx,
                    narrative_purpose="Illustrate the mathematical or algorithmic innovation in action.",
                    intended_emotion="Aha-moment clarity; intellectual satisfaction.",
                    visual_metaphor="Dynamic memory curve: an exponential red curve shoots up while the green sub-quadratic line glides flat.",
                    primary_subject="Animated coordinate chart comparing memory consumption over million-token context length.",
                    visual_action="Data curves draw themselves sequentially across a technical coordinate plane.",
                    production_mode=ProductionMode.DATA_VISUALIZATION,
                    asset_requirements=["svg_coordinate_plot", "animated_curve_overlay"],
                    composition=CompositionLayout.FULL_BLEED_CINEMATIC,
                    camera_movement=CameraMovement.PUSH_IN_SLOW,
                    animation_instructions="Axes fade in at t=0.2s; O(N^2) curve surges to ceiling at t=1.0s; O(N) sub-quadratic curve glides steadily at t=2.0s.",
                    transition_in="fade",
                    transition_out="cross_dissolve",
                    on_screen_text="O(N) LINEAR MEMORY // 1,000,000 TOKENS",
                    duration_seconds=round(dur, 2),
                    factual_claims_represented=["Linear memory scaling across million-token contexts demonstrated"],
                    visual_concept_rationale="Mathematical proof visualized directly: communicates speedup faster than spoken words.",
                )

            elif idx == 4:
                # 4. EXPLANATION: Show actual implementation architecture
                brief = SceneCreativeBrief(
                    scene_id=f"scene_{idx:03d}_explanation",
                    scene_index=idx,
                    narrative_purpose="Provide tangible technical grounding: how the pipeline is constructed.",
                    intended_emotion="Practical builder validation; actionable confidence.",
                    visual_metaphor="Animated system topology flowchart connecting quantization kernels to inference engine.",
                    primary_subject="Interactive block architecture diagram with glowing signal routing.",
                    visual_action="Signal pulses travel through node 01 (Weights) -> node 02 (Kernel) -> node 03 (Engine).",
                    production_mode=ProductionMode.ANIMATED_TECHNICAL_DIAGRAM,
                    asset_requirements=["flowchart_nodes", "svg_arrow_connectors"],
                    composition=CompositionLayout.NETWORK_TOPOLOGY,
                    camera_movement=CameraMovement.DRIFT_SUBTLE,
                    animation_instructions="Active stage illuminates with cyan neon border as signal packet traverses the block diagram.",
                    transition_in="cross_dissolve",
                    transition_out="cross_dissolve",
                    on_screen_text="EXECUTION PIPELINE // ZERO BRUTE FORCE",
                    duration_seconds=round(dur, 2),
                    factual_claims_represented=["Refined algorithmic optimizations replace brute-force compute"],
                    visual_concept_rationale="Proves this is an architectural solution rather than generic marketing claims.",
                )

            elif idx == 5:
                # 5. IMPLICATIONS: Software terminal & developer workflow
                brief = SceneCreativeBrief(
                    scene_id=f"scene_{idx:03d}_implications",
                    scene_index=idx,
                    narrative_purpose="Demonstrate real terminal execution: code, flags, and real-time inference telemetry.",
                    intended_emotion="Excitement to test the code locally.",
                    visual_metaphor="Monospaced hacker terminal executing a localized command-line run on consumer workstation.",
                    primary_subject="IDE / Terminal console window displaying prompt throughput and zero latency spikes.",
                    visual_action="Terminal command types out, followed by instant green telemetry confirmation: 'Latency: 14ms | VRAM: 3.4GB'.",
                    production_mode=ProductionMode.INTERFACE_WALKTHROUGH,
                    asset_requirements=["terminal_window", "typing_cursor_effect"],
                    composition=CompositionLayout.TERMINAL_LOWER_THIRD,
                    camera_movement=CameraMovement.STATIC_LOCKED,
                    animation_instructions="Terminal prompt pulses green; output streams line-by-line; metric badge glows gold.",
                    transition_in="fade",
                    transition_out="cross_dissolve",
                    on_screen_text="$ python run_inference.py --local-edge",
                    duration_seconds=round(dur, 2),
                    factual_claims_represented=["Enables real-time local inference without cloud dependencies"],
                    visual_concept_rationale="Speaks directly to developers in their native visual language (the terminal).",
                )

            elif idx == 6:
                # 6. LIMITATIONS: Critical perspective and boundary stress testing
                brief = SceneCreativeBrief(
                    scene_id=f"scene_{idx:03d}_limitations",
                    scene_index=idx,
                    narrative_purpose="Establish high credibility by acknowledging edge cases and thermal boundaries.",
                    intended_emotion="Trust, respect for editorial objectivity, absence of hype.",
                    visual_metaphor="Technical telemetry HUD displaying stress test bounds and thermal envelope warning indicators.",
                    primary_subject="Industrial diagnostics card displaying boundary test conditions.",
                    visual_action="Border diagnostic grid activates with amber warning markers; text highlights active edge cases.",
                    production_mode=ProductionMode.EDITORIAL_TYPOGRAPHY,
                    asset_requirements=["diagnostic_hud_corners", "amber_warning_pill"],
                    composition=CompositionLayout.ASYMMETRIC_DIAGONAL,
                    camera_movement=CameraMovement.PAN_HORIZONTAL,
                    animation_instructions="Corner bracket HUD elements lock in; caution indicator pulses amber.",
                    transition_in="cross_dissolve",
                    transition_out="cross_dissolve",
                    on_screen_text="STRESS TESTING: EDGE CASES IN PROGRESS",
                    duration_seconds=round(dur, 2),
                    factual_claims_represented=["Edge-case validation and production stress testing still underway"],
                    visual_concept_rationale="Aesthetic shift from cyan/green to amber communicates analytical honesty.",
                )

            elif idx == len(scenes_data):
                # Final Scene: Cinematic conclusion and memorable outro
                brief = SceneCreativeBrief(
                    scene_id=f"scene_{idx:03d}_takeaway",
                    scene_index=idx,
                    narrative_purpose="Deliver a clear philosophical takeaway and crystallize the competitive moat.",
                    intended_emotion="Inspiration, conviction, retention.",
                    visual_metaphor="Full-bleed cinematic motion loop with subtle gold particle vortex and clean typography.",
                    primary_subject="High-impact kinetic outro title with verified provenance stamp.",
                    visual_action="Camera smoothly pulls in as gold particles drift upward into dark void.",
                    production_mode=ProductionMode.CINEMATIC_STOCK,
                    asset_requirements=["procedural_cinematic_motion", "verified_signature_stamp"],
                    composition=CompositionLayout.FULL_BLEED_CINEMATIC,
                    camera_movement=CameraMovement.PUSH_IN_SLOW,
                    animation_instructions="Cinematic background flows continuously; final takeaway animates in with spring easing.",
                    transition_in="cross_dissolve",
                    transition_out="fade",
                    on_screen_text="EFFICIENCY & VERIFICATION ARE THE MOAT",
                    duration_seconds=round(dur, 2),
                    factual_claims_represented=["Efficiency and verified execution are becoming competitive moats"],
                    visual_concept_rationale="Leaves the viewer with an unforgettable final image and clear takeaway.",
                )

            else:
                # Dynamic Middle Scene: Technical diagram or data telemetry
                brief = SceneCreativeBrief(
                    scene_id=f"scene_{idx:03d}_deepdive",
                    scene_index=idx,
                    narrative_purpose=f"Deep-dive technical breakdown of component phase #{idx}.",
                    intended_emotion="Technical clarity and analytical depth.",
                    visual_metaphor="Decoupled vector flow diagram with glowing state transitions.",
                    primary_subject=f"System Diagram Phase {idx}",
                    visual_action="Data nodes animate sequentially with spring easing.",
                    production_mode=ProductionMode.ANIMATED_TECHNICAL_DIAGRAM,
                    asset_requirements=["vector_flow_elements", "accent_cyan_glow"],
                    composition=CompositionLayout.NETWORK_TOPOLOGY,
                    camera_movement=CameraMovement.STATIC_LOCKED,
                    animation_instructions="Nodes illuminate sequentially as narration describes data flow.",
                    transition_in="wipeleft",
                    transition_out="cross_dissolve",
                    on_screen_text=f"PHASE {idx}: ARCHITECTURAL PIPELINE",
                    duration_seconds=round(dur, 2),
                    factual_claims_represented=[sc.get("on_screen_text", f"Phase {idx} Architecture")],
                    visual_concept_rationale="Provides visual structure for complex multi-stage engineering concepts.",
                )

            creative_scenes.append(brief)

        plan = ReelCreativePlan(
            topic_id=topic_id,
            title=title,
            overall_visual_theme="Cyber-Industrial Systems Architecture & Dynamic Mathematical Proofs",
            narrative_pacing_arc="Scroll Interrupt (0-8s) -> Problem Split (8-16s) -> Curve Proof (16-32s) -> Terminal Execution (32-40s) -> Honest Rigor (40-48s) -> Cinematic Moat (48-55s)",
            color_palette=color_palette,
            scenes=creative_scenes,
            total_duration_seconds=round(total_duration, 2),
        )

        logger.info(
            f"Formulated Reel Creative Plan for '{title}': {len(creative_scenes)} scenes across "
            f"{len(set(s.production_mode for s in creative_scenes))} distinct production modes (Total: {plan.total_duration_seconds}s)"
        )
        return plan
