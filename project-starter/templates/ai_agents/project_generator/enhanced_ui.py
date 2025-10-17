"""
Enhanced Developer UI for AI Agent Project Generation

This module provides an enhanced interactive interface that builds on the existing
project generator with better question flow, validation, and user experience.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import re

# Add parent directories to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

# Add the ai_agents directory to path
ai_agents_dir = current_dir.parent
sys.path.append(str(ai_agents_dir))

from schemas.agent_schemas import AgentSchemaGenerator
from mcp.mcp_framework import MCPFramework
from prompting.structured_prompts import PromptFramework, PromptType
from test_data.data_generator import TestDataGenerator, DataContext
from configuration.subject_setting_style import SubjectSettingStyleFramework, SubjectType, SettingType, StyleType


class EnhancedProjectGeneratorUI:
    """Enhanced interactive UI for generating AI agent projects"""
    
    def __init__(self):
        """Initialize the enhanced project generator UI"""
        self.schema_generator = AgentSchemaGenerator()
        self.mcp_framework = MCPFramework()
        self.prompt_framework = PromptFramework()
        self.data_generator = TestDataGenerator()
        self.config_framework = SubjectSettingStyleFramework()
        
        self.current_project = {}
        self.project_requirements = {}
        self.validation_errors = []
        
        # Project templates and presets
        self.project_templates = self._load_project_templates()
        self.domain_presets = self._load_domain_presets()
        
    def _load_project_templates(self):
        """Load predefined project templates"""
        return {
            "customer_service_bot": {
                "name": "Customer Service Bot",
                "description": "AI-powered customer service agent with empathy and problem-solving capabilities",
                "domain": "customer_service",
                "patterns": ["pattern_2", "pattern_3", "pattern_14", "pattern_16"],
                "capabilities": ["customer support", "problem solving", "empathy", "ticket management"],
                "communication_style": "empathetic and supportive",
                "integrations": ["database", "api", "file_processing"],
                "test_requirements": {
                    "data_types": ["user_profiles", "conversations", "tasks"],
                    "volume": 1000,
                    "context": "customer_service"
                }
            },
            "data_analyst_agent": {
                "name": "Data Analyst Agent",
                "description": "Intelligent data analysis agent with learning and optimization capabilities",
                "domain": "technology",
                "patterns": ["pattern_4", "pattern_8", "pattern_10", "pattern_15"],
                "capabilities": ["data analysis", "pattern recognition", "reporting", "optimization"],
                "communication_style": "technical and precise",
                "integrations": ["database", "api", "file_processing"],
                "test_requirements": {
                    "data_types": ["metrics", "documents", "events"],
                    "volume": 2000,
                    "context": "technology"
                }
            },
            "creative_writing_assistant": {
                "name": "Creative Writing Assistant",
                "description": "AI assistant for creative content generation with empathy and creativity",
                "domain": "education",
                "patterns": ["pattern_13", "pattern_14", "pattern_16", "pattern_19"],
                "capabilities": ["creative writing", "content generation", "style adaptation", "feedback"],
                "communication_style": "creative and engaging",
                "integrations": ["file_processing", "image_processing"],
                "test_requirements": {
                    "data_types": ["documents", "conversations", "sessions"],
                    "volume": 500,
                    "context": "education"
                }
            },
            "healthcare_assistant": {
                "name": "Healthcare Assistant",
                "description": "Medical AI assistant with empathy, ethics, and safety guardrails",
                "domain": "healthcare",
                "patterns": ["pattern_14", "pattern_16", "pattern_17", "pattern_18"],
                "capabilities": ["medical information", "patient support", "safety monitoring", "compliance"],
                "communication_style": "empathetic and supportive",
                "integrations": ["database", "api"],
                "test_requirements": {
                    "data_types": ["user_profiles", "conversations", "documents"],
                    "volume": 1000,
                    "context": "healthcare"
                }
            }
        }
    
    def _load_domain_presets(self):
        """Load domain-specific presets"""
        return {
            "customer_service": {
                "common_patterns": ["pattern_2", "pattern_3", "pattern_14", "pattern_16"],
                "common_capabilities": ["customer support", "problem solving", "empathy", "ticket management"],
                "communication_styles": ["empathetic and supportive", "professional and helpful"],
                "integrations": ["database", "api", "file_processing"]
            },
            "healthcare": {
                "common_patterns": ["pattern_14", "pattern_16", "pattern_17", "pattern_18"],
                "common_capabilities": ["medical information", "patient support", "safety monitoring"],
                "communication_styles": ["empathetic and supportive", "professional and precise"],
                "integrations": ["database", "api"]
            },
            "technology": {
                "common_patterns": ["pattern_4", "pattern_8", "pattern_10", "pattern_15"],
                "common_capabilities": ["data analysis", "problem solving", "optimization", "monitoring"],
                "communication_styles": ["technical and precise", "professional and clear"],
                "integrations": ["database", "api", "file_processing"]
            },
            "e_commerce": {
                "common_patterns": ["pattern_2", "pattern_3", "pattern_14", "pattern_15"],
                "common_capabilities": ["sales support", "product recommendations", "order management"],
                "communication_styles": ["friendly and helpful", "professional and persuasive"],
                "integrations": ["database", "api", "file_processing", "image_processing"]
            }
        }
    
    def welcome_message(self):
        """Display enhanced welcome message"""
        print("🚀 Welcome to the Enhanced AI Agent Project Generator!")
        print("=" * 60)
        print("This intelligent tool will guide you through creating")
        print("sophisticated AI agent projects using our data-driven frameworks.")
        print()
        print("✨ Features:")
        print("• Smart project templates and presets")
        print("• Real-time validation and suggestions")
        print("• Domain-specific recommendations")
        print("• Advanced configuration options")
        print("• Export to multiple deployment formats")
        print()
        print("🎯 What we'll generate for you:")
        print("• Agent configurations using Subject-Setting-Style framework")
        print("• Structured prompts for agent behavior")
        print("• Realistic test data for validation")
        print("• MCP tool integrations for external services")
        print("• JSON schemas for pattern validation")
        print("• Complete project structure with documentation")
        print()
    
    def get_project_creation_mode(self):
        """Get the project creation mode"""
        print("🎯 How would you like to create your project?")
        print()
        print("1. 🚀 Quick Start (Use a template)")
        print("2. 🎨 Custom Build (Build from scratch)")
        print("3. 🔍 Guided Wizard (Step-by-step with recommendations)")
        print("4. 📋 Import Configuration (Load from file)")
        print()
        
        while True:
            choice = input("Choose your mode (1-4): ").strip()
            if choice in ["1", "2", "3", "4"]:
                return choice
            print("❌ Please enter a valid choice (1-4)")
    
    def quick_start_template_selection(self):
        """Handle quick start template selection"""
        print("\n🚀 Quick Start - Choose a Template")
        print("=" * 40)
        print()
        
        templates = list(self.project_templates.items())
        for i, (template_id, template) in enumerate(templates, 1):
            print(f"{i}. {template['name']}")
            print(f"   {template['description']}")
            print(f"   Domain: {template['domain'].replace('_', ' ').title()}")
            print(f"   Patterns: {len(template['patterns'])} selected")
            print()
        
        while True:
            try:
                choice = int(input("Select a template (1-{}): ".format(len(templates))))
                if 1 <= choice <= len(templates):
                    template_id, template = templates[choice - 1]
                    self.current_project = template.copy()
                    self.current_project["template_id"] = template_id
                    print(f"\n✅ Selected: {template['name']}")
                    return True
                else:
                    print("❌ Please enter a number between 1 and {}".format(len(templates)))
            except ValueError:
                print("❌ Please enter a valid number")
    
    def guided_wizard(self):
        """Run the guided wizard with smart recommendations"""
        print("\n🔍 Guided Wizard - Let's Build Your Perfect Agent")
        print("=" * 55)
        print()
        
        # Step 1: Basic Info with validation
        if not self._get_basic_info_with_validation():
            return False
        
        # Step 2: Domain-specific recommendations
        if not self._apply_domain_recommendations():
            return False
        
        # Step 3: Pattern selection with recommendations
        if not self._select_patterns_with_recommendations():
            return False
        
        # Step 4: Agent configuration with templates
        if not self._configure_agent_with_templates():
            return False
        
        # Step 5: Capabilities with smart suggestions
        if not self._configure_capabilities_with_suggestions():
            return False
        
        # Step 6: Integrations with recommendations
        if not self._configure_integrations_with_recommendations():
            return False
        
        # Step 7: Testing with smart defaults
        if not self._configure_testing_with_smart_defaults():
            return False
        
        return True
    
    def _get_basic_info_with_validation(self):
        """Get basic project info with validation"""
        print("📋 Step 1: Basic Project Information")
        print("-" * 35)
        print()
        
        # Project name with validation
        while True:
            project_name = input("What would you like to name your project? ").strip()
            if self._validate_project_name(project_name):
                break
            print("❌ " + self.validation_errors[-1])
        
        # Project description with validation
        while True:
            print("\nDescribe what your AI agent project will do:")
            project_description = input("> ").strip()
            if self._validate_project_description(project_description):
                break
            print("❌ " + self.validation_errors[-1])
        
        # Domain selection with recommendations
        print("\nWhat domain will your agent operate in?")
        domains = [
            ("1", "Customer Service", "Customer support and service"),
            ("2", "Healthcare", "Medical and health-related services"),
            ("3", "E-commerce", "Online retail and shopping"),
            ("4", "Technology", "Software and tech development"),
            ("5", "Education", "Learning and educational services"),
            ("6", "Finance", "Financial services and banking"),
            ("7", "Other", "Custom domain")
        ]
        
        for num, name, desc in domains:
            print(f"{num}. {name} - {desc}")
        
        while True:
            domain_choice = input("\nChoose a domain (1-7): ").strip()
            if domain_choice in [d[0] for d in domains]:
                domain_map = {
                    "1": "customer_service", "2": "healthcare", "3": "e_commerce",
                    "4": "technology", "5": "education", "6": "finance", "7": "other"
                }
                project_domain = domain_map[domain_choice]
                break
            print("❌ Please enter a valid choice (1-7)")
        
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
    
    def _validate_project_name(self, name):
        """Validate project name"""
        if not name:
            self.validation_errors.append("Project name cannot be empty")
            return False
        
        if len(name) < 3:
            self.validation_errors.append("Project name must be at least 3 characters")
            return False
        
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
            self.validation_errors.append("Project name can only contain letters, numbers, spaces, hyphens, and underscores")
            return False
        
        return True
    
    def _validate_project_description(self, description):
        """Validate project description"""
        if not description:
            self.validation_errors.append("Project description cannot be empty")
            return False
        
        if len(description) < 10:
            self.validation_errors.append("Project description must be at least 10 characters")
            return False
        
        return True
    
    def _apply_domain_recommendations(self):
        """Apply domain-specific recommendations"""
        print("\n🎯 Step 2: Domain-Specific Recommendations")
        print("-" * 45)
        print()
        
        domain = self.current_project["domain"]
        if domain in self.domain_presets:
            preset = self.domain_presets[domain]
            print(f"💡 Based on the {domain.replace('_', ' ')} domain, I recommend:")
            print()
            print("🔧 Common Patterns:")
            for pattern in preset["common_patterns"]:
                pattern_name = self._get_pattern_name(pattern)
                print(f"   • {pattern_name}")
            print()
            print("⚡ Common Capabilities:")
            for capability in preset["common_capabilities"]:
                print(f"   • {capability}")
            print()
            print("💬 Communication Styles:")
            for style in preset["communication_styles"]:
                print(f"   • {style}")
            print()
            print("🔗 Recommended Integrations:")
            for integration in preset["integrations"]:
                print(f"   • {integration}")
            print()
            
            apply = input("Would you like to apply these recommendations? (y/n): ").strip().lower()
            if apply == 'y':
                self.current_project["recommended_patterns"] = preset["common_patterns"]
                self.current_project["recommended_capabilities"] = preset["common_capabilities"]
                self.current_project["recommended_communication_style"] = preset["communication_styles"][0]
                self.current_project["recommended_integrations"] = preset["integrations"]
                print("✅ Recommendations applied!")
            else:
                print("ℹ️  You can customize these later")
        else:
            print(f"ℹ️  No specific recommendations for '{domain}' domain")
        
        return True
    
    def _get_pattern_name(self, pattern_id):
        """Get human-readable pattern name"""
        pattern_names = {
            "pattern_1": "Multi-Agent Orchestration",
            "pattern_2": "Agent Communication",
            "pattern_3": "Agent Collaboration",
            "pattern_4": "Agent Learning",
            "pattern_8": "Memory Management",
            "pattern_10": "Goal Setting & Monitoring",
            "pattern_11": "Exception Handling & Recovery",
            "pattern_12": "Agent Adaptation",
            "pattern_13": "Agent Creativity",
            "pattern_14": "Agent Empathy",
            "pattern_15": "Resource-Aware Optimization",
            "pattern_16": "Agent Ethics",
            "pattern_17": "Evaluation & Monitoring",
            "pattern_18": "Guardrails & Safety",
            "pattern_19": "Agent Evolution",
            "pattern_20": "Agent Swarming"
        }
        return pattern_names.get(pattern_id, pattern_id)
    
    def _select_patterns_with_recommendations(self):
        """Select patterns with smart recommendations"""
        print("\n🤖 Step 3: Agent Pattern Selection")
        print("-" * 35)
        print()
        
        # Show all available patterns
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
            recommended = ""
            if "recommended_patterns" in self.current_project:
                pattern_id = patterns[key][1]
                if pattern_id in self.current_project["recommended_patterns"]:
                    recommended = " ⭐ (Recommended)"
            print(f"{key}. {name}{recommended}")
        
        print("\nOptions:")
        print("• Enter numbers separated by commas (e.g., '1,3,5')")
        print("• Type 'recommended' to use domain recommendations")
        print("• Type 'all' to select all patterns")
        print("• Type 'help' for pattern descriptions")
        
        while True:
            selection = input("\nYour selection: ").strip().lower()
            
            if selection == "help":
                self._show_pattern_help()
                continue
            elif selection == "recommended":
                if "recommended_patterns" in self.current_project:
                    selected_patterns = [(self._get_pattern_name(p), p) for p in self.current_project["recommended_patterns"]]
                    print("✅ Using recommended patterns")
                    break
                else:
                    print("❌ No recommendations available for this domain")
                    continue
            elif selection == "all":
                selected_patterns = list(patterns.values())
                print("✅ All patterns selected")
                break
            else:
                try:
                    indices = [x.strip() for x in selection.split(",")]
                    selected_patterns = []
                    for idx in indices:
                        if idx in patterns:
                            selected_patterns.append(patterns[idx])
                        else:
                            print(f"❌ Invalid pattern number: {idx}")
                            break
                    else:
                        print(f"✅ Selected {len(selected_patterns)} patterns")
                        break
                except:
                    print("❌ Invalid selection format")
                    continue
        
        self.current_project["selected_patterns"] = selected_patterns
        return True
    
    def _show_pattern_help(self):
        """Show detailed pattern help"""
        print("\n📚 Pattern Descriptions:")
        print("-" * 25)
        patterns = {
            "Multi-Agent Orchestration": "Coordinate multiple agents working together",
            "Agent Communication": "Handle message passing between agents",
            "Agent Collaboration": "Enable agents to work on shared tasks",
            "Agent Learning": "Allow agents to learn from experience",
            "Memory Management": "Persistent memory and context management",
            "Goal Setting & Monitoring": "Track and manage agent objectives",
            "Exception Handling & Recovery": "Robust error handling and recovery",
            "Agent Adaptation": "Dynamic behavior modification",
            "Agent Creativity": "Creative problem-solving capabilities",
            "Agent Empathy": "Emotional intelligence and user understanding",
            "Resource-Aware Optimization": "Monitor and optimize resource usage",
            "Agent Ethics": "Ethical decision-making framework",
            "Evaluation & Monitoring": "Performance evaluation and monitoring",
            "Guardrails & Safety": "Safety constraints and content moderation",
            "Agent Evolution": "Adaptive learning and self-improvement",
            "Agent Swarming": "Coordinated multi-agent behavior"
        }
        
        for name, desc in patterns.items():
            print(f"• {name}: {desc}")
        print()
    
    def _configure_agent_with_templates(self):
        """Configure agent using templates"""
        print("\n🎭 Step 4: Agent Configuration")
        print("-" * 30)
        print()
        
        # Show available templates
        templates = self.config_framework.get_available_templates()
        print("Available agent templates:")
        for i, template in enumerate(templates, 1):
            template_info = self.config_framework.templates[template]
            print(f"{i}. {template.replace('_', ' ').title()}")
            print(f"   {template_info['description']}")
        
        print(f"\n{len(templates) + 1}. Custom Agent (Build from scratch)")
        
        while True:
            try:
                choice = int(input(f"\nChoose a template (1-{len(templates) + 1}): "))
                if 1 <= choice <= len(templates):
                    template_name = templates[choice - 1]
                    agent_config = self.config_framework.create_from_template(template_name, {
                        "name": f"{self.current_project['name']} Agent",
                        "description": self.current_project['description']
                    })
                    break
                elif choice == len(templates) + 1:
                    agent_config = self._create_custom_agent_config()
                    break
                else:
                    print("❌ Please enter a valid choice")
            except ValueError:
                print("❌ Please enter a valid number")
        
        self.current_project["agent_config_id"] = agent_config
        
        # Show photographic prompt
        prompt = self.config_framework.generate_photographic_prompt(agent_config)
        print(f"\n📸 Your agent's photographic description:")
        print(f"   {prompt}")
        
        return True
    
    def _create_custom_agent_config(self):
        """Create custom agent configuration"""
        print("\n🎨 Custom Agent Configuration")
        print("-" * 30)
        
        # Get custom role
        role = input("What is the primary role of your agent? ").strip()
        while not role:
            role = input("Please enter a role: ").strip()
        
        # Get personality traits
        print("\nWhat are the key personality traits? (comma-separated)")
        traits = input("> ").strip()
        if not traits:
            traits = "helpful, knowledgeable, responsive"
        
        # Get communication style
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
        
        # Create custom configuration
        from project_starter.templates.ai_agents.configuration.subject_setting_style import SubjectDescriptor, SettingDescriptor, StyleDescriptor
        
        subject = SubjectDescriptor(
            subject_type=SubjectType.PERSONALITY,
            primary_subject=role,
            secondary_subjects=[t.strip() for t in traits.split(",")],
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
            primary_style=comm_style,
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
    
    def _configure_capabilities_with_suggestions(self):
        """Configure capabilities with smart suggestions"""
        print("\n⚡ Step 5: Agent Capabilities")
        print("-" * 30)
        print()
        
        # Show recommended capabilities if available
        if "recommended_capabilities" in self.current_project:
            print("💡 Recommended capabilities for your domain:")
            for cap in self.current_project["recommended_capabilities"]:
                print(f"   • {cap}")
            print()
        
        # Get core capabilities
        print("What are the core capabilities your agent needs?")
        print("(Enter multiple capabilities separated by commas)")
        print("Examples: problem solving, data analysis, creative writing, customer support")
        
        core_caps = input("Core capabilities: ").strip()
        if not core_caps and "recommended_capabilities" in self.current_project:
            core_caps = ", ".join(self.current_project["recommended_capabilities"])
            print(f"Using recommended: {core_caps}")
        
        capabilities = [cap.strip() for cap in core_caps.split(",") if cap.strip()]
        
        # Get technical capabilities
        print("\nWhat technical capabilities are required?")
        print("Examples: API integration, database access, file processing, web scraping")
        
        tech_caps = input("Technical capabilities: ").strip()
        if tech_caps:
            capabilities.extend([cap.strip() for cap in tech_caps.split(",") if cap.strip()])
        
        self.current_project["capabilities"] = capabilities
        
        # Set communication style
        if "recommended_communication_style" in self.current_project:
            comm_style = self.current_project["recommended_communication_style"]
            print(f"\nUsing recommended communication style: {comm_style}")
        else:
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
        
        self.current_project["communication_style"] = comm_style
        
        print(f"\n✅ Agent capabilities configured: {len(capabilities)} capabilities, {comm_style} style")
        return True
    
    def _configure_integrations_with_recommendations(self):
        """Configure integrations with recommendations"""
        print("\n🔗 Step 6: External Integrations")
        print("-" * 35)
        print()
        
        # Show recommended integrations if available
        if "recommended_integrations" in self.current_project:
            print("💡 Recommended integrations for your domain:")
            for integration in self.current_project["recommended_integrations"]:
                print(f"   • {integration}")
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
    
    def _configure_testing_with_smart_defaults(self):
        """Configure testing with smart defaults"""
        print("\n🧪 Step 7: Testing & Validation")
        print("-" * 30)
        print()
        
        # Smart defaults based on domain
        domain = self.current_project["domain"]
        smart_defaults = {
            "customer_service": {
                "data_types": ["user_profiles", "conversations", "tasks"],
                "volume": 1000
            },
            "healthcare": {
                "data_types": ["user_profiles", "conversations", "documents"],
                "volume": 1000
            },
            "technology": {
                "data_types": ["metrics", "documents", "events"],
                "volume": 2000
            },
            "e_commerce": {
                "data_types": ["user_profiles", "conversations", "tasks", "events"],
                "volume": 1500
            }
        }
        
        if domain in smart_defaults:
            defaults = smart_defaults[domain]
            print(f"💡 Smart defaults for {domain} domain:")
            print(f"   Data types: {', '.join(defaults['data_types'])}")
            print(f"   Volume: {defaults['volume']} records")
            print()
            
            use_defaults = input("Use these smart defaults? (y/n): ").strip().lower()
            if use_defaults == 'y':
                selected_test_types = defaults["data_types"]
                test_volume = defaults["volume"]
            else:
                selected_test_types, test_volume = self._get_custom_test_requirements()
        else:
            selected_test_types, test_volume = self._get_custom_test_requirements()
        
        # Context mapping
        context_map = {
            "customer_service": DataContext.CUSTOMER_SERVICE,
            "healthcare": DataContext.HEALTHCARE,
            "e_commerce": DataContext.E_COMMERCE,
            "technology": DataContext.TECHNOLOGY,
            "education": DataContext.EDUCATION,
            "finance": DataContext.FINANCE
        }
        test_context = context_map.get(domain, DataContext.TECHNOLOGY)
        
        self.current_project["test_requirements"] = {
            "data_types": selected_test_types,
            "volume": test_volume,
            "context": test_context
        }
        
        print(f"\n✅ Test requirements configured: {len(selected_test_types)} data types, {test_volume} records")
        return True
    
    def _get_custom_test_requirements(self):
        """Get custom test requirements"""
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
        
        return selected_test_types, test_volume
    
    def generate_project_files(self):
        """Generate all project files with enhanced features"""
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
        
        # Generate deployment configurations
        self._generate_deployment_configs(project_dir)
        
        print(f"\n✅ Project generated successfully in: {project_dir}")
        return str(project_dir)
    
    def _generate_deployment_configs(self, project_dir: Path):
        """Generate deployment configurations"""
        deploy_dir = project_dir / "deployment"
        deploy_dir.mkdir(exist_ok=True)
        
        # Docker configuration
        dockerfile_content = f"""FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p data

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
"""
        
        with open(deploy_dir / "Dockerfile", "w") as f:
            f.write(dockerfile_content)
        
        # Docker Compose
        docker_compose_content = f"""version: '3.8'

services:
  {self.current_project['name'].replace(' ', '_').lower()}-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - AGENT_NAME={self.current_project['name']}
      - AGENT_DESCRIPTION={self.current_project['description']}
      - AGENT_DOMAIN={self.current_project['domain']}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
"""
        
        with open(deploy_dir / "docker-compose.yml", "w") as f:
            f.write(docker_compose_content)
        
        # Kubernetes deployment
        k8s_deployment_content = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {self.current_project['name'].replace(' ', '-').lower()}-agent
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {self.current_project['name'].replace(' ', '-').lower()}-agent
  template:
    metadata:
      labels:
        app: {self.current_project['name'].replace(' ', '-').lower()}-agent
    spec:
      containers:
      - name: agent
        image: {self.current_project['name'].replace(' ', '-').lower()}-agent:latest
        ports:
        - containerPort: 8000
        env:
        - name: AGENT_NAME
          value: "{self.current_project['name']}"
        - name: AGENT_DESCRIPTION
          value: "{self.current_project['description']}"
        - name: AGENT_DOMAIN
          value: "{self.current_project['domain']}"
---
apiVersion: v1
kind: Service
metadata:
  name: {self.current_project['name'].replace(' ', '-').lower()}-agent-service
spec:
  selector:
    app: {self.current_project['name'].replace(' ', '-').lower()}-agent
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
"""
        
        with open(deploy_dir / "k8s-deployment.yaml", "w") as f:
            f.write(k8s_deployment_content)
        
        print("✅ Deployment configurations generated")
    
    def run_enhanced_generator(self):
        """Run the enhanced interactive generator"""
        self.welcome_message()
        
        try:
            # Get creation mode
            mode = self.get_project_creation_mode()
            
            if mode == "1":  # Quick Start
                if not self.quick_start_template_selection():
                    return False
            elif mode == "2":  # Custom Build
                if not self._get_basic_info_with_validation():
                    return False
                if not self._select_patterns_with_recommendations():
                    return False
                if not self._configure_agent_with_templates():
                    return False
                if not self._configure_capabilities_with_suggestions():
                    return False
                if not self._configure_integrations_with_recommendations():
                    return False
                if not self._configure_testing_with_smart_defaults():
                    return False
            elif mode == "3":  # Guided Wizard
                if not self.guided_wizard():
                    return False
            elif mode == "4":  # Import Configuration
                print("📋 Import Configuration feature coming soon!")
                return False
            
            # Generate project
            project_path = self.generate_project_files()
            
            print("\n🎉 Project generation complete!")
            print(f"📁 Project location: {project_path}")
            print("\nNext steps:")
            print("1. Navigate to your project directory")
            print("2. Install dependencies: pip install -r requirements.txt")
            print("3. Configure environment variables: cp .env.example .env")
            print("4. Run your agent: python main.py")
            print("5. Deploy with Docker: cd deployment && docker-compose up")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n❌ Project generation cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Error during project generation: {e}")
            return False


def main():
    """Main entry point for the enhanced generator"""
    generator = EnhancedProjectGeneratorUI()
    success = generator.run_enhanced_generator()
    
    if success:
        print("\n✅ Thank you for using the Enhanced AI Agent Project Generator!")
    else:
        print("\n❌ Project generation failed. Please try again.")


if __name__ == "__main__":
    main()
