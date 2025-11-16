#!/usr/bin/env python3
"""
Generic Image Sourcing Agent for Agentic Image Selector

This agent uses MCP servers to source relevant image pairs for any project type
using configurable search queries and evaluation criteria.
"""

import asyncio
import json
import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
import aiohttp
from datetime import datetime

# Add the MCP framework to the path
mcp_path = Path(__file__).parent.parent.parent.parent / "6_mcp"
if mcp_path.exists():
    sys.path.append(str(mcp_path))
    try:
        from agents.mcp import MCPServerStdio
    except ImportError:
        print("⚠️ MCP framework not found, using fallback image sourcing")
        MCPServerStdio = None
else:
    print("⚠️ MCP framework not found, using fallback image sourcing")
    MCPServerStdio = None

# Add utils to the path
utils_path = Path(__file__).parent.parent / "utils"
if utils_path.exists():
    sys.path.append(str(utils_path))
    try:
        from open_source_image_client import OpenSourceImageAggregator
    except ImportError:
        print("⚠️ Open source image client not found, using basic image sourcing")
        OpenSourceImageAggregator = None
else:
    print("⚠️ Utils directory not found, using basic image sourcing")
    OpenSourceImageAggregator = None

@dataclass
class ImagePair:
    """Represents a before/after image pair for any project type"""
    before_url: str
    after_url: str
    before_description: str
    after_description: str
    source: str
    project_type: str
    quality_score: float = 0.0
    commercial_appeal: float = 0.0
    animation_potential: float = 0.0
    overall_score: float = 0.0

class GenericImageSourcingAgent:
    """Generic agent responsible for sourcing image pairs for any project type"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.project_type = config.get("projectType", "unknown")
        self.search_queries = config.get("searchQueries", [])
        self.image_count = config.get("imageCount", 100)
        self.image_pairs: List[ImagePair] = []
        self.open_source_aggregator = OpenSourceImageAggregator() if OpenSourceImageAggregator else None
    
    async def search_with_brave(self, query: str, count: int = 10) -> List[Dict]:
        """Search for images using Brave Search MCP server with open source focus"""
        if MCPServerStdio is None:
            print("⚠️ Brave Search MCP server not available, skipping")
            return []
            
        try:
            # Configure Brave Search MCP server
            brave_params = {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                "env": {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY", "")}
            }
            
            async with MCPServerStdio(params=brave_params) as brave:
                # Search for open source images specifically
                open_source_query = f"{query} site:unsplash.com OR site:pixabay.com OR site:pexels.com OR site:freepik.com OR 'free to use' OR 'creative commons' OR 'public domain' cartoon character animation"
                
                result = await brave.call_tool(
                    "brave_web_search",
                    {
                        "query": open_source_query,
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
        """Search for images using Perplexity MCP server with open source focus"""
        if MCPServerStdio is None:
            print("⚠️ Perplexity MCP server not available, skipping")
            return []
            
        try:
            perplexity_params = {
                "command": "npx",
                "args": ["-y", "@perplexity/mcp-server"],
                "env": {"PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY", "")}
            }
            
            async with MCPServerStdio(params=perplexity_params) as perplexity:
                open_source_query = f"Find high-quality cartoon images from open source repositories (Unsplash, Pixabay, Pexels, Freepik) showing {self.project_type} transformation, progress, or success stories. Only include images that are free to use, creative commons licensed, or public domain. {query}"
                
                result = await perplexity.call_tool(
                    "perplexity_search",
                    {
                        "query": open_source_query,
                        "max_results": 5
                    }
                )
                
                return result.get("results", [])
        except Exception as e:
            print(f"Error with Perplexity search: {e}")
            return []
    
    def is_open_source_image(self, url: str) -> bool:
        """Check if an image URL is from an open source repository"""
        open_source_domains = [
            "unsplash.com",
            "pixabay.com", 
            "pexels.com",
            "freepik.com",
            "openclipart.org",
            "wikimedia.org",
            "commons.wikimedia.org",
            "flickr.com/photos",
            "deviantart.com",
            "behance.net"
        ]
        
        return any(domain in url.lower() for domain in open_source_domains)
    
    def has_open_source_license(self, description: str) -> bool:
        """Check if description mentions open source licensing"""
        license_keywords = [
            "creative commons",
            "public domain",
            "free to use",
            "open source",
            "cc0",
            "cc by",
            "attribution",
            "royalty free",
            "commercial use",
            "no attribution required"
        ]
        
        description_lower = description.lower()
        return any(keyword in description_lower for keyword in license_keywords)

    async def fetch_image_details(self, url: str) -> Dict[str, Any]:
        """Fetch detailed information about an image with open source validation"""
        try:
            # Check if URL is from open source domain
            is_open_source = self.is_open_source_image(url)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        content_type = response.headers.get('content-type', '')
                        size = len(await response.read())
                        return {
                            "url": url,
                            "content_type": content_type,
                            "size": size,
                            "accessible": True,
                            "is_open_source": is_open_source
                        }
        except Exception as e:
            print(f"Error fetching image {url}: {e}")
        
        return {
            "url": url,
            "content_type": "unknown",
            "size": 0,
            "accessible": False,
            "is_open_source": False
        }
    
    def extract_image_pairs(self, search_results: List[Dict]) -> List[ImagePair]:
        """Extract potential image pairs from search results based on project type"""
        pairs = []
        
        # Define project-specific keywords for before/after identification
        before_keywords = {
            "fitness": ["before", "start", "beginning", "unfit", "overweight", "out of shape"],
            "finance": ["poor", "struggling", "debt", "financial stress", "before investment"],
            "productivity": ["disorganized", "chaos", "inefficient", "before system"],
            "ecommerce": ["empty cart", "browsing", "considering", "before purchase"],
            "education": ["beginner", "learning", "studying", "before knowledge"],
            "gaming": ["level 1", "beginner", "starting", "before progress"],
            "social": ["lonely", "isolated", "before connection", "starting network"],
            "custom": ["before", "start", "beginning", "initial"]
        }
        
        after_keywords = {
            "fitness": ["after", "result", "transformed", "fit", "muscular", "healthy"],
            "finance": ["wealthy", "successful", "prosperous", "after investment", "financial freedom"],
            "productivity": ["organized", "efficient", "systematic", "after system"],
            "ecommerce": ["purchased", "satisfied", "happy customer", "after purchase"],
            "education": ["expert", "knowledgeable", "graduated", "after learning"],
            "gaming": ["level up", "advanced", "achievement", "after progress"],
            "social": ["connected", "popular", "after network", "social success"],
            "custom": ["after", "result", "success", "achieved"]
        }
        
        project_before = before_keywords.get(self.project_type, before_keywords["custom"])
        project_after = after_keywords.get(self.project_type, after_keywords["custom"])
        
        for result in search_results:
            # Look for image URLs in the result
            images = result.get("images", [])
            if not images:
                continue
            
            # Try to find pairs based on titles and descriptions
            title = result.get("title", "").lower()
            description = result.get("description", "").lower()
            
            is_before = any(keyword in title or keyword in description for keyword in project_before)
            is_after = any(keyword in title or keyword in description for keyword in project_after)
            
            if is_before or is_after:
                for img in images:
                    if img.get("src"):
                        pair = ImagePair(
                            before_url=img["src"] if is_before else "",
                            after_url=img["src"] if is_after else "",
                            before_description=description if is_before else "",
                            after_description=description if is_after else "",
                            source=result.get("url", ""),
                            project_type=self.project_type,
                            quality_score=0.0,
                            commercial_appeal=0.0,
                            animation_potential=0.0
                        )
                        pairs.append(pair)
        
        return pairs
    
    async def source_from_open_repositories(self) -> List[ImagePair]:
        """Source images directly from open source repositories"""
        if self.open_source_aggregator is None:
            print("⚠️ Open source aggregator not available, skipping direct repository search")
            return []
            
        print("🎯 Sourcing images from open source repositories...")
        
        all_images = []
        
        # Search all open source repositories
        for query in self.search_queries[:3]:  # Use first 3 queries for open source
            images = await self.open_source_aggregator.search_all_sources(query, 10)
            all_images.extend(images)
            print(f"   Query '{query}': Found {len(images)} open source images")
        
        # Filter for commercial use
        commercial_images = self.open_source_aggregator.filter_by_license(all_images)
        print(f"📊 Commercial use images: {len(commercial_images)}")
        
        # Create image pairs
        pair_data = self.open_source_aggregator.create_image_pairs(commercial_images, self.project_type)
        
        # Convert to ImagePair objects
        pairs = []
        for pair_dict in pair_data:
            pair = ImagePair(
                before_url=pair_dict["before_url"],
                after_url=pair_dict["after_url"],
                before_description=pair_dict["before_description"],
                after_description=pair_dict["after_description"],
                source=pair_dict["source"],
                project_type=pair_dict["project_type"],
                quality_score=0.0,
                commercial_appeal=0.0,
                animation_potential=0.0
            )
            pairs.append(pair)
        
        return pairs

    async def source_images(self) -> List[ImagePair]:
        """Main method to source images from open source repositories and MCP servers"""
        print(f"🎯 Starting image sourcing for {self.project_type} project...")
        print(f"📊 Target: {self.image_count} image pairs")
        print(f"🔍 Search queries: {len(self.search_queries)}")
        
        all_pairs = []
        
        # Primary: Search open source repositories
        print("🌟 PRIMARY: Searching open source repositories...")
        open_source_pairs = await self.source_from_open_repositories()
        all_pairs.extend(open_source_pairs)
        print(f"   Found {len(open_source_pairs)} pairs from open source repositories")
        
        # Secondary: Search with MCP servers (as backup)
        if len(all_pairs) < self.image_count // 2:  # If we don't have enough open source pairs
            print("🔍 SECONDARY: Searching with MCP servers (open source focus)...")
            
            # Search with Brave
            for i, query in enumerate(self.search_queries[:3]):  # Use first 3 queries
                results = await self.search_with_brave(query, count=5)
                pairs = self.extract_image_pairs(results)
                all_pairs.extend(pairs)
                print(f"   Brave Query {i+1}: Found {len(pairs)} potential pairs for '{query}'")
            
            # Search with Perplexity
            for i, query in enumerate(self.search_queries[3:6]):  # Use next 3 queries
                results = await self.search_with_perplexity(query)
                pairs = self.extract_image_pairs(results)
                all_pairs.extend(pairs)
                print(f"   Perplexity Query {i+4}: Found {len(pairs)} potential pairs for '{query}'")
        
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
        
        # Validate image accessibility and open source licensing
        print("🔍 Validating image accessibility and open source licensing...")
        validated_pairs = []
        
        # Limit validation to avoid timeout
        validation_limit = min(50, len(unique_pairs))
        
        for pair in unique_pairs[:validation_limit]:
            before_details = await self.fetch_image_details(pair.before_url)
            after_details = await self.fetch_image_details(pair.after_url)
            
            # Check if both images are accessible and from open source
            both_accessible = before_details["accessible"] and after_details["accessible"]
            both_open_source = before_details.get("is_open_source", False) and after_details.get("is_open_source", False)
            
            # Also check if descriptions mention open source licensing
            before_has_license = self.has_open_source_license(pair.before_description)
            after_has_license = self.has_open_source_license(pair.after_description)
            
            if both_accessible and (both_open_source or before_has_license or after_has_license):
                validated_pairs.append(pair)
                source_type = "Open Source" if both_open_source else "Licensed"
                print(f"   ✅ Validated {source_type} pair: {pair.before_description[:50]}...")
            else:
                print(f"   ❌ Invalid pair (not open source): {pair.before_url}")
        
        self.image_pairs = validated_pairs
        return validated_pairs
    
    def save_results(self, output_file: str = "image_pairs.json"):
        """Save the sourced image pairs to a JSON file"""
        output_path = Path(__file__).parent / output_file
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "project_type": self.project_type,
            "total_pairs": len(self.image_pairs),
            "config": self.config,
            "pairs": [
                {
                    "before_url": pair.before_url,
                    "after_url": pair.after_url,
                    "before_description": pair.before_description,
                    "after_description": pair.after_description,
                    "source": pair.source,
                    "project_type": pair.project_type,
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
    parser = argparse.ArgumentParser(description="Generic Image Sourcing Agent")
    parser.add_argument("--config", required=True, help="Path to configuration file")
    
    args = parser.parse_args()
    
    # Load configuration
    with open(args.config, 'r') as f:
        config = json.load(f)
    
    print("🚀 Generic Image Sourcing Agent")
    print("=" * 50)
    print(f"Project Type: {config.get('projectType', 'unknown')}")
    print(f"Search Queries: {len(config.get('searchQueries', []))}")
    print(f"Target Pairs: {config.get('imageCount', 100)}")
    
    agent = GenericImageSourcingAgent(config)
    
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
