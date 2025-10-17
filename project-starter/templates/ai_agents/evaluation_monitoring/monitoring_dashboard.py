"""
Pattern 17: Evaluation & Monitoring - Dashboard
Real-time monitoring dashboard for AI agents
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from evaluation_framework import EvaluationFramework, MetricType, EvaluationLevel

class MonitoringDashboard:
    """
    Real-time monitoring dashboard for AI agents
    Provides visual representation of agent performance
    """
    
    def __init__(self, framework: EvaluationFramework):
        self.framework = framework
        self.update_interval = 5  # seconds
        self.is_running = False
    
    async def start_monitoring(self):
        """Start real-time monitoring"""
        self.is_running = True
        print("🖥️  Monitoring Dashboard Started")
        print("=" * 60)
        
        while self.is_running:
            await self._update_dashboard()
            await asyncio.sleep(self.update_interval)
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.is_running = False
        print("\n🛑 Monitoring Dashboard Stopped")
    
    async def _update_dashboard(self):
        """Update the dashboard display"""
        # Clear screen (simple approach)
        print("\033[2J\033[H", end="")
        
        # Header
        print("🤖 AI Agent Monitoring Dashboard")
        print("=" * 60)
        print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # System Health
        health = self.framework.get_system_health()
        self._display_system_health(health)
        
        # Agent Performance
        self._display_agent_performance()
        
        # Real-time Metrics
        self._display_real_time_metrics()
        
        # Recent Alerts
        self._display_recent_alerts()
        
        print("\n" + "=" * 60)
        print("Press Ctrl+C to stop monitoring")
    
    def _display_system_health(self, health: Dict[str, Any]):
        """Display system health status"""
        print("🏥 System Health")
        print("-" * 30)
        
        status_emoji = {
            "healthy": "✅",
            "warning": "⚠️",
            "degraded": "🔶",
            "critical": "🚨",
            "no_data": "❓",
            "no_recent_data": "⏰"
        }
        
        emoji = status_emoji.get(health["status"], "❓")
        print(f"Status: {emoji} {health['status'].upper()}")
        
        if "health_score" in health:
            print(f"Health Score: {health['health_score']:.1f}/100")
        
        if "total_metrics" in health:
            print(f"Total Metrics: {health['total_metrics']}")
        
        if "recent_metrics" in health:
            print(f"Recent Metrics: {health['recent_metrics']}")
        
        if "active_alerts" in health:
            print(f"Active Alerts: {health['active_alerts']}")
        
        print()
    
    def _display_agent_performance(self):
        """Display agent performance summary"""
        print("📊 Agent Performance")
        print("-" * 30)
        
        # Get all unique agent IDs
        agent_ids = list(set(m.agent_id for m in self.framework.metrics))
        
        if not agent_ids:
            print("No agent data available")
            print()
            return
        
        for agent_id in agent_ids[:5]:  # Show top 5 agents
            summary = self.framework.get_agent_performance_summary(agent_id)
            
            if "error" in summary:
                print(f"Agent {agent_id}: {summary['error']}")
                continue
            
            print(f"Agent: {agent_id}")
            print(f"  Metrics: {summary['total_metrics']}")
            
            # Show key metrics
            if "response_time" in summary["metrics"]:
                rt = summary["metrics"]["response_time"]
                print(f"  Response Time: {rt['mean']:.2f}s (avg)")
            
            if "success_rate" in summary["metrics"]:
                sr = summary["metrics"]["success_rate"]
                print(f"  Success Rate: {sr['mean']:.1%} (avg)")
            
            if "error_rate" in summary["metrics"]:
                er = summary["metrics"]["error_rate"]
                print(f"  Error Rate: {er['mean']:.1%} (avg)")
            
            print()
    
    def _display_real_time_metrics(self):
        """Display real-time metrics"""
        print("⚡ Real-time Metrics")
        print("-" * 30)
        
        rt_metrics = self.framework.get_real_time_metrics()
        
        if not rt_metrics["metrics"]:
            print("No real-time metrics available")
            print()
            return
        
        # Show recent metrics
        for key, metric in list(rt_metrics["metrics"].items())[:10]:
            agent_id, operation, metric_name = key.split("_", 2)
            print(f"{agent_name}: {metric_name} = {metric['current']:.2f}")
        
        print()
    
    def _display_recent_alerts(self):
        """Display recent alerts"""
        print("🚨 Recent Alerts")
        print("-" * 30)
        
        # Get recent evaluation results with alerts
        recent_results = [
            r for r in self.framework.evaluation_results
            if r.timestamp > datetime.now() - timedelta(minutes=10)
            and r.alerts
        ]
        
        if not recent_results:
            print("No recent alerts")
            print()
            return
        
        for result in recent_results[-5:]:  # Show last 5 alerts
            print(f"Agent {result.agent_id} ({result.timestamp.strftime('%H:%M:%S')}):")
            for alert in result.alerts:
                print(f"  - {alert}")
            print()
    
    def generate_report(self, agent_id: str = None) -> str:
        """Generate a detailed performance report"""
        report = []
        report.append("🤖 AI Agent Performance Report")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        if agent_id:
            # Single agent report
            result = self.framework.evaluate_agent(agent_id, level=EvaluationLevel.DEEP)
            report.append(f"Agent: {agent_id}")
            report.append(f"Overall Score: {result.overall_score:.2f}/100")
            report.append("")
            
            report.append("Metric Scores:")
            for metric, score in result.metric_scores.items():
                report.append(f"  {metric}: {score:.2f}")
            report.append("")
            
            report.append("Recommendations:")
            for rec in result.recommendations:
                report.append(f"  - {rec}")
            report.append("")
            
            if result.alerts:
                report.append("Active Alerts:")
                for alert in result.alerts:
                    report.append(f"  - {alert}")
                report.append("")
        else:
            # System-wide report
            health = self.framework.get_system_health()
            report.append(f"System Health: {health['status'].upper()}")
            if "health_score" in health:
                report.append(f"Health Score: {health['health_score']:.1f}/100")
            report.append("")
            
            # Agent summaries
            agent_ids = list(set(m.agent_id for m in self.framework.metrics))
            report.append("Agent Performance Summary:")
            for agent_id in agent_ids:
                summary = self.framework.get_agent_performance_summary(agent_id)
                if "error" not in summary:
                    report.append(f"  {agent_id}: {summary['total_metrics']} metrics")
            report.append("")
        
        return "\n".join(report)
    
    def export_data(self, format: str = "json") -> str:
        """Export monitoring data"""
        if format == "json":
            return json.dumps({
                "timestamp": datetime.now().isoformat(),
                "system_health": self.framework.get_system_health(),
                "real_time_metrics": self.framework.get_real_time_metrics(),
                "evaluation_results": [
                    {
                        "agent_id": r.agent_id,
                        "operation": r.operation,
                        "timestamp": r.timestamp.isoformat(),
                        "overall_score": r.overall_score,
                        "alerts": r.alerts
                    }
                    for r in self.framework.evaluation_results[-10:]  # Last 10 results
                ]
            }, indent=2, default=str)
        else:
            return self.framework.export_metrics(format=format)

# Example usage
async def demo_monitoring_dashboard():
    """Demonstrate the monitoring dashboard"""
    # Create framework and add some test data
    framework = EvaluationFramework()
    
    # Add test metrics
    test_agents = ["agent1", "agent2", "agent3"]
    test_operations = ["process_request", "analyze_data", "generate_response"]
    
    for i in range(20):
        agent_id = test_agents[i % len(test_agents)]
        operation = test_operations[i % len(test_operations)]
        
        # Add various metrics
        framework.add_metric("response_time", 1.0 + (i % 5), MetricType.PERFORMANCE, agent_id, operation)
        framework.add_metric("error_rate", 0.01 + (i % 3) * 0.01, MetricType.RELIABILITY, agent_id, operation)
        framework.add_metric("success_rate", 0.95 + (i % 5) * 0.01, MetricType.QUALITY, agent_id, operation)
        framework.add_metric("throughput", 10 + (i % 10), MetricType.PERFORMANCE, agent_id, operation)
        
        # Simulate some time passing
        await asyncio.sleep(0.1)
    
    # Create and start dashboard
    dashboard = MonitoringDashboard(framework)
    
    print("🎬 Starting Monitoring Dashboard Demo")
    print("This will run for 30 seconds...")
    
    # Run dashboard for 30 seconds
    try:
        await asyncio.wait_for(dashboard.start_monitoring(), timeout=30)
    except asyncio.TimeoutError:
        dashboard.stop_monitoring()
    
    # Generate final report
    print("\n📋 Final Performance Report")
    print("=" * 60)
    report = dashboard.generate_report()
    print(report)

if __name__ == "__main__":
    asyncio.run(demo_monitoring_dashboard())
