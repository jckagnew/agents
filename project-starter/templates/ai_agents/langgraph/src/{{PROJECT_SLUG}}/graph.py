"""
{{PROJECT_NAME}} LangGraph Implementation
{{PROJECT_DESCRIPTION}}
"""

from typing import Annotated, TypedDict, List, Any, Optional, Dict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uuid
import asyncio
from datetime import datetime

# Load environment variables
load_dotenv()

class State(TypedDict):
    """State definition for the graph"""
    messages: Annotated[List[Any], add_messages]
    success_criteria: str
    feedback_on_work: Optional[str]
    success_criteria_met: bool
    user_input_needed: bool
    current_task: Optional[str]
    task_results: Dict[str, Any]
    iteration_count: int
    max_iterations: int

class EvaluatorOutput(BaseModel):
    """Output from the evaluator agent"""
    feedback: str = Field(description="Feedback on the assistant's response")
    success_criteria_met: bool = Field(description="Whether the success criteria have been met")
    user_input_needed: bool = Field(
        description="True if more input is needed from the user, or clarifications, or the assistant is stuck"
    )

class {{PROJECT_NAME}}Graph:
    """Main LangGraph implementation for {{PROJECT_NAME}}"""
    
    def __init__(self):
        self.worker_llm = None
        self.evaluator_llm = None
        self.tools = []
        self.graph = None
        self.session_id = str(uuid.uuid4())
        self.memory = None
        
    async def setup(self):
        """Setup the graph with LLMs and tools"""
        # Initialize LLMs
        self.worker_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.evaluator_llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize tools
        self.tools = await self._get_tools()
        
        # Create the graph
        self._create_graph()
    
    async def _get_tools(self) -> List[Any]:
        """Get tools for the graph"""
        # This is a placeholder - implement actual tool creation
        # based on your specific needs
        tools = []
        
        # Add web search tool
        # Add file operations tool
        # Add code analysis tool
        # Add custom tools
        
        return tools
    
    def _create_graph(self):
        """Create the LangGraph workflow"""
        # Create the state graph
        workflow = StateGraph(State)
        
        # Add nodes
        workflow.add_node("worker", self._worker_node)
        workflow.add_node("evaluator", self._evaluator_node)
        workflow.add_node("tools", ToolNode(self.tools))
        
        # Add edges
        workflow.add_edge(START, "worker")
        workflow.add_edge("worker", "tools")
        workflow.add_edge("tools", "evaluator")
        workflow.add_conditional_edges(
            "evaluator",
            self._should_continue,
            {
                "continue": "worker",
                "end": END
            }
        )
        
        # Compile the graph
        self.graph = workflow.compile()
    
    async def _worker_node(self, state: State) -> State:
        """Worker node that processes tasks"""
        messages = state["messages"]
        current_task = state.get("current_task", "No specific task")
        
        # Create system message
        system_message = SystemMessage(content=f"""
        You are a {{AGENT_ROLE}} working on: {current_task}
        
        Your goal: {{AGENT_GOAL}}
        
        Success criteria: {state.get('success_criteria', 'Complete the task successfully')}
        
        Previous feedback: {state.get('feedback_on_work', 'No previous feedback')}
        
        Iteration: {state.get('iteration_count', 0)}/{state.get('max_iterations', 10)}
        """)
        
        # Add system message to the beginning
        messages_with_system = [system_message] + messages
        
        # Get response from worker LLM
        response = await self.worker_llm.ainvoke(messages_with_system)
        
        # Update state
        state["messages"] = messages + [response]
        state["iteration_count"] = state.get("iteration_count", 0) + 1
        
        return state
    
    async def _evaluator_node(self, state: State) -> State:
        """Evaluator node that assesses the work"""
        messages = state["messages"]
        success_criteria = state.get("success_criteria", "Complete the task successfully")
        
        # Create evaluation prompt
        evaluation_prompt = f"""
        Evaluate the assistant's work based on the following criteria:
        
        Success Criteria: {success_criteria}
        
        Recent Messages:
        {messages[-3:] if len(messages) >= 3 else messages}
        
        Provide feedback on:
        1. Quality of the work
        2. Whether success criteria are met
        3. If more user input is needed
        4. Suggestions for improvement
        
        Respond in JSON format:
        {{
            "feedback": "Your feedback here",
            "success_criteria_met": true/false,
            "user_input_needed": true/false
        }}
        """
        
        # Get evaluation from evaluator LLM
        evaluation_response = await self.evaluator_llm.ainvoke([HumanMessage(content=evaluation_prompt)])
        
        # Parse evaluation
        try:
            import json
            evaluation = json.loads(evaluation_response.content)
            state["feedback_on_work"] = evaluation["feedback"]
            state["success_criteria_met"] = evaluation["success_criteria_met"]
            state["user_input_needed"] = evaluation["user_input_needed"]
        except:
            # Fallback if JSON parsing fails
            state["feedback_on_work"] = evaluation_response.content
            state["success_criteria_met"] = False
            state["user_input_needed"] = True
        
        return state
    
    def _should_continue(self, state: State) -> str:
        """Determine whether to continue or end"""
        if state.get("success_criteria_met", False):
            return "end"
        
        if state.get("iteration_count", 0) >= state.get("max_iterations", 10):
            return "end"
        
        if state.get("user_input_needed", False):
            return "end"
        
        return "continue"
    
    async def run(self, inputs: Dict[str, Any] = None) -> str:
        """Run the graph with given inputs"""
        if not self.graph:
            await self.setup()
        
        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content=inputs.get("query", "Hello"))],
            "success_criteria": inputs.get("success_criteria", "Complete the task successfully"),
            "feedback_on_work": None,
            "success_criteria_met": False,
            "user_input_needed": False,
            "current_task": inputs.get("task", "General assistance"),
            "task_results": {},
            "iteration_count": 0,
            "max_iterations": inputs.get("max_iterations", 10)
        }
        
        # Run the graph
        result = await self.graph.ainvoke(initial_state)
        
        return result
    
    async def train(self, training_data: Dict[str, Any] = None) -> str:
        """Train the graph with training data"""
        # Implement training logic here
        return "Training completed"
    
    async def replay(self, session_id: str) -> str:
        """Replay a previous graph execution"""
        # Implement replay logic here
        return f"Replaying session: {session_id}"
    
    async def test(self, test_inputs: Dict[str, Any] = None) -> str:
        """Test the graph with test inputs"""
        # Implement testing logic here
        return "Testing completed"
