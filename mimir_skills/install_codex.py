"""Backward-compatibility shim — delegates to mimir_skills.install with target='codex'."""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

from .install import WORKFLOW_DEPENDENCIES, run_install as _run_install


def run_install(
    *,
    codex_home: Path | None = None,
    workflows: Sequence[str] | None = None,
    force: bool = False,
    repo_root: Path | None = None,
) -> int:
    return _run_install(
        target="codex",
        codex_home=codex_home,
        workflows=workflows,
        force=force,
        repo_root=repo_root,
    )


def main(argv: Sequence[str] | None = None) -> int:
    from .install import build_parser as _build_parser

    parser = _build_parser()
    args = parser.parse_args(argv)
    return _run_install(
        target=args.target or "codex",
        codex_home=args.codex_home,
        project_dir=getattr(args, "project_dir", None),
        workflows=args.workflows,
        force=args.force,
    )


__all__ = [
    "WORKFLOW_DEPENDENCIES",
    "main",
    "run_install",
]
