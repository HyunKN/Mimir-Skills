[English](quick-start.md) | 한국어

# Quick Start

## 목적

이 문서는 지금 시점에서 `Mimir-Skills`를 가장 짧고 실용적인 경로로 바로 써보는 방법을 정리한다.

현재 지원되는 진입 경로는 두 가지다:

1. project-root workflow에 가장 마찰이 적은 `shared CLI`
2. Codex가 설치된 workflow skill을 직접 읽게 만들고 싶을 때의 `Codex local install`

이 경로들이 현재 target agent family와 어떻게 연결되는지는 [Agent Support Levels](agent-support-levels.ko.md)를 참고한다.

## Path 1: Shared CLI

오늘 기준 기본 추천 경로는 이것이다.

저장소 루트에서 workflow output을 가장 적은 마찰로 직접 써보고 싶을 때 사용한다.

![Shared CLI command snapshot](assets/shared-cli-quick-start.svg)

### 명령

사용 가능한 shared workflow를 확인:

```bash
python -m mimir_skills list
```

현재 저장소 상태로부터 handoff 초안 생성:

```bash
python -m mimir_skills prepare-handoff --repo .
```

현재 브랜치로부터 reviewer-facing PR rationale 초안 생성:

```bash
python -m mimir_skills write-pr-rationale --repo .
```

실제로 파일이 필요할 때만 Markdown draft를 디스크에 남긴다:

```bash
python -m mimir_skills prepare-handoff --repo . --output handoff.md
python -m mimir_skills write-pr-rationale --repo . --output pr-rationale.md
```

### 기대할 수 있는 것

- `prepare-handoff`가 현재 더 강한 clean-state workflow다.
- `write-pr-rationale`도 사용 가능하지만, 로컬 branch context가 얇을 때는 더 강한 `why` capture가 아직 필요하다.
- output은 draft이며, 외부 공유 전에는 여전히 human review가 필요하다.

## Path 2: Codex Local Install

Codex가 outward-facing workflow를 설치된 로컬 skill로 읽게 만들고 싶다면 이 경로를 사용한다.

![Codex local install snapshot](assets/codex-local-install.svg)

### 명령

현재 outward-facing workflow를 기본 Codex home에 설치:

```bash
python adapters/codex/scripts/install_codex_skills.py
```

주요 direct-use workflow만 설치:

```bash
python adapters/codex/scripts/install_codex_skills.py --workflows prepare-handoff write-pr-rationale
```

그 다음 Codex에게 다음과 같이 직접 workflow 언어로 요청한다:

- `Prepare a handoff from my current changes.`
- `Write PR rationale for this branch.`
- `Summarize this CI failure as a bounded investigation note.`

### 기대할 수 있는 것

- 이것은 hosted registry flow가 아니라 실제 로컬 install path다
- 설치된 wrapper도 shared CLI 경로와 같은 shared workflow core를 사용한다
- 설치된 Codex skill이 꼭 필요한 경우가 아니면, shared CLI 경로가 여전히 더 낮은 마찰의 기본 경로다

## 두 경로 중 무엇을 고를까

다음과 같다면 `shared CLI`를 고른다:

- workflow를 가장 빨리 시험해보고 싶다
- project-root CLI agent를 사용한다
- agent-specific install이나 discovery 동작이 꼭 필요하지 않다

다음과 같다면 `Codex local install`을 고른다:

- Codex가 workflow를 설치된 로컬 skill로 읽게 하고 싶다
- thin adapter support의 실제 proof point가 필요하다

## 현재 한계

- `capture-ci-investigation`은 여전히 더 좁은 beta wrapper다
- hosted multi-agent install story는 아직 없다
- agent family마다 support level이 다르며, 모든 target이 thin adapter를 갖고 있는 것은 아니다
- 더 자세한 동작과 safety constraint는 [Always-Loaded Rules](always-loaded-rules.ko.md), [Workflow Surface](workflow-surface.ko.md), 각 workflow `SKILL.md`에 남아 있다
