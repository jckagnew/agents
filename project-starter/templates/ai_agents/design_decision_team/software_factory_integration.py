"""
Design Decision Team Integration with Software Factory
Extends the existing Software Factory with comprehensive design automation
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from software_factory.src.agents.orchestrator import SoftwareFactoryOrchestrator, ProjectStatus
from software_factory.src.agents.idea_validation import IdeaValidationAgent
from software_factory.src.agents.rapid_prototyping import RapidPrototypingAgent
from software_factory.src.agents.collaboration import CollaborationAgent
from software_factory.src.agents.monetization import MonetizationAgent
from software_factory.src.agents.analytics import AnalyticsAgent

from .design_decision_team import DesignDecisionTeam, DesignRequest, DesignRequestType


class DesignIntegrationStatus(Enum):
    """Design integration status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class DesignIntegration:
    """Design integration data structure"""
    project_id: str
    design_requests: List[DesignRequest]
    status: DesignIntegrationStatus
    design_decisions: List[Any]  # DesignDecision objects
    integration_timeline: str
    design_quality_scores: Dict[str, int]


class EnhancedSoftwareFactoryOrchestrator(SoftwareFactoryOrchestrator):
    """Enhanced Software Factory Orchestrator with Design Decision Team"""
    
    def __init__(self):
        super().__init__()
        self.design_decision_team = DesignDecisionTeam()
        self.design_integrations: Dict[str, DesignIntegration] = {}
    
    async def process_idea_with_design(self, idea_description: str, owner_id: str, design_requirements: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process idea with comprehensive design integration"""
        
        # 1. Standard idea validation
        validation_result = await self.idea_validator.analyze(idea_description)
        
        if not validation_result.get('is_viable', False):
            return {
                "status": "failed",
                "reason": "Idea validation failed",
                "validation_result": validation_result
            }
        
        # 2. Create project
        project = self._create_project(idea_description, owner_id)
        self.projects[project.id] = project
        
        # 3. Generate design requests based on project type
        design_requests = await self._generate_design_requests(project, design_requirements)
        
        # 4. Process design requests through Design Decision Team
        design_decisions = []
        for request in design_requests:
            try:
                decision = await self.design_decision_team.process_design_request(request)
                design_decisions.append(decision)
            except Exception as e:
                print(f"Design request failed for {request.id}: {e}")
                continue
        
        # 5. Create design integration record
        design_integration = DesignIntegration(
            project_id=project.id,
            design_requests=design_requests,
            status=DesignIntegrationStatus.COMPLETED if design_decisions else DesignIntegrationStatus.FAILED,
            design_decisions=design_decisions,
            integration_timeline="2-4 hours",
            design_quality_scores=self._calculate_design_quality_scores(design_decisions)
        )
        
        self.design_integrations[project.id] = design_integration
        
        # 6. Enhanced rapid prototyping with design decisions
        prototype_result = await self.prototyper.create_with_design(validation_result, design_decisions)
        
        # 7. Set up collaboration with design assets
        collaboration_space = await self.collaborator.setup_with_design(prototype_result, design_decisions)
        
        # 8. Plan monetization with design considerations
        monetization_plan = await self.monetizer.plan_with_design(prototype_result, design_decisions)
        
        return {
            "project_id": project.id,
            "status": "success",
            "validation": validation_result,
            "design_integration": design_integration,
            "prototype": prototype_result,
            "collaboration": collaboration_space,
            "monetization": monetization_plan,
            "design_quality_scores": design_integration.design_quality_scores
        }
    
    async def _generate_design_requests(self, project, design_requirements: Dict[str, Any] = None) -> List[DesignRequest]:
        """Generate design requests based on project type and requirements"""
        
        design_requests = []
        
        # Determine project type and generate appropriate design requests
        if "mobile" in project.description.lower() or "app" in project.description.lower():
            # Mobile app design requests
            design_requests.extend([
                DesignRequest(
                    id=f"{project.id}_splash_screen",
                    project_id=project.id,
                    request_type=DesignRequestType.SPLASH_SCREEN,
                    description="Create engaging splash screen with morphing transformation animation",
                    requirements={
                        "quality": "high",
                        "performance": "high",
                        "animation_type": "morphing",
                        "character_style": "cartoon",
                        "transformation": "overweight_to_fit"
                    },
                    budget_tier="ai_generated",
                    timeline="urgent",
                    target_platform="mobile",
                    brand_guidelines=design_requirements.get("brand_guidelines", {}),
                    user_personas=design_requirements.get("user_personas", [])
                ),
                DesignRequest(
                    id=f"{project.id}_ui_components",
                    project_id=project.id,
                    request_type=DesignRequestType.UI_COMPONENT,
                    description="Design modern UI components with consistent styling",
                    requirements={
                        "quality": "high",
                        "consistency": "high",
                        "accessibility": "required"
                    },
                    budget_tier="ai_generated",
                    timeline="standard",
                    target_platform="mobile",
                    brand_guidelines=design_requirements.get("brand_guidelines", {}),
                    user_personas=design_requirements.get("user_personas", [])
                )
            ])
        
        elif "website" in project.description.lower() or "web" in project.description.lower():
            # Web application design requests
            design_requests.extend([
                DesignRequest(
                    id=f"{project.id}_landing_page",
                    project_id=project.id,
                    request_type=DesignRequestType.UI_COMPONENT,
                    description="Design compelling landing page with modern UI/UX",
                    requirements={
                        "quality": "high",
                        "conversion": "high",
                        "responsive": "required"
                    },
                    budget_tier="premium",
                    timeline="standard",
                    target_platform="web",
                    brand_guidelines=design_requirements.get("brand_guidelines", {}),
                    user_personas=design_requirements.get("user_personas", [])
                ),
                DesignRequest(
                    id=f"{project.id}_brand_identity",
                    project_id=project.id,
                    request_type=DesignRequestType.BRAND_IDENTITY,
                    description="Develop comprehensive brand identity and visual guidelines",
                    requirements={
                        "quality": "premium",
                        "consistency": "high",
                        "scalability": "required"
                    },
                    budget_tier="premium",
                    timeline="standard",
                    target_platform="multi",
                    brand_guidelines=design_requirements.get("brand_guidelines", {}),
                    user_personas=design_requirements.get("user_personas", [])
                )
            ])
        
        # Add visual assets request for all projects
        design_requests.append(
            DesignRequest(
                id=f"{project.id}_visual_assets",
                project_id=project.id,
                request_type=DesignRequestType.VISUAL_ASSETS,
                description="Create comprehensive visual asset library",
                requirements={
                    "quality": "high",
                    "variety": "high",
                    "consistency": "required"
                },
                budget_tier="ai_generated",
                timeline="standard",
                target_platform="multi",
                brand_guidelines=design_requirements.get("brand_guidelines", {}),
                user_personas=design_requirements.get("user_personas", [])
            )
        )
        
        return design_requests
    
    def _calculate_design_quality_scores(self, design_decisions: List[Any]) -> Dict[str, int]:
        """Calculate overall design quality scores"""
        
        if not design_decisions:
            return {"overall": 0, "ux": 0, "brand": 0, "technical": 0}
        
        # Calculate average scores across all design decisions
        total_scores = {"overall": 0, "ux": 0, "brand": 0, "technical": 0}
        
        for decision in design_decisions:
            if hasattr(decision, 'quality_scores'):
                for key in total_scores:
                    total_scores[key] += decision.quality_scores.get(key, 0)
        
        # Calculate averages
        count = len(design_decisions)
        for key in total_scores:
            total_scores[key] = total_scores[key] // count if count > 0 else 0
        
        return total_scores
    
    async def get_design_integration_status(self, project_id: str) -> Optional[DesignIntegration]:
        """Get design integration status for a project"""
        return self.design_integrations.get(project_id)
    
    async def update_design_requirements(self, project_id: str, new_requirements: Dict[str, Any]) -> bool:
        """Update design requirements for a project"""
        
        if project_id not in self.design_integrations:
            return False
        
        # Regenerate design requests with new requirements
        project = self.projects.get(project_id)
        if not project:
            return False
        
        design_requests = await self._generate_design_requests(project, new_requirements)
        
        # Update design integration
        self.design_integrations[project_id].design_requests = design_requests
        self.design_integrations[project_id].status = DesignIntegrationStatus.IN_PROGRESS
        
        # Process new design requests
        design_decisions = []
        for request in design_requests:
            try:
                decision = await self.design_decision_team.process_design_request(request)
                design_decisions.append(decision)
            except Exception as e:
                print(f"Design request failed for {request.id}: {e}")
                continue
        
        # Update design integration
        self.design_integrations[project_id].design_decisions = design_decisions
        self.design_integrations[project_id].status = DesignIntegrationStatus.COMPLETED if design_decisions else DesignIntegrationStatus.FAILED
        self.design_integrations[project_id].design_quality_scores = self._calculate_design_quality_scores(design_decisions)
        
        return True


# Example usage with weight tracker project
async def process_weight_tracker_with_design():
    """Example: Process weight tracker project with design integration"""
    
    orchestrator = EnhancedSoftwareFactoryOrchestrator()
    
    # Design requirements for weight tracker
    design_requirements = {
        "brand_guidelines": {
            "colors": ["#667eea", "#4CAF50", "#fff"],
            "style": "modern",
            "tone": "motivational",
            "target_audience": "fitness_enthusiasts"
        },
        "user_personas": [
            {
                "age": "25-45",
                "interests": "fitness",
                "tech_savvy": "high",
                "goals": "weight_tracking"
            }
        ],
        "design_priorities": [
            "morphing_transformation_animations",
            "motivational_visual_elements",
            "clean_modern_ui",
            "mobile_first_design"
        ]
    }
    
    # Process idea with design integration
    result = await orchestrator.process_idea_with_design(
        idea_description="AI-powered weight tracking mobile app with transformation animations",
        owner_id="user_123",
        design_requirements=design_requirements
    )
    
    print(f"Project ID: {result['project_id']}")
    print(f"Design Quality Scores: {result['design_quality_scores']}")
    print(f"Design Integration Status: {result['design_integration'].status}")
    
    return result


if __name__ == "__main__":
    asyncio.run(process_weight_tracker_with_design())
