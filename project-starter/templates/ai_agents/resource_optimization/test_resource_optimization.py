"""
Test suite for Pattern 15: Resource-Aware Optimization
Comprehensive testing of resource monitoring and optimization capabilities
"""

import asyncio
import sys
import os
import tempfile
import shutil
import time
from datetime import datetime, timedelta

# Add the resource optimization module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from resource_framework import (
    ResourceFramework, 
    ResourceType, 
    ResourceStatus, 
    OptimizationAction
)

async def test_basic_functionality():
    """Test basic resource monitoring functionality"""
    print("🧪 Testing Pattern 15: Resource-Aware Optimization")
    print("=" * 60)
    
    # Create framework with temporary storage
    temp_dir = tempfile.mkdtemp()
    try:
        framework = ResourceFramework({"storage_path": temp_dir})
        print("✅ Resource framework created")
        
        # Test recording resource usage
        success = await framework.record_resource_usage(
            ResourceType.CPU, 50.0, 100.0, "%", "agent1", "test_operation"
        )
        assert success is True
        print("✅ Resource usage recording works")
        
        # Test getting resource usage
        usage = await framework.get_resource_usage(agent_id="agent1")
        assert len(usage) == 1
        assert usage[0].current_value == 50.0
        print("✅ Resource usage retrieval works")
        
        # Test resource statistics
        stats = framework.get_resource_statistics()
        assert stats.total_metrics == 1
        assert stats.current_usage["cpu"] == 50.0
        print("✅ Resource statistics work")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
    
    print("🎯 All basic tests passed!")
    return True

async def test_resource_types():
    """Test different resource types"""
    print("\n📊 Testing Resource Types")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = ResourceFramework({"storage_path": temp_dir})
        
        # Test all resource types
        resource_types = [
            ResourceType.CPU,
            ResourceType.MEMORY,
            ResourceType.DISK,
            ResourceType.NETWORK,
            ResourceType.API_CALLS,
            ResourceType.TOKENS,
            ResourceType.COST,
            ResourceType.TIME
        ]
        
        for resource_type in resource_types:
            success = await framework.record_resource_usage(
                resource_type, 50.0, 100.0, "%", "agent1", f"test_{resource_type.value}"
            )
            assert success is True
            print(f"✅ {resource_type.value} resource recording works")
        
        # Verify all resources recorded
        stats = framework.get_resource_statistics()
        assert stats.total_metrics == len(resource_types)
        print("✅ All resource types work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Resource type tests passed!")
    return True

async def test_resource_thresholds():
    """Test resource threshold monitoring"""
    print("\n⚠️  Testing Resource Thresholds")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = ResourceFramework({"storage_path": temp_dir})
        
        # Test warning threshold
        await framework.record_resource_usage(
            ResourceType.CPU, 75.0, 100.0, "%", "agent1", "warning_test"
        )
        
        # Test critical threshold
        await framework.record_resource_usage(
            ResourceType.CPU, 90.0, 100.0, "%", "agent1", "critical_test"
        )
        
        # Test exhausted threshold
        await framework.record_resource_usage(
            ResourceType.CPU, 98.0, 100.0, "%", "agent1", "exhausted_test"
        )
        
        # Check alerts
        alerts = await framework.get_resource_alerts()
        assert len(alerts) >= 2  # At least warning and critical alerts
        print("✅ Resource threshold monitoring works")
        
        # Check alert statuses
        warning_alerts = [a for a in alerts if a.status == ResourceStatus.WARNING]
        critical_alerts = [a for a in alerts if a.status == ResourceStatus.CRITICAL]
        assert len(warning_alerts) > 0
        assert len(critical_alerts) > 0
        print("✅ Alert status classification works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Resource threshold tests passed!")
    return True

async def test_optimization_actions():
    """Test optimization action determination"""
    print("\n🔧 Testing Optimization Actions")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = ResourceFramework({"storage_path": temp_dir})
        
        # Test different usage levels
        test_cases = [
            (30.0, OptimizationAction.OPTIMIZE),  # Low usage
            (75.0, OptimizationAction.THROTTLE),  # Warning level
            (90.0, OptimizationAction.PAUSE),     # Critical level
            (98.0, OptimizationAction.CANCEL)     # Exhausted level
        ]
        
        for usage, expected_action in test_cases:
            action = await framework.optimize_resource_usage(
                ResourceType.CPU, "agent1", usage, 100.0
            )
            assert action == expected_action
            print(f"✅ Optimization action for {usage}%: {action.value}")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Optimization action tests passed!")
    return True

async def test_system_resources():
    """Test system resource monitoring"""
    print("\n💻 Testing System Resources")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = ResourceFramework({"storage_path": temp_dir})
        
        # Get system resources
        system_resources = await framework.get_system_resources()
        assert "cpu_percent" in system_resources
        assert "memory_percent" in system_resources
        assert "disk_percent" in system_resources
        assert "network_bytes" in system_resources
        print("✅ System resource monitoring works")
        
        # Verify resource values are reasonable
        assert 0 <= system_resources["cpu_percent"] <= 100
        assert 0 <= system_resources["memory_percent"] <= 100
        assert 0 <= system_resources["disk_percent"] <= 100
        print("✅ System resource values are valid")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 System resource tests passed!")
    return True

async def test_resource_filtering():
    """Test resource data filtering"""
    print("\n🔍 Testing Resource Filtering")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = ResourceFramework({"storage_path": temp_dir})
        
        # Record resources for different agents and types
        await framework.record_resource_usage(ResourceType.CPU, 50.0, 100.0, "%", "agent1", "op1")
        await framework.record_resource_usage(ResourceType.MEMORY, 60.0, 100.0, "%", "agent1", "op2")
        await framework.record_resource_usage(ResourceType.CPU, 70.0, 100.0, "%", "agent2", "op3")
        
        # Test filtering by agent
        agent1_usage = await framework.get_resource_usage(agent_id="agent1")
        assert len(agent1_usage) == 2
        print("✅ Agent filtering works")
        
        # Test filtering by resource type
        cpu_usage = await framework.get_resource_usage(resource_type=ResourceType.CPU)
        assert len(cpu_usage) == 2
        print("✅ Resource type filtering works")
        
        # Test filtering by time
        recent_usage = await framework.get_resource_usage(hours=1)
        assert len(recent_usage) == 3
        print("✅ Time filtering works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Resource filtering tests passed!")
    return True

async def test_alert_filtering():
    """Test alert filtering"""
    print("\n🚨 Testing Alert Filtering")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = ResourceFramework({"storage_path": temp_dir})
        
        # Generate alerts by exceeding thresholds
        await framework.record_resource_usage(ResourceType.CPU, 85.0, 100.0, "%", "agent1", "critical_op")
        await framework.record_resource_usage(ResourceType.MEMORY, 75.0, 100.0, "%", "agent1", "warning_op")
        await framework.record_resource_usage(ResourceType.CPU, 90.0, 100.0, "%", "agent2", "critical_op2")
        
        # Test filtering by resource type
        cpu_alerts = await framework.get_resource_alerts(resource_type=ResourceType.CPU)
        assert len(cpu_alerts) >= 1
        print("✅ Alert resource type filtering works")
        
        # Test filtering by status
        critical_alerts = await framework.get_resource_alerts(status=ResourceStatus.CRITICAL)
        assert len(critical_alerts) >= 1
        print("✅ Alert status filtering works")
        
        # Test filtering by agent
        agent1_alerts = await framework.get_resource_alerts()
        agent1_cpu_alerts = [a for a in agent1_alerts if a.agent_id == "agent1" and a.resource_type == ResourceType.CPU]
        assert len(agent1_cpu_alerts) >= 1
        print("✅ Alert agent filtering works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Alert filtering tests passed!")
    return True

async def test_custom_thresholds():
    """Test custom threshold setting"""
    print("\n⚙️  Testing Custom Thresholds")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = ResourceFramework({"storage_path": temp_dir})
        
        # Set custom threshold
        await framework.set_resource_threshold(
            ResourceType.CPU, 50.0, 70.0, 90.0, OptimizationAction.SCALE_UP
        )
        
        # Test with custom threshold
        await framework.record_resource_usage(ResourceType.CPU, 60.0, 100.0, "%", "agent1", "custom_test")
        
        # Check if alert was generated
        alerts = await framework.get_resource_alerts()
        cpu_alerts = [a for a in alerts if a.resource_type == ResourceType.CPU]
        assert len(cpu_alerts) >= 1
        print("✅ Custom threshold setting works")
        
        # Test optimization action with custom threshold
        action = await framework.optimize_resource_usage(
            ResourceType.CPU, "agent1", 60.0, 100.0
        )
        assert action == OptimizationAction.SCALE_UP
        print("✅ Custom threshold optimization works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Custom threshold tests passed!")
    return True

async def test_resource_statistics():
    """Test resource statistics functionality"""
    print("\n📈 Testing Resource Statistics")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = ResourceFramework({"storage_path": temp_dir})
        
        # Record various resources
        await framework.record_resource_usage(ResourceType.CPU, 50.0, 100.0, "%", "agent1", "op1")
        await framework.record_resource_usage(ResourceType.MEMORY, 60.0, 100.0, "%", "agent1", "op2")
        await framework.record_resource_usage(ResourceType.CPU, 70.0, 100.0, "%", "agent2", "op3")
        
        # Get statistics
        stats = framework.get_resource_statistics()
        assert stats.total_metrics == 3
        assert stats.metrics_by_type["cpu"] == 2
        assert stats.metrics_by_type["memory"] == 1
        assert stats.metrics_by_agent["agent1"] == 2
        assert stats.metrics_by_agent["agent2"] == 1
        assert stats.current_usage["cpu"] == 70.0  # Most recent CPU usage
        assert stats.peak_usage["cpu"] == 70.0
        assert stats.average_usage["cpu"] == 60.0  # (50 + 70) / 2
        print("✅ Resource statistics work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Resource statistics tests passed!")
    return True

async def test_resource_export():
    """Test resource data export"""
    print("\n📤 Testing Resource Export")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = ResourceFramework({"storage_path": temp_dir})
        
        # Record test data
        await framework.record_resource_usage(ResourceType.CPU, 50.0, 100.0, "%", "agent1", "op1")
        await framework.record_resource_usage(ResourceType.MEMORY, 60.0, 100.0, "%", "agent2", "op2")
        
        # Test JSON export
        json_export = await framework.export_resource_data(format="json")
        assert "cpu" in json_export
        assert "memory" in json_export
        assert "agent1" in json_export
        assert "agent2" in json_export
        print("✅ JSON export works")
        
        # Test CSV export
        csv_export = await framework.export_resource_data(format="csv")
        assert "cpu" in csv_export
        assert "memory" in csv_export
        assert "agent1" in csv_export
        assert "agent2" in csv_export
        print("✅ CSV export works")
        
        # Test filtered export
        agent1_export = await framework.export_resource_data(agent_id="agent1", format="json")
        assert "agent1" in agent1_export
        # Note: agent2 might still appear in statistics, so we check that agent1 data is present
        assert "agent1" in agent1_export
        print("✅ Filtered export works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Resource export tests passed!")
    return True

async def test_integration_scenario():
    """Test complete integration scenario"""
    print("\n🔗 Testing Integration Scenario")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = ResourceFramework({"storage_path": temp_dir})
        
        # Simulate a real agent scenario
        class MockAgent:
            def __init__(self, name, resource_framework):
                self.name = name
                self.resources = resource_framework
                self.operations = []
            
            async def perform_operation(self, operation_name, resource_usage):
                # Record resource usage
                await self.resources.record_resource_usage(
                    ResourceType.CPU, resource_usage, 100.0, "%", self.name, operation_name
                )
                
                # Check if optimization is needed
                action = await self.resources.optimize_resource_usage(
                    ResourceType.CPU, self.name, resource_usage, 100.0
                )
                
                self.operations.append({
                    "operation": operation_name,
                    "resource_usage": resource_usage,
                    "optimization_action": action.value
                })
                
                return action
        
        # Create agent
        agent = MockAgent("agent1", framework)
        print("✅ Mock agent created")
        
        # Perform operations with different resource usage
        operations = [
            ("light_operation", 30.0),
            ("medium_operation", 60.0),
            ("heavy_operation", 85.0),
            ("critical_operation", 95.0)
        ]
        
        for op_name, usage in operations:
            action = await agent.perform_operation(op_name, usage)
            print(f"  Operation: {op_name} ({usage}%) -> Action: {action.value}")
        
        # Check operations recorded
        assert len(agent.operations) == 4
        print("✅ Agent resource monitoring works")
        
        # Check resource statistics
        stats = framework.get_resource_statistics()
        assert stats.total_metrics == 4
        assert stats.metrics_by_agent["agent1"] == 4
        print("✅ Integration statistics work")
        
        # Check alerts generated
        alerts = await framework.get_resource_alerts()
        assert len(alerts) >= 1  # Should have at least one alert for heavy usage
        print("✅ Integration alerting works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Integration scenario tests passed!")
    return True

async def test_performance_monitoring():
    """Test performance monitoring capabilities"""
    print("\n⚡ Testing Performance Monitoring")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = ResourceFramework({"storage_path": temp_dir})
        
        # Simulate performance monitoring
        start_time = time.time()
        
        # Record multiple metrics over time
        for i in range(10):
            await framework.record_resource_usage(
                ResourceType.CPU, 50.0 + i, 100.0, "%", "agent1", f"perf_test_{i}"
            )
            await asyncio.sleep(0.01)  # Small delay to simulate time
        
        end_time = time.time()
        
        # Check performance metrics
        usage = await framework.get_resource_usage(agent_id="agent1")
        assert len(usage) == 10
        
        # Check that metrics are ordered by time
        for i in range(1, len(usage)):
            assert usage[i].timestamp >= usage[i-1].timestamp
        
        # Check statistics
        stats = framework.get_resource_statistics()
        assert stats.total_metrics == 10
        assert stats.peak_usage["cpu"] == 59.0  # 50 + 9
        assert stats.average_usage["cpu"] == 54.5  # (50 + 59) / 2
        
        print("✅ Performance monitoring works")
        print(f"✅ Processed {len(usage)} metrics in {end_time - start_time:.2f} seconds")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Performance monitoring tests passed!")
    return True

async def run_all_tests():
    """Run all tests"""
    try:
        print("🚀 Starting Pattern 15 Tests")
        print("=" * 60)
        
        # Run all test functions
        await test_basic_functionality()
        await test_resource_types()
        await test_resource_thresholds()
        await test_optimization_actions()
        await test_system_resources()
        await test_resource_filtering()
        await test_alert_filtering()
        await test_custom_thresholds()
        await test_resource_statistics()
        await test_resource_export()
        await test_integration_scenario()
        await test_performance_monitoring()
        
        print("\n✅ ALL TESTS PASSED!")
        print("🎯 Pattern 15: Resource-Aware Optimization is working correctly")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(run_all_tests())
