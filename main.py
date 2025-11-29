#!/usr/bin/env python3
"""KeepMePosted - AI-Powered Tech Newsletter"""

import asyncio
import logging
import warnings
from config import CONFIG, RSS_FEEDS, MAILING_LIST
from agents.orchestrator import TechNewsOrchestrator

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main():
    print("\n" + "=" * 60)
    print("🚀 KeepMePosted - AI Tech Newsletter (Powered by Gemini)")
    print("=" * 60)

    try:
        print("\n⚙️  Initializing agents...")
        orchestrator = TechNewsOrchestrator(CONFIG, RSS_FEEDS, MAILING_LIST)
        await orchestrator.initialize_agents()

        await orchestrator.run_dialog_workflow()

        print("\n" + "=" * 60)
        print("✅ Newsletter generation completed!")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
