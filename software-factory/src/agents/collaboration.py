"""
Collaboration Agent

This agent handles partner and customer collaboration, feedback collection,
and project management for the software factory.
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum


class CollaborationSpaceType(Enum):
    """Types of collaboration spaces"""
    PARTNER_WORKSPACE = "partner_workspace"
    CUSTOMER_FEEDBACK = "customer_feedback"
    DEVELOPMENT_TEAM = "development_team"
    STAKEHOLDER_REVIEW = "stakeholder_review"


@dataclass
class CollaborationSpace:
    """Collaboration space data structure"""
    id: str
    name: str
    type: CollaborationSpaceType
    project_id: str
    members: List[str]
    created_at: datetime
    settings: Dict[str, Any]
    active: bool = True


@dataclass
class FeedbackItem:
    """Feedback item data structure"""
    id: str
    project_id: str
    user_id: str
    category: str
    priority: str
    description: str
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None


class PartnerManagementAgent:
    """Manages partner relationships and onboarding"""
    
    async def onboard_partner(self, partner_info: Dict[str, Any]) -> Dict[str, Any]:
        """Onboard a new partner to the collaboration system"""
        await asyncio.sleep(0.5)  # Simulate onboarding process
        
        return {
            "partner_id": f"partner_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "name": partner_info.get("name", "Unknown Partner"),
            "email": partner_info.get("email"),
            "role": partner_info.get("role", "collaborator"),
            "permissions": self._determine_permissions(partner_info.get("role")),
            "onboarding_status": "completed",
            "welcome_message": f"Welcome {partner_info.get('name')}! You now have access to the collaboration workspace.",
            "next_steps": [
                "Complete profile setup",
                "Review project documentation",
                "Join team communication channels",
                "Attend project kickoff meeting"
            ]
        }
    
    def _determine_permissions(self, role: str) -> List[str]:
        """Determine permissions based on partner role"""
        permission_map = {
            "investor": ["view_progress", "view_financials", "receive_updates"],
            "advisor": ["view_progress", "provide_feedback", "view_metrics"],
            "developer": ["view_code", "contribute_code", "view_tasks"],
            "designer": ["view_designs", "contribute_designs", "view_feedback"],
            "customer": ["view_demo", "provide_feedback", "test_features"],
            "collaborator": ["view_progress", "provide_feedback"]
        }
        return permission_map.get(role, permission_map["collaborator"])
    
    async def create_partner_workspace(self, project_id: str, partners: List[Dict]) -> CollaborationSpace:
        """Create a dedicated workspace for partners"""
        await asyncio.sleep(0.3)  # Simulate workspace creation
        
        return CollaborationSpace(
            id=f"workspace_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=f"Partner Workspace - {project_id}",
            type=CollaborationSpaceType.PARTNER_WORKSPACE,
            project_id=project_id,
            members=[p["partner_id"] for p in partners],
            created_at=datetime.now(),
            settings={
                "communication_channels": ["general", "updates", "feedback"],
                "file_sharing": True,
                "video_calls": True,
                "project_boards": True,
                "notifications": "real_time"
            }
        )


class FeedbackCollectionAgent:
    """Handles feedback collection and analysis"""
    
    async def collect_feedback(
        self, 
        project_id: str, 
        feedback_type: str, 
        feedback_data: Dict[str, Any]
    ) -> FeedbackItem:
        """Collect and process feedback from users"""
        await asyncio.sleep(0.2)  # Simulate feedback processing
        
        feedback = FeedbackItem(
            id=f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            project_id=project_id,
            user_id=feedback_data.get("user_id", "anonymous"),
            category=feedback_type,
            priority=self._determine_priority(feedback_data),
            description=feedback_data.get("description", ""),
            status="new",
            created_at=datetime.now()
        )
        
        # Analyze feedback for actionable insights
        insights = await self._analyze_feedback(feedback)
        feedback.analysis = insights
        
        return feedback
    
    def _determine_priority(self, feedback_data: Dict[str, Any]) -> str:
        """Determine priority level based on feedback content"""
        description = feedback_data.get("description", "").lower()
        
        if any(keyword in description for keyword in ["bug", "error", "broken", "not working"]):
            return "high"
        elif any(keyword in description for keyword in ["improvement", "enhancement", "feature"]):
            return "medium"
        else:
            return "low"
    
    async def _analyze_feedback(self, feedback: FeedbackItem) -> Dict[str, Any]:
        """Analyze feedback for insights and recommendations"""
        await asyncio.sleep(0.3)  # Simulate AI analysis
        
        return {
            "sentiment": "positive",  # AI analysis of sentiment
            "key_themes": ["usability", "performance", "features"],
            "actionable_items": [
                "Improve loading speed",
                "Add user onboarding tutorial",
                "Enhance mobile responsiveness"
            ],
            "urgency_score": 7.5,  # Out of 10
            "recommended_actions": [
                "Schedule user interview",
                "Create improvement task",
                "Update product roadmap"
            ]
        }
    
    async def get_feedback_summary(self, project_id: str) -> Dict[str, Any]:
        """Get summary of all feedback for a project"""
        await asyncio.sleep(0.2)  # Simulate data aggregation
        
        return {
            "total_feedback": 25,
            "feedback_by_category": {
                "bug_reports": 8,
                "feature_requests": 12,
                "usability_issues": 3,
                "general_feedback": 2
            },
            "feedback_by_priority": {
                "high": 5,
                "medium": 15,
                "low": 5
            },
            "average_sentiment": 7.2,
            "top_themes": [
                "User interface improvements",
                "Performance optimization",
                "New feature requests"
            ],
            "response_rate": 0.85,  # 85% of feedback has been addressed
            "average_resolution_time": "3.2 days"
        }


class ProjectManagementAgent:
    """Handles project management and task tracking"""
    
    async def create_project_plan(self, project: Any) -> Dict[str, Any]:
        """Create a comprehensive project management plan"""
        await asyncio.sleep(0.5)  # Simulate planning
        
        return {
            "project_id": project.id,
            "phases": [
                {
                    "name": "Planning & Setup",
                    "duration": "1 week",
                    "tasks": [
                        {"name": "Define requirements", "assignee": "product_manager", "status": "pending"},
                        {"name": "Set up development environment", "assignee": "tech_lead", "status": "pending"},
                        {"name": "Create project timeline", "assignee": "project_manager", "status": "pending"}
                    ]
                },
                {
                    "name": "Development",
                    "duration": "3-4 weeks",
                    "tasks": [
                        {"name": "Backend API development", "assignee": "backend_developer", "status": "pending"},
                        {"name": "Frontend development", "assignee": "frontend_developer", "status": "pending"},
                        {"name": "Database setup", "assignee": "backend_developer", "status": "pending"},
                        {"name": "Testing", "assignee": "qa_engineer", "status": "pending"}
                    ]
                },
                {
                    "name": "Testing & Launch",
                    "duration": "1-2 weeks",
                    "tasks": [
                        {"name": "User acceptance testing", "assignee": "qa_engineer", "status": "pending"},
                        {"name": "Performance optimization", "assignee": "tech_lead", "status": "pending"},
                        {"name": "Deployment", "assignee": "devops_engineer", "status": "pending"},
                        {"name": "Launch preparation", "assignee": "product_manager", "status": "pending"}
                    ]
                }
            ],
            "milestones": [
                {"name": "MVP Complete", "date": "2024-02-15", "status": "pending"},
                {"name": "Beta Launch", "date": "2024-03-01", "status": "pending"},
                {"name": "Production Launch", "date": "2024-03-15", "status": "pending"}
            ],
            "resources": {
                "team_members": 5,
                "estimated_hours": 400,
                "budget": "$50,000"
            }
        }
    
    async def update_task_status(self, task_id: str, status: str, assignee: str) -> Dict[str, Any]:
        """Update the status of a specific task"""
        await asyncio.sleep(0.1)  # Simulate update
        
        return {
            "task_id": task_id,
            "status": status,
            "assignee": assignee,
            "updated_at": datetime.now().isoformat(),
            "message": f"Task {task_id} status updated to {status} by {assignee}"
        }
    
    async def get_project_dashboard(self, project_id: str) -> Dict[str, Any]:
        """Get comprehensive project dashboard data"""
        await asyncio.sleep(0.3)  # Simulate data aggregation
        
        return {
            "project_id": project_id,
            "overall_progress": 35,  # Percentage
            "tasks_completed": 12,
            "tasks_total": 34,
            "upcoming_deadlines": [
                {"task": "API Documentation", "due_date": "2024-01-20", "assignee": "backend_developer"},
                {"task": "UI Mockups", "due_date": "2024-01-22", "assignee": "designer"}
            ],
            "team_performance": {
                "backend_developer": {"tasks_completed": 5, "efficiency": 0.9},
                "frontend_developer": {"tasks_completed": 4, "efficiency": 0.85},
                "designer": {"tasks_completed": 3, "efficiency": 0.95}
            },
            "risks": [
                {"description": "API integration delay", "severity": "medium", "mitigation": "Add buffer time"},
                {"description": "Design approval pending", "severity": "low", "mitigation": "Schedule review meeting"}
            ]
        }


class CommunicationAgent:
    """Handles communication and notifications"""
    
    async def send_notification(
        self, 
        recipient_id: str, 
        message: str, 
        notification_type: str = "info"
    ) -> Dict[str, Any]:
        """Send notification to a user"""
        await asyncio.sleep(0.1)  # Simulate notification sending
        
        return {
            "notification_id": f"notif_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "recipient_id": recipient_id,
            "message": message,
            "type": notification_type,
            "sent_at": datetime.now().isoformat(),
            "status": "delivered"
        }
    
    async def schedule_meeting(
        self, 
        participants: List[str], 
        meeting_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Schedule a meeting with participants"""
        await asyncio.sleep(0.2)  # Simulate meeting scheduling
        
        return {
            "meeting_id": f"meeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": meeting_details.get("title", "Project Meeting"),
            "participants": participants,
            "scheduled_time": meeting_details.get("scheduled_time"),
            "duration": meeting_details.get("duration", "60 minutes"),
            "meeting_link": f"https://meet.yourdomain.com/{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "agenda": meeting_details.get("agenda", []),
            "status": "scheduled"
        }
    
    async def send_project_update(self, project_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send project update to all stakeholders"""
        await asyncio.sleep(0.3)  # Simulate update distribution
        
        return {
            "update_id": f"update_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "project_id": project_id,
            "title": update_data.get("title", "Project Update"),
            "content": update_data.get("content", ""),
            "recipients": update_data.get("recipients", []),
            "sent_at": datetime.now().isoformat(),
            "delivery_status": "sent_to_all_recipients"
        }


class CollaborationAgent:
    """
    Master agent for collaboration management.
    
    This agent coordinates partner management, feedback collection,
    project management, and communication to enable effective collaboration.
    """
    
    def __init__(self):
        """Initialize with specialized sub-agents"""
        self.partner_management = PartnerManagementAgent()
        self.feedback_collection = FeedbackCollectionAgent()
        self.project_management = ProjectManagementAgent()
        self.communication = CommunicationAgent()
        
        # Storage for collaboration data (in production, this would be a database)
        self.collaboration_spaces: Dict[str, CollaborationSpace] = {}
        self.feedback_items: List[FeedbackItem] = []
    
    async def setup_collaboration_space(
        self, 
        project: Any, 
        team_members: List[str]
    ) -> Dict[str, Any]:
        """
        Set up comprehensive collaboration space for a project.
        
        Args:
            project: Project object
            team_members: List of team member IDs
            
        Returns:
            Collaboration space configuration and setup details
        """
        print(f"Setting up collaboration space for project: {project.id}")
        
        # Create partner workspace
        partner_workspace = await self.partner_management.create_partner_workspace(
            project.id, 
            [{"partner_id": member, "role": "collaborator"} for member in team_members]
        )
        
        self.collaboration_spaces[partner_workspace.id] = partner_workspace
        
        # Create project management plan
        project_plan = await self.project_management.create_project_plan(project)
        
        # Set up communication channels
        communication_setup = await self._setup_communication_channels(project.id, team_members)
        
        # Send welcome notifications
        welcome_messages = await self._send_welcome_messages(project, team_members)
        
        collaboration_space = {
            "workspace_id": partner_workspace.id,
            "project_id": project.id,
            "team_members": team_members,
            "workspace_settings": partner_workspace.settings,
            "project_plan": project_plan,
            "communication_setup": communication_setup,
            "welcome_messages": welcome_messages,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        print(f"Collaboration space created successfully: {partner_workspace.id}")
        return collaboration_space
    
    async def collect_and_process_feedback(
        self, 
        project_id: str, 
        feedback_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Collect and process feedback for a project"""
        
        feedback = await self.feedback_collection.collect_feedback(
            project_id, 
            feedback_data.get("category", "general"),
            feedback_data
        )
        
        self.feedback_items.append(feedback)
        
        # Notify relevant team members
        await self._notify_feedback_received(project_id, feedback)
        
        return {
            "feedback_id": feedback.id,
            "status": "received",
            "priority": feedback.priority,
            "assigned_to": self._assign_feedback_owner(feedback),
            "estimated_resolution": self._estimate_resolution_time(feedback),
            "next_steps": [
                "Review feedback details",
                "Assess impact on project timeline",
                "Create action plan",
                "Update stakeholders"
            ]
        }
    
    async def get_collaboration_dashboard(self, project_id: str) -> Dict[str, Any]:
        """Get comprehensive collaboration dashboard for a project"""
        
        # Get project feedback summary
        feedback_summary = await self.feedback_collection.get_feedback_summary(project_id)
        
        # Get project management dashboard
        project_dashboard = await self.project_management.get_project_dashboard(project_id)
        
        # Get collaboration space info
        workspace = next((w for w in self.collaboration_spaces.values() 
                         if w.project_id == project_id), None)
        
        return {
            "project_id": project_id,
            "collaboration_space": {
                "id": workspace.id if workspace else None,
                "name": workspace.name if workspace else None,
                "active_members": len(workspace.members) if workspace else 0,
                "settings": workspace.settings if workspace else {}
            },
            "feedback_summary": feedback_summary,
            "project_dashboard": project_dashboard,
            "recent_activity": await self._get_recent_activity(project_id),
            "upcoming_events": await self._get_upcoming_events(project_id)
        }
    
    async def notify_project_failure(self, project: Any, error_message: str):
        """Notify stakeholders about project failure"""
        
        notification_message = f"""
        Project {project.name} has encountered an issue:
        
        Error: {error_message}
        
        The project has been paused and the team is investigating.
        We will provide updates as soon as we have more information.
        """
        
        # Notify all team members
        for member in project.team_members:
            await self.communication.send_notification(
                member,
                notification_message,
                "error"
            )
        
        # Notify project owner
        await self.communication.send_notification(
            project.owner_id,
            f"Project {project.name} has failed: {error_message}",
            "critical"
        )
    
    async def _setup_communication_channels(self, project_id: str, team_members: List[str]) -> Dict[str, Any]:
        """Set up communication channels for the project"""
        await asyncio.sleep(0.2)  # Simulate channel setup
        
        return {
            "slack_workspace": f"project-{project_id}",
            "channels": [
                {"name": "general", "purpose": "General project discussion"},
                {"name": "development", "purpose": "Technical development discussions"},
                {"name": "feedback", "purpose": "User feedback and feature requests"},
                {"name": "updates", "purpose": "Project updates and announcements"}
            ],
            "video_calls": {
                "platform": "Zoom/Google Meet",
                "recurring_meetings": [
                    {"name": "Daily Standup", "frequency": "daily", "time": "9:00 AM"},
                    {"name": "Weekly Review", "frequency": "weekly", "time": "Friday 2:00 PM"}
                ]
            },
            "email_distribution": f"project-{project_id}@yourdomain.com"
        }
    
    async def _send_welcome_messages(self, project: Any, team_members: List[str]) -> List[Dict[str, Any]]:
        """Send welcome messages to all team members"""
        messages = []
        
        for member in team_members:
            message = f"""
            Welcome to the {project.name} project!
            
            You now have access to the collaboration workspace where you can:
            - View project progress and milestones
            - Provide feedback and suggestions
            - Participate in team discussions
            - Access project documentation
            
            Let's build something amazing together!
            """
            
            notification = await self.communication.send_notification(
                member,
                message,
                "welcome"
            )
            messages.append(notification)
        
        return messages
    
    async def _notify_feedback_received(self, project_id: str, feedback: FeedbackItem):
        """Notify team about new feedback"""
        message = f"""
        New feedback received for project {project_id}:
        
        Category: {feedback.category}
        Priority: {feedback.priority}
        Description: {feedback.description}
        
        Please review and take appropriate action.
        """
        
        # Notify project manager
        await self.communication.send_notification(
            "project_manager",
            message,
            "feedback"
        )
    
    def _assign_feedback_owner(self, feedback: FeedbackItem) -> str:
        """Assign feedback to appropriate team member"""
        if feedback.category == "bug_reports":
            return "qa_engineer"
        elif feedback.category == "feature_requests":
            return "product_manager"
        else:
            return "project_manager"
    
    def _estimate_resolution_time(self, feedback: FeedbackItem) -> str:
        """Estimate time to resolve feedback"""
        if feedback.priority == "high":
            return "1-2 days"
        elif feedback.priority == "medium":
            return "3-5 days"
        else:
            return "1-2 weeks"
    
    async def _get_recent_activity(self, project_id: str) -> List[Dict[str, Any]]:
        """Get recent activity for the project"""
        await asyncio.sleep(0.1)  # Simulate data retrieval
        
        return [
            {
                "type": "feedback_received",
                "description": "New feature request: Dark mode support",
                "timestamp": "2024-01-15T10:30:00Z",
                "user": "customer_123"
            },
            {
                "type": "task_completed",
                "description": "API documentation completed",
                "timestamp": "2024-01-15T09:15:00Z",
                "user": "backend_developer"
            },
            {
                "type": "meeting_scheduled",
                "description": "Weekly review meeting scheduled",
                "timestamp": "2024-01-15T08:45:00Z",
                "user": "project_manager"
            }
        ]
    
    async def _get_upcoming_events(self, project_id: str) -> List[Dict[str, Any]]:
        """Get upcoming events for the project"""
        await asyncio.sleep(0.1)  # Simulate data retrieval
        
        return [
            {
                "type": "meeting",
                "title": "Daily Standup",
                "time": "2024-01-16T09:00:00Z",
                "participants": 5
            },
            {
                "type": "deadline",
                "title": "MVP Feature Complete",
                "time": "2024-01-20T17:00:00Z",
                "priority": "high"
            },
            {
                "type": "meeting",
                "title": "Weekly Review",
                "time": "2024-01-19T14:00:00Z",
                "participants": 8
            }
        ]


# Example usage and testing
async def main():
    """Example usage of the Collaboration Agent"""
    agent = CollaborationAgent()
    
    # Mock project
    class MockProject:
        def __init__(self):
            self.id = "proj_123"
            self.name = "AI Finance Assistant"
            self.owner_id = "owner_456"
            self.team_members = ["dev_1", "designer_1", "pm_1"]
    
    project = MockProject()
    
    # Set up collaboration space
    collaboration_space = await agent.setup_collaboration_space(
        project, 
        project.team_members
    )
    
    print(f"Collaboration space created: {collaboration_space['workspace_id']}")
    
    # Collect feedback
    feedback_result = await agent.collect_and_process_feedback(
        project.id,
        {
            "user_id": "customer_123",
            "category": "feature_request",
            "description": "Please add dark mode support to the app"
        }
    )
    
    print(f"Feedback processed: {feedback_result['feedback_id']}")
    
    # Get dashboard
    dashboard = await agent.get_collaboration_dashboard(project.id)
    print(f"Dashboard data: {dashboard['feedback_summary']['total_feedback']} feedback items")


if __name__ == "__main__":
    asyncio.run(main())

