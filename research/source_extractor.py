import re
import html
from typing import Dict, Any

class SourceExtractor:
    """Cleans raw RSS entries and extracts clean text and metadata."""
    
    @staticmethod
    def clean_text(raw_html: str) -> str:
        if not raw_html:
            return ""
        # Unescape HTML entities
        text = html.unescape(raw_html)
        # Remove script and style elements
        text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        # Remove all HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        # Collapse multiple whitespace characters into a single space
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @classmethod
    def process_entry(cls, entry: Any, feed_info: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a feedparser entry or dict into a standardized article dict."""
        def _get_field(obj: Any, key: str, default: Any = "") -> Any:
            if isinstance(obj, dict):
                return obj.get(key, default)
            return getattr(obj, key, default)

        raw_title = _get_field(entry, "title", "")
        title = cls.clean_text(raw_title)
        url = _get_field(entry, "link", "") or _get_field(entry, "url", "")
        summary = ""
        
        raw_summary = _get_field(entry, "summary", "") or _get_field(entry, "description", "")
        if not raw_summary:
            content_list = _get_field(entry, "content", None)
            if content_list and len(content_list) > 0:
                raw_summary = content_list[0].get("value", "") if isinstance(content_list[0], dict) else getattr(content_list[0], "value", "")
        
        summary = cls.clean_text(raw_summary)

        # Truncate summary if excessively long
        if len(summary) > 600:
            summary = summary[:597] + "..."

        published_date = ""
        if hasattr(entry, "published"):
            published_date = entry.published
        elif hasattr(entry, "updated"):
            published_date = entry.updated

        return {
            "title": title,
            "url": url,
            "publisher": feed_info.get("publisher", "Unknown Publisher"),
            "summary": summary,
            "category": feed_info.get("category", "Artificial Intelligence News"),
            "published_date": published_date,
            "status": "DISCOVERED",
            "score": 0.0,
            "weight": feed_info.get("weight", 1.0)
        }
