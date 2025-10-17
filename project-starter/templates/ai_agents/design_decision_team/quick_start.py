"""
Design Decision Team Quick Start
Demonstrates the team with a simple design request
"""

import asyncio
import os
from design_decision_team.design_decision_team import DesignDecisionTeam, DesignRequest, DesignRequestType

async def quick_start():
    """Quick start example"""
    
    print("🎨 Design Decision Team Quick Start")
    print("=" * 50)
    
    # Check if we have required API keys
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not found in environment")
        print("   Please set your OpenAI API key in .env file")
        return
    
    # Create a simple design request
    request = DesignRequest(
        id="quick_start_001",
        project_id="demo_project",
        request_type=DesignRequestType.SPLASH_SCREEN,
        description="Create a simple splash screen for a fitness app",
        requirements={
            "quality": "medium",
            "style": "modern",
            "colors": "blue_green"
        },
        budget_tier="free",
        timeline="standard",
        target_platform="mobile"
    )
    
    print(f"📋 Processing design request: {request.description}")
    
    try:
        # Initialize design team
        design_team = DesignDecisionTeam()
        
        # Process request
        decision = await design_team.process_design_request(request)
        
        print("\n🎉 Design Decision Complete!")
        print(f"Request ID: {decision.request_id}")
        print(f"Quality Scores: {decision.quality_scores}")
        print(f"Timeline: {decision.estimated_timeline}")
        print(f"Cost: {decision.estimated_cost}")
        
    except Exception as e:
        print(f"❌ Error processing design request: {e}")
        print("   Please check your setup and API keys")

if __name__ == "__main__":
    asyncio.run(quick_start())
