"""
SUPER.INTELLIGENCEEE — Topic & Source Deduplicator
Detects and filters exact URL matches, tracking-parameter variants,
and semantic title / subject overlap to prevent duplicate documentary coverage.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Set, Tuple
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


class Deduplicator:
    """Detects and removes duplicate articles and topics based on normalized URLs and semantic similarity."""

    TRACKING_PARAMS = {
        "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
        "ref", "fbclid", "gclid", "msclkid", "mc_cid", "mc_eid", "source", "share"
    }

    STOPWORDS = {
        "the", "and", "for", "with", "from", "that", "this", "new", "how", "why",
        "what", "are", "has", "have", "been", "was", "were", "into", "over", "about",
        "more", "than", "will", "can", "could", "should", "your", "their", "our",
    }

    @classmethod
    def normalize_url(cls, url: str) -> str:
        """Strip tracking query parameters, hashes, and normalize scheme/host/path."""
        if not url:
            return ""
        parsed = urlparse(url.strip())
        # Filter out tracking query params
        keep_params = [
            (k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=False)
            if k.lower() not in cls.TRACKING_PARAMS and not k.lower().startswith("utm_")
        ]
        clean_query = urlencode(sorted(keep_params))
        clean_path = parsed.path.rstrip("/")
        normalized = urlunparse((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            clean_path,
            parsed.params,
            clean_query,
            ""  # strip fragment
        ))
        return normalized

    @classmethod
    def tokenize_title(cls, title: str) -> Set[str]:
        """Convert title to normalized word set for similarity checking."""
        words = re.findall(r"\b[a-z0-9]{3,}\b", title.lower())
        return set(w for w in words if w not in cls.STOPWORDS)

    @classmethod
    def title_similarity(cls, title1: str, title2: str) -> float:
        """Calculate Jaccard similarity between two title word sets."""
        set1 = cls.tokenize_title(title1)
        set2 = cls.tokenize_title(title2)
        if not set1 or not set2:
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    @classmethod
    def filter_duplicates_with_report(
        cls,
        new_articles: List[Dict[str, Any]],
        existing_articles: List[Dict[str, Any]],
        threshold: float = 0.65,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Filters duplicates against existing articles and within the batch.
        Returns:
            (unique_articles, duplicate_records)
        """
        seen_urls: Set[str] = set()
        seen_items: List[Dict[str, Any]] = []

        for a in existing_articles:
            u = cls.normalize_url(a.get("url", ""))
            if u:
                seen_urls.add(u)
            if a.get("title"):
                seen_items.append({"title": a.get("title", ""), "url": u, "source": "historical_database"})

        unique_articles: List[Dict[str, Any]] = []
        duplicate_records: List[Dict[str, Any]] = []

        for article in new_articles:
            raw_url = article.get("url", "")
            norm_url = cls.normalize_url(raw_url)
            title = article.get("title", "").strip()

            if not raw_url or not title or len(title) < 5:
                continue

            # 1. Exact or normalized URL match
            if norm_url in seen_urls:
                duplicate_records.append({
                    "title": title,
                    "url": raw_url,
                    "reason": "EXACT_OR_NORMALIZED_URL_MATCH",
                    "matched_url": norm_url,
                })
                continue

            # 2. Semantic title similarity
            is_dup = False
            for prev in seen_items:
                sim = cls.title_similarity(title, prev["title"])
                if sim >= threshold:
                    is_dup = True
                    duplicate_records.append({
                        "title": title,
                        "url": raw_url,
                        "reason": f"SEMANTIC_SIMILARITY ({sim:.2f} >= {threshold:.2f})",
                        "matched_title": prev["title"],
                        "similarity_score": round(sim, 3),
                    })
                    break

            if not is_dup:
                seen_urls.add(norm_url)
                seen_items.append({"title": title, "url": norm_url, "source": "current_batch"})
                unique_articles.append(article)

        return unique_articles, duplicate_records

    @classmethod
    def filter_duplicates(
        cls,
        new_articles: List[Dict[str, Any]],
        existing_articles: List[Dict[str, Any]],
        threshold: float = 0.65,
    ) -> List[Dict[str, Any]]:
        """Backward-compatible wrapper returning only unique articles."""
        uniques, _ = cls.filter_duplicates_with_report(new_articles, existing_articles, threshold)
        return uniques
