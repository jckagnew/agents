#!/usr/bin/env python3
"""
Enhanced Date Search Agent
Integrates date math capabilities with search agents for intelligent date handling
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from date_math_manager import DateMathManager, enhance_search_query_with_dates
from smart_date_manager import SmartDateManager
from date_manager import get_formatted_date, get_current_datetime

class EnhancedDateSearchAgent:
    """Enhanced search agent with advanced date math capabilities"""
    
    def __init__(self):
        self.date_math_manager = DateMathManager()
        self.smart_date_manager = SmartDateManager()
        self.current_date = get_formatted_date('standard')
        self.current_year = get_formatted_date('iso')[:4]
    
    def enhance_search_query(self, query: str, search_type: str = "general") -> tuple:
        """
        Enhance a search query with both date math and smart date context
        
        Args:
            query: Original search query
            search_type: Type of search (general, job, financial, etc.)
            
        Returns:
            Tuple of (enhanced_query, date_info_list, search_terms)
        """
        # First, enhance with date math for relative expressions
        enhanced_query, date_info_list = self.date_math_manager.enhance_search_query_with_date_math(query)
        
        # Then, add general date context using search query enhancer
        from search_query_enhancer import enhance_search_query
        base_enhanced = enhance_search_query(enhanced_query, search_type)
        
        # Combine search terms from both enhancements
        all_search_terms = []
        for date_info in date_info_list:
            all_search_terms.extend(date_info.get('search_terms', []))
        
        # Add current date context
        all_search_terms.extend([
            self.current_year,
            "latest",
            "recent",
            "current"
        ])
        
        # Create final enhanced query
        final_query = f"{base_enhanced} {' '.join(set(all_search_terms))}"
        
        return final_query, date_info_list, all_search_terms
    
    def create_date_aware_search_instructions(self, base_instructions: str, search_type: str = "general") -> str:
        """
        Create search agent instructions with advanced date awareness
        
        Args:
            base_instructions: Base instructions for the agent
            search_type: Type of search
            
        Returns:
            Enhanced instructions with date math capabilities
        """
        date_context = f"""
        
ADVANCED DATE AWARENESS INSTRUCTIONS:
- Current Date: {self.current_date}
- Current Year: {self.current_year}
- Current Quarter: Q{self.date_math_manager.get_current_quarter()}

RELATIVE DATE EXPRESSIONS SUPPORTED:
- Time periods: "this year", "last year", "this month", "last month", "this week", "last week"
- Quarters: "this quarter", "last quarter", "Q1", "Q2", "Q3", "Q4"
- Relative periods: "last 2 weeks", "last 3 months", "last 6 months"
- Recent terms: "recent", "latest", "current", "today", "yesterday"

SEARCH ENHANCEMENT RULES:
- When you see relative date expressions, automatically expand them with specific date ranges
- For "this year" searches, prioritize 2025 data and include "2025", "this year", "current year"
- For "last quarter" searches, include "Q2 2025", "last quarter", "previous quarter"
- For "recent" searches, focus on last 30 days and include "recent", "latest", "current"
- Always include current year ({self.current_year}) in search terms
- Prioritize the most recent information available
- Avoid outdated information from previous years unless specifically requested

SEARCH TYPE: {search_type}
- Focus on the most current and relevant information for this search type
- Use appropriate date ranges based on the search context
- Include both specific dates and relative time periods in search terms
"""
        
        return base_instructions + date_context
    
    def create_smart_writing_instructions_with_dates(self, base_instructions: str, context: str = "general") -> str:
        """
        Create writing agent instructions with both smart dates and date math
        
        Args:
            base_instructions: Base instructions for the agent
            context: Context type (cover_letter, email, report, etc.)
            
        Returns:
            Enhanced instructions with advanced date capabilities
        """
        # Get smart date instructions
        smart_instructions = self.smart_date_manager.create_date_aware_instructions(base_instructions, context)
        
        # Add date math capabilities
        date_math_context = f"""
        
DATE MATH CAPABILITIES:
- Support relative date expressions: "this year", "last quarter", "recent", etc.
- Automatically calculate date ranges for relative expressions
- Use specific dates when appropriate, relative dates when more natural
- Examples:
  * "this year" → "2025" or "this year (2025)"
  * "last quarter" → "Q2 2025" or "last quarter (Q2 2025)"
  * "recent" → "recent (last 30 days)" or "recent developments"
  * "this month" → "September 2025" or "this month (September 2025)"

RELATIVE DATE EXPRESSIONS TO RECOGNIZE:
- Time periods: this year, last year, this month, last month, this week, last week
- Quarters: this quarter, last quarter, Q1, Q2, Q3, Q4
- Relative periods: last 2 weeks, last 3 months, last 6 months
- Recent terms: recent, latest, current, today, yesterday

WHEN TO USE RELATIVE vs SPECIFIC DATES:
- Use relative dates in natural language: "I worked there this year"
- Use specific dates in formal documents: "I worked there from January 2025 to present"
- Use relative dates for general references: "recent developments in AI"
- Use specific dates for precise references: "the announcement on September 15, 2025"
"""
        
        return smart_instructions + date_math_context
    
    def analyze_query_for_dates(self, query: str) -> dict:
        """
        Analyze a query to extract date information and context
        
        Args:
            query: Search or writing query
            
        Returns:
            Dictionary with date analysis results
        """
        enhanced_query, date_info_list, search_terms = self.enhance_search_query(query)
        
        analysis = {
            'original_query': query,
            'enhanced_query': enhanced_query,
            'date_expressions_found': len(date_info_list),
            'date_info': date_info_list,
            'search_terms_added': search_terms,
            'has_relative_dates': len(date_info_list) > 0,
            'date_range_info': []
        }
        
        # Extract date range information
        for date_info in date_info_list:
            if date_info['type'] in ['year_range', 'month_range', 'week_range', 'quarter_range', 'period_range']:
                analysis['date_range_info'].append({
                    'description': date_info['description'],
                    'start_date': date_info['start_date'],
                    'end_date': date_info['end_date']
                })
            elif date_info['type'] == 'single_date':
                analysis['date_range_info'].append({
                    'description': date_info['description'],
                    'date': date_info['date']
                })
        
        return analysis

def create_enhanced_search_agent():
    """Create a search agent with enhanced date capabilities"""
    from agents import Agent, WebSearchTool, ModelSettings
    
    enhanced_agent = EnhancedDateSearchAgent()
    
    base_instructions = (
        "You are a research assistant. Given a search term, you search the web for that term and "
        "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
        "words. Capture the main points. Write succinctly, no need to have complete sentences or good "
        "grammar. This will be consumed by someone synthesizing a report, so it's vital you capture the "
        "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
    )
    
    enhanced_instructions = enhanced_agent.create_date_aware_search_instructions(base_instructions)
    
    return Agent(
        name="Enhanced Date Search Agent",
        instructions=enhanced_instructions,
        tools=[WebSearchTool(search_context_size="medium")],
        model="gpt-4o-mini",
        model_settings=ModelSettings(tool_choice="required"),
    )

def create_enhanced_writing_agent(context: str = "general"):
    """Create a writing agent with enhanced date capabilities"""
    from agents import Agent, WebSearchTool, ModelSettings
    
    enhanced_agent = EnhancedDateSearchAgent()
    
    base_instructions = (
        "You are a professional writer. Create high-quality, well-structured content "
        "based on the provided requirements and context."
    )
    
    enhanced_instructions = enhanced_agent.create_smart_writing_instructions_with_dates(base_instructions, context)
    
    return Agent(
        name=f"Enhanced Date Writing Agent ({context})",
        instructions=enhanced_instructions,
        tools=[WebSearchTool(search_context_size="medium")],
        model="gpt-4o",
        model_settings=ModelSettings(tool_choice="optional"),
    )

# Example usage and testing
if __name__ == "__main__":
    print("🔍 Enhanced Date Search Agent Test")
    print("=" * 60)
    
    enhanced_agent = EnhancedDateSearchAgent()
    
    # Test query enhancement
    test_queries = [
        "Apple stock performance this year",
        "Tesla earnings last quarter",
        "AI job opportunities in the last 2 weeks",
        "OpenAI developments this month",
        "cryptocurrency trends recent",
        "Microsoft financial results Q3",
        "Google announcements this week"
    ]
    
    print(f"Current Date: {enhanced_agent.current_date}")
    print(f"Current Year: {enhanced_agent.current_year}")
    print()
    
    for query in test_queries:
        print(f"🔍 Query: {query}")
        analysis = enhanced_agent.analyze_query_for_dates(query)
        
        print(f"  Enhanced: {analysis['enhanced_query']}")
        print(f"  Date Expressions Found: {analysis['date_expressions_found']}")
        print(f"  Has Relative Dates: {analysis['has_relative_dates']}")
        
        if analysis['date_range_info']:
            print(f"  Date Ranges:")
            for range_info in analysis['date_range_info']:
                print(f"    - {range_info['description']}")
        
        print()
    
    # Test instruction creation
    print("📝 Sample Enhanced Instructions:")
    sample_instructions = "You are a research assistant."
    enhanced = enhanced_agent.create_date_aware_search_instructions(sample_instructions, "financial")
    print(enhanced[:300] + "...")
