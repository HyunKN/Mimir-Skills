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
SCHEMA_PATH = REPO_ROOT / "spec" / "decision-record-schema.json"
VALIDATOR_PATH = REPO_ROOT / "skills" / "decision-core" / "scripts" / "validate_decision_record.py"
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

    if not check_rendered_summaries(records):
        return 2

    print(f"\nVerified {len(records)} example decision record(s) and their derived summaries.")
    return 0


def check_schema_json() -> bool:
    try:
        json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"FAIL missing machine-readable schema: {SCHEMA_PATH}", file=sys.stderr)
        return False
    except json.JSONDecodeError as exc:
        print(
            f"FAIL invalid machine-readable schema: {SCHEMA_PATH} "
            f"({exc.msg} at line {exc.lineno}, column {exc.colno})",
            file=sys.stderr,
        )
        return False

    print(f"PASS machine-readable schema parses: {SCHEMA_PATH.relative_to(REPO_ROOT)}")
    return True


def run_validator(records: list[Path]) -> bool:
    command = [sys.executable, str(VALIDATOR_PATH), *[str(path) for path in records]]
    result = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, check=False)

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")

    return result.returncode == 0


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
