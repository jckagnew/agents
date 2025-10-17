import React, { useEffect, useState } from 'react';
import { ComponentLibrary } from './components/Library/ComponentLibrary';
import { DesignCanvas } from './components/Canvas/DesignCanvas';
import { PropertiesPanel } from './components/Properties/PropertiesPanel';
import { DesignSkillsPanel } from './components/DesignSkills/DesignSkillsPanel';
import { WebsiteAnalyzer } from './components/Analyzer/WebsiteAnalyzer';
import { Header } from './components/Layout/Header';
import { Sidebar } from './components/Layout/Sidebar';
import { useComponentStore } from './stores/componentStore';
import { ComponentDefinition } from './types/components';

// Sample component library data
const sampleComponents: ComponentDefinition[] = [
  {
    id: 'button',
    name: 'Button',
    category: 'atom',
    icon: '🔘',
    description: 'Interactive button component',
    properties: [
      { id: 'text', name: 'text', type: 'string', value: 'Button', required: true },
      { id: 'variant', name: 'variant', type: 'select', value: 'primary', options: ['primary', 'secondary', 'outline'] },
      { id: 'size', name: 'size', type: 'select', value: 'md', options: ['sm', 'md', 'lg'] },
    ],
    variants: [
      { id: 'primary', name: 'Primary', properties: { variant: 'primary' } },
      { id: 'secondary', name: 'Secondary', properties: { variant: 'secondary' } },
    ],
    code: {
      react: `const Button = ({ text, variant, size }) => (
  <button className={\`btn btn-\${variant} btn-\${size}\`}>
    {text}
  </button>
);`,
      css: `.btn { padding: 8px 16px; border-radius: 4px; }`,
    },
    preview: '',
    tags: ['interactive', 'form', 'action'],
  },
  {
    id: 'text',
    name: 'Text',
    category: 'atom',
    icon: '📝',
    description: 'Text display component',
    properties: [
      { id: 'text', name: 'text', type: 'string', value: 'Text', required: true },
      { id: 'size', name: 'size', type: 'select', value: 'md', options: ['xs', 'sm', 'md', 'lg', 'xl'] },
      { id: 'weight', name: 'weight', type: 'select', value: 'normal', options: ['normal', 'medium', 'semibold', 'bold'] },
    ],
    variants: [],
    code: {
      react: `const Text = ({ text, size, weight }) => (
  <span className={\`text-\${size} font-\${weight}\`}>
    {text}
  </span>
);`,
      css: `.text-xs { font-size: 12px; }`,
    },
    preview: '',
    tags: ['content', 'typography'],
  },
  {
    id: 'input',
    name: 'Input',
    category: 'atom',
    icon: '📝',
    description: 'Text input field',
    properties: [
      { id: 'placeholder', name: 'placeholder', type: 'string', value: 'Enter text...' },
      { id: 'type', name: 'type', type: 'select', value: 'text', options: ['text', 'email', 'password', 'number'] },
      { id: 'disabled', name: 'disabled', type: 'boolean', value: false },
    ],
    variants: [],
    code: {
      react: `const Input = ({ placeholder, type, disabled }) => (
  <input
    type={type}
    placeholder={placeholder}
    disabled={disabled}
    className="input"
  />
);`,
      css: `.input { padding: 8px 12px; border: 1px solid #ccc; }`,
    },
    preview: '',
    tags: ['form', 'input', 'interactive'],
  },
  {
    id: 'card',
    name: 'Card',
    category: 'molecule',
    icon: '🃏',
    description: 'Container card component',
    properties: [
      { id: 'title', name: 'title', type: 'string', value: 'Card Title' },
      { id: 'content', name: 'content', type: 'string', value: 'Card content...' },
      { id: 'padding', name: 'padding', type: 'select', value: 'md', options: ['sm', 'md', 'lg'] },
    ],
    variants: [],
    code: {
      react: `const Card = ({ title, content, padding }) => (
  <div className={\`card card-\${padding}\`}>
    <h3 className="card-title">{title}</h3>
    <p className="card-content">{content}</p>
  </div>
);`,
      css: `.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }`,
    },
    preview: '',
    tags: ['container', 'layout', 'content'],
  },
  {
    id: 'image',
    name: 'Image',
    category: 'atom',
    icon: '🖼️',
    description: 'Image display component',
    properties: [
      { id: 'src', name: 'src', type: 'string', value: '' },
      { id: 'alt', name: 'alt', type: 'string', value: 'Image' },
      { id: 'fit', name: 'fit', type: 'select', value: 'cover', options: ['cover', 'contain', 'fill'] },
    ],
    variants: [],
    code: {
      react: `const Image = ({ src, alt, fit }) => (
  <img
    src={src}
    alt={alt}
    className={\`image image-\${fit}\`}
  />
);`,
      css: `.image { max-width: 100%; height: auto; }`,
    },
    preview: '',
    tags: ['media', 'content', 'visual'],
  },
  {
    id: 'container',
    name: 'Container',
    category: 'layout',
    icon: '📦',
    description: 'Layout container component',
    properties: [
      { id: 'direction', name: 'direction', type: 'select', value: 'column', options: ['row', 'column'] },
      { id: 'align', name: 'align', type: 'select', value: 'start', options: ['start', 'center', 'end', 'stretch'] },
      { id: 'justify', name: 'justify', type: 'select', value: 'start', options: ['start', 'center', 'end', 'space-between'] },
    ],
    variants: [],
    code: {
      react: `const Container = ({ direction, align, justify, children }) => (
  <div className={\`container container-\${direction} align-\${align} justify-\${justify}\`}>
    {children}
  </div>
);`,
      css: `.container { display: flex; }`,
    },
    preview: '',
    tags: ['layout', 'container', 'flexbox'],
  },
  {
    id: 'hero-section',
    name: 'Hero Section',
    category: 'conversion',
    icon: '🎯',
    description: 'High-converting hero section with clear CTA',
    properties: [
      { id: 'headline', name: 'headline', type: 'string', value: 'Transform Your Business Today', required: true },
      { id: 'subheadline', name: 'subheadline', type: 'string', value: 'Join thousands of successful entrepreneurs who trust our platform' },
      { id: 'ctaText', name: 'ctaText', type: 'string', value: 'Get Started Free', required: true },
      { id: 'ctaVariant', name: 'ctaVariant', type: 'select', value: 'primary', options: ['primary', 'secondary', 'outline'] },
    ],
    variants: [
      { id: 'conversion-focused', name: 'Conversion Focused', properties: { ctaVariant: 'primary' } },
      { id: 'trust-building', name: 'Trust Building', properties: { ctaVariant: 'secondary' } },
    ],
    code: {
      react: `const HeroSection = ({ headline, subheadline, ctaText, ctaVariant }) => (
  <section className="hero-section">
    <div className="hero-content">
      <h1 className="hero-headline">{headline}</h1>
      <p className="hero-subheadline">{subheadline}</p>
      <button className={\`cta-button cta-\${ctaVariant}\`}>
        {ctaText}
      </button>
    </div>
  </section>
);`,
      css: `.hero-section { padding: 80px 0; text-align: center; }
.hero-headline { font-size: 3rem; font-weight: 700; margin-bottom: 1rem; }
.hero-subheadline { font-size: 1.25rem; color: #666; margin-bottom: 2rem; }
.cta-button { padding: 16px 32px; font-size: 1.125rem; border-radius: 8px; }`,
    },
    preview: '',
    tags: ['conversion', 'hero', 'cta', 'landing'],
  },
  {
    id: 'testimonial',
    name: 'Testimonial',
    category: 'conversion',
    icon: '💬',
    description: 'Social proof testimonial component',
    properties: [
      { id: 'quote', name: 'quote', type: 'string', value: 'This platform changed everything for our business!', required: true },
      { id: 'author', name: 'author', type: 'string', value: 'Sarah Johnson', required: true },
      { id: 'title', name: 'title', type: 'string', value: 'CEO, TechStart Inc.' },
      { id: 'avatar', name: 'avatar', type: 'string', value: 'https://via.placeholder.com/60' },
    ],
    variants: [],
    code: {
      react: `const Testimonial = ({ quote, author, title, avatar }) => (
  <div className="testimonial">
    <blockquote className="testimonial-quote">"{quote}"</blockquote>
    <div className="testimonial-author">
      <img src={avatar} alt={author} className="testimonial-avatar" />
      <div>
        <div className="testimonial-name">{author}</div>
        <div className="testimonial-title">{title}</div>
      </div>
    </div>
  </div>
);`,
      css: `.testimonial { background: #f8f9fa; padding: 2rem; border-radius: 12px; }
.testimonial-quote { font-size: 1.25rem; font-style: italic; margin-bottom: 1rem; }
.testimonial-author { display: flex; align-items: center; gap: 1rem; }
.testimonial-avatar { width: 60px; height: 60px; border-radius: 50%; }`,
    },
    preview: '',
    tags: ['conversion', 'social-proof', 'testimonial', 'trust'],
  },
  {
    id: 'typography-scale',
    name: 'Typography Scale',
    category: 'typography',
    icon: '📏',
    description: 'Complete typography scale system',
    properties: [
      { id: 'baseSize', name: 'baseSize', type: 'select', value: '16px', options: ['14px', '16px', '18px'] },
      { id: 'scale', name: 'scale', type: 'select', value: 'major-third', options: ['minor-second', 'major-second', 'minor-third', 'major-third', 'perfect-fourth'] },
      { id: 'fontFamily', name: 'fontFamily', type: 'select', value: 'Inter', options: ['Inter', 'Roboto', 'Open Sans', 'Lato', 'Poppins'] },
    ],
    variants: [
      { id: 'major-third', name: 'Major Third Scale', properties: { scale: 'major-third' } },
      { id: 'perfect-fourth', name: 'Perfect Fourth Scale', properties: { scale: 'perfect-fourth' } },
    ],
    code: {
      react: `const TypographyScale = ({ baseSize, scale, fontFamily }) => (
  <div className="typography-scale" style={{ fontFamily }}>
    <h1 style={{ fontSize: 'calc(' + baseSize + ' * 2.488)' }}>Heading 1</h1>
    <h2 style={{ fontSize: 'calc(' + baseSize + ' * 2.074)' }}>Heading 2</h2>
    <h3 style={{ fontSize: 'calc(' + baseSize + ' * 1.728)' }}>Heading 3</h3>
    <h4 style={{ fontSize: 'calc(' + baseSize + ' * 1.44)' }}>Heading 4</h4>
    <h5 style={{ fontSize: 'calc(' + baseSize + ' * 1.2)' }}>Heading 5</h5>
    <h6 style={{ fontSize: 'calc(' + baseSize + ' * 1)' }}>Heading 6</h6>
    <p style={{ fontSize: baseSize, lineHeight: '1.5' }}>Body text with proper line height for readability</p>
  </div>
);`,
      css: `.typography-scale { font-family: var(--font-family); }
h1, h2, h3, h4, h5, h6 { margin: 0 0 0.5rem 0; font-weight: 600; }
p { margin: 0 0 1rem 0; }`,
    },
    preview: '',
    tags: ['typography', 'scale', 'hierarchy', 'readability'],
  },
  {
    id: 'color-palette',
    name: 'Color Palette',
    category: 'color',
    icon: '🎨',
    description: '60-30-10 color system palette',
    properties: [
      { id: 'primary', name: 'primary', type: 'color', value: '#3B82F6' },
      { id: 'secondary', name: 'secondary', type: 'color', value: '#6B7280' },
      { id: 'accent', name: 'accent', type: 'color', value: '#F59E0B' },
      { id: 'neutral', name: 'neutral', type: 'color', value: '#F9FAFB' },
    ],
    variants: [
      { id: 'blue-theme', name: 'Blue Theme', properties: { primary: '#3B82F6', secondary: '#6B7280', accent: '#F59E0B' } },
      { id: 'green-theme', name: 'Green Theme', properties: { primary: '#10B981', secondary: '#6B7280', accent: '#F59E0B' } },
    ],
    code: {
      react: `const ColorPalette = ({ primary, secondary, accent, neutral }) => (
  <div className="color-palette">
    <div className="color-60" style={{ backgroundColor: neutral }}>60% Neutral</div>
    <div className="color-30" style={{ backgroundColor: secondary }}>30% Secondary</div>
    <div className="color-10" style={{ backgroundColor: accent }}>10% Accent</div>
    <div className="color-primary" style={{ backgroundColor: primary }}>Primary</div>
  </div>
);`,
      css: `.color-palette { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.color-60, .color-30, .color-10, .color-primary { padding: 2rem; border-radius: 8px; color: white; text-align: center; }`,
    },
    preview: '',
    tags: ['color', 'palette', '60-30-10', 'design-system'],
  },
];

function App() {
  const { loadComponentLibrary } = useComponentStore();
  const [showDesignSkills, setShowDesignSkills] = useState(false);
  const [showWebsiteAnalyzer, setShowWebsiteAnalyzer] = useState(false);

  useEffect(() => {
    // Load sample component library
    loadComponentLibrary(sampleComponents);
  }, [loadComponentLibrary]);

  return (
    <div className="App h-screen flex flex-col bg-gray-50">
      <Header 
        onToggleDesignSkills={() => setShowDesignSkills(!showDesignSkills)}
        onToggleWebsiteAnalyzer={() => setShowWebsiteAnalyzer(!showWebsiteAnalyzer)}
      />
      
      <div className="flex-1 flex overflow-hidden">
        <Sidebar>
          <ComponentLibrary />
        </Sidebar>
        
        <div className="flex-1 flex flex-col">
          <DesignCanvas className="flex-1" />
        </div>
        
        <PropertiesPanel />
        
        {showDesignSkills && <DesignSkillsPanel />}
        {showWebsiteAnalyzer && <WebsiteAnalyzer />}
      </div>
    </div>
  );
}

export default App;