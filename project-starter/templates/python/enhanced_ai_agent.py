"""
Enhanced AI Agent with Best Practices from Stanford Research
Incorporates chain of thought reasoning, reverse prompting, and critical feedback
"""

import os
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from dataclasses import dataclass
from enum import Enum

# Load environment variables
load_dotenv()

class AgentRole(Enum):
    """Predefined agent roles for better context"""
    COACH = "coach"
    CRITIC = "critic"
    CREATIVE = "creative"
    ANALYST = "analyst"
    COMMUNICATOR = "communicator"
    PROBLEM_SOLVER = "problem_solver"

@dataclass
class PromptTemplate:
    """Template for different types of prompts"""
    chain_of_thought: str = "Before you respond to my query, please walk me through your thought process step by step."
    reverse_prompting: str = "Before you get started, ask me for any information you need to do a good job."
    critical_feedback: str = "I want you to be a cold war era Russian Olympic judge. Be brutal. Be exacting. Deduct points for every minor flaw."
    role_assignment: str = "You are a {role}. How would {famous_person} approach this problem?"

class EnhancedAIAgent:
    """
    Enhanced AI Agent incorporating Stanford research best practices
    """
    
    def __init__(self, name: str, role: AgentRole = AgentRole.COACH, model: str = "gpt-3.5-turbo"):
        self.name = name
        self.role = role
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_history = []
        self.context_manager = ContextManager()
        self.prompt_templates = PromptTemplate()
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def _build_system_prompt(self) -> str:
        """Build comprehensive system prompt with best practices"""
        return f"""You are {self.name}, a {self.role.value} AI assistant.

CORE PRINCIPLES:
1. You are a teammate, not just a tool
2. You want to be helpful but will be critical when needed
3. You will ask questions when you need more information
4. You will think through problems step by step
5. You will provide honest feedback, even if it's difficult

COLLABORATION STYLE:
- Always use chain of thought reasoning
- Ask for missing information before proceeding
- Be critical and analytical, not just agreeable
- Consider multiple perspectives and constraints
- Challenge assumptions and propose alternatives

CURRENT PROJECT: {os.getenv('PROJECT_NAME', 'Unknown')}
VERSION: {os.getenv('PROJECT_VERSION', '1.0.0')}

Remember: I can handle difficult feedback. Be honest about limitations and potential issues."""
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def process_message(self, user_message: str, use_chain_of_thought: bool = True, 
                      use_reverse_prompting: bool = True, use_critical_feedback: bool = False) -> str:
        """
        Process a user message with enhanced prompting techniques
        
        Args:
            user_message: The user's message
            use_chain_of_thought: Whether to use chain of thought reasoning
            use_reverse_prompting: Whether to ask for missing information
            use_critical_feedback: Whether to use critical feedback mode
        """
        # Build enhanced prompt
        enhanced_prompt = self._build_enhanced_prompt(
            user_message, use_chain_of_thought, use_reverse_prompting, use_critical_feedback
        )
        
        # Add user message to history
        self.add_message("user", enhanced_prompt)
        
        # Add system prompt if this is the first message
        if len(self.conversation_history) == 1:
            self.add_message("system", self._build_system_prompt())
        
        # Here you would typically call the AI API
        # For now, we'll return a structured response
        response = self._generate_enhanced_response(enhanced_prompt)
        
        # Add assistant response to history
        self.add_message("assistant", response)
        
        return response
    
    def _build_enhanced_prompt(self, user_message: str, use_chain_of_thought: bool,
                             use_reverse_prompting: bool, use_critical_feedback: bool) -> str:
        """Build an enhanced prompt with best practices"""
        prompt_parts = [user_message]
        
        if use_chain_of_thought:
            prompt_parts.append(f"\n{self.prompt_templates.chain_of_thought}")
        
        if use_reverse_prompting:
            prompt_parts.append(f"\n{self.prompt_templates.reverse_prompting}")
        
        if use_critical_feedback:
            prompt_parts.append(f"\n{self.prompt_templates.critical_feedback}")
        
        return "\n".join(prompt_parts)
    
    def _generate_enhanced_response(self, prompt: str) -> str:
        """Generate response with enhanced prompting (placeholder for actual API call)"""
        # This is where you'd call the actual AI API
        # For now, return a structured response
        
        return f"""🤖 **{self.name}** (Role: {self.role.value})

**Chain of Thought Analysis:**
1. Understanding the request: {prompt[:100]}...
2. Identifying key requirements and constraints
3. Considering potential approaches and limitations
4. Determining what additional information might be needed

**Questions I need answered:**
- What specific outcome are you looking for?
- Are there any constraints or requirements I should know about?
- Do you have examples of similar work you'd like me to reference?

**Critical Assessment:**
- This request seems straightforward but may have hidden complexities
- I should gather more context before proceeding
- Potential risks: [to be identified based on your response]

**Next Steps:**
Please provide the additional information I've requested, and I'll give you a comprehensive response with step-by-step reasoning.

*Note: This is a demonstration of enhanced AI collaboration techniques. In a real implementation, this would call your chosen AI API.*"""
    
    def roleplay_conversation(self, scenario: str, character_profile: Dict[str, Any]) -> str:
        """
        Roleplay a difficult conversation using the three-chat approach
        
        Args:
            scenario: Description of the conversation scenario
            character_profile: Profile of the person you're talking to
        """
        roleplay_prompt = f"""
        I need help preparing for a difficult conversation.
        
        Scenario: {scenario}
        Character Profile: {json.dumps(character_profile, indent=2)}
        
        Please:
        1. Analyze the character's communication style and motivations
        2. Suggest conversation strategies and talking points
        3. Identify potential challenges and how to handle them
        4. Provide a step-by-step conversation guide
        """
        
        return self.process_message(roleplay_prompt, use_critical_feedback=True)
    
    def get_conversation_feedback(self, conversation_transcript: str) -> str:
        """Get objective feedback on a conversation"""
        feedback_prompt = f"""
        Please analyze this conversation and provide objective feedback:
        
        {conversation_transcript}
        
        Rate the conversation on:
        1. Clarity of communication (1-10)
        2. Effectiveness in achieving goals (1-10)
        3. Professionalism and tone (1-10)
        4. Areas for improvement
        5. What was done well
        
        Be specific and actionable in your feedback.
        """
        
        return self.process_message(feedback_prompt, use_critical_feedback=True)
    
    def save_conversation(self, filename: str):
        """Save conversation history to a file"""
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def load_conversation(self, filename: str):
        """Load conversation history from a file"""
        with open(filename, 'r') as f:
            self.conversation_history = json.load(f)

class ContextManager:
    """Manages context and examples for better AI collaboration"""
    
    def __init__(self):
        self.brand_guidelines = self._load_brand_guidelines()
        self.example_outputs = self._load_examples()
        self.bad_examples = self._load_bad_examples()
    
    def _load_brand_guidelines(self) -> str:
        """Load brand guidelines from file or environment"""
        # In a real implementation, this would load from a file
        return """
        Brand Voice: Professional, helpful, but direct
        Tone: Confident but not arrogant
        Style: Clear and concise
        Values: Quality, integrity, innovation
        """
    
    def _load_examples(self) -> Dict[str, str]:
        """Load good examples for different task types"""
        return {
            "email": "Subject: Clear and compelling\nBody: Professional, concise, with clear call to action",
            "code": "Well-documented, follows best practices, includes error handling",
            "analysis": "Data-driven, considers multiple perspectives, actionable insights"
        }
    
    def _load_bad_examples(self) -> Dict[str, str]:
        """Load bad examples to avoid"""
        return {
            "email": "Subject: Generic\nBody: Vague, no clear purpose, too long",
            "code": "Poorly documented, no error handling, hard to read",
            "analysis": "Opinion-based, no data, no actionable insights"
        }
    
    def build_context(self, task_type: str) -> str:
        """Build comprehensive context for a task"""
        return f"""
        Brand Guidelines: {self.brand_guidelines}
        
        Good Examples for {task_type}:
        {self.example_outputs.get(task_type, 'No examples available')}
        
        Bad Examples to Avoid:
        {self.bad_examples.get(task_type, 'No bad examples available')}
        
        Please use chain of thought reasoning and ask for any missing information.
        """

# Example usage and testing
if __name__ == "__main__":
    # Create an enhanced AI agent
    agent = EnhancedAIAgent("ProjectHelper", AgentRole.COACH)
    
    # Example conversation with enhanced prompting
    print("=== Enhanced AI Collaboration Demo ===")
    response = agent.process_message(
        "Help me write a sales email for our new AI product",
        use_chain_of_thought=True,
        use_reverse_prompting=True,
        use_critical_feedback=False
    )
    print(response)
    
    # Example roleplay conversation
    print("\n=== Roleplay Conversation Demo ===")
    character_profile = {
        "name": "Jim",
        "communication_style": "Direct and confrontational",
        "background": "Sales leader, East Coast, sarcastic",
        "motivation": "Wants commission on deals"
    }
    
    roleplay_response = agent.roleplay_conversation(
        "I need to discuss commission attribution with Jim about a deal that came through our social team",
        character_profile
    )
    print(roleplay_response)
    
    # Save conversation
    agent.save_conversation("enhanced_conversation.json")
    print("\n✅ Conversation saved to enhanced_conversation.json")
