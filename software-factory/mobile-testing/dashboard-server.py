#!/usr/bin/env python3
"""
Mobile Testing Dashboard Server
Serves the dashboard and executes real mobile tests
"""

import asyncio
import json
import os
import subprocess
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
from browser_verification import BrowserVerifier

class MobileTestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_dashboard()
        elif parsed_path.path == '/api/status':
            self.serve_status()
        elif parsed_path.path == '/api/test':
            self.handle_test_request(parsed_path)
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        try:
            with open('updated-mobile-testing-dashboard.html', 'r') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode())
        except FileNotFoundError:
            self.send_error(404, "Dashboard file not found")
    
    def serve_status(self):
        status = {
            'android': self.check_android_status(),
            'ios': self.check_ios_status(),
            'web': self.check_web_status(),
            'playwright': self.check_playwright_status()
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(status).encode())
    
    def handle_test_request(self, parsed_path):
        query_params = parse_qs(parsed_path.query)
        test_type = query_params.get('type', [''])[0]
        
        if test_type == 'collaborative_ui':
            self.run_collaborative_ui_test()
        elif test_type == 'weight_tracker':
            self.run_weight_tracker_test()
        elif test_type == 'universal':
            self.run_universal_test()
        elif test_type == 'mobile_responsiveness':
            self.run_mobile_responsiveness_test()
        else:
            self.send_error(400, "Invalid test type")
    
    def check_android_status(self):
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
            return 'online' if 'device' in result.stdout else 'offline'
        except:
            return 'offline'
    
    def check_ios_status(self):
        try:
            result = subprocess.run(['xcrun', 'simctl', 'list', 'devices'], capture_output=True, text=True, timeout=5)
            return 'online' if 'Booted' in result.stdout else 'offline'
        except:
            return 'offline'
    
    def check_web_status(self):
        try:
            result = subprocess.run(['curl', '-s', 'http://localhost:3000'], capture_output=True, text=True, timeout=5)
            return 'online' if result.returncode == 0 else 'offline'
        except:
            return 'offline'
    
    def check_playwright_status(self):
        try:
            import playwright
            return 'online'
        except ImportError:
            return 'offline'
    
    def run_collaborative_ui_test(self):
        """Run Collaborative UI test in background"""
        def run_test():
            asyncio.run(self._test_collaborative_ui())
        
        thread = threading.Thread(target=run_test)
        thread.daemon = True
        thread.start()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'started'}).encode())
    
    def run_weight_tracker_test(self):
        """Run Weight Tracker test in background"""
        def run_test():
            asyncio.run(self._test_weight_tracker())
        
        thread = threading.Thread(target=run_test)
        thread.daemon = True
        thread.start()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'started'}).encode())
    
    def run_universal_test(self):
        """Run Universal test in background"""
        def run_test():
            asyncio.run(self._test_universal())
        
        thread = threading.Thread(target=run_test)
        thread.daemon = True
        thread.start()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'started'}).encode())
    
    def run_mobile_responsiveness_test(self):
        """Run Mobile Responsiveness test in background"""
        def run_test():
            asyncio.run(self._test_mobile_responsiveness())
        
        thread = threading.Thread(target=run_test)
        thread.daemon = True
        thread.start()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'started'}).encode())
    
    async def _test_collaborative_ui(self):
        """Test Collaborative UI Design App"""
        print("🔍 Testing Collaborative UI Design App...")
        
        test_configs = [
            {'name': 'Desktop', 'viewport': {'width': 1920, 'height': 1080}},
            {'name': 'Android Phone', 'viewport': {'width': 360, 'height': 640}},
            {'name': 'iPhone', 'viewport': {'width': 375, 'height': 667}},
            {'name': 'iPad', 'viewport': {'width': 768, 'height': 1024}}
        ]
        
        results = []
        for config in test_configs:
            async with BrowserVerifier(headless=True) as verifier:
                await verifier.page.set_viewport_size(config['viewport'])
                
                try:
                    await verifier.page.goto('http://localhost:3000', timeout=30000)
                    await verifier.page.wait_for_selector('body', timeout=10000)
                    
                    # Test responsiveness
                    content_width = await verifier.page.evaluate('document.body.scrollWidth')
                    is_responsive = content_width <= config['viewport']['width'] + 100
                    
                    # Test touch elements
                    touch_elements = await verifier.page.query_selector_all('button, input, [role="button"]')
                    
                    # Test search functionality
                    search_working = False
                    search_input = await verifier.page.query_selector('input[placeholder*="Search"]')
                    if search_input:
                        search_working = True
                    
                    # Test filters
                    filters_working = False
                    filter_buttons = await verifier.page.query_selector_all('button:has-text("Atom"), button:has-text("All")')
                    if filter_buttons:
                        filters_working = True
                    
                    # Take screenshot
                    screenshot_path = f"collaborative_ui_{config['name'].lower().replace(' ', '_')}_{int(time.time())}.png"
                    await verifier.page.screenshot(path=screenshot_path)
                    
                    result = {
                        'platform': config['name'],
                        'responsive': is_responsive,
                        'touch_elements': len(touch_elements),
                        'search_working': search_working,
                        'filters_working': filters_working,
                        'screenshot': screenshot_path,
                        'success': is_responsive and len(touch_elements) >= 5 and search_working and filters_working
                    }
                    
                    results.append(result)
                    print(f"✅ {config['name']}: {'Pass' if result['success'] else 'Fail'}")
                    
                except Exception as e:
                    print(f"❌ {config['name']}: Error - {str(e)[:100]}")
                    results.append({
                        'platform': config['name'],
                        'success': False,
                        'error': str(e)
                    })
        
        # Save results
        with open('collaborative_ui_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📊 Collaborative UI Test Complete: {sum(1 for r in results if r.get('success', False))}/{len(results)} passed")
    
    async def _test_weight_tracker(self):
        """Test Weight Tracker App"""
        print("🏋️ Testing Weight Tracker App...")
        
        test_configs = [
            {'name': 'Desktop', 'viewport': {'width': 1920, 'height': 1080}},
            {'name': 'Android Phone', 'viewport': {'width': 360, 'height': 640}},
            {'name': 'iPhone', 'viewport': {'width': 375, 'height': 667}},
            {'name': 'iPad', 'viewport': {'width': 768, 'height': 1024}}
        ]
        
        results = []
        for config in test_configs:
            async with BrowserVerifier(headless=True) as verifier:
                await verifier.page.set_viewport_size(config['viewport'])
                
                try:
                    await verifier.page.goto('http://localhost:3001', timeout=30000)
                    await verifier.page.wait_for_selector('body', timeout=10000)
                    await verifier.page.wait_for_load_state('networkidle')
                    
                    # Test for Weight Tracker elements
                    title_found = False
                    title_elements = await verifier.page.query_selector_all('h1, h2, [class*="title"]')
                    for element in title_elements:
                        text = await element.inner_text()
                        if 'Weight Tracker' in text or 'weight' in text.lower():
                            title_found = True
                            break
                    
                    # Test for buttons
                    buttons_found = False
                    button_elements = await verifier.page.query_selector_all('button')
                    button_texts = []
                    for button in button_elements:
                        text = await button.inner_text()
                        button_texts.append(text)
                        if any(keyword in text.lower() for keyword in ['log', 'entry', 'history', 'analytics', 'track']):
                            buttons_found = True
                    
                    # Test for charts
                    charts_found = False
                    chart_elements = await verifier.page.query_selector_all('svg, canvas, [class*="chart"]')
                    if len(chart_elements) > 0:
                        charts_found = True
                    
                    # Test responsiveness
                    content_width = await verifier.page.evaluate('document.body.scrollWidth')
                    is_responsive = content_width <= config['viewport']['width'] + 100
                    
                    # Take screenshot
                    screenshot_path = f"weight_tracker_{config['name'].lower().replace(' ', '_')}_{int(time.time())}.png"
                    await verifier.page.screenshot(path=screenshot_path)
                    
                    result = {
                        'platform': config['name'],
                        'title_found': title_found,
                        'buttons_found': buttons_found,
                        'button_count': len(button_elements),
                        'charts_found': charts_found,
                        'responsive': is_responsive,
                        'screenshot': screenshot_path,
                        'success': title_found and buttons_found and charts_found and is_responsive
                    }
                    
                    results.append(result)
                    print(f"✅ {config['name']}: {'Pass' if result['success'] else 'Fail'}")
                    
                except Exception as e:
                    print(f"❌ {config['name']}: Error - {str(e)[:100]}")
                    results.append({
                        'platform': config['name'],
                        'success': False,
                        'error': str(e)
                    })
        
        # Save results
        with open('weight_tracker_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📊 Weight Tracker Test Complete: {sum(1 for r in results if r.get('success', False))}/{len(results)} passed")
    
    async def _test_universal(self):
        """Test Universal App functionality"""
        print("🚀 Testing Universal App functionality...")
        
        # Test both apps
        await self._test_collaborative_ui()
        await self._test_weight_tracker()
        
        print("✅ Universal App testing complete")
    
    async def _test_mobile_responsiveness(self):
        """Test Mobile Responsiveness"""
        print("📱 Testing Mobile Responsiveness...")
        
        # Test responsive breakpoints
        breakpoints = [
            {'name': 'Mobile Small', 'width': 320, 'height': 568},
            {'name': 'Mobile Medium', 'width': 375, 'height': 667},
            {'name': 'Mobile Large', 'width': 414, 'height': 896},
            {'name': 'Tablet', 'width': 768, 'height': 1024},
            {'name': 'Desktop', 'width': 1920, 'height': 1080}
        ]
        
        results = []
        for bp in breakpoints:
            async with BrowserVerifier(headless=True) as verifier:
                await verifier.page.set_viewport_size({'width': bp['width'], 'height': bp['height']})
                
                try:
                    # Test both apps
                    for url, name in [('http://localhost:3000', 'Collaborative UI'), ('http://localhost:3001', 'Weight Tracker')]:
                        await verifier.page.goto(url, timeout=30000)
                        await verifier.page.wait_for_selector('body', timeout=10000)
                        
                        # Test responsiveness
                        content_width = await verifier.page.evaluate('document.body.scrollWidth')
                        is_responsive = content_width <= bp['width'] + 100
                        
                        # Test touch elements
                        touch_elements = await verifier.page.query_selector_all('button, input, [role="button"]')
                        touch_friendly = len(touch_elements) >= 3
                        
                        result = {
                            'breakpoint': bp['name'],
                            'app': name,
                            'viewport': f"{bp['width']}x{bp['height']}",
                            'responsive': is_responsive,
                            'touch_friendly': touch_friendly,
                            'touch_elements': len(touch_elements),
                            'success': is_responsive and touch_friendly
                        }
                        
                        results.append(result)
                        print(f"✅ {bp['name']} - {name}: {'Pass' if result['success'] else 'Fail'}")
                        
                except Exception as e:
                    print(f"❌ {bp['name']}: Error - {str(e)[:100]}")
        
        # Save results
        with open('mobile_responsiveness_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📊 Mobile Responsiveness Test Complete: {sum(1 for r in results if r.get('success', False))}/{len(results)} passed")

def run_dashboard_server(port=8080):
    """Run the mobile testing dashboard server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MobileTestHandler)
    
    print(f"🚀 Mobile Testing Dashboard Server starting on port {port}")
    print(f"📱 Open http://localhost:{port} in your browser")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == "__main__":
    run_dashboard_server()
