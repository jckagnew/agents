"""
{{PROJECT_NAME}} CrewAI Implementation
{{PROJECT_DESCRIPTION}}
"""

import os
import yaml
from typing import List, Dict, Any
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

class {{PROJECT_NAME}}Crew:
    """Main CrewAI crew for {{PROJECT_NAME}}"""
    
    def __init__(self):
        self.agents = []
        self.tasks = []
        self.crew = None
        self._load_config()
        self._create_agents()
        self._create_tasks()
        self._create_crew()
    
    def _load_config(self):
        """Load configuration from YAML files"""
        config_dir = os.path.join(os.path.dirname(__file__), 'config')
        
        # Load agents configuration
        with open(os.path.join(config_dir, 'agents.yaml'), 'r') as f:
            self.agents_config = yaml.safe_load(f)
        
        # Load tasks configuration
        with open(os.path.join(config_dir, 'tasks.yaml'), 'r') as f:
            self.tasks_config = yaml.safe_load(f)
    
    def _get_llm(self, provider: str, model: str, temperature: float = 0.7, max_tokens: int = 2000):
        """Get LLM instance based on provider"""
        if provider == "openai":
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "anthropic":
            return ChatAnthropic(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        elif provider == "google":
            return ChatGoogleGenerativeAI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=os.getenv("GOOGLE_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def _create_agents(self):
        """Create agents from configuration"""
        for agent_config in self.agents_config['agents']:
            llm = self._get_llm(
                provider=agent_config['llm']['provider'],
                model=agent_config['llm']['model'],
                temperature=agent_config['llm']['temperature'],
                max_tokens=agent_config['llm']['max_tokens']
            )
            
            agent = Agent(
                name=agent_config['name'],
                role=agent_config['role'],
                goal=agent_config['goal'],
                backstory=agent_config['backstory'],
                llm=llm,
                tools=self._get_tools(agent_config.get('tools', [])),
                verbose=agent_config.get('verbose', True),
                allow_delegation=agent_config.get('allow_delegation', False)
            )
            
            self.agents.append(agent)
    
    def _get_tools(self, tool_names: List[str]) -> List[BaseTool]:
        """Get tools based on names"""
        # This is a placeholder - implement actual tool creation
        # based on your specific needs
        tools = []
        
        for tool_name in tool_names:
            if tool_name == "web_search":
                # Add web search tool
                pass
            elif tool_name == "file_operations":
                # Add file operations tool
                pass
            elif tool_name == "code_analysis":
                # Add code analysis tool
                pass
        
        return tools
    
    def _create_tasks(self):
        """Create tasks from configuration"""
        for task_config in self.tasks_config['tasks']:
            # Find the agent for this task
            agent = next(
                (a for a in self.agents if a.name == task_config['agent']),
                None
            )
            
            if not agent:
                raise ValueError(f"Agent {task_config['agent']} not found")
            
            task = Task(
                name=task_config['name'],
                description=task_config['description'],
                expected_output=task_config['expected_output'],
                agent=agent,
                context=task_config.get('context', []),
                async_execution=task_config.get('async_execution', False),
                tools=self._get_tools(task_config.get('tools', [])),
                dependencies=task_config.get('dependencies', [])
            )
            
            self.tasks.append(task)
    
    def _create_crew(self):
        """Create the crew with agents and tasks"""
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  # or Process.hierarchical
            verbose=True,
            memory=True,
            planning=True,
            max_iterations=self.agents_config['global_config']['max_iterations'],
            max_execution_time=self.agents_config['global_config']['max_execution_time']
        )
    
    def run(self, inputs: Dict[str, Any] = None) -> str:
        """Run the crew with given inputs"""
        if not self.crew:
            raise RuntimeError("Crew not initialized")
        
        result = self.crew.kickoff(inputs=inputs)
        return result
    
    def train(self, training_data: Dict[str, Any] = None) -> str:
        """Train the crew with training data"""
        # Implement training logic here
        return "Training completed"
    
    def replay(self, session_id: str) -> str:
        """Replay a previous crew execution"""
        # Implement replay logic here
        return f"Replaying session: {session_id}"
    
    def test(self, test_inputs: Dict[str, Any] = None) -> str:
        """Test the crew with test inputs"""
        # Implement testing logic here
        return "Testing completed"
