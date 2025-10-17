"""
Pattern 1: Multi-Agent Orchestration
Comprehensive multi-agent coordination and workflow management system
"""

import logging
import json
import asyncio
import sqlite3
import uuid
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """Agent status states"""
    IDLE = "idle"                 # Agent is available for tasks
    BUSY = "busy"                 # Agent is working on a task
    OFFLINE = "offline"           # Agent is not available
    ERROR = "error"               # Agent encountered an error
    MAINTENANCE = "maintenance"   # Agent is in maintenance mode

class TaskStatus(Enum):
    """Task status states"""
    PENDING = "pending"           # Task is waiting to be assigned
    ASSIGNED = "assigned"         # Task has been assigned to an agent
    IN_PROGRESS = "in_progress"   # Task is being worked on
    COMPLETED = "completed"       # Task has been completed
    FAILED = "failed"            # Task failed to complete
    CANCELLED = "cancelled"       # Task was cancelled
    TIMEOUT = "timeout"          # Task timed out

class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class WorkflowStatus(Enum):
    """Workflow status states"""
    ACTIVE = "active"             # Workflow is running
    PAUSED = "paused"            # Workflow is paused
    COMPLETED = "completed"       # Workflow has finished
    FAILED = "failed"            # Workflow failed
    CANCELLED = "cancelled"       # Workflow was cancelled

@dataclass
class Agent:
    """Individual agent definition"""
    id: str
    name: str
    capabilities: List[str]
    status: AgentStatus
    current_task: Optional[str] = None
    max_concurrent_tasks: int = 1
    created_at: datetime = None
    last_heartbeat: datetime = None
    metadata: Dict[str, Any] = None

@dataclass
class Task:
    """Individual task definition"""
    id: str
    name: str
    description: str
    agent_id: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    timeout: Optional[timedelta] = None
    dependencies: List[str] = None
    result: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class Workflow:
    """Workflow definition"""
    id: str
    name: str
    description: str
    tasks: List[str]
    dependencies: Dict[str, List[str]]
    status: WorkflowStatus = WorkflowStatus.ACTIVE
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None

@dataclass
class OrchestrationStats:
    """Orchestration statistics"""
    total_agents: int
    active_agents: int
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    active_workflows: int
    completed_workflows: int
    average_task_completion_time: float
    agent_utilization: Dict[str, float]

class OrchestrationFramework:
    """
    Comprehensive multi-agent orchestration framework
    Implements Pattern 1 with agent coordination, task distribution, and workflow management
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.workflows: Dict[str, Workflow] = {}
        self.task_queue: List[str] = []
        self.workflow_queue: List[str] = []
        
        # Storage configuration
        self.storage_path = Path(self.config.get("storage_path", "orchestration_storage"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Database connection
        self.db_path = self.storage_path / "orchestration.db"
        self._init_database()
        
        # Threading and concurrency
        self.executor = ThreadPoolExecutor(max_workers=self.config.get("max_workers", 10))
        self.lock = threading.Lock()
        
        # Event handlers
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        # Load existing data
        self._load_agents()
        self._load_tasks()
        self._load_workflows()
        
        # Start background processes
        self._start_background_processes()
    
    def _init_database(self):
        """Initialize SQLite database for persistent storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Agents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                capabilities TEXT NOT NULL,
                status TEXT NOT NULL,
                current_task TEXT,
                max_concurrent_tasks INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                last_heartbeat TEXT,
                metadata TEXT
            )
        ''')
        
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                agent_id TEXT,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                timeout_seconds INTEGER,
                dependencies TEXT,
                result TEXT,
                error TEXT,
                metadata TEXT
            )
        ''')
        
        # Workflows table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflows (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                tasks TEXT NOT NULL,
                dependencies TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                metadata TEXT
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_agent_id ON tasks(agent_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_workflows_status ON workflows(status)')
        
        conn.commit()
        conn.close()
    
    def _load_agents(self):
        """Load agents from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM agents')
        rows = cursor.fetchall()
        
        for row in rows:
            agent = Agent(
                id=row[0],
                name=row[1],
                capabilities=json.loads(row[2]),
                status=AgentStatus(row[3]),
                current_task=row[4],
                max_concurrent_tasks=row[5],
                created_at=datetime.fromisoformat(row[6]),
                last_heartbeat=datetime.fromisoformat(row[7]) if row[7] else None,
                metadata=json.loads(row[8]) if row[8] else {}
            )
            self.agents[agent.id] = agent
        
        conn.close()
        logger.info(f"Loaded {len(self.agents)} agents from database")
    
    def _load_tasks(self):
        """Load tasks from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        
        for row in rows:
            task = Task(
                id=row[0],
                name=row[1],
                description=row[2],
                agent_id=row[3],
                status=TaskStatus(row[4]),
                priority=TaskPriority(row[5]),
                created_at=datetime.fromisoformat(row[6]),
                started_at=datetime.fromisoformat(row[7]) if row[7] else None,
                completed_at=datetime.fromisoformat(row[8]) if row[8] else None,
                timeout=timedelta(seconds=row[9]) if row[9] else None,
                dependencies=json.loads(row[10]) if row[10] else [],
                result=json.loads(row[11]) if row[11] else None,
                error=row[12],
                metadata=json.loads(row[13]) if row[13] else {}
            )
            self.tasks[task.id] = task
            
            # Add to queue if pending
            if task.status == TaskStatus.PENDING:
                self.task_queue.append(task.id)
        
        conn.close()
        logger.info(f"Loaded {len(self.tasks)} tasks from database")
    
    def _load_workflows(self):
        """Load workflows from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM workflows')
        rows = cursor.fetchall()
        
        for row in rows:
            workflow = Workflow(
                id=row[0],
                name=row[1],
                description=row[2],
                tasks=json.loads(row[3]),
                dependencies=json.loads(row[4]),
                status=WorkflowStatus(row[5]),
                created_at=datetime.fromisoformat(row[6]),
                started_at=datetime.fromisoformat(row[7]) if row[7] else None,
                completed_at=datetime.fromisoformat(row[8]) if row[8] else None,
                metadata=json.loads(row[9]) if row[9] else {}
            )
            self.workflows[workflow.id] = workflow
            
            # Add to queue if active
            if workflow.status == WorkflowStatus.ACTIVE:
                self.workflow_queue.append(workflow.id)
        
        conn.close()
        logger.info(f"Loaded {len(self.workflows)} workflows from database")
    
    def _save_agent(self, agent: Agent):
        """Save agent to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO agents 
            (id, name, capabilities, status, current_task, max_concurrent_tasks, 
             created_at, last_heartbeat, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            agent.id, agent.name, json.dumps(agent.capabilities),
            agent.status.value, agent.current_task, agent.max_concurrent_tasks,
            agent.created_at.isoformat(),
            agent.last_heartbeat.isoformat() if agent.last_heartbeat else None,
            json.dumps(agent.metadata)
        ))
        
        conn.commit()
        conn.close()
    
    def _save_task(self, task: Task):
        """Save task to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO tasks 
            (id, name, description, agent_id, status, priority, created_at,
             started_at, completed_at, timeout_seconds, dependencies, result, error, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task.id, task.name, task.description, task.agent_id,
            task.status.value, task.priority.value, task.created_at.isoformat(),
            task.started_at.isoformat() if task.started_at else None,
            task.completed_at.isoformat() if task.completed_at else None,
            task.timeout.total_seconds() if task.timeout else None,
            json.dumps(task.dependencies), json.dumps(task.result),
            task.error, json.dumps(task.metadata)
        ))
        
        conn.commit()
        conn.close()
    
    def _save_workflow(self, workflow: Workflow):
        """Save workflow to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO workflows 
            (id, name, description, tasks, dependencies, status, created_at,
             started_at, completed_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            workflow.id, workflow.name, workflow.description,
            json.dumps(workflow.tasks), json.dumps(workflow.dependencies),
            workflow.status.value, workflow.created_at.isoformat(),
            workflow.started_at.isoformat() if workflow.started_at else None,
            workflow.completed_at.isoformat() if workflow.completed_at else None,
            json.dumps(workflow.metadata)
        ))
        
        conn.commit()
        conn.close()
    
    def _start_background_processes(self):
        """Start background orchestration processes"""
        # Start task assignment process
        asyncio.create_task(self._task_assignment_loop())
        
        # Start workflow execution process
        asyncio.create_task(self._workflow_execution_loop())
        
        # Start agent health monitoring
        asyncio.create_task(self._agent_health_monitor())
        
        logger.info("Background processes started")
    
    async def register_agent(self, 
                           name: str,
                           capabilities: List[str],
                           max_concurrent_tasks: int = 1,
                           metadata: Dict[str, Any] = None) -> str:
        """
        Register a new agent
        """
        agent_id = str(uuid.uuid4())
        
        agent = Agent(
            id=agent_id,
            name=name,
            capabilities=capabilities,
            status=AgentStatus.IDLE,
            max_concurrent_tasks=max_concurrent_tasks,
            created_at=datetime.now(),
            last_heartbeat=datetime.now(),
            metadata=metadata or {}
        )
        
        with self.lock:
            self.agents[agent_id] = agent
            self._save_agent(agent)
        
        await self._emit_event("agent_registered", {"agent_id": agent_id, "agent": agent})
        
        logger.info(f"Registered agent {agent_id}: {name}")
        return agent_id
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister an agent
        """
        if agent_id not in self.agents:
            return False
        
        with self.lock:
            agent = self.agents[agent_id]
            agent.status = AgentStatus.OFFLINE
            
            # Reassign current task if any
            if agent.current_task:
                task = self.tasks[agent.current_task]
                task.status = TaskStatus.PENDING
                task.agent_id = None
                self.task_queue.append(task.id)
                self._save_task(task)
            
            self._save_agent(agent)
        
        await self._emit_event("agent_unregistered", {"agent_id": agent_id})
        
        logger.info(f"Unregistered agent {agent_id}")
        return True
    
    async def create_task(self, 
                        name: str,
                        description: str,
                        capabilities_required: List[str] = None,
                        priority: TaskPriority = TaskPriority.MEDIUM,
                        timeout: timedelta = None,
                        dependencies: List[str] = None,
                        metadata: Dict[str, Any] = None) -> str:
        """
        Create a new task
        """
        task_id = str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            name=name,
            description=description,
            status=TaskStatus.PENDING,
            priority=priority,
            created_at=datetime.now(),
            timeout=timeout,
            dependencies=dependencies or [],
            metadata=metadata or {}
        )
        
        with self.lock:
            self.tasks[task_id] = task
            self.task_queue.append(task_id)
            self._save_task(task)
        
        await self._emit_event("task_created", {"task_id": task_id, "task": task})
        
        logger.info(f"Created task {task_id}: {name}")
        return task_id
    
    async def create_workflow(self, 
                            name: str,
                            description: str,
                            tasks: List[Dict[str, Any]],
                            dependencies: Dict[str, List[str]] = None,
                            metadata: Dict[str, Any] = None) -> str:
        """
        Create a new workflow
        """
        workflow_id = str(uuid.uuid4())
        
        # Create individual tasks
        task_ids = []
        for task_def in tasks:
            task_id = await self.create_task(
                name=task_def["name"],
                description=task_def["description"],
                capabilities_required=task_def.get("capabilities_required"),
                priority=TaskPriority(task_def.get("priority", "medium")),
                timeout=timedelta(seconds=task_def.get("timeout", 3600)) if task_def.get("timeout") else None,
                metadata=task_def.get("metadata", {})
            )
            task_ids.append(task_id)
        
        workflow = Workflow(
            id=workflow_id,
            name=name,
            description=description,
            tasks=task_ids,
            dependencies=dependencies or {},
            status=WorkflowStatus.ACTIVE,
            created_at=datetime.now(),
            metadata=metadata or {}
        )
        
        with self.lock:
            self.workflows[workflow_id] = workflow
            self.workflow_queue.append(workflow_id)
            self._save_workflow(workflow)
        
        await self._emit_event("workflow_created", {"workflow_id": workflow_id, "workflow": workflow})
        
        logger.info(f"Created workflow {workflow_id}: {name}")
        return workflow_id
    
    async def assign_task(self, task_id: str, agent_id: str) -> bool:
        """
        Assign a task to an agent
        """
        if task_id not in self.tasks or agent_id not in self.agents:
            return False
        
        task = self.tasks[task_id]
        agent = self.agents[agent_id]
        
        # Check if agent is available
        if agent.status != AgentStatus.IDLE:
            return False
        
        # Check if agent has capacity
        if agent.current_task:
            return False
        
        with self.lock:
            task.agent_id = agent_id
            task.status = TaskStatus.ASSIGNED
            task.started_at = datetime.now()
            
            agent.current_task = task_id
            agent.status = AgentStatus.BUSY
            
            self._save_task(task)
            self._save_agent(agent)
        
        await self._emit_event("task_assigned", {"task_id": task_id, "agent_id": agent_id})
        
        logger.info(f"Assigned task {task_id} to agent {agent_id}")
        return True
    
    async def complete_task(self, 
                          task_id: str, 
                          result: Any = None,
                          error: str = None) -> bool:
        """
        Mark a task as completed
        """
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        agent = self.agents.get(task.agent_id) if task.agent_id else None
        
        with self.lock:
            if error:
                task.status = TaskStatus.FAILED
                task.error = error
            else:
                task.status = TaskStatus.COMPLETED
                task.result = result
            
            task.completed_at = datetime.now()
            
            if agent:
                agent.current_task = None
                agent.status = AgentStatus.IDLE
                self._save_agent(agent)
            
            self._save_task(task)
        
        await self._emit_event("task_completed", {
            "task_id": task_id, 
            "status": task.status.value,
            "result": result,
            "error": error
        })
        
        logger.info(f"Completed task {task_id}: {task.status.value}")
        return True
    
    async def _task_assignment_loop(self):
        """
        Background task assignment loop
        """
        while True:
            try:
                await self._process_task_queue()
                await asyncio.sleep(1)  # Check every second
            except Exception as e:
                logger.error(f"Error in task assignment loop: {e}")
                await asyncio.sleep(5)
    
    async def _process_task_queue(self):
        """
        Process pending tasks in the queue
        """
        if not self.task_queue:
            return
        
        # Get available agents
        available_agents = [
            agent for agent in self.agents.values()
            if agent.status == AgentStatus.IDLE
        ]
        
        if not available_agents:
            return
        
        # Process tasks by priority
        with self.lock:
            pending_tasks = [
                task_id for task_id in self.task_queue
                if self.tasks[task_id].status == TaskStatus.PENDING
            ]
        
        # Sort by priority
        pending_tasks.sort(key=lambda tid: self.tasks[tid].priority.value, reverse=True)
        
        for task_id in pending_tasks[:len(available_agents)]:
            task = self.tasks[task_id]
            
            # Find suitable agent
            suitable_agent = None
            for agent in available_agents:
                if not task.metadata.get("capabilities_required") or \
                   all(cap in agent.capabilities for cap in task.metadata.get("capabilities_required", [])):
                    suitable_agent = agent
                    break
            
            if suitable_agent:
                await self.assign_task(task_id, suitable_agent.id)
                available_agents.remove(suitable_agent)
                self.task_queue.remove(task_id)
    
    async def _workflow_execution_loop(self):
        """
        Background workflow execution loop
        """
        while True:
            try:
                await self._process_workflow_queue()
                await asyncio.sleep(2)  # Check every 2 seconds
            except Exception as e:
                logger.error(f"Error in workflow execution loop: {e}")
                await asyncio.sleep(5)
    
    async def _process_workflow_queue(self):
        """
        Process active workflows
        """
        for workflow_id in self.workflow_queue[:]:
            workflow = self.workflows[workflow_id]
            
            if workflow.status != WorkflowStatus.ACTIVE:
                continue
            
            # Check if all tasks are completed
            all_completed = True
            for task_id in workflow.tasks:
                task = self.tasks[task_id]
                if task.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                    all_completed = False
                    break
            
            if all_completed:
                with self.lock:
                    workflow.status = WorkflowStatus.COMPLETED
                    workflow.completed_at = datetime.now()
                    self._save_workflow(workflow)
                    self.workflow_queue.remove(workflow_id)
                
                await self._emit_event("workflow_completed", {"workflow_id": workflow_id})
                logger.info(f"Completed workflow {workflow_id}")
    
    async def _agent_health_monitor(self):
        """
        Monitor agent health and handle timeouts
        """
        while True:
            try:
                await self._check_agent_health()
                await asyncio.sleep(10)  # Check every 10 seconds
            except Exception as e:
                logger.error(f"Error in agent health monitor: {e}")
                await asyncio.sleep(30)
    
    async def _check_agent_health(self):
        """
        Check agent health and handle timeouts
        """
        now = datetime.now()
        timeout_threshold = timedelta(minutes=5)
        
        for agent in self.agents.values():
            if agent.status == AgentStatus.BUSY and agent.current_task:
                task = self.tasks[agent.current_task]
                
                # Check task timeout
                if task.timeout and task.started_at:
                    if now - task.started_at > task.timeout:
                        await self.complete_task(task.id, error="Task timeout")
                        logger.warning(f"Task {task.id} timed out")
                
                # Check agent heartbeat
                if agent.last_heartbeat and now - agent.last_heartbeat > timeout_threshold:
                    agent.status = AgentStatus.ERROR
                    self._save_agent(agent)
                    logger.warning(f"Agent {agent.id} appears to be unresponsive")
    
    async def _emit_event(self, event_type: str, data: Dict[str, Any]):
        """
        Emit an event to registered handlers
        """
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    await handler(data)
                except Exception as e:
                    logger.error(f"Error in event handler for {event_type}: {e}")
    
    def add_event_handler(self, event_type: str, handler: Callable):
        """
        Add an event handler
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def get_agents(self, status: AgentStatus = None) -> List[Agent]:
        """
        Get agents with optional status filter
        """
        agents = list(self.agents.values())
        if status:
            agents = [a for a in agents if a.status == status]
        return agents
    
    def get_tasks(self, 
                 status: TaskStatus = None,
                 agent_id: str = None,
                 priority: TaskPriority = None) -> List[Task]:
        """
        Get tasks with optional filters
        """
        tasks = list(self.tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        if agent_id:
            tasks = [t for t in tasks if t.agent_id == agent_id]
        
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        
        return tasks
    
    def get_workflows(self, status: WorkflowStatus = None) -> List[Workflow]:
        """
        Get workflows with optional status filter
        """
        workflows = list(self.workflows.values())
        if status:
            workflows = [w for w in workflows if w.status == status]
        return workflows
    
    def get_orchestration_statistics(self) -> OrchestrationStats:
        """
        Get orchestration statistics
        """
        agents = list(self.agents.values())
        tasks = list(self.tasks.values())
        workflows = list(self.workflows.values())
        
        # Calculate agent utilization
        agent_utilization = {}
        for agent in agents:
            if agent.status == AgentStatus.BUSY:
                agent_utilization[agent.id] = 1.0
            else:
                agent_utilization[agent.id] = 0.0
        
        # Calculate average task completion time
        completed_tasks = [t for t in tasks if t.status == TaskStatus.COMPLETED and t.started_at and t.completed_at]
        if completed_tasks:
            total_time = sum((t.completed_at - t.started_at).total_seconds() for t in completed_tasks)
            avg_completion_time = total_time / len(completed_tasks)
        else:
            avg_completion_time = 0.0
        
        return OrchestrationStats(
            total_agents=len(agents),
            active_agents=len([a for a in agents if a.status in [AgentStatus.IDLE, AgentStatus.BUSY]]),
            total_tasks=len(tasks),
            completed_tasks=len([t for t in tasks if t.status == TaskStatus.COMPLETED]),
            failed_tasks=len([t for t in tasks if t.status == TaskStatus.FAILED]),
            active_workflows=len([w for w in workflows if w.status == WorkflowStatus.ACTIVE]),
            completed_workflows=len([w for w in workflows if w.status == WorkflowStatus.COMPLETED]),
            average_task_completion_time=avg_completion_time,
            agent_utilization=agent_utilization
        )
    
    async def export_data(self, format: str = "json") -> str:
        """
        Export orchestration data
        """
        data = {
            "agents": [asdict(a) for a in self.agents.values()],
            "tasks": [asdict(t) for t in self.tasks.values()],
            "workflows": [asdict(w) for w in self.workflows.values()],
            "statistics": asdict(self.get_orchestration_statistics())
        }
        
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        else:
            # CSV format
            lines = ["type,id,name,status,created_at"]
            for agent in self.agents.values():
                lines.append(f"agent,{agent.id},{agent.name},{agent.status.value},{agent.created_at.isoformat()}")
            for task in self.tasks.values():
                lines.append(f"task,{task.id},{task.name},{task.status.value},{task.created_at.isoformat()}")
            for workflow in self.workflows.values():
                lines.append(f"workflow,{workflow.id},{workflow.name},{workflow.status.value},{workflow.created_at.isoformat()}")
            return "\n".join(lines)

# Example usage and testing
async def test_orchestration_framework():
    """Test the orchestration framework"""
    framework = OrchestrationFramework()
    
    # Register agents
    agent1_id = await framework.register_agent("Agent1", ["data_processing", "analysis"])
    agent2_id = await framework.register_agent("Agent2", ["web_scraping", "api_calls"])
    
    # Create tasks
    task1_id = await framework.create_task("Process Data", "Process incoming data", ["data_processing"])
    task2_id = await framework.create_task("Scrape Website", "Scrape website data", ["web_scraping"])
    
    # Create workflow
    workflow_id = await framework.create_workflow(
        "Data Pipeline",
        "Complete data processing pipeline",
        [
            {"name": "Fetch Data", "description": "Fetch data from API", "capabilities_required": ["api_calls"]},
            {"name": "Process Data", "description": "Process the fetched data", "capabilities_required": ["data_processing"]}
        ]
    )
    
    # Get statistics
    stats = framework.get_orchestration_statistics()
    print(f"Total agents: {stats.total_agents}")
    print(f"Total tasks: {stats.total_tasks}")
    print(f"Active workflows: {stats.active_workflows}")

if __name__ == "__main__":
    asyncio.run(test_orchestration_framework())
