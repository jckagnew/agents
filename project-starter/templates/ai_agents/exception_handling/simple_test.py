"""
Simple test for Pattern 11: Exception Handling & Recovery
No external dependencies required
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the exception handling module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from exception_handler import ExceptionHandler, ErrorType, ErrorSeverity

async def test_basic_functionality():
    """Test basic exception handling functionality"""
    print("🧪 Testing Pattern 11: Exception Handling & Recovery")
    print("=" * 60)
    
    # Create handler
    handler = ExceptionHandler()
    print("✅ Exception handler created")
    
    # Test error classification
    print("\n📋 Testing error classification...")
    
    # Test temporary error
    try:
        raise TimeoutError("Request timeout")
    except Exception as e:
        error_context = handler._classify_error(e, {}, "test_agent", "test_operation")
        assert error_context.error_type == ErrorType.TEMPORARY
        assert error_context.severity == ErrorSeverity.LOW
        print("✅ Temporary error classification works")
    
    # Test permanent error
    try:
        raise ValueError("Invalid input")
    except Exception as e:
        error_context = handler._classify_error(e, {}, "test_agent", "test_operation")
        assert error_context.error_type == ErrorType.PERMANENT
        assert error_context.severity == ErrorSeverity.MEDIUM
        print("✅ Permanent error classification works")
    
    # Test critical error
    try:
        raise PermissionError("Security violation")
    except Exception as e:
        error_context = handler._classify_error(e, {"security_related": True}, "test_agent", "test_operation")
        assert error_context.error_type == ErrorType.CRITICAL
        assert error_context.severity == ErrorSeverity.CRITICAL
        print("✅ Critical error classification works")
    
    # Test recoverable error
    try:
        raise RuntimeError("Runtime error")
    except Exception as e:
        error_context = handler._classify_error(e, {}, "test_agent", "test_operation")
        assert error_context.error_type == ErrorType.RECOVERABLE
        assert error_context.severity == ErrorSeverity.HIGH
        print("✅ Recoverable error classification works")
    
    print("\n🔄 Testing recovery strategies...")
    
    # Test fallback agent recovery
    try:
        raise ValueError("Invalid input")
    except Exception as e:
        result = await handler.handle_exception(e, {"operation": "test"}, "test_agent", "test_operation")
        assert result is not None
        print("✅ Fallback agent recovery works")
    
    # Test retry with backoff
    try:
        raise TimeoutError("Request timeout")
    except Exception as e:
        result = await handler.handle_exception(e, {"operation": "test"}, "test_agent", "test_operation")
        assert result is not None
        print("✅ Retry with backoff works")
    
    # Test human escalation
    try:
        raise PermissionError("Security violation")
    except Exception as e:
        result = await handler.handle_exception(e, {"security_related": True}, "test_agent", "test_operation")
        assert result is not None
        print("✅ Human escalation works")
    
    # Test emergency fallback
    result = handler._emergency_fallback(Exception("Test error"), {"test": "data"})
    assert result is not None
    assert result["emergency_fallback"] is True
    print("✅ Emergency fallback works")
    
    # Test error statistics
    stats = handler.get_error_statistics()
    assert "total_errors" in stats
    print("✅ Error statistics work")
    
    print("\n🎯 All basic tests passed!")
    return True

async def test_integration_example():
    """Test the integration example"""
    print("\n🔗 Testing integration example...")
    
    # Import the example
    from exception_handling_example import AIAgentWithExceptionHandling
    
    # Create agent
    handler = ExceptionHandler()
    agent = AIAgentWithExceptionHandling("TestAgent", handler)
    
    # Test successful request
    result = await agent.process_request("Hello world")
    assert result["success"] is True
    print("✅ Successful request processing works")
    
    # Test failing request
    result = await agent.process_request("This will fail")
    assert result["success"] is False
    assert "recovery_result" in result
    print("✅ Failing request recovery works")
    
    # Test statistics
    stats = agent.get_statistics()
    assert stats["total_requests"] >= 2
    print("✅ Agent statistics work")
    
    print("🎯 Integration example works!")
    return True

async def run_demonstration():
    """Run the full demonstration"""
    print("\n🎬 Running Pattern 11 Demonstration...")
    print("=" * 60)
    
    # Import and run the demonstration
    from exception_handling_example import demonstrate_exception_handling, demonstrate_recovery_strategies
    
    await demonstrate_exception_handling()
    await demonstrate_recovery_strategies()
    
    print("\n🎉 Pattern 11 demonstration complete!")
    return True

async def main():
    """Main test runner"""
    try:
        print("🚀 Starting Pattern 11 Tests")
        print("=" * 60)
        
        # Run basic tests
        await test_basic_functionality()
        
        # Run integration tests
        await test_integration_example()
        
        # Run demonstration
        await run_demonstration()
        
        print("\n✅ ALL TESTS PASSED!")
        print("🎯 Pattern 11: Exception Handling & Recovery is working correctly")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(main())
