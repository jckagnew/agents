"""
Test suite for Project Generator
"""

import json
import tempfile
import shutil
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from interactive_ui import ProjectGeneratorUI


def test_project_generator_initialization():
    """Test project generator initialization"""
    print("🧪 Testing Project Generator Initialization")
    print("=" * 45)
    
    generator = ProjectGeneratorUI()
    
    # Test framework initialization
    assert generator.schema_generator is not None
    assert generator.mcp_framework is not None
    assert generator.prompt_framework is not None
    assert generator.data_generator is not None
    assert generator.config_framework is not None
    print("✅ All frameworks initialized")
    
    # Test initial state
    assert generator.current_project == {}
    assert generator.project_requirements == {}
    print("✅ Initial state correct")


def test_project_basic_info():
    """Test project basic info collection"""
    print("\n🧪 Testing Project Basic Info Collection")
    print("=" * 45)
    
    generator = ProjectGeneratorUI()
    
    # Mock user input
    import builtins
    original_input = builtins.input
    
    def mock_input(prompt):
        if "project name" in prompt.lower():
            return "Test Project"
        elif "description" in prompt.lower():
            return "A test AI agent project"
        elif "domain" in prompt.lower():
            return "1"  # Customer Service
        return ""
    
    builtins.input = mock_input
    
    try:
        result = generator.get_project_basic_info()
        assert result == True
        assert generator.current_project["name"] == "Test Project"
        assert generator.current_project["description"] == "A test AI agent project"
        assert generator.current_project["domain"] == "customer_service"
        print("✅ Project basic info collection works")
    finally:
        builtins.input = original_input


def test_pattern_selection():
    """Test pattern selection"""
    print("\n🧪 Testing Pattern Selection")
    print("=" * 30)
    
    generator = ProjectGeneratorUI()
    generator.current_project = {
        "name": "Test Project",
        "description": "Test description",
        "domain": "technology"
    }
    
    # Mock user input
    import builtins
    original_input = builtins.input
    
    def mock_input(prompt):
        if "patterns" in prompt.lower():
            return "1,2,3"  # Select first 3 patterns
        return ""
    
    builtins.input = mock_input
    
    try:
        result = generator.select_agent_patterns()
        assert result == True
        assert len(generator.current_project["selected_patterns"]) == 3
        print("✅ Pattern selection works")
    finally:
        builtins.input = original_input


def test_agent_personality_configuration():
    """Test agent personality configuration"""
    print("\n🧪 Testing Agent Personality Configuration")
    print("=" * 50)
    
    generator = ProjectGeneratorUI()
    generator.current_project = {
        "name": "Test Project",
        "description": "Test description",
        "domain": "technology",
        "selected_patterns": [("Pattern 1", "pattern_1")]
    }
    
    # Mock user input
    import builtins
    original_input = builtins.input
    
    def mock_input(prompt):
        if "role" in prompt.lower():
            return "1"  # Customer Service Representative
        return ""
    
    builtins.input = mock_input
    
    try:
        result = generator.configure_agent_personality()
        assert result == True
        assert "agent_config_id" in generator.current_project
        print("✅ Agent personality configuration works")
    finally:
        builtins.input = original_input


def test_capabilities_configuration():
    """Test capabilities configuration"""
    print("\n🧪 Testing Capabilities Configuration")
    print("=" * 40)
    
    generator = ProjectGeneratorUI()
    generator.current_project = {
        "name": "Test Project",
        "description": "Test description",
        "domain": "technology",
        "selected_patterns": [("Pattern 1", "pattern_1")],
        "agent_config_id": "test_config_id"
    }
    
    # Mock user input
    import builtins
    original_input = builtins.input
    
    def mock_input(prompt):
        if "capabilities" in prompt.lower():
            return "problem solving, data analysis"
        elif "technical capabilities" in prompt.lower():
            return "API integration, database access"
        elif "communication" in prompt.lower():
            return "1"  # Professional and formal
        return ""
    
    builtins.input = mock_input
    
    try:
        result = generator.configure_agent_capabilities()
        assert result == True
        assert "capabilities" in generator.current_project
        assert "communication_style" in generator.current_project
        print("✅ Capabilities configuration works")
    finally:
        builtins.input = original_input


def test_external_integrations():
    """Test external integrations configuration"""
    print("\n🧪 Testing External Integrations")
    print("=" * 35)
    
    generator = ProjectGeneratorUI()
    generator.current_project = {
        "name": "Test Project",
        "description": "Test description",
        "domain": "technology",
        "selected_patterns": [("Pattern 1", "pattern_1")],
        "agent_config_id": "test_config_id",
        "capabilities": ["problem solving"],
        "communication_style": "professional"
    }
    
    # Mock user input
    import builtins
    original_input = builtins.input
    
    def mock_input(prompt):
        if "database" in prompt.lower():
            return "y"
        elif "database type" in prompt.lower():
            return "1"  # SQLite
        elif "api" in prompt.lower():
            return "y"
        elif "apis" in prompt.lower():
            return "OpenAI, Google"
        elif "file processing" in prompt.lower():
            return "y"
        elif "file types" in prompt.lower():
            return "PDF, CSV, JSON"
        elif "image processing" in prompt.lower():
            return "n"
        return ""
    
    builtins.input = mock_input
    
    try:
        result = generator.configure_external_integrations()
        assert result == True
        assert "integrations" in generator.current_project
        assert len(generator.current_project["integrations"]) > 0
        print("✅ External integrations configuration works")
    finally:
        builtins.input = original_input


def test_testing_requirements():
    """Test testing requirements configuration"""
    print("\n🧪 Testing Testing Requirements")
    print("=" * 35)
    
    generator = ProjectGeneratorUI()
    generator.current_project = {
        "name": "Test Project",
        "description": "Test description",
        "domain": "technology",
        "selected_patterns": [("Pattern 1", "pattern_1")],
        "agent_config_id": "test_config_id",
        "capabilities": ["problem solving"],
        "communication_style": "professional",
        "integrations": []
    }
    
    # Mock user input
    import builtins
    original_input = builtins.input
    
    def mock_input(prompt):
        if "test data" in prompt.lower():
            return "1"  # User profiles and interactions
        elif "data volume" in prompt.lower():
            return "2"  # Medium (500-2000 records)
        return ""
    
    builtins.input = mock_input
    
    try:
        result = generator.configure_testing_requirements()
        assert result == True
        assert "test_requirements" in generator.current_project
        assert "data_types" in generator.current_project["test_requirements"]
        assert "volume" in generator.current_project["test_requirements"]
        print("✅ Testing requirements configuration works")
    finally:
        builtins.input = original_input


def test_project_file_generation():
    """Test project file generation"""
    print("\n🧪 Testing Project File Generation")
    print("=" * 40)
    
    generator = ProjectGeneratorUI()
    generator.current_project = {
        "name": "Test Project",
        "description": "A test AI agent project",
        "domain": "technology",
        "selected_patterns": [("Multi-Agent Orchestration", "pattern_1")],
        "agent_config_id": "test_config_id",
        "capabilities": ["problem solving", "data analysis"],
        "communication_style": "professional",
        "integrations": [{"type": "database", "subtype": "sqlite"}],
        "test_requirements": {
            "data_types": ["user_profiles", "conversations"],
            "volume": 100,
            "context": "technology"
        }
    }
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir) / "test_project"
        
        try:
            # Test project structure generation
            generator._generate_project_structure(project_dir)
            assert project_dir.exists()
            assert (project_dir / "agents").exists()
            assert (project_dir / "configs").exists()
            assert (project_dir / "schemas").exists()
            assert (project_dir / "prompts").exists()
            assert (project_dir / "test_data").exists()
            print("✅ Project structure generation works")
            
            # Test agent config generation
            generator._generate_agent_configs(project_dir)
            assert (project_dir / "configs" / "agent_config.json").exists()
            print("✅ Agent config generation works")
            
            # Test schema generation
            generator._generate_schemas(project_dir)
            assert (project_dir / "schemas" / "selected_patterns.json").exists()
            print("✅ Schema generation works")
            
            # Test prompt generation
            generator._generate_prompts(project_dir)
            assert (project_dir / "prompts" / "agent_instructions.md").exists()
            print("✅ Prompt generation works")
            
            # Test test data generation
            generator._generate_test_data(project_dir)
            assert (project_dir / "test_data" / "user_profiles.json").exists()
            print("✅ Test data generation works")
            
            # Test MCP config generation
            generator._generate_mcp_configs(project_dir)
            assert (project_dir / "configs" / "mcp_config.json").exists()
            print("✅ MCP config generation works")
            
            # Test documentation generation
            generator._generate_documentation(project_dir)
            assert (project_dir / "README.md").exists()
            print("✅ Documentation generation works")
            
            # Test setup files generation
            generator._generate_setup_files(project_dir)
            assert (project_dir / "requirements.txt").exists()
            assert (project_dir / ".env.example").exists()
            assert (project_dir / "main.py").exists()
            print("✅ Setup files generation works")
            
        except Exception as e:
            print(f"❌ Error in file generation: {e}")
            raise


def test_custom_agent_creation():
    """Test custom agent creation"""
    print("\n🧪 Testing Custom Agent Creation")
    print("=" * 35)
    
    generator = ProjectGeneratorUI()
    generator.current_project = {
        "name": "Custom Test Project",
        "description": "A custom test project",
        "domain": "technology"
    }
    
    # Test custom agent config creation
    agent_config_id = generator._create_custom_agent_config("Custom AI Assistant")
    assert agent_config_id is not None
    
    # Test agent config retrieval
    agent_config = generator.config_framework.get_agent_by_id(agent_config_id)
    assert agent_config is not None
    assert "Custom AI Assistant" in agent_config.subject.primary_subject
    print("✅ Custom agent creation works")


def test_error_handling():
    """Test error handling"""
    print("\n🧪 Testing Error Handling")
    print("=" * 25)
    
    generator = ProjectGeneratorUI()
    
    # Test invalid project ID
    try:
        generator.config_framework.generate_photographic_prompt("invalid_id")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Invalid agent ID error handled")
    
    # Test empty project data
    generator.current_project = {}
    try:
        generator._generate_project_structure(Path("/invalid/path"))
        # This should not raise an error, just create the structure
        print("✅ Empty project data handled gracefully")
    except Exception as e:
        print(f"❌ Unexpected error with empty project: {e}")


def test_integration_workflow():
    """Test complete integration workflow"""
    print("\n🧪 Testing Complete Integration Workflow")
    print("=" * 45)
    
    generator = ProjectGeneratorUI()
    
    # Simulate complete workflow
    generator.current_project = {
        "name": "Integration Test Project",
        "description": "A complete integration test",
        "domain": "technology",
        "selected_patterns": [("Multi-Agent Orchestration", "pattern_1")],
        "capabilities": ["problem solving", "data analysis"],
        "communication_style": "professional",
        "integrations": [{"type": "database", "subtype": "sqlite"}],
        "test_requirements": {
            "data_types": ["user_profiles"],
            "volume": 50,
            "context": "technology"
        }
    }
    
    # Create agent configuration
    agent_config_id = generator.config_framework.create_from_template(
        "customer_service_agent",
        {
            "name": f"{generator.current_project['name']} Agent",
            "description": generator.current_project['description']
        }
    )
    generator.current_project["agent_config_id"] = agent_config_id
    
    # Test complete project generation
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir) / "integration_test"
        
        try:
            # Generate all files
            generator._generate_project_structure(project_dir)
            generator._generate_agent_configs(project_dir)
            generator._generate_schemas(project_dir)
            generator._generate_prompts(project_dir)
            generator._generate_test_data(project_dir)
            generator._generate_mcp_configs(project_dir)
            generator._generate_documentation(project_dir)
            generator._generate_setup_files(project_dir)
            
            # Verify all files exist
            expected_files = [
                "main.py",
                "requirements.txt",
                "README.md",
                ".env.example",
                "configs/agent_config.json",
                "configs/mcp_config.json",
                "schemas/selected_patterns.json",
                "prompts/agent_instructions.md",
                "test_data/user_profiles.json"
            ]
            
            for file_path in expected_files:
                assert (project_dir / file_path).exists(), f"Missing file: {file_path}"
            
            print("✅ Complete integration workflow works")
            
        except Exception as e:
            print(f"❌ Error in integration workflow: {e}")
            raise


def main():
    """Run all tests"""
    print("🚀 Starting Project Generator Tests")
    print("=" * 50)
    
    test_project_generator_initialization()
    test_project_basic_info()
    test_pattern_selection()
    test_agent_personality_configuration()
    test_capabilities_configuration()
    test_external_integrations()
    test_testing_requirements()
    test_project_file_generation()
    test_custom_agent_creation()
    test_error_handling()
    test_integration_workflow()
    
    print("\n🎉 All Project Generator tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    main()





