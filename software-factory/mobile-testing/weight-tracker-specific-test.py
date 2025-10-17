#!/usr/bin/env python3
"""
Weight Tracker Specific Testing
Tests Weight Tracker with proper element detection
"""

import asyncio
import subprocess
import json
import time
from browser_verification import BrowserVerifier

async def test_weight_tracker_specific():
    """Test Weight Tracker with specific element detection"""
    print("🏋️  WEIGHT TRACKER SPECIFIC TESTING")
    print("=" * 50)
    
    url = "http://localhost:3001"
    results = []
    
    # Test configurations
    test_configs = [
        {
            'name': 'Desktop Web',
            'platform': 'web',
            'viewport': {'width': 1920, 'height': 1080},
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        },
        {
            'name': 'Android Phone',
            'platform': 'android',
            'viewport': {'width': 360, 'height': 640},
            'user_agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36'
        },
        {
            'name': 'iPhone',
            'platform': 'ios',
            'viewport': {'width': 375, 'height': 667},
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        },
        {
            'name': 'iPad',
            'platform': 'ios',
            'viewport': {'width': 768, 'height': 1024},
            'user_agent': 'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        }
    ]
    
    for i, config in enumerate(test_configs, 1):
        print(f"\n{'='*20} Test {i}/{len(test_configs)}: {config['name']} {'='*20}")
        
        async with BrowserVerifier(headless=False) as verifier:
            await verifier.page.set_viewport_size(config['viewport'])
            await verifier.page.set_extra_http_headers({'User-Agent': config['user_agent']})
            
            try:
                print(f"   📱 Loading Weight Tracker...")
                await verifier.page.goto(url, timeout=30000)
                await verifier.page.wait_for_selector('body', timeout=10000)
                await verifier.page.wait_for_load_state('networkidle')
                
                # Test Weight Tracker specific elements
                print("   🏋️  Testing Weight Tracker elements...")
                
                # Test for Weight Tracker title
                title_found = False
                title_elements = await verifier.page.query_selector_all('h1, h2, [class*="title"]')
                for element in title_elements:
                    text = await element.inner_text()
                    if 'Weight Tracker' in text or 'weight' in text.lower():
                        title_found = True
                        break
                
                # Test for weight display
                weight_display = False
                weight_elements = await verifier.page.query_selector_all('[class*="weight"], [class*="lbs"], [class*="kg"]')
                if len(weight_elements) > 0:
                    weight_display = True
                
                # Test for buttons (Log Entry, History, Analytics)
                buttons_found = False
                button_elements = await verifier.page.query_selector_all('button')
                button_texts = []
                for button in button_elements:
                    text = await button.inner_text()
                    button_texts.append(text)
                    if any(keyword in text.lower() for keyword in ['log', 'entry', 'history', 'analytics', 'track']):
                        buttons_found = True
                
                # Test for charts/graphs
                charts_found = False
                chart_elements = await verifier.page.query_selector_all('svg, canvas, [class*="chart"], [class*="graph"]')
                if len(chart_elements) > 0:
                    charts_found = True
                
                # Test for progress indicators
                progress_found = False
                progress_elements = await verifier.page.query_selector_all('[class*="progress"], [class*="bar"], [class*="goal"]')
                if len(progress_elements) > 0:
                    progress_found = True
                
                # Test for data cards/summary
                data_cards = False
                card_elements = await verifier.page.query_selector_all('[class*="card"], [class*="summary"], [class*="stats"]')
                if len(card_elements) > 0:
                    data_cards = True
                
                # Test mobile responsiveness
                content_width = await verifier.page.evaluate('document.body.scrollWidth')
                viewport_width = config['viewport']['width']
                is_responsive = content_width <= viewport_width + 100
                
                # Test touch elements
                touch_elements = await verifier.page.query_selector_all('button, input, [role="button"], a')
                touch_friendly = len(touch_elements) >= 5
                
                # Take screenshot
                screenshot_path = f"weight_tracker_{config['platform']}_{config['name'].lower().replace(' ', '_')}_{int(time.time())}.png"
                await verifier.page.screenshot(path=screenshot_path, full_page=True)
                print(f"   📸 Screenshot: {screenshot_path}")
                
                # Determine success
                errors = []
                if not title_found: errors.append("Weight Tracker title not found")
                if not weight_display: errors.append("Weight display not found")
                if not buttons_found: errors.append("Action buttons not found")
                if not charts_found: errors.append("Charts/graphs not found")
                if not progress_found: errors.append("Progress indicators not found")
                if not data_cards: errors.append("Data cards not found")
                if not is_responsive: errors.append("Not mobile responsive")
                if not touch_friendly: errors.append("Insufficient touch elements")
                
                success = len(errors) == 0
                status = "✅" if success else "❌"
                
                print(f"   {status} Title Found: {title_found}")
                print(f"   {status} Weight Display: {weight_display}")
                print(f"   {status} Buttons Found: {buttons_found} ({len(button_elements)} total)")
                print(f"   {status} Charts Found: {charts_found}")
                print(f"   {status} Progress Found: {progress_found}")
                print(f"   {status} Data Cards: {data_cards}")
                print(f"   {status} Responsive: {is_responsive}")
                print(f"   {status} Touch Elements: {len(touch_elements)}")
                
                if button_texts:
                    print(f"   📝 Button texts found: {button_texts[:5]}")  # Show first 5
                
                if errors:
                    print(f"   ⚠️  Issues: {', '.join(errors)}")
                
                result = {
                    'platform': config['platform'],
                    'device': config['name'],
                    'viewport': config['viewport'],
                    'success': success,
                    'title_found': title_found,
                    'weight_display': weight_display,
                    'buttons_found': buttons_found,
                    'button_count': len(button_elements),
                    'charts_found': charts_found,
                    'progress_found': progress_found,
                    'data_cards': data_cards,
                    'responsive': is_responsive,
                    'touch_elements': len(touch_elements),
                    'button_texts': button_texts,
                    'errors': errors,
                    'screenshot': screenshot_path
                }
                
                results.append(result)
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:100]}")
                results.append({
                    'platform': config['platform'],
                    'device': config['name'],
                    'success': False,
                    'error': str(e)
                })
        
        # Small delay between tests
        if i < len(test_configs):
            print("   ⏳ Waiting 2 seconds before next test...")
            await asyncio.sleep(2)
    
    # Print comprehensive results
    print("\n" + "=" * 70)
    print("📊 WEIGHT TRACKER SPECIFIC TESTING SUMMARY")
    print("=" * 70)
    
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r.get('success', False))
    
    print(f"Total Platforms Tested: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    print(f"Success Rate: {(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
    
    print("\n📱 Platform-Specific Results:")
    for result in results:
        platform = result['platform'].upper()
        device = result['device']
        success = result.get('success', False)
        status = "✅" if success else "❌"
        
        print(f"\n{status} {platform}: {device}")
        if 'viewport' in result:
            print(f"   Viewport: {result['viewport']['width']}x{result['viewport']['height']}")
        if success:
            print(f"   Title Found: {result.get('title_found', 'N/A')}")
            print(f"   Weight Display: {result.get('weight_display', 'N/A')}")
            print(f"   Buttons: {result.get('button_count', 'N/A')} found")
            print(f"   Charts: {result.get('charts_found', 'N/A')}")
            print(f"   Progress: {result.get('progress_found', 'N/A')}")
            print(f"   Data Cards: {result.get('data_cards', 'N/A')}")
            print(f"   Responsive: {result.get('responsive', 'N/A')}")
            print(f"   Touch Elements: {result.get('touch_elements', 'N/A')}")
        else:
            if 'error' in result:
                print(f"   Error: {result['error'][:100]}")
            if 'errors' in result and result['errors']:
                print(f"   Issues: {', '.join(result['errors'])}")
    
    print(f"\n📸 Screenshots Captured: {len([r for r in results if 'screenshot' in r])}")
    
    # Weight Tracker specific insights
    print("\n💡 WEIGHT TRACKER INSIGHTS:")
    web_results = [r for r in results if r['platform'] == 'web']
    mobile_results = [r for r in results if r['platform'] in ['android', 'ios']]
    
    if web_results and web_results[0].get('success'):
        print("   🖥️  Desktop: Full Weight Tracker experience working")
    if mobile_results:
        successful_mobile = [r for r in mobile_results if r.get('success')]
        print(f"   📱 Mobile: {len(successful_mobile)}/{len(mobile_results)} devices working")
    
    print("\n🎯 Weight Tracker testing complete across all platforms!")
    return results

if __name__ == "__main__":
    asyncio.run(test_weight_tracker_specific())
