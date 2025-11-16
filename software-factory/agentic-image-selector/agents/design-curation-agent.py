#!/usr/bin/env python3
"""
Default design curation agent invoked by the orchestration workflow.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from simple_design_curation_core import SimpleDesignCurationAgent


def main() -> int:
    parser = argparse.ArgumentParser(description="Design Curation Agent")
    parser.add_argument("--config", required=True, help="Temp configuration file injected by the orchestrator")

    args = parser.parse_args()
    config_path = Path(args.config)
    if not config_path.exists():
        print("❌ Configuration file missing.")
        return 1

    with open(config_path, "r") as handle:
        config = json.load(handle)

    agent_dir = Path(__file__).parent
    pairs_path = agent_dir / "image_pairs.json"
    if not pairs_path.exists():
        print("❌ image_pairs.json not found. Run the image sourcing phase first.")
        return 1

    with open(pairs_path, "r") as handle:
        pairs_data = json.load(handle)

    image_pairs = pairs_data.get("pairs", [])
    if not image_pairs:
        print("❌ No image pairs available for curation.")
        return 1

    agent = SimpleDesignCurationAgent(config)
    curated_pairs = agent.curate_image_pairs(image_pairs)
    top_pairs = agent.select_top_pairs(curated_pairs)
    agent.save_results(top_pairs, agent_dir / "top_image_pairs.json")

    print(f"✅ Selected {len(top_pairs)} top image pairs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
