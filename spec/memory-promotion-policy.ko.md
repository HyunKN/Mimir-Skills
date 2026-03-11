[English](memory-promotion-policy.md) | 한국어

# Memory Promotion Policy v0.1

## 목적

이 정책은 재사용 가능한 교훈이 decision record에서 제한된 프로젝트 memory로 어떻게 이동하는지 정의한다.
Memory는 파생 계층이며, 검증 없이 곧바로 진실처럼 취급하면 안 된다.

## 산출물 흐름

```text
decision record(s) -> memory candidate -> validated memory
```

- 공유 프로젝트 memory의 허용된 출처는 decision record뿐이다.
- v0.1에서 승격은 명시적 단계다. 자동이 아니다.
- 아래 게이트를 통과하지 못하면 candidate에 머물거나 버린다.

## 저장 위치

- Candidates: `.ai/records/memories/candidates/`
- Validated memory: `.ai/records/memories/validated/`

## Candidate 최소 계약

각 candidate는 다음을 포함해야 한다.

- `id`
- `statement`
- `scope`
- `source_decision_ids`
- `evidence_refs`
- `confidence`
- `created_at`
- `status`는 `candidate`

## Validated Memory 최소 계약

각 validated memory는 candidate 필드에 더해 다음을 포함해야 한다.

- `validated_at`
- `validation_basis`
- `last_validated_at`
- `freshness`
- `status`는 `validated`

`freshness`에는 변동 가능한 지식에 대한 만료일 또는 재검증 주기가 포함될 수 있다.

## 승격 게이트

다음 조건을 모두 통과할 때만 candidate를 승격한다.

1. Provenance: `source_decision_ids`로 하나 이상의 decision record를 인용한다.
2. Evidence: 요약 주장만이 아니라 이를 뒷받침하는 `evidence_refs`가 있다.
3. Reuse value: 단일 작업을 넘어 미래에도 도움이 될 가능성이 높다.
4. Current validity: 현재 저장소나 브랜치 상태에서 유효성을 확인했다.
5. Safety: secret, unsafe private reasoning, 불필요한 민감 정보를 노출하지 않는다.
6. Freshness: 오래될 수 있는 지식이라면 재검증 또는 만료 전략이 있다.

## 강등과 보관

validated memory는 다음 경우 candidate로 강등하거나 보관 해제해야 한다.

- 참조한 결정이 superseded 되었다
- 기반 코드, workflow, 환경이 실질적으로 바뀌었다
- 더 이상 시간 절약이나 위험 감소에 도움이 되지 않는다
- safety 분류가 바뀌었다

## 허용되는 Memory 형태

v0.1에서 지원하는 memory statement 예시는 다음과 같다.

- 안정적인 프로젝트 규칙
- 오래 유지되는 workflow 사실
- 반복적으로 검증된 환경 제약

v0.1에서 승격을 피해야 하는 것은 다음과 같다.

- 일회성 작업 메모
- 미래 가치가 없는 브랜치 한정 임시 workaround
- 검증되지 않은 개인 선호

## 리뷰 질문

승격 전에 다음을 묻는다.

1. 새 에이전트가 memory에서 원래 decision record까지 역추적할 수 있는가?
2. 그 주장을 뒷받침하는 evidence가 현재 저장소 상태와 여전히 맞는가?
3. 전체 decision log를 다시 늘어놓지 않아도 미래 작업에 도움이 되는가?
4. 이 memory를 미래 에이전트에게 노출해도 안전한가?

하나라도 no면 승격하지 않는다.
