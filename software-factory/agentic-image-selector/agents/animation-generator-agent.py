#!/usr/bin/env python3
"""
Animation Generator Agent for Agentic Image Selector

This script coordinates prototype generation by reusing the simple animation
agent, saving outputs into the project workspace, and building a comparison page.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from textwrap import dedent
from typing import Any, Dict, List

from simple_animation_core import SimpleAnimationPrototypeAgent


def load_config(config_path: Path) -> Dict[str, Any]:
    with open(config_path, "r") as handle:
        return json.load(handle)


def load_top_pairs(pairs_path: Path) -> List[Dict[str, Any]]:
    with open(pairs_path, "r") as handle:
        data = json.load(handle)
    return data.get("top_pairs", [])


def ensure_project_paths(project_root: Path) -> Dict[str, Path]:
    components_dir = project_root / "src" / "components" / "splash-prototypes"
    comparison_dir = project_root / "src" / "app" / "splash-comparison"

    components_dir.mkdir(parents=True, exist_ok=True)
    comparison_dir.mkdir(parents=True, exist_ok=True)

    return {
        "components_dir": components_dir,
        "comparison_dir": comparison_dir,
    }


def save_prototypes(
    agent: SimpleAnimationPrototypeAgent,
    top_pairs: List[Dict[str, Any]],
    destination: Path,
) -> List[str]:
    prototypes = agent.generate_prototypes(top_pairs)

    written_files: List[str] = []
    for name, content in prototypes.items():
        if name == "README.md":
            target = destination / name
        else:
            target = destination / f"{name}.tsx"

        with open(target, "w") as handle:
            handle.write(content)
        written_files.append(str(target))

    return written_files


def build_comparison_page(top_pairs: List[Dict[str, Any]]) -> str:
    imports = "\n".join(
        f"import SplashScreen{i} from '../../components/splash-prototypes/SplashScreen{i}';"
        for i in range(1, len(top_pairs) + 1)
    )

    versions = []
    for i, pair in enumerate(top_pairs, start=1):
        score = pair.get("scores", {}).get("overall", pair.get("overall_score", 0.0))
        versions.append(
            f"    {{ id: {i}, name: 'Version {i}', component: SplashScreen{i}, score: {score:.2f} }}"
        )

    versions_block = ",\n".join(versions) if versions else "    // Add prototypes"

    template = """
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
              <CurrentComponent onGetStarted={handleCreateProfile} onLogin={handleLogin} />
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

    page = dedent(template).strip()
    page = page.replace("__IMPORTS__", imports or "// Add splash screen imports")
    page = page.replace("__VERSIONS__", versions_block)
    return page


def main() -> int:
    parser = argparse.ArgumentParser(description="Animation generator for Agentic Image Selector")
    parser.add_argument("--config", required=True, help="Path to temporary configuration file")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print("❌ Configuration file not found.")
        return 1

    config = load_config(config_path)

    output_root = Path(config.get("outputPath", Path.cwd()))
    project_paths = ensure_project_paths(output_root)

    pairs_path = Path(__file__).parent / "top_image_pairs.json"
    if not pairs_path.exists():
        print("❌ No top_image_pairs.json found. Run the design curation agent first.")
        return 1

    top_pairs = load_top_pairs(pairs_path)
    if not top_pairs:
        print("❌ No curated image pairs available to generate prototypes.")
        return 1

    agent = SimpleAnimationPrototypeAgent(config)
    written_files = save_prototypes(agent, top_pairs, project_paths["components_dir"])

    comparison_page = build_comparison_page(top_pairs)
    comparison_file = project_paths["comparison_dir"] / "page.tsx"
    comparison_file.write_text(comparison_page)
    written_files.append(str(comparison_file))

    print("✅ Animation generation complete!")
    print(f"📁 Components saved to {project_paths['components_dir']}")
    print(f"📄 Comparison page saved to {comparison_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
