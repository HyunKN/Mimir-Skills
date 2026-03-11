[English](trigger-taxonomy.md) | 한국어

# Trigger Taxonomy v0.1

## 목적

이 taxonomy는 언제 workflow가 decision record를 만들어야 하고 언제 조용히 지나가야 하는지를 정의한다.
목표는 저장소를 시끄러운 활동 로그로 만들지 않으면서도 고가치 결정을 포착하는 것이다.

## 기본 규칙

다음 조건이 모두 참이면 decision record를 만든다.

- 그 선택이 동작, 위험, 공유 인터페이스, 운영, 이후 작업에 영향을 준다
- 그 선택이 의미 있는 대안들 사이의 판단을 필요로 했다
- 그 선택을 evidence reference로 뒷받침할 수 있다

이 조건이 성립하지 않으면 standalone record를 만들지 않는다.

## 기록 대상 범주

| Category | Record when | Typical examples |
| --- | --- | --- |
| Architecture and interfaces | 공유 설계나 계약이 바뀔 때 | API shape 변경, schema version 변경, 모듈 경계 리팩터링 |
| Dependencies, config, and security | 의존성, 권한, secret 처리 규칙, 배포 설정이 위험이나 동작을 바꿀 때 | package 추가/제거, CI 권한 변경, runtime config 변경 |
| CI, build, and test strategy | 프로젝트의 검증 또는 배포 방식을 바꾸는 workflow 변경일 때 | 테스트 전략 변경, 빌드 파이프라인 수정, 근거가 있는 flake workaround |
| Root cause and remediation | 실패 원인을 진단하고 해결 경로를 선택했을 때 | CI 실패 분석, production bug 분석, rollback 결정 |
| Workflow boundary and handoff | 지속 가능한 이어받기 맥락이 필요한 작업 경계일 때 | handoff note, 중단된 migration, 부분 rollout 요약 |
| Memory promotion signals | 반복적으로 등장한 교훈이 한 번의 작업을 넘어 재사용 가능해 보일 때 | 프로젝트 규칙 candidate, 반복되는 환경 제약 |

## 보통 기록하지 않는 것

다음 항목에는 standalone decision record를 만들지 않는다.

- 포맷팅만 바뀐 수정
- 공유 영향이 없는 사소한 로컬 리팩터링
- 해석이 없는 원시 명령 출력
- 근거가 없는 추측 메모
- 이미 최신 record가 다루고 있는 중복 메모

## Trigger가 발생했을 때 최소 필수 출력

trigger가 유효하다면 record에는 최소한 다음이 있어야 한다.

- `decision`
- `selected_option`
- `rationale`
- `evidence_refs`
- `affected_paths`
- `confidence`

## 기록을 우선해야 하는 신호

다음 중 하나라도 참이면 작은 결정이라도 기록을 우선한다.

- 인증, 권한, secret, permission을 건드린다
- 공유 계약이나 생성 산출물을 바꾼다
- 실패 원인 진단이 나중에 다시 참조될 가능성이 높다
- 작업이 사람, 세션, 에이전트 사이에서 handoff될 예정이다

## 리뷰 가이드

애매할 때는 다음을 묻는다.

1. 이 근거가 없으면 미래의 에이전트가 시간을 잃거나 실수할까?
2. 코드 리뷰에서 이 결정이 질문받을 가능성이 높은가?
3. 이 주장을 파일, 테스트, 로그, diff, 이슈로 뒷받침할 수 있는가?

세 질문 중 두 개 이상이 yes면 record를 만든다.
