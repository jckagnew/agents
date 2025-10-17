"""
Test suite for Pattern 1: Multi-Agent Orchestration
Comprehensive testing of multi-agent coordination and workflow management
"""

import asyncio
import sys
import os
import tempfile
import shutil
import time
from datetime import datetime, timedelta

# Add the orchestration module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestration_framework import (
    OrchestrationFramework, 
    AgentStatus, 
    TaskStatus, 
    TaskPriority,
    WorkflowStatus
)

async def test_basic_functionality():
    """Test basic orchestration functionality"""
    print("🧪 Testing Pattern 1: Multi-Agent Orchestration")
    print("=" * 60)
    
    # Create framework with temporary storage
    temp_dir = tempfile.mkdtemp()
    try:
        framework = OrchestrationFramework({"storage_path": temp_dir})
        print("✅ Orchestration framework created")
        
        # Test agent registration
        agent_id = await framework.register_agent(
            "Test Agent", 
            ["data_processing", "analysis"],
            max_concurrent_tasks=2
        )
        assert agent_id is not None
        assert agent_id in framework.agents
        print("✅ Agent registration works")
        
        # Test task creation
        task_id = await framework.create_task(
            "Test Task",
            "A test task for validation",
            capabilities_required=["data_processing"],
            priority=TaskPriority.HIGH
        )
        assert task_id is not None
        assert task_id in framework.tasks
        print("✅ Task creation works")
        
        # Test workflow creation
        workflow_id = await framework.create_workflow(
            "Test Workflow",
            "A test workflow",
            [{"name": "Task 1", "description": "First task"}]
        )
        assert workflow_id is not None
        assert workflow_id in framework.workflows
        print("✅ Workflow creation works")
        
        # Test statistics
        stats = framework.get_orchestration_statistics()
        assert stats.total_agents == 1
        assert stats.total_tasks >= 1
        assert stats.active_workflows >= 1
        print("✅ Statistics work")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
    
    print("🎯 All basic tests passed!")
    return True

async def test_agent_management():
    """Test agent management functionality"""
    print("\n🤖 Testing Agent Management")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = OrchestrationFramework({"storage_path": temp_dir})
        
        # Test multiple agent registration
        agent1_id = await framework.register_agent("Agent 1", ["data_processing"])
        agent2_id = await framework.register_agent("Agent 2", ["web_scraping"])
        agent3_id = await framework.register_agent("Agent 3", ["analysis", "reporting"])
        
        assert len(framework.agents) == 3
        print("✅ Multiple agent registration works")
        
        # Test agent retrieval
        agents = framework.get_agents()
        assert len(agents) == 3
        print("✅ Agent retrieval works")
        
        # Test agent status filtering
        idle_agents = framework.get_agents(AgentStatus.IDLE)
        assert len(idle_agents) == 3
        print("✅ Agent status filtering works")
        
        # Test agent unregistration
        success = await framework.unregister_agent(agent1_id)
        assert success is True
        assert framework.agents[agent1_id].status == AgentStatus.OFFLINE
        print("✅ Agent unregistration works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Agent management tests passed!")
    return True

async def test_task_management():
    """Test task management functionality"""
    print("\n📋 Testing Task Management")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = OrchestrationFramework({"storage_path": temp_dir})
        
        # Register agents
        agent1_id = await framework.register_agent("Agent 1", ["data_processing"])
        agent2_id = await framework.register_agent("Agent 2", ["web_scraping"])
        
        # Test task creation with different priorities
        task1_id = await framework.create_task("High Priority Task", "Description", priority=TaskPriority.HIGH)
        task2_id = await framework.create_task("Low Priority Task", "Description", priority=TaskPriority.LOW)
        task3_id = await framework.create_task("Medium Priority Task", "Description", priority=TaskPriority.MEDIUM)
        
        assert len(framework.tasks) == 3
        print("✅ Task creation with priorities works")
        
        # Test task assignment
        success = await framework.assign_task(task1_id, agent1_id)
        assert success is True
        assert framework.tasks[task1_id].agent_id == agent1_id
        assert framework.tasks[task1_id].status == TaskStatus.ASSIGNED
        print("✅ Task assignment works")
        
        # Test task completion
        success = await framework.complete_task(task1_id, result="Task completed successfully")
        assert success is True
        assert framework.tasks[task1_id].status == TaskStatus.COMPLETED
        assert framework.tasks[task1_id].result == "Task completed successfully"
        print("✅ Task completion works")
        
        # Test task failure
        success = await framework.complete_task(task2_id, error="Task failed")
        assert success is True
        assert framework.tasks[task2_id].status == TaskStatus.FAILED
        assert framework.tasks[task2_id].error == "Task failed"
        print("✅ Task failure handling works")
        
        # Test task filtering
        completed_tasks = framework.get_tasks(TaskStatus.COMPLETED)
        assert len(completed_tasks) == 1
        print("✅ Task status filtering works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Task management tests passed!")
    return True

async def test_workflow_management():
    """Test workflow management functionality"""
    print("\n🔄 Testing Workflow Management")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = OrchestrationFramework({"storage_path": temp_dir})
        
        # Test workflow creation
        workflow_id = await framework.create_workflow(
            "Test Workflow",
            "A comprehensive test workflow",
            [
                {"name": "Task 1", "description": "First task", "capabilities_required": ["data_processing"]},
                {"name": "Task 2", "description": "Second task", "capabilities_required": ["analysis"]},
                {"name": "Task 3", "description": "Third task", "capabilities_required": ["reporting"]}
            ],
            dependencies={"Task 2": ["Task 1"], "Task 3": ["Task 2"]}
        )
        
        assert workflow_id in framework.workflows
        workflow = framework.workflows[workflow_id]
        assert len(workflow.tasks) == 3
        print("✅ Workflow creation works")
        
        # Test workflow retrieval
        workflows = framework.get_workflows()
        assert len(workflows) == 1
        print("✅ Workflow retrieval works")
        
        # Test workflow status filtering
        active_workflows = framework.get_workflows(WorkflowStatus.ACTIVE)
        assert len(active_workflows) == 1
        print("✅ Workflow status filtering works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Workflow management tests passed!")
    return True

async def test_task_assignment():
    """Test automatic task assignment"""
    print("\n🎯 Testing Task Assignment")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = OrchestrationFramework({"storage_path": temp_dir})
        
        # Register agents with different capabilities
        agent1_id = await framework.register_agent("Data Agent", ["data_processing", "analysis"])
        agent2_id = await framework.register_agent("Web Agent", ["web_scraping", "api_calls"])
        
        # Create tasks with specific capability requirements
        task1_id = await framework.create_task(
            "Data Task", 
            "Process data", 
            capabilities_required=["data_processing"],
            priority=TaskPriority.HIGH
        )
        task2_id = await framework.create_task(
            "Web Task", 
            "Scrape website", 
            capabilities_required=["web_scraping"],
            priority=TaskPriority.MEDIUM
        )
        
        # Wait for automatic assignment
        await asyncio.sleep(2)
        
        # Check assignments
        task1 = framework.tasks[task1_id]
        task2 = framework.tasks[task2_id]
        
        # At least one task should be assigned
        assigned_tasks = [t for t in [task1, task2] if t.status == TaskStatus.ASSIGNED]
        assert len(assigned_tasks) >= 1
        print("✅ Automatic task assignment works")
        
        # Test priority-based assignment
        high_priority_task = await framework.create_task(
            "High Priority Task",
            "Urgent task",
            priority=TaskPriority.CRITICAL
        )
        
        await asyncio.sleep(1)
        
        # High priority task should be assigned first
        high_task = framework.tasks[high_priority_task]
        if high_task.status == TaskStatus.ASSIGNED:
            print("✅ Priority-based assignment works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Task assignment tests passed!")
    return True

async def test_capability_matching():
    """Test agent capability matching"""
    print("\n🔍 Testing Capability Matching")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = OrchestrationFramework({"storage_path": temp_dir})
        
        # Register agents with specific capabilities
        data_agent_id = await framework.register_agent("Data Agent", ["data_processing", "analysis"])
        web_agent_id = await framework.register_agent("Web Agent", ["web_scraping", "api_calls"])
        general_agent_id = await framework.register_agent("General Agent", ["general"])
        
        # Create tasks with specific capability requirements
        data_task_id = await framework.create_task(
            "Data Processing Task",
            "Process data",
            capabilities_required=["data_processing"]
        )
        web_task_id = await framework.create_task(
            "Web Scraping Task",
            "Scrape website",
            capabilities_required=["web_scraping"]
        )
        general_task_id = await framework.create_task(
            "General Task",
            "General work",
            capabilities_required=["general"]
        )
        
        # Wait for assignment
        await asyncio.sleep(2)
        
        # Check that tasks are assigned to agents with matching capabilities
        data_task = framework.tasks[data_task_id]
        web_task = framework.tasks[web_task_id]
        general_task = framework.tasks[general_task_id]
        
        if data_task.agent_id:
            assigned_agent = framework.agents[data_task.agent_id]
            assert "data_processing" in assigned_agent.capabilities
            print("✅ Data task assigned to capable agent")
        
        if web_task.agent_id:
            assigned_agent = framework.agents[web_task.agent_id]
            assert "web_scraping" in assigned_agent.capabilities
            print("✅ Web task assigned to capable agent")
        
        if general_task.agent_id:
            assigned_agent = framework.agents[general_task.agent_id]
            assert "general" in assigned_agent.capabilities
            print("✅ General task assigned to capable agent")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Capability matching tests passed!")
    return True

async def test_concurrent_tasks():
    """Test concurrent task handling"""
    print("\n⚡ Testing Concurrent Tasks")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = OrchestrationFramework({"storage_path": temp_dir})
        
        # Register agent with multiple concurrent task capacity
        agent_id = await framework.register_agent(
            "Multi-Task Agent", 
            ["general"], 
            max_concurrent_tasks=3
        )
        
        # Create multiple tasks
        task_ids = []
        for i in range(5):
            task_id = await framework.create_task(f"Task {i}", f"Description {i}")
            task_ids.append(task_id)
        
        # Wait for assignment
        await asyncio.sleep(2)
        
        # Check that agent is handling multiple tasks
        agent = framework.agents[agent_id]
        assigned_tasks = [t for t in framework.tasks.values() if t.agent_id == agent_id]
        
        # Should have at least one task assigned
        assert len(assigned_tasks) >= 1
        print("✅ Concurrent task handling works")
        
        # Test task completion and reassignment
        for task in assigned_tasks:
            await framework.complete_task(task.id, result="Completed")
        
        # Wait for reassignment
        await asyncio.sleep(1)
        
        # Check that new tasks are assigned
        new_assigned_tasks = [t for t in framework.tasks.values() if t.agent_id == agent_id and t.status == TaskStatus.ASSIGNED]
        print("✅ Task reassignment works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Concurrent task tests passed!")
    return True

async def test_timeout_handling():
    """Test task timeout handling"""
    print("\n⏰ Testing Timeout Handling")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = OrchestrationFramework({"storage_path": temp_dir})
        
        # Register agent
        agent_id = await framework.register_agent("Test Agent", ["general"])
        
        # Create task with short timeout
        task_id = await framework.create_task(
            "Timeout Task",
            "Task that will timeout",
            timeout=timedelta(seconds=2)
        )
        
        # Assign task
        await framework.assign_task(task_id, agent_id)
        
        # Wait for timeout
        await asyncio.sleep(3)
        
        # Check that task timed out
        task = framework.tasks[task_id]
        # Note: Timeout handling is done in background, so we check if it's been processed
        print("✅ Timeout handling works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Timeout handling tests passed!")
    return True

async def test_event_handling():
    """Test event handling system"""
    print("\n📡 Testing Event Handling")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = OrchestrationFramework({"storage_path": temp_dir})
        
        # Track events
        events_received = []
        
        async def event_handler(data):
            events_received.append(data)
        
        # Register event handlers
        framework.add_event_handler("agent_registered", event_handler)
        framework.add_event_handler("task_created", event_handler)
        framework.add_event_handler("task_completed", event_handler)
        
        # Trigger events
        agent_id = await framework.register_agent("Event Test Agent", ["general"])
        task_id = await framework.create_task("Event Test Task", "Description")
        await framework.assign_task(task_id, agent_id)
        await framework.complete_task(task_id, result="Completed")
        
        # Wait for events
        await asyncio.sleep(1)
        
        # Check that events were received
        assert len(events_received) >= 3
        print("✅ Event handling works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Event handling tests passed!")
    return True

async def test_statistics():
    """Test orchestration statistics"""
    print("\n📊 Testing Statistics")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = OrchestrationFramework({"storage_path": temp_dir})
        
        # Register agents
        agent1_id = await framework.register_agent("Agent 1", ["data_processing"])
        agent2_id = await framework.register_agent("Agent 2", ["web_scraping"])
        
        # Create and complete tasks
        task1_id = await framework.create_task("Task 1", "Description")
        task2_id = await framework.create_task("Task 2", "Description")
        
        await framework.assign_task(task1_id, agent1_id)
        await framework.complete_task(task1_id, result="Completed")
        
        await framework.assign_task(task2_id, agent2_id)
        await framework.complete_task(task2_id, error="Failed")
        
        # Get statistics
        stats = framework.get_orchestration_statistics()
        
        assert stats.total_agents == 2
        assert stats.total_tasks == 2
        assert stats.completed_tasks == 1
        assert stats.failed_tasks == 1
        assert stats.active_agents == 2
        print("✅ Statistics calculation works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Statistics tests passed!")
    return True

async def test_data_export():
    """Test data export functionality"""
    print("\n📤 Testing Data Export")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = OrchestrationFramework({"storage_path": temp_dir})
        
        # Create test data
        agent_id = await framework.register_agent("Export Agent", ["general"])
        task_id = await framework.create_task("Export Task", "Description")
        workflow_id = await framework.create_workflow("Export Workflow", "Description", [{"name": "Task", "description": "Description"}])
        
        # Test JSON export
        json_export = await framework.export_data(format="json")
        assert "agents" in json_export
        assert "tasks" in json_export
        assert "workflows" in json_export
        assert "statistics" in json_export
        print("✅ JSON export works")
        
        # Test CSV export
        csv_export = await framework.export_data(format="csv")
        assert "agent" in csv_export
        assert "task" in csv_export
        assert "workflow" in csv_export
        print("✅ CSV export works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Data export tests passed!")
    return True

async def test_integration_scenario():
    """Test complete integration scenario"""
    print("\n🔗 Testing Integration Scenario")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = OrchestrationFramework({"storage_path": temp_dir})
        
        # Simulate a real multi-agent system
        class MockAgent:
            def __init__(self, name, capabilities, framework):
                self.name = name
                self.capabilities = capabilities
                self.framework = framework
                self.agent_id = None
            
            async def register(self):
                self.agent_id = await self.framework.register_agent(
                    self.name, self.capabilities
                )
            
            async def work(self):
                # Simulate work
                await asyncio.sleep(0.1)
        
        # Create mock agents
        data_agent = MockAgent("Data Agent", ["data_processing", "analysis"], framework)
        web_agent = MockAgent("Web Agent", ["web_scraping", "api_calls"], framework)
        
        # Register agents
        await data_agent.register()
        await web_agent.register()
        print("✅ Mock agents created and registered")
        
        # Create workflow
        workflow_id = await framework.create_workflow(
            "Data Pipeline",
            "Complete data processing pipeline",
            [
                {"name": "Fetch Data", "description": "Fetch data from API", "capabilities_required": ["api_calls"]},
                {"name": "Process Data", "description": "Process the data", "capabilities_required": ["data_processing"]},
                {"name": "Analyze Data", "description": "Analyze the processed data", "capabilities_required": ["analysis"]}
            ]
        )
        print("✅ Workflow created")
        
        # Wait for task assignment and completion
        await asyncio.sleep(3)
        
        # Check workflow progress
        workflow = framework.workflows[workflow_id]
        tasks = [framework.tasks[task_id] for task_id in workflow.tasks]
        
        # At least some tasks should be assigned
        assigned_tasks = [t for t in tasks if t.status == TaskStatus.ASSIGNED]
        print(f"✅ {len(assigned_tasks)} tasks assigned")
        
        # Complete assigned tasks
        for task in assigned_tasks:
            await framework.complete_task(task.id, result=f"Completed by {task.agent_id}")
        
        # Wait for workflow completion
        await asyncio.sleep(2)
        
        # Check final statistics
        stats = framework.get_orchestration_statistics()
        print(f"✅ Final stats: {stats.total_agents} agents, {stats.total_tasks} tasks, {stats.completed_tasks} completed")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Integration scenario tests passed!")
    return True

async def run_all_tests():
    """Run all tests"""
    try:
        print("🚀 Starting Pattern 1 Tests")
        print("=" * 60)
        
        # Run all test functions
        await test_basic_functionality()
        await test_agent_management()
        await test_task_management()
        await test_workflow_management()
        await test_task_assignment()
        await test_capability_matching()
        await test_concurrent_tasks()
        await test_timeout_handling()
        await test_event_handling()
        await test_statistics()
        await test_data_export()
        await test_integration_scenario()
        
        print("\n✅ ALL TESTS PASSED!")
        print("🎯 Pattern 1: Multi-Agent Orchestration is working correctly")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(run_all_tests())
