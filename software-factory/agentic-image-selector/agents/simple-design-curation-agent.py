#!/usr/bin/env python3
"""
CLI wrapper around the simple design curation heuristics.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from simple_design_curation_core import SimpleDesignCurationAgent


def main() -> int:
    parser = argparse.ArgumentParser(description="Simple Design Curation Agent")
    parser.add_argument("--input", default="image_pairs.json", help="Input file with image pairs")
    parser.add_argument("--config", default="splash-config.json", help="Configuration file")
    parser.add_argument("--count", type=int, default=3, help="Number of top pairs to select")
    parser.add_argument("--output", default="top_image_pairs.json", help="Output file")

    args = parser.parse_args()
    script_dir = Path(__file__).parent

    config_path = script_dir / args.config
    if not config_path.exists():
        print("❌ Configuration file not found.")
        return 1

    with open(config_path, "r") as handle:
        config = json.load(handle)

    pairs_path = script_dir / args.input
    if not pairs_path.exists():
        print("❌ No image_pairs.json found. Run the image sourcing agent first.")
        return 1

    with open(pairs_path, "r") as handle:
        all_pairs = json.load(handle).get("pairs", [])

    agent = SimpleDesignCurationAgent(config)
    curated_pairs = agent.curate_image_pairs(all_pairs)
    top_pairs = agent.select_top_pairs(curated_pairs, args.count)
    agent.save_results(top_pairs, script_dir / args.output)

    print(f"✅ Curation complete! Saved {len(top_pairs)} pairs to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
