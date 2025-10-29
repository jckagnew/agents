#!/usr/bin/env python3
"""
API Key Audit System for Agentic Image Selector

This script audits all required API keys, checks existing .env files,
and provides automated instructions for acquiring missing keys.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import webbrowser
import subprocess
import sys

@dataclass
class APIKeyInfo:
    """Information about an API key"""
    name: str
    description: str
    category: str
    priority: str  # "required", "recommended", "optional"
    free_tier: str
    signup_url: str
    documentation_url: str
    env_var_name: str
    current_value: Optional[str] = None
    status: str = "missing"  # "missing", "configured", "invalid"

class APIKeyAuditor:
    """Audits API keys for the Agentic Image Selector system"""
    
    def __init__(self):
        self.workspace_root = Path(__file__).parent.parent.parent.parent
        self.env_files = self.find_env_files()
        self.required_keys = self.get_required_api_keys()
        self.current_keys = self.scan_existing_keys()
    
    def find_env_files(self) -> List[Path]:
        """Find all .env files in the workspace"""
        env_files = []
        
        # Check common locations
        locations = [
            self.workspace_root / "utilities" / "env.master",
            self.workspace_root / ".env",
            self.workspace_root / ".env.local",
            self.workspace_root / ".env.development",
            self.workspace_root / "software-factory" / ".env",
            self.workspace_root / "software-factory" / "generated-apps" / "weight-tracker-nextjs" / ".env.local",
        ]
        
        for location in locations:
            if location.exists():
                env_files.append(location)
        
        # Search for additional .env files
        for env_file in self.workspace_root.rglob(".env*"):
            if env_file not in env_files and env_file.is_file():
                env_files.append(env_file)
        
        return env_files
    
    def get_required_api_keys(self) -> List[APIKeyInfo]:
        """Define all required API keys for the Agentic Image Selector"""
        return [
            # Primary: Open Source Image Repositories
            APIKeyInfo(
                name="Unsplash",
                description="High-quality free photos for commercial use",
                category="Open Source Images",
                priority="required",
                free_tier="50 requests/hour",
                signup_url="https://unsplash.com/developers",
                documentation_url="https://unsplash.com/documentation",
                env_var_name="UNSPLASH_API_KEY"
            ),
            APIKeyInfo(
                name="Pixabay",
                description="Free images, vectors, and videos",
                category="Open Source Images",
                priority="required",
                free_tier="5,000 requests/hour",
                signup_url="https://pixabay.com/api/docs/",
                documentation_url="https://pixabay.com/api/docs/",
                env_var_name="PIXABAY_API_KEY"
            ),
            APIKeyInfo(
                name="Pexels",
                description="Free stock photos and videos",
                category="Open Source Images",
                priority="recommended",
                free_tier="200 requests/hour",
                signup_url="https://www.pexels.com/api/",
                documentation_url="https://www.pexels.com/api/documentation/",
                env_var_name="PEXELS_API_KEY"
            ),
            
            # Secondary: MCP Servers (Backup)
            APIKeyInfo(
                name="Brave Search",
                description="Web search with open source image filtering",
                category="MCP Servers",
                priority="recommended",
                free_tier="2,000 requests/month",
                signup_url="https://brave.com/search/api/",
                documentation_url="https://brave.com/search/api/docs/",
                env_var_name="BRAVE_API_KEY"
            ),
            APIKeyInfo(
                name="Perplexity",
                description="AI-powered search with image discovery",
                category="MCP Servers",
                priority="recommended",
                free_tier="5 requests/minute",
                signup_url="https://www.perplexity.ai/settings/api",
                documentation_url="https://docs.perplexity.ai/",
                env_var_name="PERPLEXITY_API_KEY"
            ),
            APIKeyInfo(
                name="Serper",
                description="Google Search API (alternative to Brave)",
                category="MCP Servers",
                priority="optional",
                free_tier="2,500 requests/month",
                signup_url="https://serper.dev/",
                documentation_url="https://serper.dev/api-documentation",
                env_var_name="SERPER_API_KEY"
            ),
        ]
    
    def scan_existing_keys(self) -> Dict[str, str]:
        """Scan all .env files for existing API keys"""
        existing_keys = {}
        
        for env_file in self.env_files:
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                
                # Extract key-value pairs
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Skip placeholder values (but allow empty values for now)
                        if value and not any(placeholder in value.lower() for placeholder in ['your_', 'placeholder', 'example']):
                            existing_keys[key] = value
                            
            except Exception as e:
                print(f"⚠️ Error reading {env_file}: {e}")
        
        return existing_keys
    
    def audit_keys(self) -> Dict[str, APIKeyInfo]:
        """Audit all required keys against existing configuration"""
        audited_keys = {}
        
        for key_info in self.required_keys:
            # Check if key exists in current configuration
            if key_info.env_var_name in self.current_keys:
                key_info.current_value = self.current_keys[key_info.env_var_name]
                key_info.status = "configured"
            else:
                key_info.status = "missing"
            
            audited_keys[key_info.env_var_name] = key_info
        
        return audited_keys
    
    def generate_report(self, audited_keys: Dict[str, APIKeyInfo]) -> str:
        """Generate a comprehensive audit report"""
        report = []
        report.append("🔑 API KEY AUDIT REPORT")
        report.append("=" * 50)
        report.append(f"📁 Scanned {len(self.env_files)} .env files")
        report.append(f"🎯 Found {len(self.current_keys)} configured keys")
        report.append("")
        
        # Group by category
        categories = {}
        for key_info in audited_keys.values():
            if key_info.category not in categories:
                categories[key_info.category] = []
            categories[key_info.category].append(key_info)
        
        # Report by category
        for category, keys in categories.items():
            report.append(f"📂 {category}")
            report.append("-" * 30)
            
            for key_info in keys:
                status_icon = "✅" if key_info.status == "configured" else "❌"
                priority_icon = "🔴" if key_info.priority == "required" else "🟡" if key_info.priority == "recommended" else "🟢"
                
                report.append(f"{status_icon} {priority_icon} {key_info.name}")
                report.append(f"   Description: {key_info.description}")
                report.append(f"   Free Tier: {key_info.free_tier}")
                report.append(f"   Status: {key_info.status.upper()}")
                
                if key_info.status == "configured":
                    # Mask the key for security
                    masked_key = key_info.current_value[:8] + "..." + key_info.current_value[-4:] if len(key_info.current_value) > 12 else "***"
                    report.append(f"   Current Value: {masked_key}")
                else:
                    report.append(f"   Signup URL: {key_info.signup_url}")
                
                report.append("")
        
        return "\n".join(report)
    
    def generate_setup_instructions(self, audited_keys: Dict[str, APIKeyInfo]) -> str:
        """Generate automated setup instructions for missing keys"""
        missing_keys = [key for key in audited_keys.values() if key.status == "missing"]
        
        if not missing_keys:
            return "🎉 All required API keys are configured!"
        
        instructions = []
        instructions.append("🚀 AUTOMATED SETUP INSTRUCTIONS")
        instructions.append("=" * 40)
        instructions.append("")
        
        # Group by priority
        required = [key for key in missing_keys if key.priority == "required"]
        recommended = [key for key in missing_keys if key.priority == "recommended"]
        optional = [key for key in missing_keys if key.priority == "optional"]
        
        if required:
            instructions.append("🔴 REQUIRED KEYS (Must configure for basic functionality)")
            instructions.append("-" * 50)
            for key_info in required:
                instructions.append(f"1. {key_info.name}")
                instructions.append(f"   • Visit: {key_info.signup_url}")
                instructions.append(f"   • Free Tier: {key_info.free_tier}")
                instructions.append(f"   • Add to env.master: {key_info.env_var_name}=your_key_here")
                instructions.append("")
        
        if recommended:
            instructions.append("🟡 RECOMMENDED KEYS (Better results and more options)")
            instructions.append("-" * 50)
            for key_info in recommended:
                instructions.append(f"1. {key_info.name}")
                instructions.append(f"   • Visit: {key_info.signup_url}")
                instructions.append(f"   • Free Tier: {key_info.free_tier}")
                instructions.append(f"   • Add to env.master: {key_info.env_var_name}=your_key_here")
                instructions.append("")
        
        if optional:
            instructions.append("🟢 OPTIONAL KEYS (Additional features)")
            instructions.append("-" * 50)
            for key_info in optional:
                instructions.append(f"1. {key_info.name}")
                instructions.append(f"   • Visit: {key_info.signup_url}")
                instructions.append(f"   • Free Tier: {key_info.free_tier}")
                instructions.append(f"   • Add to env.master: {key_info.env_var_name}=your_key_here")
                instructions.append("")
        
        instructions.append("📝 QUICK SETUP COMMANDS")
        instructions.append("-" * 30)
        instructions.append("# Open the main environment file")
        instructions.append("code utilities/env.master")
        instructions.append("")
        instructions.append("# Or edit directly")
        instructions.append("nano utilities/env.master")
        instructions.append("")
        instructions.append("# Add your keys in this format:")
        for key_info in missing_keys:
            instructions.append(f"# {key_info.name}")
            instructions.append(f"{key_info.env_var_name}=your_{key_info.name.lower()}_key_here")
            instructions.append("")
        
        return "\n".join(instructions)
    
    def open_signup_pages(self, audited_keys: Dict[str, APIKeyInfo]):
        """Open signup pages for missing required keys"""
        missing_required = [key for key in audited_keys.values() if key.status == "missing" and key.priority == "required"]
        
        if not missing_required:
            print("✅ All required API keys are configured!")
            return
        
        print(f"🌐 Opening {len(missing_required)} signup pages...")
        
        for key_info in missing_required:
            try:
                webbrowser.open(key_info.signup_url)
                print(f"   Opened: {key_info.name}")
            except Exception as e:
                print(f"   Failed to open {key_info.name}: {e}")
    
    def create_env_template(self, audited_keys: Dict[str, APIKeyInfo]) -> str:
        """Create a template .env file with all required keys"""
        template = []
        template.append("# Agentic Image Selector - API Keys")
        template.append("# Generated by api-key-audit.py")
        template.append("")
        
        # Group by category
        categories = {}
        for key_info in audited_keys.values():
            if key_info.category not in categories:
                categories[key_info.category] = []
            categories[key_info.category].append(key_info)
        
        for category, keys in categories.items():
            template.append(f"# {category}")
            for key_info in keys:
                if key_info.status == "missing":
                    template.append(f"{key_info.env_var_name}=your_{key_info.name.lower()}_key_here")
                else:
                    template.append(f"{key_info.env_var_name}={key_info.current_value}")
            template.append("")
        
        return "\n".join(template)
    
    def run_audit(self):
        """Run the complete API key audit"""
        print("🔍 Starting API Key Audit...")
        print(f"📁 Scanning {len(self.env_files)} .env files...")
        
        # Find all .env files
        print(f"   Found .env files:")
        for env_file in self.env_files:
            print(f"   - {env_file.relative_to(self.workspace_root)}")
        
        # Audit keys
        audited_keys = self.audit_keys()
        
        # Generate report
        report = self.generate_report(audited_keys)
        print("\n" + report)
        
        # Generate setup instructions
        instructions = self.generate_setup_instructions(audited_keys)
        print("\n" + instructions)
        
        # Save reports
        self.save_reports(audited_keys, report, instructions)
        
        # Ask if user wants to open signup pages (skip in non-interactive mode)
        missing_required = [key for key in audited_keys.values() if key.status == "missing" and key.priority == "required"]
        if missing_required and sys.stdin.isatty():
            try:
                response = input(f"\n🌐 Open signup pages for {len(missing_required)} missing required keys? (y/n): ")
                if response.lower() in ['y', 'yes']:
                    self.open_signup_pages(audited_keys)
            except (EOFError, KeyboardInterrupt):
                print("\n⏭️ Skipping interactive prompts")
        
        return audited_keys
    
    def save_reports(self, audited_keys: Dict[str, APIKeyInfo], report: str, instructions: str):
        """Save audit reports to files"""
        reports_dir = Path(__file__).parent / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        # Save main report
        report_file = reports_dir / "api-key-audit-report.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        # Save setup instructions
        instructions_file = reports_dir / "api-key-setup-instructions.md"
        with open(instructions_file, 'w') as f:
            f.write(instructions)
        
        # Save JSON data
        json_data = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "env_files_scanned": [str(f) for f in self.env_files],
            "keys_found": len(self.current_keys),
            "audit_results": {
                name: {
                    "name": key.name,
                    "description": key.description,
                    "category": key.category,
                    "priority": key.priority,
                    "free_tier": key.free_tier,
                    "signup_url": key.signup_url,
                    "status": key.status,
                    "configured": key.status == "configured"
                }
                for name, key in audited_keys.items()
            }
        }
        
        json_file = reports_dir / "api-key-audit-data.json"
        with open(json_file, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"\n💾 Reports saved to:")
        print(f"   - {report_file}")
        print(f"   - {instructions_file}")
        print(f"   - {json_file}")

def main():
    """Main execution function"""
    auditor = APIKeyAuditor()
    audited_keys = auditor.run_audit()
    
    # Summary
    total_keys = len(audited_keys)
    configured_keys = len([k for k in audited_keys.values() if k.status == "configured"])
    missing_keys = total_keys - configured_keys
    
    print(f"\n📊 SUMMARY")
    print(f"   Total Keys: {total_keys}")
    print(f"   Configured: {configured_keys}")
    print(f"   Missing: {missing_keys}")
    
    if missing_keys == 0:
        print("🎉 All API keys are configured! Ready to run the Agentic Image Selector.")
    else:
        print(f"⚠️ {missing_keys} keys need to be configured before running the system.")

if __name__ == "__main__":
    main()
