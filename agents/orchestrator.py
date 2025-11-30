"""
Tech News Orchestrator
Coordinates the interaction between collector, summarizer, and email agents,
including agent dialog and workflow management.
"""

import logging
from typing import Dict, List
from .collector import NewsCollectorAgent
from .summarizer import NewsSummarizerAgent
from .email_sender import EmailAgent

logger = logging.getLogger(__name__)


class TechNewsOrchestrator:
    """Orchestrates the collector, summarizer, and email agents with dialog capabilities."""

    def __init__(self, config: Dict, rss_feeds: Dict[str, str], mailing_list: List[str]):
        self.config = config
        self.mailing_list = mailing_list
        self.collector = NewsCollectorAgent(rss_feeds, config)
        self.summarizer = NewsSummarizerAgent(config)
        self.email_agent = EmailAgent(config)

    async def initialize_agents(self):
        """Validate configuration."""
        if not self.config["google_api_key"]:
            logger.error("GOOGLE_API_KEY not found")
            raise ValueError("GOOGLE_API_KEY not found. Set it in .env file.")
        logger.info("Agents initialized successfully")

    async def run_dialog_workflow(self):
        """Run the dialog workflow between collector, summarizer, and email agents."""
        # Collect news
        articles = await self.collector.collect_news()

        # Collector reports
        report = await self.collector.report_to_summarizer()
        print("\n" + "=" * 80)
        print("📊 COLLECTOR REPORT:")
        print("=" * 80)
        print(report)

        # Summarizer analyzes
        analysis = await self.summarizer.analyze_articles(articles)
        print("\n" + "=" * 80)
        print("🤖 SUMMARIZER ANALYSIS (Powered by Google Gemini):")
        print("=" * 80)
        print(analysis)

        # Agent dialog
        await self._simulate_dialog(articles)

        # Send email to mailing list
        if self.mailing_list:
            await self.email_agent.execute(analysis, articles, self.mailing_list)

        return analysis

    async def _simulate_dialog(self, articles: List[Dict]):
        """Simulate a dialog between the collector, summarizer, and email agents.
        TODO: Implement real AI-powered dialog between agents for more dynamic interaction.
        """
        print("\n" + "=" * 80)
        print("💬 AGENT DIALOG:")
        print("=" * 80)

        # Find top companies
        by_source = self.collector._group_by_source()
        priority = ["NVIDIA", "Intel", "AMD", "Qualcomm", "Broadcom", "OpenAI"]
        top = sorted(
            [(co, len(by_source.get(co, []))) for co in priority if co in by_source],
            key=lambda x: x[1],
            reverse=True,
        )

        if top:
            companies = ", ".join([f"{co} ({cnt})" for co, cnt in top[:3]])
            print(f"🗂️  Collector: Collected {len(articles)} articles. Top: {companies}")
            print(f"🤖 Summarizer: I'll focus on {top[0][0]} and competitive intelligence.")

            # Email agent status
            if self.config.get("email_enabled") and self.mailing_list:
                print(f"📧 Email Agent: Ready to send to {len(self.mailing_list)} recipient(s).")
            elif self.mailing_list:
                print(
                    f"📧 Email Agent: {len(self.mailing_list)} recipient(s) configured (email disabled)."
                )

        print("✅ Dialog complete!")
