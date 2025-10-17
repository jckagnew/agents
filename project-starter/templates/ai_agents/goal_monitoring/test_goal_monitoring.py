"""
Test suite for Pattern 10: Goal Setting & Monitoring
Comprehensive testing of goal setting and monitoring capabilities
"""

import asyncio
import sys
import os
import tempfile
import shutil
from datetime import datetime, timedelta

# Add the goal monitoring module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from goal_framework import (
    GoalFramework, 
    GoalType, 
    GoalPriority, 
    GoalStatus,
    ProgressMetric
)

async def test_basic_functionality():
    """Test basic goal management functionality"""
    print("🧪 Testing Pattern 10: Goal Setting & Monitoring")
    print("=" * 60)
    
    # Create framework with temporary storage
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        print("✅ Goal framework created")
        
        # Test creating goal
        goal_id = await framework.create_goal(
            "Test Goal",
            "A test goal for validation",
            GoalType.TASK,
            "agent1",
            priority=GoalPriority.MEDIUM
        )
        assert goal_id is not None
        assert goal_id in framework.goals
        print("✅ Goal creation works")
        
        # Test retrieving goals
        goals = framework.get_goals(agent_id="agent1")
        assert len(goals) == 1
        assert goals[0].title == "Test Goal"
        print("✅ Goal retrieval works")
        
        # Test goal statistics
        stats = framework.get_goal_statistics()
        assert stats.total_goals == 1
        assert stats.goals_by_status[GoalStatus.PENDING.value] == 1
        print("✅ Goal statistics work")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
    
    print("🎯 All basic tests passed!")
    return True

async def test_goal_types():
    """Test different goal types"""
    print("\n🎯 Testing Goal Types")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        
        # Test all goal types
        goal_types = [
            GoalType.TASK,
            GoalType.OBJECTIVE,
            GoalType.MILESTONE,
            GoalType.PERFORMANCE,
            GoalType.LEARNING,
            GoalType.BEHAVIORAL
        ]
        
        for goal_type in goal_types:
            goal_id = await framework.create_goal(
                f"Test {goal_type.value} goal",
                f"A test {goal_type.value} goal",
                goal_type,
                "agent1"
            )
            assert goal_id is not None
            print(f"✅ {goal_type.value} goal creation works")
        
        # Verify all goals stored
        stats = framework.get_goal_statistics()
        assert stats.total_goals == len(goal_types)
        print("✅ All goal types work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Goal type tests passed!")
    return True

async def test_goal_priorities():
    """Test goal priorities"""
    print("\n⭐ Testing Goal Priorities")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        
        # Test all priorities
        priorities = [
            GoalPriority.LOW,
            GoalPriority.MEDIUM,
            GoalPriority.HIGH,
            GoalPriority.CRITICAL
        ]
        
        for priority in priorities:
            goal_id = await framework.create_goal(
                f"Test {priority.value} priority goal",
                f"A test {priority.value} priority goal",
                GoalType.TASK,
                "agent1",
                priority=priority
            )
            assert goal_id is not None
            print(f"✅ {priority.value} priority goal creation works")
        
        # Verify all goals stored
        stats = framework.get_goal_statistics()
        assert stats.total_goals == len(priorities)
        print("✅ All goal priorities work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Goal priority tests passed!")
    return True

async def test_goal_progress():
    """Test goal progress tracking"""
    print("\n📊 Testing Goal Progress")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        
        # Create goal
        goal_id = await framework.create_goal(
            "Progress Test Goal",
            "A goal for testing progress tracking",
            GoalType.TASK,
            "agent1"
        )
        
        # Update progress
        success = await framework.update_goal_progress(goal_id, 25.0, "Quarter complete")
        assert success is True
        print("✅ Progress update works")
        
        # Verify progress updated
        goal = framework.goals[goal_id]
        assert goal.progress == 25.0
        assert goal.status == GoalStatus.IN_PROGRESS
        print("✅ Progress verification works")
        
        # Update to completion
        success = await framework.update_goal_progress(goal_id, 100.0, "Fully complete")
        assert success is True
        assert goal.status == GoalStatus.COMPLETED
        print("✅ Progress completion works")
        
        # Test progress history
        progress_history = framework.get_goal_progress(goal_id)
        assert len(progress_history) == 2
        print("✅ Progress history works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Goal progress tests passed!")
    return True

async def test_goal_completion():
    """Test goal completion functionality"""
    print("\n✅ Testing Goal Completion")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        
        # Create goal with success criteria
        goal_id = await framework.create_goal(
            "Completion Test Goal",
            "A goal for testing completion",
            GoalType.TASK,
            "agent1",
            success_criteria=["Criterion 1", "Criterion 2"]
        )
        
        # Complete goal
        success = await framework.complete_goal(
            goal_id,
            success_criteria_met=["Criterion 1", "Criterion 2"],
            evidence={"proof": "test evidence"},
            notes="Goal completed successfully"
        )
        assert success is True
        print("✅ Goal completion works")
        
        # Verify completion
        goal = framework.goals[goal_id]
        assert goal.status == GoalStatus.COMPLETED
        assert goal.progress == 100.0
        assert goal.completed_at is not None
        print("✅ Goal completion verification works")
        
        # Test achievements
        achievements = [a for a in framework.achievements if a.goal_id == goal_id]
        assert len(achievements) == 1
        assert "Criterion 1" in achievements[0].success_criteria_met
        print("✅ Goal achievements work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Goal completion tests passed!")
    return True

async def test_goal_failure():
    """Test goal failure functionality"""
    print("\n❌ Testing Goal Failure")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        
        # Create goal
        goal_id = await framework.create_goal(
            "Failure Test Goal",
            "A goal for testing failure",
            GoalType.TASK,
            "agent1"
        )
        
        # Fail goal
        success = await framework.fail_goal(
            goal_id,
            reason="Test failure",
            evidence={"error": "test error"}
        )
        assert success is True
        print("✅ Goal failure works")
        
        # Verify failure
        goal = framework.goals[goal_id]
        assert goal.status == GoalStatus.FAILED
        print("✅ Goal failure verification works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Goal failure tests passed!")
    return True

async def test_goal_pause_resume():
    """Test goal pause and resume functionality"""
    print("\n⏸️  Testing Goal Pause/Resume")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        
        # Create goal
        goal_id = await framework.create_goal(
            "Pause Test Goal",
            "A goal for testing pause/resume",
            GoalType.TASK,
            "agent1"
        )
        
        # Pause goal
        success = await framework.pause_goal(goal_id, "Test pause")
        assert success is True
        print("✅ Goal pause works")
        
        # Verify pause
        goal = framework.goals[goal_id]
        assert goal.status == GoalStatus.PAUSED
        print("✅ Goal pause verification works")
        
        # Resume goal
        success = await framework.resume_goal(goal_id)
        assert success is True
        print("✅ Goal resume works")
        
        # Verify resume
        goal = framework.goals[goal_id]
        assert goal.status == GoalStatus.IN_PROGRESS
        print("✅ Goal resume verification works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Goal pause/resume tests passed!")
    return True

async def test_goal_cancellation():
    """Test goal cancellation functionality"""
    print("\n🚫 Testing Goal Cancellation")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        
        # Create goal
        goal_id = await framework.create_goal(
            "Cancel Test Goal",
            "A goal for testing cancellation",
            GoalType.TASK,
            "agent1"
        )
        
        # Cancel goal
        success = await framework.cancel_goal(goal_id, "Test cancellation")
        assert success is True
        print("✅ Goal cancellation works")
        
        # Verify cancellation
        goal = framework.goals[goal_id]
        assert goal.status == GoalStatus.CANCELLED
        print("✅ Goal cancellation verification works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Goal cancellation tests passed!")
    return True

async def test_goal_filtering():
    """Test goal filtering functionality"""
    print("\n🔍 Testing Goal Filtering")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        
        # Create goals with different properties
        goal1_id = await framework.create_goal(
            "High Priority Task",
            "A high priority task",
            GoalType.TASK,
            "agent1",
            priority=GoalPriority.HIGH
        )
        
        goal2_id = await framework.create_goal(
            "Learning Goal",
            "A learning goal",
            GoalType.LEARNING,
            "agent2",
            priority=GoalPriority.MEDIUM
        )
        
        # Test filtering by agent
        agent1_goals = framework.get_goals(agent_id="agent1")
        assert len(agent1_goals) == 1
        assert agent1_goals[0].title == "High Priority Task"
        print("✅ Agent filtering works")
        
        # Test filtering by priority
        high_priority_goals = framework.get_goals(priority=GoalPriority.HIGH)
        assert len(high_priority_goals) == 1
        assert high_priority_goals[0].title == "High Priority Task"
        print("✅ Priority filtering works")
        
        # Test filtering by type
        learning_goals = framework.get_goals(goal_type=GoalType.LEARNING)
        assert len(learning_goals) == 1
        assert learning_goals[0].title == "Learning Goal"
        print("✅ Type filtering works")
        
        # Test filtering by status
        pending_goals = framework.get_goals(status=GoalStatus.PENDING)
        assert len(pending_goals) == 2
        print("✅ Status filtering works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Goal filtering tests passed!")
    return True

async def test_overdue_goals():
    """Test overdue goal detection"""
    print("\n⏰ Testing Overdue Goals")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        
        # Create goal with past due date
        past_due = datetime.now() - timedelta(days=1)
        goal_id = await framework.create_goal(
            "Overdue Goal",
            "A goal that is overdue",
            GoalType.TASK,
            "agent1",
            due_date=past_due
        )
        
        # Create goal with future due date
        future_due = datetime.now() + timedelta(days=1)
        await framework.create_goal(
            "Future Goal",
            "A goal with future due date",
            GoalType.TASK,
            "agent1",
            due_date=future_due
        )
        
        # Test overdue detection
        overdue_goals = framework.get_overdue_goals()
        assert len(overdue_goals) == 1
        assert overdue_goals[0].title == "Overdue Goal"
        print("✅ Overdue goal detection works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Overdue goal tests passed!")
    return True

async def test_goal_statistics():
    """Test goal statistics functionality"""
    print("\n📈 Testing Goal Statistics")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        
        # Create various goals
        goal1_id = await framework.create_goal("Task 1", "Description 1", GoalType.TASK, "agent1", GoalPriority.HIGH)
        goal2_id = await framework.create_goal("Task 2", "Description 2", GoalType.LEARNING, "agent1", GoalPriority.MEDIUM)
        goal3_id = await framework.create_goal("Task 3", "Description 3", GoalType.OBJECTIVE, "agent2", GoalPriority.LOW)
        
        # Complete one goal
        await framework.complete_goal(goal1_id)
        
        # Get statistics
        stats = framework.get_goal_statistics()
        assert stats.total_goals == 3
        assert stats.goals_by_status[GoalStatus.COMPLETED.value] == 1
        assert stats.goals_by_status[GoalStatus.PENDING.value] == 2
        assert stats.goals_by_priority[GoalPriority.HIGH.value] == 1
        assert stats.goals_by_priority[GoalPriority.MEDIUM.value] == 1
        assert stats.goals_by_priority[GoalPriority.LOW.value] == 1
        assert stats.goals_by_type[GoalType.TASK.value] == 1
        assert stats.goals_by_type[GoalType.LEARNING.value] == 1
        assert stats.goals_by_type[GoalType.OBJECTIVE.value] == 1
        assert stats.completion_rate > 0
        assert stats.active_goals == 2
        print("✅ Goal statistics work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Goal statistics tests passed!")
    return True

async def test_goal_export():
    """Test goal export functionality"""
    print("\n📤 Testing Goal Export")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        
        # Create test goals
        await framework.create_goal("Export Test 1", "Description 1", GoalType.TASK, "agent1")
        await framework.create_goal("Export Test 2", "Description 2", GoalType.LEARNING, "agent2")
        
        # Test JSON export
        json_export = await framework.export_goals(format="json")
        assert "Export Test 1" in json_export
        assert "Export Test 2" in json_export
        print("✅ JSON export works")
        
        # Test CSV export
        csv_export = await framework.export_goals(format="csv")
        assert "Export Test 1" in csv_export
        assert "Export Test 2" in csv_export
        print("✅ CSV export works")
        
        # Test filtered export
        agent1_export = await framework.export_goals(agent_id="agent1", format="json")
        assert "Export Test 1" in agent1_export
        assert "Export Test 2" not in agent1_export
        print("✅ Filtered export works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Goal export tests passed!")
    return True

async def test_integration_scenario():
    """Test complete integration scenario"""
    print("\n🔗 Testing Integration Scenario")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = GoalFramework({"storage_path": temp_dir})
        
        # Simulate a real agent scenario
        class MockAgent:
            def __init__(self, name, goal_framework):
                self.name = name
                self.goals = goal_framework
            
            async def set_goal(self, title, description, goal_type, priority=GoalPriority.MEDIUM):
                return await self.goals.create_goal(
                    title, description, goal_type, self.name, priority
                )
            
            async def work_on_goal(self, goal_id, progress, notes=""):
                return await self.goals.update_goal_progress(goal_id, progress, notes)
            
            async def complete_goal(self, goal_id, evidence=None):
                return await self.goals.complete_goal(goal_id, evidence=evidence)
            
            def get_my_goals(self):
                return self.goals.get_goals(agent_id=self.name)
        
        # Create agent
        agent = MockAgent("agent1", framework)
        print("✅ Mock agent created")
        
        # Set goals
        goal1_id = await agent.set_goal("Learn Python", "Master Python programming", GoalType.LEARNING, GoalPriority.HIGH)
        goal2_id = await agent.set_goal("Build Project", "Create a Python project", GoalType.TASK, GoalPriority.MEDIUM)
        
        # Work on goals
        await agent.work_on_goal(goal1_id, 50.0, "Halfway through tutorial")
        await agent.work_on_goal(goal2_id, 25.0, "Started project setup")
        
        # Complete one goal
        await agent.complete_goal(goal1_id, {"tutorial_completed": True})
        
        # Check goals
        goals = agent.get_my_goals()
        assert len(goals) == 2
        print("✅ Agent goal management works")
        
        # Check statistics
        stats = framework.get_goal_statistics()
        assert stats.total_goals == 2
        assert stats.completion_rate == 50.0
        print("✅ Integration statistics work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Integration scenario tests passed!")
    return True

async def run_all_tests():
    """Run all tests"""
    try:
        print("🚀 Starting Pattern 10 Tests")
        print("=" * 60)
        
        # Run all test functions
        await test_basic_functionality()
        await test_goal_types()
        await test_goal_priorities()
        await test_goal_progress()
        await test_goal_completion()
        await test_goal_failure()
        await test_goal_pause_resume()
        await test_goal_cancellation()
        await test_goal_filtering()
        await test_overdue_goals()
        await test_goal_statistics()
        await test_goal_export()
        await test_integration_scenario()
        
        print("\n✅ ALL TESTS PASSED!")
        print("🎯 Pattern 10: Goal Setting & Monitoring is working correctly")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(run_all_tests())
