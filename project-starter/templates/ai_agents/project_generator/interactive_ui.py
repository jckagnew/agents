"""
Interactive Developer UI for AI Agent Project Generation

This module provides a conversational interface that guides developers through
creating new AI agent projects using our data-driven frameworks.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

# Add parent directories to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from project_starter.templates.ai_agents.schemas.agent_schemas import AgentSchemaGenerator
from project_starter.templates.ai_agents.mcp.mcp_framework import MCPFramework
from project_starter.templates.ai_agents.prompting.structured_prompts import PromptFramework, PromptType
from project_starter.templates.ai_agents.test_data.data_generator import TestDataGenerator, DataContext
from project_starter.templates.ai_agents.configuration.subject_setting_style import SubjectSettingStyleFramework, SubjectType, SettingType, StyleType


class ProjectGeneratorUI:
    """Interactive UI for generating AI agent projects"""
    
    def __init__(self):
        """Initialize the project generator UI"""
        self.schema_generator = AgentSchemaGenerator()
        self.mcp_framework = MCPFramework()
        self.prompt_framework = PromptFramework()
        self.data_generator = TestDataGenerator()
        self.config_framework = SubjectSettingStyleFramework()
        
        self.current_project = {}
        self.project_requirements = {}
        
    def welcome_message(self):
        """Display welcome message and introduction"""
        print("🚀 Welcome to the AI Agent Project Generator!")
        print("=" * 50)
        print("This interactive tool will guide you through creating")
        print("a new AI agent project using our data-driven frameworks.")
        print()
        print("We'll ask you questions about your project and generate:")
        print("• Agent configurations using Subject-Setting-Style framework")
        print("• Structured prompts for agent behavior")
        print("• Realistic test data for validation")
        print("• MCP tool integrations for external services")
        print("• JSON schemas for pattern validation")
        print()
    
    def get_project_basic_info(self):
        """Get basic project information"""
        print("📋 Let's start with some basic information about your project:")
        print()
        
        # Project name
        project_name = input("What would you like to name your project? ").strip()
        while not project_name:
            project_name = input("Please enter a project name: ").strip()
        
        # Project description
        print("\nDescribe what your AI agent project will do:")
        project_description = input("> ").strip()
        while not project_description:
            project_description = input("Please provide a description: ").strip()
        
        # Project domain
        print("\nWhat domain will your agent operate in?")
        print("1. Customer Service")
        print("2. Healthcare")
        print("3. E-commerce")
        print("4. Technology/Software")
        print("5. Education")
        print("6. Finance")
        print("7. Other")
        
        domain_choice = input("Choose a domain (1-7): ").strip()
        domain_map = {
            "1": "customer_service",
            "2": "healthcare", 
            "3": "e_commerce",
            "4": "technology",
            "5": "education",
            "6": "finance",
            "7": "other"
        }
        project_domain = domain_map.get(domain_choice, "other")
        
        if project_domain == "other":
            project_domain = input("Please specify the domain: ").strip().lower().replace(" ", "_")
        
        self.current_project = {
            "name": project_name,
            "description": project_description,
            "domain": project_domain,
            "created_at": datetime.now().isoformat()
        }
        
        print(f"\n✅ Project '{project_name}' created for {project_domain} domain")
        return True
    
    def select_agent_patterns(self):
        """Select which agent patterns to include"""
        print("\n🤖 Which agent patterns would you like to include?")
        print("(You can select multiple patterns)")
        print()
        
        patterns = {
            "1": ("Multi-Agent Orchestration", "pattern_1"),
            "2": ("Agent Communication", "pattern_2"),
            "3": ("Agent Collaboration", "pattern_3"),
            "4": ("Agent Learning", "pattern_4"),
            "5": ("Memory Management", "pattern_8"),
            "6": ("Goal Setting & Monitoring", "pattern_10"),
            "7": ("Exception Handling & Recovery", "pattern_11"),
            "8": ("Agent Adaptation", "pattern_12"),
            "9": ("Agent Creativity", "pattern_13"),
            "10": ("Agent Empathy", "pattern_14"),
            "11": ("Resource-Aware Optimization", "pattern_15"),
            "12": ("Agent Ethics", "pattern_16"),
            "13": ("Evaluation & Monitoring", "pattern_17"),
            "14": ("Guardrails & Safety", "pattern_18"),
            "15": ("Agent Evolution", "pattern_19"),
            "16": ("Agent Swarming", "pattern_20")
        }
        
        print("Available patterns:")
        for key, (name, _) in patterns.items():
            print(f"{key}. {name}")
        
        print("\nEnter the numbers of patterns you want (e.g., '1,3,5' or 'all'):")
        selection = input("> ").strip().lower()
        
        selected_patterns = []
        if selection == "all":
            selected_patterns = list(patterns.values())
        else:
            try:
                indices = [x.strip() for x in selection.split(",")]
                for idx in indices:
                    if idx in patterns:
                        selected_patterns.append(patterns[idx])
            except:
                print("Invalid selection, using default patterns")
                selected_patterns = [patterns["1"], patterns["2"], patterns["3"]]
        
        self.current_project["selected_patterns"] = selected_patterns
        print(f"\n✅ Selected {len(selected_patterns)} agent patterns")
        return True
    
    def configure_agent_personality(self):
        """Configure agent personality using Subject-Setting-Style framework"""
        print("\n🎭 Let's configure your agent's personality and behavior:")
        print()
        
        # Agent role/personality
        print("What is the primary role of your agent?")
        print("1. Customer Service Representative")
        print("2. Technical Analyst")
        print("3. Creative Writer")
        print("4. Project Manager")
        print("5. Healthcare Assistant")
        print("6. Custom")
        
        role_choice = input("Choose a role (1-6): ").strip()
        
        if role_choice == "6":
            custom_role = input("Describe your custom agent role: ").strip()
            agent_config = self._create_custom_agent_config(custom_role)
        else:
            role_map = {
                "1": "customer_service_agent",
                "2": "technical_analyst", 
                "3": "creative_writer",
                "4": "project_manager",
                "5": "healthcare_assistant"
            }
            template_name = role_map.get(role_choice, "customer_service_agent")
            agent_config = self.config_framework.create_from_template(template_name, {
                "name": f"{self.current_project['name']} Agent",
                "description": self.current_project['description']
            })
        
        self.current_project["agent_config_id"] = agent_config
        
        # Get photographic prompt
        prompt = self.config_framework.generate_photographic_prompt(agent_config)
        print(f"\n📸 Your agent's photographic description:")
        print(f"   {prompt}")
        
        return True
    
    def configure_agent_capabilities(self):
        """Configure specific agent capabilities"""
        print("\n⚡ Let's define your agent's specific capabilities:")
        print()
        
        capabilities = []
        
        # Core capabilities
        print("What are the core capabilities your agent needs?")
        print("(Enter multiple capabilities separated by commas)")
        print("Examples: problem solving, data analysis, creative writing, customer support")
        
        core_caps = input("Core capabilities: ").strip()
        if core_caps:
            capabilities.extend([cap.strip() for cap in core_caps.split(",")])
        
        # Technical capabilities
        print("\nWhat technical capabilities are required?")
        print("Examples: API integration, database access, file processing, web scraping")
        
        tech_caps = input("Technical capabilities: ").strip()
        if tech_caps:
            capabilities.extend([cap.strip() for cap in tech_caps.split(",")])
        
        # Communication style
        print("\nHow should your agent communicate?")
        print("1. Professional and formal")
        print("2. Friendly and casual")
        print("3. Technical and precise")
        print("4. Empathetic and supportive")
        print("5. Creative and engaging")
        
        comm_choice = input("Choose communication style (1-5): ").strip()
        comm_styles = {
            "1": "professional and formal",
            "2": "friendly and casual",
            "3": "technical and precise", 
            "4": "empathetic and supportive",
            "5": "creative and engaging"
        }
        comm_style = comm_styles.get(comm_choice, "professional and formal")
        
        self.current_project["capabilities"] = capabilities
        self.current_project["communication_style"] = comm_style
        
        print(f"\n✅ Agent capabilities configured: {len(capabilities)} capabilities, {comm_style} style")
        return True
    
    def configure_external_integrations(self):
        """Configure external service integrations"""
        print("\n🔗 Let's set up external service integrations:")
        print()
        
        integrations = []
        
        # Database integration
        print("Do you need database integration? (y/n)")
        if input("> ").strip().lower() == 'y':
            print("What type of database?")
            print("1. SQLite (local)")
            print("2. PostgreSQL")
            print("3. MySQL")
            print("4. MongoDB")
            
            db_choice = input("Choose database type (1-4): ").strip()
            db_types = {"1": "sqlite", "2": "postgresql", "3": "mysql", "4": "mongodb"}
            db_type = db_types.get(db_choice, "sqlite")
            integrations.append({"type": "database", "subtype": db_type})
        
        # API integration
        print("\nDo you need API integration? (y/n)")
        if input("> ").strip().lower() == 'y':
            print("What APIs do you need?")
            print("Examples: OpenAI, Google, Stripe, Slack, etc.")
            apis = input("API names (comma-separated): ").strip()
            if apis:
                for api in apis.split(","):
                    integrations.append({"type": "api", "name": api.strip()})
        
        # File processing
        print("\nDo you need file processing capabilities? (y/n)")
        if input("> ").strip().lower() == 'y':
            print("What file types?")
            print("Examples: PDF, CSV, JSON, images, documents")
            file_types = input("File types (comma-separated): ").strip()
            if file_types:
                integrations.append({"type": "file_processing", "types": [t.strip() for t in file_types.split(",")]})
        
        # Image processing
        print("\nDo you need image processing? (y/n)")
        if input("> ").strip().lower() == 'y':
            integrations.append({"type": "image_processing"})
        
        self.current_project["integrations"] = integrations
        print(f"\n✅ Configured {len(integrations)} external integrations")
        return True
    
    def configure_testing_requirements(self):
        """Configure testing and validation requirements"""
        print("\n🧪 Let's set up testing and validation:")
        print()
        
        # Test data requirements
        print("What type of test data do you need?")
        print("1. User profiles and interactions")
        print("2. Business data (orders, transactions)")
        print("3. Technical data (logs, metrics)")
        print("4. Content data (documents, conversations)")
        print("5. All of the above")
        
        test_choice = input("Choose test data type (1-5): ").strip()
        test_data_types = {
            "1": ["user_profiles", "conversations", "interactions"],
            "2": ["tasks", "events", "feedback"],
            "3": ["metrics", "performance", "events"],
            "4": ["documents", "conversations", "sessions"],
            "5": ["user_profiles", "conversations", "tasks", "events", "metrics", "documents"]
        }
        selected_test_types = test_data_types.get(test_choice, ["user_profiles", "conversations"])
        
        # Test data volume
        print("\nHow much test data do you need?")
        print("1. Small (100-500 records)")
        print("2. Medium (500-2000 records)")
        print("3. Large (2000-10000 records)")
        print("4. Custom")
        
        volume_choice = input("Choose data volume (1-4): ").strip()
        volume_map = {"1": 300, "2": 1000, "3": 5000, "4": 0}
        test_volume = volume_map.get(volume_choice, 1000)
        
        if test_volume == 0:
            test_volume = int(input("Enter number of records: ") or "1000")
        
        # Context for test data
        context_map = {
            "customer_service": DataContext.CUSTOMER_SERVICE,
            "healthcare": DataContext.HEALTHCARE,
            "e_commerce": DataContext.E_COMMERCE,
            "technology": DataContext.TECHNOLOGY,
            "education": DataContext.EDUCATION,
            "finance": DataContext.FINANCE
        }
        test_context = context_map.get(self.current_project["domain"], DataContext.TECHNOLOGY)
        
        self.current_project["test_requirements"] = {
            "data_types": selected_test_types,
            "volume": test_volume,
            "context": test_context
        }
        
        print(f"\n✅ Test requirements configured: {len(selected_test_types)} data types, {test_volume} records")
        return True
    
    def generate_project_files(self):
        """Generate all project files based on configuration"""
        print("\n🏗️  Generating your AI agent project files...")
        print()
        
        project_name = self.current_project["name"].replace(" ", "_").lower()
        project_dir = Path(f"generated_projects/{project_name}")
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate project structure
        self._generate_project_structure(project_dir)
        
        # Generate agent configurations
        self._generate_agent_configs(project_dir)
        
        # Generate schemas
        self._generate_schemas(project_dir)
        
        # Generate prompts
        self._generate_prompts(project_dir)
        
        # Generate test data
        self._generate_test_data(project_dir)
        
        # Generate MCP configurations
        self._generate_mcp_configs(project_dir)
        
        # Generate documentation
        self._generate_documentation(project_dir)
        
        # Generate setup files
        self._generate_setup_files(project_dir)
        
        print(f"\n✅ Project generated successfully in: {project_dir}")
        return str(project_dir)
    
    def _create_custom_agent_config(self, role_description: str):
        """Create custom agent configuration"""
        # Parse role description to extract subject, setting, style
        subject = SubjectDescriptor(
            subject_type=SubjectType.PERSONALITY,
            primary_subject=role_description,
            secondary_subjects=["helpful", "knowledgeable", "responsive"],
            intensity=0.8,
            confidence=0.7
        )
        
        setting = SettingDescriptor(
            setting_type=SettingType.ENVIRONMENT,
            primary_setting=f"AI agent environment for {self.current_project['domain']}",
            secondary_settings=["user interaction", "task execution", "data processing"],
            specificity=0.7,
            relevance=0.8
        )
        
        style = StyleDescriptor(
            style_type=StyleType.COMMUNICATION,
            primary_style=self.current_project.get("communication_style", "professional and helpful"),
            secondary_styles=["clear communication", "problem solving", "user assistance"],
            consistency=0.8,
            adaptability=0.7
        )
        
        return self.config_framework.create_agent_configuration(
            name=f"{self.current_project['name']} Agent",
            description=self.current_project['description'],
            subject=subject,
            setting=setting,
            style=style
        )
    
    def _generate_project_structure(self, project_dir: Path):
        """Generate basic project structure"""
        dirs = [
            "agents",
            "configs", 
            "schemas",
            "prompts",
            "test_data",
            "tests",
            "docs",
            "scripts"
        ]
        
        for dir_name in dirs:
            (project_dir / dir_name).mkdir(exist_ok=True)
        
        # Create __init__.py files
        for dir_name in dirs:
            init_file = project_dir / dir_name / "__init__.py"
            init_file.write_text('"""Generated AI Agent Project"""\n')
    
    def _generate_agent_configs(self, project_dir: Path):
        """Generate agent configuration files"""
        config_dir = project_dir / "configs"
        
        # Generate main agent config
        agent_config = self.config_framework.get_agent_by_id(self.current_project["agent_config_id"])
        if agent_config:
            config_data = {
                "agent": agent_config.dict(),
                "capabilities": self.current_project.get("capabilities", []),
                "communication_style": self.current_project.get("communication_style", "professional"),
                "integrations": self.current_project.get("integrations", [])
            }
            
            with open(config_dir / "agent_config.json", "w") as f:
                json.dump(config_data, f, indent=2, default=str)
        
        # Generate pattern-specific configs
        for pattern_name, pattern_id in self.current_project["selected_patterns"]:
            schema = self.schema_generator.generate_schema_for_pattern(pattern_id)
            if schema:
                with open(config_dir / f"{pattern_id}_config.json", "w") as f:
                    json.dump(schema, f, indent=2, default=str)
    
    def _generate_schemas(self, project_dir: Path):
        """Generate JSON schemas"""
        schema_dir = project_dir / "schemas"
        
        # Generate all pattern schemas
        all_schemas = self.schema_generator.get_pattern_schemas()
        with open(schema_dir / "all_patterns.json", "w") as f:
            json.dump(all_schemas, f, indent=2, default=str)
        
        # Generate selected pattern schemas
        selected_schemas = {}
        for pattern_name, pattern_id in self.current_project["selected_patterns"]:
            schema = self.schema_generator.generate_schema_for_pattern(pattern_id)
            if schema:
                selected_schemas[pattern_id] = schema
        
        with open(schema_dir / "selected_patterns.json", "w") as f:
            json.dump(selected_schemas, f, indent=2, default=str)
    
    def _generate_prompts(self, project_dir: Path):
        """Generate structured prompts"""
        prompt_dir = project_dir / "prompts"
        
        # Generate prompts for each pattern
        for pattern_name, pattern_id in self.current_project["selected_patterns"]:
            prompt_variables = {
                "agent_name": self.current_project["name"],
                "domain": self.current_project["domain"],
                "capabilities": ", ".join(self.current_project.get("capabilities", [])),
                "communication_style": self.current_project.get("communication_style", "professional")
            }
            
            # Create pattern-specific prompt
            prompt_id = self.prompt_framework.create_prompt_from_template(
                "task_execution", prompt_variables
            )
            prompt_text = self.prompt_framework.generate_prompt_text(prompt_id)
            
            with open(prompt_dir / f"{pattern_id}_prompt.txt", "w") as f:
                f.write(prompt_text)
        
        # Generate agent instructions
        agent_config = self.config_framework.get_agent_by_id(self.current_project["agent_config_id"])
        if agent_config:
            instructions = self.config_framework.generate_agent_instructions(self.current_project["agent_config_id"])
            with open(prompt_dir / "agent_instructions.md", "w") as f:
                f.write(instructions)
    
    def _generate_test_data(self, project_dir: Path):
        """Generate test data"""
        test_dir = project_dir / "test_data"
        test_requirements = self.current_project["test_requirements"]
        
        # Generate test data for each type
        for data_type in test_requirements["data_types"]:
            if data_type == "user_profiles":
                data = self.data_generator.generate_user_profiles(
                    test_requirements["volume"] // 10, test_requirements["context"]
                )
            elif data_type == "conversations":
                users = self.data_generator.generate_user_profiles(10, test_requirements["context"])
                data = self.data_generator.generate_conversations(
                    test_requirements["volume"] // 5, users, test_requirements["context"]
                )
            elif data_type == "tasks":
                data = self.data_generator.generate_tasks(
                    test_requirements["volume"] // 20, test_requirements["context"]
                )
            elif data_type == "events":
                users = self.data_generator.generate_user_profiles(10, test_requirements["context"])
                data = self.data_generator.generate_events(
                    test_requirements["volume"] // 10, users, test_requirements["context"]
                )
            elif data_type == "metrics":
                data = self.data_generator.generate_metrics(
                    test_requirements["volume"] // 50, test_requirements["context"]
                )
            elif data_type == "documents":
                data = self.data_generator.generate_documents(
                    test_requirements["volume"] // 100, test_requirements["context"]
                )
            else:
                continue
            
            # Save test data
            with open(test_dir / f"{data_type}.json", "w") as f:
                json.dump(data, f, indent=2, default=str)
    
    def _generate_mcp_configs(self, project_dir: Path):
        """Generate MCP configurations"""
        config_dir = project_dir / "configs"
        
        mcp_config = {
            "tools": self.current_project.get("integrations", []),
            "settings": {
                "timeout": 30,
                "retry_attempts": 3,
                "concurrent_requests": 10
            }
        }
        
        with open(config_dir / "mcp_config.json", "w") as f:
            json.dump(mcp_config, f, indent=2)
    
    def _generate_documentation(self, project_dir: Path):
        """Generate project documentation"""
        docs_dir = project_dir / "docs"
        
        # Generate README
        readme_content = f"""# {self.current_project['name']}

## Description
{self.current_project['description']}

## Domain
{self.current_project['domain'].replace('_', ' ').title()}

## Agent Patterns
{chr(10).join([f"- {name}" for name, _ in self.current_project['selected_patterns']])}

## Capabilities
{chr(10).join([f"- {cap}" for cap in self.current_project.get('capabilities', [])])}

## Communication Style
{self.current_project.get('communication_style', 'Professional')}

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Run the agent:
   ```bash
   python main.py
   ```

## Testing

Run tests with:
```bash
python -m pytest tests/
```

## Generated Files

- `configs/` - Agent configurations
- `schemas/` - JSON schemas for patterns
- `prompts/` - Structured prompts
- `test_data/` - Generated test data
- `tests/` - Test files
"""
        
        with open(project_dir / "README.md", "w") as f:
            f.write(readme_content)
    
    def _generate_setup_files(self, project_dir: Path):
        """Generate setup and configuration files"""
        # Generate requirements.txt
        requirements = [
            "pydantic>=2.0.0",
            "asyncio",
            "requests",
            "sqlite3",
            "pathlib",
            "datetime",
            "uuid",
            "json",
            "typing"
        ]
        
        with open(project_dir / "requirements.txt", "w") as f:
            f.write("\n".join(requirements))
        
        # Generate .env.example
        env_example = """# Agent Configuration
AGENT_NAME={agent_name}
AGENT_DESCRIPTION={agent_description}
AGENT_DOMAIN={domain}

# Database Configuration
DATABASE_URL=sqlite:///agent_data.db

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# MCP Configuration
MCP_TIMEOUT=30
MCP_RETRY_ATTEMPTS=3
""".format(
            agent_name=self.current_project['name'],
            agent_description=self.current_project['description'],
            domain=self.current_project['domain']
        )
        
        with open(project_dir / ".env.example", "w") as f:
            f.write(env_example)
        
        # Generate main.py
        main_py = f'''"""
{self.current_project['name']} - AI Agent Project
Generated by AI Agent Project Generator
"""

import asyncio
import json
from pathlib import Path
from configs.agent_config import agent_config
from schemas.selected_patterns import selected_patterns

async def main():
    """Main entry point for the agent"""
    print("🤖 Starting {self.current_project['name']} Agent")
    print("=" * 50)
    
    # Load agent configuration
    print(f"Agent: {{agent_config['agent']['name']}}")
    print(f"Description: {{agent_config['agent']['description']}}")
    print(f"Capabilities: {{', '.join(agent_config['capabilities'])}}")
    
    # Initialize agent patterns
    print("\\nInitializing agent patterns...")
    for pattern_name, pattern_id in selected_patterns.items():
        print(f"✅ {{pattern_name}} ({{pattern_id}})")
    
    print("\\n🚀 Agent is ready!")

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        with open(project_dir / "main.py", "w") as f:
            f.write(main_py)
    
    def run_interactive_generator(self):
        """Run the complete interactive generator"""
        self.welcome_message()
        
        try:
            # Step 1: Basic project info
            if not self.get_project_basic_info():
                return False
            
            # Step 2: Select patterns
            if not self.select_agent_patterns():
                return False
            
            # Step 3: Configure agent personality
            if not self.configure_agent_personality():
                return False
            
            # Step 4: Configure capabilities
            if not self.configure_agent_capabilities():
                return False
            
            # Step 5: Configure integrations
            if not self.configure_external_integrations():
                return False
            
            # Step 6: Configure testing
            if not self.configure_testing_requirements():
                return False
            
            # Step 7: Generate project
            project_path = self.generate_project_files()
            
            print("\n🎉 Project generation complete!")
            print(f"📁 Project location: {project_path}")
            print("\nNext steps:")
            print("1. Navigate to your project directory")
            print("2. Install dependencies: pip install -r requirements.txt")
            print("3. Configure environment variables: cp .env.example .env")
            print("4. Run your agent: python main.py")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n❌ Project generation cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Error during project generation: {e}")
            return False


def main():
    """Main entry point for the interactive generator"""
    generator = ProjectGeneratorUI()
    success = generator.run_interactive_generator()
    
    if success:
        print("\n✅ Thank you for using the AI Agent Project Generator!")
    else:
        print("\n❌ Project generation failed. Please try again.")


if __name__ == "__main__":
    main()
