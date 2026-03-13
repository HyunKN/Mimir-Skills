#!/usr/bin/env python3
"""Check that public JSON Schemas stay aligned with helper validators."""

from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DECISION_SCHEMA_PATH = REPO_ROOT / "spec" / "decision-record-schema.json"
MEMORY_SCHEMA_PATH = REPO_ROOT / "spec" / "memory-artifact-schema.json"
DECISION_VALIDATOR_PATH = REPO_ROOT / "skills" / "decision-core" / "scripts" / "validate_decision_record.py"
MEMORY_VALIDATOR_PATH = REPO_ROOT / "skills" / "memory-promote" / "scripts" / "validate_memory_artifact.py"


@dataclass
class CheckResult:
    name: str
    errors: list[str]


def main() -> int:
    decision_schema = load_json(DECISION_SCHEMA_PATH)
    memory_schema = load_json(MEMORY_SCHEMA_PATH)
    decision_validator = load_module("decision_validator", DECISION_VALIDATOR_PATH)
    memory_validator = load_module("memory_validator", MEMORY_VALIDATOR_PATH)

    results = [
        check_set_match(
            "decision required fields",
            set(decision_schema.get("required", [])),
            {
                "id",
                "timestamp",
                "task_ref",
                "decision",
                "selected_option",
                "rationale",
                "evidence_refs",
                "affected_paths",
                "confidence",
            },
        ),
        check_set_match(
            "decision task_ref sources",
            extract_enum(decision_schema, "properties", "task_ref", "properties", "source"),
            set(decision_validator.TASK_REF_SOURCES),
        ),
        check_set_match(
            "decision evidence kinds",
            extract_enum(decision_schema, "properties", "evidence_refs", "items", "properties", "kind"),
            set(decision_validator.EVIDENCE_KINDS),
        ),
        check_set_match(
            "decision alternative statuses",
            extract_enum(
                decision_schema,
                "properties",
                "alternatives_considered",
                "items",
                "properties",
                "status",
            ),
            set(decision_validator.ALTERNATIVE_STATUSES),
        ),
        check_set_match(
            "decision validation types",
            extract_enum(
                decision_schema,
                "properties",
                "validation_run",
                "items",
                "properties",
                "type",
            ),
            set(decision_validator.VALIDATION_TYPES),
        ),
        check_set_match(
            "decision validation results",
            extract_enum(
                decision_schema,
                "properties",
                "validation_run",
                "items",
                "properties",
                "result",
            ),
            set(decision_validator.VALIDATION_RESULTS),
        ),
        check_set_match(
            "memory required fields",
            set(memory_schema.get("required", [])),
            {
                "id",
                "statement",
                "scope",
                "source_decision_ids",
                "evidence_refs",
                "confidence",
                "created_at",
                "status",
            },
        ),
        check_set_match(
            "memory statuses",
            extract_enum(memory_schema, "properties", "status"),
            set(memory_validator.MEMORY_STATUSES),
        ),
        check_set_match(
            "memory evidence kinds",
            extract_enum(memory_schema, "properties", "evidence_refs", "items", "properties", "kind"),
            set(memory_validator.EVIDENCE_KINDS),
        ),
        check_set_match(
            "validated memory conditional fields",
            extract_conditional_required(memory_schema, "validated"),
            {"validated_at", "validation_basis", "last_validated_at", "freshness"},
        ),
    ]

    failures = 0
    for result in results:
        if result.errors:
            failures += 1
            print(f"FAIL {result.name}")
            for error in result.errors:
                print(f"  - {error}")
        else:
            print(f"PASS {result.name}")

    print(
        f"\nChecked {len(results)} schema consistency rule(s): "
        f"{len(results) - failures} passed, {failures} failed."
    )
    return 0 if failures == 0 else 2


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing schema file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Invalid schema JSON in {path}: {exc.msg} at line {exc.lineno}, column {exc.colno}"
        ) from exc

    if not isinstance(data, dict):
        raise SystemExit(f"Schema root must be an object: {path}")

    return data


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load module spec from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def extract_enum(schema: dict[str, Any], *segments: str) -> set[str]:
    node: Any = schema
    for segment in segments:
        if not isinstance(node, dict) or segment not in node:
            raise SystemExit(f"Missing schema path: {'/'.join(segments)}")
        node = node[segment]

    if not isinstance(node, dict) or "enum" not in node or not isinstance(node["enum"], list):
        raise SystemExit(f"Schema path does not end in enum: {'/'.join(segments)}")

    return {str(value) for value in node["enum"]}


def extract_conditional_required(schema: dict[str, Any], target_status: str) -> set[str]:
    all_of = schema.get("allOf")
    if not isinstance(all_of, list):
        raise SystemExit("Memory schema is missing allOf conditional rules")

    for clause in all_of:
        if not isinstance(clause, dict):
            continue
        if_block = clause.get("if")
        then_block = clause.get("then")
        if not isinstance(if_block, dict) or not isinstance(then_block, dict):
            continue
        properties = if_block.get("properties")
        if not isinstance(properties, dict):
            continue
        status = properties.get("status")
        if not isinstance(status, dict):
            continue
        if status.get("const") != target_status:
            continue
        required = then_block.get("required")
        if not isinstance(required, list):
            raise SystemExit(f"Memory schema conditional for status={target_status} is missing required")
        return {str(value) for value in required}

    raise SystemExit(f"Memory schema conditional for status={target_status} not found")


def check_set_match(name: str, actual: set[str], expected: set[str]) -> CheckResult:
    errors: list[str] = []
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)

    if missing:
        errors.append(f"missing expected values: {', '.join(missing)}")
    if extra:
        errors.append(f"unexpected extra values: {', '.join(extra)}")

    return CheckResult(name=name, errors=errors)


if __name__ == "__main__":
    raise SystemExit(main())
