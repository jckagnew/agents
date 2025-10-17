#!/usr/bin/env python3
"""
End-to-end tests for Vision-Based Design System
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from agents.vision_design_agent import VisionDesignAgent, DesignAnalysisType

class TestVisionE2E:
    """End-to-end tests for the complete vision-based design workflow"""
    
    @pytest.fixture
    def agent(self):
        """Create a VisionDesignAgent instance for E2E testing"""
        return VisionDesignAgent()
    
    @pytest.fixture
    def mock_playwright_session(self):
        """Mock Playwright session for testing"""
        session = AsyncMock()
        session.page = AsyncMock()
        session.page.goto = AsyncMock()
        session.page.screenshot = AsyncMock(return_value=b"fake_screenshot_data")
        session.page.evaluate = AsyncMock(return_value={
            "title": "Test Website",
            "elements": [
                {
                    "selector": ".hero",
                    "properties": {
                        "backgroundColor": "#3B82F6",
                        "color": "#FFFFFF",
                        "fontSize": "3rem"
                    }
                }
            ]
        })
        session.page.close = AsyncMock()
        return session

    @pytest.mark.asyncio
    async def test_complete_website_analysis_workflow(self, agent, mock_playwright_session):
        """Test the complete website analysis workflow from URL to design system"""
        url = "https://stripe.com"
        
        with patch('playwright.async_api.async_playwright') as mock_playwright:
            mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = mock_playwright_session
            mock_playwright.return_value.__aenter__.return_value.chromium.new_context.return_value = mock_playwright_session
            
            # Step 1: Analyze website
            analysis = await agent.analyze_website(url)
            
            assert analysis.url == url
            assert analysis.title == "Sample Website Analysis"
            assert len(analysis.design_elements) > 0
            assert len(analysis.color_palette) > 0
            assert len(analysis.typography_scale) > 0
            
            # Step 2: Extract specific component
            component = await agent.extract_component_from_website(url, ".hero-section")
            
            assert component["id"] == "extracted_hero_section"
            assert component["name"] == "Extracted .hero-section"
            assert "react" in component["code"]
            assert "css" in component["code"]
            
            # Step 3: Generate design system
            design_system = await agent.generate_design_system_from_website(url)
            
            assert design_system["name"] == f"Design System from {url}"
            assert "colors" in design_system
            assert "typography" in design_system
            assert "components" in design_system
            assert "layout" in design_system

    @pytest.mark.asyncio
    async def test_multi_website_comparison_workflow(self, agent):
        """Test comparing multiple websites and extracting common patterns"""
        urls = [
            "https://stripe.com",
            "https://linear.app", 
            "https://vercel.com"
        ]
        
        # Mock different analyses for each site
        mock_analyses = []
        for i, url in enumerate(urls):
            mock_analysis = Mock()
            mock_analysis.url = url
            mock_analysis.title = f"Site {i+1}"
            mock_analysis.color_palette = [f"#color{i}1", f"#color{i}2", "#common_color"]
            mock_analysis.typography_scale = {"h1": f"{i+2}rem", "body": "1rem"}
            mock_analysis.component_patterns = [
                {"name": f"Component{i}", "pattern": "grid"},
                {"name": "CommonComponent", "pattern": "card"}
            ]
            mock_analyses.append(mock_analysis)
        
        with patch.object(agent, 'analyze_website') as mock_analyze:
            mock_analyze.side_effect = mock_analyses
            
            # Compare websites
            comparison = await agent.compare_websites(urls)
            
            assert comparison["websites_analyzed"] == 3
            assert "#common_color" in comparison["common_colors"]
            assert "CommonComponent" in comparison["common_components"]
            assert "body" in comparison["common_typography_elements"]
            assert len(comparison["design_trends"]) > 0
            assert len(comparison["recommendations"]) > 0

    @pytest.mark.asyncio
    async def test_design_system_generation_workflow(self, agent):
        """Test generating a complete design system from website analysis"""
        url = "https://figma.com"
        
        # Mock a comprehensive analysis
        mock_analysis = Mock()
        mock_analysis.url = url
        mock_analysis.title = "Figma Website"
        mock_analysis.color_palette = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57"]
        mock_analysis.typography_scale = {
            "h1": "4rem", "h2": "3rem", "h3": "2rem", 
            "h4": "1.5rem", "h5": "1.25rem", "h6": "1rem", "body": "1rem"
        }
        mock_analysis.layout_grid = {
            "columns": 12, "gutter": "32px", "max_width": "1440px"
        }
        mock_analysis.component_patterns = [
            {"name": "Button", "pattern": "cta", "elements": ["text", "icon"]},
            {"name": "Card", "pattern": "content", "elements": ["header", "body", "footer"]},
            {"name": "Navigation", "pattern": "header", "elements": ["logo", "menu", "cta"]}
        ]
        mock_analysis.responsive_breakpoints = [480, 768, 1024, 1440]
        mock_analysis.accessibility_score = 9.2
        mock_analysis.conversion_elements = [
            {"type": "cta_button", "text": "Get Started", "position": "hero"},
            {"type": "signup_form", "position": "footer"}
        ]
        mock_analysis.recommendations = [
            "Excellent color contrast ratios",
            "Strong typography hierarchy",
            "Good responsive design implementation"
        ]
        
        with patch.object(agent, 'analyze_website') as mock_analyze:
            mock_analyze.return_value = mock_analysis
            
            # Generate design system
            design_system = await agent.generate_design_system_from_website(url)
            
            # Validate design system structure
            assert design_system["name"] == f"Design System from {url}"
            
            # Validate colors
            assert "colors" in design_system
            assert "primary" in design_system["colors"]
            assert "secondary" in design_system["colors"]
            assert "accent" in design_system["colors"]
            assert "neutral" in design_system["colors"]
            
            # Validate typography
            assert "typography" in design_system
            assert design_system["typography"]["h1"] == "4rem"
            assert design_system["typography"]["body"] == "1rem"
            
            # Validate spacing
            assert "spacing" in design_system
            assert "xs" in design_system["spacing"]
            assert "xl" in design_system["spacing"]
            
            # Validate components
            assert "components" in design_system
            assert len(design_system["components"]) > 0
            
            # Validate layout
            assert "layout" in design_system
            assert design_system["layout"]["columns"] == 12
            
            # Validate breakpoints
            assert "breakpoints" in design_system
            assert "mobile" in design_system["breakpoints"]
            assert "desktop" in design_system["breakpoints"]

    @pytest.mark.asyncio
    async def test_component_extraction_workflow(self, agent):
        """Test extracting and converting website components to React components"""
        url = "https://tailwindcss.com"
        selectors = [".hero-section", ".cta-button", ".feature-card", ".testimonial"]
        
        extracted_components = []
        
        for selector in selectors:
            component = await agent.extract_component_from_website(url, selector)
            extracted_components.append(component)
            
            # Validate component structure
            assert component["id"].startswith("extracted_")
            assert component["name"].startswith("Extracted")
            assert component["category"] == "extracted"
            assert component["source_url"] == url
            assert "extracted_at" in component
            
            # Validate code generation
            assert "react" in component["code"]
            assert "css" in component["code"]
            assert "const " in component["code"]["react"]
            assert "className=" in component["code"]["react"]
            
            # Validate properties
            assert "properties" in component
            assert len(component["properties"]) > 0
            
            # Validate tags
            assert "extracted" in component["tags"]
            assert "website" in component["tags"]
            assert "component" in component["tags"]
        
        # Validate that all components were extracted
        assert len(extracted_components) == len(selectors)
        
        # Validate unique IDs
        component_ids = [comp["id"] for comp in extracted_components]
        assert len(set(component_ids)) == len(component_ids)

    @pytest.mark.asyncio
    async def test_error_handling_workflow(self, agent):
        """Test error handling throughout the workflow"""
        invalid_url = "https://this-site-does-not-exist-12345.com"
        
        # Test analysis with invalid URL
        with patch.object(agent, '_perform_website_analysis') as mock_analysis:
            mock_analysis.side_effect = Exception("Network timeout")
            
            with pytest.raises(Exception):
                await agent.analyze_website(invalid_url)
        
        # Test component extraction with invalid selector
        component = await agent.extract_component_from_website(invalid_url, ".invalid-selector")
        assert component["id"] == "extracted_invalid_selector"
        assert component["name"] == "Extracted .invalid-selector"
        
        # Test design system generation with empty analysis
        empty_analysis = Mock()
        empty_analysis.color_palette = []
        empty_analysis.typography_scale = {}
        empty_analysis.component_patterns = []
        empty_analysis.layout_grid = {}
        empty_analysis.responsive_breakpoints = []
        
        with patch.object(agent, 'analyze_website') as mock_analyze:
            mock_analyze.return_value = empty_analysis
            
            design_system = await agent.generate_design_system_from_website(invalid_url)
            
            # Should still generate a valid design system with defaults
            assert design_system["name"] == f"Design System from {invalid_url}"
            assert "colors" in design_system
            assert "typography" in design_system

    @pytest.mark.asyncio
    async def test_performance_workflow(self, agent):
        """Test performance with multiple concurrent operations"""
        urls = [f"https://site{i}.com" for i in range(10)]
        
        with patch.object(agent, '_perform_website_analysis') as mock_analysis:
            mock_analysis.return_value = Mock()
            mock_analysis.return_value.url = "test"
            mock_analysis.return_value.color_palette = ["#test"]
            mock_analysis.return_value.typography_scale = {"body": "1rem"}
            mock_analysis.return_value.component_patterns = []
            mock_analysis.return_value.layout_grid = {}
            mock_analysis.return_value.responsive_breakpoints = []
            
            # Run multiple analyses concurrently
            start_time = asyncio.get_event_loop().time()
            
            tasks = [agent.analyze_website(url) for url in urls]
            results = await asyncio.gather(*tasks)
            
            end_time = asyncio.get_event_loop().time()
            execution_time = end_time - start_time
            
            # Validate results
            assert len(results) == len(urls)
            assert execution_time < 5.0  # Should complete within 5 seconds
            
            # Validate that all analyses were cached
            assert len(agent.analysis_cache) == len(urls)

    @pytest.mark.asyncio
    async def test_integration_with_design_skills(self, agent):
        """Test integration with the 5 essential design skills"""
        url = "https://design-system-example.com"
        
        # Mock analysis that demonstrates all 5 design skills
        mock_analysis = Mock()
        mock_analysis.url = url
        mock_analysis.title = "Design Skills Example"
        mock_analysis.color_palette = ["#3B82F6", "#6B7280", "#F59E0B", "#F9FAFB"]  # 60-30-10 rule
        mock_analysis.typography_scale = {
            "h1": "3rem", "h2": "2.25rem", "h3": "1.875rem",  # Typography hierarchy
            "h4": "1.5rem", "h5": "1.25rem", "h6": "1rem", "body": "1rem"
        }
        mock_analysis.layout_grid = {
            "columns": 12, "gutter": "24px", "max_width": "1200px"  # Layout system
        }
        mock_analysis.component_patterns = [
            {"name": "Hero Section", "pattern": "conversion_focused", "elements": ["headline", "cta"]},
            {"name": "Testimonial", "pattern": "social_proof", "elements": ["quote", "author"]},
            {"name": "Feature Card", "pattern": "grid_layout", "elements": ["icon", "title", "description"]}
        ]
        mock_analysis.responsive_breakpoints = [768, 1024, 1200]  # Responsive design
        mock_analysis.accessibility_score = 9.5  # Accessibility
        mock_analysis.conversion_elements = [
            {"type": "cta_button", "text": "Get Started Free", "position": "hero", "visibility": "high"},
            {"type": "newsletter_signup", "position": "footer", "visibility": "medium"}
        ]
        mock_analysis.recommendations = [
            "Excellent typography hierarchy implementation",
            "Strong color contrast ratios for accessibility",
            "Well-structured layout grid system",
            "Effective conversion-focused component design",
            "Good responsive design implementation"
        ]
        
        with patch.object(agent, 'analyze_website') as mock_analyze:
            mock_analyze.return_value = mock_analysis
            
            # Analyze website
            analysis = await agent.analyze_website(url)
            
            # Validate typography skills
            assert len(analysis.typography_scale) >= 6  # Good typography hierarchy
            assert "h1" in analysis.typography_scale
            assert "body" in analysis.typography_scale
            
            # Validate layout skills
            assert analysis.layout_grid["columns"] == 12  # Good grid system
            assert "gutter" in analysis.layout_grid
            
            # Validate color theory skills
            assert len(analysis.color_palette) == 4  # 60-30-10 rule implementation
            assert analysis.accessibility_score >= 9.0  # Good contrast ratios
            
            # Validate conversion skills
            assert len(analysis.conversion_elements) > 0
            assert any(elem["type"] == "cta_button" for elem in analysis.conversion_elements)
            
            # Validate coding basics (component generation)
            design_system = await agent.generate_design_system_from_website(url)
            assert "components" in design_system
            assert len(design_system["components"]) > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
