from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable


ContextCollector = Callable[[Path, int], dict[str, Any]]


def load_context(
    context_json: str | None,
    repo_path: Path,
    commit_limit: int,
    collector: ContextCollector,
) -> dict[str, Any]:
    if context_json:
        context_path = Path(context_json)
        try:
            data = json.loads(context_path.read_text(encoding="utf-8-sig"))
        except FileNotFoundError as exc:
            raise RuntimeError(f"Context JSON not found: {context_path}") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Invalid JSON in {context_path}: {exc.msg} at line {exc.lineno}, column {exc.colno}"
            ) from exc
        if not isinstance(data, dict):
            raise RuntimeError("Context JSON must be a top-level object.")
        return data
    return collector(repo_path, commit_limit)


def emit_json_output(context: dict[str, Any], output: str | None, label: str) -> int:
    payload = json.dumps(context, indent=2) + "\n"
    return emit_text_output(payload, output, label)


def emit_text_output(payload: str, output: str | None, label: str) -> int:
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload, encoding="utf-8")
        print(f"Wrote {label}: {output_path}")
    else:
        sys.stdout.write(payload)
    return 0


def section(title: str, bullets: list[str]) -> list[str]:
    lines = [f"## {title}", ""]
    lines.extend(bullets)
    lines.append("")
    return lines


def clean_bullets(values: list[str]) -> list[str]:
    cleaned: list[str] = []
    for value in values:
        text = value.strip()
        if not text:
            continue
        cleaned.append(text if text.startswith("- ") else f"- {text}")
    return cleaned


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_value(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def int_value(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def summarize_files(files: list[str]) -> str:
    if not files:
        return ""
    preview = [f"`{path}`" for path in files[:3]]
    if len(files) > 3:
        preview.append(f"and `{len(files) - 3}` more files")
    return ", ".join(preview)
