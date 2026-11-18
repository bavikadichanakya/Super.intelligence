"""
SUPER.INTELLIGENCEEE — Source Extractor & Metadata Normalizer
Cleans raw RSS entries, parses publication dates to standard UTC ISO 8601 strings,
and guarantees complete provenance attributes.
"""

from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class SourceExtractor:
    """Cleans raw RSS/Atom entries and extracts standardized metadata and normalized dates."""

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

    @staticmethod
    def normalize_date(raw_date: Any) -> str:
        """Converts varied date strings or time tuples into normalized UTC ISO 8601 string."""
        if not raw_date:
            return ""

        # Handle time.struct_time if provided by feedparser (e.g. published_parsed)
        if isinstance(raw_date, (tuple, list)) and len(raw_date) >= 6:
            try:
                import time
                dt = datetime.fromtimestamp(time.mktime(raw_date), tz=timezone.utc)
                return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                pass

        s = str(raw_date).strip()
        if not s:
            return ""

        # Match pure date YYYY-MM-DD directly
        m = re.match(r"^(\d{4}-\d{2}-\d{2})$", s)
        if m:
            return f"{m.group(1)}T00:00:00Z"

        # Try ISO 8601
        try:
            clean_s = s.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean_s)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            pass

        # Try RFC 2822 (e.g., 'Sat, 07 Nov 2026 10:15:00 GMT')
        try:
            import email.utils
            dt = email.utils.parsedate_to_datetime(s)
            if dt:
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            pass

        # Substring match YYYY-MM-DD
        m_sub = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", s)
        if m_sub:
            return f"{m_sub.group(1)}T00:00:00Z"

        return s

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
        if len(summary) > 600:
            summary = summary[:597] + "..."

        raw_date = ""
        # Prefer parsed struct_time if available
        parsed_time = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
        if parsed_time:
            raw_date = parsed_time
        elif hasattr(entry, "published"):
            raw_date = entry.published
        elif hasattr(entry, "updated"):
            raw_date = entry.updated

        normalized_pub_date = cls.normalize_date(raw_date)
        retrieval_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        return {
            "title": title,
            "url": url,
            "publisher": feed_info.get("publisher", "Unknown Publisher"),
            "summary": summary,
            "category": feed_info.get("category", "Artificial Intelligence News"),
            "published_date": normalized_pub_date,
            "retrieval_timestamp": retrieval_timestamp,
            "status": "DISCOVERED",
            "score": 0.0,
            "weight": feed_info.get("weight", 1.0),
        }
