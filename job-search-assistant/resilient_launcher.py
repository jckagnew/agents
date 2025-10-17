#!/usr/bin/env python3
"""
Resilient Job Search Assistant Launcher
Handles port conflicts, import errors, and provides fallback options
"""

import subprocess
import webbrowser
import time
import requests
import socket
import sys
from pathlib import Path
import random

class ResilientJobSearchLauncher:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.base_port = 8000
        self.max_port_attempts = 10
        self.server_process = None
        self.server_url = None
        
    def print_banner(self):
        """Print the application banner."""
        print("🎯" + "=" * 60)
        print("   JOB SEARCH ASSISTANT - RESILIENT LAUNCHER")
        print("=" * 62)
        print()
        
    def check_port_available(self, port):
        """Check if a port is available."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return True
        except OSError:
            return False
            
    def find_available_port(self):
        """Find an available port starting from base_port."""
        print(f"🔍 Checking for available port starting from {self.base_port}...")
        
        for port in range(self.base_port, self.base_port + self.max_port_attempts):
            if self.check_port_available(port):
                print(f"✅ Found available port: {port}")
                return port
            else:
                print(f"⚠️  Port {port} is in use, trying next...")
                
        # If no port found in range, try random ports
        print("🔄 Trying random ports...")
        for _ in range(20):
            port = random.randint(8001, 8999)
            if self.check_port_available(port):
                print(f"✅ Found available random port: {port}")
                return port
                
        return None
        
    def check_imports(self):
        """Check if the application can be imported."""
        print("🔍 Checking application imports...")
        try:
            # Test basic imports
            import sys
            sys.path.insert(0, str(self.project_dir / "src"))
            
            # Try to import the main app
            from job_search_assistant.api.main import app
            print("✅ Application imports successful!")
            return True
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("🔧 Attempting to fix import issues...")
            return self.fix_imports()
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
            
    def fix_imports(self):
        """Attempt to fix common import issues."""
        print("🔧 Attempting to fix import issues...")
        
        # Check if we're in the right directory
        if not (self.project_dir / "src" / "job_search_assistant").exists():
            print("❌ Job search assistant source not found")
            return False
            
        # Try to install the package
        try:
            print("📦 Installing package in editable mode...")
            result = subprocess.run(
                ["uv", "pip", "install", "-e", "."],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print("✅ Package installed successfully!")
                return True
            else:
                print(f"❌ Package installation failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error installing package: {e}")
            return False
            
    def start_server(self, port):
        """Start the FastAPI server on the specified port."""
        print(f"🚀 Starting server on port {port}...")
        try:
            self.server_process = subprocess.Popen(
                ["uv", "run", "python", "-m", "uvicorn", "src.job_search_assistant.api.main:app", 
                 "--reload", "--host", "127.0.0.1", f"--port", str(port)],
                cwd=self.project_dir
            )
            
            # Wait for server to start
            print("⏳ Waiting for server to start...")
            for i in range(10):
                time.sleep(1)
                try:
                    response = requests.get(f"http://127.0.0.1:{port}/health", timeout=2)
                    if response.status_code == 200:
                        print("✅ Server started successfully!")
                        self.server_url = f"http://127.0.0.1:{port}"
                        return True
                except:
                    if i < 9:
                        print(f"⏳ Still starting... ({i+1}/10)")
                    continue
                    
            print("❌ Server failed to start within timeout")
            return False
            
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
            
    def open_browser(self):
        """Open the web interface in the browser."""
        if self.server_url:
            print(f"🌐 Opening web interface at {self.server_url}/docs...")
            webbrowser.open(f"{self.server_url}/docs")
            
    def show_status(self):
        """Show server status and available URLs."""
        if not self.server_url:
            return
            
        print("\n" + "=" * 60)
        print("🎉 SERVER IS RUNNING!")
        print("=" * 60)
        print(f"🌐 API Server: {self.server_url}")
        print(f"📚 Documentation: {self.server_url}/docs")
        print(f"📋 Alternative Docs: {self.server_url}/redoc")
        print(f"❤️  Health Check: {self.server_url}/health")
        print(f"💼 Job Opportunities: {self.server_url}/api/job-opportunities/")
        print(f"📊 Analytics: {self.server_url}/api/analytics/overview")
        print("\n�� What you can do:")
        print("   • Create and manage job opportunities")
        print("   • Track your applications")
        print("   • Generate documents (resumes, cover letters)")
        print("   • Monitor email interactions")
        print("   • View analytics and insights")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 60)
        
    def cleanup(self):
        """Clean up resources."""
        if self.server_process:
            print("\n🛑 Stopping server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            print("✅ Server stopped.")
            
    def run(self):
        """Main launcher function."""
        self.print_banner()
        
        try:
            # Check imports
            if not self.check_imports():
                print("\n❌ Failed to resolve import issues.")
                print("💡 Try running: cd /Users/jackagnew/projects/agents/job-search-assistant && uv sync")
                return False
                
            # Find available port
            port = self.find_available_port()
            if not port:
                print("\n❌ No available ports found. Please close some applications and try again.")
                return False
                
            # Start server
            if not self.start_server(port):
                print("\n❌ Failed to start server.")
                return False
                
            # Open browser
            self.open_browser()
            
            # Show status
            self.show_status()
            
            # Keep running until interrupted
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return False
        finally:
            self.cleanup()

if __name__ == "__main__":
    launcher = ResilientJobSearchLauncher()
    success = launcher.run()
    sys.exit(0 if success else 1)
