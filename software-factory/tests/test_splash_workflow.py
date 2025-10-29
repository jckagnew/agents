#!/usr/bin/env python3
"""
Smoke test to ensure the splash generation CLI produces artifacts.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def test_create_splash_smoke(tmp_path):
    project_root = tmp_path / "demo-app"
    (project_root / "src" / "components").mkdir(parents=True)
    (project_root / "src" / "app").mkdir(parents=True)

    cmd = [
        sys.executable,
        "create_splash.py",
        "--project-type",
        "fitness",
        "--app-name",
        "Test Splash",
        "--project-root",
        str(project_root),
    ]

    subprocess.run(cmd, cwd=BASE_DIR, check=True)

    components_dir = project_root / "src" / "components" / "splash-prototypes"
    comparison_page = project_root / "src" / "app" / "splash-comparison" / "page.tsx"

    assert components_dir.exists()
    assert any(components_dir.glob("SplashScreen*.tsx"))
    assert (components_dir / "README.md").exists()
    assert comparison_page.exists()
