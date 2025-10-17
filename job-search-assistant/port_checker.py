#!/usr/bin/env python3
"""
Port Conflict Checker for Job Search Assistant
"""

import socket
import subprocess
import sys

def check_port(port):
    """Check if a port is available."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', port))
            return True
    except OSError:
        return False

def find_process_using_port(port):
    """Find what process is using a port."""
    try:
        result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                return lines[1]  # Return the process line
        return None
    except:
        return None

def main():
    print("🔍 Port Conflict Checker")
    print("=" * 30)
    
    base_port = 8000
    max_checks = 10
    
    for port in range(base_port, base_port + max_checks):
        if check_port(port):
            print(f"✅ Port {port} is available")
            if port == base_port:
                print("🎉 Default port 8000 is free!")
            return port
        else:
            process = find_process_using_port(port)
            if process:
                print(f"❌ Port {port} is in use by: {process}")
            else:
                print(f"❌ Port {port} is in use (unknown process)")
    
    print(f"\n⚠️  No available ports found in range {base_port}-{base_port + max_checks - 1}")
    print("💡 Try closing some applications or use a different port range")
    return None

if __name__ == "__main__":
    available_port = main()
    if available_port:
        print(f"\n🚀 You can start the server on port {available_port}")
    else:
        print("\n❌ No available ports found")
        sys.exit(1)
