#!/usr/bin/env python3
"""
CLI wrapper for the simple animation prototype generator.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from simple_animation_core import SimpleAnimationPrototypeAgent


def load_pairs(pairs_path: Path) -> List[Dict[str, Any]]:
    with open(pairs_path, "r") as handle:
        data = json.load(handle)
    return data.get("top_pairs", [])


def main() -> int:
    parser = argparse.ArgumentParser(description="Simple Animation Prototype Agent")
    parser.add_argument("--input", default="top_image_pairs.json", help="Input file with top image pairs")
    parser.add_argument("--config", default="splash-config.json", help="Configuration file")
    parser.add_argument("--output", default="splash-prototypes", help="Output directory for prototypes")

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    config_file = script_dir / args.config
    if not config_file.exists():
        print("❌ Configuration file not found.")
        return 1

    with open(config_file, "r") as handle:
        config = json.load(handle)

    pairs_file = script_dir / args.input
    if not pairs_file.exists():
        print("❌ No top image pairs found. Run the mcp sourcing workflow first.")
        return 1

    top_pairs = load_pairs(pairs_file)
    if not top_pairs:
        print("❌ No curated image pairs available.")
        return 1

    output_dir = script_dir / args.output

    agent = SimpleAnimationPrototypeAgent(config)
    prototypes = agent.generate_prototypes(top_pairs)
    agent.save_prototypes(prototypes, output_dir)

    print(f"\n✅ Successfully generated {len(prototypes)} prototype artifacts.")
    print(f"📁 Files saved to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
