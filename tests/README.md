# KeepMePosted Tests

## 🧪 Test Suite Overview

This directory contains the test suite for KeepMePosted, organized by testing level.

### Current Test Coverage: 69%

## 📁 Test Files

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

- ✅ **14 tests** passing
- ⚡ **1.08s** total test time
- 📈 **69% code coverage**

## 🎯 Future Testing Phases

### Phase 2: Component Tests (Planned)
- Mock RSS feeds and test full article collection
- Mock Google Gemini API and test summarization
- Test error scenarios and edge cases

### Phase 3: Integration Tests (Planned)
- Test agent orchestration
- Test dialog simulation
- Test end-to-end workflow

### Phase 4: E2E Tests (Planned)
- Real API integration tests (manual)
- Smoke tests for production readiness

## 🏗️ Test Structure

```
tests/
├── __init__.py
├── README.md (this file)
├── test_collector_unit.py    # NewsCollectorAgent unit tests
├── test_summarizer_unit.py   # NewsSummarizerAgent unit tests
└── test_utils.py              # Utility functions tests
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

