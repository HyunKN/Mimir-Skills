[English](README.md) | 한국어

# decision-skills

로컬 프로젝트 상태를 바탕으로 handoff, PR rationale, CI investigation context 초안을 생성합니다.

`decision-skills`는 AI coding agent를 위한 output-first workflow skill pack으로 전환 중입니다.
제품 방향은 단순합니다. skill이 로컬 signal을 읽고 첫 번째로 유용한 버전을 초안으로 만들 수 있다면, 엔지니어링 맥락을 손으로 다시 구성하는 일을 멈추자는 것입니다.

## 누구를 위한 것인가

- 대략 2명에서 8명 규모의 작은 소프트웨어 팀
- GitHub pull-request 기반 흐름으로 일하는 팀
- 일상적인 엔지니어링 작업에서 이미 AI coding agent를 사용하는 팀

또한 세션, 브랜치, 리뷰 사이에서 더 나은 연속성을 원하는, AI coding agent를 매일 사용하는 개인 개발자에게도 도움이 되도록 설계되고 있습니다.

## v1이 하도록 만들고 있는 일

- `prepare-handoff`: 현재 브랜치 context를 읽고 무엇이 바뀌었는지, 무엇이 남았는지, 어디서 이어야 하는지를 설명하는 handoff 초안을 만듭니다
- `write-pr-rationale`: 브랜치 diff와 validation context를 읽고 왜 이 변경이 일어났는지를 설명하는 reviewer-facing 설명 초안을 만듭니다
- `capture-ci-investigation`: 사용 가능한 실패 맥락에서 bounded CI investigation summary 초안을 만들되, 완벽한 root-cause analysis는 약속하지 않습니다

## 왜 필요한가

AI coding agent는 이미 코드를 수정하고, 테스트를 실행하고, CI를 확인하고, pull request를 준비할 수 있습니다.
그런데 팀이 여전히 잃어버리는 것은 그 작업을 둘러싼 맥락입니다.

- 왜 이 경로를 선택했는가
- 실제로 무엇이 바뀌었는가
- 무엇이 근거였는가
- 무엇이 아직 위험하거나 불확실한가
- 다음 에이전트나 리뷰어가 이어가기 전에 무엇을 알아야 하는가

`decision-skills`는 그 맥락을 보존하는 비용을 낮추기 위해 존재합니다.

## 품질 경계

이 저장소는 강한 초안을 생성하는 데 도움을 줘야지, engineering judgment를 대체하는 것처럼 보여서는 안 됩니다.

- output은 final truth가 아니라 draft입니다
- 외부 공유 전에는 여전히 human review가 필요합니다
- CI 지원은 best-effort이며, 사용 가능한 log와 context에 좌우됩니다
- 자동화는 bounded되고 review 가능해야 하며, 명시적 근거 기반 record보다 앞서면 안 됩니다

## 현재 상태

이 저장소는 오늘 시점에도 여전히 문서 우선 공개형 v0.1 단계에 있습니다.
위의 output-first 방향은 현재 내부 엔진 위에 다음으로 쌓아 올리고 있는 레이어입니다.

현재 제공되는 것:

- 공개 project one-pager
- 공통 glossary
- trigger, decision record, memory promotion을 위한 v0.1 spec과, decision record 및 memory artifact를 위한 machine-readable companion schema
- `decision-core`, `decision-capture`, `dependency-upgrade-decision`, `ci-rationale`, `handoff-context`, `pr-rationale`, `memory-promote`, 그리고 public workflow wrapper인 `prepare-handoff`, `write-pr-rationale`, 더 좁은 beta인 `capture-ci-investigation`을 포함한 시작용 skill template
- CI, dependency/config, memory-promotion 흐름을 위한 public-safe end-to-end example
- replay, reviewer comprehension, memory promotion을 위한 evaluation prompt
- schema-helper 일관성 체크, example 검증, 공개 memory artifact 검증, 파생 summary drift 체크를 위한 최소 CI
- 루트 README와 `docs/`에 대한 한국어 동반 문서, 그리고 공개 저장소 표면 밖의 미러링된 로컬 workspace 메모

다음 단계:

- `prepare-handoff`, `write-pr-rationale`, `capture-ci-investigation` 중심의 공개 skill surface 구현을 계속 진행
- 더 나은 output shape, 선택적 evidence 입력, 실제 사용 피드백을 통해 `prepare-handoff`와 `write-pr-rationale`를 더 다듬기
- 더 강한 example과 reliability boundary가 direct-use script layer를 정당화할 때까지 `capture-ci-investigation`은 더 좁고 best-effort로 유지

## 문서 안내

- [Project One-Pager](docs/project-one-pager.ko.md)
- [Glossary](docs/glossary.ko.md)
- [Workflow Surface](docs/workflow-surface.ko.md)
- [Trigger Taxonomy v0.1](spec/trigger-taxonomy.md)
- [Decision Record Schema v0.1](spec/decision-record-schema.md)
- [Memory Promotion Policy v0.1](spec/memory-promotion-policy.md)
- [Security Policy](SECURITY.md)
- [Contributing Guide](CONTRIBUTING.md)
- [License](LICENSE)

## 저장소 구조

```text
decision-skills/
  README.md
  README.ko.md
  docs/
  spec/
  template/
  skills/
  examples/
  evaluations/
```

사용자 저장소 내부에서 의도하는 runtime artifact 구조는 다음과 같습니다.

```text
.ai/
  records/
    decisions/
    memories/
      candidates/
      validated/
    plans/
    reports/
```

## 언어 운영 정책

- GitHub 기본 진입점은 `README.md`입니다.
- 의미 기준 source of truth는 영어 파일입니다.
- 한국어 파일은 영어 원문과 나란히 `*.ko.md` 형식으로, 루트 README와 `docs/` 아래 파일에 대해서만 유지합니다.
- 로컬 `.workspace/` 메모도 한국어로 미러링할 수 있지만, gitignore 대상이며 공개 저장소 표면에는 포함되지 않습니다.
- 공개 기술 스펙, skill, example, evaluation, contributor workflow 파일은 영어만 유지합니다.
- JSON 키, schema 이름, file path는 두 언어 모두 영어를 유지합니다.

## 시작 자산

- [Skill Template](template/SKILL.md)
- [Skills 디렉터리 안내](skills/README.md)
- [Workflow Surface](docs/workflow-surface.ko.md)
- [Examples 디렉터리 안내](examples/README.md)
- [Evaluations 디렉터리 안내](evaluations/README.md)
- [Contributing Guide](CONTRIBUTING.md)
- `.github/workflows/ci.yml`의 GitHub Actions CI

## 단기 목표

현재의 문서, schema, validation 기반을 그 아래에 그대로 유지하면서도, 팀이 즉시 workflow 가치를 느낄 수 있는 신뢰할 만한 public v1 방향을 만드는 것입니다.
