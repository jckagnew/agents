"""
Pattern 19: Agent Evolution - Adaptive Learning and Self-Improvement

This framework provides evolutionary capabilities for AI agents,
including genetic algorithms, performance optimization, mutation,
crossover, selection, and adaptive behavior modification.
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


class EvolutionStrategy(str, Enum):
    """Evolution strategies for agent improvement"""
    GENETIC_ALGORITHM = "genetic_algorithm"
    PARTICLE_SWARM = "particle_swarm"
    SIMULATED_ANNEALING = "simulated_annealing"
    GRADIENT_DESCENT = "gradient_descent"
    REINFORCEMENT_LEARNING = "reinforcement_learning"
    META_LEARNING = "meta_learning"


class MutationType(str, Enum):
    """Types of mutations for genetic evolution"""
    GAUSSIAN = "gaussian"
    UNIFORM = "uniform"
    POLYNOMIAL = "polynomial"
    ADAPTIVE = "adaptive"
    CUSTOM = "custom"


class SelectionType(str, Enum):
    """Selection strategies for evolution"""
    TOURNAMENT = "tournament"
    RANK_SELECTION = "rank_selection"
    ROULETTE_WHEEL = "roulette_wheel"
    ELITISM = "elitism"
    STOCHASTIC_UNIVERSAL = "stochastic_universal"


class FitnessFunction(str, Enum):
    """Fitness functions for evaluating agent performance"""
    ACCURACY = "accuracy"
    EFFICIENCY = "efficiency"
    ROBUSTNESS = "robustness"
    ADAPTABILITY = "adaptability"
    CREATIVITY = "creativity"
    CUSTOM = "custom"


class EvolutionStatus(str, Enum):
    """Status of evolution process"""
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentGenome(BaseModel):
    """Represents an agent's genetic code"""
    id: str
    agent_id: str
    generation: int
    genes: Dict[str, Any]  # Genetic parameters
    fitness_score: float
    performance_metrics: Dict[str, float]
    mutation_history: List[Dict[str, Any]] = Field(default_factory=list)
    crossover_history: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class EvolutionExperiment(BaseModel):
    """Represents an evolution experiment"""
    id: str
    name: str
    description: str
    strategy: EvolutionStrategy
    population_size: int
    max_generations: int
    fitness_function: FitnessFunction
    mutation_rate: float
    crossover_rate: float
    selection_type: SelectionType
    status: EvolutionStatus
    current_generation: int
    best_fitness: float
    average_fitness: float
    parameters: Dict[str, Any] = Field(default_factory=dict)
    results: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class EvolutionEvent(BaseModel):
    """Represents an event in the evolution process"""
    id: str
    experiment_id: str
    event_type: str
    generation: int
    agent_id: Optional[str]
    description: str
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime


class EvolutionMetrics(BaseModel):
    """Metrics for evolution performance"""
    total_experiments: int
    active_experiments: int
    completed_experiments: int
    total_generations: int
    average_fitness: float
    best_fitness: float
    evolution_speed: float  # Generations per hour
    success_rate: float
    mutation_effectiveness: float
    crossover_effectiveness: float
    last_experiment: Optional[datetime]


class EvolutionFramework:
    """Framework for agent evolution and self-improvement"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the evolution framework"""
        self.config = config or {}
        self.storage_path = Path(self.config.get("storage_path", "evolution_data"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Threading and concurrency
        self.lock = threading.Lock()
        self.db_lock = threading.Lock()
        
        # Database setup
        self.db_path = self.storage_path / "evolution.db"
        self._init_database()
        
        # Core data structures
        self.genomes: Dict[str, AgentGenome] = {}
        self.experiments: Dict[str, EvolutionExperiment] = {}
        self.events: Dict[str, EvolutionEvent] = {}
        
        # Load existing data
        self._load_genomes()
        self._load_experiments()
        self._load_events()
        
        # Background processing
        self.evolution_processor_running = False
        self.evolution_queue = []
        
        logger.info("Evolution framework initialized")
    
    def _init_database(self):
        """Initialize the evolution database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                # Create tables
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS agent_genomes (
                        id TEXT PRIMARY KEY,
                        agent_id TEXT NOT NULL,
                        generation INTEGER NOT NULL,
                        genes TEXT NOT NULL,
                        fitness_score REAL NOT NULL,
                        performance_metrics TEXT NOT NULL,
                        mutation_history TEXT,
                        crossover_history TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS evolution_experiments (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT NOT NULL,
                        strategy TEXT NOT NULL,
                        population_size INTEGER NOT NULL,
                        max_generations INTEGER NOT NULL,
                        fitness_function TEXT NOT NULL,
                        mutation_rate REAL NOT NULL,
                        crossover_rate REAL NOT NULL,
                        selection_type TEXT NOT NULL,
                        status TEXT NOT NULL,
                        current_generation INTEGER NOT NULL,
                        best_fitness REAL NOT NULL,
                        average_fitness REAL NOT NULL,
                        parameters TEXT,
                        results TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS evolution_events (
                        id TEXT PRIMARY KEY,
                        experiment_id TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        generation INTEGER NOT NULL,
                        agent_id TEXT,
                        description TEXT NOT NULL,
                        data TEXT,
                        timestamp TEXT NOT NULL
                    )
                """)
                
                conn.commit()
                conn.close()
                logger.info("Evolution database initialized")
            except Exception as e:
                logger.error(f"Error initializing evolution database: {e}")
    
    def _load_genomes(self):
        """Load agent genomes from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM agent_genomes")
                rows = cursor.fetchall()
                
                for row in rows:
                    genome = AgentGenome(
                        id=row[0],
                        agent_id=row[1],
                        generation=row[2],
                        genes=json.loads(row[3]),
                        fitness_score=row[4],
                        performance_metrics=json.loads(row[5]),
                        mutation_history=json.loads(row[6]) if row[6] else [],
                        crossover_history=json.loads(row[7]) if row[7] else [],
                        created_at=datetime.fromisoformat(row[8]),
                        updated_at=datetime.fromisoformat(row[9])
                    )
                    self.genomes[genome.id] = genome
                
                conn.close()
                logger.info(f"Loaded {len(self.genomes)} agent genomes")
            except Exception as e:
                logger.error(f"Error loading agent genomes: {e}")
    
    def _load_experiments(self):
        """Load evolution experiments from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM evolution_experiments")
                rows = cursor.fetchall()
                
                for row in rows:
                    experiment = EvolutionExperiment(
                        id=row[0],
                        name=row[1],
                        description=row[2],
                        strategy=EvolutionStrategy(row[3]),
                        population_size=row[4],
                        max_generations=row[5],
                        fitness_function=FitnessFunction(row[6]),
                        mutation_rate=row[7],
                        crossover_rate=row[8],
                        selection_type=SelectionType(row[9]),
                        status=EvolutionStatus(row[10]),
                        current_generation=row[11],
                        best_fitness=row[12],
                        average_fitness=row[13],
                        parameters=json.loads(row[14]) if row[14] else {},
                        results=json.loads(row[15]) if row[15] else {},
                        created_at=datetime.fromisoformat(row[16]),
                        updated_at=datetime.fromisoformat(row[17])
                    )
                    self.experiments[experiment.id] = experiment
                
                conn.close()
                logger.info(f"Loaded {len(self.experiments)} evolution experiments")
            except Exception as e:
                logger.error(f"Error loading evolution experiments: {e}")
    
    def _load_events(self):
        """Load evolution events from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM evolution_events")
                rows = cursor.fetchall()
                
                for row in rows:
                    event = EvolutionEvent(
                        id=row[0],
                        experiment_id=row[1],
                        event_type=row[2],
                        generation=row[3],
                        agent_id=row[4],
                        description=row[5],
                        data=json.loads(row[6]) if row[6] else {},
                        timestamp=datetime.fromisoformat(row[7])
                    )
                    self.events[event.id] = event
                
                conn.close()
                logger.info(f"Loaded {len(self.events)} evolution events")
            except Exception as e:
                logger.error(f"Error loading evolution events: {e}")
    
    def _save_genome(self, genome: AgentGenome):
        """Save agent genome to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO agent_genomes 
                    (id, agent_id, generation, genes, fitness_score, performance_metrics,
                     mutation_history, crossover_history, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    genome.id, genome.agent_id, genome.generation,
                    json.dumps(genome.genes), genome.fitness_score,
                    json.dumps(genome.performance_metrics),
                    json.dumps(genome.mutation_history),
                    json.dumps(genome.crossover_history),
                    genome.created_at.isoformat(), genome.updated_at.isoformat()
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving genome {genome.id}: {e}")
    
    def _save_experiment(self, experiment: EvolutionExperiment):
        """Save evolution experiment to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO evolution_experiments 
                    (id, name, description, strategy, population_size, max_generations,
                     fitness_function, mutation_rate, crossover_rate, selection_type,
                     status, current_generation, best_fitness, average_fitness,
                     parameters, results, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    experiment.id, experiment.name, experiment.description,
                    experiment.strategy.value, experiment.population_size,
                    experiment.max_generations, experiment.fitness_function.value,
                    experiment.mutation_rate, experiment.crossover_rate,
                    experiment.selection_type.value, experiment.status.value,
                    experiment.current_generation, experiment.best_fitness,
                    experiment.average_fitness, json.dumps(experiment.parameters),
                    json.dumps(experiment.results), experiment.created_at.isoformat(),
                    experiment.updated_at.isoformat()
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving experiment {experiment.id}: {e}")
    
    def _save_event(self, event: EvolutionEvent):
        """Save evolution event to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO evolution_events 
                    (id, experiment_id, event_type, generation, agent_id, description, data, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.id, event.experiment_id, event.event_type, event.generation,
                    event.agent_id, event.description, json.dumps(event.data),
                    event.timestamp.isoformat()
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving event {event.id}: {e}")
    
    def create_agent_genome(self, agent_id: str, genes: Dict[str, Any],
                          performance_metrics: Optional[Dict[str, float]] = None) -> str:
        """Create a new agent genome"""
        genome_id = str(uuid.uuid4())
        genome = AgentGenome(
            id=genome_id,
            agent_id=agent_id,
            generation=0,
            genes=genes,
            fitness_score=0.0,
            performance_metrics=performance_metrics or {},
            mutation_history=[],
            crossover_history=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with self.lock:
            self.genomes[genome_id] = genome
            self._save_genome(genome)
        
        logger.info(f"Created genome {genome_id} for agent {agent_id}")
        return genome_id
    
    def create_evolution_experiment(self, name: str, description: str,
                                  strategy: EvolutionStrategy,
                                  population_size: int = 50,
                                  max_generations: int = 100,
                                  fitness_function: FitnessFunction = FitnessFunction.ACCURACY,
                                  mutation_rate: float = 0.1,
                                  crossover_rate: float = 0.8,
                                  selection_type: SelectionType = SelectionType.TOURNAMENT) -> str:
        """Create a new evolution experiment"""
        experiment_id = str(uuid.uuid4())
        experiment = EvolutionExperiment(
            id=experiment_id,
            name=name,
            description=description,
            strategy=strategy,
            population_size=population_size,
            max_generations=max_generations,
            fitness_function=fitness_function,
            mutation_rate=mutation_rate,
            crossover_rate=crossover_rate,
            selection_type=selection_type,
            status=EvolutionStatus.INITIALIZING,
            current_generation=0,
            best_fitness=0.0,
            average_fitness=0.0,
            parameters={},
            results={},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with self.lock:
            self.experiments[experiment_id] = experiment
            self._save_experiment(experiment)
        
        logger.info(f"Created evolution experiment {experiment_id}: {name}")
        return experiment_id
    
    def start_evolution_experiment(self, experiment_id: str) -> bool:
        """Start an evolution experiment"""
        if experiment_id not in self.experiments:
            return False
        
        experiment = self.experiments[experiment_id]
        if experiment.status != EvolutionStatus.INITIALIZING:
            return False
        
        # Update status
        experiment.status = EvolutionStatus.RUNNING
        experiment.updated_at = datetime.now()
        self._save_experiment(experiment)
        
        # Add to processing queue
        self.evolution_queue.append({
            "type": "run_experiment",
            "experiment_id": experiment_id
        })
        
        logger.info(f"Started evolution experiment {experiment_id}")
        return True
    
    def evaluate_fitness(self, genome_id: str, performance_data: Dict[str, Any]) -> float:
        """Evaluate fitness of an agent genome"""
        if genome_id not in self.genomes:
            return 0.0
        
        genome = self.genomes[genome_id]
        
        # Calculate fitness based on performance data
        fitness = 0.0
        if "accuracy" in performance_data:
            fitness += performance_data["accuracy"] * 0.4
        if "efficiency" in performance_data:
            fitness += performance_data["efficiency"] * 0.3
        if "robustness" in performance_data:
            fitness += performance_data["robustness"] * 0.2
        if "adaptability" in performance_data:
            fitness += performance_data["adaptability"] * 0.1
        
        # Update genome
        genome.fitness_score = fitness
        genome.performance_metrics.update(performance_data)
        genome.updated_at = datetime.now()
        
        with self.lock:
            self._save_genome(genome)
        
        logger.info(f"Evaluated fitness for genome {genome_id}: {fitness:.3f}")
        return fitness
    
    def mutate_genome(self, genome_id: str, mutation_type: MutationType = MutationType.GAUSSIAN,
                     mutation_strength: float = 0.1) -> str:
        """Mutate an agent genome"""
        if genome_id not in self.genomes:
            return None
        
        parent_genome = self.genomes[genome_id]
        
        # Create mutated genome
        mutated_genes = self._apply_mutation(parent_genome.genes, mutation_type, mutation_strength)
        
        # Create new genome
        mutated_genome_id = str(uuid.uuid4())
        mutated_genome = AgentGenome(
            id=mutated_genome_id,
            agent_id=parent_genome.agent_id,
            generation=parent_genome.generation + 1,
            genes=mutated_genes,
            fitness_score=0.0,
            performance_metrics={},
            mutation_history=parent_genome.mutation_history + [{
                "parent_id": genome_id,
                "mutation_type": mutation_type.value,
                "strength": mutation_strength,
                "timestamp": datetime.now().isoformat()
            }],
            crossover_history=parent_genome.crossover_history.copy(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with self.lock:
            self.genomes[mutated_genome_id] = mutated_genome
            self._save_genome(mutated_genome)
        
        logger.info(f"Mutated genome {genome_id} -> {mutated_genome_id}")
        return mutated_genome_id
    
    def crossover_genomes(self, parent1_id: str, parent2_id: str,
                         crossover_type: str = "uniform") -> Tuple[str, str]:
        """Perform crossover between two genomes"""
        if parent1_id not in self.genomes or parent2_id not in self.genomes:
            return None, None
        
        parent1 = self.genomes[parent1_id]
        parent2 = self.genomes[parent2_id]
        
        # Create offspring genomes
        offspring1_genes, offspring2_genes = self._apply_crossover(
            parent1.genes, parent2.genes, crossover_type
        )
        
        offspring1_id = str(uuid.uuid4())
        offspring1 = AgentGenome(
            id=offspring1_id,
            agent_id=parent1.agent_id,
            generation=max(parent1.generation, parent2.generation) + 1,
            genes=offspring1_genes,
            fitness_score=0.0,
            performance_metrics={},
            mutation_history=[],
            crossover_history=[{
                "parent1_id": parent1_id,
                "parent2_id": parent2_id,
                "crossover_type": crossover_type,
                "timestamp": datetime.now().isoformat()
            }],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        offspring2_id = str(uuid.uuid4())
        offspring2 = AgentGenome(
            id=offspring2_id,
            agent_id=parent2.agent_id,
            generation=max(parent1.generation, parent2.generation) + 1,
            genes=offspring2_genes,
            fitness_score=0.0,
            performance_metrics={},
            mutation_history=[],
            crossover_history=[{
                "parent1_id": parent1_id,
                "parent2_id": parent2_id,
                "crossover_type": crossover_type,
                "timestamp": datetime.now().isoformat()
            }],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with self.lock:
            self.genomes[offspring1_id] = offspring1
            self.genomes[offspring2_id] = offspring2
            self._save_genome(offspring1)
            self._save_genome(offspring2)
        
        logger.info(f"Crossover: {parent1_id} + {parent2_id} -> {offspring1_id}, {offspring2_id}")
        return offspring1_id, offspring2_id
    
    def select_parents(self, experiment_id: str, selection_size: int = 2) -> List[str]:
        """Select parents for reproduction using specified selection strategy"""
        if experiment_id not in self.experiments:
            return []
        
        experiment = self.experiments[experiment_id]
        
        # Get genomes for this experiment
        experiment_genomes = [
            genome for genome in self.genomes.values()
            if genome.agent_id.startswith(f"exp_{experiment_id}")
        ]
        
        if len(experiment_genomes) < selection_size:
            return []
        
        # Apply selection strategy
        if experiment.selection_type == SelectionType.TOURNAMENT:
            return self._tournament_selection(experiment_genomes, selection_size)
        elif experiment.selection_type == SelectionType.RANK_SELECTION:
            return self._rank_selection(experiment_genomes, selection_size)
        elif experiment.selection_type == SelectionType.ROULETTE_WHEEL:
            return self._roulette_wheel_selection(experiment_genomes, selection_size)
        elif experiment.selection_type == SelectionType.ELITISM:
            return self._elitism_selection(experiment_genomes, selection_size)
        else:
            return self._tournament_selection(experiment_genomes, selection_size)
    
    def _apply_mutation(self, genes: Dict[str, Any], mutation_type: MutationType,
                       strength: float) -> Dict[str, Any]:
        """Apply mutation to genes"""
        mutated_genes = genes.copy()
        
        for key, value in mutated_genes.items():
            if isinstance(value, (int, float)):
                if mutation_type == MutationType.GAUSSIAN:
                    # Gaussian mutation
                    noise = random.gauss(0, strength)
                    mutated_genes[key] = value + noise
                elif mutation_type == MutationType.UNIFORM:
                    # Uniform mutation
                    noise = random.uniform(-strength, strength)
                    mutated_genes[key] = value + noise
                elif mutation_type == MutationType.POLYNOMIAL:
                    # Polynomial mutation
                    if random.random() < 0.5:
                        delta = (2 * random.random()) ** (1 / (1 + 1)) - 1
                    else:
                        delta = 1 - (2 * (1 - random.random())) ** (1 / (1 + 1))
                    mutated_genes[key] = value + delta * strength
                elif mutation_type == MutationType.ADAPTIVE:
                    # Adaptive mutation based on fitness
                    adaptive_strength = strength * (1 - abs(value))
                    noise = random.gauss(0, adaptive_strength)
                    mutated_genes[key] = value + noise
        
        return mutated_genes
    
    def _apply_crossover(self, genes1: Dict[str, Any], genes2: Dict[str, Any],
                        crossover_type: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Apply crossover between two gene sets"""
        offspring1 = genes1.copy()
        offspring2 = genes2.copy()
        
        if crossover_type == "uniform":
            # Uniform crossover
            for key in genes1:
                if random.random() < 0.5:
                    offspring1[key], offspring2[key] = offspring2[key], offspring1[key]
        elif crossover_type == "single_point":
            # Single-point crossover
            keys = list(genes1.keys())
            if len(keys) > 1:
                crossover_point = random.randint(1, len(keys) - 1)
                for i, key in enumerate(keys):
                    if i >= crossover_point:
                        offspring1[key], offspring2[key] = offspring2[key], offspring1[key]
        elif crossover_type == "arithmetic":
            # Arithmetic crossover
            alpha = random.random()
            for key in genes1:
                if isinstance(genes1[key], (int, float)) and isinstance(genes2[key], (int, float)):
                    offspring1[key] = alpha * genes1[key] + (1 - alpha) * genes2[key]
                    offspring2[key] = (1 - alpha) * genes1[key] + alpha * genes2[key]
        
        return offspring1, offspring2
    
    def _tournament_selection(self, genomes: List[AgentGenome], selection_size: int) -> List[str]:
        """Tournament selection"""
        selected = []
        tournament_size = min(3, len(genomes))
        
        for _ in range(selection_size):
            tournament = random.sample(genomes, tournament_size)
            winner = max(tournament, key=lambda g: g.fitness_score)
            selected.append(winner.id)
        
        return selected
    
    def _rank_selection(self, genomes: List[AgentGenome], selection_size: int) -> List[str]:
        """Rank-based selection"""
        sorted_genomes = sorted(genomes, key=lambda g: g.fitness_score, reverse=True)
        ranks = list(range(1, len(sorted_genomes) + 1))
        
        # Calculate selection probabilities
        total_rank = sum(ranks)
        probabilities = [rank / total_rank for rank in ranks]
        
        selected = []
        for _ in range(selection_size):
            selected.append(random.choices(sorted_genomes, weights=probabilities)[0].id)
        
        return selected
    
    def _roulette_wheel_selection(self, genomes: List[AgentGenome], selection_size: int) -> List[str]:
        """Roulette wheel selection"""
        # Normalize fitness scores
        min_fitness = min(g.fitness_score for g in genomes)
        max_fitness = max(g.fitness_score for g in genomes)
        
        if max_fitness == min_fitness:
            # Equal fitness - random selection
            return random.sample([g.id for g in genomes], selection_size)
        
        # Shift fitness scores to positive values
        shifted_fitness = [g.fitness_score - min_fitness + 1 for g in genomes]
        total_fitness = sum(shifted_fitness)
        probabilities = [f / total_fitness for f in shifted_fitness]
        
        selected = []
        for _ in range(selection_size):
            selected.append(random.choices(genomes, weights=probabilities)[0].id)
        
        return selected
    
    def _elitism_selection(self, genomes: List[AgentGenome], selection_size: int) -> List[str]:
        """Elitism selection - select best performers"""
        sorted_genomes = sorted(genomes, key=lambda g: g.fitness_score, reverse=True)
        return [g.id for g in sorted_genomes[:selection_size]]
    
    def get_evolution_metrics(self) -> EvolutionMetrics:
        """Get evolution performance metrics"""
        with self.lock:
            total_experiments = len(self.experiments)
            active_experiments = len([e for e in self.experiments.values() if e.status == EvolutionStatus.RUNNING])
            completed_experiments = len([e for e in self.experiments.values() if e.status == EvolutionStatus.COMPLETED])
            
            total_generations = sum(e.current_generation for e in self.experiments.values())
            
            if self.genomes:
                average_fitness = sum(g.fitness_score for g in self.genomes.values()) / len(self.genomes)
                best_fitness = max(g.fitness_score for g in self.genomes.values())
            else:
                average_fitness = 0.0
                best_fitness = 0.0
            
            # Calculate evolution speed (simplified)
            evolution_speed = total_generations / max(1, len(self.experiments))
            
            # Calculate success rate
            success_rate = completed_experiments / max(1, total_experiments)
            
            # Calculate mutation effectiveness (simplified)
            mutation_effectiveness = 0.8  # Placeholder
            
            # Calculate crossover effectiveness (simplified)
            crossover_effectiveness = 0.7  # Placeholder
            
            last_experiment = max([e.created_at for e in self.experiments.values()], default=None)
            
            return EvolutionMetrics(
                total_experiments=total_experiments,
                active_experiments=active_experiments,
                completed_experiments=completed_experiments,
                total_generations=total_generations,
                average_fitness=average_fitness,
                best_fitness=best_fitness,
                evolution_speed=evolution_speed,
                success_rate=success_rate,
                mutation_effectiveness=mutation_effectiveness,
                crossover_effectiveness=crossover_effectiveness,
                last_experiment=last_experiment
            )
    
    def start_evolution_processing(self):
        """Start the evolution processing background thread"""
        if not self.evolution_processor_running:
            self.evolution_processor_running = True
            self.evolution_thread = threading.Thread(target=self._process_evolution_queue, daemon=True)
            self.evolution_thread.start()
            logger.info("Evolution processor started")
    
    def stop_evolution_processing(self):
        """Stop the evolution processing background thread"""
        self.evolution_processor_running = False
        if hasattr(self, 'evolution_thread'):
            self.evolution_thread.join(timeout=1.0)
        logger.info("Evolution processor stopped")
    
    def _process_evolution_queue(self):
        """Process the evolution queue in background"""
        while self.evolution_processor_running:
            try:
                if self.evolution_queue:
                    task = self.evolution_queue.pop(0)
                    self._process_evolution_task(task)
                else:
                    time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error processing evolution task: {e}")
                time.sleep(1.0)
    
    def _process_evolution_task(self, task: Dict[str, Any]):
        """Process a single evolution task"""
        task_type = task.get("type")
        
        if task_type == "run_experiment":
            self._run_evolution_experiment(task["experiment_id"])
        elif task_type == "evaluate_fitness":
            self._evaluate_fitness_batch(task["genome_ids"])
        elif task_type == "evolve_generation":
            self._evolve_generation(task["experiment_id"])
    
    def _run_evolution_experiment(self, experiment_id: str):
        """Run a complete evolution experiment"""
        if experiment_id not in self.experiments:
            return
        
        experiment = self.experiments[experiment_id]
        experiment.status = EvolutionStatus.RUNNING
        self._save_experiment(experiment)
        
        # Initialize population
        self._initialize_population(experiment)
        
        # Run generations
        for generation in range(experiment.max_generations):
            if experiment.status != EvolutionStatus.RUNNING:
                break
            
            self._evolve_generation(experiment_id)
            experiment.current_generation = generation + 1
            self._save_experiment(experiment)
            
            # Log progress
            logger.info(f"Generation {generation + 1}/{experiment.max_generations} completed")
        
        # Complete experiment
        experiment.status = EvolutionStatus.COMPLETED
        experiment.updated_at = datetime.now()
        self._save_experiment(experiment)
        
        logger.info(f"Evolution experiment {experiment_id} completed")
    
    def _initialize_population(self, experiment: EvolutionExperiment):
        """Initialize population for evolution experiment"""
        # Create initial genomes
        for i in range(experiment.population_size):
            agent_id = f"exp_{experiment.id}_agent_{i}"
            genes = self._generate_random_genes()
            self.create_agent_genome(agent_id, genes)
    
    def _generate_random_genes(self) -> Dict[str, Any]:
        """Generate random genes for initial population"""
        return {
            "learning_rate": random.uniform(0.001, 0.1),
            "exploration_rate": random.uniform(0.1, 0.9),
            "memory_size": random.randint(100, 1000),
            "patience": random.randint(5, 50),
            "creativity": random.uniform(0.0, 1.0),
            "empathy": random.uniform(0.0, 1.0),
            "ethics_weight": random.uniform(0.0, 1.0)
        }
    
    def _evolve_generation(self, experiment_id: str):
        """Evolve one generation"""
        if experiment_id not in self.experiments:
            return
        
        experiment = self.experiments[experiment_id]
        
        # Get current population
        population = [
            genome for genome in self.genomes.values()
            if genome.agent_id.startswith(f"exp_{experiment_id}")
        ]
        
        if len(population) < 2:
            return
        
        # Select parents
        parents = self.select_parents(experiment_id, experiment.population_size // 2)
        
        # Create new generation through crossover and mutation
        new_genomes = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                parent1_id, parent2_id = parents[i], parents[i + 1]
                offspring1_id, offspring2_id = self.crossover_genomes(parent1_id, parent2_id)
                
                if offspring1_id and offspring2_id:
                    # Mutate offspring
                    if random.random() < experiment.mutation_rate:
                        self.mutate_genome(offspring1_id, MutationType.GAUSSIAN)
                    if random.random() < experiment.mutation_rate:
                        self.mutate_genome(offspring2_id, MutationType.GAUSSIAN)
                    
                    new_genomes.extend([offspring1_id, offspring2_id])
        
        # Update experiment statistics
        if new_genomes:
            fitness_scores = [self.genomes[gid].fitness_score for gid in new_genomes if gid in self.genomes]
            if fitness_scores:
                experiment.average_fitness = sum(fitness_scores) / len(fitness_scores)
                experiment.best_fitness = max(fitness_scores)
                experiment.updated_at = datetime.now()
                self._save_experiment(experiment)
    
    def _evaluate_fitness_batch(self, genome_ids: List[str]):
        """Evaluate fitness for a batch of genomes"""
        for genome_id in genome_ids:
            if genome_id in self.genomes:
                # Simulate performance evaluation
                performance_data = {
                    "accuracy": random.uniform(0.5, 1.0),
                    "efficiency": random.uniform(0.3, 1.0),
                    "robustness": random.uniform(0.4, 1.0),
                    "adaptability": random.uniform(0.2, 1.0)
                }
                self.evaluate_fitness(genome_id, performance_data)
    
    def export_evolution_data(self, format: str = "json") -> Union[str, Dict[str, Any]]:
        """Export evolution data in specified format"""
        with self.lock:
            data = {
                "genomes": [genome.dict() for genome in self.genomes.values()],
                "experiments": [experiment.dict() for experiment in self.experiments.values()],
                "events": [event.dict() for event in self.events.values()],
                "metrics": self.get_evolution_metrics().dict()
            }
            
            if format == "json":
                return json.dumps(data, indent=2, default=str)
            else:
                return data
    
    def clear_evolution_data(self):
        """Clear all evolution data"""
        with self.lock:
            self.genomes.clear()
            self.experiments.clear()
            self.events.clear()
            
            # Clear database
            with self.db_lock:
                try:
                    conn = sqlite3.connect(self.db_path, timeout=10.0)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM agent_genomes")
                    cursor.execute("DELETE FROM evolution_experiments")
                    cursor.execute("DELETE FROM evolution_events")
                    conn.commit()
                    conn.close()
                except Exception as e:
                    logger.error(f"Error clearing evolution data: {e}")
            
        logger.info("Cleared all evolution data")


# Example usage and testing
if __name__ == "__main__":
    # Create evolution framework
    framework = EvolutionFramework()
    
    # Test basic functionality
    print("🧪 Testing Pattern 19: Agent Evolution")
    print("=" * 50)
    
    # Create test genome
    genes = {"learning_rate": 0.01, "exploration_rate": 0.5, "memory_size": 500}
    genome_id = framework.create_agent_genome("test_agent", genes)
    print(f"✅ Created genome: {genome_id}")
    
    # Evaluate fitness
    performance = {"accuracy": 0.85, "efficiency": 0.7, "robustness": 0.8}
    fitness = framework.evaluate_fitness(genome_id, performance)
    print(f"✅ Evaluated fitness: {fitness:.3f}")
    
    # Create evolution experiment
    experiment_id = framework.create_evolution_experiment(
        "Test Evolution", "Testing evolution capabilities",
        EvolutionStrategy.GENETIC_ALGORITHM, population_size=10, max_generations=5
    )
    print(f"✅ Created experiment: {experiment_id}")
    
    # Get metrics
    metrics = framework.get_evolution_metrics()
    print(f"✅ Evolution metrics: {metrics.total_experiments} experiments")
    
    print("🎯 Pattern 19: Agent Evolution basic test completed!")

