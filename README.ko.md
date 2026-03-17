[English](README.md) | 한국어

# Mimir-Skills

로컬 파일을 읽는 AI coding agent를 위한 skill-first workflow guidance, playbook, validator 모음입니다.

`Mimir-Skills`는 로컬 파일 기반 AI coding agent를 위한 skill-first 저장소로 현재 baseline이 정리된 상태입니다.
방향은 단순합니다. workflow 판단 규칙, safety constraint, output pattern을 `SKILL.md`와 companion reference에 담아 에이전트가 직접 읽게 하고, Python 코드는 결정론적 검증과 얇은 로컬 수집 helper에만 남기자는 것입니다.

## 누구를 위한 것인가

- 대략 2명에서 8명 규모의 작은 소프트웨어 팀
- GitHub pull-request 기반 흐름으로 일하는 팀
- 일상적인 엔지니어링 작업에서 이미 AI coding agent를 사용하는 팀

또한 세션, 브랜치, 리뷰 사이에서 더 나은 연속성을 원하는, AI coding agent를 매일 사용하는 개인 개발자에게도 도움이 되도록 설계되고 있습니다.

## v1이 하도록 만들고 있는 일

- `prepare-handoff`: 로컬 파일 기반 에이전트가 무엇이 바뀌었고 무엇이 남았으며 어디서 이어야 하는지 설명하는 handoff 패턴을 따르게 합니다
- `write-pr-rationale`: 로컬 파일 기반 에이전트가 무엇이 바뀌었고 왜 바뀌었으며 무엇이 검증되었는지 설명하는 reviewer-facing 패턴을 따르게 합니다
- `capture-ci-investigation`: 로컬 파일 기반 에이전트가 불확실성을 숨기지 않고 bounded CI investigation 패턴을 따르게 합니다

## 왜 필요한가

AI coding agent는 이미 코드를 수정하고, 테스트를 실행하고, CI를 확인하고, pull request를 준비할 수 있습니다.
그런데 팀이 여전히 잃어버리는 것은 그 작업을 둘러싼 맥락입니다.

- 왜 이 경로를 선택했는가
- 실제로 무엇이 바뀌었는가
- 무엇이 근거였는가
- 무엇이 아직 위험하거나 불확실한가
- 다음 에이전트나 리뷰어가 이어가기 전에 무엇을 알아야 하는가

`Mimir-Skills`는 그 맥락을 보존하는 비용을 낮추기 위해 존재합니다.

## 품질 경계

이 저장소는 강한 초안을 생성하는 데 도움을 줘야지, engineering judgment를 대체하는 것처럼 보여서는 안 됩니다.

- output은 final truth가 아니라 draft입니다
- 외부 공유 전에는 여전히 human review가 필요합니다
- CI 지원은 best-effort이며, 사용 가능한 log와 context에 좌우됩니다
- 자동화는 bounded되고 review 가능해야 하며, 명시적 근거 기반 record보다 앞서면 안 됩니다

## 현재 상태

이 저장소는 이제 current skill-first baseline 위에서 운영되고 있습니다.
공개 가치의 중심은 `SKILL.md`, reference, example, schema, deterministic validator에 있고, 로컬 Python helper는 여전히 존재하지만 이제는 skill 문서보다 앞에 오는 주인공이 아닙니다.

현재 제공되는 것:

- 공개 project one-pager
- `skills/prepare-handoff/`, `skills/write-pr-rationale/`, 더 좁은 beta인 `skills/capture-ci-investigation/` 아래의 user-facing workflow skill
- `decision-core`, `decision-capture`, `handoff-context`, `pr-rationale`, `ci-rationale`, `dependency-upgrade-decision`, `memory-promote` 같은 internal support skill
- 명령형 helper가 필요할 때 사용할 수 있는 `mimir_skills/`와 `skills/*/scripts/` 아래의 로컬 helper surface
- `adapters/codex/scripts/install_codex_skills.py`와 `docs/codex-local-install.md`로 제공되는 첫 Codex 전용 로컬 install path. 다만 이제는 main public path가 아니라 optional thin-adapter proof point로 본다
- Claude Code, OpenAI / Codex 및 GPT-facing coding-agent surface, Gemini CLI, Qwen Code에 대한 공개 support-level 정의와 `shared CLI support`, `documented support`, `thin adapter support` 구분
- shared CLI run과 남아 있을 future adapter가 함께 참조할 compact always-loaded rules baseline
- 공통 glossary
- trigger, decision record, memory promotion을 위한 v0.1 spec과, decision record 및 memory artifact를 위한 machine-readable companion schema
- CI, dependency/config, memory-promotion 흐름을 위한 public-safe end-to-end example
- replay, reviewer comprehension, memory promotion을 위한 evaluation prompt
- schema-helper 일관성 체크, example 검증, 공개 memory artifact 검증, 파생 summary drift 체크를 위한 최소 CI
- 루트 README와 `docs/` 아래의 소수 입구/개요 문서(`project-one-pager`, `quick-start`, `glossary`)에 대한 한국어 동반 문서

다음 단계:

- current skill-first baseline을 유지하고, 의미 있는 workflow-surface 변경 뒤에는 lightweight staleness review를 다시 실행하기
- workflow routing은 public trigger table을 기준으로 유지하고, workflow 수나 ambiguity가 실제로 커지기 전에는 machine-readable routing을 만들지 않기
- 결정론적 validator와 example verification은 안정적으로 유지하되, 더 큰 workflow runtime으로 되돌아가지 않기
- 지금은 다른 agent-specific adapter를 추가하지 않고, current skill-first baseline을 넘는 분명한 UX 이득이 반복 관찰될 때만 adapter 확장을 다시 검토하기
- `write-pr-rationale`는 explicit `why`가 없을 때의 한계를 계속 정직하게 드러내고, `capture-ci-investigation`은 repeated real usage가 더 넓은 surface를 정당화하기 전까지 narrow + wrapper-only 상태를 유지하기

## 문서 안내

- [Project One-Pager](docs/project-one-pager.ko.md)
- [Glossary](docs/glossary.ko.md)
- [Always-Loaded Rules (English)](docs/always-loaded-rules.md)
- [Quick Start](docs/quick-start.ko.md)
- [Codex Local Install (English)](docs/codex-local-install.md)
- [Agent Support Levels (English)](docs/agent-support-levels.md)
- [Adapter Feedback Loop (English)](docs/adapter-feedback-loop.md)
- [Workflow Surface (English)](docs/workflow-surface.md)
- [Trigger Taxonomy v0.1](spec/trigger-taxonomy.md)
- [Decision Record Schema v0.1](spec/decision-record-schema.md)
- [Memory Promotion Policy v0.1](spec/memory-promotion-policy.md)
- [Security Policy](SECURITY.md)
- [Contributing Guide](CONTRIBUTING.md)
- [License](LICENSE)

## 저장소 구조

```text
Mimir-Skills/
  README.md
  README.ko.md
  docs/
  skills/
  spec/
  examples/
  evaluations/
  scripts/
  template/
  mimir_skills/
  adapters/
```

기본 public surface:

- `skills/`
- `docs/`
- `spec/`
- `examples/`

보조 helper surface:

- `scripts/`
- `mimir_skills/`
- `adapters/`

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
- 한국어 파일은 루트 README와 `docs/` 아래의 소수 입구/개요 문서(`project-one-pager`, `quick-start`, `glossary`)에 대해서만 유지합니다.
- 상세 workflow 문서, helper 문서, skill, reference, evaluation, contributor workflow 파일, 로컬 planning 메모는 영어를 기준으로 유지합니다.
- 공개 기술 스펙, skill, example, evaluation, contributor workflow 파일은 영어만 유지합니다.
- JSON 키, schema 이름, file path는 두 언어 모두 영어를 유지합니다.

## 시작 자산

- [Skill Template](template/SKILL.md)
- [Skills 디렉터리 안내](skills/README.md)
- [Workflow Surface (English)](docs/workflow-surface.md)
- [Examples 디렉터리 안내](examples/README.md)
- [Evaluations 디렉터리 안내](evaluations/README.md)
- [Contributing Guide](CONTRIBUTING.md)
- `.github/workflows/ci.yml`의 GitHub Actions CI

## 단기 목표

로컬 파일 기반 에이전트가 skill을 직접 읽어 사용할 수 있는 신뢰할 만한 public v1 방향을 만들고, 결정론적 validator와 얇은 로컬 helper는 그 아래의 보조 수단으로 유지하는 것입니다.
