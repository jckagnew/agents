"""
Pattern 12: Agent Adaptation - Complete Implementation
Dynamic behavior modification and environmental adaptation system
Built on existing communication framework with advanced adaptation capabilities
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdaptationType(Enum):
    """Types of adaptation"""
    BEHAVIORAL = "behavioral"         # Adapt behavior patterns
    COMMUNICATION = "communication"   # Adapt communication style
    PERSONALITY = "personality"       # Adapt personality traits
    CONTEXTUAL = "contextual"         # Adapt to context changes
    ENVIRONMENTAL = "environmental"   # Adapt to environment changes
    TEMPORAL = "temporal"             # Adapt over time
    SOCIAL = "social"                 # Adapt to social context
    TASK_SPECIFIC = "task_specific"   # Adapt to specific tasks

class AdaptationTrigger(Enum):
    """Adaptation triggers"""
    PERFORMANCE = "performance"       # Based on performance metrics
    FEEDBACK = "feedback"             # Based on user feedback
    CONTEXT_CHANGE = "context_change" # Context has changed
    ENVIRONMENT_CHANGE = "environment_change" # Environment has changed
    TIME_BASED = "time_based"         # Time-based adaptation
    SOCIAL_CUE = "social_cue"         # Social cues detected
    TASK_CHANGE = "task_change"       # Task type changed
    ERROR_RATE = "error_rate"         # Error rate threshold

class AdaptationStatus(Enum):
    """Adaptation status"""
    ACTIVE = "active"                 # Currently adapting
    PAUSED = "paused"                 # Adaptation paused
    COMPLETED = "completed"           # Adaptation completed
    FAILED = "failed"                 # Adaptation failed
    IDLE = "idle"                     # No active adaptation

@dataclass
class AdaptationProfile:
    """Agent adaptation profile"""
    id: str
    agent_id: str
    profile_type: str
    personality_traits: Dict[str, float]
    communication_style: Dict[str, Any]
    behavior_patterns: Dict[str, Any]
    context_preferences: Dict[str, Any]
    adaptation_history: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

@dataclass
class AdaptationRule:
    """Adaptation rule"""
    id: str
    name: str
    trigger: AdaptationTrigger
    condition: Dict[str, Any]
    action: Dict[str, Any]
    priority: int
    enabled: bool = True
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

@dataclass
class AdaptationEvent:
    """Adaptation event"""
    id: str
    agent_id: str
    adaptation_type: AdaptationType
    trigger: AdaptationTrigger
    old_state: Dict[str, Any]
    new_state: Dict[str, Any]
    context: Dict[str, Any]
    timestamp: datetime
    success: bool
    confidence: float
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class AdaptationStats:
    """Adaptation statistics"""
    total_adaptations: int
    successful_adaptations: int
    failed_adaptations: int
    adaptation_types: Dict[str, int]
    triggers: Dict[str, int]
    average_confidence: float
    adaptation_frequency: float
    success_rate: float
    last_adaptation: datetime

class AdaptationFramework:
    """
    Comprehensive agent adaptation framework
    Built on existing communication framework with dynamic behavior modification
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.storage_path = Path(self.config.get("storage_path", "adaptation_data"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Threading and concurrency
        self.lock = threading.Lock()
        self.db_lock = threading.Lock()
        
        # Database setup
        self.db_path = self.storage_path / "adaptation.db"
        self._init_database()
        
        # Adaptation components
        self.profiles: Dict[str, AdaptationProfile] = {}
        self.rules: Dict[str, AdaptationRule] = {}
        self.events: Dict[str, AdaptationEvent] = {}
        self.adaptation_queue = deque()
        
        # Adaptation state
        self.adaptation_active = False
        self.current_adaptations: Dict[str, AdaptationType] = {}
        self.adaptation_threshold = 0.7
        
        # Load existing data
        self._load_profiles()
        self._load_rules()
        self._load_events()
        
        # Start adaptation processor
        self._start_adaptation_processor()
    
    def _init_database(self):
        """Initialize adaptation database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                # Create profiles table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS adaptation_profiles (
                        id TEXT PRIMARY KEY,
                        agent_id TEXT,
                        profile_type TEXT,
                        personality_traits TEXT,
                        communication_style TEXT,
                        behavior_patterns TEXT,
                        context_preferences TEXT,
                        adaptation_history TEXT,
                        created_at TEXT,
                        updated_at TEXT,
                        is_active BOOLEAN
                    )
                """)
                
                # Create rules table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS adaptation_rules (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        trigger TEXT,
                        condition TEXT,
                        action TEXT,
                        priority INTEGER,
                        enabled BOOLEAN,
                        created_at TEXT,
                        updated_at TEXT
                    )
                """)
                
                # Create events table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS adaptation_events (
                        id TEXT PRIMARY KEY,
                        agent_id TEXT,
                        adaptation_type TEXT,
                        trigger TEXT,
                        old_state TEXT,
                        new_state TEXT,
                        context TEXT,
                        timestamp TEXT,
                        success BOOLEAN,
                        confidence REAL
                    )
                """)
                
                conn.commit()
                conn.close()
                logger.info("Adaptation database initialized")
            except Exception as e:
                logger.error(f"Error initializing adaptation database: {e}")
    
    def _load_profiles(self):
        """Load adaptation profiles from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM adaptation_profiles")
                
                for row in cursor.fetchall():
                    profile = AdaptationProfile(
                        id=row[0],
                        agent_id=row[1],
                        profile_type=row[2],
                        personality_traits=json.loads(row[3]),
                        communication_style=json.loads(row[4]),
                        behavior_patterns=json.loads(row[5]),
                        context_preferences=json.loads(row[6]),
                        adaptation_history=json.loads(row[7]),
                        created_at=datetime.fromisoformat(row[8]),
                        updated_at=datetime.fromisoformat(row[9]),
                        is_active=bool(row[10])
                    )
                    self.profiles[profile.id] = profile
                
                conn.close()
                logger.info(f"Loaded {len(self.profiles)} adaptation profiles")
            except Exception as e:
                logger.error(f"Error loading profiles: {e}")
    
    def _load_rules(self):
        """Load adaptation rules from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM adaptation_rules")
                
                for row in cursor.fetchall():
                    rule = AdaptationRule(
                        id=row[0],
                        name=row[1],
                        trigger=AdaptationTrigger(row[2]),
                        condition=json.loads(row[3]),
                        action=json.loads(row[4]),
                        priority=row[5],
                        enabled=bool(row[6]),
                        created_at=datetime.fromisoformat(row[7]),
                        updated_at=datetime.fromisoformat(row[8])
                    )
                    self.rules[rule.id] = rule
                
                conn.close()
                logger.info(f"Loaded {len(self.rules)} adaptation rules")
            except Exception as e:
                logger.error(f"Error loading rules: {e}")
    
    def _load_events(self):
        """Load adaptation events from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM adaptation_events")
                
                for row in cursor.fetchall():
                    event = AdaptationEvent(
                        id=row[0],
                        agent_id=row[1],
                        adaptation_type=AdaptationType(row[2]),
                        trigger=AdaptationTrigger(row[3]),
                        old_state=json.loads(row[4]),
                        new_state=json.loads(row[5]),
                        context=json.loads(row[6]),
                        timestamp=datetime.fromisoformat(row[7]),
                        success=bool(row[8]),
                        confidence=row[9]
                    )
                    self.events[event.id] = event
                
                conn.close()
                logger.info(f"Loaded {len(self.events)} adaptation events")
            except Exception as e:
                logger.error(f"Error loading events: {e}")
    
    def _save_profile(self, profile: AdaptationProfile):
        """Save adaptation profile to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO adaptation_profiles 
                    (id, agent_id, profile_type, personality_traits, communication_style, 
                     behavior_patterns, context_preferences, adaptation_history, 
                     created_at, updated_at, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    profile.id,
                    profile.agent_id,
                    profile.profile_type,
                    json.dumps(profile.personality_traits),
                    json.dumps(profile.communication_style),
                    json.dumps(profile.behavior_patterns),
                    json.dumps(profile.context_preferences),
                    json.dumps(profile.adaptation_history),
                    profile.created_at.isoformat(),
                    profile.updated_at.isoformat(),
                    profile.is_active
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving profile {profile.id}: {e}")
    
    def _save_rule(self, rule: AdaptationRule):
        """Save adaptation rule to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO adaptation_rules 
                    (id, name, trigger, condition, action, priority, enabled, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    rule.id,
                    rule.name,
                    rule.trigger.value,
                    json.dumps(rule.condition),
                    json.dumps(rule.action),
                    rule.priority,
                    rule.enabled,
                    rule.created_at.isoformat(),
                    rule.updated_at.isoformat()
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving rule {rule.id}: {e}")
    
    def _save_event(self, event: AdaptationEvent):
        """Save adaptation event to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO adaptation_events 
                    (id, agent_id, adaptation_type, trigger, old_state, new_state, 
                     context, timestamp, success, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.id,
                    event.agent_id,
                    event.adaptation_type.value,
                    event.trigger.value,
                    json.dumps(event.old_state),
                    json.dumps(event.new_state),
                    json.dumps(event.context),
                    event.timestamp.isoformat(),
                    event.success,
                    event.confidence
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving event {event.id}: {e}")
    
    def _start_adaptation_processor(self):
        """Start background adaptation processor"""
        def process_adaptation():
            while True:
                try:
                    if self.adaptation_queue:
                        adaptation_task = self.adaptation_queue.popleft()
                        self._process_adaptation_task(adaptation_task)
                    else:
                        time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Error in adaptation processor: {e}")
                    time.sleep(1)
        
        thread = threading.Thread(target=process_adaptation, daemon=True)
        thread.start()
        logger.info("Adaptation processor started")
    
    def _process_adaptation_task(self, task: Dict[str, Any]):
        """Process an adaptation task"""
        try:
            task_type = task.get("type")
            
            if task_type == "behavioral_adaptation":
                self._process_behavioral_adaptation(task)
            elif task_type == "communication_adaptation":
                self._process_communication_adaptation(task)
            elif task_type == "personality_adaptation":
                self._process_personality_adaptation(task)
            elif task_type == "contextual_adaptation":
                self._process_contextual_adaptation(task)
            elif task_type == "environmental_adaptation":
                self._process_environmental_adaptation(task)
            else:
                logger.warning(f"Unknown adaptation task type: {task_type}")
                
        except Exception as e:
            logger.error(f"Error processing adaptation task: {e}")
    
    def create_adaptation_profile(self, 
                                agent_id: str,
                                profile_type: str = "default",
                                personality_traits: Optional[Dict[str, float]] = None,
                                communication_style: Optional[Dict[str, Any]] = None,
                                behavior_patterns: Optional[Dict[str, Any]] = None,
                                context_preferences: Optional[Dict[str, Any]] = None) -> str:
        """Create an adaptation profile for an agent"""
        profile_id = str(uuid.uuid4())
        
        # Default values
        if personality_traits is None:
            personality_traits = {
                "friendliness": 0.5,
                "formality": 0.5,
                "assertiveness": 0.5,
                "empathy": 0.5,
                "creativity": 0.5
            }
        
        if communication_style is None:
            communication_style = {
                "tone": "neutral",
                "verbosity": "medium",
                "technical_level": "medium",
                "formality": "medium"
            }
        
        if behavior_patterns is None:
            behavior_patterns = {
                "response_time": "normal",
                "proactivity": "medium",
                "collaboration": "medium",
                "independence": "medium"
            }
        
        if context_preferences is None:
            context_preferences = {
                "preferred_contexts": ["general"],
                "avoided_contexts": [],
                "adaptation_sensitivity": 0.5
            }
        
        profile = AdaptationProfile(
            id=profile_id,
            agent_id=agent_id,
            profile_type=profile_type,
            personality_traits=personality_traits,
            communication_style=communication_style,
            behavior_patterns=behavior_patterns,
            context_preferences=context_preferences,
            adaptation_history=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with self.lock:
            self.profiles[profile_id] = profile
            self._save_profile(profile)
        
        logger.info(f"Created adaptation profile {profile_id} for agent {agent_id}")
        return profile_id
    
    def add_adaptation_rule(self,
                          name: str,
                          trigger: AdaptationTrigger,
                          condition: Dict[str, Any],
                          action: Dict[str, Any],
                          priority: int = 1) -> str:
        """Add an adaptation rule"""
        rule_id = str(uuid.uuid4())
        
        rule = AdaptationRule(
            id=rule_id,
            name=name,
            trigger=trigger,
            condition=condition,
            action=action,
            priority=priority
        )
        
        with self.lock:
            self.rules[rule_id] = rule
            self._save_rule(rule)
        
        logger.info(f"Added adaptation rule {rule_id}: {name}")
        return rule_id
    
    def trigger_adaptation(self,
                         agent_id: str,
                         trigger: AdaptationTrigger,
                         context: Dict[str, Any],
                         adaptation_type: AdaptationType = AdaptationType.BEHAVIORAL) -> str:
        """Trigger adaptation for an agent"""
        adaptation_id = str(uuid.uuid4())
        
        # Find applicable rules
        applicable_rules = self._find_applicable_rules(trigger, context)
        
        if not applicable_rules:
            logger.info(f"No applicable rules found for trigger {trigger.value}")
            # Still record the event even if no rules apply
            event = AdaptationEvent(
                id=adaptation_id,
                agent_id=agent_id,
                adaptation_type=adaptation_type,
                trigger=trigger,
                old_state={},
                new_state={},
                context=context,
                timestamp=datetime.now(),
                success=False,
                confidence=0.0
            )
            with self.lock:
                self.events[adaptation_id] = event
                self._save_event(event)
            return adaptation_id
        
        # Get current profile
        current_profile = self._get_agent_profile(agent_id)
        if not current_profile:
            logger.warning(f"No profile found for agent {agent_id}")
            return adaptation_id
        
        # Store old state
        old_state = {
            "personality_traits": current_profile.personality_traits.copy(),
            "communication_style": current_profile.communication_style.copy(),
            "behavior_patterns": current_profile.behavior_patterns.copy(),
            "context_preferences": current_profile.context_preferences.copy()
        }
        
        # Apply adaptations
        new_state = old_state.copy()
        for rule in applicable_rules:
            new_state = self._apply_rule(rule, new_state, context)
        
        # Update profile
        self._update_profile_from_state(current_profile, new_state)
        
        # Record adaptation event
        event = AdaptationEvent(
            id=adaptation_id,
            agent_id=agent_id,
            adaptation_type=adaptation_type,
            trigger=trigger,
            old_state=old_state,
            new_state=new_state,
            context=context,
            timestamp=datetime.now(),
            success=True,
            confidence=self._calculate_adaptation_confidence(applicable_rules, context)
        )
        
        with self.lock:
            self.events[adaptation_id] = event
            self._save_event(event)
        
        # Add to adaptation history
        current_profile.adaptation_history.append({
            "event_id": adaptation_id,
            "timestamp": event.timestamp.isoformat(),
            "trigger": trigger.value,
            "type": adaptation_type.value,
            "success": True
        })
        current_profile.updated_at = datetime.now()
        self._save_profile(current_profile)
        
        logger.info(f"Triggered adaptation {adaptation_id} for agent {agent_id}")
        return adaptation_id
    
    def _find_applicable_rules(self, trigger: AdaptationTrigger, context: Dict[str, Any]) -> List[AdaptationRule]:
        """Find rules applicable to the trigger and context"""
        applicable_rules = []
        
        for rule in self.rules.values():
            if not rule.enabled:
                continue
            
            if rule.trigger != trigger:
                continue
            
            if self._evaluate_condition(rule.condition, context):
                applicable_rules.append(rule)
        
        # Sort by priority (higher priority first)
        applicable_rules.sort(key=lambda r: r.priority, reverse=True)
        
        return applicable_rules
    
    def _evaluate_condition(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate a condition against context"""
        try:
            condition_type = condition.get("type")
            
            if condition_type == "threshold":
                metric = condition.get("metric")
                threshold = condition.get("threshold")
                operator = condition.get("operator", ">=")
                
                value = context.get(metric, 0)
                
                if operator == ">=":
                    return value >= threshold
                elif operator == ">":
                    return value > threshold
                elif operator == "<=":
                    return value <= threshold
                elif operator == "<":
                    return value < threshold
                elif operator == "==":
                    return value == threshold
                elif operator == "!=":
                    return value != threshold
            
            elif condition_type == "contains":
                key = condition.get("key")
                values = condition.get("values", [])
                return context.get(key) in values
            
            elif condition_type == "time_based":
                time_condition = condition.get("time_condition")
                current_hour = datetime.now().hour
                
                if time_condition == "business_hours":
                    return 9 <= current_hour <= 17
                elif time_condition == "evening":
                    return 18 <= current_hour <= 22
                elif time_condition == "night":
                    return current_hour >= 23 or current_hour <= 6
            
            elif condition_type == "context_change":
                old_context = condition.get("old_context", {})
                new_context = condition.get("new_context", {})
                
                for key, old_value in old_context.items():
                    if context.get(key) != old_value:
                        return True
                
                return False
            
            return False
            
        except Exception as e:
            logger.error(f"Error evaluating condition: {e}")
            return False
    
    def _apply_rule(self, rule: AdaptationRule, state: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a rule to the current state"""
        try:
            action = rule.action
            action_type = action.get("type")
            
            if action_type == "adjust_personality":
                trait = action.get("trait")
                adjustment = action.get("adjustment", 0.1)
                direction = action.get("direction", "increase")
                
                if trait in state["personality_traits"]:
                    current_value = state["personality_traits"][trait]
                    if direction == "increase":
                        new_value = min(current_value + adjustment, 1.0)
                    else:
                        new_value = max(current_value - adjustment, 0.0)
                    state["personality_traits"][trait] = new_value
            
            elif action_type == "change_communication_style":
                style_key = action.get("style_key")
                new_value = action.get("new_value")
                state["communication_style"][style_key] = new_value
            
            elif action_type == "adjust_behavior":
                behavior = action.get("behavior")
                adjustment = action.get("adjustment", 0.1)
                direction = action.get("direction", "increase")
                
                if behavior in state["behavior_patterns"]:
                    current_value = state["behavior_patterns"][behavior]
                    if direction == "increase":
                        new_value = min(current_value + adjustment, 1.0)
                    else:
                        new_value = max(current_value - adjustment, 0.0)
                    state["behavior_patterns"][behavior] = new_value
            
            elif action_type == "update_context_preferences":
                preference_key = action.get("preference_key")
                new_value = action.get("new_value")
                state["context_preferences"][preference_key] = new_value
            
            return state
            
        except Exception as e:
            logger.error(f"Error applying rule {rule.id}: {e}")
            return state
    
    def _get_agent_profile(self, agent_id: str) -> Optional[AdaptationProfile]:
        """Get the active profile for an agent"""
        for profile in self.profiles.values():
            if profile.agent_id == agent_id and profile.is_active:
                return profile
        return None
    
    def _update_profile_from_state(self, profile: AdaptationProfile, state: Dict[str, Any]):
        """Update profile from new state"""
        profile.personality_traits = state["personality_traits"]
        profile.communication_style = state["communication_style"]
        profile.behavior_patterns = state["behavior_patterns"]
        profile.context_preferences = state["context_preferences"]
        profile.updated_at = datetime.now()
        self._save_profile(profile)
    
    def _calculate_adaptation_confidence(self, rules: List[AdaptationRule], context: Dict[str, Any]) -> float:
        """Calculate confidence in adaptation based on rules and context"""
        if not rules:
            return 0.0
        
        # Base confidence on number of applicable rules
        base_confidence = min(len(rules) * 0.3, 0.9)
        
        # Adjust based on rule priorities
        priority_bonus = sum(rule.priority for rule in rules) * 0.05
        priority_bonus = min(priority_bonus, 0.1)
        
        # Context relevance bonus
        context_bonus = 0.0
        for rule in rules:
            if self._evaluate_condition(rule.condition, context):
                context_bonus += 0.1
        
        context_bonus = min(context_bonus, 0.2)
        
        return min(base_confidence + priority_bonus + context_bonus, 1.0)
    
    def get_agent_adaptation_state(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get current adaptation state for an agent"""
        profile = self._get_agent_profile(agent_id)
        if not profile:
            return None
        
        return {
            "personality_traits": profile.personality_traits,
            "communication_style": profile.communication_style,
            "behavior_patterns": profile.behavior_patterns,
            "context_preferences": profile.context_preferences,
            "adaptation_count": len(profile.adaptation_history),
            "last_adaptation": profile.adaptation_history[-1]["timestamp"] if profile.adaptation_history else None
        }
    
    def get_adaptation_stats(self) -> AdaptationStats:
        """Get comprehensive adaptation statistics"""
        total_adaptations = len(self.events)
        successful_adaptations = sum(1 for event in self.events.values() if event.success)
        failed_adaptations = total_adaptations - successful_adaptations
        
        # Adaptation types distribution
        adaptation_types = defaultdict(int)
        for event in self.events.values():
            adaptation_types[event.adaptation_type.value] += 1
        
        # Triggers distribution
        triggers = defaultdict(int)
        for event in self.events.values():
            triggers[event.trigger.value] += 1
        
        # Average confidence
        confidences = [event.confidence for event in self.events.values()]
        average_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        # Adaptation frequency (adaptations per day)
        if self.events:
            time_span = (datetime.now() - min(event.timestamp for event in self.events.values())).total_seconds() / 86400
            adaptation_frequency = len(self.events) / max(time_span, 1)
        else:
            adaptation_frequency = 0.0
        
        # Success rate
        success_rate = successful_adaptations / max(total_adaptations, 1)
        
        # Last adaptation
        last_adaptation = max((event.timestamp for event in self.events.values()), default=datetime.now())
        
        return AdaptationStats(
            total_adaptations=total_adaptations,
            successful_adaptations=successful_adaptations,
            failed_adaptations=failed_adaptations,
            adaptation_types=dict(adaptation_types),
            triggers=dict(triggers),
            average_confidence=average_confidence,
            adaptation_frequency=adaptation_frequency,
            success_rate=success_rate,
            last_adaptation=last_adaptation
        )
    
    def export_adaptation_data(self, format: str = "json") -> Union[str, Dict[str, Any]]:
        """Export adaptation data"""
        data = {
            "profiles": [asdict(p) for p in self.profiles.values()],
            "rules": [asdict(r) for r in self.rules.values()],
            "events": [asdict(e) for e in self.events.values()],
            "stats": asdict(self.get_adaptation_stats())
        }
        
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        else:
            return data
    
    def start_adaptation(self):
        """Start adaptation process"""
        self.adaptation_active = True
        logger.info("Started adaptation process")
    
    def stop_adaptation(self):
        """Stop adaptation process"""
        self.adaptation_active = False
        logger.info("Stopped adaptation process")
    
    def clear_adaptation_data(self):
        """Clear all adaptation data"""
        with self.lock:
            self.profiles.clear()
            self.rules.clear()
            self.events.clear()
            
            # Clear database
            with self.db_lock:
                try:
                    conn = sqlite3.connect(self.db_path, timeout=10.0)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM adaptation_profiles")
                    cursor.execute("DELETE FROM adaptation_rules")
                    cursor.execute("DELETE FROM adaptation_events")
                    conn.commit()
                    conn.close()
                    logger.info("Cleared all adaptation data")
                except Exception as e:
                    logger.error(f"Error clearing adaptation data: {e}")
