#!/usr/bin/env python3
"""
Canva Marketing Campaign Example
Demonstrates automated marketing asset generation using Canva AI workflows
"""

import asyncio
import os
import json
from datetime import datetime
from typing import List, Dict

# Import Canva agents
from canva_design_agent import CanvaDesignAgent, Platform, DesignFormat
from canva_brand_agent import CanvaBrandAgent
from canva_analytics_agent import CanvaAnalyticsAgent

class MarketingCampaignManager:
    """Manages end-to-end marketing campaign creation using Canva AI workflows"""
    
    def __init__(self, campaign_name: str, brand_guidelines_path: str = "config/brand_guidelines.json"):
        self.campaign_name = campaign_name
        self.brand_guidelines_path = brand_guidelines_path
        self.campaign_data = {}
        
        # Initialize agents
        self.design_agent = CanvaDesignAgent(
            api_key=os.getenv("CANVA_API_KEY"),
            team_id=os.getenv("CANVA_TEAM_ID"),
            brand_kit_id=os.getenv("CANVA_BRAND_KIT_ID"),
            output_dir=f"./campaigns/{campaign_name}"
        )
        
        self.brand_agent = CanvaBrandAgent(
            brand_guidelines_path=brand_guidelines_path
        )
        
        self.analytics_agent = CanvaAnalyticsAgent(
            tracking_enabled=True
        )
    
    async def create_campaign(self, 
                            products: List[str],
                            platforms: List[Platform],
                            content_strategy: Dict) -> Dict:
        """
        Create a complete marketing campaign with automated design generation
        
        Args:
            products: List of products to feature
            platforms: Target social media platforms
            content_strategy: Content strategy configuration
            
        Returns:
            Campaign results with generated assets
        """
        print(f"🚀 Creating marketing campaign: {self.campaign_name}")
        
        # Step 1: Campaign Planning
        campaign_plan = await self._plan_campaign(products, platforms, content_strategy)
        
        # Step 2: Generate Product Showcase Designs
        product_designs = await self._generate_product_showcases(products, platforms)
        
        # Step 3: Generate Campaign Banners
        banner_designs = await self._generate_campaign_banners(platforms)
        
        # Step 4: Generate Social Media Content
        social_designs = await self._generate_social_content(platforms, content_strategy)
        
        # Step 5: Brand Consistency Validation
        all_designs = product_designs + banner_designs + social_designs
        validated_designs = await self._validate_brand_consistency(all_designs)
        
        # Step 6: Generate A/B Test Variations
        ab_test_designs = await self._generate_ab_test_variations(validated_designs)
        
        # Step 7: Organize and Package Assets
        campaign_assets = await self._organize_campaign_assets(ab_test_designs)
        
        # Step 8: Generate Campaign Report
        campaign_report = await self._generate_campaign_report(campaign_assets)
        
        # Store campaign data
        self.campaign_data = {
            "campaign_name": self.campaign_name,
            "created_at": datetime.now().isoformat(),
            "plan": campaign_plan,
            "assets": campaign_assets,
            "report": campaign_report
        }
        
        print(f"✅ Campaign created successfully: {len(campaign_assets)} assets generated")
        return self.campaign_data
    
    async def _plan_campaign(self, products: List[str], platforms: List[Platform], content_strategy: Dict) -> Dict:
        """Plan the marketing campaign structure"""
        print("📋 Planning campaign structure...")
        
        campaign_plan = {
            "products": products,
            "platforms": [p.value for p in platforms],
            "content_types": content_strategy.get("content_types", ["post", "story", "banner"]),
            "themes": content_strategy.get("themes", ["product_showcase", "lifestyle", "testimonial"]),
            "timeline": content_strategy.get("timeline", "2_weeks"),
            "budget": content_strategy.get("budget", "medium"),
            "target_audience": content_strategy.get("target_audience", "general")
        }
        
        return campaign_plan
    
    async def _generate_product_showcases(self, products: List[str], platforms: List[Platform]) -> List:
        """Generate product showcase designs for each product and platform"""
        print("🎨 Generating product showcase designs...")
        
        all_designs = []
        
        for product in products:
            print(f"  Creating designs for: {product}")
            
            for platform in platforms:
                # Generate product showcase designs
                designs = await self.design_agent.generate_social_media_designs(
                    platform=platform,
                    content_type="post",
                    content=f"{self.campaign_name}: {product}",
                    quantity=2,
                    variations=["product_showcase", "lifestyle"],
                    style="modern"
                )
                
                # Add product metadata
                for design in designs:
                    design.metadata.update({
                        "product": product,
                        "design_type": "product_showcase",
                        "campaign": self.campaign_name
                    })
                
                all_designs.extend(designs)
        
        print(f"  Generated {len(all_designs)} product showcase designs")
        return all_designs
    
    async def _generate_campaign_banners(self, platforms: List[Platform]) -> List:
        """Generate campaign banner designs"""
        print("🎨 Generating campaign banners...")
        
        banner_designs = []
        
        for platform in platforms:
            designs = await self.design_agent.generate_social_media_designs(
                platform=platform,
                content_type="cover",
                content=self.campaign_name,
                quantity=1,
                variations=["banner"],
                style="bold"
            )
            
            # Add campaign metadata
            for design in designs:
                design.metadata.update({
                    "design_type": "campaign_banner",
                    "campaign": self.campaign_name
                })
            
            banner_designs.extend(designs)
        
        print(f"  Generated {len(banner_designs)} campaign banners")
        return banner_designs
    
    async def _generate_social_content(self, platforms: List[Platform], content_strategy: Dict) -> List:
        """Generate social media content based on strategy"""
        print("🎨 Generating social media content...")
        
        content_types = content_strategy.get("content_types", ["post", "story"])
        themes = content_strategy.get("themes", ["lifestyle", "testimonial"])
        
        social_designs = []
        
        for platform in platforms:
            for content_type in content_types:
                for theme in themes:
                    # Generate themed content
                    content_text = self._generate_content_text(theme, content_type)
                    
                    designs = await self.design_agent.generate_social_media_designs(
                        platform=platform,
                        content_type=content_type,
                        content=content_text,
                        quantity=1,
                        variations=[theme],
                        style="engaging"
                    )
                    
                    # Add content metadata
                    for design in designs:
                        design.metadata.update({
                            "design_type": "social_content",
                            "theme": theme,
                            "content_type": content_type,
                            "campaign": self.campaign_name
                        })
                    
                    social_designs.extend(designs)
        
        print(f"  Generated {len(social_designs)} social media content pieces")
        return social_designs
    
    def _generate_content_text(self, theme: str, content_type: str) -> str:
        """Generate content text based on theme and type"""
        content_templates = {
            "lifestyle": {
                "post": "Experience the lifestyle with our latest collection",
                "story": "Behind the scenes of our brand story"
            },
            "testimonial": {
                "post": "What our customers are saying about us",
                "story": "Customer success stories that inspire"
            },
            "product_showcase": {
                "post": "Discover our innovative new products",
                "story": "See our products in action"
            }
        }
        
        return content_templates.get(theme, {}).get(content_type, f"{theme} content for {content_type}")
    
    async def _validate_brand_consistency(self, designs: List) -> List:
        """Validate and fix brand consistency across all designs"""
        print("🔍 Validating brand consistency...")
        
        validated_designs = await self.brand_agent.validate_designs(
            designs=designs,
            auto_fix=True,
            strict_mode=True
        )
        
        print(f"  Validated {len(validated_designs)} designs for brand consistency")
        return validated_designs
    
    async def _generate_ab_test_variations(self, designs: List) -> List:
        """Generate A/B test variations for key designs"""
        print("🧪 Generating A/B test variations...")
        
        # Select top designs for A/B testing
        key_designs = designs[:5]  # Top 5 designs
        
        ab_test_designs = []
        
        for design in key_designs:
            # Generate color variations
            color_variations = await self.design_agent.generate_variations(
                base_design=design,
                variation_type="color_scheme",
                variations=["vibrant", "muted", "monochrome"]
            )
            
            # Generate layout variations
            layout_variations = await self.design_agent.generate_variations(
                base_design=design,
                variation_type="layout",
                variations=["minimal", "detailed", "centered"]
            )
            
            ab_test_designs.extend(color_variations + layout_variations)
        
        print(f"  Generated {len(ab_test_designs)} A/B test variations")
        return designs + ab_test_designs
    
    async def _organize_campaign_assets(self, designs: List) -> Dict:
        """Organize campaign assets by platform and type"""
        print("📁 Organizing campaign assets...")
        
        organized_assets = {
            "by_platform": {},
            "by_type": {},
            "by_product": {},
            "ab_tests": []
        }
        
        for design in designs:
            platform = design.platform.value
            design_type = design.metadata.get("design_type", "unknown")
            product = design.metadata.get("product", "general")
            
            # Organize by platform
            if platform not in organized_assets["by_platform"]:
                organized_assets["by_platform"][platform] = []
            organized_assets["by_platform"][platform].append(design)
            
            # Organize by type
            if design_type not in organized_assets["by_type"]:
                organized_assets["by_type"][design_type] = []
            organized_assets["by_type"][design_type].append(design)
            
            # Organize by product
            if product not in organized_assets["by_product"]:
                organized_assets["by_product"][product] = []
            organized_assets["by_product"][product].append(design)
            
            # Identify A/B tests
            if "variation" in design.metadata:
                organized_assets["ab_tests"].append(design)
        
        # Generate asset summary
        organized_assets["summary"] = {
            "total_designs": len(designs),
            "platforms": list(organized_assets["by_platform"].keys()),
            "design_types": list(organized_assets["by_type"].keys()),
            "products": list(organized_assets["by_product"].keys()),
            "ab_test_variations": len(organized_assets["ab_tests"])
        }
        
        print(f"  Organized {len(designs)} assets across {len(organized_assets['by_platform'])} platforms")
        return organized_assets
    
    async def _generate_campaign_report(self, campaign_assets: Dict) -> Dict:
        """Generate comprehensive campaign report"""
        print("📊 Generating campaign report...")
        
        report = {
            "campaign_name": self.campaign_name,
            "generated_at": datetime.now().isoformat(),
            "asset_summary": campaign_assets["summary"],
            "platform_breakdown": {},
            "design_type_breakdown": {},
            "recommendations": []
        }
        
        # Platform breakdown
        for platform, designs in campaign_assets["by_platform"].items():
            report["platform_breakdown"][platform] = {
                "count": len(designs),
                "formats": list(set(d.format.value for d in designs)),
                "avg_file_size": sum(d.file_size for d in designs) / len(designs) if designs else 0
            }
        
        # Design type breakdown
        for design_type, designs in campaign_assets["by_type"].items():
            report["design_type_breakdown"][design_type] = {
                "count": len(designs),
                "platforms": list(set(d.platform.value for d in designs))
            }
        
        # Generate recommendations
        report["recommendations"] = [
            "Consider A/B testing the top-performing designs",
            "Monitor engagement metrics for each platform",
            "Update designs based on performance data",
            "Maintain brand consistency across all assets"
        ]
        
        print("  Campaign report generated successfully")
        return report
    
    async def download_campaign_assets(self, output_formats: List[DesignFormat] = None) -> List[str]:
        """Download all campaign assets"""
        if not output_formats:
            output_formats = [DesignFormat.PNG, DesignFormat.PDF]
        
        print("📥 Downloading campaign assets...")
        
        all_designs = []
        for platform_designs in self.campaign_data["assets"]["by_platform"].values():
            all_designs.extend(platform_designs)
        
        downloaded_files = []
        for format in output_formats:
            files = await self.design_agent.batch_download(all_designs, format)
            downloaded_files.extend(files)
        
        print(f"  Downloaded {len(downloaded_files)} files")
        return downloaded_files
    
    def save_campaign_data(self, filepath: str = None):
        """Save campaign data to JSON file"""
        if not filepath:
            filepath = f"./campaigns/{self.campaign_name}/campaign_data.json"
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "w") as f:
            json.dump(self.campaign_data, f, indent=2, default=str)
        
        print(f"💾 Campaign data saved to: {filepath}")

# Example usage
async def main():
    """Example marketing campaign creation"""
    
    # Campaign configuration
    campaign_config = {
        "products": ["AI Design Tool", "Brand Kit Pro", "Template Library"],
        "platforms": [Platform.INSTAGRAM, Platform.FACEBOOK, Platform.LINKEDIN],
        "content_strategy": {
            "content_types": ["post", "story", "cover"],
            "themes": ["product_showcase", "lifestyle", "testimonial"],
            "timeline": "2_weeks",
            "budget": "medium",
            "target_audience": "designers_and_marketers"
        }
    }
    
    # Create campaign manager
    campaign_manager = MarketingCampaignManager("AI Design Launch 2024")
    
    # Create campaign
    campaign_data = await campaign_manager.create_campaign(
        products=campaign_config["products"],
        platforms=campaign_config["platforms"],
        content_strategy=campaign_config["content_strategy"]
    )
    
    # Download assets
    downloaded_files = await campaign_manager.download_campaign_assets()
    
    # Save campaign data
    campaign_manager.save_campaign_data()
    
    print(f"\n🎉 Campaign created successfully!")
    print(f"📊 Generated {campaign_data['asset_summary']['total_designs']} designs")
    print(f"📁 Downloaded {len(downloaded_files)} files")
    print(f"📋 Report saved to campaign_data.json")

if __name__ == "__main__":
    asyncio.run(main())

