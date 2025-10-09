"""
Unit tests for NewsSummarizerAgent
"""

import pytest
from datetime import datetime, timezone
from agents.summarizer import NewsSummarizerAgent


class TestSummarizerPureFunctions:
    """Test pure functions in NewsSummarizerAgent."""
    
    @pytest.fixture
    def summarizer(self):
        """Create a summarizer instance for testing."""
        config = {
            'hours_back': 120,
            'max_ai': 15,
            'model': 'models/gemini-2.5-flash',
            'ai_tokens': 2000,
            'ai_temp': 0.7
        }
        return NewsSummarizerAgent(config)
    
    def test_build_prompt_structure(self, summarizer):
        """Test that prompt has correct structure."""
        articles = [
            {'source': 'TechCrunch', 'title': 'Test Article 1', 'published': datetime.now(timezone.utc)},
            {'source': 'The Verge', 'title': 'Test Article 2', 'published': datetime.now(timezone.utc)},
        ]
        days = 5
        
        prompt = summarizer._build_prompt(articles, days)
        
        # Check key sections are present
        assert "🚀 NEW TECHNOLOGIES & PRODUCTS:" in prompt
        assert "📈 BUSINESS & CORPORATE NEWS:" in prompt
        assert "💰 CAPITAL MARKETS & STOCKS:" in prompt
        assert "🎯 PRIORITY COMPANY UPDATES:" in prompt
        assert "🔍 MARKET ANALYSIS:" in prompt
        assert "🌍 INDUSTRY TRENDS & ANALYSIS:" in prompt
        assert "🌐 REGULATORY & POLICY:" in prompt
        assert "📊 WEEKLY INTELLIGENCE BRIEF:" in prompt
    
    def test_build_prompt_includes_articles(self, summarizer):
        """Test that prompt includes article titles."""
        articles = [
            {'source': 'TechCrunch', 'title': 'AI Breakthrough Announced', 'published': datetime.now(timezone.utc)},
            {'source': 'The Verge', 'title': 'New GPU Released', 'published': datetime.now(timezone.utc)},
        ]
        days = 5
        
        prompt = summarizer._build_prompt(articles, days)
        
        assert "AI Breakthrough Announced" in prompt
        assert "New GPU Released" in prompt
        assert "TechCrunch" in prompt
        assert "The Verge" in prompt
    
    def test_build_prompt_respects_max_ai_limit(self, summarizer):
        """Test that prompt limits articles to max_ai."""
        # Create more articles than max_ai
        articles = [
            {'source': f'Source{i}', 'title': f'Article {i}', 'published': datetime.now(timezone.utc)}
            for i in range(20)  # More than max_ai (15)
        ]
        days = 5
        
        prompt = summarizer._build_prompt(articles, days)
        
        # Should include first 15 articles
        assert "Article 0" in prompt
        assert "Article 14" in prompt
        # Should NOT include article 15 and beyond
        assert "Article 15" not in prompt
        assert "Article 19" not in prompt
    
    def test_build_prompt_includes_timeframe(self, summarizer):
        """Test that prompt mentions the correct timeframe."""
        articles = [
            {'source': 'TechCrunch', 'title': 'Test', 'published': datetime.now(timezone.utc)},
        ]
        days = 7
        
        prompt = summarizer._build_prompt(articles, days)
        
        assert f"from the last {days} days" in prompt
    
    def test_build_prompt_empty_articles(self, summarizer):
        """Test prompt generation with empty article list."""
        articles = []
        days = 5
        
        prompt = summarizer._build_prompt(articles, days)
        
        # Should still have structure
        assert "🚀 NEW TECHNOLOGIES & PRODUCTS:" in prompt
        # But no article content
        assert "News articles:" in prompt

