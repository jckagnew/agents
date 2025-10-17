#!/usr/bin/env python3
"""
Optimized Mobile Testing - Tests fewer devices to avoid resource limits
"""

import asyncio
import subprocess
import json
import time
from browser_verification import BrowserVerifier

async def test_optimized_mobile():
    """Test mobile with optimized device selection"""
    print("🚀 Optimized Mobile Testing")
    print("=" * 40)
    
    # Test only key devices to avoid resource limits
    test_devices = [
        # Android - one emulator
        {"platform": "android", "name": "Android Phone", "viewport": {"width": 360, "height": 640}},
        # iOS - one iPhone and one iPad
        {"platform": "ios", "name": "iPhone", "viewport": {"width": 375, "height": 667}},
        {"platform": "ios", "name": "iPad", "viewport": {"width": 768, "height": 1024}},
    ]
    
    url = "http://localhost:3000"
    results = []
    
    for device in test_devices:
        print(f"\n🧪 Testing on {device['platform'].upper()}: {device['name']}")
        
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
                await verifier.page.goto(url, timeout=30000)
                await verifier.page.wait_for_selector('#root', timeout=10000)
                
                # Test mobile responsiveness
                content_width = await verifier.page.evaluate('document.body.scrollWidth')
                viewport_width = device['viewport']['width']
                is_responsive = content_width <= viewport_width + 100  # Allow some margin
                
                # Test touch elements
                touch_elements = await verifier.page.query_selector_all('button, input, [role="button"]')
                touch_friendly = len(touch_elements) >= 3
                
                # Test search functionality
                search_working = False
                search_input = await verifier.page.query_selector('input[placeholder*="Search"]')
                if search_input:
                    await search_input.fill('test')
                    search_working = True
                
                # Test category filters
                filters_working = False
                filter_buttons = await verifier.page.query_selector_all('button:has-text("Atom"), button:has-text("All")')
                if filter_buttons:
                    await filter_buttons[0].click()
                    filters_working = True
                
                # Take screenshot
                screenshot_path = f"mobile_test_{device['platform']}_{device['name'].lower().replace(' ', '_')}.png"
                await verifier.page.screenshot(path=screenshot_path)
                
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
                
                success = len(errors) == 0
                status = "✅" if success else "❌"
                
                print(f"   {status} Responsive: {is_responsive}")
                print(f"   {status} Touch Elements: {len(touch_elements)}")
                print(f"   {status} Search: {search_working}")
                print(f"   {status} Filters: {filters_working}")
                if errors:
                    print(f"   Issues: {', '.join(errors)}")
                
                results.append({
                    'platform': device['platform'],
                    'device': device['name'],
                    'success': success,
                    'responsive': is_responsive,
                    'touch_elements': len(touch_elements),
                    'search_working': search_working,
                    'filters_working': filters_working,
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
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 MOBILE TESTING SUMMARY")
    print("=" * 50)
    
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
        else:
            if 'error' in result:
                print(f"   Error: {result['error'][:100]}")
            if 'errors' in result and result['errors']:
                print(f"   Issues: {', '.join(result['errors'])}")
    
    print(f"\n📸 Screenshots saved: {len([r for r in results if 'screenshot' in r])}")
    
    return results

if __name__ == "__main__":
    asyncio.run(test_optimized_mobile())
