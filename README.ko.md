[English](README.md) | 한국어

# decision-skills

AI 에이전트의 엔지니어링 결정을 추적 가능하고, 재사용 가능하며, 리뷰 가능한 형태로 만들기 위한 오픈 스킬과 레퍼런스 문서 모음입니다.

## 왜 필요한가

AI 코딩 에이전트는 이미 코드를 수정하고, 테스트를 실행하고, CI를 확인하고, PR을 준비할 수 있습니다.
그런데 팀이 여전히 잃어버리는 것은 그 작업을 둘러싼 결정 맥락입니다.

- 왜 이 경로를 선택했는가
- 어떤 대안을 검토했는가
- 무엇이 근거였는가
- 무엇이 아직 위험하거나 불확실한가
- 다음 에이전트가 이어서 작업하기 전에 무엇을 알아야 하는가

`decision-skills`는 바로 그 공백에 집중합니다.

## 핵심 원칙

- Decision traceability 우선
- AI-readable canonical record 우선
- 같은 원본에서 파생되는 human-readable summary
- 파생되고 검증된 계층으로서의 long-term memory
- 공개 재사용을 위한 skills 스타일 저장소 구조

## 안전성 안내

`decision-skills`는 기본적으로 결정 기록 도구입니다. 일관성과 안전성을 높이는 범위에서 제한적인 script나 hook을 포함할 수 있지만, 자동화는 항상 보조적이어야 하며 명시적 근거 기반 record보다 앞서면 안 됩니다.

## 현재 상태

이 저장소는 문서 우선 공개형 v0.1 단계에 있습니다.

현재 제공되는 것:

- 공개용 project one-pager
- 공통 glossary
- trigger, decision record, memory promotion에 대한 v0.1 spec
- 시작용 skill template와 `decision-core`, `decision-capture`, `dependency-upgrade-decision`, `ci-rationale`, `handoff-context`, `pr-rationale`, `memory-promote`
- CI, dependency/config, memory-promotion 흐름을 다루는 공개용 end-to-end example
- replay, reviewer comprehension, memory promotion을 위한 evaluation prompt
- example 검증, 공개 memory artifact 검증, 파생 summary drift 체크를 위한 최소 CI
- 루트 README와 `docs/`에 대한 한국어 동반 문서

다음 단계:

- 더 많은 사용 피드백 이후의 좁은 hook 또는 guardrail 결정
- 이후의 evaluation automation과, 실제로 유용함이 확인된 추가 workflow-specific skill
- 공개 memory artifact에도 machine-readable schema가 필요한지 판단

## 문서 안내

- [Project One-Pager](docs/project-one-pager.ko.md)
- [Glossary](docs/glossary.ko.md)
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

사용자 저장소 안에서 의도하는 런타임 산출물 구조는 다음과 같습니다.

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
- 의미 기준 원문은 영어 문서입니다.
- 한국어 문서는 루트 README와 `docs/` 아래 문서에 한해 같은 구조로 `*.ko.md` 이름을 사용합니다.
- 로컬 `.workspace/` 문서는 한글 미러를 둘 수 있지만 gitignore 대상이며 공개 저장소 표면에는 포함되지 않습니다.
- 공개 기술 스펙, skill, example, evaluation, contributor workflow 문서는 영어만 유지합니다.
- JSON 키, 스키마 이름, 파일 경로는 두 언어 모두 영어를 유지합니다.

## 시작 자산

- [Skill Template](template/SKILL.md)
- [Skills 디렉터리 안내](skills/README.md)
- [Examples 디렉터리 안내](examples/README.md)
- [Evaluations 디렉터리 안내](evaluations/README.md)
- [Contributing Guide](CONTRIBUTING.md)
- `.github/workflows/ci.yml`의 GitHub Actions CI

## 단기 목표

기여자가 문제 정의를 이해하고, 스키마를 검토하고, 첫 스킬과 example을 안정적인 문서 기반 위에서 만들 수 있는 작지만 신뢰할 수 있는 공개 v0.1을 만드는 것입니다.
