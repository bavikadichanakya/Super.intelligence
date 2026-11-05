import re
from datetime import datetime, timezone
from typing import Dict, Any, List

AI_HIGH_VALUE_KEYWORDS = [
    "artificial intelligence", "foundation model", "llm", "deep learning",
    "neural", "breakthrough", "benchmark", "reasoning", "agent", "robotics",
    "humanoid", "semiconductor", "quantum", "cybersecurity", "zero-day",
    "open-source", "gpu", "inference", "multimodal", "generative ai",
    "superintelligence", "reinforcement learning", "autonomous"
]

class TopicRanker:
    """Scores technology stories on relevance, publisher authority, recency, and audience interest."""

    @classmethod
    def calculate_score(cls, article: Dict[str, Any]) -> float:
        title = (article.get("title") or "").lower()
        summary = (article.get("summary") or "").lower()
        full_text = f"{title} {summary}"

        # 1. Base score from publisher weight
        publisher_weight = article.get("weight", 1.0)
        base_score = 40.0 * publisher_weight

        # 2. Keyword relevance scoring
        keyword_hits = 0
        for kw in AI_HIGH_VALUE_KEYWORDS:
            if kw in title:
                keyword_hits += 3
            elif kw in summary:
                keyword_hits += 1
        keyword_score = min(35.0, keyword_hits * 3.5)

        # 3. Recency scoring
        recency_score = 15.0  # default for recent/undated
        pub_date_str = article.get("published_date")
        if pub_date_str:
            # Check for current year in string
            current_year = str(datetime.now(timezone.utc).year)
            if current_year in pub_date_str:
                recency_score = 20.0
            else:
                recency_score = 10.0

        # 4. Impact boost (actionable advancements)
        action_boost = 0.0
        if re.search(r'\b(unveils|launches|releases|achieves|discovers|demonstrates|surpasses|builds)\b', title):
            action_boost += 8.0

        # Penalize vague roundups / sponsored style
        if re.search(r'\b(best deals|discount|roundup|how to buy|top 10 gifts|sponsored)\b', title):
            action_boost -= 25.0

        total_score = max(0.0, min(100.0, base_score + keyword_score + recency_score + action_boost))
        return round(total_score, 1)

    @classmethod
    def rank_articles(cls, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for art in articles:
            art["score"] = cls.calculate_score(art)
        articles.sort(key=lambda x: x["score"], reverse=True)
        return articles
