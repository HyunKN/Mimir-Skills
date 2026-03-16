#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path


SUPPORT_DIR_NAME = "decision-skills-support"
INSTALL_MARKER_NAME = ".decision-skills-install.json"
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install decision-skills public workflows into a local Codex skills directory."
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=None,
        help="Override CODEX_HOME. Defaults to $CODEX_HOME or ~/.codex.",
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
    return parser.parse_args()


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
    runtime_root = destination / "decision_skills"
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
            f"Refusing to replace {destination} because it is outside the managed Codex skills root {skills_root}."
        )

    if entry_type == "support":
        looks_managed = looks_like_managed_support_dir(destination)
    else:
        looks_managed = looks_like_managed_skill_dir(destination, expected_name)

    if not looks_managed:
        raise RuntimeError(
            f"Refusing to replace {destination} with --force because it does not look like a previous decision-skills installation. "
            "Remove it manually or choose a different --codex-home if this path is intentional."
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
    text = text.replace("../../examples/", f"../{SUPPORT_DIR_NAME}/examples/")
    text = text.replace("../../evaluations/", f"../{SUPPORT_DIR_NAME}/evaluations/")
    skill_file.write_text(text, encoding="utf-8", newline="\n")


def install_support_assets(repo_root: Path, skills_root: Path, force: bool) -> Path:
    support_root = skills_root / SUPPORT_DIR_NAME
    support_root.mkdir(parents=True, exist_ok=True)

    if force and any(
        destination.exists()
        for destination in [
            support_root / "examples",
            support_root / "evaluations",
            support_root / "decision_skills",
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
    copy_tree(repo_root / "decision_skills", support_root / "decision_skills", force)
    write_install_marker(support_root, repo_root, "support", SUPPORT_DIR_NAME)

    return support_root


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[3]
    codex_home = resolve_codex_home(args.codex_home)
    skills_root = codex_home / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)

    selected_workflows = list(dict.fromkeys(args.workflows))
    skill_names = sorted(
        {
            skill_name
            for workflow in selected_workflows
            for skill_name in WORKFLOW_DEPENDENCIES[workflow]
        }
    )

    support_root = install_support_assets(repo_root, skills_root, args.force)

    for skill_name in skill_names:
        source = repo_root / "skills" / skill_name
        destination = skills_root / skill_name
        if args.force and destination.exists():
            ensure_safe_force_replace(
                destination,
                skills_root,
                entry_type="skill",
                expected_name=skill_name,
            )
        copy_tree(source, destination, args.force)
        rewrite_installed_skill(destination)
        write_install_marker(destination, repo_root, "skill", skill_name)

    manifest = {
        "source_repo": str(repo_root),
        "workflows": selected_workflows,
        "installed_skills": skill_names,
        "support_root": str(support_root),
        "shared_runtime_root": str(support_root / "decision_skills"),
    }
    (support_root / "install-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print(f"Installed decision-skills workflows into {skills_root}")
    print("Installed workflows:")
    for workflow in selected_workflows:
        print(f"- {workflow}")
    print("Installed skill directories:")
    for skill_name in skill_names:
        print(f"- {skills_root / skill_name}")
    print(f"Installed support assets under {support_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
