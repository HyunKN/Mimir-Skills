[English](README.md) | 한국어

# Mimir-Skills

로컬 파일을 읽는 AI coding agent를 위한 skill-first workflow guidance, playbook, validator 모음입니다.

`Mimir-Skills`는 현재 skill-first baseline 위에서 운영됩니다.
핵심 방향은 단순합니다. workflow 판단 규칙, safety constraint, output pattern을 `SKILL.md`와 companion reference에 담아 에이전트가 직접 읽게 하고, Python 코드는 결정론적 검증과 얇은 로컬 수집 helper에만 남기는 것입니다.

## 왜 Mimir-Skills를 써야 하나

AI coding agent는 이미 코드를 수정하고, 테스트를 실행하고, CI를 확인하고, pull request를 준비할 수 있습니다.
그런데 팀이 여전히 잃어버리는 것은 그 작업을 둘러싼 맥락입니다.

- 왜 이 경로를 선택했는가
- 실제로 무엇이 바뀌었는가
- 무엇이 근거였는가
- 무엇이 아직 위험하거나 불확실한가
- 다음 에이전트나 리뷰어가 이어가기 전에 무엇을 알아야 하는가

`Mimir-Skills`는 이런 맥락을 보존하기 위한 재사용 가능한 workflow skill을 제공합니다.

- `prepare-handoff`
- `write-pr-rationale`
- `capture-ci-investigation`

잘 맞는 대상:

- 대략 2명에서 8명 규모의 작은 소프트웨어 팀
- GitHub pull-request 기반 흐름으로 일하는 팀
- 로컬 파일 기반 AI coding agent를 이미 일상적인 개발 흐름에 쓰고 있는 개발자나 팀

품질 경계:

- output은 final truth가 아니라 draft입니다
- 외부 공유 전에는 여전히 human review가 필요합니다
- CI 지원은 best-effort이며, 사용 가능한 log와 context에 좌우됩니다
- 자동화는 bounded되고 review 가능해야 하며, 명시적 근거 기반 record보다 앞서면 안 됩니다

## 빠른 시작

지금 `Mimir-Skills`를 쓰는 실용적인 경로는 세 가지입니다.
자세한 명령과 경로별 설명은 [Quick Start](docs/quick-start.ko.md)를 보면 됩니다.

### 1. Skill-First Reading (권장)

먼저 workflow `SKILL.md`를 직접 읽어 시작합니다.

- `skills/prepare-handoff/SKILL.md`
- `skills/write-pr-rationale/SKILL.md`
- `skills/capture-ci-investigation/SKILL.md`

로컬 파일을 직접 열 수 있는 agent라면 이 경로가 기본입니다.

### 2. Local Helpers

draft를 쓰기 전에 discovery나 structured context collection이 필요할 때 repository-root helper를 씁니다.

- `python -m mimir_skills list`
- `python skills/prepare-handoff/scripts/collect_git_context.py --repo . --output handoff-context.json`
- `python skills/write-pr-rationale/scripts/collect_pr_context.py --repo . --output pr-context.json`

예전 `prepare-handoff`, `write-pr-rationale` generate 명령은 현재 primary path가 아니라 compatibility 또는 deprecation stub입니다.

### 3. Codex Local Install (선택)

Codex가 outward-facing workflow를 설치된 local skill로 읽게 하고 싶다면 이 경로를 씁니다.

```bash
python -m mimir_skills install
```

이건 실제 로컬 설치 경로이지만, 여전히 main baseline이 아니라 optional thin-adapter proof point입니다.

## 문서 안내

먼저 보면 좋은 문서:

- [Project One-Pager](docs/project-one-pager.ko.md)
- [Quick Start](docs/quick-start.ko.md)
- [Workflow Trigger Table (English)](docs/workflow-trigger-table.md)
- [Workflow Surface (English)](docs/workflow-surface.md)
- [Agent Support Levels (English)](docs/agent-support-levels.md)

참고 문서:

- [Always-Loaded Rules (English)](docs/always-loaded-rules.md)
- [Codex Local Install (English)](docs/codex-local-install.md)
- [Adapter Feedback Loop (English)](docs/adapter-feedback-loop.md)
- [Skills Directory Notes (English)](skills/README.md)
- [Examples Directory Notes (English)](examples/README.md)
- [Evaluations Directory Notes (English)](evaluations/README.md)
- [Trigger Taxonomy v0.1](spec/trigger-taxonomy.md)
- [Decision Record Schema v0.1](spec/decision-record-schema.md)
- [Memory Promotion Policy v0.1](spec/memory-promotion-policy.md)
- [Security Policy](SECURITY.md)
- [Contributing Guide](CONTRIBUTING.md)

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

## 현재 상태

이 저장소는 현재 skill-first baseline 위에서 운영됩니다.

- `prepare-handoff`와 `write-pr-rationale`는 live collector와 deprecated generate stub를 가진 skill-first workflow입니다
- `capture-ci-investigation`은 여전히 더 좁은 wrapper-only beta workflow입니다
- workflow routing은 규모나 ambiguity가 커지기 전까지 public trigger table 기준으로 유지합니다
- 결정론적 validator와 example verification은 안정적으로 유지하고, 더 큰 workflow runtime으로 되돌아가지 않습니다
- 새로운 agent-specific adapter는 repeated usage가 현재 baseline을 넘는 분명한 UX 이득을 보여주기 전까지 보류합니다

## 언어 운영 정책

- GitHub 기본 진입점은 `README.md`입니다.
- 의미 기준 source of truth는 영어 파일입니다.
- 한국어 파일은 루트 README와 `docs/` 아래의 소수 입구/개요 문서(`project-one-pager`, `quick-start`, `glossary`)에 대해서만 유지합니다.
- 상세 workflow 문서, helper 문서, skill, reference, evaluation, contributor workflow 파일, 로컬 planning 메모는 영어를 기준으로 유지합니다.
- 공개 기술 스펙, skill, example, evaluation, contributor workflow 파일은 영어만 유지합니다.
- JSON 키, schema 이름, file path는 두 언어 모두 영어를 유지합니다.

## 라이선스

Apache 2.0입니다. 자세한 내용은 [LICENSE](LICENSE)를 보세요.
