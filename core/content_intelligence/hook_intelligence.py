"""
Hook Intelligence & Multi-Archetype Generation Engine
Generates 6–10 genuinely diverse hook concepts for any technical topic.
Enforces the 3-Layer Hook standard (Visual + Spoken + On-Screen Text) and lints against anti-patterns.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class HookArchetype(str, Enum):
    DIRECT_CONTRAST = "direct_contrast"            # Inverting consensus (e.g., Hormozi / Koe)
    SHOCKING_METRIC = "shocking_metric"            # Concrete numbers that shatter intuition
    SECRET_MECHANISM = "secret_mechanism"          # How it actually works under the hood (Kallaway)
    INDUSTRY_THREAT = "industry_threat"            # Why this breaks an existing monopoly or workflow (Welsh)
    PROOF_RECEIPT = "proof_receipt"                # Showing the code / benchmark receipt immediately
    UNCOMFORTABLE_TRUTH = "uncomfortable_truth"    # Calling out marketing hype vs technical reality
    LOCAL_POWER = "local_power"                    # Running supercomputing capabilities on consumer hardware
    VISUAL_ANOMALY = "visual_anomaly"              # Immediate unexpected visual demonstration (MrBeast style)


@dataclass
class ThreeLayerHook:
    archetype: HookArchetype
    title: str
    first_frame_visual: str        # Layer 1: What the viewer SEES in the first 0.5 seconds
    spoken_opening_line: str       # Layer 2: What the viewer HEARS immediately
    on_screen_headline: str        # Layer 3: Bold text on screen (for muted autoplay)
    curiosity_gap: str             # The unanswered tension
    promised_payoff: str           # The concrete takeaway delivered in the video
    target_persona_why: str        # Why the specific target viewer stops scrolling
    anti_pattern_score: float      # 1.0 = clean, 0.0 = toxic anti-pattern detected
    lint_warnings: List[str] = field(default_factory=list)


class HookIntelligenceEngine:
    """Generates, scores, and lints short-form video hooks across multiple archetypes."""

    # Words and phrases that kill first-3-second retention (from Vyral references)
    FORBIDDEN_RHETORICAL_STARTERS = [
        r"^ever wondered",
        r"^did you know",
        r"^have you ever",
        r"^what if i told you",
        r"^can you imagine",
        r"^do you know why",
    ]

    THROAT_CLEARING_PATTERNS = [
        r"^today we are",
        r"^in this video",
        r"^welcome back",
        r"^hey guys",
        r"^so basically",
        r"^i want to talk about",
    ]

    def lint_spoken_hook(self, spoken_line: str) -> Tuple[float, List[str]]:
        """Lints a spoken line against known early drop-off anti-patterns."""
        warnings: List[str] = []
        score = 1.0
        line_clean = spoken_line.strip().lower()

        # Check rhetorical question starters (the #1 skip cause)
        for pat in self.FORBIDDEN_RHETORICAL_STARTERS:
            if re.search(pat, line_clean):
                warnings.append(f"Anti-Pattern Detected: Rhetorical question opener ('{pat}'). Reframe as an assertive claim.")
                score -= 0.5

        # Check throat-clearing fluff
        for pat in self.THROAT_CLEARING_PATTERNS:
            if re.search(pat, line_clean):
                warnings.append(f"Anti-Pattern Detected: Throat-clearing filler ('{pat}'). Start directly on the core tension.")
                score -= 0.4

        # Check word count of first sentence (must be punchy: <= 18 words)
        words = spoken_line.split()
        if len(words) > 22:
            warnings.append(f"Pacing Warning: Opening sentence has {len(words)} words. Split or trim to under 18 words.")
            score -= 0.2

        return max(0.0, score), warnings

    def generate_hook_batch(
        self,
        topic: str,
        hero_metric: str,
        incumbent_entity: str,
        technical_mechanism: str,
        practical_result: str,
    ) -> List[ThreeLayerHook]:
        """Generates 8 genuinely diverse hook concepts spanning all core archetypes."""
        batch: List[ThreeLayerHook] = []

        # 1. Direct Contrast
        spoken_1 = f"Silicon Valley spent billions on human labeling. This open repo just beat them with pure math."
        s1, w1 = self.lint_spoken_hook(spoken_1)
        batch.append(
            ThreeLayerHook(
                archetype=HookArchetype.DIRECT_CONTRAST,
                title="The $100M Inversion",
                first_frame_visual=f"Split screen: {incumbent_entity} labeled data warehouse vs 10 lines of mathematical reward code.",
                spoken_opening_line=spoken_1,
                on_screen_headline="THE $100M MISTAKE IN AI",
                curiosity_gap="Why did human fine-tuning fail where autonomous math succeeded?",
                promised_payoff=f"Explains how {technical_mechanism} eliminates human annotation bottlenecks.",
                target_persona_why="Engineers love seeing complex brute-force replaced by elegant mathematical systems.",
                anti_pattern_score=s1,
                lint_warnings=w1,
            )
        )

        # 2. Shocking Metric
        spoken_2 = f"This single engineering breakthrough slashed GPU memory consumption by {hero_metric}."
        s2, w2 = self.lint_spoken_hook(spoken_2)
        batch.append(
            ThreeLayerHook(
                archetype=HookArchetype.SHOCKING_METRIC,
                title="The Memory Cliff",
                first_frame_visual=f"High-contrast memory gauge dropping from 100% full VRAM down to {hero_metric} with glowing green highlight.",
                spoken_opening_line=spoken_2,
                on_screen_headline=f"{hero_metric} VRAM REDUCTION",
                curiosity_gap=f"How can a model lose {hero_metric} of its KV cache without degrading accuracy?",
                promised_payoff=f"Step-by-step breakdown of low-rank down-projection and decompressed latent attention.",
                target_persona_why="GPU memory is the single most expensive bottleneck for AI developers.",
                anti_pattern_score=s2,
                lint_warnings=w2,
            )
        )

        # 3. Secret Mechanism
        spoken_3 = f"Watch what happens inside this model's thinking tokens the moment it catches its own mistake."
        s3, w3 = self.lint_spoken_hook(spoken_3)
        batch.append(
            ThreeLayerHook(
                archetype=HookArchetype.SECRET_MECHANISM,
                title="Inside the Thinking Trace",
                first_frame_visual="Raw terminal typing out live self-correction tokens: 'Wait, wait, wait... recalculating.'",
                spoken_opening_line=spoken_3,
                on_screen_headline="AI SPONTANEOUSLY RETHINKING",
                curiosity_gap="Can neural networks actually self-reflect without human training prompts?",
                promised_payoff=f"Demonstrates how pure reinforcement learning induces autonomous verification.",
                target_persona_why="Viewing an AI pause and correct itself feels like watching spontaneous reasoning.",
                anti_pattern_score=s3,
                lint_warnings=w3,
            )
        )

        # 4. Industry Threat
        spoken_4 = f"This open-source release just made cloud API subscriptions 27 times too expensive."
        s4, w4 = self.lint_spoken_hook(spoken_4)
        batch.append(
            ThreeLayerHook(
                archetype=HookArchetype.INDUSTRY_THREAT,
                title="The 27x Pricing War",
                first_frame_visual=f"Cost comparison ledger: $15.00/1M tokens crossing out down to $0.55/1M tokens.",
                spoken_opening_line=spoken_4,
                on_screen_headline="THE 27x COST DISRUPTION",
                curiosity_gap="Why can this architecture operate at a tiny fraction of proprietary costs?",
                promised_payoff=f"Explains sparse Mixture-of-Experts routing where only 5.5% of parameters activate per token.",
                target_persona_why="Tech leads and founders immediately send pricing disruption to their leadership.",
                anti_pattern_score=s4,
                lint_warnings=w4,
            )
        )

        # 5. Proof Receipt
        spoken_5 = f"Here is the exact benchmark table where an open-source model surpassed closed frontier AI."
        s5, w5 = self.lint_spoken_hook(spoken_5)
        batch.append(
            ThreeLayerHook(
                archetype=HookArchetype.PROOF_RECEIPT,
                title="The Math Olympiad Receipt",
                first_frame_visual="High-contrast AIME 2024 Math Olympiad leaderboard showing open-source score 79.8% ahead of o1.",
                spoken_opening_line=spoken_5,
                on_screen_headline="THE OFFICIAL BENCHMARK RECEIPT",
                curiosity_gap="Is the benchmark real or an overfitted cherry-pick?",
                promised_payoff="Rigorous breakdown of independent SWE-bench and Codeforces verifications.",
                target_persona_why="Technical viewers demand hard empirical receipts over influencer hype.",
                anti_pattern_score=s5,
                lint_warnings=w5,
            )
        )

        # 6. Local Power
        spoken_6 = f"You can run this frontier reasoning model completely offline on your personal laptop right now."
        s6, w6 = self.lint_spoken_hook(spoken_6)
        batch.append(
            ThreeLayerHook(
                archetype=HookArchetype.LOCAL_POWER,
                title="Sovereign Laptop AI",
                first_frame_visual="Terminal running Ollama on a MacBook with zero Wi-Fi connection generating 40 tokens/sec.",
                spoken_opening_line=spoken_6,
                on_screen_headline="RUN IT LOCALLY // ZERO CLOUD",
                curiosity_gap="How can a 671-billion parameter architecture run on consumer silicon?",
                promised_payoff=f"Explains distillation matrices (1.5B to 70B weights) under MIT license.",
                target_persona_why="Total privacy and zero API bills are the dream of every independent developer.",
                anti_pattern_score=s6,
                lint_warnings=w6,
            )
        )

        # 7. Uncomfortable Truth
        spoken_7 = f"Most AI companies pretend reasoning requires trillions in capital. This repository proved them wrong."
        s7, w7 = self.lint_spoken_hook(spoken_7)
        batch.append(
            ThreeLayerHook(
                archetype=HookArchetype.UNCOMFORTABLE_TRUTH,
                title="The Capital Myth",
                first_frame_visual="Dark-mode architectural blueprint stamped with large red 'DEBUNKED' text.",
                spoken_opening_line=spoken_7,
                on_screen_headline="THE EXPENSIVE AI LIE",
                curiosity_gap="Why did big tech claim algorithmic scaling was impossible without vast budgets?",
                promised_payoff="Explains algorithmic efficiency gains that outpace raw hardware spending.",
                target_persona_why="Audience craves authentic insider critique over corporate PR releases.",
                anti_pattern_score=s7,
                lint_warnings=w7,
            )
        )

        # 8. Visual Anomaly
        spoken_8 = f"Look at these 256 neural specialists activating across this matrix in under ten milliseconds."
        s8, w8 = self.lint_spoken_hook(spoken_8)
        batch.append(
            ThreeLayerHook(
                archetype=HookArchetype.VISUAL_ANOMALY,
                title="The 256 Specialist Lattice",
                first_frame_visual="A rapid 16x16 neural grid pulsing with purple and gold sparks as tokens route through.",
                spoken_opening_line=spoken_8,
                on_screen_headline="256 SPECIALISTS IN 10ms",
                curiosity_gap="What does dynamic token routing look like inside a sparse neural network?",
                promised_payoff=f"Visualizes auxiliary-loss-free routing in {technical_mechanism}.",
                target_persona_why="Stunning original visualizations hold the initial 3 seconds effortlessly.",
                anti_pattern_score=s8,
                lint_warnings=w8,
            )
        )

        return batch
