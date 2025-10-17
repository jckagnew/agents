#!/usr/bin/env python3
"""
Universal Mobile Testing System
Supports both Android (via Android Studio) and iOS (via Xcode Simulator)
"""

import asyncio
import subprocess
import json
import time
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from browser_verification import BrowserVerifier

@dataclass
class MobileDevice:
    """Represents a mobile device for testing"""
    platform: str  # 'android' or 'ios'
    name: str
    id: str
    status: str  # 'booted', 'shutdown', 'unavailable'
    version: str

@dataclass
class TestResult:
    """Result of a mobile test"""
    platform: str
    device_name: str
    success: bool
    url: str
    errors: List[str]
    screenshot_path: Optional[str] = None
    timestamp: str = None

class UniversalMobileTester:
    """Universal mobile testing system for Android and iOS"""
    
    def __init__(self):
        self.android_devices: List[MobileDevice] = []
        self.ios_devices: List[MobileDevice] = []
        self.test_results: List[TestResult] = []
    
    def discover_android_devices(self) -> List[MobileDevice]:
        """Discover available Android devices/emulators"""
        devices = []
        
        try:
            # Check for connected Android devices
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if line.strip() and 'device' in line:
                        device_id = line.split('\t')[0]
                        status = 'booted' if 'device' in line else 'offline'
                        devices.append(MobileDevice(
                            platform='android',
                            name=f'Android Device {device_id[:8]}',
                            id=device_id,
                            status=status,
                            version='Unknown'
                        ))
            
            # Check for Android emulators
            result = subprocess.run(['emulator', '-list-avds'], capture_output=True, text=True)
            if result.returncode == 0:
                avds = result.stdout.strip().split('\n')
                for avd in avds:
                    if avd.strip():
                        devices.append(MobileDevice(
                            platform='android',
                            name=f'Emulator: {avd}',
                            id=avd,
                            status='shutdown',
                            version='Emulator'
                        ))
        
        except FileNotFoundError:
            print("⚠️  Android SDK tools not found. Install Android Studio.")
        
        self.android_devices = devices
        return devices
    
    def discover_ios_devices(self) -> List[MobileDevice]:
        """Discover available iOS simulators"""
        devices = []
        
        try:
            # List iOS simulators
            result = subprocess.run(['xcrun', 'simctl', 'list', 'devices', 'available', '--json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for runtime, device_list in data['devices'].items():
                    for device in device_list:
                        devices.append(MobileDevice(
                            platform='ios',
                            name=device['name'],
                            id=device['udid'],
                            status=device['state'],
                            version=runtime
                        ))
        
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️  iOS Simulator tools not found. Check Xcode installation.")
        
        self.ios_devices = devices
        return devices
    
    def start_android_emulator(self, device_id: str) -> bool:
        """Start an Android emulator"""
        try:
            print(f"🚀 Starting Android emulator: {device_id}")
            subprocess.Popen(['emulator', '-avd', device_id], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            
            # Wait for emulator to boot
            print("⏳ Waiting for emulator to boot...")
            for i in range(60):  # Wait up to 60 seconds
                result = subprocess.run(['adb', 'shell', 'getprop', 'sys.boot_completed'], 
                                      capture_output=True, text=True)
                if result.stdout.strip() == '1':
                    print("✅ Android emulator booted successfully")
                    return True
                time.sleep(1)
            
            print("❌ Android emulator failed to boot")
            return False
        
        except FileNotFoundError:
            print("❌ Android emulator not found. Install Android Studio.")
            return False
    
    def start_ios_simulator(self, device_id: str) -> bool:
        """Start an iOS simulator"""
        try:
            print(f"🍎 Starting iOS simulator: {device_id}")
            subprocess.run(['xcrun', 'simctl', 'boot', device_id], check=True)
            subprocess.run(['open', '-a', 'Simulator'], check=True)
            
            # Wait for simulator to boot
            print("⏳ Waiting for iOS simulator to boot...")
            for i in range(30):  # Wait up to 30 seconds
                result = subprocess.run(['xcrun', 'simctl', 'list', 'devices', device_id], 
                                      capture_output=True, text=True)
                if 'Booted' in result.stdout:
                    print("✅ iOS simulator booted successfully")
                    return True
                time.sleep(1)
            
            print("❌ iOS simulator failed to boot")
            return False
        
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("❌ iOS simulator tools not found. Check Xcode installation.")
            return False
    
    async def test_web_app_on_device(self, device: MobileDevice, url: str) -> TestResult:
        """Test a web app on a specific mobile device"""
        print(f"🧪 Testing {url} on {device.platform} device: {device.name}")
        
        # Configure browser for mobile testing
        mobile_config = {
            'viewport': {'width': 375, 'height': 667},  # iPhone 6/7/8 size
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        }
        
        if device.platform == 'android':
            mobile_config['user_agent'] = 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36'
            mobile_config['viewport'] = {'width': 360, 'height': 640}
        
        async with BrowserVerifier(headless=True) as verifier:
            # Set mobile viewport
            await verifier.page.set_viewport_size(mobile_config['viewport'])
            await verifier.page.set_extra_http_headers({
                'User-Agent': mobile_config['user_agent']
            })
            
            # Navigate to the app
            try:
                await verifier.page.goto(url, timeout=30000)
                await verifier.page.wait_for_selector('#root', timeout=10000)
                
                # Test mobile-specific functionality
                title = await verifier.page.title()
                
                # Check for mobile responsiveness
                content_width = await verifier.page.evaluate('document.body.scrollWidth')
                viewport_width = mobile_config['viewport']['width']
                is_responsive = content_width <= viewport_width + 50  # Allow some margin
                
                # Take mobile screenshot
                screenshot_path = f"mobile_test_{device.platform}_{int(time.time())}.png"
                await verifier.page.screenshot(path=screenshot_path)
                
                # Check for mobile-specific errors
                errors = []
                if not is_responsive:
                    errors.append("Not mobile responsive")
                
                # Check for touch-friendly elements
                touch_elements = await verifier.page.query_selector_all('button, input, [role="button"]')
                if len(touch_elements) < 3:
                    errors.append("Insufficient touch-friendly elements")
                
                success = len(errors) == 0
                
                result = TestResult(
                    platform=device.platform,
                    device_name=device.name,
                    success=success,
                    url=url,
                    errors=errors,
                    screenshot_path=screenshot_path,
                    timestamp=time.strftime('%Y-%m-%d %H:%M:%S')
                )
                
                self.test_results.append(result)
                return result
                
            except Exception as e:
                result = TestResult(
                    platform=device.platform,
                    device_name=device.name,
                    success=False,
                    url=url,
                    errors=[str(e)],
                    timestamp=time.strftime('%Y-%m-%d %H:%M:%S')
                )
                self.test_results.append(result)
                return result
    
    async def test_all_platforms(self, url: str) -> List[TestResult]:
        """Test a web app on all available mobile platforms"""
        print("🔍 Discovering mobile devices...")
        
        # Discover devices
        android_devices = self.discover_android_devices()
        ios_devices = self.discover_ios_devices()
        
        print(f"📱 Found {len(android_devices)} Android devices")
        print(f"🍎 Found {len(ios_devices)} iOS simulators")
        
        results = []
        
        # Test on Android devices
        for device in android_devices:
            if device.status == 'shutdown' and 'Emulator' in device.name:
                if self.start_android_emulator(device.id):
                    device.status = 'booted'
            
            if device.status == 'booted':
                result = await self.test_web_app_on_device(device, url)
                results.append(result)
        
        # Test on iOS simulators
        for device in ios_devices:
            if device.status == 'Shutdown':
                if self.start_ios_simulator(device.id):
                    device.status = 'Booted'
            
            if device.status == 'Booted':
                result = await self.test_web_app_on_device(device, url)
                results.append(result)
        
        return results
    
    def print_test_summary(self):
        """Print a summary of all test results"""
        print("\n" + "="*50)
        print("📊 MOBILE TESTING SUMMARY")
        print("="*50)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r.success)
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        print(f"Success Rate: {(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
        
        print("\n📱 Test Results by Platform:")
        for result in self.test_results:
            status = "✅" if result.success else "❌"
            print(f"  {status} {result.platform.upper()}: {result.device_name}")
            if not result.success and result.errors:
                for error in result.errors:
                    print(f"    - {error}")
        
        print(f"\n📸 Screenshots saved: {len([r for r in self.test_results if r.screenshot_path])}")

# Convenience functions
async def test_collaborative_ui_mobile():
    """Test the Collaborative UI Design App on mobile devices"""
    tester = UniversalMobileTester()
    results = await tester.test_all_platforms("http://localhost:3000")
    tester.print_test_summary()
    return results

async def test_any_web_app_mobile(url: str):
    """Test any web app on mobile devices"""
    tester = UniversalMobileTester()
    results = await tester.test_all_platforms(url)
    tester.print_test_summary()
    return results

# CLI interface
async def main():
    """Command line interface for mobile testing"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python universal-mobile-testing.py <url>")
        print("Example: python universal-mobile-testing.py http://localhost:3000")
        sys.exit(1)
    
    url = sys.argv[1]
    await test_any_web_app_mobile(url)

if __name__ == "__main__":
    asyncio.run(main())
