"""
Pattern 18: Guardrails & Safety
Comprehensive guardrails and safety system for AI agents
"""

import logging
import re
import asyncio
from typing import Dict, List, Optional, Any, Callable, Union
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SafetyLevel(Enum):
    """Safety levels for different operations"""
    LOW = "low"           # Basic safety checks
    MEDIUM = "medium"     # Standard safety checks
    HIGH = "high"         # Enhanced safety checks
    CRITICAL = "critical" # Maximum safety checks

class ViolationType(Enum):
    """Types of safety violations"""
    CONTENT_SAFETY = "content_safety"     # Harmful content
    DATA_PRIVACY = "data_privacy"         # Privacy violations
    SECURITY = "security"                 # Security threats
    COMPLIANCE = "compliance"             # Regulatory compliance
    ETHICAL = "ethical"                   # Ethical violations
    OPERATIONAL = "operational"           # Operational safety

class ActionType(Enum):
    """Actions to take when violations are detected"""
    ALLOW = "allow"                       # Allow the action
    BLOCK = "block"                       # Block the action
    MODIFY = "modify"                     # Modify the content
    ESCALATE = "escalate"                 # Escalate to human
    LOG = "log"                          # Log for review

@dataclass
class SafetyViolation:
    """Represents a safety violation"""
    violation_type: ViolationType
    severity: str  # "low", "medium", "high", "critical"
    description: str
    detected_content: str
    agent_id: str
    operation: str
    timestamp: datetime
    confidence: float  # 0.0 to 1.0
    metadata: Dict[str, Any] = None

@dataclass
class SafetyRule:
    """A safety rule definition"""
    rule_id: str
    name: str
    description: str
    violation_type: ViolationType
    pattern: str  # Regex pattern or keyword list
    action: ActionType
    safety_level: SafetyLevel
    enabled: bool = True
    metadata: Dict[str, Any] = None

@dataclass
class SafetyResult:
    """Result of safety evaluation"""
    safe: bool
    violations: List[SafetyViolation]
    action_taken: ActionType
    modified_content: Optional[str] = None
    escalation_required: bool = False
    confidence: float = 1.0

class GuardrailsFramework:
    """
    Comprehensive guardrails and safety framework for AI agents
    Implements Pattern 18 with multi-layered safety checks
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.safety_rules: List[SafetyRule] = []
        self.violation_history: List[SafetyViolation] = []
        self.alert_callbacks: List[Callable] = []
        self.content_modifiers: Dict[str, Callable] = {}
        
        # Safety statistics
        self.safety_stats = {
            "total_checks": 0,
            "violations_detected": 0,
            "content_blocked": 0,
            "content_modified": 0,
            "escalations": 0
        }
        
        # Initialize default safety rules
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """Initialize default safety rules"""
        
        # Content safety rules
        self.add_safety_rule(SafetyRule(
            rule_id="harmful_content",
            name="Harmful Content Detection",
            description="Detect and block harmful or inappropriate content",
            violation_type=ViolationType.CONTENT_SAFETY,
            pattern=r"(?i)(violence|hate|harm|discrimination|harassment|threat)",
            action=ActionType.BLOCK,
            safety_level=SafetyLevel.HIGH
        ))
        
        # Data privacy rules
        self.add_safety_rule(SafetyRule(
            rule_id="pii_detection",
            name="PII Detection",
            description="Detect personally identifiable information",
            violation_type=ViolationType.DATA_PRIVACY,
            pattern=r"\b(?:\d{3}-\d{2}-\d{4}|\d{3}\.\d{2}\.\d{4}|\d{9})\b|\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            action=ActionType.MODIFY,
            safety_level=SafetyLevel.MEDIUM
        ))
        
        # Security rules
        self.add_safety_rule(SafetyRule(
            rule_id="injection_attempts",
            name="Injection Attack Detection",
            description="Detect potential injection attacks",
            violation_type=ViolationType.SECURITY,
            pattern=r"(?i)(script|javascript|sql|command|exec|eval)",
            action=ActionType.BLOCK,
            safety_level=SafetyLevel.HIGH
        ))
        
        # Compliance rules
        self.add_safety_rule(SafetyRule(
            rule_id="gdpr_compliance",
            name="GDPR Compliance Check",
            description="Ensure GDPR compliance in data handling",
            violation_type=ViolationType.COMPLIANCE,
            pattern=r"(?i)(consent|opt-in|opt-out|data subject|right to be forgotten)",
            action=ActionType.ESCALATE,
            safety_level=SafetyLevel.HIGH
        ))
        
        # Ethical rules
        self.add_safety_rule(SafetyRule(
            rule_id="bias_detection",
            name="Bias Detection",
            description="Detect potentially biased language",
            violation_type=ViolationType.ETHICAL,
            pattern=r"(?i)(all|always|never|everyone|nobody|typical|normal)",
            action=ActionType.LOG,
            safety_level=SafetyLevel.MEDIUM
        ))
        
        # Operational safety rules
        self.add_safety_rule(SafetyRule(
            rule_id="resource_limits",
            name="Resource Limit Check",
            description="Check for resource-intensive operations",
            violation_type=ViolationType.OPERATIONAL,
            pattern=r"(?i)(infinite|loop|recursive|memory|disk|cpu)",
            action=ActionType.ESCALATE,
            safety_level=SafetyLevel.MEDIUM
        ))
    
    def add_safety_rule(self, rule: SafetyRule):
        """Add a new safety rule"""
        self.safety_rules.append(rule)
        logger.info(f"Added safety rule: {rule.name}")
    
    def add_alert_callback(self, callback: Callable):
        """Add a callback for safety alerts"""
        self.alert_callbacks.append(callback)
    
    def add_content_modifier(self, violation_type: ViolationType, modifier: Callable):
        """Add a content modifier for specific violation types"""
        self.content_modifiers[violation_type.value] = modifier
    
    async def evaluate_safety(self, 
                             content: str, 
                             agent_id: str, 
                             operation: str,
                             safety_level: SafetyLevel = SafetyLevel.HIGH) -> SafetyResult:
        """
        Evaluate content for safety violations
        """
        self.safety_stats["total_checks"] += 1
        
        violations = []
        action_taken = ActionType.ALLOW
        modified_content = content
        escalation_required = False
        
        # Get applicable rules based on safety level
        applicable_rules = [
            rule for rule in self.safety_rules 
            if rule.enabled and self._is_rule_applicable(rule, safety_level)
        ]
        
        # Check each rule
        for rule in applicable_rules:
            violation = await self._check_rule(rule, content, agent_id, operation)
            if violation:
                violations.append(violation)
                
                # Determine action based on rule
                if rule.action == ActionType.BLOCK:
                    action_taken = ActionType.BLOCK
                    break
                elif rule.action == ActionType.MODIFY:
                    action_taken = ActionType.MODIFY
                    modified_content = await self._modify_content(content, violation)
                elif rule.action == ActionType.ESCALATE:
                    escalation_required = True
                    action_taken = ActionType.ESCALATE
                elif rule.action == ActionType.LOG:
                    if action_taken == ActionType.ALLOW:
                        action_taken = ActionType.LOG
        
        # Update statistics
        if violations:
            self.safety_stats["violations_detected"] += 1
            self.violation_history.extend(violations)
            
            if action_taken == ActionType.BLOCK:
                self.safety_stats["content_blocked"] += 1
            elif action_taken == ActionType.MODIFY:
                self.safety_stats["content_modified"] += 1
            elif action_taken == ActionType.ESCALATE:
                self.safety_stats["escalations"] += 1
        
        # Trigger alerts for critical violations
        critical_violations = [v for v in violations if v.severity == "critical"]
        if critical_violations:
            await self._trigger_alerts(critical_violations)
        
        # Calculate overall confidence
        confidence = self._calculate_confidence(violations)
        
        result = SafetyResult(
            safe=action_taken != ActionType.BLOCK,
            violations=violations,
            action_taken=action_taken,
            modified_content=modified_content if action_taken == ActionType.MODIFY else None,
            escalation_required=escalation_required,
            confidence=confidence
        )
        
        return result
    
    def _is_rule_applicable(self, rule: SafetyRule, safety_level: SafetyLevel) -> bool:
        """Check if a rule is applicable for the given safety level"""
        level_priority = {
            SafetyLevel.LOW: 1,
            SafetyLevel.MEDIUM: 2,
            SafetyLevel.HIGH: 3,
            SafetyLevel.CRITICAL: 4
        }
        
        return level_priority[rule.safety_level] <= level_priority[safety_level]
    
    async def _check_rule(self, rule: SafetyRule, content: str, agent_id: str, operation: str) -> Optional[SafetyViolation]:
        """Check if content violates a specific rule"""
        try:
            # Check if pattern matches
            if re.search(rule.pattern, content, re.IGNORECASE):
                # Calculate confidence based on match strength
                confidence = self._calculate_match_confidence(rule.pattern, content)
                
                # Determine severity based on rule and confidence
                severity = self._determine_severity(rule, confidence)
                
                violation = SafetyViolation(
                    violation_type=rule.violation_type,
                    severity=severity,
                    description=rule.description,
                    detected_content=content,
                    agent_id=agent_id,
                    operation=operation,
                    timestamp=datetime.now(),
                    confidence=confidence,
                    metadata={"rule_id": rule.rule_id, "rule_name": rule.name}
                )
                
                return violation
                
        except Exception as e:
            logger.error(f"Error checking rule {rule.rule_id}: {e}")
        
        return None
    
    def _calculate_match_confidence(self, pattern: str, content: str) -> float:
        """Calculate confidence score for pattern match"""
        try:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if not matches:
                return 0.0
            
            # Base confidence on number of matches and content length
            match_count = len(matches)
            content_length = len(content)
            
            # Higher confidence for more matches relative to content length
            confidence = min(1.0, (match_count * 10) / max(content_length, 1))
            
            return confidence
            
        except Exception:
            return 0.5  # Default confidence
    
    def _determine_severity(self, rule: SafetyRule, confidence: float) -> str:
        """Determine severity based on rule and confidence"""
        if rule.safety_level == SafetyLevel.CRITICAL:
            return "critical"
        elif rule.safety_level == SafetyLevel.HIGH:
            return "high" if confidence > 0.7 else "medium"
        elif rule.safety_level == SafetyLevel.MEDIUM:
            return "medium" if confidence > 0.5 else "low"
        else:
            return "low"
    
    async def _modify_content(self, content: str, violation: SafetyViolation) -> str:
        """Modify content to address safety violations"""
        if violation.violation_type.value in self.content_modifiers:
            modifier = self.content_modifiers[violation.violation_type.value]
            return await modifier(content, violation)
        
        # Default modification based on violation type
        if violation.violation_type == ViolationType.DATA_PRIVACY:
            # Mask PII
            return self._mask_pii(content)
        elif violation.violation_type == ViolationType.CONTENT_SAFETY:
            # Remove harmful content
            return self._remove_harmful_content(content)
        else:
            # Generic sanitization
            return self._sanitize_content(content)
    
    def _mask_pii(self, content: str) -> str:
        """Mask personally identifiable information"""
        # Mask SSN
        content = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', 'XXX-XX-XXXX', content)
        content = re.sub(r'\b\d{3}\.\d{2}\.\d{4}\b', 'XXX.XX.XXXX', content)
        content = re.sub(r'\b\d{9}\b', 'XXXXXXXXX', content)
        
        # Mask email addresses
        content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***@***.***', content)
        
        # Mask phone numbers
        content = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', 'XXX-XXX-XXXX', content)
        content = re.sub(r'\(\d{3}\)\s*\d{3}-\d{4}', '(XXX) XXX-XXXX', content)
        
        return content
    
    def _remove_harmful_content(self, content: str) -> str:
        """Remove harmful content"""
        # Remove content that matches harmful patterns
        harmful_patterns = [
            r'(?i)(violence|hate|discrimination|harassment|threat)',
            r'(?i)(kill|murder|suicide|self-harm)',
            r'(?i)(bomb|explosive|weapon)'
        ]
        
        for pattern in harmful_patterns:
            content = re.sub(pattern, '[CONTENT REMOVED]', content, flags=re.IGNORECASE)
        
        return content
    
    def _sanitize_content(self, content: str) -> str:
        """Generic content sanitization"""
        # Remove potential script tags
        content = re.sub(r'<script.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove potential HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content).strip()
        
        return content
    
    def _calculate_confidence(self, violations: List[SafetyViolation]) -> float:
        """Calculate overall confidence in safety assessment"""
        if not violations:
            return 1.0
        
        # Weight confidence by severity
        severity_weights = {
            "low": 0.1,
            "medium": 0.3,
            "high": 0.7,
            "critical": 1.0
        }
        
        weighted_confidence = 0.0
        total_weight = 0.0
        
        for violation in violations:
            weight = severity_weights.get(violation.severity, 0.5)
            weighted_confidence += violation.confidence * weight
            total_weight += weight
        
        return weighted_confidence / total_weight if total_weight > 0 else 0.0
    
    async def _trigger_alerts(self, violations: List[SafetyViolation]):
        """Trigger alerts for critical violations"""
        for violation in violations:
            alert = {
                "timestamp": violation.timestamp.isoformat(),
                "agent_id": violation.agent_id,
                "operation": violation.operation,
                "violation_type": violation.violation_type.value,
                "severity": violation.severity,
                "description": violation.description,
                "confidence": violation.confidence
            }
            
            logger.critical(f"SAFETY ALERT: {alert}")
            
            # Call alert callbacks
            for callback in self.alert_callbacks:
                try:
                    await callback(alert)
                except Exception as e:
                    logger.error(f"Alert callback failed: {e}")
    
    def get_safety_statistics(self) -> Dict[str, Any]:
        """Get safety statistics"""
        return {
            "total_checks": self.safety_stats["total_checks"],
            "violations_detected": self.safety_stats["violations_detected"],
            "content_blocked": self.safety_stats["content_blocked"],
            "content_modified": self.safety_stats["content_modified"],
            "escalations": self.safety_stats["escalations"],
            "violation_rate": (
                self.safety_stats["violations_detected"] / 
                max(self.safety_stats["total_checks"], 1)
            ),
            "recent_violations": len([
                v for v in self.violation_history 
                if v.timestamp > datetime.now() - timedelta(hours=1)
            ])
        }
    
    def get_violation_history(self, 
                            agent_id: str = None, 
                            violation_type: ViolationType = None,
                            hours: int = 24) -> List[SafetyViolation]:
        """Get violation history with optional filters"""
        filtered_violations = self.violation_history
        
        # Filter by time
        cutoff_time = datetime.now() - timedelta(hours=hours)
        filtered_violations = [
            v for v in filtered_violations 
            if v.timestamp > cutoff_time
        ]
        
        # Filter by agent
        if agent_id:
            filtered_violations = [
                v for v in filtered_violations 
                if v.agent_id == agent_id
            ]
        
        # Filter by violation type
        if violation_type:
            filtered_violations = [
                v for v in filtered_violations 
                if v.violation_type == violation_type
            ]
        
        return filtered_violations
    
    def export_safety_report(self, format: str = "json") -> str:
        """Export safety report"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "statistics": self.get_safety_statistics(),
            "recent_violations": [
                {
                    "violation_type": v.violation_type.value,
                    "severity": v.severity,
                    "description": v.description,
                    "agent_id": v.agent_id,
                    "operation": v.operation,
                    "timestamp": v.timestamp.isoformat(),
                    "confidence": v.confidence
                }
                for v in self.violation_history[-50:]  # Last 50 violations
            ],
            "active_rules": [
                {
                    "rule_id": r.rule_id,
                    "name": r.name,
                    "violation_type": r.violation_type.value,
                    "action": r.action.value,
                    "safety_level": r.safety_level.value,
                    "enabled": r.enabled
                }
                for r in self.safety_rules
            ]
        }
        
        if format == "json":
            return json.dumps(report_data, indent=2, default=str)
        else:
            # CSV format
            lines = ["timestamp,violation_type,severity,agent_id,operation,confidence"]
            for v in self.violation_history:
                lines.append(f"{v.timestamp.isoformat()},{v.violation_type.value},{v.severity},{v.agent_id},{v.operation},{v.confidence}")
            return "\n".join(lines)

# Example usage and testing
async def test_guardrails_framework():
    """Test the guardrails framework"""
    framework = GuardrailsFramework()
    
    # Test safe content
    result = await framework.evaluate_safety(
        "Hello, how can I help you today?",
        "agent1",
        "process_request"
    )
    print(f"Safe content result: {result.safe}")
    
    # Test harmful content
    result = await framework.evaluate_safety(
        "I want to harm someone",
        "agent1",
        "process_request"
    )
    print(f"Harmful content result: {result.safe}")
    print(f"Violations: {len(result.violations)}")
    
    # Test PII content
    result = await framework.evaluate_safety(
        "My email is john@example.com and SSN is 123-45-6789",
        "agent1",
        "process_request"
    )
    print(f"PII content result: {result.safe}")
    print(f"Modified content: {result.modified_content}")
    
    # Test statistics
    stats = framework.get_safety_statistics()
    print(f"Safety statistics: {stats}")

if __name__ == "__main__":
    asyncio.run(test_guardrails_framework())
