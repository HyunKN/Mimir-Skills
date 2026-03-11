[English](glossary.md) | 한국어

# Glossary

## decision traceability

중요한 엔지니어링 선택이 왜 내려졌는지, 어떤 근거가 있었는지, 다음에 무엇을 해야 하는지를 다시 복원할 수 있는 능력.

## decision record

영향도가 높은 단일 결정을 위한 canonical machine-readable artifact. v0.1에서는 결정당 JSON 파일 1개로 정의한다.

## evidence reference

파일 경로, 테스트 실행, CI 로그, diff, 이슈, 명령 출력, 문서 같은 근거 자료를 가리키는 구조화된 포인터.

## rendered summary

하나 이상의 canonical record에서 파생된 사람이 읽는 Markdown view. 원문의 source of truth는 아니다.

## trigger

CI 수정, 아키텍처 변경, 의존성 업데이트, handoff 같은 record 생성을 정당화하는 워크플로 이벤트 또는 결정 경계.

## memory candidate

하나 이상의 decision record에서 추출되었지만 아직 장기 재사용 가능성이 검증되지 않은 재사용 교훈.

## validated memory

provenance, evidence, safety, freshness 검증을 통과해 승격된 memory entry.

## promotion

재사용 가능한 교훈을 candidate 상태에서 validated memory로 명시적으로 옮기는 행위.

## supersedes

더 새로운 decision record가 이전 결정을 대체하거나 갱신한다는 관계.

## runtime artifact root

생성된 산출물을 저장하는 프로젝트 로컬 디렉터리. 이 저장소에서는 `.ai/records/`를 목표 경로로 둔다.

## confidence

기록 시점에서 해당 record나 결론이 얼마나 신뢰 가능한지에 대한 제한된 추정치. 스키마에서는 `0.0`에서 `1.0` 사이 숫자로 표현한다.
