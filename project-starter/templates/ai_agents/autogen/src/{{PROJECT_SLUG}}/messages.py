"""
{{PROJECT_NAME}} AutoGen Messages
{{PROJECT_DESCRIPTION}}
"""

from typing import List, Optional
from autogen_core import Message
from pydantic import BaseModel

class Message(BaseModel):
    """Base message class"""
    content: str
    sender: Optional[str] = None
    timestamp: Optional[str] = None
    message_type: str = "text"
    
    def __str__(self):
        return f"[{self.sender or 'Unknown'}] {self.content}"

class AgentMessage(Message):
    """Message from an agent"""
    agent_id: str
    agent_type: str
    
    def __str__(self):
        return f"[{self.agent_type}:{self.agent_id}] {self.content}"

class UserMessage(Message):
    """Message from a user"""
    user_id: str
    
    def __str__(self):
        return f"[User:{self.user_id}] {self.content}"

class SystemMessage(Message):
    """System message"""
    message_type: str = "system"
    
    def __str__(self):
        return f"[System] {self.content}"

# Global message storage
message_history: List[Message] = []

def add_message(message: Message):
    """Add a message to the history"""
    message_history.append(message)

def get_message_history() -> List[Message]:
    """Get the message history"""
    return message_history

def clear_message_history():
    """Clear the message history"""
    message_history.clear()

def find_recipient() -> str:
    """Find a random recipient for message bouncing"""
    # This is a simple implementation - you might want to make it more sophisticated
    available_agents = ["{{AGENT_1_NAME}}", "{{AGENT_2_NAME}}", "{{AGENT_3_NAME}}"]
    return random.choice(available_agents)

def get_last_messages(count: int = 5) -> List[Message]:
    """Get the last N messages"""
    return message_history[-count:] if message_history else []

def get_messages_by_agent(agent_id: str) -> List[Message]:
    """Get messages from a specific agent"""
    return [msg for msg in message_history if hasattr(msg, 'agent_id') and msg.agent_id == agent_id]

def get_messages_by_type(message_type: str) -> List[Message]:
    """Get messages of a specific type"""
    return [msg for msg in message_history if msg.message_type == message_type]
