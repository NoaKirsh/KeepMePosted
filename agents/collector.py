"""
News Collector Agent
Responsible for fetching and processing RSS feeds from tech news sources.
"""

import logging
import feedparser
from datetime import datetime, timedelta, timezone
from typing import List, Dict


class NewsCollectorAgent:
    """Agent responsible for collecting news from RSS feeds."""

    def __init__(self, rss_feeds: Dict[str, str], config: Dict):
        self.rss_feeds = rss_feeds
        self.config = config
        self.collected_articles = []
        self.logger = logging.getLogger(self.__class__.__name__)

    async def collect_news(self) -> List[Dict]:
        """Collect news articles from RSS feeds."""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=self.config["hours_back"])
        articles = []
        days = self.config["hours_back"] // 24

        print(f"\n🔍 Collecting articles from the last {days} days...")

        for idx, (source, url) in enumerate(self.rss_feeds.items(), 1):
            try:
                print(
                    f"   [{idx}/{len(self.rss_feeds)}] Fetching from {source}...",
                    end=" ",
                    flush=True,
                )
                feed = feedparser.parse(url)
                print(f"✓ ({len(feed.entries)} entries)")

                for entry in feed.entries:
                    try:
                        published = (
                            datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                            if hasattr(entry, "published_parsed") and entry.published_parsed
                            else datetime.now(timezone.utc)
                        )

                        if published > cutoff:
                            articles.append(
                                {
                                    "source": source,
                                    "title": entry.title,
                                    "link": entry.link,
                                    "published": published,
                                    "summary": getattr(entry, "summary", ""),
                                }
                            )
                    except Exception as e:
                        self.logger.warning(f"Error parsing entry from {source}: {e}")
            except Exception as e:
                print("✗ Error")
                self.logger.error(f"Error fetching from {source}: {e}")

        self.collected_articles = sorted(articles, key=lambda x: x["published"], reverse=True)[
            : self.config["max_articles"]
        ]
        print(f"✅ Successfully collected {len(self.collected_articles)} articles\n")
        return self.collected_articles

    def _group_by_source(self) -> Dict[str, List[Dict]]:
        """Group articles by source."""
        by_source = {}
        for article in self.collected_articles:
            by_source.setdefault(article["source"], []).append(article)
        return by_source

    async def report_to_summarizer(self) -> str:
        """Report collected articles to the summarizer agent."""
        if not self.collected_articles:
            return "No articles collected yet."

        days = self.config["hours_back"] // 24
        report = f"I've collected {len(self.collected_articles)} tech articles from the last {days} days. Here's what I found:\n\n"

        for source, source_articles in self._group_by_source().items():
            report += f"**{source}** ({len(source_articles)} articles):\n"
            for article in source_articles[:3]:
                report += f"- {article['title']}\n"
            if len(source_articles) > 3:
                report += f"  ... and {len(source_articles) - 3} more articles\n"
            report += "\n"

        return report
