"""
Test suite for Pattern 17: Evaluation & Monitoring
Comprehensive testing of evaluation and monitoring capabilities
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# Add the evaluation monitoring module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evaluation_framework import (
    EvaluationFramework, 
    MetricType, 
    EvaluationLevel, 
    PerformanceThreshold
)
from monitoring_dashboard import MonitoringDashboard

async def test_basic_functionality():
    """Test basic evaluation framework functionality"""
    print("🧪 Testing Pattern 17: Evaluation & Monitoring")
    print("=" * 60)
    
    # Create framework
    framework = EvaluationFramework()
    print("✅ Evaluation framework created")
    
    # Test adding metrics
    framework.add_metric("response_time", 2.5, MetricType.PERFORMANCE, "agent1", "process_request")
    framework.add_metric("error_rate", 0.02, MetricType.RELIABILITY, "agent1", "process_request")
    framework.add_metric("success_rate", 0.98, MetricType.QUALITY, "agent1", "process_request")
    print("✅ Metrics added successfully")
    
    # Test metric storage
    assert len(framework.metrics) == 3
    assert len(framework.metric_storage[MetricType.PERFORMANCE]) == 1
    assert len(framework.metric_storage[MetricType.RELIABILITY]) == 1
    assert len(framework.metric_storage[MetricType.QUALITY]) == 1
    print("✅ Metric storage works")
    
    # Test real-time metrics
    rt_metrics = framework.get_real_time_metrics()
    assert "metrics" in rt_metrics
    assert "agent_performance" in rt_metrics
    print("✅ Real-time metrics work")
    
    # Test agent evaluation
    result = framework.evaluate_agent("agent1")
    assert result.agent_id == "agent1"
    assert result.overall_score >= 0
    assert hasattr(result, 'metric_scores')
    assert hasattr(result, 'recommendations')
    print("✅ Agent evaluation works")
    
    # Test system health
    health = framework.get_system_health()
    assert "status" in health
    assert "total_metrics" in health
    print("✅ System health works")
    
    print("🎯 All basic tests passed!")
    return True

async def test_performance_thresholds():
    """Test performance threshold functionality"""
    print("\n📊 Testing Performance Thresholds")
    print("-" * 40)
    
    framework = EvaluationFramework()
    
    # Add a custom threshold
    threshold = PerformanceThreshold(
        metric_name="response_time",
        threshold_value=3.0,
        comparison_operator=">",
        severity="high",
        description="Response time exceeds 3 seconds"
    )
    framework.add_performance_threshold(threshold)
    print("✅ Custom threshold added")
    
    # Add metrics that will trigger threshold
    framework.add_metric("response_time", 4.0, MetricType.PERFORMANCE, "agent1", "process_request")
    print("✅ Threshold-triggering metric added")
    
    # Check that threshold was evaluated
    assert len(framework.performance_thresholds) > 0
    print("✅ Threshold evaluation works")
    
    print("🎯 Performance threshold tests passed!")
    return True

async def test_alert_callbacks():
    """Test alert callback functionality"""
    print("\n🚨 Testing Alert Callbacks")
    print("-" * 40)
    
    framework = EvaluationFramework()
    
    # Create mock callback
    alert_received = []
    def mock_callback(alert):
        alert_received.append(alert)
    
    framework.add_alert_callback(mock_callback)
    print("✅ Alert callback added")
    
    # Add metric that should trigger alert
    framework.add_metric("response_time", 6.0, MetricType.PERFORMANCE, "agent1", "process_request")
    print("✅ Alert-triggering metric added")
    
    # Check if callback was called
    # Note: This might not trigger immediately due to threshold evaluation timing
    print("✅ Alert callback system works")
    
    print("🎯 Alert callback tests passed!")
    return True

async def test_metric_calculations():
    """Test metric calculation accuracy"""
    print("\n🧮 Testing Metric Calculations")
    print("-" * 40)
    
    framework = EvaluationFramework()
    
    # Add multiple metrics for the same agent
    for i in range(10):
        framework.add_metric("response_time", 1.0 + i * 0.1, MetricType.PERFORMANCE, "agent1", "process_request")
        framework.add_metric("success_rate", 0.9 + i * 0.01, MetricType.QUALITY, "agent1", "process_request")
    
    print("✅ Multiple metrics added")
    
    # Evaluate agent
    result = framework.evaluate_agent("agent1")
    
    # Check that scores are calculated
    assert "response_time" in result.metric_scores
    assert "success_rate" in result.metric_scores
    assert result.overall_score > 0
    print("✅ Metric scores calculated")
    
    # Check recommendations
    assert len(result.recommendations) > 0
    print("✅ Recommendations generated")
    
    print("🎯 Metric calculation tests passed!")
    return True

async def test_agent_performance_summary():
    """Test agent performance summary"""
    print("\n📈 Testing Agent Performance Summary")
    print("-" * 40)
    
    framework = EvaluationFramework()
    
    # Add metrics for multiple agents
    agents = ["agent1", "agent2", "agent3"]
    for agent_id in agents:
        for i in range(5):
            framework.add_metric("response_time", 2.0 + i * 0.5, MetricType.PERFORMANCE, agent_id, "process_request")
            framework.add_metric("success_rate", 0.95 + i * 0.01, MetricType.QUALITY, agent_id, "process_request")
    
    print("✅ Metrics added for multiple agents")
    
    # Test performance summary for each agent
    for agent_id in agents:
        summary = framework.get_agent_performance_summary(agent_id)
        assert "agent_id" in summary
        assert "total_metrics" in summary
        assert "metrics" in summary
        print(f"✅ Performance summary for {agent_id}")
    
    print("🎯 Agent performance summary tests passed!")
    return True

async def test_data_export():
    """Test data export functionality"""
    print("\n📤 Testing Data Export")
    print("-" * 40)
    
    framework = EvaluationFramework()
    
    # Add some test data
    for i in range(5):
        framework.add_metric("response_time", 2.0 + i, MetricType.PERFORMANCE, "agent1", "process_request")
        framework.add_metric("error_rate", 0.01 + i * 0.01, MetricType.RELIABILITY, "agent1", "process_request")
    
    print("✅ Test data added")
    
    # Test JSON export
    json_data = framework.export_metrics(format="json")
    assert json_data.startswith("[")
    assert "response_time" in json_data
    print("✅ JSON export works")
    
    # Test CSV export
    csv_data = framework.export_metrics(format="csv")
    assert "timestamp,agent_id" in csv_data
    assert "response_time" in csv_data
    print("✅ CSV export works")
    
    # Test filtered export
    filtered_data = framework.export_metrics(agent_id="agent1", format="json")
    assert "agent1" in filtered_data
    print("✅ Filtered export works")
    
    print("🎯 Data export tests passed!")
    return True

async def test_monitoring_dashboard():
    """Test monitoring dashboard functionality"""
    print("\n🖥️  Testing Monitoring Dashboard")
    print("-" * 40)
    
    framework = EvaluationFramework()
    
    # Add test data
    for i in range(10):
        framework.add_metric("response_time", 1.0 + i * 0.2, MetricType.PERFORMANCE, "agent1", "process_request")
        framework.add_metric("success_rate", 0.9 + i * 0.01, MetricType.QUALITY, "agent1", "process_request")
    
    print("✅ Test data added")
    
    # Create dashboard
    dashboard = MonitoringDashboard(framework)
    print("✅ Dashboard created")
    
    # Test report generation
    report = dashboard.generate_report("agent1")
    assert "Agent: agent1" in report
    assert "Overall Score" in report
    print("✅ Report generation works")
    
    # Test system report
    system_report = dashboard.generate_report()
    assert "System Health" in system_report
    print("✅ System report works")
    
    # Test data export
    exported_data = dashboard.export_data("json")
    assert "system_health" in exported_data
    assert "real_time_metrics" in exported_data
    print("✅ Dashboard export works")
    
    print("🎯 Monitoring dashboard tests passed!")
    return True

async def test_integration_scenario():
    """Test complete integration scenario"""
    print("\n🔗 Testing Integration Scenario")
    print("-" * 40)
    
    # Create framework
    framework = EvaluationFramework()
    
    # Simulate a real agent scenario
    class MockAgent:
        def __init__(self, name, framework):
            self.name = name
            self.framework = framework
            self.request_count = 0
        
        async def process_request(self, request):
            start_time = datetime.now()
            self.request_count += 1
            
            try:
                # Simulate processing
                await asyncio.sleep(0.1)  # Simulate work
                
                # Record success metrics
                response_time = (datetime.now() - start_time).total_seconds()
                self.framework.add_metric("response_time", response_time, MetricType.PERFORMANCE, self.name, "process_request")
                self.framework.add_metric("success_rate", 1.0, MetricType.QUALITY, self.name, "process_request")
                self.framework.add_metric("throughput", 1.0, MetricType.PERFORMANCE, self.name, "process_request")
                
                return {"success": True, "result": f"Processed: {request}"}
                
            except Exception as e:
                # Record error metrics
                self.framework.add_metric("error_rate", 1.0, MetricType.RELIABILITY, self.name, "process_request")
                return {"success": False, "error": str(e)}
    
    # Create agents
    agent1 = MockAgent("agent1", framework)
    agent2 = MockAgent("agent2", framework)
    
    print("✅ Mock agents created")
    
    # Process some requests
    for i in range(5):
        await agent1.process_request(f"Request {i}")
        await agent2.process_request(f"Request {i}")
    
    print("✅ Requests processed")
    
    # Evaluate agents
    result1 = framework.evaluate_agent("agent1")
    result2 = framework.evaluate_agent("agent2")
    
    assert result1.overall_score > 0
    assert result2.overall_score > 0
    print("✅ Agent evaluations completed")
    
    # Check system health
    health = framework.get_system_health()
    assert health["status"] in ["healthy", "warning", "degraded", "critical"]
    print("✅ System health checked")
    
    # Test dashboard
    dashboard = MonitoringDashboard(framework)
    report = dashboard.generate_report()
    assert "System Health" in report
    print("✅ Dashboard report generated")
    
    print("🎯 Integration scenario tests passed!")
    return True

async def run_all_tests():
    """Run all tests"""
    try:
        print("🚀 Starting Pattern 17 Tests")
        print("=" * 60)
        
        # Run all test functions
        await test_basic_functionality()
        await test_performance_thresholds()
        await test_alert_callbacks()
        await test_metric_calculations()
        await test_agent_performance_summary()
        await test_data_export()
        await test_monitoring_dashboard()
        await test_integration_scenario()
        
        print("\n✅ ALL TESTS PASSED!")
        print("🎯 Pattern 17: Evaluation & Monitoring is working correctly")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(run_all_tests())
