"""
Pattern 3: Agent Collaboration
Comprehensive agent collaboration and shared workspace management system
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
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CollaborationType(Enum):
    """Types of collaboration"""
    SHARED_WORKSPACE = "shared_workspace"     # Shared workspace collaboration
    PEER_REVIEW = "peer_review"               # Peer review collaboration
    PAIR_PROGRAMMING = "pair_programming"     # Pair programming collaboration
    BRAINSTORMING = "brainstorming"           # Brainstorming session
    DECISION_MAKING = "decision_making"       # Collaborative decision making
    KNOWLEDGE_SHARING = "knowledge_sharing"   # Knowledge sharing session
    MENTORING = "mentoring"                   # Mentoring collaboration
    TEAM_MEETING = "team_meeting"            # Team meeting collaboration

class CollaborationStatus(Enum):
    """Collaboration status states"""
    PLANNING = "planning"                     # Collaboration is being planned
    ACTIVE = "active"                         # Collaboration is active
    PAUSED = "paused"                         # Collaboration is paused
    COMPLETED = "completed"                   # Collaboration is completed
    CANCELLED = "cancelled"                   # Collaboration was cancelled
    ARCHIVED = "archived"                     # Collaboration is archived

class ParticipantRole(Enum):
    """Participant roles in collaboration"""
    LEADER = "leader"                         # Collaboration leader
    CONTRIBUTOR = "contributor"               # Active contributor
    REVIEWER = "reviewer"                     # Reviewer/validator
    OBSERVER = "observer"                     # Observer/spectator
    MENTOR = "mentor"                         # Mentor/advisor
    MENTEE = "mentee"                         # Mentee/learner
    FACILITATOR = "facilitator"              # Session facilitator
    RECORDER = "recorder"                     # Meeting recorder

class ConflictResolutionStrategy(Enum):
    """Conflict resolution strategies"""
    MAJORITY_VOTE = "majority_vote"          # Majority vote decision
    LEADER_DECISION = "leader_decision"       # Leader makes final decision
    CONSENSUS = "consensus"                   # Consensus building
    EXPERT_OPINION = "expert_opinion"         # Expert opinion based
    RANDOM_SELECTION = "random_selection"     # Random selection
    MEDIATION = "mediation"                   # Mediation process
    HIERARCHICAL = "hierarchical"            # Hierarchical decision

@dataclass
class CollaborationParticipant:
    """Individual participant in collaboration"""
    agent_id: str
    role: ParticipantRole
    joined_at: datetime
    permissions: List[str]
    contribution_score: float = 0.0
    last_active: Optional[datetime] = None
    metadata: Dict[str, Any] = None

@dataclass
class SharedWorkspace:
    """Shared workspace definition"""
    id: str
    name: str
    description: str
    collaboration_type: CollaborationType
    participants: List[CollaborationParticipant]
    status: CollaborationStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    shared_resources: Dict[str, Any] = None
    collaboration_rules: Dict[str, Any] = None
    metadata: Dict[str, Any] = None

@dataclass
class CollaborationEvent:
    """Collaboration event definition"""
    id: str
    workspace_id: str
    agent_id: str
    event_type: str
    content: Any
    timestamp: datetime
    metadata: Dict[str, Any] = None

@dataclass
class Conflict:
    """Conflict definition"""
    id: str
    workspace_id: str
    conflicting_agents: List[str]
    conflict_type: str
    description: str
    severity: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    resolution_strategy: Optional[ConflictResolutionStrategy] = None
    resolution_details: Optional[str] = None

@dataclass
class CollaborationMetrics:
    """Collaboration metrics"""
    total_workspaces: int
    active_workspaces: int
    total_participants: int
    average_participants_per_workspace: float
    collaboration_events: int
    conflicts_resolved: int
    average_collaboration_duration: float
    participant_engagement_scores: Dict[str, float]

class CollaborationFramework:
    """
    Comprehensive agent collaboration framework
    Implements Pattern 3 with shared workspaces, collaborative decision making, and conflict resolution
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.workspaces: Dict[str, SharedWorkspace] = {}
        self.events: Dict[str, CollaborationEvent] = {}
        self.conflicts: Dict[str, Conflict] = {}
        self.agent_workspaces: Dict[str, List[str]] = defaultdict(list)
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
        
        # Storage configuration
        self.storage_path = Path(self.config.get("storage_path", "collaboration_storage"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Database connection
        self.db_path = self.storage_path / "collaboration.db"
        self._init_database()
        
        # Threading and concurrency
        self.lock = threading.Lock()
        self.db_lock = threading.Lock()
        
        # Load existing data
        self._load_workspaces()
        self._load_events()
        self._load_conflicts()
        
        # Start background processes
        self._start_background_processes()
    
    def _init_database(self):
        """Initialize SQLite database for persistent storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Workspaces table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workspaces (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                collaboration_type TEXT NOT NULL,
                participants TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                shared_resources TEXT,
                collaboration_rules TEXT,
                metadata TEXT
            )
        ''')
        
        # Events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                metadata TEXT
            )
        ''')
        
        # Conflicts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conflicts (
                id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                conflicting_agents TEXT NOT NULL,
                conflict_type TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT NOT NULL,
                created_at TEXT NOT NULL,
                resolved_at TEXT,
                resolution_strategy TEXT,
                resolution_details TEXT
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_workspaces_status ON workspaces(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_workspace_id ON events(workspace_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_agent_id ON events(agent_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conflicts_workspace_id ON conflicts(workspace_id)')
        
        conn.commit()
        conn.close()
    
    def _load_workspaces(self):
        """Load workspaces from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM workspaces')
        rows = cursor.fetchall()
        
        for row in rows:
            participants_data = json.loads(row[4])
            participants = [
                CollaborationParticipant(
                    agent_id=p["agent_id"],
                    role=ParticipantRole(p["role"]),
                    joined_at=datetime.fromisoformat(p["joined_at"]),
                    permissions=p.get("permissions", []),
                    contribution_score=p.get("contribution_score", 0.0),
                    last_active=datetime.fromisoformat(p["last_active"]) if p.get("last_active") else None,
                    metadata=p.get("metadata", {})
                )
                for p in participants_data
            ]
            
            workspace = SharedWorkspace(
                id=row[0],
                name=row[1],
                description=row[2],
                collaboration_type=CollaborationType(row[3]),
                participants=participants,
                status=CollaborationStatus(row[5]),
                created_at=datetime.fromisoformat(row[6]),
                started_at=datetime.fromisoformat(row[7]) if row[7] else None,
                completed_at=datetime.fromisoformat(row[8]) if row[8] else None,
                shared_resources=json.loads(row[9]) if row[9] else {},
                collaboration_rules=json.loads(row[10]) if row[10] else {},
                metadata=json.loads(row[11]) if row[11] else {}
            )
            self.workspaces[workspace.id] = workspace
            
            # Update agent workspace mapping
            for participant in participants:
                self.agent_workspaces[participant.agent_id].append(workspace.id)
        
        conn.close()
        logger.info(f"Loaded {len(self.workspaces)} workspaces from database")
    
    def _load_events(self):
        """Load events from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM events ORDER BY timestamp DESC LIMIT 10000')
        rows = cursor.fetchall()
        
        for row in rows:
            event = CollaborationEvent(
                id=row[0],
                workspace_id=row[1],
                agent_id=row[2],
                event_type=row[3],
                content=json.loads(row[4]),
                timestamp=datetime.fromisoformat(row[5]),
                metadata=json.loads(row[6]) if row[6] else {}
            )
            self.events[event.id] = event
        
        conn.close()
        logger.info(f"Loaded {len(self.events)} events from database")
    
    def _load_conflicts(self):
        """Load conflicts from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM conflicts')
        rows = cursor.fetchall()
        
        for row in rows:
            conflict = Conflict(
                id=row[0],
                workspace_id=row[1],
                conflicting_agents=json.loads(row[2]),
                conflict_type=row[3],
                description=row[4],
                severity=row[5],
                created_at=datetime.fromisoformat(row[6]),
                resolved_at=datetime.fromisoformat(row[7]) if row[7] else None,
                resolution_strategy=ConflictResolutionStrategy(row[8]) if row[8] else None,
                resolution_details=row[9]
            )
            self.conflicts[conflict.id] = conflict
        
        conn.close()
        logger.info(f"Loaded {len(self.conflicts)} conflicts from database")
    
    def _save_workspace(self, workspace: SharedWorkspace):
        """Save workspace to database"""
        # Skip database saving in test mode to avoid locking issues
        if self.config.get("skip_database", False):
            return
            
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                participants_data = [
                    {
                        "agent_id": p.agent_id,
                        "role": p.role.value,
                        "joined_at": p.joined_at.isoformat(),
                        "permissions": p.permissions,
                        "contribution_score": p.contribution_score,
                        "last_active": p.last_active.isoformat() if p.last_active else None,
                        "metadata": p.metadata
                    }
                    for p in workspace.participants
                ]
                
                cursor.execute('''
                    INSERT OR REPLACE INTO workspaces 
                    (id, name, description, collaboration_type, participants, status, created_at,
                     started_at, completed_at, shared_resources, collaboration_rules, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    workspace.id, workspace.name, workspace.description,
                    workspace.collaboration_type.value, json.dumps(participants_data),
                    workspace.status.value, workspace.created_at.isoformat(),
                    workspace.started_at.isoformat() if workspace.started_at else None,
                    workspace.completed_at.isoformat() if workspace.completed_at else None,
                    json.dumps(workspace.shared_resources), json.dumps(workspace.collaboration_rules),
                    json.dumps(workspace.metadata)
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving workspace {workspace.id}: {e}")
    
    def _save_event(self, event: CollaborationEvent):
        """Save event to database"""
        # Skip database saving in test mode to avoid locking issues
        if self.config.get("skip_database", False):
            return
            
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO events 
                    (id, workspace_id, agent_id, event_type, content, timestamp, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    event.id, event.workspace_id, event.agent_id,
                    event.event_type, json.dumps(event.content),
                    event.timestamp.isoformat(), json.dumps(event.metadata)
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving event {event.id}: {e}")
    
    def _save_conflict(self, conflict: Conflict):
        """Save conflict to database"""
        # Skip database saving in test mode to avoid locking issues
        if self.config.get("skip_database", False):
            return
            
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO conflicts 
                    (id, workspace_id, conflicting_agents, conflict_type, description, severity,
                     created_at, resolved_at, resolution_strategy, resolution_details)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    conflict.id, conflict.workspace_id, json.dumps(conflict.conflicting_agents),
                    conflict.conflict_type, conflict.description, conflict.severity,
                    conflict.created_at.isoformat(),
                    conflict.resolved_at.isoformat() if conflict.resolved_at else None,
                    conflict.resolution_strategy.value if conflict.resolution_strategy else None,
                    conflict.resolution_details
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving conflict {conflict.id}: {e}")
    
    def _start_background_processes(self):
        """Start background collaboration processes"""
        asyncio.create_task(self._collaboration_monitor_loop())
        asyncio.create_task(self._conflict_detection_loop())
        logger.info("Background collaboration processes started")
    
    async def _collaboration_monitor_loop(self):
        """Background collaboration monitoring loop"""
        while True:
            try:
                await self._monitor_collaborations()
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Error in collaboration monitor loop: {e}")
                await asyncio.sleep(60)
    
    async def _monitor_collaborations(self):
        """Monitor active collaborations"""
        now = datetime.now()
        
        for workspace in self.workspaces.values():
            if workspace.status == CollaborationStatus.ACTIVE:
                # Check for inactive participants
                for participant in workspace.participants:
                    if participant.last_active and now - participant.last_active > timedelta(hours=1):
                        await self._emit_event("participant_inactive", {
                            "workspace_id": workspace.id,
                            "agent_id": participant.agent_id,
                            "last_active": participant.last_active.isoformat()
                        })
    
    async def _conflict_detection_loop(self):
        """Background conflict detection loop"""
        while True:
            try:
                await self._detect_conflicts()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in conflict detection loop: {e}")
                await asyncio.sleep(120)
    
    async def _detect_conflicts(self):
        """Detect potential conflicts in active workspaces"""
        for workspace in self.workspaces.values():
            if workspace.status == CollaborationStatus.ACTIVE:
                # Simple conflict detection based on event patterns
                recent_events = [
                    e for e in self.events.values()
                    if e.workspace_id == workspace.id and 
                    e.timestamp > datetime.now() - timedelta(minutes=5)
                ]
                
                # Check for conflicting actions
                conflicting_actions = {}
                for event in recent_events:
                    if event.event_type == "action":
                        action_key = f"{event.agent_id}_{event.content.get('action', '')}"
                        if action_key in conflicting_actions:
                            # Potential conflict detected
                            await self._create_conflict(
                                workspace_id=workspace.id,
                                conflicting_agents=[event.agent_id, conflicting_actions[action_key]],
                                conflict_type="action_conflict",
                                description=f"Conflicting actions detected: {event.content.get('action', '')}",
                                severity="medium"
                            )
                        else:
                            conflicting_actions[action_key] = event.agent_id
    
    async def create_workspace(self, 
                             name: str,
                             description: str,
                             collaboration_type: CollaborationType,
                             creator_agent_id: str,
                             collaboration_rules: Dict[str, Any] = None,
                             metadata: Dict[str, Any] = None) -> str:
        """
        Create a new collaboration workspace
        """
        workspace_id = str(uuid.uuid4())
        
        # Create creator as leader
        creator = CollaborationParticipant(
            agent_id=creator_agent_id,
            role=ParticipantRole.LEADER,
            joined_at=datetime.now(),
            permissions=["read", "write", "admin"],
            metadata={}
        )
        
        workspace = SharedWorkspace(
            id=workspace_id,
            name=name,
            description=description,
            collaboration_type=collaboration_type,
            participants=[creator],
            status=CollaborationStatus.PLANNING,
            created_at=datetime.now(),
            shared_resources={},
            collaboration_rules=collaboration_rules or {},
            metadata=metadata or {}
        )
        
        with self.lock:
            self.workspaces[workspace_id] = workspace
            self.agent_workspaces[creator_agent_id].append(workspace_id)
            self._save_workspace(workspace)
        
        await self._emit_event("workspace_created", {
            "workspace_id": workspace_id,
            "creator_agent_id": creator_agent_id,
            "collaboration_type": collaboration_type.value
        })
        
        logger.info(f"Created workspace {workspace_id}: {name}")
        return workspace_id
    
    async def join_workspace(self, 
                           workspace_id: str,
                           agent_id: str,
                           role: ParticipantRole = ParticipantRole.CONTRIBUTOR,
                           permissions: List[str] = None) -> bool:
        """
        Join an existing workspace
        """
        if workspace_id not in self.workspaces:
            return False
        
        workspace = self.workspaces[workspace_id]
        
        # Check if agent is already a participant
        if any(p.agent_id == agent_id for p in workspace.participants):
            return False
        
        participant = CollaborationParticipant(
            agent_id=agent_id,
            role=role,
            joined_at=datetime.now(),
            permissions=permissions or ["read"],
            metadata={}
        )
        
        with self.lock:
            workspace.participants.append(participant)
            self.agent_workspaces[agent_id].append(workspace_id)
            self._save_workspace(workspace)
        
        await self._emit_event("agent_joined_workspace", {
            "workspace_id": workspace_id,
            "agent_id": agent_id,
            "role": role.value
        })
        
        logger.info(f"Agent {agent_id} joined workspace {workspace_id}")
        return True
    
    async def leave_workspace(self, workspace_id: str, agent_id: str) -> bool:
        """
        Leave a workspace
        """
        if workspace_id not in self.workspaces:
            return False
        
        workspace = self.workspaces[workspace_id]
        
        # Remove participant
        workspace.participants = [p for p in workspace.participants if p.agent_id != agent_id]
        
        with self.lock:
            if workspace_id in self.agent_workspaces[agent_id]:
                self.agent_workspaces[agent_id].remove(workspace_id)
            self._save_workspace(workspace)
        
        await self._emit_event("agent_left_workspace", {
            "workspace_id": workspace_id,
            "agent_id": agent_id
        })
        
        logger.info(f"Agent {agent_id} left workspace {workspace_id}")
        return True
    
    async def start_collaboration(self, workspace_id: str) -> bool:
        """
        Start a collaboration session
        """
        if workspace_id not in self.workspaces:
            return False
        
        workspace = self.workspaces[workspace_id]
        
        if workspace.status != CollaborationStatus.PLANNING:
            return False
        
        workspace.status = CollaborationStatus.ACTIVE
        workspace.started_at = datetime.now()
        
        with self.lock:
            self._save_workspace(workspace)
        
        await self._emit_event("collaboration_started", {
            "workspace_id": workspace_id,
            "participants": [p.agent_id for p in workspace.participants]
        })
        
        logger.info(f"Started collaboration in workspace {workspace_id}")
        return True
    
    async def complete_collaboration(self, workspace_id: str) -> bool:
        """
        Complete a collaboration session
        """
        if workspace_id not in self.workspaces:
            return False
        
        workspace = self.workspaces[workspace_id]
        
        if workspace.status != CollaborationStatus.ACTIVE:
            return False
        
        workspace.status = CollaborationStatus.COMPLETED
        workspace.completed_at = datetime.now()
        
        with self.lock:
            self._save_workspace(workspace)
        
        await self._emit_event("collaboration_completed", {
            "workspace_id": workspace_id,
            "duration": (workspace.completed_at - workspace.started_at).total_seconds() if workspace.started_at else 0
        })
        
        logger.info(f"Completed collaboration in workspace {workspace_id}")
        return True
    
    async def add_shared_resource(self, 
                                workspace_id: str,
                                resource_name: str,
                                resource_data: Any,
                                agent_id: str) -> bool:
        """
        Add a shared resource to workspace
        """
        if workspace_id not in self.workspaces:
            return False
        
        workspace = self.workspaces[workspace_id]
        
        # Check permissions
        participant = next((p for p in workspace.participants if p.agent_id == agent_id), None)
        if not participant or "write" not in participant.permissions:
            return False
        
        workspace.shared_resources[resource_name] = resource_data
        
        with self.lock:
            self._save_workspace(workspace)
        
        await self._emit_event("resource_added", {
            "workspace_id": workspace_id,
            "resource_name": resource_name,
            "agent_id": agent_id
        })
        
        logger.info(f"Added resource {resource_name} to workspace {workspace_id}")
        return True
    
    async def record_collaboration_event(self, 
                                       workspace_id: str,
                                       agent_id: str,
                                       event_type: str,
                                       content: Any,
                                       metadata: Dict[str, Any] = None) -> str:
        """
        Record a collaboration event
        """
        if workspace_id not in self.workspaces:
            return None
        
        event_id = str(uuid.uuid4())
        
        event = CollaborationEvent(
            id=event_id,
            workspace_id=workspace_id,
            agent_id=agent_id,
            event_type=event_type,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        with self.lock:
            self.events[event_id] = event
            self._save_event(event)
            
            # Update participant last active time
            workspace = self.workspaces[workspace_id]
            for participant in workspace.participants:
                if participant.agent_id == agent_id:
                    participant.last_active = datetime.now()
                    break
            self._save_workspace(workspace)
        
        await self._emit_event("collaboration_event", {
            "event_id": event_id,
            "workspace_id": workspace_id,
            "agent_id": agent_id,
            "event_type": event_type
        })
        
        logger.debug(f"Recorded event {event_id} in workspace {workspace_id}")
        return event_id
    
    async def _create_conflict(self, 
                             workspace_id: str,
                             conflicting_agents: List[str],
                             conflict_type: str,
                             description: str,
                             severity: str = "medium") -> str:
        """
        Create a conflict record
        """
        conflict_id = str(uuid.uuid4())
        
        conflict = Conflict(
            id=conflict_id,
            workspace_id=workspace_id,
            conflicting_agents=conflicting_agents,
            conflict_type=conflict_type,
            description=description,
            severity=severity,
            created_at=datetime.now()
        )
        
        with self.lock:
            self.conflicts[conflict_id] = conflict
            self._save_conflict(conflict)
        
        await self._emit_event("conflict_detected", {
            "conflict_id": conflict_id,
            "workspace_id": workspace_id,
            "conflicting_agents": conflicting_agents,
            "conflict_type": conflict_type,
            "severity": severity
        })
        
        logger.warning(f"Created conflict {conflict_id} in workspace {workspace_id}")
        return conflict_id
    
    async def resolve_conflict(self, 
                             conflict_id: str,
                             resolution_strategy: ConflictResolutionStrategy,
                             resolution_details: str,
                             resolver_agent_id: str) -> bool:
        """
        Resolve a conflict
        """
        if conflict_id not in self.conflicts:
            return False
        
        conflict = self.conflicts[conflict_id]
        
        conflict.resolved_at = datetime.now()
        conflict.resolution_strategy = resolution_strategy
        conflict.resolution_details = resolution_details
        
        with self.lock:
            self._save_conflict(conflict)
        
        await self._emit_event("conflict_resolved", {
            "conflict_id": conflict_id,
            "workspace_id": conflict.workspace_id,
            "resolution_strategy": resolution_strategy.value,
            "resolver_agent_id": resolver_agent_id
        })
        
        logger.info(f"Resolved conflict {conflict_id}")
        return True
    
    async def get_workspace_events(self, 
                                 workspace_id: str,
                                 event_types: List[str] = None,
                                 limit: int = 100) -> List[CollaborationEvent]:
        """
        Get events for a workspace
        """
        events = [
            e for e in self.events.values()
            if e.workspace_id == workspace_id
        ]
        
        if event_types:
            events = [e for e in events if e.event_type in event_types]
        
        # Sort by timestamp (newest first)
        events.sort(key=lambda e: e.timestamp, reverse=True)
        
        return events[:limit]
    
    async def get_agent_workspaces(self, agent_id: str) -> List[SharedWorkspace]:
        """
        Get workspaces for an agent
        """
        workspace_ids = self.agent_workspaces.get(agent_id, [])
        return [self.workspaces[wid] for wid in workspace_ids if wid in self.workspaces]
    
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
        self.event_handlers[event_type].append(handler)
    
    def get_collaboration_metrics(self) -> CollaborationMetrics:
        """
        Get collaboration metrics
        """
        workspaces = list(self.workspaces.values())
        events = list(self.events.values())
        conflicts = list(self.conflicts.values())
        
        # Calculate metrics
        total_workspaces = len(workspaces)
        active_workspaces = len([w for w in workspaces if w.status == CollaborationStatus.ACTIVE])
        
        total_participants = sum(len(w.participants) for w in workspaces)
        average_participants = total_participants / total_workspaces if total_workspaces > 0 else 0
        
        collaboration_events = len(events)
        conflicts_resolved = len([c for c in conflicts if c.resolved_at])
        
        # Calculate average collaboration duration
        completed_workspaces = [w for w in workspaces if w.status == CollaborationStatus.COMPLETED and w.started_at and w.completed_at]
        if completed_workspaces:
            total_duration = sum((w.completed_at - w.started_at).total_seconds() for w in completed_workspaces)
            average_duration = total_duration / len(completed_workspaces)
        else:
            average_duration = 0.0
        
        # Calculate participant engagement scores
        participant_engagement = {}
        for workspace in workspaces:
            for participant in workspace.participants:
                if participant.agent_id not in participant_engagement:
                    participant_engagement[participant.agent_id] = []
                participant_engagement[participant.agent_id].append(participant.contribution_score)
        
        engagement_scores = {}
        for agent_id, scores in participant_engagement.items():
            engagement_scores[agent_id] = sum(scores) / len(scores) if scores else 0.0
        
        return CollaborationMetrics(
            total_workspaces=total_workspaces,
            active_workspaces=active_workspaces,
            total_participants=total_participants,
            average_participants_per_workspace=average_participants,
            collaboration_events=collaboration_events,
            conflicts_resolved=conflicts_resolved,
            average_collaboration_duration=average_duration,
            participant_engagement_scores=engagement_scores
        )
    
    async def export_collaboration_data(self, format: str = "json") -> str:
        """
        Export collaboration data
        """
        data = {
            "workspaces": [asdict(w) for w in self.workspaces.values()],
            "events": [asdict(e) for e in self.events.values()],
            "conflicts": [asdict(c) for c in self.conflicts.values()],
            "metrics": asdict(self.get_collaboration_metrics())
        }
        
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        else:
            # CSV format
            lines = ["type,id,name,status,created_at"]
            for workspace in self.workspaces.values():
                lines.append(f"workspace,{workspace.id},{workspace.name},{workspace.status.value},{workspace.created_at.isoformat()}")
            for event in self.events.values():
                lines.append(f"event,{event.id},{event.event_type},{event.workspace_id},{event.timestamp.isoformat()}")
            for conflict in self.conflicts.values():
                lines.append(f"conflict,{conflict.id},{conflict.conflict_type},{conflict.workspace_id},{conflict.created_at.isoformat()}")
            return "\n".join(lines)

# Example usage and testing
async def test_collaboration_framework():
    """Test the collaboration framework"""
    framework = CollaborationFramework()
    
    # Create workspace
    workspace_id = await framework.create_workspace(
        "Test Workspace",
        "A test collaboration workspace",
        CollaborationType.SHARED_WORKSPACE,
        "agent1"
    )
    
    # Join workspace
    await framework.join_workspace(workspace_id, "agent2", ParticipantRole.CONTRIBUTOR)
    
    # Start collaboration
    await framework.start_collaboration(workspace_id)
    
    # Record events
    await framework.record_collaboration_event(workspace_id, "agent1", "action", {"action": "create_document"})
    await framework.record_collaboration_event(workspace_id, "agent2", "comment", {"comment": "Great idea!"})
    
    # Get metrics
    metrics = framework.get_collaboration_metrics()
    print(f"Total workspaces: {metrics.total_workspaces}")
    print(f"Active workspaces: {metrics.active_workspaces}")

if __name__ == "__main__":
    asyncio.run(test_collaboration_framework())
