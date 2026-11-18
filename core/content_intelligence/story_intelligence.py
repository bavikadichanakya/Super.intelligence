"""
Story Intelligence & Narrative Retention Engine
Structures short-form technical documentaries using high-retention narrative escalation:
Hook -> Escalation -> Technical Revelation -> Empirical Evidence -> Practical Payoff -> Named-Persona CTA.
Enforces visual storytelling velocity and eliminates mid-video drop-offs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StorySection:
    section_name: str              # "hook", "escalation", "technical_revelation", "evidence", "payoff", "cta"
    target_start_sec: float
    target_end_sec: float
    core_narrative_job: str
    spoken_script: str
    visual_action: str             # Specific custom UI/diagram/terminal/hardware animation
    on_screen_typography: str      # Subtitle/headline text
    retention_hook_into_next: str  # Why the viewer refuses to leave before the next beat


@dataclass
class NarrativeStructure:
    topic_title: str
    total_target_duration: float
    sections: List[StorySection]
    pacing_velocity: str           # "high", "moderate", "deliberate"
    core_payoff_summary: str


class StoryIntelligenceEngine:
    """Designs retention-optimized narrative structures for high-depth engineering documentaries."""

    def build_narrative_arc(
        self,
        topic: str,
        hook_spoken: str,
        hook_visual: str,
        hook_text: str,
        escalation_tension: str,
        technical_revelation: str,
        empirical_evidence: str,
        practical_payoff: str,
        share_persona: str,
        cta_instruction: str,
        total_duration: float = 45.0,
    ) -> NarrativeStructure:
        """
        Builds a 6-stage narrative arc tuned for maximum retention and cold-audience discovery.
        Optimal sweet spot: 35s to 50s for technical Shorts and Reels.
        """
        # Time distribution proportional to total duration
        t_hook = min(4.5, round(total_duration * 0.10, 1))
        t_esc = round(total_duration * 0.22, 1)
        t_rev = round(total_duration * 0.50, 1)
        t_evi = round(total_duration * 0.72, 1)
        t_pay = round(total_duration * 0.90, 1)
        t_end = total_duration

        sections = [
            StorySection(
                section_name="hook",
                target_start_sec=0.0,
                target_end_sec=t_hook,
                core_narrative_job="Stop the scroll in < 1s; present the anomaly or bold contrast without throat clearing.",
                spoken_script=hook_spoken,
                visual_action=hook_visual,
                on_screen_typography=hook_text,
                retention_hook_into_next="Creates an open curiosity gap: 'How was this physically possible?'",
            ),
            StorySection(
                section_name="escalation",
                target_start_sec=t_hook,
                target_end_sec=t_esc,
                core_narrative_job="Raise the stakes. Explain why the existing standard or status quo was completely stuck.",
                spoken_script=escalation_tension,
                visual_action="High-contrast comparison diagram showing the traditional bottleneck or failure mode.",
                on_screen_typography="THE BOTTLENECK NOBODY COULD SOLVE",
                retention_hook_into_next="Teases the arrival of an unexpected architectural solution.",
            ),
            StorySection(
                section_name="technical_revelation",
                target_start_sec=t_esc,
                target_end_sec=t_rev,
                core_narrative_job="Deliver the core mechanism. Deconstruct the algorithm, math, or physics visually.",
                spoken_script=technical_revelation,
                visual_action="Dynamic animated matrix, memory projection flow, or live terminal execution trace.",
                on_screen_typography="THE CORE BREAKTHROUGH MECHANISM",
                retention_hook_into_next="Promises the empirical proof: 'Does it actually work in production?'",
            ),
            StorySection(
                section_name="evidence",
                target_start_sec=t_rev,
                target_end_sec=t_evi,
                core_narrative_job="Provide the receipts. Show benchmark charts, speed comparisons, or compiler verification.",
                spoken_script=empirical_evidence,
                visual_action="Comparative bar charts, leaderboards, or test-suite verification outputs.",
                on_screen_typography="THE EMPIRICAL RECEIPTS",
                retention_hook_into_next="Prepares the viewer for the practical takeaway they can use.",
            ),
            StorySection(
                section_name="payoff",
                target_start_sec=t_evi,
                target_end_sec=t_pay,
                core_narrative_job="Deliver the tangible value. How this changes sovereign AI, local deployment, or developer freedom.",
                spoken_script=practical_payoff,
                visual_action="Open weights badges, local Ollama execution, or architectural blueprint.",
                on_screen_typography="THE PRACTICAL TAKEAWAY",
                retention_hook_into_next="Sets up the natural urge to share this insight with someone in their network.",
            ),
            StorySection(
                section_name="cta",
                target_start_sec=t_pay,
                target_end_sec=t_end,
                core_narrative_job=f"Earn a DM send by naming the exact persona ({share_persona}) who needs this.",
                spoken_script=cta_instruction,
                visual_action="Clean architectural channel seal for SUPER.INTELLIGENCEEE with follow and subscribe pills.",
                on_screen_typography=f"SEND THIS TO A {share_persona.upper()}",
                retention_hook_into_next="Leaves a strong lingering impression on the final looping frame.",
            ),
        ]

        return NarrativeStructure(
            topic_title=topic,
            total_target_duration=total_duration,
            sections=sections,
            pacing_velocity="high" if total_duration <= 45.0 else "moderate",
            core_payoff_summary=practical_payoff,
        )
