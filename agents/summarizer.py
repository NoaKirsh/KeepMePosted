"""
News Summarizer Agent
Responsible for analyzing and summarizing collected news using Google Gemini.
"""

import logging
import textwrap
from typing import List, Dict
from utils.ai_client import get_google_ai_client


class NewsSummarizerAgent:
    """Agent responsible for summarizing collected news using Google Gemini."""

    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.genai = None

    def _get_ai_client(self):
        """Get or initialize Google Gemini client (lazy loading)."""
        if self.genai is None:
            self.genai = get_google_ai_client()
        return self.genai

    def _build_prompt(self, articles: List[Dict], days: int) -> str:
        """Build the AI prompt for summarization."""
        articles_text = "\n".join(
            [f"- {a['source']}: {a['title']}" for a in articles[: self.config["max_ai"]]]
        )

        return textwrap.dedent(
            f"""I am a software engineer at NVIDIA, interested in the world of technology and networking details, AI, etc.
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
                                    - Legal proceedings and intellectual property matters
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

                                    **🔍 MARKET ANALYSIS:**
                                    - **NVIDIA Product Portfolio & Market Position:**
                                    - Gaming GPUs: compared to AMD Radeon, Intel Arc
                                    - Data Center GPUs: compared to AMD MI series, Intel Gaudi
                                    - AI/ML Platforms: compared to Google TPU, AWS Trainium
                                    - Automotive: compared to Mobileye, Qualcomm Snapdragon
                                    - Professional Visualization: compared to AMD Radeon Pro
                                    - **Market Leadership Overview**: Industry positioning by segment
                                    - **Technology Roadmaps**: Upcoming product launches and market trends

                                    **🌍 INDUSTRY TRENDS & ANALYSIS:**
                                    - AI/ML Developments: [Model advances, training costs, inference optimization]
                                    - Semiconductor Industry: [Supply chain, manufacturing advances, geopolitical factors]
                                    - Data Center Evolution: [Cloud computing, edge computing, sustainability]
                                    - Automotive Technology: [Autonomous driving, electric vehicles, connectivity]

                                    **🌐 REGULATORY & POLICY:**
                                    - International Trade: [Export controls, investment policies]
                                    - Government AI Policies: [Regulation, safety standards]
                                    - Supply Chain: [Semiconductor manufacturing, materials sourcing]

                                    **📊 WEEKLY INTELLIGENCE BRIEF:**
                                    - Key metrics and performance indicators
                                    - Competitive positioning changes
                                    - Strategic partnership announcements
                                    - Technology adoption trends
                                    - Market sentiment and analyst opinions

                                    News articles:
                                    {articles_text}

                                    Structured Summary:"""
        )

    async def analyze_articles(self, articles: List[Dict]) -> str:
        """Analyze and summarize collected articles using Google Gemini."""
        if not articles:
            return "No articles available for analysis."

        try:
            genai = self._get_ai_client()
            model = genai.GenerativeModel(self.config["model"])
            days = self.config["hours_back"] // 24

            print("🤖 Generating AI summary with Google Gemini (this may take 30-60 seconds)...")

            safety_settings = [
                {"category": cat, "threshold": "BLOCK_NONE"}
                for cat in [
                    "HARM_CATEGORY_HARASSMENT",
                    "HARM_CATEGORY_HATE_SPEECH",
                    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "HARM_CATEGORY_DANGEROUS_CONTENT",
                ]
            ]

            response = model.generate_content(
                self._build_prompt(articles, days),
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.config["ai_tokens"], temperature=self.config["ai_temp"]
                ),
                safety_settings=safety_settings,
            )

            print("✅ AI summary generated successfully!\n")

            # Check if response was blocked
            if not response.candidates or not response.candidates[0].content.parts:
                reason = response.candidates[0].finish_reason if response.candidates else "Unknown"

                # Map finish reasons to user-friendly messages
                reason_messages = {
                    1: "STOP - Normal completion (but empty response)",
                    2: "SAFETY - Content filtered by safety settings. Try softening the prompt language.",
                    3: "RECITATION - Content blocked due to recitation. Try rephrasing the prompt.",
                    4: "OTHER - Unknown blocking reason",
                    5: "MAX_TOKENS - Response too long. Increase ai_tokens in config.py",
                }

                reason_text = reason_messages.get(reason, f"Unknown reason code: {reason}")
                return (
                    f"⚠️ AI response was blocked.\n"
                    f"Reason: {reason_text}\n\n"
                    f"Possible causes:\n"
                    f"- API quota exceeded (check: https://aistudio.google.com/app/apikey)\n"
                    f"- Content safety filters triggered\n"
                    f"- Rate limit reached (wait a few minutes)\n\n"
                    f"Try: Reduce max_ai in config.py or wait and retry."
                )

            return response.text.strip()

        except Exception as e:
            error_msg = str(e).lower()

            # Check for specific error types
            if "quota" in error_msg or "limit" in error_msg:
                self.logger.error(f"API quota/rate limit error: {e}")
                return (
                    f"❌ API Quota or Rate Limit Exceeded!\n\n"
                    f"Error: {e}\n\n"
                    f"Solutions:\n"
                    f"1. Check your quota: https://aistudio.google.com/app/apikey\n"
                    f"2. Wait a few minutes and try again\n"
                    f"3. Reduce max_ai in config.py (currently: {self.config['max_ai']})\n"
                    f"4. Get a new API key if quota is exhausted"
                )
            elif "api" in error_msg and "key" in error_msg:
                self.logger.error(f"API key error: {e}")
                return (
                    f"❌ API Key Error!\n\n"
                    f"Error: {e}\n\n"
                    f"Check that GOOGLE_API_KEY in .env is valid."
                )
            else:
                self.logger.error(f"Error creating AI summary: {e}")
                return f"❌ Error creating AI summary: {e}"
