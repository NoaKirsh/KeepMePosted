"""
Unit tests for NewsSummarizerAgent
Tests pure functions with no external dependencies.
"""

from datetime import datetime, timezone


class TestSummarizerPureFunctions:
    """Test pure functions in NewsSummarizerAgent."""

    def test_build_prompt_structure(self, summarizer):
        """Test that prompt has all required sections."""
        articles = [
            {"source": "TechCrunch", "title": "Test 1", "published": datetime.now(timezone.utc)},
        ]
        prompt = summarizer._build_prompt(articles, days=5)

        # Check all key sections are present
        required_sections = [
            "🚀 NEW TECHNOLOGIES & PRODUCTS:",
            "📈 BUSINESS & CORPORATE NEWS:",
            "💰 CAPITAL MARKETS & STOCKS:",
            "🎯 PRIORITY COMPANY UPDATES:",
            "🔍 MARKET ANALYSIS:",
            "🌍 INDUSTRY TRENDS & ANALYSIS:",
            "🌐 REGULATORY & POLICY:",
            "📊 WEEKLY INTELLIGENCE BRIEF:",
        ]
        for section in required_sections:
            assert section in prompt

    def test_build_prompt_respects_max_ai_and_timeframe(self, summarizer):
        """Test max_ai limit and timeframe in one test."""
        articles = [
            {
                "source": f"Source{i}",
                "title": f"Article {i}",
                "published": datetime.now(timezone.utc),
            }
            for i in range(20)  # More than max_ai (15)
        ]

        prompt = summarizer._build_prompt(articles, days=7)

        # Max AI limit
        assert "Article 0" in prompt
        assert "Article 14" in prompt
        assert "Article 15" not in prompt

        # Timeframe
        assert "from the last 7 days" in prompt

    def test_build_prompt_empty_articles(self, summarizer):
        """Test prompt generation with empty article list."""
        prompt = summarizer._build_prompt([], days=5)

        # Should still have structure
        assert "🚀 NEW TECHNOLOGIES & PRODUCTS:" in prompt
        assert "News articles:" in prompt
