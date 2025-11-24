"""
Component tests for NewsCollectorAgent
Tests with mocked external dependencies (RSS feeds).
"""

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch
from agents.collector import NewsCollectorAgent


@pytest.mark.unit
class TestCollectorWithMockedFeeds:
    """Test NewsCollectorAgent with mocked feedparser."""
    
    @pytest.mark.asyncio
    async def test_collect_news_with_filtering_and_sorting(self, collector):
        """Test collection with date filtering and sorting in one test."""
        def mock_parse(url):
            mock_feed = Mock()
            # Mix of old and new entries to test filtering AND sorting
            old_entry = Mock()
            old_entry.title = "Old Article"
            old_entry.link = "https://example.com/old"
            old_entry.summary = "Old"
            old_entry.published_parsed = (datetime.now(timezone.utc) - timedelta(days=10)).timetuple()[:9]
            
            newer_entry = Mock()
            newer_entry.title = "Newer Article"
            newer_entry.link = "https://example.com/new"
            newer_entry.summary = "Newer"
            newer_entry.published_parsed = (datetime.now(timezone.utc) - timedelta(hours=1)).timetuple()[:9]
            
            older_entry = Mock()
            older_entry.title = "Older Article"
            older_entry.link = "https://example.com/older"
            older_entry.summary = "Older"
            older_entry.published_parsed = (datetime.now(timezone.utc) - timedelta(hours=5)).timetuple()[:9]
            
            mock_feed.entries = [old_entry, older_entry, newer_entry]  # Unsorted
            return mock_feed
        
        with patch('feedparser.parse', side_effect=mock_parse):
            articles = await collector.collect_news()
        
        # Old article should be filtered out
        assert all(article['title'] != "Old Article" for article in articles)
        # Articles should be sorted newest first
        newer_articles = [a for a in articles if 'Newer' in a['title']]
        older_articles = [a for a in articles if 'Older' in a['title']]
        if newer_articles and older_articles:
            assert articles.index(newer_articles[0]) < articles.index(older_articles[0])
    
    @pytest.mark.asyncio
    async def test_collect_news_respects_max_articles(self, collector):
        """Test that max_articles limit is enforced."""
        collector.config['max_articles'] = 5
        
        mock_feed = Mock()
        entries = []
        for i in range(10):
            entry = Mock()
            entry.title = f"Article {i}"
            entry.link = f"https://example.com/{i}"
            entry.summary = f"Summary {i}"
            entry.published_parsed = (datetime.now(timezone.utc) - timedelta(hours=1)).timetuple()[:9]
            entries.append(entry)
        mock_feed.entries = entries
        
        with patch('feedparser.parse', return_value=mock_feed):
            articles = await collector.collect_news()
        
        assert len(articles) == 5
    
    @pytest.mark.asyncio
    async def test_collect_news_handles_errors_gracefully(self, collector):
        """Test error handling for failed feeds and malformed entries."""
        def mock_parse(url):
            if "techcrunch.com" in url.lower():
                raise Exception("Network error")
            
            mock_feed = Mock()
            # Good entry
            good_entry = Mock()
            good_entry.title = "Good Article"
            good_entry.link = "https://example.com/good"
            good_entry.summary = "Good"
            good_entry.published_parsed = (datetime.now(timezone.utc) - timedelta(hours=1)).timetuple()[:9]
            
            # Malformed entry (missing link)
            bad_entry = Mock()
            bad_entry.title = "Bad Article"
            delattr(bad_entry, 'link') if hasattr(bad_entry, 'link') else None
            bad_entry.summary = "Bad"
            bad_entry.published_parsed = (datetime.now(timezone.utc) - timedelta(hours=1)).timetuple()[:9]
            
            mock_feed.entries = [bad_entry, good_entry]
            return mock_feed
        
        with patch('feedparser.parse', side_effect=mock_parse):
            articles = await collector.collect_news()
        
        # Should have articles from working feeds only
        assert len(articles) >= 2
        assert all(article['source'] != 'TechCrunch' for article in articles)
        assert all('link' in article for article in articles)
    
    @pytest.mark.asyncio
    async def test_collect_news_handles_missing_dates(self, collector):
        """Test handling of entries without published date."""
        mock_feed = Mock()
        entry = Mock()
        entry.title = "Article Without Date"
        entry.link = "https://example.com/no-date"
        entry.summary = "No date"
        entry.published_parsed = None
        mock_feed.entries = [entry]
        
        with patch('feedparser.parse', return_value=mock_feed):
            articles = await collector.collect_news()
        
        assert len(articles) >= 3
        assert all('published' in article for article in articles)
    
    @pytest.mark.asyncio
    async def test_collect_news_empty_feed(self, collector):
        """Test handling of empty RSS feed."""
        mock_feed = Mock()
        mock_feed.entries = []
        
        with patch('feedparser.parse', return_value=mock_feed):
            articles = await collector.collect_news()
        
        assert articles == []

