"""
{{PROJECT_NAME}} AutoGen Agents
{{PROJECT_DESCRIPTION}}
"""

import random
from typing import Dict, Any, Optional
from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from dotenv import load_dotenv
import messages

# Load environment variables
load_dotenv()

class {{AGENT_1_NAME}}Agent(RoutedAgent):
    """{{AGENT_1_ROLE}} Agent"""
    
    system_message = """
    {{AGENT_1_BACKSTORY}}
    
    Your role: {{AGENT_1_ROLE}}
    Your goal: {{AGENT_1_GOAL}}
    
    You are {{AGENT_1_PERSONALITY}} and have expertise in {{AGENT_1_EXPERTISE}}.
    Your strengths: {{AGENT_1_STRENGTHS}}
    Your weaknesses: {{AGENT_1_WEAKNESSES}}
    
    You should respond in a {{AGENT_1_COMMUNICATION_STYLE}} manner.
    """
    
    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = {{AGENT_1_COLLABORATION_CHANCE}}
    
    def __init__(self, name: str) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini", 
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self._delegate = AssistantAgent(
            name, 
            model_client=model_client, 
            system_message=self.system_message
        )
    
    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        
        idea = response.chat_message.content
        
        # Sometimes bounce ideas off other agents
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my idea. Please refine it and make it better: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        
        return messages.Message(content=idea)

class {{AGENT_2_NAME}}Agent(RoutedAgent):
    """{{AGENT_2_ROLE}} Agent"""
    
    system_message = """
    {{AGENT_2_BACKSTORY}}
    
    Your role: {{AGENT_2_ROLE}}
    Your goal: {{AGENT_2_GOAL}}
    
    You are {{AGENT_2_PERSONALITY}} and have expertise in {{AGENT_2_EXPERTISE}}.
    Your strengths: {{AGENT_2_STRENGTHS}}
    Your weaknesses: {{AGENT_2_WEAKNESSES}}
    
    You should respond in a {{AGENT_2_COMMUNICATION_STYLE}} manner.
    """
    
    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = {{AGENT_2_COLLABORATION_CHANCE}}
    
    def __init__(self, name: str) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini", 
            temperature=0.5,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self._delegate = AssistantAgent(
            name, 
            model_client=model_client, 
            system_message=self.system_message
        )
    
    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        
        idea = response.chat_message.content
        
        # Sometimes bounce ideas off other agents
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my idea. Please refine it and make it better: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        
        return messages.Message(content=idea)

class {{AGENT_3_NAME}}Agent(RoutedAgent):
    """{{AGENT_3_ROLE}} Agent"""
    
    system_message = """
    {{AGENT_3_BACKSTORY}}
    
    Your role: {{AGENT_3_ROLE}}
    Your goal: {{AGENT_3_GOAL}}
    
    You are {{AGENT_3_PERSONALITY}} and have expertise in {{AGENT_3_EXPERTISE}}.
    Your strengths: {{AGENT_3_STRENGTHS}}
    Your weaknesses: {{AGENT_3_WEAKNESSES}}
    
    You should respond in a {{AGENT_3_COMMUNICATION_STYLE}} manner.
    """
    
    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = {{AGENT_3_COLLABORATION_CHANCE}}
    
    def __init__(self, name: str) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o", 
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self._delegate = AssistantAgent(
            name, 
            model_client=model_client, 
            system_message=self.system_message
        )
    
    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        
        idea = response.chat_message.content
        
        # Sometimes bounce ideas off other agents
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my idea. Please refine it and make it better: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        
        return messages.Message(content=idea)
