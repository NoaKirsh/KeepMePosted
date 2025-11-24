"""
Tests pure functions with no external dependencies.
"""

import pytest
from datetime import datetime, timezone
from agents.collector import NewsCollectorAgent


class TestCollectorPureFunctions:
    """Test pure functions in NewsCollectorAgent."""
    
    def test_group_by_source_empty(self, collector):
        """Test grouping with no articles."""
        collector.collected_articles = []
        result = collector._group_by_source()
        assert result == {}
    
    def test_group_by_source_multiple_sources(self, collector):
        """Test grouping articles from multiple sources."""
        collector.collected_articles = [
            {'source': 'TechCrunch', 'title': 'Article 1', 'published': datetime.now(timezone.utc)},
            {'source': 'The Verge', 'title': 'Article 2', 'published': datetime.now(timezone.utc)},
            {'source': 'TechCrunch', 'title': 'Article 3', 'published': datetime.now(timezone.utc)},
        ]
        result = collector._group_by_source()
        
        assert len(result) == 2
        assert len(result['TechCrunch']) == 2
        assert len(result['The Verge']) == 1
    
    @pytest.mark.asyncio
    async def test_report_to_summarizer_empty(self, collector):
        """Test report generation with no articles."""
        collector.collected_articles = []
        result = await collector.report_to_summarizer()
        assert result == "No articles collected yet."
    
    @pytest.mark.asyncio
    async def test_report_to_summarizer_with_truncation(self, collector):
        """Test report generation with articles and truncation."""
        collector.collected_articles = [
            {'source': 'TechCrunch', 'title': f'Article {i}', 'published': datetime.now(timezone.utc)}
            for i in range(5)
        ]
        result = await collector.report_to_summarizer()
        
        assert "I've collected 5 tech articles" in result
        assert "TechCrunch" in result
        # Should show first 3 and indicate more
        assert "Article 0" in result
        assert "Article 2" in result
        assert "and 2 more articles" in result

