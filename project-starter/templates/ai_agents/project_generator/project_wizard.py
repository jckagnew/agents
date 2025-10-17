"""
Project Wizard for AI Agent Project Generation

This module provides a step-by-step wizard that guides users through
creating AI agent projects with intelligent recommendations and validation.
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


class ProjectWizard:
    """Step-by-step project wizard with intelligent guidance"""
    
    def __init__(self):
        """Initialize the project wizard"""
        self.schema_generator = AgentSchemaGenerator()
        self.mcp_framework = MCPFramework()
        self.prompt_framework = PromptFramework()
        self.data_generator = TestDataGenerator()
        self.config_framework = SubjectSettingStyleFramework()
        
        self.current_project = {}
        self.wizard_state = {
            "current_step": 0,
            "total_steps": 8,
            "completed_steps": [],
            "validation_errors": [],
            "recommendations": {}
        }
        
        # Step definitions
        self.steps = [
            self._step_welcome,
            self._step_project_basics,
            self._step_domain_analysis,
            self._step_pattern_selection,
            self._step_agent_configuration,
            self._step_capabilities_definition,
            self._step_integrations_setup,
            self._step_testing_configuration,
            self._step_project_generation
        ]
        
        # Domain intelligence
        self.domain_intelligence = self._load_domain_intelligence()
        
    def _load_domain_intelligence(self):
        """Load domain-specific intelligence and recommendations"""
        return {
            "customer_service": {
                "description": "Customer support and service automation",
                "key_patterns": ["pattern_2", "pattern_3", "pattern_14", "pattern_16"],
                "essential_capabilities": ["empathy", "problem solving", "ticket management", "escalation handling"],
                "communication_style": "empathetic and supportive",
                "common_integrations": ["database", "api", "file_processing"],
                "test_data_focus": ["conversations", "user_profiles", "tasks"],
                "success_metrics": ["customer satisfaction", "resolution time", "first contact resolution"],
                "challenges": ["emotional intelligence", "context understanding", "escalation decisions"],
                "best_practices": [
                    "Always acknowledge customer emotions",
                    "Provide clear next steps",
                    "Know when to escalate to humans",
                    "Maintain conversation context"
                ]
            },
            "healthcare": {
                "description": "Medical and health-related AI assistance",
                "key_patterns": ["pattern_14", "pattern_16", "pattern_17", "pattern_18"],
                "essential_capabilities": ["medical knowledge", "safety monitoring", "compliance", "privacy protection"],
                "communication_style": "empathetic and precise",
                "common_integrations": ["database", "api"],
                "test_data_focus": ["user_profiles", "conversations", "documents"],
                "success_metrics": ["patient safety", "accuracy", "compliance", "user trust"],
                "challenges": ["medical accuracy", "regulatory compliance", "privacy protection", "liability"],
                "best_practices": [
                    "Always include medical disclaimers",
                    "Protect patient privacy rigorously",
                    "Know when to defer to medical professionals",
                    "Maintain audit trails"
                ]
            },
            "technology": {
                "description": "Software development and technical assistance",
                "key_patterns": ["pattern_4", "pattern_8", "pattern_10", "pattern_15"],
                "essential_capabilities": ["code analysis", "problem solving", "optimization", "monitoring"],
                "communication_style": "technical and precise",
                "common_integrations": ["database", "api", "file_processing"],
                "test_data_focus": ["metrics", "documents", "events"],
                "success_metrics": ["code quality", "performance", "bug reduction", "developer productivity"],
                "challenges": ["code complexity", "performance optimization", "security", "scalability"],
                "best_practices": [
                    "Provide clear code explanations",
                    "Suggest best practices",
                    "Consider security implications",
                    "Optimize for performance"
                ]
            },
            "e_commerce": {
                "description": "Online retail and shopping assistance",
                "key_patterns": ["pattern_2", "pattern_3", "pattern_14", "pattern_15"],
                "essential_capabilities": ["product knowledge", "recommendations", "order management", "customer service"],
                "communication_style": "friendly and helpful",
                "common_integrations": ["database", "api", "file_processing", "image_processing"],
                "test_data_focus": ["user_profiles", "conversations", "tasks", "events"],
                "success_metrics": ["conversion rate", "customer satisfaction", "average order value", "return rate"],
                "challenges": ["product recommendations", "inventory management", "customer preferences", "seasonal trends"],
                "best_practices": [
                    "Personalize recommendations",
                    "Provide clear product information",
                    "Handle returns and refunds gracefully",
                    "Maintain shopping cart context"
                ]
            },
            "education": {
                "description": "Learning and educational assistance",
                "key_patterns": ["pattern_4", "pattern_13", "pattern_14", "pattern_16"],
                "essential_capabilities": ["content generation", "adaptive learning", "assessment", "feedback"],
                "communication_style": "encouraging and clear",
                "common_integrations": ["file_processing", "image_processing"],
                "test_data_focus": ["documents", "conversations", "sessions"],
                "success_metrics": ["learning outcomes", "engagement", "completion rate", "knowledge retention"],
                "challenges": ["learning personalization", "content quality", "assessment accuracy", "motivation"],
                "best_practices": [
                    "Adapt to learning styles",
                    "Provide constructive feedback",
                    "Encourage progress",
                    "Make learning engaging"
                ]
            },
            "finance": {
                "description": "Financial services and banking assistance",
                "key_patterns": ["pattern_16", "pattern_17", "pattern_18", "pattern_15"],
                "essential_capabilities": ["financial analysis", "risk assessment", "compliance", "security"],
                "communication_style": "professional and precise",
                "common_integrations": ["database", "api"],
                "test_data_focus": ["user_profiles", "documents", "events"],
                "success_metrics": ["accuracy", "compliance", "security", "user trust"],
                "challenges": ["regulatory compliance", "data security", "risk management", "fraud detection"],
                "best_practices": [
                    "Maintain strict security standards",
                    "Ensure regulatory compliance",
                    "Provide clear financial advice",
                    "Protect sensitive data"
                ]
            }
        }
    
    def run_wizard(self):
        """Run the complete project wizard"""
        try:
            for step_func in self.steps:
                if not step_func():
                    print("\n❌ Wizard cancelled by user")
                    return False
                self.wizard_state["current_step"] += 1
                self.wizard_state["completed_steps"].append(step_func.__name__)
            
            print("\n🎉 Project wizard completed successfully!")
            return True
            
        except KeyboardInterrupt:
            print("\n\n❌ Wizard cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Error in wizard: {e}")
            return False
    
    def _step_welcome(self):
        """Step 1: Welcome and introduction"""
        print("🧙‍♂️ AI Agent Project Wizard")
        print("=" * 50)
        print()
        print("Welcome to the intelligent project wizard!")
        print("I'll guide you through creating a sophisticated AI agent project")
        print("with smart recommendations and best practices.")
        print()
        print("✨ What makes this wizard special:")
        print("• Domain-specific intelligence and recommendations")
        print("• Real-time validation and error prevention")
        print("• Best practices from industry experts")
        print("• Smart defaults based on your choices")
        print("• Complete project generation with deployment configs")
        print()
        print(f"📊 Progress: {self.wizard_state['current_step'] + 1}/{self.wizard_state['total_steps']} steps")
        print()
        
        input("Press Enter to begin your AI agent journey...")
        return True
    
    def _step_project_basics(self):
        """Step 2: Project basics with validation"""
        print("\n📋 Step 2: Project Basics")
        print("=" * 30)
        print()
        
        # Project name with validation
        while True:
            project_name = input("What would you like to name your project? ").strip()
            if self._validate_project_name(project_name):
                break
            print(f"❌ {self.wizard_state['validation_errors'][-1]}")
        
        # Project description with validation
        while True:
            print("\nDescribe what your AI agent project will do:")
            print("💡 Tip: Be specific about the agent's purpose and target users")
            project_description = input("> ").strip()
            if self._validate_project_description(project_description):
                break
            print(f"❌ {self.wizard_state['validation_errors'][-1]}")
        
        # Domain selection with intelligence
        print("\nWhat domain will your agent operate in?")
        domains = [
            ("1", "Customer Service", "Customer support and service automation"),
            ("2", "Healthcare", "Medical and health-related assistance"),
            ("3", "Technology", "Software development and technical assistance"),
            ("4", "E-commerce", "Online retail and shopping assistance"),
            ("5", "Education", "Learning and educational assistance"),
            ("6", "Finance", "Financial services and banking assistance"),
            ("7", "Other", "Custom domain")
        ]
        
        for num, name, desc in domains:
            print(f"{num}. {name} - {desc}")
        
        while True:
            domain_choice = input("\nChoose a domain (1-7): ").strip()
            if domain_choice in [d[0] for d in domains]:
                domain_map = {
                    "1": "customer_service", "2": "healthcare", "3": "technology",
                    "4": "e_commerce", "5": "education", "6": "finance", "7": "other"
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
    
    def _step_domain_analysis(self):
        """Step 3: Domain analysis and recommendations"""
        print("\n🔍 Step 3: Domain Analysis")
        print("=" * 30)
        print()
        
        domain = self.current_project["domain"]
        
        if domain in self.domain_intelligence:
            intelligence = self.domain_intelligence[domain]
            
            print(f"🎯 Analyzing {domain.replace('_', ' ').title()} Domain")
            print("-" * 40)
            print()
            print(f"📝 Description: {intelligence['description']}")
            print()
            print("🔧 Key Patterns for this domain:")
            for pattern in intelligence["key_patterns"]:
                pattern_name = self._get_pattern_name(pattern)
                print(f"   • {pattern_name}")
            print()
            print("⚡ Essential Capabilities:")
            for capability in intelligence["essential_capabilities"]:
                print(f"   • {capability}")
            print()
            print("💬 Recommended Communication Style:")
            print(f"   • {intelligence['communication_style']}")
            print()
            print("🔗 Common Integrations:")
            for integration in intelligence["common_integrations"]:
                print(f"   • {integration}")
            print()
            print("📊 Success Metrics to Track:")
            for metric in intelligence["success_metrics"]:
                print(f"   • {metric}")
            print()
            print("⚠️  Key Challenges:")
            for challenge in intelligence["challenges"]:
                print(f"   • {challenge}")
            print()
            print("💡 Best Practices:")
            for practice in intelligence["best_practices"]:
                print(f"   • {practice}")
            print()
            
            # Store recommendations
            self.wizard_state["recommendations"] = {
                "patterns": intelligence["key_patterns"],
                "capabilities": intelligence["essential_capabilities"],
                "communication_style": intelligence["communication_style"],
                "integrations": intelligence["common_integrations"],
                "test_data_focus": intelligence["test_data_focus"],
                "success_metrics": intelligence["success_metrics"]
            }
            
            print("✅ Domain analysis complete! I'll use these insights to guide your project.")
        else:
            print(f"ℹ️  No specific intelligence available for '{domain}' domain")
            print("I'll provide general recommendations based on best practices.")
        
        input("\nPress Enter to continue...")
        return True
    
    def _step_pattern_selection(self):
        """Step 4: Pattern selection with recommendations"""
        print("\n🤖 Step 4: Agent Pattern Selection")
        print("=" * 40)
        print()
        
        # Show all available patterns
        patterns = {
            "1": ("Multi-Agent Orchestration", "pattern_1", "Coordinate multiple agents working together"),
            "2": ("Agent Communication", "pattern_2", "Handle message passing between agents"),
            "3": ("Agent Collaboration", "pattern_3", "Enable agents to work on shared tasks"),
            "4": ("Agent Learning", "pattern_4", "Allow agents to learn from experience"),
            "5": ("Memory Management", "pattern_8", "Persistent memory and context management"),
            "6": ("Goal Setting & Monitoring", "pattern_10", "Track and manage agent objectives"),
            "7": ("Exception Handling & Recovery", "pattern_11", "Robust error handling and recovery"),
            "8": ("Agent Adaptation", "pattern_12", "Dynamic behavior modification"),
            "9": ("Agent Creativity", "pattern_13", "Creative problem-solving capabilities"),
            "10": ("Agent Empathy", "pattern_14", "Emotional intelligence and user understanding"),
            "11": ("Resource-Aware Optimization", "pattern_15", "Monitor and optimize resource usage"),
            "12": ("Agent Ethics", "pattern_16", "Ethical decision-making framework"),
            "13": ("Evaluation & Monitoring", "pattern_17", "Performance evaluation and monitoring"),
            "14": ("Guardrails & Safety", "pattern_18", "Safety constraints and content moderation"),
            "15": ("Agent Evolution", "pattern_19", "Adaptive learning and self-improvement"),
            "16": ("Agent Swarming", "pattern_20", "Coordinated multi-agent behavior")
        }
        
        print("Available patterns:")
        for key, (name, pattern_id, description) in patterns.items():
            recommended = ""
            if "recommendations" in self.wizard_state and pattern_id in self.wizard_state["recommendations"].get("patterns", []):
                recommended = " ⭐ (Recommended for your domain)"
            print(f"{key}. {name}{recommended}")
            print(f"   {description}")
            print()
        
        print("Options:")
        print("• Enter numbers separated by commas (e.g., '1,3,5')")
        print("• Type 'recommended' to use domain recommendations")
        print("• Type 'all' to select all patterns")
        print("• Type 'help' for detailed pattern information")
        
        while True:
            selection = input("\nYour selection: ").strip().lower()
            
            if selection == "help":
                self._show_detailed_pattern_help()
                continue
            elif selection == "recommended":
                if "recommendations" in self.wizard_state and "patterns" in self.wizard_state["recommendations"]:
                    recommended_patterns = self.wizard_state["recommendations"]["patterns"]
                    selected_patterns = [(self._get_pattern_name(p), p) for p in recommended_patterns]
                    print("✅ Using domain-recommended patterns")
                    break
                else:
                    print("❌ No recommendations available for this domain")
                    continue
            elif selection == "all":
                selected_patterns = [(name, pattern_id) for name, pattern_id, _ in patterns.values()]
                print("✅ All patterns selected")
                break
            else:
                try:
                    indices = [x.strip() for x in selection.split(",")]
                    selected_patterns = []
                    for idx in indices:
                        if idx in patterns:
                            name, pattern_id, _ = patterns[idx]
                            selected_patterns.append((name, pattern_id))
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
    
    def _show_detailed_pattern_help(self):
        """Show detailed pattern help with use cases"""
        print("\n📚 Detailed Pattern Information:")
        print("-" * 35)
        
        pattern_details = {
            "Multi-Agent Orchestration": {
                "description": "Coordinate multiple agents working together",
                "use_cases": ["Complex workflows", "Task distribution", "Agent coordination"],
                "benefits": ["Scalability", "Specialization", "Fault tolerance"]
            },
            "Agent Communication": {
                "description": "Handle message passing between agents",
                "use_cases": ["Agent coordination", "Information sharing", "Event handling"],
                "benefits": ["Reliability", "Asynchronous processing", "Message persistence"]
            },
            "Agent Collaboration": {
                "description": "Enable agents to work on shared tasks",
                "use_cases": ["Team projects", "Shared resources", "Collaborative decision making"],
                "benefits": ["Knowledge sharing", "Conflict resolution", "Collective intelligence"]
            },
            "Agent Learning": {
                "description": "Allow agents to learn from experience",
                "use_cases": ["Performance improvement", "Pattern recognition", "Adaptive behavior"],
                "benefits": ["Continuous improvement", "Personalization", "Efficiency gains"]
            },
            "Memory Management": {
                "description": "Persistent memory and context management",
                "use_cases": ["Context retention", "Knowledge storage", "Experience tracking"],
                "benefits": ["Consistency", "Learning", "Personalization"]
            },
            "Goal Setting & Monitoring": {
                "description": "Track and manage agent objectives",
                "use_cases": ["Progress tracking", "Objective management", "Performance monitoring"],
                "benefits": ["Accountability", "Progress visibility", "Goal achievement"]
            },
            "Exception Handling & Recovery": {
                "description": "Robust error handling and recovery",
                "use_cases": ["Error recovery", "Fault tolerance", "System resilience"],
                "benefits": ["Reliability", "User experience", "System stability"]
            },
            "Agent Adaptation": {
                "description": "Dynamic behavior modification",
                "use_cases": ["Behavior adjustment", "Context adaptation", "User preference learning"],
                "benefits": ["Flexibility", "Personalization", "User satisfaction"]
            },
            "Agent Creativity": {
                "description": "Creative problem-solving capabilities",
                "use_cases": ["Content generation", "Innovative solutions", "Creative tasks"],
                "benefits": ["Innovation", "Unique solutions", "Creative output"]
            },
            "Agent Empathy": {
                "description": "Emotional intelligence and user understanding",
                "use_cases": ["User support", "Emotional recognition", "Appropriate responses"],
                "benefits": ["User satisfaction", "Emotional connection", "Better communication"]
            },
            "Resource-Aware Optimization": {
                "description": "Monitor and optimize resource usage",
                "use_cases": ["Performance optimization", "Cost management", "Resource monitoring"],
                "benefits": ["Efficiency", "Cost savings", "Performance"]
            },
            "Agent Ethics": {
                "description": "Ethical decision-making framework",
                "use_cases": ["Ethical decisions", "Bias prevention", "Fair treatment"],
                "benefits": ["Trust", "Compliance", "Fairness"]
            },
            "Evaluation & Monitoring": {
                "description": "Performance evaluation and monitoring",
                "use_cases": ["Performance tracking", "Quality assessment", "Metrics collection"],
                "benefits": ["Quality assurance", "Performance insights", "Continuous improvement"]
            },
            "Guardrails & Safety": {
                "description": "Safety constraints and content moderation",
                "use_cases": ["Content safety", "Harmful content prevention", "Safety constraints"],
                "benefits": ["User safety", "Content quality", "Risk mitigation"]
            },
            "Agent Evolution": {
                "description": "Adaptive learning and self-improvement",
                "use_cases": ["Self-improvement", "Adaptation", "Evolution"],
                "benefits": ["Continuous growth", "Adaptation", "Long-term improvement"]
            },
            "Agent Swarming": {
                "description": "Coordinated multi-agent behavior",
                "use_cases": ["Collective behavior", "Swarm intelligence", "Coordinated actions"],
                "benefits": ["Collective intelligence", "Scalability", "Emergent behavior"]
            }
        }
        
        for name, details in pattern_details.items():
            print(f"\n• {name}:")
            print(f"  Description: {details['description']}")
            print(f"  Use Cases: {', '.join(details['use_cases'])}")
            print(f"  Benefits: {', '.join(details['benefits'])}")
        
        print()
    
    def _step_agent_configuration(self):
        """Step 5: Agent configuration with templates"""
        print("\n🎭 Step 5: Agent Configuration")
        print("=" * 35)
        print()
        
        # Show available templates
        templates = self.config_framework.get_available_templates()
        print("Available agent templates:")
        for i, template in enumerate(templates, 1):
            template_info = self.config_framework.templates[template]
            print(f"{i}. {template.replace('_', ' ').title()}")
            print(f"   {template_info['description']}")
            print()
        
        print(f"{len(templates) + 1}. Custom Agent (Build from scratch)")
        print("   Create a completely custom agent configuration")
        print()
        
        while True:
            try:
                choice = int(input(f"Choose a template (1-{len(templates) + 1}): "))
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
        print()
        
        # Show agent instructions
        instructions = self.config_framework.generate_agent_instructions(agent_config)
        print("📋 Agent Instructions Preview:")
        print("-" * 30)
        print(instructions[:200] + "..." if len(instructions) > 200 else instructions)
        print()
        
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
        print("Examples: helpful, knowledgeable, responsive, creative, analytical")
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
    
    def _step_capabilities_definition(self):
        """Step 6: Capabilities definition with recommendations"""
        print("\n⚡ Step 6: Agent Capabilities")
        print("=" * 30)
        print()
        
        # Show recommended capabilities if available
        if "recommendations" in self.wizard_state and "capabilities" in self.wizard_state["recommendations"]:
            print("💡 Recommended capabilities for your domain:")
            for cap in self.wizard_state["recommendations"]["capabilities"]:
                print(f"   • {cap}")
            print()
        
        # Get core capabilities
        print("What are the core capabilities your agent needs?")
        print("(Enter multiple capabilities separated by commas)")
        print("Examples: problem solving, data analysis, creative writing, customer support")
        
        core_caps = input("Core capabilities: ").strip()
        if not core_caps and "recommendations" in self.wizard_state and "capabilities" in self.wizard_state["recommendations"]:
            core_caps = ", ".join(self.wizard_state["recommendations"]["capabilities"])
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
        if "recommendations" in self.wizard_state and "communication_style" in self.wizard_state["recommendations"]:
            comm_style = self.wizard_state["recommendations"]["communication_style"]
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
    
    def _step_integrations_setup(self):
        """Step 7: Integrations setup with recommendations"""
        print("\n🔗 Step 7: External Integrations")
        print("=" * 35)
        print()
        
        # Show recommended integrations if available
        if "recommendations" in self.wizard_state and "integrations" in self.wizard_state["recommendations"]:
            print("💡 Recommended integrations for your domain:")
            for integration in self.wizard_state["recommendations"]["integrations"]:
                print(f"   • {integration}")
            print()
        
        integrations = []
        
        # Database integration
        print("Do you need database integration? (y/n)")
        if input("> ").strip().lower() == 'y':
            print("What type of database?")
            print("1. SQLite (local development)")
            print("2. PostgreSQL (production)")
            print("3. MySQL (web applications)")
            print("4. MongoDB (document storage)")
            
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
    
    def _step_testing_configuration(self):
        """Step 8: Testing configuration with smart defaults"""
        print("\n🧪 Step 8: Testing & Validation")
        print("=" * 35)
        print()
        
        # Smart defaults based on domain and recommendations
        domain = self.current_project["domain"]
        
        if "recommendations" in self.wizard_state and "test_data_focus" in self.wizard_state["recommendations"]:
            recommended_types = self.wizard_state["recommendations"]["test_data_focus"]
            print(f"💡 Recommended test data types for {domain} domain:")
            for data_type in recommended_types:
                print(f"   • {data_type}")
            print()
            
            use_recommended = input("Use these recommended test data types? (y/n): ").strip().lower()
            if use_recommended == 'y':
                selected_test_types = recommended_types
            else:
                selected_test_types = self._get_custom_test_requirements()
        else:
            selected_test_types = self._get_custom_test_requirements()
        
        # Smart volume defaults
        volume_defaults = {
            "customer_service": 1000,
            "healthcare": 1000,
            "technology": 2000,
            "e_commerce": 1500,
            "education": 500,
            "finance": 1000
        }
        
        default_volume = volume_defaults.get(domain, 1000)
        print(f"💡 Recommended test data volume for {domain} domain: {default_volume} records")
        
        use_default_volume = input(f"Use recommended volume ({default_volume})? (y/n): ").strip().lower()
        if use_default_volume == 'y':
            test_volume = default_volume
        else:
            test_volume = int(input("Enter number of records: ") or str(default_volume))
        
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
        return test_data_types.get(test_choice, ["user_profiles", "conversations"])
    
    def _step_project_generation(self):
        """Step 9: Project generation"""
        print("\n🏗️  Step 9: Project Generation")
        print("=" * 35)
        print()
        
        print("Generating your AI agent project with all configurations...")
        print()
        
        # Generate project files using the enhanced UI
        from enhanced_ui import EnhancedProjectGeneratorUI
        enhanced_ui = EnhancedProjectGeneratorUI()
        enhanced_ui.current_project = self.current_project
        
        project_path = enhanced_ui.generate_project_files()
        
        print(f"\n✅ Project generated successfully in: {project_path}")
        print()
        print("🎉 Your AI agent project is ready!")
        print()
        print("Next steps:")
        print("1. Navigate to your project directory")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Configure environment variables: cp .env.example .env")
        print("4. Run your agent: python main.py")
        print("5. Deploy with Docker: cd deployment && docker-compose up")
        print()
        print("📚 Check the README.md for detailed instructions and examples")
        
        return True
    
    def _validate_project_name(self, name):
        """Validate project name"""
        if not name:
            self.wizard_state["validation_errors"].append("Project name cannot be empty")
            return False
        
        if len(name) < 3:
            self.wizard_state["validation_errors"].append("Project name must be at least 3 characters")
            return False
        
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
            self.wizard_state["validation_errors"].append("Project name can only contain letters, numbers, spaces, hyphens, and underscores")
            return False
        
        return True
    
    def _validate_project_description(self, description):
        """Validate project description"""
        if not description:
            self.wizard_state["validation_errors"].append("Project description cannot be empty")
            return False
        
        if len(description) < 10:
            self.wizard_state["validation_errors"].append("Project description must be at least 10 characters")
            return False
        
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


def main():
    """Main entry point for the project wizard"""
    wizard = ProjectWizard()
    success = wizard.run_wizard()
    
    if success:
        print("\n✅ Thank you for using the AI Agent Project Wizard!")
    else:
        print("\n❌ Project wizard failed. Please try again.")


if __name__ == "__main__":
    main()
