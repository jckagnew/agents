#!/usr/bin/env python3
"""
Final Job Search Assistant Launcher
"""

import subprocess
import webbrowser
import time
import requests
from pathlib import Path

def main():
    print("🎯 JOB SEARCH ASSISTANT - FINAL LAUNCHER")
    print("=" * 50)
    
    project_dir = Path(__file__).parent
    
    print("🚀 Starting server...")
    try:
        # Start the server using the correct command
        process = subprocess.Popen(
            ["uv", "run", "python", "-m", "uvicorn", "src.job_search_assistant.api.main:app", 
             "--reload", "--host", "127.0.0.1", "--port", "8000"],
            cwd=project_dir
        )
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(8)
        
        # Check if server is running
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is running!")
                print("\n🌐 Opening web interface...")
                webbrowser.open("http://localhost:8000/docs")
                
                print("\n" + "=" * 50)
                print("🎉 SERVER IS RUNNING!")
                print("=" * 50)
                print("🌐 API Server: http://localhost:8000")
                print("📚 Documentation: http://localhost:8000/docs")
                print("❤️  Health Check: http://localhost:8000/health")
                print("💼 Job Opportunities: http://localhost:8000/api/job-opportunities/")
                print("📊 Analytics: http://localhost:8000/api/analytics/overview")
                print("\nPress Ctrl+C to stop the server")
                print("=" * 50)
                
                # Keep running
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n\n🛑 Stopping server...")
                    process.terminate()
                    print("✅ Server stopped. Goodbye!")
            else:
                print("❌ Server failed to start properly")
                process.terminate()
        except Exception as e:
            print(f"❌ Server not responding: {e}")
            process.terminate()
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
