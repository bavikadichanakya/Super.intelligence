import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
from core.logger import get_logger

logger = get_logger("PublicWebCollector")

class PublicWebCollector:
    """Safely extracts publicly accessible editorial technology articles."""

    USER_AGENT = "SUPER.INTELLIGENCEEE-Researcher/2.0 (Open Technology Media; +http://super.intelligenceee.local)"

    @classmethod
    def extract_page(cls, url: str, timeout_sec: float = 10.0) -> Optional[Dict[str, Any]]:
        if not url or not url.startswith(("http://", "https://")):
            return None

        headers = {"User-Agent": cls.USER_AGENT}
        try:
            res = requests.get(url, headers=headers, timeout=timeout_sec)
            if res.status_code != 200:
                logger.warning(f"URL {url} responded with status {res.status_code}")
                return None

            soup = BeautifulSoup(res.text, "lxml")
            
            # Extract title
            title = ""
            if soup.title and soup.title.string:
                title = soup.title.string.strip()
            h1 = soup.find("h1")
            if h1 and h1.text:
                title = h1.text.strip()

            # Extract paragraphs
            paragraphs = []
            for p in soup.find_all("p"):
                txt = p.get_text().strip()
                if len(txt) > 40:
                    paragraphs.append(txt)

            article_body = " ".join(paragraphs[:8])
            return {
                "title": title,
                "url": url,
                "summary": article_body[:600] + ("..." if len(article_body) > 600 else ""),
                "full_text": article_body
            }
        except Exception as e:
            logger.warning(f"Could not extract page {url}: {e}")
            return None

