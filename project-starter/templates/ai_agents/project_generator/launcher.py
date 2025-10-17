"""
Project Generator Launcher

This module provides a simple launcher for the AI Agent Project Generator
with options for both command-line and web interfaces.
"""

import sys
import argparse
from pathlib import Path

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description='AI Agent Project Generator')
    parser.add_argument('--mode', choices=['cli', 'web'], default='cli',
                       help='Choose interface mode: cli (command-line) or web (browser)')
    parser.add_argument('--port', type=int, default=5000,
                       help='Port for web interface (default: 5000)')
    
    args = parser.parse_args()
    
    if args.mode == 'cli':
        print("🚀 Starting Command-Line Interface...")
        try:
            from interactive_ui import ProjectGeneratorUI
            generator = ProjectGeneratorUI()
            generator.run_interactive_generator()
        except ImportError as e:
            print(f"❌ Error importing CLI interface: {e}")
            print("Make sure all dependencies are installed")
            sys.exit(1)
    
    elif args.mode == 'web':
        print("🌐 Starting Web Interface...")
        print(f"Open your browser to: http://localhost:{args.port}")
        try:
            from web_ui import app
            app.run(debug=False, host='0.0.0.0', port=args.port)
        except ImportError as e:
            print(f"❌ Error importing web interface: {e}")
            print("Make sure Flask is installed: pip install flask")
            sys.exit(1)

if __name__ == '__main__':
    main()





