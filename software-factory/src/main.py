"""
Software Factory Main Application

This is the main entry point for the Software Factory system.
It provides a FastAPI application with endpoints for managing the software factory.
"""

import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime

from agents.orchestrator import SoftwareFactoryOrchestrator, ProjectStatus
from agents.idea_validation import IdeaValidationAgent
from agents.rapid_prototyping import RapidPrototypingAgent
from agents.collaboration import CollaborationAgent
from agents.monetization import MonetizationAgent
from agents.analytics import AnalyticsAgent
from agents.ui_analysis import UIAnalysisAgent
from agents.universal_app_generator import UniversalAppGenerator


# Pydantic models for API
class IdeaSubmission(BaseModel):
    idea_description: str
    owner_id: str
    team_members: Optional[List[str]] = []


class ProjectUpdate(BaseModel):
    project_id: str
    updates: Dict[str, Any]


class FeedbackSubmission(BaseModel):
    project_id: str
    user_id: str
    category: str
    description: str
    priority: Optional[str] = "medium"


class MetricsRequest(BaseModel):
    project_id: str
    metric_types: Optional[List[str]] = ["revenue", "users", "technical"]


# Initialize FastAPI app
app = FastAPI(
    title="Software Factory API",
    description="AI-powered software factory for rapid idea-to-revenue development",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the orchestrator and agents
orchestrator = SoftwareFactoryOrchestrator()
idea_validator = IdeaValidationAgent()
prototyper = RapidPrototypingAgent()
collaborator = CollaborationAgent()
monetizer = MonetizationAgent()
analytics = AnalyticsAgent()
ui_analyzer = UIAnalysisAgent()
universal_app_generator = UniversalAppGenerator()


@app.get("/")
async def root():
    """Root endpoint with basic information"""
    return {
        "message": "Software Factory API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "orchestrator": "running",
            "idea_validation": "running",
            "rapid_prototyping": "running",
            "collaboration": "running",
            "monetization": "running",
            "analytics": "running"
        }
    }


@app.post("/ideas/submit")
async def submit_idea(idea: IdeaSubmission, background_tasks: BackgroundTasks):
    """
    Submit a new idea to the software factory.
    
    This endpoint processes ideas through the complete workflow:
    1. Idea validation
    2. Rapid prototyping
    3. Collaboration setup
    4. Monetization planning
    """
    try:
        # Process the idea through the complete workflow
        project = await orchestrator.process_new_idea(
            idea_description=idea.idea_description,
            owner_id=idea.owner_id,
            team_members=idea.team_members
        )
        
        # Add background task to send notifications
        background_tasks.add_task(send_project_notifications, project)
        
        return {
            "success": True,
            "project_id": project.id,
            "project_name": project.name,
            "status": project.status.value,
            "message": f"Project {project.id} created successfully",
            "next_steps": get_next_steps(project.status)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing idea: {str(e)}")


@app.get("/projects/{project_id}")
async def get_project(project_id: str):
    """Get project details by ID"""
    project = await orchestrator.get_project_status(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "project_id": project.id,
        "name": project.name,
        "description": project.description,
        "status": project.status.value,
        "created_at": project.created_at.isoformat(),
        "updated_at": project.updated_at.isoformat(),
        "owner_id": project.owner_id,
        "team_members": project.team_members,
        "validation_result": project.validation_result,
        "prototype": project.prototype,
        "collaboration_space": project.collaboration_space,
        "monetization_plan": project.monetization_plan,
        "metrics": project.metrics
    }


@app.get("/projects")
async def list_projects():
    """List all projects in the software factory"""
    dashboard = await orchestrator.get_factory_dashboard()
    
    return {
        "total_projects": dashboard["total_projects"],
        "active_projects": dashboard["active_projects"],
        "completed_projects": dashboard["completed_projects"],
        "average_completion_time_days": dashboard["average_completion_time_days"],
        "revenue_metrics": dashboard["revenue_metrics"],
        "projects_by_status": dashboard["projects_by_status"],
        "recent_activity": dashboard["recent_activity"]
    }


@app.post("/projects/{project_id}/feedback")
async def submit_feedback(project_id: str, feedback: FeedbackSubmission):
    """Submit feedback for a project"""
    try:
        feedback_data = {
            "user_id": feedback.user_id,
            "category": feedback.category,
            "description": feedback.description,
            "priority": feedback.priority
        }
        
        result = await collaborator.collect_and_process_feedback(project_id, feedback_data)
        
        return {
            "success": True,
            "feedback_id": result["feedback_id"],
            "status": result["status"],
            "priority": result["priority"],
            "assigned_to": result["assigned_to"],
            "message": "Feedback submitted successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")


@app.get("/projects/{project_id}/dashboard")
async def get_project_dashboard(project_id: str):
    """Get comprehensive project dashboard"""
    try:
        # Get collaboration dashboard
        collaboration_dashboard = await collaborator.get_collaboration_dashboard(project_id)
        
        # Get analytics metrics
        metrics = await analytics.update_project_metrics(
            type('Project', (), {'id': project_id})()
        )
        
        return {
            "project_id": project_id,
            "collaboration": collaboration_dashboard,
            "analytics": metrics,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting dashboard: {str(e)}")


@app.get("/projects/{project_id}/metrics")
async def get_project_metrics(project_id: str, request: MetricsRequest):
    """Get specific metrics for a project"""
    try:
        metrics = await analytics.update_project_metrics(
            type('Project', (), {'id': project_id})()
        )
        
        # Filter metrics based on request
        filtered_metrics = {}
        for metric_type in request.metric_types:
            if metric_type in metrics:
                filtered_metrics[metric_type] = metrics[metric_type]
        
        return {
            "project_id": project_id,
            "metrics": filtered_metrics,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting metrics: {str(e)}")


@app.post("/projects/{project_id}/monetization/optimize")
async def optimize_monetization(project_id: str):
    """Optimize monetization strategy for a project"""
    try:
        # Get current metrics
        current_metrics = await analytics.update_project_metrics(
            type('Project', (), {'id': project_id})()
        )
        
        # Optimize monetization
        optimization = await monetizer.optimize_monetization(project_id, current_metrics)
        
        return {
            "success": True,
            "project_id": project_id,
            "optimization": optimization,
            "message": "Monetization optimization completed"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing monetization: {str(e)}")


@app.get("/factory/dashboard")
async def get_factory_dashboard():
    """Get comprehensive factory dashboard"""
    try:
        dashboard = await orchestrator.get_factory_dashboard()
        return dashboard
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting factory dashboard: {str(e)}")


@app.get("/factory/analytics")
async def get_factory_analytics():
    """Get factory-wide analytics"""
    try:
        revenue_metrics = await analytics.get_factory_revenue_metrics()
        return revenue_metrics
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting factory analytics: {str(e)}")


@app.post("/projects/{project_id}/ui/analyze")
async def analyze_project_ui(project_id: str, project_path: str):
    """Analyze UI/UX for a specific project"""
    try:
        result = await orchestrator.analyze_project_ui(project_id, project_path)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing project UI: {str(e)}")


@app.post("/ui/analyze-file")
async def analyze_file_ui(file_path: str):
    """Analyze UI/UX for a single file"""
    try:
        result = await orchestrator.analyze_single_file_ui(file_path)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing file UI: {str(e)}")


@app.get("/ui/checklist")
async def get_ui_checklist():
    """Get UI/UX analysis checklist and guidelines"""
    try:
        checklist = {
            "accessibility": {
                "alt_text": "All images must have descriptive alt text",
                "form_labels": "All form inputs must have associated labels",
                "keyboard_navigation": "All interactive elements must be keyboard accessible",
                "focus_indicators": "Visible focus indicators for keyboard navigation",
                "color_contrast": "Text must meet WCAG AA contrast ratios (4.5:1)",
                "color_only_info": "Information must not rely solely on color"
            },
            "responsiveness": {
                "viewport_meta": "Viewport meta tag for mobile responsiveness",
                "media_queries": "Responsive breakpoints for different screen sizes",
                "flexible_layouts": "Use relative units instead of fixed widths",
                "touch_targets": "Touch targets must be at least 44px for mobile"
            },
            "typography": {
                "font_sizes": "Body text must be at least 14px for readability",
                "line_length": "Text lines should not exceed 75 characters",
                "font_consistency": "Limit to 2-3 font families maximum",
                "hierarchy": "Clear heading structure (h1, h2, h3, etc.)"
            },
            "layout": {
                "visual_hierarchy": "Clear content priority through size, color, and positioning",
                "white_space": "Adequate white space for breathing room",
                "clutter": "Avoid overwhelming users with too many elements",
                "grouping": "Group related elements together"
            },
            "navigation": {
                "clear_structure": "Simple, intuitive navigation structure",
                "breadcrumbs": "Breadcrumb navigation for deep pages",
                "consistency": "Consistent navigation across all pages",
                "mobile_friendly": "Mobile-optimized navigation patterns"
            },
            "interaction": {
                "feedback": "Immediate feedback for user actions",
                "loading_states": "Loading indicators for async operations",
                "error_handling": "Clear error messages and recovery options",
                "cta_clarity": "Clear, compelling call-to-action buttons"
            }
        }
        
        return {
            "checklist": checklist,
            "wcag_levels": {
                "A": "Basic accessibility requirements",
                "AA": "Standard accessibility requirements (recommended)",
                "AAA": "Enhanced accessibility requirements"
            },
            "tools": {
                "color_contrast": "WebAIM Contrast Checker",
                "accessibility": "axe DevTools, WAVE",
                "mobile_testing": "Chrome DevTools Device Mode",
                "performance": "Lighthouse, PageSpeed Insights"
            }
        }
    
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting UI checklist: {str(e)}")

# Universal App Generation Endpoints

@app.post("/projects/{project_id}/universal-app")
async def generate_universal_app(project_id: str, app_config: dict):
    """Generate a universal app (iOS, Android, Web) for a project"""
    try:
        result = await orchestrator.generate_universal_app(project_id, app_config)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating universal app: {str(e)}")

@app.get("/universal-app/templates")
async def get_universal_app_templates():
    """Get available universal app templates and configurations"""
    try:
        result = await orchestrator.get_universal_app_templates()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting templates: {str(e)}")

@app.post("/universal-app/generate")
async def generate_standalone_universal_app(app_config: dict):
    """Generate a standalone universal app without a project"""
    try:
        result = await universal_app_generator.generate_app(app_config)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating standalone app: {str(e)}")


@app.post("/factory/validate-idea")
async def validate_idea_only(idea: IdeaSubmission):
    """Validate an idea without creating a full project"""
    try:
        validation_result = await idea_validator.analyze_comprehensive(idea.idea_description)
        
        return {
            "success": True,
            "validation_result": validation_result,
            "message": "Idea validation completed"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating idea: {str(e)}")


@app.post("/factory/create-prototype")
async def create_prototype_only(idea: IdeaSubmission):
    """Create a prototype without full project setup"""
    try:
        # First validate the idea
        validation_result = await idea_validator.analyze_comprehensive(idea.idea_description)
        
        if not validation_result.get('is_viable', False):
            return {
                "success": False,
                "message": "Idea is not viable for prototyping",
                "validation_result": validation_result
            }
        
        # Create prototype
        prototype = await prototyper.create_prototype(idea.idea_description, validation_result)
        
        return {
            "success": True,
            "prototype": prototype,
            "message": "Prototype created successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating prototype: {str(e)}")


# Background tasks
async def send_project_notifications(project):
    """Send notifications about project creation"""
    # In production, this would send actual notifications
    print(f"Sending notifications for project {project.id}")


def get_next_steps(status: ProjectStatus) -> List[str]:
    """Get next steps based on project status"""
    next_steps_map = {
        ProjectStatus.IDEA_SUBMITTED: [
            "Wait for idea validation to complete",
            "Review validation results",
            "Provide additional information if needed"
        ],
        ProjectStatus.VALIDATING: [
            "Wait for validation to complete",
            "Prepare for next phase"
        ],
        ProjectStatus.PROTOTYPING: [
            "Review prototype specifications",
            "Provide feedback on design",
            "Prepare for collaboration phase"
        ],
        ProjectStatus.COLLABORATING: [
            "Join collaboration workspace",
            "Review project plan",
            "Provide input and feedback"
        ],
        ProjectStatus.MONETIZING: [
            "Review monetization plan",
            "Provide pricing feedback",
            "Prepare for launch"
        ],
        ProjectStatus.LAUNCHING: [
            "Review launch plan",
            "Prepare marketing materials",
            "Set up monitoring"
        ],
        ProjectStatus.LIVE: [
            "Monitor performance",
            "Gather user feedback",
            "Plan next iteration"
        ],
        ProjectStatus.COMPLETED: [
            "Review project outcomes",
            "Document lessons learned",
            "Plan next project"
        ],
        ProjectStatus.CANCELLED: [
            "Review cancellation reasons",
            "Consider alternative approaches",
            "Learn from the experience"
        ]
    }
    
    return next_steps_map.get(status, ["Contact support for guidance"])


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize the software factory on startup"""
    print("Software Factory starting up...")
    print("All agents initialized and ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Software Factory shutting down...")


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

