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
        description="Deprecated helper stub for the skill-first write-pr-rationale workflow."
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
        help="Legacy title input. The deprecated helper no longer renders a rationale draft.",
    )
    parser.add_argument(
        "--commit-limit",
        type=int,
        default=5,
        help="Legacy collection hint retained for compatibility with older invocations.",
    )
    parser.add_argument(
        "--why",
        action="append",
        default=[],
        help="Legacy explicit rationale input retained for compatibility.",
    )
    parser.add_argument(
        "--validation",
        action="append",
        default=[],
        help="Legacy validation input retained for compatibility.",
    )
    parser.add_argument(
        "--reviewer-note",
        action="append",
        default=[],
        help="Legacy reviewer-note input retained for compatibility.",
    )
    parser.add_argument(
        "--risk",
        action="append",
        default=[],
        help="Legacy risk input retained for compatibility.",
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
    return emit_json_output(context, args.output, "PR context")


def generate_main(argv: list[str] | None = None) -> int:
    args = build_generate_parser().parse_args(argv)
    payload = build_deprecation_note(
        repo_path=Path(args.repo).resolve(),
        context_json=args.context_json,
        explicit_inputs_present=any(
            [args.why, args.validation, args.reviewer_note, args.risk, args.evidence]
        ),
    )
    return emit_text_output(payload, args.output, "write-pr-rationale deprecation note")


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


def build_deprecation_note(
    *,
    repo_path: Path,
    context_json: str | None,
    explicit_inputs_present: bool,
) -> str:
    lines = [
        "# write-pr-rationale helper deprecated",
        "",
        "- Runtime-generated PR rationale drafts are deprecated for this workflow.",
        "- Draft the rationale directly from `skills/write-pr-rationale/SKILL.md` and `skills/_internal/pr-rationale/references/pr-playbook.md`.",
        f"- Repository under review: `{repo_path}`",
        "- Use `python skills/write-pr-rationale/scripts/collect_pr_context.py --repo <path> --output pr-context.json` when you want structured git context before drafting.",
        "- The old shared CLI path (`python -m mimir_skills write-pr-rationale`) and `scripts/generate_pr_rationale.py` now exist only to point older flows back to the skill-first guidance.",
    ]

    if context_json:
        lines.append(
            f"- Carry the existing context file `{context_json}` into the skill-first workflow as supporting evidence if it is still relevant."
        )
    if explicit_inputs_present:
        lines.append(
            "- Preserve any explicit why, validation, reviewer-note, risk, or evidence input you already have; those inputs should override local inference when following the skill."
        )

    return "\n".join(lines).rstrip() + "\n"
