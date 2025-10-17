#!/usr/bin/env python3
"""
Enhanced Search Agent with Date Management
Integrates current date awareness into web search queries for more accurate results
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from date_manager import get_formatted_date, get_current_datetime

class EnhancedSearchAgent:
    """Enhanced search agent with date-aware query construction"""
    
    def __init__(self):
        self.current_date = get_formatted_date('standard')
        self.current_year = get_formatted_date('iso')[:4]
        self.current_month = get_formatted_date('iso')[5:7]
        self.current_day = get_formatted_date('iso')[8:10]
    
    def enhance_search_query(self, base_query: str, include_date_context: bool = True) -> str:
        """
        Enhance a search query with current date context for more accurate results
        
        Args:
            base_query: The original search query
            include_date_context: Whether to add date-specific terms
            
        Returns:
            Enhanced query with date context
        """
        if not include_date_context:
            return base_query
        
        # Add current date context to the query
        date_context = f" {self.current_year} latest recent current"
        
        # Add time-specific terms for better results
        time_terms = [
            "latest news",
            "recent developments", 
            "current status",
            f"as of {self.current_date}",
            "2024 2025"
        ]
        
        # Construct enhanced query
        enhanced_query = f"{base_query} {' '.join(time_terms)}{date_context}"
        
        return enhanced_query.strip()
    
    def get_date_aware_instructions(self, base_instructions: str) -> str:
        """
        Enhance agent instructions with date awareness
        
        Args:
            base_instructions: Original agent instructions
            
        Returns:
            Enhanced instructions with date context
        """
        date_context = f"""
        
IMPORTANT DATE CONTEXT:
- Current Date: {self.current_date}
- Current Year: {self.current_year}
- Search for the most recent information available
- Prioritize data from {self.current_year} and recent months
- Include terms like "latest", "recent", "current", "{self.current_year}" in searches
- Avoid outdated information from previous years unless specifically requested
"""
        
        return base_instructions + date_context
    
    def create_search_prompt(self, query: str, reason: str = None) -> str:
        """
        Create a comprehensive search prompt with date awareness
        
        Args:
            query: The search query
            reason: Reason for the search
            
        Returns:
            Enhanced search prompt
        """
        enhanced_query = self.enhance_search_query(query)
        
        prompt_parts = [
            f"Search Query: {enhanced_query}",
            f"Current Date: {self.current_date}",
            f"Focus on: Latest information from {self.current_year}"
        ]
        
        if reason:
            prompt_parts.append(f"Search Reason: {reason}")
        
        prompt_parts.extend([
            "",
            "Instructions:",
            "- Search for the most recent and current information",
            f"- Prioritize results from {self.current_year}",
            "- Include recent news, updates, and developments",
            "- Avoid outdated information unless specifically relevant"
        ])
        
        return "\n".join(prompt_parts)

def create_date_aware_search_agent():
    """Create a search agent with enhanced date awareness"""
    from agents import Agent, WebSearchTool, ModelSettings
    
    enhanced_agent = EnhancedSearchAgent()
    
    base_instructions = (
        "You are a research assistant. Given a search term, you search the web for that term and "
        "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
        "words. Capture the main points. Write succinctly, no need to have complete sentences or good "
        "grammar. This will be consumed by someone synthesizing a report, so it's vital you capture the "
        "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
    )
    
    enhanced_instructions = enhanced_agent.get_date_aware_instructions(base_instructions)
    
    return Agent(
        name="Date-Aware Search Agent",
        instructions=enhanced_instructions,
        tools=[WebSearchTool(search_context_size="medium")],
        model="gpt-4o-mini",
        model_settings=ModelSettings(tool_choice="required"),
    )

def create_financial_research_agent():
    """Create a financial research agent with date awareness"""
    from agents import Agent, WebSearchTool, ModelSettings
    
    enhanced_agent = EnhancedSearchAgent()
    
    base_instructions = (
        "You are a senior financial researcher. Research companies, markets, and financial topics "
        "with focus on current data and recent developments. Provide comprehensive analysis of "
        "financial information, market trends, and company performance."
    )
    
    enhanced_instructions = enhanced_agent.get_date_aware_instructions(base_instructions)
    
    return Agent(
        name="Date-Aware Financial Research Agent",
        instructions=enhanced_instructions,
        tools=[WebSearchTool(search_context_size="high")],
        model="gpt-4o",
        model_settings=ModelSettings(tool_choice="required"),
    )

def create_job_search_agent():
    """Create a job search agent with date awareness"""
    from agents import Agent, WebSearchTool, ModelSettings
    
    enhanced_agent = EnhancedSearchAgent()
    
    base_instructions = (
        "You are a specialized job search research assistant. Search for current job opportunities "
        "and produce detailed summaries of the results. Focus on finding specific job postings, "
        "company information, and relevant details that would help a candidate evaluate opportunities."
    )
    
    enhanced_instructions = enhanced_agent.get_date_aware_instructions(base_instructions)
    
    return Agent(
        name="Date-Aware Job Search Agent",
        instructions=enhanced_instructions,
        tools=[WebSearchTool(search_context_size="medium")],
        model="gpt-4o",
        model_settings=ModelSettings(tool_choice="required"),
    )

# Example usage and testing
if __name__ == "__main__":
    print("🔍 Enhanced Search Agent Test")
    print("=" * 50)
    
    enhanced_agent = EnhancedSearchAgent()
    
    # Test query enhancement
    test_queries = [
        "Apple stock performance",
        "AI job opportunities",
        "Tesla financial results",
        "cryptocurrency market trends"
    ]
    
    print(f"Current Date: {enhanced_agent.current_date}")
    print(f"Current Year: {enhanced_agent.current_year}")
    print()
    
    for query in test_queries:
        enhanced = enhanced_agent.enhance_search_query(query)
        print(f"Original: {query}")
        print(f"Enhanced: {enhanced}")
        print()
    
    # Test search prompt creation
    prompt = enhanced_agent.create_search_prompt(
        "OpenAI latest developments",
        "Research for AI industry report"
    )
    
    print("Sample Search Prompt:")
    print("-" * 30)
    print(prompt)
