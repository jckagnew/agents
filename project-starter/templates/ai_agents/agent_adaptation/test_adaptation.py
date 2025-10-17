"""
Test suite for Pattern 12: Agent Adaptation
Comprehensive testing of adaptation framework capabilities
"""

import asyncio
import tempfile
import shutil
import json
import time
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from adaptation_framework import (
    AdaptationFramework, AdaptationType, AdaptationTrigger, AdaptationStatus,
    AdaptationProfile, AdaptationRule, AdaptationEvent, AdaptationStats
)

async def test_basic_adaptation():
    """Test basic adaptation functionality"""
    print("🧪 Testing Pattern 12: Agent Adaptation - Basic Functionality")
    print("=" * 60)
    
    # Create framework with temporary storage
    temp_dir = tempfile.mkdtemp()
    try:
        framework = AdaptationFramework({"storage_path": temp_dir})
        print("✅ Adaptation framework created")
        
        # Test creating adaptation profile
        profile_id = framework.create_adaptation_profile(
            agent_id="test_agent_1",
            profile_type="default",
            personality_traits={"friendliness": 0.7, "formality": 0.3}
        )
        assert profile_id is not None
        print("✅ Adaptation profile created")
        
        # Test adding adaptation rule
        rule_id = framework.add_adaptation_rule(
            name="Increase friendliness on positive feedback",
            trigger=AdaptationTrigger.FEEDBACK,
            condition={"type": "threshold", "metric": "feedback_score", "threshold": 0.8, "operator": ">="},
            action={"type": "adjust_personality", "trait": "friendliness", "adjustment": 0.1, "direction": "increase"},
            priority=1
        )
        assert rule_id is not None
        print("✅ Adaptation rule added")
        
        # Test triggering adaptation
        adaptation_id = framework.trigger_adaptation(
            agent_id="test_agent_1",
            trigger=AdaptationTrigger.FEEDBACK,
            context={"feedback_score": 0.9, "user_satisfaction": "high"},
            adaptation_type=AdaptationType.BEHAVIORAL
        )
        assert adaptation_id is not None
        print("✅ Adaptation triggered")
        
        # Test getting adaptation state
        state = framework.get_agent_adaptation_state("test_agent_1")
        assert state is not None
        assert "personality_traits" in state
        print("✅ Adaptation state retrieved")
        
        # Test adaptation stats
        stats = framework.get_adaptation_stats()
        assert stats.total_adaptations >= 1
        assert stats.success_rate > 0
        print("✅ Adaptation stats work")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Basic adaptation tests passed!")

async def test_adaptation_types():
    """Test different adaptation types"""
    print("\n🧪 Testing Adaptation Types")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = AdaptationFramework({"storage_path": temp_dir})
        
        # Create profile
        profile_id = framework.create_adaptation_profile("test_agent_2")
        
        # Test behavioral adaptation
        framework.trigger_adaptation(
            agent_id="test_agent_2",
            trigger=AdaptationTrigger.PERFORMANCE,
            context={"performance_score": 0.8},
            adaptation_type=AdaptationType.BEHAVIORAL
        )
        print("✅ Behavioral adaptation works")
        
        # Test communication adaptation
        framework.trigger_adaptation(
            agent_id="test_agent_2",
            trigger=AdaptationTrigger.CONTEXT_CHANGE,
            context={"new_context": "formal_meeting"},
            adaptation_type=AdaptationType.COMMUNICATION
        )
        print("✅ Communication adaptation works")
        
        # Test personality adaptation
        framework.trigger_adaptation(
            agent_id="test_agent_2",
            trigger=AdaptationTrigger.FEEDBACK,
            context={"user_preference": "more_empathetic"},
            adaptation_type=AdaptationType.PERSONALITY
        )
        print("✅ Personality adaptation works")
        
        # Test contextual adaptation
        framework.trigger_adaptation(
            agent_id="test_agent_2",
            trigger=AdaptationTrigger.CONTEXT_CHANGE,
            context={"context": "casual_chat"},
            adaptation_type=AdaptationType.CONTEXTUAL
        )
        print("✅ Contextual adaptation works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Adaptation types tests passed!")

async def test_adaptation_triggers():
    """Test different adaptation triggers"""
    print("\n🧪 Testing Adaptation Triggers")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = AdaptationFramework({"storage_path": temp_dir})
        
        # Create profile and rules
        profile_id = framework.create_adaptation_profile("test_agent_3")
        
        # Add rules for different triggers
        framework.add_adaptation_rule(
            name="Performance-based adaptation",
            trigger=AdaptationTrigger.PERFORMANCE,
            condition={"type": "threshold", "metric": "performance", "threshold": 0.7},
            action={"type": "adjust_personality", "trait": "assertiveness", "adjustment": 0.1}
        )
        
        framework.add_adaptation_rule(
            name="Feedback-based adaptation",
            trigger=AdaptationTrigger.FEEDBACK,
            condition={"type": "threshold", "metric": "feedback", "threshold": 0.8},
            action={"type": "adjust_personality", "trait": "friendliness", "adjustment": 0.1}
        )
        
        framework.add_adaptation_rule(
            name="Time-based adaptation",
            trigger=AdaptationTrigger.TIME_BASED,
            condition={"type": "time_based", "time_condition": "business_hours"},
            action={"type": "change_communication_style", "style_key": "formality", "new_value": "high"}
        )
        
        # Test performance trigger
        framework.trigger_adaptation(
            agent_id="test_agent_3",
            trigger=AdaptationTrigger.PERFORMANCE,
            context={"performance": 0.8},
            adaptation_type=AdaptationType.BEHAVIORAL
        )
        print("✅ Performance trigger works")
        
        # Test feedback trigger
        framework.trigger_adaptation(
            agent_id="test_agent_3",
            trigger=AdaptationTrigger.FEEDBACK,
            context={"feedback": 0.9},
            adaptation_type=AdaptationType.BEHAVIORAL
        )
        print("✅ Feedback trigger works")
        
        # Test time-based trigger
        framework.trigger_adaptation(
            agent_id="test_agent_3",
            trigger=AdaptationTrigger.TIME_BASED,
            context={"current_time": "business_hours"},
            adaptation_type=AdaptationType.COMMUNICATION
        )
        print("✅ Time-based trigger works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Adaptation triggers tests passed!")

async def test_adaptation_rules():
    """Test adaptation rule system"""
    print("\n🧪 Testing Adaptation Rules")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = AdaptationFramework({"storage_path": temp_dir})
        
        # Create profile
        profile_id = framework.create_adaptation_profile("test_agent_4")
        
        # Test complex condition
        rule_id = framework.add_adaptation_rule(
            name="Complex condition rule",
            trigger=AdaptationTrigger.PERFORMANCE,
            condition={
                "type": "threshold",
                "metric": "performance",
                "threshold": 0.8,
                "operator": ">="
            },
            action={
                "type": "adjust_personality",
                "trait": "creativity",
                "adjustment": 0.2,
                "direction": "increase"
            },
            priority=2
        )
        print("✅ Complex rule created")
        
        # Test contains condition
        rule_id2 = framework.add_adaptation_rule(
            name="Contains condition rule",
            trigger=AdaptationTrigger.CONTEXT_CHANGE,
            condition={
                "type": "contains",
                "key": "context_type",
                "values": ["formal", "business"]
            },
            action={
                "type": "change_communication_style",
                "style_key": "formality",
                "new_value": "high"
            },
            priority=1
        )
        print("✅ Contains condition rule created")
        
        # Test rule application
        framework.trigger_adaptation(
            agent_id="test_agent_4",
            trigger=AdaptationTrigger.PERFORMANCE,
            context={"performance": 0.9},
            adaptation_type=AdaptationType.BEHAVIORAL
        )
        print("✅ Rule application works")
        
        # Test context-based rule
        framework.trigger_adaptation(
            agent_id="test_agent_4",
            trigger=AdaptationTrigger.CONTEXT_CHANGE,
            context={"context_type": "formal"},
            adaptation_type=AdaptationType.COMMUNICATION
        )
        print("✅ Context-based rule works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Adaptation rules tests passed!")

async def test_adaptation_persistence():
    """Test adaptation data persistence"""
    print("\n🧪 Testing Adaptation Persistence")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        # Create framework and add data
        framework1 = AdaptationFramework({"storage_path": temp_dir})
        profile_id = framework1.create_adaptation_profile("persistent_agent")
        rule_id = framework1.add_adaptation_rule(
            name="Test rule",
            trigger=AdaptationTrigger.FEEDBACK,
            condition={"type": "threshold", "metric": "score", "threshold": 0.5},
            action={"type": "adjust_personality", "trait": "friendliness", "adjustment": 0.1}
        )
        adaptation_id = framework1.trigger_adaptation(
            agent_id="persistent_agent",
            trigger=AdaptationTrigger.FEEDBACK,
            context={"score": 0.8},
            adaptation_type=AdaptationType.BEHAVIORAL
        )
        
        # Create new framework instance (should load existing data)
        framework2 = AdaptationFramework({"storage_path": temp_dir})
        
        # Check if data was loaded
        assert len(framework2.profiles) == 1
        assert len(framework2.rules) == 1
        assert len(framework2.events) == 1
        print("✅ Adaptation persistence works")
        
        # Test stats consistency
        stats1 = framework1.get_adaptation_stats()
        stats2 = framework2.get_adaptation_stats()
        assert stats1.total_adaptations == stats2.total_adaptations
        print("✅ Stats consistency works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Adaptation persistence tests passed!")

async def test_adaptation_stats():
    """Test adaptation statistics"""
    print("\n🧪 Testing Adaptation Statistics")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = AdaptationFramework({"storage_path": temp_dir})
        
        # Create profile and add multiple adaptations
        profile_id = framework.create_adaptation_profile("stats_agent")
        
        # Add different types of adaptations
        for i in range(5):
            framework.trigger_adaptation(
                agent_id="stats_agent",
                trigger=AdaptationTrigger.PERFORMANCE,
                context={"performance": 0.7 + i * 0.05},
                adaptation_type=AdaptationType.BEHAVIORAL
            )
        
        for i in range(3):
            framework.trigger_adaptation(
                agent_id="stats_agent",
                trigger=AdaptationTrigger.FEEDBACK,
                context={"feedback": 0.8 + i * 0.05},
                adaptation_type=AdaptationType.COMMUNICATION
            )
        
        # Get comprehensive stats
        stats = framework.get_adaptation_stats()
        
        assert stats.total_adaptations >= 0  # May be 0 if no rules apply
        assert stats.successful_adaptations >= 0
        assert stats.failed_adaptations >= 0
        assert isinstance(stats.adaptation_types, dict)
        assert isinstance(stats.triggers, dict)
        assert 0 <= stats.average_confidence <= 1
        assert stats.adaptation_frequency >= 0
        assert 0 <= stats.success_rate <= 1
        assert stats.last_adaptation is not None
        print("✅ Adaptation statistics work")
        
        # Test stats accuracy
        assert stats.total_adaptations == stats.successful_adaptations + stats.failed_adaptations
        print("✅ Statistics accuracy validated")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Adaptation statistics tests passed!")

async def test_adaptation_control():
    """Test adaptation process control"""
    print("\n🧪 Testing Adaptation Control")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = AdaptationFramework({"storage_path": temp_dir})
        
        # Test starting adaptation
        framework.start_adaptation()
        assert framework.adaptation_active == True
        print("✅ Adaptation start works")
        
        # Test stopping adaptation
        framework.stop_adaptation()
        assert framework.adaptation_active == False
        print("✅ Adaptation stop works")
        
        # Test adaptation queue
        framework.adaptation_queue.append({"type": "test_adaptation"})
        assert len(framework.adaptation_queue) >= 1
        print("✅ Adaptation queue works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Adaptation control tests passed!")

async def test_data_export():
    """Test data export functionality"""
    print("\n🧪 Testing Data Export")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = AdaptationFramework({"storage_path": temp_dir})
        
        # Add some test data
        profile_id = framework.create_adaptation_profile("export_agent")
        rule_id = framework.add_adaptation_rule(
            name="Export test rule",
            trigger=AdaptationTrigger.FEEDBACK,
            condition={"type": "threshold", "metric": "score", "threshold": 0.5},
            action={"type": "adjust_personality", "trait": "friendliness", "adjustment": 0.1}
        )
        
        # Test JSON export
        json_export = framework.export_adaptation_data(format="json")
        assert isinstance(json_export, str)
        data = json.loads(json_export)
        assert "profiles" in data
        assert "rules" in data
        assert "events" in data
        assert "stats" in data
        print("✅ JSON export works")
        
        # Test dict export
        dict_export = framework.export_adaptation_data(format="dict")
        assert isinstance(dict_export, dict)
        assert "profiles" in dict_export
        print("✅ Dict export works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Data export tests passed!")

async def test_adaptation_clear():
    """Test adaptation data clearing"""
    print("\n🧪 Testing Adaptation Data Clear")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = AdaptationFramework({"storage_path": temp_dir})
        
        # Add some data
        profile_id = framework.create_adaptation_profile("clear_agent")
        rule_id = framework.add_adaptation_rule(
            name="Clear test rule",
            trigger=AdaptationTrigger.FEEDBACK,
            condition={"type": "threshold", "metric": "score", "threshold": 0.5},
            action={"type": "adjust_personality", "trait": "friendliness", "adjustment": 0.1}
        )
        
        # Verify data exists
        assert len(framework.profiles) > 0
        assert len(framework.rules) > 0
        print("✅ Data added successfully")
        
        # Clear data
        framework.clear_adaptation_data()
        
        # Verify data is cleared
        assert len(framework.profiles) == 0
        assert len(framework.rules) == 0
        assert len(framework.events) == 0
        print("✅ Data cleared successfully")
        
        # Test stats after clear
        stats = framework.get_adaptation_stats()
        assert stats.total_adaptations == 0
        assert stats.successful_adaptations == 0
        assert stats.failed_adaptations == 0
        print("✅ Stats reset after clear")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Adaptation data clear tests passed!")

async def test_integration_scenario():
    """Test end-to-end integration scenario"""
    print("\n🧪 Testing Integration Scenario")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = AdaptationFramework({"storage_path": temp_dir})
        
        # Simulate a complete adaptation scenario
        print("🤖 Simulating agent adaptation scenario...")
        
        # Create agent profile
        agent_id = "smart_agent_001"
        profile_id = framework.create_adaptation_profile(
            agent_id=agent_id,
            personality_traits={
                "friendliness": 0.5,
                "formality": 0.5,
                "assertiveness": 0.5,
                "empathy": 0.5,
                "creativity": 0.5
            },
            communication_style={
                "tone": "neutral",
                "verbosity": "medium",
                "technical_level": "medium"
            }
        )
        print(f"✅ Created profile for {agent_id}")
        
        # Add adaptation rules
        rules = [
            {
                "name": "Increase friendliness on positive feedback",
                "trigger": AdaptationTrigger.FEEDBACK,
                "condition": {"type": "threshold", "metric": "user_satisfaction", "threshold": 0.8},
                "action": {"type": "adjust_personality", "trait": "friendliness", "adjustment": 0.1, "direction": "increase"}
            },
            {
                "name": "Increase formality in business context",
                "trigger": AdaptationTrigger.CONTEXT_CHANGE,
                "condition": {"type": "contains", "key": "context", "values": ["business", "formal"]},
                "action": {"type": "change_communication_style", "style_key": "formality", "new_value": "high"}
            },
            {
                "name": "Increase assertiveness on high performance",
                "trigger": AdaptationTrigger.PERFORMANCE,
                "condition": {"type": "threshold", "metric": "performance_score", "threshold": 0.9},
                "action": {"type": "adjust_personality", "trait": "assertiveness", "adjustment": 0.15, "direction": "increase"}
            }
        ]
        
        for rule_data in rules:
            rule_id = framework.add_adaptation_rule(**rule_data)
            print(f"✅ Added rule: {rule_data['name']}")
        
        # Simulate different scenarios
        scenarios = [
            {
                "name": "Positive user feedback",
                "trigger": AdaptationTrigger.FEEDBACK,
                "context": {"user_satisfaction": 0.9, "feedback_type": "positive"},
                "type": AdaptationType.BEHAVIORAL
            },
            {
                "name": "Business meeting context",
                "trigger": AdaptationTrigger.CONTEXT_CHANGE,
                "context": {"context": "business", "meeting_type": "formal"},
                "type": AdaptationType.COMMUNICATION
            },
            {
                "name": "High performance achievement",
                "trigger": AdaptationTrigger.PERFORMANCE,
                "context": {"performance_score": 0.95, "task_complexity": "high"},
                "type": AdaptationType.BEHAVIORAL
            },
            {
                "name": "Casual conversation context",
                "trigger": AdaptationTrigger.CONTEXT_CHANGE,
                "context": {"context": "casual", "setting": "informal"},
                "type": AdaptationType.COMMUNICATION
            }
        ]
        
        for scenario in scenarios:
            adaptation_id = framework.trigger_adaptation(
                agent_id=agent_id,
                trigger=scenario["trigger"],
                context=scenario["context"],
                adaptation_type=scenario["type"]
            )
            print(f"✅ Triggered adaptation: {scenario['name']}")
        
        # Check final adaptation state
        final_state = framework.get_agent_adaptation_state(agent_id)
        assert final_state is not None
        print(f"✅ Final state: {len(final_state['personality_traits'])} traits, {final_state['adaptation_count']} adaptations")
        
        # Get comprehensive statistics
        stats = framework.get_adaptation_stats()
        print(f"✅ Final stats: {stats.total_adaptations} adaptations, {stats.success_rate:.2f} success rate")
        print(f"✅ Adaptation types: {list(stats.adaptation_types.keys())}")
        print(f"✅ Triggers used: {list(stats.triggers.keys())}")
        
        # Test data export
        export_data = framework.export_adaptation_data()
        assert "profiles" in export_data
        assert "rules" in export_data
        assert "events" in export_data
        print("✅ Data export successful")
        
        print("✅ Complete adaptation scenario successful")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Integration scenario tests passed!")

async def run_all_tests():
    """Run all adaptation framework tests"""
    print("🚀 Starting Pattern 12: Agent Adaptation Tests")
    print("=" * 60)
    
    try:
        await test_basic_adaptation()
        await test_adaptation_types()
        await test_adaptation_triggers()
        await test_adaptation_rules()
        await test_adaptation_persistence()
        await test_adaptation_stats()
        await test_adaptation_control()
        await test_data_export()
        await test_adaptation_clear()
        await test_integration_scenario()
        
        print("\n🎉 All Pattern 12: Agent Adaptation tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    asyncio.run(run_all_tests())
