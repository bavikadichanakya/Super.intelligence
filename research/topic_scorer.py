"""
SUPER.INTELLIGENCEEE — Topic Scorer & Opportunity Evaluator
Calculates multi-dimensional editorial and algorithmic scoring for tech stories
based on technical depth, evidence provenance, timeliness, audience utility,
and topic fatigue penalties.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from core.schemas import TopicScoreBreakdown


class TopicScorer:
    """Calculates transparent, multi-dimensional editorial and algorithmic scoring."""

    def __init__(self, db=None, config=None):
        self.db = db
        self.config = config

    @staticmethod
    def _calculate_timeliness_score(pub_date_str: Optional[str]) -> float:
        """
        Calculates timeliness score (0.0 - 10.0) based on hours elapsed since publication:
        - < 24h: 10.0 pts
        - < 72h: 8.5 pts
        - < 7 days: 7.0 pts
        - < 30 days: 4.0 pts
        - > 30 days or missing: 2.0 pts
        """
        if not pub_date_str:
            return 2.0

        try:
            clean = pub_date_str.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean)
            now = datetime.now(timezone.utc)
            delta_hours = (now - dt).total_seconds() / 3600.0

            if delta_hours < 0:
                # Slight clock skew or future date from RSS
                return 10.0
            if delta_hours <= 24.0:
                return 10.0
            if delta_hours <= 72.0:
                return 8.5
            if delta_hours <= 168.0:  # 7 days
                return 7.0
            if delta_hours <= 720.0:  # 30 days
                return 4.0
            return 2.0
        except Exception:
            return 4.0

    @classmethod
    def score_100_points(
        cls,
        topic: Dict[str, Any],
        existing_topics: Optional[List[Dict[str, Any]]] = None,
        recent_production_topics: Optional[List[str]] = None,
    ) -> TopicScoreBreakdown:
        """
        Calculates transparent 100-point opportunity score:
        - Information Value: 25 pts (technical depth & engineering substance)
        - Originality: 20 pts (novel angle vs historical database)
        - Evidence Quality: 20 pts (primary paper, repo, lab documentation)
        - Audience Relevance: 15 pts (builder utility & open-source applicability)
        - Visual Potential: 10 pts (diagram, UI, benchmark visualization)
        - Timeliness: 10 pts (freshness based on publication date)
        - Fatigue Penalty: 0 to -15 pts (recent topic saturation/repetition)
        """
        title = topic.get("title", "").lower()
        summary = topic.get("summary", "").lower()
        full_text = f"{title} {summary}"
        url = (topic.get("url") or topic.get("source_url") or "").lower()
        publisher = (topic.get("publisher") or "").lower()

        # 1. Information Value (max 25 pts)
        info_keywords = [
            "quantization", "fp8", "int4", "weights", "pruning", "latency", "throughput",
            "transformer", "state space", "mamba", "moe", "mixture of experts", "attention",
            "kernel", "cuda", "vram", "benchmark", "accuracy", "zero-shot", "fine-tuning",
            "inference", "distillation", "reasoning", "multimodal", "synthetic data", "linear",
            "draft model", "speculative decoding", "world model", "diffusion", "kv cache"
        ]
        info_matches = sum(1 for kw in info_keywords if kw in full_text)
        info_val = min(25.0, 8.0 + (info_matches * 3.5))
        if any(fluff in full_text for fluff in ["could change everything", "mind-blowing", "is crazy", "you won't believe"]):
            info_val = max(5.0, info_val - 8.0)

        # 2. Originality (max 20 pts)
        dup_penalty = 0.0
        if existing_topics:
            t_words = set(re.findall(r"\w{4,}", title))
            for ex in existing_topics:
                ex_title = ex.get("title", "").lower()
                ex_words = set(re.findall(r"\w{4,}", ex_title))
                if t_words and ex_words:
                    overlap = len(t_words & ex_words) / max(len(t_words), 1)
                    if overlap > 0.5:
                        dup_penalty += 12.0
                        break
        orig_val = max(3.0, 20.0 - dup_penalty)

        # 3. Evidence Quality (max 20 pts)
        evidence_val = 6.0
        if any(dom in url for dom in ["arxiv.org", "biorxiv.org", "github.com", "huggingface.co", "openreview.net"]):
            evidence_val = 20.0
        elif any(lab in publisher or lab in url for lab in ["deepmind", "openai", "anthropic", "meta", "microsoft", "google", "berkeley", "stanford", "mit"]):
            evidence_val = 18.0
        elif any(press in publisher or press in url for press in ["technologyreview.com", "arstechnica.com", "ieee.org"]):
            evidence_val = 14.0
        elif url.startswith("https://") and len(url) > 20:
            evidence_val = 10.0

        # 4. Audience Relevance (max 15 pts)
        eng_keywords = ["open source", "weights", "github", "api", "local", "deploy", "hardware", "edge", "production", "agent", "tooling"]
        eng_matches = sum(1 for kw in eng_keywords if kw in full_text)
        aud_val = min(15.0, 5.0 + (eng_matches * 2.5))

        # 5. Visual Potential (max 10 pts)
        vis_keywords = ["diagram", "architecture", "demo", "code", "benchmark", "visual", "robot", "vision", "graph", "chart", "pipeline"]
        vis_matches = sum(1 for kw in vis_keywords if kw in full_text)
        vis_val = min(10.0, 4.0 + (vis_matches * 2.0))

        # 6. Timeliness (max 10 pts)
        pub_date = topic.get("published_date") or topic.get("publication_date") or topic.get("discovered_at")
        time_val = cls._calculate_timeliness_score(pub_date)

        # 7. Fatigue Penalty (0 to -15 pts)
        fatigue_penalty = 0.0
        if recent_production_topics:
            t_words = set(re.findall(r"\b[a-z0-9]{4,}\b", title))
            for rec in recent_production_topics:
                r_words = set(re.findall(r"\b[a-z0-9]{4,}\b", rec.lower()))
                if t_words and r_words:
                    overlap = len(t_words & r_words)
                    if overlap >= 2 or (overlap == 1 and any(core in t_words & r_words for core in ["mamba", "speculative", "whisper", "deepseek"])):
                        fatigue_penalty = 15.0
                        break

        total_score = round(
            max(0.0, min(100.0, info_val + orig_val + evidence_val + aud_val + vis_val + time_val - fatigue_penalty)),
            1,
        )

        # Decision & Explainable Reasoning
        reasons: List[str] = []
        if total_score >= 80.0:
            decision = "HIGH_PRIORITY"
            reasons.append("High technical depth, primary evidence backing, and actionable builder utility.")
        elif total_score >= 65.0:
            decision = "CONSIDER"
            reasons.append("Solid information value and timeliness; suitable for editorial selection.")
        elif total_score >= 50.0:
            decision = "RESEARCH_FURTHER"
            reasons.append("Promising topic but requires additional supporting evidence or deeper technical confirmation.")
        else:
            decision = "REJECT"
            reasons.append("Insufficient technical depth, unverified secondary source, or topic fatigue.")

        if fatigue_penalty > 0:
            reasons.append(f"Subject fatigue penalty applied (-{fatigue_penalty} pts) due to recent documentary coverage.")
        if evidence_val >= 18.0:
            reasons.append(f"Primary technical source recognized ({publisher or 'Academic/Repository'}).")

        return TopicScoreBreakdown(
            information_value=round(info_val, 1),
            originality=round(orig_val, 1),
            evidence_quality=round(evidence_val, 1),
            audience_relevance=round(aud_val, 1),
            visual_potential=round(vis_val, 1),
            timeliness=round(time_val, 1),
            fatigue_penalty=round(fatigue_penalty, 1),
            decision=decision,
            reasoning=" ".join(reasons),
        )

    @classmethod
    def score_topic(
        cls,
        topic: Dict[str, Any],
        existing_topics: Optional[List[Dict[str, Any]]] = None,
        recent_production_topics: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Backward-compatible method returning dict with total score and breakdown."""
        breakdown = cls.score_100_points(topic, existing_topics, recent_production_topics)
        res = dict(topic)
        res["score"] = breakdown.total_score
        res["relevance_score"] = round(breakdown.information_value + breakdown.audience_relevance, 1)
        res["freshness_score"] = round(breakdown.timeliness * 10.0, 1)
        res["originality_score"] = round(breakdown.originality * 5.0, 1)
        res["score_breakdown"] = breakdown.to_dict()
        return res
