#!/usr/bin/env python3
"""
Update Search Agents with Date Awareness
Automatically updates all search agents to use current date context
"""

import os
import re
from pathlib import Path
from date_manager import get_formatted_date, get_current_datetime

class SearchAgentUpdater:
    """Updates search agents with date awareness"""
    
    def __init__(self):
        self.current_date = get_formatted_date('standard')
        self.current_year = get_formatted_date('iso')[:4]
        self.current_datetime = get_current_datetime()
        
    def update_agent_file(self, file_path: str) -> bool:
        """Update a single agent file with date awareness"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if already updated
            if "CURRENT_DATE" in content or "date_manager" in content:
                print(f"✅ {file_path} - Already updated")
                return True
            
            # Add date manager import
            if "from agents import" in content:
                # Find the import section and add date_manager import
                import_pattern = r'(from agents import.*?)\n'
                match = re.search(import_pattern, content, re.DOTALL)
                
                if match:
                    # Add date_manager import after agents import
                    new_import = f"""from agents import Agent, WebSearchTool, ModelSettings
import sys
from pathlib import Path

# Add parent directory to path for date_manager import
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.append(str(parent_dir))

from date_manager import get_formatted_date

# Get current date for search context
CURRENT_DATE = get_formatted_date('standard')
CURRENT_YEAR = get_formatted_date('iso')[:4]
"""
                    
                    content = content.replace(match.group(1), new_import)
            
            # Update instructions with date context
            instructions_pattern = r'(INSTRUCTIONS = \(.*?\)\n)'
            match = re.search(instructions_pattern, content, re.DOTALL)
            
            if match:
                old_instructions = match.group(1)
                date_context = f"""
IMPORTANT DATE CONTEXT:
- Current Date: {self.current_date}
- Current Year: {self.current_year}
- Search for the most recent information available
- Prioritize data from {self.current_year} and recent months
- Include terms like 'latest', 'recent', 'current', '{self.current_year}' in searches
- Avoid outdated information from previous years unless specifically requested
"""
                
                # Add date context to instructions
                new_instructions = old_instructions.rstrip() + date_context + "\n)"
                content = content.replace(old_instructions, new_instructions)
            
            # Write updated content
            with open(file_path, 'w') as f:
                f.write(content)
            
            print(f"✅ {file_path} - Updated with date awareness")
            return True
            
        except Exception as e:
            print(f"❌ {file_path} - Error: {e}")
            return False
    
    def find_search_agent_files(self, root_dir: str) -> list:
        """Find all search agent files"""
        search_files = []
        
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.py') and ('search' in file.lower() or 'agent' in file.lower()):
                    file_path = os.path.join(root, file)
                    # Skip __pycache__ and other non-agent files
                    if '__pycache__' not in file_path and 'test' not in file_path:
                        search_files.append(file_path)
        
        return search_files
    
    def update_all_search_agents(self, root_dir: str = ".") -> dict:
        """Update all search agents in the directory tree"""
        print("🔍 Finding search agent files...")
        search_files = self.find_search_agent_files(root_dir)
        
        print(f"Found {len(search_files)} potential search agent files")
        print()
        
        results = {
            'updated': [],
            'skipped': [],
            'errors': []
        }
        
        for file_path in search_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Check if it's actually a search agent
                if ('Agent(' in content and 
                    ('WebSearchTool' in content or 'SerperDevTool' in content) and
                    'instructions' in content.lower()):
                    
                    if self.update_agent_file(file_path):
                        results['updated'].append(file_path)
                    else:
                        results['errors'].append(file_path)
                else:
                    results['skipped'].append(file_path)
                    print(f"⏭️  {file_path} - Not a search agent")
                    
            except Exception as e:
                results['errors'].append(file_path)
                print(f"❌ {file_path} - Error: {e}")
        
        return results
    
    def create_date_aware_template(self, output_file: str = "date_aware_search_agent_template.py"):
        """Create a template for date-aware search agents"""
        template_content = f'''#!/usr/bin/env python3
"""
Date-Aware Search Agent Template
Template for creating search agents with current date context
"""

from agents import Agent, WebSearchTool, ModelSettings
import sys
from pathlib import Path

# Add parent directory to path for date_manager import
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.append(str(parent_dir))

from date_manager import get_formatted_date

# Get current date for search context
CURRENT_DATE = get_formatted_date('standard')
CURRENT_YEAR = get_formatted_date('iso')[:4]

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succinctly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so it's vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself.\\n\\n"
    f"IMPORTANT DATE CONTEXT:\\n"
    f"- Current Date: {{CURRENT_DATE}}\\n"
    f"- Current Year: {{CURRENT_YEAR}}\\n"
    f"- Search for the most recent information available\\n"
    f"- Prioritize data from {{CURRENT_YEAR}} and recent months\\n"
    f"- Include terms like 'latest', 'recent', 'current', '{{CURRENT_YEAR}}' in searches\\n"
    f"- Avoid outdated information from previous years unless specifically requested"
)

search_agent = Agent(
    name="Date-Aware Search Agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="medium")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)
'''
        
        with open(output_file, 'w') as f:
            f.write(template_content)
        
        print(f"✅ Created template: {output_file}")

def main():
    """Main function to update all search agents"""
    print("📅 Updating Search Agents with Date Awareness")
    print("=" * 60)
    
    updater = SearchAgentUpdater()
    
    print(f"Current Date: {updater.current_date}")
    print(f"Current Year: {updater.current_year}")
    print()
    
    # Update all search agents
    results = updater.update_all_search_agents()
    
    print("\n📊 Update Results:")
    print(f"✅ Updated: {len(results['updated'])} files")
    print(f"⏭️  Skipped: {len(results['skipped'])} files")
    print(f"❌ Errors: {len(results['errors'])} files")
    
    if results['updated']:
        print("\n✅ Successfully Updated Files:")
        for file_path in results['updated']:
            print(f"  - {file_path}")
    
    if results['errors']:
        print("\n❌ Files with Errors:")
        for file_path in results['errors']:
            print(f"  - {file_path}")
    
    # Create template
    print("\n📝 Creating template...")
    updater.create_date_aware_template()
    
    print("\n🎉 Search agent update completed!")

if __name__ == "__main__":
    main()
