"""
Pattern 4: Agent Learning - Complete Implementation
Comprehensive agent learning and adaptation system built on existing memory framework
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
import pickle
import hashlib
import time

# Optional ML dependencies
try:
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    from sklearn.metrics.pairwise import cosine_similarity
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    # Mock classes for when sklearn is not available
    class TfidfVectorizer:
        def __init__(self, **kwargs):
            pass
        def fit_transform(self, texts):
            return [[0.0] * 10] * len(texts)
    
    class KMeans:
        def __init__(self, **kwargs):
            pass
        def fit_predict(self, data):
            return [0] * len(data)
    
    def cosine_similarity(a, b):
        return [[0.5]]  # Mock similarity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LearningType(Enum):
    """Types of learning"""
    SUPERVISED = "supervised"           # Learning from labeled examples
    UNSUPERVISED = "unsupervised"       # Learning from patterns in data
    REINFORCEMENT = "reinforcement"     # Learning from rewards/penalties
    TRANSFER = "transfer"               # Learning from related tasks
    META = "meta"                       # Learning how to learn
    EXPERIENTIAL = "experiential"       # Learning from experience
    COLLABORATIVE = "collaborative"     # Learning from other agents
    ADAPTIVE = "adaptive"               # Learning to adapt behavior

class LearningStatus(Enum):
    """Learning status"""
    ACTIVE = "active"                   # Currently learning
    PAUSED = "paused"                   # Learning paused
    COMPLETED = "completed"             # Learning completed
    FAILED = "failed"                   # Learning failed
    IDLE = "idle"                       # No active learning

class LearningStrategy(Enum):
    """Learning strategies"""
    INCREMENTAL = "incremental"         # Learn incrementally
    BATCH = "batch"                     # Learn in batches
    ONLINE = "online"                   # Continuous online learning
    EPISODIC = "episodic"               # Learn from episodes
    CONTINUOUS = "continuous"           # Continuous learning
    ADAPTIVE = "adaptive"               # Adaptive learning rate

@dataclass
class LearningExample:
    """Learning example"""
    id: str
    input_data: Dict[str, Any]
    expected_output: Any
    actual_output: Any
    feedback: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    timestamp: datetime = None
    quality_score: float = 0.0
    difficulty: float = 0.0
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class LearningPattern:
    """Learned pattern"""
    id: str
    pattern_type: str
    pattern_data: Dict[str, Any]
    confidence: float
    frequency: int
    success_rate: float
    last_used: datetime
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

@dataclass
class LearningModel:
    """Learning model"""
    id: str
    model_type: str
    model_data: bytes
    performance_metrics: Dict[str, float]
    training_examples: int
    last_trained: datetime
    version: str
    is_active: bool = True
    
    def __post_init__(self):
        if self.last_trained is None:
            self.last_trained = datetime.now()

@dataclass
class LearningStats:
    """Learning statistics"""
    total_examples: int
    total_patterns: int
    total_models: int
    learning_accuracy: float
    learning_speed: float
    adaptation_rate: float
    transfer_effectiveness: float
    collaboration_benefit: float
    learning_types: Dict[str, int]
    learning_strategies: Dict[str, int]
    performance_trends: List[float]
    last_learning: datetime

class LearningFramework:
    """
    Comprehensive agent learning framework
    Built on existing memory framework with advanced learning capabilities
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.storage_path = Path(self.config.get("storage_path", "learning_data"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Threading and concurrency
        self.lock = threading.Lock()
        self.db_lock = threading.Lock()
        
        # Database setup
        self.db_path = self.storage_path / "learning.db"
        self._init_database()
        
        # Learning components
        self.examples: Dict[str, LearningExample] = {}
        self.patterns: Dict[str, LearningPattern] = {}
        self.models: Dict[str, LearningModel] = {}
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.clusterer = KMeans(n_clusters=10, random_state=42)
        self.ml_available = ML_AVAILABLE
        
        # Learning state
        self.learning_active = False
        self.current_learning_type = None
        self.learning_queue = deque()
        self.adaptation_threshold = 0.7
        
        # Load existing data
        self._load_examples()
        self._load_patterns()
        self._load_models()
        
        # Start learning processor
        self._start_learning_processor()
    
    def _init_database(self):
        """Initialize learning database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                # Create examples table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS learning_examples (
                        id TEXT PRIMARY KEY,
                        input_data TEXT,
                        expected_output TEXT,
                        actual_output TEXT,
                        feedback TEXT,
                        context TEXT,
                        timestamp TEXT,
                        quality_score REAL,
                        difficulty REAL
                    )
                """)
                
                # Create patterns table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS learning_patterns (
                        id TEXT PRIMARY KEY,
                        pattern_type TEXT,
                        pattern_data TEXT,
                        confidence REAL,
                        frequency INTEGER,
                        success_rate REAL,
                        last_used TEXT,
                        created_at TEXT,
                        updated_at TEXT
                    )
                """)
                
                # Create models table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS learning_models (
                        id TEXT PRIMARY KEY,
                        model_type TEXT,
                        model_data BLOB,
                        performance_metrics TEXT,
                        training_examples INTEGER,
                        last_trained TEXT,
                        version TEXT,
                        is_active BOOLEAN
                    )
                """)
                
                conn.commit()
                conn.close()
                logger.info("Learning database initialized")
            except Exception as e:
                logger.error(f"Error initializing learning database: {e}")
    
    def _load_examples(self):
        """Load learning examples from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM learning_examples")
                
                for row in cursor.fetchall():
                    example = LearningExample(
                        id=row[0],
                        input_data=json.loads(row[1]),
                        expected_output=json.loads(row[2]) if row[2] else None,
                        actual_output=json.loads(row[3]) if row[3] else None,
                        feedback=json.loads(row[4]) if row[4] else None,
                        context=json.loads(row[5]) if row[5] else None,
                        timestamp=datetime.fromisoformat(row[6]),
                        quality_score=row[7],
                        difficulty=row[8]
                    )
                    self.examples[example.id] = example
                
                conn.close()
                logger.info(f"Loaded {len(self.examples)} learning examples")
            except Exception as e:
                logger.error(f"Error loading examples: {e}")
    
    def _load_patterns(self):
        """Load learning patterns from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM learning_patterns")
                
                for row in cursor.fetchall():
                    pattern = LearningPattern(
                        id=row[0],
                        pattern_type=row[1],
                        pattern_data=json.loads(row[2]),
                        confidence=row[3],
                        frequency=row[4],
                        success_rate=row[5],
                        last_used=datetime.fromisoformat(row[6]),
                        created_at=datetime.fromisoformat(row[7]),
                        updated_at=datetime.fromisoformat(row[8])
                    )
                    self.patterns[pattern.id] = pattern
                
                conn.close()
                logger.info(f"Loaded {len(self.patterns)} learning patterns")
            except Exception as e:
                logger.error(f"Error loading patterns: {e}")
    
    def _load_models(self):
        """Load learning models from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM learning_models")
                
                for row in cursor.fetchall():
                    model = LearningModel(
                        id=row[0],
                        model_type=row[1],
                        model_data=row[2],
                        performance_metrics=json.loads(row[3]),
                        training_examples=row[4],
                        last_trained=datetime.fromisoformat(row[5]),
                        version=row[6],
                        is_active=bool(row[7])
                    )
                    self.models[model.id] = model
                
                conn.close()
                logger.info(f"Loaded {len(self.models)} learning models")
            except Exception as e:
                logger.error(f"Error loading models: {e}")
    
    def _save_example(self, example: LearningExample):
        """Save learning example to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO learning_examples 
                    (id, input_data, expected_output, actual_output, feedback, context, 
                     timestamp, quality_score, difficulty)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    example.id,
                    json.dumps(example.input_data),
                    json.dumps(example.expected_output) if example.expected_output else None,
                    json.dumps(example.actual_output) if example.actual_output else None,
                    json.dumps(example.feedback) if example.feedback else None,
                    json.dumps(example.context) if example.context else None,
                    example.timestamp.isoformat(),
                    example.quality_score,
                    example.difficulty
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving example {example.id}: {e}")
    
    def _save_pattern(self, pattern: LearningPattern):
        """Save learning pattern to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO learning_patterns 
                    (id, pattern_type, pattern_data, confidence, frequency, success_rate, 
                     last_used, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pattern.id,
                    pattern.pattern_type,
                    json.dumps(pattern.pattern_data),
                    pattern.confidence,
                    pattern.frequency,
                    pattern.success_rate,
                    pattern.last_used.isoformat(),
                    pattern.created_at.isoformat(),
                    pattern.updated_at.isoformat()
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving pattern {pattern.id}: {e}")
    
    def _save_model(self, model: LearningModel):
        """Save learning model to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO learning_models 
                    (id, model_type, model_data, performance_metrics, training_examples, 
                     last_trained, version, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    model.id,
                    model.model_type,
                    model.model_data,
                    json.dumps(model.performance_metrics),
                    model.training_examples,
                    model.last_trained.isoformat(),
                    model.version,
                    model.is_active
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving model {model.id}: {e}")
    
    def _start_learning_processor(self):
        """Start background learning processor"""
        def process_learning():
            while True:
                try:
                    if self.learning_queue:
                        learning_task = self.learning_queue.popleft()
                        self._process_learning_task(learning_task)
                    else:
                        time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Error in learning processor: {e}")
                    time.sleep(1)
        
        thread = threading.Thread(target=process_learning, daemon=True)
        thread.start()
        logger.info("Learning processor started")
    
    def _process_learning_task(self, task: Dict[str, Any]):
        """Process a learning task"""
        try:
            task_type = task.get("type")
            
            if task_type == "supervised_learning":
                self._process_supervised_learning(task)
            elif task_type == "unsupervised_learning":
                self._process_unsupervised_learning(task)
            elif task_type == "reinforcement_learning":
                self._process_reinforcement_learning(task)
            elif task_type == "pattern_extraction":
                self._extract_patterns(task)
            elif task_type == "model_training":
                self._train_model(task)
            else:
                logger.warning(f"Unknown learning task type: {task_type}")
                
        except Exception as e:
            logger.error(f"Error processing learning task: {e}")
    
    def add_learning_example(self, 
                           input_data: Dict[str, Any],
                           expected_output: Any = None,
                           actual_output: Any = None,
                           feedback: Optional[Dict[str, Any]] = None,
                           context: Optional[Dict[str, Any]] = None,
                           learning_type: LearningType = LearningType.EXPERIENTIAL) -> str:
        """Add a learning example"""
        example_id = str(uuid.uuid4())
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(input_data, expected_output, actual_output, feedback)
        
        # Calculate difficulty
        difficulty = self._calculate_difficulty(input_data, expected_output)
        
        example = LearningExample(
            id=example_id,
            input_data=input_data,
            expected_output=expected_output,
            actual_output=actual_output,
            feedback=feedback,
            context=context,
            quality_score=quality_score,
            difficulty=difficulty
        )
        
        with self.lock:
            self.examples[example_id] = example
            self._save_example(example)
        
        # Queue for learning
        self.learning_queue.append({
            "type": "supervised_learning",
            "example_id": example_id,
            "learning_type": learning_type.value
        })
        
        logger.info(f"Added learning example {example_id}")
        return example_id
    
    def _calculate_quality_score(self, input_data: Dict[str, Any], 
                                expected_output: Any, actual_output: Any, 
                                feedback: Optional[Dict[str, Any]]) -> float:
        """Calculate quality score for learning example"""
        score = 0.0
        
        # Base score from feedback
        if feedback:
            score += feedback.get("quality", 0.5)
        
        # Score from output comparison
        if expected_output and actual_output:
            if expected_output == actual_output:
                score += 0.8
            else:
                # Partial credit for similar outputs
                similarity = self._calculate_similarity(expected_output, actual_output)
                score += similarity * 0.6
        
        # Score from input complexity
        input_complexity = len(str(input_data))
        if input_complexity > 100:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_difficulty(self, input_data: Dict[str, Any], expected_output: Any) -> float:
        """Calculate difficulty of learning example"""
        difficulty = 0.0
        
        # Input complexity
        input_str = str(input_data)
        difficulty += min(len(input_str) / 1000, 0.3)
        
        # Output complexity
        if expected_output:
            output_str = str(expected_output)
            difficulty += min(len(output_str) / 500, 0.3)
        
        # Data structure complexity
        if isinstance(input_data, dict):
            difficulty += len(input_data) * 0.05
        
        return min(difficulty, 1.0)
    
    def _calculate_similarity(self, output1: Any, output2: Any) -> float:
        """Calculate similarity between two outputs"""
        try:
            str1 = str(output1)
            str2 = str(output2)
            
            if str1 == str2:
                return 1.0
            
            # Simple similarity based on common words
            words1 = set(str1.lower().split())
            words2 = set(str2.lower().split())
            
            if not words1 and not words2:
                return 1.0
            if not words1 or not words2:
                return 0.0
            
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            
            return intersection / union if union > 0 else 0.0
        except:
            return 0.0
    
    def _process_supervised_learning(self, task: Dict[str, Any]):
        """Process supervised learning task"""
        example_id = task.get("example_id")
        if example_id not in self.examples:
            return
        
        example = self.examples[example_id]
        
        # Extract features from input
        features = self._extract_features(example.input_data)
        
        # Update existing patterns or create new ones
        self._update_patterns_from_example(example, features)
        
        # Train models if enough examples
        if len(self.examples) % 10 == 0:
            self._train_models()
        
        logger.info(f"Processed supervised learning for example {example_id}")
    
    def _process_unsupervised_learning(self, task: Dict[str, Any]):
        """Process unsupervised learning task"""
        # Extract patterns from all examples
        self._extract_patterns_from_examples()
        
        # Cluster similar examples
        self._cluster_examples()
        
        logger.info("Processed unsupervised learning")
    
    def _process_reinforcement_learning(self, task: Dict[str, Any]):
        """Process reinforcement learning task"""
        # Update patterns based on rewards/penalties
        reward = task.get("reward", 0.0)
        action = task.get("action")
        
        if action and reward != 0:
            self._update_patterns_from_reward(action, reward)
        
        logger.info(f"Processed reinforcement learning with reward {reward}")
    
    def _extract_features(self, input_data: Dict[str, Any]) -> List[float]:
        """Extract features from input data"""
        features = []
        
        # Text features
        text_content = str(input_data)
        if text_content:
            try:
                # Use TF-IDF for text features
                tfidf_matrix = self.vectorizer.fit_transform([text_content])
                features.extend(tfidf_matrix.toarray()[0])
            except:
                # Fallback to simple features
                features.extend([len(text_content), text_content.count(' '), text_content.count('\n')])
        
        # Structural features
        features.append(len(input_data) if isinstance(input_data, dict) else 1)
        features.append(sum(1 for v in input_data.values() if isinstance(v, str)) if isinstance(input_data, dict) else 0)
        
        return features
    
    def _update_patterns_from_example(self, example: LearningExample, features: List[float]):
        """Update patterns based on learning example"""
        # Find similar patterns
        similar_patterns = self._find_similar_patterns(features)
        
        if similar_patterns:
            # Update existing pattern
            pattern_id = similar_patterns[0]
            pattern = self.patterns[pattern_id]
            pattern.frequency += 1
            pattern.success_rate = (pattern.success_rate * (pattern.frequency - 1) + example.quality_score) / pattern.frequency
            pattern.last_used = datetime.now()
            pattern.updated_at = datetime.now()
            self._save_pattern(pattern)
        else:
            # Create new pattern
            pattern_id = str(uuid.uuid4())
            pattern = LearningPattern(
                id=pattern_id,
                pattern_type="learned",
                pattern_data={"features": features, "input_type": type(example.input_data).__name__},
                confidence=example.quality_score,
                frequency=1,
                success_rate=example.quality_score,
                last_used=datetime.now(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.patterns[pattern_id] = pattern
            self._save_pattern(pattern)
    
    def _find_similar_patterns(self, features: List[float], threshold: float = 0.7) -> List[str]:
        """Find patterns similar to given features"""
        similar_patterns = []
        
        for pattern_id, pattern in self.patterns.items():
            if "features" in pattern.pattern_data:
                pattern_features = pattern.pattern_data["features"]
                if len(pattern_features) == len(features):
                    # Calculate cosine similarity
                    similarity = cosine_similarity([features], [pattern_features])[0][0]
                    if similarity >= threshold:
                        similar_patterns.append(pattern_id)
        
        return similar_patterns
    
    def _extract_patterns_from_examples(self):
        """Extract patterns from all examples using unsupervised learning"""
        if len(self.examples) < 5:
            return
        
        # Extract features from all examples
        all_features = []
        example_ids = []
        
        for example_id, example in self.examples.items():
            features = self._extract_features(example.input_data)
            all_features.append(features)
            example_ids.append(example_id)
        
        if not all_features:
            return
        
        # Normalize features
        max_len = max(len(f) for f in all_features)
        normalized_features = []
        for features in all_features:
            normalized = features + [0.0] * (max_len - len(features))
            normalized_features.append(normalized)
        
        # Cluster examples
        try:
            if self.ml_available:
                clusters = self.clusterer.fit_predict(normalized_features)
                
                # Create patterns for each cluster
                for cluster_id in set(clusters):
                    cluster_examples = [example_ids[i] for i, c in enumerate(clusters) if c == cluster_id]
                    if len(cluster_examples) >= 2:
                        self._create_pattern_from_cluster(cluster_id, cluster_examples, normalized_features)
            else:
                # Simple clustering when ML is not available
                logger.info("ML not available, using simple pattern extraction")
                self._simple_pattern_extraction(example_ids, normalized_features)
        except Exception as e:
            logger.error(f"Error in pattern extraction: {e}")
    
    def _create_pattern_from_cluster(self, cluster_id: int, example_ids: List[str], features: List[List[float]]):
        """Create pattern from cluster of examples"""
        cluster_features = [features[i] for i, example_id in enumerate(example_ids) if example_id in self.examples]
        
        if not cluster_features:
            return
        
        # Calculate centroid
        centroid = [sum(f[i] for f in cluster_features) / len(cluster_features) for i in range(len(cluster_features[0]))]
        
        # Calculate average quality
        quality_scores = [self.examples[eid].quality_score for eid in example_ids if eid in self.examples]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
        
        pattern_id = str(uuid.uuid4())
        pattern = LearningPattern(
            id=pattern_id,
            pattern_type="cluster",
            pattern_data={"centroid": centroid, "cluster_id": cluster_id, "example_count": len(example_ids)},
            confidence=avg_quality,
            frequency=len(example_ids),
            success_rate=avg_quality,
            last_used=datetime.now(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.patterns[pattern_id] = pattern
        self._save_pattern(pattern)
        logger.info(f"Created pattern from cluster {cluster_id} with {len(example_ids)} examples")
    
    def _simple_pattern_extraction(self, example_ids: List[str], features: List[List[float]]):
        """Simple pattern extraction when ML is not available"""
        if len(example_ids) < 2:
            return
        
        # Group examples by similarity (simple approach)
        groups = []
        used = set()
        
        for i, example_id in enumerate(example_ids):
            if example_id in used:
                continue
            
            group = [example_id]
            used.add(example_id)
            
            # Find similar examples
            for j, other_id in enumerate(example_ids):
                if other_id in used or i == j:
                    continue
                
                # Simple similarity based on feature length and values
                if len(features[i]) == len(features[j]):
                    similarity = sum(1 for a, b in zip(features[i], features[j]) if abs(a - b) < 0.1)
                    if similarity > len(features[i]) * 0.5:  # 50% similarity threshold
                        group.append(other_id)
                        used.add(other_id)
            
            if len(group) >= 2:
                groups.append(group)
        
        # Create patterns for each group
        for group_id, group in enumerate(groups):
            self._create_pattern_from_cluster(group_id, group, features)
    
    def _cluster_examples(self):
        """Cluster examples using K-means"""
        if len(self.examples) < 10:
            return
        
        # Extract features
        all_features = []
        example_ids = []
        
        for example_id, example in self.examples.items():
            features = self._extract_features(example.input_data)
            all_features.append(features)
            example_ids.append(example_id)
        
        if not all_features:
            return
        
        # Normalize features
        max_len = max(len(f) for f in all_features)
        normalized_features = []
        for features in all_features:
            normalized = features + [0.0] * (max_len - len(features))
            normalized_features.append(normalized)
        
        # Perform clustering
        try:
            if self.ml_available:
                n_clusters = min(10, len(normalized_features) // 2)
                if n_clusters >= 2:
                    clusters = KMeans(n_clusters=n_clusters, random_state=42).fit_predict(normalized_features)
                    
                    # Update example clustering info
                    for i, example_id in enumerate(example_ids):
                        if example_id in self.examples:
                            example = self.examples[example_id]
                            if not example.context:
                                example.context = {}
                            example.context["cluster_id"] = int(clusters[i])
                            self._save_example(example)
            else:
                # Simple clustering when ML is not available
                logger.info("ML not available, skipping advanced clustering")
        except Exception as e:
            logger.error(f"Error in clustering: {e}")
    
    def _train_models(self):
        """Train learning models"""
        if len(self.examples) < 5:
            return
        
        # Simple model training (placeholder for more sophisticated models)
        model_id = str(uuid.uuid4())
        
        # Calculate performance metrics
        quality_scores = [ex.quality_score for ex in self.examples.values()]
        avg_quality = sum(quality_scores) / len(quality_scores)
        
        model = LearningModel(
            id=model_id,
            model_type="simple_classifier",
            model_data=pickle.dumps({"examples": len(self.examples), "avg_quality": avg_quality}),
            performance_metrics={"accuracy": avg_quality, "examples_trained": len(self.examples)},
            training_examples=len(self.examples),
            version="1.0"
        )
        
        self.models[model_id] = model
        self._save_model(model)
        logger.info(f"Trained model {model_id} with {len(self.examples)} examples")
    
    def _update_patterns_from_reward(self, action: str, reward: float):
        """Update patterns based on reinforcement learning reward"""
        # Find patterns related to the action
        for pattern_id, pattern in self.patterns.items():
            if action in str(pattern.pattern_data):
                # Update pattern based on reward
                if reward > 0:
                    pattern.confidence = min(pattern.confidence + 0.1, 1.0)
                    pattern.success_rate = (pattern.success_rate * pattern.frequency + 1.0) / (pattern.frequency + 1)
                else:
                    pattern.confidence = max(pattern.confidence - 0.1, 0.0)
                    pattern.success_rate = (pattern.success_rate * pattern.frequency + 0.0) / (pattern.frequency + 1)
                
                pattern.frequency += 1
                pattern.updated_at = datetime.now()
                self._save_pattern(pattern)
    
    def get_learning_recommendations(self, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get learning recommendations based on input"""
        recommendations = []
        
        # Extract features
        features = self._extract_features(input_data)
        
        # Find similar patterns
        similar_patterns = self._find_similar_patterns(features, threshold=0.5)
        
        for pattern_id in similar_patterns:
            pattern = self.patterns[pattern_id]
            recommendations.append({
                "pattern_id": pattern_id,
                "confidence": pattern.confidence,
                "success_rate": pattern.success_rate,
                "recommendation": f"Use pattern {pattern.pattern_type} (confidence: {pattern.confidence:.2f})"
            })
        
        # Sort by confidence
        recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def get_learning_stats(self) -> LearningStats:
        """Get comprehensive learning statistics"""
        quality_scores = [ex.quality_score for ex in self.examples.values()]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        # Calculate learning speed (examples per hour)
        if self.examples:
            time_span = (datetime.now() - min(ex.timestamp for ex in self.examples.values())).total_seconds() / 3600
            learning_speed = len(self.examples) / max(time_span, 1)
        else:
            learning_speed = 0.0
        
        # Calculate adaptation rate
        recent_patterns = [p for p in self.patterns.values() if (datetime.now() - p.updated_at).days < 7]
        adaptation_rate = len(recent_patterns) / max(len(self.patterns), 1)
        
        # Calculate transfer effectiveness
        transfer_patterns = [p for p in self.patterns.values() if p.pattern_type == "transfer"]
        transfer_effectiveness = len(transfer_patterns) / max(len(self.patterns), 1)
        
        # Calculate collaboration benefit
        collaborative_examples = [ex for ex in self.examples.values() if ex.context and ex.context.get("collaborative", False)]
        collaboration_benefit = len(collaborative_examples) / max(len(self.examples), 1)
        
        # Learning types distribution
        learning_types = defaultdict(int)
        for ex in self.examples.values():
            if ex.context and "learning_type" in ex.context:
                learning_types[ex.context["learning_type"]] += 1
        
        # Learning strategies distribution
        learning_strategies = defaultdict(int)
        for ex in self.examples.values():
            if ex.context and "strategy" in ex.context:
                learning_strategies[ex.context["strategy"]] += 1
        
        # Performance trends (last 10 learning sessions)
        performance_trends = quality_scores[-10:] if len(quality_scores) >= 10 else quality_scores
        
        # Last learning time
        last_learning = max((ex.timestamp for ex in self.examples.values()), default=datetime.now())
        
        return LearningStats(
            total_examples=len(self.examples),
            total_patterns=len(self.patterns),
            total_models=len(self.models),
            learning_accuracy=avg_quality,
            learning_speed=learning_speed,
            adaptation_rate=adaptation_rate,
            transfer_effectiveness=transfer_effectiveness,
            collaboration_benefit=collaboration_benefit,
            learning_types=dict(learning_types),
            learning_strategies=dict(learning_strategies),
            performance_trends=performance_trends,
            last_learning=last_learning
        )
    
    def export_learning_data(self, format: str = "json") -> Union[str, Dict[str, Any]]:
        """Export learning data"""
        data = {
            "examples": [asdict(ex) for ex in self.examples.values()],
            "patterns": [asdict(p) for p in self.patterns.values()],
            "models": [{"id": m.id, "model_type": m.model_type, "performance_metrics": m.performance_metrics, 
                       "training_examples": m.training_examples, "version": m.version, "is_active": m.is_active} 
                      for m in self.models.values()],
            "stats": asdict(self.get_learning_stats())
        }
        
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        else:
            return data
    
    def start_learning(self, learning_type: LearningType = LearningType.EXPERIENTIAL):
        """Start learning process"""
        self.learning_active = True
        self.current_learning_type = learning_type
        
        # Queue unsupervised learning
        self.learning_queue.append({
            "type": "unsupervised_learning",
            "learning_type": learning_type.value
        })
        
        logger.info(f"Started learning process: {learning_type.value}")
    
    def stop_learning(self):
        """Stop learning process"""
        self.learning_active = False
        self.current_learning_type = None
        logger.info("Stopped learning process")
    
    def clear_learning_data(self):
        """Clear all learning data"""
        with self.lock:
            self.examples.clear()
            self.patterns.clear()
            self.models.clear()
            
            # Clear database
            with self.db_lock:
                try:
                    conn = sqlite3.connect(self.db_path, timeout=10.0)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM learning_examples")
                    cursor.execute("DELETE FROM learning_patterns")
                    cursor.execute("DELETE FROM learning_models")
                    conn.commit()
                    conn.close()
                    logger.info("Cleared all learning data")
                except Exception as e:
                    logger.error(f"Error clearing learning data: {e}")
