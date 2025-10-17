# Analyze Website Command

## Description
Analyze a website's design patterns and extract reusable components for the Collaborative UI Design app.

## Usage
```
/analyze-website <url> [options]
```

## Parameters
- `url` (required): The website URL to analyze
- `--extract-components`: Extract specific components for reuse
- `--generate-design-system`: Generate a complete design system
- `--compare`: Compare with other analyzed websites
- `--focus`: Focus on specific design aspects (layout, colors, typography, components)

## Examples

### Basic Analysis
```
/analyze-website https://stripe.com
```

### Extract Specific Components
```
/analyze-website https://linear.app --extract-components .hero-section,.cta-button,.feature-card
```

### Generate Design System
```
/analyze-website https://vercel.com --generate-design-system
```

### Compare Multiple Websites
```
/analyze-website https://stripe.com --compare https://linear.app https://vercel.com
```

### Focus on Specific Aspects
```
/analyze-website https://figma.com --focus typography,colors
```

## What It Does

1. **Navigates to the website** using Playwright MCP
2. **Takes screenshots** of key sections and components
3. **Analyzes design patterns** including:
   - Color palette and usage
   - Typography scale and hierarchy
   - Layout grid and spacing
   - Component patterns and variants
   - Responsive design approach
   - Accessibility considerations
4. **Extracts reusable components** with:
   - React component code
   - CSS styles
   - Props and variants
   - Usage examples
5. **Generates design system** with:
   - Color tokens
   - Typography scale
   - Spacing system
   - Component library
   - Design tokens

## Output

The command will provide:

- **Visual Analysis Report** with screenshots and findings
- **Extracted Components** ready for use in the UI designer
- **Design System Definition** for consistent design
- **Recommendations** for implementation
- **Comparison Data** if comparing multiple sites

## Integration

The extracted components and design systems are automatically:
- Added to the Collaborative UI Design app's component library
- Made available for drag-and-drop design
- Integrated with the existing design system
- Tagged for easy discovery and reuse

## Best Practices

- Analyze websites with similar target audiences
- Focus on well-designed, modern websites
- Extract components that fit your design system
- Use comparison mode to identify trends
- Regularly update your component library

## Technical Details

- Uses Playwright MCP for browser automation
- Leverages Vision Design Agent for analysis
- Integrates with existing component store
- Generates production-ready React components
- Follows established design system patterns
