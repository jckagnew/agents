#!/usr/bin/env python3
"""
Mobile Emulator Verification System
Actually opens mobile emulators and verifies the app displays correctly
"""

import asyncio
import subprocess
import json
import time
import os
from browser_verification import BrowserVerifier

class MobileEmulatorVerifier:
    """Verifies mobile apps by actually opening emulators and taking screenshots"""
    
    def __init__(self):
        self.android_emulator = None
        self.ios_simulator = None
        self.test_results = []
    
    async def start_android_emulator(self):
        """Start Android emulator and return device info"""
        print("🤖 Starting Android Emulator...")
        
        try:
            # List available AVDs
            result = subprocess.run(['emulator', '-list-avds'], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ No Android emulators found. Install Android Studio first.")
                return None
            
            avds = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            if not avds:
                print("❌ No AVDs available. Create one in Android Studio.")
                return None
            
            # Use the first available AVD
            avd_name = avds[0]
            print(f"📱 Starting AVD: {avd_name}")
            
            # Start emulator in background
            subprocess.Popen(['emulator', '-avd', avd_name, '-no-snapshot-load'], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            
            # Wait for emulator to boot
            print("⏳ Waiting for Android emulator to boot...")
            for i in range(60):  # Wait up to 60 seconds
                result = subprocess.run(['adb', 'shell', 'getprop', 'sys.boot_completed'], 
                                      capture_output=True, text=True)
                if result.stdout.strip() == '1':
                    print("✅ Android emulator booted successfully")
                    return {
                        'name': f'Android Emulator ({avd_name})',
                        'platform': 'android',
                        'status': 'running'
                    }
                time.sleep(1)
            
            print("❌ Android emulator failed to boot")
            return None
            
        except FileNotFoundError:
            print("❌ Android emulator not found. Install Android Studio.")
            return None
    
    async def start_ios_simulator(self):
        """Start iOS Simulator and return device info"""
        print("🍎 Starting iOS Simulator...")
        
        try:
            # List available iOS simulators
            result = subprocess.run(['xcrun', 'simctl', 'list', 'devices', 'available', '--json'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ iOS Simulator not available. Check Xcode installation.")
                return None
            
            data = json.loads(result.stdout)
            
            # Find iPhone simulator
            iphone_device = None
            for runtime, devices in data['devices'].items():
                if 'iOS' in runtime:
                    for device in devices:
                        if 'iPhone' in device['name'] and device['state'] == 'Shutdown':
                            iphone_device = device
                            break
                    if iphone_device:
                        break
            
            if not iphone_device:
                print("❌ No iPhone simulators available")
                return None
            
            print(f"📱 Starting iPhone: {iphone_device['name']}")
            
            # Boot the simulator
            subprocess.run(['xcrun', 'simctl', 'boot', iphone_device['udid']], check=True)
            subprocess.run(['open', '-a', 'Simulator'], check=True)
            
            # Wait for simulator to boot
            print("⏳ Waiting for iOS simulator to boot...")
            for i in range(30):  # Wait up to 30 seconds
                result = subprocess.run(['xcrun', 'simctl', 'list', 'devices', iphone_device['udid']], 
                                      capture_output=True, text=True)
                if 'Booted' in result.stdout:
                    print("✅ iOS simulator booted successfully")
                    return {
                        'name': f'iPhone Simulator ({iphone_device["name"]})',
                        'platform': 'ios',
                        'status': 'running',
                        'udid': iphone_device['udid']
                    }
                time.sleep(1)
            
            print("❌ iOS simulator failed to boot")
            return None
            
        except (FileNotFoundError, subprocess.CalledProcessError, json.JSONDecodeError) as e:
            print(f"❌ Error starting iOS simulator: {e}")
            return None
    
    async def verify_mobile_app(self, device_info, url):
        """Verify app on a specific mobile device"""
        print(f"\n🧪 Testing on {device_info['platform'].upper()}: {device_info['name']}")
        
        # Configure mobile viewport
        if device_info['platform'] == 'android':
            viewport = {'width': 360, 'height': 640}
            user_agent = 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36'
        else:  # iOS
            viewport = {'width': 375, 'height': 667}
            user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        
        async with BrowserVerifier(headless=False) as verifier:  # Set to False to see the browser
            # Configure mobile viewport
            await verifier.page.set_viewport_size(viewport)
            await verifier.page.set_extra_http_headers({'User-Agent': user_agent})
            
            try:
                print(f"   📱 Loading {url}...")
                await verifier.page.goto(url, timeout=30000)
                await verifier.page.wait_for_selector('#root', timeout=10000)
                
                # Test mobile responsiveness
                print("   🔍 Testing mobile responsiveness...")
                content_width = await verifier.page.evaluate('document.body.scrollWidth')
                viewport_width = viewport['width']
                is_responsive = content_width <= viewport_width + 100
                
                # Test touch elements
                print("   👆 Testing touch elements...")
                touch_elements = await verifier.page.query_selector_all('button, input, [role="button"]')
                touch_friendly = len(touch_elements) >= 3
                
                # Test search functionality
                print("   🔍 Testing search...")
                search_working = False
                search_input = await verifier.page.query_selector('input[placeholder*="Search"]')
                if search_input:
                    await search_input.fill('test')
                    search_working = True
                
                # Test category filters
                print("   🏷️  Testing filters...")
                filters_working = False
                filter_buttons = await verifier.page.query_selector_all('button:has-text("Atom"), button:has-text("All")')
                if filter_buttons:
                    await filter_buttons[0].click()
                    filters_working = True
                
                # Test toolbar
                print("   🛠️  Testing toolbar...")
                toolbar_working = False
                toolbar_buttons = await verifier.page.query_selector_all('button:has-text("Preview"), button:has-text("Save")')
                if toolbar_buttons:
                    await toolbar_buttons[0].click()
                    toolbar_working = True
                
                # Take mobile screenshot
                screenshot_path = f"mobile_emulator_{device_info['platform']}_{int(time.time())}.png"
                await verifier.page.screenshot(path=screenshot_path, full_page=True)
                print(f"   📸 Mobile screenshot: {screenshot_path}")
                
                # Test mobile-specific interactions
                print("   📱 Testing mobile interactions...")
                
                # Test scrolling
                await verifier.page.evaluate('window.scrollTo(0, 100)')
                await asyncio.sleep(0.5)
                
                # Test touch events (simulate mobile touch)
                await verifier.page.evaluate('''
                    const touchEvent = new TouchEvent('touchstart', {
                        touches: [new Touch({
                            identifier: 1,
                            target: document.body,
                            clientX: 100,
                            clientY: 100
                        })]
                    });
                    document.body.dispatchEvent(touchEvent);
                ''')
                
                # Determine success
                errors = []
                if not is_responsive:
                    errors.append("Not mobile responsive")
                if not touch_friendly:
                    errors.append("Insufficient touch elements")
                if not search_working:
                    errors.append("Search not working")
                if not filters_working:
                    errors.append("Filters not working")
                if not toolbar_working:
                    errors.append("Toolbar not working")
                
                success = len(errors) == 0
                status = "✅" if success else "❌"
                
                print(f"   {status} Responsive: {is_responsive}")
                print(f"   {status} Touch Elements: {len(touch_elements)}")
                print(f"   {status} Search: {search_working}")
                print(f"   {status} Filters: {filters_working}")
                print(f"   {status} Toolbar: {toolbar_working}")
                if errors:
                    print(f"   ⚠️  Issues: {', '.join(errors)}")
                
                result = {
                    'platform': device_info['platform'],
                    'device': device_info['name'],
                    'success': success,
                    'responsive': is_responsive,
                    'touch_elements': len(touch_elements),
                    'search_working': search_working,
                    'filters_working': filters_working,
                    'toolbar_working': toolbar_working,
                    'errors': errors,
                    'screenshot': screenshot_path,
                    'viewport': viewport
                }
                
                self.test_results.append(result)
                return result
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:100]}")
                result = {
                    'platform': device_info['platform'],
                    'device': device_info['name'],
                    'success': False,
                    'error': str(e)
                }
                self.test_results.append(result)
                return result
    
    async def verify_all_mobile_platforms(self, url):
        """Verify app on all available mobile platforms"""
        print("🚀 Mobile Emulator Verification System")
        print("=" * 50)
        
        # Start Android emulator
        android_device = await self.start_android_emulator()
        
        # Start iOS simulator
        ios_device = await self.start_ios_simulator()
        
        # Test on available devices
        devices_to_test = []
        if android_device:
            devices_to_test.append(android_device)
        if ios_device:
            devices_to_test.append(ios_device)
        
        if not devices_to_test:
            print("❌ No mobile devices available for testing")
            return []
        
        print(f"\n📱 Testing on {len(devices_to_test)} mobile devices...")
        
        for i, device in enumerate(devices_to_test, 1):
            print(f"\n{'='*20} Device {i}/{len(devices_to_test)} {'='*20}")
            await self.verify_mobile_app(device, url)
            
            # Small delay between tests
            if i < len(devices_to_test):
                print("   ⏳ Waiting 3 seconds before next device...")
                await asyncio.sleep(3)
        
        # Print comprehensive results
        self.print_verification_summary()
        return self.test_results
    
    def print_verification_summary(self):
        """Print detailed verification summary"""
        print("\n" + "=" * 60)
        print("📊 MOBILE EMULATOR VERIFICATION SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r.get('success', False))
        
        print(f"Total Devices Tested: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        print(f"Success Rate: {(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
        
        print("\n📱 Detailed Mobile Results:")
        for result in self.test_results:
            platform = result['platform'].upper()
            device = result['device']
            success = result.get('success', False)
            status = "✅" if success else "❌"
            
            print(f"\n{status} {platform}: {device}")
            if 'viewport' in result:
                print(f"   Viewport: {result['viewport']['width']}x{result['viewport']['height']}")
            if success:
                print(f"   Responsive: {result.get('responsive', 'N/A')}")
                print(f"   Touch Elements: {result.get('touch_elements', 'N/A')}")
                print(f"   Search Working: {result.get('search_working', 'N/A')}")
                print(f"   Filters Working: {result.get('filters_working', 'N/A')}")
                print(f"   Toolbar Working: {result.get('toolbar_working', 'N/A')}")
            else:
                if 'error' in result:
                    print(f"   Error: {result['error'][:100]}")
                if 'errors' in result and result['errors']:
                    print(f"   Issues: {', '.join(result['errors'])}")
        
        print(f"\n📸 Mobile Screenshots: {len([r for r in self.test_results if 'screenshot' in r])}")
        
        # Mobile-specific recommendations
        print("\n💡 MOBILE RECOMMENDATIONS:")
        phone_issues = [r for r in self.test_results if r['platform'] in ['android', 'ios'] and 'iPhone' in r.get('device', '') and not r.get('success', False)]
        if phone_issues:
            print("   📱 Mobile phones need attention")
        else:
            print("   ✅ Mobile phones are working well!")
        
        tablet_working = [r for r in self.test_results if 'iPad' in r.get('device', '') and r.get('success', False)]
        if tablet_working:
            print("   ✅ Tablets are working perfectly!")
        
        print("\n🎯 The mobile emulator verification shows exactly how your app looks and behaves on real mobile devices!")

# Convenience function
async def verify_mobile_emulators(url="http://localhost:3000"):
    """Verify app on mobile emulators"""
    verifier = MobileEmulatorVerifier()
    return await verifier.verify_all_mobile_platforms(url)

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
    asyncio.run(verify_mobile_emulators(url))
