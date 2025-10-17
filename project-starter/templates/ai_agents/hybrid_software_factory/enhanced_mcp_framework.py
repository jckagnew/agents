"""
Enhanced MCP Framework for Hybrid Software Factory
Integrates Claude's collaborative approach with Codex's deterministic execution
"""

from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import json
import logging
from datetime import datetime
import aiohttp
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPMode(Enum):
    """MCP operation modes"""
    COLLABORATIVE = "collaborative"  # Claude-style: exploratory, iterative
    DETERMINISTIC = "deterministic"  # Codex-style: task-oriented, precise
    ADAPTIVE = "adaptive"  # Automatically switches based on context

class ToolCategory(Enum):
    """Tool categories for organization"""
    DATABASE = "database"
    API = "api"
    FILE = "file"
    IMAGE = "image"
    WEB = "web"
    AI = "ai"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"

@dataclass
class MCPRequest:
    """Standardized MCP request format"""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tool_name: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    mode: MCPMode = MCPMode.ADAPTIVE
    context: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1
    timeout: float = 30.0
    retry_count: int = 3
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class MCPResponse:
    """Standardized MCP response format"""
    request_id: str
    status: str  # "success", "error", "partial"
    result: Any
    mode_used: MCPMode
    execution_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    suggestions: List[str] = field(default_factory=list)
    confidence: float = 0.0
    reproducible: bool = False

class MCPTool:
    """Base MCP tool class"""
    
    def __init__(self, name: str, category: ToolCategory, capabilities: List[str]):
        self.name = name
        self.category = category
        self.capabilities = capabilities
        self.usage_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "average_execution_time": 0.0,
            "mode_preferences": {}
        }
        self.config = {}
    
    async def execute(self, request: MCPRequest) -> MCPResponse:
        """Execute the tool with given request"""
        start_time = datetime.now()
        
        try:
            # Update usage stats
            self.usage_stats["total_requests"] += 1
            
            # Execute based on mode
            if request.mode == MCPMode.COLLABORATIVE:
                result = await self._execute_collaborative(request)
            elif request.mode == MCPMode.DETERMINISTIC:
                result = await self._execute_deterministic(request)
            else:  # ADAPTIVE
                result = await self._execute_adaptive(request)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update stats
            self.usage_stats["successful_requests"] += 1
            self.usage_stats["average_execution_time"] = execution_time
            
            return MCPResponse(
                request_id=request.request_id,
                status="success",
                result=result,
                mode_used=request.mode,
                execution_time=execution_time,
                metadata=self._generate_metadata(request, result),
                suggestions=self._generate_suggestions(request, result),
                confidence=self._calculate_confidence(result),
                reproducible=self._is_reproducible(request, result)
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Tool execution failed: {e}")
            
            return MCPResponse(
                request_id=request.request_id,
                status="error",
                result={"error": str(e)},
                mode_used=request.mode,
                execution_time=execution_time,
                metadata={"error_type": type(e).__name__},
                suggestions=["Check parameters", "Retry with different mode"],
                confidence=0.0,
                reproducible=False
            )
    
    async def _execute_collaborative(self, request: MCPRequest) -> Any:
        """Collaborative execution - exploratory and iterative"""
        # Override in subclasses
        return {"mode": "collaborative", "result": "base_collaborative_execution"}
    
    async def _execute_deterministic(self, request: MCPRequest) -> Any:
        """Deterministic execution - precise and fast"""
        # Override in subclasses
        return {"mode": "deterministic", "result": "base_deterministic_execution"}
    
    async def _execute_adaptive(self, request: MCPRequest) -> Any:
        """Adaptive execution - chooses best mode"""
        # Analyze context to choose mode
        if self._should_use_collaborative(request):
            return await self._execute_collaborative(request)
        else:
            return await self._execute_deterministic(request)
    
    def _should_use_collaborative(self, request: MCPRequest) -> bool:
        """Determine if collaborative mode is better"""
        # Simple heuristic - can be enhanced
        return (
            request.context.get("exploration", False) or
            request.context.get("complexity", 0) > 5 or
            request.context.get("iterative", False)
        )
    
    def _generate_metadata(self, request: MCPRequest, result: Any) -> Dict[str, Any]:
        """Generate metadata about the execution"""
        return {
            "tool_name": self.name,
            "category": self.category.value,
            "capabilities_used": self._get_used_capabilities(request),
            "execution_mode": request.mode.value,
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_suggestions(self, request: MCPRequest, result: Any) -> List[str]:
        """Generate suggestions based on execution"""
        suggestions = []
        
        if request.mode == MCPMode.COLLABORATIVE:
            suggestions.extend([
                "Consider iterating on this approach",
                "Explore alternative methods",
                "Would you like more detailed analysis?"
            ])
        elif request.mode == MCPMode.DETERMINISTIC:
            suggestions.extend([
                "Result is production-ready",
                "Consider caching for performance",
                "Monitor for consistency"
            ])
        
        return suggestions
    
    def _calculate_confidence(self, result: Any) -> float:
        """Calculate confidence in the result"""
        # Simple confidence calculation - can be enhanced
        if isinstance(result, dict) and result.get("mode") == "deterministic":
            return 0.95
        elif isinstance(result, dict) and result.get("mode") == "collaborative":
            return 0.85
        else:
            return 0.75
    
    def _is_reproducible(self, request: MCPRequest, result: Any) -> bool:
        """Determine if result is reproducible"""
        return request.mode == MCPMode.DETERMINISTIC
    
    def _get_used_capabilities(self, request: MCPRequest) -> List[str]:
        """Get list of capabilities used in this request"""
        return [cap for cap in self.capabilities if cap in str(request.parameters)]

class DatabaseMCPTool(MCPTool):
    """Database operations MCP tool"""
    
    def __init__(self, connection_string: str):
        super().__init__("database", ToolCategory.DATABASE, [
            "query", "insert", "update", "delete", "schema", "migration"
        ])
        self.connection_string = connection_string
        self.connection_pool = None
    
    async def _execute_collaborative(self, request: MCPRequest) -> Any:
        """Collaborative database operations"""
        operation = request.parameters.get("operation", "query")
        
        if operation == "query":
            # Collaborative query - exploratory analysis
            query = request.parameters.get("query", "")
            return await self._collaborative_query(query, request)
        elif operation == "schema_exploration":
            # Explore database schema
            return await self._explore_schema(request)
        else:
            return {"mode": "collaborative", "operation": operation, "exploratory": True}
    
    async def _execute_deterministic(self, request: MCPRequest) -> Any:
        """Deterministic database operations"""
        operation = request.parameters.get("operation", "query")
        
        if operation == "query":
            # Deterministic query - precise execution
            query = request.parameters.get("query", "")
            return await self._deterministic_query(query, request)
        elif operation == "transaction":
            # Atomic transaction
            return await self._execute_transaction(request)
        else:
            return {"mode": "deterministic", "operation": operation, "precise": True}
    
    async def _collaborative_query(self, query: str, request: MCPRequest) -> Any:
        """Collaborative query execution with analysis"""
        # Simulate collaborative database query
        return {
            "mode": "collaborative",
            "query": query,
            "result": "simulated_query_result",
            "analysis": "Detailed analysis of query results",
            "suggestions": [
                "Consider adding indexes for better performance",
                "This query pattern suggests optimization opportunities",
                "Would you like to explore related data?"
            ],
            "iterations": 3
        }
    
    async def _deterministic_query(self, query: str, request: MCPRequest) -> Any:
        """Deterministic query execution"""
        # Simulate deterministic database query
        return {
            "mode": "deterministic",
            "query": query,
            "result": "simulated_query_result",
            "execution_time": 0.1,
            "rows_affected": 42,
            "reproducible": True
        }
    
    async def _explore_schema(self, request: MCPRequest) -> Any:
        """Explore database schema collaboratively"""
        return {
            "mode": "collaborative",
            "schema": "simulated_schema",
            "tables": ["users", "products", "orders"],
            "relationships": "discovered_relationships",
            "suggestions": [
                "Consider normalizing this table",
                "This relationship could be optimized",
                "Missing indexes detected"
            ]
        }
    
    async def _execute_transaction(self, request: MCPRequest) -> Any:
        """Execute atomic transaction"""
        return {
            "mode": "deterministic",
            "transaction_id": str(uuid.uuid4()),
            "operations": request.parameters.get("operations", []),
            "status": "committed",
            "atomic": True
        }

class APIMCPTool(MCPTool):
    """API operations MCP tool"""
    
    def __init__(self, base_url: str, api_key: str = None):
        super().__init__("api", ToolCategory.API, [
            "get", "post", "put", "delete", "webhook", "rate_limit"
        ])
        self.base_url = base_url
        self.api_key = api_key
        self.session = None
    
    async def _execute_collaborative(self, request: MCPRequest) -> Any:
        """Collaborative API operations"""
        method = request.parameters.get("method", "GET")
        endpoint = request.parameters.get("endpoint", "")
        
        # Collaborative API call with analysis
        return {
            "mode": "collaborative",
            "method": method,
            "endpoint": endpoint,
            "response": "simulated_api_response",
            "analysis": "API response analysis with insights",
            "suggestions": [
                "Consider caching this response",
                "Rate limiting detected - optimize calls",
                "This endpoint could be enhanced"
            ],
            "exploration": True
        }
    
    async def _execute_deterministic(self, request: MCPRequest) -> Any:
        """Deterministic API operations"""
        method = request.parameters.get("method", "GET")
        endpoint = request.parameters.get("endpoint", "")
        
        # Deterministic API call
        return {
            "mode": "deterministic",
            "method": method,
            "endpoint": endpoint,
            "response": "simulated_api_response",
            "status_code": 200,
            "execution_time": 0.2,
            "reproducible": True
        }

class FileMCPTool(MCPTool):
    """File operations MCP tool"""
    
    def __init__(self, base_path: str = "./"):
        super().__init__("file", ToolCategory.FILE, [
            "read", "write", "copy", "move", "delete", "search", "analyze"
        ])
        self.base_path = base_path
    
    async def _execute_collaborative(self, request: MCPRequest) -> Any:
        """Collaborative file operations"""
        operation = request.parameters.get("operation", "read")
        file_path = request.parameters.get("file_path", "")
        
        return {
            "mode": "collaborative",
            "operation": operation,
            "file_path": file_path,
            "content": "simulated_file_content",
            "analysis": "File content analysis with insights",
            "suggestions": [
                "This file could be optimized",
                "Consider adding documentation",
                "Similar patterns found in other files"
            ]
        }
    
    async def _execute_deterministic(self, request: MCPRequest) -> Any:
        """Deterministic file operations"""
        operation = request.parameters.get("operation", "read")
        file_path = request.parameters.get("file_path", "")
        
        return {
            "mode": "deterministic",
            "operation": operation,
            "file_path": file_path,
            "content": "simulated_file_content",
            "file_size": 1024,
            "execution_time": 0.05,
            "reproducible": True
        }

class MCPFramework:
    """Enhanced MCP Framework for Hybrid Software Factory"""
    
    def __init__(self):
        self.tools: Dict[str, MCPTool] = {}
        self.request_history: List[MCPRequest] = []
        self.response_history: List[MCPResponse] = []
        self.performance_metrics = {}
        self.mode_preferences = {}
    
    def register_tool(self, tool: MCPTool):
        """Register a tool with the framework"""
        self.tools[tool.name] = tool
        logger.info(f"Registered MCP tool: {tool.name}")
    
    async def execute_request(self, request: MCPRequest) -> MCPResponse:
        """Execute an MCP request"""
        
        if request.tool_name not in self.tools:
            return MCPResponse(
                request_id=request.request_id,
                status="error",
                result={"error": f"Tool {request.tool_name} not found"},
                mode_used=request.mode,
                execution_time=0.0,
                metadata={"error": "tool_not_found"}
            )
        
        # Store request
        self.request_history.append(request)
        
        # Execute tool
        tool = self.tools[request.tool_name]
        response = await tool.execute(request)
        
        # Store response
        self.response_history.append(response)
        
        # Update performance metrics
        self._update_performance_metrics(response)
        
        return response
    
    def _update_performance_metrics(self, response: MCPResponse):
        """Update performance metrics"""
        tool_name = response.metadata.get("tool_name", "unknown")
        
        if tool_name not in self.performance_metrics:
            self.performance_metrics[tool_name] = {
                "total_requests": 0,
                "successful_requests": 0,
                "average_execution_time": 0.0,
                "mode_performance": {}
            }
        
        metrics = self.performance_metrics[tool_name]
        metrics["total_requests"] += 1
        
        if response.status == "success":
            metrics["successful_requests"] += 1
        
        # Update average execution time
        current_avg = metrics["average_execution_time"]
        total_requests = metrics["total_requests"]
        metrics["average_execution_time"] = (
            (current_avg * (total_requests - 1) + response.execution_time) / total_requests
        )
        
        # Update mode performance
        mode = response.mode_used.value
        if mode not in metrics["mode_performance"]:
            metrics["mode_performance"][mode] = {
                "count": 0,
                "success_rate": 0.0,
                "average_time": 0.0
            }
        
        mode_metrics = metrics["mode_performance"][mode]
        mode_metrics["count"] += 1
        
        if response.status == "success":
            success_rate = mode_metrics["success_rate"]
            count = mode_metrics["count"]
            mode_metrics["success_rate"] = (
                (success_rate * (count - 1) + 1.0) / count
            )
        
        # Update average time for mode
        current_mode_avg = mode_metrics["average_time"]
        count = mode_metrics["count"]
        mode_metrics["average_time"] = (
            (current_mode_avg * (count - 1) + response.execution_time) / count
        )
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        return {
            "framework_metrics": {
                "total_requests": len(self.request_history),
                "total_responses": len(self.response_history),
                "success_rate": self._calculate_overall_success_rate(),
                "average_execution_time": self._calculate_overall_avg_time()
            },
            "tool_metrics": self.performance_metrics,
            "mode_preferences": self._analyze_mode_preferences(),
            "recommendations": self._generate_recommendations()
        }
    
    def _calculate_overall_success_rate(self) -> float:
        """Calculate overall success rate"""
        if not self.response_history:
            return 0.0
        
        successful = sum(1 for r in self.response_history if r.status == "success")
        return successful / len(self.response_history)
    
    def _calculate_overall_avg_time(self) -> float:
        """Calculate overall average execution time"""
        if not self.response_history:
            return 0.0
        
        total_time = sum(r.execution_time for r in self.response_history)
        return total_time / len(self.response_history)
    
    def _analyze_mode_preferences(self) -> Dict[str, Any]:
        """Analyze mode usage preferences"""
        mode_counts = {}
        mode_success_rates = {}
        
        for response in self.response_history:
            mode = response.mode_used.value
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
            
            if mode not in mode_success_rates:
                mode_success_rates[mode] = {"success": 0, "total": 0}
            
            mode_success_rates[mode]["total"] += 1
            if response.status == "success":
                mode_success_rates[mode]["success"] += 1
        
        # Calculate success rates
        for mode in mode_success_rates:
            success_data = mode_success_rates[mode]
            mode_success_rates[mode] = (
                success_data["success"] / success_data["total"]
                if success_data["total"] > 0 else 0.0
            )
        
        return {
            "usage_counts": mode_counts,
            "success_rates": mode_success_rates,
            "preferred_mode": max(mode_counts, key=mode_counts.get) if mode_counts else "none"
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on performance data"""
        recommendations = []
        
        # Analyze performance metrics
        for tool_name, metrics in self.performance_metrics.items():
            success_rate = metrics["successful_requests"] / metrics["total_requests"]
            
            if success_rate < 0.8:
                recommendations.append(f"Tool {tool_name} has low success rate ({success_rate:.2%})")
            
            if metrics["average_execution_time"] > 5.0:
                recommendations.append(f"Tool {tool_name} is slow ({metrics['average_execution_time']:.2f}s)")
        
        # Analyze mode preferences
        mode_prefs = self._analyze_mode_preferences()
        if mode_prefs["preferred_mode"] == "collaborative":
            recommendations.append("Consider using deterministic mode for production tasks")
        elif mode_prefs["preferred_mode"] == "deterministic":
            recommendations.append("Consider using collaborative mode for exploration tasks")
        
        return recommendations

# Example usage
async def main():
    """Example usage of the enhanced MCP framework"""
    
    # Create framework
    framework = MCPFramework()
    
    # Create and register tools
    db_tool = DatabaseMCPTool("postgresql://localhost:5432/testdb")
    api_tool = APIMCPTool("https://api.example.com", "your-api-key")
    file_tool = FileMCPTool("./workspace")
    
    framework.register_tool(db_tool)
    framework.register_tool(api_tool)
    framework.register_tool(file_tool)
    
    # Test collaborative request
    collab_request = MCPRequest(
        tool_name="database",
        parameters={"operation": "query", "query": "SELECT * FROM users"},
        mode=MCPMode.COLLABORATIVE,
        context={"exploration": True, "complexity": 7}
    )
    
    collab_response = await framework.execute_request(collab_request)
    print("Collaborative Response:", json.dumps(collab_response.__dict__, indent=2, default=str))
    
    # Test deterministic request
    det_request = MCPRequest(
        tool_name="api",
        parameters={"method": "GET", "endpoint": "/users"},
        mode=MCPMode.DETERMINISTIC,
        context={"production": True, "time_constraint": True}
    )
    
    det_response = await framework.execute_request(det_request)
    print("Deterministic Response:", json.dumps(det_response.__dict__, indent=2, default=str))
    
    # Get performance report
    report = framework.get_performance_report()
    print("Performance Report:", json.dumps(report, indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(main())
