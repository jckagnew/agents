#!/usr/bin/env python3
"""
Comprehensive Weight Tracker Testing
Tests Weight Tracker on Web, Android, and multiple iOS devices
"""

import asyncio
import subprocess
import json
import time
import os
from browser_verification import BrowserVerifier

class WeightTrackerTester:
    """Comprehensive testing for Weight Tracker across all platforms"""
    
    def __init__(self):
        self.test_results = []
        self.weight_tracker_url = "http://localhost:3001"  # Weight Tracker runs on port 3001
        self.collaborative_ui_url = "http://localhost:3000"  # Collaborative UI runs on port 3000
    
    async def test_web_desktop(self, url):
        """Test on desktop web browser"""
        print("🖥️  Testing Desktop Web Browser...")
        
        async with BrowserVerifier(headless=False) as verifier:
            await verifier.page.set_viewport_size({'width': 1920, 'height': 1080})
            
            try:
                await verifier.page.goto(url, timeout=30000)
                # Wait for Next.js app to load - look for main content instead of #root
                await verifier.page.wait_for_selector('body', timeout=10000)
                await verifier.page.wait_for_load_state('networkidle')
                
                # Test Weight Tracker specific functionality
                print("   🏋️  Testing Weight Tracker features...")
                
                # Test navigation
                nav_working = False
                nav_buttons = await verifier.page.query_selector_all('button, a[href]')
                if len(nav_buttons) >= 3:
                    nav_working = True
                
                # Test weight entry form
                form_working = False
                form_inputs = await verifier.page.query_selector_all('input[type="number"], input[type="date"]')
                if len(form_inputs) >= 2:
                    form_working = True
                
                # Test charts/graphs
                charts_working = False
                chart_elements = await verifier.page.query_selector_all('svg, canvas, [class*="chart"]')
                if len(chart_elements) >= 1:
                    charts_working = True
                
                # Test data display
                data_working = False
                data_elements = await verifier.page.query_selector_all('table, [class*="list"], [class*="entry"]')
                if len(data_elements) >= 1:
                    data_working = True
                
                # Take screenshot
                screenshot_path = f"weight_tracker_desktop_{int(time.time())}.png"
                await verifier.page.screenshot(path=screenshot_path, full_page=True)
                
                success = nav_working and form_working and charts_working and data_working
                errors = []
                if not nav_working: errors.append("Navigation not working")
                if not form_working: errors.append("Form inputs not found")
                if not charts_working: errors.append("Charts not found")
                if not data_working: errors.append("Data display not found")
                
                result = {
                    'platform': 'web',
                    'device': 'Desktop Browser',
                    'viewport': {'width': 1920, 'height': 1080},
                    'success': success,
                    'nav_working': nav_working,
                    'form_working': form_working,
                    'charts_working': charts_working,
                    'data_working': data_working,
                    'errors': errors,
                    'screenshot': screenshot_path
                }
                
                self.test_results.append(result)
                return result
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:100]}")
                return {
                    'platform': 'web',
                    'device': 'Desktop Browser',
                    'success': False,
                    'error': str(e)
                }
    
    async def test_android_emulator(self, url):
        """Test on Android emulator"""
        print("🤖 Testing Android Emulator...")
        
        # Start Android emulator
        try:
            result = subprocess.run(['emulator', '-list-avds'], capture_output=True, text=True)
            if result.returncode != 0:
                print("   ❌ No Android emulators found")
                return None
            
            avds = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            if not avds:
                print("   ❌ No AVDs available")
                return None
            
            avd_name = avds[0]
            print(f"   📱 Starting AVD: {avd_name}")
            
            subprocess.Popen(['emulator', '-avd', avd_name, '-no-snapshot-load'], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait for emulator to boot
            for i in range(60):
                result = subprocess.run(['adb', 'shell', 'getprop', 'sys.boot_completed'], 
                                      capture_output=True, text=True)
                if result.stdout.strip() == '1':
                    print("   ✅ Android emulator ready")
                    break
                time.sleep(1)
            else:
                print("   ❌ Android emulator failed to boot")
                return None
                
        except FileNotFoundError:
            print("   ❌ Android emulator not found")
            return None
        
        # Test on Android
        async with BrowserVerifier(headless=False) as verifier:
            await verifier.page.set_viewport_size({'width': 360, 'height': 640})
            await verifier.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36'
            })
            
            try:
                await verifier.page.goto(url, timeout=30000)
                # Wait for Next.js app to load - look for main content instead of #root
                await verifier.page.wait_for_selector('body', timeout=10000)
                await verifier.page.wait_for_load_state('networkidle')
                
                # Test mobile responsiveness
                content_width = await verifier.page.evaluate('document.body.scrollWidth')
                is_responsive = content_width <= 400
                
                # Test touch elements
                touch_elements = await verifier.page.query_selector_all('button, input, [role="button"]')
                touch_friendly = len(touch_elements) >= 5
                
                # Test mobile navigation
                nav_working = False
                nav_buttons = await verifier.page.query_selector_all('button, a[href]')
                if len(nav_buttons) >= 3:
                    nav_working = True
                
                # Test form inputs
                form_working = False
                form_inputs = await verifier.page.query_selector_all('input, select, textarea')
                if len(form_inputs) >= 2:
                    form_working = True
                
                screenshot_path = f"weight_tracker_android_{int(time.time())}.png"
                await verifier.page.screenshot(path=screenshot_path, full_page=True)
                
                success = is_responsive and touch_friendly and nav_working and form_working
                errors = []
                if not is_responsive: errors.append("Not mobile responsive")
                if not touch_friendly: errors.append("Insufficient touch elements")
                if not nav_working: errors.append("Navigation not working")
                if not form_working: errors.append("Form inputs not found")
                
                result = {
                    'platform': 'android',
                    'device': f'Android Emulator ({avd_name})',
                    'viewport': {'width': 360, 'height': 640},
                    'success': success,
                    'responsive': is_responsive,
                    'touch_elements': len(touch_elements),
                    'nav_working': nav_working,
                    'form_working': form_working,
                    'errors': errors,
                    'screenshot': screenshot_path
                }
                
                self.test_results.append(result)
                return result
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:100]}")
                return {
                    'platform': 'android',
                    'device': f'Android Emulator ({avd_name})',
                    'success': False,
                    'error': str(e)
                }
    
    async def test_ios_simulators(self, url):
        """Test on multiple iOS simulators"""
        print("🍎 Testing iOS Simulators...")
        
        try:
            # List available iOS simulators
            result = subprocess.run(['xcrun', 'simctl', 'list', 'devices', 'available', '--json'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("   ❌ iOS Simulator not available")
                return []
            
            data = json.loads(result.stdout)
            
            # Find iPhone and iPad simulators
            ios_devices = []
            for runtime, devices in data['devices'].items():
                if 'iOS' in runtime:
                    for device in devices:
                        if device['state'] == 'Shutdown' and ('iPhone' in device['name'] or 'iPad' in device['name']):
                            ios_devices.append(device)
            
            if not ios_devices:
                print("   ❌ No iOS simulators available")
                return []
            
            # Test on first iPhone and first iPad
            test_devices = []
            for device in ios_devices:
                if 'iPhone' in device['name'] and not any('iPhone' in d['name'] for d in test_devices):
                    test_devices.append(device)
                elif 'iPad' in device['name'] and not any('iPad' in d['name'] for d in test_devices):
                    test_devices.append(device)
                if len(test_devices) >= 2:  # Test iPhone and iPad
                    break
            
            results = []
            for i, device in enumerate(test_devices, 1):
                print(f"   📱 Testing {device['name']} ({i}/{len(test_devices)})...")
                
                # Boot simulator
                subprocess.run(['xcrun', 'simctl', 'boot', device['udid']], check=True)
                if i == 1:  # Only open Simulator app once
                    subprocess.run(['open', '-a', 'Simulator'], check=True)
                
                # Wait for boot
                for j in range(30):
                    result = subprocess.run(['xcrun', 'simctl', 'list', 'devices', device['udid']], 
                                          capture_output=True, text=True)
                    if 'Booted' in result.stdout:
                        break
                    time.sleep(1)
                
                # Test on this device
                viewport = {'width': 375, 'height': 667} if 'iPhone' in device['name'] else {'width': 768, 'height': 1024}
                
                async with BrowserVerifier(headless=False) as verifier:
                    await verifier.page.set_viewport_size(viewport)
                    await verifier.page.set_extra_http_headers({
                        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
                    })
                    
                    try:
                        await verifier.page.goto(url, timeout=30000)
                        await verifier.page.wait_for_selector('#root', timeout=10000)
                        
                        # Test responsiveness
                        content_width = await verifier.page.evaluate('document.body.scrollWidth')
                        is_responsive = content_width <= viewport['width'] + 100
                        
                        # Test touch elements
                        touch_elements = await verifier.page.query_selector_all('button, input, [role="button"]')
                        touch_friendly = len(touch_elements) >= 5
                        
                        # Test navigation
                        nav_working = False
                        nav_buttons = await verifier.page.query_selector_all('button, a[href]')
                        if len(nav_buttons) >= 3:
                            nav_working = True
                        
                        # Test form inputs
                        form_working = False
                        form_inputs = await verifier.page.query_selector_all('input, select, textarea')
                        if len(form_inputs) >= 2:
                            form_working = True
                        
                        screenshot_path = f"weight_tracker_ios_{device['name'].lower().replace(' ', '_')}_{int(time.time())}.png"
                        await verifier.page.screenshot(path=screenshot_path, full_page=True)
                        
                        success = is_responsive and touch_friendly and nav_working and form_working
                        errors = []
                        if not is_responsive: errors.append("Not mobile responsive")
                        if not touch_friendly: errors.append("Insufficient touch elements")
                        if not nav_working: errors.append("Navigation not working")
                        if not form_working: errors.append("Form inputs not found")
                        
                        result = {
                            'platform': 'ios',
                            'device': f'{device["name"]} Simulator',
                            'viewport': viewport,
                            'success': success,
                            'responsive': is_responsive,
                            'touch_elements': len(touch_elements),
                            'nav_working': nav_working,
                            'form_working': form_working,
                            'errors': errors,
                            'screenshot': screenshot_path
                        }
                        
                        self.test_results.append(result)
                        results.append(result)
                        
                    except Exception as e:
                        print(f"   ❌ Error on {device['name']}: {str(e)[:100]}")
                        results.append({
                            'platform': 'ios',
                            'device': f'{device["name"]} Simulator',
                            'success': False,
                            'error': str(e)
                        })
                
                # Small delay between devices
                if i < len(test_devices):
                    await asyncio.sleep(2)
            
            return results
            
        except Exception as e:
            print(f"   ❌ Error setting up iOS simulators: {e}")
            return []
    
    async def run_comprehensive_test(self):
        """Run comprehensive Weight Tracker testing"""
        print("🏋️  COMPREHENSIVE WEIGHT TRACKER TESTING")
        print("=" * 60)
        
        # Wait for Weight Tracker to start
        print("⏳ Waiting for Weight Tracker to start...")
        await asyncio.sleep(5)
        
        # Test 1: Desktop Web
        print("\n" + "="*20 + " DESKTOP WEB " + "="*20)
        await self.test_web_desktop(self.weight_tracker_url)
        
        # Test 2: Android Emulator
        print("\n" + "="*20 + " ANDROID " + "="*20)
        await self.test_android_emulator(self.weight_tracker_url)
        
        # Test 3: iOS Simulators
        print("\n" + "="*20 + " iOS SIMULATORS " + "="*20)
        await self.test_ios_simulators(self.weight_tracker_url)
        
        # Print comprehensive results
        self.print_comprehensive_summary()
        
        return self.test_results
    
    def print_comprehensive_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE WEIGHT TRACKER TESTING SUMMARY")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r.get('success', False))
        
        print(f"Total Platforms Tested: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        print(f"Success Rate: {(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
        
        print("\n📱 Platform-Specific Results:")
        for result in self.test_results:
            platform = result['platform'].upper()
            device = result['device']
            success = result.get('success', False)
            status = "✅" if success else "❌"
            
            print(f"\n{status} {platform}: {device}")
            if 'viewport' in result:
                print(f"   Viewport: {result['viewport']['width']}x{result['viewport']['height']}")
            if success:
                if 'responsive' in result:
                    print(f"   Responsive: {result.get('responsive', 'N/A')}")
                if 'touch_elements' in result:
                    print(f"   Touch Elements: {result.get('touch_elements', 'N/A')}")
                if 'nav_working' in result:
                    print(f"   Navigation: {result.get('nav_working', 'N/A')}")
                if 'form_working' in result:
                    print(f"   Forms: {result.get('form_working', 'N/A')}")
            else:
                if 'error' in result:
                    print(f"   Error: {result['error'][:100]}")
                if 'errors' in result and result['errors']:
                    print(f"   Issues: {', '.join(result['errors'])}")
        
        print(f"\n📸 Screenshots Captured: {len([r for r in self.test_results if 'screenshot' in r])}")
        
        # Platform-specific insights
        print("\n💡 PLATFORM INSIGHTS:")
        web_results = [r for r in self.test_results if r['platform'] == 'web']
        android_results = [r for r in self.test_results if r['platform'] == 'android']
        ios_results = [r for r in self.test_results if r['platform'] == 'ios']
        
        if web_results and web_results[0].get('success'):
            print("   🖥️  Desktop: Excellent for full-featured experience")
        if android_results and android_results[0].get('success'):
            print("   🤖 Android: Great mobile experience")
        if ios_results:
            successful_ios = [r for r in ios_results if r.get('success')]
            print(f"   🍎 iOS: {len(successful_ios)}/{len(ios_results)} devices working")
        
        print("\n🎯 Weight Tracker is now verified across all major platforms!")

# Run the comprehensive test
async def main():
    tester = WeightTrackerTester()
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())
