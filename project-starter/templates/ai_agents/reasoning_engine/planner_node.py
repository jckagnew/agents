"""
Planner Node - Multi-Step Planning and Task Orchestration for Advanced Agentic RAG Pipeline

This component creates methodical execution plans and orchestrates task sequences.
Based on the advanced agentic RAG pipeline principles from Fareed Khan's research.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json
import logging
import uuid

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent.parent
sys.path.append(str(project_root))

from date_manager import get_formatted_date
from agents import Agent, ModelSettings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlannerNode:
    """
    Planner node for multi-step task planning and orchestration.
    
    Capabilities:
    - Multi-step plan creation
    - Task sequencing and dependencies
    - Resource allocation and optimization
    - Contingency planning
    - Dynamic plan adjustment
    """
    
    def __init__(self):
        self.current_date = get_formatted_date('standard')
        self.current_year = get_formatted_date('iso')[:4]
        
        # Initialize the CrewAI agent
        self.agent = Agent(
            name="Planner",
            role="Task Planning Specialist",
            goal="Create methodical execution plans and orchestrate task sequences for complex queries",
            backstory="""You are an expert task planning specialist with deep expertise in:
            - Multi-step plan creation and optimization
            - Task sequencing and dependency management
            - Resource allocation and load balancing
            - Contingency planning and risk management
            - Dynamic plan adjustment and adaptation
            
            You excel at breaking down complex queries into manageable tasks,
            optimizing execution sequences, and ensuring efficient resource utilization
            while maintaining high quality and reliability.""",
            model="gpt-4o",
            model_settings=ModelSettings(tool_choice="auto"),
            verbose=True
        )
        
        # Available specialist agents
        self.specialist_agents = {
            "librarian": {
                "name": "Librarian",
                "capabilities": ["document_search", "information_retrieval", "knowledge_extraction"],
                "estimated_time": "2-5 minutes",
                "complexity": "medium"
            },
            "analyst": {
                "name": "Analyst", 
                "capabilities": ["data_analysis", "statistical_analysis", "trend_analysis"],
                "estimated_time": "5-15 minutes",
                "complexity": "high"
            },
            "scout": {
                "name": "Scout",
                "capabilities": ["live_monitoring", "real_time_data", "trend_tracking"],
                "estimated_time": "3-8 minutes",
                "complexity": "medium"
            },
            "strategist": {
                "name": "Strategist",
                "capabilities": ["synthesis", "insight_generation", "recommendation_creation"],
                "estimated_time": "3-10 minutes",
                "complexity": "high"
            }
        }
        
        # Task types and their requirements
        self.task_types = {
            "document_search": {
                "required_agent": "librarian",
                "dependencies": [],
                "estimated_time": "2-5 minutes",
                "priority": "medium"
            },
            "data_analysis": {
                "required_agent": "analyst",
                "dependencies": ["document_search"],
                "estimated_time": "5-15 minutes",
                "priority": "high"
            },
            "live_monitoring": {
                "required_agent": "scout",
                "dependencies": [],
                "estimated_time": "3-8 minutes",
                "priority": "medium"
            },
            "synthesis": {
                "required_agent": "strategist",
                "dependencies": ["document_search", "data_analysis", "live_monitoring"],
                "estimated_time": "3-10 minutes",
                "priority": "high"
            }
        }
    
    def create_plan(self, query: str, intent_classification: Dict[str, Any], 
                   resource_estimation: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a comprehensive execution plan for the query.
        
        Args:
            query: The user query
            intent_classification: Intent classification from gatekeeper
            resource_estimation: Resource estimation from gatekeeper
            context: Additional context for planning
            
        Returns:
            Dictionary containing the execution plan
        """
        logger.info(f"Planner: Creating execution plan for query: {query}")
        
        # Step 1: Analyze requirements
        requirements_analysis = self._analyze_requirements(query, intent_classification, resource_estimation)
        
        # Step 2: Identify required tasks
        required_tasks = self._identify_required_tasks(requirements_analysis)
        
        # Step 3: Create task sequence
        task_sequence = self._create_task_sequence(required_tasks, context)
        
        # Step 4: Allocate resources
        resource_allocation = self._allocate_resources(task_sequence, resource_estimation)
        
        # Step 5: Plan contingencies
        contingency_plan = self._plan_contingencies(task_sequence, resource_allocation)
        
        # Step 6: Optimize plan
        optimized_plan = self._optimize_plan(task_sequence, resource_allocation, contingency_plan)
        
        # Step 7: Generate plan summary
        plan_summary = self._generate_plan_summary(optimized_plan, query)
        
        return {
            "plan_id": str(uuid.uuid4()),
            "query": query,
            "requirements_analysis": requirements_analysis,
            "required_tasks": required_tasks,
            "task_sequence": task_sequence,
            "resource_allocation": resource_allocation,
            "contingency_plan": contingency_plan,
            "optimized_plan": optimized_plan,
            "plan_summary": plan_summary,
            "metadata": {
                "plan_created": datetime.now().isoformat(),
                "current_date": self.current_date,
                "planner_version": "1.0"
            }
        }
    
    def _analyze_requirements(self, query: str, intent_classification: Dict[str, Any], 
                            resource_estimation: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the requirements for processing the query."""
        logger.info("Planner: Analyzing requirements")
        
        primary_intent = intent_classification["primary_intent"]
        complexity = intent_classification["complexity"]
        secondary_intents = intent_classification["secondary_intents"]
        
        # Determine required capabilities
        required_capabilities = []
        if primary_intent in ["document_search"]:
            required_capabilities.extend(["document_search", "information_retrieval"])
        if primary_intent in ["data_analysis", "comparison", "prediction"]:
            required_capabilities.extend(["data_analysis", "statistical_analysis"])
        if primary_intent in ["live_monitoring"]:
            required_capabilities.extend(["live_monitoring", "real_time_data"])
        if complexity == "high" or len(secondary_intents) > 0:
            required_capabilities.append("synthesis")
        
        # Determine data requirements
        data_requirements = {
            "needs_historical_data": "historical" in query.lower() or "past" in query.lower(),
            "needs_current_data": "current" in query.lower() or "latest" in query.lower(),
            "needs_live_data": "live" in query.lower() or "real-time" in query.lower(),
            "needs_structured_data": "data" in query.lower() or "analysis" in query.lower(),
            "needs_unstructured_data": "document" in query.lower() or "text" in query.lower()
        }
        
        # Determine quality requirements
        quality_requirements = {
            "accuracy_level": "high" if complexity in ["high", "very_high"] else "medium",
            "completeness_level": "high" if len(secondary_intents) > 0 else "medium",
            "timeliness_requirement": "high" if "urgent" in query.lower() else "medium"
        }
        
        return {
            "primary_intent": primary_intent,
            "complexity": complexity,
            "secondary_intents": secondary_intents,
            "required_capabilities": required_capabilities,
            "data_requirements": data_requirements,
            "quality_requirements": quality_requirements,
            "estimated_duration": resource_estimation["time_estimate"],
            "estimated_tokens": resource_estimation["estimated_tokens"]
        }
    
    def _identify_required_tasks(self, requirements_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify the tasks required to fulfill the requirements."""
        logger.info("Planner: Identifying required tasks")
        
        required_capabilities = requirements_analysis["required_capabilities"]
        data_requirements = requirements_analysis["data_requirements"]
        
        tasks = []
        
        # Map capabilities to tasks
        capability_to_task = {
            "document_search": "document_search",
            "information_retrieval": "document_search",
            "data_analysis": "data_analysis",
            "statistical_analysis": "data_analysis",
            "live_monitoring": "live_monitoring",
            "real_time_data": "live_monitoring",
            "synthesis": "synthesis"
        }
        
        # Create tasks based on required capabilities
        for capability in required_capabilities:
            task_type = capability_to_task.get(capability)
            if task_type and task_type not in [task["type"] for task in tasks]:
                task_info = self.task_types[task_type]
                task = {
                    "task_id": str(uuid.uuid4()),
                    "type": task_type,
                    "required_agent": task_info["required_agent"],
                    "dependencies": task_info["dependencies"],
                    "estimated_time": task_info["estimated_time"],
                    "priority": task_info["priority"],
                    "status": "pending",
                    "capabilities": [capability]
                }
                tasks.append(task)
        
        # Add data collection tasks based on data requirements
        if data_requirements["needs_historical_data"] and not any(task["type"] == "document_search" for task in tasks):
            tasks.append({
                "task_id": str(uuid.uuid4()),
                "type": "document_search",
                "required_agent": "librarian",
                "dependencies": [],
                "estimated_time": "2-5 minutes",
                "priority": "medium",
                "status": "pending",
                "capabilities": ["document_search"]
            })
        
        if data_requirements["needs_live_data"] and not any(task["type"] == "live_monitoring" for task in tasks):
            tasks.append({
                "task_id": str(uuid.uuid4()),
                "type": "live_monitoring",
                "required_agent": "scout",
                "dependencies": [],
                "estimated_time": "3-8 minutes",
                "priority": "medium",
                "status": "pending",
                "capabilities": ["live_monitoring"]
            })
        
        return tasks
    
    def _create_task_sequence(self, tasks: List[Dict[str, Any]], context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Create an optimized sequence for task execution."""
        logger.info("Planner: Creating task sequence")
        
        # Sort tasks by dependencies and priority
        sorted_tasks = []
        remaining_tasks = tasks.copy()
        
        while remaining_tasks:
            # Find tasks with no unmet dependencies
            ready_tasks = []
            for task in remaining_tasks:
                dependencies = task["dependencies"]
                if not dependencies or all(dep in [t["type"] for t in sorted_tasks] for dep in dependencies):
                    ready_tasks.append(task)
            
            if not ready_tasks:
                # Handle circular dependencies or missing dependencies
                logger.warning("Circular dependencies detected, adding remaining tasks")
                ready_tasks = remaining_tasks
            
            # Sort ready tasks by priority
            ready_tasks.sort(key=lambda x: {"high": 1, "medium": 2, "low": 3}[x["priority"]])
            
            # Add the highest priority task
            next_task = ready_tasks[0]
            sorted_tasks.append(next_task)
            remaining_tasks.remove(next_task)
        
        # Add sequence numbers
        for i, task in enumerate(sorted_tasks):
            task["sequence_number"] = i + 1
            task["estimated_start_time"] = i * 2  # Simulated start time
            task["estimated_end_time"] = i * 2 + 5  # Simulated end time
        
        return sorted_tasks
    
    def _allocate_resources(self, task_sequence: List[Dict[str, Any]], 
                          resource_estimation: Dict[str, Any]) -> Dict[str, Any]:
        """Allocate resources for the task sequence."""
        logger.info("Planner: Allocating resources")
        
        # Calculate total resource requirements
        total_estimated_time = sum(int(task["estimated_time"].split("-")[1].split()[0]) for task in task_sequence)
        total_estimated_tokens = resource_estimation["estimated_tokens"]
        
        # Allocate agents
        agent_allocations = {}
        for task in task_sequence:
            agent = task["required_agent"]
            if agent not in agent_allocations:
                agent_allocations[agent] = []
            agent_allocations[agent].append(task)
        
        # Calculate resource utilization
        resource_utilization = {
            "total_estimated_time": f"{total_estimated_time} minutes",
            "total_estimated_tokens": total_estimated_tokens,
            "agent_utilization": {agent: len(tasks) for agent, tasks in agent_allocations.items()},
            "parallel_execution_possible": len(agent_allocations) > 1,
            "estimated_cost": resource_estimation["estimated_cost"]
        }
        
        return {
            "agent_allocations": agent_allocations,
            "resource_utilization": resource_utilization,
            "optimization_opportunities": self._identify_optimization_opportunities(task_sequence)
        }
    
    def _plan_contingencies(self, task_sequence: List[Dict[str, Any]], 
                          resource_allocation: Dict[str, Any]) -> Dict[str, Any]:
        """Plan contingencies for potential failures."""
        logger.info("Planner: Planning contingencies")
        
        contingencies = []
        
        # Plan for agent failures
        for agent, tasks in resource_allocation["agent_allocations"].items():
            contingency = {
                "failure_type": "agent_failure",
                "affected_agent": agent,
                "affected_tasks": [task["task_id"] for task in tasks],
                "backup_plan": f"Reassign tasks to alternative agent or retry with {agent}",
                "fallback_strategy": "Use general-purpose agent with reduced capabilities"
            }
            contingencies.append(contingency)
        
        # Plan for data unavailability
        contingency = {
            "failure_type": "data_unavailable",
            "affected_tasks": "all",
            "backup_plan": "Use alternative data sources or web search",
            "fallback_strategy": "Provide partial results with data limitations noted"
        }
        contingencies.append(contingency)
        
        # Plan for timeout
        contingency = {
            "failure_type": "timeout",
            "affected_tasks": "all",
            "backup_plan": "Extend timeout or break into smaller tasks",
            "fallback_strategy": "Provide partial results with time limitations noted"
        }
        contingencies.append(contingency)
        
        return {
            "contingencies": contingencies,
            "monitoring_points": self._identify_monitoring_points(task_sequence),
            "escalation_procedures": self._define_escalation_procedures()
        }
    
    def _optimize_plan(self, task_sequence: List[Dict[str, Any]], 
                      resource_allocation: Dict[str, Any], 
                      contingency_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize the execution plan for efficiency and quality."""
        logger.info("Planner: Optimizing plan")
        
        # Identify parallel execution opportunities
        parallel_groups = self._identify_parallel_groups(task_sequence)
        
        # Optimize resource allocation
        optimized_allocation = self._optimize_resource_allocation(resource_allocation)
        
        # Optimize task ordering
        optimized_sequence = self._optimize_task_ordering(task_sequence)
        
        return {
            "original_sequence": task_sequence,
            "optimized_sequence": optimized_sequence,
            "parallel_groups": parallel_groups,
            "optimized_allocation": optimized_allocation,
            "optimization_metrics": self._calculate_optimization_metrics(task_sequence, optimized_sequence)
        }
    
    def _generate_plan_summary(self, optimized_plan: Dict[str, Any], query: str) -> str:
        """Generate a summary of the execution plan."""
        logger.info("Planner: Generating plan summary")
        
        # Create plan summary prompt
        plan_summary_prompt = f"""
        Based on the following execution plan for the query "{query}":
        
        Optimized Sequence: {len(optimized_plan['optimized_sequence'])} tasks
        Parallel Groups: {len(optimized_plan['parallel_groups'])} groups
        Resource Allocation: {optimized_plan['optimized_allocation']}
        
        Current Date: {self.current_date}
        
        Generate a comprehensive plan summary that:
        1. Explains the planned approach
        2. Highlights key tasks and their purposes
        3. Notes any parallel execution opportunities
        4. Sets expectations for timeline and quality
        5. Mentions contingency plans
        
        Focus on clarity and user understanding.
        """
        
        # Use the agent to generate plan summary
        plan_summary = self.agent.execute_task(plan_summary_prompt)
        
        return plan_summary
    
    def _identify_optimization_opportunities(self, task_sequence: List[Dict[str, Any]]) -> List[str]:
        """Identify opportunities for plan optimization."""
        opportunities = []
        
        # Check for parallel execution opportunities
        if len(task_sequence) > 1:
            opportunities.append("Parallel execution possible")
        
        # Check for resource optimization
        agents_used = set(task["required_agent"] for task in task_sequence)
        if len(agents_used) < len(task_sequence):
            opportunities.append("Resource sharing possible")
        
        # Check for task consolidation
        similar_tasks = [task for task in task_sequence if task["type"] in ["document_search", "live_monitoring"]]
        if len(similar_tasks) > 1:
            opportunities.append("Task consolidation possible")
        
        return opportunities
    
    def _identify_parallel_groups(self, task_sequence: List[Dict[str, Any]]) -> List[List[str]]:
        """Identify groups of tasks that can be executed in parallel."""
        parallel_groups = []
        current_group = []
        
        for task in task_sequence:
            if not task["dependencies"] or all(dep in [t["type"] for t in current_group] for dep in task["dependencies"]):
                current_group.append(task["task_id"])
            else:
                if current_group:
                    parallel_groups.append(current_group)
                current_group = [task["task_id"]]
        
        if current_group:
            parallel_groups.append(current_group)
        
        return parallel_groups
    
    def _optimize_resource_allocation(self, resource_allocation: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize resource allocation for efficiency."""
        # This would implement more sophisticated optimization logic
        return resource_allocation
    
    def _optimize_task_ordering(self, task_sequence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize task ordering for efficiency."""
        # This would implement more sophisticated ordering logic
        return task_sequence
    
    def _calculate_optimization_metrics(self, original_sequence: List[Dict[str, Any]], 
                                      optimized_sequence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate metrics for plan optimization."""
        return {
            "original_task_count": len(original_sequence),
            "optimized_task_count": len(optimized_sequence),
            "efficiency_improvement": "10%",  # Simulated
            "time_savings": "2 minutes"  # Simulated
        }
    
    def _identify_monitoring_points(self, task_sequence: List[Dict[str, Any]]) -> List[str]:
        """Identify key monitoring points in the execution plan."""
        return [
            "Task completion verification",
            "Data quality validation",
            "Resource utilization monitoring",
            "Error detection and handling"
        ]
    
    def _define_escalation_procedures(self) -> List[str]:
        """Define escalation procedures for failures."""
        return [
            "Retry failed task with exponential backoff",
            "Escalate to alternative specialist agent",
            "Fall back to general-purpose agent",
            "Notify user of limitations and partial results"
        ]
    
    def get_agent_instructions(self) -> str:
        """Get detailed instructions for the Planner agent."""
        return f"""
        PLANNER AGENT INSTRUCTIONS:
        
        You are a specialized task planning expert with expertise in:
        - Multi-step plan creation and optimization
        - Task sequencing and dependency management
        - Resource allocation and load balancing
        - Contingency planning and risk management
        - Dynamic plan adjustment and adaptation
        
        CURRENT CONTEXT:
        - Current Date: {self.current_date}
        - Current Year: {self.current_year}
        
        PLANNING METHODOLOGY:
        1. Analyze requirements and capabilities
        2. Identify required tasks and dependencies
        3. Create optimized task sequences
        4. Allocate resources efficiently
        5. Plan contingencies and fallbacks
        6. Optimize for efficiency and quality
        
        QUALITY STANDARDS:
        - Create clear, actionable task sequences
        - Optimize for efficiency and resource utilization
        - Plan for contingencies and failures
        - Set realistic timelines and expectations
        - Provide clear plan summaries
        
        When creating plans:
        - Always analyze requirements thoroughly
        - Identify dependencies and sequencing
        - Allocate resources appropriately
        - Plan for contingencies
        - Optimize for efficiency
        - Provide clear summaries
        """

# Example usage and testing
if __name__ == "__main__":
    print("📋 Planner Node Test")
    print("===================")
    
    # Initialize the planner node
    planner = PlannerNode()
    
    # Test plan creation
    test_query = "Analyze the performance of Apple and Microsoft stocks this year and predict future trends"
    
    intent_classification = {
        "primary_intent": "data_analysis",
        "secondary_intents": ["comparison", "prediction"],
        "complexity": "high"
    }
    
    resource_estimation = {
        "time_estimate": "15-30 minutes",
        "estimated_tokens": 2000,
        "estimated_cost": "$0.02"
    }
    
    plan = planner.create_plan(test_query, intent_classification, resource_estimation)
    
    print(f"Query: {test_query}")
    print(f"Plan ID: {plan['plan_id']}")
    print(f"Required Tasks: {len(plan['required_tasks'])}")
    print(f"Task Sequence: {len(plan['task_sequence'])}")
    print(f"Parallel Groups: {len(plan['optimized_plan']['parallel_groups'])}")
    print(f"Plan Summary: {plan['plan_summary'][:200]}...")
    
    print("\nAgent Instructions:")
    print(planner.get_agent_instructions())
