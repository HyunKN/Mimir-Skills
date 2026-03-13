#!/usr/bin/env python3
"""Collect a small, handoff-oriented snapshot from a local git repository."""

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
        print(f"Wrote git context: {output_path}")
    else:
        sys.stdout.write(payload)

    return 0


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


def detect_base_ref(repo_root: Path) -> dict[str, str]:
    for candidate in ("origin/main", "origin/master", "main", "master"):
        merge_base = run_git_optional(repo_root, "merge-base", "HEAD", candidate)
        if merge_base:
            return {
                "candidate": candidate,
                "merge_base": merge_base,
                "label": f"{candidate}@{short_sha(merge_base)}",
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
            "diff_stat": [],
            "name_status": [],
            "changed_files": [],
        }

    commits = split_nonempty(run_git(repo_root, "log", f"{merge_base}..HEAD", "--oneline"))
    changed_files = split_nonempty(run_git(repo_root, "diff", "--name-only", f"{merge_base}..HEAD"))
    return {
        "base_ref": label,
        "commit_count": len(commits),
        "commits": commits,
        "diff_stat": split_nonempty(run_git(repo_root, "diff", "--stat", f"{merge_base}..HEAD")),
        "name_status": split_nonempty(
            run_git(repo_root, "diff", "--name-status", f"{merge_base}..HEAD")
        ),
        "changed_files": changed_files,
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


def parse_porcelain(lines: list[str]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for line in lines:
        if len(line) < 4:
            continue
        staged_code = line[0]
        unstaged_code = line[1]
        path = line[3:]
        entry = {
            "path": path,
            "raw": line,
            "staged_code": staged_code,
            "unstaged_code": unstaged_code,
            "staged_labels": status_labels(staged_code),
            "unstaged_labels": status_labels(unstaged_code),
        }
        entries.append(entry)

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


def short_sha(value: str) -> str:
    return value[:7] if value else value


if __name__ == "__main__":
    raise SystemExit(main())
