#!/usr/bin/env python3
"""
Helper CLI to run the agentic splash workflow against a target project.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


REPO_ROOT = Path(__file__).resolve().parent
AGENT_DIR = REPO_ROOT / "agentic-image-selector" / "agents"
CONFIG_PATH = AGENT_DIR / "splash-config.json"


def run_orchestrator(args_list: list[str]) -> int:
    cmd = [sys.executable, "orchestration-agent.py", *args_list]
    proc = subprocess.run(cmd, cwd=AGENT_DIR)
    return proc.returncode


def merge_brief(config: Dict[str, Any], brief_path: Path) -> Dict[str, Any]:
    with open(brief_path, "r") as handle:
        brief = json.load(handle)

    merged = {**config}
    merged.update({k: v for k, v in brief.items() if k not in {"content"}})

    if "content" in brief:
        merged.setdefault("content", {})
        merged["content"].update(brief["content"])

    return merged


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate splash screens with the agentic workflow")
    parser.add_argument("--project-type", default="fitness", help="Project type (fitness, finance, productivity, custom)")
    parser.add_argument("--app-name", default="Splash Demo", help="Application name for generated components")
    parser.add_argument("--project-root", type=Path, default=REPO_ROOT / "generated-apps" / "weight-tracker-nextjs",
                        help="Path to the Next.js project that should receive the outputs")
    parser.add_argument("--brief", type=Path, help="Optional JSON creative brief to merge into the config")
    parser.add_argument("--theme", help="Override theme (e.g. transformation)")
    parser.add_argument("--colors", help="Override color scheme (e.g. red-to-green)")
    parser.add_argument("--animation", help="Override animation type (e.g. morphing)")
    parser.add_argument("--cta-primary", help="Primary CTA label")
    parser.add_argument("--cta-secondary", help="Secondary CTA label")

    args = parser.parse_args()
    target_project = args.project_root.expanduser().resolve()

    if not target_project.exists():
        print(f"❌ Project root {target_project} does not exist.")
        return 1

    init_args = ["--init", "--project-type", args.project_type, "--app-name", args.app_name]
    if args.theme:
        init_args += ["--theme", args.theme]
    if args.colors:
        init_args += ["--colors", args.colors]
    if args.animation:
        init_args += ["--animation", args.animation]
    if args.cta_primary:
        init_args += ["--cta-primary", args.cta_primary]
    if args.cta_secondary:
        init_args += ["--cta-secondary", args.cta_secondary]

    print("🛠️  Preparing splash configuration...")
    if run_orchestrator(init_args) != 0:
        print("❌ Failed to initialise splash configuration.")
        return 1

    with open(CONFIG_PATH, "r") as handle:
        config = json.load(handle)

    config["outputPath"] = str(target_project)
    if args.brief:
        config = merge_brief(config, args.brief.resolve())

    with open(CONFIG_PATH, "w") as handle:
        json.dump(config, handle, indent=2)

    print("🚀 Running agentic splash workflow...")
    if run_orchestrator(["--run"]) != 0:
        print("❌ Splash workflow failed. Check logs above for details.")
        return 1

    results_path = target_project / "splash-generation-results.json"
    if results_path.exists():
        print(f"📊 Workflow summary available at {results_path}")

    components_dir = target_project / "src" / "components" / "splash-prototypes"
    comparison_page = target_project / "src" / "app" / "splash-comparison" / "page.tsx"

    print("✅ Splash screens generated successfully!")
    print(f"🎨 Components directory: {components_dir}")
    print(f"📄 Comparison page: {comparison_page}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
