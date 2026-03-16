[English](adapter-feedback-loop.md) | 한국어

# Adapter 피드백 루프

## 목적

이 문서는 `Mimir-Skills`의 현재 skill-first baseline과 선택적 helper/adapter surface 전반에서 실제 workflow 사용 경험을 어떻게 평가할지 정의한다.

목표는 무거운 telemetry를 넣는 것이 아니다.
작고 반복 가능한 feedback loop를 유지해서, workflow draft가 실제로 시간을 줄여주고 있는지 판단할 수 있게 하는 것이 목표다.

## 현재 범위

현재의 주 baseline은 skill-first workflow guidance와 얇은 local collector다.
선택적인 helper stub나 adapter path도 계속 관찰할 수 있지만, 더 이상 주된 제품 스토리는 아니다.

지금 우선적으로 볼 workflow는 다음과 같다:

- `prepare-handoff`
- `write-pr-rationale`
- `capture-ci-investigation`

## 핵심 성공 지표

작고 outcome-oriented한 지표 집합을 사용한다:

### 첫 번째로 유용한 Draft까지의 시간

workflow를 호출한 시점부터, 완전히 처음부터 쓰기보다 그 draft를 이어서 편집하는 편이 나을 정도의 첫 draft가 보일 때까지 얼마나 걸리는지 측정한다.

목표 방향:

- 수동 작성보다 마찰이 낮다고 느껴질 만큼 빨라야 한다

### Draft 유용성 비율

생성된 draft를 다음 네 bucket 중 하나로 분류한다:

- 그대로 사용 가능
- 가벼운 수정 후 사용 가능
- 큰 재작성이 있어야 사용 가능
- 폐기

목표 방향:

- 대부분의 draft가 앞의 두 bucket에 들어가야 한다

### 수동 편집 시간

draft를 실제 공유나 handoff에 쓸 수 있을 정도로 다듬는 데 얼마나 걸리는지 측정한다.

목표 방향:

- 같은 결과물을 수동으로 처음부터 쓰는 것보다 확실히 적은 시간이 걸려야 한다

### 반복 사용 여부

같은 사용자나 팀이 한 번 써본 뒤 비슷한 작업에서 같은 workflow를 다시 선택하는지 확인한다.

목표 방향:

- 단순히 한 번 신기해서가 아니라, 실제로 도움이 되기 때문에 다시 사용되어야 한다

## 가벼운 검토 질문

workflow를 사용한 뒤에는 다음 질문에 답한다:

1. 이 draft가 context를 다시 복원하는 일을 줄여주었는가?
2. 여전히 빠져 있던 중요한 context는 무엇이었는가?
3. 어떤 부분이 너무 generic하거나 과장되었는가?
4. 다음번에는 어떤 evidence나 local signal을 더 수집해야 하는가?
5. 같은 사용자가 비슷한 작업에서 이 workflow를 다시 고를 것인가?

## 권장 검토 기록 형식

다음 항목을 가진 짧은 수동 메모를 사용한다:

- 날짜
- 사용한 workflow
- 저장소 또는 작업 context
- 첫 번째로 유용한 draft까지의 시간
- usefulness bucket
- 수동 편집 시간
- 가장 크게 빠진 detail
- 가장 불필요했던 detail
- 다시 사용할 의사가 있는지

이 기록은 로컬 팀 메모, 비공개 evaluation log, 또는 나중에 재사용 가능한 case가 되면 public-safe example로 남길 수 있다.

## 구조화된 Observation Checklist

비교 목적의 observation pass를 실행하기 전에는, 최소한 아래를 기록하는 작은 checklist를 준비한다:

- 실행 날짜
- 테스트한 workflow
- 테스트한 execution surface:
  - skill-first reading only
  - local helper collector 또는 deprecation stub
  - optional adapter path
- 저장소와 작업 context
- 저장소 상태:
  - dirty 또는 clean
  - external clone 또는 현재 로컬 workspace
  - synthetic sample 또는 실제 로컬 작업
- 사용한 정확한 command
- output mode:
  - stdout
  - file write
  - 또는 둘 다
- 첫 useful draft까지의 시간
- usefulness bucket
- 예상 수동 편집 시간
- 같은 사용자가 이 workflow를 다시 사용할지 여부
- path, import, discovery, stdout surface 관련 마찰
- 실행 중 발견된 stale-doc 또는 stale-example mismatch

이 checklist는 가볍게 유지해야 한다.
목적은 다음 observation pass가 또 하나의 일회성 메모가 아니라, 이후 run과 비교 가능한 기록이 되게 하는 것이다.

## 무엇부터 개선할 것인가

지표가 약하면 다음 순서로 개선한다:

1. output shape와 section ordering
2. 빠진 local context 수집
3. workflow skill 내부의 domain knowledge
4. 더 명확한 uncertainty 처리
5. helper 또는 adapter 설치/invocation 마찰

## 아직 하지 말아야 할 것

- 무거운 analytics나 background telemetry를 추가하지 않는다
- 모든 agent surface를 한 번에 최적화하지 않는다
- 더 많은 metric을 모으기 위해 workflow 수를 늘리지 않는다
- 한 번의 성공 사례를 adapter 설계가 안정적이라는 증거로 취급하지 않는다

## Failure Mode와의 관계

이 feedback loop는 나중의 failure-mode tracking으로 이어져야 한다.

같은 약한 output pattern, stale reference 문제, missing context 문제가 반복되면 이를 failure mode로 기록하고, workflow, 문서, helper rule 중 무엇을 바꿔야 하는지 검토한다.

workflow surface가 바뀐 뒤에는 명시적인 stale-doc / stale-example 점검용으로 `../evaluations/staleness-review.md`를 함께 사용한다.
반복되는 패턴은 관련 없는 메모에 흩어 적지 말고 내부 `.workspace/failure-modes.md` tracker에 기록한다.
