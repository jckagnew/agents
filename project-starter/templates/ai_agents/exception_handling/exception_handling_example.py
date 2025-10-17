"""
Pattern 11: Exception Handling & Recovery - Integration Example
Shows how to integrate exception handling with existing AI agents
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the exception handling module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from exception_handler import ExceptionHandler, ErrorType, ErrorSeverity

class AIAgentWithExceptionHandling:
    """
    Example AI agent with integrated exception handling
    Demonstrates Pattern 11 in action
    """
    
    def __init__(self, name: str, handler: ExceptionHandler = None):
        self.name = name
        self.handler = handler or ExceptionHandler()
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
    
    async def process_request(self, request: str, context: dict = None) -> dict:
        """
        Process a request with comprehensive exception handling
        """
        self.request_count += 1
        context = context or {}
        context.update({
            "agent_name": self.name,
            "request_id": f"req_{self.request_count}",
            "timestamp": datetime.now().isoformat()
        })
        
        try:
            # Simulate AI processing that might fail
            result = await self._simulate_ai_processing(request, context)
            self.success_count += 1
            return {
                "success": True,
                "result": result,
                "agent": self.name,
                "request_id": context["request_id"]
            }
            
        except Exception as e:
            self.error_count += 1
            # Use exception handler to recover
            recovery_result = await self.handler.handle_exception(
                e, context, self.name, "process_request"
            )
            
            return {
                "success": False,
                "error": str(e),
                "recovery_result": recovery_result,
                "agent": self.name,
                "request_id": context["request_id"]
            }
    
    async def _simulate_ai_processing(self, request: str, context: dict) -> str:
        """
        Simulate AI processing with various failure modes
        """
        # Simulate different types of failures based on request content
        if "timeout" in request.lower():
            raise TimeoutError("Request timeout - service unavailable")
        
        elif "invalid" in request.lower():
            raise ValueError("Invalid input format")
        
        elif "security" in request.lower():
            raise PermissionError("Security violation detected")
        
        elif "runtime" in request.lower():
            raise RuntimeError("Runtime processing error")
        
        elif "critical" in request.lower():
            raise SystemError("Critical system failure")
        
        elif "fail" in request.lower():
            raise Exception("General processing failure")
        
        else:
            # Success case
            return f"Processed: {request} by {self.name}"
    
    def get_statistics(self) -> dict:
        """Get agent performance statistics"""
        return {
            "agent_name": self.name,
            "total_requests": self.request_count,
            "successful_requests": self.success_count,
            "failed_requests": self.error_count,
            "success_rate": self.success_count / self.request_count if self.request_count > 0 else 0,
            "error_statistics": self.handler.get_error_statistics()
        }

async def demonstrate_exception_handling():
    """
    Demonstrate Pattern 11: Exception Handling & Recovery
    """
    print("🤖 Pattern 11: Exception Handling & Recovery Demo")
    print("=" * 60)
    
    # Create agent with exception handling
    handler = ExceptionHandler()
    agent = AIAgentWithExceptionHandling("DemoAgent", handler)
    
    # Test cases demonstrating different error types
    test_cases = [
        ("Hello world", "Normal request"),
        ("This will timeout", "Timeout error"),
        ("Invalid input format", "Invalid input error"),
        ("Security violation detected", "Security error"),
        ("Runtime processing error", "Runtime error"),
        ("Critical system failure", "Critical error"),
        ("This will fail", "General failure"),
        ("Another normal request", "Normal request"),
    ]
    
    print("\n📋 Running test cases...")
    print("-" * 40)
    
    for request, description in test_cases:
        print(f"\n🔍 Test: {description}")
        print(f"Request: '{request}'")
        
        result = await agent.process_request(request)
        
        if result["success"]:
            print(f"✅ Success: {result['result']}")
        else:
            print(f"❌ Failed: {result['error']}")
            if "recovery_result" in result:
                recovery = result["recovery_result"]
                print(f"🔄 Recovery: {recovery.get('fallback_used', False)}")
                if recovery.get("fallback_used"):
                    print(f"   Fallback type: {recovery.get('fallback_type', 'unknown')}")
                elif recovery.get("human_escalated"):
                    print(f"   Human escalation: {recovery.get('escalation_level', 'unknown')}")
                elif recovery.get("simplified"):
                    print(f"   Request simplified: {recovery.get('reduction_factor', 0)}")
    
    # Show statistics
    print("\n📊 Agent Statistics")
    print("-" * 40)
    stats = agent.get_statistics()
    print(f"Agent: {stats['agent_name']}")
    print(f"Total requests: {stats['total_requests']}")
    print(f"Successful: {stats['successful_requests']}")
    print(f"Failed: {stats['failed_requests']}")
    print(f"Success rate: {stats['success_rate']:.2%}")
    
    print("\n📈 Error Statistics")
    print("-" * 40)
    error_stats = stats['error_statistics']
    print(f"Total errors: {error_stats['total_errors']}")
    print(f"Recent errors: {error_stats['recent_errors']}")
    if error_stats['error_breakdown']:
        print("Error breakdown:")
        for error_type, count in error_stats['error_breakdown'].items():
            print(f"  {error_type}: {count}")
    
    print("\n🎯 Pattern 11 Benefits Demonstrated:")
    print("✅ Automatic error classification")
    print("✅ Intelligent recovery strategies")
    print("✅ Fallback mechanisms")
    print("✅ Human escalation for critical issues")
    print("✅ Request simplification for complex failures")
    print("✅ Comprehensive error monitoring")
    print("✅ Graceful degradation")

async def demonstrate_recovery_strategies():
    """
    Demonstrate different recovery strategies
    """
    print("\n🔄 Recovery Strategies Demo")
    print("=" * 60)
    
    handler = ExceptionHandler()
    agent = AIAgentWithExceptionHandling("RecoveryAgent", handler)
    
    # Test retry with backoff
    print("\n1. Retry with Backoff (Temporary errors)")
    print("-" * 40)
    result = await agent.process_request("This will timeout")
    print(f"Result: {result}")
    
    # Test fallback agent
    print("\n2. Fallback Agent (Permanent errors)")
    print("-" * 40)
    result = await agent.process_request("Invalid input format")
    print(f"Result: {result}")
    
    # Test human escalation
    print("\n3. Human Escalation (Critical errors)")
    print("-" * 40)
    result = await agent.process_request("Security violation detected")
    print(f"Result: {result}")
    
    # Test request simplification
    print("\n4. Request Simplification (Recoverable errors)")
    print("-" * 40)
    result = await agent.process_request("Runtime processing error")
    print(f"Result: {result}")

if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(demonstrate_exception_handling())
    asyncio.run(demonstrate_recovery_strategies())
