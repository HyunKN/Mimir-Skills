#!/usr/bin/env python3
"""Collect a small, PR-oriented snapshot from a local git repository."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        context = collect_context(Path(args.repo), max(1, args.commit_limit))
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    payload = json.dumps(context, indent=2) + "\n"
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload, encoding="utf-8")
        print(f"Wrote PR context: {output_path}")
    else:
        sys.stdout.write(payload)

    return 0


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


def detect_base_ref(repo_root: Path) -> dict[str, str]:
    for candidate in ("origin/main", "origin/master", "main", "master"):
        result = run_git_optional(repo_root, "merge-base", "HEAD", candidate)
        if result:
            return {
                "candidate": candidate,
                "merge_base": result,
                "label": f"{candidate}@{short_sha(result)}",
            }
    return {}


def collect_branch_range(repo_root: Path, base_ref: dict[str, str]) -> dict[str, Any]:
    merge_base = base_ref.get("merge_base", "")
    label = base_ref.get("label", "(no base ref detected)")
    if not merge_base:
        return {
            "base_ref": label,
            "commit_count": 0,
            "commits": [],
            "changed_files": [],
            "name_status": [],
            "diff_stat": [],
        }

    commits = split_nonempty(run_git(repo_root, "log", f"{merge_base}..HEAD", "--oneline"))
    changed_files = split_nonempty(run_git(repo_root, "diff", "--name-only", f"{merge_base}..HEAD"))
    return {
        "base_ref": label,
        "commit_count": len(commits),
        "commits": commits,
        "changed_files": changed_files,
        "name_status": split_nonempty(run_git(repo_root, "diff", "--name-status", f"{merge_base}..HEAD")),
        "diff_stat": split_nonempty(run_git(repo_root, "diff", "--stat", f"{merge_base}..HEAD")),
    }


def collect_recent_commit_details(repo_root: Path, commit_limit: int) -> list[dict[str, Any]]:
    raw_commits = split_nonempty(
        run_git(repo_root, "log", f"-n{commit_limit}", "--format=%H%x1f%h%x1f%s")
    )
    details: list[dict[str, Any]] = []
    for row in raw_commits:
        parts = row.split("\x1f", 2)
        if len(parts) != 3:
            continue
        full_hash, short_hash, subject = parts
        files = split_nonempty(
            run_git(repo_root, "show", "--format=", "--name-only", "--diff-filter=ACDMRT", full_hash)
        )
        details.append(
            {
                "full_hash": full_hash,
                "short_hash": short_hash,
                "subject": subject,
                "files": files,
            }
        )
    return details


def run_git(repo_path: Path, *args: str) -> str:
    command = ["git", "-C", str(repo_path), *args]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        raise RuntimeError(f"Git command failed ({' '.join(args)}): {stderr}")
    return result.stdout.rstrip("\r\n")


def run_git_optional(repo_path: Path, *args: str) -> str:
    command = ["git", "-C", str(repo_path), *args]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.rstrip("\r\n")


def split_nonempty(value: str) -> list[str]:
    return [line for line in value.splitlines() if line.strip()]


def short_sha(value: str) -> str:
    return value[:7] if value else value


if __name__ == "__main__":
    raise SystemExit(main())
