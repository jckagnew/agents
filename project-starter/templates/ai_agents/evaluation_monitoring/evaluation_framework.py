"""
Pattern 17: Evaluation & Monitoring
Comprehensive evaluation and monitoring system for AI agents
"""

import logging
import time
import asyncio
import json
from typing import Dict, List, Optional, Any, Callable, Union
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of metrics to track"""
    PERFORMANCE = "performance"      # Speed, throughput, latency
    QUALITY = "quality"             # Accuracy, relevance, correctness
    RELIABILITY = "reliability"     # Uptime, error rates, stability
    USAGE = "usage"                 # Request counts, user engagement
    COST = "cost"                   # API costs, resource usage
    CUSTOM = "custom"               # Custom business metrics

class EvaluationLevel(Enum):
    """Levels of evaluation detail"""
    BASIC = "basic"                 # High-level metrics only
    DETAILED = "detailed"           # Comprehensive metrics
    DEEP = "deep"                   # Full analysis with insights

@dataclass
class Metric:
    """Individual metric data point"""
    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime
    agent_id: str
    operation: str
    metadata: Dict[str, Any] = None
    tags: Dict[str, str] = None

@dataclass
class EvaluationResult:
    """Result of an evaluation"""
    agent_id: str
    operation: str
    timestamp: datetime
    overall_score: float
    metric_scores: Dict[str, float]
    recommendations: List[str]
    alerts: List[str]
    metadata: Dict[str, Any] = None

@dataclass
class PerformanceThreshold:
    """Performance threshold for alerting"""
    metric_name: str
    threshold_value: float
    comparison_operator: str  # ">", "<", ">=", "<=", "==", "!="
    severity: str  # "low", "medium", "high", "critical"
    description: str

class EvaluationFramework:
    """
    Comprehensive evaluation and monitoring framework for AI agents
    Implements Pattern 17 with detailed metrics, evaluation, and monitoring
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.metrics: List[Metric] = []
        self.evaluation_results: List[EvaluationResult] = []
        self.performance_thresholds: List[PerformanceThreshold] = []
        self.alert_callbacks: List[Callable] = []
        
        # Metric storage by type
        self.metric_storage: Dict[MetricType, deque] = {
            metric_type: deque(maxlen=10000) for metric_type in MetricType
        }
        
        # Real-time monitoring
        self.real_time_metrics: Dict[str, Any] = {}
        self.agent_performance: Dict[str, Dict[str, Any]] = defaultdict(dict)
        
        # Initialize default thresholds
        self._initialize_default_thresholds()
    
    def _initialize_default_thresholds(self):
        """Initialize default performance thresholds"""
        self.performance_thresholds = [
            PerformanceThreshold(
                metric_name="response_time",
                threshold_value=5.0,
                comparison_operator=">",
                severity="medium",
                description="Response time exceeds 5 seconds"
            ),
            PerformanceThreshold(
                metric_name="error_rate",
                threshold_value=0.05,
                comparison_operator=">",
                severity="high",
                description="Error rate exceeds 5%"
            ),
            PerformanceThreshold(
                metric_name="success_rate",
                threshold_value=0.95,
                comparison_operator="<",
                severity="high",
                description="Success rate below 95%"
            ),
            PerformanceThreshold(
                metric_name="throughput",
                threshold_value=10.0,
                comparison_operator="<",
                severity="medium",
                description="Throughput below 10 requests/minute"
            )
        ]
    
    def add_metric(self, 
                   name: str, 
                   value: float, 
                   metric_type: MetricType,
                   agent_id: str,
                   operation: str,
                   metadata: Dict[str, Any] = None,
                   tags: Dict[str, str] = None):
        """Add a new metric data point"""
        metric = Metric(
            name=name,
            value=value,
            metric_type=metric_type,
            timestamp=datetime.now(),
            agent_id=agent_id,
            operation=operation,
            metadata=metadata or {},
            tags=tags or {}
        )
        
        self.metrics.append(metric)
        self.metric_storage[metric_type].append(metric)
        
        # Update real-time metrics
        self._update_real_time_metrics(metric)
        
        # Check thresholds
        self._check_thresholds(metric)
        
        logger.debug(f"Added metric: {name}={value} for {agent_id}")
    
    def _update_real_time_metrics(self, metric: Metric):
        """Update real-time metrics for monitoring"""
        key = f"{metric.agent_id}_{metric.operation}_{metric.name}"
        
        if key not in self.real_time_metrics:
            self.real_time_metrics[key] = {
                "current": metric.value,
                "min": metric.value,
                "max": metric.value,
                "count": 1,
                "sum": metric.value,
                "last_updated": metric.timestamp
            }
        else:
            rt_metric = self.real_time_metrics[key]
            rt_metric["current"] = metric.value
            rt_metric["min"] = min(rt_metric["min"], metric.value)
            rt_metric["max"] = max(rt_metric["max"], metric.value)
            rt_metric["count"] += 1
            rt_metric["sum"] += metric.value
            rt_metric["last_updated"] = metric.timestamp
        
        # Update agent performance
        if metric.agent_id not in self.agent_performance:
            self.agent_performance[metric.agent_id] = {}
        
        self.agent_performance[metric.agent_id][metric.name] = {
            "current": metric.value,
            "timestamp": metric.timestamp.isoformat()
        }
    
    def _check_thresholds(self, metric: Metric):
        """Check if metric exceeds any thresholds"""
        for threshold in self.performance_thresholds:
            if threshold.metric_name == metric.name:
                if self._evaluate_threshold(metric.value, threshold):
                    self._trigger_alert(metric, threshold)
    
    def _evaluate_threshold(self, value: float, threshold: PerformanceThreshold) -> bool:
        """Evaluate if a value exceeds a threshold"""
        op = threshold.comparison_operator
        
        if op == ">":
            return value > threshold.threshold_value
        elif op == "<":
            return value < threshold.threshold_value
        elif op == ">=":
            return value >= threshold.threshold_value
        elif op == "<=":
            return value <= threshold.threshold_value
        elif op == "==":
            return value == threshold.threshold_value
        elif op == "!=":
            return value != threshold.threshold_value
        else:
            return False
    
    def _trigger_alert(self, metric: Metric, threshold: PerformanceThreshold):
        """Trigger an alert for threshold violation"""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": metric.agent_id,
            "operation": metric.operation,
            "metric_name": metric.name,
            "metric_value": metric.value,
            "threshold_value": threshold.threshold_value,
            "severity": threshold.severity,
            "description": threshold.description
        }
        
        logger.warning(f"ALERT: {alert}")
        
        # Call alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Alert callback failed: {e}")
    
    def add_alert_callback(self, callback: Callable):
        """Add a callback function for alerts"""
        self.alert_callbacks.append(callback)
    
    def evaluate_agent(self, 
                      agent_id: str, 
                      operation: str = None,
                      level: EvaluationLevel = EvaluationLevel.DETAILED) -> EvaluationResult:
        """Evaluate an agent's performance"""
        
        # Filter metrics for this agent
        agent_metrics = [
            m for m in self.metrics 
            if m.agent_id == agent_id and (operation is None or m.operation == operation)
        ]
        
        if not agent_metrics:
            return EvaluationResult(
                agent_id=agent_id,
                operation=operation or "all",
                timestamp=datetime.now(),
                overall_score=0.0,
                metric_scores={},
                recommendations=["No metrics available for evaluation"],
                alerts=[]
            )
        
        # Calculate metric scores
        metric_scores = self._calculate_metric_scores(agent_metrics, level)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(metric_scores)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(agent_metrics, metric_scores)
        
        # Check for alerts
        alerts = self._check_agent_alerts(agent_id, operation)
        
        result = EvaluationResult(
            agent_id=agent_id,
            operation=operation or "all",
            timestamp=datetime.now(),
            overall_score=overall_score,
            metric_scores=metric_scores,
            recommendations=recommendations,
            alerts=alerts
        )
        
        self.evaluation_results.append(result)
        return result
    
    def _calculate_metric_scores(self, metrics: List[Metric], level: EvaluationLevel) -> Dict[str, float]:
        """Calculate scores for different metric types"""
        scores = {}
        
        # Group metrics by name
        metric_groups = defaultdict(list)
        for metric in metrics:
            metric_groups[metric.name].append(metric)
        
        for name, metric_list in metric_groups.items():
            values = [m.value for m in metric_list]
            
            if name == "response_time":
                # Lower is better for response time
                avg_time = statistics.mean(values)
                scores[name] = max(0, 100 - (avg_time * 10))  # Scale to 0-100
                
            elif name == "error_rate":
                # Lower is better for error rate
                avg_error_rate = statistics.mean(values)
                scores[name] = max(0, 100 - (avg_error_rate * 1000))  # Scale to 0-100
                
            elif name == "success_rate":
                # Higher is better for success rate
                avg_success_rate = statistics.mean(values)
                scores[name] = avg_success_rate * 100  # Scale to 0-100
                
            elif name == "throughput":
                # Higher is better for throughput
                avg_throughput = statistics.mean(values)
                scores[name] = min(100, avg_throughput * 5)  # Scale to 0-100
                
            elif name == "accuracy":
                # Higher is better for accuracy
                avg_accuracy = statistics.mean(values)
                scores[name] = avg_accuracy * 100  # Scale to 0-100
                
            else:
                # Default scoring (higher is better)
                avg_value = statistics.mean(values)
                scores[name] = min(100, avg_value * 10)  # Scale to 0-100
        
        return scores
    
    def _calculate_overall_score(self, metric_scores: Dict[str, float]) -> float:
        """Calculate overall performance score"""
        if not metric_scores:
            return 0.0
        
        # Weight different metrics
        weights = {
            "response_time": 0.2,
            "error_rate": 0.3,
            "success_rate": 0.3,
            "throughput": 0.1,
            "accuracy": 0.1
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for metric_name, score in metric_scores.items():
            weight = weights.get(metric_name, 0.1)
            weighted_sum += score * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _generate_recommendations(self, metrics: List[Metric], scores: Dict[str, float]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        # Check response time
        if "response_time" in scores and scores["response_time"] < 70:
            recommendations.append("Consider optimizing response time - current performance is below 70%")
        
        # Check error rate
        if "error_rate" in scores and scores["error_rate"] < 80:
            recommendations.append("High error rate detected - investigate error sources and improve error handling")
        
        # Check success rate
        if "success_rate" in scores and scores["success_rate"] < 90:
            recommendations.append("Success rate below 90% - review failure patterns and improve reliability")
        
        # Check throughput
        if "throughput" in scores and scores["throughput"] < 60:
            recommendations.append("Low throughput detected - consider scaling or optimization")
        
        # Check accuracy
        if "accuracy" in scores and scores["accuracy"] < 85:
            recommendations.append("Accuracy below 85% - review model performance and training data")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Performance is within acceptable ranges")
        
        return recommendations
    
    def _check_agent_alerts(self, agent_id: str, operation: str = None) -> List[str]:
        """Check for active alerts for an agent"""
        alerts = []
        
        # Check recent threshold violations
        recent_time = datetime.now() - timedelta(minutes=5)
        recent_metrics = [
            m for m in self.metrics 
            if m.agent_id == agent_id 
            and (operation is None or m.operation == operation)
            and m.timestamp > recent_time
        ]
        
        for metric in recent_metrics:
            for threshold in self.performance_thresholds:
                if (threshold.metric_name == metric.name and 
                    self._evaluate_threshold(metric.value, threshold)):
                    alerts.append(f"{threshold.description} (Value: {metric.value})")
        
        return alerts
    
    def get_agent_performance_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get performance summary for an agent"""
        agent_metrics = [m for m in self.metrics if m.agent_id == agent_id]
        
        if not agent_metrics:
            return {"error": "No metrics available for agent"}
        
        # Calculate summary statistics
        summary = {
            "agent_id": agent_id,
            "total_metrics": len(agent_metrics),
            "time_range": {
                "start": min(m.timestamp for m in agent_metrics).isoformat(),
                "end": max(m.timestamp for m in agent_metrics).isoformat()
            },
            "metrics": {}
        }
        
        # Group by metric name
        metric_groups = defaultdict(list)
        for metric in agent_metrics:
            metric_groups[metric.name].append(metric)
        
        for name, metric_list in metric_groups.items():
            values = [m.value for m in metric_list]
            summary["metrics"][name] = {
                "count": len(values),
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "min": min(values),
                "max": max(values),
                "std": statistics.stdev(values) if len(values) > 1 else 0
            }
        
        return summary
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        if not self.metrics:
            return {"status": "no_data", "message": "No metrics available"}
        
        # Calculate system-wide metrics
        recent_metrics = [
            m for m in self.metrics 
            if m.timestamp > datetime.now() - timedelta(hours=1)
        ]
        
        if not recent_metrics:
            return {"status": "no_recent_data", "message": "No recent metrics available"}
        
        # Calculate health indicators
        error_metrics = [m for m in recent_metrics if m.name == "error_rate"]
        success_metrics = [m for m in recent_metrics if m.name == "success_rate"]
        response_metrics = [m for m in recent_metrics if m.name == "response_time"]
        
        health_score = 100.0
        
        # Check error rate
        if error_metrics:
            avg_error_rate = statistics.mean([m.value for m in error_metrics])
            if avg_error_rate > 0.05:  # 5% error rate
                health_score -= 30
        
        # Check success rate
        if success_metrics:
            avg_success_rate = statistics.mean([m.value for m in success_metrics])
            if avg_success_rate < 0.95:  # 95% success rate
                health_score -= 25
        
        # Check response time
        if response_metrics:
            avg_response_time = statistics.mean([m.value for m in response_metrics])
            if avg_response_time > 5.0:  # 5 seconds
                health_score -= 20
        
        # Determine status
        if health_score >= 90:
            status = "healthy"
        elif health_score >= 70:
            status = "warning"
        elif health_score >= 50:
            status = "degraded"
        else:
            status = "critical"
        
        return {
            "status": status,
            "health_score": health_score,
            "total_metrics": len(self.metrics),
            "recent_metrics": len(recent_metrics),
            "active_alerts": len([r for r in self.evaluation_results if r.alerts]),
            "timestamp": datetime.now().isoformat()
        }
    
    def export_metrics(self, 
                      agent_id: str = None, 
                      start_time: datetime = None, 
                      end_time: datetime = None,
                      format: str = "json") -> str:
        """Export metrics data"""
        filtered_metrics = self.metrics
        
        if agent_id:
            filtered_metrics = [m for m in filtered_metrics if m.agent_id == agent_id]
        
        if start_time:
            filtered_metrics = [m for m in filtered_metrics if m.timestamp >= start_time]
        
        if end_time:
            filtered_metrics = [m for m in filtered_metrics if m.timestamp <= end_time]
        
        if format == "json":
            return json.dumps([asdict(m) for m in filtered_metrics], indent=2, default=str)
        else:
            # CSV format
            lines = ["timestamp,agent_id,operation,metric_name,metric_type,value,metadata,tags"]
            for metric in filtered_metrics:
                lines.append(f"{metric.timestamp.isoformat()},{metric.agent_id},{metric.operation},{metric.name},{metric.metric_type.value},{metric.value},{json.dumps(metric.metadata)},{json.dumps(metric.tags)}")
            return "\n".join(lines)
    
    def add_performance_threshold(self, threshold: PerformanceThreshold):
        """Add a new performance threshold"""
        self.performance_thresholds.append(threshold)
        logger.info(f"Added performance threshold: {threshold.metric_name} {threshold.comparison_operator} {threshold.threshold_value}")
    
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get current real-time metrics"""
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": self.real_time_metrics,
            "agent_performance": dict(self.agent_performance)
        }

# Example usage and testing
async def test_evaluation_framework():
    """Test the evaluation framework"""
    framework = EvaluationFramework()
    
    # Add some test metrics
    framework.add_metric("response_time", 2.5, MetricType.PERFORMANCE, "agent1", "process_request")
    framework.add_metric("error_rate", 0.02, MetricType.RELIABILITY, "agent1", "process_request")
    framework.add_metric("success_rate", 0.98, MetricType.QUALITY, "agent1", "process_request")
    framework.add_metric("throughput", 15.0, MetricType.PERFORMANCE, "agent1", "process_request")
    framework.add_metric("accuracy", 0.92, MetricType.QUALITY, "agent1", "process_request")
    
    # Add more metrics for agent2
    framework.add_metric("response_time", 1.8, MetricType.PERFORMANCE, "agent2", "process_request")
    framework.add_metric("error_rate", 0.01, MetricType.RELIABILITY, "agent2", "process_request")
    framework.add_metric("success_rate", 0.99, MetricType.QUALITY, "agent2", "process_request")
    
    # Evaluate agents
    result1 = framework.evaluate_agent("agent1")
    result2 = framework.evaluate_agent("agent2")
    
    print(f"Agent1 evaluation: {result1.overall_score:.2f}")
    print(f"Agent2 evaluation: {result2.overall_score:.2f}")
    
    # Get system health
    health = framework.get_system_health()
    print(f"System health: {health}")
    
    # Get real-time metrics
    rt_metrics = framework.get_real_time_metrics()
    print(f"Real-time metrics: {len(rt_metrics['metrics'])} metrics")

if __name__ == "__main__":
    asyncio.run(test_evaluation_framework())
