#!/usr/bin/env python3
"""
Simple iOS integration test
"""

import subprocess
import json

def test_ios_integration():
    """Test iOS integration and simulator availability"""
    print("🍎 Testing iOS Integration...")
    
    # Test 1: Check if Xcode is installed
    print("1. Checking Xcode installation...")
    try:
        result = subprocess.run(['xcode-select', '--print-path'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"   ✅ Xcode found at: {result.stdout.strip()}")
        else:
            print("   ❌ Xcode not found")
            return False
    except Exception as e:
        print(f"   ❌ Error checking Xcode: {e}")
        return False
    
    # Test 2: Check if simctl is available
    print("2. Checking iOS Simulator tools...")
    try:
        result = subprocess.run(['xcrun', 'simctl', 'list', 'devices'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("   ✅ iOS Simulator tools working")
        else:
            print("   ❌ iOS Simulator tools not working")
            return False
    except Exception as e:
        print(f"   ❌ Error testing iOS tools: {e}")
        return False
    
    # Test 3: List available simulators
    print("3. Listing available iOS simulators...")
    try:
        result = subprocess.run(['xcrun', 'simctl', 'list', 'devices', 'available', '--json'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            device_count = 0
            for runtime, devices in data['devices'].items():
                device_count += len(devices)
                print(f"   📱 {runtime}: {len(devices)} devices")
            
            if device_count > 0:
                print(f"   ✅ Found {device_count} total iOS simulators")
            else:
                print("   ⚠️  No iOS simulators found")
        else:
            print("   ❌ Failed to list simulators")
            return False
    except Exception as e:
        print(f"   ❌ Error listing simulators: {e}")
        return False
    
    # Test 4: Try to open simulator
    print("4. Testing simulator launch...")
    try:
        result = subprocess.run(['open', '-a', 'Simulator'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("   ✅ iOS Simulator launched successfully")
        else:
            print("   ❌ Failed to launch simulator")
            return False
    except Exception as e:
        print(f"   ❌ Error launching simulator: {e}")
        return False
    
    print("\n🎉 iOS integration test completed successfully!")
    print("✅ Xcode is properly installed and configured")
    print("✅ iOS Simulator tools are working")
    print("✅ iOS Simulator can be launched")
    return True

if __name__ == "__main__":
    success = test_ios_integration()
    if success:
        print("\n🚀 iOS testing is ready for use!")
    else:
        print("\n💥 iOS testing setup needs attention")
