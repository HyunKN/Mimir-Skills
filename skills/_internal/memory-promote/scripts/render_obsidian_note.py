#!/usr/bin/env python3
"""Render a thin Obsidian-friendly note from a memory artifact JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a thin Obsidian-friendly note from one memory artifact JSON file."
    )
    parser.add_argument("artifact_path", help="Path to the memory artifact JSON file.")
    parser.add_argument(
        "--output",
        help="Optional output Markdown path. Defaults to a sibling reports directory when possible.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    artifact_path = Path(args.artifact_path)

    if not artifact_path.is_file():
        print(f"Memory artifact not found: {artifact_path}", file=sys.stderr)
        return 1

    try:
        artifact = json.loads(artifact_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        print(
            f"Invalid JSON in {artifact_path}: {exc.msg} at line {exc.lineno}, column {exc.colno}",
            file=sys.stderr,
        )
        return 1

    if not isinstance(artifact, dict):
        print("Memory artifact must be a JSON object.", file=sys.stderr)
        return 1

    artifact_id = artifact.get("id")
    status = artifact.get("status")
    if not isinstance(artifact_id, str) or not artifact_id.strip():
        print("Memory artifact must include a non-empty string id.", file=sys.stderr)
        return 1
    if not isinstance(status, str) or not status.strip():
        print("Memory artifact must include a non-empty string status.", file=sys.stderr)
        return 1

    output_path = Path(args.output) if args.output else default_output_path(artifact_path, artifact_id, status)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_note(artifact, artifact_path), encoding="utf-8")

    print(f"Rendered Obsidian note: {output_path}")
    return 0


def default_output_path(artifact_path: Path, artifact_id: str, status: str) -> Path:
    if artifact_path.parent.parent.name == "memories" and artifact_path.parent.parent.parent.name == "records":
        return artifact_path.parent.parent.parent / "reports" / f"{artifact_id}-{status}.md"
    return artifact_path.with_name(f"{artifact_id}-{status}.md")


def render_note(artifact: dict[str, Any], artifact_path: Path) -> str:
    artifact_id = str(artifact["id"]).strip()
    status = str(artifact["status"]).strip()
    statement = artifact.get("statement")
    scope = artifact.get("scope")

    lines = [f"# {artifact_id} ({status})", "", f"- Memory ID: `{artifact_id}`", f"- Status: `{status}`", ""]

    lines.append("## Source of Truth")
    lines.append("")
    lines.append(f"- Canonical JSON: `{display_path(artifact_path)}`")
    lines.append("")

    if isinstance(statement, str) and statement.strip():
        lines.append("## Statement")
        lines.append("")
        lines.append(statement.strip())
        lines.append("")

    if isinstance(scope, str) and scope.strip():
        lines.append("## Scope")
        lines.append("")
        lines.append(scope.strip())
        lines.append("")

    related: list[str] = []
    source_decision_ids = artifact.get("source_decision_ids")
    if isinstance(source_decision_ids, list):
        decision_ids = [item.strip() for item in source_decision_ids if isinstance(item, str) and item.strip()]
        if decision_ids:
            related.append("- Source decisions: " + ", ".join(f"[[{item}]]" for item in decision_ids))

    counterpart = counterpart_note_name(artifact_id, status)
    if counterpart:
        related.append(f"- Counterpart memory note: [[{counterpart}]]")

    if related:
        lines.append("## Related Artifacts")
        lines.append("")
        lines.extend(related)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def counterpart_note_name(artifact_id: str, status: str) -> str | None:
    if status == "candidate":
        return f"{artifact_id}-validated"
    if status == "validated":
        return f"{artifact_id}-candidate"
    return None


def display_path(path: Path) -> str:
    parts = list(path.parts)
    if ".ai" in parts:
        start = parts.index(".ai")
        return "/".join(parts[start:])
    return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
