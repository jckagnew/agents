"""
Test suite for Pattern 20: Agent Swarming - Coordinated Multi-Agent Behavior
"""

import asyncio
import json
import tempfile
import shutil
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from swarming_framework import (
    SwarmingFramework, SwarmAlgorithm, SwarmRole, SwarmBehavior,
    SwarmStatus, SwarmAgent, Swarm, SwarmEvent, SwarmMetrics
)


async def test_basic_functionality():
    """Test basic swarming framework functionality"""
    print("🧪 Testing Pattern 20: Agent Swarming - Basic Functionality")
    print("=" * 60)
    
    # Create framework with temporary storage
    temp_dir = tempfile.mkdtemp()
    try:
        framework = SwarmingFramework({"storage_path": temp_dir})
        print("✅ Swarming framework created")
        
        # Test swarm creation
        swarm_id = framework.create_swarm(
            "Test Swarm", "Testing swarming capabilities",
            SwarmAlgorithm.FLOCKING, SwarmBehavior.EXPLORATION, "Find optimal solution"
        )
        assert swarm_id is not None
        print("✅ Swarm creation works")
        
        # Test agent addition
        agent_id = framework.add_agent_to_swarm(swarm_id, SwarmRole.WORKER)
        assert agent_id is not None
        print("✅ Agent addition works")
        
        # Test swarm operation start
        success = framework.start_swarm_operation(swarm_id)
        assert success
        print("✅ Swarm operation start works")
        
        # Test metrics
        metrics = framework.get_swarm_metrics()
        assert metrics.total_swarms >= 1
        assert metrics.total_agents >= 1
        print("✅ Metrics work")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Basic swarming tests passed!")


async def test_swarm_algorithms():
    """Test different swarm algorithms"""
    print("\n🧪 Testing Swarm Algorithms")
    print("=" * 30)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = SwarmingFramework({"storage_path": temp_dir})
        
        # Test all algorithms
        algorithms = [
            SwarmAlgorithm.PARTICLE_SWARM_OPTIMIZATION,
            SwarmAlgorithm.ANT_COLONY_OPTIMIZATION,
            SwarmAlgorithm.BEE_ALGORITHM,
            SwarmAlgorithm.FIREFLY_ALGORITHM,
            SwarmAlgorithm.BAT_ALGORITHM,
            SwarmAlgorithm.CUCKOO_SEARCH,
            SwarmAlgorithm.FLOCKING
        ]
        
        for algorithm in algorithms:
            swarm_id = framework.create_swarm(
                f"Test {algorithm.value}", f"Testing {algorithm.value}",
                algorithm, SwarmBehavior.EXPLORATION, "Test objective"
            )
            assert swarm_id is not None
            
            # Add some agents
            for i in range(3):
                agent_id = framework.add_agent_to_swarm(swarm_id, SwarmRole.WORKER)
                assert agent_id is not None
            
            # Test algorithm application
            success = framework.apply_swarm_algorithm(swarm_id)
            assert success
            print(f"✅ {algorithm.value} algorithm works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Swarm algorithms tests passed!")


async def test_swarm_roles():
    """Test different swarm roles"""
    print("\n🧪 Testing Swarm Roles")
    print("=" * 25)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = SwarmingFramework({"storage_path": temp_dir})
        
        # Create test swarm
        swarm_id = framework.create_swarm(
            "Role Test Swarm", "Testing different roles",
            SwarmAlgorithm.FLOCKING, SwarmBehavior.EXPLORATION, "Test roles"
        )
        
        # Test all roles
        roles = [
            SwarmRole.LEADER,
            SwarmRole.FOLLOWER,
            SwarmRole.SCOUT,
            SwarmRole.WORKER,
            SwarmRole.COORDINATOR,
            SwarmRole.OBSERVER,
            SwarmRole.SPECIALIST
        ]
        
        for role in roles:
            agent_id = framework.add_agent_to_swarm(swarm_id, role)
            assert agent_id is not None
            agent = framework.agents[agent_id]
            assert agent.role == role
            print(f"✅ {role.value} role works")
        
        # Test leader assignment
        swarm = framework.swarms[swarm_id]
        assert swarm.leader_id is not None
        print("✅ Leader assignment works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Swarm roles tests passed!")


async def test_swarm_behaviors():
    """Test different swarm behaviors"""
    print("\n🧪 Testing Swarm Behaviors")
    print("=" * 30)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = SwarmingFramework({"storage_path": temp_dir})
        
        # Test all behaviors
        behaviors = [
            SwarmBehavior.EXPLORATION,
            SwarmBehavior.EXPLOITATION,
            SwarmBehavior.CONVERGENCE,
            SwarmBehavior.DIVERGENCE,
            SwarmBehavior.COOPERATION,
            SwarmBehavior.COMPETITION,
            SwarmBehavior.ADAPTATION,
            SwarmBehavior.EMERGENCE
        ]
        
        for behavior in behaviors:
            swarm_id = framework.create_swarm(
                f"Test {behavior.value}", f"Testing {behavior.value}",
                SwarmAlgorithm.FLOCKING, behavior, "Test objective"
            )
            assert swarm_id is not None
            print(f"✅ {behavior.value} behavior works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Swarm behaviors tests passed!")


async def test_agent_communication():
    """Test agent communication"""
    print("\n🧪 Testing Agent Communication")
    print("=" * 35)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = SwarmingFramework({"storage_path": temp_dir})
        
        # Create test swarm
        swarm_id = framework.create_swarm(
            "Communication Test", "Testing agent communication",
            SwarmAlgorithm.FLOCKING, SwarmBehavior.COOPERATION, "Test communication"
        )
        
        # Add agents
        agent1_id = framework.add_agent_to_swarm(swarm_id, SwarmRole.WORKER)
        agent2_id = framework.add_agent_to_swarm(swarm_id, SwarmRole.WORKER)
        
        # Position agents close to each other
        framework.update_agent_position(agent1_id, {"x": 0, "y": 0, "z": 0})
        framework.update_agent_position(agent2_id, {"x": 10, "y": 0, "z": 0})
        
        # Test message sending
        message = {"type": "coordination", "data": "test message"}
        success = framework.send_swarm_message(agent1_id, agent2_id, message)
        assert success
        print("✅ Message sending works")
        
        # Test neighbor finding
        neighbors = framework.find_neighbors(agent1_id)
        assert agent2_id in neighbors
        print("✅ Neighbor finding works")
        
        # Test message counts
        agent1 = framework.agents[agent1_id]
        agent2 = framework.agents[agent2_id]
        assert agent1.messages_sent >= 1
        assert agent2.messages_received >= 1
        print("✅ Message counting works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Agent communication tests passed!")


async def test_position_updates():
    """Test position and velocity updates"""
    print("\n🧪 Testing Position Updates")
    print("=" * 30)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = SwarmingFramework({"storage_path": temp_dir})
        
        # Create test swarm and agent
        swarm_id = framework.create_swarm(
            "Position Test", "Testing position updates",
            SwarmAlgorithm.FLOCKING, SwarmBehavior.EXPLORATION, "Test positions"
        )
        agent_id = framework.add_agent_to_swarm(swarm_id, SwarmRole.WORKER)
        
        # Test position update
        new_position = {"x": 50, "y": 75, "z": 10}
        success = framework.update_agent_position(agent_id, new_position)
        assert success
        
        agent = framework.agents[agent_id]
        assert agent.position == new_position
        print("✅ Position update works")
        
        # Test velocity update
        new_velocity = {"x": 1.5, "y": -2.0, "z": 0.5}
        success = framework.update_agent_position(agent_id, new_position, new_velocity)
        assert success
        
        agent = framework.agents[agent_id]
        assert agent.velocity == new_velocity
        print("✅ Velocity update works")
        
        # Test fitness update
        fitness = 0.85
        success = framework.update_agent_fitness(agent_id, fitness)
        assert success
        
        agent = framework.agents[agent_id]
        assert agent.fitness == fitness
        print("✅ Fitness update works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Position updates tests passed!")


async def test_swarming_persistence():
    """Test swarming data persistence"""
    print("\n🧪 Testing Swarming Persistence")
    print("=" * 35)
    
    temp_dir = tempfile.mkdtemp()
    try:
        # Create framework and add data
        framework1 = SwarmingFramework({"storage_path": temp_dir})
        
        # Add test data
        swarm_id = framework1.create_swarm(
            "Persistence Test", "Testing data persistence",
            SwarmAlgorithm.FLOCKING, SwarmBehavior.EXPLORATION, "Test persistence"
        )
        agent_id = framework1.add_agent_to_swarm(swarm_id, SwarmRole.WORKER)
        framework1.update_agent_fitness(agent_id, 0.75)
        
        # Create new framework instance (should load existing data)
        framework2 = SwarmingFramework({"storage_path": temp_dir})
        
        # Verify data was loaded
        assert swarm_id in framework2.swarms
        assert agent_id in framework2.agents
        print("✅ Swarming persistence works")
        
        # Test stats consistency
        metrics1 = framework1.get_swarm_metrics()
        metrics2 = framework2.get_swarm_metrics()
        assert metrics1.total_swarms == metrics2.total_swarms
        assert metrics1.total_agents == metrics2.total_agents
        print("✅ Stats consistency works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Swarming persistence tests passed!")


async def test_swarm_metrics():
    """Test swarm metrics calculation"""
    print("\n🧪 Testing Swarm Metrics")
    print("=" * 30)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = SwarmingFramework({"storage_path": temp_dir})
        
        # Add test data
        for i in range(3):
            swarm_id = framework.create_swarm(
                f"Test Swarm {i}", f"Testing swarm {i}",
                SwarmAlgorithm.FLOCKING, SwarmBehavior.EXPLORATION, f"Objective {i}"
            )
            
            # Add agents to each swarm
            for j in range(5):
                agent_id = framework.add_agent_to_swarm(swarm_id, SwarmRole.WORKER)
                framework.update_agent_fitness(agent_id, 0.5 + j * 0.1)
        
        # Test metrics
        metrics = framework.get_swarm_metrics()
        
        assert metrics.total_swarms >= 3
        assert metrics.total_agents >= 15
        assert metrics.average_swarm_size >= 5.0
        assert 0 <= metrics.average_fitness <= 1
        assert 0 <= metrics.best_fitness <= 1
        assert 0 <= metrics.convergence_rate <= 1
        assert 0 <= metrics.communication_efficiency <= 1
        assert 0 <= metrics.coordination_effectiveness <= 1
        assert metrics.emergent_behaviors >= 0
        print("✅ Swarm metrics work")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Swarm metrics tests passed!")


async def test_swarming_control():
    """Test swarming framework control"""
    print("\n🧪 Testing Swarming Control")
    print("=" * 30)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = SwarmingFramework({"storage_path": temp_dir})
        
        # Test start/stop
        framework.start_swarming_processing()
        assert framework.swarming_processor_running
        print("✅ Swarming start works")
        
        framework.stop_swarming_processing()
        assert not framework.swarming_processor_running
        print("✅ Swarming stop works")
        
        # Test queue
        framework.swarming_queue.append({"type": "test_task"})
        assert len(framework.swarming_queue) >= 1  # May be processed by background thread
        print("✅ Swarming queue works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Swarming control tests passed!")


async def test_data_export():
    """Test data export functionality"""
    print("\n🧪 Testing Data Export")
    print("=" * 25)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = SwarmingFramework({"storage_path": temp_dir})
        
        # Add some test data
        swarm_id = framework.create_swarm(
            "Export Test", "Testing data export",
            SwarmAlgorithm.FLOCKING, SwarmBehavior.EXPLORATION, "Test export"
        )
        agent_id = framework.add_agent_to_swarm(swarm_id, SwarmRole.WORKER)
        framework.update_agent_fitness(agent_id, 0.8)
        
        # Test JSON export
        json_export = framework.export_swarming_data(format="json")
        assert "agents" in json_export
        assert "swarms" in json_export
        assert "events" in json_export
        assert "metrics" in json_export
        print("✅ JSON export works")
        
        # Test dict export
        dict_export = framework.export_swarming_data(format="dict")
        assert "agents" in dict_export
        assert "swarms" in dict_export
        assert "events" in dict_export
        assert "metrics" in dict_export
        print("✅ Dict export works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Data export tests passed!")


async def test_data_clear():
    """Test data clearing functionality"""
    print("\n🧪 Testing Data Clear")
    print("=" * 25)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = SwarmingFramework({"storage_path": temp_dir})
        
        # Add test data
        swarm_id = framework.create_swarm(
            "Clear Test", "Testing data clearing",
            SwarmAlgorithm.FLOCKING, SwarmBehavior.EXPLORATION, "Test clear"
        )
        agent_id = framework.add_agent_to_swarm(swarm_id, SwarmRole.WORKER)
        
        # Verify data exists
        assert len(framework.swarms) >= 1
        assert len(framework.agents) >= 1
        print("✅ Data added successfully")
        
        # Clear data
        framework.clear_swarming_data()
        
        # Verify data is cleared
        assert len(framework.swarms) == 0
        assert len(framework.agents) == 0
        print("✅ Data cleared successfully")
        
        # Test stats after clear
        metrics = framework.get_swarm_metrics()
        assert metrics.total_swarms == 0
        assert metrics.total_agents == 0
        print("✅ Stats reset after clear")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Data clear tests passed!")


async def test_integration_scenario():
    """Test an end-to-end integration scenario"""
    print("\n🧪 Testing Integration Scenario")
    print("=" * 35)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = SwarmingFramework({"storage_path": temp_dir})
        
        print("🐝 Multi-Agent Swarm Optimization Scenario")
        
        # Create optimization swarm
        swarm_id = framework.create_swarm(
            "Optimization Swarm",
            "Swarm of agents optimizing a function",
            SwarmAlgorithm.PARTICLE_SWARM_OPTIMIZATION,
            SwarmBehavior.EXPLOITATION,
            "Find global optimum of function f(x,y) = x² + y²"
        )
        
        print(f"✅ Created optimization swarm: {swarm_id}")
        
        # Add diverse agents
        roles = [SwarmRole.LEADER, SwarmRole.SCOUT, SwarmRole.WORKER, SwarmRole.COORDINATOR]
        for i, role in enumerate(roles):
            agent_id = framework.add_agent_to_swarm(swarm_id, role)
            # Set different initial positions
            position = {"x": i * 10, "y": i * 5, "z": 0}
            framework.update_agent_position(agent_id, position)
            # Set different fitness values
            framework.update_agent_fitness(agent_id, 0.3 + i * 0.2)
            print(f"✅ Added {role.value} agent: {agent_id}")
        
        # Start swarm operation
        success = framework.start_swarm_operation(swarm_id)
        print(f"✅ Started swarm operation: {success}")
        
        # Run several iterations
        for iteration in range(5):
            framework.apply_swarm_algorithm(swarm_id)
            print(f"✅ Iteration {iteration + 1} completed")
        
        # Test communication
        agents = [aid for aid in framework.swarms[swarm_id].agents if aid in framework.agents]
        if len(agents) >= 2:
            message = {"type": "coordination", "iteration": 5, "best_fitness": 0.9}
            success = framework.send_swarm_message(agents[0], agents[1], message)
            print(f"✅ Agent communication: {success}")
        
        # Test neighbor finding
        if agents:
            neighbors = framework.find_neighbors(agents[0])
            print(f"✅ Found {len(neighbors)} neighbors for agent {agents[0]}")
        
        # Check final state
        metrics = framework.get_swarm_metrics()
        print(f"✅ Final stats: {metrics.total_swarms} swarms, {metrics.total_agents} agents")
        print(f"✅ Average fitness: {metrics.average_fitness:.3f}, Best fitness: {metrics.best_fitness:.3f}")
        print(f"✅ Convergence rate: {metrics.convergence_rate:.3f}")
        
        # Test data export
        export_data = framework.export_swarming_data(format="dict")
        assert "agents" in export_data
        assert "swarms" in export_data
        assert "events" in export_data
        assert "metrics" in export_data
        print("✅ Data export successful")
        
        print("✅ Complete swarming scenario successful")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Integration scenario tests passed!")


async def main():
    """Run all tests"""
    print("🚀 Starting Pattern 20: Agent Swarming Tests")
    print("=" * 60)
    
    await test_basic_functionality()
    await test_swarm_algorithms()
    await test_swarm_roles()
    await test_swarm_behaviors()
    await test_agent_communication()
    await test_position_updates()
    await test_swarming_persistence()
    await test_swarm_metrics()
    await test_swarming_control()
    await test_data_export()
    await test_data_clear()
    await test_integration_scenario()
    
    print("\n🎉 All Pattern 20: Agent Swarming tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

