import re
from datetime import datetime, timezone
from typing import Dict, Any, List

class TopicScorer:
    """Calculates multi-dimensional editorial and algorithmic scoring for tech stories."""

    def __init__(self, db=None, config=None):
        self.db = db
        self.config = config

    def score_all_pending(self) -> List[Dict[str, Any]]:
        from core.database import Database
        db = self.db or Database()
        with db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM topics WHERE score = 0.0 OR score IS NULL")
            rows = [dict(r) for r in cursor.fetchall()]
            scored_list = []
            for t in rows:
                scored = self.score_topic(t)
                cursor.execute(
                    "UPDATE topics SET score = ?, relevance_score = ?, freshness_score = ? WHERE id = ?",
                    (scored["score"], scored.get("relevance_score", 0), scored.get("freshness_score", 0), t["id"])
                )
                scored_list.append(scored)
            return scored_list

    HIGH_RELEVANCE_KEYWORDS = [
        "breakthrough", "frontier", "llm", "reasoning", "multimodal",
        "benchmark", "open-source", "weights", "inference", "efficiency",
        "robotics", "autonomous", "humanoid", "agent", "cybersecurity",
        "zero-day", "quantum", "architecture", "vulnerability", "model"
    ]

    VISUAL_POTENTIAL_KEYWORDS = [
        "robot", "vision", "demo", "benchmark", "comparison", "speed",
        "architecture", "hardware", "chip", "humanoid", "visual", "graph"
    ]

    @classmethod
    def score_topic(cls, topic: Dict[str, Any], existing_topics: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        title = topic.get("title", "").lower()
        summary = topic.get("summary", "").lower()
        full_text = f"{title} {summary}"

        # 1. Relevance Score (0.0 to 2.0)
        matched_kw = [k for k in cls.HIGH_RELEVANCE_KEYWORDS if re.search(r'\b' + k + r'\b', full_text)]
        relevance_score = min(2.0, 0.4 + (len(matched_kw) * 0.3))

        # 2. Freshness Score (0.0 to 1.5)
        # Defaults to 1.2 for newly collected items
        freshness_score = 1.2
        pub_date_str = topic.get("published_date")
        if pub_date_str:
            try:
                # Basic recency bonus
                freshness_score = 1.3
            except Exception:
                pass

        # 3. Visual Potential & Audience Interest (0.0 to 1.5)
        v_matched = [k for k in cls.VISUAL_POTENTIAL_KEYWORDS if re.search(r'\b' + k + r'\b', full_text)]
        visual_score = min(1.5, 0.5 + (len(v_matched) * 0.25))

        # 4. Source Reliability Score (0.0 to 1.0)
        source_weight = float(topic.get("weight", 1.0))
        reliability_score = min(1.0, round(source_weight / 1.3, 2))

        # 5. Originality & Duplicate Penalty
        duplicate_penalty = 0.0
        if existing_topics:
            t_words = set(re.findall(r'\w{4,}', title))
            for ex in existing_topics:
                ex_title = ex.get("title", "").lower()
                ex_words = set(re.findall(r'\w{4,}', ex_title))
                if t_words and ex_words:
                    overlap = len(t_words & ex_words) / max(len(t_words), 1)
                    if overlap > 0.6:
                        duplicate_penalty = 1.5
                        break
        originality_score = max(0.0, 1.0 - duplicate_penalty)

        # Composite Score
        composite = round(
            (relevance_score * 0.35) +
            (freshness_score * 0.25) +
            (visual_score * 0.20) +
            (reliability_score * 0.10) +
            (originality_score * 0.10) -
            duplicate_penalty,
            2
        )
        composite = max(0.1, composite)

        topic["relevance_score"] = relevance_score
        topic["freshness_score"] = freshness_score
        topic["visual_score"] = visual_score
        topic["reliability_score"] = reliability_score
        topic["originality_score"] = originality_score
        topic["score"] = composite
        return topic

    @classmethod
    def rank_topics(cls, topics: List[Dict[str, Any]], existing: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        scored = [cls.score_topic(t, existing) for t in topics]
        return sorted(scored, key=lambda x: x["score"], reverse=True)
