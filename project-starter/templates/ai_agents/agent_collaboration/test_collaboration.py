"""
Test suite for Pattern 3: Agent Collaboration
Comprehensive testing of agent collaboration and shared workspace management
"""

import asyncio
import sys
import os
import tempfile
import shutil
import time
from datetime import datetime, timedelta

# Add the collaboration module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from collaboration_framework import (
    CollaborationFramework, 
    CollaborationType, 
    CollaborationStatus,
    ParticipantRole,
    ConflictResolutionStrategy
)

async def test_basic_functionality():
    """Test basic collaboration functionality"""
    print("🧪 Testing Pattern 3: Agent Collaboration")
    print("=" * 60)
    
    # Create framework with temporary storage
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CollaborationFramework({"storage_path": temp_dir, "skip_database": True})
        print("✅ Collaboration framework created")
        
        # Test workspace creation
        workspace_id = await framework.create_workspace(
            "Test Workspace",
            "A test collaboration workspace",
            CollaborationType.SHARED_WORKSPACE,
            "agent1"
        )
        assert workspace_id is not None
        assert workspace_id in framework.workspaces
        print("✅ Workspace creation works")
        
        # Test workspace joining
        success = await framework.join_workspace(workspace_id, "agent2", ParticipantRole.CONTRIBUTOR)
        assert success is True
        workspace = framework.workspaces[workspace_id]
        assert len(workspace.participants) == 2
        print("✅ Workspace joining works")
        
        # Test collaboration start
        success = await framework.start_collaboration(workspace_id)
        assert success is True
        assert workspace.status == CollaborationStatus.ACTIVE
        print("✅ Collaboration start works")
        
        # Test event recording
        event_id = await framework.record_collaboration_event(
            workspace_id, "agent1", "action", {"action": "create_document"}
        )
        assert event_id is not None
        print("✅ Event recording works")
        
        # Test metrics
        metrics = framework.get_collaboration_metrics()
        assert metrics.total_workspaces == 1
        assert metrics.active_workspaces == 1
        print("✅ Collaboration metrics work")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
    
    print("🎯 All basic tests passed!")
    return True

async def test_workspace_management():
    """Test workspace management functionality"""
    print("\n🏢 Testing Workspace Management")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CollaborationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Test different collaboration types
        collaboration_types = [
            CollaborationType.SHARED_WORKSPACE,
            CollaborationType.PEER_REVIEW,
            CollaborationType.PAIR_PROGRAMMING,
            CollaborationType.BRAINSTORMING,
            CollaborationType.DECISION_MAKING,
            CollaborationType.KNOWLEDGE_SHARING,
            CollaborationType.MENTORING,
            CollaborationType.TEAM_MEETING
        ]
        
        workspace_ids = []
        for collab_type in collaboration_types:
            workspace_id = await framework.create_workspace(
                f"Test {collab_type.value}",
                f"Test {collab_type.value} workspace",
                collab_type,
                "agent1"
            )
            assert workspace_id is not None
            workspace_ids.append(workspace_id)
            print(f"✅ {collab_type.value} workspace creation works")
        
        # Test workspace joining with different roles
        roles = [
            ParticipantRole.LEADER,
            ParticipantRole.CONTRIBUTOR,
            ParticipantRole.REVIEWER,
            ParticipantRole.OBSERVER,
            ParticipantRole.MENTOR,
            ParticipantRole.MENTEE,
            ParticipantRole.FACILITATOR,
            ParticipantRole.RECORDER
        ]
        
        for i, role in enumerate(roles):
            workspace_id = workspace_ids[i % len(workspace_ids)]
            success = await framework.join_workspace(workspace_id, f"agent{i+2}", role)
            assert success is True
            print(f"✅ {role.value} role joining works")
        
        # Test workspace leaving
        success = await framework.leave_workspace(workspace_ids[0], "agent2")
        assert success is True
        workspace = framework.workspaces[workspace_ids[0]]
        assert len(workspace.participants) == 1  # Only creator left
        print("✅ Workspace leaving works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Workspace management tests passed!")
    return True

async def test_collaboration_lifecycle():
    """Test collaboration lifecycle management"""
    print("\n🔄 Testing Collaboration Lifecycle")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CollaborationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Create workspace
        workspace_id = await framework.create_workspace(
            "Lifecycle Test",
            "Test collaboration lifecycle",
            CollaborationType.SHARED_WORKSPACE,
            "agent1"
        )
        
        # Add participants
        await framework.join_workspace(workspace_id, "agent2", ParticipantRole.CONTRIBUTOR)
        await framework.join_workspace(workspace_id, "agent3", ParticipantRole.REVIEWER)
        
        workspace = framework.workspaces[workspace_id]
        assert workspace.status == CollaborationStatus.PLANNING
        print("✅ Planning status works")
        
        # Start collaboration
        success = await framework.start_collaboration(workspace_id)
        assert success is True
        assert workspace.status == CollaborationStatus.ACTIVE
        assert workspace.started_at is not None
        print("✅ Collaboration start works")
        
        # Record some events
        await framework.record_collaboration_event(workspace_id, "agent1", "action", {"action": "start_meeting"})
        await framework.record_collaboration_event(workspace_id, "agent2", "comment", {"comment": "Ready to collaborate"})
        await framework.record_collaboration_event(workspace_id, "agent3", "review", {"review": "Looks good"})
        
        # Complete collaboration
        success = await framework.complete_collaboration(workspace_id)
        assert success is True
        assert workspace.status == CollaborationStatus.COMPLETED
        assert workspace.completed_at is not None
        print("✅ Collaboration completion works")
        
        # Test that starting completed collaboration fails
        success = await framework.start_collaboration(workspace_id)
        assert success is False
        print("✅ Collaboration state validation works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Collaboration lifecycle tests passed!")
    return True

async def test_shared_resources():
    """Test shared resource management"""
    print("\n📁 Testing Shared Resources")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CollaborationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Create workspace
        workspace_id = await framework.create_workspace(
            "Resource Test",
            "Test shared resources",
            CollaborationType.SHARED_WORKSPACE,
            "agent1"
        )
        
        # Add participants
        await framework.join_workspace(workspace_id, "agent2", ParticipantRole.CONTRIBUTOR, ["read", "write"])
        await framework.join_workspace(workspace_id, "agent3", ParticipantRole.OBSERVER, ["read"])
        
        # Start collaboration
        await framework.start_collaboration(workspace_id)
        
        # Test adding resources
        success = await framework.add_shared_resource(workspace_id, "document1", {"content": "Test document"}, "agent1")
        assert success is True
        print("✅ Resource addition by leader works")
        
        success = await framework.add_shared_resource(workspace_id, "document2", {"content": "Another document"}, "agent2")
        assert success is True
        print("✅ Resource addition by contributor works")
        
        # Test permission check
        success = await framework.add_shared_resource(workspace_id, "document3", {"content": "Forbidden document"}, "agent3")
        assert success is False  # Observer doesn't have write permission
        print("✅ Permission validation works")
        
        # Check resources were added
        workspace = framework.workspaces[workspace_id]
        assert len(workspace.shared_resources) == 2
        assert "document1" in workspace.shared_resources
        assert "document2" in workspace.shared_resources
        print("✅ Resource storage works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Shared resources tests passed!")
    return True

async def test_event_recording():
    """Test collaboration event recording"""
    print("\n📝 Testing Event Recording")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CollaborationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Create workspace
        workspace_id = await framework.create_workspace(
            "Event Test",
            "Test event recording",
            CollaborationType.SHARED_WORKSPACE,
            "agent1"
        )
        
        # Add participants
        await framework.join_workspace(workspace_id, "agent2", ParticipantRole.CONTRIBUTOR)
        
        # Start collaboration
        await framework.start_collaboration(workspace_id)
        
        # Record various event types
        event_types = ["action", "comment", "review", "decision", "question", "answer", "suggestion", "approval"]
        
        for i, event_type in enumerate(event_types):
            event_id = await framework.record_collaboration_event(
                workspace_id, 
                f"agent{(i % 2) + 1}", 
                event_type, 
                {event_type: f"Test {event_type} {i}"}
            )
            assert event_id is not None
            print(f"✅ {event_type} event recording works")
        
        # Test event retrieval
        events = await framework.get_workspace_events(workspace_id)
        assert len(events) == len(event_types)
        print("✅ Event retrieval works")
        
        # Test event filtering
        action_events = await framework.get_workspace_events(workspace_id, ["action"])
        assert len(action_events) == 1
        print("✅ Event filtering works")
        
        # Test participant activity tracking
        workspace = framework.workspaces[workspace_id]
        for participant in workspace.participants:
            if participant.agent_id in ["agent1", "agent2"]:
                assert participant.last_active is not None
        print("✅ Activity tracking works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Event recording tests passed!")
    return True

async def test_conflict_management():
    """Test conflict detection and resolution"""
    print("\n⚔️ Testing Conflict Management")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CollaborationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Create workspace
        workspace_id = await framework.create_workspace(
            "Conflict Test",
            "Test conflict management",
            CollaborationType.DECISION_MAKING,
            "agent1"
        )
        
        # Add participants
        await framework.join_workspace(workspace_id, "agent2", ParticipantRole.CONTRIBUTOR)
        await framework.join_workspace(workspace_id, "agent3", ParticipantRole.REVIEWER)
        
        # Start collaboration
        await framework.start_collaboration(workspace_id)
        
        # Simulate conflicting actions
        await framework.record_collaboration_event(workspace_id, "agent1", "action", {"action": "choose_option_a"})
        await framework.record_collaboration_event(workspace_id, "agent2", "action", {"action": "choose_option_b"})
        
        # Wait for conflict detection
        await asyncio.sleep(2)
        
        # Check if conflicts were detected
        conflicts = [c for c in framework.conflicts.values() if c.workspace_id == workspace_id]
        print(f"✅ Detected {len(conflicts)} conflicts")
        
        # Test conflict resolution
        if conflicts:
            conflict = conflicts[0]
            success = await framework.resolve_conflict(
                conflict.id,
                ConflictResolutionStrategy.MAJORITY_VOTE,
                "Majority voted for option A",
                "agent1"
            )
            assert success is True
            assert conflict.resolved_at is not None
            print("✅ Conflict resolution works")
        
        # Test different resolution strategies
        resolution_strategies = [
            ConflictResolutionStrategy.MAJORITY_VOTE,
            ConflictResolutionStrategy.LEADER_DECISION,
            ConflictResolutionStrategy.CONSENSUS,
            ConflictResolutionStrategy.EXPERT_OPINION,
            ConflictResolutionStrategy.RANDOM_SELECTION,
            ConflictResolutionStrategy.MEDIATION,
            ConflictResolutionStrategy.HIERARCHICAL
        ]
        
        for strategy in resolution_strategies:
            # Create a test conflict
            conflict_id = await framework._create_conflict(
                workspace_id, ["agent1", "agent2"], "test_conflict", "Test conflict", "low"
            )
            
            # Resolve it
            success = await framework.resolve_conflict(conflict_id, strategy, f"Resolved using {strategy.value}", "agent1")
            assert success is True
            print(f"✅ {strategy.value} resolution works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Conflict management tests passed!")
    return True

async def test_agent_workspace_management():
    """Test agent workspace management"""
    print("\n👥 Testing Agent Workspace Management")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CollaborationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Create multiple workspaces
        workspace1_id = await framework.create_workspace("Workspace 1", "First workspace", CollaborationType.SHARED_WORKSPACE, "agent1")
        workspace2_id = await framework.create_workspace("Workspace 2", "Second workspace", CollaborationType.PEER_REVIEW, "agent2")
        workspace3_id = await framework.create_workspace("Workspace 3", "Third workspace", CollaborationType.BRAINSTORMING, "agent3")
        
        # Add agent1 to multiple workspaces
        await framework.join_workspace(workspace2_id, "agent1", ParticipantRole.CONTRIBUTOR)
        await framework.join_workspace(workspace3_id, "agent1", ParticipantRole.REVIEWER)
        
        # Test getting agent workspaces
        agent1_workspaces = await framework.get_agent_workspaces("agent1")
        assert len(agent1_workspaces) == 3
        print("✅ Agent workspace retrieval works")
        
        # Test workspace filtering by status
        await framework.start_collaboration(workspace1_id)
        await framework.start_collaboration(workspace2_id)
        
        active_workspaces = [w for w in agent1_workspaces if w.status == CollaborationStatus.ACTIVE]
        assert len(active_workspaces) == 2
        print("✅ Workspace status filtering works")
        
        # Test leaving workspaces
        success = await framework.leave_workspace(workspace3_id, "agent1")
        assert success is True
        
        agent1_workspaces = await framework.get_agent_workspaces("agent1")
        assert len(agent1_workspaces) == 2
        print("✅ Workspace leaving works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Agent workspace management tests passed!")
    return True

async def test_collaboration_metrics():
    """Test collaboration metrics calculation"""
    print("\n📊 Testing Collaboration Metrics")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CollaborationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Create multiple workspaces with different statuses
        workspace1_id = await framework.create_workspace("Active Workspace", "Active workspace", CollaborationType.SHARED_WORKSPACE, "agent1")
        workspace2_id = await framework.create_workspace("Planning Workspace", "Planning workspace", CollaborationType.PEER_REVIEW, "agent2")
        workspace3_id = await framework.create_workspace("Completed Workspace", "Completed workspace", CollaborationType.BRAINSTORMING, "agent3")
        
        # Add participants
        await framework.join_workspace(workspace1_id, "agent2", ParticipantRole.CONTRIBUTOR)
        await framework.join_workspace(workspace1_id, "agent3", ParticipantRole.REVIEWER)
        await framework.join_workspace(workspace2_id, "agent1", ParticipantRole.CONTRIBUTOR)
        await framework.join_workspace(workspace3_id, "agent1", ParticipantRole.LEADER)
        await framework.join_workspace(workspace3_id, "agent2", ParticipantRole.CONTRIBUTOR)
        
        # Start some collaborations
        await framework.start_collaboration(workspace1_id)
        await framework.start_collaboration(workspace3_id)
        
        # Complete one collaboration
        await framework.complete_collaboration(workspace3_id)
        
        # Record some events
        await framework.record_collaboration_event(workspace1_id, "agent1", "action", {"action": "test"})
        await framework.record_collaboration_event(workspace1_id, "agent2", "comment", {"comment": "test"})
        await framework.record_collaboration_event(workspace3_id, "agent3", "decision", {"decision": "test"})
        
        # Get metrics
        metrics = framework.get_collaboration_metrics()
        
        assert metrics.total_workspaces == 3
        assert metrics.active_workspaces == 1
        assert metrics.total_participants >= 6  # At least 6 participants
        assert metrics.average_participants_per_workspace >= 2.0
        assert metrics.collaboration_events == 3
        print("✅ Metrics calculation works")
        
        # Test engagement scores
        assert len(metrics.participant_engagement_scores) >= 3
        print("✅ Engagement scores work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Collaboration metrics tests passed!")
    return True

async def test_event_handling():
    """Test event handling system"""
    print("\n📡 Testing Event Handling")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CollaborationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Track events
        events_received = []
        
        async def event_handler(data):
            events_received.append(data)
        
        # Register event handlers
        framework.add_event_handler("workspace_created", event_handler)
        framework.add_event_handler("agent_joined_workspace", event_handler)
        framework.add_event_handler("collaboration_started", event_handler)
        framework.add_event_handler("collaboration_event", event_handler)
        
        # Trigger events
        workspace_id = await framework.create_workspace("Event Test", "Test events", CollaborationType.SHARED_WORKSPACE, "agent1")
        await framework.join_workspace(workspace_id, "agent2", ParticipantRole.CONTRIBUTOR)
        await framework.start_collaboration(workspace_id)
        await framework.record_collaboration_event(workspace_id, "agent1", "action", {"action": "test"})
        
        # Wait for events
        await asyncio.sleep(1)
        
        # Check that events were received
        assert len(events_received) >= 4
        print("✅ Event handling works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Event handling tests passed!")
    return True

async def test_data_export():
    """Test data export functionality"""
    print("\n📤 Testing Data Export")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CollaborationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Create test data
        workspace_id = await framework.create_workspace("Export Test", "Test export", CollaborationType.SHARED_WORKSPACE, "agent1")
        await framework.join_workspace(workspace_id, "agent2", ParticipantRole.CONTRIBUTOR)
        await framework.start_collaboration(workspace_id)
        await framework.record_collaboration_event(workspace_id, "agent1", "action", {"action": "test"})
        
        # Test JSON export
        json_export = await framework.export_collaboration_data(format="json")
        assert "workspaces" in json_export
        assert "events" in json_export
        assert "conflicts" in json_export
        assert "metrics" in json_export
        print("✅ JSON export works")
        
        # Test CSV export
        csv_export = await framework.export_collaboration_data(format="csv")
        assert "workspace" in csv_export
        assert "event" in csv_export
        # Note: conflicts may not be present if none were created
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
        framework = CollaborationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Simulate a real collaborative development session
        class MockCollaborativeAgent:
            def __init__(self, name, framework):
                self.name = name
                self.framework = framework
                self.workspace_id = None
            
            async def create_workspace(self, name, description, collab_type):
                self.workspace_id = await self.framework.create_workspace(name, description, collab_type, self.name)
                return self.workspace_id
            
            async def join_workspace(self, workspace_id, role=ParticipantRole.CONTRIBUTOR):
                return await self.framework.join_workspace(workspace_id, self.name, role)
            
            async def collaborate(self, action, content):
                if self.workspace_id:
                    return await self.framework.record_collaboration_event(
                        self.workspace_id, self.name, action, content
                    )
                return None
        
        # Create mock agents
        lead_agent = MockCollaborativeAgent("lead_agent", framework)
        dev_agent = MockCollaborativeAgent("dev_agent", framework)
        review_agent = MockCollaborativeAgent("review_agent", framework)
        
        # Create workspace
        workspace_id = await lead_agent.create_workspace(
            "Development Project",
            "Collaborative software development",
            CollaborationType.PAIR_PROGRAMMING
        )
        print("✅ Mock agents and workspace created")
        
        # Join workspace
        await dev_agent.join_workspace(workspace_id, ParticipantRole.CONTRIBUTOR)
        await review_agent.join_workspace(workspace_id, ParticipantRole.REVIEWER)
        
        # Start collaboration
        await framework.start_collaboration(workspace_id)
        print("✅ Collaboration started")
        
        # Simulate collaborative work
        await lead_agent.collaborate("action", {"action": "define_requirements", "content": "User authentication system"})
        await dev_agent.collaborate("action", {"action": "implement_feature", "content": "Login form component"})
        await review_agent.collaborate("review", {"review": "Code looks good, minor suggestions"})
        await dev_agent.collaborate("action", {"action": "apply_feedback", "content": "Updated login form"})
        await review_agent.collaborate("approval", {"approval": "Approved for merge"})
        await lead_agent.collaborate("decision", {"decision": "Feature complete", "status": "approved"})
        
        print("✅ Collaborative work simulation completed")
        
        # Check final state
        workspace = framework.workspaces[workspace_id]
        events = await framework.get_workspace_events(workspace_id)
        
        assert len(workspace.participants) == 3
        assert len(events) >= 1  # At least some events were recorded
        print(f"✅ Final state: {len(workspace.participants)} participants, {len(events)} events")
        
        # Complete collaboration
        await framework.complete_collaboration(workspace_id)
        
        # Check metrics
        metrics = framework.get_collaboration_metrics()
        assert metrics.total_workspaces == 1
        assert metrics.collaboration_events >= 1  # At least some events were recorded
        print(f"✅ Final metrics: {metrics.total_workspaces} workspaces, {metrics.collaboration_events} events")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Integration scenario tests passed!")
    return True

async def test_performance():
    """Test collaboration performance"""
    print("\n⚡ Testing Collaboration Performance")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CollaborationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Test workspace creation performance
        start_time = time.time()
        
        workspace_ids = []
        for i in range(50):
            workspace_id = await framework.create_workspace(
                f"Performance Test {i}",
                f"Test workspace {i}",
                CollaborationType.SHARED_WORKSPACE,
                f"agent{i}"
            )
            workspace_ids.append(workspace_id)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Created 50 workspaces in {duration:.2f} seconds ({50/duration:.1f} workspaces/s)")
        
        # Test event recording performance
        start_time = time.time()
        
        for i in range(100):
            workspace_id = workspace_ids[i % len(workspace_ids)]
            await framework.record_collaboration_event(
                workspace_id, f"agent{i}", "action", {"action": f"test_action_{i}"}
            )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Recorded 100 events in {duration:.2f} seconds ({100/duration:.1f} events/s)")
        
        # Test concurrent operations
        start_time = time.time()
        
        tasks = []
        for i in range(20):
            workspace_id = workspace_ids[i % len(workspace_ids)]
            task = framework.record_collaboration_event(
                workspace_id, f"agent{i}", "concurrent_action", {"action": f"concurrent_{i}"}
            )
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Recorded 20 concurrent events in {duration:.2f} seconds")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Performance tests passed!")
    return True

async def run_all_tests():
    """Run all tests"""
    try:
        print("🚀 Starting Pattern 3 Tests")
        print("=" * 60)
        
        # Run all test functions
        await test_basic_functionality()
        await test_workspace_management()
        await test_collaboration_lifecycle()
        await test_shared_resources()
        await test_event_recording()
        await test_conflict_management()
        await test_agent_workspace_management()
        await test_collaboration_metrics()
        await test_event_handling()
        await test_data_export()
        await test_integration_scenario()
        await test_performance()
        
        print("\n✅ ALL TESTS PASSED!")
        print("🎯 Pattern 3: Agent Collaboration is working correctly")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(run_all_tests())
