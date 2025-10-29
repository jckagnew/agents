#!/usr/bin/env python3
"""
Weight Tracker Splash Screen Image Sourcing Agent

This agent uses MCP servers to source and curate before/after fitness cartoon images
for the Weight Tracker splash screen animation.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
import aiohttp
import base64
from datetime import datetime

# Add the MCP framework to the path
REPO_ROOT = Path(__file__).resolve().parents[4]
MCP_PATH = REPO_ROOT / "6_mcp"

if MCP_PATH.exists():
    sys.path.append(str(MCP_PATH))
    try:
        from agents.mcp import MCPServerStdio  # type: ignore
    except ImportError:
        print("⚠️ MCP framework not available; falling back to offline image sourcing.")
        MCPServerStdio = None  # type: ignore
else:
    print("⚠️ MCP framework directory not found; using offline image sourcing.")
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

class ImageSourcingAgent:
    """Agent responsible for sourcing fitness cartoon images using MCP servers"""
    
    def __init__(self):
        self.image_pairs: List[ImagePair] = []
        self.search_queries = [
            "cartoon fitness transformation before after",
            "animated character weight loss journey",
            "cartoon person getting fit transformation",
            "before after fitness cartoon character",
            "animated weight loss success story",
            "cartoon fitness journey progression",
            "character transformation fitness cartoon",
            "animated before after weight loss",
            "cartoon fitness motivation transformation",
            "character getting in shape cartoon"
        ]
    
    async def search_with_brave(self, query: str, count: int = 10) -> List[Dict]:
        """Search for images using Brave Search MCP server"""
        try:
            # Configure Brave Search MCP server
            brave_params = {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                "env": {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY", "")}
            }
            
            async with MCPServerStdio(params=brave_params) as brave:
                # Search for images
                result = await brave.call_tool(
                    "brave_web_search",
                    {
                        "query": f"{query} cartoon fitness transformation",
                        "count": count,
                        "search_lang": "en",
                        "country": "US",
                        "safesearch": "moderate"
                    }
                )
                
                return result.get("results", [])
        except Exception as e:
            print(f"Error with Brave search: {e}")
            return []
    
    async def search_with_perplexity(self, query: str) -> List[Dict]:
        """Search for images using Perplexity MCP server"""
        try:
            perplexity_params = {
                "command": "npx",
                "args": ["-y", "@perplexity/mcp-server"],
                "env": {"PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY", "")}
            }
            
            async with MCPServerStdio(params=perplexity_params) as perplexity:
                result = await perplexity.call_tool(
                    "perplexity_search",
                    {
                        "query": f"Find high-quality cartoon images showing fitness transformation before and after. {query}",
                        "max_results": 5
                    }
                )
                
                return result.get("results", [])
        except Exception as e:
            print(f"Error with Perplexity search: {e}")
            return []
    
    async def fetch_image_details(self, url: str) -> Dict[str, Any]:
        """Fetch detailed information about an image"""
        if url.startswith("data:image"):
            return {
                "url": url,
                "content_type": "image/svg+xml",
                "size": len(url),
                "accessible": True
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        content_type = response.headers.get('content-type', '')
                        size = len(await response.read())
                        return {
                            "url": url,
                            "content_type": content_type,
                            "size": size,
                            "accessible": True
                        }
        except Exception as e:
            print(f"Error fetching image {url}: {e}")
        
        return {
            "url": url,
            "content_type": "unknown",
            "size": 0,
            "accessible": False
        }
    
    def extract_image_pairs(self, search_results: List[Dict]) -> List[ImagePair]:
        """Extract potential before/after image pairs from search results"""
        pairs = []
        
        for result in search_results:
            # Look for image URLs in the result
            images = [
                img for img in result.get("images", [])
                if isinstance(img, dict) and img.get("src")
            ]
            if len(images) < 2:
                continue
            
            description = result.get("description", "")
            source = result.get("url", "")
            
            # Pair images in twos: (0,1), (2,3), ...
            for i in range(0, len(images) - 1, 2):
                before_img = images[i]
                after_img = images[i + 1]
                pair = ImagePair(
                    before_url=before_img["src"],
                    after_url=after_img["src"],
                    before_description=before_img.get("alt", description),
                    after_description=after_img.get("alt", description),
                    source=source,
                    quality_score=0.0,
                    commercial_appeal=0.0,
                    animation_potential=0.0
                )
                pairs.append(pair)
        
        return pairs
    
    def _svg_data_uri(self, headline: str, subline: str, start_color: str, end_color: str) -> str:
        """Generate a data URI for a simple SVG card"""
        svg_template = f"""
<svg xmlns='http://www.w3.org/2000/svg' width='600' height='800'>
  <defs>
    <linearGradient id='grad' x1='0%' y1='0%' x2='0%' y2='100%'>
      <stop offset='0%' stop-color='{start_color}'/>
      <stop offset='100%' stop-color='{end_color}'/>
    </linearGradient>
  </defs>
  <rect width='600' height='800' rx='48' fill='url(#grad)'/>
  <text x='50%' y='45%' dominant-baseline='middle' text-anchor='middle'
        font-family='Poppins, Helvetica, Arial' font-size='48' fill='white' font-weight='700'>
    {headline}
  </text>
  <text x='50%' y='58%' dominant-baseline='middle' text-anchor='middle'
        font-family='Nunito, Helvetica, Arial' font-size='28' fill='rgba(255,255,255,0.92)'>
    {subline}
  </text>
</svg>"""
        encoded = base64.b64encode(svg_template.encode("utf-8")).decode("utf-8")
        return f"data:image/svg+xml;base64,{encoded}"
    
    def get_offline_pairs(self) -> List[ImagePair]:
        """Return a deterministic set of splash-friendly image pairs"""
        headline_pairs = [
            ("Day One", "Start your journey"),
            ("Momentum", "Small wins add up"),
            ("Confidence", "Feel the change"),
        ]
        
        offline_pairs = []
        for idx, (before_headline, before_sub) in enumerate(headline_pairs):
            after_headline = "Next Milestone"
            after_sub = ["Keep building habits", "Celebrate every rep", "You earned it"][idx]
            before_uri = self._svg_data_uri(before_headline, before_sub, "#111827", "#1F2937")
            after_uri = self._svg_data_uri(after_headline, after_sub, "#22C55E", "#16A34A")
            
            offline_pairs.append(
                ImagePair(
                    before_url=before_uri,
                    after_url=after_uri,
                    before_description=f"{before_headline} – {before_sub}",
                    after_description=f"{after_headline} – {after_sub}",
                    source="offline-library",
                    quality_score=0.0,
                    commercial_appeal=0.0,
                    animation_potential=0.0
                )
            )
        
        return offline_pairs
    
    async def source_images(self) -> List[ImagePair]:
        """Main method to source images from all available MCP servers"""
        print("🎯 Starting image sourcing process...")

        if MCPServerStdio is None:
            print("⚠️ MCP servers unavailable. Falling back to offline creative library.")
            self.image_pairs = self.get_offline_pairs()
            print(f"📊 Loaded {len(self.image_pairs)} offline image pairs.")
            return self.image_pairs
        
        all_pairs = []
        
        # Search with Brave
        print("🔍 Searching with Brave Search...")
        for query in self.search_queries[:5]:  # Use first 5 queries
            results = await self.search_with_brave(query, count=10)
            pairs = self.extract_image_pairs(results)
            all_pairs.extend(pairs)
            print(f"   Found {len(pairs)} potential pairs for query: {query}")
        
        # Search with Perplexity
        print("🤖 Searching with Perplexity...")
        for query in self.search_queries[5:]:  # Use remaining queries
            results = await self.search_with_perplexity(query)
            pairs = self.extract_image_pairs(results)
            all_pairs.extend(pairs)
            print(f"   Found {len(pairs)} potential pairs for query: {query}")
        
        # Remove duplicates and validate
        unique_pairs = []
        seen_urls = set()
        
        for pair in all_pairs:
            if pair.before_url and pair.after_url:
                key = f"{pair.before_url}_{pair.after_url}"
                if key not in seen_urls:
                    seen_urls.add(key)
                    unique_pairs.append(pair)
        
        print(f"📊 Total unique image pairs found: {len(unique_pairs)}")
        
        # Validate image accessibility
        print("🔍 Validating image accessibility...")
        validated_pairs = []
        
        for pair in unique_pairs[:50]:  # Limit to first 50 for validation
            before_details = await self.fetch_image_details(pair.before_url)
            after_details = await self.fetch_image_details(pair.after_url)
            
            if before_details["accessible"] and after_details["accessible"]:
                validated_pairs.append(pair)
                print(f"   ✅ Validated pair: {pair.before_description[:50]}...")
            else:
                print(f"   ❌ Invalid pair: {pair.before_url}")
        
        if not validated_pairs:
            print("⚠️ No validated image pairs found. Using offline creative library as fallback.")
            validated_pairs = self.get_offline_pairs()
        
        self.image_pairs = validated_pairs
        return validated_pairs
    
    def save_results(self, output_file: str = "image_pairs.json"):
        """Save the sourced image pairs to a JSON file"""
        output_path = Path(__file__).parent / output_file
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "total_pairs": len(self.image_pairs),
            "pairs": [
                {
                    "before_url": pair.before_url,
                    "after_url": pair.after_url,
                    "before_description": pair.before_description,
                    "after_description": pair.after_description,
                    "source": pair.source,
                    "quality_score": pair.quality_score,
                    "commercial_appeal": pair.commercial_appeal,
                    "animation_potential": pair.animation_potential,
                    "overall_score": pair.overall_score
                }
                for pair in self.image_pairs
            ]
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Saved {len(self.image_pairs)} image pairs to {output_path}")

async def main():
    """Main execution function"""
    print("🚀 Weight Tracker Image Sourcing Agent")
    print("=" * 50)
    
    agent = ImageSourcingAgent()
    
    try:
        # Source images
        pairs = await agent.source_images()
        
        if not pairs:
            print("❌ No valid image pairs found. Check your MCP server configurations.")
            return
        
        # Save results
        agent.save_results()
        
        print(f"\n✅ Successfully sourced {len(pairs)} image pairs!")
        print("📁 Results saved to image_pairs.json")
        print("\n🎯 Next step: Run the design curation agent to select the top 3 pairs.")
        
    except Exception as e:
        print(f"❌ Error during image sourcing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
