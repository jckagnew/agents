#!/usr/bin/env python3
"""
Quick test script to verify iOS integration
"""

import asyncio
import subprocess
import json
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from universal_mobile_testing import UniversalMobileTester

async def test_ios_integration():
    """Test iOS integration and simulator availability"""
    print("🍎 Testing iOS Integration...")
    
    tester = UniversalMobileTester()
    
    # Discover iOS devices
    print("1. Discovering iOS simulators...")
    ios_devices = tester.discover_ios_devices()
    
    if not ios_devices:
        print("❌ No iOS simulators found")
        print("💡 Make sure Xcode is installed and simulators are set up")
        return False
    
    print(f"✅ Found {len(ios_devices)} iOS simulators:")
    for device in ios_devices[:5]:  # Show first 5
        print(f"   - {device.name} ({device.version}) - {device.status}")
    
    # Test simulator functionality
    print("\n2. Testing simulator functionality...")
    try:
        # Try to list devices
        result = subprocess.run(['xcrun', 'simctl', 'list', 'devices'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ iOS Simulator tools working")
        else:
            print("❌ iOS Simulator tools not working")
            return False
    except Exception as e:
        print(f"❌ Error testing iOS tools: {e}")
        return False
    
    # Test opening simulator
    print("\n3. Testing simulator launch...")
    try:
        subprocess.run(['open', '-a', 'Simulator'], check=True)
        print("✅ iOS Simulator launched successfully")
    except Exception as e:
        print(f"❌ Failed to launch simulator: {e}")
        return False
    
    print("\n🎉 iOS integration test completed successfully!")
    return True

if __name__ == "__main__":
    asyncio.run(test_ios_integration())
