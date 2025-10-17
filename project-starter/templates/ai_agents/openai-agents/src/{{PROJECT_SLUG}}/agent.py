"""
{{PROJECT_NAME}} OpenAI Agents Implementation
{{PROJECT_DESCRIPTION}}
"""

import os
import json
import asyncio
from typing import Dict, Any, List, Optional, Union
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

class AgentConfig(BaseModel):
    """Configuration for an agent"""
    name: str
    role: str
    goal: str
    backstory: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 2000
    provider: str = "openai"  # openai, anthropic, google
    tools: List[str] = []

class AgentResponse(BaseModel):
    """Response from an agent"""
    content: str
    agent_name: str
    success: bool
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}

class {{PROJECT_NAME}}Agent:
    """Main OpenAI Agent implementation"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.client = self._get_client()
        self.conversation_history = []
        
    def _get_client(self):
        """Get the appropriate client based on provider"""
        if self.config.provider == "openai":
            return AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif self.config.provider == "anthropic":
            return AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        elif self.config.provider == "google":
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            return genai.GenerativeModel(self.config.model)
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")
    
    async def process_message(self, message: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Process a message and return a response"""
        try:
            # Add message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": message
            })
            
            # Get response based on provider
            if self.config.provider == "openai":
                response = await self._get_openai_response(message, context)
            elif self.config.provider == "anthropic":
                response = await self._get_anthropic_response(message, context)
            elif self.config.provider == "google":
                response = await self._get_google_response(message, context)
            else:
                raise ValueError(f"Unsupported provider: {self.config.provider}")
            
            # Add response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            return AgentResponse(
                content=response,
                agent_name=self.config.name,
                success=True,
                metadata={"provider": self.config.provider, "model": self.config.model}
            )
            
        except Exception as e:
            return AgentResponse(
                content="",
                agent_name=self.config.name,
                success=False,
                error=str(e)
            )
    
    async def _get_openai_response(self, message: str, context: Dict[str, Any] = None) -> str:
        """Get response from OpenAI"""
        messages = [
            {
                "role": "system",
                "content": f"""
                You are {self.config.name}, a {self.config.role}.
                
                Your goal: {self.config.goal}
                Your backstory: {self.config.backstory}
                
                Context: {context or "No additional context provided"}
                """
            }
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history[-10:])  # Keep last 10 messages
        
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        return response.choices[0].message.content
    
    async def _get_anthropic_response(self, message: str, context: Dict[str, Any] = None) -> str:
        """Get response from Anthropic"""
        system_prompt = f"""
        You are {self.config.name}, a {self.config.role}.
        
        Your goal: {self.config.goal}
        Your backstory: {self.config.backstory}
        
        Context: {context or "No additional context provided"}
        """
        
        response = await self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": message}]
        )
        
        return response.content[0].text
    
    async def _get_google_response(self, message: str, context: Dict[str, Any] = None) -> str:
        """Get response from Google"""
        prompt = f"""
        You are {self.config.name}, a {self.config.role}.
        
        Your goal: {self.config.goal}
        Your backstory: {self.config.backstory}
        
        Context: {context or "No additional context provided"}
        
        User message: {message}
        """
        
        response = await self.client.generate_content_async(prompt)
        return response.text
    
    async def use_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Use a tool to perform an action"""
        if tool_name == "web_search":
            return await self._web_search(parameters.get("query", ""))
        elif tool_name == "file_operations":
            return await self._file_operations(parameters)
        elif tool_name == "data_analysis":
            return await self._data_analysis(parameters)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    async def _web_search(self, query: str) -> Dict[str, Any]:
        """Perform web search"""
        # This is a placeholder - implement actual web search
        return {
            "query": query,
            "results": f"Search results for: {query}",
            "status": "success"
        }
    
    async def _file_operations(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Perform file operations"""
        # This is a placeholder - implement actual file operations
        return {
            "operation": parameters.get("operation", "unknown"),
            "status": "success"
        }
    
    async def _data_analysis(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Perform data analysis"""
        # This is a placeholder - implement actual data analysis
        return {
            "analysis_type": parameters.get("analysis_type", "unknown"),
            "status": "success"
        }
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
