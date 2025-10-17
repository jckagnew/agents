"""
JSON Schema Templates for All 20 Agentic Design Patterns

This module provides structured JSON schemas for each agent pattern,
following Ravi Mehta's data-driven prototyping approach.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class AgentSchemaGenerator:
    """Generates structured JSON schemas for agent patterns"""
    
    @staticmethod
    def get_pattern_schemas() -> Dict[str, Dict[str, Any]]:
        """Get all pattern schemas"""
        return {
            "pattern_1": AgentSchemaGenerator._get_orchestration_schema(),
            "pattern_2": AgentSchemaGenerator._get_communication_schema(),
            "pattern_3": AgentSchemaGenerator._get_collaboration_schema(),
            "pattern_4": AgentSchemaGenerator._get_learning_schema(),
            "pattern_8": AgentSchemaGenerator._get_memory_schema(),
            "pattern_10": AgentSchemaGenerator._get_goal_monitoring_schema(),
            "pattern_11": AgentSchemaGenerator._get_exception_handling_schema(),
            "pattern_12": AgentSchemaGenerator._get_adaptation_schema(),
            "pattern_13": AgentSchemaGenerator._get_creativity_schema(),
            "pattern_14": AgentSchemaGenerator._get_empathy_schema(),
            "pattern_15": AgentSchemaGenerator._get_resource_optimization_schema(),
            "pattern_16": AgentSchemaGenerator._get_ethics_schema(),
            "pattern_17": AgentSchemaGenerator._get_evaluation_schema(),
            "pattern_18": AgentSchemaGenerator._get_guardrails_schema(),
            "pattern_19": AgentSchemaGenerator._get_evolution_schema(),
            "pattern_20": AgentSchemaGenerator._get_swarming_schema()
        }
    
    @staticmethod
    def _get_orchestration_schema() -> Dict[str, Any]:
        """Pattern 1: Multi-Agent Orchestration Schema"""
        return {
            "pattern_id": "pattern_1",
            "pattern_name": "Multi-Agent Orchestration",
            "description": "Coordinates multiple agents to work together on complex tasks",
            "agent_type": "orchestrator",
            "domain": "multi_agent_systems",
            "context": {
                "environment": "distributed_system",
                "coordination_level": "high",
                "task_complexity": "complex",
                "scalability_requirements": "high"
            },
            "capabilities": [
                "task_decomposition",
                "agent_coordination",
                "workflow_management",
                "resource_allocation",
                "conflict_resolution"
            ],
            "data_structures": {
                "agent_registry": {
                    "type": "array",
                    "items": {
                        "agent_id": "string",
                        "capabilities": "array",
                        "status": "string",
                        "performance_metrics": "object"
                    }
                },
                "task_queue": {
                    "type": "array",
                    "items": {
                        "task_id": "string",
                        "description": "string",
                        "priority": "integer",
                        "assigned_agent": "string",
                        "status": "string",
                        "dependencies": "array"
                    }
                },
                "workflow_state": {
                    "current_phase": "string",
                    "completed_tasks": "array",
                    "active_tasks": "array",
                    "pending_tasks": "array"
                }
            },
            "configuration": {
                "max_concurrent_agents": 10,
                "task_timeout": 300,
                "retry_attempts": 3,
                "coordination_strategy": "centralized"
            },
            "constraints": [
                "agent_availability",
                "resource_limits",
                "task_dependencies",
                "communication_latency"
            ],
            "performance_metrics": {
                "task_completion_rate": "float",
                "average_task_duration": "float",
                "agent_utilization": "float",
                "coordination_overhead": "float"
            }
        }
    
    @staticmethod
    def _get_communication_schema() -> Dict[str, Any]:
        """Pattern 2: Agent Communication Schema"""
        return {
            "pattern_id": "pattern_2",
            "pattern_name": "Agent Communication",
            "description": "Enables structured communication between agents",
            "agent_type": "communicator",
            "domain": "inter_agent_communication",
            "context": {
                "communication_protocol": "message_passing",
                "message_types": ["request", "response", "notification", "broadcast"],
                "reliability": "high",
                "latency_requirements": "low"
            },
            "capabilities": [
                "message_routing",
                "protocol_handling",
                "message_queuing",
                "delivery_confirmation",
                "error_handling"
            ],
            "data_structures": {
                "message": {
                    "message_id": "string",
                    "sender_id": "string",
                    "recipient_id": "string",
                    "message_type": "string",
                    "content": "object",
                    "timestamp": "datetime",
                    "priority": "integer",
                    "status": "string"
                },
                "channel": {
                    "channel_id": "string",
                    "name": "string",
                    "participants": "array",
                    "message_history": "array",
                    "settings": "object"
                }
            },
            "configuration": {
                "max_message_size": 1024,
                "message_ttl": 3600,
                "retry_attempts": 3,
                "encryption_enabled": True
            },
            "constraints": [
                "message_size_limits",
                "network_bandwidth",
                "security_requirements",
                "compatibility_requirements"
            ]
        }
    
    @staticmethod
    def _get_collaboration_schema() -> Dict[str, Any]:
        """Pattern 3: Agent Collaboration Schema"""
        return {
            "pattern_id": "pattern_3",
            "pattern_name": "Agent Collaboration",
            "description": "Facilitates collaborative work between agents",
            "agent_type": "collaborator",
            "domain": "collaborative_ai",
            "context": {
                "collaboration_type": "shared_workspace",
                "conflict_resolution": "automatic",
                "consensus_mechanism": "voting",
                "transparency_level": "high"
            },
            "capabilities": [
                "workspace_management",
                "conflict_detection",
                "consensus_building",
                "shared_resource_access",
                "collaborative_decision_making"
            ],
            "data_structures": {
                "workspace": {
                    "workspace_id": "string",
                    "name": "string",
                    "participants": "array",
                    "shared_resources": "array",
                    "collaboration_rules": "object"
                },
                "collaboration_event": {
                    "event_id": "string",
                    "workspace_id": "string",
                    "event_type": "string",
                    "participants": "array",
                    "timestamp": "datetime",
                    "data": "object"
                }
            },
            "configuration": {
                "max_participants": 20,
                "conflict_timeout": 60,
                "consensus_threshold": 0.7,
                "auto_resolve_conflicts": True
            }
        }
    
    @staticmethod
    def _get_learning_schema() -> Dict[str, Any]:
        """Pattern 4: Agent Learning Schema"""
        return {
            "pattern_id": "pattern_4",
            "pattern_name": "Agent Learning",
            "description": "Enables agents to learn and improve from experience",
            "agent_type": "learner",
            "domain": "machine_learning",
            "context": {
                "learning_type": "online_learning",
                "feedback_source": "environment",
                "adaptation_rate": "moderate",
                "knowledge_retention": "persistent"
            },
            "capabilities": [
                "pattern_recognition",
                "model_training",
                "knowledge_extraction",
                "performance_optimization",
                "experience_integration"
            ],
            "data_structures": {
                "learning_example": {
                    "example_id": "string",
                    "input_data": "object",
                    "expected_output": "object",
                    "actual_output": "object",
                    "quality_score": "float",
                    "timestamp": "datetime"
                },
                "learning_pattern": {
                    "pattern_id": "string",
                    "pattern_type": "string",
                    "confidence": "float",
                    "frequency": "integer",
                    "success_rate": "float",
                    "last_used": "datetime"
                }
            },
            "configuration": {
                "learning_rate": 0.01,
                "batch_size": 32,
                "max_patterns": 1000,
                "retention_period": 30
            }
        }
    
    @staticmethod
    def _get_memory_schema() -> Dict[str, Any]:
        """Pattern 8: Memory Management Schema"""
        return {
            "pattern_id": "pattern_8",
            "pattern_name": "Memory Management",
            "description": "Manages persistent memory and knowledge retention",
            "agent_type": "memory_manager",
            "domain": "knowledge_management",
            "context": {
                "memory_types": ["short_term", "long_term", "episodic", "semantic"],
                "storage_backend": "sqlite",
                "retrieval_strategy": "semantic_search",
                "capacity_management": "automatic"
            },
            "capabilities": [
                "memory_storage",
                "knowledge_retrieval",
                "context_management",
                "memory_consolidation",
                "forgetting_mechanisms"
            ],
            "data_structures": {
                "memory": {
                    "memory_id": "string",
                    "content": "object",
                    "memory_type": "string",
                    "priority": "integer",
                    "access_count": "integer",
                    "created_at": "datetime",
                    "last_accessed": "datetime"
                },
                "context": {
                    "context_id": "string",
                    "context_type": "string",
                    "related_memories": "array",
                    "relevance_score": "float",
                    "timestamp": "datetime"
                }
            },
            "configuration": {
                "max_memory_size": 10000,
                "consolidation_threshold": 0.8,
                "forgetting_rate": 0.1,
                "search_similarity_threshold": 0.7
            }
        }
    
    @staticmethod
    def _get_goal_monitoring_schema() -> Dict[str, Any]:
        """Pattern 10: Goal Setting & Monitoring Schema"""
        return {
            "pattern_id": "pattern_10",
            "pattern_name": "Goal Setting & Monitoring",
            "description": "Manages agent goals and progress tracking",
            "agent_type": "goal_manager",
            "domain": "goal_management",
            "context": {
                "goal_types": ["performance", "learning", "behavioral", "outcome"],
                "tracking_frequency": "continuous",
                "adjustment_mechanism": "adaptive",
                "success_criteria": "quantifiable"
            },
            "capabilities": [
                "goal_definition",
                "progress_tracking",
                "milestone_detection",
                "goal_adjustment",
                "achievement_recording"
            ],
            "data_structures": {
                "goal": {
                    "goal_id": "string",
                    "description": "string",
                    "goal_type": "string",
                    "priority": "integer",
                    "target_value": "float",
                    "current_value": "float",
                    "deadline": "datetime",
                    "status": "string"
                },
                "milestone": {
                    "milestone_id": "string",
                    "goal_id": "string",
                    "description": "string",
                    "target_value": "float",
                    "achieved_at": "datetime",
                    "reward": "object"
                }
            },
            "configuration": {
                "max_active_goals": 10,
                "check_interval": 60,
                "adjustment_threshold": 0.2,
                "auto_goal_creation": False
            }
        }
    
    @staticmethod
    def _get_exception_handling_schema() -> Dict[str, Any]:
        """Pattern 11: Exception Handling Schema"""
        return {
            "pattern_id": "pattern_11",
            "pattern_name": "Exception Handling & Recovery",
            "description": "Handles errors and implements recovery strategies",
            "agent_type": "error_handler",
            "domain": "error_management",
            "context": {
                "error_severity_levels": ["low", "medium", "high", "critical"],
                "recovery_strategies": ["retry", "fallback", "escalation", "shutdown"],
                "monitoring_level": "continuous",
                "alerting_threshold": "medium"
            },
            "capabilities": [
                "error_detection",
                "error_classification",
                "recovery_execution",
                "escalation_management",
                "system_monitoring"
            ],
            "data_structures": {
                "error": {
                    "error_id": "string",
                    "error_type": "string",
                    "severity": "string",
                    "message": "string",
                    "context": "object",
                    "timestamp": "datetime",
                    "resolved": "boolean"
                },
                "recovery_action": {
                    "action_id": "string",
                    "error_id": "string",
                    "strategy": "string",
                    "parameters": "object",
                    "success": "boolean",
                    "execution_time": "float"
                }
            },
            "configuration": {
                "max_retry_attempts": 3,
                "retry_delay": 5,
                "escalation_timeout": 300,
                "auto_recovery": True
            }
        }
    
    @staticmethod
    def _get_adaptation_schema() -> Dict[str, Any]:
        """Pattern 12: Agent Adaptation Schema"""
        return {
            "pattern_id": "pattern_12",
            "pattern_name": "Agent Adaptation",
            "description": "Enables dynamic behavior modification based on context",
            "agent_type": "adapter",
            "domain": "adaptive_ai",
            "context": {
                "adaptation_triggers": ["performance", "environment", "user_feedback", "context_change"],
                "adaptation_speed": "moderate",
                "reversibility": "partial",
                "stability_requirements": "high"
            },
            "capabilities": [
                "behavior_modification",
                "context_analysis",
                "adaptation_planning",
                "change_execution",
                "performance_monitoring"
            ],
            "data_structures": {
                "adaptation_profile": {
                    "profile_id": "string",
                    "agent_id": "string",
                    "personality_traits": "object",
                    "behavior_patterns": "object",
                    "adaptation_history": "array"
                },
                "adaptation_event": {
                    "event_id": "string",
                    "agent_id": "string",
                    "trigger": "string",
                    "old_state": "object",
                    "new_state": "object",
                    "success": "boolean",
                    "timestamp": "datetime"
                }
            },
            "configuration": {
                "adaptation_threshold": 0.7,
                "max_adaptations_per_hour": 10,
                "rollback_enabled": True,
                "learning_from_adaptations": True
            }
        }
    
    @staticmethod
    def _get_creativity_schema() -> Dict[str, Any]:
        """Pattern 13: Agent Creativity Schema"""
        return {
            "pattern_id": "pattern_13",
            "pattern_name": "Agent Creativity",
            "description": "Enables creative problem-solving and content generation",
            "agent_type": "creative_agent",
            "domain": "creative_ai",
            "context": {
                "creativity_types": ["divergent", "convergent", "lateral", "systematic"],
                "inspiration_sources": ["patterns", "constraints", "randomness", "user_input"],
                "novelty_requirements": "high",
                "feasibility_balance": "moderate"
            },
            "capabilities": [
                "idea_generation",
                "creative_pattern_recognition",
                "constraint_handling",
                "novelty_assessment",
                "creative_iteration"
            ],
            "data_structures": {
                "creative_session": {
                    "session_id": "string",
                    "prompt": "string",
                    "creativity_type": "string",
                    "constraints": "array",
                    "ideas": "array",
                    "best_idea": "string"
                },
                "creative_idea": {
                    "idea_id": "string",
                    "content": "string",
                    "novelty_score": "float",
                    "feasibility_score": "float",
                    "value_score": "float",
                    "constraints_met": "array"
                }
            },
            "configuration": {
                "max_ideas_per_session": 50,
                "novelty_threshold": 0.6,
                "feasibility_weight": 0.4,
                "constraint_strictness": "moderate"
            }
        }
    
    @staticmethod
    def _get_empathy_schema() -> Dict[str, Any]:
        """Pattern 14: Agent Empathy Schema"""
        return {
            "pattern_id": "pattern_14",
            "pattern_name": "Agent Empathy",
            "description": "Provides emotional intelligence and user understanding",
            "agent_type": "empathic_agent",
            "domain": "emotional_ai",
            "context": {
                "emotion_types": ["joy", "sadness", "anger", "fear", "surprise", "disgust"],
                "empathy_contexts": ["personal", "professional", "customer_service", "crisis"],
                "response_types": ["validation", "support", "encouragement", "acknowledgment"],
                "cultural_sensitivity": "high"
            },
            "capabilities": [
                "emotion_detection",
                "empathy_response_generation",
                "emotional_context_analysis",
                "user_preference_learning",
                "cultural_adaptation"
            ],
            "data_structures": {
                "emotional_state": {
                    "state_id": "string",
                    "user_id": "string",
                    "primary_emotion": "string",
                    "intensity": "float",
                    "confidence": "float",
                    "context": "string",
                    "triggers": "array"
                },
                "empathy_response": {
                    "response_id": "string",
                    "user_id": "string",
                    "response_type": "string",
                    "content": "string",
                    "empathy_level": "float",
                    "appropriateness_score": "float"
                }
            },
            "configuration": {
                "emotion_detection_threshold": 0.7,
                "response_generation_delay": 2,
                "cultural_adaptation_enabled": True,
                "empathy_level": "moderate"
            }
        }
    
    @staticmethod
    def _get_resource_optimization_schema() -> Dict[str, Any]:
        """Pattern 15: Resource-Aware Optimization Schema"""
        return {
            "pattern_id": "pattern_15",
            "pattern_name": "Resource-Aware Optimization",
            "description": "Monitors and optimizes resource usage",
            "agent_type": "resource_optimizer",
            "domain": "resource_management",
            "context": {
                "resource_types": ["cpu", "memory", "disk", "network", "api_calls", "tokens"],
                "optimization_strategies": ["load_balancing", "caching", "compression", "batching"],
                "monitoring_frequency": "continuous",
                "alerting_thresholds": "dynamic"
            },
            "capabilities": [
                "resource_monitoring",
                "usage_optimization",
                "threshold_alerting",
                "capacity_planning",
                "cost_optimization"
            ],
            "data_structures": {
                "resource_metric": {
                    "metric_id": "string",
                    "resource_type": "string",
                    "current_usage": "float",
                    "threshold": "float",
                    "timestamp": "datetime",
                    "trend": "string"
                },
                "optimization_action": {
                    "action_id": "string",
                    "resource_type": "string",
                    "action_type": "string",
                    "parameters": "object",
                    "effectiveness": "float",
                    "timestamp": "datetime"
                }
            },
            "configuration": {
                "monitoring_interval": 30,
                "optimization_frequency": 300,
                "alert_cooldown": 60,
                "auto_optimization": True
            }
        }
    
    @staticmethod
    def _get_ethics_schema() -> Dict[str, Any]:
        """Pattern 16: Agent Ethics Schema"""
        return {
            "pattern_id": "pattern_16",
            "pattern_name": "Agent Ethics",
            "description": "Implements ethical decision-making and moral reasoning",
            "agent_type": "ethical_agent",
            "domain": "ethical_ai",
            "context": {
                "ethical_principles": ["autonomy", "beneficence", "non_maleficence", "justice", "transparency"],
                "decision_types": ["automated", "human_review", "escalation", "blocked"],
                "violation_types": ["bias", "privacy_breach", "manipulation", "harm", "discrimination"],
                "compliance_requirements": "high"
            },
            "capabilities": [
                "ethical_reasoning",
                "violation_detection",
                "risk_assessment",
                "compliance_monitoring",
                "ethical_guidance"
            ],
            "data_structures": {
                "ethical_rule": {
                    "rule_id": "string",
                    "principle": "string",
                    "condition": "string",
                    "action": "string",
                    "priority": "integer",
                    "weight": "float"
                },
                "ethical_decision": {
                    "decision_id": "string",
                    "reasoning": "string",
                    "principles_applied": "array",
                    "confidence_score": "float",
                    "risk_assessment": "object"
                }
            },
            "configuration": {
                "decision_confidence_threshold": 0.8,
                "human_review_threshold": 0.6,
                "violation_alerting": True,
                "compliance_reporting": True
            }
        }
    
    @staticmethod
    def _get_evaluation_schema() -> Dict[str, Any]:
        """Pattern 17: Evaluation & Monitoring Schema"""
        return {
            "pattern_id": "pattern_17",
            "pattern_name": "Evaluation & Monitoring",
            "description": "Evaluates agent performance and system health",
            "agent_type": "evaluator",
            "domain": "performance_monitoring",
            "context": {
                "evaluation_metrics": ["accuracy", "efficiency", "reliability", "user_satisfaction"],
                "monitoring_frequency": "continuous",
                "alerting_thresholds": "dynamic",
                "reporting_frequency": "daily"
            },
            "capabilities": [
                "performance_evaluation",
                "metric_collection",
                "trend_analysis",
                "alerting",
                "reporting"
            ],
            "data_structures": {
                "evaluation_metric": {
                    "metric_id": "string",
                    "metric_name": "string",
                    "value": "float",
                    "threshold": "float",
                    "status": "string",
                    "timestamp": "datetime"
                },
                "evaluation_report": {
                    "report_id": "string",
                    "period": "string",
                    "metrics": "object",
                    "trends": "object",
                    "recommendations": "array"
                }
            },
            "configuration": {
                "evaluation_interval": 3600,
                "metric_retention_days": 30,
                "alert_cooldown": 300,
                "auto_reporting": True
            }
        }
    
    @staticmethod
    def _get_guardrails_schema() -> Dict[str, Any]:
        """Pattern 18: Guardrails & Safety Schema"""
        return {
            "pattern_id": "pattern_18",
            "pattern_name": "Guardrails & Safety",
            "description": "Implements safety measures and content filtering",
            "agent_type": "safety_guardian",
            "domain": "ai_safety",
            "context": {
                "safety_categories": ["content_moderation", "bias_detection", "privacy_protection", "injection_prevention"],
                "filtering_levels": ["strict", "moderate", "permissive"],
                "monitoring_mode": "real_time",
                "response_actions": ["block", "flag", "modify", "allow"]
            },
            "capabilities": [
                "content_filtering",
                "bias_detection",
                "privacy_protection",
                "injection_prevention",
                "safety_monitoring"
            ],
            "data_structures": {
                "safety_rule": {
                    "rule_id": "string",
                    "category": "string",
                    "pattern": "string",
                    "action": "string",
                    "severity": "string",
                    "enabled": "boolean"
                },
                "safety_incident": {
                    "incident_id": "string",
                    "rule_triggered": "string",
                    "content": "string",
                    "action_taken": "string",
                    "severity": "string",
                    "timestamp": "datetime"
                }
            },
            "configuration": {
                "filtering_sensitivity": "moderate",
                "auto_response_enabled": True,
                "human_review_threshold": "high",
                "incident_logging": True
            }
        }
    
    @staticmethod
    def _get_evolution_schema() -> Dict[str, Any]:
        """Pattern 19: Agent Evolution Schema"""
        return {
            "pattern_id": "pattern_19",
            "pattern_name": "Agent Evolution",
            "description": "Enables adaptive learning and self-improvement",
            "agent_type": "evolving_agent",
            "domain": "evolutionary_ai",
            "context": {
                "evolution_strategies": ["genetic_algorithm", "particle_swarm", "simulated_annealing"],
                "mutation_types": ["gaussian", "uniform", "polynomial", "adaptive"],
                "selection_types": ["tournament", "rank_selection", "roulette_wheel", "elitism"],
                "fitness_functions": ["accuracy", "efficiency", "robustness", "adaptability"]
            },
            "capabilities": [
                "genetic_operations",
                "fitness_evaluation",
                "population_management",
                "evolution_tracking",
                "performance_optimization"
            ],
            "data_structures": {
                "agent_genome": {
                    "genome_id": "string",
                    "agent_id": "string",
                    "generation": "integer",
                    "genes": "object",
                    "fitness_score": "float",
                    "performance_metrics": "object"
                },
                "evolution_experiment": {
                    "experiment_id": "string",
                    "strategy": "string",
                    "population_size": "integer",
                    "max_generations": "integer",
                    "current_generation": "integer",
                    "best_fitness": "float"
                }
            },
            "configuration": {
                "population_size": 50,
                "mutation_rate": 0.1,
                "crossover_rate": 0.8,
                "max_generations": 100
            }
        }
    
    @staticmethod
    def _get_swarming_schema() -> Dict[str, Any]:
        """Pattern 20: Agent Swarming Schema"""
        return {
            "pattern_id": "pattern_20",
            "pattern_name": "Agent Swarming",
            "description": "Coordinates multi-agent collective behavior",
            "agent_type": "swarm_agent",
            "domain": "swarm_intelligence",
            "context": {
                "swarm_algorithms": ["particle_swarm", "ant_colony", "bee_algorithm", "flocking"],
                "agent_roles": ["leader", "follower", "scout", "worker", "coordinator"],
                "behaviors": ["exploration", "exploitation", "convergence", "divergence"],
                "coordination_level": "high"
            },
            "capabilities": [
                "swarm_coordination",
                "collective_decision_making",
                "emergent_behavior",
                "spatial_coordination",
                "communication_networking"
            ],
            "data_structures": {
                "swarm_agent": {
                    "agent_id": "string",
                    "swarm_id": "string",
                    "role": "string",
                    "position": "object",
                    "velocity": "object",
                    "fitness": "float",
                    "neighbors": "array"
                },
                "swarm": {
                    "swarm_id": "string",
                    "algorithm": "string",
                    "behavior": "string",
                    "agents": "array",
                    "leader_id": "string",
                    "objective": "string"
                }
            },
            "configuration": {
                "max_swarm_size": 100,
                "communication_range": 50,
                "influence_radius": 25,
                "convergence_threshold": 10
            }
        }
    
    @staticmethod
    def generate_schema_for_pattern(pattern_id: str) -> Dict[str, Any]:
        """Generate schema for a specific pattern"""
        schemas = AgentSchemaGenerator.get_pattern_schemas()
        return schemas.get(pattern_id, {})
    
    @staticmethod
    def export_all_schemas_to_json(file_path: str) -> None:
        """Export all schemas to a JSON file"""
        schemas = AgentSchemaGenerator.get_pattern_schemas()
        with open(file_path, 'w') as f:
            json.dump(schemas, f, indent=2, default=str)
    
    @staticmethod
    def validate_agent_config(config: Dict[str, Any], pattern_id: str) -> bool:
        """Validate agent configuration against pattern schema"""
        schema = AgentSchemaGenerator.generate_schema_for_pattern(pattern_id)
        if not schema:
            return False
        
        # Basic validation - check required fields
        required_fields = ["agent_type", "domain", "capabilities", "data_structures"]
        for field in required_fields:
            if field not in config:
                return False
        
        return True


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing JSON Schema Templates")
    print("=" * 50)
    
    # Test schema generation
    generator = AgentSchemaGenerator()
    schemas = generator.get_pattern_schemas()
    
    print(f"✅ Generated {len(schemas)} pattern schemas")
    
    # Test individual pattern schema
    orchestration_schema = generator.generate_schema_for_pattern("pattern_1")
    assert orchestration_schema["pattern_name"] == "Multi-Agent Orchestration"
    print("✅ Pattern 1 schema generated correctly")
    
    # Test validation
    test_config = {
        "agent_type": "orchestrator",
        "domain": "multi_agent_systems",
        "capabilities": ["task_decomposition", "agent_coordination"],
        "data_structures": {"agent_registry": "array"}
    }
    
    is_valid = generator.validate_agent_config(test_config, "pattern_1")
    assert is_valid
    print("✅ Configuration validation works")
    
    # Export schemas
    generator.export_all_schemas_to_json("agent_schemas.json")
    print("✅ Schemas exported to JSON file")
    
    print("🎯 JSON Schema Templates test completed!")

