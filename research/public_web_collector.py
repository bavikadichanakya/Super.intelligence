"""
SUPER.INTELLIGENCEEE — Public Web Research Collector
Extracts publicly accessible editorial technology articles, academic papers, and technical blogs.
Features realistic browser headers, publication date extraction, and Tier-2 fallback
to AgentReach for WAF-protected or bot-filtered sites (403/405/429).
Strictly zero-budget, read-only, cookie-safe, and rate-limit compliant.
"""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from core.logger import get_logger

logger = get_logger("PublicWebCollector")


class PublicWebCollector:
    """Safely extracts publicly accessible editorial and academic technology documentation."""

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
    }

    @staticmethod
    def _parse_iso_date(raw_date: str) -> Optional[str]:
        """Attempts to parse varied date representations into UTC ISO 8601 string."""
        if not raw_date:
            return None
        raw = raw_date.strip()
        # ISO formats
        try:
            # Handle trailing Z or offset
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            return dt.astimezone(timezone.utc).isoformat()
        except Exception:
            pass

        # Try RFC 2822
        try:
            import email.utils
            parsed_tup = email.utils.parsedate_to_datetime(raw)
            if parsed_tup:
                return parsed_tup.astimezone(timezone.utc).isoformat()
        except Exception:
            pass

        # Match YYYY-MM-DD
        m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", raw)
        if m:
            return f"{m.group(1)}T00:00:00+00:00"

        return raw

    @classmethod
    def _extract_meta_date(cls, soup: BeautifulSoup) -> Optional[str]:
        """Extracts publication date from common HTML meta and time tags."""
        date_selectors = [
            ("meta", {"property": "article:published_time"}),
            ("meta", {"property": "og:published_time"}),
            ("meta", {"name": "publication_date"}),
            ("meta", {"name": "pubdate"}),
            ("meta", {"name": "date"}),
            ("meta", {"name": "dc.date"}),
            ("meta", {"name": "dc.date.issued"}),
            ("meta", {"property": "rnews:datePublished"}),
        ]
        for tag, attrs in date_selectors:
            el = soup.find(tag, attrs)
            if el and el.get("content"):
                parsed = cls._parse_iso_date(el["content"])
                if parsed:
                    return parsed

        # Check <time datetime="...">
        time_el = soup.find("time")
        if time_el:
            dt_attr = time_el.get("datetime") or time_el.text.strip()
            parsed = cls._parse_iso_date(dt_attr)
            if parsed:
                return parsed

        # Check JSON-LD schema
        for s in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(s.string or "{}")
                if isinstance(data, dict):
                    pub = data.get("datePublished") or data.get("uploadDate")
                    if pub:
                        parsed = cls._parse_iso_date(pub)
                        if parsed:
                            return parsed
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("datePublished"):
                            parsed = cls._parse_iso_date(item["datePublished"])
                            if parsed:
                                return parsed
            except Exception:
                continue

        return None

    @classmethod
    def _extract_publisher(cls, soup: BeautifulSoup, url: str) -> str:
        """Determines publisher name from meta tags or domain."""
        og_site = soup.find("meta", {"property": "og:site_name"})
        if og_site and og_site.get("content"):
            return og_site["content"].strip()
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace("www.", "")
        if "arxiv.org" in domain:
            return "arXiv"
        if "github.com" in domain:
            return "GitHub"
        if "theverge.com" in domain:
            return "The Verge"
        if "arstechnica.com" in domain:
            return "Ars Technica"
        if "technologyreview.com" in domain:
            return "MIT Technology Review"
        if "techcrunch.com" in domain:
            return "TechCrunch"
        if "venturebeat.com" in domain:
            return "VentureBeat"
        return domain.capitalize() if domain else "Primary Source"

    @classmethod
    def extract_page(cls, url: str, timeout_sec: float = 12.0) -> Optional[Dict[str, Any]]:
        """
        Extracts webpage content with automatic fallback to Agent Reach
        when encountering HTTP 403, 405, 429, or bot challenge blocks.
        """
        if not url or not url.startswith(("http://", "https://")):
            return None

        retrieval_ts = datetime.now(timezone.utc).isoformat()
        try:
            res = requests.get(url, headers=cls.DEFAULT_HEADERS, timeout=timeout_sec)
            
            # If blocked by WAF/405/429/403, attempt Tier-2 fallback
            if res.status_code in (403, 405, 429, 503):
                logger.warning(f"Direct request to {url} returned {res.status_code}. Attempting Agent Reach Tier-2 fallback.")
                fallback = cls._fallback_agent_reach(url)
                if fallback:
                    fallback["retrieval_timestamp"] = retrieval_ts
                    return fallback
                return None

            if res.status_code != 200:
                logger.warning(f"URL {url} responded with status {res.status_code}")
                return None

            soup = BeautifulSoup(res.text, "lxml")

            # Extract title
            title = ""
            og_title = soup.find("meta", {"property": "og:title"})
            if og_title and og_title.get("content"):
                title = og_title["content"].strip()
            elif soup.title and soup.title.string:
                title = soup.title.string.strip()
            h1 = soup.find("h1")
            if not title and h1 and h1.text:
                title = h1.text.strip()

            # Clean and extract text elements (paragraphs, blockquotes, article bodies)
            paragraphs = []
            for tag in soup.find_all(["p", "blockquote"]):
                txt = tag.get_text().strip()
                if txt.startswith("Abstract:"):
                    txt = txt[len("Abstract:"):].strip()
                if len(txt) > 35:
                    paragraphs.append(txt)

            if not paragraphs:
                body_container = soup.find("main") or soup.find("article") or soup.find("div", {"id": "readme"})
                if body_container:
                    for line in body_container.get_text().split("\n"):
                        line_clean = line.strip()
                        if len(line_clean) > 35:
                            paragraphs.append(line_clean)

            article_body = " ".join(paragraphs[:12])
            pub_date = cls._extract_meta_date(soup) or ""
            publisher = cls._extract_publisher(soup, url)

            return {
                "title": title or url,
                "url": url,
                "publisher": publisher,
                "publication_date": pub_date,
                "retrieval_timestamp": retrieval_ts,
                "summary": article_body[:600] + ("..." if len(article_body) > 600 else ""),
                "full_text": article_body,
                "status": "ACCESSIBLE",
            }
        except Exception as e:
            logger.warning(f"Direct extraction error for {url}: {e}. Trying Agent Reach fallback.")
            fallback = cls._fallback_agent_reach(url)
            if fallback:
                fallback["retrieval_timestamp"] = retrieval_ts
                return fallback
            return None

    @classmethod
    def _fallback_agent_reach(cls, url: str) -> Optional[Dict[str, Any]]:
        """Tier-2 retrieval via Agent Reach CLI."""
        try:
            from research.agent_reach_connector import AgentReachConnector
            connector = AgentReachConnector()
            if not connector.is_available():
                return None
            res = connector.read_web_page(url)
            if res.get("ok") and res.get("content"):
                content = res.get("content", "").strip()
                if len(content) >= 50:
                    parsed_domain = urlparse(url).netloc.replace("www.", "")
                    return {
                        "title": res.get("title") or url,
                        "url": url,
                        "publisher": parsed_domain.capitalize(),
                        "publication_date": "",
                        "retrieval_timestamp": datetime.now(timezone.utc).isoformat(),
                        "summary": content[:600] + ("..." if len(content) > 600 else ""),
                        "full_text": content[:4000],
                        "status": "ACCESSIBLE",
                    }
        except Exception as e:
            logger.warning(f"Agent Reach fallback failed for {url}: {e}")
        return None
