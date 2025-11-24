"""
Component tests for TechNewsOrchestrator
Tests orchestrator with mocked agents.
"""

import pytest
from unittest.mock import AsyncMock
from agents.orchestrator import TechNewsOrchestrator


@pytest.mark.unit
class TestOrchestratorComponent:
    """Test TechNewsOrchestrator with mocked agents."""
    
    @pytest.mark.asyncio
    async def test_initialize_agents_success(self, orchestrator):
        """Test successful agent initialization."""
        await orchestrator.initialize_agents()
        assert orchestrator.collector is not None
        assert orchestrator.summarizer is not None
    
    @pytest.mark.asyncio
    async def test_initialize_agents_invalid_api_key(self, sample_rss_feeds):
        """Test initialization fails with empty or None API key."""
        for invalid_key in ['', None]:
            config = {'hours_back': 120, 'max_articles': 10, 'google_api_key': invalid_key}
            orchestrator = TechNewsOrchestrator(config, sample_rss_feeds)
            
            with pytest.raises(ValueError, match="GOOGLE_API_KEY not found"):
                await orchestrator.initialize_agents()
    
    @pytest.mark.asyncio
    async def test_run_dialog_workflow_success(self, orchestrator, sample_articles):
        """Test successful workflow execution."""
        orchestrator.collector.collect_news = AsyncMock(return_value=sample_articles)
        orchestrator.collector.report_to_summarizer = AsyncMock(return_value="Report")
        orchestrator.collector.collected_articles = sample_articles
        orchestrator.summarizer.analyze_articles = AsyncMock(return_value="Analysis")
        
        result = await orchestrator.run_dialog_workflow()
        
        orchestrator.collector.collect_news.assert_called_once()
        orchestrator.collector.report_to_summarizer.assert_called_once()
        orchestrator.summarizer.analyze_articles.assert_called_once_with(sample_articles)
        assert result == "Analysis"
    
    @pytest.mark.asyncio
    async def test_run_dialog_workflow_empty_articles(self, orchestrator):
        """Test workflow with no articles collected."""
        orchestrator.collector.collect_news = AsyncMock(return_value=[])
        orchestrator.collector.report_to_summarizer = AsyncMock(return_value="No articles")
        orchestrator.collector.collected_articles = []
        orchestrator.summarizer.analyze_articles = AsyncMock(return_value="No articles available")
        
        result = await orchestrator.run_dialog_workflow()
        
        assert "No articles available" in result
    
    @pytest.mark.asyncio
    async def test_run_dialog_workflow_error_propagation(self, orchestrator, sample_articles):
        """Test error propagation from collector and summarizer."""
        # Test collector error
        orchestrator.collector.collect_news = AsyncMock(side_effect=Exception("RSS error"))
        
        with pytest.raises(Exception, match="RSS error"):
            await orchestrator.run_dialog_workflow()
        
        # Test summarizer error
        orchestrator.collector.collect_news = AsyncMock(return_value=sample_articles)
        orchestrator.collector.report_to_summarizer = AsyncMock(return_value="Report")
        orchestrator.collector.collected_articles = sample_articles
        orchestrator.summarizer.analyze_articles = AsyncMock(side_effect=Exception("API error"))
        
        with pytest.raises(Exception, match="API error"):
            await orchestrator.run_dialog_workflow()
    
    @pytest.mark.asyncio
    async def test_simulate_dialog_variations(self, orchestrator, sample_articles):
        """Test dialog simulation with various article counts."""
        # Test with articles
        orchestrator.collector.collected_articles = sample_articles
        await orchestrator._simulate_dialog(sample_articles)
        
        # Test with empty articles
        orchestrator.collector.collected_articles = []
        await orchestrator._simulate_dialog([])
        
        # Test with priority companies
        priority_articles = [
            {'source': 'NVIDIA', 'title': 'GPU', 'published': None},
            {'source': 'NVIDIA', 'title': 'AI', 'published': None},
            {'source': 'Intel', 'title': 'CPU', 'published': None},
        ]
        orchestrator.collector.collected_articles = priority_articles
        await orchestrator._simulate_dialog(priority_articles)
        
        # Test without priority companies
        other_articles = [
            {'source': 'TechCrunch', 'title': 'Article', 'published': None},
        ]
        orchestrator.collector.collected_articles = other_articles
        await orchestrator._simulate_dialog(other_articles)
    
    def test_orchestrator_initialization(self, sample_config, sample_rss_feeds):
        """Test orchestrator creates correct agent types."""
        from agents.collector import NewsCollectorAgent
        from agents.summarizer import NewsSummarizerAgent
        
        orchestrator = TechNewsOrchestrator(sample_config, sample_rss_feeds)
        
        assert orchestrator.config == sample_config
        assert isinstance(orchestrator.collector, NewsCollectorAgent)
        assert isinstance(orchestrator.summarizer, NewsSummarizerAgent)
    
    @pytest.mark.asyncio
    async def test_workflow_order_of_operations(self, orchestrator, sample_articles):
        """Test that workflow steps execute in correct order."""
        call_order = []
        
        async def mock_collect():
            call_order.append('collect')
            return sample_articles
        
        async def mock_report():
            call_order.append('report')
            return "Report"
        
        async def mock_analyze(articles):
            call_order.append('analyze')
            return "Analysis"
        
        orchestrator.collector.collect_news = mock_collect
        orchestrator.collector.report_to_summarizer = mock_report
        orchestrator.collector.collected_articles = sample_articles
        orchestrator.summarizer.analyze_articles = mock_analyze
        
        await orchestrator.run_dialog_workflow()
        
        assert call_order == ['collect', 'report', 'analyze']

