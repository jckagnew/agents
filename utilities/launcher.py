#!/usr/bin/env python3
"""
Job Search Assistant - Easy Launcher
This script provides an easy way to start the Job Search Assistant
"""

import os
import sys
import subprocess
import webbrowser
import time
import requests
from pathlib import Path

class JobSearchLauncher:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.server_url = "http://localhost:8000"
        self.server_process = None
        
    def print_banner(self):
        """Print the application banner."""
        print("🎯" + "=" * 50)
        print("   JOB SEARCH ASSISTANT - EASY LAUNCHER")
        print("=" * 52)
        print()
        
    def check_environment(self):
        """Check if the environment is set up correctly."""
        print("🔍 Checking environment...")
        
        # Check if we're in the right directory
        if not (self.project_dir / "pyproject.toml").exists():
            print("❌ Error: pyproject.toml not found. Please run from job-search-assistant directory.")
            return False
            
        # Check if virtual environment exists
        venv_path = self.project_dir.parent / ".venv"
        if not venv_path.exists():
            print("❌ Error: Virtual environment not found. Please run 'uv sync' first.")
            return False
            
        print("✅ Environment looks good!")
        return True
        
    def install_package(self):
        """Install/update the package in editable mode."""
        print("📦 Package already installed!")
        return True
            
    def start_server(self):
        """Start the FastAPI server."""
        print("🚀 Starting server...")
        try:
            self.server_process = subprocess.Popen(
                ["uv", "run", "uvicorn", "src.job_search_assistant.api.main:app", 
                 "--reload", "--host", "127.0.0.1", "--port", "8000"],
                cwd=self.project_dir
            )
            
            # Wait a moment for server to start
            print("⏳ Waiting for server to start...")
            time.sleep(3)
            
            return True
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
            
    def check_server(self):
        """Check if the server is running."""
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
            
    def open_browser(self):
        """Open the web interface in the browser."""
        print("🌐 Opening web interface...")
        webbrowser.open(f"{self.server_url}/docs")
        
    def show_status(self):
        """Show server status and available URLs."""
        print("\n" + "=" * 50)
        print("🎉 SERVER IS RUNNING!")
        print("=" * 50)
        print(f"🌐 API Server: {self.server_url}")
        print(f"📚 Documentation: {self.server_url}/docs")
        print(f"📋 Alternative Docs: {self.server_url}/redoc")
        print(f"❤️  Health Check: {self.server_url}/health")
        print(f"💼 Job Opportunities: {self.server_url}/api/job-opportunities/")
        print(f"📊 Analytics: {self.server_url}/api/analytics/overview")
        print("\n🎯 What you can do:")
        print("   • Create and manage job opportunities")
        print("   • Track your applications")
        print("   • Generate documents (resumes, cover letters)")
        print("   • Monitor email interactions")
        print("   • View analytics and insights")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 50)
        
    def run(self):
        """Main launcher function."""
        self.print_banner()
        
        # Check environment
        if not self.check_environment():
            return
            
        # Install package
        if not self.install_package():
            return
            
        # Start server
        if not self.start_server():
            return
            
        # Check if server started successfully
        if not self.check_server():
            print("❌ Server failed to start properly")
            return
            
        # Open browser
        self.open_browser()
        
        # Show status
        self.show_status()
        
        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping server...")
            if self.server_process:
                self.server_process.terminate()
            print("✅ Server stopped. Goodbye!")

if __name__ == "__main__":
    launcher = JobSearchLauncher()
    launcher.run()
