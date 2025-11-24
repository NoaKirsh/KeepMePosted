# KeepMePosted Tests

## 🧪 Test Suite Overview

This directory contains the test suite for KeepMePosted, organized by testing level.

### Current Test Coverage: 92% ✅

## 📁 Test Files

### Unit Tests (Stage 1 - Completed)
- **`test_collector_unit.py`** - Unit tests for NewsCollectorAgent
  - Pure function tests (_group_by_source, report_to_summarizer)
  - No external dependencies
  
- **`test_summarizer_unit.py`** - Unit tests for NewsSummarizerAgent
  - Prompt building logic tests
  - Article limiting behavior
  
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
  - Tests `analyze_articles()` with mocked responses
  - API error handling (quota, rate limits, key errors)
  - Safety filters, blocked responses
  - Configuration validation
  
- **`test_orchestrator_component.py`** - Orchestrator coordination
  - Agent initialization and configuration
  - Workflow execution and error propagation
  - Dialog simulation
  - Order of operations

### Support Files
- **`conftest.py`** - Shared pytest fixtures
  - Configuration fixtures
  - Sample article data
  - Mock response objects
  - Agent instances

## 🚀 Running Tests

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run With Coverage
```bash
python -m pytest tests/ --cov=. --cov-report=term-missing
```

### Run Specific Test File
```bash
python -m pytest tests/test_collector_unit.py -v
```

### Run Specific Test
```bash
python -m pytest tests/test_collector_unit.py::TestCollectorPureFunctions::test_group_by_source_empty -v
```

## 📊 Test Statistics

- ✅ **30 tests** passing (down from 52 - removed redundancies)
- ⚡ **1.86s** total test time (down from 2.96s - 37% faster!)
- 📈 **92% code coverage** (agents: 100%)
  - Collector: 100% ✅
  - Summarizer: 100% ✅
  - Orchestrator: 100% ✅
  - Utils: 100% ✅

**Optimization Results:**
- Removed 22 redundant tests (42% reduction)
- Maintained 100% coverage on all agent code
- Tests run 37% faster
- More efficient test suite with combined tests

## 🎯 Testing Phases

### ✅ Phase 1: Unit Tests (COMPLETED)
- Pure functions, no external dependencies
- 14 tests, fast execution

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
- Smoke tests for production readiness
- Performance benchmarks

## 🏗️ Test Structure

```
tests/
├── __init__.py
├── README.md (this file)
├── test_collector_unit.py    # NewsCollectorAgent unit tests
├── test_summarizer_unit.py   # NewsSummarizerAgent unit tests
└── test_utils.py             # Utility functions tests
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

