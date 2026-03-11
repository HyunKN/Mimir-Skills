English | [한국어](decision-record-schema.ko.md)

# Decision Record Schema v0.1

## Purpose

This document defines the canonical machine-readable format for one high-impact decision.
In v0.1, one decision record maps to one JSON file.

Companion files:

- Human-readable specification: this document
- Machine-readable schema: `decision-record-schema.json`

## Storage Contract

- Directory: `.ai/records/decisions/`
- File format: UTF-8 JSON
- File naming: `<id>.json`
- Canonical source: the JSON record
- Human view: derived Markdown summaries in `.ai/records/reports/` or other render outputs

## Identifier and Timestamp Rules

- `id` should use the pattern `dec-YYYYMMDD-<slug>-NNN`
- `YYYYMMDD` should represent a valid calendar date
- `timestamp` must be ISO 8601 in UTC
- IDs should remain stable once written

## Required Fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Stable decision identifier |
| `timestamp` | string | UTC timestamp for record creation |
| `task_ref` | object | Reference to the originating task or workflow boundary |
| `decision` | string | Short statement of the decision being made |
| `selected_option` | object | The option chosen and its brief summary |
| `rationale` | string | Why the selected option was chosen |
| `evidence_refs` | array | One or more structured evidence references |
| `affected_paths` | array | Relative file paths touched or affected by the decision |
| `confidence` | number | Numeric score from `0.0` to `1.0` |

### `task_ref`

```json
{
  "source": "issue|pr|thread|ci|local|other",
  "id": "string",
  "title": "string"
}
```

### `selected_option`

```json
{
  "name": "string",
  "summary": "string"
}
```

## Optional Fields

| Field | Type | Description |
| --- | --- | --- |
| `problem_context` | string | Context explaining the problem or constraint |
| `alternatives_considered` | array | Alternatives reviewed during the decision |
| `validation_run` | array | Validation attempts or checks performed |
| `remaining_risks` | array | Risks, caveats, or unknowns that remain |
| `follow_up` | array | Next steps still required |
| `supersedes` | array | Prior decision IDs replaced or updated by this record |

### `alternatives_considered[]`

```json
{
  "name": "string",
  "status": "rejected|deferred|selected",
  "reason": "string"
}
```

### `evidence_refs[]`

```json
{
  "kind": "file|diff|test|ci|doc|issue|command|discussion|other",
  "ref": "string",
  "summary": "string",
  "captured_at": "2026-03-11T10:30:00Z"
}
```

### `validation_run[]`

```json
{
  "type": "test|build|lint|manual|other",
  "command": "string",
  "result": "passed|failed|partial|not_run",
  "summary": "string"
}
```

## Behavioral Rules

- `evidence_refs` must not be empty.
- `affected_paths` should contain repo-relative paths. Use an empty array only when no file path applies.
- `confidence` describes the quality of the conclusion at write time, not a permanent truth claim.
- Unknown fields may be added by future versions, and readers should ignore fields they do not understand.
- Markdown summaries must not introduce claims that are absent from the JSON source.
- The companion JSON Schema is intended for structural validation; helper validators may enforce additional semantic checks such as calendar-valid IDs or UTC-only timestamps.

## Example Record

```json
{
  "id": "dec-20260311-ci-timeout-001",
  "timestamp": "2026-03-11T10:30:00Z",
  "task_ref": {
    "source": "ci",
    "id": "build-1824",
    "title": "Fix failing Windows test job"
  },
  "decision": "Increase the Windows integration test timeout and keep the retry count unchanged.",
  "problem_context": "The Windows integration suite started failing after asset extraction time increased by about 40 seconds.",
  "alternatives_considered": [
    {
      "name": "Raise retries",
      "status": "rejected",
      "reason": "Would hide the timeout root cause and lengthen successful runs."
    },
    {
      "name": "Increase timeout threshold",
      "status": "selected",
      "reason": "Matches observed extraction time and preserves failure visibility."
    }
  ],
  "selected_option": {
    "name": "Increase timeout threshold",
    "summary": "Extend the timeout from 120s to 180s without changing retry behavior."
  },
  "rationale": "The failures were caused by slower setup time rather than flakiness in the tests themselves.",
  "evidence_refs": [
    {
      "kind": "ci",
      "ref": "build-1824/windows-integration",
      "summary": "Three consecutive failures timed out during the setup stage.",
      "captured_at": "2026-03-11T10:08:00Z"
    },
    {
      "kind": "file",
      "ref": ".github/workflows/test.yml",
      "summary": "Timeout was configured at 120 seconds for the integration step.",
      "captured_at": "2026-03-11T10:12:00Z"
    }
  ],
  "affected_paths": [
    ".github/workflows/test.yml"
  ],
  "validation_run": [
    {
      "type": "test",
      "command": "pnpm test:integration:windows",
      "result": "passed",
      "summary": "The workflow completed once with the new timeout."
    }
  ],
  "remaining_risks": [
    "If setup time continues to grow, the timeout may need to be revisited."
  ],
  "confidence": 0.82,
  "follow_up": [
    "Track setup duration for the next five CI runs."
  ],
  "supersedes": []
}
```
