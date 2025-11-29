# 📰 KeepMePosted

> An AI-powered tech newsletter using Google Gemini with intelligent agent dialog capabilities.
> Two specialized agents work together to collect and summarize tech news for software engineers.
// An AI-powered tech newsletter using Google Gemini with intelligent agent dialog capabilities.
// Two specialized agents work together to collect and summarize tech news for software engineers.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Powered by Google Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4?logo=google)](https://ai.google.dev/)

## ✨ Features

- **Three-Agent System**: Collector, Summarizer, and Email agents with dialog capabilities
- **Priority Tech Companies**: NVIDIA, Intel, AMD, Qualcomm, Broadcom, OpenAI
- **Quality News Sources**: TechCrunch, Ars Technica, The Verge, WIRED, VentureBeat, CNET
- **AI-Powered Summaries**: Using Google Gemini (FREE tier available)
- **Email Delivery**: Beautiful HTML newsletters sent directly to your inbox
- **Agent Dialog**: Interactive conversation between agents
- **Configurable Time Range**: Filter articles from the last 5 days (configurable)
- **Async Architecture**: Modern async/await patterns for better performance

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.8 or higher
- Google AI Studio API key (free!)
- Internet connection for RSS feeds

### 💻 Installation

1. **📥 Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/KeepMePosted.git
   cd KeepMePosted
   ```

2. **🐍 Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **⚙️ Activate the virtual environment:**
   ```bash
   # 🪟 Windows
   .venv\Scripts\activate
   
   # 🍎 Mac/Linux
   source .venv/bin/activate
   ```

4. **📦 Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **🔑 Set up your configuration:**
   
   **Google AI Studio API key (FREE):**
   - Go to https://aistudio.google.com/
   - Sign in with your Google account
   - Click 'Get API key' in the left sidebar
   - Create a new API key
   
   **Create a `.env` file in the project root:**
   ```
   # Google AI Studio API Key (FREE!)
   GOOGLE_API_KEY=your_google_api_key_here
   
   # Time range for news fetching (in hours, default: 120 = 5 days)
   HOURS_BACK=120
   
   # Email Configuration (Optional - leave disabled to skip email)
   EMAIL_ENABLED=false
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASSWORD=your_gmail_app_password
   MAILING_LIST=recipient@example.com
   ```
   
   **To Enable Email Delivery (Optional):**
   
   Email requires authentication - you need to send FROM a real email account. Here's how:
   
   1. **Get Gmail App Password** (recommended - it's free):
      - Go to https://myaccount.google.com/apppasswords
      - Enable 2-factor authentication if not already enabled
      - Generate an app password for "Mail"
      - Use this password in `EMAIL_PASSWORD` (not your regular Gmail password)
   
   2. **Update your `.env`:**
      ```
      EMAIL_ENABLED=true
      EMAIL_USER=your_email@gmail.com
      EMAIL_PASSWORD=your_16_char_app_password
      MAILING_LIST=recipient1@example.com,recipient2@example.com
      ```

6. **▶️ Run the application from the project's root directory:**
   ```bash
   python main.py
   ```

## 🔐 Security Notes

- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore`
- API keys are loaded from environment variables
- The script includes proper error handling for API issues

## 💰 Cost Optimization

- **FREE AI summaries** using Google AI Studio's free tier
- **Configurable limits** to control API usage
- **Efficient prompts** to minimize token usage
- No credit card required for Google AI Studio free tier

## Agent Architecture

KeepMePosted uses a three-agent system where agents communicate and collaborate:

### 📰 NewsCollectorAgent
- **Responsibility**: Fetches and processes RSS feeds
- **Features**: 
  - Parses multiple RSS sources
  - Filters articles by date and relevance
  - Provides structured article data
  - Groups articles by source
  - Reports findings to Summarizer

### 🤖 NewsSummarizerAgent
- **Responsibility**: Analyzes and summarizes collected news
- **Features**:
  - Uses Google Gemini for intelligent analysis
  - Focuses on priority tech companies
  - Creates structured summaries by category
  - Provides competitive intelligence
  - Tailored insights for software engineers

### 📧 EmailAgent
- **Responsibility**: Delivers newsletters via email
- **Features**:
  - Beautiful HTML email formatting
  - SMTP configuration support
  - Multiple recipient support
  - Error handling and delivery status
  - Professional newsletter templates

### TechNewsOrchestrator
- **Responsibility**: Coordinates agent interactions
- **Features**:
  - Manages async workflow between agents
  - Facilitates agent dialog
  - Handles error propagation and logging
  - Coordinates email delivery
  - Provides comprehensive reporting

## File Structure

```
KeepMePosted/
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD pipeline
├── agents/                  # Agent modules
│   ├── __init__.py          # Agent exports
│   ├── collector.py         # NewsCollectorAgent
│   ├── summarizer.py        # NewsSummarizerAgent
│   ├── email_sender.py      # EmailAgent
│   └── orchestrator.py      # TechNewsOrchestrator
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── ai_client.py         # Google AI client setup
│   └── email_template.py    # HTML email template
├── tests/                   # Comprehensive test suite
│   ├── conftest.py          # Shared test fixtures
│   ├── test_collector_unit.py
│   ├── test_collector_component.py
│   ├── test_summarizer_unit.py
│   ├── test_summarizer_component.py
│   ├── test_email_unit.py
│   ├── test_email_component.py
│   ├── test_orchestrator_component.py
│   ├── test_utils.py
│   └── README.md            # Testing documentation
├── scripts/                 # Development scripts
│   ├── run_tests.py         # Local CI/CD checks
│   └── run_tests.bat        # Windows shortcut
├── main.py                  # Main entry point
├── config.py                # Configuration management
├── pyproject.toml           # Tool configuration (pytest, black, ruff)
├── requirements.txt         # Python dependencies
├── CICD_SETUP.md            # CI/CD setup guide
├── .env                     # Your API keys (not in git)
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## What Makes KeepMePosted Special

- **Personalized for Tech Engineers**: Tailored summaries focusing on your priority companies
- **Competitive Intelligence**: Detailed analysis of NVIDIA vs competitors
- **Business & Market News**: CEO changes, partnerships, stock movements
- **Technical Deep Dives**: Product launches, specifications, roadmaps
- **Weekly Intelligence Brief**: Key metrics and strategic insights
- **Structured Output**: Organized by categories for easy scanning

## Troubleshooting

### Google AI API Issues
- Make sure you have a valid Google AI Studio API key
- Check that your API key is set in the `.env` file
- Verify you're using the correct model name in `config.py`
- The script will show error messages if AI summary fails

### No Articles Found
- Check your internet connection
- Verify RSS feed URLs are accessible
- Try increasing `HOURS_BACK` in `.env` to fetch older articles

### Python Issues
- Make sure Python 3.8+ is installed
- Activate your virtual environment before running
- Install all dependencies: `pip install -r requirements.txt`

## Testing

The project includes comprehensive unit and component tests covering all agents and functionality.

### Quick Start
Run these commands from the **project root directory** (the folder containing `main.py`):

```bash
# Run all tests
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=. --cov-report=term-missing -v

# Specific categories
python -m pytest tests/test_*_unit.py -v
python -m pytest tests/test_*_component.py -v
```

See [`tests/README.md`](tests/README.md) for details.

## CI/CD Pipeline

GitHub Actions automatically runs all tests on every push:

- **Automated Testing**: Tests on Python 3.10, 3.11, and 3.12 simultaneously
- **Code Quality**: Ruff linter and Black formatter checks

**Local testing:** Run `python scripts/run_tests.py` before pushing.

See [`CICD_SETUP.md`](CICD_SETUP.md) for setup instructions.

## Contributing

Contributions are welcome! Please check out our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- AI-assisted development practices
- Code style and standards
- Testing requirements
- Pull request process

## License

MIT License - feel free to use and modify for your needs!