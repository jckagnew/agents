#!/usr/bin/env python3
"""
Get All Free API Keys - Automated Setup

This script opens all the signup pages for free API keys and provides
step-by-step instructions for each service.
"""

import webbrowser
import time
import subprocess
import sys
from pathlib import Path

class FreeAPIKeyGetter:
    """Automated setup for all free API keys"""
    
    def __init__(self):
        self.keys_to_get = [
            {
                "name": "Pixabay",
                "url": "https://pixabay.com/api/docs/",
                "steps": [
                    "1. Click 'Get Started' or 'Sign Up'",
                    "2. Create account with email/password",
                    "3. Verify email if required",
                    "4. Go to 'My Account' → 'API'",
                    "5. Copy your API key",
                    "6. Add to utilities/env.master: PIXABAY_API_KEY=your_key_here"
                ],
                "free_tier": "5,000 requests/hour",
                "time_estimate": "2 minutes"
            },
            {
                "name": "Pexels",
                "url": "https://www.pexels.com/api/",
                "steps": [
                    "1. Click 'Get Started' or 'Sign Up'",
                    "2. Create account with email/password",
                    "3. Verify email if required",
                    "4. Go to 'API' section in your account",
                    "5. Copy your API key",
                    "6. Add to utilities/env.master: PEXELS_API_KEY=your_key_here"
                ],
                "free_tier": "200 requests/hour",
                "time_estimate": "2 minutes"
            },
            {
                "name": "Brave Search",
                "url": "https://brave.com/search/api/",
                "steps": [
                    "1. Click 'Get Started' or 'Sign Up'",
                    "2. Create account with email/password",
                    "3. Verify email if required",
                    "4. Go to 'API Keys' section",
                    "5. Generate new API key",
                    "6. Copy your API key",
                    "7. Add to utilities/env.master: BRAVE_API_KEY=your_key_here"
                ],
                "free_tier": "2,000 requests/month",
                "time_estimate": "3 minutes"
            },
            {
                "name": "Perplexity",
                "url": "https://www.perplexity.ai/settings/api",
                "steps": [
                    "1. Create account or sign in",
                    "2. Go to Settings → API",
                    "3. Click 'Create API Key'",
                    "4. Copy your API key",
                    "5. Add to utilities/env.master: PERPLEXITY_API_KEY=your_key_here"
                ],
                "free_tier": "5 requests/minute",
                "time_estimate": "2 minutes"
            }
        ]
    
    def open_all_signup_pages(self):
        """Open all signup pages in sequence"""
        print("🚀 Opening all signup pages...")
        print("=" * 50)
        
        for i, key_info in enumerate(self.keys_to_get, 1):
            print(f"\n{i}. {key_info['name']} - {key_info['free_tier']}")
            print(f"   Opening: {key_info['url']}")
            
            try:
                webbrowser.open(key_info['url'])
                print(f"   ✅ Opened in browser")
            except Exception as e:
                print(f"   ❌ Failed to open: {e}")
            
            # Small delay between openings
            time.sleep(1)
        
        print(f"\n🌐 Opened {len(self.keys_to_get)} signup pages!")
        print("📋 Follow the instructions below for each service...")
    
    def print_detailed_instructions(self):
        """Print detailed step-by-step instructions"""
        print("\n" + "=" * 60)
        print("📋 DETAILED SETUP INSTRUCTIONS")
        print("=" * 60)
        
        for i, key_info in enumerate(self.keys_to_get, 1):
            print(f"\n🔑 {i}. {key_info['name']} API Key")
            print(f"   Free Tier: {key_info['free_tier']}")
            print(f"   Time: {key_info['time_estimate']}")
            print(f"   URL: {key_info['url']}")
            print("   Steps:")
            
            for step in key_info['steps']:
                print(f"      {step}")
            
            print("   " + "-" * 40)
    
    def create_env_template(self):
        """Create a template .env file with all keys"""
        template = """# Agentic Image Selector - API Keys
# Add your API keys here after getting them from the signup pages

# Open Source Image Repositories
UNSPLASH_API_KEY=L72pBjj5...x7CE  # Already configured
PIXABAY_API_KEY=your_pixabay_key_here
PEXELS_API_KEY=your_pexels_key_here

# MCP Servers (Backup)
SERPER_API_KEY=4d723748...e36e  # Already configured
BRAVE_API_KEY=your_brave_key_here
PERPLEXITY_API_KEY=your_perplexity_key_here

# Instructions:
# 1. Get your keys from the signup pages (opened above)
# 2. Replace 'your_*_key_here' with your actual keys
# 3. Save this file
# 4. Run: python3 agents/orchestration-agent.py --run
"""
        
        template_file = Path(__file__).parent.parent / "api-keys-template.env"
        with open(template_file, 'w') as f:
            f.write(template)
        
        print(f"\n💾 Created template file: {template_file}")
        return template_file
    
    def open_env_file(self):
        """Open the main environment file for editing"""
        env_file = Path(__file__).parent.parent.parent.parent / "utilities" / "env.master"
        
        if env_file.exists():
            print(f"\n📝 Opening environment file for editing...")
            print(f"   File: {env_file}")
            
            try:
                # Try to open with VS Code first
                subprocess.run(["code", str(env_file)], check=False)
                print("   ✅ Opened with VS Code")
            except:
                try:
                    # Fallback to nano
                    subprocess.run(["nano", str(env_file)], check=False)
                    print("   ✅ Opened with nano")
                except:
                    print("   ⚠️ Could not open editor automatically")
                    print(f"   Please manually edit: {env_file}")
        else:
            print(f"   ❌ Environment file not found: {env_file}")
    
    def run_setup(self):
        """Run the complete setup process"""
        print("🔑 FREE API KEY SETUP AUTOMATION")
        print("=" * 50)
        print("This will help you get all the free API keys needed for the Agentic Image Selector.")
        print("Total time: ~10 minutes for all keys")
        print("")
        
        # Open all signup pages
        self.open_all_signup_pages()
        
        # Print detailed instructions
        self.print_detailed_instructions()
        
        # Create template file
        template_file = self.create_env_template()
        
        # Open environment file
        self.open_env_file()
        
        # Final instructions
        print("\n" + "=" * 60)
        print("🎯 NEXT STEPS")
        print("=" * 60)
        print("1. Complete the signup process for each service (pages opened above)")
        print("2. Copy your API keys from each service")
        print("3. Add them to utilities/env.master (file opened above)")
        print("4. Save the file")
        print("5. Run: cd software-factory/agentic-image-selector && python3 agents/orchestration-agent.py --run")
        print("")
        print("💡 TIP: Keep this terminal open while you sign up for each service")
        print("💡 TIP: You can copy-paste the template from the created file")
        
        return template_file

def main():
    """Main execution function"""
    getter = FreeAPIKeyGetter()
    template_file = getter.run_setup()
    
    print(f"\n✅ Setup automation complete!")
    print(f"📁 Template saved to: {template_file}")
    print(f"🌐 Signup pages opened in your browser")
    print(f"📝 Environment file opened for editing")
    print(f"\n🚀 Ready to get your free API keys!")

if __name__ == "__main__":
    main()
