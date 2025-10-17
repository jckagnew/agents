#!/usr/bin/env python3
"""
Search Query Enhancer
Universal utility for enhancing search queries with current date context
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from date_manager import get_formatted_date, get_current_datetime

class SearchQueryEnhancer:
    """Enhances search queries with current date context for better results"""
    
    def __init__(self):
        self.current_date = get_formatted_date('standard')
        self.current_year = get_formatted_date('iso')[:4]
        self.current_month = get_formatted_date('iso')[5:7]
        self.current_day = get_formatted_date('iso')[8:10]
        self.current_datetime = get_current_datetime()
    
    def enhance_query(self, query: str, search_type: str = "general") -> str:
        """
        Enhance a search query with date context based on search type
        
        Args:
            query: Original search query
            search_type: Type of search (general, job, financial, news, etc.)
            
        Returns:
            Enhanced query with date context
        """
        # Base date terms for all searches
        date_terms = [
            self.current_year,
            "latest",
            "recent", 
            "current"
        ]
        
        # Type-specific enhancements
        if search_type == "job":
            date_terms.extend([
                "hiring now",
                "active jobs",
                "open positions",
                "recent postings"
            ])
        elif search_type == "financial":
            date_terms.extend([
                "Q3 2025",
                "recent earnings",
                "latest financial results",
                "current market"
            ])
        elif search_type == "news":
            date_terms.extend([
                "breaking news",
                "today",
                "this week",
                "latest updates"
            ])
        elif search_type == "technology":
            date_terms.extend([
                "latest developments",
                "recent updates",
                "new features",
                "current trends"
            ])
        
        # Add current month context
        month_name = get_formatted_date('readable').split(',')[0]  # Get day name
        date_terms.append(f"{month_name} 2025")
        
        # Construct enhanced query
        enhanced_query = f"{query} {' '.join(date_terms)}"
        
        return enhanced_query.strip()
    
    def get_search_context(self) -> dict:
        """Get current search context information"""
        return {
            "current_date": self.current_date,
            "current_year": self.current_year,
            "current_month": self.current_month,
            "current_day": self.current_day,
            "current_datetime": self.current_datetime,
            "search_tips": [
                f"Focus on {self.current_year} data",
                "Include 'latest' and 'recent' in searches",
                "Avoid outdated information",
                "Prioritize current developments"
            ]
        }
    
    def create_search_prompt(self, query: str, search_type: str = "general", reason: str = None) -> str:
        """
        Create a comprehensive search prompt with date awareness
        
        Args:
            query: The search query
            search_type: Type of search
            reason: Reason for the search
            
        Returns:
            Enhanced search prompt
        """
        enhanced_query = self.enhance_query(query, search_type)
        context = self.get_search_context()
        
        prompt_parts = [
            f"Search Query: {enhanced_query}",
            f"Search Type: {search_type}",
            f"Current Date: {context['current_date']}",
            f"Focus Year: {context['current_year']}"
        ]
        
        if reason:
            prompt_parts.append(f"Search Reason: {reason}")
        
        prompt_parts.extend([
            "",
            "Search Instructions:",
            "- Prioritize the most recent information available",
            f"- Focus on data from {context['current_year']}",
            "- Include recent news, updates, and developments",
            "- Avoid outdated information unless specifically relevant",
            "- Use current date context to find timely results"
        ])
        
        return "\n".join(prompt_parts)

# Convenience functions for easy use
def enhance_search_query(query: str, search_type: str = "general") -> str:
    """Convenience function to enhance a search query"""
    enhancer = SearchQueryEnhancer()
    return enhancer.enhance_query(query, search_type)

def create_search_prompt(query: str, search_type: str = "general", reason: str = None) -> str:
    """Convenience function to create a search prompt"""
    enhancer = SearchQueryEnhancer()
    return enhancer.create_search_prompt(query, search_type, reason)

def get_search_context() -> dict:
    """Convenience function to get search context"""
    enhancer = SearchQueryEnhancer()
    return enhancer.get_search_context()

# Example usage and testing
if __name__ == "__main__":
    print("🔍 Search Query Enhancer Test")
    print("=" * 50)
    
    enhancer = SearchQueryEnhancer()
    
    # Test different search types
    test_cases = [
        ("Apple stock performance", "financial"),
        ("AI job opportunities", "job"),
        ("Tesla latest news", "news"),
        ("OpenAI developments", "technology"),
        ("cryptocurrency trends", "general")
    ]
    
    print(f"Current Date: {enhancer.current_date}")
    print(f"Current Year: {enhancer.current_year}")
    print()
    
    for query, search_type in test_cases:
        enhanced = enhancer.enhance_query(query, search_type)
        print(f"Type: {search_type}")
        print(f"Original: {query}")
        print(f"Enhanced: {enhanced}")
        print()
    
    # Test search prompt creation
    prompt = enhancer.create_search_prompt(
        "OpenAI latest developments",
        "technology",
        "Research for AI industry report"
    )
    
    print("Sample Search Prompt:")
    print("-" * 30)
    print(prompt)
    
    # Test search context
    context = enhancer.get_search_context()
    print("\nSearch Context:")
    for key, value in context.items():
        print(f"  {key}: {value}")
