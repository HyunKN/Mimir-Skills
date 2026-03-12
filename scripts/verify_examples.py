#!/usr/bin/env python3
"""Verify public examples and derived summaries for decision-skills."""

from __future__ import annotations

import difflib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = REPO_ROOT / "examples"
DECISION_SCHEMA_PATH = REPO_ROOT / "spec" / "decision-record-schema.json"
MEMORY_SCHEMA_PATH = REPO_ROOT / "spec" / "memory-artifact-schema.json"
VALIDATOR_PATH = REPO_ROOT / "skills" / "decision-core" / "scripts" / "validate_decision_record.py"
MEMORY_VALIDATOR_PATH = (
    REPO_ROOT / "skills" / "memory-promote" / "scripts" / "validate_memory_artifact.py"
)
RENDERER_PATH = REPO_ROOT / "skills" / "decision-capture" / "scripts" / "render_summary.py"


def main() -> int:
    if not EXAMPLES_ROOT.is_dir():
        print(f"Examples directory not found: {EXAMPLES_ROOT}", file=sys.stderr)
        return 1

    if not check_schema_json():
        return 1

    records = sorted(EXAMPLES_ROOT.glob("* /.ai/records/decisions/*.json".replace(" ", "")))
    if not records:
        print("No example decision records found.", file=sys.stderr)
        return 1

    if not run_validator(records):
        return 2

    if not check_memory_artifacts():
        return 2

    if not check_rendered_summaries(records):
        return 2

    print(f"\nVerified {len(records)} example decision record(s) and their derived summaries.")
    return 0


def check_schema_json() -> bool:
    success = True
    for schema_path in (DECISION_SCHEMA_PATH, MEMORY_SCHEMA_PATH):
        try:
            json.loads(schema_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            print(f"FAIL missing machine-readable schema: {schema_path}", file=sys.stderr)
            success = False
            continue
        except json.JSONDecodeError as exc:
            print(
                f"FAIL invalid machine-readable schema: {schema_path} "
                f"({exc.msg} at line {exc.lineno}, column {exc.colno})",
                file=sys.stderr,
            )
            success = False
            continue

        print(f"PASS machine-readable schema parses: {schema_path.relative_to(REPO_ROOT)}")

    return success


def run_validator(records: list[Path]) -> bool:
    command = [sys.executable, str(VALIDATOR_PATH), *[str(path) for path in records]]
    result = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, check=False)

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")

    return result.returncode == 0


def check_memory_artifacts() -> bool:
    candidate_paths = sorted(EXAMPLES_ROOT.glob("* /.ai/records/memories/candidates/*.json".replace(" ", "")))
    validated_paths = sorted(EXAMPLES_ROOT.glob("* /.ai/records/memories/validated/*.json".replace(" ", "")))

    if not candidate_paths and not validated_paths:
        return True

    artifact_paths = [*candidate_paths, *validated_paths]
    command = [sys.executable, str(MEMORY_VALIDATOR_PATH), *[str(path) for path in artifact_paths]]
    result = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, check=False)

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")

    if result.returncode != 0:
        return False

    success = True
    candidate_map = {(path.parents[3], path.stem): path for path in candidate_paths}

    for validated_path in validated_paths:
        key = (validated_path.parents[3], validated_path.stem)
        if key not in candidate_map:
            print(
                "FAIL missing matching candidate for validated memory: "
                f"{validated_path.relative_to(REPO_ROOT)}",
                file=sys.stderr,
            )
            success = False
        else:
            print(
                "PASS matching candidate exists for validated memory: "
                f"{validated_path.relative_to(REPO_ROOT)}"
            )

    return success


def check_rendered_summaries(records: list[Path]) -> bool:
    success = True

    with tempfile.TemporaryDirectory(prefix="decision-skills-render-") as temp_dir:
        temp_root = Path(temp_dir)

        for record_path in records:
            example_dir = record_path.parents[3]
            checked_in_summary = (
                example_dir / ".ai" / "records" / "reports" / f"{example_dir.name}-summary.md"
            )
            rendered_summary = temp_root / f"{example_dir.name}-summary.md"

            if not checked_in_summary.is_file():
                print(
                    f"FAIL missing checked-in summary: {checked_in_summary.relative_to(REPO_ROOT)}",
                    file=sys.stderr,
                )
                success = False
                continue

            command = [
                sys.executable,
                str(RENDERER_PATH),
                str(record_path),
                "--output",
                str(rendered_summary),
            ]
            result = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, check=False)

            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, file=sys.stderr, end="")

            if result.returncode != 0:
                success = False
                continue

            expected = normalize_text(checked_in_summary.read_text(encoding="utf-8"))
            actual = normalize_text(rendered_summary.read_text(encoding="utf-8"))

            if expected != actual:
                print(
                    f"FAIL rendered summary drift: {checked_in_summary.relative_to(REPO_ROOT)}",
                    file=sys.stderr,
                )
                diff = difflib.unified_diff(
                    expected.splitlines(),
                    actual.splitlines(),
                    fromfile=str(checked_in_summary.relative_to(REPO_ROOT)),
                    tofile=f"rendered:{checked_in_summary.relative_to(REPO_ROOT)}",
                    lineterm="",
                )
                for line in diff:
                    print(line, file=sys.stderr)
                success = False
            else:
                print(f"PASS rendered summary matches: {checked_in_summary.relative_to(REPO_ROOT)}")

    return success


def normalize_text(value: str) -> str:
    return value.replace("\r\n", "\n").rstrip() + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
