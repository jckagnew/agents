#!/usr/bin/env python3
"""
Job Search Assistant - AI-Powered Job Search for Jack Agnew
Finds remote enterprise sales positions in AI/technology companies
"""

import asyncio
import sys
from dotenv import load_dotenv
from src.job_search_manager import JobSearchManager

# Load environment variables
load_dotenv()

async def main():
    """Main application entry point"""
    print("🚀 Job Search Assistant - AI/Technology Enterprise Sales")
    print("=" * 60)
    print("Finding remote enterprise sales positions for Jack Agnew...")
    print("Target: AI/Technology companies with remote work options")
    print("=" * 60)
    
    # Initialize job search manager
    job_search = JobSearchManager()
    
    # Run the job search process
    async for result in job_search.run_job_search():
        print(result)
        print("-" * 40)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Job search interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
