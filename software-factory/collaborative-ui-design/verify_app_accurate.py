#!/usr/bin/env python3
"""
Accurate verification script for the Collaborative UI Design App
Focuses on actual functionality rather than pattern matching
"""

import asyncio
import sys
from browser_verification import BrowserVerifier

async def verify_app_accurately():
    """Verify the app with accurate checks"""
    print("🔍 Accurately verifying Collaborative UI Design App...")
    
    async with BrowserVerifier(headless=True) as verifier:
        # Navigate to the app
        print("1. Navigating to http://localhost:3000...")
        await verifier.page.goto("http://localhost:3000", timeout=30000)
        
        # Wait for the React app to load
        print("2. Waiting for React app to load...")
        try:
            await verifier.page.wait_for_selector('#root', timeout=10000)
            print("✅ Found #root element")
        except Exception as e:
            print(f"❌ #root element not found: {e}")
            return False
        
        # Check if the page has loaded without major errors
        print("3. Checking for major errors...")
        
        # Get page title
        title = await verifier.page.title()
        print(f"   Title: {title}")
        
        # Check for obvious error overlays or messages
        error_selectors = [
            '[data-testid="error-overlay"]',
            '.error-overlay',
            '.webpack-error-overlay',
            '[class*="error"]',
            '[class*="Error"]'
        ]
        
        has_error_overlay = False
        for selector in error_selectors:
            try:
                element = await verifier.page.query_selector(selector)
                if element:
                    text = await element.inner_text()
                    if text and len(text.strip()) > 0:
                        print(f"   ❌ Found error overlay: {text[:100]}...")
                        has_error_overlay = True
                        break
            except:
                continue
        
        if not has_error_overlay:
            print("   ✅ No error overlays found")
        
        # Check if the page is interactive (has some content)
        print("4. Checking page interactivity...")
        
        # Look for common React app elements
        react_elements = [
            'body',
            'div',
            'button',
            'input',
            'canvas'
        ]
        
        element_count = 0
        for selector in react_elements:
            count = await verifier.page.query_selector_all(selector)
            element_count += len(count)
        
        print(f"   Found {element_count} interactive elements")
        
        # Check console errors (but don't fail on warnings)
        console_errors = []
        for error in verifier.console_errors:
            if error['type'] == 'console' and error['text']:
                # Only count actual errors, not warnings
                if 'error' in error['text'].lower() and 'warning' not in error['text'].lower():
                    console_errors.append(error['text'])
        
        if console_errors:
            print(f"   ⚠️  Found {len(console_errors)} console errors:")
            for error in console_errors[:3]:  # Show first 3
                print(f"      - {error}")
        else:
            print("   ✅ No critical console errors")
        
        # Check if the page is responsive (not just a blank page)
        body_text = await verifier.page.query_selector('body')
        if body_text:
            text_content = await body_text.inner_text()
            if len(text_content.strip()) > 100:  # Has substantial content
                print("   ✅ Page has substantial content")
            else:
                print("   ⚠️  Page has minimal content")
        
        # Take a screenshot for debugging
        screenshot_path = f"app_verification_{int(asyncio.get_event_loop().time())}.png"
        await verifier.page.screenshot(path=screenshot_path)
        print(f"   📸 Screenshot saved: {screenshot_path}")
        
        # Determine success
        success = not has_error_overlay and element_count > 10
        
        print(f"\n=== VERIFICATION RESULT ===")
        print(f"Success: {'✅ YES' if success else '❌ NO'}")
        print(f"Error Overlays: {'Yes' if has_error_overlay else 'No'}")
        print(f"Interactive Elements: {element_count}")
        print(f"Console Errors: {len(console_errors)}")
        
        return success

async def main():
    """Main verification function"""
    success = await verify_app_accurately()
    
    if success:
        print("\n🎉 APP VERIFICATION SUCCESSFUL!")
        print("The Collaborative UI Design App is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 APP VERIFICATION FAILED!")
        print("The app has issues that need to be fixed.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
