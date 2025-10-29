#!/usr/bin/env python3
"""
Weight Tracker Animation Prototype Agent

This agent creates animated splash screen prototypes using the top-curated
image pairs for the Weight Tracker app.
"""

import json
import asyncio
from pathlib import Path
from textwrap import dedent
from typing import List, Dict, Any

class AnimationPrototypeAgent:
    """Agent responsible for creating animated splash screen prototypes"""
    
    def __init__(self):
        self.template_path = Path(__file__).parent.parent / "src" / "components"
        self.output_path = Path(__file__).parent.parent / "src" / "components" / "splash-prototypes"
    
    async def create_animated_splash(self, image_pair: Dict[str, Any], rank: int) -> str:
        """Create an animated splash screen component for a specific image pair"""
        
        component_name = f"SplashScreenV{rank}"
        before_url = image_pair.get("before_url", "")
        after_url = image_pair.get("after_url", "")
        before_alt = image_pair.get("before_description") or "Before transformation"
        after_alt = image_pair.get("after_description") or "After transformation"
        
        frames = [
            {
                "src": before_url,
                "alt": before_alt,
                "headline": "Start Strong",
                "message": "Document day-one stats and set a confident baseline."
            },
            {
                "src": after_url,
                "alt": after_alt,
                "headline": "Stay Consistent",
                "message": "Celebrate habit streaks and incremental wins."
            },
        ]
        frames_json = json.dumps(frames, indent=2)
        
        component_template = """
        'use client';
        import React, { useEffect, useState } from 'react';
        import Image from 'next/image';
        import { PillButton } from '../design-system';

        interface __COMPONENT_NAME__Props {
          onCreateProfile: () => void;
          onLogin: () => void;
        }

        export const __COMPONENT_NAME__: React.FC<__COMPONENT_NAME__Props> = ({
          onCreateProfile,
          onLogin,
        }) => {
          const [currentFrame, setCurrentFrame] = useState(0);
          const [isTransitioning, setIsTransitioning] = useState(false);
          const frames = __FRAMES__;

          useEffect(() => {
            const interval = setInterval(() => {
              setIsTransitioning(true);
              setTimeout(() => {
                setCurrentFrame((prev) => (prev + 1) % frames.length);
                setIsTransitioning(false);
              }, 400);
            }, 3600);

            return () => clearInterval(interval);
          }, [frames.length]);

          const gradient = `linear-gradient(135deg,
            rgba(220,38,38,0.85) 0%,
            rgba(59,130,246,0.85) 45%,
            rgba(34,197,94,0.9) 100%
          )`;

          return (
            <div className="splash-container" style={{ background: gradient }}>
              <div className="splash-content">
                <div className="hero-visual">
                  <div className={`image-frame ${isTransitioning ? 'fade-out' : 'fade-in'}`}>
                    <Image
                      src={frames[currentFrame].src}
                      alt={frames[currentFrame].alt}
                      fill
                      priority
                      sizes="(max-width: 768px) 90vw, 480px"
                    />
                  </div>
                </div>

                <div className="copy-stack">
                  <h1 className="splash-title">{frames[currentFrame].headline}</h1>
                  <p className="splash-subtitle">{frames[currentFrame].message}</p>

                  <div className="splash-actions">
                    <PillButton variant="primary" onClick={onCreateProfile}>
                      Create Profile
                    </PillButton>
                    <PillButton variant="secondary" onClick={onLogin}>
                      Log In
                    </PillButton>
                  </div>
                </div>
              </div>

              <style jsx>{`
                .splash-container {
                  min-height: 100vh;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  padding: 2rem;
                  position: relative;
                  overflow: hidden;
                  color: #f8fafc;
                }

                .splash-content {
                  display: grid;
                  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                  gap: 3rem;
                  align-items: center;
                  width: min(1080px, 100%);
                }

                .hero-visual {
                  position: relative;
                  width: 100%;
                  aspect-ratio: 3 / 4;
                  border-radius: 32px;
                  overflow: hidden;
                  box-shadow: 0 45px 70px rgba(15, 23, 42, 0.28);
                  isolation: isolate;
                }

                .image-frame {
                  position: absolute;
                  inset: 0;
                  transition: opacity 0.4s ease;
                }

                .image-frame :global(img) {
                  object-fit: cover;
                }

                .fade-in {
                  opacity: 1;
                }

                .fade-out {
                  opacity: 0;
                }

                .copy-stack {
                  display: flex;
                  flex-direction: column;
                  gap: 1.5rem;
                }

                .splash-title {
                  font-size: clamp(2.5rem, 4vw, 3.5rem);
                  font-weight: 700;
                  letter-spacing: -0.03em;
                  margin: 0;
                }

                .splash-subtitle {
                  font-size: clamp(1.1rem, 2.2vw, 1.4rem);
                  line-height: 1.6;
                  opacity: 0.92;
                  margin: 0;
                }

                .splash-actions {
                  display: flex;
                  gap: 1rem;
                  flex-wrap: wrap;
                }

                :global(.pill-button) {
                  min-width: 160px;
                  justify-content: center;
                }

                @media (max-width: 900px) {
                  .splash-content {
                    grid-template-columns: 1fr;
                    text-align: center;
                  }

                  .copy-stack {
                    align-items: center;
                  }

                  .splash-actions {
                    justify-content: center;
                  }
                }
              `}</style>
            </div>
          );
        };
        """
        
        component_code = dedent(component_template).strip()
        component_code = component_code.replace("__COMPONENT_NAME__", component_name)
        component_code = component_code.replace("__FRAMES__", frames_json)
        return component_code
    
    async def create_comparison_page(self, top_pairs: List[Dict[str, Any]]) -> str:
        """Create a comparison page to showcase all three prototypes"""
        
        imports = "\n".join(
            f"import {{ SplashScreenV{i} }} from '../../components/splash-prototypes/SplashScreenV{i}';"
            for i in range(1, len(top_pairs) + 1)
        )
        
        version_entries = []
        for i, pair in enumerate(top_pairs, start=1):
            score = pair.get("scores", {}).get("overall", 0.0)
            version_entries.append(
                f"    {{ id: {i}, name: 'Version {i}', component: SplashScreenV{i}, score: {score:.2f} }}"
            )
        versions_block = ",\n".join(version_entries) if version_entries else "    // No prototypes generated yet"
        
        comparison_template = """
        'use client';
        import React, { useState } from 'react';
        __IMPORTS__

        export default function SplashComparison() {
          const [currentVersion, setCurrentVersion] = useState(1);
          const versions = [
        __VERSIONS__
          ];

          const CurrentComponent = versions.find((version) => version.id === currentVersion)?.component;

          const handleCreateProfile = () => {
            console.log('Create Profile clicked');
          };

          const handleLogin = () => {
            console.log('Login clicked');
          };

          return (
            <div className="comparison-container">
              <div className="version-selector">
                {versions.map((version) => (
                  <button
                    key={version.id}
                    className={`version-button ${currentVersion === version.id ? 'active' : ''}`}
                    onClick={() => setCurrentVersion(version.id)}
                  >
                    <span className="version-name">{version.name}</span>
                    <span className="score">Score: {version.score.toFixed(2)}</span>
                  </button>
                ))}
              </div>

              <div className="prototype-container">
                {CurrentComponent ? (
                  <CurrentComponent onCreateProfile={handleCreateProfile} onLogin={handleLogin} />
                ) : (
                  <div className="empty-state">
                    <p>No prototypes generated yet.</p>
                  </div>
                )}
              </div>

              <style jsx>{`
                .comparison-container {
                  min-height: 100vh;
                  background: #f5f7fa;
                }

                .version-selector {
                  position: sticky;
                  top: 0;
                  display: flex;
                  flex-wrap: wrap;
                  gap: 0.75rem;
                  justify-content: center;
                  background: rgba(255, 255, 255, 0.92);
                  padding: 1rem;
                  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
                  backdrop-filter: blur(10px);
                  z-index: 10;
                }

                .version-button {
                  min-width: 180px;
                  border-radius: 999px;
                  padding: 0.75rem 1.25rem;
                  border: 2px solid #e2e8f0;
                  background: white;
                  display: flex;
                  flex-direction: column;
                  gap: 0.25rem;
                  align-items: center;
                  transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
                }

                .version-button:hover {
                  transform: translateY(-2px);
                  border-color: #38bdf8;
                  box-shadow: 0 16px 32px rgba(56, 189, 248, 0.18);
                }

                .version-button.active {
                  border-color: #22c55e;
                  background: linear-gradient(135deg, #ecfeff 0%, #dcfce7 100%);
                }

                .version-name {
                  font-weight: 600;
                  color: #0f172a;
                }

                .score {
                  font-size: 0.85rem;
                  color: #475569;
                }

                .prototype-container {
                  padding: 2rem 0 4rem;
                }

                .empty-state {
                  padding: 6rem 2rem;
                  text-align: center;
                  color: #64748b;
                }
              `}</style>
            </div>
          );
        }
        """
        
        comparison_code = dedent(comparison_template).strip()
        comparison_code = comparison_code.replace("__IMPORTS__", imports or "// No prototypes to import yet")
        comparison_code = comparison_code.replace("__VERSIONS__", versions_block)
        
        return comparison_code
    
    async def generate_prototypes(self, top_pairs: List[Dict[str, Any]]) -> None:
        """Generate all splash screen prototypes"""
        print("🎬 Creating animated splash screen prototypes...")
        
        # Create output directory
        self.output_path.mkdir(exist_ok=True)
        
        # Generate individual components
        for i, pair in enumerate(top_pairs, 1):
            print(f"🎨 Creating Version {i}...")
            component_code = await self.create_animated_splash(pair, i)
            
            component_file = self.output_path / f"SplashScreenV{i}.tsx"
            with open(component_file, 'w') as f:
                f.write(component_code)
            
            print(f"   ✅ Created {component_file}")
        
        # Generate comparison page
        print("📊 Creating comparison page...")
        comparison_code = await self.create_comparison_page(top_pairs)
        
        comparison_file = self.template_path.parent / "app" / "splash-comparison" / "page.tsx"
        comparison_file.parent.mkdir(exist_ok=True)
        
        with open(comparison_file, 'w') as f:
            f.write(comparison_code)
        
        print(f"   ✅ Created {comparison_file}")
        
        # Generate README with instructions
        readme_content = f'''# Weight Tracker Splash Screen Prototypes

## Overview
This directory contains {len(top_pairs)} animated splash screen prototypes for the Weight Tracker app, generated using AI-powered image sourcing and design curation.

## Prototypes

'''
        
        for i, pair in enumerate(top_pairs, 1):
            scores = pair.get('scores', {})
            readme_content += f'''### Version {i} (Score: {scores.get('overall', 0.0):.2f})
- **Commercial Appeal**: {scores.get('commercial_appeal', 0.0):.2f}
- **Animation Potential**: {scores.get('animation_potential', 0.0):.2f}
- **Design Quality**: {scores.get('design_quality', 0.0):.2f}

**Implementation Suggestions**:
'''
            for suggestion in pair.get('implementation_suggestions', []):
                readme_content += f"- {suggestion}\n"
            readme_content += "\n"
        
        readme_content += '''## Usage

1. **View All Prototypes**: Visit `/splash-comparison` to see all versions side by side
2. **Test Individual Versions**: Import and use individual components in your app
3. **Customize**: Modify the animation timing, colors, and messaging as needed

## Next Steps

1. **User Testing**: Test the prototypes with real users
2. **A/B Testing**: Implement A/B testing to measure conversion rates
3. **Final Selection**: Choose the best-performing prototype
4. **Integration**: Integrate the selected prototype into the main app

## Technical Details

- Built with React 19 and Next.js 15
- Uses CSS-in-JS for styling
- Responsive design for mobile and desktop
- Smooth animations with CSS keyframes
- Accessible design with proper ARIA labels
'''
        
        readme_file = self.output_path / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        print(f"   ✅ Created {readme_file}")

async def main():
    """Main execution function"""
    print("🎬 Weight Tracker Animation Prototype Agent")
    print("=" * 50)
    
    # Load top image pairs from curation agent
    input_file = Path(__file__).parent / "top_image_pairs.json"
    if not input_file.exists():
        print("❌ No top_image_pairs.json found. Run the design curation agent first.")
        return
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    top_pairs = data["top_pairs"]
    print(f"📁 Loaded {len(top_pairs)} top image pairs for prototyping")
    
    agent = AnimationPrototypeAgent()
    
    try:
        # Generate prototypes
        await agent.generate_prototypes(top_pairs)
        
        print(f"\n✅ Prototype generation complete!")
        print(f"🎨 Created {len(top_pairs)} animated splash screen prototypes")
        print(f"📊 Created comparison page at /splash-comparison")
        print(f"📁 All files saved to src/components/splash-prototypes/")
        print("\n🎯 Next step: Test the prototypes and select the best one for production.")
        
    except Exception as e:
        print(f"❌ Error during prototype generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
