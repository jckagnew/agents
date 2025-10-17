#!/usr/bin/env python3
"""
Comprehensive Browser Verification System using Playwright
Provides tools to verify web applications, check for errors, and validate functionality
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Tuple, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Error
from dataclasses import dataclass
from datetime import datetime

@dataclass
class VerificationResult:
    """Result of a browser verification check"""
    success: bool
    url: str
    title: str
    errors: List[str]
    warnings: List[str]
    console_errors: List[Dict[str, Any]]
    network_errors: List[Dict[str, Any]]
    compilation_errors: List[str]
    page_content: str
    screenshot_path: Optional[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class BrowserVerifier:
    """Comprehensive browser verification system"""
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            ignore_https_errors=True
        )
        self.page = await self.context.new_page()
        
        # Set up error collection
        self.console_errors = []
        self.network_errors = []
        
        # Listen for console errors
        self.page.on("console", self._handle_console_message)
        self.page.on("pageerror", self._handle_page_error)
        self.page.on("requestfailed", self._handle_request_failed)
        
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
    
    def _handle_console_message(self, msg):
        """Handle console messages and collect errors"""
        if msg.type == 'error':
            self.console_errors.append({
                'type': 'console',
                'text': msg.text,
                'location': msg.location,
                'timestamp': datetime.now().isoformat()
            })
    
    def _handle_page_error(self, error):
        """Handle page errors"""
        self.console_errors.append({
            'type': 'page_error',
            'text': str(error),
            'timestamp': datetime.now().isoformat()
        })
    
    def _handle_request_failed(self, request):
        """Handle failed network requests"""
        self.network_errors.append({
            'type': 'request_failed',
            'url': request.url,
            'method': request.method,
            'timestamp': datetime.now().isoformat()
        })
    
    async def verify_url(self, url: str, wait_for_selector: Optional[str] = None, 
                        check_compilation: bool = True) -> VerificationResult:
        """
        Verify a URL for errors and functionality
        
        Args:
            url: URL to verify
            wait_for_selector: CSS selector to wait for (e.g., '#root' for React apps)
            check_compilation: Whether to check for compilation errors
            
        Returns:
            VerificationResult with detailed information
        """
        errors = []
        warnings = []
        compilation_errors = []
        
        try:
            # Navigate to the URL
            print(f"Navigating to {url}...")
            response = await self.page.goto(url, timeout=self.timeout, wait_until='domcontentloaded')
            
            if not response or response.status >= 400:
                errors.append(f"HTTP Error: {response.status if response else 'No response'}")
            
            # Wait for specific selector if provided
            if wait_for_selector:
                try:
                    await self.page.wait_for_selector(wait_for_selector, timeout=10000)
                    print(f"Found selector: {wait_for_selector}")
                except Error as e:
                    errors.append(f"Selector not found: {wait_for_selector} - {str(e)}")
            
            # Get page information
            title = await self.page.title()
            content = await self.page.content()
            
            # Check for compilation errors in content
            if check_compilation:
                compilation_errors = self._check_compilation_errors(content)
            
            # Check for common error patterns
            error_patterns = [
                "Compiled with problems",
                "Module build failed",
                "ERROR in",
                "Failed to compile",
                "Webpack compilation error",
                "PostCSS error",
                "Tailwind CSS error"
            ]
            
            for pattern in error_patterns:
                if pattern.lower() in content.lower():
                    errors.append(f"Found error pattern: {pattern}")
            
            # Take screenshot for debugging
            screenshot_path = f"screenshot_{int(time.time())}.png"
            await self.page.screenshot(path=screenshot_path)
            
            success = len(errors) == 0 and len(compilation_errors) == 0
            
            return VerificationResult(
                success=success,
                url=url,
                title=title,
                errors=errors,
                warnings=warnings,
                console_errors=self.console_errors.copy(),
                network_errors=self.network_errors.copy(),
                compilation_errors=compilation_errors,
                page_content=content,
                screenshot_path=screenshot_path
            )
            
        except Error as e:
            errors.append(f"Navigation error: {str(e)}")
            return VerificationResult(
                success=False,
                url=url,
                title="",
                errors=errors,
                warnings=warnings,
                console_errors=self.console_errors.copy(),
                network_errors=self.network_errors.copy(),
                compilation_errors=compilation_errors,
                page_content=""
            )
    
    def _check_compilation_errors(self, content: str) -> List[str]:
        """Check for compilation errors in page content"""
        errors = []
        
        # Look for React compilation error overlays
        if "Compiled with problems" in content:
            errors.append("React compilation errors detected")
        
        # Look for webpack errors
        if "Module build failed" in content:
            errors.append("Webpack module build failed")
        
        # Look for PostCSS errors
        if "PostCSS" in content and "error" in content.lower():
            errors.append("PostCSS error detected")
        
        # Look for Tailwind CSS errors
        if "tailwindcss" in content.lower() and "error" in content.lower():
            errors.append("Tailwind CSS error detected")
        
        return errors
    
    async def check_react_app_loading(self, url: str) -> VerificationResult:
        """Specifically check if a React app loads properly"""
        return await self.verify_url(
            url=url,
            wait_for_selector='#root',
            check_compilation=True
        )
    
    async def check_development_server(self, url: str) -> VerificationResult:
        """Check if a development server is running and accessible"""
        return await self.verify_url(
            url=url,
            wait_for_selector='body',
            check_compilation=False
        )
    
    async def interactive_test(self, url: str, actions: List[Dict[str, Any]]) -> VerificationResult:
        """
        Perform interactive tests on a page
        
        Args:
            url: URL to test
            actions: List of actions to perform
                Example: [
                    {'type': 'click', 'selector': '#button'},
                    {'type': 'fill', 'selector': '#input', 'value': 'test'},
                    {'type': 'wait', 'time': 1000}
                ]
        """
        result = await self.verify_url(url)
        
        if not result.success:
            return result
        
        try:
            for action in actions:
                action_type = action.get('type')
                
                if action_type == 'click':
                    await self.page.click(action['selector'])
                elif action_type == 'fill':
                    await self.page.fill(action['selector'], action['value'])
                elif action_type == 'wait':
                    await asyncio.sleep(action['time'] / 1000)
                elif action_type == 'wait_for_selector':
                    await self.page.wait_for_selector(action['selector'])
                
                # Check for new errors after each action
                current_errors = self._check_compilation_errors(await self.page.content())
                if current_errors:
                    result.errors.extend(current_errors)
                    result.success = False
            
        except Error as e:
            result.errors.append(f"Interactive test error: {str(e)}")
            result.success = False
        
        return result

# Convenience functions for common use cases
async def verify_localhost_app(port: int = 3000, path: str = "") -> VerificationResult:
    """Verify a localhost app on a specific port"""
    url = f"http://localhost:{port}{path}"
    
    async with BrowserVerifier(headless=True) as verifier:
        return await verifier.check_react_app_loading(url)

async def verify_web_app(url: str) -> VerificationResult:
    """Verify any web application"""
    async with BrowserVerifier(headless=True) as verifier:
        return await verifier.verify_url(url)

async def check_compilation_errors(url: str) -> VerificationResult:
    """Specifically check for compilation errors"""
    async with BrowserVerifier(headless=True) as verifier:
        return await verifier.verify_url(url, check_compilation=True)

# CLI interface
async def main():
    """Command line interface for browser verification"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python browser_verification.py <url> [options]")
        print("Options:")
        print("  --headless=false    Run in non-headless mode")
        print("  --wait-for=<selector>  Wait for specific selector")
        print("  --check-compilation  Check for compilation errors")
        sys.exit(1)
    
    url = sys.argv[1]
    headless = '--headless=false' not in sys.argv
    wait_for = None
    check_compilation = '--check-compilation' in sys.argv
    
    for arg in sys.argv:
        if arg.startswith('--wait-for='):
            wait_for = arg.split('=')[1]
    
    async with BrowserVerifier(headless=headless) as verifier:
        result = await verifier.verify_url(url, wait_for_selector=wait_for, check_compilation=check_compilation)
        
        print(f"\n=== VERIFICATION RESULT ===")
        print(f"URL: {result.url}")
        print(f"Success: {result.success}")
        print(f"Title: {result.title}")
        print(f"Errors: {len(result.errors)}")
        print(f"Warnings: {len(result.warnings)}")
        print(f"Console Errors: {len(result.console_errors)}")
        print(f"Network Errors: {len(result.network_errors)}")
        print(f"Compilation Errors: {len(result.compilation_errors)}")
        
        if result.errors:
            print(f"\n=== ERRORS ===")
            for error in result.errors:
                print(f"- {error}")
        
        if result.console_errors:
            print(f"\n=== CONSOLE ERRORS ===")
            for error in result.console_errors:
                print(f"- {error['type']}: {error['text']}")
        
        if result.compilation_errors:
            print(f"\n=== COMPILATION ERRORS ===")
            for error in result.compilation_errors:
                print(f"- {error}")
        
        if result.screenshot_path:
            print(f"\nScreenshot saved: {result.screenshot_path}")
        
        return result

if __name__ == "__main__":
    asyncio.run(main())
