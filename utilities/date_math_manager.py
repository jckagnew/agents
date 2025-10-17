#!/usr/bin/env python3
"""
Date Math Manager
Advanced date calculation and relative date expression handling
"""

import os
import re
from datetime import datetime, timedelta, date
from typing import Dict, List, Tuple, Optional, Union
from dateutil.relativedelta import relativedelta
from date_manager import get_formatted_date, get_current_datetime

class DateMathManager:
    """Advanced date math and relative date expression handling"""
    
    def __init__(self):
        self.current_date = get_formatted_date('standard')
        self.current_datetime = get_current_datetime()
        self.current_year = get_formatted_date('iso')[:4]
        self.current_month = get_formatted_date('iso')[5:7]
        self.current_day = get_formatted_date('iso')[8:10]
        
        # Convert to datetime objects for calculations
        self.now = datetime.now()
        self.today = date.today()
        
        # Relative date patterns
        self.relative_patterns = {
            # Time periods
            'this_year': r'\bthis\s+year\b',
            'last_year': r'\blast\s+year\b',
            'next_year': r'\bnext\s+year\b',
            'this_month': r'\bthis\s+month\b',
            'last_month': r'\blast\s+month\b',
            'next_month': r'\bnext\s+month\b',
            'this_week': r'\bthis\s+week\b',
            'last_week': r'\blast\s+week\b',
            'next_week': r'\bnext\s+week\b',
            'today': r'\btoday\b',
            'yesterday': r'\byesterday\b',
            'tomorrow': r'\btomorrow\b',
            
            # Quarters
            'this_quarter': r'\bthis\s+quarter\b',
            'last_quarter': r'\blast\s+quarter\b',
            'next_quarter': r'\bnext\s+quarter\b',
            'q1': r'\bq1\b',
            'q2': r'\bq2\b',
            'q3': r'\bq3\b',
            'q4': r'\bq4\b',
            
            # Relative periods
            'last_2_weeks': r'\blast\s+two\s+weeks\b|\blast\s+2\s+weeks\b',
            'last_3_months': r'\blast\s+three\s+months\b|\blast\s+3\s+months\b',
            'last_6_months': r'\blast\s+six\s+months\b|\blast\s+6\s+months\b',
            'last_year': r'\blast\s+year\b',
            'past_year': r'\bpast\s+year\b',
            'recent': r'\brecent\b',
            'latest': r'\blatest\b',
            'current': r'\bcurrent\b',
        }
    
    def get_quarter_dates(self, year: int, quarter: int) -> Tuple[date, date]:
        """Get start and end dates for a quarter"""
        quarter_starts = {
            1: date(year, 1, 1),
            2: date(year, 4, 1),
            3: date(year, 7, 1),
            4: date(year, 10, 1)
        }
        quarter_ends = {
            1: date(year, 3, 31),
            2: date(year, 6, 30),
            3: date(year, 9, 30),
            4: date(year, 12, 31)
        }
        return quarter_starts[quarter], quarter_ends[quarter]
    
    def get_current_quarter(self) -> int:
        """Get current quarter number (1-4)"""
        month = self.now.month
        if month <= 3:
            return 1
        elif month <= 6:
            return 2
        elif month <= 9:
            return 3
        else:
            return 4
    
    def calculate_relative_date(self, expression: str) -> Dict[str, Union[date, str, List[date]]]:
        """
        Calculate actual dates for relative date expressions
        
        Args:
            expression: Relative date expression like "this year", "last 2 weeks", etc.
            
        Returns:
            Dictionary with calculated dates and metadata
        """
        expression_lower = expression.lower().strip()
        
        # This year
        if re.search(self.relative_patterns['this_year'], expression_lower):
            start_date = date(self.now.year, 1, 1)
            end_date = date(self.now.year, 12, 31)
            return {
                'type': 'year_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'This year ({self.now.year})',
                'search_terms': [f'{self.now.year}', 'this year', 'current year']
            }
        
        # Last year
        elif re.search(self.relative_patterns['last_year'], expression_lower):
            last_year = self.now.year - 1
            start_date = date(last_year, 1, 1)
            end_date = date(last_year, 12, 31)
            return {
                'type': 'year_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Last year ({last_year})',
                'search_terms': [f'{last_year}', 'last year', 'previous year']
            }
        
        # This month
        elif re.search(self.relative_patterns['this_month'], expression_lower):
            start_date = date(self.now.year, self.now.month, 1)
            next_month = self.now.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)
            return {
                'type': 'month_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'This month ({self.now.strftime("%B %Y")})',
                'search_terms': [f'{self.now.strftime("%B %Y")}', 'this month', 'current month']
            }
        
        # Last month
        elif re.search(self.relative_patterns['last_month'], expression_lower):
            last_month = self.now - relativedelta(months=1)
            start_date = date(last_month.year, last_month.month, 1)
            next_month = last_month.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)
            return {
                'type': 'month_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Last month ({last_month.strftime("%B %Y")})',
                'search_terms': [f'{last_month.strftime("%B %Y")}', 'last month', 'previous month']
            }
        
        # This week
        elif re.search(self.relative_patterns['this_week'], expression_lower):
            start_date = self.today - timedelta(days=self.today.weekday())
            end_date = start_date + timedelta(days=6)
            return {
                'type': 'week_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'This week ({start_date.strftime("%B %d")} - {end_date.strftime("%B %d, %Y")})',
                'search_terms': ['this week', 'current week', 'week of']
            }
        
        # Last week
        elif re.search(self.relative_patterns['last_week'], expression_lower):
            last_week = self.today - timedelta(weeks=1)
            start_date = last_week - timedelta(days=last_week.weekday())
            end_date = start_date + timedelta(days=6)
            return {
                'type': 'week_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Last week ({start_date.strftime("%B %d")} - {end_date.strftime("%B %d, %Y")})',
                'search_terms': ['last week', 'previous week', 'week of']
            }
        
        # Last 2 weeks
        elif re.search(self.relative_patterns['last_2_weeks'], expression_lower):
            end_date = self.today
            start_date = end_date - timedelta(weeks=2)
            return {
                'type': 'period_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Last 2 weeks ({start_date.strftime("%B %d")} - {end_date.strftime("%B %d, %Y")})',
                'search_terms': ['last 2 weeks', 'past 2 weeks', 'recent weeks']
            }
        
        # Last 3 months
        elif re.search(self.relative_patterns['last_3_months'], expression_lower):
            end_date = self.today
            start_date = end_date - relativedelta(months=3)
            return {
                'type': 'period_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Last 3 months ({start_date.strftime("%B %Y")} - {end_date.strftime("%B %Y")})',
                'search_terms': ['last 3 months', 'past 3 months', 'recent months']
            }
        
        # Last 6 months
        elif re.search(self.relative_patterns['last_6_months'], expression_lower):
            end_date = self.today
            start_date = end_date - relativedelta(months=6)
            return {
                'type': 'period_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Last 6 months ({start_date.strftime("%B %Y")} - {end_date.strftime("%B %Y")})',
                'search_terms': ['last 6 months', 'past 6 months', 'recent months']
            }
        
        # This quarter
        elif re.search(self.relative_patterns['this_quarter'], expression_lower):
            current_quarter = self.get_current_quarter()
            start_date, end_date = self.get_quarter_dates(self.now.year, current_quarter)
            return {
                'type': 'quarter_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Q{current_quarter} {self.now.year}',
                'search_terms': [f'Q{current_quarter}', f'Q{current_quarter} {self.now.year}', 'this quarter', 'current quarter']
            }
        
        # Last quarter
        elif re.search(self.relative_patterns['last_quarter'], expression_lower):
            current_quarter = self.get_current_quarter()
            if current_quarter == 1:
                last_quarter = 4
                year = self.now.year - 1
            else:
                last_quarter = current_quarter - 1
                year = self.now.year
            start_date, end_date = self.get_quarter_dates(year, last_quarter)
            return {
                'type': 'quarter_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Q{last_quarter} {year}',
                'search_terms': [f'Q{last_quarter}', f'Q{last_quarter} {year}', 'last quarter', 'previous quarter']
            }
        
        # Q1, Q2, Q3, Q4 (current year)
        elif re.search(self.relative_patterns['q1'], expression_lower):
            start_date, end_date = self.get_quarter_dates(self.now.year, 1)
            return {
                'type': 'quarter_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Q1 {self.now.year}',
                'search_terms': ['Q1', f'Q1 {self.now.year}', 'first quarter']
            }
        elif re.search(self.relative_patterns['q2'], expression_lower):
            start_date, end_date = self.get_quarter_dates(self.now.year, 2)
            return {
                'type': 'quarter_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Q2 {self.now.year}',
                'search_terms': ['Q2', f'Q2 {self.now.year}', 'second quarter']
            }
        elif re.search(self.relative_patterns['q3'], expression_lower):
            start_date, end_date = self.get_quarter_dates(self.now.year, 3)
            return {
                'type': 'quarter_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Q3 {self.now.year}',
                'search_terms': ['Q3', f'Q3 {self.now.year}', 'third quarter']
            }
        elif re.search(self.relative_patterns['q4'], expression_lower):
            start_date, end_date = self.get_quarter_dates(self.now.year, 4)
            return {
                'type': 'quarter_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Q4 {self.now.year}',
                'search_terms': ['Q4', f'Q4 {self.now.year}', 'fourth quarter']
            }
        
        # Today
        elif re.search(self.relative_patterns['today'], expression_lower):
            return {
                'type': 'single_date',
                'date': self.today,
                'description': f'Today ({self.today.strftime("%B %d, %Y")})',
                'search_terms': ['today', 'current date', self.today.strftime("%B %d, %Y")]
            }
        
        # Yesterday
        elif re.search(self.relative_patterns['yesterday'], expression_lower):
            yesterday = self.today - timedelta(days=1)
            return {
                'type': 'single_date',
                'date': yesterday,
                'description': f'Yesterday ({yesterday.strftime("%B %d, %Y")})',
                'search_terms': ['yesterday', yesterday.strftime("%B %d, %Y")]
            }
        
        # Recent/Latest/Current (last 30 days)
        elif re.search(self.relative_patterns['recent'], expression_lower) or \
             re.search(self.relative_patterns['latest'], expression_lower) or \
             re.search(self.relative_patterns['current'], expression_lower):
            end_date = self.today
            start_date = end_date - timedelta(days=30)
            return {
                'type': 'period_range',
                'start_date': start_date,
                'end_date': end_date,
                'description': f'Recent (last 30 days)',
                'search_terms': ['recent', 'latest', 'current', 'last 30 days']
            }
        
        # Default fallback
        else:
            return {
                'type': 'unknown',
                'description': f'Unknown expression: {expression}',
                'search_terms': [expression]
            }
    
    def enhance_search_query_with_date_math(self, query: str) -> str:
        """
        Enhance a search query by replacing relative date expressions with specific date ranges
        
        Args:
            query: Original search query
            
        Returns:
            Enhanced query with specific date information
        """
        enhanced_query = query
        date_info_list = []
        
        # Find and replace relative date expressions
        for pattern_name, pattern in self.relative_patterns.items():
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                expression = match.group(0)
                date_info = self.calculate_relative_date(expression)
                
                if date_info['type'] != 'unknown':
                    # Add specific date terms to the query
                    search_terms = ' '.join(date_info['search_terms'])
                    enhanced_query = enhanced_query.replace(expression, f"{expression} {search_terms}")
                    date_info_list.append(date_info)
        
        return enhanced_query, date_info_list
    
    def get_date_range_for_expression(self, expression: str) -> Optional[Tuple[date, date]]:
        """
        Get start and end dates for a relative date expression
        
        Args:
            expression: Relative date expression
            
        Returns:
            Tuple of (start_date, end_date) or None if not found
        """
        date_info = self.calculate_relative_date(expression)
        
        if date_info['type'] in ['year_range', 'month_range', 'week_range', 'quarter_range', 'period_range']:
            return date_info['start_date'], date_info['end_date']
        elif date_info['type'] == 'single_date':
            return date_info['date'], date_info['date']
        
        return None
    
    def is_date_in_range(self, check_date: date, expression: str) -> bool:
        """
        Check if a specific date falls within a relative date expression
        
        Args:
            check_date: Date to check
            expression: Relative date expression
            
        Returns:
            True if date is in range, False otherwise
        """
        date_range = self.get_date_range_for_expression(expression)
        if date_range:
            start_date, end_date = date_range
            return start_date <= check_date <= end_date
        return False
    
    def get_available_expressions(self) -> List[str]:
        """Get list of all supported relative date expressions"""
        return [
            'this year', 'last year', 'next year',
            'this month', 'last month', 'next month',
            'this week', 'last week', 'next week',
            'today', 'yesterday', 'tomorrow',
            'this quarter', 'last quarter', 'next quarter',
            'Q1', 'Q2', 'Q3', 'Q4',
            'last 2 weeks', 'last 3 months', 'last 6 months',
            'recent', 'latest', 'current'
        ]

# Convenience functions
def calculate_relative_date(expression: str) -> Dict:
    """Convenience function to calculate relative date"""
    manager = DateMathManager()
    return manager.calculate_relative_date(expression)

def enhance_search_query_with_dates(query: str) -> Tuple[str, List[Dict]]:
    """Convenience function to enhance search query with date math"""
    manager = DateMathManager()
    return manager.enhance_search_query_with_date_math(query)

def get_date_range(expression: str) -> Optional[Tuple[date, date]]:
    """Convenience function to get date range for expression"""
    manager = DateMathManager()
    return manager.get_date_range_for_expression(expression)

# Example usage and testing
if __name__ == "__main__":
    print("🧮 Date Math Manager Test")
    print("=" * 50)
    
    manager = DateMathManager()
    
    # Test various expressions
    test_expressions = [
        "this year",
        "last year", 
        "this quarter",
        "last quarter",
        "Q3",
        "this month",
        "last month",
        "this week",
        "last week",
        "last 2 weeks",
        "last 3 months",
        "last 6 months",
        "today",
        "yesterday",
        "recent",
        "latest",
        "current"
    ]
    
    print(f"Current Date: {manager.current_date}")
    print(f"Current Year: {manager.current_year}")
    print(f"Current Quarter: Q{manager.get_current_quarter()}")
    print()
    
    for expr in test_expressions:
        result = manager.calculate_relative_date(expr)
        print(f"Expression: '{expr}'")
        print(f"  Type: {result['type']}")
        print(f"  Description: {result['description']}")
        if 'start_date' in result and 'end_date' in result:
            print(f"  Range: {result['start_date']} to {result['end_date']}")
        elif 'date' in result:
            print(f"  Date: {result['date']}")
        print(f"  Search Terms: {', '.join(result['search_terms'])}")
        print()
    
    # Test query enhancement
    print("🔍 Query Enhancement Test:")
    test_queries = [
        "Apple stock performance this year",
        "Tesla earnings last quarter", 
        "AI job opportunities in the last 2 weeks",
        "OpenAI developments this month",
        "cryptocurrency trends recent"
    ]
    
    for query in test_queries:
        enhanced, date_info = manager.enhance_search_query_with_date_math(query)
        print(f"Original: {query}")
        print(f"Enhanced: {enhanced}")
        if date_info:
            print(f"Date Info: {date_info[0]['description']}")
        print()
