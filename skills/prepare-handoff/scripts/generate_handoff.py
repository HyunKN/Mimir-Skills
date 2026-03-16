#!/usr/bin/env python3
"""Thin wrapper for the shared prepare-handoff generator."""

from __future__ import annotations

import sys
from pathlib import Path


def bootstrap_package_root() -> None:
    script_path = Path(__file__).resolve()
    for parent in script_path.parents:
        if (parent / "mimir_skills").is_dir():
            sys.path.insert(0, str(parent))
            return
        support_root = parent / "mimir-skills-support"
        if (support_root / "mimir_skills").is_dir():
            sys.path.insert(0, str(support_root))
            return
    raise RuntimeError("Could not locate the mimir_skills package for prepare-handoff.")


bootstrap_package_root()

from mimir_skills.workflows.prepare_handoff import generate_main


if __name__ == "__main__":
    raise SystemExit(generate_main())
