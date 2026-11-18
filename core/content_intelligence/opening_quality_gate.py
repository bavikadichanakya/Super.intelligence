"""
Opening Quality Gate & Pre-Production Hook Evaluation Engine
Phase 12.1 — Replaces static title cards and rhetorical question openers with
three materially different, high-velocity opening concepts:
A. Result-First Visual (immediate numerical shockwave / benchmark timer)
B. Mechanism-First Demonstration (live terminal execution / memory hierarchy)
C. Unexpected Contrast / Misconception (shattering conventional developer dogma)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class OpeningConceptType(str, Enum):
    RESULT_FIRST = "result_first_visual"
    MECHANISM_FIRST = "mechanism_first_demonstration"
    UNEXPECTED_CONTRAST = "unexpected_contrast_misconception"


@dataclass
class OpeningConcept:
    concept_id: str
    concept_type: OpeningConceptType
    headline: str
    first_frame_visual: str            # Frame 0 specification
    first_spoken_sentence: str         # Spoken audio (strictly <= 14 words)
    on_screen_hook: str                # Screen typography (strictly <= 7 words)
    first_visual_action: str           # Kinetic motion in 0.0s - 2.5s
    expected_audience_curiosity: str   # The psychological tension
    promised_payoff: str               # What the viewer will understand by second 45
    supporting_evidence: str           # Citation / benchmark / code proof
    spoken_word_count: int = 0
    on_screen_word_count: int = 0
    linter_passed: bool = True
    linter_violations: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.spoken_word_count = len(self.first_spoken_sentence.split())
        self.on_screen_word_count = len(self.on_screen_hook.split())


class OpeningQualityGate:
    """Pre-production evaluation and rejection gate for video openings."""

    BANNED_OPENING_PATTERNS = [
        (r"^ever wonder(ed)?", "Rhetorical question opener ('Ever wondered...') is strictly prohibited."),
        (r"^have you (ever )?heard", "Rhetorical question opener ('Have you heard...') is prohibited."),
        (r"^did you know", "Rhetorical question opener ('Did you know...') is prohibited."),
        (r"^in this video", "Throat-clearing filler ('In this video...') is prohibited."),
        (r"^today we are", "Generic announcement ('Today we are...') is prohibited."),
        (r"^welcome back", "Creator-centric greeting ('Welcome back...') is prohibited on cold-discovery feeds."),
        (r"^hey (guys|everyone|there)", "Social greeting ('Hey guys...') wastes the first 1.5s filter."),
        (r"^so basically", "Casual conversational filler is prohibited in Frame 0."),
    ]

    BANNED_VISUAL_PATTERNS = [
        ("static title card", "Static title slides or plain text cards fail the 1.5s swipe filter."),
        ("logo animation", "Logo intros or channel bumpers before the hook are prohibited."),
        ("empty slide", "Blank or decorative-only backgrounds without visual context are prohibited."),
    ]

    def lint_opening_concept(self, concept: OpeningConcept) -> Tuple[bool, List[str]]:
        """Validates opening concept against strict engagement standards."""
        violations: List[str] = []
        spoken_lower = concept.first_spoken_sentence.strip().lower()
        visual_lower = concept.first_frame_visual.strip().lower()

        # 1. Spoken Word Count Gate (strictly <= 14 words)
        words = concept.first_spoken_sentence.split()
        if len(words) > 14:
            violations.append(f"Spoken hook has {len(words)} words; must be 14 words or fewer.")

        # 2. On-screen typography word count (strictly <= 7 words)
        text_words = concept.on_screen_hook.split()
        if len(text_words) > 7:
            violations.append(f"On-screen hook has {len(text_words)} words; must be 7 words or fewer.")

        # 3. Banned Spoken Patterns
        for pattern, reason in self.BANNED_OPENING_PATTERNS:
            if re.search(pattern, spoken_lower):
                violations.append(reason)

        # 4. Banned Visual Patterns
        for pattern, reason in self.BANNED_VISUAL_PATTERNS:
            if pattern in visual_lower:
                violations.append(reason)

        # 5. Evidence grounding check
        if not concept.supporting_evidence or len(concept.supporting_evidence.strip()) < 10:
            violations.append("Supporting evidence citation is missing or unsubstantiated.")

        passed = len(violations) == 0
        concept.linter_passed = passed
        concept.linter_violations = violations
        return passed, violations

    def generate_candidate_openings(
        self,
        topic: str,
        hero_metric: str,
        technical_mechanism: str,
        conventional_dogma: str,
        evidence_citation: str,
    ) -> List[OpeningConcept]:
        """
        Generates 3 materially distinct opening concepts:
        A. Result-First Visual
        B. Mechanism-First Demonstration
        C. Unexpected Contrast / Misconception
        """
        # Concept A: Result-First Visual
        concept_a = OpeningConcept(
            concept_id="OP_CONCEPT_A_RESULT",
            concept_type=OpeningConceptType.RESULT_FIRST,
            headline=f"{hero_metric} Speedup Demonstrated Live",
            first_frame_visual=(
                "Split-screen benchmark timer showing standard PyTorch attention lagging behind "
                "while optimized Hopper kernel finishes in real-time."
            ),
            first_spoken_sentence=f"This single kernel rewrite delivers {hero_metric} on standard Nvidia silicon.",
            on_screen_hook=f"{hero_metric.upper()} ON HOPPER",
            first_visual_action="Kinetic dual-timer stopwatch starting at 0ms and stopping with a green checkmark.",
            expected_audience_curiosity="How can identical GPU hardware run 75% faster with zero accuracy loss?",
            promised_payoff="Explains asynchronous hardware warp-specialization and memory tiling.",
            supporting_evidence=evidence_citation,
        )

        # Concept B: Mechanism-First Demonstration
        concept_b = OpeningConcept(
            concept_id="OP_CONCEPT_B_MECHANISM",
            concept_type=OpeningConceptType.MECHANISM_FIRST,
            headline="The Hardware Memory Bandwidth Bottleneck",
            first_frame_visual=(
                "Animated 3D memory hierarchy showing High-Bandwidth Memory (HBM) choking data "
                "transfers while tensor cores sit idle."
            ),
            first_spoken_sentence="Your GPU spends eighty percent of its time waiting for memory roundtrips.",
            on_screen_hook="THE GPU MEMORY WALL",
            first_visual_action="Red memory bottleneck pipe filling up while compute cores pulse at zero utilization.",
            expected_audience_curiosity="Why are billion-dollar AI clusters bottlenecked by memory instead of compute?",
            promised_payoff="Reveals how on-chip SRAM tiling eliminates global memory roundtrips completely.",
            supporting_evidence=evidence_citation,
        )

        # Concept C: Unexpected Contrast / Misconception
        concept_c = OpeningConcept(
            concept_id="OP_CONCEPT_C_CONTRAST",
            concept_type=OpeningConceptType.UNEXPECTED_CONTRAST,
            headline="Why Traditional Transformers Waste 80% of Compute",
            first_frame_visual=(
                "Contrasting code diff highlighting synchronous memory stalls versus asynchronous "
                "Tensor Memory Accelerator (TMA) pipelines."
            ),
            first_spoken_sentence="Everything you were taught about transformer attention scaling is obsolete.",
            on_screen_hook="TRANSFORMER SCALING IS BROKEN",
            first_visual_action="Code editor diff cross-fading into an asynchronous hardware execution timeline.",
            expected_audience_curiosity="What architectural assumption did every mainstream library get wrong?",
            promised_payoff="Deconstructs how asynchrony hides memory latency behind matrix math.",
            supporting_evidence=evidence_citation,
        )

        openings = [concept_a, concept_b, concept_c]
        for op in openings:
            self.lint_opening_concept(op)

        return openings
