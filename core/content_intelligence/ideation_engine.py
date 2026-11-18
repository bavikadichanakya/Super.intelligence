"""
Content Ideation & Research-Driven Backlog Engine
Mines high-signal developer platforms (GitHub releases, arXiv papers, technical discussions)
to produce ranked content candidates across 5 distinct narrative angles with expiration tracking.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional


@dataclass
class ContentAngle:
    angle_type: str  # "contrast", "mechanical", "financial_disruption", "practical_laptop", "uncomfortable_truth"
    headline: str
    target_curiosity: str
    core_premise: str
    primary_share_persona: str


@dataclass
class IdeaCandidate:
    idea_id: str
    topic_title: str
    content_pillar: str
    source_attribution: str
    source_url: str
    angles: List[ContentAngle]
    priority_score: float  # 0.0 to 10.0
    is_time_sensitive: bool
    expiration_date: Optional[str]  # ISO format string
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ContentIdeationEngine:
    """Generates multi-angle technical concepts and ranks them in a structured backlog."""

    def __init__(self):
        self.backlog: List[IdeaCandidate] = []

    def generate_angles_for_topic(
        self,
        topic: str,
        technical_breakthrough: str,
        counter_status_quo: str,
        practical_takeaway: str,
    ) -> List[ContentAngle]:
        """Expands a single breakthrough into 5 distinct high-retention angles."""
        return [
            ContentAngle(
                angle_type="contrast",
                headline=f"Open vs Closed: How {topic} Beat a Multi-Billion Dollar Model",
                target_curiosity="How can an open community out-innovate trillion-dollar monopolies?",
                core_premise=f"{counter_status_quo} was assumed to be the only path until {topic} proved otherwise.",
                primary_share_persona="Engineers and founders who champion open-source software.",
            ),
            ContentAngle(
                angle_type="mechanical",
                headline=f"The Hidden Architecture Behind {topic}: How It Actually Works",
                target_curiosity="What is the exact engineering mechanism inside the paper?",
                core_premise=f"Deconstructs {technical_breakthrough} down to matrix math and memory layouts.",
                primary_share_persona="Computer science students and systems architects.",
            ),
            ContentAngle(
                angle_type="financial_disruption",
                headline=f"The 90% Cost Drop: The Brutal Economics of {topic}",
                target_curiosity="Why does this make traditional enterprise software pricing obsolete?",
                core_premise="Exposes the massive delta between proprietary API markups and raw inference costs.",
                primary_share_persona="Tech leads and CTOs managing cloud infrastructure bills.",
            ),
            ContentAngle(
                angle_type="practical_laptop",
                headline=f"Run {topic} Locally on Your Own Machine in 3 Minutes",
                target_curiosity="Can I actually use this right now without sending my data to the cloud?",
                core_premise=f"Demonstrates practical local deployment: {practical_takeaway}.",
                primary_share_persona="Independent hackers and privacy-conscious developers.",
            ),
            ContentAngle(
                angle_type="uncomfortable_truth",
                headline=f"What Big Tech Isn't Telling You About {topic}",
                target_curiosity="What is the trade-off or dirty secret behind the marketing press release?",
                core_premise="Exposes the memory bandwidth, training stability, or data bottlenecks rarely discussed.",
                primary_share_persona="Senior engineers skeptical of marketing hype.",
            ),
        ]

    def add_to_backlog(
        self,
        topic_title: str,
        content_pillar: str,
        source_attribution: str,
        source_url: str,
        technical_breakthrough: str,
        counter_status_quo: str,
        practical_takeaway: str,
        priority_score: float = 8.0,
        is_time_sensitive: bool = False,
        lifespan_days: int = 30,
    ) -> IdeaCandidate:
        """Creates and indexes a validated multi-angle idea candidate."""
        now = datetime.now(timezone.utc)
        exp_date = (now + timedelta(days=lifespan_days)).isoformat() if is_time_sensitive else None

        angles = self.generate_angles_for_topic(
            topic=topic_title,
            technical_breakthrough=technical_breakthrough,
            counter_status_quo=counter_status_quo,
            practical_takeaway=practical_takeaway,
        )

        candidate = IdeaCandidate(
            idea_id=f"idea_{int(time.time() * 1000)}",
            topic_title=topic_title,
            content_pillar=content_pillar,
            source_attribution=source_attribution,
            source_url=source_url,
            angles=angles,
            priority_score=priority_score,
            is_time_sensitive=is_time_sensitive,
            expiration_date=exp_date,
        )

        self.backlog.append(candidate)
        self.backlog.sort(key=lambda x: x.priority_score, reverse=True)
        return candidate

    def get_ranked_backlog(self, pillar_filter: Optional[str] = None) -> List[IdeaCandidate]:
        """Returns non-expired ideas ranked by priority."""
        now_iso = datetime.now(timezone.utc).isoformat()
        active = [
            i for i in self.backlog
            if not i.is_time_sensitive or (i.expiration_date and i.expiration_date > now_iso)
        ]
        if pillar_filter:
            active = [i for i in active if i.content_pillar == pillar_filter]
        return active
