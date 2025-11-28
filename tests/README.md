# KeepMePosted Tests

## 🧪 Test Suite Overview

### Current Test Coverage: 94% ✅

## Test Files

### Unit Tests
- `test_collector_unit.py` - Pure functions, article grouping
- `test_summarizer_unit.py` - Prompt building, article limiting
- `test_email_unit.py` - Email validation, recipient handling, SMTP config
- `test_utils.py` - AI client initialization, error handling

### Component Tests
- `test_collector_component.py` - RSS feeds (mocked), date filtering, errors
- `test_summarizer_component.py` - Gemini API (mocked), safety filters, errors
- `test_email_component.py` - SMTP (mocked), HTML generation, edge cases
- `test_orchestrator_component.py` - Agent coordination, workflow, dialog

### Unit Tests (Stage 1 - Completed)
- **`test_collector_unit.py`**
  - Pure function tests (_group_by_source, report_to_summarizer)
  - Article grouping and reporting logic
  
- **`test_summarizer_unit.py`** - Unit tests for NewsSummarizerAgent
  - Prompt building logic tests
  - Article limiting behavior
  
- **`test_email_unit.py`**
  - Email validation (disabled, missing credentials, empty recipients)
  - Recipient cleaning and filtering
  - Subject generation with dates
  - SMTP configuration (Gmail default, custom settings)
  
- **`test_utils.py`** - Unit tests for utility functions
  - AI client initialization
  - Configuration validation
  - Error handling

### Component Tests (Stage 2 - Completed)
- **`test_collector_component.py`** - Collector with mocked RSS feeds
  - Tests `collect_news()` with various scenarios
  - Date filtering, sorting, error handling
  - Feed errors, malformed entries, empty feeds
  
- **`test_summarizer_component.py`** - Summarizer with mocked Gemini API
  - Gemini API integration with mocked responses
  - API error handling (quota, rate limits, key errors)
  - Safety filters and blocked responses
  - Configuration validation and client caching
  
- **`test_email_component.py`** 
  - SMTP integration with mocked server
  - Multiple recipients handling
  - Authentication and SMTP error handling
  - HTML email generation and structure
  - Edge cases (long summaries, special characters, many articles)
  
- **`test_orchestrator_component.py`**
  - Agent initialization and configuration
  - Workflow execution and error propagation
  - Dialog simulation between agents
  - Order of operations and email integration

### Support Files
- **`conftest.py`** - Shared pytest fixtures
  - Configuration fixtures (app config, RSS feeds, email config)
  - Sample article data (single, multiple, old articles)
  - Mock RSS feed objects
  - Mock Gemini API responses
  - Mock email/SMTP configurations
  - Agent instances (collector, summarizer, email, orchestrator)

## 🚀 Running Tests

### Run All Tests
```bash
# All tests
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=. --cov-report=term-missing -v

# By category
python -m pytest tests/test_*_unit.py -v
python -m pytest tests/test_*_component.py -v

# Specific file
python -m pytest tests/test_email_component.py -v
```

### Run Specific Test
```bash
python -m pytest tests/test_collector_unit.py::TestCollectorPureFunctions::test_group_by_source_empty -v
python -m pytest tests/test_email_component.py::TestEmailAgentWithMockedSMTP::test_send_email_success -v
```

**Test Categories:**
- ✅ Unit Tests: Pure functions, validation, configuration
- ✅ Component Tests: Mocked external dependencies
- ✅ Integration Tests: Agent interactions and workflows
- ✅ Edge Cases: Error handling, special inputs, large data

## Test Breakdown

### ✅ Phase 1: Unit Tests (COMPLETED)
Pure functions, no external dependencies

### ✅ Phase 2: Component Tests (COMPLETED)
- Mocked RSS feeds and Gemini API
- Comprehensive error handling
- 38 tests, ~3s execution

### 📋 Phase 3: Integration Tests (Planned)
- Test agent orchestration end-to-end
- Test dialog simulation with real logic
- Test configuration variations
- Error recovery and resilience

### 📋 Phase 4: E2E Tests (Planned)
- Real API integration tests (manual)
- End-to-end workflow validation
- Performance benchmarks

## 🏗️ Test Structure

```
tests/
├── __init__.py
├── README.md                      # This file
├── conftest.py                    # Shared fixtures
├── test_collector_unit.py         # Collector unit tests
├── test_collector_component.py    # Collector component tests
├── test_summarizer_unit.py        # Summarizer unit tests
├── test_summarizer_component.py   # Summarizer component tests
├── test_email_unit.py             # Email unit tests
├── test_email_component.py        # Email component tests
├── test_orchestrator_component.py # Orchestrator tests
└── test_utils.py                  # Utility tests
```

## 📝 Writing Tests

### Test Naming Convention
- Test files: `test_<module>_<level>.py`
- Test classes: `Test<Feature>`
- Test methods: `test_<specific_behavior>`

### Example Test
```python
def test_group_by_source_empty(self, collector):
    """Test grouping with no articles."""
    collector.collected_articles = []
    result = collector._group_by_source()
    assert result == {}
```

## 🔍 pytest Configuration

See `pytest.ini` in the project root for configuration options.

Markers available:
- `@pytest.mark.unit` - Fast unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.slow` - Slow-running tests

