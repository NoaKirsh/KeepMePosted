"""
Shared pytest fixtures for KeepMePosted tests.

Fixtures are organized into sections:
1. Configuration Fixtures - Test configs and RSS feeds
2. Article Data Fixtures - Sample articles for testing
3. Mock RSS Feed Fixtures - Mocked feedparser objects
4. Mock Gemini API Fixtures - Mocked Google AI responses
5. Mock Email/SMTP Fixtures - Email configs and SMTP mocks
6. Agent Instance Fixtures - Pre-configured agent instances
"""

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, MagicMock
from agents.collector import NewsCollectorAgent
from agents.summarizer import NewsSummarizerAgent
from agents.orchestrator import TechNewsOrchestrator
from agents.email_sender import EmailAgent


# =============================================================================
# CONFIGURATION FIXTURES
# =============================================================================
# Test configuration and RSS feed data


@pytest.fixture
def sample_config():
    """Standard test configuration with all required settings."""
    return {
        "hours_back": 120,
        "max_articles": 10,
        "max_ai": 15,
        "google_api_key": "test_api_key_12345",
        "model": "models/gemini-2.5-flash",
        "ai_tokens": 2000,
        "ai_temp": 0.7,
    }


@pytest.fixture
def sample_rss_feeds():
    """Standard RSS feeds for testing (3 feeds)."""
    return {
        "TechCrunch": "https://techcrunch.com/feed/",
        "The Verge": "https://theverge.com/rss",
        "NVIDIA": "https://nvidianews.nvidia.com/rss",
    }


# =============================================================================
# ARTICLE DATA FIXTURES
# =============================================================================
# Sample article data for testing collector and summarizer


@pytest.fixture
def sample_article():
    """A single sample article with all required fields."""
    return {
        "source": "TechCrunch",
        "title": "Breaking: New AI Model Released",
        "link": "https://example.com/article1",
        "published": datetime.now(timezone.utc),
        "summary": "A revolutionary new AI model has been announced.",
    }


@pytest.fixture
def sample_articles():
    """Multiple sample articles with staggered timestamps (4 articles)."""
    base_time = datetime.now(timezone.utc)
    return [
        {
            "source": "TechCrunch",
            "title": "NVIDIA Announces New GPU Architecture",
            "link": "https://example.com/nvidia-gpu",
            "published": base_time - timedelta(hours=2),
            "summary": "NVIDIA revealed its next-generation GPU architecture.",
        },
        {
            "source": "The Verge",
            "title": "Intel CEO Discusses Future Plans",
            "link": "https://example.com/intel-ceo",
            "published": base_time - timedelta(hours=5),
            "summary": "Intel's CEO outlined the company's roadmap.",
        },
        {
            "source": "NVIDIA",
            "title": "NVIDIA Partners with Major Cloud Provider",
            "link": "https://example.com/nvidia-partnership",
            "published": base_time - timedelta(hours=10),
            "summary": "NVIDIA announced a strategic partnership.",
        },
        {
            "source": "TechCrunch",
            "title": "AMD Releases New Processor Line",
            "link": "https://example.com/amd-processor",
            "published": base_time - timedelta(hours=15),
            "summary": "AMD launched its latest processor family.",
        },
    ]


@pytest.fixture
def old_articles():
    """Articles that are too old (beyond cutoff date) for filtering tests."""
    old_time = datetime.now(timezone.utc) - timedelta(days=10)
    return [
        {
            "source": "TechCrunch",
            "title": "Old News Article",
            "link": "https://example.com/old",
            "published": old_time,
            "summary": "This article is too old.",
        }
    ]


# =============================================================================
# MOCK RSS FEED FIXTURES
# =============================================================================
# Mocked feedparser objects for testing RSS collection


@pytest.fixture
def mock_rss_entry():
    """Mock RSS entry object from feedparser with all standard fields."""
    entry = Mock()
    entry.title = "Test Article Title"
    entry.link = "https://example.com/test"
    entry.summary = "Test article summary"
    entry.published_parsed = (2024, 10, 14, 12, 0, 0, 0, 0, 0)
    return entry


@pytest.fixture
def mock_rss_feed():
    """Mock RSS feed object from feedparser (empty feed by default)."""
    feed = Mock()
    feed.entries = []
    feed.bozo = False  # No errors
    return feed


# =============================================================================
# MOCK GEMINI API FIXTURES
# =============================================================================
# Mocked Google Generative AI responses for testing summarizer


@pytest.fixture
def mock_gemini_response():
    """Mock successful Gemini API response with structured content."""
    response = Mock()
    response.text = """**🚀 NEW TECHNOLOGIES & PRODUCTS:**
- NVIDIA announced new GPU architecture with 2x performance

**📈 BUSINESS & CORPORATE NEWS:**
- Intel CEO discussed future roadmap

**💰 CAPITAL MARKETS & STOCKS:**
- NVIDIA stock up 5% on strong earnings

**🎯 PRIORITY COMPANY UPDATES:**
- NVIDIA: Leading in AI datacenter market
- Intel: Focusing on foundry business"""

    # Mock candidates structure (Gemini response format)
    candidate = Mock()
    candidate.content.parts = [Mock(text=response.text)]
    candidate.finish_reason = 1  # STOP (successful completion)
    response.candidates = [candidate]

    return response


@pytest.fixture
def mock_gemini_blocked_response():
    """Mock blocked Gemini API response (empty candidates)."""
    response = Mock()
    response.text = ""
    response.candidates = []  # Empty = blocked
    return response


@pytest.fixture
def mock_genai_client():
    """Mock Google Generative AI client with model and config."""
    client = MagicMock()
    model = MagicMock()
    client.GenerativeModel.return_value = model
    client.types.GenerationConfig = MagicMock()
    return client, model


# =============================================================================
# MOCK EMAIL/SMTP FIXTURES
# =============================================================================
# Mocked SMTP and email configurations for testing


@pytest.fixture
def sample_email_config():
    """Email configuration for testing."""
    return {
        "email_enabled": True,
        "email_user": "test@gmail.com",
        "email_password": "test_password",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
    }


@pytest.fixture
def disabled_email_config():
    """Email configuration with email disabled."""
    return {
        "email_enabled": False,
        "email_user": "test@gmail.com",
        "email_password": "test_password",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
    }


@pytest.fixture
def no_credentials_email_config():
    """Email configuration with missing credentials."""
    return {
        "email_enabled": True,
        "email_user": "",
        "email_password": "",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
    }


# =============================================================================
# AGENT INSTANCE FIXTURES
# =============================================================================
# Pre-configured agent instances for testing


@pytest.fixture
def collector(sample_rss_feeds, sample_config):
    """Create a NewsCollectorAgent instance with test config."""
    return NewsCollectorAgent(sample_rss_feeds, sample_config)


@pytest.fixture
def summarizer(sample_config):
    """Create a NewsSummarizerAgent instance with test config."""
    return NewsSummarizerAgent(sample_config)


@pytest.fixture
def email_agent(sample_email_config):
    """Create an EmailAgent instance with test config (email enabled)."""
    return EmailAgent(sample_email_config)


@pytest.fixture
def email_agent_disabled(disabled_email_config):
    """Create an EmailAgent instance with email disabled."""
    return EmailAgent(disabled_email_config)


@pytest.fixture
def email_agent_no_credentials(no_credentials_email_config):
    """Create an EmailAgent instance with missing credentials."""
    return EmailAgent(no_credentials_email_config)


@pytest.fixture
def email_agent_with_mock_smtp(sample_email_config):
    """Create an EmailAgent instance configured for mocked SMTP testing."""
    return EmailAgent(sample_email_config)


@pytest.fixture
def orchestrator(sample_config, sample_rss_feeds):
    """Create a TechNewsOrchestrator instance with test config."""
    return TechNewsOrchestrator(sample_config, sample_rss_feeds, [])
