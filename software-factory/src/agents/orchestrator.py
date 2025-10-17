"""
Software Factory Orchestrator Agent

This is the master agent that coordinates all other agents in the software factory.
It manages the complete workflow from idea to revenue.
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from .idea_validation import IdeaValidationAgent
from .rapid_prototyping import RapidPrototypingAgent
from .collaboration import CollaborationAgent
from .monetization import MonetizationAgent
from .analytics import AnalyticsAgent
from .ui_analysis import UIAnalysisAgent
from .universal_app_generator import UniversalAppGenerator, AppConfig, Platform
from .mobile_tester import MobileTester


class ProjectStatus(Enum):
    """Project status enumeration"""
    IDEA_SUBMITTED = "idea_submitted"
    VALIDATING = "validating"
    PROTOTYPING = "prototyping"
    COLLABORATING = "collaborating"
    MONETIZING = "monetizing"
    UNIVERSAL_APP_GENERATED = "universal_app_generated"
    LAUNCHING = "launching"
    LIVE = "live"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Project:
    """Project data structure"""
    id: str
    name: str
    description: str
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    owner_id: str
    team_members: List[str]
    validation_result: Optional[Dict[str, Any]] = None
    prototype: Optional[Dict[str, Any]] = None
    collaboration_space: Optional[Dict[str, Any]] = None
    monetization_plan: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    universal_app_path: Optional[str] = None


class SoftwareFactoryOrchestrator:
    """
    Master orchestrator for the software factory.
    
    This agent coordinates all other agents to transform ideas into
    monetizable software products through a systematic, AI-powered process.
    """
    
    def __init__(self):
        """Initialize the orchestrator with all specialized agents"""
        self.idea_validator = IdeaValidationAgent()
        self.prototyper = RapidPrototypingAgent()
        self.collaborator = CollaborationAgent()
        self.monetizer = MonetizationAgent()
        self.analytics = AnalyticsAgent()
        self.ui_analyzer = UIAnalysisAgent()
        self.universal_app_generator = UniversalAppGenerator()
        
        # Project storage (in production, this would be a database)
        self.projects: Dict[str, Project] = {}
        
    async def process_new_idea(
        self, 
        idea_description: str, 
        owner_id: str,
        team_members: List[str] = None
    ) -> Project:
        """
        Process a new idea through the complete software factory workflow.
        
        Args:
            idea_description: Detailed description of the software idea
            owner_id: ID of the project owner
            team_members: List of team member IDs
            
        Returns:
            Project object with complete workflow results
        """
        if team_members is None:
            team_members = []
            
        # Create new project
        project_id = f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        project = Project(
            id=project_id,
            name=self._extract_project_name(idea_description),
            description=idea_description,
            status=ProjectStatus.IDEA_SUBMITTED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            owner_id=owner_id,
            team_members=team_members
        )
        
        self.projects[project_id] = project
        
        try:
            # Phase 1: Idea Validation
            await self._update_project_status(project, ProjectStatus.VALIDATING)
            validation_result = await self.idea_validator.analyze_comprehensive(idea_description)
            project.validation_result = validation_result
            
            # Check if idea is viable
            if not validation_result.get('is_viable', False):
                await self._update_project_status(project, ProjectStatus.CANCELLED)
                return project
            
            # Phase 2: Rapid Prototyping
            await self._update_project_status(project, ProjectStatus.PROTOTYPING)
            prototype = await self.prototyper.create_prototype(
                idea_description, 
                validation_result
            )
            project.prototype = prototype
            
            # Phase 3: Collaboration Setup
            await self._update_project_status(project, ProjectStatus.COLLABORATING)
            collaboration_space = await self.collaborator.setup_collaboration_space(
                project, 
                team_members
            )
            project.collaboration_space = collaboration_space
            
            # Phase 4: Monetization Planning
            await self._update_project_status(project, ProjectStatus.MONETIZING)
            monetization_plan = await self.monetizer.create_monetization_plan(
                project, 
                validation_result
            )
            project.monetization_plan = monetization_plan
            
            # Phase 5: Launch Preparation
            await self._update_project_status(project, ProjectStatus.LAUNCHING)
            launch_plan = await self._create_launch_plan(project)
            
            # Phase 6: Go Live
            await self._update_project_status(project, ProjectStatus.LIVE)
            
            # Initialize analytics
            project.metrics = await self.analytics.initialize_project_metrics(project)
            
            return project
            
        except Exception as e:
            # Handle errors gracefully
            await self._handle_project_error(project, str(e))
            return project
    
    async def get_project_status(self, project_id: str) -> Optional[Project]:
        """Get current status of a project"""
        return self.projects.get(project_id)
    
    async def update_project_metrics(self, project_id: str) -> Dict[str, Any]:
        """Update and return current project metrics"""
        project = self.projects.get(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        metrics = await self.analytics.update_project_metrics(project)
        project.metrics = metrics
        return metrics
    
    async def get_factory_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive factory dashboard data"""
        total_projects = len(self.projects)
        active_projects = len([p for p in self.projects.values() 
                             if p.status in [ProjectStatus.VALIDATING, 
                                           ProjectStatus.PROTOTYPING,
                                           ProjectStatus.COLLABORATING,
                                           ProjectStatus.MONETIZING,
                                           ProjectStatus.LAUNCHING,
                                           ProjectStatus.LIVE]])
        
        completed_projects = len([p for p in self.projects.values() 
                                if p.status == ProjectStatus.COMPLETED])
        
        # Calculate average time to completion
        completed_times = []
        for project in self.projects.values():
            if project.status == ProjectStatus.COMPLETED:
                duration = (project.updated_at - project.created_at).days
                completed_times.append(duration)
        
        avg_completion_time = sum(completed_times) / len(completed_times) if completed_times else 0
        
        # Get revenue metrics
        revenue_metrics = await self.analytics.get_factory_revenue_metrics()
        
        return {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": completed_projects,
            "average_completion_time_days": avg_completion_time,
            "revenue_metrics": revenue_metrics,
            "projects_by_status": self._get_projects_by_status(),
            "recent_activity": self._get_recent_activity()
        }
    
    async def analyze_project_ui(self, project_id: str, project_path: str) -> Dict[str, Any]:
        """Analyze UI/UX for a specific project"""
        try:
            ui_analysis = await self.ui_analyzer.analyze_project_ui(project_path)
            
            return {
                "success": True,
                "project_id": project_id,
                "ui_analysis": {
                    "overall_score": ui_analysis.overall_score,
                    "accessibility_score": ui_analysis.accessibility_score,
                    "mobile_score": ui_analysis.mobile_score,
                    "performance_score": ui_analysis.performance_score,
                    "total_issues": ui_analysis.total_issues,
                    "issues_by_severity": ui_analysis.issues_by_severity,
                    "issues_by_category": ui_analysis.issues_by_category,
                    "recommendations": ui_analysis.recommendations,
                    "summary": ui_analysis.summary
                },
                "timestamp": ui_analysis.analysis_timestamp.isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "project_id": project_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def analyze_single_file_ui(self, file_path: str) -> Dict[str, Any]:
        """Analyze UI/UX for a single file"""
        try:
            ui_analysis = await self.ui_analyzer.analyze_single_file(file_path)
            
            return {
                "success": True,
                "file_path": file_path,
                "ui_analysis": {
                    "overall_score": ui_analysis.overall_score,
                    "accessibility_score": ui_analysis.accessibility_score,
                    "mobile_score": ui_analysis.mobile_score,
                    "performance_score": ui_analysis.performance_score,
                    "total_issues": ui_analysis.total_issues,
                    "issues_by_severity": ui_analysis.issues_by_severity,
                    "issues_by_category": ui_analysis.issues_by_category,
                    "recommendations": ui_analysis.recommendations,
                    "summary": ui_analysis.summary
                },
                "timestamp": ui_analysis.analysis_timestamp.isoformat()
            }
        except Exception as e:
        return {
            "success": False,
            "file_path": file_path,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

    async def generate_universal_app(self, project_id: str, app_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a universal app (iOS, Android, Web) for a project"""
        try:
            # Convert dict to AppConfig
            config = AppConfig(
                name=app_config.get("name", "Universal App"),
                description=app_config.get("description", "A universal app for all platforms"),
                bundle_id=app_config.get("bundle_id", "com.yourcompany.universalapp"),
                version=app_config.get("version", "1.0.0"),
                platforms=[Platform(p) for p in app_config.get("platforms", ["ios", "android", "web"])],
                features=app_config.get("features", ["Dashboard", "Settings"]),
                ui_theme=app_config.get("ui_theme", "modern"),
                navigation_type=app_config.get("navigation_type", "tabs")
            )
            
            # Generate the universal app
            result = await self.universal_app_generator.generate_app(config)
            
            # Update project status
            if project_id in self.projects:
                self.projects[project_id].status = ProjectStatus.UNIVERSAL_APP_GENERATED
                self.projects[project_id].universal_app_path = result.get("app_path")
            
            return {
                "success": True,
                "project_id": project_id,
                "universal_app": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "project_id": project_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def get_universal_app_templates(self) -> Dict[str, Any]:
        """Get available universal app templates and configurations"""
        try:
            templates = {
                "basic": {
                    "name": "Basic Universal App",
                    "description": "Simple app with dashboard and settings",
                    "features": ["Dashboard", "Settings"],
                    "platforms": ["ios", "android", "web"]
                },
                "ecommerce": {
                    "name": "E-commerce Universal App",
                    "description": "Full-featured e-commerce app for all platforms",
                    "features": ["Dashboard", "Products", "Cart", "Orders", "Profile", "Settings"],
                    "platforms": ["ios", "android", "web"]
                },
                "social": {
                    "name": "Social Media Universal App",
                    "description": "Social media app with real-time features",
                    "features": ["Feed", "Profile", "Chat", "Notifications", "Search", "Settings"],
                    "platforms": ["ios", "android", "web"]
                },
                "fitness": {
                    "name": "Fitness Universal App",
                    "description": "Fitness tracking app with analytics",
                    "features": ["Dashboard", "Workouts", "Progress", "Analytics", "Profile", "Settings"],
                    "platforms": ["ios", "android", "web"]
                },
                "productivity": {
                    "name": "Productivity Universal App",
                    "description": "Task management and productivity app",
                    "features": ["Dashboard", "Tasks", "Calendar", "Notes", "Analytics", "Settings"],
                    "platforms": ["ios", "android", "web"]
                }
            }
            
            return {
                "success": True,
                "templates": templates,
                "platforms": [p.value for p in Platform],
                "ui_themes": ["modern", "classic", "minimal", "dark"],
                "navigation_types": ["tabs", "drawer", "stack", "mixed"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _extract_project_name(self, idea_description: str) -> str:
        """Extract a project name from the idea description"""
        # Simple extraction - in production, use AI for better naming
        words = idea_description.split()[:3]
        return "_".join(words).lower().replace(" ", "_")
    
    async def _update_project_status(self, project: Project, status: ProjectStatus):
        """Update project status and timestamp"""
        project.status = status
        project.updated_at = datetime.now()
        self.projects[project.id] = project
        
        # Log status change
        print(f"Project {project.id} status updated to {status.value}")
    
    async def _create_launch_plan(self, project: Project) -> Dict[str, Any]:
        """Create a comprehensive launch plan"""
        return {
            "launch_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "marketing_strategy": await self.monetizer.create_marketing_strategy(project),
            "technical_deployment": await self.prototyper.create_deployment_plan(project),
            "success_metrics": await self.analytics.define_success_metrics(project),
            "rollback_plan": "Automated rollback to previous version if issues detected"
        }
    
    async def _handle_project_error(self, project: Project, error_message: str):
        """Handle project errors gracefully"""
        project.status = ProjectStatus.CANCELLED
        project.updated_at = datetime.now()
        
        # Log error
        print(f"Project {project.id} failed: {error_message}")
        
        # Notify stakeholders
        await self.collaborator.notify_project_failure(project, error_message)
    
    def _get_projects_by_status(self) -> Dict[str, int]:
        """Get count of projects by status"""
        status_counts = {}
        for project in self.projects.values():
            status = project.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts
    
    def _get_recent_activity(self) -> List[Dict[str, Any]]:
        """Get recent project activity"""
        recent_projects = sorted(
            self.projects.values(), 
            key=lambda p: p.updated_at, 
            reverse=True
        )[:10]
        
        return [
            {
                "project_id": p.id,
                "project_name": p.name,
                "status": p.status.value,
                "updated_at": p.updated_at.isoformat(),
                "owner_id": p.owner_id
            }
            for p in recent_projects
        ]


# Example usage and testing
async def main():
    """Example usage of the Software Factory Orchestrator"""
    orchestrator = SoftwareFactoryOrchestrator()
    
    # Example idea
    idea = """
    I want to create an AI-powered personal finance assistant that helps users 
    track expenses, create budgets, and get personalized financial advice. 
    The app should integrate with bank accounts, provide real-time spending 
    insights, and offer investment recommendations based on user goals.
    """
    
    # Process the idea
    project = await orchestrator.process_new_idea(
        idea_description=idea,
        owner_id="user_123",
        team_members=["dev_456", "designer_789"]
    )
    
    print(f"Project created: {project.id}")
    print(f"Status: {project.status.value}")
    print(f"Validation result: {project.validation_result}")
    
    # Get factory dashboard
    dashboard = await orchestrator.get_factory_dashboard()
    print(f"Factory dashboard: {dashboard}")


if __name__ == "__main__":
    asyncio.run(main())

