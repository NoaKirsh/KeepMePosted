"""
Google AI Client Utility
Handles initialization and configuration of Google Gemini client.
"""

from config import CONFIG


def get_google_ai_client():
    """Initialize and return Google Gemini client.

    Returns:
        genai.Client: Configured Google Generative AI client instance

    Raises:
        ValueError: If GOOGLE_API_KEY is not found in configuration
        ImportError: If google-generativeai package is not installed
    """
    try:
        import google.generativeai as genai

        if not CONFIG["google_api_key"]:
            raise ValueError("GOOGLE_API_KEY not found. Set it in .env file.")

        # Configure API key globally - required for genai.GenerativeModel()
        genai.configure(api_key=CONFIG["google_api_key"])
        return genai
    except ImportError:
        raise ImportError("Install: pip install google-generativeai")
