#!/usr/bin/env python3
"""Validate public memory candidate and validated JSON artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


MEMORY_ID_PATTERN = re.compile(r"^mem-\d{8}-[a-z0-9-]+-\d{3}$")
DECISION_ID_PATTERN = re.compile(r"^dec-\d{8}-[a-z0-9-]+-\d{3}$")
MEMORY_STATUSES = {"candidate", "validated"}
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


@dataclass
class ValidationResult:
    path: Path
    errors: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate one memory artifact JSON file or every JSON file under a directory."
    )
    parser.add_argument(
        "path",
        nargs="+",
        help="JSON file or directory containing memory candidate or validated JSON files.",
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
        f"\nValidated {len(results)} memory artifact file(s): "
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
    validate_memory_id(data.get("id"), errors)
    validate_required_string(data, "statement", errors)
    validate_required_string(data, "scope", errors)
    validate_source_decision_ids(data.get("source_decision_ids"), errors)
    validate_evidence_refs(data.get("evidence_refs"), errors)
    validate_confidence(data.get("confidence"), errors)
    validate_required_timestamp(data, "created_at", errors)
    validate_status(data.get("status"), errors)

    status = data.get("status")
    if status == "validated":
        validate_required_timestamp(data, "validated_at", errors)
        validate_required_timestamp(data, "last_validated_at", errors)
        validate_validation_basis(data.get("validation_basis"), errors)
        validate_freshness(data.get("freshness"), errors)

    record_id = data.get("id")
    if isinstance(record_id, str) and path.name != f"{record_id}.json":
        errors.append(f"file name must match id: expected {record_id}.json")

    return ValidationResult(path, errors)


def validate_required_string(data: dict[str, Any], key: str, errors: list[str]) -> None:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{key} must be a non-empty string")


def validate_memory_id(value: Any, errors: list[str]) -> None:
    if not isinstance(value, str):
        return
    if not MEMORY_ID_PATTERN.fullmatch(value):
        errors.append("id must match mem-YYYYMMDD-<slug>-NNN")
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


def validate_source_decision_ids(value: Any, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append("source_decision_ids must be a non-empty array")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"source_decision_ids[{index}] must be a non-empty string")
            continue
        if not DECISION_ID_PATTERN.fullmatch(item.strip()):
            errors.append(f"source_decision_ids[{index}] must match dec-YYYYMMDD-<slug>-NNN")


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


def validate_confidence(value: Any, errors: list[str]) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        errors.append("confidence must be a number between 0.0 and 1.0")
        return
    if value < 0.0 or value > 1.0:
        errors.append("confidence must be between 0.0 and 1.0")


def validate_status(value: Any, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append("status must be a non-empty string")
        return
    if value not in MEMORY_STATUSES:
        errors.append(f"status must be one of: {', '.join(sorted(MEMORY_STATUSES))}")


def validate_validation_basis(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("validation_basis must be an object when status is validated")
        return

    summary = value.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        errors.append("validation_basis.summary must be a non-empty string")

    branch = value.get("branch")
    if branch is not None and (not isinstance(branch, str) or not branch.strip()):
        errors.append("validation_basis.branch must be a non-empty string when present")


def validate_freshness(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("freshness must be an object when status is validated")
        return

    has_expiry = False
    expires_at = value.get("expires_at")
    if expires_at is not None:
        has_expiry = True
        if not isinstance(expires_at, str) or not is_valid_utc_timestamp(expires_at):
            errors.append("freshness.expires_at must be an ISO 8601 UTC timestamp when present")

    has_interval = False
    revalidate_after_days = value.get("revalidate_after_days")
    if revalidate_after_days is not None:
        has_interval = True
        if not isinstance(revalidate_after_days, int) or isinstance(revalidate_after_days, bool):
            errors.append("freshness.revalidate_after_days must be an integer when present")
        elif revalidate_after_days <= 0:
            errors.append("freshness.revalidate_after_days must be greater than 0")

    if not has_expiry and not has_interval:
        errors.append("freshness must include expires_at or revalidate_after_days")

    reason = value.get("reason")
    if reason is not None and (not isinstance(reason, str) or not reason.strip()):
        errors.append("freshness.reason must be a non-empty string when present")


def is_valid_utc_timestamp(value: str) -> bool:
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return False
    return parsed.utcoffset() is not None and parsed.utcoffset().total_seconds() == 0


if __name__ == "__main__":
    raise SystemExit(main())
