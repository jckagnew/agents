"""
ShadCN/UI Agent Collection for MCP Integration
Specialized agents for working with shadcn/ui components using MCP (Model Context Protocol)
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class AgentType(Enum):
    """Types of ShadCN UI agents"""
    REQUIREMENTS_ANALYSIS = "requirements_analysis"
    COMPONENT_RESEARCH = "component_research"
    IMPLEMENTATION = "implementation"
    EXPRESS = "express"

@dataclass
class ComponentInfo:
    """Information about a shadcn component"""
    name: str
    description: str
    dependencies: List[str]
    props: Dict[str, Any]
    examples: List[str]
    installation_command: str

@dataclass
class ProjectRequirements:
    """Project requirements for UI build"""
    feature_name: str
    components_needed: List[str]
    component_hierarchy: Dict[str, Any]
    registries: List[str]

class ShadCNUIAgent:
    """
    Base class for ShadCN UI agents
    """
    
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.mcp_client = None  # Would be initialized with actual MCP client
    
    def get_project_registries(self) -> List[str]:
        """Get available project registries"""
        # This would call the actual MCP function
        # mcp__shadcn__get_project_registries()
        return ["default", "custom"]
    
    def search_components(self, query: str, registries: List[str]) -> List[str]:
        """Search for components in registries"""
        # This would call the actual MCP function
        # mcp__shadcn__search_items_in_registries(query, registries)
        return [f"component_{query}"]
    
    def view_component(self, component_name: str, registries: List[str]) -> ComponentInfo:
        """Get component implementation details"""
        # This would call the actual MCP function
        # mcp__shadcn__view_items_in_registries(component_name, registries)
        return ComponentInfo(
            name=component_name,
            description=f"Implementation for {component_name}",
            dependencies=[],
            props={},
            examples=[],
            installation_command=f"npx shadcn@latest add {component_name}"
        )
    
    def get_component_examples(self, component_name: str, registries: List[str]) -> List[str]:
        """Get component examples"""
        # This would call the actual MCP function
        # mcp__shadcn__get_item_examples_from_registries(component_name, registries)
        return [f"example_{component_name}"]
    
    def get_installation_command(self, components: List[str]) -> str:
        """Get installation command for components"""
        # This would call the actual MCP function
        # mcp__shadcn__get_add_command_for_items(components)
        return f"npx shadcn@latest add {' '.join(components)}"

class RequirementsAnalysisAgent(ShadCNUIAgent):
    """
    Agent 1: Requirements Analysis Agent
    Analyzes requirements for complex UI builds using shadcn MCP
    """
    
    def __init__(self):
        super().__init__(AgentType.REQUIREMENTS_ANALYSIS)
    
    def analyze_requirements(self, user_request: str) -> ProjectRequirements:
        """
        Analyze user request and break down into components
        
        Args:
            user_request: User's request for a complete feature/section
            
        Returns:
            ProjectRequirements object with component breakdown
        """
        # Get available registries
        registries = self.get_project_registries()
        
        # Break down request into components
        components = self._identify_components(user_request)
        
        # Verify components exist in registries
        verified_components = []
        for component in components:
            search_results = self.search_components(component, registries)
            if search_results:
                verified_components.append(component)
        
        # Create component hierarchy
        hierarchy = self._create_hierarchy(user_request, verified_components)
        
        return ProjectRequirements(
            feature_name=self._extract_feature_name(user_request),
            components_needed=verified_components,
            component_hierarchy=hierarchy,
            registries=registries
        )
    
    def _identify_components(self, request: str) -> List[str]:
        """Identify components needed from user request"""
        # This is a simplified example - in practice, you'd use NLP/AI
        component_mapping = {
            "form": ["form", "input", "button", "label", "card"],
            "login": ["form", "input", "button", "card", "alert"],
            "dashboard": ["card", "table", "chart", "button"],
            "modal": ["dialog", "button", "form"],
            "navigation": ["nav", "button", "dropdown"],
        }
        
        request_lower = request.lower()
        components = []
        
        for keyword, comps in component_mapping.items():
            if keyword in request_lower:
                components.extend(comps)
        
        return list(set(components))  # Remove duplicates
    
    def _extract_feature_name(self, request: str) -> str:
        """Extract feature name from request"""
        # Simple extraction - in practice, use more sophisticated NLP
        words = request.split()
        if len(words) >= 2:
            return " ".join(words[:2]).title()
        return "Feature"
    
    def _create_hierarchy(self, request: str, components: List[str]) -> Dict[str, Any]:
        """Create component hierarchy"""
        # This is a simplified example
        if "form" in components:
            return {
                "Card": {
                    "Form": {
                        "Label + Input": "email",
                        "Label + Input": "password", 
                        "Button": "submit",
                        "Alert": "errors"
                    }
                }
            }
        return {"Container": components}
    
    def generate_requirements_doc(self, requirements: ProjectRequirements, task_name: str) -> str:
        """Generate requirements markdown document"""
        doc = f"""## Feature: {requirements.feature_name}

## Components Required:
{chr(10).join([f"- {comp} ({self._get_component_description(comp)})" for comp in requirements.components_needed])}

## Component Hierarchy:
{self._format_hierarchy(requirements.component_hierarchy)}

## Registries Available:
{chr(10).join([f"- {reg}" for reg in requirements.registries])}
"""
        return doc
    
    def _get_component_description(self, component: str) -> str:
        """Get description for component"""
        descriptions = {
            "form": "validation and submission",
            "input": "text input fields",
            "button": "action buttons",
            "card": "container component",
            "alert": "error/success messages",
            "label": "field labels",
            "table": "data display",
            "dialog": "modal dialogs"
        }
        return descriptions.get(component, "UI component")
    
    def _format_hierarchy(self, hierarchy: Dict[str, Any], indent: int = 0) -> str:
        """Format hierarchy as markdown"""
        result = []
        for key, value in hierarchy.items():
            result.append("  " * indent + f"- {key}")
            if isinstance(value, dict):
                result.append(self._format_hierarchy(value, indent + 1))
            elif isinstance(value, str):
                result.append("  " * (indent + 1) + f"- {value}")
        return "\n".join(result)

class ComponentResearchAgent(ShadCNUIAgent):
    """
    Agent 2: Component Research Agent
    Researches shadcn components for implementation
    """
    
    def __init__(self):
        super().__init__(AgentType.COMPONENT_RESEARCH)
    
    def research_components(self, requirements_file: str) -> Dict[str, ComponentInfo]:
        """
        Research components based on requirements
        
        Args:
            requirements_file: Path to requirements markdown file
            
        Returns:
            Dictionary of component information
        """
        # Read requirements file (simplified)
        components = self._parse_requirements_file(requirements_file)
        registries = self.get_project_registries()
        
        component_info = {}
        
        for component in components:
            # Get implementation details
            info = self.view_component(component, registries)
            
            # Get examples
            examples = self.get_component_examples(f"{component}-demo", registries)
            info.examples = examples
            
            component_info[component] = info
        
        return component_info
    
    def _parse_requirements_file(self, file_path: str) -> List[str]:
        """Parse requirements file to extract components"""
        # This is a simplified parser - in practice, use proper markdown parsing
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract components from markdown
        components = []
        lines = content.split('\n')
        in_components_section = False
        
        for line in lines:
            if "## Components Required:" in line:
                in_components_section = True
                continue
            elif line.startswith("## ") and in_components_section:
                break
            elif in_components_section and line.startswith("- "):
                component = line.split("- ")[1].split(" ")[0]
                components.append(component)
        
        return components
    
    def generate_research_doc(self, component_info: Dict[str, ComponentInfo]) -> str:
        """Generate component research markdown document"""
        components = list(component_info.keys())
        install_command = self.get_installation_command(components)
        
        doc = f"""## Installation Commands:
```bash
{install_command}
```

"""
        
        for name, info in component_info.items():
            doc += f"""Component: {name.title()}
Implementation:
```tsx
{self._generate_component_code(info)}
```

Best Example:
```tsx
{self._generate_example_code(info)}
```

Key Props: {', '.join(info.props.keys()) if info.props else 'Standard component props'}

"""
        
        return doc
    
    def _generate_component_code(self, info: ComponentInfo) -> str:
        """Generate component implementation code"""
        return f"""// {info.name} component implementation
import {{ {info.name.title()} }} from "@/components/ui/{info.name}"

export function {info.name.title()}Component() {{
  return (
    <{info.name.title()}>
      {/* Implementation details */}
    </{info.name.title()}>
  )
}}"""
    
    def _generate_example_code(self, info: ComponentInfo) -> str:
        """Generate example code"""
        return f"""// Example usage of {info.name}
<{info.name.title()}>
  {/* Example content */}
</{info.name.title()}>"""

class ImplementationAgent(ShadCNUIAgent):
    """
    Agent 3: Implementation Agent
    Builds the final implementation using researched components
    """
    
    def __init__(self):
        super().__init__(AgentType.IMPLEMENTATION)
    
    def build_implementation(self, requirements_file: str, research_file: str) -> str:
        """
        Build complete implementation
        
        Args:
            requirements_file: Path to requirements file
            research_file: Path to component research file
            
        Returns:
            Complete TypeScript/React implementation
        """
        # Parse requirements and research
        requirements = self._parse_requirements(requirements_file)
        research = self._parse_research(research_file)
        
        # Generate implementation
        implementation = self._generate_implementation(requirements, research)
        
        return implementation
    
    def _parse_requirements(self, file_path: str) -> Dict[str, Any]:
        """Parse requirements file"""
        # Simplified parsing - in practice, use proper markdown parsing
        return {"feature_name": "LoginForm", "components": ["form", "input", "button"]}
    
    def _parse_research(self, file_path: str) -> Dict[str, Any]:
        """Parse research file"""
        # Simplified parsing - in practice, use proper markdown parsing
        return {"components": {"form": {}, "input": {}, "button": {}}}
    
    def _generate_implementation(self, requirements: Dict[str, Any], research: Dict[str, Any]) -> str:
        """Generate complete implementation"""
        return f"""// Complete implementation for {requirements.get('feature_name', 'Feature')}
import {{ Form, FormControl, FormField, FormItem, FormLabel, FormMessage }} from "@/components/ui/form"
import {{ Input }} from "@/components/ui/input"
import {{ Button }} from "@/components/ui/button"
import {{ Card, CardHeader, CardTitle, CardContent }} from "@/components/ui/card"
import {{ Alert, AlertDescription }} from "@/components/ui/alert"

export function {requirements.get('feature_name', 'Feature')}() {{
  // State management
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  // Form handling
  const form = useForm()

  const onSubmit = async (data) => {{
    setIsLoading(true)
    try {{
      // Implementation logic
      console.log("Form submitted:", data)
    }} catch (err) {{
      setError("An error occurred")
    }} finally {{
      setIsLoading(false)
    }}
  }}

  return (
    <Card>
      <CardHeader>
        <CardTitle>{requirements.get('feature_name', 'Feature')}</CardTitle>
      </CardHeader>
      <CardContent>
        <Form {{...form}}>
          <form onSubmit={{form.handleSubmit(onSubmit)}}>
            <FormField
              control={{form.control}}
              name="email"
              render={{({ field }}) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input type="email" {{...field}} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}}
            />
            <Button type="submit" disabled={{isLoading}}>
              {{isLoading ? "Loading..." : "Submit"}}
            </Button>
            {{error && (
              <Alert>
                <AlertDescription>{{error}}</AlertDescription>
              </Alert>
            )}}
          </form>
        </Form>
      </CardContent>
    </Card>
  )
}}"""

class ExpressAgent(ShadCNUIAgent):
    """
    Express Agent: Quick Implementation
    Implements quick component additions using shadcn MCP server
    """
    
    def __init__(self):
        super().__init__(AgentType.EXPRESS)
    
    def quick_implement(self, user_request: str) -> Dict[str, str]:
        """
        Quick implementation for single component
        
        Args:
            user_request: User's request for a single component
            
        Returns:
            Dictionary with installation command and implementation
        """
        # Verify project setup
        registries = self.get_project_registries()
        if not registries:
            return {"error": "No components.json found. Run: npx shadcn@latest init"}
        
        # Identify component
        component = self._identify_single_component(user_request)
        
        # Search and view component
        search_results = self.search_components(component, registries)
        if not search_results:
            return {"error": f"Component '{component}' not found in registries"}
        
        # Get component details
        component_info = self.view_component(component, registries)
        examples = self.get_component_examples(f"{component}-demo", registries)
        
        # Generate implementation
        install_command = self.get_installation_command([component])
        implementation = self._generate_quick_implementation(component, component_info, examples)
        
        return {
            "install_command": install_command,
            "implementation": implementation,
            "setup_instructions": self._generate_setup_instructions(component)
        }
    
    def _identify_single_component(self, request: str) -> str:
        """Identify single component from request"""
        # Simple mapping - in practice, use more sophisticated NLP
        mappings = {
            "date picker": "calendar",
            "datepicker": "calendar",
            "calendar": "calendar",
            "button": "button",
            "input": "input",
            "form": "form",
            "modal": "dialog",
            "popup": "dialog",
            "table": "table",
            "card": "card"
        }
        
        request_lower = request.lower()
        for keyword, component in mappings.items():
            if keyword in request_lower:
                return component
        
        # Default to first word
        return request.split()[0].lower()
    
    def _generate_quick_implementation(self, component: str, info: ComponentInfo, examples: List[str]) -> str:
        """Generate quick implementation"""
        return f"""// Quick implementation for {component}
import {{ {component.title()} }} from "@/components/ui/{component}"

export function {component.title()}Component() {{
  return (
    <{component.title()}>
      {/* Add your content here */}
    </{component.title()}>
  )
}}

// Example usage:
// <{component.title()}Component />"""
    
    def _generate_setup_instructions(self, component: str) -> str:
        """Generate setup instructions"""
        return f"""Setup Instructions for {component}:

1. Run the installation command
2. Import the component in your file
3. Add to your JSX where needed
4. Customize props as required

Additional setup may be required for:
- Form components: Add form provider
- Dialog components: Add portal setup
- Table components: Add data configuration"""

# Example usage and testing
if __name__ == "__main__":
    print("=== ShadCN UI Agents Demo ===\n")
    
    # Test Requirements Analysis Agent
    print("1. Testing Requirements Analysis Agent:")
    req_agent = RequirementsAnalysisAgent()
    requirements = req_agent.analyze_requirements("I need a login form with email and password fields")
    print(f"Feature: {requirements.feature_name}")
    print(f"Components: {requirements.components_needed}")
    print()
    
    # Test Express Agent
    print("2. Testing Express Agent:")
    express_agent = ExpressAgent()
    result = express_agent.quick_implement("add a date picker")
    print(f"Install command: {result.get('install_command', 'Error')}")
    print(f"Implementation ready: {'Yes' if 'implementation' in result else 'No'}")
    print()
    
    print("✅ ShadCN UI Agents ready for use!")
