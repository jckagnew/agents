#!/usr/bin/env python3
"""
Update Agents with Date Math Capabilities
Integrates advanced date math into all search and writing agents
"""

import os
import re
from pathlib import Path
from date_math_manager import DateMathManager
from enhanced_date_search_agent import EnhancedDateSearchAgent

class DateMathAgentUpdater:
    """Updates agents with advanced date math capabilities"""
    
    def __init__(self):
        self.date_math_manager = DateMathManager()
        self.enhanced_agent = EnhancedDateSearchAgent()
        self.current_date = self.date_math_manager.current_date
        self.current_year = self.date_math_manager.current_year
        
    def update_search_agent_file(self, file_path: str) -> bool:
        """Update a search agent file with date math capabilities"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if already updated with date math
            if "DateMathManager" in content or "date_math_manager" in content:
                print(f"✅ {file_path} - Already updated with date math")
                return True
            
            # Add date math manager import
            if "from date_manager import" in content:
                # Add date_math_manager import after date_manager import
                import_pattern = r'(from date_manager import.*?)\n'
                match = re.search(import_pattern, content, re.DOTALL)
                
                if match:
                    new_import = f"""from date_manager import get_formatted_date, get_current_datetime
from date_math_manager import DateMathManager, enhance_search_query_with_dates
from enhanced_date_search_agent import EnhancedDateSearchAgent

# Initialize date math manager
date_math_manager = DateMathManager()
enhanced_agent = EnhancedDateSearchAgent()
"""
                    
                    content = content.replace(match.group(1), new_import)
            
            # Update instructions with date math capabilities
            instructions_pattern = r'(IMPORTANT DATE CONTEXT:.*?DO NOT overwrite dates that are historically correct or contextually appropriate\.)'
            match = re.search(instructions_pattern, content, re.DOTALL)
            
            if match:
                old_instructions = match.group(1)
                date_math_context = f"""
RELATIVE DATE EXPRESSIONS SUPPORTED:
- Time periods: "this year", "last year", "this month", "last month", "this week", "last week"
- Quarters: "this quarter", "last quarter", "Q1", "Q2", "Q3", "Q4"
- Relative periods: "last 2 weeks", "last 3 months", "last 6 months"
- Recent terms: "recent", "latest", "current", "today", "yesterday"

DATE MATH ENHANCEMENT RULES:
- When you see relative date expressions, automatically expand them with specific date ranges
- For "this year" searches, prioritize {self.current_year} data and include "{self.current_year}", "this year", "current year"
- For "last quarter" searches, include specific quarter information (e.g., "Q2 {self.current_year}")
- For "recent" searches, focus on last 30 days and include "recent", "latest", "current"
- Always include current year ({self.current_year}) in search terms
- Use date_math_manager.calculate_relative_date() to process relative expressions
- Use enhanced_agent.enhance_search_query() for advanced query enhancement

EXAMPLES:
- "Apple stock performance this year" → "Apple stock performance this year 2025 this year current year"
- "Tesla earnings last quarter" → "Tesla earnings last quarter Q2 Q2 2025 last quarter previous quarter"
- "AI jobs in the last 2 weeks" → "AI jobs in the last 2 weeks last 2 weeks past 2 weeks recent weeks"
"""
                
                new_instructions = old_instructions + date_math_context
                content = content.replace(old_instructions, new_instructions)
            
            # Write updated content
            with open(file_path, 'w') as f:
                f.write(content)
            
            print(f"✅ {file_path} - Updated with date math capabilities")
            return True
            
        except Exception as e:
            print(f"❌ {file_path} - Error: {e}")
            return False
    
    def update_writing_agent_file(self, file_path: str) -> bool:
        """Update a writing agent file with date math capabilities"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if already updated with date math
            if "DateMathManager" in content or "date_math_manager" in content:
                print(f"✅ {file_path} - Already updated with date math")
                return True
            
            # Add date math manager import
            if "from smart_date_manager import" in content:
                # Add date_math_manager import after smart_date_manager import
                import_pattern = r'(from smart_date_manager import.*?)\n'
                match = re.search(import_pattern, content, re.DOTALL)
                
                if match:
                    new_import = f"""from smart_date_manager import SmartDateManager, create_smart_writing_agent_instructions
from date_math_manager import DateMathManager, calculate_relative_date
from enhanced_date_search_agent import EnhancedDateSearchAgent

# Initialize managers
smart_date_manager = SmartDateManager()
date_math_manager = DateMathManager()
enhanced_agent = EnhancedDateSearchAgent()
"""
                    
                    content = content.replace(match.group(1), new_import)
            
            # Update instructions with date math capabilities
            instructions_pattern = r'(DO NOT overwrite dates that are historically correct or contextually appropriate\.)'
            match = re.search(instructions_pattern, content, re.DOTALL)
            
            if match:
                old_instructions = match.group(1)
                date_math_context = f"""

RELATIVE DATE EXPRESSIONS SUPPORTED:
- Time periods: "this year", "last year", "this month", "last month", "this week", "last week"
- Quarters: "this quarter", "last quarter", "Q1", "Q2", "Q3", "Q4"
- Relative periods: "last 2 weeks", "last 3 months", "last 6 months"
- Recent terms: "recent", "latest", "current", "today", "yesterday"

DATE MATH WRITING RULES:
- Support relative date expressions in natural language
- Use specific dates when appropriate, relative dates when more natural
- Examples:
  * "this year" → "this year ({self.current_year})" or "{self.current_year}"
  * "last quarter" → "last quarter (Q2 {self.current_year})" or "Q2 {self.current_year}"
  * "recent" → "recent (last 30 days)" or "recent developments"
  * "this month" → "this month (September {self.current_year})" or "September {self.current_year}"

WHEN TO USE RELATIVE vs SPECIFIC DATES:
- Use relative dates in natural language: "I worked there this year"
- Use specific dates in formal documents: "I worked there from January {self.current_year} to present"
- Use relative dates for general references: "recent developments in AI"
- Use specific dates for precise references: "the announcement on September 15, {self.current_year}"

USE date_math_manager.calculate_relative_date() to process relative expressions
USE enhanced_agent.create_smart_writing_instructions_with_dates() for advanced writing
"""
                
                new_instructions = old_instructions + date_math_context
                content = content.replace(old_instructions, new_instructions)
            
            # Write updated content
            with open(file_path, 'w') as f:
                f.write(content)
            
            print(f"✅ {file_path} - Updated with date math capabilities")
            return True
            
        except Exception as e:
            print(f"❌ {file_path} - Error: {e}")
            return False
    
    def find_agent_files(self, root_dir: str) -> dict:
        """Find all agent files that need date math updates"""
        search_files = []
        writing_files = []
        
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.py') and ('search' in file.lower() or 'agent' in file.lower() or 'writer' in file.lower() or 'email' in file.lower()):
                    file_path = os.path.join(root, file)
                    # Skip __pycache__ and other non-agent files
                    if '__pycache__' not in file_path and 'test' not in file_path:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        
                        if ('Agent(' in content and 'instructions' in content.lower()):
                            if 'search' in file.lower() or 'WebSearchTool' in content:
                                search_files.append(file_path)
                            elif any(keyword in file.lower() for keyword in ['writer', 'email', 'report', 'letter']):
                                writing_files.append(file_path)
        
        return {'search': search_files, 'writing': writing_files}
    
    def update_all_agents(self, root_dir: str = ".") -> dict:
        """Update all agents with date math capabilities"""
        print("🧮 Updating Agents with Date Math Capabilities")
        print("=" * 60)
        
        print(f"Current Date: {self.current_date}")
        print(f"Current Year: {self.current_year}")
        print()
        
        # Find agent files
        print("🔍 Finding agent files...")
        agent_files = self.find_agent_files(root_dir)
        
        print(f"Found {len(agent_files['search'])} search agent files")
        print(f"Found {len(agent_files['writing'])} writing agent files")
        print()
        
        results = {
            'search_updated': [],
            'search_skipped': [],
            'search_errors': [],
            'writing_updated': [],
            'writing_skipped': [],
            'writing_errors': []
        }
        
        # Update search agents
        print("🔍 Updating search agents...")
        for file_path in agent_files['search']:
            try:
                if self.update_search_agent_file(file_path):
                    results['search_updated'].append(file_path)
                else:
                    results['search_skipped'].append(file_path)
            except Exception as e:
                results['search_errors'].append(file_path)
                print(f"❌ {file_path} - Error: {e}")
        
        # Update writing agents
        print("\n📝 Updating writing agents...")
        for file_path in agent_files['writing']:
            try:
                if self.update_writing_agent_file(file_path):
                    results['writing_updated'].append(file_path)
                else:
                    results['writing_skipped'].append(file_path)
            except Exception as e:
                results['writing_errors'].append(file_path)
                print(f"❌ {file_path} - Error: {e}")
        
        return results
    
    def create_date_math_template(self, output_file: str = "date_math_agent_template.py"):
        """Create a template for agents with date math capabilities"""
        template_content = f'''#!/usr/bin/env python3
"""
Date Math Agent Template
Template for creating agents with advanced date math capabilities
"""

from agents import Agent, WebSearchTool, ModelSettings
import sys
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.append(str(parent_dir))

from date_manager import get_formatted_date, get_current_datetime
from date_math_manager import DateMathManager, enhance_search_query_with_dates
from smart_date_manager import SmartDateManager, create_smart_writing_agent_instructions
from enhanced_date_search_agent import EnhancedDateSearchAgent

# Initialize managers
date_math_manager = DateMathManager()
smart_date_manager = SmartDateManager()
enhanced_agent = EnhancedDateSearchAgent()

# Base instructions
BASE_INSTRUCTIONS = (
    "You are a professional AI agent with advanced date math capabilities. "
    "You can understand and process relative date expressions like 'this year', "
    "'last quarter', 'recent', etc., and convert them to specific date ranges."
)

# Create enhanced instructions
ENHANCED_INSTRUCTIONS = enhanced_agent.create_date_aware_search_instructions(BASE_INSTRUCTIONS, "general")

# Create the agent
date_math_agent = Agent(
    name="Date Math Agent",
    instructions=ENHANCED_INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="medium")],
    model="gpt-4o",
    model_settings=ModelSettings(tool_choice="optional"),
)

# Example usage
if __name__ == "__main__":
    print("🧮 Date Math Agent Template")
    print("=" * 50)
    print(f"Current Date: {{date_math_manager.current_date}}")
    print(f"Current Year: {{date_math_manager.current_year}}")
    print(f"Current Quarter: Q{{date_math_manager.get_current_quarter()}}")
    print("\\nSupported Expressions:")
    for expr in date_math_manager.get_available_expressions():
        print(f"  - {{expr}}")
'''
        
        with open(output_file, 'w') as f:
            f.write(template_content)
        
        print(f"✅ Created template: {output_file}")

def main():
    """Main function to update all agents with date math"""
    updater = DateMathAgentUpdater()
    
    # Update all agents
    results = updater.update_all_agents()
    
    print("\n📊 Update Results:")
    print(f"✅ Search Agents Updated: {len(results['search_updated'])}")
    print(f"⏭️  Search Agents Skipped: {len(results['search_skipped'])}")
    print(f"❌ Search Agent Errors: {len(results['search_errors'])}")
    print(f"✅ Writing Agents Updated: {len(results['writing_updated'])}")
    print(f"⏭️  Writing Agents Skipped: {len(results['writing_skipped'])}")
    print(f"❌ Writing Agent Errors: {len(results['writing_errors'])}")
    
    if results['search_updated']:
        print("\n✅ Successfully Updated Search Agents:")
        for file_path in results['search_updated']:
            print(f"  - {file_path}")
    
    if results['writing_updated']:
        print("\n✅ Successfully Updated Writing Agents:")
        for file_path in results['writing_updated']:
            print(f"  - {file_path}")
    
    if results['search_errors'] or results['writing_errors']:
        print("\n❌ Files with Errors:")
        for file_path in results['search_errors'] + results['writing_errors']:
            print(f"  - {file_path}")
    
    # Create template
    print("\n📝 Creating template...")
    updater.create_date_math_template()
    
    print("\n🎉 Date math update completed!")

if __name__ == "__main__":
    main()
