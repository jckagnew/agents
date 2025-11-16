#!/usr/bin/env python3
"""
Load environment variables from env.master file
"""

import os
from pathlib import Path

def load_env_file(env_file_path):
    """Load environment variables from a file"""
    env_file = Path(env_file_path)
    if not env_file.exists():
        print(f"❌ Environment file not found: {env_file}")
        return False
    
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                os.environ[key] = value
    
    return True

if __name__ == "__main__":
    # Load environment variables
    env_file = Path(__file__).parent.parent.parent.parent / "utilities" / "env.master"
    if load_env_file(env_file):
        print("✅ Environment variables loaded")
        
        # Check specific keys
        keys_to_check = ["UNSPLASH_API_KEY", "PIXABAY_API_KEY", "PEXELS_API_KEY"]
        for key in keys_to_check:
            value = os.getenv(key)
            if value:
                print(f"   {key}: {value[:8]}...{value[-4:]}")
            else:
                print(f"   {key}: Not found")
    else:
        print("❌ Failed to load environment variables")
