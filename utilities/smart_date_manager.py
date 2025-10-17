#!/usr/bin/env python3
"""
Smart Date Manager for AI-Generated Content
Handles current dates for new content while preserving historical dates
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any
from date_manager import get_formatted_date, get_current_datetime

class SmartDateManager:
    """Manages dates intelligently - current for new content, historical for existing documents"""
    
    def __init__(self):
        self.current_date = get_formatted_date('standard')
        self.current_year = get_formatted_date('iso')[:4]
        self.current_datetime = get_current_datetime()
        
        # Common date patterns to detect in documents
        self.date_patterns = [
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
        ]
        
        # Keywords that indicate historical context
        self.historical_indicators = [
            'sent on', 'submitted on', 'delivered on', 'created on', 'dated',
            'as of', 'effective date', 'from', 'since', 'previously',
            'earlier', 'before', 'past', 'historical', 'archive'
        ]
    
    def should_use_current_date(self, content: str, context: str = "general") -> bool:
        """
        Determine if current date should be used based on content analysis
        
        Args:
            content: The content being generated
            context: Context type (cover_letter, report, email, etc.)
            
        Returns:
            True if current date should be used, False if historical date should be preserved
        """
        # Check for historical indicators
        content_lower = content.lower()
        for indicator in self.historical_indicators:
            if indicator in content_lower:
                return False
        
        # Check for existing dates in content
        existing_dates = self.find_existing_dates(content)
        if existing_dates:
            # If dates are recent (within last 2 years), might be current
            # If dates are older, likely historical
            for date_str in existing_dates:
                if self.is_historical_date(date_str):
                    return False
        
        # Context-specific rules
        if context == "cover_letter":
            # Cover letters should use current date unless it's a draft of a previously sent letter
            return not self.has_historical_context(content)
        elif context == "report":
            # Reports should use current date unless it's a historical analysis
            return not self.has_historical_context(content)
        elif context == "email":
            # Emails should use current date unless it's a reply or historical
            return not self.has_historical_context(content)
        elif context == "resume":
            # Resumes should use current date for new entries
            return True
        elif context == "historical":
            # Explicitly historical content
            return False
        
        # Default to current date for new content
        return True
    
    def find_existing_dates(self, content: str) -> list:
        """Find all dates in the content"""
        dates = []
        for pattern in self.date_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            dates.extend(matches)
        return dates
    
    def is_historical_date(self, date_str: str) -> bool:
        """Check if a date is historical (more than 1 year old)"""
        try:
            # Parse various date formats
            date_obj = self.parse_date(date_str)
            if date_obj:
                current_year = int(self.current_year)
                return date_obj.year < (current_year - 1)
        except:
            pass
        return False
    
    def parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats"""
        date_formats = [
            '%B %d, %Y',      # January 15, 2024
            '%b %d, %Y',      # Jan 15, 2024
            '%m/%d/%Y',       # 01/15/2024
            '%Y-%m-%d',       # 2024-01-15
            '%d/%m/%Y',       # 15/01/2024
            '%d %B %Y',       # 15 January 2024
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue
        return None
    
    def has_historical_context(self, content: str) -> bool:
        """Check if content has historical context indicators"""
        content_lower = content.lower()
        
        # Check for historical indicators
        for indicator in self.historical_indicators:
            if indicator in content_lower:
                return True
        
        # Check for past tense indicators
        past_tense_indicators = [
            'was', 'were', 'had', 'did', 'went', 'came', 'took', 'gave',
            'previously', 'earlier', 'before', 'past', 'historical'
        ]
        
        past_tense_count = sum(1 for indicator in past_tense_indicators if indicator in content_lower)
        return past_tense_count > 2
    
    def get_appropriate_date(self, content: str, context: str = "general", 
                           force_current: bool = False) -> str:
        """
        Get the appropriate date for the content
        
        Args:
            content: The content being generated
            context: Context type
            force_current: Force use of current date
            
        Returns:
            Appropriate date string
        """
        if force_current:
            return self.current_date
        
        if self.should_use_current_date(content, context):
            return self.current_date
        else:
            # Return the most recent historical date found, or current date as fallback
            existing_dates = self.find_existing_dates(content)
            if existing_dates:
                # Return the most recent historical date
                return existing_dates[-1]
            return self.current_date
    
    def create_date_aware_instructions(self, base_instructions: str, context: str = "general") -> str:
        """
        Create date-aware instructions for writing agents
        
        Args:
            base_instructions: Base instructions for the agent
            context: Context type (cover_letter, report, etc.)
            
        Returns:
            Enhanced instructions with date awareness
        """
        date_context = f"""
        
DATE AWARENESS INSTRUCTIONS:
- Current Date: {self.current_date}
- Current Year: {self.current_year}

IMPORTANT: Use dates intelligently based on context:
- For NEW content (cover letters, reports, emails): Use current date ({self.current_date})
- For HISTORICAL content: Preserve existing dates, don't change them
- For DRAFTS of previously sent documents: Use the original date, not current date
- For UPDATES to existing documents: Use current date for new sections, preserve original dates for existing sections

Context: {context}
- If creating new {context}: Use current date
- If updating existing {context}: Preserve historical dates, use current date only for new content
- If referencing historical events: Use appropriate historical dates

DO NOT overwrite dates that are historically correct or contextually appropriate.
"""
        
        return base_instructions + date_context
    
    def enhance_writing_prompt(self, prompt: str, context: str = "general") -> str:
        """
        Enhance a writing prompt with date awareness
        
        Args:
            prompt: Original writing prompt
            context: Context type
            
        Returns:
            Enhanced prompt with date context
        """
        date_context = f"""
        
DATE CONTEXT:
- Current Date: {self.current_date}
- Current Year: {self.current_year}
- Context: {context}

When writing:
- Use current date for new content
- Preserve historical dates in existing content
- Don't change dates that are contextually correct
- If unsure, ask for clarification about date requirements
"""
        
        return prompt + date_context

def create_smart_writing_agent_instructions(base_instructions: str, context: str = "general") -> str:
    """Convenience function to create smart writing agent instructions"""
    manager = SmartDateManager()
    return manager.create_date_aware_instructions(base_instructions, context)

def get_smart_date(content: str, context: str = "general", force_current: bool = False) -> str:
    """Convenience function to get appropriate date"""
    manager = SmartDateManager()
    return manager.get_appropriate_date(content, context, force_current)

# Example usage and testing
if __name__ == "__main__":
    print("🧠 Smart Date Manager Test")
    print("=" * 50)
    
    manager = SmartDateManager()
    
    # Test cases
    test_cases = [
        {
            "content": "I am writing to apply for the position of Software Engineer.",
            "context": "cover_letter",
            "expected": "current"
        },
        {
            "content": "As mentioned in my email sent on January 15, 2024, I would like to follow up.",
            "context": "email",
            "expected": "historical"
        },
        {
            "content": "The company was founded in 2010 and has grown significantly since then.",
            "context": "report",
            "expected": "historical"
        },
        {
            "content": "I am excited to announce our new product launch.",
            "context": "announcement",
            "expected": "current"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['context']}")
        print(f"Content: {test['content'][:50]}...")
        
        should_use_current = manager.should_use_current_date(test['content'], test['context'])
        appropriate_date = manager.get_appropriate_date(test['content'], test['context'])
        
        print(f"Should use current date: {should_use_current}")
        print(f"Appropriate date: {appropriate_date}")
        print(f"Expected: {test['expected']}")
        print(f"✅ Correct: {('current' if should_use_current else 'historical') == test['expected']}")
    
    # Test instruction creation
    print(f"\n📝 Sample Instructions for Cover Letter Agent:")
    sample_instructions = "You are a professional cover letter writer."
    enhanced = manager.create_date_aware_instructions(sample_instructions, "cover_letter")
    print(enhanced[:200] + "...")
