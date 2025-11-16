# Accessibility Guidelines

## Overview

The Partner Showcase UI follows WCAG 2.1 AA guidelines to ensure all prospective partners—including those using assistive technology—can access the content.

## Key Principles

1. **Perceivable**
   - Provide text alternatives for images, icons, and diagrams explaining the Software Factory workflow.
   - Ensure color contrast ratio ≥ 4.5:1 for text/interactive elements; use brand palette with accessible pairings.
   - Support captioning or transcripts for embedded media (e.g., AI workflow video).

2. **Operable**
   - Keyboard access for navigation, CTA buttons, and accordions; focus outlines clearly visible.
   - Provide skip-to-content link for screen-reader and keyboard users.
   - Avoid auto-playing animations longer than 5 seconds; provide pause/stop controls.

3. **Understandable**
   - Use consistent navigation patterns across sections (workflow, AI Studio research, case studies).
   - Plain-language summaries for technical diagrams; glossary for terms like “Respect-Spec” or “Parking Lot.”
   - Form validation errors presented inline with clear instructions.

4. **Robust**
   - Semantic HTML: headings in logical order, landmark roles (`header`, `main`, `nav`, `footer`).
   - ARIA attributes for timeline components and interactive cards.
   - Test with screen readers (NVDA, VoiceOver) and automated tools (axe, Lighthouse).

## Testing Checklist

- [ ] axe DevTools scan shows no critical issues.
- [ ] Keyboard only walkthrough confirms tab order and focus management.
- [ ] Screen reader (VoiceOver/NVDA) announces timeline events and CTA labels.
- [ ] Lighthouse accessibility score ≥ 95.
- [ ] Visual QA adds accessibility regression checks (contrast, focus state screenshots).

## References

- [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/TR/wai-aria-practices/)
- Internal Design System: see `design/design-system.md` once generated.
