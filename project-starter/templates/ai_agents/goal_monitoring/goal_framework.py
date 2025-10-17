"""
Pattern 10: Goal Setting & Monitoring
Comprehensive goal setting and monitoring system for AI agents
"""

import logging
import json
import asyncio
import sqlite3
from typing import Dict, List, Optional, Any, Union, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoalStatus(Enum):
    """Goal status states"""
    PENDING = "pending"           # Goal created but not started
    IN_PROGRESS = "in_progress"   # Goal is being worked on
    COMPLETED = "completed"       # Goal has been achieved
    FAILED = "failed"            # Goal could not be achieved
    CANCELLED = "cancelled"      # Goal was cancelled
    PAUSED = "paused"            # Goal is temporarily paused

class GoalPriority(Enum):
    """Goal priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class GoalType(Enum):
    """Types of goals"""
    TASK = "task"                 # Specific task to complete
    OBJECTIVE = "objective"       # High-level objective
    MILESTONE = "milestone"       # Project milestone
    PERFORMANCE = "performance"   # Performance improvement goal
    LEARNING = "learning"         # Learning and development goal
    BEHAVIORAL = "behavioral"     # Behavioral change goal

class ProgressMetric(Enum):
    """Types of progress metrics"""
    PERCENTAGE = "percentage"     # 0-100% completion
    COUNT = "count"              # Number of items completed
    TIME = "time"                # Time-based progress
    QUALITY = "quality"          # Quality-based progress
    CUSTOM = "custom"            # Custom metric

@dataclass
class Goal:
    """Individual goal definition"""
    id: str
    title: str
    description: str
    goal_type: GoalType
    priority: GoalPriority
    status: GoalStatus
    agent_id: str
    created_at: datetime
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0
    progress_metric: ProgressMetric = ProgressMetric.PERCENTAGE
    success_criteria: List[str] = None
    dependencies: List[str] = None
    tags: List[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class GoalProgress:
    """Goal progress update"""
    goal_id: str
    progress: float
    metric_type: ProgressMetric
    timestamp: datetime
    notes: str = ""
    evidence: Dict[str, Any] = None

@dataclass
class GoalAchievement:
    """Goal achievement record"""
    goal_id: str
    achieved_at: datetime
    success_criteria_met: List[str]
    evidence: Dict[str, Any]
    notes: str = ""

@dataclass
class GoalStats:
    """Goal statistics"""
    total_goals: int
    goals_by_status: Dict[str, int]
    goals_by_priority: Dict[str, int]
    goals_by_type: Dict[str, int]
    completion_rate: float
    average_completion_time: float
    overdue_goals: int
    active_goals: int

class GoalFramework:
    """
    Comprehensive goal setting and monitoring framework for AI agents
    Implements Pattern 10 with goal tracking, progress monitoring, and achievement validation
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.goals: Dict[str, Goal] = {}
        self.progress_history: List[GoalProgress] = []
        self.achievements: List[GoalAchievement] = []
        
        # Storage configuration
        self.storage_path = Path(self.config.get("storage_path", "goal_storage"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Database connection
        self.db_path = self.storage_path / "goals.db"
        self._init_database()
        
        # Load existing data
        self._load_goals()
        self._load_progress_history()
        self._load_achievements()
    
    def _init_database(self):
        """Initialize SQLite database for persistent storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                goal_type TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                due_date TEXT,
                completed_at TEXT,
                progress REAL DEFAULT 0.0,
                progress_metric TEXT DEFAULT 'percentage',
                success_criteria TEXT,
                dependencies TEXT,
                tags TEXT,
                metadata TEXT
            )
        ''')
        
        # Progress history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goal_progress (
                id TEXT PRIMARY KEY,
                goal_id TEXT NOT NULL,
                progress REAL NOT NULL,
                metric_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                notes TEXT,
                evidence TEXT,
                FOREIGN KEY (goal_id) REFERENCES goals (id)
            )
        ''')
        
        # Achievements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goal_achievements (
                id TEXT PRIMARY KEY,
                goal_id TEXT NOT NULL,
                achieved_at TEXT NOT NULL,
                success_criteria_met TEXT NOT NULL,
                evidence TEXT,
                notes TEXT,
                FOREIGN KEY (goal_id) REFERENCES goals (id)
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_goals_agent_id ON goals(agent_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_goals_status ON goals(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_goals_priority ON goals(priority)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_progress_goal_id ON goal_progress(goal_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_achievements_goal_id ON goal_achievements(goal_id)')
        
        conn.commit()
        conn.close()
    
    def _load_goals(self):
        """Load goals from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM goals')
        rows = cursor.fetchall()
        
        for row in rows:
            goal = Goal(
                id=row[0],
                title=row[1],
                description=row[2],
                goal_type=GoalType(row[3]),
                priority=GoalPriority(row[4]),
                status=GoalStatus(row[5]),
                agent_id=row[6],
                created_at=datetime.fromisoformat(row[7]),
                due_date=datetime.fromisoformat(row[8]) if row[8] else None,
                completed_at=datetime.fromisoformat(row[9]) if row[9] else None,
                progress=row[10],
                progress_metric=ProgressMetric(row[11]),
                success_criteria=json.loads(row[12]) if row[12] else [],
                dependencies=json.loads(row[13]) if row[13] else [],
                tags=json.loads(row[14]) if row[14] else [],
                metadata=json.loads(row[15]) if row[15] else {}
            )
            self.goals[goal.id] = goal
        
        conn.close()
        logger.info(f"Loaded {len(self.goals)} goals from database")
    
    def _load_progress_history(self):
        """Load progress history from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM goal_progress')
        rows = cursor.fetchall()
        
        for row in rows:
            progress = GoalProgress(
                goal_id=row[1],
                progress=row[2],
                metric_type=ProgressMetric(row[3]),
                timestamp=datetime.fromisoformat(row[4]),
                notes=row[5] or "",
                evidence=json.loads(row[6]) if row[6] else {}
            )
            self.progress_history.append(progress)
        
        conn.close()
        logger.info(f"Loaded {len(self.progress_history)} progress records from database")
    
    def _load_achievements(self):
        """Load achievements from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM goal_achievements')
        rows = cursor.fetchall()
        
        for row in rows:
            achievement = GoalAchievement(
                goal_id=row[1],
                achieved_at=datetime.fromisoformat(row[2]),
                success_criteria_met=json.loads(row[3]),
                evidence=json.loads(row[4]) if row[4] else {},
                notes=row[5] or ""
            )
            self.achievements.append(achievement)
        
        conn.close()
        logger.info(f"Loaded {len(self.achievements)} achievements from database")
    
    def _save_goal(self, goal: Goal):
        """Save goal to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO goals 
            (id, title, description, goal_type, priority, status, agent_id, created_at,
             due_date, completed_at, progress, progress_metric, success_criteria,
             dependencies, tags, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            goal.id, goal.title, goal.description, goal.goal_type.value,
            goal.priority.value, goal.status.value, goal.agent_id,
            goal.created_at.isoformat(), goal.due_date.isoformat() if goal.due_date else None,
            goal.completed_at.isoformat() if goal.completed_at else None,
            goal.progress, goal.progress_metric.value,
            json.dumps(goal.success_criteria), json.dumps(goal.dependencies),
            json.dumps(goal.tags), json.dumps(goal.metadata)
        ))
        
        conn.commit()
        conn.close()
    
    def _save_progress(self, progress: GoalProgress):
        """Save progress record to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        progress_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO goal_progress 
            (id, goal_id, progress, metric_type, timestamp, notes, evidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            progress_id, progress.goal_id, progress.progress,
            progress.metric_type.value, progress.timestamp.isoformat(),
            progress.notes, json.dumps(progress.evidence)
        ))
        
        conn.commit()
        conn.close()
    
    def _save_achievement(self, achievement: GoalAchievement):
        """Save achievement record to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        achievement_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO goal_achievements 
            (id, goal_id, achieved_at, success_criteria_met, evidence, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            achievement_id, achievement.goal_id, achievement.achieved_at.isoformat(),
            json.dumps(achievement.success_criteria_met), json.dumps(achievement.evidence),
            achievement.notes
        ))
        
        conn.commit()
        conn.close()
    
    async def create_goal(self, 
                         title: str,
                         description: str,
                         goal_type: GoalType,
                         agent_id: str,
                         priority: GoalPriority = GoalPriority.MEDIUM,
                         due_date: Optional[datetime] = None,
                         success_criteria: List[str] = None,
                         dependencies: List[str] = None,
                         tags: List[str] = None,
                         metadata: Dict[str, Any] = None) -> str:
        """
        Create a new goal
        """
        goal_id = str(uuid.uuid4())
        
        goal = Goal(
            id=goal_id,
            title=title,
            description=description,
            goal_type=goal_type,
            priority=priority,
            status=GoalStatus.PENDING,
            agent_id=agent_id,
            created_at=datetime.now(),
            due_date=due_date,
            success_criteria=success_criteria or [],
            dependencies=dependencies or [],
            tags=tags or [],
            metadata=metadata or {}
        )
        
        self.goals[goal_id] = goal
        self._save_goal(goal)
        
        logger.info(f"Created goal {goal_id}: {title}")
        return goal_id
    
    async def update_goal_progress(self, 
                                  goal_id: str, 
                                  progress: float,
                                  notes: str = "",
                                  evidence: Dict[str, Any] = None) -> bool:
        """
        Update goal progress
        """
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        
        # Update goal progress
        goal.progress = min(100.0, max(0.0, progress))
        
        # Update status based on progress
        if goal.progress >= 100.0 and goal.status == GoalStatus.IN_PROGRESS:
            goal.status = GoalStatus.COMPLETED
            goal.completed_at = datetime.now()
        elif goal.progress > 0 and goal.status == GoalStatus.PENDING:
            goal.status = GoalStatus.IN_PROGRESS
        
        # Save goal
        self._save_goal(goal)
        
        # Create progress record
        progress_record = GoalProgress(
            goal_id=goal_id,
            progress=progress,
            metric_type=goal.progress_metric,
            timestamp=datetime.now(),
            notes=notes,
            evidence=evidence or {}
        )
        
        self.progress_history.append(progress_record)
        self._save_progress(progress_record)
        
        logger.info(f"Updated progress for goal {goal_id}: {progress}%")
        return True
    
    async def complete_goal(self, 
                           goal_id: str,
                           success_criteria_met: List[str] = None,
                           evidence: Dict[str, Any] = None,
                           notes: str = "") -> bool:
        """
        Mark a goal as completed
        """
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        
        # Update goal
        goal.status = GoalStatus.COMPLETED
        goal.progress = 100.0
        goal.completed_at = datetime.now()
        
        self._save_goal(goal)
        
        # Create achievement record
        achievement = GoalAchievement(
            goal_id=goal_id,
            achieved_at=datetime.now(),
            success_criteria_met=success_criteria_met or goal.success_criteria,
            evidence=evidence or {},
            notes=notes
        )
        
        self.achievements.append(achievement)
        self._save_achievement(achievement)
        
        logger.info(f"Completed goal {goal_id}: {goal.title}")
        return True
    
    async def fail_goal(self, 
                       goal_id: str,
                       reason: str = "",
                       evidence: Dict[str, Any] = None) -> bool:
        """
        Mark a goal as failed
        """
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        goal.status = GoalStatus.FAILED
        
        self._save_goal(goal)
        
        logger.info(f"Failed goal {goal_id}: {goal.title} - {reason}")
        return True
    
    async def pause_goal(self, goal_id: str, reason: str = "") -> bool:
        """
        Pause a goal
        """
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        goal.status = GoalStatus.PAUSED
        
        self._save_goal(goal)
        
        logger.info(f"Paused goal {goal_id}: {goal.title} - {reason}")
        return True
    
    async def resume_goal(self, goal_id: str) -> bool:
        """
        Resume a paused goal
        """
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        if goal.status == GoalStatus.PAUSED:
            goal.status = GoalStatus.IN_PROGRESS
            self._save_goal(goal)
            logger.info(f"Resumed goal {goal_id}: {goal.title}")
            return True
        
        return False
    
    async def cancel_goal(self, goal_id: str, reason: str = "") -> bool:
        """
        Cancel a goal
        """
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        goal.status = GoalStatus.CANCELLED
        
        self._save_goal(goal)
        
        logger.info(f"Cancelled goal {goal_id}: {goal.title} - {reason}")
        return True
    
    def get_goals(self, 
                  agent_id: str = None,
                  status: GoalStatus = None,
                  priority: GoalPriority = None,
                  goal_type: GoalType = None,
                  limit: int = 100) -> List[Goal]:
        """
        Get goals with optional filters
        """
        goals = list(self.goals.values())
        
        # Apply filters
        if agent_id:
            goals = [g for g in goals if g.agent_id == agent_id]
        
        if status:
            goals = [g for g in goals if g.status == status]
        
        if priority:
            goals = [g for g in goals if g.priority == priority]
        
        if goal_type:
            goals = [g for g in goals if g.goal_type == goal_type]
        
        # Sort by priority and created date
        goals.sort(key=lambda x: (x.priority.value, x.created_at), reverse=True)
        
        return goals[:limit]
    
    def get_goal_progress(self, goal_id: str) -> List[GoalProgress]:
        """
        Get progress history for a goal
        """
        return [p for p in self.progress_history if p.goal_id == goal_id]
    
    def get_overdue_goals(self) -> List[Goal]:
        """
        Get goals that are overdue
        """
        now = datetime.now()
        overdue = []
        
        for goal in self.goals.values():
            if (goal.due_date and 
                goal.due_date < now and 
                goal.status in [GoalStatus.PENDING, GoalStatus.IN_PROGRESS]):
                overdue.append(goal)
        
        return overdue
    
    def get_goal_statistics(self) -> GoalStats:
        """
        Get goal statistics
        """
        goals = list(self.goals.values())
        
        # Count by status
        status_counts = {}
        for status in GoalStatus:
            status_counts[status.value] = len([g for g in goals if g.status == status])
        
        # Count by priority
        priority_counts = {}
        for priority in GoalPriority:
            priority_counts[priority.value] = len([g for g in goals if g.priority == priority])
        
        # Count by type
        type_counts = {}
        for goal_type in GoalType:
            type_counts[goal_type.value] = len([g for g in goals if g.goal_type == goal_type])
        
        # Calculate completion rate
        completed_goals = len([g for g in goals if g.status == GoalStatus.COMPLETED])
        total_goals = len(goals)
        completion_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0
        
        # Calculate average completion time
        completed_with_times = [g for g in goals if g.status == GoalStatus.COMPLETED and g.completed_at]
        if completed_with_times:
            total_time = sum((g.completed_at - g.created_at).total_seconds() for g in completed_with_times)
            avg_completion_time = total_time / len(completed_with_times) / 3600  # Convert to hours
        else:
            avg_completion_time = 0
        
        # Count overdue goals
        overdue_count = len(self.get_overdue_goals())
        
        # Count active goals
        active_count = len([g for g in goals if g.status in [GoalStatus.PENDING, GoalStatus.IN_PROGRESS]])
        
        return GoalStats(
            total_goals=total_goals,
            goals_by_status=status_counts,
            goals_by_priority=priority_counts,
            goals_by_type=type_counts,
            completion_rate=completion_rate,
            average_completion_time=avg_completion_time,
            overdue_goals=overdue_count,
            active_goals=active_count
        )
    
    async def export_goals(self, 
                          agent_id: str = None,
                          format: str = "json") -> str:
        """
        Export goals data
        """
        goals = self.get_goals(agent_id=agent_id, limit=10000)
        
        if format == "json":
            return json.dumps([asdict(g) for g in goals], indent=2, default=str)
        else:
            # CSV format
            lines = ["id,title,description,goal_type,priority,status,agent_id,created_at,due_date,progress"]
            for goal in goals:
                lines.append(f"{goal.id},{goal.title},{goal.description},{goal.goal_type.value},{goal.priority.value},{goal.status.value},{goal.agent_id},{goal.created_at.isoformat()},{goal.due_date.isoformat() if goal.due_date else ''},{goal.progress}")
            return "\n".join(lines)

# Example usage and testing
async def test_goal_framework():
    """Test the goal framework"""
    framework = GoalFramework()
    
    # Create a test goal
    goal_id = await framework.create_goal(
        "Learn Python",
        "Master Python programming language",
        GoalType.LEARNING,
        "agent1",
        priority=GoalPriority.HIGH,
        success_criteria=["Complete 10 exercises", "Build a project"]
    )
    
    # Update progress
    await framework.update_goal_progress(goal_id, 50.0, "Halfway through exercises")
    
    # Complete goal
    await framework.complete_goal(goal_id, ["Completed 10 exercises", "Built a project"])
    
    # Get statistics
    stats = framework.get_goal_statistics()
    print(f"Total goals: {stats.total_goals}")
    print(f"Completion rate: {stats.completion_rate:.1f}%")

if __name__ == "__main__":
    asyncio.run(test_goal_framework())
