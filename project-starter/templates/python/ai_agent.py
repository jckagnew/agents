"""
AI Agent Template
"""

import os
from dotenv import load_dotenv
from typing import Dict, List, Optional
import json

# Load environment variables
load_dotenv()

class AIAgent:
    """Base AI Agent class with common functionality"""
    
    def __init__(self, name: str, model: str = "gpt-3.5-turbo"):
        self.name = name
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_history = []
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        return f"""You are {self.name}, an AI assistant created from the project-starter template.
        
Your capabilities:
- Answer questions and provide helpful information
- Assist with coding and development tasks
- Help with problem-solving and analysis
- Maintain a professional and helpful tone

Current project: {os.getenv('PROJECT_NAME', 'Unknown')}
Version: {os.getenv('PROJECT_VERSION', '1.0.0')}"""
    
    def process_message(self, user_message: str) -> str:
        """Process a user message and return a response"""
        # Add user message to history
        self.add_message("user", user_message)
        
        # Add system prompt if this is the first message
        if len(self.conversation_history) == 1:
            self.add_message("system", self.get_system_prompt())
        
        # Here you would typically call the AI API
        # For now, we'll return a placeholder response
        response = f"Hello! I'm {self.name}. I received your message: '{user_message}'. How can I help you today?"
        
        # Add assistant response to history
        self.add_message("assistant", response)
        
        return response
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
    
    def save_conversation(self, filename: str):
        """Save conversation history to a file"""
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def load_conversation(self, filename: str):
        """Load conversation history from a file"""
        with open(filename, 'r') as f:
            self.conversation_history = json.load(f)

# Example usage
if __name__ == "__main__":
    # Create an AI agent
    agent = AIAgent("ProjectHelper", "gpt-3.5-turbo")
    
    # Example conversation
    print(agent.process_message("Hello! What can you help me with?"))
    print(agent.process_message("Can you help me with Python coding?"))
    
    # Save conversation
    agent.save_conversation("conversation.json")
    print("Conversation saved to conversation.json")
