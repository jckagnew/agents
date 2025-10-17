"""
Hybrid Software Factory Agent Framework
Combines Claude's collaborative approach with Codex's deterministic execution
"""

from typing import Dict, List, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod
import asyncio
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentMode(Enum):
    """Agent operation modes"""
    COLLABORATIVE = "collaborative"  # Claude-style: exploratory, iterative
    DETERMINISTIC = "deterministic"  # Codex-style: task-oriented, precise
    HYBRID = "hybrid"  # Switches between modes based on context

class TaskType(Enum):
    """Types of tasks for mode selection"""
    EXPLORATION = "exploration"  # Idea validation, brainstorming
    PROTOTYPING = "prototyping"  # Rapid development, iteration
    PRODUCTION = "production"  # Deployment, scaling, monetization
    MAINTENANCE = "maintenance"  # Bug fixes, updates

@dataclass
class AgentContext:
    """Context for agent decision making"""
    task_type: TaskType
    complexity: int  # 1-10 scale
    time_constraint: bool
    quality_requirement: str  # "exploratory", "production", "critical"
    user_preference: Optional[AgentMode] = None
    previous_success_rate: float = 0.0

@dataclass
class ToolRequest:
    """Standardized tool request format"""
    tool_name: str
    parameters: Dict[str, Any]
    context: AgentContext
    mode: AgentMode
    priority: int = 1

class MCPToolInterface(ABC):
    """Abstract base class for MCP tool interfaces"""
    
    @abstractmethod
    async def execute(self, request: ToolRequest) -> Dict[str, Any]:
        """Execute tool with given request"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of tool capabilities"""
        pass

class CollaborativeMCPTool(MCPToolInterface):
    """Claude-style collaborative tool interface"""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.conversation_history = []
        self.context_memory = {}
    
    async def execute(self, request: ToolRequest) -> Dict[str, Any]:
        """Execute with collaborative approach"""
        logger.info(f"Collaborative execution: {request.tool_name}")
        
        # Add to conversation history for context
        self.conversation_history.append({
            "timestamp": datetime.now(),
            "tool": request.tool_name,
            "parameters": request.parameters,
            "context": request.context
        })
        
        # Collaborative execution with context awareness
        result = await self._collaborative_execute(request)
        
        # Update context memory
        self.context_memory[request.tool_name] = {
            "last_used": datetime.now(),
            "success_rate": 0.8,  # Would be calculated from actual results
            "preferences": self._extract_preferences(request)
        }
        
        return result
    
    async def _collaborative_execute(self, request: ToolRequest) -> Dict[str, Any]:
        """Collaborative execution logic"""
        # Simulate collaborative tool execution
        return {
            "status": "success",
            "mode": "collaborative",
            "result": f"Collaborative execution of {request.tool_name}",
            "suggestions": self._generate_suggestions(request),
            "context_used": len(self.conversation_history),
            "iterations": 3  # Collaborative tools often iterate
        }
    
    def _generate_suggestions(self, request: ToolRequest) -> List[str]:
        """Generate suggestions based on context"""
        return [
            f"Consider exploring {request.tool_name} alternatives",
            "Would you like to iterate on this approach?",
            "I noticed a pattern in your usage - shall we optimize?"
        ]
    
    def _extract_preferences(self, request: ToolRequest) -> Dict[str, Any]:
        """Extract user preferences from request"""
        return {
            "preferred_approach": "iterative",
            "detail_level": "comprehensive",
            "exploration_tendency": "high"
        }
    
    def get_capabilities(self) -> List[str]:
        return self.capabilities

class DeterministicMCPTool(MCPToolInterface):
    """Codex-style deterministic tool interface"""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.execution_stats = {}
    
    async def execute(self, request: ToolRequest) -> Dict[str, Any]:
        """Execute with deterministic approach"""
        logger.info(f"Deterministic execution: {request.tool_name}")
        
        # Track execution statistics
        if request.tool_name not in self.execution_stats:
            self.execution_stats[request.tool_name] = {
                "total_executions": 0,
                "success_rate": 0.0,
                "average_time": 0.0
            }
        
        start_time = datetime.now()
        
        # Deterministic execution
        result = await self._deterministic_execute(request)
        
        # Update statistics
        execution_time = (datetime.now() - start_time).total_seconds()
        self.execution_stats[request.tool_name]["total_executions"] += 1
        self.execution_stats[request.tool_name]["average_time"] = execution_time
        
        return result
    
    async def _deterministic_execute(self, request: ToolRequest) -> Dict[str, Any]:
        """Deterministic execution logic"""
        # Simulate deterministic tool execution
        return {
            "status": "success",
            "mode": "deterministic",
            "result": f"Deterministic execution of {request.tool_name}",
            "execution_time": 0.5,  # Fast, precise execution
            "confidence": 0.95,  # High confidence in deterministic results
            "reproducible": True
        }
    
    def get_capabilities(self) -> List[str]:
        return self.capabilities

class HybridAgent:
    """Hybrid agent that switches between collaborative and deterministic modes"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools: Dict[str, MCPToolInterface] = {}
        self.mode_history = []
        self.performance_metrics = {}
        self.current_mode = AgentMode.HYBRID
        
    def register_tool(self, tool: MCPToolInterface):
        """Register a tool with the agent"""
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")
    
    def select_mode(self, context: AgentContext) -> AgentMode:
        """Intelligently select the best mode for the given context"""
        
        # User preference override
        if context.user_preference:
            return context.user_preference
        
        # Mode selection logic
        if context.task_type == TaskType.EXPLORATION:
            return AgentMode.COLLABORATIVE
        elif context.task_type == TaskType.PRODUCTION:
            return AgentMode.DETERMINISTIC
        elif context.task_type == TaskType.PROTOTYPING:
            # Hybrid for prototyping - start collaborative, end deterministic
            return AgentMode.HYBRID
        elif context.complexity > 7:
            return AgentMode.COLLABORATIVE
        elif context.time_constraint:
            return AgentMode.DETERMINISTIC
        else:
            return AgentMode.HYBRID
    
    async def execute_task(self, tool_name: str, parameters: Dict[str, Any], 
                          context: AgentContext) -> Dict[str, Any]:
        """Execute a task using the appropriate mode"""
        
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not registered")
        
        # Select mode
        selected_mode = self.select_mode(context)
        self.current_mode = selected_mode
        
        # Create tool request
        request = ToolRequest(
            tool_name=tool_name,
            parameters=parameters,
            context=context,
            mode=selected_mode
        )
        
        # Execute based on mode
        if selected_mode == AgentMode.COLLABORATIVE:
            return await self._execute_collaborative(request)
        elif selected_mode == AgentMode.DETERMINISTIC:
            return await self._execute_deterministic(request)
        else:  # HYBRID
            return await self._execute_hybrid(request)
    
    async def _execute_collaborative(self, request: ToolRequest) -> Dict[str, Any]:
        """Execute in collaborative mode"""
        tool = self.tools[request.tool_name]
        
        # Ensure tool supports collaborative mode
        if isinstance(tool, CollaborativeMCPTool):
            return await tool.execute(request)
        else:
            # Convert deterministic tool to collaborative approach
            return await self._adapt_tool_to_collaborative(request)
    
    async def _execute_deterministic(self, request: ToolRequest) -> Dict[str, Any]:
        """Execute in deterministic mode"""
        tool = self.tools[request.tool_name]
        
        # Ensure tool supports deterministic mode
        if isinstance(tool, DeterministicMCPTool):
            return await tool.execute(request)
        else:
            # Convert collaborative tool to deterministic approach
            return await self._adapt_tool_to_deterministic(request)
    
    async def _execute_hybrid(self, request: ToolRequest) -> Dict[str, Any]:
        """Execute in hybrid mode - combines both approaches"""
        logger.info(f"Hybrid execution for {request.tool_name}")
        
        # Start with collaborative exploration
        collaborative_result = await self._execute_collaborative(request)
        
        # Refine with deterministic execution
        deterministic_result = await self._execute_deterministic(request)
        
        # Combine results
        return {
            "mode": "hybrid",
            "collaborative_result": collaborative_result,
            "deterministic_result": deterministic_result,
            "recommendation": self._generate_hybrid_recommendation(
                collaborative_result, deterministic_result
            ),
            "best_approach": self._select_best_approach(
                collaborative_result, deterministic_result, request.context
            )
        }
    
    async def _adapt_tool_to_collaborative(self, request: ToolRequest) -> Dict[str, Any]:
        """Adapt deterministic tool to collaborative approach"""
        tool = self.tools[request.tool_name]
        
        # Add collaborative wrapper
        result = await tool.execute(request)
        
        return {
            **result,
            "mode": "collaborative_adapted",
            "suggestions": [
                "Consider exploring alternative approaches",
                "Would you like to iterate on this result?",
                "I can provide more detailed analysis if needed"
            ],
            "collaborative_features": {
                "iterative": True,
                "exploratory": True,
                "context_aware": True
            }
        }
    
    async def _adapt_tool_to_deterministic(self, request: ToolRequest) -> Dict[str, Any]:
        """Adapt collaborative tool to deterministic approach"""
        tool = self.tools[request.tool_name]
        
        # Add deterministic wrapper
        result = await tool.execute(request)
        
        return {
            **result,
            "mode": "deterministic_adapted",
            "precision": "high",
            "reproducible": True,
            "execution_time": 0.3,
            "confidence": 0.9
        }
    
    def _generate_hybrid_recommendation(self, collab_result: Dict, det_result: Dict) -> str:
        """Generate recommendation based on both results"""
        if collab_result.get("iterations", 0) > det_result.get("execution_time", 0):
            return "Use collaborative approach for exploration, deterministic for production"
        else:
            return "Use deterministic approach for efficiency, collaborative for complex tasks"
    
    def _select_best_approach(self, collab_result: Dict, det_result: Dict, 
                             context: AgentContext) -> str:
        """Select the best approach based on context"""
        if context.task_type == TaskType.PRODUCTION:
            return "deterministic"
        elif context.task_type == TaskType.EXPLORATION:
            return "collaborative"
        else:
            return "hybrid"

class SoftwareFactoryOrchestrator:
    """Orchestrates the hybrid software factory workflow"""
    
    def __init__(self):
        self.agents: Dict[str, HybridAgent] = {}
        self.workflow_state = {}
        self.handoff_points = []
    
    def register_agent(self, agent: HybridAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")
    
    async def execute_software_factory_workflow(self, idea: str, 
                                              requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete software factory workflow"""
        
        logger.info(f"Starting software factory workflow for: {idea}")
        
        # Phase 1: Collaborative Exploration (Idea to Prototype)
        exploration_result = await self._collaborative_exploration_phase(idea, requirements)
        
        # Phase 2: Hybrid Prototyping
        prototype_result = await self._hybrid_prototyping_phase(exploration_result)
        
        # Phase 3: Deterministic Production (Prototype to Monetization)
        production_result = await self._deterministic_production_phase(prototype_result)
        
        # Phase 4: Seamless Handoffs
        handoff_result = await self._create_seamless_handoffs(
            exploration_result, prototype_result, production_result
        )
        
        return {
            "workflow": "software_factory",
            "idea": idea,
            "exploration": exploration_result,
            "prototyping": prototype_result,
            "production": production_result,
            "handoffs": handoff_result,
            "success": True
        }
    
    async def _collaborative_exploration_phase(self, idea: str, 
                                             requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborative exploration phase (Claude-style)"""
        
        context = AgentContext(
            task_type=TaskType.EXPLORATION,
            complexity=5,
            time_constraint=False,
            quality_requirement="exploratory"
        )
        
        # Use idea validation agent
        if "idea_validator" in self.agents:
            result = await self.agents["idea_validator"].execute_task(
                "validate_idea", {"idea": idea, "requirements": requirements}, context
            )
        else:
            result = {"status": "no_idea_validator", "idea": idea}
        
        return {
            "phase": "collaborative_exploration",
            "mode": "collaborative",
            "result": result,
            "next_phase": "hybrid_prototyping"
        }
    
    async def _hybrid_prototyping_phase(self, exploration_result: Dict[str, Any]) -> Dict[str, Any]:
        """Hybrid prototyping phase"""
        
        context = AgentContext(
            task_type=TaskType.PROTOTYPING,
            complexity=7,
            time_constraint=True,
            quality_requirement="production"
        )
        
        # Use rapid prototyping agent
        if "rapid_prototyper" in self.agents:
            result = await self.agents["rapid_prototyper"].execute_task(
                "create_prototype", exploration_result, context
            )
        else:
            result = {"status": "no_prototyper", "exploration": exploration_result}
        
        return {
            "phase": "hybrid_prototyping",
            "mode": "hybrid",
            "result": result,
            "next_phase": "deterministic_production"
        }
    
    async def _deterministic_production_phase(self, prototype_result: Dict[str, Any]) -> Dict[str, Any]:
        """Deterministic production phase (Codex-style)"""
        
        context = AgentContext(
            task_type=TaskType.PRODUCTION,
            complexity=8,
            time_constraint=True,
            quality_requirement="critical"
        )
        
        # Use monetization agent
        if "monetizer" in self.agents:
            result = await self.agents["monetizer"].execute_task(
                "monetize_prototype", prototype_result, context
            )
        else:
            result = {"status": "no_monetizer", "prototype": prototype_result}
        
        return {
            "phase": "deterministic_production",
            "mode": "deterministic",
            "result": result,
            "next_phase": "complete"
        }
    
    async def _create_seamless_handoffs(self, exploration: Dict, 
                                      prototyping: Dict, production: Dict) -> Dict[str, Any]:
        """Create seamless handoffs between phases"""
        
        return {
            "exploration_to_prototyping": {
                "data_transfer": "seamless",
                "context_preservation": True,
                "mode_transition": "collaborative_to_hybrid"
            },
            "prototyping_to_production": {
                "data_transfer": "seamless",
                "context_preservation": True,
                "mode_transition": "hybrid_to_deterministic"
            },
            "overall_workflow": {
                "continuity": "maintained",
                "context_accumulation": True,
                "quality_progression": "exploratory_to_critical"
            }
        }

# Example usage and testing
async def main():
    """Example usage of the hybrid software factory framework"""
    
    # Create orchestrator
    orchestrator = SoftwareFactoryOrchestrator()
    
    # Create hybrid agents
    idea_validator = HybridAgent("idea_validator")
    rapid_prototyper = HybridAgent("rapid_prototyper")
    monetizer = HybridAgent("monetizer")
    
    # Register agents
    orchestrator.register_agent(idea_validator)
    orchestrator.register_agent(rapid_prototyper)
    orchestrator.register_agent(monetizer)
    
    # Create tools
    collaborative_tool = CollaborativeMCPTool("validate_idea", ["analysis", "research"])
    deterministic_tool = DeterministicMCPTool("monetize_prototype", ["deployment", "scaling"])
    
    # Register tools with agents
    idea_validator.register_tool(collaborative_tool)
    monetizer.register_tool(deterministic_tool)
    
    # Execute workflow
    result = await orchestrator.execute_software_factory_workflow(
        "AI-powered fitness app",
        {"target_users": "fitness enthusiasts", "monetization": "subscription"}
    )
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
