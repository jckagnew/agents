#!/usr/bin/env python3
"""
Canva Design Generation Agent
AI-powered design creation using Canva's API and AI capabilities
"""

import os
import json
import asyncio
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum
import requests
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DesignFormat(Enum):
    PNG = "png"
    PDF = "pdf"
    SVG = "svg"
    JPG = "jpg"

class Platform(Enum):
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    WEB = "web"
    PRINT = "print"

@dataclass
class DesignRequest:
    """Request for design generation"""
    content_type: str
    platform: Platform
    brand_guidelines: Dict
    content: str
    dimensions: Optional[Dict] = None
    style: Optional[str] = None
    quantity: int = 1
    variations: Optional[List[str]] = None

@dataclass
class GeneratedDesign:
    """Generated design result"""
    design_id: str
    url: str
    format: DesignFormat
    platform: Platform
    dimensions: Dict
    file_size: int
    created_at: datetime
    metadata: Dict

class CanvaDesignAgent:
    """AI-powered design generation agent using Canva API"""
    
    def __init__(self, 
                 api_key: str = None,
                 team_id: str = None,
                 brand_kit_id: str = None,
                 output_dir: str = "./generated_designs"):
        """
        Initialize Canva Design Agent
        
        Args:
            api_key: Canva API key
            team_id: Canva team ID
            brand_kit_id: Brand kit ID for consistent branding
            output_dir: Directory to save generated designs
        """
        self.api_key = api_key or os.getenv("CANVA_API_KEY")
        self.team_id = team_id or os.getenv("CANVA_TEAM_ID")
        self.brand_kit_id = brand_kit_id or os.getenv("CANVA_BRAND_KIT_ID")
        self.output_dir = output_dir
        
        if not self.api_key:
            raise ValueError("Canva API key is required")
        
        self.base_url = "https://api.canva.com/rest/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load platform specifications
        self.platform_specs = self._load_platform_specs()
        
    def _load_platform_specs(self) -> Dict:
        """Load platform-specific design specifications"""
        return {
            Platform.INSTAGRAM: {
                "post": {"width": 1080, "height": 1080},
                "story": {"width": 1080, "height": 1920},
                "reel": {"width": 1080, "height": 1920}
            },
            Platform.FACEBOOK: {
                "post": {"width": 1200, "height": 630},
                "cover": {"width": 1200, "height": 315},
                "story": {"width": 1080, "height": 1920}
            },
            Platform.LINKEDIN: {
                "post": {"width": 1200, "height": 627},
                "cover": {"width": 1584, "height": 396},
                "article": {"width": 1200, "height": 627}
            },
            Platform.TWITTER: {
                "post": {"width": 1200, "height": 675},
                "header": {"width": 1500, "height": 500}
            }
        }
    
    async def generate_social_media_designs(self, 
                                          platform: Platform,
                                          content_type: str,
                                          content: str,
                                          quantity: int = 1,
                                          variations: List[str] = None,
                                          style: str = "modern") -> List[GeneratedDesign]:
        """
        Generate social media designs for specific platform
        
        Args:
            platform: Target social media platform
            content_type: Type of content (post, story, cover, etc.)
            content: Text content for the design
            quantity: Number of designs to generate
            variations: List of variation types
            style: Design style preference
            
        Returns:
            List of generated designs
        """
        logger.info(f"Generating {quantity} {content_type} designs for {platform.value}")
        
        # Get platform specifications
        platform_spec = self.platform_specs.get(platform, {})
        dimensions = platform_spec.get(content_type, {"width": 1200, "height": 630})
        
        designs = []
        for i in range(quantity):
            try:
                # Create design request
                design_request = DesignRequest(
                    content_type=content_type,
                    platform=platform,
                    brand_guidelines=self._get_brand_guidelines(),
                    content=content,
                    dimensions=dimensions,
                    style=style,
                    variations=variations
                )
                
                # Generate design
                design = await self._create_design(design_request)
                designs.append(design)
                
                logger.info(f"Generated design {i+1}/{quantity}: {design.design_id}")
                
            except Exception as e:
                logger.error(f"Failed to generate design {i+1}: {str(e)}")
                continue
        
        return designs
    
    async def generate_marketing_assets(self,
                                      campaign_name: str,
                                      products: List[str],
                                      platforms: List[Platform],
                                      output_formats: List[DesignFormat] = None) -> Dict[str, List[GeneratedDesign]]:
        """
        Generate marketing assets for a campaign
        
        Args:
            campaign_name: Name of the marketing campaign
            products: List of products to feature
            platforms: List of target platforms
            output_formats: Desired output formats
            
        Returns:
            Dictionary of platform -> designs mapping
        """
        logger.info(f"Generating marketing assets for campaign: {campaign_name}")
        
        if not output_formats:
            output_formats = [DesignFormat.PNG, DesignFormat.PDF]
        
        campaign_designs = {}
        
        for platform in platforms:
            platform_designs = []
            
            # Generate product showcase designs
            for product in products:
                content = f"{campaign_name}: {product}"
                
                designs = await self.generate_social_media_designs(
                    platform=platform,
                    content_type="post",
                    content=content,
                    quantity=2,
                    variations=["product_showcase", "lifestyle"]
                )
                
                platform_designs.extend(designs)
            
            # Generate campaign banner
            banner_designs = await self.generate_social_media_designs(
                platform=platform,
                content_type="cover",
                content=campaign_name,
                quantity=1,
                variations=["banner"]
            )
            
            platform_designs.extend(banner_designs)
            campaign_designs[platform.value] = platform_designs
        
        return campaign_designs
    
    async def generate_data_visualizations(self,
                                         data: Dict,
                                         chart_types: List[str],
                                         title: str = "Data Visualization") -> List[GeneratedDesign]:
        """
        Generate data visualization designs
        
        Args:
            data: Data to visualize
            chart_types: Types of charts to create
            title: Title for the visualization
            
        Returns:
            List of generated chart designs
        """
        logger.info(f"Generating data visualizations: {chart_types}")
        
        designs = []
        
        for chart_type in chart_types:
            try:
                # Create chart design request
                chart_request = DesignRequest(
                    content_type="chart",
                    platform=Platform.WEB,
                    brand_guidelines=self._get_brand_guidelines(),
                    content=title,
                    dimensions={"width": 1200, "height": 800},
                    style="data_visualization"
                )
                
                # Generate chart design
                design = await self._create_chart_design(chart_request, data, chart_type)
                designs.append(design)
                
                logger.info(f"Generated {chart_type} chart: {design.design_id}")
                
            except Exception as e:
                logger.error(f"Failed to generate {chart_type} chart: {str(e)}")
                continue
        
        return designs
    
    async def _create_design(self, request: DesignRequest) -> GeneratedDesign:
        """Create a single design using Canva API"""
        
        # Prepare design parameters
        design_params = {
            "content_type": request.content_type,
            "platform": request.platform.value,
            "dimensions": request.dimensions,
            "content": request.content,
            "style": request.style,
            "brand_kit_id": self.brand_kit_id
        }
        
        # Make API request to create design
        response = requests.post(
            f"{self.base_url}/designs",
            headers=self.headers,
            json=design_params
        )
        
        if response.status_code != 201:
            raise Exception(f"Failed to create design: {response.text}")
        
        design_data = response.json()
        
        # Create GeneratedDesign object
        design = GeneratedDesign(
            design_id=design_data["id"],
            url=design_data["url"],
            format=DesignFormat.PNG,  # Default format
            platform=request.platform,
            dimensions=request.dimensions,
            file_size=design_data.get("file_size", 0),
            created_at=datetime.now(),
            metadata=design_data.get("metadata", {})
        )
        
        return design
    
    async def _create_chart_design(self, request: DesignRequest, data: Dict, chart_type: str) -> GeneratedDesign:
        """Create a chart design using Canva API"""
        
        # Prepare chart parameters
        chart_params = {
            "content_type": "chart",
            "chart_type": chart_type,
            "data": data,
            "dimensions": request.dimensions,
            "title": request.content,
            "brand_kit_id": self.brand_kit_id
        }
        
        # Make API request to create chart
        response = requests.post(
            f"{self.base_url}/charts",
            headers=self.headers,
            json=chart_params
        )
        
        if response.status_code != 201:
            raise Exception(f"Failed to create chart: {response.text}")
        
        chart_data = response.json()
        
        # Create GeneratedDesign object
        design = GeneratedDesign(
            design_id=chart_data["id"],
            url=chart_data["url"],
            format=DesignFormat.PNG,
            platform=request.platform,
            dimensions=request.dimensions,
            file_size=chart_data.get("file_size", 0),
            created_at=datetime.now(),
            metadata={
                "chart_type": chart_type,
                "data_points": len(data.get("values", [])),
                **chart_data.get("metadata", {})
            }
        )
        
        return design
    
    def _get_brand_guidelines(self) -> Dict:
        """Get brand guidelines from configuration"""
        try:
            with open("config/brand_guidelines.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Brand guidelines not found, using defaults")
            return {
                "colors": {"primary": "#1a73e8", "secondary": "#34a853"},
                "fonts": {"primary": "Roboto", "secondary": "Open Sans"}
            }
    
    async def download_design(self, design: GeneratedDesign, format: DesignFormat = None) -> str:
        """Download design to local file system"""
        
        if not format:
            format = design.format
        
        # Prepare download request
        download_params = {
            "format": format.value,
            "quality": "high"
        }
        
        # Make API request to download design
        response = requests.get(
            f"{self.base_url}/designs/{design.design_id}/download",
            headers=self.headers,
            params=download_params
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to download design: {response.text}")
        
        # Save file
        filename = f"{design.design_id}_{design.platform.value}_{design.content_type}.{format.value}"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        logger.info(f"Downloaded design: {filepath}")
        return filepath
    
    async def batch_download(self, designs: List[GeneratedDesign], format: DesignFormat = None) -> List[str]:
        """Download multiple designs in batch"""
        
        download_tasks = [self.download_design(design, format) for design in designs]
        filepaths = await asyncio.gather(*download_tasks, return_exceptions=True)
        
        # Filter out exceptions
        successful_downloads = [fp for fp in filepaths if isinstance(fp, str)]
        
        logger.info(f"Downloaded {len(successful_downloads)}/{len(designs)} designs")
        return successful_downloads

# Example usage
async def main():
    """Example usage of Canva Design Agent"""
    
    # Initialize agent
    agent = CanvaDesignAgent(
        api_key=os.getenv("CANVA_API_KEY"),
        team_id=os.getenv("CANVA_TEAM_ID"),
        brand_kit_id=os.getenv("CANVA_BRAND_KIT_ID")
    )
    
    # Generate social media designs
    designs = await agent.generate_social_media_designs(
        platform=Platform.INSTAGRAM,
        content_type="post",
        content="Check out our new product!",
        quantity=3,
        variations=["product_showcase", "lifestyle", "testimonial"]
    )
    
    # Download designs
    filepaths = await agent.batch_download(designs)
    
    print(f"Generated {len(designs)} designs")
    print(f"Downloaded to: {filepaths}")

if __name__ == "__main__":
    asyncio.run(main())

