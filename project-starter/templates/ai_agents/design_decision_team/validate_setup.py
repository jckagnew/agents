"""
Design Decision Team Setup Validation
Validates that all components are properly configured
"""

import os
import sys
from pathlib import Path

def validate_environment():
    """Validate environment configuration"""
    print("🔍 Validating Design Decision Team Setup...")
    
    # Check Python dependencies
    required_packages = [
        'crewai',
        'requests',
        'PIL',
        'cv2',
        'reportlab'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - Installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    # Check environment file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Environment file exists")
    else:
        print("❌ Environment file missing")
        print("   Run: cp env_template.txt .env")
    
    # Check API keys
    required_keys = [
        'OPENAI_API_KEY',
        'UNSPLASH_API_KEY',
        'PEXELS_API_KEY'
    ]
    
    missing_keys = []
    for key in required_keys:
        if os.getenv(key):
            print(f"✅ {key} - Set")
        else:
            missing_keys.append(key)
            print(f"❌ {key} - Missing")
    
    # Summary
    print("\n📊 Validation Summary:")
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install crewai[all] requests pillow opencv-python reportlab")
    
    if missing_keys:
        print(f"❌ Missing API keys: {', '.join(missing_keys)}")
        print("   Add keys to .env file")
    
    if not missing_packages and not missing_keys:
        print("✅ All components properly configured!")
        return True
    else:
        print("❌ Setup incomplete. Please fix issues above.")
        return False

if __name__ == "__main__":
    success = validate_environment()
    sys.exit(0 if success else 1)
