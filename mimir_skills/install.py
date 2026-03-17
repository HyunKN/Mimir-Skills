from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path
from typing import Sequence


SUPPORT_DIR_NAME = "mimir-skills-support"
INSTALL_MARKER_NAME = ".mimir-skills-install.json"
VALID_TARGETS = ("claude", "codex", "generic")
WORKFLOW_DEPENDENCIES = {
    "prepare-handoff": [
        "prepare-handoff",
        "handoff-context",
        "decision-capture",
        "decision-core",
    ],
    "write-pr-rationale": [
        "write-pr-rationale",
        "pr-rationale",
        "decision-capture",
        "decision-core",
    ],
    "capture-ci-investigation": [
        "capture-ci-investigation",
        "ci-rationale",
        "decision-capture",
        "decision-core",
    ],
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install Mimir-Skills workflows into a local AI agent skills directory."
    )
    parser.add_argument(
        "--target",
        choices=VALID_TARGETS,
        default=None,
        help="Install target: claude (.claude/skills/), codex ($CODEX_HOME/skills/), or generic (.skills/).",
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=None,
        help="Override CODEX_HOME for codex target. Defaults to $CODEX_HOME or ~/.codex.",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=None,
        help="Project directory for claude/generic targets. Defaults to current working directory.",
    )
    parser.add_argument(
        "--workflows",
        nargs="+",
        choices=sorted(WORKFLOW_DEPENDENCIES),
        default=sorted(WORKFLOW_DEPENDENCIES),
        help="Install only the selected outward-facing workflows and their dependencies.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing installed folders for the selected workflows and support assets.",
    )
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def detect_target(project_dir: Path) -> str:
    has_claude = (project_dir / ".claude").is_dir()
    has_codex = (project_dir / ".codex").is_dir()

    if has_claude and has_codex:
        raise RuntimeError(
            "Both .claude/ and .codex/ directories found. "
            "Please specify --target explicitly (claude, codex, or generic)."
        )
    if has_claude:
        return "claude"
    if has_codex:
        return "codex"
    # Fall back to codex if $CODEX_HOME is set (backward compat)
    if os.environ.get("CODEX_HOME"):
        return "codex"
    return "generic"


def resolve_skills_root(target: str, codex_home: Path | None, project_dir: Path | None) -> Path:
    if target == "codex":
        return resolve_codex_home(codex_home) / "skills"
    if target == "claude":
        base = (project_dir or Path.cwd()).resolve()
        return base / ".claude" / "skills"
    base = (project_dir or Path.cwd()).resolve()
    return base / ".skills"


def resolve_codex_home(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.expanduser().resolve()

    env_value = os.environ.get("CODEX_HOME")
    if env_value:
        return Path(env_value).expanduser().resolve()

    return (Path.home() / ".codex").resolve()


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def write_install_marker(destination: Path, repo_root: Path, entry_type: str, name: str) -> None:
    marker = {
        "source_repo": str(repo_root),
        "entry_type": entry_type,
        "name": name,
    }
    (destination / INSTALL_MARKER_NAME).write_text(
        json.dumps(marker, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def looks_like_managed_skill_dir(destination: Path, expected_name: str) -> bool:
    marker_file = destination / INSTALL_MARKER_NAME
    if marker_file.exists():
        try:
            marker = json.loads(marker_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return False
        return (
            marker.get("entry_type") == "skill"
            and marker.get("name") == expected_name
        )

    skill_file = destination / "SKILL.md"
    if not skill_file.exists():
        return False

    text = skill_file.read_text(encoding="utf-8")
    return f"name: {expected_name}" in text


def looks_like_managed_support_dir(destination: Path) -> bool:
    marker_file = destination / INSTALL_MARKER_NAME
    if marker_file.exists():
        try:
            marker = json.loads(marker_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return False
        return (
            marker.get("entry_type") == "support"
            and marker.get("name") == SUPPORT_DIR_NAME
        )

    manifest_file = destination / "install-manifest.json"
    runtime_root = destination / "mimir_skills"
    return manifest_file.exists() and runtime_root.exists()


def ensure_safe_force_replace(
    destination: Path,
    skills_root: Path,
    *,
    entry_type: str,
    expected_name: str,
) -> None:
    if destination.parent != skills_root or not is_relative_to(destination, skills_root):
        raise RuntimeError(
            f"Refusing to replace {destination} because it is outside the managed skills root {skills_root}."
        )

    if entry_type == "support":
        looks_managed = looks_like_managed_support_dir(destination)
    else:
        looks_managed = looks_like_managed_skill_dir(destination, expected_name)

    if not looks_managed:
        raise RuntimeError(
            f"Refusing to replace {destination} with --force because it does not look like a previous Mimir-Skills installation. "
            "Remove it manually if this path is intentional."
        )


def copy_tree(source: Path, destination: Path, force: bool) -> None:
    if destination.exists():
        if not force:
            raise FileExistsError(
                f"{destination} already exists. Re-run with --force to replace it."
            )
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def rewrite_installed_skill(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    text = text.replace("../../../examples/", f"../{SUPPORT_DIR_NAME}/examples/")
    text = text.replace("../../../evaluations/", f"../{SUPPORT_DIR_NAME}/evaluations/")
    text = text.replace("../../examples/", f"../{SUPPORT_DIR_NAME}/examples/")
    text = text.replace("../../evaluations/", f"../{SUPPORT_DIR_NAME}/evaluations/")
    skill_file.write_text(text, encoding="utf-8", newline="\n")
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        for ref_file in refs_dir.glob("*.md"):
            ref_text = ref_file.read_text(encoding="utf-8")
            ref_text = ref_text.replace("../../../examples/", f"../../{SUPPORT_DIR_NAME}/examples/")
            ref_text = ref_text.replace("../../../evaluations/", f"../../{SUPPORT_DIR_NAME}/evaluations/")
            ref_text = ref_text.replace("../../examples/", f"../../{SUPPORT_DIR_NAME}/examples/")
            ref_text = ref_text.replace("../../evaluations/", f"../../{SUPPORT_DIR_NAME}/evaluations/")
            ref_file.write_text(ref_text, encoding="utf-8", newline="\n")


def install_support_assets(repo_root: Path, skills_root: Path, force: bool) -> Path:
    support_root = skills_root / SUPPORT_DIR_NAME
    support_root.mkdir(parents=True, exist_ok=True)

    if force and any(
        destination.exists()
        for destination in [
            support_root / "examples",
            support_root / "evaluations",
            support_root / "mimir_skills",
        ]
    ):
        ensure_safe_force_replace(
            support_root,
            skills_root,
            entry_type="support",
            expected_name=SUPPORT_DIR_NAME,
        )

    copy_tree(repo_root / "examples", support_root / "examples", force)
    copy_tree(repo_root / "evaluations", support_root / "evaluations", force)
    copy_tree(repo_root / "mimir_skills", support_root / "mimir_skills", force)
    write_install_marker(support_root, repo_root, "support", SUPPORT_DIR_NAME)

    return support_root


def run_install(
    *,
    target: str | None = None,
    codex_home: Path | None = None,
    project_dir: Path | None = None,
    workflows: Sequence[str] | None = None,
    force: bool = False,
    repo_root: Path | None = None,
) -> int:
    resolved_repo_root = repo_root or Path(__file__).resolve().parents[1]
    resolved_project_dir = (project_dir or Path.cwd()).resolve()

    resolved_target = target or detect_target(resolved_project_dir)
    skills_root = resolve_skills_root(resolved_target, codex_home, project_dir)
    skills_root.mkdir(parents=True, exist_ok=True)

    selected_workflows = list(dict.fromkeys(workflows or sorted(WORKFLOW_DEPENDENCIES)))
    skill_names = sorted(
        {
            skill_name
            for workflow in selected_workflows
            for skill_name in WORKFLOW_DEPENDENCIES[workflow]
        }
    )

    support_root = install_support_assets(resolved_repo_root, skills_root, force)

    for skill_name in skill_names:
        if skill_name in WORKFLOW_DEPENDENCIES:
            source = resolved_repo_root / "skills" / skill_name
        else:
            source = resolved_repo_root / "skills" / "_internal" / skill_name
        destination = skills_root / skill_name
        if force and destination.exists():
            ensure_safe_force_replace(
                destination,
                skills_root,
                entry_type="skill",
                expected_name=skill_name,
            )
        copy_tree(source, destination, force)
        rewrite_installed_skill(destination)
        write_install_marker(destination, resolved_repo_root, "skill", skill_name)

    manifest = {
        "source_repo": str(resolved_repo_root),
        "target": resolved_target,
        "workflows": selected_workflows,
        "installed_skills": skill_names,
        "support_root": str(support_root),
        "shared_runtime_root": str(support_root / "mimir_skills"),
    }
    (support_root / "install-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print(f"Installed Mimir-Skills workflows into {skills_root} (target: {resolved_target})")
    print("Installed workflows:")
    for workflow in selected_workflows:
        print(f"  {workflow}")
    print("Installed skill directories:")
    for skill_name in skill_names:
        print(f"  {skills_root / skill_name}")
    print(f"Support assets: {support_root}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    return run_install(
        target=args.target,
        codex_home=args.codex_home,
        project_dir=args.project_dir,
        workflows=args.workflows,
        force=args.force,
    )


__all__ = [
    "VALID_TARGETS",
    "WORKFLOW_DEPENDENCIES",
    "build_parser",
    "detect_target",
    "main",
    "parse_args",
    "run_install",
]
