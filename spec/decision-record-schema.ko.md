[English](decision-record-schema.md) | 한국어

# Decision Record Schema v0.1

## 목적

이 문서는 영향도가 높은 단일 결정을 위한 canonical machine-readable format을 정의한다.
v0.1에서는 decision record 하나가 JSON 파일 하나에 대응된다.

Companion files:

- human-readable specification: 이 문서
- machine-readable schema: `decision-record-schema.json`

## 저장 계약

- 디렉터리: `.ai/records/decisions/`
- 파일 형식: UTF-8 JSON
- 파일 이름: `<id>.json`
- canonical source: JSON record
- human view: `.ai/records/reports/` 또는 다른 렌더 출력으로 생성되는 Markdown summary

## 식별자와 시간 규칙

- `id`는 `dec-YYYYMMDD-<slug>-NNN` 패턴을 권장한다
- `YYYYMMDD`는 실제 달력 날짜여야 한다
- `timestamp`는 UTC 기준 ISO 8601이어야 한다
- 한 번 기록된 ID는 안정적으로 유지해야 한다

## 필수 필드

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | 안정적인 decision identifier |
| `timestamp` | string | record 생성 시점의 UTC timestamp |
| `task_ref` | object | 원래 작업 또는 workflow boundary에 대한 참조 |
| `decision` | string | 내려진 결정을 짧게 설명하는 문장 |
| `selected_option` | object | 선택한 옵션과 짧은 요약 |
| `rationale` | string | 왜 그 옵션을 선택했는지 |
| `evidence_refs` | array | 하나 이상의 구조화된 evidence reference |
| `affected_paths` | array | 이 결정이 영향을 준 상대 파일 경로들 |
| `confidence` | number | `0.0`에서 `1.0` 사이 점수 |

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

## 선택 필드

| Field | Type | Description |
| --- | --- | --- |
| `problem_context` | string | 문제나 제약을 설명하는 맥락 |
| `alternatives_considered` | array | 결정 과정에서 검토한 대안 |
| `validation_run` | array | 수행한 검증 또는 체크 |
| `remaining_risks` | array | 아직 남아 있는 위험, 주의점, 미확정 사항 |
| `follow_up` | array | 이후에 필요한 다음 작업 |
| `supersedes` | array | 이 record가 대체하거나 갱신하는 이전 decision ID |

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

## 동작 규칙

- `evidence_refs`는 비어 있으면 안 된다.
- `affected_paths`는 저장소 기준 상대 경로를 사용한다. 파일 경로가 전혀 없는 경우에만 빈 배열을 쓴다.
- `confidence`는 기록 시점의 결론 품질을 나타내며, 영구적인 진실 주장으로 해석하지 않는다.
- 이후 버전에서 알 수 없는 필드가 추가될 수 있으며, 소비자는 이해하지 못하는 필드를 무시해야 한다.
- Markdown summary는 JSON source에 없는 주장을 새로 만들면 안 된다.
- companion JSON Schema는 구조 검증을 위한 것이며, 달력상 유효한 ID나 UTC-only timestamp 같은 추가 의미 검증은 helper validator가 더 엄격하게 적용할 수 있다.

## 예시 Record

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
