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
from .render_support import emit_json_output, emit_text_output


def build_collect_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect local git context for the prepare-handoff workflow."
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
        description="Deprecated helper stub for the skill-first prepare-handoff workflow."
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Repository path. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--context-json",
        help="Optional pre-collected context JSON path to carry into the skill-first workflow.",
    )
    parser.add_argument(
        "--output",
        help="Optional output path for the deprecation note. Defaults to stdout when omitted.",
    )
    parser.add_argument(
        "--title",
        help="Legacy title input. The deprecated helper no longer renders a handoff draft.",
    )
    parser.add_argument(
        "--commit-limit",
        type=int,
        default=5,
        help="Legacy collection hint retained for compatibility with older invocations.",
    )
    parser.add_argument(
        "--validation",
        action="append",
        default=[],
        help="Legacy validation input retained for compatibility.",
    )
    parser.add_argument(
        "--blocker",
        action="append",
        default=[],
        help="Legacy blocker input retained for compatibility.",
    )
    parser.add_argument(
        "--risk",
        action="append",
        default=[],
        help="Legacy risk input retained for compatibility.",
    )
    parser.add_argument(
        "--next-step",
        action="append",
        default=[],
        help="Legacy next-step input retained for compatibility.",
    )
    parser.add_argument(
        "--evidence",
        action="append",
        default=[],
        help="Legacy evidence input retained for compatibility.",
    )
    return parser


def collect_main(argv: list[str] | None = None) -> int:
    args = build_collect_parser().parse_args(argv)
    try:
        context = collect_context(Path(args.repo), max(1, args.commit_limit))
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return emit_json_output(context, args.output, "git context")


def generate_main(argv: list[str] | None = None) -> int:
    args = build_generate_parser().parse_args(argv)
    payload = build_deprecation_note(
        repo_path=Path(args.repo).resolve(),
        context_json=args.context_json,
        explicit_inputs_present=any(
            [args.validation, args.blocker, args.risk, args.next_step, args.evidence]
        ),
    )
    return emit_text_output(payload, args.output, "prepare-handoff deprecation note")


def collect_context(repo_path: Path, commit_limit: int = 5) -> dict[str, Any]:
    repo_root = Path(run_git(repo_path, "rev-parse", "--show-toplevel")).resolve()
    branch = run_git(repo_root, "branch", "--show-current")
    head_short = run_git(repo_root, "rev-parse", "--short", "HEAD")
    head_full = run_git(repo_root, "rev-parse", "HEAD")
    base_ref = detect_base_ref(repo_root)
    porcelain_lines = split_nonempty(run_git(repo_root, "status", "--short"))
    staged_files = split_nonempty(run_git(repo_root, "diff", "--cached", "--name-only"))
    unstaged_files = split_nonempty(run_git(repo_root, "diff", "--name-only"))
    untracked_files = split_nonempty(
        run_git(repo_root, "ls-files", "--others", "--exclude-standard")
    )
    recent_commits = split_nonempty(run_git(repo_root, "log", f"-n{commit_limit}", "--oneline"))
    recent_commit_details = collect_recent_commit_details(repo_root, commit_limit)
    branch_range = collect_branch_range(repo_root, base_ref)

    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo_root),
        "repo_name": repo_root.name,
        "branch": branch or "(detached HEAD)",
        "head_short": head_short,
        "head_full": head_full,
        "base_ref": base_ref.get("label", "(no base ref detected)"),
        "is_worktree_clean": not porcelain_lines,
        "status": {
            "staged_count": len(staged_files),
            "unstaged_count": len(unstaged_files),
            "untracked_count": len(untracked_files),
            "porcelain": porcelain_lines,
            "entries": parse_porcelain(porcelain_lines),
        },
        "diff": {
            "staged_stat": split_nonempty(run_git(repo_root, "diff", "--cached", "--stat")),
            "unstaged_stat": split_nonempty(run_git(repo_root, "diff", "--stat")),
            "staged_files": staged_files,
            "unstaged_files": unstaged_files,
            "untracked_files": untracked_files,
            "all_changed_files": sorted(set(staged_files + unstaged_files + untracked_files)),
        },
        "recent_commits": recent_commits,
        "recent_commit_details": recent_commit_details,
        "branch_range": branch_range,
    }


def parse_porcelain(lines: list[str]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for line in lines:
        if len(line) < 4:
            continue
        staged_code = line[0]
        unstaged_code = line[1]
        path = line[3:]
        entries.append(
            {
                "path": path,
                "raw": line,
                "staged_code": staged_code,
                "unstaged_code": unstaged_code,
                "staged_labels": status_labels(staged_code),
                "unstaged_labels": status_labels(unstaged_code),
            }
        )
    return entries


def status_labels(code: str) -> list[str]:
    mapping = {
        "M": "modified",
        "A": "added",
        "D": "deleted",
        "R": "renamed",
        "C": "copied",
        "U": "unmerged",
        "?": "untracked",
    }
    if code == " ":
        return []
    label = mapping.get(code)
    return [label] if label else [f"status:{code}"]


def build_deprecation_note(
    *,
    repo_path: Path,
    context_json: str | None,
    explicit_inputs_present: bool,
) -> str:
    lines = [
        "# prepare-handoff helper deprecated",
        "",
        "- Runtime-generated handoff drafts are deprecated for this workflow.",
        "- Draft the handoff directly from `skills/prepare-handoff/SKILL.md` and `skills/handoff-context/references/handoff-playbook.md`.",
        f"- Repository under review: `{repo_path}`",
        "- Use `python skills/prepare-handoff/scripts/collect_git_context.py --repo <path> --output handoff-context.json` when you want structured git context before drafting.",
        "- The old shared CLI path (`python -m mimir_skills prepare-handoff`) and `scripts/generate_handoff.py` now exist only to point older flows back to the skill-first guidance.",
    ]

    if context_json:
        lines.append(
            f"- Carry the existing context file `{context_json}` into the skill-first workflow as supporting evidence if it is still relevant."
        )
    if explicit_inputs_present:
        lines.append(
            "- Preserve any explicit validation, blocker, risk, next-step, or evidence input you already have; those inputs should override local fallback bullets when following the skill."
        )

    return "\n".join(lines).rstrip() + "\n"
