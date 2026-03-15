#!/usr/bin/env python3
"""Thin wrapper for the shared write-pr-rationale generator."""

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
    raise RuntimeError("Could not locate the decision_skills package for write-pr-rationale.")


bootstrap_package_root()

from decision_skills.workflows.write_pr_rationale import generate_main


if __name__ == "__main__":
    raise SystemExit(generate_main())
