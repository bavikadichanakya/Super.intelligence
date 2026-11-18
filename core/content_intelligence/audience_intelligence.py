"""
Audience & Editorial Identity Intelligence Module
Defines core niche, audience personas, audience promise, and editorial quality gates.
Prevents channel from degrading into generic technology-news aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class TargetAudience:
    segment_id: str
    name: str
    description: str
    primary_curiosity: str
    share_motivator: str
    technical_depth_tolerance: float  # 0.0 (casual) to 1.0 (academic paper)


@dataclass(frozen=True)
class EditorialIdentity:
    brand_name: str = "SUPER.INTELLIGENCEEE"
    mission: str = (
        "Deliver deep, visually rigorous breakdowns of breakthrough AI repositories, "
        "autonomous systems, semiconductor physics, and computing revolutions."
    )
    audience_promise: str = (
        "Every video must teach something useful, reveal a hidden engineering mechanism, "
        "demonstrate something real, or permanently change how the viewer understands a technology."
    )
    uncompromising_rules: List[str] = field(
        default_factory=lambda: [
            "Never devolve into generic tech news aggregation or clickbait headline reading.",
            "Always explain the underlying mechanism (how it works), not merely what it does.",
            "Use precise technical terms (e.g. GRPO, MLA, KV cache, eBPF) and define them visually.",
            "Maintain zero budget tolerance: zero paid promotion, zero bots, 100% organic merit.",
            "Enforce strict human editorial approval before publishing to any public platform.",
        ]
    )


class AudienceIntelligence:
    """Manages niche definition, audience personas, and editorial alignment."""

    def __init__(self, identity: Optional[EditorialIdentity] = None):
        self.identity = identity or EditorialIdentity()
        self.personas: Dict[str, TargetAudience] = self._init_personas()

    def _init_personas(self) -> Dict[str, TargetAudience]:
        return {
            "ai_engineer": TargetAudience(
                segment_id="ai_engineer",
                name="AI & ML Engineer / Developer",
                description="Engineers building with LLMs, fine-tuning models, and designing agentic pipelines.",
                primary_curiosity="How are frontier architectures achieving 10x throughput and memory efficiency?",
                share_motivator="Sends to teammates to solve engineering bottlenecks or recommend GitHub repos.",
                technical_depth_tolerance=0.9,
            ),
            "tech_builder": TargetAudience(
                segment_id="tech_builder",
                name="Builder / Founder / Hacker",
                description="Creators building startups and autonomous software products using open weights.",
                primary_curiosity="Can I run this locally on my MacBook/workstation at zero API cost?",
                share_motivator="Sends to co-founders or technical friends as competitive market intelligence.",
                technical_depth_tolerance=0.75,
            ),
            "student_researcher": TargetAudience(
                segment_id="student_researcher",
                name="CS Student / Academic Researcher",
                description="Students and scholars studying machine learning, hardware physics, and algorithms.",
                primary_curiosity="What is the mathematical formulation and proof behind this milestone?",
                share_motivator="Shares in study groups, Discord servers, and campus research labs.",
                technical_depth_tolerance=0.95,
            ),
            "curious_professional": TargetAudience(
                segment_id="curious_professional",
                name="Curious Tech Professional",
                description="Knowledge workers, designers, and managers wanting to understand how AI truly works.",
                primary_curiosity="What is the real difference between marketing hype and true technological capability?",
                share_motivator="Sends on LinkedIn/X or DMs colleagues: 'Look at how this actually works.'",
                technical_depth_tolerance=0.6,
            ),
        }

    def evaluate_editorial_alignment(self, topic: str, core_mechanism: str) -> Dict[str, bool | str]:
        """Validates that a candidate video fulfills the audience promise."""
        has_mechanism = len(core_mechanism.strip()) > 15
        is_generic_news = any(
            buzzword in topic.lower()
            for buzzword in ["announced today", "rumor says", "might release", "stock price"]
        )

        aligned = has_mechanism and not is_generic_news
        reason = (
            "Passed editorial criteria: contains deep mechanism explanation and avoids gossip."
            if aligned
            else "Failed: topic lacks a concrete technical mechanism or resembles generic news aggregation."
        )

        return {
            "aligned": aligned,
            "topic": topic,
            "core_mechanism": core_mechanism,
            "reason": reason,
            "audience_promise": self.identity.audience_promise,
        }
