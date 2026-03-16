from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


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
