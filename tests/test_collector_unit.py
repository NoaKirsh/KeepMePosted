"""
Unit tests for NewsCollectorAgent
"""

import pytest
from datetime import datetime, timezone
from agents.collector import NewsCollectorAgent


class TestCollectorPureFunctions:
    """Test pure functions in NewsCollectorAgent."""
    
    @pytest.fixture
    def collector(self):
        """Create a collector instance for testing."""
        config = {
            'hours_back': 120,
            'max_articles': 10
        }
        rss_feeds = {
            'TechCrunch': 'https://techcrunch.com/feed/',
            'The Verge': 'https://theverge.com/rss'
        }
        return NewsCollectorAgent(rss_feeds, config)
    
    def test_group_by_source_empty(self, collector):
        """Test grouping with no articles."""
        collector.collected_articles = []
        result = collector._group_by_source()
        
        assert result == {}
    
    def test_group_by_source_single_source(self, collector):
        """Test grouping articles from a single source."""
        collector.collected_articles = [
            {'source': 'TechCrunch', 'title': 'Article 1', 'published': datetime.now(timezone.utc)},
            {'source': 'TechCrunch', 'title': 'Article 2', 'published': datetime.now(timezone.utc)},
        ]
        result = collector._group_by_source()
        
        assert len(result) == 1
        assert 'TechCrunch' in result
        assert len(result['TechCrunch']) == 2
    
    def test_group_by_source_multiple_sources(self, collector):
        """Test grouping articles from multiple sources."""
        collector.collected_articles = [
            {'source': 'TechCrunch', 'title': 'Article 1', 'published': datetime.now(timezone.utc)},
            {'source': 'The Verge', 'title': 'Article 2', 'published': datetime.now(timezone.utc)},
            {'source': 'TechCrunch', 'title': 'Article 3', 'published': datetime.now(timezone.utc)},
        ]
        result = collector._group_by_source()
        
        assert len(result) == 2
        assert 'TechCrunch' in result
        assert 'The Verge' in result
        assert len(result['TechCrunch']) == 2
        assert len(result['The Verge']) == 1
    
    @pytest.mark.asyncio
    async def test_report_to_summarizer_empty(self, collector):
        """Test report generation with no articles."""
        collector.collected_articles = []
        result = await collector.report_to_summarizer()
        
        assert result == "No articles collected yet."
    
    @pytest.mark.asyncio
    async def test_report_to_summarizer_with_articles(self, collector):
        """Test report generation with articles."""
        collector.collected_articles = [
            {'source': 'TechCrunch', 'title': 'Article 1', 'published': datetime.now(timezone.utc)},
            {'source': 'TechCrunch', 'title': 'Article 2', 'published': datetime.now(timezone.utc)},
        ]
        result = await collector.report_to_summarizer()
        
        assert "I've collected 2 tech articles" in result
        assert "TechCrunch" in result
        assert "Article 1" in result
    
    @pytest.mark.asyncio
    async def test_report_to_summarizer_truncates_long_list(self, collector):
        """Test that report shows only top 3 articles per source."""
        collector.collected_articles = [
            {'source': 'TechCrunch', 'title': f'Article {i}', 'published': datetime.now(timezone.utc)}
            for i in range(5)
        ]
        result = await collector.report_to_summarizer()
        
        # Should show first 3 articles
        assert "Article 0" in result
        assert "Article 1" in result
        assert "Article 2" in result
        # Should indicate there are more
        assert "and 2 more articles" in result

