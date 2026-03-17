from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import install_codex
from .workflows import prepare_handoff, write_pr_rationale


def load_manifest() -> dict:
    manifest_path = Path(__file__).with_name("manifest.json")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m mimir_skills",
        description="Shared helper surface for Mimir-Skills workflows.",
    )
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser(
        "list",
        help="List the current outward-facing workflows and their availability.",
    )
    list_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the lightweight workflow manifest as JSON.",
    )

    install_parser = subparsers.add_parser(
        "install",
        help="Install the current outward-facing workflows into a local Codex skills directory.",
    )
    install_parser.add_argument(
        "adapter",
        nargs="?",
        default="codex",
        choices=["codex"],
        help="Install target. Currently only `codex` is supported.",
    )
    install_parser.add_argument(
        "--codex-home",
        type=Path,
        default=None,
        help="Override CODEX_HOME. Defaults to $CODEX_HOME or ~/.codex.",
    )
    install_parser.add_argument(
        "--workflows",
        nargs="+",
        choices=sorted(install_codex.WORKFLOW_DEPENDENCIES),
        default=sorted(install_codex.WORKFLOW_DEPENDENCIES),
        help="Install only the selected outward-facing workflows and their dependencies.",
    )
    install_parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing installed folders for the selected workflows and support assets.",
    )

    subparsers.add_parser(
        "prepare-handoff",
        add_help=False,
        help="Show the deprecated prepare-handoff helper note and point back to the skill-first path.",
    )
    subparsers.add_parser(
        "write-pr-rationale",
        add_help=False,
        help="Show the deprecated write-pr-rationale helper note and point back to the skill-first path.",
    )

    return parser


def render_manifest_lines(manifest: dict) -> list[str]:
    lines = ["Mimir-Skills workflows and helper surfaces:", ""]
    for workflow in manifest.get("workflows", []):
        if not isinstance(workflow, dict):
            continue
        name = workflow.get("name", "(unknown)")
        summary = workflow.get("summary", "")
        availability = workflow.get("availability", "unknown")
        lines.append(f"- {name} [{availability}]")
        if summary:
            lines.append(f"  {summary}")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args, remaining = parser.parse_known_args(argv)

    if args.command == "list":
        manifest = load_manifest()
        if args.json:
            print(json.dumps(manifest, indent=2))
        else:
            print("\n".join(render_manifest_lines(manifest)))
        return 0

    if args.command == "prepare-handoff":
        return prepare_handoff.generate_main(remaining)

    if args.command == "write-pr-rationale":
        return write_pr_rationale.generate_main(remaining)

    if args.command == "install":
        return install_codex.run_install(
            codex_home=args.codex_home,
            workflows=args.workflows,
            force=args.force,
        )

    parser.print_help()
    return 0
