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
    explicit_why_items = clean_bullets(why_items)
    explicit_validations = clean_bullets(validations)
    explicit_reviewer_notes = clean_bullets(reviewer_notes)
    explicit_risks = clean_bullets(risks)

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
            explicit_why_items or default_why_lines(diff, branch_range, context),
        )
    )
    lines.extend(render_commit_section(context))
    lines.extend(
        section(
            "Validation",
            explicit_validations or default_validation_lines(diff, branch_range, context),
        )
    )
    lines.extend(
        section(
            "Reviewer Notes",
            explicit_reviewer_notes or default_reviewer_notes(diff, branch_range, context),
        )
    )
    lines.extend(
        section(
            "Risks and Follow-Up",
            explicit_risks
            or default_risk_lines(
                diff,
                branch_range,
                context,
                has_explicit_why=bool(explicit_why_items),
            ),
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
    branch_range = as_dict(context.get("branch_range"))
    branch_commits = as_list(branch_range.get("commits"))
    branch_base = string_value(branch_range.get("base_ref")) or "base"
    if branch_commits:
        return section(
            f"Commits Since {branch_base}",
            [
                f"- `{commit}`"
                for commit in branch_commits
                if isinstance(commit, str) and commit.strip()
            ]
            or ["- No branch-range commit history was available."],
        )

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
    source_label, _, subjects = analysis_inputs(diff, branch_range, context)
    if as_list(diff.get("changed_files")):
        lines = [
            "- The current working-tree diff is the primary local evidence for this draft.",
        ]
        preview = summarize_subjects(subjects)
        if preview:
            lines.append(f"- Supporting commit signals nearby include {preview}.")
        return lines
    if as_list(branch_range.get("changed_files")):
        lines = [
            "- The working tree is clean, so this draft is using committed branch-range diff context as its main evidence.",
        ]
        preview = summarize_subjects(subjects)
        if preview:
            lines.append(f"- Supporting branch-history signals include {preview}.")
        return lines
    if as_list(context.get("recent_commit_details")):
        lines = [
            "- The working tree and branch-range diff are both clean, so this draft is falling back to recent committed work as evidence.",
        ]
        preview = summarize_subjects(subjects)
        if preview:
            lines.append(f"- The most relevant recent commit signals are {preview}.")
        return lines
    return ["- No extra branch evidence was provided for this draft."]


def default_why_lines(
    diff: dict[str, Any],
    branch_range: dict[str, Any],
    context: dict[str, Any],
) -> list[str]:
    source_label, files, subjects = analysis_inputs(diff, branch_range, context)
    signals = infer_signals(files, subjects)
    summary = infer_change_goal(signals)
    preview_files = summarize_files(files)
    preview_subjects = summarize_subjects(subjects)

    if not summary:
        return [
            "- Local repository context shows what changed, but the motivating `why` is still missing; add an explicit `--why` note before external sharing.",
        ]

    lines = [f"- Inferred from {source_label}: this branch appears to {summary}."]
    if preview_subjects:
        lines.append(f"- The strongest local intent signals are {preview_subjects}.")
    if preview_files:
        lines.append(f"- Touched areas include {preview_files}.")
    lines.append(
        "- Replace or tighten this inferred rationale with an explicit `--why` note if reviewers need the product, incident, or tradeoff context behind the change."
    )
    return lines


def default_validation_lines(
    diff: dict[str, Any],
    branch_range: dict[str, Any],
    context: dict[str, Any],
) -> list[str]:
    _, files, subjects = analysis_inputs(diff, branch_range, context)
    signals = infer_signals(files, subjects)
    lines = ["- No explicit validation notes were provided for this draft."]

    if "adapter" in signals or "workflow" in signals or "runtime" in signals:
        lines.append(
            "- Add at least one shared CLI, direct-script, or installed-wrapper smoke test result before external sharing."
        )
    elif "ci" in signals:
        lines.append(
            "- Add the relevant workflow rerun or CI result so reviewers can see the effect of the change directly."
        )
    elif "dependency" in signals or "config" in signals:
        lines.append(
            "- Add the build, compatibility, or configuration check that justified the change."
        )
    elif "docs" in signals and not any(
        name in signals for name in ("adapter", "workflow", "runtime", "ci", "dependency")
    ):
        lines.append(
            "- If this is guidance-only work, confirm that commands, paths, and examples still match the current implementation."
        )
    elif "examples" in signals or "evaluation" in signals or "spec" in signals:
        lines.append(
            "- Confirm that examples, evaluations, and schema-facing artifacts still match the generated output shape."
        )

    return lines


def default_reviewer_notes(
    diff: dict[str, Any],
    branch_range: dict[str, Any],
    context: dict[str, Any],
) -> list[str]:
    source_label, files, subjects = analysis_inputs(diff, branch_range, context)
    signals = infer_signals(files, subjects)
    lines: list[str] = []

    if as_list(branch_range.get("changed_files")) and not as_list(diff.get("changed_files")):
        lines.append(
            "- The working tree is clean, so review the committed branch-range changes above rather than expecting uncommitted diffs."
        )
    elif source_label == "recent committed work":
        lines.append(
            "- There is no current diff against the base reference, so review should anchor on the recent commit history and the explicit rationale notes."
        )

    if "rename" in signals:
        lines.append(
            "- Check that rename-sensitive surfaces stay aligned across commands, package paths, installed support directories, and published docs."
        )
    if "workflow" in signals or "runtime" in signals:
        lines.append(
            "- Focus review on whether the documented workflow entry points still match the runtime behavior and shared helper paths."
        )
    if "adapter" in signals:
        lines.append(
            "- Verify installed-path behavior, not just repository-root execution, when adapter or installer glue changed."
        )
    if "docs" in signals:
        lines.append(
            "- Confirm that README, skill instructions, and examples describe the same behavior the code now implements."
        )
    if "ci" in signals:
        lines.append(
            "- Review whether the workflow change preserves failure visibility instead of only making the pipeline look greener."
        )
    if "dependency" in signals or "config" in signals:
        lines.append(
            "- Check compatibility assumptions, migration cost, and rollback safety for the dependency or config change."
        )
    if "examples" in signals or "evaluation" in signals:
        lines.append(
            "- Check that published examples and evaluation prompts still match the current workflow output shape."
        )
    if "spec" in signals:
        lines.append(
            "- Confirm that schemas, docs, and any helper scripts stay consistent when spec-facing files changed."
        )

    return dedupe_preserve_order(lines)[:4] or [
        "- Add reviewer watch points once the branch has a clearer diff against its intended base or more explicit rationale inputs.",
    ]


def default_risk_lines(
    diff: dict[str, Any],
    branch_range: dict[str, Any],
    context: dict[str, Any],
    *,
    has_explicit_why: bool,
) -> list[str]:
    source_label, files, subjects = analysis_inputs(diff, branch_range, context)
    signals = infer_signals(files, subjects)
    has_change_signal = bool(files or subjects)
    lines: list[str] = []

    if not has_explicit_why and has_change_signal:
        lines.append(
            "- The reviewer-facing draft still needs an explicit tradeoff or motivation note if approval depends on more than the local branch evidence."
        )
    if "rename" in signals:
        lines.append(
            "- Partial rename drift can leave old commands, paths, or install locations behind even when the main code path looks correct."
        )
    if "adapter" in signals or "workflow" in signals or "runtime" in signals:
        lines.append(
            "- Path or wrapper changes can still break installed or cross-agent execution surfaces unless they are smoke-tested explicitly."
        )
    if "docs" in signals:
        lines.append(
            "- Stale docs or examples would mislead reviewers and future agents even if the underlying code change is correct."
        )
    if "ci" in signals:
        lines.append(
            "- CI-facing changes can mask the underlying failure mode if the rationale or validation evidence is too thin."
        )
    if "dependency" in signals or "config" in signals:
        lines.append(
            "- Dependency or config changes may need explicit rollback or follow-up notes if the migration is only partial."
        )
    if "examples" in signals or "evaluation" in signals or "spec" in signals:
        lines.append(
            "- Supporting artifacts can drift from the implementation if they are not regenerated or rechecked alongside the code change."
        )

    if lines:
        return dedupe_preserve_order(lines)[:4]

    if as_list(diff.get("changed_files")) or as_list(branch_range.get("changed_files")):
        return [
            "- This draft still needs explicit risk and follow-up notes tied to the actual change before external sharing.",
        ]
    if source_label == "recent committed work":
        return [
            "- No working-tree or branch-range diff was detected; confirm whether the intended change already lives in recent commits or a different branch.",
        ]
    return [
        "- The local branch evidence is still too thin to describe the main risk confidently; add an explicit risk or follow-up note before sharing externally.",
    ]


def analysis_inputs(
    diff: dict[str, Any],
    branch_range: dict[str, Any],
    context: dict[str, Any],
) -> tuple[str, list[str], list[str]]:
    changed_files = normalized_paths(as_list(diff.get("changed_files")))
    if changed_files:
        return (
            "the current working-tree diff",
            changed_files,
            extract_subjects(branch_range, context, allow_recent_fallback=False),
        )

    branch_files = normalized_paths(as_list(branch_range.get("changed_files")))
    if branch_files:
        return (
            "committed branch-range context",
            branch_files,
            extract_subjects(branch_range, context, allow_recent_fallback=False),
        )

    recent_files = collect_recent_files(context)
    if recent_files:
        return "recent committed work", recent_files, extract_subjects(
            branch_range, context, allow_recent_fallback=True
        )

    return "local repository context", [], extract_subjects(
        branch_range, context, allow_recent_fallback=True
    )


def normalized_paths(values: list[Any]) -> list[str]:
    cleaned: list[str] = []
    for value in values:
        if not isinstance(value, str):
            continue
        path = value.strip().replace("\\", "/")
        if path:
            cleaned.append(path)
    return dedupe_preserve_order(cleaned)


def collect_recent_files(context: dict[str, Any]) -> list[str]:
    files: list[str] = []
    for entry in as_list(context.get("recent_commit_details"))[:5]:
        if not isinstance(entry, dict):
            continue
        files.extend(normalized_paths(as_list(entry.get("files"))))
    return dedupe_preserve_order(files)


def extract_subjects(
    branch_range: dict[str, Any],
    context: dict[str, Any],
    *,
    allow_recent_fallback: bool,
) -> list[str]:
    branch_commits = as_list(branch_range.get("commits"))
    subjects: list[str] = []

    for commit in branch_commits[:5]:
        if not isinstance(commit, str):
            continue
        _, _, tail = commit.partition(" ")
        subject = tail.strip() or commit.strip()
        if subject:
            subjects.append(subject)

    if subjects:
        return dedupe_preserve_order(subjects)

    if not allow_recent_fallback:
        return []

    for entry in as_list(context.get("recent_commit_details"))[:5]:
        if not isinstance(entry, dict):
            continue
        subject = string_value(entry.get("subject"))
        if subject:
            subjects.append(subject)

    if subjects:
        return dedupe_preserve_order(subjects)

    for commit in as_list(context.get("recent_commits"))[:5]:
        if not isinstance(commit, str):
            continue
        _, _, tail = commit.partition(" ")
        subject = tail.strip() or commit.strip()
        if subject:
            subjects.append(subject)

    return dedupe_preserve_order(subjects)


def summarize_subjects(subjects: list[str]) -> str:
    preview = [f"`{subject}`" for subject in subjects[:2] if subject]
    if not preview:
        return ""
    if len(subjects) > 2:
        preview.append(f"and `{len(subjects) - 2}` more subjects")
    return ", ".join(preview)


def infer_signals(files: list[str], subjects: list[str]) -> set[str]:
    signals: set[str] = set()

    for path in files:
        lower = path.lower()
        name = lower.rsplit("/", 1)[-1]
        if (
            lower.startswith("docs/")
            or name in {"readme.md", "readme.ko.md", "contributing.md", "security.md"}
            or lower.endswith(".md")
        ):
            signals.add("docs")
        if lower.startswith("adapters/") or "install" in name:
            signals.add("adapter")
        if lower.startswith("mimir_skills/") or lower.startswith("skills/") or lower.startswith("scripts/"):
            signals.add("workflow")
            signals.add("runtime")
        if lower.startswith(".github/") or lower.startswith(".circleci/") or lower.startswith(".gitlab/"):
            signals.add("ci")
        if lower.startswith("examples/"):
            signals.add("examples")
        if lower.startswith("evaluations/"):
            signals.add("evaluation")
        if lower.startswith("spec/") or "schema" in name:
            signals.add("spec")
        if name in {
            "package.json",
            "pnpm-lock.yaml",
            "poetry.lock",
            "pyproject.toml",
            "requirements.txt",
            "requirements-dev.txt",
            "cargo.toml",
            "cargo.lock",
            "go.mod",
            "go.sum",
        }:
            signals.add("dependency")
        if name.endswith((".yaml", ".yml", ".json", ".toml")) and not lower.startswith("examples/"):
            signals.add("config")

    for subject in subjects:
        lower = subject.lower()
        if any(token in lower for token in ("rename", "rebrand")):
            signals.add("rename")
        if any(token in lower for token in ("docs", "readme", "guide", "quick start")):
            signals.add("docs")
        if any(token in lower for token in ("adapter", "installer", "install", "support-level")):
            signals.add("adapter")
        if any(token in lower for token in ("cli", "workflow", "wrapper", "runtime")):
            signals.add("workflow")
            signals.add("runtime")
        if any(token in lower for token in ("ci", "github actions", "timeout", "build")):
            signals.add("ci")
        if any(token in lower for token in ("schema", "spec", "policy")):
            signals.add("spec")
        if any(token in lower for token in ("evaluation", "reviewer", "comprehension")):
            signals.add("evaluation")
        if any(token in lower for token in ("example", "summary")):
            signals.add("examples")
        if any(token in lower for token in ("dependency", "upgrade", "pin", "lockfile")):
            signals.add("dependency")
        if any(token in lower for token in ("config", "configuration")):
            signals.add("config")

    return signals


def infer_change_goal(signals: set[str]) -> str:
    if "rename" in signals and {"workflow", "adapter", "docs"} & signals:
        return "align the rename across the runtime surface, installed path, and published guidance"
    if {"workflow", "adapter", "docs"} <= signals:
        return "bring the workflow runtime, adapter path, and public guidance back into sync"
    if "workflow" in signals and "docs" in signals:
        return "update the workflow or runtime surface and align the docs around that behavior"
    if "adapter" in signals and "workflow" in signals:
        return "change workflow execution behavior and keep the installed adapter path aligned"
    if "dependency" in signals or "config" in signals:
        return "adjust dependency or configuration behavior in a way reviewers should evaluate for compatibility and rollout risk"
    if "ci" in signals:
        return "change CI or automation behavior while preserving visibility into the real failure or maintenance cost"
    if "spec" in signals and ("docs" in signals or "evaluation" in signals):
        return "update the spec-facing contract and keep docs or evaluation surfaces aligned with it"
    if "examples" in signals or "evaluation" in signals:
        return "refresh supporting examples or evaluation material so they still match the current workflow story"
    if "docs" in signals:
        return "tighten the published guidance around the current behavior or product direction"
    if "workflow" in signals or "runtime" in signals:
        return "change the workflow or runtime implementation shown in the branch context above"
    if "adapter" in signals:
        return "adjust installation or adapter glue so the supported execution surface still works"
    return ""


def dedupe_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result
