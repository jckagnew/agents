"""
Test suite for JSON Schema Templates
"""

import json
import tempfile
import shutil
import sys
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from agent_schemas import AgentSchemaGenerator


def test_all_pattern_schemas():
    """Test all pattern schemas"""
    print("🧪 Testing All Pattern Schemas")
    print("=" * 40)
    
    generator = AgentSchemaGenerator()
    schemas = generator.get_pattern_schemas()
    
    # Test that we have all expected patterns
    expected_patterns = [
        "pattern_1", "pattern_2", "pattern_3", "pattern_4", "pattern_8",
        "pattern_10", "pattern_11", "pattern_12", "pattern_13", "pattern_14",
        "pattern_15", "pattern_16", "pattern_17", "pattern_18", "pattern_19", "pattern_20"
    ]
    
    for pattern_id in expected_patterns:
        assert pattern_id in schemas, f"Missing schema for {pattern_id}"
        schema = schemas[pattern_id]
        
        # Test required fields
        required_fields = ["pattern_id", "pattern_name", "description", "agent_type", "domain", "context", "capabilities", "data_structures", "configuration"]
        for field in required_fields:
            assert field in schema, f"Missing {field} in {pattern_id}"
        
        print(f"✅ {pattern_id}: {schema['pattern_name']}")
    
    print(f"✅ All {len(schemas)} pattern schemas validated")


def test_schema_validation():
    """Test schema validation functionality"""
    print("\n🧪 Testing Schema Validation")
    print("=" * 30)
    
    generator = AgentSchemaGenerator()
    
    # Test valid configuration
    valid_config = {
        "agent_type": "orchestrator",
        "domain": "multi_agent_systems",
        "capabilities": ["task_decomposition", "agent_coordination"],
        "data_structures": {"agent_registry": "array"}
    }
    
    is_valid = generator.validate_agent_config(valid_config, "pattern_1")
    assert is_valid
    print("✅ Valid configuration passes validation")
    
    # Test invalid configuration
    invalid_config = {
        "agent_type": "orchestrator",
        "domain": "multi_agent_systems"
        # Missing required fields
    }
    
    is_valid = generator.validate_agent_config(invalid_config, "pattern_1")
    assert not is_valid
    print("✅ Invalid configuration fails validation")
    
    # Test non-existent pattern
    is_valid = generator.validate_agent_config(valid_config, "pattern_999")
    assert not is_valid
    print("✅ Non-existent pattern fails validation")


def test_schema_export_import():
    """Test schema export and import functionality"""
    print("\n🧪 Testing Schema Export/Import")
    print("=" * 35)
    
    generator = AgentSchemaGenerator()
    
    # Test JSON export
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        generator.export_all_schemas_to_json(temp_file)
        
        # Verify file was created and contains data
        with open(temp_file, 'r') as f:
            exported_data = json.load(f)
        
        assert len(exported_data) == 16
        assert "pattern_1" in exported_data
        assert exported_data["pattern_1"]["pattern_name"] == "Multi-Agent Orchestration"
        print("✅ Schema export works")
        
        # Test individual schema generation
        pattern_1_schema = generator.generate_schema_for_pattern("pattern_1")
        assert pattern_1_schema["pattern_name"] == "Multi-Agent Orchestration"
        print("✅ Individual schema generation works")
        
    finally:
        # Clean up
        import os
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_schema_structure():
    """Test schema structure and content"""
    print("\n🧪 Testing Schema Structure")
    print("=" * 30)
    
    generator = AgentSchemaGenerator()
    schemas = generator.get_pattern_schemas()
    
    for pattern_id, schema in schemas.items():
        # Test pattern_id matches key
        assert schema["pattern_id"] == pattern_id
        
        # Test agent_type is valid
        valid_agent_types = [
            "orchestrator", "communicator", "collaborator", "learner", "memory_manager",
            "goal_manager", "error_handler", "adapter", "creative_agent", "empathic_agent",
            "resource_optimizer", "ethical_agent", "evaluator", "safety_guardian",
            "evolving_agent", "swarm_agent"
        ]
        assert schema["agent_type"] in valid_agent_types
        
        # Test capabilities is a list
        assert isinstance(schema["capabilities"], list)
        assert len(schema["capabilities"]) > 0
        
        # Test data_structures is a dict
        assert isinstance(schema["data_structures"], dict)
        assert len(schema["data_structures"]) > 0
        
        # Test configuration is a dict
        assert isinstance(schema["configuration"], dict)
        assert len(schema["configuration"]) > 0
        
        print(f"✅ {pattern_id} structure validated")


def test_example_configurations():
    """Test example configurations for each pattern"""
    print("\n🧪 Testing Example Configurations")
    print("=" * 40)
    
    generator = AgentSchemaGenerator()
    
    # Create example configurations for each pattern
    example_configs = {
        "pattern_1": {
            "agent_type": "orchestrator",
            "domain": "multi_agent_systems",
            "capabilities": ["task_decomposition", "agent_coordination", "workflow_management"],
            "data_structures": {
                "agent_registry": "array",
                "task_queue": "array",
                "workflow_state": "object"
            },
            "configuration": {
                "max_concurrent_agents": 10,
                "task_timeout": 300,
                "coordination_strategy": "centralized"
            }
        },
        "pattern_13": {
            "agent_type": "creative_agent",
            "domain": "creative_ai",
            "capabilities": ["idea_generation", "creative_pattern_recognition", "constraint_handling"],
            "data_structures": {
                "creative_session": "object",
                "creative_idea": "object"
            },
            "configuration": {
                "max_ideas_per_session": 50,
                "novelty_threshold": 0.6,
                "creativity_type": "divergent"
            }
        },
        "pattern_16": {
            "agent_type": "ethical_agent",
            "domain": "ethical_ai",
            "capabilities": ["ethical_reasoning", "violation_detection", "risk_assessment"],
            "data_structures": {
                "ethical_rule": "object",
                "ethical_decision": "object"
            },
            "configuration": {
                "decision_confidence_threshold": 0.8,
                "human_review_threshold": 0.6,
                "compliance_reporting": True
            }
        }
    }
    
    for pattern_id, config in example_configs.items():
        is_valid = generator.validate_agent_config(config, pattern_id)
        assert is_valid, f"Example configuration for {pattern_id} failed validation"
        print(f"✅ {pattern_id} example configuration validated")


def main():
    """Run all tests"""
    print("🚀 Starting JSON Schema Templates Tests")
    print("=" * 50)
    
    test_all_pattern_schemas()
    test_schema_validation()
    test_schema_export_import()
    test_schema_structure()
    test_example_configurations()
    
    print("\n🎉 All JSON Schema Templates tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    main()

