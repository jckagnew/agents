#!/usr/bin/env python3
"""
Update Writing Agents with Smart Date Management
Updates writing agents to use intelligent date handling
"""

import os
import re
from pathlib import Path
from smart_date_manager import SmartDateManager, create_smart_writing_agent_instructions

class WritingAgentUpdater:
    """Updates writing agents with smart date management"""
    
    def __init__(self):
        self.smart_date_manager = SmartDateManager()
        self.current_date = self.smart_date_manager.current_date
        self.current_year = self.smart_date_manager.current_year
        
    def update_agent_file(self, file_path: str) -> bool:
        """Update a single agent file with smart date management"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if already updated
            if "SmartDateManager" in content or "smart_date_manager" in content:
                print(f"✅ {file_path} - Already updated")
                return True
            
            # Add smart date manager import
            if "from agents import" in content or "import agents" in content:
                # Find the import section and add smart_date_manager import
                import_pattern = r'(from agents import.*?)\n'
                match = re.search(import_pattern, content, re.DOTALL)
                
                if match:
                    # Add smart_date_manager import after agents import
                    new_import = f"""from agents import Agent, WebSearchTool, ModelSettings
import sys
from pathlib import Path

# Add parent directory to path for smart_date_manager import
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.append(str(parent_dir))

from smart_date_manager import SmartDateManager, create_smart_writing_agent_instructions

# Initialize smart date manager
smart_date_manager = SmartDateManager()
"""
                    
                    content = content.replace(match.group(1), new_import)
            
            # Update instructions with smart date context
            instructions_pattern = r'(INSTRUCTIONS = .*?\)\n)'
            match = re.search(instructions_pattern, content, re.DOTALL)
            
            if match:
                old_instructions = match.group(1)
                
                # Determine context type from file path or content
                context = self.determine_context(file_path, content)
                
                # Create smart instructions
                smart_instructions = create_smart_writing_agent_instructions(
                    old_instructions.strip().rstrip(')'),
                    context
                )
                
                # Replace the old instructions
                new_instructions = f"INSTRUCTIONS = {smart_instructions}\n"
                content = content.replace(old_instructions, new_instructions)
            
            # Write updated content
            with open(file_path, 'w') as f:
                f.write(content)
            
            print(f"✅ {file_path} - Updated with smart date management")
            return True
            
        except Exception as e:
            print(f"❌ {file_path} - Error: {e}")
            return False
    
    def determine_context(self, file_path: str, content: str) -> str:
        """Determine the context type for the agent"""
        file_path_lower = file_path.lower()
        content_lower = content.lower()
        
        if 'cover' in file_path_lower or 'cover' in content_lower:
            return 'cover_letter'
        elif 'email' in file_path_lower or 'email' in content_lower:
            return 'email'
        elif 'report' in file_path_lower or 'report' in content_lower:
            return 'report'
        elif 'resume' in file_path_lower or 'resume' in content_lower:
            return 'resume'
        elif 'writer' in file_path_lower or 'writer' in content_lower:
            return 'report'
        else:
            return 'general'
    
    def find_writing_agent_files(self, root_dir: str) -> list:
        """Find all writing agent files"""
        writing_files = []
        
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.py') and any(keyword in file.lower() for keyword in 
                    ['writer', 'email', 'cover', 'report', 'letter', 'document']):
                    file_path = os.path.join(root, file)
                    # Skip __pycache__ and other non-agent files
                    if '__pycache__' not in file_path and 'test' not in file_path:
                        writing_files.append(file_path)
        
        return writing_files
    
    def update_all_writing_agents(self, root_dir: str = ".") -> dict:
        """Update all writing agents in the directory tree"""
        print("📝 Finding writing agent files...")
        writing_files = self.find_writing_agent_files(root_dir)
        
        print(f"Found {len(writing_files)} potential writing agent files")
        print()
        
        results = {
            'updated': [],
            'skipped': [],
            'errors': []
        }
        
        for file_path in writing_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Check if it's actually a writing agent
                if ('Agent(' in content and 
                    ('instructions' in content.lower() or 'INSTRUCTIONS' in content) and
                    any(keyword in content.lower() for keyword in 
                        ['write', 'email', 'cover', 'report', 'letter', 'document', 'content'])):
                    
                    if self.update_agent_file(file_path):
                        results['updated'].append(file_path)
                    else:
                        results['errors'].append(file_path)
                else:
                    results['skipped'].append(file_path)
                    print(f"⏭️  {file_path} - Not a writing agent")
                    
            except Exception as e:
                results['errors'].append(file_path)
                print(f"❌ {file_path} - Error: {e}")
        
        return results
    
    def create_smart_writing_template(self, output_file: str = "smart_writing_agent_template.py"):
        """Create a template for smart writing agents"""
        template_content = f'''#!/usr/bin/env python3
"""
Smart Writing Agent Template
Template for creating writing agents with intelligent date handling
"""

from agents import Agent, WebSearchTool, ModelSettings
import sys
from pathlib import Path

# Add parent directory to path for smart_date_manager import
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.append(str(parent_dir))

from smart_date_manager import SmartDateManager, create_smart_writing_agent_instructions

# Initialize smart date manager
smart_date_manager = SmartDateManager()

# Base instructions for a writing agent
BASE_INSTRUCTIONS = (
    "You are a professional writer. Create high-quality, well-structured content "
    "based on the provided requirements and context."
)

# Create smart instructions with date awareness
INSTRUCTIONS = create_smart_writing_agent_instructions(BASE_INSTRUCTIONS, "general")

# Create the agent
writing_agent = Agent(
    name="Smart Writing Agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="medium")],
    model="gpt-4o",
    model_settings=ModelSettings(tool_choice="optional"),
)

# Example usage
if __name__ == "__main__":
    print("📝 Smart Writing Agent Template")
    print("=" * 50)
    print(f"Current Date: {{smart_date_manager.current_date}}")
    print(f"Current Year: {{smart_date_manager.current_year}}")
    print("\\nAgent Instructions:")
    print(INSTRUCTIONS[:200] + "...")
'''
        
        with open(output_file, 'w') as f:
            f.write(template_content)
        
        print(f"✅ Created template: {output_file}")

def main():
    """Main function to update all writing agents"""
    print("📝 Updating Writing Agents with Smart Date Management")
    print("=" * 60)
    
    updater = WritingAgentUpdater()
    
    print(f"Current Date: {updater.current_date}")
    print(f"Current Year: {updater.current_year}")
    print()
    
    # Update all writing agents
    results = updater.update_all_writing_agents()
    
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
    updater.create_smart_writing_template()
    
    print("\n🎉 Writing agent update completed!")

if __name__ == "__main__":
    main()
