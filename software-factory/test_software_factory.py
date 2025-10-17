#!/usr/bin/env python3
"""
Test Script for Software Factory
This script demonstrates the Software Factory functionality without requiring a full setup.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# Import our agents
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.orchestrator import SoftwareFactoryOrchestrator
from agents.idea_validation import IdeaValidationAgent
from agents.rapid_prototyping import RapidPrototypingAgent
from agents.collaboration import CollaborationAgent
from agents.monetization import MonetizationAgent
from agents.analytics import AnalyticsAgent


async def test_idea_validation():
    """Test the idea validation agent"""
    print("🔍 Testing Idea Validation Agent...")
    
    agent = IdeaValidationAgent()
    
    # Test idea
    idea = """
    I want to create an AI-powered personal finance assistant that helps users 
    track expenses, create budgets, and get personalized financial advice. 
    The app should integrate with bank accounts, provide real-time spending 
    insights, and offer investment recommendations based on user goals.
    """
    
    print(f"📝 Idea: {idea.strip()[:100]}...")
    
    try:
        result = await agent.analyze_comprehensive(idea)
        
        print(f"✅ Validation Complete!")
        print(f"   Viability Score: {result['overall_viability_score']}/10")
        print(f"   Is Viable: {result['is_viable']}")
        print(f"   Market Size: {result['market_analysis']['market_size']}")
        print(f"   Competition Level: {result['market_analysis']['competition_level']}")
        print(f"   Technical Feasibility: {result['technical_analysis']['feasibility_score']}/10")
        
        return result
    except Exception as e:
        print(f"❌ Error in idea validation: {e}")
        return None


async def test_rapid_prototyping(validation_result):
    """Test the rapid prototyping agent"""
    print("\n🛠️ Testing Rapid Prototyping Agent...")
    
    agent = RapidPrototypingAgent()
    
    idea = """
    AI-powered personal finance assistant with bank integration, 
    real-time insights, and investment recommendations.
    """
    
    try:
        prototype = await agent.create_prototype(idea, validation_result or {})
        
        print(f"✅ Prototype Created!")
        print(f"   Project Name: {prototype['project_name']}")
        print(f"   Template Used: {prototype['template_used']}")
        print(f"   Tech Stack: {', '.join(prototype['template_config']['tech_stack'])}")
        print(f"   Development Time: {prototype['estimated_development_time']}")
        print(f"   Development Cost: {prototype['estimated_cost']['development']}")
        
        return prototype
    except Exception as e:
        print(f"❌ Error in rapid prototyping: {e}")
        return None


async def test_collaboration(project_id):
    """Test the collaboration agent"""
    print("\n👥 Testing Collaboration Agent...")
    
    agent = CollaborationAgent()
    
    # Mock project
    class MockProject:
        def __init__(self):
            self.id = project_id
            self.name = "AI Finance Assistant"
            self.owner_id = "user_123"
            self.team_members = ["dev_456", "designer_789"]
    
    project = MockProject()
    
    try:
        # Test feedback collection
        feedback_result = await agent.collect_and_process_feedback(
            project_id,
            {
                "user_id": "customer_123",
                "category": "feature_request",
                "description": "Please add dark mode support to the app",
                "priority": "medium"
            }
        )
        
        print(f"✅ Collaboration Test Complete!")
        print(f"   Feedback ID: {feedback_result['feedback_id']}")
        print(f"   Status: {feedback_result['status']}")
        print(f"   Priority: {feedback_result['priority']}")
        print(f"   Assigned To: {feedback_result['assigned_to']}")
        
        return feedback_result
    except Exception as e:
        print(f"❌ Error in collaboration: {e}")
        return None


async def test_monetization(project_id):
    """Test the monetization agent"""
    print("\n💰 Testing Monetization Agent...")
    
    agent = MonetizationAgent()
    
    # Mock project
    class MockProject:
        def __init__(self):
            self.id = project_id
            self.name = "AI Finance Assistant"
    
    project = MockProject()
    
    # Mock validation result
    validation_result = {
        "customer_analysis": {
            "target_segments": [{"name": "Young Professionals", "size": "15M people"}]
        }
    }
    
    try:
        monetization_plan = await agent.create_monetization_plan(project, validation_result)
        
        print(f"✅ Monetization Plan Created!")
        print(f"   Pricing Tiers: {len(monetization_plan['pricing_tiers'])}")
        print(f"   Marketing Budget: ${monetization_plan['campaign_plan']['total_budget']:,}")
        print(f"   Projected ARR (Month 12): ${monetization_plan['revenue_projections'][11]['arr']:,.0f}")
        
        # Show pricing tiers
        print("\n   📊 Pricing Tiers:")
        for tier in monetization_plan['pricing_tiers']:
            print(f"      - {tier['name']}: ${tier['price']}/month")
        
        return monetization_plan
    except Exception as e:
        print(f"❌ Error in monetization: {e}")
        return None


async def test_analytics(project_id):
    """Test the analytics agent"""
    print("\n📊 Testing Analytics Agent...")
    
    agent = AnalyticsAgent()
    
    # Mock project
    class MockProject:
        def __init__(self):
            self.id = project_id
            self.name = "AI Finance Assistant"
    
    project = MockProject()
    
    try:
        # Initialize metrics
        initial_metrics = await agent.initialize_project_metrics(project)
        print(f"✅ Metrics Initialized: {initial_metrics['metrics_initialized']}")
        
        # Update metrics
        current_metrics = await agent.update_project_metrics(project)
        print(f"✅ Metrics Updated!")
        print(f"   Current MRR: ${current_metrics['revenue']['mrr']['current']:,.0f}")
        print(f"   Total Customers: {current_metrics['revenue']['customer_metrics']['total_customers']}")
        print(f"   Overall Health Score: {current_metrics['overall_health_score']}/10")
        
        return current_metrics
    except Exception as e:
        print(f"❌ Error in analytics: {e}")
        return None


async def test_full_workflow():
    """Test the complete software factory workflow"""
    print("🏭 Testing Complete Software Factory Workflow")
    print("=" * 50)
    
    # Generate a project ID
    project_id = f"test_proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Step 1: Idea Validation
    validation_result = await test_idea_validation()
    
    if not validation_result or not validation_result.get('is_viable'):
        print("\n❌ Idea validation failed - stopping workflow")
        return
    
    # Step 2: Rapid Prototyping
    prototype = await test_rapid_prototyping(validation_result)
    
    if not prototype:
        print("\n❌ Prototyping failed - stopping workflow")
        return
    
    # Step 3: Collaboration
    collaboration_result = await test_collaboration(project_id)
    
    # Step 4: Monetization
    monetization_plan = await test_monetization(project_id)
    
    # Step 5: Analytics
    analytics_result = await test_analytics(project_id)
    
    # Summary
    print("\n🎉 Software Factory Workflow Complete!")
    print("=" * 50)
    print(f"Project ID: {project_id}")
    print(f"Idea Viable: {validation_result['is_viable'] if validation_result else 'Unknown'}")
    print(f"Prototype Created: {prototype['project_name'] if prototype else 'Failed'}")
    print(f"Collaboration Ready: {collaboration_result['status'] if collaboration_result else 'Failed'}")
    print(f"Monetization Planned: {len(monetization_plan['pricing_tiers']) if monetization_plan else 0} pricing tiers")
    print(f"Analytics Active: {analytics_result['overall_health_score'] if analytics_result else 'Unknown'}/10 health score")


async def main():
    """Main test function"""
    print("🚀 Starting Software Factory Test")
    print("=" * 40)
    
    try:
        await test_full_workflow()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
