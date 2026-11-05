import re
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from typing import List, Dict, Any, Set

class Deduplicator:
    """Detects and removes duplicate articles based on normalized URLs and fuzzy title similarity."""

    @staticmethod
    def normalize_url(url: str) -> str:
        """Strip tracking query parameters (utm_*, ref, etc.) and trailing slashes."""
        if not url:
            return ""
        parsed = urlparse(url.strip())
        # Filter out tracking query params
        keep_params = [(k, v) for k, v in parse_qsl(parsed.query) if not k.startswith("utm_") and k not in ("ref", "fbclid", "gclid")]
        clean_query = urlencode(keep_params)
        clean_path = parsed.path.rstrip("/")
        normalized = urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), clean_path, parsed.params, clean_query, ""))
        return normalized

    @staticmethod
    def tokenize_title(title: str) -> Set[str]:
        """Convert title to normalized word set for similarity checking."""
        words = re.findall(r'\b[a-z0-9]{3,}\b', title.lower())
        stopwords = {"the", "and", "for", "with", "from", "that", "this", "new", "how", "why", "what", "are", "has"}
        return set(w for w in words if w not in stopwords)

    @classmethod
    def title_similarity(cls, title1: str, title2: str) -> float:
        """Calculate Jaccard similarity between two titles."""
        set1 = cls.tokenize_title(title1)
        set2 = cls.tokenize_title(title2)
        if not set1 or not set2:
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    @classmethod
    def filter_duplicates(cls, new_articles: List[Dict[str, Any]], existing_articles: List[Dict[str, Any]], threshold: float = 0.65) -> List[Dict[str, Any]]:
        """Filter out duplicates against both existing database records and intra-batch duplicates."""
        seen_urls = set(cls.normalize_url(a.get("url", "")) for a in existing_articles)
        existing_titles = [a.get("title", "") for a in existing_articles if a.get("title")]

        unique_articles = []
        for article in new_articles:
            raw_url = article.get("url", "")
            norm_url = cls.normalize_url(raw_url)
            title = article.get("title", "")

            if not raw_url or not title or len(title) < 5:
                continue

            if norm_url in seen_urls:
                continue

            # Check fuzzy title similarity against existing and already accepted in current batch
            is_dup = False
            for prev_title in existing_titles:
                if cls.title_similarity(title, prev_title) >= threshold:
                    is_dup = True
                    break

            if not is_dup:
                seen_urls.add(norm_url)
                existing_titles.append(title)
                unique_articles.append(article)

        return unique_articles
