#!/usr/bin/env python3
"""
KeepMePosted - AI-Powered Tech Newsletter with AutoGen Agents
Two-agent system using Google AI Studio (Gemini): Collector and Summarizer with dialog capabilities
"""

import asyncio
import feedparser
import logging
import textwrap
import warnings
from datetime import datetime, timedelta, timezone
from typing import List, Dict
from config import CONFIG, RSS_FEEDS

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_google_ai_client():
    """Initialize Google Gemini client."""
    try:
        import google.generativeai as genai
        if not CONFIG["google_api_key"]:
            raise ValueError("GOOGLE_API_KEY not found. Set it in .env file.")
        genai.configure(api_key=CONFIG["google_api_key"])
        return genai
    except ImportError:
        raise ImportError("Install: pip install google-generativeai")

class NewsCollectorAgent:
    """Agent responsible for collecting news from RSS feeds."""
    
    def __init__(self, rss_feeds: Dict[str, str], config: Dict):
        self.rss_feeds = rss_feeds
        self.config = config
        self.collected_articles = []
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def collect_news(self) -> List[Dict]:
        """Collect news articles from RSS feeds."""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=self.config["hours_back"])
        articles = []
        days = self.config["hours_back"] // 24
        
        print(f"\n🔍 Collecting articles from the last {days} days...")
        
        for idx, (source, url) in enumerate(self.rss_feeds.items(), 1):
            try:
                print(f"   [{idx}/{len(self.rss_feeds)}] Fetching from {source}...", end=" ", flush=True)
                feed = feedparser.parse(url)
                print(f"✓ ({len(feed.entries)} entries)")
                
                for entry in feed.entries:
                    try:
                        published = (datetime(*entry.published_parsed[:6], tzinfo=timezone.utc) 
                                   if hasattr(entry, "published_parsed") and entry.published_parsed 
                                   else datetime.now(timezone.utc))
                        
                        if published > cutoff:
                            articles.append({
                                "source": source,
                                "title": entry.title,
                                "link": entry.link,
                                "published": published,
                                "summary": getattr(entry, "summary", ""),
                            })
                    except Exception as e:
                        self.logger.warning(f"Error parsing entry from {source}: {e}")
            except Exception as e:
                print(f"✗ Error")
                self.logger.error(f"Error fetching from {source}: {e}")
        
        self.collected_articles = sorted(articles, key=lambda x: x['published'], reverse=True)[:self.config["max_articles"]]
        print(f"✅ Successfully collected {len(self.collected_articles)} articles\n")
        return self.collected_articles
    
    def _group_by_source(self) -> Dict[str, List[Dict]]:
        """Group articles by source."""
        by_source = {}
        for article in self.collected_articles:
            by_source.setdefault(article['source'], []).append(article)
        return by_source
    
    async def report_to_summarizer(self) -> str:
        """Report collected articles to the summarizer agent."""
        if not self.collected_articles:
            return "No articles collected yet."
        
        days = self.config['hours_back'] // 24
        report = f"I've collected {len(self.collected_articles)} tech articles from the last {days} days. Here's what I found:\n\n"
        
        for source, source_articles in self._group_by_source().items():
            report += f"**{source}** ({len(source_articles)} articles):\n"
            for article in source_articles[:3]:
                report += f"- {article['title']}\n"
            if len(source_articles) > 3:
                report += f"  ... and {len(source_articles) - 3} more articles\n"
            report += "\n"
        
        return report

class NewsSummarizerAgent:
    """Agent responsible for summarizing collected news using Google Gemini."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.genai = None
    
    def _get_ai_client(self):
        """Get or initialize Google Gemini client."""
        if self.genai is None:
            self.genai = get_google_ai_client()
        return self.genai
    
    def _build_prompt(self, articles: List[Dict], days: int) -> str:
        """Build the AI prompt for summarization."""
        articles_text = "\n".join([
            f"- {a['source']}: {a['title']}" 
            for a in articles[:self.config["max_ai"]]
        ])
        
        return textwrap.dedent(f"""I am a software engineer at NVIDIA, interested in the world of technology and networking details, AI, etc. 
                                    I would be happy to receive an email update once a week on the updates at the leading technology companies - 
                                    everything you need to know to stay up to date with what is happening in the world of technology. 
                                    Be as concise as possible, but also include the details that are important to me.
                                    I am interested in the following companies: NVIDIA, Intel, AMD, Qualcomm, Broadcom, and OpenAI.
                                    Create a comprehensive tech news summary from the last {days} days, with special focus on these priority companies: NVIDIA, Intel, AMD, Qualcomm, Broadcom, and OpenAI.

                                    Structure the response as follows:

                                    **🚀 NEW TECHNOLOGIES & PRODUCTS:**
                                    - Breakthrough technologies and innovative products
                                    - AI/ML developments and applications
                                    - Semiconductor advances and new architectures
                                    - Networking and infrastructure innovations
                                    - [Include specific product launches, technical specifications, and competitive advantages]

                                    **📈 BUSINESS & CORPORATE NEWS:**
                                    - CEO changes and executive movements
                                    - Major partnerships and acquisitions
                                    - Legal battles and patent disputes
                                    - Regulatory developments and policy changes
                                    - [Include specific names, dates, and business implications]

                                    **💰 CAPITAL MARKETS & STOCKS:**
                                    - Stock price movements and market analysis
                                    - Earnings reports and financial performance
                                    - Investment announcements and funding rounds
                                    - Market cap changes and valuation updates
                                    - [Include specific percentages, reasons for movements, and market context]

                                    **🎯 PRIORITY COMPANY UPDATES:**
                                    - **NVIDIA**: [GPU innovations, AI datacenter news, automotive, gaming, professional visualization]
                                    - **Intel**: [Processor launches, foundry business, AI chips, competition analysis]
                                    - **AMD**: [CPU/GPU competition, data center wins, market share changes]
                                    - **Qualcomm**: [Mobile chips, automotive partnerships, 5G developments]
                                    - **Broadcom**: [Networking infrastructure, AI hardware, acquisition activity]
                                    - **OpenAI**: [Model releases, partnerships, business model changes, competition]

                                    **🔍 COMPETITIVE INTELLIGENCE:**
                                    - **NVIDIA Product Portfolio & Competitors:**
                                    - Gaming GPUs: vs AMD Radeon, Intel Arc
                                    - Data Center GPUs: vs AMD MI series, Intel Gaudi
                                    - AI/ML Platforms: vs Google TPU, AWS Trainium
                                    - Automotive: vs Mobileye, Qualcomm Snapdragon
                                    - Professional Visualization: vs AMD Radeon Pro
                                    - **Market Leadership Analysis**: Who leads each segment and why
                                    - **Technology Roadmaps**: Upcoming product launches and competitive positioning

                                    **🌍 INDUSTRY TRENDS & ANALYSIS:**
                                    - AI/ML Developments: [Model advances, training costs, inference optimization]
                                    - Semiconductor Industry: [Supply chain, manufacturing advances, geopolitical factors]
                                    - Data Center Evolution: [Cloud computing, edge computing, sustainability]
                                    - Automotive Technology: [Autonomous driving, electric vehicles, connectivity]

                                    **🌐 GEOPOLITICAL & REGULATORY:**
                                    - US-China Tech Relations: [Export controls, investment restrictions]
                                    - Government AI Policies: [Regulation, safety standards, national security]
                                    - Trade and Supply Chain: [Semiconductor manufacturing, critical materials]

                                    **📊 WEEKLY INTELLIGENCE BRIEF:**
                                    - Key metrics and performance indicators
                                    - Competitive positioning changes
                                    - Strategic partnership announcements
                                    - Technology adoption trends
                                    - Market sentiment and analyst opinions

                                    News articles:
                                    {articles_text}

                                    Structured Summary:""")
    
    async def analyze_articles(self, articles: List[Dict]) -> str:
        """Analyze and summarize collected articles using Google Gemini."""
        if not articles:
            return "No articles available for analysis."
        
        try:
            genai = self._get_ai_client()
            model = genai.GenerativeModel(self.config["model"])
            days = self.config["hours_back"] // 24
            
            print(f"🤖 Generating AI summary with Google Gemini (this may take 30-60 seconds)...")
            
            safety_settings = [
                {"category": cat, "threshold": "BLOCK_NONE"}
                for cat in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
                           "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]
            ]
            
            response = model.generate_content(
                self._build_prompt(articles, days),
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.config["ai_tokens"],
                    temperature=self.config["ai_temp"]
                ),
                safety_settings=safety_settings
            )
            
            print(f"✅ AI summary generated successfully!\n")
            
            if not response.candidates or not response.candidates[0].content.parts:
                reason = response.candidates[0].finish_reason if response.candidates else 'Unknown'
                return f"⚠️ AI response was blocked. Reason: {reason}\nPlease try again or adjust the prompt."
            
            return response.text.strip()
            
        except Exception as e:
            self.logger.error(f"Error creating AI summary: {e}")
            return f"Error creating AI summary: {e}"

class TechNewsOrchestrator:
    """Orchestrates the collector and summarizer agents."""
    
    def __init__(self, config: Dict, rss_feeds: Dict[str, str]):
        self.config = config
        self.collector = NewsCollectorAgent(rss_feeds, config)
        self.summarizer = NewsSummarizerAgent(config)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def initialize_agents(self):
        """Validate configuration."""
        if not self.config["google_api_key"]:
            raise ValueError("GOOGLE_API_KEY not found. Set it in .env file.")
        self.logger.info("Agents initialized successfully")
    
    async def run_dialog_workflow(self):
        """Run the dialog workflow between collector and summarizer."""
        # Collect news
        articles = await self.collector.collect_news()
        
        # Collector reports
        report = await self.collector.report_to_summarizer()
        print("\n" + "="*80)
        print("📊 COLLECTOR REPORT:")
        print("="*80)
        print(report)
        
        # Summarizer analyzes
        analysis = await self.summarizer.analyze_articles(articles)
        print("\n" + "="*80)
        print("🤖 SUMMARIZER ANALYSIS (Powered by Google Gemini):")
        print("="*80)
        print(analysis)
        
        # Agent dialog
        await self._simulate_dialog(articles)
        
        return analysis
    
    async def _simulate_dialog(self, articles: List[Dict]):
        """Simulate a dialog between the two agents."""
        print("\n" + "="*80)
        print("💬 AGENT DIALOG:")
        print("="*80)
        
        by_source = self.collector._group_by_source()
        priority_companies = ["NVIDIA", "Intel", "AMD", "Qualcomm", "Broadcom", "OpenAI"]
        priority_counts = sorted(
            [(co, len(by_source.get(co, []))) for co in priority_companies if co in by_source],
            key=lambda x: x[1], reverse=True
        )
        
        if priority_counts:
            top_companies = ", ".join([f"{co} ({cnt})" for co, cnt in priority_counts[:3]])
            print(f"🗂️  Collector: I've collected {len(articles)} articles. Top companies: {top_companies}")
            print(f"🤖 Summarizer: Thank you! I see {priority_counts[0][0]} has the most coverage. "
                  f"I'll focus on analyzing their latest developments along with competitive intelligence.")
        
        print("\n✅ Dialog completed successfully!")

async def main():
    """Main function."""
    print("\n" + "="*60)
    print("🚀 KeepMePosted - AI-Powered Tech Newsletter")
    print("   Powered by Google AI Studio (Gemini)")
    print("="*60)
    
    try:
        print("\n⚙️  Initializing agents...")
        orchestrator = TechNewsOrchestrator(CONFIG, RSS_FEEDS)
        await orchestrator.initialize_agents()
        print("✅ Agents initialized\n")
        
        await orchestrator.run_dialog_workflow()
        
        print("\n" + "="*60)
        print("✅ Newsletter generation completed!")
        print("="*60 + "\n")
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())