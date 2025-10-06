#!/usr/bin/env python3
"""
Configuration management for KeepMePosted with Google AI Studio.
"""

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

# Application Configuration
CONFIG = {
    "max_articles": 10,
    "max_ai": 15,
    "hours_back": int(os.getenv('HOURS_BACK', '120')),
    "google_api_key": os.getenv('GOOGLE_API_KEY', ''),
    "model": "models/gemini-2.5-flash",  # Current stable Gemini model (use models/ prefix)
    "ai_tokens": 2000,  # Increased for longer summaries
    "ai_temp": 0.7,  # Slightly higher for more creative responses
}
