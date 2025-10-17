"""
Test suite for Pattern 11: Exception Handling & Recovery
Comprehensive testing of exception handling capabilities
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# Add the exception handling module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from exception_handler import (
    ExceptionHandler, 
    ErrorType, 
    ErrorSeverity, 
    ErrorContext, 
    RecoveryAction
)

class TestExceptionHandler:
    """Test cases for ExceptionHandler"""
    
    @pytest.fixture
    def handler(self):
        """Create a fresh exception handler for each test"""
        return ExceptionHandler()
    
    @pytest.fixture
    def mock_context(self):
        """Mock context for testing"""
        return {
            "operation": "test_operation",
            "agent_id": "test_agent",
            "user_input": False,
            "security_related": False
        }
    
    def test_error_classification_permanent(self, handler, mock_context):
        """Test classification of permanent errors"""
        try:
            raise ValueError("Invalid input")
        except Exception as e:
            error_context = handler._classify_error(e, mock_context, "test_agent", "test_operation")
            
            assert error_context.error_type == ErrorType.PERMANENT
            assert error_context.severity == ErrorSeverity.MEDIUM
            assert error_context.agent_id == "test_agent"
            assert error_context.operation == "test_operation"
    
    def test_error_classification_temporary(self, handler, mock_context):
        """Test classification of temporary errors"""
        try:
            raise TimeoutError("Request timeout")
        except Exception as e:
            error_context = handler._classify_error(e, mock_context, "test_agent", "test_operation")
            
            assert error_context.error_type == ErrorType.TEMPORARY
            assert error_context.severity == ErrorSeverity.LOW
    
    def test_error_classification_critical(self, handler, mock_context):
        """Test classification of critical errors"""
        mock_context["security_related"] = True
        
        try:
            raise PermissionError("Security violation")
        except Exception as e:
            error_context = handler._classify_error(e, mock_context, "test_agent", "test_operation")
            
            assert error_context.error_type == ErrorType.CRITICAL
            assert error_context.severity == ErrorSeverity.CRITICAL
    
    def test_error_classification_recoverable(self, handler, mock_context):
        """Test classification of recoverable errors"""
        try:
            raise RuntimeError("Runtime error")
        except Exception as e:
            error_context = handler._classify_error(e, mock_context, "test_agent", "test_operation")
            
            assert error_context.error_type == ErrorType.RECOVERABLE
            assert error_context.severity == ErrorSeverity.HIGH
    
    def test_error_logging(self, handler, mock_context, caplog):
        """Test error logging functionality"""
        try:
            raise ValueError("Test error")
        except Exception as e:
            error_context = handler._classify_error(e, mock_context, "test_agent", "test_operation")
            handler._log_error(error_context)
            
            # Check that error was logged
            assert len(handler.error_history) == 1
            assert error_context in handler.error_history
            
            # Check log message
            assert "Error in test_agent: test_operation" in caplog.text
    
    def test_alert_conditions(self, handler, mock_context):
        """Test alert condition checking"""
        # Create multiple high severity errors
        for i in range(5):
            try:
                raise RuntimeError(f"Test error {i}")
            except Exception as e:
                error_context = handler._classify_error(e, mock_context, "test_agent", "test_operation")
                error_context.severity = ErrorSeverity.HIGH
                handler._log_error(error_context)
        
        # Check alert conditions
        handler._check_alert_conditions(handler.error_history[-1])
        
        # Should have 5 errors in history
        assert len(handler.error_history) == 5
    
    @pytest.mark.asyncio
    async def test_retry_with_backoff(self, handler):
        """Test retry with exponential backoff"""
        action = RecoveryAction(
            action_type="retry_with_backoff",
            parameters={"max_retries": 2, "base_delay": 0.1},
            success_criteria=lambda result: result is not None
        )
        
        error_context = ErrorContext(
            error_type=ErrorType.TEMPORARY,
            severity=ErrorSeverity.LOW,
            timestamp=datetime.now(),
            agent_id="test_agent",
            operation="test_operation"
        )
        
        context = {"test": "data"}
        
        # Mock the retry operation to succeed on second attempt
        call_count = 0
        async def mock_retry_operation(ctx):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("First attempt fails")
            return {"success": True, "attempt": call_count}
        
        with patch.object(handler, '_retry_original_operation', side_effect=mock_retry_operation):
            result = await handler._execute_recovery_action(action, error_context, context)
            
            assert result is not None
            assert call_count == 2  # Should have retried once
    
    @pytest.mark.asyncio
    async def test_fallback_agent(self, handler):
        """Test fallback agent recovery"""
        action = RecoveryAction(
            action_type="fallback_agent",
            parameters={"fallback_type": "general_assistant"},
            success_criteria=lambda result: result is not None
        )
        
        error_context = ErrorContext(
            error_type=ErrorType.PERMANENT,
            severity=ErrorSeverity.MEDIUM,
            timestamp=datetime.now(),
            agent_id="test_agent",
            operation="test_operation"
        )
        
        context = {"test": "data"}
        
        result = await handler._execute_recovery_action(action, error_context, context)
        
        assert result is not None
        assert result["fallback_used"] is True
        assert result["fallback_type"] == "general_assistant"
    
    @pytest.mark.asyncio
    async def test_human_escalation(self, handler):
        """Test human escalation recovery"""
        action = RecoveryAction(
            action_type="human_escalation",
            parameters={"escalation_level": "high"},
            success_criteria=lambda result: result.get("human_escalated", False)
        )
        
        error_context = ErrorContext(
            error_type=ErrorType.CRITICAL,
            severity=ErrorSeverity.CRITICAL,
            timestamp=datetime.now(),
            agent_id="test_agent",
            operation="test_operation"
        )
        
        context = {"test": "data"}
        
        result = await handler._execute_recovery_action(action, error_context, context)
        
        assert result is not None
        assert result["human_escalated"] is True
        assert result["escalation_level"] == "high"
        assert "ticket_id" in result
    
    @pytest.mark.asyncio
    async def test_simplify_request(self, handler):
        """Test request simplification recovery"""
        action = RecoveryAction(
            action_type="simplify_request",
            parameters={"complexity_reduction": 0.5},
            success_criteria=lambda result: result.get("simplified", False)
        )
        
        error_context = ErrorContext(
            error_type=ErrorType.RECOVERABLE,
            severity=ErrorSeverity.HIGH,
            timestamp=datetime.now(),
            agent_id="test_agent",
            operation="test_operation"
        )
        
        context = {"complexity": 1.0, "test": "data"}
        
        result = await handler._execute_recovery_action(action, error_context, context)
        
        assert result is not None
        assert result["simplified"] is True
        assert result["reduction_factor"] == 0.5
    
    @pytest.mark.asyncio
    async def test_alternative_approach(self, handler):
        """Test alternative approach recovery"""
        action = RecoveryAction(
            action_type="alternative_approach",
            parameters={"approach": "simplified"},
            success_criteria=lambda result: result.get("alternative_approach", False)
        )
        
        error_context = ErrorContext(
            error_type=ErrorType.RECOVERABLE,
            severity=ErrorSeverity.HIGH,
            timestamp=datetime.now(),
            agent_id="test_agent",
            operation="test_operation"
        )
        
        context = {"test": "data"}
        
        result = await handler._execute_recovery_action(action, error_context, context)
        
        assert result is not None
        assert result["alternative_approach"] is True
        assert result["approach_used"] == "simplified"
    
    @pytest.mark.asyncio
    async def test_immediate_escalation(self, handler):
        """Test immediate escalation for critical errors"""
        action = RecoveryAction(
            action_type="immediate_escalation",
            parameters={"escalation_level": "critical"},
            success_criteria=lambda result: result.get("immediate_escalation", False)
        )
        
        error_context = ErrorContext(
            error_type=ErrorType.CRITICAL,
            severity=ErrorSeverity.CRITICAL,
            timestamp=datetime.now(),
            agent_id="test_agent",
            operation="test_operation"
        )
        
        context = {"test": "data"}
        
        result = await handler._execute_recovery_action(action, error_context, context)
        
        assert result is not None
        assert result["immediate_escalation"] is True
        assert result["escalation_level"] == "critical"
        assert result["alert_sent"] is True
    
    @pytest.mark.asyncio
    async def test_system_shutdown(self, handler):
        """Test system shutdown for critical errors"""
        action = RecoveryAction(
            action_type="system_shutdown",
            parameters={"graceful": True},
            success_criteria=lambda result: result.get("system_shutdown", False)
        )
        
        error_context = ErrorContext(
            error_type=ErrorType.CRITICAL,
            severity=ErrorSeverity.CRITICAL,
            timestamp=datetime.now(),
            agent_id="test_agent",
            operation="test_operation"
        )
        
        context = {"test": "data"}
        
        result = await handler._execute_recovery_action(action, error_context, context)
        
        assert result is not None
        assert result["system_shutdown"] is True
        assert result["graceful"] is True
    
    @pytest.mark.asyncio
    async def test_emergency_fallback(self, handler):
        """Test emergency fallback when all strategies fail"""
        result = handler._emergency_fallback(Exception("Test error"), {"test": "data"})
        
        assert result is not None
        assert result["emergency_fallback"] is True
        assert "Test error" in result["error"]
        assert result["status"] == "fallback_activated"
    
    @pytest.mark.asyncio
    async def test_full_exception_handling_flow(self, handler):
        """Test complete exception handling flow"""
        # Test with a temporary error
        try:
            raise TimeoutError("Request timeout")
        except Exception as e:
            result = await handler.handle_exception(
                e,
                {"operation": "api_call", "timeout": 30},
                "test_agent",
                "test_operation"
            )
            
            assert result is not None
            # Should have used retry strategy for temporary error
            assert "retry" in str(result).lower() or "fallback" in str(result).lower()
    
    def test_error_statistics(self, handler):
        """Test error statistics functionality"""
        # Add some test errors
        for i in range(3):
            try:
                raise ValueError(f"Test error {i}")
            except Exception as e:
                error_context = handler._classify_error(e, {}, "test_agent", "test_operation")
                handler._log_error(error_context)
        
        stats = handler.get_error_statistics()
        
        assert stats["total_errors"] == 3
        assert stats["recent_errors"] == 3
        assert "error_breakdown" in stats
        assert stats["last_error"] is not None
    
    def test_recovery_strategies_initialization(self, handler):
        """Test that recovery strategies are properly initialized"""
        assert ErrorType.PERMANENT in handler.recovery_strategies
        assert ErrorType.TEMPORARY in handler.recovery_strategies
        assert ErrorType.CRITICAL in handler.recovery_strategies
        assert ErrorType.RECOVERABLE in handler.recovery_strategies
        
        # Check that each error type has at least one recovery strategy
        for error_type in ErrorType:
            assert len(handler.recovery_strategies[error_type]) > 0
    
    def test_alert_thresholds(self, handler):
        """Test alert threshold configuration"""
        assert ErrorSeverity.LOW in handler.alert_thresholds
        assert ErrorSeverity.MEDIUM in handler.alert_thresholds
        assert ErrorSeverity.HIGH in handler.alert_thresholds
        assert ErrorSeverity.CRITICAL in handler.alert_thresholds
        
        # Check that thresholds are reasonable
        assert handler.alert_thresholds[ErrorSeverity.CRITICAL] == 1
        assert handler.alert_thresholds[ErrorSeverity.HIGH] == 3
        assert handler.alert_thresholds[ErrorSeverity.MEDIUM] == 5
        assert handler.alert_thresholds[ErrorSeverity.LOW] == 10

# Integration test
@pytest.mark.asyncio
async def test_integration_with_agent():
    """Test integration with a mock AI agent"""
    handler = ExceptionHandler()
    
    # Mock agent that might fail
    class MockAgent:
        def __init__(self, name):
            self.name = name
            self.handler = handler
        
        async def process_request(self, request):
            try:
                # Simulate some processing that might fail
                if "fail" in request.lower():
                    raise RuntimeError("Processing failed")
                return {"success": True, "result": "Processed successfully"}
            except Exception as e:
                return await self.handler.handle_exception(
                    e, 
                    {"request": request, "agent": self.name}, 
                    self.name, 
                    "process_request"
                )
    
    agent = MockAgent("test_agent")
    
    # Test successful request
    result = await agent.process_request("Hello world")
    assert result["success"] is True
    
    # Test failing request
    result = await agent.process_request("This will fail")
    assert result is not None
    # Should have used recovery strategy

if __name__ == "__main__":
    # Run basic tests
    pytest.main([__file__, "-v"])
