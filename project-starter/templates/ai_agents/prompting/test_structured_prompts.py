"""
Test suite for Structured Prompt Framework
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from structured_prompts import (
    PromptFramework, PromptType, PromptRole, PromptComponent, 
    StructuredPrompt, PromptTemplate
)


def test_framework_initialization():
    """Test framework initialization"""
    print("🧪 Testing Framework Initialization")
    print("=" * 35)
    
    framework = PromptFramework()
    
    # Test default templates
    assert len(framework.templates) >= 4
    print("✅ Default templates loaded")
    
    # Test template types
    template_types = {template.template_type for template in framework.templates.values()}
    expected_types = {PromptType.TASK_ORIENTED, PromptType.CREATIVE, PromptType.ANALYTICAL, PromptType.CONVERSATIONAL}
    assert expected_types.issubset(template_types)
    print("✅ All expected template types present")
    
    # Test initial state
    assert len(framework.prompts) == 0
    assert len(framework.prompt_history) == 0
    print("✅ Initial state correct")


def test_template_creation():
    """Test template creation and usage"""
    print("\n🧪 Testing Template Creation")
    print("=" * 30)
    
    framework = PromptFramework()
    
    # Test getting templates by type
    task_templates = framework.get_template_by_type(PromptType.TASK_ORIENTED)
    assert len(task_templates) >= 1
    print("✅ Template retrieval by type works")
    
    # Test template variables
    task_template = task_templates[0]
    assert "context" in task_template.variables
    assert "task_description" in task_template.variables
    print("✅ Template variables correct")


def test_prompt_creation_from_template():
    """Test creating prompts from templates"""
    print("\n🧪 Testing Prompt Creation from Template")
    print("=" * 45)
    
    framework = PromptFramework()
    
    # Test task execution prompt
    task_variables = {
        "context": "AI agent development",
        "task_description": "Implement memory management system",
        "constraints": "Must be thread-safe and efficient",
        "output_format": "Code implementation with tests",
        "examples": "Example: class MemoryManager: def __init__(self): ..."
    }
    
    prompt_id = framework.create_prompt_from_template("task_execution", task_variables)
    assert prompt_id in framework.prompts
    print("✅ Task execution prompt created")
    
    # Test creative prompt
    creative_variables = {
        "domain": "artificial intelligence",
        "brief": "Create a compelling story about AI agents",
        "style_guidelines": "Science fiction, optimistic tone",
        "constraints": "Maximum 500 words, family-friendly",
        "inspiration_sources": "Asimov, Clarke, modern AI research",
        "output_requirements": "Narrative structure, character development"
    }
    
    creative_prompt_id = framework.create_prompt_from_template("creative_generation", creative_variables)
    assert creative_prompt_id in framework.prompts
    print("✅ Creative prompt created")
    
    # Test analytical prompt
    analytical_variables = {
        "data_context": "User engagement metrics from mobile app",
        "objective": "Identify patterns in user behavior",
        "methodology": "Statistical analysis and clustering",
        "key_metrics": "session_duration, feature_usage, retention_rate",
        "hypothesis": "Users who engage with feature X have higher retention",
        "output_format": "Detailed analysis report with visualizations"
    }
    
    analytical_prompt_id = framework.create_prompt_from_template("data_analysis", analytical_variables)
    assert analytical_prompt_id in framework.prompts
    print("✅ Analytical prompt created")


def test_custom_prompt_creation():
    """Test creating custom prompts"""
    print("\n🧪 Testing Custom Prompt Creation")
    print("=" * 35)
    
    framework = PromptFramework()
    
    # Create custom components
    components = [
        PromptComponent(
            role=PromptRole.SYSTEM,
            content="You are an expert in {domain} with {experience} years of experience.",
            priority=1,
            is_required=True,
            metadata={"domain": "technology"}
        ),
        PromptComponent(
            role=PromptRole.USER,
            content="I need help with {specific_task} in the context of {project_context}.",
            priority=2,
            is_required=True
        ),
        PromptComponent(
            role=PromptRole.CONSTRAINT,
            content="Please provide a solution that is {solution_requirements}.",
            priority=3,
            is_required=False
        )
    ]
    
    # Create custom prompt
    custom_prompt_id = framework.create_structured_prompt(
        name="Expert Consultation",
        prompt_type=PromptType.TECHNICAL,
        description="A prompt for expert technical consultation",
        components=components,
        variables={
            "domain": "software engineering",
            "experience": "10",
            "specific_task": "system design",
            "project_context": "e-commerce platform",
            "solution_requirements": "scalable and maintainable"
        },
        constraints=["Must be production-ready", "Should follow best practices"],
        examples=[
            {"input": "Design a payment system", "output": "Microservices architecture with API gateway..."}
        ]
    )
    
    assert custom_prompt_id in framework.prompts
    prompt = framework.prompts[custom_prompt_id]
    assert prompt.name == "Expert Consultation"
    assert prompt.prompt_type == PromptType.TECHNICAL
    assert len(prompt.components) == 3
    print("✅ Custom prompt created with all components")


def test_prompt_generation():
    """Test prompt text generation"""
    print("\n🧪 Testing Prompt Generation")
    print("=" * 30)
    
    framework = PromptFramework()
    
    # Create a simple prompt
    components = [
        PromptComponent(
            role=PromptRole.SYSTEM,
            content="You are a {role} specializing in {domain}.",
            priority=1,
            is_required=True
        ),
        PromptComponent(
            role=PromptRole.USER,
            content="Please help me with {task}.",
            priority=2,
            is_required=True
        )
    ]
    
    prompt_id = framework.create_structured_prompt(
        name="Simple Helper",
        prompt_type=PromptType.CONVERSATIONAL,
        description="A simple helper prompt",
        components=components,
        variables={"role": "AI assistant", "domain": "programming", "task": "debugging"}
    )
    
    # Test basic generation
    prompt_text = framework.generate_prompt_text(prompt_id)
    assert "SYSTEM:" in prompt_text
    assert "USER:" in prompt_text
    assert "AI assistant" in prompt_text
    assert "programming" in prompt_text
    assert "debugging" in prompt_text
    print("✅ Basic prompt generation works")
    
    # Test generation with additional variables
    additional_variables = {"role": "expert", "domain": "machine learning", "task": "model selection"}
    updated_prompt_text = framework.generate_prompt_text(prompt_id, additional_variables)
    assert "expert" in updated_prompt_text
    assert "machine learning" in updated_prompt_text
    assert "model selection" in updated_prompt_text
    print("✅ Prompt generation with additional variables works")
    
    # Test prompt history
    assert len(framework.prompt_history) >= 2
    print("✅ Prompt history tracking works")


def test_prompt_management():
    """Test prompt management operations"""
    print("\n🧪 Testing Prompt Management")
    print("=" * 30)
    
    framework = PromptFramework()
    
    # Create a prompt
    components = [
        PromptComponent(
            role=PromptRole.SYSTEM,
            content="You are a helpful assistant.",
            priority=1,
            is_required=True
        )
    ]
    
    prompt_id = framework.create_structured_prompt(
        name="Test Prompt",
        prompt_type=PromptType.CONVERSATIONAL,
        description="A test prompt",
        components=components
    )
    
    # Test adding component
    new_component = PromptComponent(
        role=PromptRole.CONSTRAINT,
        content="Be concise and helpful.",
        priority=2,
        is_required=False
    )
    
    success = framework.add_component_to_prompt(prompt_id, new_component)
    assert success
    assert len(framework.prompts[prompt_id].components) == 2
    print("✅ Component addition works")
    
    # Test updating variables
    new_variables = {"context": "testing", "style": "formal"}
    success = framework.update_prompt_variables(prompt_id, new_variables)
    assert success
    assert framework.prompts[prompt_id].variables["context"] == "testing"
    print("✅ Variable update works")
    
    # Test getting prompts by type
    conversational_prompts = framework.get_prompt_by_type(PromptType.CONVERSATIONAL)
    assert len(conversational_prompts) >= 1
    print("✅ Prompt retrieval by type works")
    
    # Test search
    search_results = framework.search_prompts("test")
    assert len(search_results) >= 1
    print("✅ Prompt search works")


def test_framework_statistics():
    """Test framework statistics"""
    print("\n🧪 Testing Framework Statistics")
    print("=" * 35)
    
    framework = PromptFramework()
    
    # Create some prompts
    for i in range(3):
        components = [
            PromptComponent(
                role=PromptRole.SYSTEM,
                content=f"Test prompt {i}",
                priority=1,
                is_required=True
            )
        ]
        
        framework.create_structured_prompt(
            name=f"Test Prompt {i}",
            prompt_type=PromptType.TECHNICAL,
            description=f"Test description {i}",
            components=components
        )
    
    # Generate some prompts to create history
    for prompt_id in list(framework.prompts.keys())[:2]:
        framework.generate_prompt_text(prompt_id)
    
    # Test statistics
    stats = framework.get_prompt_statistics()
    assert stats["total_prompts"] >= 3
    assert stats["total_templates"] >= 4
    assert "technical" in stats["prompt_types"]
    assert stats["recent_activity"] >= 0
    print("✅ Framework statistics work")


def test_export_functionality():
    """Test export functionality"""
    print("\n🧪 Testing Export Functionality")
    print("=" * 30)
    
    framework = PromptFramework()
    
    # Create a test prompt
    components = [
        PromptComponent(
            role=PromptRole.SYSTEM,
            content="Test export prompt",
            priority=1,
            is_required=True
        )
    ]
    
    framework.create_structured_prompt(
        name="Export Test",
        prompt_type=PromptType.CONVERSATIONAL,
        description="Test prompt for export",
        components=components
    )
    
    # Test JSON export
    json_export = framework.export_prompts("json")
    assert "prompts" in json_export
    assert "templates" in json_export
    assert "export_timestamp" in json_export
    assert len(json_export["prompts"]) >= 1
    print("✅ JSON export works")
    
    # Test text export
    text_export = framework.export_prompts("text")
    assert "Export Test" in text_export
    assert "conversational" in text_export.lower()  # Check for case-insensitive match
    print("✅ Text export works")


def test_error_handling():
    """Test error handling"""
    print("\n🧪 Testing Error Handling")
    print("=" * 25)
    
    framework = PromptFramework()
    
    # Test invalid template
    try:
        framework.create_prompt_from_template("nonexistent_template", {})
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Invalid template error handled")
    
    # Test invalid prompt ID
    try:
        framework.generate_prompt_text("nonexistent_prompt")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Invalid prompt ID error handled")
    
    # Test invalid export format
    try:
        framework.export_prompts("invalid_format")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Invalid export format error handled")


def main():
    """Run all tests"""
    print("🚀 Starting Structured Prompt Framework Tests")
    print("=" * 55)
    
    test_framework_initialization()
    test_template_creation()
    test_prompt_creation_from_template()
    test_custom_prompt_creation()
    test_prompt_generation()
    test_prompt_management()
    test_framework_statistics()
    test_export_functionality()
    test_error_handling()
    
    print("\n🎉 All Structured Prompt Framework tests passed!")
    print("=" * 55)


if __name__ == "__main__":
    main()
