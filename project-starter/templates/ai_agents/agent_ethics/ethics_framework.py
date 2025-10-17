"""
Pattern 16: Agent Ethics - Ethical Decision Making and Moral Reasoning

This framework provides ethical decision-making capabilities for AI agents,
including ethical principles, moral reasoning, ethical dilemmas, and
ethical monitoring and compliance.
"""

import asyncio
import json
import logging
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


class EthicalPrinciple(str, Enum):
    """Core ethical principles for AI agents"""
    AUTONOMY = "autonomy"  # Respect for human autonomy
    BENEFICENCE = "beneficence"  # Do good and prevent harm
    NON_MALEFICENCE = "non_maleficence"  # Do no harm
    JUSTICE = "justice"  # Fairness and equality
    TRANSPARENCY = "transparency"  # Openness and explainability
    ACCOUNTABILITY = "accountability"  # Responsibility for actions
    PRIVACY = "privacy"  # Protection of personal information
    FAIRNESS = "fairness"  # Unbiased treatment
    HUMAN_DIGNITY = "human_dignity"  # Respect for human worth
    SUSTAINABILITY = "sustainability"  # Long-term environmental and social impact


class EthicalDilemmaType(str, Enum):
    """Types of ethical dilemmas"""
    PRIVACY_VS_SAFETY = "privacy_vs_safety"
    AUTONOMY_VS_PROTECTION = "autonomy_vs_protection"
    EFFICIENCY_VS_FAIRNESS = "efficiency_vs_fairness"
    TRANSPARENCY_VS_SECURITY = "transparency_vs_security"
    INDIVIDUAL_VS_COLLECTIVE = "individual_vs_collective"
    SHORT_TERM_VS_LONG_TERM = "short_term_vs_long_term"
    CUSTOM = "custom"


class EthicalDecisionType(str, Enum):
    """Types of ethical decisions"""
    AUTOMATED = "automated"  # System can decide automatically
    HUMAN_REVIEW = "human_review"  # Requires human oversight
    ESCALATION = "escalation"  # Must be escalated to ethics committee
    BLOCKED = "blocked"  # Action should be blocked


class EthicalViolationType(str, Enum):
    """Types of ethical violations"""
    BIAS = "bias"  # Discriminatory behavior
    PRIVACY_BREACH = "privacy_breach"  # Unauthorized data access
    MANIPULATION = "manipulation"  # Deceptive practices
    HARM = "harm"  # Physical or psychological harm
    DISCRIMINATION = "discrimination"  # Unfair treatment
    TRANSPARENCY_VIOLATION = "transparency_violation"  # Lack of explainability
    ACCOUNTABILITY_VIOLATION = "accountability_violation"  # Lack of responsibility
    CUSTOM = "custom"


class EthicalContext(BaseModel):
    """Context for ethical decision making"""
    domain: str  # e.g., healthcare, finance, education
    stakeholders: List[str]  # Affected parties
    risk_level: str  # low, medium, high, critical
    legal_requirements: List[str]  # Applicable laws/regulations
    cultural_context: Dict[str, Any]  # Cultural considerations
    temporal_context: str  # Immediate, short-term, long-term
    scope: str  # Individual, group, society


class EthicalRule(BaseModel):
    """Ethical rule for decision making"""
    id: str
    principle: EthicalPrinciple
    condition: str  # When this rule applies
    action: str  # What to do when condition is met
    priority: int  # Higher number = higher priority
    weight: float  # Importance weight (0.0 to 1.0)
    exceptions: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class EthicalDilemma(BaseModel):
    """Ethical dilemma scenario"""
    id: str
    dilemma_type: EthicalDilemmaType
    title: str
    description: str
    context: EthicalContext
    conflicting_principles: List[EthicalPrinciple]
    stakeholders: List[str]
    potential_outcomes: List[Dict[str, Any]]
    recommended_approach: str
    created_at: datetime
    updated_at: datetime


class EthicalDecision(BaseModel):
    """Ethical decision made by the system"""
    id: str
    dilemma_id: Optional[str]
    decision_type: EthicalDecisionType
    reasoning: str
    principles_applied: List[EthicalPrinciple]
    confidence_score: float
    risk_assessment: Dict[str, Any]
    mitigation_strategies: List[str]
    stakeholders_notified: List[str]
    created_at: datetime
    updated_at: datetime


class EthicalViolation(BaseModel):
    """Ethical violation detected"""
    id: str
    violation_type: EthicalViolationType
    description: str
    severity: str  # low, medium, high, critical
    agent_id: str
    context: Dict[str, Any]
    evidence: List[str]
    remediation_actions: List[str]
    status: str  # detected, investigating, resolved, dismissed
    created_at: datetime
    updated_at: datetime


class EthicalMetrics(BaseModel):
    """Ethical performance metrics"""
    total_decisions: int
    automated_decisions: int
    human_review_decisions: int
    escalated_decisions: int
    blocked_actions: int
    violations_detected: int
    violations_resolved: int
    average_confidence: float
    principle_usage: Dict[str, int]
    violation_types: Dict[str, int]
    decision_accuracy: float
    compliance_score: float
    last_decision: Optional[datetime]


class EthicsFramework:
    """Framework for ethical decision making and moral reasoning"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the ethics framework"""
        self.config = config or {}
        self.storage_path = Path(self.config.get("storage_path", "ethics_data"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Threading and concurrency
        self.lock = threading.Lock()
        self.db_lock = threading.Lock()
        
        # Database setup
        self.db_path = self.storage_path / "ethics.db"
        self._init_database()
        
        # Core data structures
        self.rules: Dict[str, EthicalRule] = {}
        self.dilemmas: Dict[str, EthicalDilemma] = {}
        self.decisions: Dict[str, EthicalDecision] = {}
        self.violations: Dict[str, EthicalViolation] = {}
        
        # Load existing data
        self._load_rules()
        self._load_dilemmas()
        self._load_decisions()
        self._load_violations()
        
        # Initialize default rules
        self._initialize_default_rules()
        
        # Background processing
        self.ethics_processor_running = False
        self.ethics_queue = []
        
        logger.info("Ethics framework initialized")
    
    def _init_database(self):
        """Initialize the ethics database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                # Create tables
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ethical_rules (
                        id TEXT PRIMARY KEY,
                        principle TEXT NOT NULL,
                        condition TEXT NOT NULL,
                        action TEXT NOT NULL,
                        priority INTEGER NOT NULL,
                        weight REAL NOT NULL,
                        exceptions TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ethical_dilemmas (
                        id TEXT PRIMARY KEY,
                        dilemma_type TEXT NOT NULL,
                        title TEXT NOT NULL,
                        description TEXT NOT NULL,
                        context TEXT NOT NULL,
                        conflicting_principles TEXT NOT NULL,
                        stakeholders TEXT NOT NULL,
                        potential_outcomes TEXT NOT NULL,
                        recommended_approach TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ethical_decisions (
                        id TEXT PRIMARY KEY,
                        dilemma_id TEXT,
                        decision_type TEXT NOT NULL,
                        reasoning TEXT NOT NULL,
                        principles_applied TEXT NOT NULL,
                        confidence_score REAL NOT NULL,
                        risk_assessment TEXT NOT NULL,
                        mitigation_strategies TEXT NOT NULL,
                        stakeholders_notified TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ethical_violations (
                        id TEXT PRIMARY KEY,
                        violation_type TEXT NOT NULL,
                        description TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        agent_id TEXT NOT NULL,
                        context TEXT NOT NULL,
                        evidence TEXT NOT NULL,
                        remediation_actions TEXT NOT NULL,
                        status TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                conn.commit()
                conn.close()
                logger.info("Ethics database initialized")
            except Exception as e:
                logger.error(f"Error initializing ethics database: {e}")
    
    def _load_rules(self):
        """Load ethical rules from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ethical_rules")
                rows = cursor.fetchall()
                
                for row in rows:
                    rule = EthicalRule(
                        id=row[0],
                        principle=EthicalPrinciple(row[1]),
                        condition=row[2],
                        action=row[3],
                        priority=row[4],
                        weight=row[5],
                        exceptions=json.loads(row[6]) if row[6] else [],
                        created_at=datetime.fromisoformat(row[7]),
                        updated_at=datetime.fromisoformat(row[8])
                    )
                    self.rules[rule.id] = rule
                
                conn.close()
                logger.info(f"Loaded {len(self.rules)} ethical rules")
            except Exception as e:
                logger.error(f"Error loading ethical rules: {e}")
    
    def _load_dilemmas(self):
        """Load ethical dilemmas from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ethical_dilemmas")
                rows = cursor.fetchall()
                
                for row in rows:
                    dilemma = EthicalDilemma(
                        id=row[0],
                        dilemma_type=EthicalDilemmaType(row[1]),
                        title=row[2],
                        description=row[3],
                        context=EthicalContext(**json.loads(row[4])),
                        conflicting_principles=[EthicalPrinciple(p) for p in json.loads(row[5])],
                        stakeholders=json.loads(row[6]),
                        potential_outcomes=json.loads(row[7]),
                        recommended_approach=row[8],
                        created_at=datetime.fromisoformat(row[9]),
                        updated_at=datetime.fromisoformat(row[10])
                    )
                    self.dilemmas[dilemma.id] = dilemma
                
                conn.close()
                logger.info(f"Loaded {len(self.dilemmas)} ethical dilemmas")
            except Exception as e:
                logger.error(f"Error loading ethical dilemmas: {e}")
    
    def _load_decisions(self):
        """Load ethical decisions from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ethical_decisions")
                rows = cursor.fetchall()
                
                for row in rows:
                    decision = EthicalDecision(
                        id=row[0],
                        dilemma_id=row[1],
                        decision_type=EthicalDecisionType(row[2]),
                        reasoning=row[3],
                        principles_applied=[EthicalPrinciple(p) for p in json.loads(row[4])],
                        confidence_score=row[5],
                        risk_assessment=json.loads(row[6]),
                        mitigation_strategies=json.loads(row[7]),
                        stakeholders_notified=json.loads(row[8]),
                        created_at=datetime.fromisoformat(row[9]),
                        updated_at=datetime.fromisoformat(row[10])
                    )
                    self.decisions[decision.id] = decision
                
                conn.close()
                logger.info(f"Loaded {len(self.decisions)} ethical decisions")
            except Exception as e:
                logger.error(f"Error loading ethical decisions: {e}")
    
    def _load_violations(self):
        """Load ethical violations from database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ethical_violations")
                rows = cursor.fetchall()
                
                for row in rows:
                    violation = EthicalViolation(
                        id=row[0],
                        violation_type=EthicalViolationType(row[1]),
                        description=row[2],
                        severity=row[3],
                        agent_id=row[4],
                        context=json.loads(row[5]),
                        evidence=json.loads(row[6]),
                        remediation_actions=json.loads(row[7]),
                        status=row[8],
                        created_at=datetime.fromisoformat(row[9]),
                        updated_at=datetime.fromisoformat(row[10])
                    )
                    self.violations[violation.id] = violation
                
                conn.close()
                logger.info(f"Loaded {len(self.violations)} ethical violations")
            except Exception as e:
                logger.error(f"Error loading ethical violations: {e}")
    
    def _initialize_default_rules(self):
        """Initialize default ethical rules"""
        default_rules = [
            {
                "principle": EthicalPrinciple.NON_MALEFICENCE,
                "condition": "action_could_cause_harm",
                "action": "block_action",
                "priority": 100,
                "weight": 1.0,
                "exceptions": ["emergency_situation", "informed_consent"]
            },
            {
                "principle": EthicalPrinciple.PRIVACY,
                "condition": "accessing_personal_data",
                "action": "require_consent",
                "priority": 90,
                "weight": 0.9,
                "exceptions": ["public_data", "legal_requirement"]
            },
            {
                "principle": EthicalPrinciple.TRANSPARENCY,
                "condition": "making_decision",
                "action": "provide_explanation",
                "priority": 80,
                "weight": 0.8,
                "exceptions": ["security_critical"]
            },
            {
                "principle": EthicalPrinciple.FAIRNESS,
                "condition": "treating_users",
                "action": "ensure_unbiased_treatment",
                "priority": 85,
                "weight": 0.85,
                "exceptions": []
            },
            {
                "principle": EthicalPrinciple.ACCOUNTABILITY,
                "condition": "system_error",
                "action": "log_and_notify",
                "priority": 95,
                "weight": 0.95,
                "exceptions": []
            }
        ]
        
        for rule_data in default_rules:
            rule_id = str(uuid.uuid4())
            rule = EthicalRule(
                id=rule_id,
                principle=rule_data["principle"],
                condition=rule_data["condition"],
                action=rule_data["action"],
                priority=rule_data["priority"],
                weight=rule_data["weight"],
                exceptions=rule_data["exceptions"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.rules[rule_id] = rule
            self._save_rule(rule)
    
    def _save_rule(self, rule: EthicalRule):
        """Save ethical rule to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO ethical_rules 
                    (id, principle, condition, action, priority, weight, exceptions, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    rule.id, rule.principle.value, rule.condition, rule.action,
                    rule.priority, rule.weight, json.dumps(rule.exceptions),
                    rule.created_at.isoformat(), rule.updated_at.isoformat()
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving rule {rule.id}: {e}")
    
    def _save_dilemma(self, dilemma: EthicalDilemma):
        """Save ethical dilemma to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO ethical_dilemmas 
                    (id, dilemma_type, title, description, context, conflicting_principles, 
                     stakeholders, potential_outcomes, recommended_approach, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    dilemma.id, dilemma.dilemma_type.value, dilemma.title, dilemma.description,
                    json.dumps(dilemma.context.dict()), json.dumps([p.value for p in dilemma.conflicting_principles]),
                    json.dumps(dilemma.stakeholders), json.dumps(dilemma.potential_outcomes),
                    dilemma.recommended_approach, dilemma.created_at.isoformat(), dilemma.updated_at.isoformat()
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving dilemma {dilemma.id}: {e}")
    
    def _save_decision(self, decision: EthicalDecision):
        """Save ethical decision to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO ethical_decisions 
                    (id, dilemma_id, decision_type, reasoning, principles_applied, confidence_score,
                     risk_assessment, mitigation_strategies, stakeholders_notified, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    decision.id, decision.dilemma_id, decision.decision_type.value, decision.reasoning,
                    json.dumps([p.value for p in decision.principles_applied]), decision.confidence_score,
                    json.dumps(decision.risk_assessment), json.dumps(decision.mitigation_strategies),
                    json.dumps(decision.stakeholders_notified), decision.created_at.isoformat(), decision.updated_at.isoformat()
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving decision {decision.id}: {e}")
    
    def _save_violation(self, violation: EthicalViolation):
        """Save ethical violation to database"""
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO ethical_violations 
                    (id, violation_type, description, severity, agent_id, context, evidence,
                     remediation_actions, status, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    violation.id, violation.violation_type.value, violation.description, violation.severity,
                    violation.agent_id, json.dumps(violation.context), json.dumps(violation.evidence),
                    json.dumps(violation.remediation_actions), violation.status,
                    violation.created_at.isoformat(), violation.updated_at.isoformat()
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving violation {violation.id}: {e}")
    
    def create_ethical_rule(self, principle: EthicalPrinciple, condition: str, action: str,
                          priority: int = 50, weight: float = 0.5,
                          exceptions: Optional[List[str]] = None) -> str:
        """Create a new ethical rule"""
        rule_id = str(uuid.uuid4())
        rule = EthicalRule(
            id=rule_id,
            principle=principle,
            condition=condition,
            action=action,
            priority=priority,
            weight=weight,
            exceptions=exceptions or [],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with self.lock:
            self.rules[rule_id] = rule
            self._save_rule(rule)
        
        logger.info(f"Created ethical rule {rule_id} for principle {principle.value}")
        return rule_id
    
    def create_ethical_dilemma(self, dilemma_type: EthicalDilemmaType, title: str, description: str,
                             context: EthicalContext, conflicting_principles: List[EthicalPrinciple],
                             stakeholders: List[str], potential_outcomes: List[Dict[str, Any]],
                             recommended_approach: str) -> str:
        """Create a new ethical dilemma"""
        dilemma_id = str(uuid.uuid4())
        dilemma = EthicalDilemma(
            id=dilemma_id,
            dilemma_type=dilemma_type,
            title=title,
            description=description,
            context=context,
            conflicting_principles=conflicting_principles,
            stakeholders=stakeholders,
            potential_outcomes=potential_outcomes,
            recommended_approach=recommended_approach,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with self.lock:
            self.dilemmas[dilemma_id] = dilemma
            self._save_dilemma(dilemma)
        
        logger.info(f"Created ethical dilemma {dilemma_id}: {title}")
        return dilemma_id
    
    def make_ethical_decision(self, context: Dict[str, Any], agent_id: str,
                            dilemma_id: Optional[str] = None) -> str:
        """Make an ethical decision based on context and rules"""
        decision_id = str(uuid.uuid4())
        
        # Analyze context against rules
        applicable_rules = self._find_applicable_rules(context)
        decision_type = self._determine_decision_type(applicable_rules, context)
        reasoning = self._generate_reasoning(applicable_rules, context)
        principles_applied = [rule.principle for rule in applicable_rules]
        confidence_score = self._calculate_confidence(applicable_rules, context)
        risk_assessment = self._assess_risks(context, principles_applied)
        mitigation_strategies = self._generate_mitigation_strategies(risk_assessment)
        stakeholders_notified = self._identify_stakeholders(context)
        
        decision = EthicalDecision(
            id=decision_id,
            dilemma_id=dilemma_id,
            decision_type=decision_type,
            reasoning=reasoning,
            principles_applied=principles_applied,
            confidence_score=confidence_score,
            risk_assessment=risk_assessment,
            mitigation_strategies=mitigation_strategies,
            stakeholders_notified=stakeholders_notified,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with self.lock:
            self.decisions[decision_id] = decision
            self._save_decision(decision)
        
        logger.info(f"Made ethical decision {decision_id}: {decision_type.value}")
        return decision_id
    
    def detect_ethical_violation(self, agent_id: str, violation_type: EthicalViolationType,
                               description: str, context: Dict[str, Any],
                               evidence: List[str], severity: str = "medium") -> str:
        """Detect and record an ethical violation"""
        violation_id = str(uuid.uuid4())
        
        remediation_actions = self._generate_remediation_actions(violation_type, severity)
        
        violation = EthicalViolation(
            id=violation_id,
            violation_type=violation_type,
            description=description,
            severity=severity,
            agent_id=agent_id,
            context=context,
            evidence=evidence,
            remediation_actions=remediation_actions,
            status="detected",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        with self.lock:
            self.violations[violation_id] = violation
            self._save_violation(violation)
        
        logger.warning(f"Detected ethical violation {violation_id}: {violation_type.value if hasattr(violation_type, 'value') else violation_type}")
        return violation_id
    
    def _find_applicable_rules(self, context: Dict[str, Any]) -> List[EthicalRule]:
        """Find rules applicable to the given context"""
        applicable_rules = []
        
        for rule in self.rules.values():
            if self._evaluate_condition(rule.condition, context):
                # Check if any exceptions apply
                if not self._check_exceptions(rule.exceptions, context):
                    applicable_rules.append(rule)
        
        # Sort by priority (higher first)
        applicable_rules.sort(key=lambda r: r.priority, reverse=True)
        return applicable_rules
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate if a condition is met in the given context"""
        # Simple condition evaluation - in practice, this would be more sophisticated
        condition_lower = condition.lower()
        
        if "harm" in condition_lower and context.get("risk_level") in ["high", "critical"]:
            return True
        elif "personal_data" in condition_lower and context.get("data_type") == "personal":
            return True
        elif "decision" in condition_lower and context.get("action_type") == "decision":
            return True
        elif "users" in condition_lower and context.get("stakeholders"):
            return True
        elif "error" in condition_lower and context.get("error_occurred", False):
            return True
        
        return False
    
    def _check_exceptions(self, exceptions: List[str], context: Dict[str, Any]) -> bool:
        """Check if any exceptions apply to the context"""
        for exception in exceptions:
            if exception in context.get("exceptions", []):
                return True
        return False
    
    def _determine_decision_type(self, rules: List[EthicalRule], context: Dict[str, Any]) -> EthicalDecisionType:
        """Determine the type of decision based on rules and context"""
        if not rules:
            return EthicalDecisionType.ESCALATION
        
        # Check for blocking conditions
        for rule in rules:
            if rule.action == "block_action":
                return EthicalDecisionType.BLOCKED
        
        # Check risk level
        risk_level = context.get("risk_level", "low")
        if risk_level in ["high", "critical"]:
            return EthicalDecisionType.HUMAN_REVIEW
        
        # Check confidence in rules
        total_weight = sum(rule.weight for rule in rules)
        if total_weight >= 0.8:
            return EthicalDecisionType.AUTOMATED
        else:
            return EthicalDecisionType.HUMAN_REVIEW
    
    def _generate_reasoning(self, rules: List[EthicalRule], context: Dict[str, Any]) -> str:
        """Generate reasoning for the ethical decision"""
        if not rules:
            return "No applicable ethical rules found. Escalation required."
        
        reasoning_parts = []
        for rule in rules:
            reasoning_parts.append(f"Applied {rule.principle.value}: {rule.action}")
        
        return "; ".join(reasoning_parts)
    
    def _calculate_confidence(self, rules: List[EthicalRule], context: Dict[str, Any]) -> float:
        """Calculate confidence score for the decision"""
        if not rules:
            return 0.0
        
        # Weighted average of rule weights
        total_weight = sum(rule.weight for rule in rules)
        return min(total_weight / len(rules), 1.0)
    
    def _assess_risks(self, context: Dict[str, Any], principles: List[EthicalPrinciple]) -> Dict[str, Any]:
        """Assess risks associated with the decision"""
        risks = {
            "privacy_risk": 0.0,
            "safety_risk": 0.0,
            "fairness_risk": 0.0,
            "transparency_risk": 0.0,
            "overall_risk": "low"
        }
        
        # Assess based on principles applied
        if EthicalPrinciple.PRIVACY in principles:
            risks["privacy_risk"] = 0.3
        if EthicalPrinciple.NON_MALEFICENCE in principles:
            risks["safety_risk"] = 0.2
        if EthicalPrinciple.FAIRNESS in principles:
            risks["fairness_risk"] = 0.1
        if EthicalPrinciple.TRANSPARENCY in principles:
            risks["transparency_risk"] = 0.1
        
        # Calculate overall risk (only from numeric values)
        numeric_risks = [v for k, v in risks.items() if k != "overall_risk" and isinstance(v, (int, float))]
        if numeric_risks:
            max_risk = max(numeric_risks)
            if max_risk >= 0.7:
                risks["overall_risk"] = "high"
            elif max_risk >= 0.4:
                risks["overall_risk"] = "medium"
        
        return risks
    
    def _generate_mitigation_strategies(self, risk_assessment: Dict[str, Any]) -> List[str]:
        """Generate mitigation strategies based on risk assessment"""
        strategies = []
        
        if risk_assessment.get("privacy_risk", 0) > 0.2:
            strategies.append("Implement data anonymization")
            strategies.append("Obtain explicit consent")
        
        if risk_assessment.get("safety_risk", 0) > 0.2:
            strategies.append("Add safety checks")
            strategies.append("Implement human oversight")
        
        if risk_assessment.get("fairness_risk", 0) > 0.2:
            strategies.append("Bias testing")
            strategies.append("Diverse training data")
        
        if risk_assessment.get("transparency_risk", 0) > 0.2:
            strategies.append("Provide explanations")
            strategies.append("Document decision process")
        
        return strategies
    
    def _identify_stakeholders(self, context: Dict[str, Any]) -> List[str]:
        """Identify stakeholders who should be notified"""
        stakeholders = context.get("stakeholders", [])
        if not stakeholders:
            stakeholders = ["system_administrator"]
        return stakeholders
    
    def _generate_remediation_actions(self, violation_type: EthicalViolationType, severity: str) -> List[str]:
        """Generate remediation actions for a violation"""
        actions = []
        
        if violation_type == EthicalViolationType.BIAS:
            actions.extend(["Retrain model", "Audit training data", "Implement bias testing"])
        elif violation_type == EthicalViolationType.PRIVACY_BREACH:
            actions.extend(["Notify affected users", "Audit access logs", "Strengthen security"])
        elif violation_type == EthicalViolationType.MANIPULATION:
            actions.extend(["Review decision logic", "Add transparency measures", "Human oversight"])
        elif violation_type == EthicalViolationType.HARM:
            actions.extend(["Immediate system shutdown", "Emergency response", "Root cause analysis"])
        
        if severity == "critical":
            actions.insert(0, "Immediate escalation")
        elif severity == "high":
            actions.insert(0, "Priority investigation")
        
        return actions
    
    def get_ethical_metrics(self) -> EthicalMetrics:
        """Get ethical performance metrics"""
        with self.lock:
            total_decisions = len(self.decisions)
            automated_decisions = len([d for d in self.decisions.values() if d.decision_type == EthicalDecisionType.AUTOMATED])
            human_review_decisions = len([d for d in self.decisions.values() if d.decision_type == EthicalDecisionType.HUMAN_REVIEW])
            escalated_decisions = len([d for d in self.decisions.values() if d.decision_type == EthicalDecisionType.ESCALATION])
            blocked_actions = len([d for d in self.decisions.values() if d.decision_type == EthicalDecisionType.BLOCKED])
            
            violations_detected = len(self.violations)
            violations_resolved = len([v for v in self.violations.values() if v.status == "resolved"])
            
            if total_decisions > 0:
                average_confidence = sum(d.confidence_score for d in self.decisions.values()) / total_decisions
            else:
                average_confidence = 0.0
            
            # Principle usage
            principle_usage = {}
            for decision in self.decisions.values():
                for principle in decision.principles_applied:
                    principle_usage[principle.value] = principle_usage.get(principle.value, 0) + 1
            
            # Violation types
            violation_types = {}
            for violation in self.violations.values():
                violation_types[violation.violation_type.value] = violation_types.get(violation.violation_type.value, 0) + 1
            
            # Decision accuracy (simplified)
            decision_accuracy = 1.0 - (violations_detected / max(total_decisions, 1))
            
            # Compliance score
            compliance_score = 1.0 - (violations_detected / max(total_decisions, 1))
            
            last_decision = max([d.created_at for d in self.decisions.values()], default=None)
            
            return EthicalMetrics(
                total_decisions=total_decisions,
                automated_decisions=automated_decisions,
                human_review_decisions=human_review_decisions,
                escalated_decisions=escalated_decisions,
                blocked_actions=blocked_actions,
                violations_detected=violations_detected,
                violations_resolved=violations_resolved,
                average_confidence=average_confidence,
                principle_usage=principle_usage,
                violation_types=violation_types,
                decision_accuracy=decision_accuracy,
                compliance_score=compliance_score,
                last_decision=last_decision
            )
    
    def start_ethics_processing(self):
        """Start the ethics processing background thread"""
        if not self.ethics_processor_running:
            self.ethics_processor_running = True
            self.ethics_thread = threading.Thread(target=self._process_ethics_queue, daemon=True)
            self.ethics_thread.start()
            logger.info("Ethics processor started")
    
    def stop_ethics_processing(self):
        """Stop the ethics processing background thread"""
        self.ethics_processor_running = False
        if hasattr(self, 'ethics_thread'):
            self.ethics_thread.join(timeout=1.0)
        logger.info("Ethics processor stopped")
    
    def _process_ethics_queue(self):
        """Process the ethics queue in background"""
        while self.ethics_processor_running:
            try:
                if self.ethics_queue:
                    task = self.ethics_queue.pop(0)
                    self._process_ethics_task(task)
                else:
                    time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error processing ethics task: {e}")
                time.sleep(1.0)
    
    def _process_ethics_task(self, task: Dict[str, Any]):
        """Process a single ethics task"""
        task_type = task.get("type")
        
        if task_type == "decision_review":
            # Review past decisions for ethical issues
            self._review_decisions()
        elif task_type == "violation_analysis":
            # Analyze patterns in violations
            self._analyze_violation_patterns()
        elif task_type == "rule_optimization":
            # Optimize rules based on outcomes
            self._optimize_rules()
    
    def _review_decisions(self):
        """Review past decisions for ethical issues"""
        # Implementation would analyze decision outcomes
        pass
    
    def _analyze_violation_patterns(self):
        """Analyze patterns in ethical violations"""
        # Implementation would identify common violation patterns
        pass
    
    def _optimize_rules(self):
        """Optimize ethical rules based on outcomes"""
        # Implementation would adjust rule weights and priorities
        pass
    
    def export_ethics_data(self, format: str = "json") -> Union[str, Dict[str, Any]]:
        """Export ethics data in specified format"""
        with self.lock:
            data = {
                "rules": [rule.dict() for rule in self.rules.values()],
                "dilemmas": [dilemma.dict() for dilemma in self.dilemmas.values()],
                "decisions": [decision.dict() for decision in self.decisions.values()],
                "violations": [violation.dict() for violation in self.violations.values()],
                "metrics": self.get_ethical_metrics().dict()
            }
            
            if format == "json":
                return json.dumps(data, indent=2, default=str)
            else:
                return data
    
    def clear_ethics_data(self):
        """Clear all ethics data"""
        with self.lock:
            self.rules.clear()
            self.dilemmas.clear()
            self.decisions.clear()
            self.violations.clear()
            
            # Clear database
            with self.db_lock:
                try:
                    conn = sqlite3.connect(self.db_path, timeout=10.0)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM ethical_rules")
                    cursor.execute("DELETE FROM ethical_dilemmas")
                    cursor.execute("DELETE FROM ethical_decisions")
                    cursor.execute("DELETE FROM ethical_violations")
                    conn.commit()
                    conn.close()
                except Exception as e:
                    logger.error(f"Error clearing ethics data: {e}")
            
            # Reinitialize default rules
            self._initialize_default_rules()
            
        logger.info("Cleared all ethics data")


# Example usage and testing
if __name__ == "__main__":
    # Create ethics framework
    framework = EthicsFramework()
    
    # Test basic functionality
    print("🧪 Testing Pattern 16: Agent Ethics")
    print("=" * 50)
    
    # Create a test context
    context = {
        "action_type": "decision",
        "data_type": "personal",
        "risk_level": "medium",
        "stakeholders": ["user_001", "admin_001"]
    }
    
    # Make an ethical decision
    decision_id = framework.make_ethical_decision(context, "agent_001")
    print(f"✅ Made ethical decision: {decision_id}")
    
    # Detect a violation
    violation_id = framework.detect_ethical_violation(
        "agent_001", 
        EthicalViolationType.BIAS,
        "Model shows gender bias in hiring recommendations",
        {"domain": "hr", "impact": "high"},
        ["bias_analysis_report.pdf"],
        "high"
    )
    print(f"✅ Detected ethical violation: {violation_id}")
    
    # Get metrics
    metrics = framework.get_ethical_metrics()
    print(f"✅ Ethics metrics: {metrics.total_decisions} decisions, {metrics.violations_detected} violations")
    
    print("🎯 Pattern 16: Agent Ethics basic test completed!")
