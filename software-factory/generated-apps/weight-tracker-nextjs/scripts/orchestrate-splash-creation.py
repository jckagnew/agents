#!/usr/bin/env python3
"""
Weight Tracker Splash Screen Creation Orchestrator

This script orchestrates the complete agent-driven workflow for creating
animated splash screens for the Weight Tracker app.
"""

import asyncio
import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime

class SplashCreationOrchestrator:
    """Orchestrates the complete splash screen creation workflow"""
    
    def __init__(self):
        self.scripts_dir = Path(__file__).parent
        self.project_root = self.scripts_dir.parent
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "phases": {},
            "success": False,
            "final_prototypes": []
        }
    
    async def run_phase(self, phase_name: str, script_path: str, description: str) -> bool:
        """Run a single phase of the workflow"""
        print(f"\n{'='*60}")
        print(f"🚀 PHASE: {phase_name}")
        print(f"📝 {description}")
        print(f"{'='*60}")
        
        try:
            # Run the script
            result = subprocess.run([
                sys.executable, str(script_path)
            ], capture_output=True, text=True, cwd=self.scripts_dir)
            
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
        
        # Check if MCP servers are configured
        env_file = self.project_root.parent.parent.parent / "utilities" / "env.master"
        if not env_file.exists():
            print("❌ Environment file not found. Please run the MCP setup first.")
            return False
        
        # Check for required API keys
        with open(env_file, 'r') as f:
            env_content = f.read()
        
        required_keys = ["BRAVE_API_KEY", "PERPLEXITY_API_KEY"]
        missing_keys = []
        
        for key in required_keys:
            if f"{key}=" not in env_content or f"{key}=your_" in env_content:
                missing_keys.append(key)
        
        if missing_keys:
            print(f"⚠️ Missing API keys: {', '.join(missing_keys)}")
            print("   Falling back to offline creative library. Add keys to enable live sourcing.")
        else:
            print("✅ Prerequisites check passed")
        return True
    
    async def run_workflow(self) -> bool:
        """Run the complete workflow"""
        print("🎯 Weight Tracker Splash Screen Creation Workflow")
        print("=" * 60)
        print("This workflow will:")
        print("1. Source 100+ fitness cartoon image pairs using MCP servers")
        print("2. Curate and score the best 3 pairs using AI analysis")
        print("3. Generate animated splash screen prototypes")
        print("4. Create a comparison page for testing")
        print("=" * 60)
        
        # Check prerequisites
        if not await self.check_prerequisites():
            return False
        
        # Phase 1: Image Sourcing
        success = await self.run_phase(
            "Image Sourcing",
            "image-sourcing-agent.py",
            "Using MCP servers (Brave Search, Perplexity) to source 100+ fitness cartoon image pairs"
        )
        if not success:
            return False
        
        # Phase 2: Design Curation
        success = await self.run_phase(
            "Design Curation",
            "design-curation-agent.py",
            "Using AI to evaluate and select the top 3 image pairs based on commercial appeal, animation potential, and design quality"
        )
        if not success:
            return False
        
        # Phase 3: Animation Prototyping
        success = await self.run_phase(
            "Animation Prototyping",
            "animation-prototype-agent.py",
            "Creating animated splash screen prototypes with the top 3 image pairs"
        )
        if not success:
            return False
        
        # Load final results
        try:
            with open(self.scripts_dir / "top_image_pairs.json", 'r') as f:
                top_pairs_data = json.load(f)
            self.results["final_prototypes"] = top_pairs_data["top_pairs"]
        except Exception as e:
            print(f"⚠️ Could not load final results: {e}")
        
        self.results["success"] = True
        return True
    
    def save_workflow_results(self):
        """Save the complete workflow results"""
        results_file = self.scripts_dir / "workflow_results.json"
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
            
            if self.results["final_prototypes"]:
                print(f"\n🏆 Top 3 Prototypes Created:")
                for i, prototype in enumerate(self.results["final_prototypes"], 1):
                    print(f"   {i}. Overall Score: {prototype['scores']['overall']:.2f}")
                    print(f"      Commercial: {prototype['scores']['commercial_appeal']:.2f}")
                    print(f"      Animation: {prototype['scores']['animation_potential']:.2f}")
                    print(f"      Design: {prototype['scores']['design_quality']:.2f}")
                    print()
            
            print("🎯 Next Steps:")
            print("   1. Visit /splash-comparison to test all prototypes")
            print("   2. Run user testing to measure commercial appeal")
            print("   3. Select the best-performing prototype")
            print("   4. Integrate into the main Weight Tracker app")
            
        else:
            print("❌ Workflow failed. Check the phase details below:")
            for phase, details in self.results["phases"].items():
                if details["status"] != "success":
                    print(f"   - {phase}: {details['status']}")
        
        print(f"\n📁 All files saved in: {self.scripts_dir}")
        print(f"📊 Detailed results: workflow_results.json")

async def main():
    """Main execution function"""
    orchestrator = SplashCreationOrchestrator()
    
    try:
        success = await orchestrator.run_workflow()
        orchestrator.save_workflow_results()
        orchestrator.print_summary()
        
        if success:
            print("\n🎉 Splash screen creation workflow completed successfully!")
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

if __name__ == "__main__":
    asyncio.run(main())
