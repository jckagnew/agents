"""
Pattern 15: Resource-Aware Optimization
Comprehensive resource monitoring and optimization system for AI agents
"""

import logging
import json
import asyncio
import sqlite3
import time
from typing import Dict, List, Optional, Any, Union, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import uuid

# Optional psutil import for system resource monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResourceType(Enum):
    """Types of resources to monitor"""
    CPU = "cpu"                   # CPU usage
    MEMORY = "memory"             # Memory usage
    DISK = "disk"                 # Disk usage
    NETWORK = "network"           # Network usage
    API_CALLS = "api_calls"       # API call limits
    TOKENS = "tokens"             # Token usage
    COST = "cost"                 # Financial cost
    TIME = "time"                 # Time-based resources

class ResourceStatus(Enum):
    """Resource status levels"""
    OPTIMAL = "optimal"           # Resource usage is optimal
    WARNING = "warning"           # Resource usage is high but acceptable
    CRITICAL = "critical"         # Resource usage is critical
    EXHAUSTED = "exhausted"       # Resource is exhausted

class OptimizationAction(Enum):
    """Actions to take for optimization"""
    SCALE_UP = "scale_up"         # Increase resource allocation
    SCALE_DOWN = "scale_down"     # Decrease resource allocation
    PAUSE = "pause"               # Pause non-critical operations
    THROTTLE = "throttle"         # Throttle operations
    QUEUE = "queue"               # Queue operations
    CANCEL = "cancel"             # Cancel operations
    OPTIMIZE = "optimize"         # Optimize current operations

@dataclass
class ResourceMetric:
    """Individual resource metric"""
    resource_type: ResourceType
    current_value: float
    max_value: float
    unit: str
    timestamp: datetime
    agent_id: str
    operation: str
    metadata: Dict[str, Any] = None

@dataclass
class ResourceThreshold:
    """Resource threshold configuration"""
    resource_type: ResourceType
    warning_threshold: float
    critical_threshold: float
    max_threshold: float
    unit: str
    optimization_action: OptimizationAction

@dataclass
class ResourceAlert:
    """Resource alert"""
    resource_type: ResourceType
    status: ResourceStatus
    current_value: float
    threshold_value: float
    timestamp: datetime
    agent_id: str
    operation: str
    message: str
    recommended_action: OptimizationAction

@dataclass
class ResourceStats:
    """Resource usage statistics"""
    total_metrics: int
    metrics_by_type: Dict[str, int]
    metrics_by_agent: Dict[str, int]
    current_usage: Dict[str, float]
    peak_usage: Dict[str, float]
    average_usage: Dict[str, float]
    alerts_count: int
    optimization_actions: Dict[str, int]

class ResourceFramework:
    """
    Comprehensive resource monitoring and optimization framework for AI agents
    Implements Pattern 15 with resource tracking, cost optimization, and performance tuning
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.resource_metrics: List[ResourceMetric] = []
        self.resource_thresholds: Dict[ResourceType, ResourceThreshold] = {}
        self.resource_alerts: List[ResourceAlert] = []
        self.optimization_history: List[Dict[str, Any]] = []
        
        # Storage configuration
        self.storage_path = Path(self.config.get("storage_path", "resource_storage"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Database connection
        self.db_path = self.storage_path / "resources.db"
        self._init_database()
        
        # Initialize default thresholds
        self._initialize_default_thresholds()
        
        # Load existing data
        self._load_resource_metrics()
        self._load_resource_alerts()
    
    def _init_database(self):
        """Initialize SQLite database for persistent storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Resource metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resource_metrics (
                id TEXT PRIMARY KEY,
                resource_type TEXT NOT NULL,
                current_value REAL NOT NULL,
                max_value REAL NOT NULL,
                unit TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                operation TEXT NOT NULL,
                metadata TEXT
            )
        ''')
        
        # Resource alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resource_alerts (
                id TEXT PRIMARY KEY,
                resource_type TEXT NOT NULL,
                status TEXT NOT NULL,
                current_value REAL NOT NULL,
                threshold_value REAL NOT NULL,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                operation TEXT NOT NULL,
                message TEXT NOT NULL,
                recommended_action TEXT NOT NULL
            )
        ''')
        
        # Optimization history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS optimization_history (
                id TEXT PRIMARY KEY,
                action TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                details TEXT NOT NULL
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_resource_type ON resource_metrics(resource_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_agent_id ON resource_metrics(agent_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON resource_metrics(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_resource_type ON resource_alerts(resource_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_status ON resource_alerts(status)')
        
        conn.commit()
        conn.close()
    
    def _initialize_default_thresholds(self):
        """Initialize default resource thresholds"""
        self.resource_thresholds = {
            ResourceType.CPU: ResourceThreshold(
                resource_type=ResourceType.CPU,
                warning_threshold=70.0,
                critical_threshold=85.0,
                max_threshold=95.0,
                unit="%",
                optimization_action=OptimizationAction.THROTTLE
            ),
            ResourceType.MEMORY: ResourceThreshold(
                resource_type=ResourceType.MEMORY,
                warning_threshold=80.0,
                critical_threshold=90.0,
                max_threshold=95.0,
                unit="%",
                optimization_action=OptimizationAction.SCALE_UP
            ),
            ResourceType.DISK: ResourceThreshold(
                resource_type=ResourceType.DISK,
                warning_threshold=85.0,
                critical_threshold=95.0,
                max_threshold=98.0,
                unit="%",
                optimization_action=OptimizationAction.OPTIMIZE
            ),
            ResourceType.API_CALLS: ResourceThreshold(
                resource_type=ResourceType.API_CALLS,
                warning_threshold=80.0,
                critical_threshold=90.0,
                max_threshold=95.0,
                unit="%",
                optimization_action=OptimizationAction.THROTTLE
            ),
            ResourceType.TOKENS: ResourceThreshold(
                resource_type=ResourceType.TOKENS,
                warning_threshold=80.0,
                critical_threshold=90.0,
                max_threshold=95.0,
                unit="%",
                optimization_action=OptimizationAction.OPTIMIZE
            ),
            ResourceType.COST: ResourceThreshold(
                resource_type=ResourceType.COST,
                warning_threshold=80.0,
                critical_threshold=90.0,
                max_threshold=95.0,
                unit="%",
                optimization_action=OptimizationAction.OPTIMIZE
            )
        }
    
    def _load_resource_metrics(self):
        """Load resource metrics from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM resource_metrics ORDER BY timestamp DESC LIMIT 10000')
        rows = cursor.fetchall()
        
        for row in rows:
            metric = ResourceMetric(
                resource_type=ResourceType(row[1]),
                current_value=row[2],
                max_value=row[3],
                unit=row[4],
                timestamp=datetime.fromisoformat(row[5]),
                agent_id=row[6],
                operation=row[7],
                metadata=json.loads(row[8]) if row[8] else {}
            )
            self.resource_metrics.append(metric)
        
        conn.close()
        logger.info(f"Loaded {len(self.resource_metrics)} resource metrics from database")
    
    def _load_resource_alerts(self):
        """Load resource alerts from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM resource_alerts ORDER BY timestamp DESC LIMIT 1000')
        rows = cursor.fetchall()
        
        for row in rows:
            alert = ResourceAlert(
                resource_type=ResourceType(row[1]),
                status=ResourceStatus(row[2]),
                current_value=row[3],
                threshold_value=row[4],
                timestamp=datetime.fromisoformat(row[5]),
                agent_id=row[6],
                operation=row[7],
                message=row[8],
                recommended_action=OptimizationAction(row[9])
            )
            self.resource_alerts.append(alert)
        
        conn.close()
        logger.info(f"Loaded {len(self.resource_alerts)} resource alerts from database")
    
    def _save_resource_metric(self, metric: ResourceMetric):
        """Save resource metric to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        metric_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO resource_metrics 
            (id, resource_type, current_value, max_value, unit, timestamp, agent_id, operation, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metric_id, metric.resource_type.value, metric.current_value,
            metric.max_value, metric.unit, metric.timestamp.isoformat(),
            metric.agent_id, metric.operation, json.dumps(metric.metadata)
        ))
        
        conn.commit()
        conn.close()
    
    def _save_resource_alert(self, alert: ResourceAlert):
        """Save resource alert to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        alert_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO resource_alerts 
            (id, resource_type, status, current_value, threshold_value, timestamp, 
             agent_id, operation, message, recommended_action)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            alert_id, alert.resource_type.value, alert.status.value,
            alert.current_value, alert.threshold_value, alert.timestamp.isoformat(),
            alert.agent_id, alert.operation, alert.message, alert.recommended_action.value
        ))
        
        conn.commit()
        conn.close()
    
    def _save_optimization_action(self, action: OptimizationAction, resource_type: ResourceType, 
                                 agent_id: str, details: Dict[str, Any]):
        """Save optimization action to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        action_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO optimization_history 
            (id, action, resource_type, agent_id, timestamp, details)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            action_id, action.value, resource_type.value, agent_id,
            datetime.now().isoformat(), json.dumps(details)
        ))
        
        conn.commit()
        conn.close()
    
    async def record_resource_usage(self, 
                                   resource_type: ResourceType,
                                   current_value: float,
                                   max_value: float,
                                   unit: str,
                                   agent_id: str,
                                   operation: str,
                                   metadata: Dict[str, Any] = None) -> bool:
        """
        Record resource usage
        """
        metric = ResourceMetric(
            resource_type=resource_type,
            current_value=current_value,
            max_value=max_value,
            unit=unit,
            timestamp=datetime.now(),
            agent_id=agent_id,
            operation=operation,
            metadata=metadata or {}
        )
        
        self.resource_metrics.append(metric)
        self._save_resource_metric(metric)
        
        # Check thresholds and generate alerts
        await self._check_thresholds(metric)
        
        logger.debug(f"Recorded {resource_type.value} usage: {current_value}{unit}")
        return True
    
    async def _check_thresholds(self, metric: ResourceMetric):
        """Check resource thresholds and generate alerts"""
        if metric.resource_type not in self.resource_thresholds:
            return
        
        threshold = self.resource_thresholds[metric.resource_type]
        usage_percentage = (metric.current_value / metric.max_value) * 100
        
        status = ResourceStatus.OPTIMAL
        if usage_percentage >= threshold.max_threshold:
            status = ResourceStatus.EXHAUSTED
        elif usage_percentage >= threshold.critical_threshold:
            status = ResourceStatus.CRITICAL
        elif usage_percentage >= threshold.warning_threshold:
            status = ResourceStatus.WARNING
        
        if status != ResourceStatus.OPTIMAL:
            alert = ResourceAlert(
                resource_type=metric.resource_type,
                status=status,
                current_value=metric.current_value,
                threshold_value=threshold.critical_threshold,
                timestamp=datetime.now(),
                agent_id=metric.agent_id,
                operation=metric.operation,
                message=f"{metric.resource_type.value} usage is {usage_percentage:.1f}% (threshold: {threshold.critical_threshold}%)",
                recommended_action=threshold.optimization_action
            )
            
            self.resource_alerts.append(alert)
            self._save_resource_alert(alert)
            
            logger.warning(f"Resource alert: {alert.message}")
    
    async def get_system_resources(self) -> Dict[str, float]:
        """Get current system resource usage"""
        if not PSUTIL_AVAILABLE:
            logger.warning("psutil not available, returning mock system resources")
            return {
                "cpu_percent": 50.0,
                "memory_percent": 60.0,
                "disk_percent": 70.0,
                "network_bytes": 1000000,
                "timestamp": datetime.now().isoformat()
            }
        
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # Network usage
            network = psutil.net_io_counters()
            network_bytes = network.bytes_sent + network.bytes_recv
            
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "disk_percent": disk_percent,
                "network_bytes": network_bytes,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting system resources: {e}")
            return {}
    
    async def optimize_resource_usage(self, 
                                    resource_type: ResourceType,
                                    agent_id: str,
                                    current_usage: float,
                                    max_usage: float) -> OptimizationAction:
        """
        Determine optimization action based on resource usage
        """
        if resource_type not in self.resource_thresholds:
            return OptimizationAction.OPTIMIZE
        
        threshold = self.resource_thresholds[resource_type]
        usage_percentage = (current_usage / max_usage) * 100
        
        action = OptimizationAction.OPTIMIZE
        
        if usage_percentage >= threshold.max_threshold:
            action = OptimizationAction.CANCEL
        elif usage_percentage >= threshold.critical_threshold:
            action = OptimizationAction.PAUSE
        elif usage_percentage >= threshold.warning_threshold:
            action = threshold.optimization_action
        
        # Record optimization action
        self._save_optimization_action(
            action, resource_type, agent_id,
            {
                "current_usage": current_usage,
                "max_usage": max_usage,
                "usage_percentage": usage_percentage,
                "threshold": threshold.critical_threshold
            }
        )
        
        logger.info(f"Optimization action for {resource_type.value}: {action.value}")
        return action
    
    async def get_resource_usage(self, 
                               resource_type: ResourceType = None,
                               agent_id: str = None,
                               hours: int = 24) -> List[ResourceMetric]:
        """Get resource usage with optional filters"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        filtered_metrics = [
            m for m in self.resource_metrics 
            if m.timestamp > cutoff_time
        ]
        
        if resource_type:
            filtered_metrics = [m for m in filtered_metrics if m.resource_type == resource_type]
        
        if agent_id:
            filtered_metrics = [m for m in filtered_metrics if m.agent_id == agent_id]
        
        return filtered_metrics
    
    async def get_resource_alerts(self, 
                                resource_type: ResourceType = None,
                                status: ResourceStatus = None,
                                hours: int = 24) -> List[ResourceAlert]:
        """Get resource alerts with optional filters"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        filtered_alerts = [
            a for a in self.resource_alerts 
            if a.timestamp > cutoff_time
        ]
        
        if resource_type:
            filtered_alerts = [a for a in filtered_alerts if a.resource_type == resource_type]
        
        if status:
            filtered_alerts = [a for a in filtered_alerts if a.status == status]
        
        return filtered_alerts
    
    def get_resource_statistics(self) -> ResourceStats:
        """Get resource usage statistics"""
        if not self.resource_metrics:
            return ResourceStats(
                total_metrics=0,
                metrics_by_type={},
                metrics_by_agent={},
                current_usage={},
                peak_usage={},
                average_usage={},
                alerts_count=len(self.resource_alerts),
                optimization_actions={}
            )
        
        # Count by type
        metrics_by_type = {}
        for resource_type in ResourceType:
            metrics_by_type[resource_type.value] = len([
                m for m in self.resource_metrics 
                if m.resource_type == resource_type
            ])
        
        # Count by agent
        metrics_by_agent = {}
        for metric in self.resource_metrics:
            if metric.agent_id not in metrics_by_agent:
                metrics_by_agent[metric.agent_id] = 0
            metrics_by_agent[metric.agent_id] += 1
        
        # Calculate current, peak, and average usage
        current_usage = {}
        peak_usage = {}
        average_usage = {}
        
        for resource_type in ResourceType:
            type_metrics = [m for m in self.resource_metrics if m.resource_type == resource_type]
            if type_metrics:
                current_usage[resource_type.value] = type_metrics[-1].current_value
                peak_usage[resource_type.value] = max(m.current_value for m in type_metrics)
                average_usage[resource_type.value] = sum(m.current_value for m in type_metrics) / len(type_metrics)
            else:
                current_usage[resource_type.value] = 0
                peak_usage[resource_type.value] = 0
                average_usage[resource_type.value] = 0
        
        # Count optimization actions
        optimization_actions = {}
        for action in OptimizationAction:
            optimization_actions[action.value] = len([
                h for h in self.optimization_history 
                if h.get("action") == action.value
            ])
        
        return ResourceStats(
            total_metrics=len(self.resource_metrics),
            metrics_by_type=metrics_by_type,
            metrics_by_agent=metrics_by_agent,
            current_usage=current_usage,
            peak_usage=peak_usage,
            average_usage=average_usage,
            alerts_count=len(self.resource_alerts),
            optimization_actions=optimization_actions
        )
    
    async def set_resource_threshold(self, 
                                   resource_type: ResourceType,
                                   warning_threshold: float,
                                   critical_threshold: float,
                                   max_threshold: float,
                                   optimization_action: OptimizationAction):
        """Set custom resource threshold"""
        self.resource_thresholds[resource_type] = ResourceThreshold(
            resource_type=resource_type,
            warning_threshold=warning_threshold,
            critical_threshold=critical_threshold,
            max_threshold=max_threshold,
            unit="%",
            optimization_action=optimization_action
        )
        
        logger.info(f"Set threshold for {resource_type.value}: warning={warning_threshold}%, critical={critical_threshold}%")
    
    async def export_resource_data(self, 
                                 resource_type: ResourceType = None,
                                 agent_id: str = None,
                                 format: str = "json") -> str:
        """Export resource data"""
        metrics = await self.get_resource_usage(resource_type=resource_type, agent_id=agent_id)
        alerts = await self.get_resource_alerts(resource_type=resource_type)
        
        data = {
            "metrics": [asdict(m) for m in metrics],
            "alerts": [asdict(a) for a in alerts],
            "statistics": asdict(self.get_resource_statistics())
        }
        
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        else:
            # CSV format
            lines = ["timestamp,resource_type,current_value,max_value,unit,agent_id,operation"]
            for metric in metrics:
                lines.append(f"{metric.timestamp.isoformat()},{metric.resource_type.value},{metric.current_value},{metric.max_value},{metric.unit},{metric.agent_id},{metric.operation}")
            return "\n".join(lines)

# Example usage and testing
async def test_resource_framework():
    """Test the resource framework"""
    framework = ResourceFramework()
    
    # Record some test resource usage
    await framework.record_resource_usage(
        ResourceType.CPU, 75.0, 100.0, "%", "agent1", "test_operation"
    )
    
    await framework.record_resource_usage(
        ResourceType.MEMORY, 85.0, 100.0, "%", "agent1", "test_operation"
    )
    
    # Get statistics
    stats = framework.get_resource_statistics()
    print(f"Total metrics: {stats.total_metrics}")
    print(f"Current CPU usage: {stats.current_usage['cpu']}%")
    
    # Get system resources
    system_resources = await framework.get_system_resources()
    print(f"System CPU: {system_resources.get('cpu_percent', 0)}%")

if __name__ == "__main__":
    asyncio.run(test_resource_framework())
