from __future__ import annotations

import json
from pathlib import Path


CONFIG_DIR_NAME = "local"
CONFIG_FILENAME = "obsidian-output.json"
VALID_MODES = ("reports", "vault")


def resolve_project_dir(project_dir: Path | None = None) -> Path:
    return (project_dir or Path.cwd()).resolve()


def config_path_for_project(project_dir: Path | None = None) -> Path:
    base = resolve_project_dir(project_dir)
    return base / ".ai" / CONFIG_DIR_NAME / CONFIG_FILENAME


def find_ai_root(path: Path) -> Path | None:
    resolved = path.resolve()
    current = resolved if resolved.is_dir() else resolved.parent
    for candidate in [current, *current.parents]:
        if candidate.name == ".ai":
            return candidate
    return None


def project_dir_for_artifact(path: Path) -> Path | None:
    ai_root = find_ai_root(path)
    if ai_root is None:
        return None
    return ai_root.parent


def load_preference(project_dir: Path | None = None) -> dict[str, str] | None:
    config_path = config_path_for_project(project_dir)
    if not config_path.is_file():
        return None

    data = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Obsidian output preference must be a JSON object.")

    mode = data.get("mode")
    if mode not in VALID_MODES:
        raise ValueError("Obsidian output preference has an invalid mode.")

    vault_path = data.get("vault_path", "")
    if not isinstance(vault_path, str):
        raise ValueError("Obsidian output preference vault_path must be a string.")

    if mode == "vault" and not vault_path.strip():
        raise ValueError("Obsidian output preference in vault mode must include vault_path.")

    return {
        "mode": mode,
        "vault_path": vault_path.strip(),
    }


def save_reports_preference(project_dir: Path | None = None) -> Path:
    return save_preference({"mode": "reports", "vault_path": ""}, project_dir=project_dir)


def save_vault_preference(vault_path: Path, project_dir: Path | None = None) -> Path:
    resolved_vault_path = vault_path.expanduser().resolve()
    return save_preference(
        {"mode": "vault", "vault_path": str(resolved_vault_path)},
        project_dir=project_dir,
    )


def save_preference(data: dict[str, str], project_dir: Path | None = None) -> Path:
    mode = data.get("mode")
    vault_path = data.get("vault_path", "")
    if mode not in VALID_MODES:
        raise ValueError("Obsidian output preference has an invalid mode.")
    if mode == "vault" and not vault_path:
        raise ValueError("Vault mode requires a non-empty vault_path.")

    config_path = config_path_for_project(project_dir)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(
            {
                "mode": mode,
                "vault_path": vault_path,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return config_path


def clear_preference(project_dir: Path | None = None) -> Path:
    config_path = config_path_for_project(project_dir)
    if config_path.exists():
        config_path.unlink()
    return config_path


def describe_preference(project_dir: Path | None = None) -> str:
    preference = load_preference(project_dir)
    config_path = config_path_for_project(project_dir)
    if preference is None:
        return (
            f"No saved Obsidian output preference for this project. "
            f"Default output remains `.ai/records/reports/`. "
            f"Config path: {config_path}"
        )
    if preference["mode"] == "reports":
        return (
            f"Obsidian output preference: reports\n"
            f"Saved at: {config_path}\n"
            f"Effective default output: .ai/records/reports/"
        )
    return (
        f"Obsidian output preference: vault\n"
        f"Saved at: {config_path}\n"
        f"Vault path: {preference['vault_path']}"
    )


def preferred_output_path(source_path: Path, filename: str) -> Path:
    project_dir = project_dir_for_artifact(source_path)
    if project_dir is None:
        return source_path.with_name(filename)

    preference = load_preference(project_dir)
    ai_root = project_dir / ".ai"
    if preference is None or preference["mode"] == "reports":
        return ai_root / "records" / "reports" / filename

    return Path(preference["vault_path"]) / filename
