#!/usr/bin/env python3
"""Generate a Markdown handoff draft from local git context."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from collect_git_context import collect_context


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown handoff draft from local repository context."
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Repository path. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--context-json",
        help="Optional path to a pre-collected context JSON file.",
    )
    parser.add_argument(
        "--output",
        help="Output Markdown path. Defaults to <repo>/handoff.md.",
    )
    parser.add_argument(
        "--title",
        help="Optional handoff title. Defaults to the repository name.",
    )
    parser.add_argument(
        "--commit-limit",
        type=int,
        default=5,
        help="How many recent commits to include when collecting context live.",
    )
    parser.add_argument(
        "--validation",
        action="append",
        default=[],
        help="Validation note to include. Repeat as needed.",
    )
    parser.add_argument(
        "--blocker",
        action="append",
        default=[],
        help="Known blocker to include. Repeat as needed.",
    )
    parser.add_argument(
        "--risk",
        action="append",
        default=[],
        help="Known risk to include. Repeat as needed.",
    )
    parser.add_argument(
        "--next-step",
        action="append",
        default=[],
        help="Next-step note to include. Repeat as needed.",
    )
    parser.add_argument(
        "--evidence",
        action="append",
        default=[],
        help="Evidence note to include. Repeat as needed.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_path = Path(args.repo).resolve()

    try:
        context = load_context(args.context_json, repo_path, max(1, args.commit_limit))
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    context_repo_root = Path(string_value(context.get("repo_root")) or str(repo_path))
    output_path = Path(args.output) if args.output else context_repo_root / "handoff.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    markdown = render_handoff(
        context,
        title=args.title,
        validations=args.validation,
        blockers=args.blocker,
        risks=args.risk,
        next_steps=args.next_step,
        evidence=args.evidence,
    )
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Wrote handoff draft: {output_path}")
    return 0


def load_context(context_json: str | None, repo_path: Path, commit_limit: int) -> dict[str, Any]:
    if context_json:
        context_path = Path(context_json)
        try:
            data = json.loads(context_path.read_text(encoding="utf-8-sig"))
        except FileNotFoundError as exc:
            raise RuntimeError(f"Context JSON not found: {context_path}") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Invalid JSON in {context_path}: {exc.msg} at line {exc.lineno}, column {exc.colno}"
            ) from exc
        if not isinstance(data, dict):
            raise RuntimeError("Context JSON must be a top-level object.")
        return data
    return collect_context(repo_path, commit_limit=commit_limit)


def render_handoff(
    context: dict[str, Any],
    *,
    title: str | None,
    validations: list[str],
    blockers: list[str],
    risks: list[str],
    next_steps: list[str],
    evidence: list[str],
) -> str:
    repo_name = string_value(context.get("repo_name")) or "repository"
    heading = title.strip() if isinstance(title, str) and title.strip() else repo_name
    branch = string_value(context.get("branch")) or "(unknown branch)"
    head_short = string_value(context.get("head_short")) or "(unknown HEAD)"
    generated_at = string_value(context.get("generated_at")) or "(unknown time)"
    base_ref = string_value(context.get("base_ref")) or "(no base ref detected)"

    status = as_dict(context.get("status"))
    diff = as_dict(context.get("diff"))
    branch_range = as_dict(context.get("branch_range"))

    lines: list[str] = []
    lines.append(f"# Handoff: {heading}")
    lines.append("")
    lines.append(
        f"> Generated from local repository context for branch `{branch}` at `{generated_at}`."
    )
    lines.append("")

    lines.extend(
        section(
            "Current Snapshot",
            [
                f"- Repository: `{repo_name}`",
                f"- Branch: `{branch}`",
                f"- HEAD: `{head_short}`",
                f"- Branch context base: `{base_ref}`",
                render_worktree_state(status),
            ],
        )
    )

    lines.extend(render_work_section(context, status, diff, branch_range))
    lines.extend(
        section(
            "Relevant Evidence",
            clean_bullets(evidence) or default_evidence_lines(context, status, branch_range),
        )
    )
    lines.extend(render_commit_section(context))
    lines.extend(
        section(
            "Validation",
            clean_bullets(validations)
            or ["- No explicit validation notes were provided for this draft."],
        )
    )

    blocker_and_risks = clean_bullets(blockers) + default_risk_lines(status) + clean_bullets(risks)
    lines.extend(
        section(
            "Blockers and Risks",
            blocker_and_risks or ["- No blockers or additional risks were recorded."],
        )
    )

    lines.extend(
        section(
            "Next Steps",
            clean_bullets(next_steps) or default_next_steps(status, diff),
        )
    )

    return "\n".join(lines).rstrip() + "\n"


def render_worktree_state(status: dict[str, Any]) -> str:
    if status.get("porcelain"):
        staged = int_value(status.get("staged_count"))
        unstaged = int_value(status.get("unstaged_count"))
        untracked = int_value(status.get("untracked_count"))
        return (
            f"- Working tree: not clean (`{staged}` staged, `{unstaged}` unstaged, `{untracked}` untracked)"
        )
    return "- Working tree: clean"


def render_work_section(
    context: dict[str, Any],
    status: dict[str, Any],
    diff: dict[str, Any],
    branch_range: dict[str, Any],
) -> list[str]:
    entries = status.get("entries")
    changed_files = as_list(diff.get("all_changed_files"))
    untracked_files = as_list(diff.get("untracked_files"))
    lines: list[str] = ["## What Changed", ""]

    if changed_files:
        lines.append(f"- Working-tree file changes detected: `{len(changed_files)}`")

        if isinstance(entries, list) and entries:
            for entry in entries[:12]:
                if not isinstance(entry, dict):
                    continue
                path = string_value(entry.get("path"))
                raw = string_value(entry.get("raw"))
                if path and raw:
                    lines.append(f"- `{raw}`")
            if len(entries) > 12:
                lines.append(f"- ... and `{len(entries) - 12}` more status entries")
        else:
            for path in changed_files[:12]:
                if isinstance(path, str) and path.strip():
                    lines.append(f"- `{path.strip()}`")
            if len(changed_files) > 12:
                lines.append(f"- ... and `{len(changed_files) - 12}` more changed files")

        exact_untracked = [
            path.strip() for path in untracked_files if isinstance(path, str) and path.strip()
        ]
        if exact_untracked:
            lines.append("")
            lines.append("### Untracked Files")
            lines.append("")
            for path in exact_untracked[:12]:
                lines.append(f"- `{path}`")
            if len(exact_untracked) > 12:
                lines.append(f"- ... and `{len(exact_untracked) - 12}` more untracked files")

        staged_stat = as_list(diff.get("staged_stat"))
        unstaged_stat = as_list(diff.get("unstaged_stat"))
        if staged_stat or unstaged_stat:
            lines.append("")
            lines.append("### Diff Summary")
            lines.append("")
            if staged_stat:
                lines.append("- Staged diff stat:")
                for item in staged_stat:
                    if isinstance(item, str) and item.strip():
                        lines.append(f"  - `{item.strip()}`")
            if unstaged_stat:
                lines.append("- Unstaged diff stat:")
                for item in unstaged_stat:
                    if isinstance(item, str) and item.strip():
                        lines.append(f"  - `{item.strip()}`")
    else:
        lines.extend(render_clean_state_fallback(context, branch_range))

    lines.append("")
    return lines


def render_clean_state_fallback(
    context: dict[str, Any],
    branch_range: dict[str, Any],
) -> list[str]:
    lines: list[str] = []
    branch_files = as_list(branch_range.get("changed_files"))
    branch_name_status = as_list(branch_range.get("name_status"))
    branch_diff_stat = as_list(branch_range.get("diff_stat"))
    base_ref = string_value(branch_range.get("base_ref")) or "(no base ref detected)"

    if branch_files:
        lines.append("- No working-tree changes were detected, so this draft is using committed branch context.")
        lines.append(f"- Committed branch-range files since `{base_ref}`: `{len(branch_files)}`")
        source_items = branch_name_status or branch_files
        for item in source_items[:12]:
            if isinstance(item, str) and item.strip():
                lines.append(f"- `{item.strip()}`")
        if len(source_items) > 12:
            lines.append(f"- ... and `{len(source_items) - 12}` more committed branch entries")
        if branch_diff_stat:
            lines.append("")
            lines.append("### Committed Branch Diff Summary")
            lines.append("")
            for item in branch_diff_stat:
                if isinstance(item, str) and item.strip():
                    lines.append(f"- `{item.strip()}`")
        return lines

    lines.append("- No file changes were detected in the current working tree.")
    lines.append(
        "- No committed branch-range diff was detected either, so this draft is falling back to recent committed work."
    )
    lines.append("")
    lines.append("### Recent Committed Work")
    lines.append("")
    lines.extend(render_recent_commit_details(context))
    return lines


def render_commit_section(context: dict[str, Any]) -> list[str]:
    commits = as_list(context.get("recent_commits"))
    return section(
        "Recent Commits",
        [f"- `{commit}`" for commit in commits if isinstance(commit, str) and commit.strip()]
        or ["- No recent commit history was available."],
    )


def render_recent_commit_details(context: dict[str, Any]) -> list[str]:
    details = as_list(context.get("recent_commit_details"))
    if not details:
        return ["- No recent committed work was available."]

    lines: list[str] = []
    for entry in details[:5]:
        if not isinstance(entry, dict):
            continue
        short_hash = string_value(entry.get("short_hash")) or "(unknown)"
        subject = string_value(entry.get("subject")) or "(no subject)"
        files = [
            path.strip()
            for path in as_list(entry.get("files"))
            if isinstance(path, str) and path.strip()
        ]
        file_summary = summarize_files(files)
        if file_summary:
            lines.append(f"- `{short_hash}` {subject} — touched {file_summary}")
        else:
            lines.append(f"- `{short_hash}` {subject}")
    return lines or ["- No recent committed work was available."]


def default_evidence_lines(
    context: dict[str, Any],
    status: dict[str, Any],
    branch_range: dict[str, Any],
) -> list[str]:
    if status.get("porcelain"):
        return [
            "- Use the current working-tree status and diff summary above as the primary local evidence for this draft.",
        ]
    if as_list(branch_range.get("changed_files")):
        return [
            "- The working tree is clean, so this draft is using committed branch-range context as the primary local evidence.",
        ]
    if as_list(context.get("recent_commit_details")):
        return [
            "- The working tree and branch-range diff are both clean, so this draft is using recent committed work as fallback evidence.",
        ]
    return ["- No extra local evidence was provided for this draft."]


def default_risk_lines(status: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    if status.get("porcelain"):
        lines.append(
            "- The branch still contains uncommitted changes, so the next owner should verify the final intended state before sharing externally."
        )
    if (
        not int_value(status.get("staged_count"))
        and not int_value(status.get("unstaged_count"))
        and not int_value(status.get("untracked_count"))
    ):
        lines.append(
            "- No working-tree changes were detected; verify that any missing context already lives in commits or decision records."
        )
    return lines


def default_next_steps(status: dict[str, Any], diff: dict[str, Any]) -> list[str]:
    steps: list[str] = []
    if status.get("porcelain"):
        steps.append(
            "- Review the listed changed files and confirm which updates should be committed before handoff."
        )
    else:
        steps.append(
            "- Confirm whether the next owner needs only a clean-state checkpoint or a richer summary of the most recent committed work."
        )
    if as_list(diff.get("all_changed_files")):
        steps.append(
            "- Re-run any relevant validation and replace the placeholder validation section with concrete results before external sharing."
        )
    steps.append(
        "- Add task-specific blockers, risks, and owner notes if this draft is going to another person or agent."
    )
    return steps


def section(title: str, bullets: list[str]) -> list[str]:
    lines = [f"## {title}", ""]
    lines.extend(bullets)
    lines.append("")
    return lines


def clean_bullets(values: list[str]) -> list[str]:
    cleaned: list[str] = []
    for value in values:
        text = value.strip()
        if not text:
            continue
        cleaned.append(text if text.startswith("- ") else f"- {text}")
    return cleaned


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_value(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def int_value(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def summarize_files(files: list[str]) -> str:
    if not files:
        return ""
    preview = [f"`{path}`" for path in files[:3]]
    if len(files) > 3:
        preview.append(f"and `{len(files) - 3}` more files")
    return ", ".join(preview)


if __name__ == "__main__":
    raise SystemExit(main())
