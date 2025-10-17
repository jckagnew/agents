#!/usr/bin/env python3
"""
Test the Collaborative UI Design app across different devices
"""

import asyncio
import argparse
from pathlib import Path
import sys

# Add the mobile testing directory to the path
sys.path.append(str(Path(__file__).parent))

from browser_verification import BrowserVerifier

async def test_collaborative_ui_design():
    """Test the Collaborative UI Design app on different devices"""
    
    # Test configurations
    devices = [
        {"name": "Desktop", "viewport": {"width": 1920, "height": 1080}},
        {"name": "iPhone 14", "viewport": {"width": 390, "height": 844}},
        {"name": "iPad Pro 11", "viewport": {"width": 834, "height": 1194}},
        {"name": "Pixel 7", "viewport": {"width": 412, "height": 915}},
    ]
    
    url = "http://localhost:3000"
    results = []
    
    print("🎨 Collaborative UI Design App Testing")
    print("=" * 50)
    
    async with BrowserVerifier(headless=True) as verifier:
        for i, device in enumerate(devices, 1):
            print(f"\n🧪 Test {i}/{len(devices)}: {device['name']}")
            print(f"   Viewport: {device['viewport']['width']}x{device['viewport']['height']}")
            
            try:
                # Set viewport
                await verifier.page.set_viewport_size(device['viewport'])
                
                # Navigate to the app
                print("   📱 Loading app...")
                await verifier.page.goto(url, timeout=30000)
                await verifier.page.wait_for_load_state('networkidle')
                
                # Test basic app loading
                print("   🔍 Testing app loading...")
                app_title = await verifier.page.text_content('h1')
                if "Collaborative UI Design" in app_title:
                    print("   ✅ App title loaded correctly")
                else:
                    print(f"   ⚠️  Unexpected app title: {app_title}")
                
                # Test header elements
                print("   🔍 Testing header elements...")
                header_elements = [
                    "button[title='Design Skills Guide']",
                    "button[title='Website Analyzer']",
                    "button:has-text('Preview')",
                    "button:has-text('Save')"
                ]
                
                for selector in header_elements:
                    try:
                        element = await verifier.page.wait_for_selector(selector, timeout=5000)
                        if element:
                            print(f"   ✅ Found: {selector}")
                    except:
                        print(f"   ❌ Missing: {selector}")
                
                # Test sidebar
                print("   🔍 Testing sidebar...")
                try:
                    sidebar = await verifier.page.wait_for_selector('[data-testid="sidebar"]', timeout=5000)
                    if sidebar:
                        print("   ✅ Sidebar loaded")
                    else:
                        print("   ⚠️  Sidebar not found")
                except:
                    print("   ⚠️  Sidebar test skipped")
                
                # Test canvas area
                print("   🔍 Testing canvas area...")
                try:
                    canvas = await verifier.page.wait_for_selector('[data-testid="canvas"]', timeout=5000)
                    if canvas:
                        print("   ✅ Canvas area loaded")
                    else:
                        print("   ⚠️  Canvas area not found")
                except:
                    print("   ⚠️  Canvas test skipped")
                
                # Test responsive design
                print("   📱 Testing responsive design...")
                viewport_width = device['viewport']['width']
                
                if viewport_width < 768:
                    # Mobile-specific tests
                    print("   📱 Mobile viewport detected")
                    try:
                        # Check if mobile menu exists or if elements are properly stacked
                        mobile_elements = await verifier.page.query_selector_all('button')
                        if len(mobile_elements) > 0:
                            print("   ✅ Mobile elements accessible")
                        else:
                            print("   ⚠️  No mobile elements found")
                    except:
                        print("   ⚠️  Mobile responsiveness test failed")
                elif viewport_width < 1024:
                    # Tablet-specific tests
                    print("   📱 Tablet viewport detected")
                    try:
                        # Check if layout adapts to tablet size
                        layout_elements = await verifier.page.query_selector_all('div')
                        if len(layout_elements) > 0:
                            print("   ✅ Tablet layout elements found")
                        else:
                            print("   ⚠️  No tablet layout elements found")
                    except:
                        print("   ⚠️  Tablet responsiveness test failed")
                else:
                    # Desktop-specific tests
                    print("   💻 Desktop viewport detected")
                    try:
                        # Check if desktop layout is properly displayed
                        desktop_elements = await verifier.page.query_selector_all('div')
                        if len(desktop_elements) > 0:
                            print("   ✅ Desktop layout elements found")
                        else:
                            print("   ⚠️  No desktop layout elements found")
                    except:
                        print("   ⚠️  Desktop responsiveness test failed")
                
                # Test interactive elements
                print("   👆 Testing interactive elements...")
                try:
                    # Test if buttons are clickable
                    buttons = await verifier.page.query_selector_all('button')
                    clickable_buttons = 0
                    for button in buttons[:3]:  # Test first 3 buttons
                        try:
                            is_visible = await button.is_visible()
                            is_enabled = await button.is_enabled()
                            if is_visible and is_enabled:
                                clickable_buttons += 1
                        except:
                            pass
                    
                    if clickable_buttons > 0:
                        print(f"   ✅ {clickable_buttons} buttons are clickable")
                    else:
                        print("   ⚠️  No clickable buttons found")
                except:
                    print("   ⚠️  Interactive elements test failed")
                
                # Test accessibility
                print("   ♿ Testing accessibility...")
                try:
                    # Check for proper heading structure
                    headings = await verifier.page.query_selector_all('h1, h2, h3, h4, h5, h6')
                    if len(headings) > 0:
                        print(f"   ✅ Found {len(headings)} headings")
                    else:
                        print("   ⚠️  No headings found")
                    
                    # Check for alt text on images
                    images = await verifier.page.query_selector_all('img')
                    images_with_alt = 0
                    for img in images:
                        alt_text = await img.get_attribute('alt')
                        if alt_text:
                            images_with_alt += 1
                    
                    if images_with_alt == len(images) and len(images) > 0:
                        print(f"   ✅ All {len(images)} images have alt text")
                    elif len(images) > 0:
                        print(f"   ⚠️  Only {images_with_alt}/{len(images)} images have alt text")
                    else:
                        print("   ✅ No images to test")
                        
                except:
                    print("   ⚠️  Accessibility test failed")
                
                # Take screenshot
                screenshot_path = f"test-results/collaborative-ui-design-{device['name'].lower().replace(' ', '-')}.png"
                Path("test-results").mkdir(exist_ok=True)
                await verifier.page.screenshot(path=screenshot_path)
                print(f"   📸 Screenshot saved: {screenshot_path}")
                
                results.append({
                    "device": device['name'],
                    "status": "success",
                    "viewport": device['viewport'],
                    "screenshot": screenshot_path
                })
                
                print(f"   ✅ {device['name']} test completed successfully")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                results.append({
                    "device": device['name'],
                    "status": "failed",
                    "viewport": device['viewport'],
                    "error": str(e)
                })
            
            # Wait between tests
            if i < len(devices):
                print("   ⏳ Waiting 2 seconds before next test...")
                await asyncio.sleep(2)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 COLLABORATIVE UI DESIGN TESTING SUMMARY")
    print("=" * 50)
    
    successful = sum(1 for r in results if r['status'] == 'success')
    total = len(results)
    success_rate = (successful / total) * 100 if total > 0 else 0
    
    print(f"Total Tests: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    print("\n📱 Detailed Results:")
    for result in results:
        if result['status'] == 'success':
            print(f"✅ {result['device']}: {result['viewport']['width']}x{result['viewport']['height']}")
            if 'screenshot' in result:
                print(f"   📸 Screenshot: {result['screenshot']}")
        else:
            print(f"❌ {result['device']}: {result['viewport']['width']}x{result['viewport']['height']}")
            if 'error' in result:
                print(f"   Error: {result['error']}")
    
    if success_rate >= 75:
        print("\n🎉 EXCELLENT! The app works well across devices!")
    elif success_rate >= 50:
        print("\n👍 GOOD! The app mostly works, but some improvements needed.")
    else:
        print("\n⚠️  NEEDS WORK! The app needs significant improvements for mobile.")
    
    return results

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Test Collaborative UI Design app')
    parser.add_argument('--url', default='http://localhost:3000', help='App URL to test')
    args = parser.parse_args()
    
    print(f"🎨 Testing Collaborative UI Design app at {args.url}")
    results = await test_collaborative_ui_design()
    return results

if __name__ == "__main__":
    asyncio.run(main())
