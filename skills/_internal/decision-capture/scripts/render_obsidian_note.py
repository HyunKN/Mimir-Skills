#!/usr/bin/env python3
"""Render a thin Obsidian-friendly note from a canonical decision record JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a thin Obsidian-friendly note from one decision record JSON file."
    )
    parser.add_argument("record_path", help="Path to the canonical decision record JSON file.")
    parser.add_argument(
        "--output",
        help="Optional output Markdown path. Defaults to a sibling reports directory when possible.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    record_path = Path(args.record_path)

    if not record_path.is_file():
        print(f"Decision record not found: {record_path}", file=sys.stderr)
        return 1

    try:
        record = json.loads(record_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        print(
            f"Invalid JSON in {record_path}: {exc.msg} at line {exc.lineno}, column {exc.colno}",
            file=sys.stderr,
        )
        return 1

    if not isinstance(record, dict):
        print("Decision record must be a JSON object.", file=sys.stderr)
        return 1

    record_id = record.get("id")
    if not isinstance(record_id, str) or not record_id.strip():
        print("Decision record must include a non-empty string id.", file=sys.stderr)
        return 1

    output_path = Path(args.output) if args.output else default_output_path(record_path, record_id)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_note(record, record_path), encoding="utf-8")

    print(f"Rendered Obsidian note: {output_path}")
    return 0


def default_output_path(record_path: Path, record_id: str) -> Path:
    if record_path.parent.name == "decisions" and record_path.parent.parent.name == "records":
        return record_path.parent.parent / "reports" / f"{record_id}.md"
    return record_path.with_name(f"{record_id}.md")


def render_note(record: dict[str, Any], record_path: Path) -> str:
    record_id = str(record["id"]).strip()
    title = record_id
    task_ref = record.get("task_ref")
    if isinstance(task_ref, dict):
        raw_title = task_ref.get("title")
        if isinstance(raw_title, str) and raw_title.strip():
            title = raw_title.strip()

    lines = [f"# {title}", "", f"- Decision ID: `{record_id}`", ""]

    lines.append("## Source of Truth")
    lines.append("")
    lines.append(f"- Canonical JSON: `{display_path(record_path)}`")
    lines.append("")

    summary = record.get("decision")
    if isinstance(summary, str) and summary.strip():
        lines.append("## Summary")
        lines.append("")
        lines.append(summary.strip())
        lines.append("")

    related: list[str] = []
    supersedes = record.get("supersedes")
    if isinstance(supersedes, list):
        superseded_ids = [item.strip() for item in supersedes if isinstance(item, str) and item.strip()]
        if superseded_ids:
            related.append("- Supersedes: " + ", ".join(f"[[{item}]]" for item in superseded_ids))

    if related:
        lines.append("## Related Artifacts")
        lines.append("")
        lines.extend(related)
        lines.append("")

    follow_up = record.get("follow_up")
    if isinstance(follow_up, list):
        bullets = [item.strip() for item in follow_up if isinstance(item, str) and item.strip()]
        if bullets:
            lines.append("## Follow-Up")
            lines.append("")
            lines.extend(f"- {item}" for item in bullets)
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def display_path(path: Path) -> str:
    parts = list(path.parts)
    if ".ai" in parts:
        start = parts.index(".ai")
        return "/".join(parts[start:])
    return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
