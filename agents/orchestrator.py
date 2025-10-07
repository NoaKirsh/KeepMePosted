"""
Tech News Orchestrator
Coordinates the interaction between collector and summarizer agents,
including agent dialog and workflow management.
"""

import logging
from typing import Dict, List
from .collector import NewsCollectorAgent
from .summarizer import NewsSummarizerAgent


class TechNewsOrchestrator:
    """Orchestrates the collector and summarizer agents with dialog capabilities."""
    
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
        """Simulate a dialog between the collector and summarizer agents.
        
        TODO: Implement real AI-powered dialog between agents for more dynamic interaction.
        """
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
