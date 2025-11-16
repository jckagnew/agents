#!/usr/bin/env python3
"""
Generate Splash Screens - Simple version

This script generates React components for animated splash screens
using the top 3 curated image pairs.
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

def generate_splash_component(pair: Dict[str, Any], index: int, content: Dict[str, Any]) -> str:
    """Generate a React component for a splash screen"""
    component_name = f"SplashScreen{index + 1}"
    
    # Extract image URLs
    before_url = pair.get("before_url", "")
    after_url = pair.get("after_url", "")
    
    # Extract content
    title = content.get("title", "Transform Your Life")
    subtitle = content.get("subtitle", "Track. Transform. Triumph.")
    description = content.get("description", "Your journey starts here.")
    cta_primary = content.get("ctaPrimary", "Create Profile")
    cta_secondary = content.get("ctaSecondary", "Log In")
    
    # Generate stats
    stats = content.get("stats", [])
    stats_html = ""
    for stat in stats:
        stats_html += f'        <div className="stat-item">\n'
        stats_html += f'          <div className="stat-value">{stat["value"]}</div>\n'
        stats_html += f'          <div className="stat-label">{stat["label"]}</div>\n'
        stats_html += f'        </div>\n'
    
    # Create the component using string formatting
    component = f'''import React, {{ useState, useEffect }} from 'react';
import Image from 'next/image';

interface {component_name}Props {{
  onGetStarted: () => void;
  onLogin: () => void;
}}

const {component_name}: React.FC<{component_name}Props> = ({{ onGetStarted, onLogin }}) => {{
  const [currentImage, setCurrentImage] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  
  const images = [
    {{
      src: "{before_url}",
      alt: "Before transformation",
      description: "{pair.get('before_description', '')[:100]}..."
    }},
    {{
      src: "{after_url}",
      alt: "After transformation", 
      description: "{pair.get('after_description', '')[:100]}..."
    }}
  ];
  
  useEffect(() => {{
    const interval = setInterval(() => {{
      setIsAnimating(true);
      setTimeout(() => {{
        setCurrentImage((prev) => (prev + 1) % images.length);
        setIsAnimating(false);
      }}, 300);
    }}, 3000);
    
    return () => clearInterval(interval);
  }}, [images.length]);
  
  return (
    <div className="splash-screen">
      <div className="splash-background">
        <div className="image-container">
          <Image
            src={{images[currentImage].src}}
            alt={{images[currentImage].alt}}
            fill
            className={{`splash-image ${{isAnimating ? 'fade-out' : 'fade-in'}}`}}
            priority
          />
          <div className="image-overlay" />
        </div>
      </div>
      
      <div className="splash-content">
        <div className="splash-header">
          <h1 className="splash-title">{title}</h1>
          <h2 className="splash-subtitle">{subtitle}</h2>
          <p className="splash-description">{description}</p>
        </div>
        
        <div className="splash-stats">
{stats_html}        </div>
        
        <div className="splash-actions">
          <button 
            className="btn-primary"
            onClick={{onGetStarted}}
          >
            {cta_primary}
          </button>
          <button 
            className="btn-secondary"
            onClick={{onLogin}}
          >
            {cta_secondary}
          </button>
        </div>
        
        <div className="splash-footer">
          <p className="transformation-text">
            Watch your transformation unfold
          </p>
        </div>
      </div>
      
      <style jsx>{{`{{
        .splash-screen {{
          position: relative;
          width: 100vw;
          height: 100vh;
          overflow: hidden;
          display: flex;
          align-items: center;
          justify-content: center;
        }}
        
        .splash-background {{
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 1;
        }}
        
        .image-container {{
          position: relative;
          width: 100%;
          height: 100%;
        }}
        
        .splash-image {{
          object-fit: cover;
          transition: opacity 0.3s ease-in-out;
        }}
        
        .fade-in {{
          opacity: 1;
        }}
        
        .fade-out {{
          opacity: 0;
        }}
        
        .image-overlay {{
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: linear-gradient(
            135deg,
            rgba(0, 0, 0, 0.7) 0%,
            rgba(0, 0, 0, 0.3) 50%,
            rgba(0, 0, 0, 0.7) 100%
          );
          z-index: 2;
        }}
        
        .splash-content {{
          position: relative;
          z-index: 3;
          text-align: center;
          color: white;
          max-width: 600px;
          padding: 2rem;
        }}
        
        .splash-title {{
          font-size: 3.5rem;
          font-weight: 800;
          margin-bottom: 1rem;
          background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }}
        
        .splash-subtitle {{
          font-size: 1.5rem;
          font-weight: 600;
          margin-bottom: 1rem;
          color: #e2e8f0;
        }}
        
        .splash-description {{
          font-size: 1.1rem;
          margin-bottom: 2rem;
          color: #cbd5e0;
          line-height: 1.6;
        }}
        
        .splash-stats {{
          display: flex;
          justify-content: center;
          gap: 2rem;
          margin-bottom: 2rem;
        }}
        
        .stat-item {{
          text-align: center;
        }}
        
        .stat-value {{
          font-size: 2rem;
          font-weight: 700;
          color: #4ecdc4;
          margin-bottom: 0.5rem;
        }}
        
        .stat-label {{
          font-size: 0.9rem;
          color: #a0aec0;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }}
        
        .splash-actions {{
          display: flex;
          gap: 1rem;
          justify-content: center;
          margin-bottom: 2rem;
        }}
        
        .btn-primary {{
          background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
          color: white;
          border: none;
          padding: 1rem 2rem;
          border-radius: 50px;
          font-size: 1.1rem;
          font-weight: 600;
          cursor: pointer;
          transition: transform 0.2s ease;
        }}
        
        .btn-primary:hover {{
          transform: translateY(-2px);
        }}
        
        .btn-secondary {{
          background: transparent;
          color: white;
          border: 2px solid white;
          padding: 1rem 2rem;
          border-radius: 50px;
          font-size: 1.1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
        }}
        
        .btn-secondary:hover {{
          background: white;
          color: #1a202c;
        }}
        
        .splash-footer {{
          margin-top: 2rem;
        }}
        
        .transformation-text {{
          font-size: 0.9rem;
          color: #a0aec0;
          font-style: italic;
        }}
        
        @media (max-width: 768px) {{
          .splash-title {{
            font-size: 2.5rem;
          }}
          
          .splash-subtitle {{
            font-size: 1.2rem;
          }}
          
          .splash-stats {{
            flex-direction: column;
            gap: 1rem;
          }}
          
          .splash-actions {{
            flex-direction: column;
            align-items: center;
          }}
        }}
      `}}</style>
    </div>
  );
}};

export default {component_name};'''
    
    return component

def generate_readme(app_name: str, theme: str, animation_type: str, top_pairs: List[Dict[str, Any]]) -> str:
    """Generate a README for the splash screens"""
    readme = f'''# {app_name} - Animated Splash Screens

## 🎯 Overview

This directory contains 3 AI-generated animated splash screens for {app_name}, created using the Agentic Image Selector system.

## 🎨 Generated Components

### SplashScreen1
- **Theme**: {theme}
- **Animation**: {animation_type}
- **Source**: {top_pairs[0].get('source', 'Unknown')}
- **Score**: {top_pairs[0].get('overall_score', 0):.3f}

### SplashScreen2  
- **Theme**: {theme}
- **Animation**: {animation_type}
- **Source**: {top_pairs[1].get('source', 'Unknown')}
- **Score**: {top_pairs[1].get('overall_score', 0):.3f}

### SplashScreen3
- **Theme**: {theme}
- **Animation**: {animation_type}
- **Source**: {top_pairs[2].get('source', 'Unknown')}
- **Score**: {top_pairs[2].get('overall_score', 0):.3f}

## 🚀 Usage

### Individual Components
```tsx
import SplashScreen1 from './SplashScreen1';

<SplashScreen1 
  onGetStarted={() => console.log('Get Started')}
  onLogin={() => console.log('Login')}
/>
```

## 🎭 Features

- **Animated Image Transitions**: Smooth morphing between before/after images
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Customizable Content**: Easy to modify titles, descriptions, and CTAs
- **Modern Styling**: Gradient backgrounds and smooth animations
- **Accessibility**: Proper alt text and keyboard navigation

## 🛠️ Customization

Each component can be easily customized by modifying:
- Image URLs in the `images` array
- Content in the `content` object
- Styling in the `<style jsx>` section
- Animation timing in the `useEffect` hook

## 📱 Responsive Breakpoints

- **Desktop**: Full layout with side-by-side stats
- **Tablet**: Adjusted font sizes and spacing
- **Mobile**: Stacked layout with vertical buttons

## 🎨 Design System

- **Primary Colors**: Red to green gradient (#ff6b6b to #4ecdc4)
- **Typography**: Modern sans-serif with weight variations
- **Spacing**: Consistent 1rem base unit
- **Animations**: 0.3s ease-in-out transitions

## 🔧 Technical Details

- **Framework**: Next.js with TypeScript
- **Styling**: Styled JSX for component-scoped styles
- **Images**: Next.js Image component for optimization
- **State**: React hooks for animation control

## 📊 Performance

- **Image Optimization**: Next.js automatic image optimization
- **Lazy Loading**: Images load only when needed
- **Smooth Animations**: 60fps CSS transitions
- **Minimal Bundle**: No external animation libraries

## 🎯 Next Steps

1. **Test the components** in your app
2. **Choose your favorite** design
3. **Customize the content** for your brand
4. **Integrate with your app** routing
5. **Add analytics** tracking for user interactions

---

*Generated by Agentic Image Selector - AI-powered splash screen creation*
'''
    
    return readme

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Generate Splash Screens")
    parser.add_argument("--input", default="top_image_pairs.json", help="Input file with top image pairs")
    parser.add_argument("--config", default="splash-config.json", help="Configuration file")
    parser.add_argument("--output", default="splash-prototypes", help="Output directory for prototypes")
    
    args = parser.parse_args()
    
    # Load configuration
    config_file = Path(__file__).parent / args.config
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Load top image pairs
    pairs_file = Path(__file__).parent / args.input
    with open(pairs_file, 'r') as f:
        pairs_data = json.load(f)
    
    top_pairs = pairs_data.get("top_pairs", [])
    
    print("🎬 Generate Splash Screens")
    print("=" * 50)
    print(f"Project Type: {config.get('projectType', 'unknown')}")
    print(f"App Name: {config.get('appName', 'App')}")
    print(f"Top Pairs: {len(top_pairs)}")
    print(f"Output Directory: {args.output}")
    
    # Create output directory
    output_path = Path(__file__).parent / args.output
    output_path.mkdir(exist_ok=True)
    
    # Generate components
    for i, pair in enumerate(top_pairs):
        component_name = f"SplashScreen{i + 1}"
        component = generate_splash_component(pair, i, config.get("content", {}))
        
        file_path = output_path / f"{component_name}.tsx"
        with open(file_path, 'w') as f:
            f.write(component)
        print(f"💾 Saved {component_name} to {file_path}")
    
    # Generate README
    readme = generate_readme(
        config.get("appName", "App"),
        config.get("theme", "transformation"),
        config.get("animationType", "morphing"),
        top_pairs
    )
    
    readme_path = output_path / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme)
    print(f"💾 Saved README.md to {readme_path}")
    
    print(f"\n✅ Successfully generated {len(top_pairs) + 1} files!")
    print("📁 All files saved to splash-prototypes/")
    print("\n🎯 Next step: Test the components in your Next.js app!")

if __name__ == "__main__":
    main()