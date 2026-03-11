#!/usr/bin/env python3
"""Create draft decision record JSON files for decision-skills."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


SLUG_PATTERN = re.compile(r"[^a-z0-9]+")
TASK_SOURCES = {"issue", "pr", "thread", "ci", "local", "other"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a draft canonical decision record with bounded defaults."
    )
    parser.add_argument(
        "slug",
        help="Short identifier for the decision, for example 'ci-timeout' or 'schema-migration'.",
    )
    parser.add_argument(
        "--output-root",
        default=".ai/records/decisions",
        help="Directory where the draft JSON file should be written.",
    )
    parser.add_argument(
        "--task-source",
        default="local",
        choices=sorted(TASK_SOURCES),
        help="Originating task source for task_ref.source.",
    )
    parser.add_argument("--task-id", default="", help="Originating task identifier.")
    parser.add_argument("--task-title", default="", help="Originating task title.")
    parser.add_argument(
        "--sequence",
        type=int,
        help="Optional explicit numeric suffix. Defaults to the next available sequence for the date and slug.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the target file if it already exists.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    slug = normalize_slug(args.slug)
    if not slug:
        print("Slug must contain at least one ASCII letter or digit after normalization.", file=sys.stderr)
        return 1

    timestamp = datetime.now(timezone.utc).replace(microsecond=0)
    date_part = timestamp.strftime("%Y%m%d")
    output_root = Path(args.output_root)
    sequence = args.sequence or next_sequence(output_root, date_part, slug)
    record_id = f"dec-{date_part}-{slug}-{sequence:03d}"
    target = output_root / f"{record_id}.json"

    if target.exists() and not args.force:
        print(f"Refusing to overwrite existing file: {target}", file=sys.stderr)
        print("Pass --force to overwrite it.", file=sys.stderr)
        return 1

    target.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "id": record_id,
        "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
        "task_ref": {
            "source": args.task_source,
            "id": args.task_id,
            "title": args.task_title,
        },
        "decision": "",
        "selected_option": {
            "name": "",
            "summary": "",
        },
        "rationale": "",
        "evidence_refs": [],
        "affected_paths": [],
        "confidence": None,
        "alternatives_considered": [],
        "validation_run": [],
        "remaining_risks": [],
        "follow_up": [],
        "supersedes": [],
    }

    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"Created draft decision record: {target}")
    print("This draft is intentionally incomplete and should fail validation until you fill the required fields.")
    print(
        "Next steps: edit the file with evidence and rationale, then run "
        "`python skills/decision-core/scripts/validate_decision_record.py <path>`. "
        "Render Markdown only after validation passes."
    )
    return 0


def normalize_slug(value: str) -> str:
    lowered = value.strip().lower()
    collapsed = SLUG_PATTERN.sub("-", lowered).strip("-")
    return collapsed


def next_sequence(output_root: Path, date_part: str, slug: str) -> int:
    prefix = f"dec-{date_part}-{slug}-"
    highest = 0

    if not output_root.exists():
        return 1

    for candidate in output_root.glob(f"{prefix}*.json"):
        suffix = candidate.stem.removeprefix(prefix)
        if suffix.isdigit():
            highest = max(highest, int(suffix))
    return highest + 1


if __name__ == "__main__":
    raise SystemExit(main())
