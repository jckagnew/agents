#!/usr/bin/env python3
"""
Conservative Mobile Testing - Safe, efficient testing that won't stress your Mac
"""

import asyncio
import subprocess
import json
import time
from browser_verification import BrowserVerifier

async def test_conservative_mobile():
    """Test mobile with conservative device selection - safe for your Mac"""
    print("🛡️  Conservative Mobile Testing (Mac-Safe)")
    print("=" * 50)
    
    # Test only 3 key devices to avoid system overload
    test_devices = [
        # Android - one phone
        {"platform": "android", "name": "Android Phone", "viewport": {"width": 360, "height": 640}},
        # iOS - one iPhone and one iPad
        {"platform": "ios", "name": "iPhone", "viewport": {"width": 375, "height": 667}},
        {"platform": "ios", "name": "iPad", "viewport": {"width": 768, "height": 1024}},
    ]
    
    url = "http://localhost:3000"
    results = []
    
    for i, device in enumerate(test_devices, 1):
        print(f"\n🧪 Test {i}/3: {device['platform'].upper()} - {device['name']}")
        print(f"   Viewport: {device['viewport']['width']}x{device['viewport']['height']}")
        
        async with BrowserVerifier(headless=True) as verifier:
            # Set mobile viewport
            await verifier.page.set_viewport_size(device['viewport'])
            
            # Set appropriate user agent
            if device['platform'] == 'android':
                await verifier.page.set_extra_http_headers({
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36'
                })
            else:  # iOS
                await verifier.page.set_extra_http_headers({
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
                })
            
            try:
                # Navigate to app
                print("   📱 Loading app...")
                await verifier.page.goto(url, timeout=30000)
                await verifier.page.wait_for_selector('#root', timeout=10000)
                
                # Test mobile responsiveness
                print("   🔍 Testing responsiveness...")
                content_width = await verifier.page.evaluate('document.body.scrollWidth')
                viewport_width = device['viewport']['width']
                is_responsive = content_width <= viewport_width + 100  # Allow some margin
                
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
                
                # Test toolbar buttons
                print("   🛠️  Testing toolbar...")
                toolbar_working = False
                toolbar_buttons = await verifier.page.query_selector_all('button:has-text("Preview"), button:has-text("Save")')
                if toolbar_buttons:
                    await toolbar_buttons[0].click()
                    toolbar_working = True
                
                # Take screenshot
                screenshot_path = f"mobile_test_{device['platform']}_{device['name'].lower().replace(' ', '_')}.png"
                await verifier.page.screenshot(path=screenshot_path)
                print(f"   📸 Screenshot: {screenshot_path}")
                
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
                
                results.append({
                    'platform': device['platform'],
                    'device': device['name'],
                    'success': success,
                    'responsive': is_responsive,
                    'touch_elements': len(touch_elements),
                    'search_working': search_working,
                    'filters_working': filters_working,
                    'toolbar_working': toolbar_working,
                    'errors': errors,
                    'screenshot': screenshot_path
                })
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:100]}")
                results.append({
                    'platform': device['platform'],
                    'device': device['name'],
                    'success': False,
                    'error': str(e)
                })
        
        # Small delay between tests to be gentle on the system
        if i < len(test_devices):
            print("   ⏳ Waiting 2 seconds before next test...")
            await asyncio.sleep(2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 CONSERVATIVE MOBILE TESTING SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r.get('success', False))
    
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    print(f"Success Rate: {(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
    
    print("\n📱 Detailed Results:")
    for result in results:
        platform = result['platform'].upper()
        device = result['device']
        success = result.get('success', False)
        status = "✅" if success else "❌"
        
        print(f"\n{status} {platform}: {device}")
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
    
    print(f"\n📸 Screenshots saved: {len([r for r in results if 'screenshot' in r])}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    phone_issues = [r for r in results if r['platform'] in ['android', 'ios'] and 'iPhone' in r.get('device', '') and not r.get('success', False)]
    if phone_issues:
        print("   📱 Mobile phones need responsiveness improvements")
        print("   💻 Consider adding mobile-specific CSS breakpoints")
        print("   📐 Test with smaller viewport widths (320px-375px)")
    
    tablet_working = [r for r in results if 'iPad' in r.get('device', '') and r.get('success', False)]
    if tablet_working:
        print("   ✅ Tablets are working well - good baseline!")
    
    return results

if __name__ == "__main__":
    asyncio.run(test_conservative_mobile())
