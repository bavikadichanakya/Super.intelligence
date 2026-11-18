"""
SUPER.INTELLIGENCEEE — Visual Metaphor Engine
Maps decomposed technical concepts to authentic, full-bleed visual metaphors
and compositional paradigms. Eradicates the card-box and dashboard anti-patterns.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from creative.visual_intelligence.concept_decomposer import TechnicalConceptBreakdown, TechnicalDomain

logger = logging.getLogger("super_intelligence.visual_metaphor_engine")


class VisualMetaphorType(str, Enum):
    # AI / Latent Space / Model Architecture Metaphors
    REASONING_CHAIN_EXPANSION = "reasoning_chain_expansion"
    NEURAL_TENSOR_FLOW = "neural_tensor_flow"
    VERIFICATION_REWARD_LATTICE = "verification_reward_lattice"
    KV_CACHE_PAGINATION = "kv_cache_pagination"

    # Cybersecurity / Kernel Systems Metaphors
    KERNEL_RING_BOUNDARY = "kernel_ring_boundary"
    BYTECODE_VERIFIER_GRAPH = "bytecode_verifier_graph"
    MEMORY_CORRUPTION_MAP = "memory_corruption_map"
    TRACEPOINT_INTERCEPTION = "tracepoint_interception"

    # Hardware / Compiler / GPU Metaphors
    MEMORY_HIERARCHY_PIPELINE = "memory_hierarchy_pipeline"
    ASYNCHRONOUS_TENSOR_WARP = "asynchronous_tensor_warp"
    CACHE_LINE_CONCURRENCY = "cache_line_concurrency"
    HARDWARE_REGISTER_MESH = "hardware_register_mesh"

    # Authentic Evidence Anchors
    PRIMARY_EVIDENCE_DEEP_ZOOM = "primary_evidence_deep_zoom"
    COMPARATIVE_BENCHMARK_MATRIX = "comparative_benchmark_matrix"
    CIRCULAR_LOOP_TAKEOUT = "circular_loop_takeout"


@dataclass
class VisualMetaphorAssignment:
    scene_id: str
    beat_name: str
    metaphor_type: VisualMetaphorType
    theme_mode: str  # "dark" or "light"
    hero_object_description: str
    camera_movement_type: str  # "slow_zoom_in", "pan_right", "macro_isolate", "parallax_tilt"
    kinetic_focus_noun: str
    kinetic_italic_keyword: str
    color_accents: Dict[str, str]
    parameters: Dict[str, Any]


class VisualMetaphorEngine:
    """
    Selects mathematically and visually appropriate representations for each concept
    based on the technical domain and cause-and-effect attributes.
    """

    def __init__(self):
        pass

    def assign_metaphors(self, breakdown: TechnicalConceptBreakdown) -> List[VisualMetaphorAssignment]:
        """
        Derives an ordered sequence of visually diverse, topic-native metaphors
        for each narrative beat of the breakdown.
        """
        domain = breakdown.domain
        assignments: List[VisualMetaphorAssignment] = []

        if domain == TechnicalDomain.AI_MODEL_ARCHITECTURE:
            assignments = self._plan_ai_model_metaphors(breakdown)
        elif domain == TechnicalDomain.CYBERSECURITY_SYSTEMS:
            assignments = self._plan_cybersecurity_metaphors(breakdown)
        elif domain == TechnicalDomain.HARDWARE_COMPILER:
            assignments = self._plan_hardware_compiler_metaphors(breakdown)
        else:
            assignments = self._plan_generic_systems_metaphors(breakdown)

        logger.info(
            f"VisualMetaphorEngine: Generated {len(assignments)} metaphor assignments for topic '{breakdown.topic_name}' ({domain.value})"
        )
        return assignments

    def _plan_ai_model_metaphors(self, b: TechnicalConceptBreakdown) -> List[VisualMetaphorAssignment]:
        """Plans visual beats for AI Model Architecture (e.g., DeepSeek-R1, Latent Reasoning)."""
        return [
            # Beat 1: Dark Hook - The Emergence of Pure Reasoning
            VisualMetaphorAssignment(
                scene_id="scene_01_hook",
                beat_name="Reasoning Paradigm Shift",
                metaphor_type=VisualMetaphorType.REASONING_CHAIN_EXPANSION,
                theme_mode="dark",
                hero_object_description="Branching 3D thought tree with pulsing incandescent token nodes",
                camera_movement_type="slow_zoom_in",
                kinetic_focus_noun="[latent reasoning]",
                kinetic_italic_keyword="thinks",
                color_accents={"primary": "#38BDF8", "accent": "#818CF8", "bg": "#0A0D14"},
                parameters={"branch_depth": 5, "pulse_frequency": 2.5, "metric_label": b.key_metrics.get("compute_scale", "100x")},
            ),
            # Beat 2: Light Plane - The Traditional Limitation (Supervised Fine-Tuning Bottleneck)
            VisualMetaphorAssignment(
                scene_id="scene_02_problem",
                beat_name="Human Data Bottleneck",
                metaphor_type=VisualMetaphorType.VERIFICATION_REWARD_LATTICE,
                theme_mode="light",
                hero_object_description="SFT plateau boundary with constrained human demonstration limits",
                camera_movement_type="macro_isolate",
                kinetic_focus_noun="[human limits]",
                kinetic_italic_keyword="plateaus",
                color_accents={"primary": "#EF4444", "accent": "#0F172A", "bg": "#E5E5E0"},
                parameters={"bottleneck_ceiling": 0.65, "error_nodes_count": 8},
            ),
            # Beat 3: Light Plane - Pure RL Cold Start (Aha Moment)
            VisualMetaphorAssignment(
                scene_id="scene_03_mechanism",
                beat_name="Autonomous Chain-of-Thought",
                metaphor_type=VisualMetaphorType.NEURAL_TENSOR_FLOW,
                theme_mode="light",
                hero_object_description="Self-correcting backtracks dynamically pruning invalid proof paths",
                camera_movement_type="pan_right",
                kinetic_focus_noun="[self evolution]",
                kinetic_italic_keyword="learns",
                color_accents={"primary": "#059669", "accent": "#0284C7", "bg": "#E5E5E0"},
                parameters={"active_beams": 4, "pruned_branches": 12, "convergence_speed": 1.8},
            ),
            # Beat 4: Light Plane - Primary Source & Benchmark Proof
            VisualMetaphorAssignment(
                scene_id="scene_04_evidence",
                beat_name="AIME & MATH-500 Validation",
                metaphor_type=VisualMetaphorType.COMPARATIVE_BENCHMARK_MATRIX,
                theme_mode="light",
                hero_object_description="Dynamic 3D benchmark bars rising from 15.6% to 79.8% on AIME 2024",
                camera_movement_type="slow_zoom_in",
                kinetic_focus_noun="[AIME 2024]",
                kinetic_italic_keyword="proves",
                color_accents={"primary": "#0284C7", "accent": "#10B981", "bg": "#E5E5E0"},
                parameters={"baseline_score": 15.6, "achieved_score": 79.8, "target_label": "DeepSeek-R1"},
            ),
            # Beat 5: Light Plane - Test-Time Compute Scaling
            VisualMetaphorAssignment(
                scene_id="scene_05_scaling",
                beat_name="Test-Time Compute Expansion",
                metaphor_type=VisualMetaphorType.KV_CACHE_PAGINATION,
                theme_mode="light",
                hero_object_description="Logarithmic compute curve with expanding token allocations per question",
                camera_movement_type="parallax_tilt",
                kinetic_focus_noun="[inference compute]",
                kinetic_italic_keyword="scales",
                color_accents={"primary": "#6366F1", "accent": "#0F172A", "bg": "#E5E5E0"},
                parameters={"scaling_ratio": "32k tokens", "accuracy_gain": "+42%"},
            ),
            # Beat 6: Dark Loop Takeaway
            VisualMetaphorAssignment(
                scene_id="scene_06_loop",
                beat_name="Open Weights Revolution",
                metaphor_type=VisualMetaphorType.CIRCULAR_LOOP_TAKEOUT,
                theme_mode="dark",
                hero_object_description="Universal reasoning core glowing on dark field, connecting to start",
                camera_movement_type="slow_zoom_in",
                kinetic_focus_noun="[open weights]",
                kinetic_italic_keyword="forever",
                color_accents={"primary": "#38BDF8", "accent": "#F59E0B", "bg": "#0A0D14"},
                parameters={"repo_stars": "DeepSeek-R1", "license": "MIT Open Source"},
            ),
        ]

    def _plan_cybersecurity_metaphors(self, b: TechnicalConceptBreakdown) -> List[VisualMetaphorAssignment]:
        """Plans visual beats for Cybersecurity & Systems (e.g., eBPF Kernel Verifier Exploitation)."""
        return [
            # Beat 1: Dark Hook - Ring 0 Kernel Execution
            VisualMetaphorAssignment(
                scene_id="scene_01_hook",
                beat_name="Kernel Space Privilege",
                metaphor_type=VisualMetaphorType.KERNEL_RING_BOUNDARY,
                theme_mode="dark",
                hero_object_description="Concentric glowing security rings with Ring 0 core pulsating at center",
                camera_movement_type="slow_zoom_in",
                kinetic_focus_noun="[Ring 0 kernel]",
                kinetic_italic_keyword="controls",
                color_accents={"primary": "#F43F5E", "accent": "#38BDF8", "bg": "#0A0D14"},
                parameters={"ring_levels": 4, "core_pulse": True, "target": "Linux Kernel"},
            ),
            # Beat 2: Light Plane - The Verifier Safety Gate
            VisualMetaphorAssignment(
                scene_id="scene_02_verifier",
                beat_name="Static Verification Boundary",
                metaphor_type=VisualMetaphorType.BYTECODE_VERIFIER_GRAPH,
                theme_mode="light",
                hero_object_description="eBPF register bounds analysis graph checking pointer arithmetic safety",
                camera_movement_type="pan_right",
                kinetic_focus_noun="[BPF verifier]",
                kinetic_italic_keyword="inspects",
                color_accents={"primary": "#059669", "accent": "#0F172A", "bg": "#E5E5E0"},
                parameters={"insn_count": 4096, "checked_branches": 256},
            ),
            # Beat 3: Light Plane - The 32-bit Truncation Exploit
            VisualMetaphorAssignment(
                scene_id="scene_03_exploit",
                beat_name="Register Truncation Flaw",
                metaphor_type=VisualMetaphorType.MEMORY_CORRUPTION_MAP,
                theme_mode="light",
                hero_object_description="Upper 32-bit register masking creating divergent verifier vs runtime state",
                camera_movement_type="macro_isolate",
                kinetic_focus_noun="[bit truncation]",
                kinetic_italic_keyword="bypasses",
                color_accents={"primary": "#DC2626", "accent": "#B91C1C", "bg": "#E5E5E0"},
                parameters={"reg_source": "R1 (64-bit)", "truncated_val": "0x00000000", "actual_val": "0x100000000"},
            ),
            # Beat 4: Light Plane - Arbitrary Kernel Memory Read/Write
            VisualMetaphorAssignment(
                scene_id="scene_04_arbitrary_rw",
                beat_name="Arbitrary Memory Access",
                metaphor_type=VisualMetaphorType.TRACEPOINT_INTERCEPTION,
                theme_mode="light",
                hero_object_description="Out-of-bounds pointer traversal writing into cred struct for root UID 0",
                camera_movement_type="slow_zoom_in",
                kinetic_focus_noun="[root privilege]",
                kinetic_italic_keyword="overwrites",
                color_accents={"primary": "#D97706", "accent": "#0F172A", "bg": "#E5E5E0"},
                parameters={"target_struct": "struct cred", "new_uid": 0, "verified_safe": False},
            ),
            # Beat 5: Light Plane - Kernel Patch & Verification Armor
            VisualMetaphorAssignment(
                scene_id="scene_05_remediation",
                beat_name="Mitigation & Constant Blinding",
                metaphor_type=VisualMetaphorType.BYTECODE_VERIFIER_GRAPH,
                theme_mode="light",
                hero_object_description="Armored 64-bit ALU bounds propagation blocking tainted pointer manipulation",
                camera_movement_type="pan_right",
                kinetic_focus_noun="[kernel patch]",
                kinetic_italic_keyword="hardens",
                color_accents={"primary": "#2563EB", "accent": "#059669", "bg": "#E5E5E0"},
                parameters={"patch_commit": "CVE-2023-2163", "status": "UPSTREAM SECURED"},
            ),
            # Beat 6: Dark Loop Conclusion
            VisualMetaphorAssignment(
                scene_id="scene_06_loop",
                beat_name="The Systems Arms Race",
                metaphor_type=VisualMetaphorType.CIRCULAR_LOOP_TAKEOUT,
                theme_mode="dark",
                hero_object_description="Hardened kernel shield glowing against cyber threats, looping back to Ring 0",
                camera_movement_type="slow_zoom_in",
                kinetic_focus_noun="[kernel boundary]",
                kinetic_italic_keyword="defends",
                color_accents={"primary": "#38BDF8", "accent": "#10B981", "bg": "#0A0D14"},
                parameters={"security_model": "eBPF Safe Virtualization"},
            ),
        ]

    def _plan_hardware_compiler_metaphors(self, b: TechnicalConceptBreakdown) -> List[VisualMetaphorAssignment]:
        """Plans visual beats for Hardware & GPU Compilers (e.g., FlashAttention-3 Hopper Asynchrony)."""
        return [
            # Beat 1: Dark Hook - The Memory Wall Bottleneck
            VisualMetaphorAssignment(
                scene_id="scene_01_hook",
                beat_name="High-Bandwidth Memory Wall",
                metaphor_type=VisualMetaphorType.MEMORY_HIERARCHY_PIPELINE,
                theme_mode="dark",
                hero_object_description="Towering HBM3 memory stacks bottlenecked by high memory roundtrip latency",
                camera_movement_type="slow_zoom_in",
                kinetic_focus_noun="[memory wall]",
                kinetic_italic_keyword="stalls",
                color_accents={"primary": "#F59E0B", "accent": "#38BDF8", "bg": "#0A0D14"},
                parameters={"hbm_bandwidth": "3.35 TB/s", "compute_flops": "1,000 TFLOPS", "gap_ratio": "300x"},
            ),
            # Beat 2: Light Plane - Traditional Attention GEMM Overhead
            VisualMetaphorAssignment(
                scene_id="scene_02_gemm",
                beat_name="Standard Softmax Stalling",
                metaphor_type=VisualMetaphorType.CACHE_LINE_CONCURRENCY,
                theme_mode="light",
                hero_object_description="Synchronous wait states between Matrix Multiply (GEMM) and Softmax reduction",
                camera_movement_type="macro_isolate",
                kinetic_focus_noun="[synchronous stalls]",
                kinetic_italic_keyword="wastes",
                color_accents={"primary": "#EF4444", "accent": "#0F172A", "bg": "#E5E5E0"},
                parameters={"sm_utilization": "38%", "idle_cycles": "62%"},
            ),
            # Beat 3: Light Plane - Asynchronous TMA Hardware Engine
            VisualMetaphorAssignment(
                scene_id="scene_03_tma",
                beat_name="Tensor Memory Accelerator",
                metaphor_type=VisualMetaphorType.ASYNCHRONOUS_TENSOR_WARP,
                theme_mode="light",
                hero_object_description="Hardware TMA moving 5D tensor tiles directly from HBM3 to SRAM without SM cores",
                camera_movement_type="pan_right",
                kinetic_focus_noun="[hardware TMA]",
                kinetic_italic_keyword="streams",
                color_accents={"primary": "#059669", "accent": "#0284C7", "bg": "#E5E5E0"},
                parameters={"zero_register_load": True, "dma_speed": "Direct Hardware"},
            ),
            # Beat 4: Light Plane - Overlapping WGMMA & Softmax Pipeline
            VisualMetaphorAssignment(
                scene_id="scene_04_wgmma",
                beat_name="Warp-Group Matrix Multiply",
                metaphor_type=VisualMetaphorType.HARDWARE_REGISTER_MESH,
                theme_mode="light",
                hero_object_description="Ping-pong double buffering overlapping GEMM calculation with Softmax normalization",
                camera_movement_type="slow_zoom_in",
                kinetic_focus_noun="[ping-pong buffer]",
                kinetic_italic_keyword="overlaps",
                color_accents={"primary": "#0284C7", "accent": "#10B981", "bg": "#E5E5E0"},
                parameters={"overlap_percentage": "100%", "pipeline_stages": 3},
            ),
            # Beat 5: Light Plane - Authentic Benchmark TFLOPS Validation
            VisualMetaphorAssignment(
                scene_id="scene_05_benchmark",
                beat_name="FP16 & FP8 Flops Horizon",
                metaphor_type=VisualMetaphorType.COMPARATIVE_BENCHMARK_MATRIX,
                theme_mode="light",
                hero_object_description="3D benchmark bars showing FlashAttention-3 leaping to 840 TFLOPS on H100",
                camera_movement_type="parallax_tilt",
                kinetic_focus_noun="[840 TFLOPS]",
                kinetic_italic_keyword="unleashes",
                color_accents={"primary": "#10B981", "accent": "#0F172A", "bg": "#E5E5E0"},
                parameters={"fa2_flops": 420, "fa3_flops": 840, "gpu_target": "NVIDIA H100 SXM5"},
            ),
            # Beat 6: Dark Loop Conclusion
            VisualMetaphorAssignment(
                scene_id="scene_06_loop",
                beat_name="Zero-Overhead Inference",
                metaphor_type=VisualMetaphorType.CIRCULAR_LOOP_TAKEOUT,
                theme_mode="dark",
                hero_object_description="The Hopper silicon die illuminated in cyan neon, looping back to the compute horizon",
                camera_movement_type="slow_zoom_in",
                kinetic_focus_noun="[hardware limit]",
                kinetic_italic_keyword="conquered",
                color_accents={"primary": "#38BDF8", "accent": "#F59E0B", "bg": "#0A0D14"},
                parameters={"release": "FlashAttention-3 Open Source"},
            ),
        ]

    def _plan_generic_systems_metaphors(self, b: TechnicalConceptBreakdown) -> List[VisualMetaphorAssignment]:
        """Generic fallback for other systems topics."""
        return [
            VisualMetaphorAssignment(
                scene_id="scene_01_hook",
                beat_name="Systems Breakthrough",
                metaphor_type=VisualMetaphorType.MEMORY_HIERARCHY_PIPELINE,
                theme_mode="dark",
                hero_object_description="Dynamic 3D system pipeline",
                camera_movement_type="slow_zoom_in",
                kinetic_focus_noun="[architecture]",
                kinetic_italic_keyword="transforms",
                color_accents={"primary": "#38BDF8", "accent": "#818CF8", "bg": "#0A0D14"},
                parameters={},
            ),
            VisualMetaphorAssignment(
                scene_id="scene_02_loop",
                beat_name="Conclusion",
                metaphor_type=VisualMetaphorType.CIRCULAR_LOOP_TAKEOUT,
                theme_mode="dark",
                hero_object_description="Closing loop graphic",
                camera_movement_type="slow_zoom_in",
                kinetic_focus_noun="[future]",
                kinetic_italic_keyword="begins",
                color_accents={"primary": "#38BDF8", "accent": "#10B981", "bg": "#0A0D14"},
                parameters={},
            ),
        ]
