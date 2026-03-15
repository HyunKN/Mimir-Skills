#!/usr/bin/env python3
"""Thin wrapper for the shared prepare-handoff collector."""

from __future__ import annotations

import sys
from pathlib import Path


def bootstrap_package_root() -> None:
    script_path = Path(__file__).resolve()
    for parent in script_path.parents:
        if (parent / "decision_skills").is_dir():
            sys.path.insert(0, str(parent))
            return
        support_root = parent / "decision-skills-support"
        if (support_root / "decision_skills").is_dir():
            sys.path.insert(0, str(support_root))
            return
    raise RuntimeError("Could not locate the decision_skills package for prepare-handoff.")


bootstrap_package_root()

from decision_skills.workflows.prepare_handoff import collect_main


if __name__ == "__main__":
    raise SystemExit(collect_main())
