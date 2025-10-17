"""
Pattern 13: Agent Creativity - Complete Implementation
Creative problem solving and content generation system
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
from collections import defaultdict, deque
import time
import random
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreativityType(Enum):
    """Types of creativity"""
    DIVERGENT = "divergent"           # Generating multiple ideas
    CONVERGENT = "convergent"         # Finding best solution
    LATERAL = "lateral"               # Thinking outside the box
    COMBINATORIAL = "combinatorial"   # Combining existing ideas
    TRANSFORMATIONAL = "transformational" # Transforming ideas
    EXPLORATORY = "exploratory"       # Exploring new possibilities
    SYNTHETIC = "synthetic"           # Synthesizing new concepts
    ADAPTIVE = "adaptive"             # Adapting to constraints

class CreativityConstraint(Enum):
    """Types of creative constraints"""
    TIME = "time"                     # Time limitations
    RESOURCE = "resource"             # Resource limitations
    TECHNICAL = "technical"           # Technical constraints
    BUDGET = "budget"                 # Budget limitations
    LEGAL = "legal"                   # Legal constraints
    ETHICAL = "ethical"               # Ethical constraints
    CULTURAL = "cultural"             # Cultural constraints
    AESTHETIC = "aesthetic"           # Aesthetic constraints

class CreativityStatus(Enum):
    """Creativity process status"""
    ACTIVE = "active"                 # Currently creating
    PAUSED = "paused"                 # Process paused
    COMPLETED = "completed"           # Process completed
    FAILED = "failed"                 # Process failed
    IDLE = "idle"                     # No active process

@dataclass
class CreativeIdea:
    """Creative idea representation"""
    id: str
    content: str
    idea_type: str
    novelty_score: float
    feasibility_score: float
    value_score: float
    constraints: List[str]
    inspiration_sources: List[str]
    created_at: datetime
    updated_at: datetime
    status: str = "draft"
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

@dataclass
class CreativeSession:
    """Creative session representation"""
    id: str
    session_type: CreativityType
    prompt: str
    constraints: List[CreativityConstraint]
    ideas: List[str]
    best_idea: Optional[str]
    session_metrics: Dict[str, float]
    created_at: datetime
    completed_at: Optional[datetime] = None
    status: CreativityStatus = CreativityStatus.ACTIVE
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class CreativePattern:
    """Creative pattern for idea generation"""
    id: str
    pattern_name: str
    pattern_type: str
    template: str
    variables: List[str]
    success_rate: float
    usage_count: int
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

@dataclass
class CreativityStats:
    """Creativity statistics"""
    total_sessions: int
    total_ideas: int
    average_novelty: float
    average_feasibility: float
    average_value: float
    creativity_types: Dict[str, int]
    constraint_types: Dict[str, int]
    success_rate: float
    most_used_patterns: List[str]
    last_creativity: datetime

class CreativityFramework:
    """
    Comprehensive agent creativity framework
    Enables creative problem solving and content generation
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.storage_path = Path(self.config.get("storage_path", "creativity_data"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Threading and concurrency
        self.lock = threading.Lock()
        self.db_lock = threading.Lock()
        
        # Database setup
        self.db_path = self.storage_path / "creativity.db"
        self._init_database()
        
        # Creativity components
        self.ideas: Dict[str, CreativeIdea] = {}
        self.sessions: Dict[str, CreativeSession] = {}
        self.patterns: Dict[str, CreativePattern] = {}
        self.creativity_queue = deque()
        
        # Creativity state
        self.creativity_active = False
        self.current_sessions: Dict[str, CreativeSession] = {}
        
        # Load existing data
        self._load_ideas()
        self._load_sessions()
        self._load_patterns()
        
        # Initialize default patterns
        self._initialize_default_patterns()
        
        # Start creativity processor
        self._start_creativity_processor()
    
    def _init_database(self):
        """Initialize creativity database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                # Create ideas table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS creative_ideas (
                        id TEXT PRIMARY KEY,
                        content TEXT,
                        idea_type TEXT,
                        novelty_score REAL,
                        feasibility_score REAL,
                        value_score REAL,
                        constraints TEXT,
                        inspiration_sources TEXT,
                        created_at TEXT,
                        updated_at TEXT,
                        status TEXT
                    )
                """)
                
                # Create sessions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS creative_sessions (
                        id TEXT PRIMARY KEY,
                        session_type TEXT,
                        prompt TEXT,
                        constraints TEXT,
                        ideas TEXT,
                        best_idea TEXT,
                        session_metrics TEXT,
                        created_at TEXT,
                        completed_at TEXT,
                        status TEXT
                    )
                """)
                
                # Create patterns table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS creative_patterns (
                        id TEXT PRIMARY KEY,
                        pattern_name TEXT,
                        pattern_type TEXT,
                        template TEXT,
                        variables TEXT,
                        success_rate REAL,
                        usage_count INTEGER,
                        created_at TEXT,
                        updated_at TEXT
                    )
                """)
                
                conn.commit()
                conn.close()
                logger.info("Creativity database initialized")
            except Exception as e:
                logger.error(f"Error initializing creativity database: {e}")
    
    def _load_ideas(self):
        """Load creative ideas from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM creative_ideas")
                
                for row in cursor.fetchall():
                    idea = CreativeIdea(
                        id=row[0],
                        content=row[1],
                        idea_type=row[2],
                        novelty_score=row[3],
                        feasibility_score=row[4],
                        value_score=row[5],
                        constraints=json.loads(row[6]) if row[6] else [],
                        inspiration_sources=json.loads(row[7]) if row[7] else [],
                        created_at=datetime.fromisoformat(row[8]),
                        updated_at=datetime.fromisoformat(row[9]),
                        status=row[10]
                    )
                    self.ideas[idea.id] = idea
                
                conn.close()
                logger.info(f"Loaded {len(self.ideas)} creative ideas")
            except Exception as e:
                logger.error(f"Error loading ideas: {e}")
    
    def _load_sessions(self):
        """Load creative sessions from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM creative_sessions")
                
                for row in cursor.fetchall():
                    session = CreativeSession(
                        id=row[0],
                        session_type=CreativityType(row[1]),
                        prompt=row[2],
                        constraints=[CreativityConstraint(c) for c in json.loads(row[3])] if row[3] else [],
                        ideas=json.loads(row[4]) if row[4] else [],
                        best_idea=row[5],
                        session_metrics=json.loads(row[6]) if row[6] else {},
                        created_at=datetime.fromisoformat(row[7]),
                        completed_at=datetime.fromisoformat(row[8]) if row[8] else None,
                        status=CreativityStatus(row[9])
                    )
                    self.sessions[session.id] = session
                
                conn.close()
                logger.info(f"Loaded {len(self.sessions)} creative sessions")
            except Exception as e:
                logger.error(f"Error loading sessions: {e}")
    
    def _load_patterns(self):
        """Load creative patterns from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM creative_patterns")
                
                for row in cursor.fetchall():
                    pattern = CreativePattern(
                        id=row[0],
                        pattern_name=row[1],
                        pattern_type=row[2],
                        template=row[3],
                        variables=json.loads(row[4]) if row[4] else [],
                        success_rate=row[5],
                        usage_count=row[6],
                        created_at=datetime.fromisoformat(row[7]),
                        updated_at=datetime.fromisoformat(row[8])
                    )
                    self.patterns[pattern.id] = pattern
                
                conn.close()
                logger.info(f"Loaded {len(self.patterns)} creative patterns")
            except Exception as e:
                logger.error(f"Error loading patterns: {e}")
    
    def _save_idea(self, idea: CreativeIdea):
        """Save creative idea to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO creative_ideas 
                    (id, content, idea_type, novelty_score, feasibility_score, value_score, 
                     constraints, inspiration_sources, created_at, updated_at, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    idea.id,
                    idea.content,
                    idea.idea_type,
                    idea.novelty_score,
                    idea.feasibility_score,
                    idea.value_score,
                    json.dumps(idea.constraints),
                    json.dumps(idea.inspiration_sources),
                    idea.created_at.isoformat(),
                    idea.updated_at.isoformat(),
                    idea.status
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving idea {idea.id}: {e}")
    
    def _save_session(self, session: CreativeSession):
        """Save creative session to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO creative_sessions 
                    (id, session_type, prompt, constraints, ideas, best_idea, 
                     session_metrics, created_at, completed_at, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session.id,
                    session.session_type.value,
                    session.prompt,
                    json.dumps([c.value for c in session.constraints]),
                    json.dumps(session.ideas),
                    session.best_idea,
                    json.dumps(session.session_metrics),
                    session.created_at.isoformat(),
                    session.completed_at.isoformat() if session.completed_at else None,
                    session.status.value
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving session {session.id}: {e}")
    
    def _save_pattern(self, pattern: CreativePattern):
        """Save creative pattern to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO creative_patterns 
                    (id, pattern_name, pattern_type, template, variables, success_rate, 
                     usage_count, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pattern.id,
                    pattern.pattern_name,
                    pattern.pattern_type,
                    pattern.template,
                    json.dumps(pattern.variables),
                    pattern.success_rate,
                    pattern.usage_count,
                    pattern.created_at.isoformat(),
                    pattern.updated_at.isoformat()
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving pattern {pattern.id}: {e}")
    
    def _start_creativity_processor(self):
        """Start background creativity processor"""
        def process_creativity():
            while True:
                try:
                    if self.creativity_queue:
                        creativity_task = self.creativity_queue.popleft()
                        self._process_creativity_task(creativity_task)
                    else:
                        time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Error in creativity processor: {e}")
                    time.sleep(1)
        
        thread = threading.Thread(target=process_creativity, daemon=True)
        thread.start()
        logger.info("Creativity processor started")
    
    def _process_creativity_task(self, task: Dict[str, Any]):
        """Process a creativity task"""
        try:
            task_type = task.get("type")
            
            if task_type == "divergent_thinking":
                self._process_divergent_thinking(task)
            elif task_type == "convergent_thinking":
                self._process_convergent_thinking(task)
            elif task_type == "lateral_thinking":
                self._process_lateral_thinking(task)
            elif task_type == "combinatorial_creativity":
                self._process_combinatorial_creativity(task)
            elif task_type == "pattern_generation":
                self._generate_creative_patterns(task)
            else:
                logger.warning(f"Unknown creativity task type: {task_type}")
                
        except Exception as e:
            logger.error(f"Error processing creativity task: {e}")
    
    def _initialize_default_patterns(self):
        """Initialize default creative patterns"""
        default_patterns = [
            {
                "name": "SCAMPER",
                "type": "divergent",
                "template": "Substitute: {substitute}, Combine: {combine}, Adapt: {adapt}, Modify: {modify}, Put to other uses: {other_uses}, Eliminate: {eliminate}, Reverse: {reverse}",
                "variables": ["substitute", "combine", "adapt", "modify", "other_uses", "eliminate", "reverse"]
            },
            {
                "name": "Six Thinking Hats",
                "type": "convergent",
                "template": "White Hat (Facts): {facts}, Red Hat (Emotions): {emotions}, Black Hat (Caution): {caution}, Yellow Hat (Benefits): {benefits}, Green Hat (Creativity): {creativity}, Blue Hat (Process): {process}",
                "variables": ["facts", "emotions", "caution", "benefits", "creativity", "process"]
            },
            {
                "name": "Mind Mapping",
                "type": "lateral",
                "template": "Central: {central}, Branch 1: {branch1}, Branch 2: {branch2}, Branch 3: {branch3}, Sub-branches: {sub_branches}",
                "variables": ["central", "branch1", "branch2", "branch3", "sub_branches"]
            },
            {
                "name": "Random Word",
                "type": "lateral",
                "template": "Random word: {random_word}, Connection: {connection}, Application: {application}",
                "variables": ["random_word", "connection", "application"]
            },
            {
                "name": "What If",
                "type": "exploratory",
                "template": "What if {scenario}? Then {consequence}. This could lead to {implications}.",
                "variables": ["scenario", "consequence", "implications"]
            }
        ]
        
        for pattern_data in default_patterns:
            if not any(p.pattern_name == pattern_data["name"] for p in self.patterns.values()):
                pattern_id = str(uuid.uuid4())
                pattern = CreativePattern(
                    id=pattern_id,
                    pattern_name=pattern_data["name"],
                    pattern_type=pattern_data["type"],
                    template=pattern_data["template"],
                    variables=pattern_data["variables"],
                    success_rate=0.5,
                    usage_count=0,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                self.patterns[pattern_id] = pattern
                self._save_pattern(pattern)
    
    def start_creative_session(self,
                             prompt: str,
                             creativity_type: CreativityType = CreativityType.DIVERGENT,
                             constraints: List[CreativityConstraint] = None) -> str:
        """Start a new creative session"""
        session_id = str(uuid.uuid4())
        
        session = CreativeSession(
            id=session_id,
            session_type=creativity_type,
            prompt=prompt,
            constraints=constraints or [],
            ideas=[],
            best_idea=None,
            session_metrics={},
            created_at=datetime.now()
        )
        
        with self.lock:
            self.sessions[session_id] = session
            self.current_sessions[session_id] = session
            self._save_session(session)
        
        # Queue for processing
        self.creativity_queue.append({
            "type": f"{creativity_type.value}_thinking",
            "session_id": session_id,
            "prompt": prompt,
            "constraints": [c.value for c in constraints] if constraints else []
        })
        
        logger.info(f"Started creative session {session_id}: {creativity_type.value}")
        return session_id
    
    def generate_ideas(self,
                      session_id: str,
                      num_ideas: int = 5,
                      idea_type: str = "general") -> List[str]:
        """Generate creative ideas for a session"""
        if session_id not in self.sessions:
            logger.warning(f"Session {session_id} not found")
            return []
        
        session = self.sessions[session_id]
        ideas = []
        
        # Generate ideas based on session type
        if session.session_type == CreativityType.DIVERGENT:
            ideas = self._generate_divergent_ideas(session.prompt, num_ideas, idea_type)
        elif session.session_type == CreativityType.CONVERGENT:
            ideas = self._generate_convergent_ideas(session.prompt, num_ideas, idea_type)
        elif session.session_type == CreativityType.LATERAL:
            ideas = self._generate_lateral_ideas(session.prompt, num_ideas, idea_type)
        elif session.session_type == CreativityType.COMBINATORIAL:
            ideas = self._generate_combinatorial_ideas(session.prompt, num_ideas, idea_type)
        else:
            ideas = self._generate_general_ideas(session.prompt, num_ideas, idea_type)
        
        # Create idea objects
        idea_ids = []
        for idea_content in ideas:
            idea_id = str(uuid.uuid4())
            idea = CreativeIdea(
                id=idea_id,
                content=idea_content,
                idea_type=idea_type,
                novelty_score=self._calculate_novelty_score(idea_content),
                feasibility_score=self._calculate_feasibility_score(idea_content, session.constraints),
                value_score=self._calculate_value_score(idea_content),
                constraints=[c.value for c in session.constraints],
                inspiration_sources=[session.prompt],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            self.ideas[idea_id] = idea
            self._save_idea(idea)
            idea_ids.append(idea_id)
        
        # Update session
        session.ideas.extend(idea_ids)
        session.session_metrics.update({
            "ideas_generated": len(ideas),
            "average_novelty": sum(self.ideas[i].novelty_score for i in idea_ids) / len(idea_ids),
            "average_feasibility": sum(self.ideas[i].feasibility_score for i in idea_ids) / len(idea_ids),
            "average_value": sum(self.ideas[i].value_score for i in idea_ids) / len(idea_ids)
        })
        self._save_session(session)
        
        logger.info(f"Generated {len(ideas)} ideas for session {session_id}")
        return ideas
    
    def _generate_divergent_ideas(self, prompt: str, num_ideas: int, idea_type: str) -> List[str]:
        """Generate divergent thinking ideas"""
        ideas = []
        
        # Use SCAMPER pattern
        scamper_pattern = next((p for p in self.patterns.values() if p.pattern_name == "SCAMPER"), None)
        if scamper_pattern:
            for i in range(num_ideas):
                idea = self._apply_pattern(scamper_pattern, prompt, idea_type)
                ideas.append(idea)
        
        # Generate additional random ideas
        while len(ideas) < num_ideas:
            idea = f"Alternative approach to {prompt}: {self._generate_random_idea(prompt, idea_type)}"
            ideas.append(idea)
        
        return ideas[:num_ideas]
    
    def _generate_convergent_ideas(self, prompt: str, num_ideas: int, idea_type: str) -> List[str]:
        """Generate convergent thinking ideas"""
        ideas = []
        
        # Use Six Thinking Hats pattern
        hats_pattern = next((p for p in self.patterns.values() if p.pattern_name == "Six Thinking Hats"), None)
        if hats_pattern:
            for i in range(num_ideas):
                idea = self._apply_pattern(hats_pattern, prompt, idea_type)
                ideas.append(idea)
        
        # Generate focused solutions
        while len(ideas) < num_ideas:
            idea = f"Best solution for {prompt}: {self._generate_focused_idea(prompt, idea_type)}"
            ideas.append(idea)
        
        return ideas[:num_ideas]
    
    def _generate_lateral_ideas(self, prompt: str, num_ideas: int, idea_type: str) -> List[str]:
        """Generate lateral thinking ideas"""
        ideas = []
        
        # Use Random Word pattern
        random_word_pattern = next((p for p in self.patterns.values() if p.pattern_name == "Random Word"), None)
        if random_word_pattern:
            for i in range(num_ideas):
                idea = self._apply_pattern(random_word_pattern, prompt, idea_type)
                ideas.append(idea)
        
        # Generate unconventional ideas
        while len(ideas) < num_ideas:
            idea = f"Unconventional approach to {prompt}: {self._generate_unconventional_idea(prompt, idea_type)}"
            ideas.append(idea)
        
        return ideas[:num_ideas]
    
    def _generate_combinatorial_ideas(self, prompt: str, num_ideas: int, idea_type: str) -> List[str]:
        """Generate combinatorial creativity ideas"""
        ideas = []
        
        # Combine existing ideas
        existing_ideas = [idea.content for idea in self.ideas.values() if idea.idea_type == idea_type]
        
        for i in range(num_ideas):
            if existing_ideas:
                # Combine two random existing ideas
                idea1 = random.choice(existing_ideas)
                idea2 = random.choice(existing_ideas)
                combined_idea = f"Combining '{idea1}' with '{idea2}' for {prompt}: {self._combine_ideas(idea1, idea2)}"
            else:
                # Generate new combination
                combined_idea = f"Creative combination for {prompt}: {self._generate_combination_idea(prompt, idea_type)}"
            ideas.append(combined_idea)
        
        return ideas[:num_ideas]
    
    def _generate_general_ideas(self, prompt: str, num_ideas: int, idea_type: str) -> List[str]:
        """Generate general creative ideas"""
        ideas = []
        
        for i in range(num_ideas):
            idea = f"Creative solution for {prompt}: {self._generate_random_idea(prompt, idea_type)}"
            ideas.append(idea)
        
        return ideas
    
    def _apply_pattern(self, pattern: CreativePattern, prompt: str, idea_type: str) -> str:
        """Apply a creative pattern to generate an idea"""
        try:
            # Generate values for pattern variables
            values = {}
            for var in pattern.variables:
                values[var] = self._generate_pattern_value(var, prompt, idea_type)
            
            # Apply template
            idea = pattern.template.format(**values)
            
            # Update pattern usage
            pattern.usage_count += 1
            pattern.updated_at = datetime.now()
            self._save_pattern(pattern)
            
            return idea
        except Exception as e:
            logger.error(f"Error applying pattern {pattern.pattern_name}: {e}")
            return f"Pattern-based idea for {prompt}: {self._generate_random_idea(prompt, idea_type)}"
    
    def _generate_pattern_value(self, variable: str, prompt: str, idea_type: str) -> str:
        """Generate a value for a pattern variable"""
        variable_lower = variable.lower()
        
        if "substitute" in variable_lower:
            return f"replace {prompt.split()[0]} with something else"
        elif "combine" in variable_lower:
            return f"merge {prompt} with another concept"
        elif "adapt" in variable_lower:
            return f"modify {prompt} for different context"
        elif "modify" in variable_lower:
            return f"change aspects of {prompt}"
        elif "eliminate" in variable_lower:
            return f"remove parts of {prompt}"
        elif "reverse" in variable_lower:
            return f"do the opposite of {prompt}"
        elif "random_word" in variable_lower:
            return random.choice(["elephant", "rainbow", "mountain", "ocean", "forest", "desert"])
        elif "connection" in variable_lower:
            return f"link to {prompt}"
        elif "application" in variable_lower:
            return f"use for {prompt}"
        elif "scenario" in variable_lower:
            return f"if {prompt} was different"
        elif "consequence" in variable_lower:
            return f"then {prompt} would change"
        elif "implications" in variable_lower:
            return f"this affects {prompt}"
        else:
            return f"creative {variable} for {prompt}"
    
    def _generate_random_idea(self, prompt: str, idea_type: str) -> str:
        """Generate a random creative idea"""
        random_ideas = [
            f"Use technology to enhance {prompt}",
            f"Apply {prompt} in a completely different field",
            f"Create a game around {prompt}",
            f"Make {prompt} more accessible to everyone",
            f"Combine {prompt} with art and creativity",
            f"Use {prompt} to solve environmental problems",
            f"Apply {prompt} to education and learning",
            f"Create a community around {prompt}",
            f"Use {prompt} to improve health and wellness",
            f"Apply {prompt} to space exploration"
        ]
        return random.choice(random_ideas)
    
    def _generate_focused_idea(self, prompt: str, idea_type: str) -> str:
        """Generate a focused, solution-oriented idea"""
        focused_ideas = [
            f"Streamlined approach to {prompt}",
            f"Efficient method for {prompt}",
            f"Proven solution for {prompt}",
            f"Best practice for {prompt}",
            f"Optimized version of {prompt}",
            f"Standardized approach to {prompt}",
            f"Professional solution for {prompt}",
            f"Industry-standard {prompt}",
            f"Expert-recommended {prompt}",
            f"Validated approach to {prompt}"
        ]
        return random.choice(focused_ideas)
    
    def _generate_unconventional_idea(self, prompt: str, idea_type: str) -> str:
        """Generate an unconventional, lateral thinking idea"""
        unconventional_ideas = [
            f"Turn {prompt} upside down",
            f"Use {prompt} backwards",
            f"Apply {prompt} to something completely unrelated",
            f"Make {prompt} invisible or hidden",
            f"Use {prompt} in reverse order",
            f"Apply {prompt} to the opposite problem",
            f"Use {prompt} in a different dimension",
            f"Make {prompt} work in zero gravity",
            f"Apply {prompt} to time travel",
            f"Use {prompt} for alien communication"
        ]
        return random.choice(unconventional_ideas)
    
    def _combine_ideas(self, idea1: str, idea2: str) -> str:
        """Combine two ideas creatively"""
        return f"Merge '{idea1}' with '{idea2}' to create something new"
    
    def _generate_combination_idea(self, prompt: str, idea_type: str) -> str:
        """Generate a combination-based idea"""
        return f"Creative fusion of multiple concepts for {prompt}"
    
    def _calculate_novelty_score(self, idea: str) -> float:
        """Calculate novelty score for an idea"""
        # Simple heuristic based on word uniqueness and length
        words = idea.lower().split()
        unique_words = len(set(words))
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        uniqueness_ratio = unique_words / total_words
        length_factor = min(len(idea) / 100, 1.0)  # Longer ideas might be more novel
        
        return (uniqueness_ratio * 0.7 + length_factor * 0.3)
    
    def _calculate_feasibility_score(self, idea: str, constraints: List[CreativityConstraint]) -> float:
        """Calculate feasibility score for an idea"""
        base_score = 0.5
        
        # Adjust based on constraints
        for constraint in constraints:
            if constraint == CreativityConstraint.TIME:
                if "quick" in idea.lower() or "fast" in idea.lower():
                    base_score += 0.1
                elif "long" in idea.lower() or "extensive" in idea.lower():
                    base_score -= 0.1
            elif constraint == CreativityConstraint.RESOURCE:
                if "simple" in idea.lower() or "minimal" in idea.lower():
                    base_score += 0.1
                elif "complex" in idea.lower() or "expensive" in idea.lower():
                    base_score -= 0.1
            elif constraint == CreativityConstraint.TECHNICAL:
                if "technology" in idea.lower() or "digital" in idea.lower():
                    base_score += 0.1
                elif "manual" in idea.lower() or "traditional" in idea.lower():
                    base_score -= 0.1
        
        return max(0.0, min(1.0, base_score))
    
    def _calculate_value_score(self, idea: str) -> float:
        """Calculate value score for an idea"""
        # Simple heuristic based on positive words
        positive_words = ["improve", "enhance", "better", "efficient", "effective", "innovative", "creative", "useful", "valuable", "beneficial"]
        negative_words = ["worse", "ineffective", "useless", "pointless", "harmful", "damaging", "destructive"]
        
        idea_lower = idea.lower()
        positive_count = sum(1 for word in positive_words if word in idea_lower)
        negative_count = sum(1 for word in negative_words if word in idea_lower)
        
        base_score = 0.5
        base_score += positive_count * 0.1
        base_score -= negative_count * 0.1
        
        return max(0.0, min(1.0, base_score))
    
    def evaluate_ideas(self, session_id: str) -> Dict[str, Any]:
        """Evaluate ideas in a session and select the best one"""
        if session_id not in self.sessions:
            logger.warning(f"Session {session_id} not found")
            return {}
        
        session = self.sessions[session_id]
        if not session.ideas:
            logger.warning(f"No ideas found in session {session_id}")
            return {}
        
        # Get idea scores
        idea_scores = []
        for idea_id in session.ideas:
            if idea_id in self.ideas:
                idea = self.ideas[idea_id]
                # Combined score: novelty + feasibility + value
                combined_score = (idea.novelty_score + idea.feasibility_score + idea.value_score) / 3
                idea_scores.append((idea_id, combined_score, idea.content))
        
        # Sort by combined score
        idea_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Select best idea
        if idea_scores:
            best_idea_id, best_score, best_content = idea_scores[0]
            session.best_idea = best_idea_id
            session.session_metrics.update({
                "best_idea_score": best_score,
                "evaluation_completed": True
            })
            session.status = CreativityStatus.COMPLETED
            session.completed_at = datetime.now()
            self._save_session(session)
            
            return {
                "best_idea_id": best_idea_id,
                "best_idea_content": best_content,
                "best_score": best_score,
                "all_scores": [(idea_id, score, content) for idea_id, score, content in idea_scores]
            }
        
        return {}
    
    def get_creativity_stats(self) -> CreativityStats:
        """Get comprehensive creativity statistics"""
        total_sessions = len(self.sessions)
        total_ideas = len(self.ideas)
        
        # Calculate averages
        if self.ideas:
            avg_novelty = sum(idea.novelty_score for idea in self.ideas.values()) / len(self.ideas)
            avg_feasibility = sum(idea.feasibility_score for idea in self.ideas.values()) / len(self.ideas)
            avg_value = sum(idea.value_score for idea in self.ideas.values()) / len(self.ideas)
        else:
            avg_novelty = avg_feasibility = avg_value = 0.0
        
        # Creativity types distribution
        creativity_types = defaultdict(int)
        for session in self.sessions.values():
            creativity_types[session.session_type.value] += 1
        
        # Constraint types distribution
        constraint_types = defaultdict(int)
        for session in self.sessions.values():
            for constraint in session.constraints:
                constraint_types[constraint.value] += 1
        
        # Success rate (completed sessions)
        completed_sessions = sum(1 for s in self.sessions.values() if s.status == CreativityStatus.COMPLETED)
        success_rate = completed_sessions / max(total_sessions, 1)
        
        # Most used patterns
        most_used_patterns = sorted(
            [(p.pattern_name, p.usage_count) for p in self.patterns.values()],
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Last creativity activity
        last_creativity = max(
            (session.created_at for session in self.sessions.values()),
            default=datetime.now()
        )
        
        return CreativityStats(
            total_sessions=total_sessions,
            total_ideas=total_ideas,
            average_novelty=avg_novelty,
            average_feasibility=avg_feasibility,
            average_value=avg_value,
            creativity_types=dict(creativity_types),
            constraint_types=dict(constraint_types),
            success_rate=success_rate,
            most_used_patterns=[name for name, _ in most_used_patterns],
            last_creativity=last_creativity
        )
    
    def export_creativity_data(self, format: str = "json") -> Union[str, Dict[str, Any]]:
        """Export creativity data"""
        data = {
            "ideas": [asdict(idea) for idea in self.ideas.values()],
            "sessions": [asdict(session) for session in self.sessions.values()],
            "patterns": [asdict(pattern) for pattern in self.patterns.values()],
            "stats": asdict(self.get_creativity_stats())
        }
        
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        else:
            return data
    
    def start_creativity(self):
        """Start creativity process"""
        self.creativity_active = True
        logger.info("Started creativity process")
    
    def stop_creativity(self):
        """Stop creativity process"""
        self.creativity_active = False
        logger.info("Stopped creativity process")
    
    def clear_creativity_data(self):
        """Clear all creativity data"""
        with self.lock:
            self.ideas.clear()
            self.sessions.clear()
            self.patterns.clear()
            self.current_sessions.clear()
            
            # Clear database
            with self.db_lock:
                try:
                    conn = sqlite3.connect(self.db_path, timeout=10.0)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM creative_ideas")
                    cursor.execute("DELETE FROM creative_sessions")
                    cursor.execute("DELETE FROM creative_patterns")
                    conn.commit()
                    conn.close()
                    logger.info("Cleared all creativity data")
                except Exception as e:
                    logger.error(f"Error clearing creativity data: {e}")
