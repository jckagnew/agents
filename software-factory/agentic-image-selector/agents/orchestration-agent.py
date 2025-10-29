#!/usr/bin/env python3
"""
Generic Agentic Image Selector Orchestration Agent

This agent orchestrates the complete workflow for creating commercial splash screens
for any project type using AI-powered image sourcing and curation.
"""

import asyncio
import subprocess
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class AgenticImageSelectorOrchestrator:
    """Orchestrates the complete splash screen creation workflow for any project type"""
    
    def __init__(self, project_config: Dict[str, Any]):
        self.project_config = project_config
        self.scripts_dir = Path(__file__).parent
        output_override = project_config.get("outputPath")
        if output_override:
            self.project_root = Path(output_override)
        else:
            self.project_root = self.scripts_dir.parent.parent
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "project_config": project_config,
            "phases": {},
            "success": False,
            "generated_components": []
        }
    
    async def run_phase(self, phase_name: str, script_path: str, description: str, config: Dict[str, Any] = None) -> bool:
        """Run a single phase of the workflow with project-specific configuration"""
        print(f"\n{'='*60}")
        print(f"🚀 PHASE: {phase_name}")
        print(f"📝 {description}")
        print(f"🎯 Project: {self.project_config.get('projectType', 'unknown')}")
        print(f"{'='*60}")
        
        try:
            # Prepare configuration for the phase
            phase_config = {
                **self.project_config,
                **(config or {})
            }
            
            # Write temporary config file
            config_file = self.scripts_dir / f"temp_config_{phase_name.lower().replace(' ', '_')}.json"
            with open(config_file, 'w') as f:
                json.dump(phase_config, f, indent=2)
            
            # Run the script with configuration
            cmd = [sys.executable, str(script_path), "--config", str(config_file)]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.scripts_dir)
            
            # Clean up temp config
            config_file.unlink(missing_ok=True)
            
            if result.returncode == 0:
                print(f"✅ {phase_name} completed successfully")
                self.results["phases"][phase_name] = {
                    "status": "success",
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
                return True
            else:
                print(f"❌ {phase_name} failed")
                print(f"Error: {result.stderr}")
                self.results["phases"][phase_name] = {
                    "status": "failed",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
                return False
                
        except Exception as e:
            print(f"❌ {phase_name} failed with exception: {e}")
            self.results["phases"][phase_name] = {
                "status": "error",
                "error": str(e)
            }
            return False
    
    async def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met"""
        print("🔍 Checking prerequisites...")
        
        env_candidates = [
            self.project_root / "utilities" / "env.master",
            self.project_root.parent / "utilities" / "env.master",
            self.scripts_dir.parent.parent.parent / "utilities" / "env.master",
        ]
        
        env_file = next((candidate for candidate in env_candidates if candidate.exists()), None)
        open_source_available = False
        mcp_available = False
        
        if env_file:
            with open(env_file, 'r') as f:
                env_content = f.read()
            
            open_source_keys = ["UNSPLASH_API_KEY", "PIXABAY_API_KEY"]
            open_source_available = any(
                f"{key}=" in env_content and f"{key}=your_" not in env_content
                for key in open_source_keys
            )
            
            mcp_keys = ["BRAVE_API_KEY", "PERPLEXITY_API_KEY", "SERPER_API_KEY"]
            mcp_available = any(
                f"{key}=" in env_content and f"{key}=your_" not in env_content
                for key in mcp_keys
            )
        else:
            print("⚠️ No env.master found; proceeding with offline defaults.")
        
        if not env_file or (not open_source_available and not mcp_available):
            print("⚠️ Image sourcing keys not configured. Offline creative library will be used.")
        elif open_source_available:
            print("✅ Open source repository API keys found")
        else:
            print("⚠️ Using MCP servers as backup (open source repositories preferred)")
            print("Consider adding UNSPLASH_API_KEY or PIXABAY_API_KEY for better results")
        
        # Check if project directory exists
        if not self.project_root.exists():
            print(f"❌ Project directory not found: {self.project_root}")
            return False
        
        print("✅ Prerequisites check passed")
        return True
    
    async def initialize_project(self) -> bool:
        """Initialize the project with the selected configuration"""
        print("🏗️ Initializing project...")
        
        # Create necessary directories
        directories = [
            "src/components/splash-prototypes",
            "src/app/splash-comparison"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Created {directory}")
        
        # Generate project-specific configuration
        config_file = self.project_root / "splash-config.json"
        with open(config_file, 'w') as f:
            json.dump(self.project_config, f, indent=2)
        
        print(f"   ✅ Created splash configuration: {config_file}")
        return True
    
    async def run_workflow(self) -> bool:
        """Run the complete workflow"""
        print("🎯 Agentic Image Selector for Splash Screens")
        print("=" * 60)
        print(f"Project Type: {self.project_config.get('projectType', 'unknown')}")
        print(f"App Name: {self.project_config.get('appName', 'Unknown App')}")
        print(f"Theme: {self.project_config.get('theme', 'default')}")
        print("=" * 60)
        
        # Check prerequisites
        if not await self.check_prerequisites():
            return False
        
        # Initialize project
        if not await self.initialize_project():
            return False
        
        # Phase 1: Image Sourcing
        success = await self.run_phase(
            "Image Sourcing",
            "image-sourcing-agent.py",
            f"Using MCP servers to source 100+ {self.project_config.get('projectType', '')} image pairs",
            {
                "searchQueries": self.project_config.get("searchQueries", []),
                "imageCount": self.project_config.get("imageCount", 100)
            }
        )
        if not success:
            return False
        
        # Phase 2: Design Curation
        success = await self.run_phase(
            "Design Curation",
            "design-curation-agent.py",
            f"Using AI to evaluate and select the top 3 {self.project_config.get('projectType', '')} image pairs",
            {
                "evaluationCriteria": self.project_config.get("evaluationCriteria", {}),
                "commercialWeight": self.project_config.get("commercialWeight", 0.4)
            }
        )
        if not success:
            return False
        
        # Phase 3: Animation Generation
        success = await self.run_phase(
            "Animation Generation",
            "animation-generator-agent.py",
            f"Creating animated splash screen prototypes for {self.project_config.get('appName', 'the app')}",
            {
                "animationType": self.project_config.get("animationType", "morphing"),
                "colorScheme": self.project_config.get("colorScheme", "red-to-green"),
                "content": self.project_config.get("content", {}),
                "outputPath": str(self.project_root)
            }
        )
        if not success:
            return False
        
        # Load final results
        try:
            results_file = self.scripts_dir / "top_image_pairs.json"
            if results_file.exists():
                with open(results_file, 'r') as f:
                    top_pairs_data = json.load(f)
                self.results["generated_components"] = top_pairs_data.get("top_pairs", [])
        except Exception as e:
            print(f"⚠️ Could not load final results: {e}")
        
        self.results["success"] = True
        return True
    
    def save_workflow_results(self):
        """Save the complete workflow results"""
        results_file = self.project_root / "splash-generation-results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Workflow results saved to {results_file}")
    
    def print_summary(self):
        """Print a summary of the workflow results"""
        print(f"\n{'='*60}")
        print("📊 WORKFLOW SUMMARY")
        print(f"{'='*60}")
        
        if self.results["success"]:
            print("✅ All phases completed successfully!")
            
            if self.results["generated_components"]:
                print(f"\n🏆 Generated {len(self.results['generated_components'])} Splash Screen Prototypes:")
                for i, component in enumerate(self.results["generated_components"], 1):
                    print(f"   {i}. Overall Score: {component.get('scores', {}).get('overall', 0):.2f}")
                    print(f"      Commercial: {component.get('scores', {}).get('commercial_appeal', 0):.2f}")
                    print(f"      Animation: {component.get('scores', {}).get('animation_potential', 0):.2f}")
                    print(f"      Design: {component.get('scores', {}).get('design_quality', 0):.2f}")
                    print()
            
            print("🎯 Next Steps:")
            print("   1. Visit /splash-comparison to test all prototypes")
            print("   2. Run user testing to measure commercial appeal")
            print("   3. Select the best-performing prototype")
            print("   4. Integrate into your main application")
            
        else:
            print("❌ Workflow failed. Check the phase details below:")
            for phase, details in self.results["phases"].items():
                if details["status"] != "success":
                    print(f"   - {phase}: {details['status']}")
        
        print(f"\n📁 All files saved in: {self.project_root}")
        print(f"📊 Detailed results: splash-generation-results.json")

def load_project_type_config(project_type: str) -> Dict[str, Any]:
    """Load configuration for a specific project type"""
    config_file = Path(__file__).parent.parent / "config" / "project-types.json"
    
    if not config_file.exists():
        # Create default configuration
        default_config = {
            "fitness": {
                "projectType": "fitness",
                "theme": "transformation",
                "colorScheme": "red-to-green",
                "animationType": "morphing",
                "searchQueries": [
                    "fitness transformation before after",
                    "weight loss journey cartoon",
                    "fitness motivation character",
                    "health transformation animation"
                ],
                "content": {
                    "title": "Transform Your Life",
                    "subtitle": "Track. Transform. Triumph.",
                    "description": "Your journey starts here.",
                    "ctaPrimary": "Create Profile",
                    "ctaSecondary": "Log In"
                },
                "evaluationCriteria": {
                    "commercial_appeal": 0.4,
                    "animation_potential": 0.3,
                    "design_quality": 0.3
                }
            },
            "finance": {
                "projectType": "finance",
                "theme": "wealth-building",
                "colorScheme": "blue-to-gold",
                "animationType": "scale",
                "searchQueries": [
                    "wealth building cartoon",
                    "financial growth animation",
                    "money management character",
                    "investment success story"
                ],
                "content": {
                    "title": "Build Your Wealth",
                    "subtitle": "Invest. Grow. Prosper.",
                    "description": "Your financial future starts here.",
                    "ctaPrimary": "Get Started",
                    "ctaSecondary": "Learn More"
                },
                "evaluationCriteria": {
                    "commercial_appeal": 0.5,
                    "animation_potential": 0.2,
                    "design_quality": 0.3
                }
            },
            "productivity": {
                "projectType": "productivity",
                "theme": "efficiency",
                "colorScheme": "purple-to-pink",
                "animationType": "fade",
                "searchQueries": [
                    "productivity cartoon character",
                    "efficiency improvement animation",
                    "task management success",
                    "workflow optimization"
                ],
                "content": {
                    "title": "Boost Your Productivity",
                    "subtitle": "Organize. Execute. Succeed.",
                    "description": "Achieve more with less effort.",
                    "ctaPrimary": "Start Free",
                    "ctaSecondary": "View Demo"
                },
                "evaluationCriteria": {
                    "commercial_appeal": 0.3,
                    "animation_potential": 0.4,
                    "design_quality": 0.3
                }
            }
        }
        
        # Save default configuration
        config_file.parent.mkdir(exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
    
    # Load configuration
    with open(config_file, 'r') as f:
        configs = json.load(f)
    
    return configs.get(project_type, configs["fitness"])

async def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Agentic Image Selector for Splash Screens")
    parser.add_argument("--init", action="store_true", help="Initialize a new project")
    parser.add_argument("--run", action="store_true", help="Run the complete workflow")
    parser.add_argument("--project-type", default="fitness", help="Project type (fitness, finance, productivity)")
    parser.add_argument("--app-name", default="MyApp", help="Application name")
    parser.add_argument("--theme", help="Custom theme")
    parser.add_argument("--colors", help="Color scheme (e.g., 'red-to-green')")
    parser.add_argument("--animation", help="Animation type (morphing, scale, fade)")
    parser.add_argument("--cta-primary", help="Primary call-to-action text")
    parser.add_argument("--cta-secondary", help="Secondary call-to-action text")
    
    args = parser.parse_args()
    
    if args.init:
        # Load base configuration
        project_config = load_project_type_config(args.project_type)
        
        # Override with command line arguments
        if args.app_name:
            project_config["appName"] = args.app_name
        if args.theme:
            project_config["theme"] = args.theme
        if args.colors:
            project_config["colorScheme"] = args.colors
        if args.animation:
            project_config["animationType"] = args.animation
        if args.cta_primary:
            project_config["content"]["ctaPrimary"] = args.cta_primary
        if args.cta_secondary:
            project_config["content"]["ctaSecondary"] = args.cta_secondary
        
        print("🎯 Initializing Agentic Image Selector")
        print(f"Project Type: {project_config['projectType']}")
        print(f"App Name: {project_config['appName']}")
        print(f"Theme: {project_config['theme']}")
        print(f"Color Scheme: {project_config['colorScheme']}")
        print(f"Animation: {project_config['animationType']}")
        
        # Save configuration
        config_file = Path("splash-config.json")
        with open(config_file, 'w') as f:
            json.dump(project_config, f, indent=2)
        
        print(f"✅ Configuration saved to {config_file}")
        print("Run with --run to generate splash screens")
        return
    
    if args.run:
        # Load configuration
        config_file = Path("splash-config.json")
        if not config_file.exists():
            print("❌ No configuration found. Run with --init first.")
            return
        
        with open(config_file, 'r') as f:
            project_config = json.load(f)
        
        orchestrator = AgenticImageSelectorOrchestrator(project_config)
        
        try:
            success = await orchestrator.run_workflow()
            orchestrator.save_workflow_results()
            orchestrator.print_summary()
            
            if success:
                print("\n🎉 Splash screen generation completed successfully!")
                print("🚀 Ready to test your animated splash screens!")
            else:
                print("\n💥 Workflow failed. Please check the error messages above.")
                sys.exit(1)
                
        except KeyboardInterrupt:
            print("\n⏹️ Workflow interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n💥 Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    if not args.init and not args.run:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())
