"""
Weight Tracker Design Request Example
Demonstrates Design Decision Team for morphing transformation splash screen
"""

import asyncio
from design_decision_team.design_decision_team import DesignDecisionTeam, DesignRequest, DesignRequestType

async def weight_tracker_design_example():
    """Example design request for weight tracker morphing splash screen"""
    
    # Create design request for weight tracker
    request = DesignRequest(
        id="weight_tracker_splash_001",
        project_id="weight_tracker_mobile",
        request_type=DesignRequestType.SPLASH_SCREEN,
        description="Create morphing transformation splash screen showing cartoon people transforming from overweight to fit",
        requirements={
            "quality": "high",
            "performance": "high",
            "animation_type": "morphing",
            "character_style": "cartoon",
            "transformation": "overweight_to_fit",
            "motivational": True,
            "engaging": True
        },
        budget_tier="ai_generated",
        timeline="urgent",
        target_platform="mobile",
        brand_guidelines={
            "colors": ["#667eea", "#4CAF50", "#fff"],
            "style": "modern",
            "tone": "motivational",
            "target_audience": "fitness_enthusiasts"
        },
        user_personas=[
            {
                "age": "25-45",
                "interests": "fitness",
                "tech_savvy": "high",
                "goals": "weight_tracking",
                "motivation": "transformation"
            }
        ]
    )
    
    # Process design request
    design_team = DesignDecisionTeam()
    decision = await design_team.process_design_request(request)
    
    print(f"Design Decision for Weight Tracker:")
    print(f"Project ID: {decision.request_id}")
    print(f"Recommended Morphing: {decision.recommended_morphing.technique.value}")
    print(f"Quality Scores: {decision.quality_scores}")
    print(f"Estimated Timeline: {decision.estimated_timeline}")
    print(f"Estimated Cost: {decision.estimated_cost}")
    
    return decision

if __name__ == "__main__":
    asyncio.run(weight_tracker_design_example())
