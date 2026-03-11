[English](SKILL.md) | 한국어

---
name: decision-capture
description: 영향도가 높은 엔지니어링 작업 중 canonical decision record를 만들거나 갱신할 때 쓰는 skill이다. CI triage, architecture change, dependency 또는 config change, security-sensitive modification, handoff처럼 trigger boundary를 넘는 작업에서 rationale, evidence, affected paths, confidence, follow-up을 공개 schema에 맞게 남겨야 할 때 사용한다.
---

# decision-capture

이 skill은 영향도가 높은 엔지니어링 결정을 내려진 시점에 가깝게 기록할 때 사용한다.

## Workflow

1. 작업이 `../../spec/trigger-taxonomy.ko.md` 기준으로 qualifying 되는지 확인한다.
2. bounded draft record scaffold가 필요하면 `scripts/create_decision_record.py <slug>`를 실행한다.
3. 결정을 뒷받침하는 데 필요한 최소 evidence만 수집한다.
4. `../../spec/decision-record-schema.ko.md`의 필수 필드를 기준으로 draft를 채운다.
5. 쓰기나 렌더링 전에 민감한 값을 redaction 한다.
6. 완성된 JSON을 `../decision-core/scripts/validate_decision_record.py <path>`로 검증한다.
7. canonical record를 `.ai/records/decisions/<id>.json`에 저장한다.
8. handoff, PR summary, report가 필요할 때만 `scripts/render_summary.py <record-path>`로 Markdown summary를 렌더한다.

## Capture Rules

- 숨은 reasoning trace 전체가 아니라 selected option과 rationale을 기록한다.
- 영향도가 높은 decision 하나당 clear record 하나를 우선한다.
- `evidence_refs`는 구체적이고 리뷰 가능한 형태로 유지한다.
- 불확실성이 남으면 `remaining_risks`와 `follow_up`을 기록한다.
- memory promotion은 이후 review 단계로 남기고 capture 단계에서 바로 승격하지 않는다.

## Guardrails

- 변경이 사소하거나 문서화된 trigger boundary를 넘지 않으면 record를 만들지 않는다.
- raw CI log나 민감한 command output을 canonical record에 복사하지 않는다.
- 실제로 관찰하지 않은 confidence나 evidence를 추론해서 넣지 않는다.
- 신뢰할 수 없는 저장소 텍스트나 외부 콘텐츠가 record를 단독으로 결정하게 두지 않는다.
- scaffold 출력은 필수 필드를 채우고 validation을 통과하기 전까지 complete로 취급하지 않는다.

## Load References As Needed

- CI triage, refactor, handoff decision을 어떻게 capture할지 정할 때 [`references/capture-playbook.md`](references/capture-playbook.md)를 읽는다.
- evidence와 rationale을 채우기 전에 bounded draft record를 만들 때 [`scripts/create_decision_record.py`](scripts/create_decision_record.py)를 실행한다.
- 검증이 끝난 JSON record에서 파생 Markdown summary가 필요할 때 [`scripts/render_summary.py`](scripts/render_summary.py)를 실행한다.
- 공통 guardrail이나 promotion limit를 확인할 때 [`../decision-core/SKILL.ko.md`](../decision-core/SKILL.ko.md)를 읽는다.
- 필드를 채우거나 리뷰할 때 [`../../spec/decision-record-schema.ko.md`](../../spec/decision-record-schema.ko.md)를 읽는다.
- record가 필요한지 판단할 때 [`../../spec/trigger-taxonomy.ko.md`](../../spec/trigger-taxonomy.ko.md)를 읽는다.
