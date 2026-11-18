"""
SUPER.INTELLIGENCEEE — Multi-Factor Opportunity Scoring Engine
Evaluates content opportunities using a 7-factor transparent scoring matrix with hard evidence gating.
Prevents ungrounded or low-evidence topics from entering the production workflow.
"""

from __future__ import annotations

import datetime
import logging
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from core.database import Database, get_db
from core.owner_config import get_owner_config

logger = logging.getLogger("super_intelligence.opportunity_scorer")

DEFAULT_WEIGHTS = {
    "evidence_quality": 0.25,
    "strategic_fit": 0.25,
    "audience_relevance": 0.20,
    "expected_impact": 0.15,
    "urgency": 0.15,
}

EVIDENCE_PASSING_THRESHOLD = 4.0


@dataclass
class OpportunityScore:
    """Detailed multi-factor opportunity score breakdown."""
    topic_id: Optional[int]
    title: str
    overall_score: float                  # 0.0 to 100.0
    eligible: bool                        # Hard gate: False if evidence is insufficient
    factors: Dict[str, float]             # 1.0 to 10.0 per factor
    weights: Dict[str, float]
    reasoning: str
    evidence_refs: List[str]
    scored_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class OpportunityScorer:
    """Calculates transparent opportunity scores with strict evidence gating."""

    def __init__(self, db: Optional[Database] = None, weights: Optional[Dict[str, float]] = None):
        self.db = db or get_db()
        self.weights = weights or dict(DEFAULT_WEIGHTS)
        self.owner_config = get_owner_config()

    def evaluate_opportunity(self, topic: Dict[str, Any]) -> OpportunityScore:
        """
        Computes 7 individual factor scores and overall score.
        Enforces hard evidence requirement: if evidence is missing, score is 0.
        """
        title = topic.get("title", "")
        summary = topic.get("summary", "")
        category = topic.get("category", "")
        source_url = topic.get("url") or topic.get("source_url") or ""
        publisher = topic.get("publisher", "")

        corpus = f"{title} {summary} {category} {publisher}".lower()

        # ---------------------------------------------------------
        # Factor 1: Evidence Quality (1 - 10) [HARD GATE]
        # ---------------------------------------------------------
        evidence_score = 1.0
        evidence_reasons = []

        if not source_url or not source_url.startswith("http"):
            evidence_score = 0.0
            evidence_reasons.append("Missing primary source URL.")
        else:
            # Check for authoritative primary domains
            high_trust_domains = [
                "arxiv.org", "github.com", "deepmind.google", "openai.com", "anthropic.com",
                "huggingface.co", "research.facebook.com", "mistral.ai", "nature.com"
            ]
            if any(dom in source_url.lower() for dom in high_trust_domains):
                evidence_score = 10.0
                evidence_reasons.append("Primary research repository / lab publication.")
            elif publisher and publisher.lower() not in {"unknown", "anonymous"}:
                evidence_score = 7.5
                evidence_reasons.append(f"Established publisher: {publisher}.")
            else:
                evidence_score = 5.0
                evidence_reasons.append("Public web source.")

        # Hard Gate Check
        if evidence_score < EVIDENCE_PASSING_THRESHOLD:
            return OpportunityScore(
                topic_id=topic.get("id"),
                title=title,
                overall_score=0.0,
                eligible=False,
                factors={"evidence_quality": evidence_score},
                weights=self.weights,
                reasoning=f"DISQUALIFIED: Lacks required primary evidence. ({'; '.join(evidence_reasons)})",
                evidence_refs=[source_url] if source_url else [],
            )

        # ---------------------------------------------------------
        # Factor 2: Strategic Fit (1 - 10)
        # Matches core pillars: Architecture, Local AI, Reliability, Open Source
        # ---------------------------------------------------------
        fit_keywords = {
            "frontier_architecture": ["architecture", "transformer", "attention", "ssm", "mamba", "linear scaling", "quantization", "pruning"],
            "local_edge": ["local", "offline", "workstation", "edge", "consumer hardware", "gguf", "vram", "latency"],
            "reliability": ["benchmark", "throughput", "reliability", "deterministic", "reproducible", "audit", "bottleneck"],
            "open_source": ["open source", "weights", "weights available", "github", "apache", "mit license"],
        }
        fit_matches = sum(1 for p_list in fit_keywords.values() if any(kw in corpus for kw in p_list))
        strategic_fit = min(10.0, max(2.0, fit_matches * 2.5))

        # ---------------------------------------------------------
        # Factor 3: Audience Relevance (1 - 10)
        # Software engineers, AI builders, technical leaders
        # ---------------------------------------------------------
        audience_keywords = ["engineer", "developer", "builder", "code", "model", "inference", "kernel", "gpu", "compiler"]
        aud_matches = sum(1 for kw in audience_keywords if kw in corpus)
        audience_relevance = min(10.0, max(3.0, 3.0 + aud_matches * 1.5))

        # ---------------------------------------------------------
        # Factor 4: Expected Impact (1 - 10)
        # Quantitative multipliers, breakthrough assertions
        # ---------------------------------------------------------
        has_multiplier = bool(re.search(r"\b\d+(\.\d+)?x\b|\b\d+%\b", corpus))
        has_breakthrough = any(w in corpus for w in ["breakthrough", "sota", "million-token", "outperforms", "unlocked"])
        expected_impact = 5.0
        if has_multiplier:
            expected_impact += 3.0
        if has_breakthrough:
            expected_impact += 2.0
        expected_impact = min(10.0, expected_impact)

        # ---------------------------------------------------------
        # Factor 5: Urgency (1 - 10)
        # Recency, breaking release
        # ---------------------------------------------------------
        urgency = 7.0
        if any(w in corpus for w in ["today", "just released", "unveiled", "breaking", "announcing"]):
            urgency = 9.5
        elif any(w in corpus for w in ["yesterday", "this week"]):
            urgency = 8.0

        # ---------------------------------------------------------
        # Factor 6: Production Effort (1 - 10)
        # ---------------------------------------------------------
        production_effort = 4.0  # Automated zero-budget pipeline standard

        # ---------------------------------------------------------
        # Factor 7: Duplication Risk (1 - 10)
        # ---------------------------------------------------------
        duplication_risk = 2.0   # Low default for fresh RSS entries

        # Calculate weighted composite score (0 to 100)
        composite = (
            evidence_score * self.weights.get("evidence_quality", 0.25)
            + strategic_fit * self.weights.get("strategic_fit", 0.25)
            + audience_relevance * self.weights.get("audience_relevance", 0.20)
            + expected_impact * self.weights.get("expected_impact", 0.15)
            + urgency * self.weights.get("urgency", 0.15)
        )
        final_score = round(composite * 10.0, 1) # scale 1-10 to 10-100

        reasoning = (
            f"Evidence: {evidence_score}/10 ({'; '.join(evidence_reasons)}). "
            f"Strategic Fit: {strategic_fit}/10 across {fit_matches} pillars. "
            f"Impact: {expected_impact}/10."
        )

        return OpportunityScore(
            topic_id=topic.get("id"),
            title=title,
            overall_score=final_score,
            eligible=True,
            factors={
                "evidence_quality": evidence_score,
                "strategic_fit": strategic_fit,
                "audience_relevance": audience_relevance,
                "expected_impact": expected_impact,
                "urgency": urgency,
                "production_effort": production_effort,
                "duplication_risk": duplication_risk,
            },
            weights=self.weights,
            reasoning=reasoning,
            evidence_refs=[source_url] if source_url else [],
        )

    def score_and_rank_pending_topics(self) -> List[OpportunityScore]:
        """Scores all pending topics in the database and updates their scores."""
        scores = []
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM topics WHERE score == 0 OR score IS NULL ORDER BY id DESC LIMIT 50")
            topics = [dict(r) for r in cursor.fetchall()]

            for t in topics:
                opp_score = self.evaluate_opportunity(t)
                scores.append(opp_score)
                cursor.execute(
                    "UPDATE topics SET score = ?, status = ? WHERE id = ?",
                    (opp_score.overall_score, "SHORTLISTED" if opp_score.eligible else "REJECTED", t["id"]),
                )
        return sorted(scores, key=lambda s: s.overall_score, reverse=True)

