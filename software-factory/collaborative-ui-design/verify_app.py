#!/usr/bin/env python3
"""
Quick verification script for the Collaborative UI Design App
"""

import asyncio
import sys
from browser_verification import BrowserVerifier, verify_localhost_app

async def verify_collaborative_ui_app():
    """Verify the Collaborative UI Design App"""
    print("🔍 Verifying Collaborative UI Design App...")
    
    try:
        # First check if the development server is running
        print("1. Checking if development server is accessible...")
        async with BrowserVerifier(headless=True) as verifier:
            server_result = await verifier.check_development_server("http://localhost:3000")
            
            if not server_result.success:
                print("❌ Development server is not accessible")
                print("Errors:", server_result.errors)
                return False
            
            print("✅ Development server is accessible")
        
        # Now check the React app specifically
        print("2. Checking React app loading...")
        result = await verify_localhost_app(3000)
        
        print(f"\n=== VERIFICATION RESULTS ===")
        print(f"URL: {result.url}")
        print(f"Success: {'✅ YES' if result.success else '❌ NO'}")
        print(f"Title: {result.title}")
        print(f"Total Errors: {len(result.errors)}")
        print(f"Console Errors: {len(result.console_errors)}")
        print(f"Compilation Errors: {len(result.compilation_errors)}")
        
        if result.errors:
            print(f"\n=== ERRORS ===")
            for i, error in enumerate(result.errors, 1):
                print(f"{i}. {error}")
        
        if result.console_errors:
            print(f"\n=== CONSOLE ERRORS ===")
            for i, error in enumerate(result.console_errors, 1):
                print(f"{i}. {error['type']}: {error['text']}")
        
        if result.compilation_errors:
            print(f"\n=== COMPILATION ERRORS ===")
            for i, error in enumerate(result.compilation_errors, 1):
                print(f"{i}. {error}")
        
        if result.screenshot_path:
            print(f"\n📸 Screenshot saved: {result.screenshot_path}")
        
        return result.success
        
    except Exception as e:
        print(f"❌ Verification failed with exception: {str(e)}")
        return False

async def main():
    """Main verification function"""
    success = await verify_collaborative_ui_app()
    
    if success:
        print("\n🎉 VERIFICATION SUCCESSFUL!")
        print("The Collaborative UI Design App is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 VERIFICATION FAILED!")
        print("The app has issues that need to be fixed.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
