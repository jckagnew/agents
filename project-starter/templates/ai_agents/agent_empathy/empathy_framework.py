"""
Pattern 14: Agent Empathy - Complete Implementation
Emotional intelligence and user understanding system
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
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmotionType(Enum):
    """Types of emotions"""
    JOY = "joy"                     # Happiness, excitement, satisfaction
    SADNESS = "sadness"             # Grief, disappointment, melancholy
    ANGER = "anger"                 # Frustration, rage, irritation
    FEAR = "fear"                   # Anxiety, worry, terror
    SURPRISE = "surprise"           # Shock, amazement, astonishment
    DISGUST = "disgust"             # Revulsion, contempt, aversion
    TRUST = "trust"                 # Confidence, faith, reliability
    ANTICIPATION = "anticipation"   # Expectation, eagerness, hope
    NEUTRAL = "neutral"             # Calm, balanced, indifferent
    CONFUSION = "confusion"         # Uncertainty, bewilderment, perplexity

class EmpathyLevel(Enum):
    """Levels of empathy"""
    NONE = "none"                   # No emotional understanding
    BASIC = "basic"                 # Basic emotional recognition
    MODERATE = "moderate"           # Good emotional understanding
    HIGH = "high"                   # Strong emotional intelligence
    EXPERT = "expert"               # Exceptional emotional insight

class EmpathyContext(Enum):
    """Contexts for empathy"""
    PERSONAL = "personal"           # Personal conversations
    PROFESSIONAL = "professional"   # Work-related interactions
    CUSTOMER_SERVICE = "customer_service"  # Customer support
    THERAPEUTIC = "therapeutic"     # Counseling or therapy
    EDUCATIONAL = "educational"     # Teaching and learning
    SOCIAL = "social"              # Social interactions
    CRISIS = "crisis"              # Emergency or crisis situations
    CREATIVE = "creative"          # Creative collaboration

@dataclass
class EmotionalState:
    """Emotional state representation"""
    id: str
    user_id: str
    primary_emotion: EmotionType
    secondary_emotions: List[EmotionType]
    intensity: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    context: EmpathyContext
    triggers: List[str]
    expressions: List[str]
    detected_at: datetime
    duration: Optional[float] = None  # Duration in seconds
    
    def __post_init__(self):
        if self.detected_at is None:
            self.detected_at = datetime.now()

@dataclass
class EmpathyResponse:
    """Empathetic response representation"""
    id: str
    user_id: str
    emotional_state_id: str
    response_type: str
    response_content: str
    empathy_level: EmpathyLevel
    appropriateness_score: float
    effectiveness_score: float
    created_at: datetime
    feedback: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class EmpathyProfile:
    """User empathy profile"""
    id: str
    user_id: str
    emotional_patterns: Dict[str, float]
    communication_preferences: Dict[str, Any]
    sensitivity_levels: Dict[str, float]
    cultural_context: Dict[str, Any]
    interaction_history: List[str]
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

@dataclass
class EmpathyStats:
    """Empathy statistics"""
    total_interactions: int
    emotional_states_detected: int
    empathy_responses_given: int
    average_empathy_level: float
    emotion_distribution: Dict[str, int]
    context_distribution: Dict[str, int]
    effectiveness_score: float
    user_satisfaction: float
    last_interaction: datetime

class EmpathyFramework:
    """
    Comprehensive agent empathy framework
    Enables emotional intelligence and user understanding
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.storage_path = Path(self.config.get("storage_path", "empathy_data"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Threading and concurrency
        self.lock = threading.Lock()
        self.db_lock = threading.Lock()
        
        # Database setup
        self.db_path = self.storage_path / "empathy.db"
        self._init_database()
        
        # Empathy components
        self.emotional_states: Dict[str, EmotionalState] = {}
        self.empathy_responses: Dict[str, EmpathyResponse] = {}
        self.empathy_profiles: Dict[str, EmpathyProfile] = {}
        self.empathy_queue = deque()
        
        # Empathy state
        self.empathy_active = False
        self.current_empathy_level = EmpathyLevel.MODERATE
        
        # Load existing data
        self._load_emotional_states()
        self._load_empathy_responses()
        self._load_empathy_profiles()
        
        # Start empathy processor
        self._start_empathy_processor()
    
    def _init_database(self):
        """Initialize empathy database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                # Create emotional states table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS emotional_states (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        primary_emotion TEXT,
                        secondary_emotions TEXT,
                        intensity REAL,
                        confidence REAL,
                        context TEXT,
                        triggers TEXT,
                        expressions TEXT,
                        detected_at TEXT,
                        duration REAL
                    )
                """)
                
                # Create empathy responses table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS empathy_responses (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        emotional_state_id TEXT,
                        response_type TEXT,
                        response_content TEXT,
                        empathy_level TEXT,
                        appropriateness_score REAL,
                        effectiveness_score REAL,
                        created_at TEXT,
                        feedback TEXT
                    )
                """)
                
                # Create empathy profiles table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS empathy_profiles (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        emotional_patterns TEXT,
                        communication_preferences TEXT,
                        sensitivity_levels TEXT,
                        cultural_context TEXT,
                        interaction_history TEXT,
                        created_at TEXT,
                        updated_at TEXT
                    )
                """)
                
                conn.commit()
                conn.close()
                logger.info("Empathy database initialized")
            except Exception as e:
                logger.error(f"Error initializing empathy database: {e}")
    
    def _load_emotional_states(self):
        """Load emotional states from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM emotional_states")
                
                for row in cursor.fetchall():
                    state = EmotionalState(
                        id=row[0],
                        user_id=row[1],
                        primary_emotion=EmotionType(row[2]),
                        secondary_emotions=[EmotionType(e) for e in json.loads(row[3])] if row[3] else [],
                        intensity=row[4],
                        confidence=row[5],
                        context=EmpathyContext(row[6]),
                        triggers=json.loads(row[7]) if row[7] else [],
                        expressions=json.loads(row[8]) if row[8] else [],
                        detected_at=datetime.fromisoformat(row[9]),
                        duration=row[10]
                    )
                    self.emotional_states[state.id] = state
                
                conn.close()
                logger.info(f"Loaded {len(self.emotional_states)} emotional states")
            except Exception as e:
                logger.error(f"Error loading emotional states: {e}")
    
    def _load_empathy_responses(self):
        """Load empathy responses from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM empathy_responses")
                
                for row in cursor.fetchall():
                    response = EmpathyResponse(
                        id=row[0],
                        user_id=row[1],
                        emotional_state_id=row[2],
                        response_type=row[3],
                        response_content=row[4],
                        empathy_level=EmpathyLevel(row[5]),
                        appropriateness_score=row[6],
                        effectiveness_score=row[7],
                        created_at=datetime.fromisoformat(row[8]),
                        feedback=json.loads(row[9]) if row[9] else None
                    )
                    self.empathy_responses[response.id] = response
                
                conn.close()
                logger.info(f"Loaded {len(self.empathy_responses)} empathy responses")
            except Exception as e:
                logger.error(f"Error loading empathy responses: {e}")
    
    def _load_empathy_profiles(self):
        """Load empathy profiles from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM empathy_profiles")
                
                for row in cursor.fetchall():
                    profile = EmpathyProfile(
                        id=row[0],
                        user_id=row[1],
                        emotional_patterns=json.loads(row[2]),
                        communication_preferences=json.loads(row[3]),
                        sensitivity_levels=json.loads(row[4]),
                        cultural_context=json.loads(row[5]),
                        interaction_history=json.loads(row[6]),
                        created_at=datetime.fromisoformat(row[7]),
                        updated_at=datetime.fromisoformat(row[8])
                    )
                    self.empathy_profiles[profile.id] = profile
                
                conn.close()
                logger.info(f"Loaded {len(self.empathy_profiles)} empathy profiles")
            except Exception as e:
                logger.error(f"Error loading empathy profiles: {e}")
    
    def _save_emotional_state(self, state: EmotionalState):
        """Save emotional state to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO emotional_states 
                    (id, user_id, primary_emotion, secondary_emotions, intensity, confidence, 
                     context, triggers, expressions, detected_at, duration)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    state.id,
                    state.user_id,
                    state.primary_emotion.value,
                    json.dumps([e.value for e in state.secondary_emotions]),
                    state.intensity,
                    state.confidence,
                    state.context.value,
                    json.dumps(state.triggers),
                    json.dumps(state.expressions),
                    state.detected_at.isoformat(),
                    state.duration
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving emotional state {state.id}: {e}")
    
    def _save_empathy_response(self, response: EmpathyResponse):
        """Save empathy response to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO empathy_responses 
                    (id, user_id, emotional_state_id, response_type, response_content, 
                     empathy_level, appropriateness_score, effectiveness_score, created_at, feedback)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    response.id,
                    response.user_id,
                    response.emotional_state_id,
                    response.response_type,
                    response.response_content,
                    response.empathy_level.value,
                    response.appropriateness_score,
                    response.effectiveness_score,
                    response.created_at.isoformat(),
                    json.dumps(response.feedback) if response.feedback else None
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving empathy response {response.id}: {e}")
    
    def _save_empathy_profile(self, profile: EmpathyProfile):
        """Save empathy profile to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO empathy_profiles 
                    (id, user_id, emotional_patterns, communication_preferences, 
                     sensitivity_levels, cultural_context, interaction_history, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    profile.id,
                    profile.user_id,
                    json.dumps(profile.emotional_patterns),
                    json.dumps(profile.communication_preferences),
                    json.dumps(profile.sensitivity_levels),
                    json.dumps(profile.cultural_context),
                    json.dumps(profile.interaction_history),
                    profile.created_at.isoformat(),
                    profile.updated_at.isoformat()
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving empathy profile {profile.id}: {e}")
    
    def _start_empathy_processor(self):
        """Start background empathy processor"""
        def process_empathy():
            while True:
                try:
                    if self.empathy_queue:
                        empathy_task = self.empathy_queue.popleft()
                        self._process_empathy_task(empathy_task)
                    else:
                        time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Error in empathy processor: {e}")
                    time.sleep(1)
        
        thread = threading.Thread(target=process_empathy, daemon=True)
        thread.start()
        logger.info("Empathy processor started")
    
    def _process_empathy_task(self, task: Dict[str, Any]):
        """Process an empathy task"""
        try:
            task_type = task.get("type")
            
            if task_type == "emotion_detection":
                self._process_emotion_detection(task)
            elif task_type == "empathy_response":
                self._process_empathy_response(task)
            elif task_type == "profile_update":
                self._update_empathy_profile(task)
            elif task_type == "context_analysis":
                self._analyze_context(task)
            else:
                logger.warning(f"Unknown empathy task type: {task_type}")
                
        except Exception as e:
            logger.error(f"Error processing empathy task: {e}")
    
    def detect_emotion(self,
                      user_id: str,
                      text: str,
                      context: EmpathyContext = EmpathyContext.PERSONAL,
                      additional_context: Optional[Dict[str, Any]] = None) -> str:
        """Detect emotion from user input"""
        state_id = str(uuid.uuid4())
        
        # Analyze text for emotional indicators
        emotion_analysis = self._analyze_text_emotion(text)
        primary_emotion = emotion_analysis["primary_emotion"]
        secondary_emotions = emotion_analysis["secondary_emotions"]
        intensity = emotion_analysis["intensity"]
        confidence = emotion_analysis["confidence"]
        
        # Extract triggers and expressions
        triggers = self._extract_triggers(text)
        expressions = self._extract_expressions(text)
        
        # Create emotional state
        state = EmotionalState(
            id=state_id,
            user_id=user_id,
            primary_emotion=primary_emotion,
            secondary_emotions=secondary_emotions,
            intensity=intensity,
            confidence=confidence,
            context=context,
            triggers=triggers,
            expressions=expressions,
            detected_at=datetime.now()
        )
        
        with self.lock:
            self.emotional_states[state_id] = state
            self._save_emotional_state(state)
        
        # Queue for processing
        self.empathy_queue.append({
            "type": "emotion_detection",
            "state_id": state_id,
            "user_id": user_id,
            "context": context.value,
            "additional_context": additional_context or {}
        })
        
        logger.info(f"Detected emotion {primary_emotion.value} for user {user_id}")
        return state_id
    
    def _analyze_text_emotion(self, text: str) -> Dict[str, Any]:
        """Analyze text to detect emotions"""
        text_lower = text.lower()
        
        # Emotion keywords and their weights
        emotion_keywords = {
            EmotionType.JOY: ["happy", "excited", "great", "wonderful", "amazing", "fantastic", "love", "enjoy", "pleased", "delighted"],
            EmotionType.SADNESS: ["sad", "depressed", "upset", "disappointed", "hurt", "grief", "sorrow", "melancholy", "down", "blue"],
            EmotionType.ANGER: ["angry", "mad", "furious", "irritated", "annoyed", "frustrated", "rage", "outraged", "livid", "fuming"],
            EmotionType.FEAR: ["afraid", "scared", "worried", "anxious", "nervous", "terrified", "panic", "frightened", "concerned", "uneasy"],
            EmotionType.SURPRISE: ["surprised", "shocked", "amazed", "astonished", "stunned", "bewildered", "startled", "taken aback"],
            EmotionType.DISGUST: ["disgusted", "revolted", "sickened", "repulsed", "appalled", "horrified", "nauseated", "contempt"],
            EmotionType.TRUST: ["trust", "confident", "secure", "reliable", "faith", "belief", "assurance", "certainty", "dependable"],
            EmotionType.ANTICIPATION: ["excited", "eager", "hopeful", "expectant", "looking forward", "anticipating", "waiting", "expecting"],
            EmotionType.CONFUSION: ["confused", "puzzled", "bewildered", "lost", "unclear", "uncertain", "perplexed", "baffled", "mystified"]
        }
        
        # Calculate emotion scores
        emotion_scores = {}
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        # Find primary emotion
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            max_score = emotion_scores[primary_emotion]
        else:
            primary_emotion = EmotionType.NEUTRAL
            max_score = 0
        
        # Calculate intensity (0.0 to 1.0)
        intensity = min(max_score / 5.0, 1.0)  # Normalize to 0-1
        
        # Calculate confidence (0.0 to 1.0)
        total_words = len(text.split())
        confidence = min(max_score / max(total_words, 1), 1.0)
        
        # Find secondary emotions (other emotions with scores > 0)
        secondary_emotions = [emotion for emotion, score in emotion_scores.items() 
                             if score > 0 and emotion != primary_emotion]
        
        return {
            "primary_emotion": primary_emotion,
            "secondary_emotions": secondary_emotions,
            "intensity": intensity,
            "confidence": confidence
        }
    
    def _extract_triggers(self, text: str) -> List[str]:
        """Extract emotional triggers from text"""
        triggers = []
        
        # Common trigger patterns
        trigger_patterns = [
            r"because of (.+?)(?:\.|,|!|\?)",
            r"due to (.+?)(?:\.|,|!|\?)",
            r"caused by (.+?)(?:\.|,|!|\?)",
            r"when (.+?)(?:\.|,|!|\?)",
            r"after (.+?)(?:\.|,|!|\?)",
            r"since (.+?)(?:\.|,|!|\?)"
        ]
        
        for pattern in trigger_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            triggers.extend(matches)
        
        return triggers[:5]  # Limit to 5 triggers
    
    def _extract_expressions(self, text: str) -> List[str]:
        """Extract emotional expressions from text"""
        expressions = []
        
        # Common expression patterns
        expression_patterns = [
            r"i feel (.+?)(?:\.|,|!|\?)",
            r"i'm (.+?)(?:\.|,|!|\?)",
            r"i am (.+?)(?:\.|,|!|\?)",
            r"this makes me (.+?)(?:\.|,|!|\?)",
            r"i'm so (.+?)(?:\.|,|!|\?)"
        ]
        
        for pattern in expression_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            expressions.extend(matches)
        
        return expressions[:5]  # Limit to 5 expressions
    
    def generate_empathy_response(self,
                                user_id: str,
                                emotional_state_id: str,
                                response_type: str = "acknowledgment") -> str:
        """Generate an empathetic response"""
        response_id = str(uuid.uuid4())
        
        # Get emotional state
        if emotional_state_id not in self.emotional_states:
            logger.warning(f"Emotional state {emotional_state_id} not found")
            return response_id
        
        state = self.emotional_states[emotional_state_id]
        
        # Generate appropriate response
        response_content = self._generate_response_content(state, response_type)
        
        # Calculate appropriateness and effectiveness scores
        appropriateness_score = self._calculate_appropriateness_score(state, response_content)
        effectiveness_score = self._calculate_effectiveness_score(state, response_content)
        
        # Create empathy response
        response = EmpathyResponse(
            id=response_id,
            user_id=user_id,
            emotional_state_id=emotional_state_id,
            response_type=response_type,
            response_content=response_content,
            empathy_level=self.current_empathy_level,
            appropriateness_score=appropriateness_score,
            effectiveness_score=effectiveness_score,
            created_at=datetime.now()
        )
        
        with self.lock:
            self.empathy_responses[response_id] = response
            self._save_empathy_response(response)
        
        logger.info(f"Generated empathy response {response_id} for user {user_id}")
        return response_id
    
    def _generate_response_content(self, state: EmotionalState, response_type: str) -> str:
        """Generate empathetic response content"""
        emotion = state.primary_emotion
        intensity = state.intensity
        context = state.context
        
        # Base responses by emotion and intensity
        responses = {
            EmotionType.JOY: {
                "acknowledgment": "I can see you're really happy about this!",
                "validation": "That's wonderful! Your joy is completely justified.",
                "support": "I'm so glad this is bringing you happiness!",
                "encouragement": "Your enthusiasm is contagious! Keep celebrating!"
            },
            EmotionType.SADNESS: {
                "acknowledgment": "I can hear that you're feeling sad about this.",
                "validation": "It's completely understandable to feel this way.",
                "support": "I'm here for you. You don't have to go through this alone.",
                "encouragement": "It's okay to feel sad. These feelings will pass."
            },
            EmotionType.ANGER: {
                "acknowledgment": "I can tell you're really frustrated about this.",
                "validation": "Your anger is completely justified given the situation.",
                "support": "I understand why you're upset. Let's work through this together.",
                "encouragement": "It's okay to feel angry. Let's channel this energy positively."
            },
            EmotionType.FEAR: {
                "acknowledgment": "I can sense that you're feeling anxious about this.",
                "validation": "It's natural to feel worried in this situation.",
                "support": "I'm here to help you through this. You're not alone.",
                "encouragement": "Take deep breaths. We'll get through this together."
            },
            EmotionType.SURPRISE: {
                "acknowledgment": "I can see this caught you completely off guard!",
                "validation": "That's quite a surprise! I can understand your reaction.",
                "support": "Unexpected news can be overwhelming. How are you feeling?",
                "encouragement": "Sometimes surprises can lead to great opportunities!"
            },
            EmotionType.DISGUST: {
                "acknowledgment": "I can tell you're really bothered by this.",
                "validation": "Your reaction is completely understandable.",
                "support": "I understand why you feel this way. Let's address this.",
                "encouragement": "It's good that you're standing up for what you believe in."
            },
            EmotionType.TRUST: {
                "acknowledgment": "I can see you have confidence in this.",
                "validation": "Your trust is well-placed here.",
                "support": "I'm glad you feel comfortable with this decision.",
                "encouragement": "Trust is the foundation of good relationships."
            },
            EmotionType.ANTICIPATION: {
                "acknowledgment": "I can feel your excitement about this!",
                "validation": "It's great that you're looking forward to this.",
                "support": "I'm excited for you too! This sounds promising.",
                "encouragement": "Your anticipation shows how much this means to you."
            },
            EmotionType.CONFUSION: {
                "acknowledgment": "I can tell this is confusing for you.",
                "validation": "It's okay to feel uncertain about this.",
                "support": "Let me help clarify this for you.",
                "encouragement": "Confusion is often the first step to understanding."
            },
            EmotionType.NEUTRAL: {
                "acknowledgment": "I understand your perspective on this.",
                "validation": "Your balanced view is appreciated.",
                "support": "I'm here to help if you need anything.",
                "encouragement": "Sometimes a calm approach is the best way forward."
            }
        }
        
        # Get base response
        base_response = responses.get(emotion, responses[EmotionType.NEUTRAL]).get(
            response_type, "I understand how you're feeling."
        )
        
        # Adjust based on intensity
        if intensity > 0.7:
            intensity_modifier = " really"
        elif intensity > 0.4:
            intensity_modifier = " quite"
        else:
            intensity_modifier = ""
        
        # Adjust based on context
        context_modifier = ""
        if context == EmpathyContext.PROFESSIONAL:
            context_modifier = " I appreciate you sharing this with me."
        elif context == EmpathyContext.CUSTOMER_SERVICE:
            context_modifier = " I'm here to help resolve this for you."
        elif context == EmpathyContext.CRISIS:
            context_modifier = " This is a serious situation and I'm here to support you."
        
        # Combine response
        response_content = base_response.replace("really", f"really{intensity_modifier}")
        response_content += context_modifier
        
        return response_content
    
    def _calculate_appropriateness_score(self, state: EmotionalState, response: str) -> float:
        """Calculate appropriateness score for response"""
        base_score = 0.5
        
        # Adjust based on emotion match
        emotion = state.primary_emotion
        if emotion in [EmotionType.JOY, EmotionType.ANTICIPATION]:
            if "happy" in response.lower() or "excited" in response.lower():
                base_score += 0.3
        elif emotion in [EmotionType.SADNESS, EmotionType.FEAR]:
            if "understand" in response.lower() or "support" in response.lower():
                base_score += 0.3
        elif emotion == EmotionType.ANGER:
            if "frustrated" in response.lower() or "upset" in response.lower():
                base_score += 0.3
        elif emotion == EmotionType.CONFUSION:
            if "confusing" in response.lower() or "clarify" in response.lower():
                base_score += 0.3
        
        # Adjust based on context
        if state.context == EmpathyContext.PROFESSIONAL:
            if "professional" in response.lower() or "appreciate" in response.lower():
                base_score += 0.1
        elif state.context == EmpathyContext.CRISIS:
            if "serious" in response.lower() or "support" in response.lower():
                base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _calculate_effectiveness_score(self, state: EmotionalState, response: str) -> float:
        """Calculate effectiveness score for response"""
        base_score = 0.5
        
        # Adjust based on response length (not too short, not too long)
        word_count = len(response.split())
        if 10 <= word_count <= 30:
            base_score += 0.2
        elif word_count < 5 or word_count > 50:
            base_score -= 0.2
        
        # Adjust based on emotional keywords
        emotional_keywords = ["understand", "feel", "here", "support", "help", "together"]
        keyword_count = sum(1 for keyword in emotional_keywords if keyword in response.lower())
        base_score += keyword_count * 0.05
        
        # Adjust based on intensity match
        if state.intensity > 0.7 and "really" in response.lower():
            base_score += 0.1
        elif state.intensity < 0.3 and "really" not in response.lower():
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def create_empathy_profile(self,
                             user_id: str,
                             emotional_patterns: Optional[Dict[str, float]] = None,
                             communication_preferences: Optional[Dict[str, Any]] = None,
                             sensitivity_levels: Optional[Dict[str, float]] = None,
                             cultural_context: Optional[Dict[str, Any]] = None) -> str:
        """Create an empathy profile for a user"""
        profile_id = str(uuid.uuid4())
        
        # Default values
        if emotional_patterns is None:
            emotional_patterns = {
                "joy": 0.5,
                "sadness": 0.5,
                "anger": 0.5,
                "fear": 0.5,
                "surprise": 0.5,
                "disgust": 0.5,
                "trust": 0.5,
                "anticipation": 0.5,
                "confusion": 0.5,
                "neutral": 0.5
            }
        
        if communication_preferences is None:
            communication_preferences = {
                "formality_level": "medium",
                "response_length": "medium",
                "empathy_style": "supportive",
                "language_preference": "english"
            }
        
        if sensitivity_levels is None:
            sensitivity_levels = {
                "emotional_sensitivity": 0.5,
                "criticism_sensitivity": 0.5,
                "praise_sensitivity": 0.5,
                "change_sensitivity": 0.5
            }
        
        if cultural_context is None:
            cultural_context = {
                "culture": "western",
                "communication_style": "direct",
                "emotional_expression": "moderate",
                "formality_preference": "medium"
            }
        
        profile = EmpathyProfile(
            id=profile_id,
            user_id=user_id,
            emotional_patterns=emotional_patterns,
            communication_preferences=communication_preferences,
            sensitivity_levels=sensitivity_levels,
            cultural_context=cultural_context,
            interaction_history=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with self.lock:
            self.empathy_profiles[profile_id] = profile
            self._save_empathy_profile(profile)
        
        logger.info(f"Created empathy profile {profile_id} for user {user_id}")
        return profile_id
    
    def get_empathy_stats(self) -> EmpathyStats:
        """Get comprehensive empathy statistics"""
        total_interactions = len(self.emotional_states)
        emotional_states_detected = len(self.emotional_states)
        empathy_responses_given = len(self.empathy_responses)
        
        # Calculate average empathy level
        if self.empathy_responses:
            empathy_levels = [response.empathy_level.value for response in self.empathy_responses.values()]
            level_scores = {"none": 0, "basic": 1, "moderate": 2, "high": 3, "expert": 4}
            avg_level_score = sum(level_scores[level] for level in empathy_levels) / len(empathy_levels)
            avg_empathy_level = avg_level_score / 4.0  # Normalize to 0-1
        else:
            avg_empathy_level = 0.0
        
        # Emotion distribution
        emotion_distribution = defaultdict(int)
        for state in self.emotional_states.values():
            emotion_distribution[state.primary_emotion.value] += 1
        
        # Context distribution
        context_distribution = defaultdict(int)
        for state in self.emotional_states.values():
            context_distribution[state.context.value] += 1
        
        # Calculate effectiveness score
        if self.empathy_responses:
            effectiveness_scores = [response.effectiveness_score for response in self.empathy_responses.values()]
            effectiveness_score = sum(effectiveness_scores) / len(effectiveness_scores)
        else:
            effectiveness_score = 0.0
        
        # Calculate user satisfaction (placeholder)
        user_satisfaction = min(effectiveness_score * 1.2, 1.0)
        
        # Last interaction
        last_interaction = max(
            (state.detected_at for state in self.emotional_states.values()),
            default=datetime.now()
        )
        
        return EmpathyStats(
            total_interactions=total_interactions,
            emotional_states_detected=emotional_states_detected,
            empathy_responses_given=empathy_responses_given,
            average_empathy_level=avg_empathy_level,
            emotion_distribution=dict(emotion_distribution),
            context_distribution=dict(context_distribution),
            effectiveness_score=effectiveness_score,
            user_satisfaction=user_satisfaction,
            last_interaction=last_interaction
        )
    
    def export_empathy_data(self, format: str = "json") -> Union[str, Dict[str, Any]]:
        """Export empathy data"""
        data = {
            "emotional_states": [asdict(state) for state in self.emotional_states.values()],
            "empathy_responses": [asdict(response) for response in self.empathy_responses.values()],
            "empathy_profiles": [asdict(profile) for profile in self.empathy_profiles.values()],
            "stats": asdict(self.get_empathy_stats())
        }
        
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        else:
            return data
    
    def start_empathy(self):
        """Start empathy process"""
        self.empathy_active = True
        logger.info("Started empathy process")
    
    def stop_empathy(self):
        """Stop empathy process"""
        self.empathy_active = False
        logger.info("Stopped empathy process")
    
    def clear_empathy_data(self):
        """Clear all empathy data"""
        with self.lock:
            self.emotional_states.clear()
            self.empathy_responses.clear()
            self.empathy_profiles.clear()
            
            # Clear database
            with self.db_lock:
                try:
                    conn = sqlite3.connect(self.db_path, timeout=10.0)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM emotional_states")
                    cursor.execute("DELETE FROM empathy_responses")
                    cursor.execute("DELETE FROM empathy_profiles")
                    conn.commit()
                    conn.close()
                    logger.info("Cleared all empathy data")
                except Exception as e:
                    logger.error(f"Error clearing empathy data: {e}")
