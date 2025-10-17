#!/usr/bin/env python3
"""
ntfy.sh Notification Agent
Replaces ntfy.sh with ntfy.sh for better reliability and self-hosting
"""

import os
import requests
import json
from typing import Optional
from agents import Agent

class NtfyNotificationService:
    """Service for sending notifications via ntfy.sh"""
    
    def __init__(self, server_url: str = None, topic: str = "mytopic"):
        self.server_url = server_url or os.getenv('NTFY_SERVER_URL', 'http://192.168.0.146:8080')
        self.topic = topic or os.getenv('NTFY_TOPIC', 'mytopic')
    
    def send_notification(self, message: str, title: str = None, priority: int = 3, url: str = None) -> dict:
        """Send a notification via ntfy.sh"""
        try:
            # Prepare headers
            headers = {'Content-Type': 'text/plain'}
            if title:
                headers['X-Title'] = title
            if priority:
                headers['X-Priority'] = str(priority)
            if url:
                headers['X-Actions'] = f'view, Open Link, {url}'
            
            # Send notification
            response = requests.post(
                f"{self.server_url}/{self.topic}",
                headers=headers,
                data=message,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'response': response.json(),
                    'message': 'Notification sent successfully'
                }
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}: {response.text}',
                    'message': 'Failed to send notification'
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Network error sending notification'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Unexpected error sending notification'
            }

# Initialize notification service
notification_service = NtfyNotificationService()

# Create the agent
ntfy_notification_agent = Agent(
    name="ntfy Notification Agent",
    goal="Send notifications via ntfy.sh when research is complete",
    backstory="""You are a notification agent that sends alerts via ntfy.sh 
    when research tasks are completed. You provide clear, concise notifications 
    with relevant details about the completed research.""",
    instructions="""When you receive research content, send a notification with:
    1. A clear title indicating the research is complete
    2. A brief summary of what was researched
    3. A link to view the full report if available
    4. Appropriate priority level (3 for normal, 4 for important, 5 for urgent)
    
    Always include the topic 'mytopic' and ensure the notification is helpful and informative.""",
    tools=[],
    verbose=True
)

async def send_research_notification(research_content: str, report_url: str = None) -> dict:
    """Send a notification about completed research"""
    
    # Extract key information from research content
    lines = research_content.split('\n')
    title_line = next((line for line in lines if line.startswith('#')), "Research Complete")
    title = title_line.replace('#', '').strip()
    
    # Create a brief summary (first 200 characters)
    summary = research_content[:200] + "..." if len(research_content) > 200 else research_content
    
    # Send notification
    result = notification_service.send_notification(
        message=f"Research completed: {summary}",
        title=f"🔍 {title}",
        priority=4,
        url=report_url
    )
    
    return result

# Example usage
if __name__ == "__main__":
    # Test the notification service
    result = notification_service.send_notification(
        message="Test notification from ntfy.sh! 🚀",
        title="Deep Research Test",
        priority=3
    )
    print(json.dumps(result, indent=2))
