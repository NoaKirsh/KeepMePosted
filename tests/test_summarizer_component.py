"""
Component tests for NewsSummarizerAgent
Tests with mocked Gemini API.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.summarizer import NewsSummarizerAgent


@pytest.mark.unit
class TestSummarizerWithMockedAPI:
    """Test NewsSummarizerAgent with mocked Gemini API."""
    
    @pytest.mark.asyncio
    async def test_analyze_articles_success(self, summarizer, sample_articles, mock_gemini_response):
        """Test successful article analysis with mocked Gemini."""
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_gemini_response
        
        mock_genai = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.types.GenerationConfig = MagicMock()
        
        with patch('agents.summarizer.get_google_ai_client', return_value=mock_genai):
            result = await summarizer.analyze_articles(sample_articles)
        
        assert "NEW TECHNOLOGIES & PRODUCTS" in result
        assert "NVIDIA" in result
        mock_model.generate_content.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_analyze_articles_empty_list(self, summarizer):
        """Test handling of empty article list."""
        result = await summarizer.analyze_articles([])
        assert result == "No articles available for analysis."
    
    @pytest.mark.asyncio
    async def test_analyze_articles_blocked_responses(self, summarizer, sample_articles):
        """Test handling of all blocked response types (empty candidates and safety)."""
        mock_model = MagicMock()
        mock_genai = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.types.GenerationConfig = MagicMock()
        
        # Test 1: Empty candidates (completely blocked)
        mock_response = Mock()
        mock_response.text = ""
        mock_response.candidates = []
        mock_model.generate_content.return_value = mock_response
        
        with patch('agents.summarizer.get_google_ai_client', return_value=mock_genai):
            result = await summarizer.analyze_articles(sample_articles)
        
        assert "AI response was blocked" in result
        assert "Reason:" in result
        
        # Test 2: Safety blocked (empty parts)
        mock_candidate = Mock()
        mock_candidate.content.parts = []
        mock_candidate.finish_reason = 2  # SAFETY
        mock_response.candidates = [mock_candidate]
        mock_model.generate_content.return_value = mock_response
        
        with patch('agents.summarizer.get_google_ai_client', return_value=mock_genai):
            result = await summarizer.analyze_articles(sample_articles)
        
        assert "AI response was blocked" in result
        assert "SAFETY" in result
    
    @pytest.mark.asyncio
    async def test_analyze_articles_api_errors(self, summarizer, sample_articles):
        """Test handling of quota, rate limit, and API key errors."""
        mock_model = MagicMock()
        mock_genai = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.types.GenerationConfig = MagicMock()
        
        # Test quota/rate limit errors (both use same code path)
        mock_model.generate_content.side_effect = Exception("quota exceeded")
        
        with patch('agents.summarizer.get_google_ai_client', return_value=mock_genai):
            result = await summarizer.analyze_articles(sample_articles)
        
        assert "API Quota or Rate Limit Exceeded" in result
        
        # Test API key error
        mock_model.generate_content.side_effect = Exception("Invalid API key")
        
        with patch('agents.summarizer.get_google_ai_client', return_value=mock_genai):
            result = await summarizer.analyze_articles(sample_articles)
        
        assert "API Key Error" in result
        assert "GOOGLE_API_KEY" in result
    
    @pytest.mark.asyncio
    async def test_analyze_articles_generic_error(self, summarizer, sample_articles):
        """Test handling of generic errors."""
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("Unknown error")
        
        mock_genai = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.types.GenerationConfig = MagicMock()
        
        with patch('agents.summarizer.get_google_ai_client', return_value=mock_genai):
            result = await summarizer.analyze_articles(sample_articles)
        
        assert "Error creating AI summary" in result
        assert "Unknown error" in result
    
    @pytest.mark.asyncio
    async def test_analyze_articles_uses_correct_config(self, summarizer, sample_articles, mock_gemini_response):
        """Test that API is called with correct configuration."""
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_gemini_response
        
        mock_genai = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.types.GenerationConfig = MagicMock()
        
        with patch('agents.summarizer.get_google_ai_client', return_value=mock_genai):
            await summarizer.analyze_articles(sample_articles)
        
        # Verify correct model and config usage
        mock_genai.GenerativeModel.assert_called_once_with(summarizer.config['model'])
        call_kwargs = mock_model.generate_content.call_args[1]
        assert 'generation_config' in call_kwargs
        assert 'safety_settings' in call_kwargs
    
    @pytest.mark.asyncio
    async def test_analyze_articles_lazy_loads_and_caches_client(self, summarizer, sample_articles, mock_gemini_response):
        """Test that AI client is lazy-loaded and cached."""
        assert summarizer.genai is None
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_gemini_response
        
        mock_genai = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.types.GenerationConfig = MagicMock()
        
        with patch('agents.summarizer.get_google_ai_client', return_value=mock_genai) as mock_get_client:
            # First call
            await summarizer.analyze_articles(sample_articles)
            mock_get_client.assert_called_once()
            
            # Second call should use cache
            mock_get_client.reset_mock()
            await summarizer.analyze_articles(sample_articles)
            mock_get_client.assert_not_called()

