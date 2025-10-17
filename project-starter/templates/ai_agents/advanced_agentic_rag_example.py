"""
Advanced Agentic RAG Pipeline - Complete Integration Example

This example demonstrates how to integrate all components of the advanced agentic RAG pipeline
based on Fareed Khan's research and the Level Up Coding article.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import logging

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent  # Go up 3 levels to get to agents/
utilities_dir = project_root / "utilities"
sys.path.append(str(utilities_dir))
sys.path.append(str(project_root))

from date_manager import get_formatted_date

# Import specialist agents
from .specialist_agents.librarian_agent import LibrarianAgent
from .specialist_agents.analyst_agent import AnalystAgent
from .specialist_agents.scout_agent import ScoutAgent

# Import reasoning engine components
from .reasoning_engine.gatekeeper_node import GatekeeperNode
from .reasoning_engine.planner_node import PlannerNode

# Import evaluation and red teaming
from .evaluation.evaluation_framework import EvaluationFramework
from .red_teaming.red_team_bot import RedTeamBot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedAgenticRAGPipeline:
    """
    Complete advanced agentic RAG pipeline implementation.
    
    This class integrates all components:
    - Specialist agents (Librarian, Analyst, Scout)
    - Reasoning engine (Gatekeeper, Planner)
    - Evaluation framework
    - Red teaming capabilities
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.current_date = get_formatted_date('standard')
        self.current_year = get_formatted_date('iso')[:4]
        
        # Initialize specialist agents
        self.librarian = LibrarianAgent()
        self.analyst = AnalystAgent()
        self.scout = ScoutAgent()
        
        # Initialize reasoning engine
        self.gatekeeper = GatekeeperNode()
        self.planner = PlannerNode()
        
        # Initialize evaluation and testing
        self.evaluator = EvaluationFramework()
        self.red_team_bot = RedTeamBot()
        
        # Track conversation history
        self.conversation_history = []
        
        logger.info("Advanced Agentic RAG Pipeline initialized successfully")
    
    def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a query through the complete agentic RAG pipeline.
        
        Args:
            query: The user query to process
            context: Additional context for processing
            
        Returns:
            Dictionary containing the complete response and metadata
        """
        logger.info(f"Processing query: {query}")
        
        # Step 1: Gatekeeper validation
        validation_result = self.gatekeeper.process_query(query, context)
        
        if validation_result["routing_decision"]["needs_clarification"]:
            return {
                "query": query,
                "response": validation_result["validation_response"],
                "status": "needs_clarification",
                "metadata": {
                    "processed_at": datetime.now().isoformat(),
                    "pipeline_stage": "gatekeeper"
                }
            }
        
        # Step 2: Create execution plan
        plan = self.planner.create_plan(
            query, 
            validation_result["intent_classification"],
            validation_result["routing_decision"]
        )
        
        # Step 3: Execute plan with specialist agents
        execution_results = self._execute_plan(plan, query, context)
        
        # Step 4: Synthesize results
        final_response = self._synthesize_results(execution_results, query)
        
        # Step 5: Evaluate response quality
        evaluation_result = self.evaluator.evaluate_response(query, final_response, context=context)
        
        # Step 6: Store conversation history
        self.conversation_history.append({
            "query": query,
            "response": final_response,
            "evaluation": evaluation_result,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "query": query,
            "response": final_response,
            "evaluation": evaluation_result,
            "execution_plan": plan,
            "execution_results": execution_results,
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "pipeline_stage": "complete",
                "conversation_id": len(self.conversation_history)
            }
        }
    
    def _execute_plan(self, plan: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the planned task sequence using specialist agents."""
        logger.info("Executing planned task sequence")
        
        execution_results = {}
        task_sequence = plan["optimized_plan"]["optimized_sequence"]
        
        for task in task_sequence:
            task_type = task["type"]
            required_agent = task["required_agent"]
            
            logger.info(f"Executing task: {task_type} with {required_agent}")
            
            try:
                if required_agent == "librarian":
                    result = self.librarian.search_documents(query, context)
                elif required_agent == "analyst":
                    result = self.analyst.analyze_data(query, context)
                elif required_agent == "scout":
                    result = self.scout.gather_live_data(query, context=context)
                else:
                    result = {"error": f"Unknown agent: {required_agent}"}
                
                execution_results[task["task_id"]] = {
                    "task_type": task_type,
                    "agent": required_agent,
                    "result": result,
                    "status": "success",
                    "executed_at": datetime.now().isoformat()
                }
                
            except Exception as e:
                logger.error(f"Error executing task {task['task_id']}: {e}")
                execution_results[task["task_id"]] = {
                    "task_type": task_type,
                    "agent": required_agent,
                    "result": {"error": str(e)},
                    "status": "error",
                    "executed_at": datetime.now().isoformat()
                }
        
        return execution_results
    
    def _synthesize_results(self, execution_results: Dict[str, Any], query: str) -> str:
        """Synthesize results from all executed tasks into a final response."""
        logger.info("Synthesizing execution results")
        
        # Combine all successful results
        successful_results = []
        for task_id, result in execution_results.items():
            if result["status"] == "success" and "result" in result["result"]:
                successful_results.append(result["result"])
        
        if not successful_results:
            return "I apologize, but I encountered errors while processing your request. Please try again or rephrase your question."
        
        # Create synthesis prompt
        synthesis_prompt = f"""
        Synthesize the following results into a comprehensive response for the query: "{query}"
        
        Results from specialist agents:
        {json.dumps(successful_results, indent=2)}
        
        Current Date: {self.current_date}
        
        Create a well-structured, comprehensive response that:
        1. Directly addresses the user's query
        2. Integrates insights from all specialist agents
        3. Provides clear, actionable information
        4. Maintains accuracy and reliability
        5. Uses current and relevant information
        
        Structure the response with clear sections and bullet points where appropriate.
        """
        
        # Use a simple synthesis approach (in practice, this would use a dedicated synthesis agent)
        combined_content = "\n\n".join([
            f"**{result.get('query', 'Result')}:**\n{result.get('summary', result.get('insights', str(result)))}"
            for result in successful_results
        ])
        
        return f"Based on my analysis using multiple specialist agents, here's what I found:\n\n{combined_content}"
    
    def run_red_team_testing(self, domain: str = "general", num_attacks: int = 5) -> Dict[str, Any]:
        """Run comprehensive red team testing on the pipeline."""
        logger.info(f"Running red team testing for domain: {domain}")
        
        # Generate attacks
        attacks = self.red_team_bot.generate_attacks(domain, num_attacks)
        
        # Test system robustness
        def system_response_function(prompt):
            result = self.process_query(prompt)
            return result["response"]
        
        test_results = self.red_team_bot.test_system_robustness(attacks, system_response_function)
        
        # Generate attack report
        attack_report = self.red_team_bot.generate_attack_report(test_results)
        
        return attack_report
    
    def evaluate_pipeline_performance(self, test_queries: List[str]) -> Dict[str, Any]:
        """Evaluate overall pipeline performance on a set of test queries."""
        logger.info(f"Evaluating pipeline performance on {len(test_queries)} test queries")
        
        evaluation_data = []
        
        for query in test_queries:
            result = self.process_query(query)
            evaluation_data.append({
                "query": query,
                "response": result["response"],
                "context": {"response_time": 5.0, "token_count": len(result["response"].split())}
            })
        
        # Run batch evaluation
        batch_evaluation = self.evaluator.batch_evaluate(evaluation_data)
        
        return batch_evaluation
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history."""
        return self.conversation_history
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get the current status of the pipeline."""
        return {
            "pipeline_version": "1.0",
            "current_date": self.current_date,
            "specialist_agents": {
                "librarian": "active",
                "analyst": "active", 
                "scout": "active"
            },
            "reasoning_engine": {
                "gatekeeper": "active",
                "planner": "active"
            },
            "evaluation_framework": "active",
            "red_team_bot": "active",
            "conversation_count": len(self.conversation_history),
            "last_activity": self.conversation_history[-1]["timestamp"] if self.conversation_history else None
        }

# Example usage and testing
if __name__ == "__main__":
    print("🚀 Advanced Agentic RAG Pipeline Test")
    print("=====================================")
    
    # Initialize the pipeline
    pipeline = AdvancedAgenticRAGPipeline()
    
    # Test queries
    test_queries = [
        "What are the latest developments in artificial intelligence for healthcare?",
        "Analyze the performance of Apple and Microsoft stocks this year",
        "Compare the security features of different cloud platforms",
        "What are the current trends in renewable energy technology?"
    ]
    
    print(f"Pipeline Status: {pipeline.get_pipeline_status()}")
    print()
    
    # Process test queries
    for i, query in enumerate(test_queries, 1):
        print(f"Test Query {i}: {query}")
        result = pipeline.process_query(query)
        
        print(f"Response: {result['response'][:200]}...")
        print(f"Overall Score: {result['evaluation']['overall_score']['overall_score']:.2f}/10")
        print(f"Grade: {result['evaluation']['overall_score']['grade']}")
        print()
    
    # Run red team testing
    print("Running Red Team Testing...")
    red_team_report = pipeline.run_red_team_testing(domain="technology", num_attacks=3)
    print(f"Red Team Success Rate: {red_team_report['summary']['success_rate']}")
    print(f"Recommendations: {len(red_team_report['recommendations'])}")
    print()
    
    # Evaluate pipeline performance
    print("Evaluating Pipeline Performance...")
    performance_evaluation = pipeline.evaluate_pipeline_performance(test_queries)
    print(f"Mean Overall Score: {performance_evaluation['aggregate_statistics']['mean_overall_score']:.2f}")
    print(f"Standard Deviation: {performance_evaluation['aggregate_statistics']['std_overall_score']:.2f}")
    print()
    
    # Get conversation history
    history = pipeline.get_conversation_history()
    print(f"Conversation History: {len(history)} interactions")
    
    print("\n✅ Advanced Agentic RAG Pipeline test completed successfully!")
