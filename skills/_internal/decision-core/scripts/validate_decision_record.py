#!/usr/bin/env python3
"""Validate canonical decision record JSON files for Mimir-Skills."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


ID_PATTERN = re.compile(r"^dec-\d{8}-[a-z0-9-]+-\d{3}$")
TASK_REF_SOURCES = {"issue", "pr", "thread", "ci", "local", "other"}
EVIDENCE_KINDS = {
    "file",
    "diff",
    "test",
    "ci",
    "doc",
    "issue",
    "command",
    "discussion",
    "other",
}
ALTERNATIVE_STATUSES = {"rejected", "deferred", "selected"}
VALIDATION_TYPES = {"test", "build", "lint", "manual", "other"}
VALIDATION_RESULTS = {"passed", "failed", "partial", "not_run"}


@dataclass
class ValidationResult:
    path: Path
    errors: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate one decision record JSON file or every JSON file under a directory."
    )
    parser.add_argument(
        "path",
        nargs="+",
        help="JSON file or directory containing decision record JSON files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files = collect_files(args.path)

    if not files:
        print("No JSON files found to validate.", file=sys.stderr)
        return 1

    results = [validate_file(path) for path in files]

    invalid_count = 0
    for result in results:
        if result.errors:
            invalid_count += 1
            print(f"FAIL {result.path}")
            for error in result.errors:
                print(f"  - {error}")
        else:
            print(f"PASS {result.path}")

    print(
        f"\nValidated {len(results)} file(s): "
        f"{len(results) - invalid_count} passed, {invalid_count} failed."
    )
    return 0 if invalid_count == 0 else 2


def collect_files(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(candidate for candidate in path.rglob("*.json") if candidate.is_file()))
        elif path.is_file():
            files.append(path)
    return files


def validate_file(path: Path) -> ValidationResult:
    errors: list[str] = []

    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return ValidationResult(path, [f"invalid JSON: {exc.msg} at line {exc.lineno}, column {exc.colno}"])

    if not isinstance(data, dict):
        return ValidationResult(path, ["top-level JSON value must be an object"])

    validate_required_string(data, "id", errors)
    validate_id(data.get("id"), errors)
    validate_required_timestamp(data, "timestamp", errors)
    validate_task_ref(data.get("task_ref"), errors)
    validate_selected_option(data.get("selected_option"), errors)
    validate_required_string(data, "decision", errors)
    validate_required_string(data, "rationale", errors)
    validate_evidence_refs(data.get("evidence_refs"), errors)
    validate_affected_paths(data.get("affected_paths"), errors)
    validate_confidence(data.get("confidence"), errors)

    validate_optional_string(data, "problem_context", errors)
    validate_alternatives(data.get("alternatives_considered"), errors)
    validate_validation_run(data.get("validation_run"), errors)
    validate_string_list(data.get("remaining_risks"), "remaining_risks", errors)
    validate_string_list(data.get("follow_up"), "follow_up", errors)
    validate_string_list(data.get("supersedes"), "supersedes", errors)

    record_id = data.get("id")
    if isinstance(record_id, str) and path.name != f"{record_id}.json":
        errors.append(f"file name must match id: expected {record_id}.json")

    return ValidationResult(path, errors)


def validate_required_string(data: dict[str, Any], key: str, errors: list[str]) -> None:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{key} must be a non-empty string")


def validate_optional_string(data: dict[str, Any], key: str, errors: list[str]) -> None:
    if key in data and not isinstance(data[key], str):
        errors.append(f"{key} must be a string when present")


def validate_id(value: Any, errors: list[str]) -> None:
    if not isinstance(value, str):
        return
    if not ID_PATTERN.fullmatch(value):
        errors.append("id must match dec-YYYYMMDD-<slug>-NNN")
        return
    date_part = value[4:12]
    try:
        datetime.strptime(date_part, "%Y%m%d")
    except ValueError:
        errors.append("id must contain a valid calendar date in YYYYMMDD form")


def validate_required_timestamp(data: dict[str, Any], key: str, errors: list[str]) -> None:
    value = data.get(key)
    if not isinstance(value, str):
        errors.append(f"{key} must be an ISO 8601 UTC timestamp string")
        return
    if not is_valid_utc_timestamp(value):
        errors.append(f"{key} must be an ISO 8601 UTC timestamp ending in Z or +00:00")


def validate_task_ref(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("task_ref must be an object")
        return

    for key in ("source", "id", "title"):
        if not isinstance(value.get(key), str) or not value[key].strip():
            errors.append(f"task_ref.{key} must be a non-empty string")

    source = value.get("source")
    if isinstance(source, str) and source not in TASK_REF_SOURCES:
        errors.append(f"task_ref.source must be one of: {', '.join(sorted(TASK_REF_SOURCES))}")


def validate_selected_option(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("selected_option must be an object")
        return

    for key in ("name", "summary"):
        if not isinstance(value.get(key), str) or not value[key].strip():
            errors.append(f"selected_option.{key} must be a non-empty string")


def validate_evidence_refs(value: Any, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append("evidence_refs must be a non-empty array")
        return

    for index, item in enumerate(value):
        prefix = f"evidence_refs[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in ("kind", "ref", "summary", "captured_at"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"{prefix}.{key} must be a non-empty string")
        kind = item.get("kind")
        if isinstance(kind, str) and kind not in EVIDENCE_KINDS:
            errors.append(f"{prefix}.kind must be one of: {', '.join(sorted(EVIDENCE_KINDS))}")
        captured_at = item.get("captured_at")
        if isinstance(captured_at, str) and not is_valid_utc_timestamp(captured_at):
            errors.append(f"{prefix}.captured_at must be an ISO 8601 UTC timestamp")


def validate_affected_paths(value: Any, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append("affected_paths must be an array")
        return

    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"affected_paths[{index}] must be a non-empty string")


def validate_confidence(value: Any, errors: list[str]) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        errors.append("confidence must be a number between 0.0 and 1.0")
        return
    if value < 0.0 or value > 1.0:
        errors.append("confidence must be between 0.0 and 1.0")


def validate_alternatives(value: Any, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        errors.append("alternatives_considered must be an array when present")
        return

    for index, item in enumerate(value):
        prefix = f"alternatives_considered[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in ("name", "status", "reason"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"{prefix}.{key} must be a non-empty string")
        status = item.get("status")
        if isinstance(status, str) and status not in ALTERNATIVE_STATUSES:
            errors.append(
                f"{prefix}.status must be one of: {', '.join(sorted(ALTERNATIVE_STATUSES))}"
            )


def validate_validation_run(value: Any, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        errors.append("validation_run must be an array when present")
        return

    for index, item in enumerate(value):
        prefix = f"validation_run[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in ("type", "command", "result", "summary"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"{prefix}.{key} must be a non-empty string")
        record_type = item.get("type")
        if isinstance(record_type, str) and record_type not in VALIDATION_TYPES:
            errors.append(f"{prefix}.type must be one of: {', '.join(sorted(VALIDATION_TYPES))}")
        result = item.get("result")
        if isinstance(result, str) and result not in VALIDATION_RESULTS:
            errors.append(
                f"{prefix}.result must be one of: {', '.join(sorted(VALIDATION_RESULTS))}"
            )


def validate_string_list(value: Any, field_name: str, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        errors.append(f"{field_name} must be an array when present")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{field_name}[{index}] must be a non-empty string")


def is_valid_utc_timestamp(value: str) -> bool:
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return False
    offset = parsed.utcoffset()
    return offset is not None and offset.total_seconds() == 0


if __name__ == "__main__":
    raise SystemExit(main())
