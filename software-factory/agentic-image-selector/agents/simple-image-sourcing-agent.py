#!/usr/bin/env python3
"""
Simple Image Sourcing Agent for Agentic Image Selector

This is a simplified version that works without complex dependencies,
using direct API calls to open source image repositories.
"""

import asyncio
import json
import os
import sys
import argparse
import aiohttp
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

def load_env_file(env_file_path):
    """Load environment variables from a file"""
    env_file = Path(env_file_path)
    if not env_file.exists():
        print(f"❌ Environment file not found: {env_file}")
        return False
    
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                os.environ[key] = value
    
    return True

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

class SimpleImageSourcingAgent:
    """Simple agent that sources images directly from open source APIs"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.project_type = config.get("projectType", "unknown")
        self.search_queries = config.get("searchQueries", [])
        self.image_count = config.get("imageCount", 100)
        self.image_pairs: List[ImagePair] = []
        
        # API keys
        self.unsplash_key = os.getenv("UNSPLASH_API_KEY")
        self.pixabay_key = os.getenv("PIXABAY_API_KEY")
        self.pexels_key = os.getenv("PEXELS_API_KEY")
    
    async def search_unsplash(self, query: str, count: int = 10) -> List[Dict]:
        """Search Unsplash for images"""
        if not self.unsplash_key:
            print("⚠️ Unsplash API key not configured")
            return []
        
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.unsplash.com/search/photos"
                params = {
                    "query": f"{query} fitness transformation cartoon",
                    "per_page": min(count, 30),
                    "orientation": "landscape"
                }
                headers = {"Authorization": f"Client-ID {self.unsplash_key}"}
                
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = []
                        for photo in data.get("results", []):
                            results.append({
                                "url": photo["urls"]["regular"],
                                "thumbnail": photo["urls"]["thumb"],
                                "description": photo.get("alt_description", ""),
                                "title": photo.get("description", ""),
                                "author": photo["user"]["name"],
                                "source": "unsplash"
                            })
                        return results
                    else:
                        print(f"Unsplash API error: {response.status}")
                        return []
        except Exception as e:
            print(f"Error searching Unsplash: {e}")
            return []
    
    async def search_pixabay(self, query: str, count: int = 10) -> List[Dict]:
        """Search Pixabay for images"""
        if not self.pixabay_key:
            print("⚠️ Pixabay API key not configured")
            return []
        
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://pixabay.com/api/"
                params = {
                    "key": self.pixabay_key,
                    "q": f"{query} fitness transformation cartoon",
                    "per_page": min(count, 200),
                    "image_type": "illustration",
                    "category": "backgrounds",
                    "safesearch": "true"
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = []
                        for hit in data.get("hits", []):
                            results.append({
                                "url": hit["webformatURL"],
                                "thumbnail": hit["previewURL"],
                                "description": hit.get("tags", ""),
                                "title": hit.get("tags", ""),
                                "author": hit["user"],
                                "source": "pixabay"
                            })
                        return results
                    else:
                        print(f"Pixabay API error: {response.status}")
                        return []
        except Exception as e:
            print(f"Error searching Pixabay: {e}")
            return []
    
    async def search_pexels(self, query: str, count: int = 10) -> List[Dict]:
        """Search Pexels for images"""
        if not self.pexels_key:
            print("⚠️ Pexels API key not configured")
            return []
        
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.pexels.com/v1/search"
                params = {
                    "query": f"{query} fitness transformation cartoon",
                    "per_page": min(count, 80),
                    "orientation": "landscape"
                }
                headers = {"Authorization": self.pexels_key}
                
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = []
                        for photo in data.get("photos", []):
                            results.append({
                                "url": photo["src"]["large"],
                                "thumbnail": photo["src"]["medium"],
                                "description": photo.get("alt", ""),
                                "title": f"Photo by {photo['photographer']}",
                                "author": photo["photographer"],
                                "source": "pexels"
                            })
                        return results
                    else:
                        print(f"Pexels API error: {response.status}")
                        return []
        except Exception as e:
            print(f"Error searching Pexels: {e}")
            return []
    
    def create_image_pairs(self, images: List[Dict]) -> List[ImagePair]:
        """Create before/after image pairs from search results"""
        pairs = []
        
        # Simple pairing: take every two images as a pair
        for i in range(0, len(images) - 1, 2):
            if i + 1 < len(images):
                before_img = images[i]
                after_img = images[i + 1]
                
                pair = ImagePair(
                    before_url=before_img["url"],
                    after_url=after_img["url"],
                    before_description=f"{before_img['title']} - {before_img['description']}",
                    after_description=f"{after_img['title']} - {after_img['description']}",
                    source=f"{before_img['source']},{after_img['source']}",
                    project_type=self.project_type,
                    quality_score=0.7,  # Default score
                    commercial_appeal=0.6,
                    animation_potential=0.8
                )
                pairs.append(pair)
        
        return pairs
    
    async def source_images(self) -> List[ImagePair]:
        """Main method to source images from all available APIs"""
        print(f"🎯 Starting image sourcing for {self.project_type} project...")
        print(f"📊 Target: {self.image_count} image pairs")
        print(f"🔍 Search queries: {len(self.search_queries)}")
        
        all_images = []
        
        # Search each API
        for query in self.search_queries[:3]:  # Use first 3 queries
            print(f"\n🔍 Searching for: '{query}'")
            
            # Search Unsplash
            unsplash_results = await self.search_unsplash(query, 10)
            all_images.extend(unsplash_results)
            print(f"   Unsplash: {len(unsplash_results)} images")
            
            # Search Pixabay
            pixabay_results = await self.search_pixabay(query, 10)
            all_images.extend(pixabay_results)
            print(f"   Pixabay: {len(pixabay_results)} images")
            
            # Search Pexels
            pexels_results = await self.search_pexels(query, 10)
            all_images.extend(pexels_results)
            print(f"   Pexels: {len(pexels_results)} images")
        
        print(f"\n📊 Total images found: {len(all_images)}")
        
        # Create image pairs
        pairs = self.create_image_pairs(all_images)
        print(f"📊 Image pairs created: {len(pairs)}")
        
        self.image_pairs = pairs
        return pairs
    
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
    parser = argparse.ArgumentParser(description="Simple Image Sourcing Agent")
    parser.add_argument("--config", required=True, help="Path to configuration file")
    
    args = parser.parse_args()
    
    # Load environment variables
    env_file = Path(__file__).parent.parent.parent.parent / "utilities" / "env.master"
    if not load_env_file(env_file):
        print("❌ Failed to load environment variables")
        return
    
    # Load configuration
    with open(args.config, 'r') as f:
        config = json.load(f)
    
    print("🚀 Simple Image Sourcing Agent")
    print("=" * 50)
    print(f"Project Type: {config.get('projectType', 'unknown')}")
    print(f"Search Queries: {len(config.get('searchQueries', []))}")
    print(f"Target Pairs: {config.get('imageCount', 100)}")
    
    agent = SimpleImageSourcingAgent(config)
    
    try:
        # Source images
        pairs = await agent.source_images()
        
        if not pairs:
            print("❌ No image pairs found. Check your API keys and try again.")
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
