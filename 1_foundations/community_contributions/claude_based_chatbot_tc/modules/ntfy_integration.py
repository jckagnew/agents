#!/usr/bin/env python3
"""
ntfy.sh Integration Module
Universal notification service for all projects
"""

import os
import requests
from typing import Optional

class NtfyService:
    """Universal ntfy.sh notification service"""
    
    def __init__(self, server_url: str = None, topic: str = None):
        self.server_url = server_url or os.getenv('NTFY_SERVER_URL', 'http://192.168.0.146:8080')
        self.topic = topic or os.getenv('NTFY_TOPIC', 'mytopic')
    
    def send(self, message: str, title: str = None, priority: int = 3, url: str = None) -> bool:
        """Send a notification via ntfy.sh"""
        try:
            headers = {'Content-Type': 'text/plain'}
            if title:
                headers['X-Title'] = title
            if priority:
                headers['X-Priority'] = str(priority)
            if url:
                headers['X-Actions'] = f'view, Open Link, {url}'
            
            response = requests.post(
                f"{self.server_url}/{self.topic}",
                headers=headers,
                data=message,
                timeout=10
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Failed to send notification: {e}")
            return False

# Global instance
ntfy = NtfyService()

# Convenience functions
def notify(message: str, title: str = None, priority: int = 3, url: str = None):
    """Send a notification"""
    return ntfy.send(message, title, priority, url)

def notify_success(message: str, title: str = "Success"):
    """Send a success notification"""
    return ntfy.send(message, title, 3)

def notify_error(message: str, title: str = "Error"):
    """Send an error notification"""
    return ntfy.send(message, title, 5)

def notify_info(message: str, title: str = "Info"):
    """Send an info notification"""
    return ntfy.send(message, title, 2)
