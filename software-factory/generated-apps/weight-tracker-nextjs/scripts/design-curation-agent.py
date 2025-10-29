#!/usr/bin/env python3
"""
Weight Tracker Design Curation Agent

This agent evaluates and curates the best before/after fitness cartoon images
for the Weight Tracker splash screen based on commercial appeal, animation potential,
and design quality.
"""

import json
import asyncio
import os
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
import sys

# Add the MCP framework to the path
REPO_ROOT = Path(__file__).resolve().parents[4]
MCP_PATH = REPO_ROOT / "6_mcp"

if MCP_PATH.exists():
    sys.path.append(str(MCP_PATH))
    try:
        from agents.mcp import MCPServerStdio  # type: ignore
    except ImportError:
        print("⚠️ MCP framework not available; AI analysis will use heuristics.")
        MCPServerStdio = None  # type: ignore
else:
    print("⚠️ MCP framework directory not found; AI analysis will use heuristics.")
    MCPServerStdio = None  # type: ignore

@dataclass
class ImagePair:
    """Represents a before/after fitness image pair"""
    before_url: str
    after_url: str
    before_description: str
    after_description: str
    source: str
    quality_score: float = 0.0
    commercial_appeal: float = 0.0
    animation_potential: float = 0.0
    overall_score: float = 0.0

class DesignCurationAgent:
    """Agent responsible for curating and scoring image pairs for commercial appeal"""
    
    def __init__(self):
        self.evaluation_criteria = {
            "commercial_appeal": {
                "weight": 0.4,
                "factors": [
                    "professional_quality",
                    "brand_friendly",
                    "emotional_impact",
                    "universal_appeal"
                ]
            },
            "animation_potential": {
                "weight": 0.3,
                "factors": [
                    "smooth_transition_possibility",
                    "character_consistency",
                    "motion_friendly_design",
                    "loop_compatibility"
                ]
            },
            "design_quality": {
                "weight": 0.3,
                "factors": [
                    "visual_clarity",
                    "color_harmony",
                    "composition_balance",
                    "technical_quality"
                ]
            }
        }
    
    async def analyze_with_ai(self, image_pair: ImagePair) -> Dict[str, float]:
        """Use AI to analyze the commercial and design potential of an image pair"""
        if MCPServerStdio is None:
            return self.heuristic_scoring(image_pair)
        
        try:
            # Use Perplexity for AI analysis
            perplexity_params = {
                "command": "npx",
                "args": ["-y", "@perplexity/mcp-server"],
                "env": {"PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY", "")}
            }
            
            async with MCPServerStdio(params=perplexity_params) as perplexity:
                analysis_prompt = f"""
                Analyze these fitness transformation cartoon images for a weight tracking app splash screen:
                
                Before Image: {image_pair.before_description}
                After Image: {image_pair.after_description}
                
                Rate each category from 0-10:
                1. Commercial Appeal (professional, brand-friendly, emotional impact)
                2. Animation Potential (smooth transition, character consistency, loop-friendly)
                3. Design Quality (visual clarity, color harmony, composition)
                
                Consider:
                - Will this appeal to users wanting to track their fitness journey?
                - Can this be smoothly animated from before to after?
                - Does this look professional and trustworthy?
                - Is the character design consistent between before/after?
                - Are the colors and style suitable for a health app?
                
                Respond with only 3 numbers separated by commas (e.g., "8,7,9")
                """
                
                result = await perplexity.call_tool(
                    "perplexity_search",
                    {
                        "query": analysis_prompt,
                        "max_results": 1
                    }
                )
                
                # Parse the AI response
                if result.get("results"):
                    response_text = result["results"][0].get("text", "")
                    # Extract numbers from response
                    import re
                    numbers = re.findall(r'\d+', response_text)
                    if len(numbers) >= 3:
                        return {
                            "commercial_appeal": float(numbers[0]) / 10.0,
                            "animation_potential": float(numbers[1]) / 10.0,
                            "design_quality": float(numbers[2]) / 10.0
                        }
                
        except Exception as e:
            print(f"Error analyzing with AI: {e}")
        
        # Fallback scoring based on heuristics
        return self.heuristic_scoring(image_pair)
    
    def heuristic_scoring(self, image_pair: ImagePair) -> Dict[str, float]:
        """Fallback heuristic scoring when AI analysis fails"""
        commercial_score = 0.5
        animation_score = 0.5
        design_score = 0.5
        
        # Analyze descriptions for keywords
        before_desc = image_pair.before_description.lower()
        after_desc = image_pair.after_description.lower()
        
        # Commercial appeal factors
        if any(word in before_desc for word in ["cartoon", "character", "friendly", "motivational"]):
            commercial_score += 0.2
        if any(word in after_desc for word in ["success", "confident", "strong", "healthy"]):
            commercial_score += 0.2
        if "transformation" in before_desc or "transformation" in after_desc:
            commercial_score += 0.1
        
        # Animation potential factors
        if "character" in before_desc and "character" in after_desc:
            animation_score += 0.2
        if "smooth" in before_desc or "smooth" in after_desc:
            animation_score += 0.1
        if len(before_desc) > 20 and len(after_desc) > 20:  # Detailed descriptions
            animation_score += 0.1
        
        # Design quality factors
        if any(word in before_desc for word in ["colorful", "bright", "clear", "professional"]):
            design_score += 0.2
        if any(word in after_desc for word in ["vibrant", "clean", "modern", "polished"]):
            design_score += 0.2
        
        return {
            "commercial_appeal": min(1.0, commercial_score),
            "animation_potential": min(1.0, animation_score),
            "design_quality": min(1.0, design_score)
        }
    
    def calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        total_score = 0.0
        total_weight = 0.0
        
        for category, data in self.evaluation_criteria.items():
            if category in scores:
                weight = data["weight"]
                total_score += scores[category] * weight
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    async def curate_images(self, image_pairs: List[ImagePair]) -> List[ImagePair]:
        """Curate and score all image pairs"""
        print("🎨 Starting design curation process...")
        print(f"📊 Evaluating {len(image_pairs)} image pairs...")
        
        for i, pair in enumerate(image_pairs):
            print(f"🔍 Analyzing pair {i+1}/{len(image_pairs)}...")
            
            # Get AI analysis
            scores = await self.analyze_with_ai(pair)
            
            # Update the pair with scores
            pair.commercial_appeal = scores["commercial_appeal"]
            pair.animation_potential = scores["animation_potential"]
            pair.quality_score = scores["design_quality"]
            pair.overall_score = self.calculate_overall_score(scores)
            
            print(f"   Commercial Appeal: {pair.commercial_appeal:.2f}")
            print(f"   Animation Potential: {pair.animation_potential:.2f}")
            print(f"   Design Quality: {pair.quality_score:.2f}")
            print(f"   Overall Score: {pair.overall_score:.2f}")
            print()
        
        # Sort by overall score
        image_pairs.sort(key=lambda x: x.overall_score, reverse=True)
        
        return image_pairs
    
    def select_top_pairs(self, image_pairs: List[ImagePair], count: int = 3) -> List[ImagePair]:
        """Select the top N image pairs"""
        return image_pairs[:count]
    
    def generate_mockup_specs(self, top_pairs: List[ImagePair], total_evaluated: int) -> Dict[str, Any]:
        """Generate specifications for creating mockups"""
        mockup_specs = {
            "timestamp": datetime.now().isoformat(),
            "total_evaluated": total_evaluated,
            "top_pairs": [],
            "implementation_notes": {
                "animation_style": "smooth morphing transition",
                "duration": "3-4 seconds loop",
                "easing": "ease-in-out",
                "background": "gradient from red to green",
                "call_to_action": "Create Profile / Log In"
            }
        }
        
        for i, pair in enumerate(top_pairs):
            mockup_spec = {
                "rank": i + 1,
                "before_url": pair.before_url,
                "after_url": pair.after_url,
                "before_description": pair.before_description,
                "after_description": pair.after_description,
                "scores": {
                    "commercial_appeal": pair.commercial_appeal,
                    "animation_potential": pair.animation_potential,
                    "design_quality": pair.quality_score,
                    "overall": pair.overall_score
                },
                "implementation_suggestions": self.generate_implementation_suggestions(pair)
            }
            mockup_specs["top_pairs"].append(mockup_spec)
        
        return mockup_specs
    
    def generate_implementation_suggestions(self, pair: ImagePair) -> List[str]:
        """Generate specific implementation suggestions for an image pair"""
        suggestions = []
        
        if pair.animation_potential > 0.8:
            suggestions.append("Excellent for smooth morphing animation")
        elif pair.animation_potential > 0.6:
            suggestions.append("Good for crossfade or scale transition")
        else:
            suggestions.append("Consider fade-in/fade-out transition")
        
        if pair.commercial_appeal > 0.8:
            suggestions.append("High commercial appeal - perfect for marketing")
        elif pair.commercial_appeal > 0.6:
            suggestions.append("Good commercial appeal - suitable for app")
        else:
            suggestions.append("Consider for internal testing only")
        
        if pair.quality_score > 0.8:
            suggestions.append("High design quality - professional appearance")
        elif pair.quality_score > 0.6:
            suggestions.append("Good design quality - may need minor adjustments")
        else:
            suggestions.append("Consider design improvements before use")
        
        return suggestions
    
    def save_curation_results(self, mockup_specs: Dict[str, Any], output_file: str = "top_image_pairs.json"):
        """Save the curation results"""
        output_path = Path(__file__).parent / output_file
        
        with open(output_path, 'w') as f:
            json.dump(mockup_specs, f, indent=2)
        
        print(f"💾 Saved curation results to {output_path}")

async def main():
    """Main execution function"""
    print("🎨 Weight Tracker Design Curation Agent")
    print("=" * 50)
    
    # Load image pairs from sourcing agent
    input_file = Path(__file__).parent / "image_pairs.json"
    if not input_file.exists():
        print("❌ No image_pairs.json found. Run the image sourcing agent first.")
        return
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Convert to ImagePair objects
    image_pairs = []
    for pair_data in data["pairs"]:
        pair = ImagePair(
            before_url=pair_data["before_url"],
            after_url=pair_data["after_url"],
            before_description=pair_data["before_description"],
            after_description=pair_data["after_description"],
            source=pair_data["source"]
        )
        image_pairs.append(pair)
    
    print(f"📁 Loaded {len(image_pairs)} image pairs for curation")
    
    agent = DesignCurationAgent()
    
    try:
        # Curate images
        curated_pairs = await agent.curate_images(image_pairs)
        
        # Select top 3
        top_pairs = agent.select_top_pairs(curated_pairs, 3)
        
        # Generate mockup specifications
        mockup_specs = agent.generate_mockup_specs(top_pairs, total_evaluated=len(curated_pairs))
        
        # Save results
        agent.save_curation_results(mockup_specs)
        
        print(f"\n✅ Curation complete!")
        print(f"🏆 Top 3 image pairs selected:")
        for i, pair in enumerate(top_pairs):
            print(f"   {i+1}. Overall Score: {pair.overall_score:.2f}")
            print(f"      Commercial: {pair.commercial_appeal:.2f}, Animation: {pair.animation_potential:.2f}, Design: {pair.quality_score:.2f}")
        
        print(f"\n📁 Results saved to top_image_pairs.json")
        print("🎯 Next step: Create animated mockups with the top 3 pairs.")
        
    except Exception as e:
        print(f"❌ Error during curation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import os
    from datetime import datetime
    asyncio.run(main())
