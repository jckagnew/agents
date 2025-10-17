"""
Pattern 20: Agent Swarming - Coordinated Multi-Agent Behavior

This framework provides swarming capabilities for AI agents,
including swarm coordination, collective intelligence, emergent behavior,
swarm algorithms, and distributed decision making.
"""

import asyncio
import json
import logging
import random
import sqlite3
import tempfile
import threading
import time
import uuid
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SwarmAlgorithm(str, Enum):
    """Swarm intelligence algorithms"""
    PARTICLE_SWARM_OPTIMIZATION = "particle_swarm_optimization"
    ANT_COLONY_OPTIMIZATION = "ant_colony_optimization"
    BEE_ALGORITHM = "bee_algorithm"
    FIREFLY_ALGORITHM = "firefly_algorithm"
    BAT_ALGORITHM = "bat_algorithm"
    CUCKOO_SEARCH = "cuckoo_search"
    FLOCKING = "flocking"
    CUSTOM = "custom"


class SwarmRole(str, Enum):
    """Roles within a swarm"""
    LEADER = "leader"
    FOLLOWER = "follower"
    SCOUT = "scout"
    WORKER = "worker"
    COORDINATOR = "coordinator"
    OBSERVER = "observer"
    SPECIALIST = "specialist"


class SwarmBehavior(str, Enum):
    """Swarm behaviors"""
    EXPLORATION = "exploration"
    EXPLOITATION = "exploitation"
    CONVERGENCE = "convergence"
    DIVERGENCE = "divergence"
    COOPERATION = "cooperation"
    COMPETITION = "competition"
    ADAPTATION = "adaptation"
    EMERGENCE = "emergence"


class SwarmStatus(str, Enum):
    """Status of swarm operations"""
    FORMING = "forming"
    ACTIVE = "active"
    CONVERGING = "converging"
    CONVERGED = "converged"
    DIVERGING = "diverging"
    DISPERSING = "dispersing"
    DISPERSED = "dispersed"
    FAILED = "failed"


class SwarmAgent(BaseModel):
    """Represents an agent within a swarm"""
    id: str
    swarm_id: str
    role: SwarmRole
    position: Dict[str, float]  # Spatial position
    velocity: Dict[str, float]  # Movement velocity
    fitness: float
    capabilities: List[str] = Field(default_factory=list)
    communication_range: float
    influence_radius: float
    energy_level: float
    state: Dict[str, Any] = Field(default_factory=dict)
    neighbors: List[str] = Field(default_factory=list)
    messages_sent: int = 0
    messages_received: int = 0
    created_at: datetime
    updated_at: datetime


class Swarm(BaseModel):
    """Represents a swarm of agents"""
    id: str
    name: str
    description: str
    algorithm: SwarmAlgorithm
    behavior: SwarmBehavior
    status: SwarmStatus
    agents: List[str] = Field(default_factory=list)
    leader_id: Optional[str] = None
    target_position: Optional[Dict[str, float]] = None
    objective: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    performance_metrics: Dict[str, float] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class SwarmEvent(BaseModel):
    """Represents an event in swarm operations"""
    id: str
    swarm_id: str
    event_type: str
    agent_id: Optional[str]
    description: str
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime


class SwarmMetrics(BaseModel):
    """Metrics for swarm performance"""
    total_swarms: int
    active_swarms: int
    total_agents: int
    average_swarm_size: float
    average_fitness: float
    best_fitness: float
    convergence_rate: float
    communication_efficiency: float
    coordination_effectiveness: float
    emergent_behaviors: int
    last_swarm_activity: Optional[datetime]


class SwarmingFramework:
    """Framework for agent swarming and collective intelligence"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the swarming framework"""
        self.config = config or {}
        self.storage_path = Path(self.config.get("storage_path", "swarming_data"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Threading and concurrency
        self.lock = threading.Lock()
        self.db_lock = threading.Lock()
        
        # Database setup
        self.db_path = self.storage_path / "swarming.db"
        self._init_database()
        
        # Core data structures
        self.agents: Dict[str, SwarmAgent] = {}
        self.swarms: Dict[str, Swarm] = {}
        self.events: Dict[str, SwarmEvent] = {}
        
        # Load existing data
        self._load_agents()
        self._load_swarms()
        self._load_events()
        
        # Background processing
        self.swarming_processor_running = False
        self.swarming_queue = []
        
        logger.info("Swarming framework initialized")
    
    def _init_database(self):
        """Initialize the swarming database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                # Create tables
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS swarm_agents (
                        id TEXT PRIMARY KEY,
                        swarm_id TEXT NOT NULL,
                        role TEXT NOT NULL,
                        position TEXT NOT NULL,
                        velocity TEXT NOT NULL,
                        fitness REAL NOT NULL,
                        capabilities TEXT,
                        communication_range REAL NOT NULL,
                        influence_radius REAL NOT NULL,
                        energy_level REAL NOT NULL,
                        state TEXT,
                        neighbors TEXT,
                        messages_sent INTEGER NOT NULL,
                        messages_received INTEGER NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS swarms (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT NOT NULL,
                        algorithm TEXT NOT NULL,
                        behavior TEXT NOT NULL,
                        status TEXT NOT NULL,
                        agents TEXT,
                        leader_id TEXT,
                        target_position TEXT,
                        objective TEXT NOT NULL,
                        parameters TEXT,
                        performance_metrics TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS swarm_events (
                        id TEXT PRIMARY KEY,
                        swarm_id TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        agent_id TEXT,
                        description TEXT NOT NULL,
                        data TEXT,
                        timestamp TEXT NOT NULL
                    )
                """)
                
                conn.commit()
                conn.close()
                logger.info("Swarming database initialized")
            except Exception as e:
                logger.error(f"Error initializing swarming database: {e}")
    
    def _load_agents(self):
        """Load swarm agents from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM swarm_agents")
                rows = cursor.fetchall()
                
                for row in rows:
                    agent = SwarmAgent(
                        id=row[0],
                        swarm_id=row[1],
                        role=SwarmRole(row[2]),
                        position=json.loads(row[3]),
                        velocity=json.loads(row[4]),
                        fitness=row[5],
                        capabilities=json.loads(row[6]) if row[6] else [],
                        communication_range=row[7],
                        influence_radius=row[8],
                        energy_level=row[9],
                        state=json.loads(row[10]) if row[10] else {},
                        neighbors=json.loads(row[11]) if row[11] else [],
                        messages_sent=row[12],
                        messages_received=row[13],
                        created_at=datetime.fromisoformat(row[14]),
                        updated_at=datetime.fromisoformat(row[15])
                    )
                    self.agents[agent.id] = agent
                
                conn.close()
                logger.info(f"Loaded {len(self.agents)} swarm agents")
            except Exception as e:
                logger.error(f"Error loading swarm agents: {e}")
    
    def _load_swarms(self):
        """Load swarms from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM swarms")
                rows = cursor.fetchall()
                
                for row in rows:
                    swarm = Swarm(
                        id=row[0],
                        name=row[1],
                        description=row[2],
                        algorithm=SwarmAlgorithm(row[3]),
                        behavior=SwarmBehavior(row[4]),
                        status=SwarmStatus(row[5]),
                        agents=json.loads(row[6]) if row[6] else [],
                        leader_id=row[7],
                        target_position=json.loads(row[8]) if row[8] else None,
                        objective=row[9],
                        parameters=json.loads(row[10]) if row[10] else {},
                        performance_metrics=json.loads(row[11]) if row[11] else {},
                        created_at=datetime.fromisoformat(row[12]),
                        updated_at=datetime.fromisoformat(row[13])
                    )
                    self.swarms[swarm.id] = swarm
                
                conn.close()
                logger.info(f"Loaded {len(self.swarms)} swarms")
            except Exception as e:
                logger.error(f"Error loading swarms: {e}")
    
    def _load_events(self):
        """Load swarm events from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM swarm_events")
                rows = cursor.fetchall()
                
                for row in rows:
                    event = SwarmEvent(
                        id=row[0],
                        swarm_id=row[1],
                        event_type=row[2],
                        agent_id=row[3],
                        description=row[4],
                        data=json.loads(row[5]) if row[5] else {},
                        timestamp=datetime.fromisoformat(row[6])
                    )
                    self.events[event.id] = event
                
                conn.close()
                logger.info(f"Loaded {len(self.events)} swarm events")
            except Exception as e:
                logger.error(f"Error loading swarm events: {e}")
    
    def _save_agent(self, agent: SwarmAgent):
        """Save swarm agent to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO swarm_agents 
                    (id, swarm_id, role, position, velocity, fitness, capabilities,
                     communication_range, influence_radius, energy_level, state,
                     neighbors, messages_sent, messages_received, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    agent.id, agent.swarm_id, agent.role.value,
                    json.dumps(agent.position), json.dumps(agent.velocity),
                    agent.fitness, json.dumps(agent.capabilities),
                    agent.communication_range, agent.influence_radius,
                    agent.energy_level, json.dumps(agent.state),
                    json.dumps(agent.neighbors), agent.messages_sent,
                    agent.messages_received, agent.created_at.isoformat(),
                    agent.updated_at.isoformat()
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving agent {agent.id}: {e}")
    
    def _save_swarm(self, swarm: Swarm):
        """Save swarm to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO swarms 
                    (id, name, description, algorithm, behavior, status, agents,
                     leader_id, target_position, objective, parameters,
                     performance_metrics, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    swarm.id, swarm.name, swarm.description,
                    swarm.algorithm.value, swarm.behavior.value, swarm.status.value,
                    json.dumps(swarm.agents), swarm.leader_id,
                    json.dumps(swarm.target_position) if swarm.target_position else None,
                    swarm.objective, json.dumps(swarm.parameters),
                    json.dumps(swarm.performance_metrics),
                    swarm.created_at.isoformat(), swarm.updated_at.isoformat()
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving swarm {swarm.id}: {e}")
    
    def _save_event(self, event: SwarmEvent):
        """Save swarm event to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO swarm_events 
                    (id, swarm_id, event_type, agent_id, description, data, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.id, event.swarm_id, event.event_type, event.agent_id,
                    event.description, json.dumps(event.data), event.timestamp.isoformat()
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving event {event.id}: {e}")
    
    def create_swarm(self, name: str, description: str, algorithm: SwarmAlgorithm,
                    behavior: SwarmBehavior, objective: str,
                    parameters: Optional[Dict[str, Any]] = None) -> str:
        """Create a new swarm"""
        swarm_id = str(uuid.uuid4())
        swarm = Swarm(
            id=swarm_id,
            name=name,
            description=description,
            algorithm=algorithm,
            behavior=behavior,
            status=SwarmStatus.FORMING,
            agents=[],
            leader_id=None,
            target_position=None,
            objective=objective,
            parameters=parameters or {},
            performance_metrics={},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with self.lock:
            self.swarms[swarm_id] = swarm
            self._save_swarm(swarm)
        
        logger.info(f"Created swarm {swarm_id}: {name}")
        return swarm_id
    
    def add_agent_to_swarm(self, swarm_id: str, role: SwarmRole,
                          position: Optional[Dict[str, float]] = None,
                          capabilities: Optional[List[str]] = None) -> str:
        """Add an agent to a swarm"""
        if swarm_id not in self.swarms:
            return None
        
        agent_id = str(uuid.uuid4())
        
        # Generate random position if not provided
        if position is None:
            position = {
                "x": random.uniform(-100, 100),
                "y": random.uniform(-100, 100),
                "z": random.uniform(-10, 10)
            }
        
        agent = SwarmAgent(
            id=agent_id,
            swarm_id=swarm_id,
            role=role,
            position=position,
            velocity={"x": 0.0, "y": 0.0, "z": 0.0},
            fitness=0.0,
            capabilities=capabilities or [],
            communication_range=50.0,
            influence_radius=25.0,
            energy_level=100.0,
            state={},
            neighbors=[],
            messages_sent=0,
            messages_received=0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with self.lock:
            self.agents[agent_id] = agent
            self.swarms[swarm_id].agents.append(agent_id)
            
            # Set as leader if first agent or if role is leader
            if role == SwarmRole.LEADER or len(self.swarms[swarm_id].agents) == 1:
                self.swarms[swarm_id].leader_id = agent_id
            
            self._save_agent(agent)
            self._save_swarm(self.swarms[swarm_id])
        
        logger.info(f"Added agent {agent_id} to swarm {swarm_id}")
        return agent_id
    
    def start_swarm_operation(self, swarm_id: str) -> bool:
        """Start swarm operations"""
        if swarm_id not in self.swarms:
            return False
        
        swarm = self.swarms[swarm_id]
        if swarm.status != SwarmStatus.FORMING:
            return False
        
        # Update status
        swarm.status = SwarmStatus.ACTIVE
        swarm.updated_at = datetime.now()
        self._save_swarm(swarm)
        
        # Add to processing queue
        self.swarming_queue.append({
            "type": "run_swarm",
            "swarm_id": swarm_id
        })
        
        logger.info(f"Started swarm operation {swarm_id}")
        return True
    
    def update_agent_position(self, agent_id: str, new_position: Dict[str, float],
                            new_velocity: Optional[Dict[str, float]] = None) -> bool:
        """Update agent position and velocity"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        agent.position = new_position
        if new_velocity:
            agent.velocity = new_velocity
        agent.updated_at = datetime.now()
        
        with self.lock:
            self._save_agent(agent)
        
        return True
    
    def update_agent_fitness(self, agent_id: str, fitness: float) -> bool:
        """Update agent fitness"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        agent.fitness = fitness
        agent.updated_at = datetime.now()
        
        with self.lock:
            self._save_agent(agent)
        
        return True
    
    def find_neighbors(self, agent_id: str, max_distance: Optional[float] = None) -> List[str]:
        """Find neighboring agents within communication range"""
        if agent_id not in self.agents:
            return []
        
        agent = self.agents[agent_id]
        swarm_agents = [a for a in self.agents.values() if a.swarm_id == agent.swarm_id and a.id != agent_id]
        
        neighbors = []
        for other_agent in swarm_agents:
            distance = self._calculate_distance(agent.position, other_agent.position)
            max_dist = max_distance or agent.communication_range
            
            if distance <= max_dist:
                neighbors.append(other_agent.id)
        
        # Update neighbors list
        agent.neighbors = neighbors
        agent.updated_at = datetime.now()
        
        with self.lock:
            self._save_agent(agent)
        
        return neighbors
    
    def send_swarm_message(self, sender_id: str, receiver_id: str, message: Dict[str, Any]) -> bool:
        """Send a message between swarm agents"""
        if sender_id not in self.agents or receiver_id not in self.agents:
            return False
        
        sender = self.agents[sender_id]
        receiver = self.agents[receiver_id]
        
        # Check if agents are in the same swarm
        if sender.swarm_id != receiver.swarm_id:
            return False
        
        # Check communication range
        distance = self._calculate_distance(sender.position, receiver.position)
        if distance > sender.communication_range:
            return False
        
        # Update message counts
        sender.messages_sent += 1
        receiver.messages_received += 1
        sender.updated_at = datetime.now()
        receiver.updated_at = datetime.now()
        
        with self.lock:
            self._save_agent(sender)
            self._save_agent(receiver)
        
        logger.info(f"Message sent from {sender_id} to {receiver_id}")
        return True
    
    def apply_swarm_algorithm(self, swarm_id: str) -> bool:
        """Apply the swarm algorithm to update agent positions"""
        if swarm_id not in self.swarms:
            return False
        
        swarm = self.swarms[swarm_id]
        swarm_agents = [self.agents[aid] for aid in swarm.agents if aid in self.agents]
        
        if not swarm_agents:
            return False
        
        # Apply algorithm-specific updates
        if swarm.algorithm == SwarmAlgorithm.PARTICLE_SWARM_OPTIMIZATION:
            self._apply_pso(swarm, swarm_agents)
        elif swarm.algorithm == SwarmAlgorithm.ANT_COLONY_OPTIMIZATION:
            self._apply_aco(swarm, swarm_agents)
        elif swarm.algorithm == SwarmAlgorithm.FLOCKING:
            self._apply_flocking(swarm, swarm_agents)
        else:
            self._apply_generic_swarm(swarm, swarm_agents)
        
        # Update swarm status
        self._update_swarm_status(swarm)
        
        return True
    
    def _apply_pso(self, swarm: Swarm, agents: List[SwarmAgent]):
        """Apply Particle Swarm Optimization algorithm"""
        # PSO parameters
        w = swarm.parameters.get("inertia_weight", 0.9)
        c1 = swarm.parameters.get("cognitive_weight", 2.0)
        c2 = swarm.parameters.get("social_weight", 2.0)
        
        # Find best global position
        best_agent = max(agents, key=lambda a: a.fitness)
        global_best = best_agent.position
        
        for agent in agents:
            # Update velocity
            for dim in agent.velocity:
                r1, r2 = random.random(), random.random()
                cognitive = c1 * r1 * (agent.state.get("best_position", {}).get(dim, 0) - agent.position[dim])
                social = c2 * r2 * (global_best[dim] - agent.position[dim])
                agent.velocity[dim] = w * agent.velocity[dim] + cognitive + social
            
            # Update position
            for dim in agent.position:
                agent.position[dim] += agent.velocity[dim]
            
            # Update personal best
            if agent.fitness > agent.state.get("best_fitness", 0):
                agent.state["best_fitness"] = agent.fitness
                agent.state["best_position"] = agent.position.copy()
            
            agent.updated_at = datetime.now()
            self._save_agent(agent)
    
    def _apply_aco(self, swarm: Swarm, agents: List[SwarmAgent]):
        """Apply Ant Colony Optimization algorithm"""
        # ACO parameters
        alpha = swarm.parameters.get("alpha", 1.0)
        beta = swarm.parameters.get("beta", 2.0)
        rho = swarm.parameters.get("evaporation_rate", 0.1)
        
        # Update pheromone trails (simplified)
        for agent in agents:
            # Move towards target if available
            if swarm.target_position:
                direction = self._calculate_direction(agent.position, swarm.target_position)
                for dim in agent.velocity:
                    agent.velocity[dim] = direction[dim] * 0.1
                    agent.position[dim] += agent.velocity[dim]
            
            agent.updated_at = datetime.now()
            self._save_agent(agent)
    
    def _apply_flocking(self, swarm: Swarm, agents: List[SwarmAgent]):
        """Apply flocking behavior algorithm"""
        # Flocking parameters
        separation_weight = swarm.parameters.get("separation_weight", 1.0)
        alignment_weight = swarm.parameters.get("alignment_weight", 1.0)
        cohesion_weight = swarm.parameters.get("cohesion_weight", 1.0)
        
        for agent in agents:
            neighbors = self.find_neighbors(agent.id)
            neighbor_agents = [self.agents[nid] for nid in neighbors if nid in self.agents]
            
            if not neighbor_agents:
                continue
            
            # Calculate flocking forces
            separation = self._calculate_separation(agent, neighbor_agents)
            alignment = self._calculate_alignment(agent, neighbor_agents)
            cohesion = self._calculate_cohesion(agent, neighbor_agents)
            
            # Update velocity
            for dim in agent.velocity:
                agent.velocity[dim] = (
                    separation_weight * separation[dim] +
                    alignment_weight * alignment[dim] +
                    cohesion_weight * cohesion[dim]
                )
                agent.position[dim] += agent.velocity[dim]
            
            agent.updated_at = datetime.now()
            self._save_agent(agent)
    
    def _apply_generic_swarm(self, swarm: Swarm, agents: List[SwarmAgent]):
        """Apply generic swarm behavior"""
        for agent in agents:
            # Simple random walk
            for dim in agent.velocity:
                agent.velocity[dim] = random.uniform(-1, 1)
                agent.position[dim] += agent.velocity[dim]
            
            agent.updated_at = datetime.now()
            self._save_agent(agent)
    
    def _calculate_distance(self, pos1: Dict[str, float], pos2: Dict[str, float]) -> float:
        """Calculate Euclidean distance between two positions"""
        return sum((pos1[dim] - pos2[dim]) ** 2 for dim in pos1) ** 0.5
    
    def _calculate_direction(self, from_pos: Dict[str, float], to_pos: Dict[str, float]) -> Dict[str, float]:
        """Calculate direction vector from one position to another"""
        distance = self._calculate_distance(from_pos, to_pos)
        if distance == 0:
            return {dim: 0.0 for dim in from_pos}
        
        return {dim: (to_pos[dim] - from_pos[dim]) / distance for dim in from_pos}
    
    def _calculate_separation(self, agent: SwarmAgent, neighbors: List[SwarmAgent]) -> Dict[str, float]:
        """Calculate separation force for flocking"""
        separation = {dim: 0.0 for dim in agent.position}
        
        for neighbor in neighbors:
            distance = self._calculate_distance(agent.position, neighbor.position)
            if distance > 0:
                direction = self._calculate_direction(agent.position, neighbor.position)
                for dim in separation:
                    separation[dim] -= direction[dim] / (distance ** 2)
        
        return separation
    
    def _calculate_alignment(self, agent: SwarmAgent, neighbors: List[SwarmAgent]) -> Dict[str, float]:
        """Calculate alignment force for flocking"""
        if not neighbors:
            return {dim: 0.0 for dim in agent.velocity}
        
        avg_velocity = {dim: 0.0 for dim in agent.velocity}
        for neighbor in neighbors:
            for dim in avg_velocity:
                avg_velocity[dim] += neighbor.velocity[dim]
        
        for dim in avg_velocity:
            avg_velocity[dim] /= len(neighbors)
            avg_velocity[dim] -= agent.velocity[dim]
        
        return avg_velocity
    
    def _calculate_cohesion(self, agent: SwarmAgent, neighbors: List[SwarmAgent]) -> Dict[str, float]:
        """Calculate cohesion force for flocking"""
        if not neighbors:
            return {dim: 0.0 for dim in agent.position}
        
        center = {dim: 0.0 for dim in agent.position}
        for neighbor in neighbors:
            for dim in center:
                center[dim] += neighbor.position[dim]
        
        for dim in center:
            center[dim] /= len(neighbors)
            center[dim] -= agent.position[dim]
        
        return center
    
    def _update_swarm_status(self, swarm: Swarm):
        """Update swarm status based on current state"""
        swarm_agents = [self.agents[aid] for aid in swarm.agents if aid in self.agents]
        
        if not swarm_agents:
            swarm.status = SwarmStatus.FAILED
        else:
            # Check for convergence
            positions = [agent.position for agent in swarm_agents]
            if self._check_convergence(positions):
                swarm.status = SwarmStatus.CONVERGED
            else:
                swarm.status = SwarmStatus.ACTIVE
        
        swarm.updated_at = datetime.now()
        self._save_swarm(swarm)
    
    def _check_convergence(self, positions: List[Dict[str, float]], threshold: float = 10.0) -> bool:
        """Check if agents have converged"""
        if len(positions) < 2:
            return True
        
        # Calculate average position
        avg_pos = {dim: sum(pos[dim] for pos in positions) / len(positions) for dim in positions[0]}
        
        # Check if all agents are within threshold of average
        for pos in positions:
            distance = self._calculate_distance(pos, avg_pos)
            if distance > threshold:
                return False
        
        return True
    
    def get_swarm_metrics(self) -> SwarmMetrics:
        """Get swarm performance metrics"""
        with self.lock:
            total_swarms = len(self.swarms)
            active_swarms = len([s for s in self.swarms.values() if s.status == SwarmStatus.ACTIVE])
            total_agents = len(self.agents)
            
            if self.swarms:
                average_swarm_size = sum(len(s.agents) for s in self.swarms.values()) / len(self.swarms)
            else:
                average_swarm_size = 0.0
            
            if self.agents:
                average_fitness = sum(agent.fitness for agent in self.agents.values()) / len(self.agents)
                best_fitness = max(agent.fitness for agent in self.agents.values())
            else:
                average_fitness = 0.0
                best_fitness = 0.0
            
            # Calculate convergence rate
            converged_swarms = len([s for s in self.swarms.values() if s.status == SwarmStatus.CONVERGED])
            convergence_rate = converged_swarms / max(1, total_swarms)
            
            # Calculate communication efficiency (simplified)
            total_messages = sum(agent.messages_sent for agent in self.agents.values())
            communication_efficiency = min(total_messages / max(1, total_agents), 1.0)
            
            # Calculate coordination effectiveness (simplified)
            coordination_effectiveness = 0.8  # Placeholder
            
            # Count emergent behaviors (simplified)
            emergent_behaviors = len([s for s in self.swarms.values() if s.status == SwarmStatus.CONVERGED])
            
            last_swarm_activity = max([s.updated_at for s in self.swarms.values()], default=None)
            
            return SwarmMetrics(
                total_swarms=total_swarms,
                active_swarms=active_swarms,
                total_agents=total_agents,
                average_swarm_size=average_swarm_size,
                average_fitness=average_fitness,
                best_fitness=best_fitness,
                convergence_rate=convergence_rate,
                communication_efficiency=communication_efficiency,
                coordination_effectiveness=coordination_effectiveness,
                emergent_behaviors=emergent_behaviors,
                last_swarm_activity=last_swarm_activity
            )
    
    def start_swarming_processing(self):
        """Start the swarming processing background thread"""
        if not self.swarming_processor_running:
            self.swarming_processor_running = True
            self.swarming_thread = threading.Thread(target=self._process_swarming_queue, daemon=True)
            self.swarming_thread.start()
            logger.info("Swarming processor started")
    
    def stop_swarming_processing(self):
        """Stop the swarming processing background thread"""
        self.swarming_processor_running = False
        if hasattr(self, 'swarming_thread'):
            self.swarming_thread.join(timeout=1.0)
        logger.info("Swarming processor stopped")
    
    def _process_swarming_queue(self):
        """Process the swarming queue in background"""
        while self.swarming_processor_running:
            try:
                if self.swarming_queue:
                    task = self.swarming_queue.pop(0)
                    self._process_swarming_task(task)
                else:
                    time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error processing swarming task: {e}")
                time.sleep(1.0)
    
    def _process_swarming_task(self, task: Dict[str, Any]):
        """Process a single swarming task"""
        task_type = task.get("type")
        
        if task_type == "run_swarm":
            self._run_swarm_operation(task["swarm_id"])
        elif task_type == "update_positions":
            self._update_all_positions(task["swarm_id"])
        elif task_type == "find_neighbors":
            self._update_all_neighbors(task["swarm_id"])
    
    def _run_swarm_operation(self, swarm_id: str):
        """Run swarm operations"""
        if swarm_id not in self.swarms:
            return
        
        swarm = self.swarms[swarm_id]
        if swarm.status != SwarmStatus.ACTIVE:
            return
        
        # Apply swarm algorithm
        self.apply_swarm_algorithm(swarm_id)
        
        # Update neighbors
        self._update_all_neighbors(swarm_id)
        
        # Update performance metrics
        self._update_swarm_performance(swarm_id)
    
    def _update_all_positions(self, swarm_id: str):
        """Update positions for all agents in swarm"""
        if swarm_id not in self.swarms:
            return
        
        swarm = self.swarms[swarm_id]
        for agent_id in swarm.agents:
            if agent_id in self.agents:
                self.find_neighbors(agent_id)
    
    def _update_all_neighbors(self, swarm_id: str):
        """Update neighbors for all agents in swarm"""
        if swarm_id not in self.swarms:
            return
        
        swarm = self.swarms[swarm_id]
        for agent_id in swarm.agents:
            if agent_id in self.agents:
                self.find_neighbors(agent_id)
    
    def _update_swarm_performance(self, swarm_id: str):
        """Update swarm performance metrics"""
        if swarm_id not in self.swarms:
            return
        
        swarm = self.swarms[swarm_id]
        swarm_agents = [self.agents[aid] for aid in swarm.agents if aid in self.agents]
        
        if swarm_agents:
            avg_fitness = sum(agent.fitness for agent in swarm_agents) / len(swarm_agents)
            best_fitness = max(agent.fitness for agent in swarm_agents)
            
            swarm.performance_metrics.update({
                "average_fitness": avg_fitness,
                "best_fitness": best_fitness,
                "agent_count": len(swarm_agents),
                "last_update": datetime.now().isoformat()
            })
            
            swarm.updated_at = datetime.now()
            self._save_swarm(swarm)
    
    def export_swarming_data(self, format: str = "json") -> Union[str, Dict[str, Any]]:
        """Export swarming data in specified format"""
        with self.lock:
            data = {
                "agents": [agent.dict() for agent in self.agents.values()],
                "swarms": [swarm.dict() for swarm in self.swarms.values()],
                "events": [event.dict() for event in self.events.values()],
                "metrics": self.get_swarm_metrics().dict()
            }
            
            if format == "json":
                return json.dumps(data, indent=2, default=str)
            else:
                return data
    
    def clear_swarming_data(self):
        """Clear all swarming data"""
        with self.lock:
            self.agents.clear()
            self.swarms.clear()
            self.events.clear()
            
            # Clear database
            with self.db_lock:
                try:
                    conn = sqlite3.connect(self.db_path, timeout=10.0)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM swarm_agents")
                    cursor.execute("DELETE FROM swarms")
                    cursor.execute("DELETE FROM swarm_events")
                    conn.commit()
                    conn.close()
                except Exception as e:
                    logger.error(f"Error clearing swarming data: {e}")
            
        logger.info("Cleared all swarming data")


# Example usage and testing
if __name__ == "__main__":
    # Create swarming framework
    framework = SwarmingFramework()
    
    # Test basic functionality
    print("🧪 Testing Pattern 20: Agent Swarming")
    print("=" * 50)
    
    # Create test swarm
    swarm_id = framework.create_swarm(
        "Test Swarm", "Testing swarming capabilities",
        SwarmAlgorithm.FLOCKING, SwarmBehavior.EXPLORATION, "Find optimal solution"
    )
    print(f"✅ Created swarm: {swarm_id}")
    
    # Add agents to swarm
    for i in range(5):
        agent_id = framework.add_agent_to_swarm(swarm_id, SwarmRole.WORKER)
        print(f"✅ Added agent {i+1}: {agent_id}")
    
    # Start swarm operation
    success = framework.start_swarm_operation(swarm_id)
    print(f"✅ Started swarm operation: {success}")
    
    # Get metrics
    metrics = framework.get_swarm_metrics()
    print(f"✅ Swarm metrics: {metrics.total_swarms} swarms, {metrics.total_agents} agents")
    
    print("🎯 Pattern 20: Agent Swarming basic test completed!")

