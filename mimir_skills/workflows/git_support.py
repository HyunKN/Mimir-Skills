from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any


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

