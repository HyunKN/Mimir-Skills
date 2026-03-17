[English](project-one-pager.md) | 한국어

# Project One-Pager

## `Mimir-Skills`란 무엇인가

`Mimir-Skills`는 AI 에이전트의 decision traceability를 위한 skill-first 저장소다.

이 프로젝트는 단순히 무엇이 바뀌었는지가 아니라, 의미 있는 엔지니어링 변화가 왜 일어났는지를 남기도록 돕고, 로컬 파일을 읽는 에이전트가 재사용 가능한 workflow skill, playbook, example, deterministic validator를 직접 참조하도록 만든다.

## 문제 정의

현대의 코딩 에이전트는 로그, diff, 테스트 출력은 남길 수 있다.
하지만 그런 산출물만으로는 운영 맥락 전체를 담기 어렵다.

- 어떤 결정을 내렸는가
- 어떤 대안을 기각했는가
- 어떤 증거를 참고했는가
- 어떤 검증을 수행했는가
- 어떤 위험이 남아 있는가
- 다음 에이전트나 엔지니어가 이어가기 위해 무엇을 알아야 하는가

이 때문에 활동 로그와 재사용 가능한 결정 맥락 사이에 공백이 생긴다.

## 제품 논지

이 프로젝트는 여섯 가지 주장 위에 서 있다.

1. 로그만으로는 충분하지 않다.
2. 영향도가 높은 결정은 구조화된 형태로 기록해야 한다.
3. canonical record는 먼저 AI가 읽기 쉬워야 한다.
4. 사람용 요약은 같은 원본에서 렌더링되어야 한다.
5. 장기 메모리는 직접 쓰는 것이 아니라 검증된 기록에서 승격되어야 한다.
6. 로컬 파일 기반 에이전트가 직접 읽을 수 있다면 workflow 판단 규칙은 `SKILL.md`와 reference에 살아야 하며, 코드는 결정론적 검증이나 얇은 수집 helper에만 남아야 한다.

## 공개 v0.1에 포함되는 것

- 영문 중심 공개 문서와, 루트 README 및 `docs/` 아래의 소수 입구/개요 문서에 대한 한국어 동반 문서
- `skills/` 아래의 skill-first workflow package
- 공통 용어를 위한 glossary
- 무엇을 기록할지 정하는 trigger taxonomy
- canonical decision record schema
- memory promotion policy
- public-safe example과 evaluation
- schema, example, memory artifact를 위한 deterministic validation helper
- `mimir_skills/`와 `skills/*/scripts/` 아래의 optional local helper surface

## 아직 포함하지 않는 것

- 호스팅 서비스나 중앙 조정 계층
- 모든 관찰을 자동으로 메모리로 승격하는 기능
- 모든 에이전트 플랫폼에 대한 adapter coverage
- hidden reasoning이나 안전하지 않은 비공개 정보 저장
- 판단을 skill 문서 대신 런타임이 떠맡는 큰 workflow engine

## 초기 사용 사례

- 근거와 검증 결과를 남기는 CI 실패 분석
- 지속 가능한 handoff 맥락이 필요한 다중 파일 리팩터링
- machine-readable record에서 렌더링하는 PR용 요약
- 반복 검증 이후에만 만들어지는 프로젝트 메모리

## 왜 이중 언어 저장소인가

- GitHub에는 글로벌 독자를 위한 명확한 기본 진입점이 필요하다.
- 한국어 동반 문서는 루트 README와 `docs/` 아래의 소수 입구/개요 문서(`project-one-pager`, `quick-start`, `glossary`)에만 유지한다.
- 상세 문서, 스펙, 스키마, skill, evaluation, 이후 패키징 일관성은 영어 기준 원문으로 유지한다.

## 단기 로드맵

1. skill-first baseline을 안정적으로 유지하고, 의미 있는 workflow-surface 변경 뒤에는 lightweight staleness review를 다시 돌린다.
2. 핵심 workflow는 계속 `SKILL.md`와 reference를 중심으로 유지하고, 결정론적 helper는 validator와 thin collector 정도로 제한한다.
3. 결정론적 validator와 example verification은 안정적으로 유지하되, 더 큰 workflow runtime으로 되돌아가지 않는다.
4. adapter path는 main product story가 아니라 optional proof point로 취급하고, expansion work는 기본적으로 자동으로 열지 않는다.
5. broader helper나 adapter 확장은 반복된 usage evidence가 있을 때만 다시 검토하며, `capture-ci-investigation`은 분명한 UX 이득이 나오기 전까지 wrapper-only by design으로 유지한다.

## 성공 기준

새 기여자나 새 에이전트가 이 저장소를 열고 몇 개의 문서만 읽어도 바로 이해할 수 있어야 한다.

- 무엇을 기록해야 하는지
- 어떻게 저장해야 하는지
- 요약은 어떻게 파생되는지
- 메모리는 어떻게 안전하게 승격되는지
- 첫 스킬과 example을 어디에 추가해야 하는지
- 무엇이 primary skill guidance이고 무엇이 optional local helper인지
