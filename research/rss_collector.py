import feedparser
import socket
from typing import List, Dict, Any, Optional

from core.config_manager import get_config
from core.database import get_db
from core.logger import get_logger
from research.source_extractor import SourceExtractor
from research.deduplicator import Deduplicator
from research.topic_ranker import TopicRanker

logger = get_logger("RSSCollector")

# Set socket timeout to prevent indefinite hangs
socket.setdefaulttimeout(12.0)

class RSSCollector:
    """Collects technology news from configured RSS feeds, cleans, scores, and stores them."""

    def __init__(self, db=None, config=None):
        self.config = config or get_config()
        self.db = db or get_db()

    def fetch_feed(self, feed_cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
        name = feed_cfg.get("name", "Unknown Feed")
        url = feed_cfg.get("url")
        if not url:
            return []

        logger.info(f"Fetching RSS feed: {name} ({url})")
        articles = []
        try:
            # feedparser handles redirects and gzip
            feed = feedparser.parse(url)
            if feed.bozo and not feed.entries:
                logger.warning(f"Feed parser reported issue for {name}: {feed.bozo_exception}")
                return []

            for entry in feed.entries:
                processed = SourceExtractor.process_entry(entry, feed_cfg)
                if processed["title"] and processed["url"]:
                    articles.append(processed)

            logger.info(f"Extracted {len(articles)} candidate articles from {name}")
        except Exception as e:
            logger.error(f"Failed to fetch feed {name}: {e}")

        return articles

    def collect_all(self, progress_callback: Optional[Any] = None) -> List[Dict[str, Any]]:
        """Fetch all configured feeds, deduplicate against DB, score, and persist new discoveries."""
        feeds = self.config.get("research.feeds") or self.config.get("research_feeds") or []
        if not feeds:
            logger.warning("No research feeds configured in config.yaml / config.json")
            return []

        all_candidates = []
        total_feeds = len(feeds)

        for idx, feed_cfg in enumerate(feeds):
            if progress_callback:
                progress_callback(int((idx / total_feeds) * 60), f"Fetching {feed_cfg.get('name')}")
            feed_articles = self.fetch_feed(feed_cfg)
            all_candidates.extend(feed_articles)

        if progress_callback:
            progress_callback(70, "Deduplicating articles...")

        # Get existing articles from DB for deduplication
        existing = self.db.get_articles(limit=500)
        unique_articles = Deduplicator.filter_duplicates(all_candidates, existing)

        if progress_callback:
            progress_callback(85, "Ranking topic relevance...")

        ranked_articles = TopicRanker.rank_articles(unique_articles)

        # Insert new unique articles into DB
        inserted_count = 0
        for article in ranked_articles:
            art_id = self.db.insert_article(article)
            if art_id:
                article["id"] = art_id
                inserted_count += 1

        logger.info(f"Research cycle complete: {len(all_candidates)} scanned, {len(ranked_articles)} unique, {inserted_count} new saved to database.")

        if progress_callback:
            progress_callback(100, f"Saved {inserted_count} new verified candidates.")

        return ranked_articles
