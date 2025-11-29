"""
Unit tests for utils module
"""

import pytest
from unittest.mock import patch
from utils.ai_client import get_google_ai_client


class TestAIClient:
    """Tests for AI client initialization."""

    @patch("google.generativeai.configure")
    def test_get_google_ai_client_success(self, mock_configure):
        """Test successful client initialization with valid API key."""
        with patch("utils.ai_client.CONFIG", {"google_api_key": "test_key_123"}):
            result = get_google_ai_client()

            # Should configure with the API key
            mock_configure.assert_called_once_with(api_key="test_key_123")
            # Should return the genai module
            assert result is not None

    def test_get_google_ai_client_missing_key(self):
        """Test that missing API key raises ValueError."""
        with patch("utils.ai_client.CONFIG", {"google_api_key": ""}):
            with pytest.raises(ValueError, match="GOOGLE_API_KEY not found"):
                get_google_ai_client()

    def test_get_google_ai_client_import_error(self):
        """Test that missing google-generativeai package raises ImportError."""
        with patch("utils.ai_client.CONFIG", {"google_api_key": "test_key"}):
            with patch("builtins.__import__", side_effect=ImportError):
                with pytest.raises(ImportError, match="Install: pip install google-generativeai"):
                    get_google_ai_client()
