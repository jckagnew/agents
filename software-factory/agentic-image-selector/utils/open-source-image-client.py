#!/usr/bin/env python3
"""
Open Source Image Client

This module provides direct access to open source image repositories
to ensure copyright compliance and avoid licensing issues.
"""

import asyncio
import aiohttp
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class OpenSourceImage:
    """Represents an image from an open source repository"""
    url: str
    thumbnail_url: str
    title: str
    description: str
    author: str
    license: str
    source: str
    tags: List[str]
    width: int
    height: int

class UnsplashClient:
    """Client for Unsplash API (requires free API key)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("UNSPLASH_API_KEY")
        self.base_url = "https://api.unsplash.com"
        self.headers = {
            "Authorization": f"Client-ID {self.api_key}" if self.api_key else None
        }
    
    async def search_images(self, query: str, count: int = 10) -> List[OpenSourceImage]:
        """Search for images on Unsplash"""
        if not self.api_key:
            print("⚠️ Unsplash API key not provided. Skipping Unsplash search.")
            return []
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/search/photos"
                params = {
                    "query": query,
                    "per_page": min(count, 30),  # Unsplash limit
                    "orientation": "landscape"
                }
                
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        images = []
                        
                        for photo in data.get("results", []):
                            image = OpenSourceImage(
                                url=photo["urls"]["regular"],
                                thumbnail_url=photo["urls"]["thumb"],
                                title=photo.get("alt_description", ""),
                                description=photo.get("description", ""),
                                author=photo["user"]["name"],
                                license="Unsplash License (free for commercial use)",
                                source="unsplash",
                                tags=[tag["title"] for tag in photo.get("tags", [])],
                                width=photo["width"],
                                height=photo["height"]
                            )
                            images.append(image)
                        
                        return images
                    else:
                        print(f"Unsplash API error: {response.status}")
                        return []
        except Exception as e:
            print(f"Error searching Unsplash: {e}")
            return []

class PixabayClient:
    """Client for Pixabay API (requires free API key)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("PIXABAY_API_KEY")
        self.base_url = "https://pixabay.com/api"
    
    async def search_images(self, query: str, count: int = 10) -> List[OpenSourceImage]:
        """Search for images on Pixabay"""
        if not self.api_key:
            print("⚠️ Pixabay API key not provided. Skipping Pixabay search.")
            return []
        
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "key": self.api_key,
                    "q": query,
                    "per_page": min(count, 200),  # Pixabay limit
                    "image_type": "illustration",
                    "category": "backgrounds",
                    "safesearch": "true"
                }
                
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        images = []
                        
                        for hit in data.get("hits", []):
                            image = OpenSourceImage(
                                url=hit["webformatURL"],
                                thumbnail_url=hit["previewURL"],
                                title=hit.get("tags", ""),
                                description=hit.get("tags", ""),
                                author=hit["user"],
                                license="Pixabay License (free for commercial use)",
                                source="pixabay",
                                tags=hit["tags"].split(", "),
                                width=hit["imageWidth"],
                                height=hit["imageHeight"]
                            )
                            images.append(image)
                        
                        return images
                    else:
                        print(f"Pixabay API error: {response.status}")
                        return []
        except Exception as e:
            print(f"Error searching Pixabay: {e}")
            return []

class OpenClipartClient:
    """Client for OpenClipart (no API key required)"""
    
    def __init__(self):
        self.base_url = "https://openclipart.org"
    
    async def search_images(self, query: str, count: int = 10) -> List[OpenSourceImage]:
        """Search for images on OpenClipart"""
        try:
            # OpenClipart doesn't have a public API, so we'll use web scraping
            # For now, return empty list and suggest using other sources
            print("⚠️ OpenClipart search not implemented. Use Unsplash or Pixabay instead.")
            return []
        except Exception as e:
            print(f"Error searching OpenClipart: {e}")
            return []

class OpenSourceImageAggregator:
    """Aggregates images from multiple open source repositories"""
    
    def __init__(self):
        self.unsplash = UnsplashClient()
        self.pixabay = PixabayClient()
        self.openclipart = OpenClipartClient()
    
    async def search_all_sources(self, query: str, count_per_source: int = 10) -> List[OpenSourceImage]:
        """Search all available open source repositories"""
        print(f"🔍 Searching open source repositories for: {query}")
        
        all_images = []
        
        # Search Unsplash
        print("   Searching Unsplash...")
        unsplash_images = await self.unsplash.search_images(query, count_per_source)
        all_images.extend(unsplash_images)
        print(f"   Found {len(unsplash_images)} images from Unsplash")
        
        # Search Pixabay
        print("   Searching Pixabay...")
        pixabay_images = await self.pixabay.search_images(query, count_per_source)
        all_images.extend(pixabay_images)
        print(f"   Found {len(pixabay_images)} images from Pixabay")
        
        # Search OpenClipart
        print("   Searching OpenClipart...")
        openclipart_images = await self.openclipart.search_images(query, count_per_source)
        all_images.extend(openclipart_images)
        print(f"   Found {len(openclipart_images)} images from OpenClipart")
        
        print(f"📊 Total open source images found: {len(all_images)}")
        return all_images
    
    def filter_by_license(self, images: List[OpenSourceImage], license_types: List[str] = None) -> List[OpenSourceImage]:
        """Filter images by license type"""
        if not license_types:
            license_types = ["free for commercial use", "creative commons", "public domain"]
        
        filtered = []
        for image in images:
            if any(license_type.lower() in image.license.lower() for license_type in license_types):
                filtered.append(image)
        
        return filtered
    
    def create_image_pairs(self, images: List[OpenSourceImage], project_type: str) -> List[Dict[str, Any]]:
        """Create before/after image pairs from open source images"""
        pairs = []
        
        # Group images by similarity (simple approach: by tags)
        image_groups = {}
        for image in images:
            # Create a key based on common tags
            key_tags = [tag for tag in image.tags if any(keyword in tag.lower() for keyword in 
                ["before", "after", "start", "end", "beginning", "result", "progress", "transformation"])]
            
            if key_tags:
                key = "_".join(sorted(key_tags))
                if key not in image_groups:
                    image_groups[key] = []
                image_groups[key].append(image)
        
        # Create pairs from groups
        for group_images in image_groups.values():
            if len(group_images) >= 2:
                # Simple pairing: first two images in group
                before_img = group_images[0]
                after_img = group_images[1]
                
                pair = {
                    "before_url": before_img.url,
                    "after_url": after_img.url,
                    "before_description": f"{before_img.title} - {before_img.description}",
                    "after_description": f"{after_img.title} - {after_img.description}",
                    "source": f"{before_img.source},{after_img.source}",
                    "project_type": project_type,
                    "license": f"{before_img.license} | {after_img.license}",
                    "authors": f"{before_img.author} | {after_img.author}",
                    "is_open_source": True,
                    "quality_score": 0.0,
                    "commercial_appeal": 0.0,
                    "animation_potential": 0.0,
                    "overall_score": 0.0
                }
                pairs.append(pair)
        
        return pairs

# Example usage
async def main():
    """Example usage of the open source image client"""
    aggregator = OpenSourceImageAggregator()
    
    # Search for fitness transformation images
    images = await aggregator.search_all_sources("fitness transformation cartoon", 5)
    
    # Filter for commercial use
    commercial_images = aggregator.filter_by_license(images)
    
    # Create image pairs
    pairs = aggregator.create_image_pairs(commercial_images, "fitness")
    
    print(f"Created {len(pairs)} image pairs from open source repositories")
    
    # Save results
    with open("open_source_image_pairs.json", "w") as f:
        json.dump(pairs, f, indent=2)
    
    print("Results saved to open_source_image_pairs.json")

if __name__ == "__main__":
    import os
    asyncio.run(main())
