from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .git_support import (
    collect_branch_range,
    collect_recent_commit_details,
    detect_base_ref,
    run_git,
    split_nonempty,
)
from .render_support import (
    as_dict,
    as_list,
    clean_bullets,
    emit_json_output,
    emit_text_output,
    load_context,
    section,
    string_value,
    summarize_files,
)


def build_collect_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect local git and diff context for the write-pr-rationale workflow."
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Repository path. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--commit-limit",
        type=int,
        default=5,
        help="How many recent commits to include. Defaults to 5.",
    )
    parser.add_argument(
        "--output",
        help="Optional JSON output path. Defaults to stdout when omitted.",
    )
    return parser


def build_generate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a reviewer-facing PR rationale draft from local repository context."
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
        help="Optional Markdown output path. Defaults to stdout when omitted.",
    )
    parser.add_argument(
        "--title",
        help="Optional PR title or heading. Defaults to the repository name.",
    )
    parser.add_argument(
        "--commit-limit",
        type=int,
        default=5,
        help="How many recent commits to include when collecting context live.",
    )
    parser.add_argument(
        "--why",
        action="append",
        default=[],
        help="Reason for the change. Repeat as needed.",
    )
    parser.add_argument(
        "--validation",
        action="append",
        default=[],
        help="Validation note to include. Repeat as needed.",
    )
    parser.add_argument(
        "--reviewer-note",
        action="append",
        default=[],
        help="Reviewer note or watch item. Repeat as needed.",
    )
    parser.add_argument(
        "--risk",
        action="append",
        default=[],
        help="Known risk or follow-up. Repeat as needed.",
    )
    parser.add_argument(
        "--evidence",
        action="append",
        default=[],
        help="Evidence note to include. Repeat as needed.",
    )
    return parser


def collect_main(argv: list[str] | None = None) -> int:
    args = build_collect_parser().parse_args(argv)
    try:
        context = collect_context(Path(args.repo), max(1, args.commit_limit))
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return emit_json_output(context, args.output, "PR context")


def generate_main(argv: list[str] | None = None) -> int:
    args = build_generate_parser().parse_args(argv)
    repo_path = Path(args.repo).resolve()
    try:
        context = load_context(
            args.context_json,
            repo_path,
            max(1, args.commit_limit),
            collect_context,
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    markdown = render_pr_rationale(
        context,
        title=args.title,
        why_items=args.why,
        validations=args.validation,
        reviewer_notes=args.reviewer_note,
        risks=args.risk,
        evidence=args.evidence,
    )
    return emit_text_output(markdown, args.output, "PR rationale draft")


def collect_context(repo_path: Path, commit_limit: int = 5) -> dict[str, Any]:
    repo_root = Path(run_git(repo_path, "rev-parse", "--show-toplevel")).resolve()
    branch = run_git(repo_root, "branch", "--show-current")
    head_short = run_git(repo_root, "rev-parse", "--short", "HEAD")
    head_full = run_git(repo_root, "rev-parse", "HEAD")
    base_ref = detect_base_ref(repo_root)
    changed_files = split_nonempty(run_git(repo_root, "diff", "--name-only"))
    staged_files = split_nonempty(run_git(repo_root, "diff", "--cached", "--name-only"))
    untracked_files = split_nonempty(
        run_git(repo_root, "ls-files", "--others", "--exclude-standard")
    )
    recent_commits = split_nonempty(run_git(repo_root, "log", f"-n{commit_limit}", "--oneline"))
    recent_commit_details = collect_recent_commit_details(repo_root, commit_limit)
    name_status = split_nonempty(run_git(repo_root, "diff", "--name-status"))
    name_status.extend([f"??\t{path}" for path in untracked_files])
    branch_range = collect_branch_range(repo_root, base_ref)

    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo_root),
        "repo_name": repo_root.name,
        "branch": branch or "(detached HEAD)",
        "head_short": head_short,
        "head_full": head_full,
        "base_ref": base_ref.get("label", "(no base ref detected)"),
        "working_tree_clean": not changed_files and not staged_files and not untracked_files,
        "diff": {
            "changed_files": sorted(set(changed_files + staged_files + untracked_files)),
            "staged_files": staged_files,
            "unstaged_files": changed_files,
            "untracked_files": untracked_files,
            "diff_stat": split_nonempty(run_git(repo_root, "diff", "--stat")),
            "staged_diff_stat": split_nonempty(run_git(repo_root, "diff", "--cached", "--stat")),
            "name_status": name_status,
        },
        "recent_commits": recent_commits,
        "recent_commit_details": recent_commit_details,
        "branch_range": branch_range,
    }


def render_pr_rationale(
    context: dict[str, Any],
    *,
    title: str | None,
    why_items: list[str],
    validations: list[str],
    reviewer_notes: list[str],
    risks: list[str],
    evidence: list[str],
) -> str:
    repo_name = string_value(context.get("repo_name")) or "repository"
    heading = title.strip() if isinstance(title, str) and title.strip() else repo_name
    branch = string_value(context.get("branch")) or "(unknown branch)"
    base_ref = string_value(context.get("base_ref")) or "(no base ref detected)"
    head_short = string_value(context.get("head_short")) or "(unknown HEAD)"
    generated_at = string_value(context.get("generated_at")) or "(unknown time)"
    diff = as_dict(context.get("diff"))
    branch_range = as_dict(context.get("branch_range"))

    lines: list[str] = []
    lines.append(f"# PR Rationale: {heading}")
    lines.append("")
    lines.append(
        f"> Generated from local repository context for branch `{branch}` at `{generated_at}`."
    )
    lines.append("")

    lines.extend(
        section(
            "PR Snapshot",
            [
                f"- Repository: `{repo_name}`",
                f"- Branch: `{branch}`",
                f"- Base reference: `{base_ref}`",
                f"- HEAD: `{head_short}`",
            ],
        )
    )

    lines.extend(render_change_section(context, diff, branch_range))
    lines.extend(
        section(
            "Evidence",
            clean_bullets(evidence) or default_evidence_lines(diff, branch_range, context),
        )
    )
    lines.extend(
        section(
            "Why This Changed",
            clean_bullets(why_items)
            or ["- Add the main reason for this change before sharing the PR rationale externally."],
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
    lines.extend(
        section(
            "Reviewer Notes",
            clean_bullets(reviewer_notes) or default_reviewer_notes(diff, branch_range),
        )
    )
    lines.extend(
        section(
            "Risks and Follow-Up",
            clean_bullets(risks) or default_risk_lines(diff, branch_range),
        )
    )

    return "\n".join(lines).rstrip() + "\n"


def render_change_section(
    context: dict[str, Any],
    diff: dict[str, Any],
    branch_range: dict[str, Any],
) -> list[str]:
    changed_files = as_list(diff.get("changed_files"))
    name_status = as_list(diff.get("name_status"))
    untracked_files = as_list(diff.get("untracked_files"))
    lines: list[str] = ["## What Changed", ""]

    if changed_files:
        lines.append(f"- Working-tree file changes detected: `{len(changed_files)}`")

        if name_status:
            for item in name_status[:12]:
                if isinstance(item, str) and item.strip():
                    lines.append(f"- `{item.strip()}`")
            if len(name_status) > 12:
                lines.append(f"- ... and `{len(name_status) - 12}` more diff entries")
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

        diff_stat = as_list(diff.get("diff_stat"))
        staged_diff_stat = as_list(diff.get("staged_diff_stat"))
        if diff_stat or staged_diff_stat:
            lines.append("")
            lines.append("### Diff Summary")
            lines.append("")
            if staged_diff_stat:
                lines.append("- Staged diff stat:")
                for item in staged_diff_stat:
                    if isinstance(item, str) and item.strip():
                        lines.append(f"  - `{item.strip()}`")
            if diff_stat:
                lines.append("- Working tree diff stat:")
                for item in diff_stat:
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
        lines.append("- No working-tree changes were detected, so this draft is using committed branch-range context.")
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

    lines.append("- No working-tree changes were detected.")
    lines.append(
        "- No branch-range diff was detected against the current base reference, so this draft is using recent committed work as fallback context."
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
    diff: dict[str, Any],
    branch_range: dict[str, Any],
    context: dict[str, Any],
) -> list[str]:
    if as_list(diff.get("changed_files")):
        return [
            "- The current working-tree diff is the primary local evidence for this draft.",
        ]
    if as_list(branch_range.get("changed_files")):
        return [
            "- The working tree is clean, so this draft is using committed branch-range diff context as its main evidence.",
        ]
    if as_list(context.get("recent_commit_details")):
        return [
            "- The working tree and branch-range diff are both clean, so this draft is falling back to recent committed work as evidence.",
        ]
    return ["- No extra branch evidence was provided for this draft."]


def default_reviewer_notes(diff: dict[str, Any], branch_range: dict[str, Any]) -> list[str]:
    changed_files = as_list(diff.get("changed_files"))
    if changed_files:
        return [
            "- Review the changed files list and replace this generic note with the highest-risk areas for reviewers to inspect.",
        ]
    if as_list(branch_range.get("changed_files")):
        return [
            "- The working tree is clean, so reviewers should focus on the committed branch-range changes above instead of expecting uncommitted diffs.",
        ]
    return [
        "- Add reviewer watch points once the branch has a clearer diff against its intended base or more explicit rationale inputs.",
    ]


def default_risk_lines(diff: dict[str, Any], branch_range: dict[str, Any]) -> list[str]:
    changed_files = as_list(diff.get("changed_files"))
    if changed_files or as_list(branch_range.get("changed_files")):
        return [
            "- This draft still needs explicit risk and follow-up notes tied to the actual change before external sharing.",
        ]
    return [
        "- No working-tree or branch-range diff was detected; confirm whether the intended change already lives in recent commits or a different branch.",
    ]
