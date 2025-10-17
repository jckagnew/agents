"""
Test suite for Subject-Setting-Style Framework
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from subject_setting_style import (
    SubjectSettingStyleFramework, SubjectType, SettingType, StyleType,
    SubjectDescriptor, SettingDescriptor, StyleDescriptor, AgentConfiguration
)


def test_framework_initialization():
    """Test framework initialization"""
    print("🧪 Testing Framework Initialization")
    print("=" * 35)
    
    framework = SubjectSettingStyleFramework()
    
    # Test initial state
    assert len(framework.configurations) == 0
    assert len(framework.templates) >= 5
    print("✅ Framework initialized with templates")
    
    # Test available templates
    templates = framework.get_available_templates()
    expected_templates = [
        "customer_service_agent", "technical_analyst", "creative_writer",
        "project_manager", "healthcare_assistant"
    ]
    for template in expected_templates:
        assert template in templates
    print("✅ All expected templates available")


def test_template_creation():
    """Test agent creation from templates"""
    print("\n🧪 Testing Template Creation")
    print("=" * 30)
    
    framework = SubjectSettingStyleFramework()
    
    # Test customer service agent
    agent_id = framework.create_from_template("customer_service_agent", {
        "name": "Support Bot",
        "description": "Customer support assistant"
    })
    assert agent_id in framework.configurations
    print("✅ Customer service agent created")
    
    # Test technical analyst
    agent_id = framework.create_from_template("technical_analyst", {
        "name": "Data Analyst",
        "description": "Technical data analysis specialist"
    })
    assert agent_id in framework.configurations
    print("✅ Technical analyst created")
    
    # Test creative writer
    agent_id = framework.create_from_template("creative_writer", {
        "name": "Content Creator",
        "description": "Creative content generation specialist"
    })
    assert agent_id in framework.configurations
    print("✅ Creative writer created")
    
    # Test invalid template
    try:
        framework.create_from_template("nonexistent_template", {})
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Invalid template error handled")


def test_custom_agent_creation():
    """Test custom agent creation"""
    print("\n🧪 Testing Custom Agent Creation")
    print("=" * 35)
    
    framework = SubjectSettingStyleFramework()
    
    # Create custom descriptors
    subject = SubjectDescriptor(
        subject_type=SubjectType.PERSONALITY,
        primary_subject="innovative problem solver",
        secondary_subjects=["creative", "analytical", "collaborative"],
        intensity=0.9,
        confidence=0.8
    )
    
    setting = SettingDescriptor(
        setting_type=SettingType.WORKSPACE,
        primary_setting="startup environment with agile development",
        secondary_settings=["cross-functional teams", "rapid prototyping", "user feedback"],
        specificity=0.8,
        relevance=0.9
    )
    
    style = StyleDescriptor(
        style_type=StyleType.CREATIVITY,
        primary_style="innovative and user-centered approach",
        secondary_styles=["design thinking", "rapid iteration", "user empathy"],
        consistency=0.8,
        adaptability=0.9
    )
    
    # Create agent
    agent_id = framework.create_agent_configuration(
        name="Innovation Specialist",
        description="Agent specialized in innovation and problem-solving",
        subject=subject,
        setting=setting,
        style=style,
        configuration_data={"domain": "product_development", "team_size": "small"}
    )
    
    assert agent_id in framework.configurations
    agent = framework.configurations[agent_id]
    assert agent.name == "Innovation Specialist"
    assert agent.subject.primary_subject == "innovative problem solver"
    print("✅ Custom agent created successfully")


def test_photographic_prompt_generation():
    """Test photographic prompt generation"""
    print("\n🧪 Testing Photographic Prompt Generation")
    print("=" * 45)
    
    framework = SubjectSettingStyleFramework()
    
    # Create agent from template
    agent_id = framework.create_from_template("customer_service_agent")
    
    # Generate photographic prompt
    prompt = framework.generate_photographic_prompt(agent_id)
    assert "Subject:" in prompt
    assert "Setting:" in prompt
    assert "Style:" in prompt
    print("✅ Photographic prompt generated")
    
    # Test prompt content
    assert "helpful and empathetic" in prompt.lower()
    assert "customer service" in prompt.lower()
    print("✅ Prompt contains expected content")
    
    # Test invalid agent ID
    try:
        framework.generate_photographic_prompt("nonexistent_id")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Invalid agent ID error handled")


def test_agent_instructions_generation():
    """Test agent instructions generation"""
    print("\n🧪 Testing Agent Instructions Generation")
    print("=" * 45)
    
    framework = SubjectSettingStyleFramework()
    
    # Create agent from template
    agent_id = framework.create_from_template("technical_analyst")
    
    # Generate instructions
    instructions = framework.generate_agent_instructions(agent_id)
    assert "Agent Instructions:" in instructions
    assert "Core Identity" in instructions
    assert "Operating Environment" in instructions
    assert "Behavioral Style" in instructions
    print("✅ Agent instructions generated")
    
    # Test instructions content
    assert "data analyst" in instructions.lower()
    assert "analytics tools" in instructions.lower()
    print("✅ Instructions contain expected content")


def test_compatibility_analysis():
    """Test agent-task compatibility analysis"""
    print("\n🧪 Testing Compatibility Analysis")
    print("=" * 35)
    
    framework = SubjectSettingStyleFramework()
    
    # Create agents
    cs_agent_id = framework.create_from_template("customer_service_agent")
    tech_agent_id = framework.create_from_template("technical_analyst")
    
    # Test customer service task
    cs_task = {
        "required_capabilities": ["customer service", "problem solving", "communication"],
        "environment": "online chat platform",
        "style": "professional and helpful"
    }
    
    cs_compatibility = framework.analyze_agent_compatibility(cs_agent_id, cs_task)
    assert "subject_match" in cs_compatibility
    assert "setting_match" in cs_compatibility
    assert "style_match" in cs_compatibility
    assert "overall_compatibility" in cs_compatibility
    print("✅ Compatibility analysis works")
    
    # Test technical task
    tech_task = {
        "required_capabilities": ["data analysis", "statistical analysis", "visualization"],
        "environment": "data analysis workspace",
        "style": "methodical and analytical"
    }
    
    tech_compatibility = framework.analyze_agent_compatibility(tech_agent_id, tech_task)
    assert tech_compatibility["overall_compatibility"] > 0
    print("✅ Technical task compatibility analyzed")
    
    # Test cross-compatibility
    cs_tech_compatibility = framework.analyze_agent_compatibility(cs_agent_id, tech_task)
    tech_cs_compatibility = framework.analyze_agent_compatibility(tech_agent_id, cs_task)
    
    # CS agent should be better for CS task, tech agent for tech task
    assert cs_compatibility["overall_compatibility"] > cs_tech_compatibility["overall_compatibility"]
    assert tech_compatibility["overall_compatibility"] > tech_cs_compatibility["overall_compatibility"]
    print("✅ Cross-compatibility analysis works")


def test_agent_recommendations():
    """Test agent recommendations for tasks"""
    print("\n🧪 Testing Agent Recommendations")
    print("=" * 35)
    
    framework = SubjectSettingStyleFramework()
    
    # Create multiple agents
    framework.create_from_template("customer_service_agent", {"name": "CS Agent 1"})
    framework.create_from_template("technical_analyst", {"name": "Tech Agent 1"})
    framework.create_from_template("creative_writer", {"name": "Creative Agent 1"})
    
    # Test customer service task
    cs_task = {
        "required_capabilities": ["customer service", "communication"],
        "environment": "support platform",
        "style": "helpful and professional"
    }
    
    recommendations = framework.recommend_agent_for_task(cs_task)
    assert len(recommendations) == 3
    assert recommendations[0]["compatibility_scores"]["overall_compatibility"] >= recommendations[1]["compatibility_scores"]["overall_compatibility"]
    print("✅ Agent recommendations work")
    
    # Test technical task
    tech_task = {
        "required_capabilities": ["data analysis", "statistics"],
        "environment": "analytics workspace",
        "style": "methodical and precise"
    }
    
    tech_recommendations = framework.recommend_agent_for_task(tech_task)
    assert len(tech_recommendations) == 3
    print("✅ Technical task recommendations work")


def test_agent_management():
    """Test agent management operations"""
    print("\n🧪 Testing Agent Management")
    print("=" * 30)
    
    framework = SubjectSettingStyleFramework()
    
    # Create agent
    agent_id = framework.create_from_template("customer_service_agent")
    
    # Test get agent by ID
    agent = framework.get_agent_by_id(agent_id)
    assert agent is not None
    assert "Customer Service" in agent.name
    print("✅ Get agent by ID works")
    
    # Test update agent
    updates = {
        "name": "Updated CS Agent",
        "description": "Updated description",
        "configuration_data": {"new_field": "new_value"}
    }
    
    success = framework.update_agent_configuration(agent_id, updates)
    assert success
    updated_agent = framework.get_agent_by_id(agent_id)
    assert updated_agent.name == "Updated CS Agent"
    assert updated_agent.configuration_data["new_field"] == "new_value"
    print("✅ Agent update works")
    
    # Test get all agents
    all_agents = framework.get_agent_configurations()
    assert len(all_agents) == 1
    print("✅ Get all agents works")


def test_export_functionality():
    """Test export functionality"""
    print("\n🧪 Testing Export Functionality")
    print("=" * 30)
    
    framework = SubjectSettingStyleFramework()
    
    # Create agent
    agent_id = framework.create_from_template("customer_service_agent")
    
    # Test JSON export
    json_export = framework.export_configuration(agent_id, "json")
    assert "agent_id" in json_export
    assert "name" in json_export
    assert "subject" in json_export
    assert "setting" in json_export
    assert "style" in json_export
    print("✅ JSON export works")
    
    # Test YAML export
    yaml_export = framework.export_configuration(agent_id, "yaml")
    assert "name:" in yaml_export
    assert "subject:" in yaml_export
    assert "setting:" in yaml_export
    assert "style:" in yaml_export
    print("✅ YAML export works")
    
    # Test invalid format
    try:
        framework.export_configuration(agent_id, "invalid_format")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Invalid format error handled")


def test_framework_statistics():
    """Test framework statistics"""
    print("\n🧪 Testing Framework Statistics")
    print("=" * 30)
    
    framework = SubjectSettingStyleFramework()
    
    # Create agents
    framework.create_from_template("customer_service_agent")
    framework.create_from_template("technical_analyst")
    framework.create_from_template("creative_writer")
    
    # Get statistics
    stats = framework.get_framework_statistics()
    assert "total_agents" in stats
    assert "total_templates" in stats
    assert "subject_types" in stats
    assert "setting_types" in stats
    assert "style_types" in stats
    assert stats["total_agents"] == 3
    assert stats["total_templates"] >= 5
    print("✅ Framework statistics work")


def test_descriptor_validation():
    """Test descriptor validation"""
    print("\n🧪 Testing Descriptor Validation")
    print("=" * 35)
    
    # Test valid subject descriptor
    subject = SubjectDescriptor(
        subject_type=SubjectType.PERSONALITY,
        primary_subject="test subject",
        intensity=0.5,
        confidence=0.8
    )
    assert subject.intensity == 0.5
    assert subject.confidence == 0.8
    print("✅ Subject descriptor validation works")
    
    # Test valid setting descriptor
    setting = SettingDescriptor(
        setting_type=SettingType.ENVIRONMENT,
        primary_setting="test setting",
        specificity=0.7,
        relevance=0.9
    )
    assert setting.specificity == 0.7
    assert setting.relevance == 0.9
    print("✅ Setting descriptor validation works")
    
    # Test valid style descriptor
    style = StyleDescriptor(
        style_type=StyleType.COMMUNICATION,
        primary_style="test style",
        consistency=0.8,
        adaptability=0.6
    )
    assert style.consistency == 0.8
    assert style.adaptability == 0.6
    print("✅ Style descriptor validation works")


def test_error_handling():
    """Test error handling"""
    print("\n🧪 Testing Error Handling")
    print("=" * 25)
    
    framework = SubjectSettingStyleFramework()
    
    # Test invalid agent ID
    try:
        framework.generate_photographic_prompt("nonexistent_id")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Invalid agent ID error handled")
    
    # Test invalid template
    try:
        framework.create_from_template("nonexistent_template")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Invalid template error handled")
    
    # Test invalid export format
    try:
        framework.export_configuration("nonexistent_id", "invalid_format")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Invalid export format error handled")


def main():
    """Run all tests"""
    print("🚀 Starting Subject-Setting-Style Framework Tests")
    print("=" * 55)
    
    test_framework_initialization()
    test_template_creation()
    test_custom_agent_creation()
    test_photographic_prompt_generation()
    test_agent_instructions_generation()
    test_compatibility_analysis()
    test_agent_recommendations()
    test_agent_management()
    test_export_functionality()
    test_framework_statistics()
    test_descriptor_validation()
    test_error_handling()
    
    print("\n🎉 All Subject-Setting-Style Framework tests passed!")
    print("=" * 55)


if __name__ == "__main__":
    main()
