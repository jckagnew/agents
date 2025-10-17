"""
Pattern 11: Exception Handling & Recovery
Comprehensive exception handling system for AI agents
"""

import logging
import time
import asyncio
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorType(Enum):
    """Classification of error types for appropriate handling"""
    PERMANENT = "permanent"  # Auth failure, invalid input, security breach
    TEMPORARY = "temporary"  # Timeout, rate limit, network issues
    CRITICAL = "critical"    # Security breach, data corruption
    RECOVERABLE = "recoverable"  # Can be retried with different approach

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ErrorContext:
    """Context information for error handling"""
    error_type: ErrorType
    severity: ErrorSeverity
    timestamp: datetime
    agent_id: str
    operation: str
    retry_count: int = 0
    max_retries: int = 3
    backoff_delay: float = 1.0
    metadata: Dict[str, Any] = None

@dataclass
class RecoveryAction:
    """Recovery action to take for an error"""
    action_type: str
    parameters: Dict[str, Any]
    success_criteria: Callable
    fallback_action: Optional['RecoveryAction'] = None

class ExceptionHandler:
    """
    Main exception handler for AI agents
    Implements comprehensive error classification, recovery, and fallback strategies
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.error_history: List[ErrorContext] = []
        self.recovery_strategies: Dict[ErrorType, List[RecoveryAction]] = {}
        self.fallback_agents: Dict[str, str] = {}
        self.alert_thresholds: Dict[ErrorSeverity, int] = {
            ErrorSeverity.LOW: 10,
            ErrorSeverity.MEDIUM: 5,
            ErrorSeverity.HIGH: 3,
            ErrorSeverity.CRITICAL: 1
        }
        
        # Initialize recovery strategies
        self._initialize_recovery_strategies()
    
    def _initialize_recovery_strategies(self):
        """Initialize default recovery strategies for each error type"""
        
        # Permanent errors - use fallback agents
        self.recovery_strategies[ErrorType.PERMANENT] = [
            RecoveryAction(
                action_type="fallback_agent",
                parameters={"fallback_type": "general_assistant"},
                success_criteria=lambda result: result is not None
            ),
            RecoveryAction(
                action_type="human_escalation",
                parameters={"escalation_level": "medium"},
                success_criteria=lambda result: result.get("human_handled", False)
            )
        ]
        
        # Temporary errors - retry with backoff
        self.recovery_strategies[ErrorType.TEMPORARY] = [
            RecoveryAction(
                action_type="retry_with_backoff",
                parameters={"max_retries": 3, "base_delay": 1.0},
                success_criteria=lambda result: result is not None
            ),
            RecoveryAction(
                action_type="simplify_request",
                parameters={"complexity_reduction": 0.5},
                success_criteria=lambda result: result is not None
            )
        ]
        
        # Critical errors - immediate escalation
        self.recovery_strategies[ErrorType.CRITICAL] = [
            RecoveryAction(
                action_type="immediate_escalation",
                parameters={"escalation_level": "critical"},
                success_criteria=lambda result: result.get("escalated", False)
            ),
            RecoveryAction(
                action_type="system_shutdown",
                parameters={"graceful": True},
                success_criteria=lambda result: result.get("shutdown", False)
            )
        ]
        
        # Recoverable errors - try alternative approaches
        self.recovery_strategies[ErrorType.RECOVERABLE] = [
            RecoveryAction(
                action_type="alternative_approach",
                parameters={"approach": "simplified"},
                success_criteria=lambda result: result is not None
            ),
            RecoveryAction(
                action_type="fallback_agent",
                parameters={"fallback_type": "specialist"},
                success_criteria=lambda result: result is not None
            )
        ]
    
    async def handle_exception(self, 
                             exception: Exception, 
                             context: Dict[str, Any],
                             agent_id: str,
                             operation: str) -> Any:
        """
        Main exception handling method
        Classifies error, applies recovery strategies, and returns result
        """
        try:
            # Classify the error
            error_context = self._classify_error(exception, context, agent_id, operation)
            
            # Log the error
            self._log_error(error_context)
            
            # Check for alert conditions
            self._check_alert_conditions(error_context)
            
            # Apply recovery strategies
            result = await self._apply_recovery_strategies(error_context, context)
            
            return result
            
        except Exception as e:
            logger.error(f"Exception handler failed: {e}")
            return self._emergency_fallback(exception, context)
    
    def _classify_error(self, exception: Exception, context: Dict[str, Any], 
                       agent_id: str, operation: str) -> ErrorContext:
        """Classify error type and severity"""
        
        error_type = ErrorType.TEMPORARY  # Default
        severity = ErrorSeverity.MEDIUM   # Default
        
        # Classify based on exception type
        if isinstance(exception, (ValueError, TypeError, KeyError)):
            error_type = ErrorType.PERMANENT
            severity = ErrorSeverity.MEDIUM
        elif isinstance(exception, (TimeoutError, ConnectionError)):
            error_type = ErrorType.TEMPORARY
            severity = ErrorSeverity.LOW
        elif isinstance(exception, PermissionError):
            error_type = ErrorType.CRITICAL
            severity = ErrorSeverity.CRITICAL
        elif isinstance(exception, (RuntimeError, NotImplementedError)):
            error_type = ErrorType.RECOVERABLE
            severity = ErrorSeverity.HIGH
        
        # Adjust based on context
        if context.get("security_related", False):
            error_type = ErrorType.CRITICAL
            severity = ErrorSeverity.CRITICAL
        elif context.get("user_input", False):
            error_type = ErrorType.PERMANENT
            severity = ErrorSeverity.MEDIUM
        
        return ErrorContext(
            error_type=error_type,
            severity=severity,
            timestamp=datetime.now(),
            agent_id=agent_id,
            operation=operation,
            metadata=context
        )
    
    def _log_error(self, error_context: ErrorContext):
        """Log error with appropriate level"""
        log_message = f"Error in {error_context.agent_id}: {error_context.operation} - {error_context.error_type.value}"
        
        if error_context.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message)
        elif error_context.severity == ErrorSeverity.HIGH:
            logger.error(log_message)
        elif error_context.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message)
        else:
            logger.info(log_message)
        
        # Store in error history
        self.error_history.append(error_context)
    
    def _check_alert_conditions(self, error_context: ErrorContext):
        """Check if alert conditions are met"""
        recent_errors = [
            e for e in self.error_history 
            if e.timestamp > datetime.now() - timedelta(minutes=5)
            and e.severity == error_context.severity
        ]
        
        if len(recent_errors) >= self.alert_thresholds[error_context.severity]:
            self._send_alert(error_context, len(recent_errors))
    
    def _send_alert(self, error_context: ErrorContext, count: int):
        """Send alert for error conditions"""
        alert_message = f"ALERT: {count} {error_context.severity.value} errors in last 5 minutes"
        logger.critical(alert_message)
        
        # In production, this would send to monitoring system
        # For now, just log
        print(f"🚨 {alert_message}")
    
    async def _apply_recovery_strategies(self, error_context: ErrorContext, 
                                       context: Dict[str, Any]) -> Any:
        """Apply recovery strategies based on error type"""
        
        strategies = self.recovery_strategies.get(error_context.error_type, [])
        
        for strategy in strategies:
            try:
                result = await self._execute_recovery_action(strategy, error_context, context)
                if strategy.success_criteria(result):
                    logger.info(f"Recovery successful with strategy: {strategy.action_type}")
                    return result
            except Exception as e:
                logger.warning(f"Recovery strategy {strategy.action_type} failed: {e}")
                continue
        
        # If all strategies fail, use emergency fallback
        return self._emergency_fallback(None, context)
    
    async def _execute_recovery_action(self, action: RecoveryAction, 
                                     error_context: ErrorContext, 
                                     context: Dict[str, Any]) -> Any:
        """Execute a specific recovery action"""
        
        if action.action_type == "retry_with_backoff":
            return await self._retry_with_backoff(action, error_context, context)
        elif action.action_type == "fallback_agent":
            return await self._fallback_agent(action, error_context, context)
        elif action.action_type == "human_escalation":
            return await self._human_escalation(action, error_context, context)
        elif action.action_type == "simplify_request":
            return await self._simplify_request(action, error_context, context)
        elif action.action_type == "alternative_approach":
            return await self._alternative_approach(action, error_context, context)
        elif action.action_type == "immediate_escalation":
            return await self._immediate_escalation(action, error_context, context)
        elif action.action_type == "system_shutdown":
            return await self._system_shutdown(action, error_context, context)
        else:
            raise ValueError(f"Unknown recovery action: {action.action_type}")
    
    async def _retry_with_backoff(self, action: RecoveryAction, 
                                error_context: ErrorContext, 
                                context: Dict[str, Any]) -> Any:
        """Retry operation with exponential backoff"""
        max_retries = action.parameters.get("max_retries", 3)
        base_delay = action.parameters.get("base_delay", 1.0)
        
        for attempt in range(max_retries):
            try:
                # Calculate delay with exponential backoff
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
                
                # Retry the original operation
                # This would call the original function that failed
                result = await self._retry_original_operation(context)
                return result
                
            except Exception as e:
                logger.warning(f"Retry attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
        
        return None
    
    async def _fallback_agent(self, action: RecoveryAction, 
                            error_context: ErrorContext, 
                            context: Dict[str, Any]) -> Any:
        """Use fallback agent for the operation"""
        fallback_type = action.parameters.get("fallback_type", "general_assistant")
        
        # In production, this would route to appropriate fallback agent
        logger.info(f"Using fallback agent: {fallback_type}")
        
        # Simulate fallback agent response
        return {
            "fallback_used": True,
            "fallback_type": fallback_type,
            "response": "Fallback agent handled the request",
            "original_error": str(error_context.error_type)
        }
    
    async def _human_escalation(self, action: RecoveryAction, 
                              error_context: ErrorContext, 
                              context: Dict[str, Any]) -> Any:
        """Escalate to human for handling"""
        escalation_level = action.parameters.get("escalation_level", "medium")
        
        logger.info(f"Escalating to human at level: {escalation_level}")
        
        # In production, this would create a ticket or alert
        return {
            "human_escalated": True,
            "escalation_level": escalation_level,
            "ticket_id": f"TICKET-{int(time.time())}",
            "status": "pending_human_review"
        }
    
    async def _simplify_request(self, action: RecoveryAction, 
                              error_context: ErrorContext, 
                              context: Dict[str, Any]) -> Any:
        """Simplify the request to reduce complexity"""
        complexity_reduction = action.parameters.get("complexity_reduction", 0.5)
        
        logger.info(f"Simplifying request with reduction: {complexity_reduction}")
        
        # In production, this would modify the request parameters
        simplified_context = context.copy()
        simplified_context["complexity_reduced"] = True
        simplified_context["reduction_factor"] = complexity_reduction
        
        return {
            "simplified": True,
            "original_complexity": context.get("complexity", 1.0),
            "new_complexity": context.get("complexity", 1.0) * (1 - complexity_reduction)
        }
    
    async def _alternative_approach(self, action: RecoveryAction, 
                                  error_context: ErrorContext, 
                                  context: Dict[str, Any]) -> Any:
        """Try alternative approach to the operation"""
        approach = action.parameters.get("approach", "simplified")
        
        logger.info(f"Trying alternative approach: {approach}")
        
        # In production, this would implement different logic
        return {
            "alternative_approach": True,
            "approach_used": approach,
            "success": True
        }
    
    async def _immediate_escalation(self, action: RecoveryAction, 
                                  error_context: ErrorContext, 
                                  context: Dict[str, Any]) -> Any:
        """Immediate escalation for critical errors"""
        escalation_level = action.parameters.get("escalation_level", "critical")
        
        logger.critical(f"IMMEDIATE ESCALATION: {escalation_level}")
        
        # In production, this would immediately alert on-call team
        return {
            "immediate_escalation": True,
            "escalation_level": escalation_level,
            "alert_sent": True,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _system_shutdown(self, action: RecoveryAction, 
                             error_context: ErrorContext, 
                             context: Dict[str, Any]) -> Any:
        """Graceful system shutdown for critical errors"""
        graceful = action.parameters.get("graceful", True)
        
        logger.critical(f"SYSTEM SHUTDOWN INITIATED: graceful={graceful}")
        
        # In production, this would initiate shutdown procedures
        return {
            "system_shutdown": True,
            "graceful": graceful,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _retry_original_operation(self, context: Dict[str, Any]) -> Any:
        """Retry the original operation that failed"""
        # This would be implemented to retry the specific operation
        # For now, return a mock success
        return {"retry_success": True, "context": context}
    
    def _emergency_fallback(self, exception: Exception, context: Dict[str, Any]) -> Any:
        """Emergency fallback when all recovery strategies fail"""
        logger.critical("EMERGENCY FALLBACK ACTIVATED")
        
        return {
            "emergency_fallback": True,
            "error": str(exception) if exception else "Unknown error",
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "status": "fallback_activated"
        }
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics for monitoring"""
        if not self.error_history:
            return {"total_errors": 0}
        
        recent_errors = [
            e for e in self.error_history 
            if e.timestamp > datetime.now() - timedelta(hours=1)
        ]
        
        error_counts = {}
        for error in recent_errors:
            key = f"{error.error_type.value}_{error.severity.value}"
            error_counts[key] = error_counts.get(key, 0) + 1
        
        return {
            "total_errors": len(self.error_history),
            "recent_errors": len(recent_errors),
            "error_breakdown": error_counts,
            "last_error": self.error_history[-1].timestamp.isoformat() if self.error_history else None
        }

# Example usage and testing
async def test_exception_handler():
    """Test the exception handler with various error scenarios"""
    handler = ExceptionHandler()
    
    # Test temporary error (timeout)
    try:
        raise TimeoutError("Request timeout")
    except Exception as e:
        result = await handler.handle_exception(
            e, 
            {"operation": "api_call", "timeout": 30}, 
            "test_agent", 
            "test_operation"
        )
        print(f"Temporary error result: {result}")
    
    # Test permanent error (invalid input)
    try:
        raise ValueError("Invalid input provided")
    except Exception as e:
        result = await handler.handle_exception(
            e, 
            {"operation": "data_processing", "user_input": True}, 
            "test_agent", 
            "test_operation"
        )
        print(f"Permanent error result: {result}")
    
    # Test critical error (security)
    try:
        raise PermissionError("Security violation")
    except Exception as e:
        result = await handler.handle_exception(
            e, 
            {"operation": "data_access", "security_related": True}, 
            "test_agent", 
            "test_operation"
        )
        print(f"Critical error result: {result}")
    
    # Get error statistics
    stats = handler.get_error_statistics()
    print(f"Error statistics: {stats}")

if __name__ == "__main__":
    asyncio.run(test_exception_handler())
