"""Configuration for KeepMePosted"""

import os
from dotenv import load_dotenv

load_dotenv()

# RSS Feeds Configuration
RSS_FEEDS = {
    # Priority Companies
    "NVIDIA": "https://nvidianews.nvidia.com/rss",
    "Intel": "https://newsroom.intel.com/feed/",
    # "AMD": "https://www.amd.com/en/corporate/news/rss.xml",
    "Qualcomm": "https://www.qualcomm.com/news/rss",
    "Broadcom": "https://www.broadcom.com/news/rss",
    "OpenAI": "https://openai.com/blog/rss.xml",
    # Tech News Sources
    "TechCrunch": "https://techcrunch.com/feed/",
    "Ars Technica": "http://feeds.arstechnica.com/arstechnica/index/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "WIRED": "https://www.wired.com/feed/rss",
    "VentureBeat": "https://venturebeat.com/feed/",
    "CNET": "https://www.cnet.com/rss/news/",
}

# Main Configuration
CONFIG = {
    # Article Collection
    "max_articles": 10,
    "max_ai": 15,
    "hours_back": int(os.getenv("HOURS_BACK", "120")),
    # Google AI Configuration
    "google_api_key": os.getenv("GOOGLE_API_KEY", ""),
    "model": "models/gemini-2.5-flash",
    "ai_tokens": 2000,
    "ai_temp": 0.7,
    # Email Configuration
    "email_enabled": os.getenv("EMAIL_ENABLED", "false").lower() == "true",
    "email_user": os.getenv("EMAIL_USER", ""),
    "email_password": os.getenv("EMAIL_PASSWORD", ""),
    # SMTP Configuration (Gmail by default, can override in .env if needed)
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
}

# Mailing List (comma-separated in .env)
MAILING_LIST = [
    email.strip() for email in os.getenv("MAILING_LIST", "").split(",") if email.strip()
]
