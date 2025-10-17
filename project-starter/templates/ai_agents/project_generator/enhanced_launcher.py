"""
Enhanced Launcher for AI Agent Project Generator

This module provides a comprehensive launcher that brings together all the
enhanced UI components: interactive UI, project wizard, and marketplace.
"""

import sys
import argparse
from pathlib import Path

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description='Enhanced AI Agent Project Generator')
    parser.add_argument('--mode', 
                       choices=['interactive', 'wizard', 'marketplace', 'web', 'cli'], 
                       default='interactive',
                       help='Choose interface mode')
    parser.add_argument('--port', type=int, default=5000,
                       help='Port for web interface (default: 5000)')
    parser.add_argument('--user', type=str, default='user',
                       help='User ID for marketplace features')
    
    args = parser.parse_args()
    
    print("🚀 Enhanced AI Agent Project Generator")
    print("=" * 50)
    print()
    
    if args.mode == 'interactive':
        print("🎨 Starting Enhanced Interactive Interface...")
        try:
            from enhanced_ui import EnhancedProjectGeneratorUI
            generator = EnhancedProjectGeneratorUI()
            generator.run_enhanced_generator()
        except ImportError as e:
            print(f"❌ Error importing enhanced UI: {e}")
            print("Make sure all dependencies are installed")
            sys.exit(1)
    
    elif args.mode == 'wizard':
        print("🧙‍♂️ Starting Project Wizard...")
        try:
            from project_wizard import ProjectWizard
            wizard = ProjectWizard()
            wizard.run_wizard()
        except ImportError as e:
            print(f"❌ Error importing project wizard: {e}")
            print("Make sure all dependencies are installed")
            sys.exit(1)
    
    elif args.mode == 'marketplace':
        print("🛒 Starting Project Marketplace...")
        try:
            from project_marketplace import MarketplaceUI
            marketplace_ui = MarketplaceUI()
            marketplace_ui.login(args.user)
            marketplace_ui.browse_marketplace()
        except ImportError as e:
            print(f"❌ Error importing marketplace: {e}")
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
    
    elif args.mode == 'cli':
        print("💻 Starting Command-Line Interface...")
        try:
            from interactive_ui import ProjectGeneratorUI
            generator = ProjectGeneratorUI()
            generator.run_interactive_generator()
        except ImportError as e:
            print(f"❌ Error importing CLI interface: {e}")
            print("Make sure all dependencies are installed")
            sys.exit(1)

if __name__ == '__main__':
    main()





