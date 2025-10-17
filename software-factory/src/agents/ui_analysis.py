"""
UI/UX Analysis Agent

This agent analyzes user interfaces for common design mistakes and provides
actionable recommendations for improvement. Based on modern UI/UX best practices
and accessibility guidelines.
"""

import asyncio
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import base64
from pathlib import Path


class SeverityLevel(Enum):
    """Severity levels for UI issues"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IssueCategory(Enum):
    """Categories of UI issues"""
    LAYOUT = "layout"
    TYPOGRAPHY = "typography"
    COLOR = "color"
    NAVIGATION = "navigation"
    ACCESSIBILITY = "accessibility"
    RESPONSIVENESS = "responsiveness"
    INTERACTION = "interaction"
    PERFORMANCE = "performance"
    CONTENT = "content"
    BRANDING = "branding"


@dataclass
class UIIssue:
    """UI issue data structure"""
    id: str
    category: IssueCategory
    severity: SeverityLevel
    title: str
    description: str
    file_path: str
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    recommendation: str = ""
    wcag_level: Optional[str] = None
    impact: str = ""
    effort_to_fix: str = ""


@dataclass
class UIAnalysisResult:
    """Complete UI analysis result"""
    project_id: str
    analysis_timestamp: datetime
    overall_score: float
    total_issues: int
    issues_by_severity: Dict[str, int]
    issues_by_category: Dict[str, int]
    issues: List[UIIssue]
    recommendations: List[str]
    accessibility_score: float
    mobile_score: float
    performance_score: float
    summary: str


class LayoutAnalyzer:
    """Analyzes layout and visual hierarchy issues"""
    
    async def analyze_layout(self, file_content: str, file_path: str) -> List[UIIssue]:
        """Analyze layout and visual hierarchy"""
        issues = []
        
        # Check for cluttered layouts
        if self._is_cluttered_layout(file_content):
            issues.append(UIIssue(
                id=f"layout_cluttered_{hash(file_path)}",
                category=IssueCategory.LAYOUT,
                severity=SeverityLevel.HIGH,
                title="Cluttered Layout Detected",
                description="The layout appears cluttered with too many elements competing for attention",
                file_path=file_path,
                recommendation="Reduce visual noise by grouping related elements and increasing white space",
                impact="Users may feel overwhelmed and have difficulty focusing on key actions",
                effort_to_fix="Medium - requires design restructuring"
            ))
        
        # Check for poor visual hierarchy
        if self._has_poor_hierarchy(file_content):
            issues.append(UIIssue(
                id=f"layout_hierarchy_{hash(file_path)}",
                category=IssueCategory.LAYOUT,
                severity=SeverityLevel.MEDIUM,
                title="Poor Visual Hierarchy",
                description="Lack of clear visual hierarchy makes it difficult to understand content priority",
                file_path=file_path,
                recommendation="Use size, color, and positioning to establish clear content hierarchy",
                impact="Users may miss important information or actions",
                effort_to_fix="Low - adjust typography and spacing"
            ))
        
        # Check for excessive white space
        if self._has_excessive_whitespace(file_content):
            issues.append(UIIssue(
                id=f"layout_whitespace_{hash(file_path)}",
                category=IssueCategory.LAYOUT,
                severity=SeverityLevel.LOW,
                title="Excessive White Space",
                description="Too much white space may make the interface feel empty or disconnected",
                file_path=file_path,
                recommendation="Balance white space with content density for better engagement",
                impact="May reduce content visibility and user engagement",
                effort_to_fix="Low - adjust spacing values"
            ))
        
        return issues
    
    def _is_cluttered_layout(self, content: str) -> bool:
        """Check if layout is cluttered"""
        # Look for excessive divs, buttons, or form elements
        div_count = content.count('<div')
        button_count = content.count('<button')
        input_count = content.count('<input')
        
        # Heuristic: if there are more than 20 divs or 10 interactive elements per 100 lines
        lines = content.count('\n')
        if lines > 0:
            div_density = div_count / (lines / 100)
            interactive_density = (button_count + input_count) / (lines / 100)
            return div_density > 20 or interactive_density > 10
        return False
    
    def _has_poor_hierarchy(self, content: str) -> bool:
        """Check for poor visual hierarchy"""
        # Look for lack of heading structure
        h1_count = content.count('<h1')
        h2_count = content.count('<h2')
        h3_count = content.count('<h3')
        
        # Check if there are multiple h1s (should only be one)
        if h1_count > 1:
            return True
        
        # Check if there's no clear heading structure
        if h1_count == 0 and h2_count == 0:
            return True
        
        return False
    
    def _has_excessive_whitespace(self, content: str) -> bool:
        """Check for excessive white space"""
        # Look for multiple consecutive empty lines
        empty_lines = content.count('\n\n\n')
        total_lines = content.count('\n')
        
        if total_lines > 0:
            empty_ratio = empty_lines / total_lines
            return empty_ratio > 0.1  # More than 10% empty lines


class TypographyAnalyzer:
    """Analyzes typography and text-related issues"""
    
    async def analyze_typography(self, file_content: str, file_path: str) -> List[UIIssue]:
        """Analyze typography issues"""
        issues = []
        
        # Check for font size issues
        font_issues = self._check_font_sizes(file_content)
        issues.extend(font_issues)
        
        # Check for readability issues
        readability_issues = self._check_readability(file_content)
        issues.extend(readability_issues)
        
        # Check for typography consistency
        consistency_issues = self._check_typography_consistency(file_content)
        issues.extend(consistency_issues)
        
        return issues
    
    def _check_font_sizes(self, file_content: str) -> List[UIIssue]:
        """Check for font size issues"""
        issues = []
        
        # Look for very small font sizes (less than 14px)
        small_font_pattern = r'font-size:\s*(\d+(?:\.\d+)?)px'
        matches = re.findall(small_font_pattern, file_content)
        
        for match in matches:
            size = float(match)
            if size < 14:
                issues.append(UIIssue(
                    id=f"typography_small_font_{hash(match)}",
                    category=IssueCategory.TYPOGRAPHY,
                    severity=SeverityLevel.HIGH,
                    title="Font Size Too Small",
                    description=f"Font size {size}px is too small for comfortable reading",
                    file_path="",
                    recommendation="Increase font size to at least 14px for body text",
                    impact="Poor readability, especially on mobile devices",
                    effort_to_fix="Low - adjust CSS font-size property",
                    wcag_level="AA"
                ))
        
        return issues
    
    def _check_readability(self, file_content: str) -> List[UIIssue]:
        """Check for readability issues"""
        issues = []
        
        # Check for long lines of text (more than 75 characters)
        text_lines = re.findall(r'>([^<]{75,})<', file_content)
        for line in text_lines:
            if len(line.strip()) > 75:
                issues.append(UIIssue(
                    id=f"typography_long_line_{hash(line)}",
                    category=IssueCategory.TYPOGRAPHY,
                    severity=SeverityLevel.MEDIUM,
                    title="Long Text Lines",
                    description="Text lines are too long, affecting readability",
                    file_path="",
                    recommendation="Break long lines or adjust container width",
                    impact="Reduced reading comfort and comprehension",
                    effort_to_fix="Low - adjust CSS max-width"
                ))
        
        return issues
    
    def _check_typography_consistency(self, file_content: str) -> List[UIIssue]:
        """Check for typography consistency"""
        issues = []
        
        # Count different font families
        font_families = re.findall(r'font-family:\s*([^;]+)', file_content)
        unique_fonts = set(font_families)
        
        if len(unique_fonts) > 3:
            issues.append(UIIssue(
                id=f"typography_too_many_fonts_{hash(str(unique_fonts))}",
                category=IssueCategory.TYPOGRAPHY,
                severity=SeverityLevel.MEDIUM,
                title="Too Many Font Families",
                description=f"Using {len(unique_fonts)} different font families reduces consistency",
                file_path="",
                recommendation="Limit to 2-3 font families maximum for better consistency",
                impact="Visual inconsistency and reduced brand cohesion",
                effort_to_fix="Medium - standardize font choices"
            ))
        
        return issues


class ColorAnalyzer:
    """Analyzes color and contrast issues"""
    
    async def analyze_colors(self, file_content: str, file_path: str) -> List[UIIssue]:
        """Analyze color and contrast issues"""
        issues = []
        
        # Check for color contrast issues
        contrast_issues = self._check_color_contrast(file_content)
        issues.extend(contrast_issues)
        
        # Check for color accessibility
        accessibility_issues = self._check_color_accessibility(file_content)
        issues.extend(accessibility_issues)
        
        # Check for color consistency
        consistency_issues = self._check_color_consistency(file_content)
        issues.extend(consistency_issues)
        
        return issues
    
    def _check_color_contrast(self, file_content: str) -> List[UIIssue]:
        """Check for color contrast issues"""
        issues = []
        
        # Look for common low-contrast combinations
        low_contrast_patterns = [
            (r'color:\s*#([0-9a-fA-F]{6})', r'background-color:\s*#([0-9a-fA-F]{6})'),
            (r'color:\s*rgb\(([^)]+)\)', r'background-color:\s*rgb\(([^)]+)\)'),
        ]
        
        for color_pattern, bg_pattern in low_contrast_patterns:
            color_matches = re.findall(color_pattern, file_content)
            bg_matches = re.findall(bg_pattern, file_content)
            
            # Simple heuristic: check for similar hex values
            for color in color_matches:
                for bg in bg_matches:
                    if self._colors_too_similar(color, bg):
                        issues.append(UIIssue(
                            id=f"color_contrast_{hash(color + bg)}",
                            category=IssueCategory.COLOR,
                            severity=SeverityLevel.HIGH,
                            title="Low Color Contrast",
                            description=f"Text color #{color} on background #{bg} has insufficient contrast",
                            file_path="",
                            recommendation="Increase contrast ratio to meet WCAG AA standards (4.5:1)",
                            impact="Poor readability, especially for users with visual impairments",
                            effort_to_fix="Low - adjust color values",
                            wcag_level="AA"
                        ))
        
        return issues
    
    def _check_color_accessibility(self, file_content: str) -> List[UIIssue]:
        """Check for color accessibility issues"""
        issues = []
        
        # Check for color-only information
        color_only_patterns = [
            r'color:\s*red[^;]*;.*required',
            r'color:\s*green[^;]*;.*success',
            r'color:\s*blue[^;]*;.*info',
        ]
        
        for pattern in color_only_patterns:
            if re.search(pattern, file_content, re.IGNORECASE):
                issues.append(UIIssue(
                    id=f"color_accessibility_{hash(pattern)}",
                    category=IssueCategory.ACCESSIBILITY,
                    severity=SeverityLevel.HIGH,
                    title="Color-Only Information",
                    description="Information is conveyed only through color, which is not accessible",
                    file_path="",
                    recommendation="Add text labels, icons, or other visual indicators",
                    impact="Inaccessible to colorblind users and screen readers",
                    effort_to_fix="Medium - add additional visual indicators",
                    wcag_level="AA"
                ))
        
        return issues
    
    def _check_color_consistency(self, file_content: str) -> List[UIIssue]:
        """Check for color consistency"""
        issues = []
        
        # Count different color values
        color_values = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}', file_content)
        unique_colors = set(color_values)
        
        if len(unique_colors) > 10:
            issues.append(UIIssue(
                id=f"color_too_many_{hash(str(unique_colors))}",
                category=IssueCategory.COLOR,
                severity=SeverityLevel.MEDIUM,
                title="Too Many Colors",
                description=f"Using {len(unique_colors)} different colors reduces visual consistency",
                file_path="",
                recommendation="Limit to a consistent color palette of 5-7 colors",
                impact="Visual inconsistency and reduced brand cohesion",
                effort_to_fix="Medium - standardize color palette"
            ))
        
        return issues
    
    def _colors_too_similar(self, color1: str, color2: str) -> bool:
        """Check if two hex colors are too similar"""
        try:
            # Convert hex to RGB
            r1, g1, b1 = int(color1[0:2], 16), int(color1[2:4], 16), int(color1[4:6], 16)
            r2, g2, b2 = int(color2[0:2], 16), int(color2[2:4], 16), int(color2[4:6], 16)
            
            # Calculate simple color difference
            diff = abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)
            return diff < 100  # Threshold for similar colors
        except:
            return False


class NavigationAnalyzer:
    """Analyzes navigation and user flow issues"""
    
    async def analyze_navigation(self, file_content: str, file_path: str) -> List[UIIssue]:
        """Analyze navigation issues"""
        issues = []
        
        # Check for missing navigation
        if not self._has_navigation(file_content):
            issues.append(UIIssue(
                id=f"nav_missing_{hash(file_path)}",
                category=IssueCategory.NAVIGATION,
                severity=SeverityLevel.HIGH,
                title="Missing Navigation",
                description="No clear navigation structure found",
                file_path=file_path,
                recommendation="Add a clear navigation menu or breadcrumbs",
                impact="Users may get lost or unable to navigate the application",
                effort_to_fix="Medium - implement navigation structure"
            ))
        
        # Check for complex navigation
        if self._has_complex_navigation(file_content):
            issues.append(UIIssue(
                id=f"nav_complex_{hash(file_path)}",
                category=IssueCategory.NAVIGATION,
                severity=SeverityLevel.MEDIUM,
                title="Complex Navigation Structure",
                description="Navigation appears overly complex with too many levels or options",
                file_path=file_path,
                recommendation="Simplify navigation to 2-3 levels maximum",
                impact="Users may find navigation confusing or overwhelming",
                effort_to_fix="High - restructure navigation hierarchy"
            ))
        
        # Check for missing breadcrumbs
        if self._needs_breadcrumbs(file_content):
            issues.append(UIIssue(
                id=f"nav_breadcrumbs_{hash(file_path)}",
                category=IssueCategory.NAVIGATION,
                severity=SeverityLevel.LOW,
                title="Missing Breadcrumbs",
                description="No breadcrumb navigation found for deep pages",
                file_path=file_path,
                recommendation="Add breadcrumb navigation for better user orientation",
                impact="Users may lose track of their location in the application",
                effort_to_fix="Low - add breadcrumb component"
            ))
        
        return issues
    
    def _has_navigation(self, content: str) -> bool:
        """Check if navigation exists"""
        nav_indicators = ['<nav', '<ul class="nav', 'navigation', 'menu', 'navbar']
        return any(indicator in content.lower() for indicator in nav_indicators)
    
    def _has_complex_navigation(self, content: str) -> bool:
        """Check if navigation is too complex"""
        # Count nested ul/li elements
        nested_ul = content.count('<ul')
        nested_li = content.count('<li')
        
        # Heuristic: if there are more than 3 levels of nesting
        return nested_ul > 3 or nested_li > 10
    
    def _needs_breadcrumbs(self, content: str) -> bool:
        """Check if breadcrumbs are needed"""
        # Look for deep page indicators
        deep_indicators = ['page-', 'level-', 'step-', 'stage-']
        has_deep_structure = any(indicator in content.lower() for indicator in deep_indicators)
        has_breadcrumbs = 'breadcrumb' in content.lower()
        
        return has_deep_structure and not has_breadcrumbs


class AccessibilityAnalyzer:
    """Analyzes accessibility issues"""
    
    async def analyze_accessibility(self, file_content: str, file_path: str) -> List[UIIssue]:
        """Analyze accessibility issues"""
        issues = []
        
        # Check for missing alt text
        alt_issues = self._check_alt_text(file_content)
        issues.extend(alt_issues)
        
        # Check for missing labels
        label_issues = self._check_form_labels(file_content)
        issues.extend(label_issues)
        
        # Check for keyboard navigation
        keyboard_issues = self._check_keyboard_navigation(file_content)
        issues.extend(keyboard_issues)
        
        # Check for focus indicators
        focus_issues = self._check_focus_indicators(file_content)
        issues.extend(focus_issues)
        
        return issues
    
    def _check_alt_text(self, file_content: str) -> List[UIIssue]:
        """Check for missing alt text on images"""
        issues = []
        
        # Find all img tags
        img_pattern = r'<img[^>]*>'
        img_tags = re.findall(img_pattern, file_content)
        
        for img_tag in img_tags:
            if 'alt=' not in img_tag and 'alt=""' not in img_tag:
                issues.append(UIIssue(
                    id=f"accessibility_alt_{hash(img_tag)}",
                    category=IssueCategory.ACCESSIBILITY,
                    severity=SeverityLevel.HIGH,
                    title="Missing Alt Text",
                    description="Image missing alt attribute for screen readers",
                    file_path="",
                    recommendation="Add descriptive alt text to all images",
                    impact="Inaccessible to screen reader users",
                    effort_to_fix="Low - add alt attribute",
                    wcag_level="A"
                ))
        
        return issues
    
    def _check_form_labels(self, file_content: str) -> List[UIIssue]:
        """Check for missing form labels"""
        issues = []
        
        # Find input elements without labels
        input_pattern = r'<input[^>]*>'
        inputs = re.findall(input_pattern, file_content)
        
        for input_tag in inputs:
            if 'id=' in input_tag:
                input_id = re.search(r'id="([^"]*)"', input_tag)
                if input_id:
                    input_id = input_id.group(1)
                    # Check if there's a corresponding label
                    label_pattern = f'<label[^>]*for="{input_id}"'
                    if not re.search(label_pattern, file_content):
                        issues.append(UIIssue(
                            id=f"accessibility_label_{hash(input_tag)}",
                            category=IssueCategory.ACCESSIBILITY,
                            severity=SeverityLevel.HIGH,
                            title="Missing Form Label",
                            description=f"Input field with id '{input_id}' is missing a label",
                            file_path="",
                            recommendation="Add a label element with for attribute matching input id",
                            impact="Inaccessible to screen reader users",
                            effort_to_fix="Low - add label element",
                            wcag_level="A"
                        ))
        
        return issues
    
    def _check_keyboard_navigation(self, file_content: str) -> List[UIIssue]:
        """Check for keyboard navigation issues"""
        issues = []
        
        # Check for interactive elements without tabindex
        interactive_elements = ['<button', '<a href', '<input', '<select', '<textarea']
        
        for element in interactive_elements:
            pattern = f'{element}[^>]*>'
            matches = re.findall(pattern, file_content)
            
            for match in matches:
                if 'tabindex=' not in match and 'tabindex="-1"' not in match:
                    # This is a potential issue, but not all elements need tabindex
                    if element == '<button' or element == '<a href':
                        issues.append(UIIssue(
                            id=f"accessibility_keyboard_{hash(match)}",
                            category=IssueCategory.ACCESSIBILITY,
                            severity=SeverityLevel.MEDIUM,
                            title="Keyboard Navigation Issue",
                            description="Interactive element may not be keyboard accessible",
                            file_path="",
                            recommendation="Ensure all interactive elements are keyboard accessible",
                            impact="Inaccessible to keyboard-only users",
                            effort_to_fix="Low - add proper tabindex or use semantic elements",
                            wcag_level="A"
                        ))
        
        return issues
    
    def _check_focus_indicators(self, file_content: str) -> List[UIIssue]:
        """Check for focus indicators"""
        issues = []
        
        # Look for focus styles
        focus_patterns = [':focus', ':focus-visible', 'outline:', 'box-shadow:']
        has_focus_styles = any(pattern in file_content for pattern in focus_patterns)
        
        if not has_focus_styles:
            issues.append(UIIssue(
                id=f"accessibility_focus_{hash(file_content)}",
                category=IssueCategory.ACCESSIBILITY,
                severity=SeverityLevel.MEDIUM,
                title="Missing Focus Indicators",
                description="No visible focus indicators found for keyboard navigation",
                file_path="",
                recommendation="Add visible focus indicators for all interactive elements",
                impact="Keyboard users cannot see which element has focus",
                effort_to_fix="Low - add CSS focus styles",
                wcag_level="AA"
            ))
        
        return issues


class ResponsivenessAnalyzer:
    """Analyzes responsive design issues"""
    
    async def analyze_responsiveness(self, file_content: str, file_path: str) -> List[UIIssue]:
        """Analyze responsive design issues"""
        issues = []
        
        # Check for missing viewport meta tag
        if not self._has_viewport_meta(file_content):
            issues.append(UIIssue(
                id=f"responsive_viewport_{hash(file_path)}",
                category=IssueCategory.RESPONSIVENESS,
                severity=SeverityLevel.HIGH,
                title="Missing Viewport Meta Tag",
                description="No viewport meta tag found for mobile responsiveness",
                file_path=file_path,
                recommendation="Add viewport meta tag: <meta name='viewport' content='width=device-width, initial-scale=1'>",
                impact="Poor mobile experience and layout issues",
                effort_to_fix="Low - add meta tag",
                wcag_level="AA"
            ))
        
        # Check for responsive design patterns
        responsive_issues = self._check_responsive_patterns(file_content)
        issues.extend(responsive_issues)
        
        # Check for mobile-specific issues
        mobile_issues = self._check_mobile_issues(file_content)
        issues.extend(mobile_issues)
        
        return issues
    
    def _has_viewport_meta(self, content: str) -> bool:
        """Check if viewport meta tag exists"""
        return 'viewport' in content.lower()
    
    def _check_responsive_patterns(self, file_content: str) -> List[UIIssue]:
        """Check for responsive design patterns"""
        issues = []
        
        # Check for media queries
        media_queries = re.findall(r'@media[^{]*{', file_content)
        
        if not media_queries:
            issues.append(UIIssue(
                id=f"responsive_media_queries_{hash(file_content)}",
                category=IssueCategory.RESPONSIVENESS,
                severity=SeverityLevel.HIGH,
                title="No Media Queries Found",
                description="No responsive breakpoints found for different screen sizes",
                file_path="",
                recommendation="Add media queries for mobile, tablet, and desktop breakpoints",
                impact="Poor experience on different screen sizes",
                effort_to_fix="High - implement responsive design",
                wcag_level="AA"
            ))
        
        return issues
    
    def _check_mobile_issues(self, file_content: str) -> List[UIIssue]:
        """Check for mobile-specific issues"""
        issues = []
        
        # Check for fixed widths that might break on mobile
        fixed_width_pattern = r'width:\s*(\d+)px'
        fixed_widths = re.findall(fixed_width_pattern, file_content)
        
        for width in fixed_widths:
            if int(width) > 400:  # Wider than typical mobile screen
                issues.append(UIIssue(
                    id=f"responsive_fixed_width_{width}",
                    category=IssueCategory.RESPONSIVENESS,
                    severity=SeverityLevel.MEDIUM,
                    title="Fixed Width Too Large",
                    description=f"Fixed width of {width}px may cause horizontal scrolling on mobile",
                    file_path="",
                    recommendation="Use relative units (%, vw, em) or max-width instead",
                    impact="Horizontal scrolling on mobile devices",
                    effort_to_fix="Low - adjust CSS units",
                    wcag_level="AA"
                ))
        
        return issues


class UIAnalysisAgent:
    """
    Master agent for UI/UX analysis.
    
    This agent coordinates all specialized analyzers to provide comprehensive
    UI/UX feedback and recommendations.
    """
    
    def __init__(self):
        """Initialize with specialized analyzers"""
        self.layout_analyzer = LayoutAnalyzer()
        self.typography_analyzer = TypographyAnalyzer()
        self.color_analyzer = ColorAnalyzer()
        self.navigation_analyzer = NavigationAnalyzer()
        self.accessibility_analyzer = AccessibilityAnalyzer()
        self.responsiveness_analyzer = ResponsivenessAnalyzer()
    
    async def analyze_project_ui(self, project_path: str) -> UIAnalysisResult:
        """
        Analyze UI/UX for an entire project.
        
        Args:
            project_path: Path to the project directory
            
        Returns:
            Complete UI analysis result
        """
        print(f"Starting UI analysis for project: {project_path}")
        
        # Find all UI files
        ui_files = await self._find_ui_files(project_path)
        
        all_issues = []
        
        # Analyze each file
        for file_path in ui_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Run all analyzers
                layout_issues = await self.layout_analyzer.analyze_layout(content, file_path)
                typography_issues = await self.typography_analyzer.analyze_typography(content, file_path)
                color_issues = await self.color_analyzer.analyze_colors(content, file_path)
                navigation_issues = await self.navigation_analyzer.analyze_navigation(content, file_path)
                accessibility_issues = await self.accessibility_analyzer.analyze_accessibility(content, file_path)
                responsiveness_issues = await self.responsiveness_analyzer.analyze_responsiveness(content, file_path)
                
                all_issues.extend(layout_issues)
                all_issues.extend(typography_issues)
                all_issues.extend(color_issues)
                all_issues.extend(navigation_issues)
                all_issues.extend(accessibility_issues)
                all_issues.extend(responsiveness_issues)
                
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
                continue
        
        # Calculate scores and generate recommendations
        overall_score = self._calculate_overall_score(all_issues)
        accessibility_score = self._calculate_accessibility_score(all_issues)
        mobile_score = self._calculate_mobile_score(all_issues)
        performance_score = self._calculate_performance_score(all_issues)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(all_issues)
        
        # Create summary
        summary = self._generate_summary(all_issues, overall_score)
        
        result = UIAnalysisResult(
            project_id=project_path,
            analysis_timestamp=datetime.now(),
            overall_score=overall_score,
            total_issues=len(all_issues),
            issues_by_severity=self._group_issues_by_severity(all_issues),
            issues_by_category=self._group_issues_by_category(all_issues),
            issues=all_issues,
            recommendations=recommendations,
            accessibility_score=accessibility_score,
            mobile_score=mobile_score,
            performance_score=performance_score,
            summary=summary
        )
        
        print(f"UI analysis completed. Found {len(all_issues)} issues with overall score: {overall_score}/10")
        return result
    
    async def analyze_single_file(self, file_path: str) -> UIAnalysisResult:
        """
        Analyze UI/UX for a single file.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            UI analysis result for the single file
        """
        print(f"Analyzing single file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise ValueError(f"Could not read file {file_path}: {e}")
        
        all_issues = []
        
        # Run all analyzers
        layout_issues = await self.layout_analyzer.analyze_layout(content, file_path)
        typography_issues = await self.typography_analyzer.analyze_typography(content, file_path)
        color_issues = await self.color_analyzer.analyze_colors(content, file_path)
        navigation_issues = await self.navigation_analyzer.analyze_navigation(content, file_path)
        accessibility_issues = await self.accessibility_analyzer.analyze_accessibility(content, file_path)
        responsiveness_issues = await self.responsiveness_analyzer.analyze_responsiveness(content, file_path)
        
        all_issues.extend(layout_issues)
        all_issues.extend(typography_issues)
        all_issues.extend(color_issues)
        all_issues.extend(navigation_issues)
        all_issues.extend(accessibility_issues)
        all_issues.extend(responsiveness_issues)
        
        # Calculate scores
        overall_score = self._calculate_overall_score(all_issues)
        accessibility_score = self._calculate_accessibility_score(all_issues)
        mobile_score = self._calculate_mobile_score(all_issues)
        performance_score = self._calculate_performance_score(all_issues)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(all_issues)
        
        # Create summary
        summary = self._generate_summary(all_issues, overall_score)
        
        result = UIAnalysisResult(
            project_id=file_path,
            analysis_timestamp=datetime.now(),
            overall_score=overall_score,
            total_issues=len(all_issues),
            issues_by_severity=self._group_issues_by_severity(all_issues),
            issues_by_category=self._group_issues_by_category(all_issues),
            issues=all_issues,
            recommendations=recommendations,
            accessibility_score=accessibility_score,
            mobile_score=mobile_score,
            performance_score=performance_score,
            summary=summary
        )
        
        print(f"Single file analysis completed. Found {len(all_issues)} issues with overall score: {overall_score}/10")
        return result
    
    async def _find_ui_files(self, project_path: str) -> List[str]:
        """Find all UI-related files in the project"""
        ui_files = []
        project_dir = Path(project_path)
        
        # Common UI file extensions
        ui_extensions = ['.html', '.jsx', '.tsx', '.vue', '.svelte', '.css', '.scss', '.sass', '.less']
        
        for ext in ui_extensions:
            ui_files.extend(project_dir.rglob(f'*{ext}'))
        
        # Convert Path objects to strings
        return [str(f) for f in ui_files]
    
    def _calculate_overall_score(self, issues: List[UIIssue]) -> float:
        """Calculate overall UI score based on issues"""
        if not issues:
            return 10.0
        
        # Weight issues by severity
        severity_weights = {
            SeverityLevel.CRITICAL: 3.0,
            SeverityLevel.HIGH: 2.0,
            SeverityLevel.MEDIUM: 1.0,
            SeverityLevel.LOW: 0.5,
            SeverityLevel.INFO: 0.1
        }
        
        total_weight = sum(severity_weights[issue.severity] for issue in issues)
        max_possible_weight = len(issues) * 3.0  # Assume all critical
        
        if max_possible_weight == 0:
            return 10.0
        
        score = 10.0 - (total_weight / max_possible_weight) * 10.0
        return max(0.0, min(10.0, score))
    
    def _calculate_accessibility_score(self, issues: List[UIIssue]) -> float:
        """Calculate accessibility score"""
        accessibility_issues = [i for i in issues if i.category == IssueCategory.ACCESSIBILITY]
        return self._calculate_overall_score(accessibility_issues)
    
    def _calculate_mobile_score(self, issues: List[UIIssue]) -> float:
        """Calculate mobile responsiveness score"""
        mobile_issues = [i for i in issues if i.category == IssueCategory.RESPONSIVENESS]
        return self._calculate_overall_score(mobile_issues)
    
    def _calculate_performance_score(self, issues: List[UIIssue]) -> float:
        """Calculate performance score"""
        performance_issues = [i for i in issues if i.category == IssueCategory.PERFORMANCE]
        return self._calculate_overall_score(performance_issues)
    
    def _group_issues_by_severity(self, issues: List[UIIssue]) -> Dict[str, int]:
        """Group issues by severity level"""
        groups = {}
        for severity in SeverityLevel:
            groups[severity.value] = len([i for i in issues if i.severity == severity])
        return groups
    
    def _group_issues_by_category(self, issues: List[UIIssue]) -> Dict[str, int]:
        """Group issues by category"""
        groups = {}
        for category in IssueCategory:
            groups[category.value] = len([i for i in issues if i.category == category])
        return groups
    
    def _generate_recommendations(self, issues: List[UIIssue]) -> List[str]:
        """Generate actionable recommendations based on issues"""
        recommendations = []
        
        # Group issues by category and generate recommendations
        categories = {}
        for issue in issues:
            if issue.category not in categories:
                categories[issue.category] = []
            categories[issue.category].append(issue)
        
        for category, category_issues in categories.items():
            if category == IssueCategory.ACCESSIBILITY:
                recommendations.append("🔍 **Accessibility**: Focus on adding alt text, form labels, and keyboard navigation support")
            elif category == IssueCategory.RESPONSIVENESS:
                recommendations.append("📱 **Mobile**: Implement responsive design with proper viewport settings and media queries")
            elif category == IssueCategory.COLOR:
                recommendations.append("🎨 **Color**: Improve contrast ratios and ensure color is not the only way to convey information")
            elif category == IssueCategory.TYPOGRAPHY:
                recommendations.append("📝 **Typography**: Standardize font choices and improve readability with proper sizing")
            elif category == IssueCategory.LAYOUT:
                recommendations.append("📐 **Layout**: Simplify visual hierarchy and reduce clutter for better user focus")
            elif category == IssueCategory.NAVIGATION:
                recommendations.append("🧭 **Navigation**: Simplify navigation structure and add breadcrumbs for better user orientation")
        
        # Add general recommendations
        if len(issues) > 20:
            recommendations.append("⚠️ **Overall**: Consider a comprehensive UI/UX audit to address the high number of issues")
        
        if any(issue.severity == SeverityLevel.CRITICAL for issue in issues):
            recommendations.append("🚨 **Priority**: Address critical issues immediately as they significantly impact user experience")
        
        return recommendations
    
    def _generate_summary(self, issues: List[UIIssue], overall_score: float) -> str:
        """Generate a summary of the analysis"""
        critical_count = len([i for i in issues if i.severity == SeverityLevel.CRITICAL])
        high_count = len([i for i in issues if i.severity == SeverityLevel.HIGH])
        
        if overall_score >= 8.0:
            status = "Excellent"
            emoji = "🌟"
        elif overall_score >= 6.0:
            status = "Good"
            emoji = "✅"
        elif overall_score >= 4.0:
            status = "Needs Improvement"
            emoji = "⚠️"
        else:
            status = "Poor"
            emoji = "❌"
        
        summary = f"{emoji} **UI/UX Analysis Summary**\n\n"
        summary += f"**Overall Score**: {overall_score:.1f}/10 ({status})\n"
        summary += f"**Total Issues**: {len(issues)}\n"
        summary += f"**Critical Issues**: {critical_count}\n"
        summary += f"**High Priority Issues**: {high_count}\n\n"
        
        if critical_count > 0:
            summary += "🚨 **Immediate Action Required**: Address critical issues first as they significantly impact user experience.\n\n"
        
        summary += "**Key Areas for Improvement**:\n"
        categories = self._group_issues_by_category(issues)
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        
        for category, count in sorted_categories[:3]:
            if count > 0:
                category_name = category.replace('_', ' ').title()
                summary += f"- {category_name}: {count} issues\n"
        
        return summary


# Example usage and testing
async def main():
    """Example usage of the UI Analysis Agent"""
    agent = UIAnalysisAgent()
    
    # Example: Analyze a project directory
    # result = await agent.analyze_project_ui("/path/to/project")
    
    # Example: Analyze a single file
    # result = await agent.analyze_single_file("/path/to/file.html")
    
    print("UI Analysis Agent ready for use!")
    print("Use agent.analyze_project_ui(project_path) or agent.analyze_single_file(file_path)")


if __name__ == "__main__":
    asyncio.run(main())
