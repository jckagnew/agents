"""
Core utilities for generating splash screen prototypes used across CLI agents.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


class SimpleAnimationPrototypeAgent:
    """Generates React splash screen prototypes based on curated image pairs."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.project_type = config.get("projectType", "unknown")
        self.app_name = config.get("appName", "App")
        self.theme = config.get("theme", "transformation")
        self.color_scheme = config.get("colorScheme", "red-to-green")
        self.animation_type = config.get("animationType", "morphing")
        self.content = config.get("content", {})

    def generate_splash_component(self, pair: Dict[str, Any], index: int) -> str:
        component_name = f"SplashScreen{index + 1}"

        before_url = pair.get("before_url", "")
        after_url = pair.get("after_url", "")

        title = self.content.get("title", "Transform Your Life")
        subtitle = self.content.get("subtitle", "Track. Transform. Triumph.")
        description = self.content.get("description", "Your journey starts here.")
        cta_primary = self.content.get("ctaPrimary", "Create Profile")
        cta_secondary = self.content.get("ctaSecondary", "Log In")

        stats = self.content.get("stats", [])
        stats_html = ""
        for stat in stats:
            value = stat.get("value", "")
            label = stat.get("label", "")
            stats_html += (
                "        <div className=\"stat-item\">\n"
                f"          <div className=\"stat-value\">{value}</div>\n"
                f"          <div className=\"stat-label\">{label}</div>\n"
                "        </div>\n"
            )

        component = f"""import React, {{ useState, useEffect }} from 'react';
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

export default {component_name};"""

        return component

    def generate_readme(self, top_pairs: List[Dict[str, Any]]) -> str:
        base = Path(__file__).parent.name.replace("-", " ").title()

        readme = f"""# {self.app_name} - Animated Splash Screens

## 🎯 Overview

This directory contains {len(top_pairs)} AI-generated animated splash screens for {self.app_name}, created using the Agentic Image Selector system.

## 🎨 Generated Components
"""

        for idx, pair in enumerate(top_pairs, start=1):
            readme += f"""
### SplashScreen{idx}
- **Theme**: {self.theme}
- **Animation**: {self.animation_type}
- **Source**: {pair.get('source', 'Unknown')}
- **Score**: {pair.get('overall_score', 0):.3f}
"""

        readme += """
## 🚀 Usage

### Individual Components
```tsx
import SplashScreen1 from './SplashScreen1';

<SplashScreen1 
  onGetStarted={() => console.log('Get Started')}
  onLogin={() => console.log('Login')}
/>;
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

---

*Generated by Agentic Image Selector - AI-powered splash screen creation*
"""

        return readme

    def generate_prototypes(self, top_pairs: List[Dict[str, Any]]) -> Dict[str, str]:
        prototypes: Dict[str, str] = {}

        for idx, pair in enumerate(top_pairs):
            name = f"SplashScreen{idx + 1}"
            prototypes[name] = self.generate_splash_component(pair, idx)

        prototypes["README.md"] = self.generate_readme(top_pairs)
        return prototypes

    def save_prototypes(self, prototypes: Dict[str, str], output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)

        for name, content in prototypes.items():
            if name == "README.md":
                target = output_dir / name
            else:
                target = output_dir / f"{name}.tsx"

            with open(target, "w") as handle:
                handle.write(content)

