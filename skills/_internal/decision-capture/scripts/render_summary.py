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
    lines.append(f"> Derived from canonical decision record [[{record_id}]].")
    lines.append("")

    add_text_section(lines, "Decision", record.get("decision"))
    add_text_section(lines, "Context", record.get("problem_context"))
    add_selected_option_section(lines, record.get("selected_option"))
    add_text_section(lines, "Why", record.get("rationale"))
    add_alternatives_section(lines, record.get("alternatives_considered"))
    add_evidence_section(lines, record.get("evidence_refs"))
    add_ai_assistance_section(lines, record.get("ai_assistance"))
    add_approval_section(lines, record.get("approval"))
    add_change_scope_section(lines, record.get("change_scope"))
    add_related_artifacts_section(lines, record_id, record.get("supersedes"))
    add_string_list_section(lines, "Affected Paths", record.get("affected_paths"), code=True)
    add_validation_section(lines, record.get("validation_run"))
    add_string_list_section(lines, "Remaining Risks", record.get("remaining_risks"))
    add_string_list_section(lines, "Follow-Up", record.get("follow_up"))
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
        if not isinstance(name, str) or not name.strip():
            continue
        if not isinstance(status, str) or not status.strip():
            continue
        if not isinstance(reason, str) or not reason.strip():
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
        if not isinstance(kind, str) or not kind.strip():
            continue
        if not isinstance(ref, str) or not ref.strip():
            continue
        if not isinstance(summary, str) or not summary.strip():
            continue
        if not isinstance(captured_at, str) or not captured_at.strip():
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
        if not isinstance(record_type, str) or not record_type.strip():
            continue
        if not isinstance(command, str) or not command.strip():
            continue
        if not isinstance(result, str) or not result.strip():
            continue
        if not isinstance(summary, str) or not summary.strip():
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


def add_ai_assistance_section(lines: list[str], value: Any) -> None:
    if not isinstance(value, dict):
        return
    rendered: list[str] = []

    used = value.get("used")
    if isinstance(used, bool):
        rendered.append(f"- Used: {'yes' if used else 'no'}")

    summary = value.get("summary")
    if isinstance(summary, str) and summary.strip():
        rendered.append(f"- Summary: {summary.strip()}")

    tools = value.get("tools")
    if isinstance(tools, list):
        tool_values = [item.strip() for item in tools if isinstance(item, str) and item.strip()]
        if tool_values:
            rendered.append(f"- Tools: {', '.join(tool_values)}")

    verification = value.get("human_verification")
    if isinstance(verification, str) and verification.strip():
        rendered.append(f"- Human verification: {verification.strip()}")

    if not rendered:
        return

    lines.append("## AI Assistance")
    lines.append("")
    lines.extend(rendered)
    lines.append("")


def add_approval_section(lines: list[str], value: Any) -> None:
    if not isinstance(value, dict):
        return
    rendered: list[str] = []

    required = value.get("required")
    if isinstance(required, bool):
        rendered.append(f"- Required: {'yes' if required else 'no'}")

    status = value.get("status")
    if isinstance(status, str) and status.strip():
        rendered.append(f"- Status: {status.strip()}")

    approver = value.get("approver")
    if isinstance(approver, str) and approver.strip():
        rendered.append(f"- Approver: {approver.strip()}")

    scope = value.get("scope")
    if isinstance(scope, str) and scope.strip():
        rendered.append(f"- Scope: {scope.strip()}")

    timestamp = value.get("timestamp")
    if isinstance(timestamp, str) and timestamp.strip():
        rendered.append(f"- Timestamp: {timestamp.strip()}")

    if not rendered:
        return

    lines.append("## Approval")
    lines.append("")
    lines.extend(rendered)
    lines.append("")


def add_change_scope_section(lines: list[str], value: Any) -> None:
    if not isinstance(value, dict):
        return
    rendered: list[str] = []

    risk_tier = value.get("risk_tier")
    if isinstance(risk_tier, str) and risk_tier.strip():
        rendered.append(f"- Risk tier: {risk_tier.strip()}")

    blast_radius = value.get("blast_radius")
    if isinstance(blast_radius, str) and blast_radius.strip():
        rendered.append(f"- Blast radius: {blast_radius.strip()}")

    deployment_stage = value.get("deployment_stage")
    if isinstance(deployment_stage, str) and deployment_stage.strip():
        rendered.append(f"- Deployment stage: {deployment_stage.strip()}")

    rollback_plan = value.get("rollback_plan")
    if isinstance(rollback_plan, str) and rollback_plan.strip():
        rendered.append(f"- Rollback plan: {rollback_plan.strip()}")

    post_deploy_status = value.get("post_deploy_status")
    if isinstance(post_deploy_status, str) and post_deploy_status.strip():
        rendered.append(f"- Post-deploy status: {post_deploy_status.strip()}")

    post_deploy_summary = value.get("post_deploy_summary")
    if isinstance(post_deploy_summary, str) and post_deploy_summary.strip():
        rendered.append(f"- Post-deploy summary: {post_deploy_summary.strip()}")

    if not rendered:
        return

    lines.append("## Change Governance")
    lines.append("")
    lines.extend(rendered)
    lines.append("")


def add_related_artifacts_section(lines: list[str], record_id: str, supersedes: Any) -> None:
    rendered = [f"- Canonical decision note: [[{record_id}]]"]

    if isinstance(supersedes, list):
        superseded_ids = [item.strip() for item in supersedes if isinstance(item, str) and item.strip()]
        if superseded_ids:
            rendered.append(
                "- Supersedes: " + ", ".join(f"[[{item}]]" for item in superseded_ids)
            )

    if not rendered:
        return

    lines.append("## Related Artifacts")
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
