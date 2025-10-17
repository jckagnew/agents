#!/usr/bin/env python3
"""
Unit tests for Vision Design Agent
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from dataclasses import asdict
import json

# Add the src directory to the path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from agents.vision_design_agent import (
    VisionDesignAgent,
    DesignAnalysisType,
    DesignElement,
    WebsiteAnalysis
)

class TestVisionDesignAgent:
    """Test cases for Vision Design Agent"""
    
    @pytest.fixture
    def agent(self):
        """Create a VisionDesignAgent instance for testing"""
        return VisionDesignAgent()
    
    @pytest.fixture
    def mock_website_analysis(self):
        """Mock website analysis data"""
        return WebsiteAnalysis(
            url="https://example.com",
            title="Example Website",
            design_elements=[
                DesignElement(
                    element_type="hero_section",
                    selector=".hero",
                    properties={
                        "background_color": "#3B82F6",
                        "text_color": "#FFFFFF",
                        "font_family": "Inter, sans-serif"
                    }
                )
            ],
            color_palette=["#3B82F6", "#F59E0B", "#6B7280"],
            typography_scale={"h1": "3rem", "body": "1rem"},
            layout_grid={"columns": 12, "gutter": "24px"},
            component_patterns=[
                {
                    "name": "Hero Section",
                    "pattern": "centered_text_with_cta",
                    "elements": ["headline", "cta_button"]
                }
            ],
            responsive_breakpoints=[768, 1024],
            accessibility_score=8.5,
            conversion_elements=[
                {
                    "type": "cta_button",
                    "text": "Get Started",
                    "position": "hero_section"
                }
            ],
            recommendations=[
                "Improve color contrast",
                "Add more visual hierarchy"
            ]
        )

    def test_agent_initialization(self, agent):
        """Test agent initialization with default config"""
        assert agent.playwright_config["browser"] == "chromium"
        assert agent.playwright_config["headless"] == False
        assert agent.playwright_config["viewport"]["width"] == 1920
        assert agent.playwright_config["viewport"]["height"] == 1080
        assert agent.analysis_cache == {}

    def test_agent_initialization_with_custom_config(self):
        """Test agent initialization with custom config"""
        custom_config = {
            "browser": "firefox",
            "headless": True,
            "viewport": {"width": 1280, "height": 720}
        }
        agent = VisionDesignAgent(custom_config)
        assert agent.playwright_config == custom_config

    @pytest.mark.asyncio
    async def test_analyze_website_basic(self, agent):
        """Test basic website analysis"""
        url = "https://example.com"
        
        with patch.object(agent, '_perform_website_analysis') as mock_analysis:
            mock_analysis.return_value = Mock()
            mock_analysis.return_value.url = url
            mock_analysis.return_value.title = "Example Website"
            
            result = await agent.analyze_website(url)
            
            assert result.url == url
            assert result.title == "Example Website"
            mock_analysis.assert_called_once_with(url, list(DesignAnalysisType))

    @pytest.mark.asyncio
    async def test_analyze_website_with_specific_types(self, agent):
        """Test website analysis with specific analysis types"""
        url = "https://example.com"
        analysis_types = [DesignAnalysisType.COLOR_PALETTE, DesignAnalysisType.TYPOGRAPHY]
        
        with patch.object(agent, '_perform_website_analysis') as mock_analysis:
            mock_analysis.return_value = Mock()
            
            await agent.analyze_website(url, analysis_types)
            
            mock_analysis.assert_called_once_with(url, analysis_types)

    @pytest.mark.asyncio
    async def test_analyze_website_caching(self, agent):
        """Test that website analysis results are cached"""
        url = "https://example.com"
        
        with patch.object(agent, '_perform_website_analysis') as mock_analysis:
            mock_analysis.return_value = Mock()
            mock_analysis.return_value.url = url
            
            # First call
            result1 = await agent.analyze_website(url)
            # Second call should use cache
            result2 = await agent.analyze_website(url)
            
            # Should only call the analysis method once
            assert mock_analysis.call_count == 1
            assert url in agent.analysis_cache

    @pytest.mark.asyncio
    async def test_extract_component_from_website(self, agent):
        """Test component extraction from website"""
        url = "https://example.com"
        selector = ".hero-section"
        
        result = await agent.extract_component_from_website(url, selector)
        
        assert result["id"] == "extracted_hero_section"
        assert result["name"] == "Extracted .hero-section"
        assert result["category"] == "extracted"
        assert result["source_url"] == url
        assert "react" in result["code"]
        assert "css" in result["code"]
        assert "extracted" in result["tags"]

    @pytest.mark.asyncio
    async def test_generate_design_system_from_website(self, agent, mock_website_analysis):
        """Test design system generation from website analysis"""
        url = "https://example.com"
        
        with patch.object(agent, 'analyze_website') as mock_analyze:
            mock_analyze.return_value = mock_website_analysis
            
            result = await agent.generate_design_system_from_website(url)
            
            assert result["name"] == f"Design System from {url}"
            assert "colors" in result
            assert "typography" in result
            assert "spacing" in result
            assert "components" in result
            assert "layout" in result
            assert "breakpoints" in result
            
            # Check that colors are extracted correctly
            assert result["colors"]["primary"] == "#3B82F6"
            assert result["colors"]["secondary"] == "#F59E0B"
            assert result["colors"]["accent"] == "#6B7280"
            assert result["colors"]["neutral"] == "#F9FAFB"

    @pytest.mark.asyncio
    async def test_compare_websites(self, agent):
        """Test website comparison functionality"""
        urls = ["https://site1.com", "https://site2.com", "https://site3.com"]
        
        with patch.object(agent, 'analyze_website') as mock_analyze:
            # Mock different analyses for each site
            mock_analyses = []
            for i, url in enumerate(urls):
                mock_analysis = Mock()
                mock_analysis.color_palette = [f"#color{i}1", f"#color{i}2"]
                mock_analysis.typography_scale = {f"h{i+1}": f"{i+1}rem"}
                mock_analysis.component_patterns = [{"name": f"Component{i}"}]
                mock_analyses.append(mock_analysis)
            
            mock_analyze.side_effect = mock_analyses
            
            result = await agent.compare_websites(urls)
            
            assert result["websites_analyzed"] == 3
            assert len(result["common_colors"]) > 0
            assert len(result["common_typography_elements"]) > 0
            assert len(result["common_components"]) > 0
            assert "design_trends" in result
            assert "recommendations" in result

    def test_design_element_creation(self):
        """Test DesignElement dataclass creation"""
        element = DesignElement(
            element_type="button",
            selector=".btn-primary",
            properties={"color": "blue", "size": "large"},
            position={"x": 100, "y": 200},
            size={"width": 150, "height": 40}
        )
        
        assert element.element_type == "button"
        assert element.selector == ".btn-primary"
        assert element.properties["color"] == "blue"
        assert element.position["x"] == 100
        assert element.size["width"] == 150

    def test_website_analysis_creation(self, mock_website_analysis):
        """Test WebsiteAnalysis dataclass creation"""
        assert mock_website_analysis.url == "https://example.com"
        assert mock_website_analysis.title == "Example Website"
        assert len(mock_website_analysis.design_elements) == 1
        assert len(mock_website_analysis.color_palette) == 3
        assert mock_website_analysis.accessibility_score == 8.5
        assert len(mock_website_analysis.recommendations) == 2

    @pytest.mark.asyncio
    async def test_perform_website_analysis_mock(self, agent):
        """Test the mock implementation of website analysis"""
        url = "https://example.com"
        analysis_types = [DesignAnalysisType.COLOR_PALETTE]
        
        result = await agent._perform_website_analysis(url, analysis_types)
        
        assert result.url == url
        assert result.title == "Sample Website Analysis"
        assert len(result.design_elements) == 2  # hero_section and cta_button
        assert len(result.color_palette) == 4
        assert len(result.typography_scale) == 7
        assert len(result.component_patterns) == 2
        assert len(result.recommendations) == 4

    def test_design_analysis_type_enum(self):
        """Test DesignAnalysisType enum values"""
        assert DesignAnalysisType.LAYOUT_STRUCTURE.value == "layout_structure"
        assert DesignAnalysisType.COLOR_PALETTE.value == "color_palette"
        assert DesignAnalysisType.TYPOGRAPHY.value == "typography"
        assert DesignAnalysisType.COMPONENT_PATTERNS.value == "component_patterns"
        assert DesignAnalysisType.RESPONSIVE_DESIGN.value == "responsive_design"
        assert DesignAnalysisType.ACCESSIBILITY.value == "accessibility"
        assert DesignAnalysisType.CONVERSION_ELEMENTS.value == "conversion_elements"

    @pytest.mark.asyncio
    async def test_error_handling_in_analysis(self, agent):
        """Test error handling in website analysis"""
        url = "https://invalid-url.com"
        
        with patch.object(agent, '_perform_website_analysis') as mock_analysis:
            mock_analysis.side_effect = Exception("Network error")
            
            with pytest.raises(Exception):
                await agent.analyze_website(url)

    @pytest.mark.asyncio
    async def test_concurrent_analysis_requests(self, agent):
        """Test handling of concurrent analysis requests"""
        urls = ["https://site1.com", "https://site2.com", "https://site3.com"]
        
        with patch.object(agent, '_perform_website_analysis') as mock_analysis:
            mock_analysis.return_value = Mock()
            mock_analysis.return_value.url = "test"
            
            # Run multiple analyses concurrently
            tasks = [agent.analyze_website(url) for url in urls]
            results = await asyncio.gather(*tasks)
            
            assert len(results) == 3
            assert mock_analysis.call_count == 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
