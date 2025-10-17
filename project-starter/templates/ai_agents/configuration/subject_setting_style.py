"""
Subject-Setting-Style Framework for Agent Configuration

This module implements Ravi Mehta's Subject-Setting-Style framework for agent configuration,
enabling structured, context-aware agent setup using photographic language and metadata.
"""

import json
import random
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class SubjectType(str, Enum):
    """Types of agent subjects"""
    PERSONALITY = "personality"
    CAPABILITY = "capability"
    BEHAVIOR = "behavior"
    ROLE = "role"
    DOMAIN = "domain"
    TASK = "task"
    INTERACTION = "interaction"
    RESPONSE = "response"
    CREATIVITY = "creativity"


class SettingType(str, Enum):
    """Types of agent settings"""
    ENVIRONMENT = "environment"
    CONTEXT = "context"
    SCENARIO = "scenario"
    SITUATION = "situation"
    WORKSPACE = "workspace"
    PLATFORM = "platform"
    DOMAIN = "domain"
    USE_CASE = "use_case"


class StyleType(str, Enum):
    """Types of agent styles"""
    COMMUNICATION = "communication"
    INTERACTION = "interaction"
    DECISION_MAKING = "decision_making"
    PROBLEM_SOLVING = "problem_solving"
    CREATIVITY = "creativity"
    ANALYTICAL = "analytical"
    EMOTIONAL = "emotional"
    TECHNICAL = "technical"


class SubjectDescriptor(BaseModel):
    """Subject descriptor for agent configuration"""
    subject_type: SubjectType
    primary_subject: str
    secondary_subjects: List[str] = Field(default_factory=list)
    intensity: float = Field(ge=0.0, le=1.0, default=0.5)
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SettingDescriptor(BaseModel):
    """Setting descriptor for agent configuration"""
    setting_type: SettingType
    primary_setting: str
    secondary_settings: List[str] = Field(default_factory=list)
    specificity: float = Field(ge=0.0, le=1.0, default=0.7)
    relevance: float = Field(ge=0.0, le=1.0, default=0.8)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class StyleDescriptor(BaseModel):
    """Style descriptor for agent configuration"""
    style_type: StyleType
    primary_style: str
    secondary_styles: List[str] = Field(default_factory=list)
    consistency: float = Field(ge=0.0, le=1.0, default=0.8)
    adaptability: float = Field(ge=0.0, le=1.0, default=0.6)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentConfiguration(BaseModel):
    """Complete agent configuration using Subject-Setting-Style framework"""
    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    subject: SubjectDescriptor
    setting: SettingDescriptor
    style: StyleDescriptor
    configuration_data: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class SubjectSettingStyleFramework:
    """Main framework for Subject-Setting-Style agent configuration"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the framework"""
        self.config = config or {}
        self.configurations: Dict[str, AgentConfiguration] = {}
        self.templates: Dict[str, Dict[str, Any]] = {}
        
        # Initialize templates
        self._initialize_templates()
        
        # Set random seed for reproducibility
        random.seed(self.config.get("seed", 42))
    
    def _initialize_templates(self):
        """Initialize configuration templates"""
        self.templates = {
            "customer_service_agent": {
                "subject": {
                    "type": SubjectType.PERSONALITY,
                    "primary": "helpful and empathetic customer service representative",
                    "secondary": ["patient", "knowledgeable", "solution-oriented"],
                    "intensity": 0.8,
                    "confidence": 0.9
                },
                "setting": {
                    "type": SettingType.ENVIRONMENT,
                    "primary": "customer service platform with live chat and ticketing system",
                    "secondary": ["multi-channel support", "CRM integration", "knowledge base"],
                    "specificity": 0.9,
                    "relevance": 0.95
                },
                "style": {
                    "type": StyleType.COMMUNICATION,
                    "primary": "professional, warm, and solution-focused communication",
                    "secondary": ["active listening", "clear explanations", "proactive assistance"],
                    "consistency": 0.9,
                    "adaptability": 0.8
                }
            },
            "technical_analyst": {
                "subject": {
                    "type": SubjectType.CAPABILITY,
                    "primary": "expert data analyst with deep technical knowledge",
                    "secondary": ["statistical analysis", "data visualization", "insight generation"],
                    "intensity": 0.9,
                    "confidence": 0.85
                },
                "setting": {
                    "type": SettingType.WORKSPACE,
                    "primary": "data analysis environment with advanced analytics tools",
                    "secondary": ["Jupyter notebooks", "SQL databases", "visualization software"],
                    "specificity": 0.8,
                    "relevance": 0.9
                },
                "style": {
                    "type": StyleType.ANALYTICAL,
                    "primary": "methodical, data-driven, and evidence-based approach",
                    "secondary": ["logical reasoning", "quantitative analysis", "clear reporting"],
                    "consistency": 0.95,
                    "adaptability": 0.7
                }
            },
            "creative_writer": {
                "subject": {
                    "type": SubjectType.CREATIVITY,
                    "primary": "imaginative and skilled content creator",
                    "secondary": ["storytelling", "brand voice", "audience engagement"],
                    "intensity": 0.9,
                    "confidence": 0.8
                },
                "setting": {
                    "type": SettingType.CONTEXT,
                    "primary": "creative writing environment with diverse content requirements",
                    "secondary": ["blog posts", "social media", "marketing copy", "technical documentation"],
                    "specificity": 0.7,
                    "relevance": 0.85
                },
                "style": {
                    "type": StyleType.CREATIVITY,
                    "primary": "engaging, original, and brand-consistent writing",
                    "secondary": ["voice adaptation", "tone variation", "creative problem-solving"],
                    "consistency": 0.8,
                    "adaptability": 0.9
                }
            },
            "project_manager": {
                "subject": {
                    "type": SubjectType.ROLE,
                    "primary": "organized and strategic project coordinator",
                    "secondary": ["team leadership", "timeline management", "stakeholder communication"],
                    "intensity": 0.8,
                    "confidence": 0.9
                },
                "setting": {
                    "type": SettingType.WORKSPACE,
                    "primary": "project management environment with collaboration tools",
                    "secondary": ["agile methodology", "team coordination", "progress tracking"],
                    "specificity": 0.8,
                    "relevance": 0.9
                },
                "style": {
                    "type": StyleType.DECISION_MAKING,
                    "primary": "structured, proactive, and results-oriented management",
                    "secondary": ["strategic planning", "risk assessment", "team motivation"],
                    "consistency": 0.9,
                    "adaptability": 0.8
                }
            },
            "healthcare_assistant": {
                "subject": {
                    "type": SubjectType.DOMAIN,
                    "primary": "knowledgeable healthcare support specialist",
                    "secondary": ["medical knowledge", "patient care", "health education"],
                    "intensity": 0.9,
                    "confidence": 0.95
                },
                "setting": {
                    "type": SettingType.ENVIRONMENT,
                    "primary": "healthcare facility with patient management systems",
                    "secondary": ["HIPAA compliance", "medical records", "appointment scheduling"],
                    "specificity": 0.95,
                    "relevance": 0.9
                },
                "style": {
                    "type": StyleType.EMOTIONAL,
                    "primary": "compassionate, professional, and patient-centered care",
                    "secondary": ["empathy", "clear communication", "safety focus"],
                    "consistency": 0.95,
                    "adaptability": 0.7
                }
            }
        }
    
    def create_agent_configuration(self, name: str, description: str,
                                 subject: SubjectDescriptor, setting: SettingDescriptor,
                                 style: StyleDescriptor,
                                 configuration_data: Optional[Dict[str, Any]] = None) -> str:
        """Create a new agent configuration"""
        config = AgentConfiguration(
            name=name,
            description=description,
            subject=subject,
            setting=setting,
            style=style,
            configuration_data=configuration_data or {}
        )
        
        self.configurations[config.agent_id] = config
        return config.agent_id
    
    def create_from_template(self, template_name: str, customizations: Optional[Dict[str, Any]] = None) -> str:
        """Create agent configuration from template"""
        if template_name not in self.templates:
            raise ValueError(f"Template not found: {template_name}")
        
        template = self.templates[template_name]
        customizations = customizations or {}
        
        # Create descriptors from template
        subject_data = template["subject"].copy()
        subject_data.update(customizations.get("subject", {}))
        # Map template keys to Pydantic model keys
        subject_data["subject_type"] = subject_data.pop("type")
        subject_data["primary_subject"] = subject_data.pop("primary")
        subject_data["secondary_subjects"] = subject_data.pop("secondary")
        subject = SubjectDescriptor(**subject_data)
        
        setting_data = template["setting"].copy()
        setting_data.update(customizations.get("setting", {}))
        # Map template keys to Pydantic model keys
        setting_data["setting_type"] = setting_data.pop("type")
        setting_data["primary_setting"] = setting_data.pop("primary")
        setting_data["secondary_settings"] = setting_data.pop("secondary")
        setting = SettingDescriptor(**setting_data)
        
        style_data = template["style"].copy()
        style_data.update(customizations.get("style", {}))
        # Map template keys to Pydantic model keys
        style_data["style_type"] = style_data.pop("type")
        style_data["primary_style"] = style_data.pop("primary")
        style_data["secondary_styles"] = style_data.pop("secondary")
        style = StyleDescriptor(**style_data)
        
        # Create configuration
        name = customizations.get("name", f"{template_name.replace('_', ' ').title()} Agent")
        description = customizations.get("description", f"Agent configured from {template_name} template")
        
        return self.create_agent_configuration(name, description, subject, setting, style)
    
    def generate_photographic_prompt(self, agent_id: str) -> str:
        """Generate a photographic-style prompt for the agent"""
        if agent_id not in self.configurations:
            raise ValueError(f"Agent configuration not found: {agent_id}")
        
        config = self.configurations[agent_id]
        
        # Build photographic prompt using Subject-Setting-Style framework
        prompt_parts = []
        
        # Subject (what the agent is)
        subject_part = f"Subject: {config.subject.primary_subject}"
        if config.subject.secondary_subjects:
            subject_part += f" with {', '.join(config.subject.secondary_subjects)}"
        prompt_parts.append(subject_part)
        
        # Setting (where the agent operates)
        setting_part = f"Setting: {config.setting.primary_setting}"
        if config.setting.secondary_settings:
            setting_part += f" featuring {', '.join(config.setting.secondary_settings)}"
        prompt_parts.append(setting_part)
        
        # Style (how the agent behaves)
        style_part = f"Style: {config.style.primary_style}"
        if config.style.secondary_styles:
            style_part += f" incorporating {', '.join(config.style.secondary_styles)}"
        prompt_parts.append(style_part)
        
        # Add metadata for photographic language
        metadata_parts = []
        if config.subject.intensity > 0.7:
            metadata_parts.append("high-intensity")
        if config.setting.specificity > 0.8:
            metadata_parts.append("highly-specific")
        if config.style.consistency > 0.8:
            metadata_parts.append("consistent")
        if config.style.adaptability > 0.7:
            metadata_parts.append("adaptive")
        
        if metadata_parts:
            prompt_parts.append(f"Characteristics: {', '.join(metadata_parts)}")
        
        return " | ".join(prompt_parts)
    
    def generate_agent_instructions(self, agent_id: str) -> str:
        """Generate detailed agent instructions from configuration"""
        if agent_id not in self.configurations:
            raise ValueError(f"Agent configuration not found: {agent_id}")
        
        config = self.configurations[agent_id]
        
        instructions = f"""
# Agent Instructions: {config.name}

## Overview
{config.description}

## Core Identity (Subject)
**Primary Role**: {config.subject.primary_subject}
**Secondary Capabilities**: {', '.join(config.subject.secondary_subjects) if config.subject.secondary_subjects else 'None specified'}
**Intensity Level**: {config.subject.intensity:.1f}/1.0
**Confidence Level**: {config.subject.confidence:.1f}/1.0

## Operating Environment (Setting)
**Primary Context**: {config.setting.primary_setting}
**Secondary Contexts**: {', '.join(config.setting.secondary_settings) if config.setting.secondary_settings else 'None specified'}
**Specificity Level**: {config.setting.specificity:.1f}/1.0
**Relevance Level**: {config.setting.relevance:.1f}/1.0

## Behavioral Style
**Primary Approach**: {config.style.primary_style}
**Secondary Approaches**: {', '.join(config.style.secondary_styles) if config.style.secondary_styles else 'None specified'}
**Consistency Level**: {config.style.consistency:.1f}/1.0
**Adaptability Level**: {config.style.adaptability:.1f}/1.0

## Configuration Guidelines
"""
        
        # Add specific guidelines based on configuration
        if config.subject.intensity > 0.8:
            instructions += "- Maintain high energy and engagement in all interactions\n"
        if config.setting.specificity > 0.8:
            instructions += "- Be highly specific and detailed in responses\n"
        if config.style.consistency > 0.8:
            instructions += "- Maintain consistent behavior and communication style\n"
        if config.style.adaptability > 0.7:
            instructions += "- Adapt approach based on context and user needs\n"
        
        # Add configuration data if available
        if config.configuration_data:
            instructions += "\n## Additional Configuration\n"
            for key, value in config.configuration_data.items():
                instructions += f"- **{key}**: {value}\n"
        
        return instructions.strip()
    
    def analyze_agent_compatibility(self, agent_id: str, task_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze compatibility between agent and task requirements"""
        if agent_id not in self.configurations:
            raise ValueError(f"Agent configuration not found: {agent_id}")
        
        config = self.configurations[agent_id]
        
        compatibility_scores = {
            "subject_match": 0.0,
            "setting_match": 0.0,
            "style_match": 0.0,
            "overall_compatibility": 0.0
        }
        
        # Analyze subject compatibility
        required_capabilities = task_requirements.get("required_capabilities", [])
        agent_capabilities = [config.subject.primary_subject] + config.subject.secondary_subjects
        
        subject_matches = sum(1 for cap in required_capabilities 
                            if any(cap.lower() in agent_cap.lower() for agent_cap in agent_capabilities))
        compatibility_scores["subject_match"] = subject_matches / max(len(required_capabilities), 1)
        
        # Analyze setting compatibility
        required_environment = task_requirements.get("environment", "")
        setting_match = 0.0
        if required_environment:
            setting_match = sum(1 for word in required_environment.lower().split() 
                              if word in config.setting.primary_setting.lower())
            setting_match = min(setting_match / len(required_environment.split()), 1.0)
        compatibility_scores["setting_match"] = setting_match
        
        # Analyze style compatibility
        required_style = task_requirements.get("style", "")
        style_match = 0.0
        if required_style:
            style_match = sum(1 for word in required_style.lower().split() 
                            if word in config.style.primary_style.lower())
            style_match = min(style_match / len(required_style.split()), 1.0)
        compatibility_scores["style_match"] = style_match
        
        # Calculate overall compatibility
        compatibility_scores["overall_compatibility"] = (
            compatibility_scores["subject_match"] * 0.5 +
            compatibility_scores["setting_match"] * 0.3 +
            compatibility_scores["style_match"] * 0.2
        )
        
        return compatibility_scores
    
    def recommend_agent_for_task(self, task_requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend agents for a given task"""
        recommendations = []
        
        for agent_id, config in self.configurations.items():
            compatibility = self.analyze_agent_compatibility(agent_id, task_requirements)
            
            recommendations.append({
                "agent_id": agent_id,
                "agent_name": config.name,
                "compatibility_scores": compatibility,
                "photographic_prompt": self.generate_photographic_prompt(agent_id)
            })
        
        # Sort by overall compatibility
        recommendations.sort(key=lambda x: x["compatibility_scores"]["overall_compatibility"], reverse=True)
        
        return recommendations
    
    def get_available_templates(self) -> List[str]:
        """Get list of available templates"""
        return list(self.templates.keys())
    
    def get_agent_configurations(self) -> List[AgentConfiguration]:
        """Get all agent configurations"""
        return list(self.configurations.values())
    
    def get_agent_by_id(self, agent_id: str) -> Optional[AgentConfiguration]:
        """Get agent configuration by ID"""
        return self.configurations.get(agent_id)
    
    def update_agent_configuration(self, agent_id: str, updates: Dict[str, Any]) -> bool:
        """Update agent configuration"""
        if agent_id not in self.configurations:
            return False
        
        config = self.configurations[agent_id]
        
        # Update fields
        if "name" in updates:
            config.name = updates["name"]
        if "description" in updates:
            config.description = updates["description"]
        if "subject" in updates:
            config.subject = SubjectDescriptor(**updates["subject"])
        if "setting" in updates:
            config.setting = SettingDescriptor(**updates["setting"])
        if "style" in updates:
            config.style = StyleDescriptor(**updates["style"])
        if "configuration_data" in updates:
            config.configuration_data.update(updates["configuration_data"])
        
        config.updated_at = datetime.now()
        return True
    
    def export_configuration(self, agent_id: str, format: str = "json") -> Union[str, Dict[str, Any]]:
        """Export agent configuration"""
        if agent_id not in self.configurations:
            raise ValueError(f"Agent configuration not found: {agent_id}")
        
        config = self.configurations[agent_id]
        
        if format == "json":
            return config.dict()
        elif format == "yaml":
            # Simple YAML export (would need PyYAML for full support)
            return f"""
name: {config.name}
description: {config.description}
subject:
  type: {config.subject.subject_type.value}
  primary: {config.subject.primary_subject}
  secondary: {config.subject.secondary_subjects}
  intensity: {config.subject.intensity}
  confidence: {config.subject.confidence}
setting:
  type: {config.setting.setting_type.value}
  primary: {config.setting.primary_setting}
  secondary: {config.setting.secondary_settings}
  specificity: {config.setting.specificity}
  relevance: {config.setting.relevance}
style:
  type: {config.style.style_type.value}
  primary: {config.style.primary_style}
  secondary: {config.style.secondary_styles}
  consistency: {config.style.consistency}
  adaptability: {config.style.adaptability}
"""
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_framework_statistics(self) -> Dict[str, Any]:
        """Get framework statistics"""
        total_agents = len(self.configurations)
        total_templates = len(self.templates)
        
        # Count by subject type
        subject_types = {}
        for config in self.configurations.values():
            subject_type = config.subject.subject_type.value
            subject_types[subject_type] = subject_types.get(subject_type, 0) + 1
        
        # Count by setting type
        setting_types = {}
        for config in self.configurations.values():
            setting_type = config.setting.setting_type.value
            setting_types[setting_type] = setting_types.get(setting_type, 0) + 1
        
        # Count by style type
        style_types = {}
        for config in self.configurations.values():
            style_type = config.style.style_type.value
            style_types[style_type] = style_types.get(style_type, 0) + 1
        
        return {
            "total_agents": total_agents,
            "total_templates": total_templates,
            "subject_types": subject_types,
            "setting_types": setting_types,
            "style_types": style_types
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Subject-Setting-Style Framework")
    print("=" * 45)
    
    # Create framework
    framework = SubjectSettingStyleFramework()
    
    # Test template creation
    agent_id = framework.create_from_template("customer_service_agent", {
        "name": "Customer Support Bot",
        "description": "AI assistant for customer support"
    })
    print(f"✅ Created agent from template: {agent_id}")
    
    # Test photographic prompt generation
    prompt = framework.generate_photographic_prompt(agent_id)
    print(f"✅ Generated photographic prompt: {prompt}")
    
    # Test agent instructions
    instructions = framework.generate_agent_instructions(agent_id)
    print(f"✅ Generated agent instructions ({len(instructions)} characters)")
    
    # Test task compatibility analysis
    task_requirements = {
        "required_capabilities": ["customer service", "problem solving"],
        "environment": "online chat platform",
        "style": "professional and helpful"
    }
    
    compatibility = framework.analyze_agent_compatibility(agent_id, task_requirements)
    print(f"✅ Compatibility analysis: {compatibility['overall_compatibility']:.2f}")
    
    # Test agent recommendations
    recommendations = framework.recommend_agent_for_task(task_requirements)
    print(f"✅ Found {len(recommendations)} agent recommendations")
    
    # Test framework statistics
    stats = framework.get_framework_statistics()
    print(f"✅ Framework stats: {stats['total_agents']} agents, {stats['total_templates']} templates")
    
    print("🎯 Subject-Setting-Style Framework test completed!")
