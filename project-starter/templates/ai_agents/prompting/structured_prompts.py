"""
Structured Prompting Frameworks for Agent Behavior

This module provides data-driven prompting frameworks based on Ravi Mehta's approach,
enabling agents to generate consistent, high-quality responses using structured data.
"""

import json
import logging
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptType(str, Enum):
    """Types of structured prompts"""
    TASK_ORIENTED = "task_oriented"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    CONVERSATIONAL = "conversational"
    TECHNICAL = "technical"
    EMOTIONAL = "emotional"
    DECISION_MAKING = "decision_making"
    PROBLEM_SOLVING = "problem_solving"


class PromptRole(str, Enum):
    """Roles for prompt components"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    CONTEXT = "context"
    CONSTRAINT = "constraint"
    EXAMPLE = "example"


class PromptComponent(BaseModel):
    """Individual prompt component"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: PromptRole
    content: str
    priority: int = 1
    is_required: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)


class StructuredPrompt(BaseModel):
    """Complete structured prompt"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    prompt_type: PromptType
    description: str
    components: List[PromptComponent] = Field(default_factory=list)
    variables: Dict[str, Any] = Field(default_factory=dict)
    constraints: List[str] = Field(default_factory=list)
    examples: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class PromptTemplate(BaseModel):
    """Reusable prompt template"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    template_type: PromptType
    template: str
    variables: List[str] = Field(default_factory=list)
    description: str = ""
    usage_count: int = 0
    success_rate: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)


class PromptFramework:
    """Main framework for structured prompting"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize prompt framework"""
        self.config = config or {}
        self.prompts: Dict[str, StructuredPrompt] = {}
        self.templates: Dict[str, PromptTemplate] = {}
        self.prompt_history: List[Dict[str, Any]] = []
        
        # Initialize default templates
        self._initialize_default_templates()
        
        logger.info("Structured Prompt Framework initialized")
    
    def _initialize_default_templates(self):
        """Initialize default prompt templates"""
        # Task-oriented template
        task_template = PromptTemplate(
            name="Task Execution",
            template_type=PromptType.TASK_ORIENTED,
            template="""
            SYSTEM: You are an AI agent specialized in task execution. Your role is to complete tasks efficiently and accurately.
            
            CONTEXT: {context}
            
            TASK: {task_description}
            
            CONSTRAINTS:
            - {constraints}
            
            EXPECTED_OUTPUT_FORMAT: {output_format}
            
            EXAMPLES:
            {examples}
            
            Please execute the task following the specified format and constraints.
            """,
            variables=["context", "task_description", "constraints", "output_format", "examples"],
            description="Template for task-oriented prompts"
        )
        self.templates["task_execution"] = task_template
        
        # Creative template
        creative_template = PromptTemplate(
            name="Creative Generation",
            template_type=PromptType.CREATIVE,
            template="""
            SYSTEM: You are a creative AI agent with expertise in {domain}. Your role is to generate original, innovative content.
            
            CREATIVE_BRIEF: {brief}
            
            STYLE_GUIDELINES:
            - {style_guidelines}
            
            CONSTRAINTS:
            - {constraints}
            
            INSPIRATION_SOURCES: {inspiration_sources}
            
            OUTPUT_REQUIREMENTS:
            - {output_requirements}
            
            Please generate creative content that meets all requirements.
            """,
            variables=["domain", "brief", "style_guidelines", "constraints", "inspiration_sources", "output_requirements"],
            description="Template for creative prompts"
        )
        self.templates["creative_generation"] = creative_template
        
        # Analytical template
        analytical_template = PromptTemplate(
            name="Data Analysis",
            template_type=PromptType.ANALYTICAL,
            template="""
            SYSTEM: You are an analytical AI agent specializing in data analysis and insights generation.
            
            DATA_CONTEXT: {data_context}
            
            ANALYSIS_OBJECTIVE: {objective}
            
            METHODOLOGY: {methodology}
            
            KEY_METRICS: {key_metrics}
            
            HYPOTHESIS: {hypothesis}
            
            OUTPUT_FORMAT: {output_format}
            
            Please provide a comprehensive analysis following the specified methodology.
            """,
            variables=["data_context", "objective", "methodology", "key_metrics", "hypothesis", "output_format"],
            description="Template for analytical prompts"
        )
        self.templates["data_analysis"] = analytical_template
        
        # Conversational template
        conversational_template = PromptTemplate(
            name="Conversational Agent",
            template_type=PromptType.CONVERSATIONAL,
            template="""
            SYSTEM: You are a conversational AI agent with a {personality} personality. Your role is to engage in natural, helpful conversations.
            
            CONVERSATION_CONTEXT: {context}
            
            USER_MESSAGE: {user_message}
            
            CONVERSATION_HISTORY: {conversation_history}
            
            RESPONSE_GUIDELINES:
            - {response_guidelines}
            
            EMOTIONAL_TONE: {emotional_tone}
            
            Please respond in a natural, engaging manner that matches the specified personality and tone.
            """,
            variables=["personality", "context", "user_message", "conversation_history", "response_guidelines", "emotional_tone"],
            description="Template for conversational prompts"
        )
        self.templates["conversational"] = conversational_template
    
    def create_structured_prompt(self, name: str, prompt_type: PromptType, 
                               description: str, components: List[PromptComponent],
                               variables: Optional[Dict[str, Any]] = None,
                               constraints: Optional[List[str]] = None,
                               examples: Optional[List[Dict[str, Any]]] = None) -> str:
        """Create a new structured prompt"""
        prompt = StructuredPrompt(
            name=name,
            prompt_type=prompt_type,
            description=description,
            components=components,
            variables=variables or {},
            constraints=constraints or [],
            examples=examples or []
        )
        
        self.prompts[prompt.id] = prompt
        logger.info(f"Created structured prompt: {name}")
        return prompt.id
    
    def create_prompt_from_template(self, template_name: str, variables: Dict[str, Any],
                                  custom_components: Optional[List[PromptComponent]] = None) -> str:
        """Create a prompt from a template"""
        if template_name not in self.templates:
            raise ValueError(f"Template not found: {template_name}")
        
        template = self.templates[template_name]
        
        # Fill template with variables
        filled_template = template.template.format(**variables)
        
        # Create components
        components = [
            PromptComponent(
                role=PromptRole.SYSTEM,
                content=filled_template,
                priority=1,
                is_required=True
            )
        ]
        
        # Add custom components if provided
        if custom_components:
            components.extend(custom_components)
        
        # Create structured prompt
        prompt_id = self.create_structured_prompt(
            name=f"{template.name} - {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            prompt_type=template.template_type,
            description=f"Generated from template: {template.name}",
            components=components,
            variables=variables
        )
        
        # Update template usage
        template.usage_count += 1
        
        return prompt_id
    
    def generate_prompt_text(self, prompt_id: str, additional_variables: Optional[Dict[str, Any]] = None) -> str:
        """Generate final prompt text from structured prompt"""
        if prompt_id not in self.prompts:
            raise ValueError(f"Prompt not found: {prompt_id}")
        
        prompt = self.prompts[prompt_id]
        variables = {**prompt.variables, **(additional_variables or {})}
        
        # Sort components by priority
        sorted_components = sorted(prompt.components, key=lambda c: c.priority)
        
        # Generate prompt text
        prompt_parts = []
        for component in sorted_components:
            if component.is_required or component.priority <= 2:
                # Fill variables in component content
                try:
                    filled_content = component.content.format(**variables)
                    prompt_parts.append(f"{component.role.value.upper()}: {filled_content}")
                except KeyError as e:
                    logger.warning(f"Missing variable {e} in component {component.id}")
                    prompt_parts.append(f"{component.role.value.upper()}: {component.content}")
        
        # Add examples if any
        if prompt.examples:
            prompt_parts.append("EXAMPLES:")
            for i, example in enumerate(prompt.examples, 1):
                prompt_parts.append(f"Example {i}: {json.dumps(example, indent=2)}")
        
        # Add constraints if any
        if prompt.constraints:
            prompt_parts.append("CONSTRAINTS:")
            for constraint in prompt.constraints:
                prompt_parts.append(f"- {constraint}")
        
        final_prompt = "\n\n".join(prompt_parts)
        
        # Log prompt generation
        self.prompt_history.append({
            "prompt_id": prompt_id,
            "timestamp": datetime.now(),
            "variables_used": variables,
            "prompt_length": len(final_prompt)
        })
        
        return final_prompt
    
    def add_component_to_prompt(self, prompt_id: str, component: PromptComponent) -> bool:
        """Add a component to an existing prompt"""
        if prompt_id not in self.prompts:
            return False
        
        self.prompts[prompt_id].components.append(component)
        self.prompts[prompt_id].updated_at = datetime.now()
        return True
    
    def update_prompt_variables(self, prompt_id: str, variables: Dict[str, Any]) -> bool:
        """Update variables for a prompt"""
        if prompt_id not in self.prompts:
            return False
        
        self.prompts[prompt_id].variables.update(variables)
        self.prompts[prompt_id].updated_at = datetime.now()
        return True
    
    def get_prompt_by_type(self, prompt_type: PromptType) -> List[StructuredPrompt]:
        """Get all prompts of a specific type"""
        return [prompt for prompt in self.prompts.values() if prompt.prompt_type == prompt_type]
    
    def get_template_by_type(self, template_type: PromptType) -> List[PromptTemplate]:
        """Get all templates of a specific type"""
        return [template for template in self.templates.values() if template.template_type == template_type]
    
    def search_prompts(self, query: str) -> List[StructuredPrompt]:
        """Search prompts by name or description"""
        query_lower = query.lower()
        results = []
        
        for prompt in self.prompts.values():
            if (query_lower in prompt.name.lower() or 
                query_lower in prompt.description.lower()):
                results.append(prompt)
        
        return results
    
    def get_prompt_statistics(self) -> Dict[str, Any]:
        """Get framework statistics"""
        total_prompts = len(self.prompts)
        total_templates = len(self.templates)
        
        # Count by type
        prompt_types = {}
        for prompt in self.prompts.values():
            prompt_type = prompt.prompt_type.value
            prompt_types[prompt_type] = prompt_types.get(prompt_type, 0) + 1
        
        # Template usage
        template_usage = {}
        for template in self.templates.values():
            template_usage[template.name] = template.usage_count
        
        # Recent activity
        recent_prompts = len([h for h in self.prompt_history 
                            if (datetime.now() - h['timestamp']).days < 1])
        
        return {
            "total_prompts": total_prompts,
            "total_templates": total_templates,
            "prompt_types": prompt_types,
            "template_usage": template_usage,
            "recent_activity": recent_prompts,
            "average_prompt_length": sum(h['prompt_length'] for h in self.prompt_history) / max(len(self.prompt_history), 1)
        }
    
    def export_prompts(self, format: str = "json") -> Union[str, Dict[str, Any]]:
        """Export prompts in specified format"""
        if format == "json":
            return {
                "prompts": [prompt.dict() for prompt in self.prompts.values()],
                "templates": [template.dict() for template in self.templates.values()],
                "export_timestamp": datetime.now().isoformat()
            }
        elif format == "text":
            output = []
            for prompt in self.prompts.values():
                output.append(f"=== {prompt.name} ===")
                output.append(f"Type: {prompt.prompt_type.value}")
                output.append(f"Description: {prompt.description}")
                output.append("Components:")
                for component in prompt.components:
                    output.append(f"  - {component.role.value}: {component.content[:100]}...")
                output.append("")
            return "\n".join(output)
        else:
            raise ValueError(f"Unsupported format: {format}")


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Structured Prompt Framework")
    print("=" * 40)
    
    # Create framework
    framework = PromptFramework()
    
    # Test template creation
    print(f"✅ Created {len(framework.templates)} default templates")
    
    # Test prompt creation from template
    task_variables = {
        "context": "Software development project",
        "task_description": "Implement user authentication system",
        "constraints": "Must use OAuth 2.0, support MFA, and be secure",
        "output_format": "Step-by-step implementation plan",
        "examples": "Example: 1. Set up OAuth provider 2. Configure security settings..."
    }
    
    prompt_id = framework.create_prompt_from_template("task_execution", task_variables)
    print(f"✅ Created prompt from template: {prompt_id}")
    
    # Test prompt generation
    prompt_text = framework.generate_prompt_text(prompt_id)
    print(f"✅ Generated prompt text ({len(prompt_text)} characters)")
    
    # Test custom prompt creation
    components = [
        PromptComponent(
            role=PromptRole.SYSTEM,
            content="You are a helpful AI assistant specialized in {domain}.",
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
    
    custom_prompt_id = framework.create_structured_prompt(
        name="Custom Helper",
        prompt_type=PromptType.CONVERSATIONAL,
        description="A custom conversational prompt",
        components=components,
        variables={"domain": "technology", "task": "debugging"}
    )
    print(f"✅ Created custom prompt: {custom_prompt_id}")
    
    # Test prompt generation with variables
    custom_prompt_text = framework.generate_prompt_text(custom_prompt_id, {"domain": "AI", "task": "learning"})
    print(f"✅ Generated custom prompt text")
    
    # Test statistics
    stats = framework.get_prompt_statistics()
    print(f"✅ Framework stats: {stats['total_prompts']} prompts, {stats['total_templates']} templates")
    
    # Test search
    search_results = framework.search_prompts("task")
    print(f"✅ Search found {len(search_results)} prompts")
    
    print("🎯 Structured Prompt Framework test completed!")





