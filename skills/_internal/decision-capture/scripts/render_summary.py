#!/usr/bin/env python3
"""Render a Markdown summary from a canonical decision record JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a derived Markdown summary from one decision record JSON file."
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

    markdown = render_summary(record)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"Rendered Markdown summary: {output_path}")
    return 0


def default_output_path(record_path: Path, record_id: str) -> Path:
    if record_path.parent.name == "decisions" and record_path.parent.parent.name == "records":
        return record_path.parent.parent / "reports" / f"{record_id}-summary.md"
    return record_path.with_name(f"{record_id}-summary.md")


def render_summary(record: dict[str, Any]) -> str:
    task_ref = record.get("task_ref")
    title = ""
    if isinstance(task_ref, dict):
        raw_title = task_ref.get("title")
        if isinstance(raw_title, str):
            title = raw_title.strip()

    record_id = record["id"]
    lines: list[str] = []
    lines.append(f"# {title} Decision Summary" if title else "# Decision Summary")
    lines.append("")
    lines.append(f"> Derived from canonical decision record `{record_id}`.")
    lines.append("")

    add_text_section(lines, "Decision", record.get("decision"))
    add_text_section(lines, "Context", record.get("problem_context"))
    add_selected_option_section(lines, record.get("selected_option"))
    add_text_section(lines, "Why", record.get("rationale"))
    add_alternatives_section(lines, record.get("alternatives_considered"))
    add_evidence_section(lines, record.get("evidence_refs"))
    add_string_list_section(lines, "Affected Paths", record.get("affected_paths"), code=True)
    add_validation_section(lines, record.get("validation_run"))
    add_string_list_section(lines, "Remaining Risks", record.get("remaining_risks"))
    add_string_list_section(lines, "Follow-Up", record.get("follow_up"))
    add_string_list_section(lines, "Supersedes", record.get("supersedes"), code=True)
    add_confidence_section(lines, record.get("confidence"))

    return "\n".join(lines).rstrip() + "\n"


def add_text_section(lines: list[str], heading: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        return
    lines.append(f"## {heading}")
    lines.append("")
    lines.append(value.strip())
    lines.append("")


def add_selected_option_section(lines: list[str], value: Any) -> None:
    if not isinstance(value, dict):
        return
    name = value.get("name")
    summary = value.get("summary")
    bullets = []
    if isinstance(name, str) and name.strip():
        bullets.append(name.strip())
    if isinstance(summary, str) and summary.strip():
        bullets.append(summary.strip())
    if not bullets:
        return
    lines.append("## Selected Option")
    lines.append("")
    for bullet in bullets:
        lines.append(f"- {bullet}")
    lines.append("")


def add_alternatives_section(lines: list[str], value: Any) -> None:
    if not isinstance(value, list) or not value:
        return
    rendered: list[str] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        status = item.get("status")
        reason = item.get("reason")
        if not all(isinstance(part, str) and part.strip() for part in (name, status, reason)):
            continue
        rendered.append(f"- {name.strip()} ({status.strip()}): {reason.strip()}")
    if not rendered:
        return
    lines.append("## Alternatives Considered")
    lines.append("")
    lines.extend(rendered)
    lines.append("")


def add_evidence_section(lines: list[str], value: Any) -> None:
    if not isinstance(value, list) or not value:
        return
    rendered: list[str] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        kind = item.get("kind")
        ref = item.get("ref")
        summary = item.get("summary")
        captured_at = item.get("captured_at")
        if not all(isinstance(part, str) and part.strip() for part in (kind, ref, summary, captured_at)):
            continue
        rendered.append(
            f"- [{kind.strip()}] `{ref.strip()}`: {summary.strip()} (captured {captured_at.strip()})"
        )
    if not rendered:
        return
    lines.append("## Evidence")
    lines.append("")
    lines.extend(rendered)
    lines.append("")


def add_validation_section(lines: list[str], value: Any) -> None:
    if not isinstance(value, list) or not value:
        return
    rendered: list[str] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        record_type = item.get("type")
        command = item.get("command")
        result = item.get("result")
        summary = item.get("summary")
        if not all(
            isinstance(part, str) and part.strip()
            for part in (record_type, command, result, summary)
        ):
            continue
        rendered.append(
            f"- [{record_type.strip()}] `{command.strip()}` -> {result.strip()}: {summary.strip()}"
        )
    if not rendered:
        return
    lines.append("## Validation")
    lines.append("")
    lines.extend(rendered)
    lines.append("")


def add_string_list_section(lines: list[str], heading: str, value: Any, code: bool = False) -> None:
    if not isinstance(value, list) or not value:
        return
    rendered: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            continue
        text = item.strip()
        rendered.append(f"- `{text}`" if code else f"- {text}")
    if not rendered:
        return
    lines.append(f"## {heading}")
    lines.append("")
    lines.extend(rendered)
    lines.append("")


def add_confidence_section(lines: list[str], value: Any) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return
    lines.append("## Confidence")
    lines.append("")
    lines.append(f"- {value:.2f}")
    lines.append("")


if __name__ == "__main__":
    raise SystemExit(main())
