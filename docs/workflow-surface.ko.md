[English](workflow-surface.md) | 한국어

# Workflow Surface

## Purpose

이 문서는 `decision-skills` v1을 위해 만들고 있는 outward-facing workflow surface를 정의한다.

이 저장소에는 이미 internal building block과 workflow-specific skill이 들어 있다.
이 문서는 현재의 internal 요소가 어떻게 더 단순한 public workflow story로 매핑되는지 설명한다.

## Public Workflow Surface

첫 번째 public workflow surface는 다음 세 user-facing workflow를 중심으로 한다:

- `prepare-handoff`
- `write-pr-rationale`
- `capture-ci-investigation`

이 이름들은 현재 internal package 이름이 아니라, 사용자가 원하는 눈에 보이는 output을 설명한다.

## Workflow Mapping

### `prepare-handoff`

User-facing goal:

- 현재 브랜치 상태로부터 handoff 초안을 생성한다
- 무엇이 바뀌었는지, 무엇이 남았는지, 어디서 이어야 하는지, 어떤 risk나 blocker가 남아 있는지를 설명한다

Current internal building blocks:

- `handoff-context`
- `decision-capture`
- `decision-core`

Current status:

- public workflow 이름은 정의되어 있다
- 전용 user-facing skill과 script는 아직 구현되지 않았다

### `write-pr-rationale`

User-facing goal:

- 현재 브랜치 diff와 validation context로부터 reviewer-facing rationale 초안을 생성한다
- 무엇이 바뀌었는지, 왜 바뀌었는지, 무엇이 검증되었는지, 리뷰어가 어디를 주의해서 봐야 하는지를 설명한다

Current internal building blocks:

- `pr-rationale`
- `decision-capture`
- `decision-core`

Current status:

- public workflow 이름은 정의되어 있다
- 전용 user-facing skill과 script는 아직 구현되지 않았다

### `capture-ci-investigation`

User-facing goal:

- 사용 가능한 실패 맥락으로부터 bounded CI investigation summary 초안을 생성한다
- 무엇이 실패했는지, 어떤 evidence가 있는지, 현재 시점의 가장 그럴듯한 설명이 무엇인지, 어떤 임시 next step이 취해졌는지를 설명한다

Current internal building blocks:

- `ci-rationale`
- `decision-capture`
- `decision-core`

Current status:

- public workflow 이름은 정의되어 있다
- 더 강한 example과 reliability boundary가 생길 때까지 더 좁은 beta 방향으로 유지된다

## Supporting Internal Skills

현재의 몇몇 skill은 여전히 중요하지만, 첫 outward-facing product promise의 일부는 아니다:

- `dependency-upgrade-decision`은 dependency 및 config change를 위한 specialized support workflow로 남는다
- `memory-promote`는 반복된 evidence와 review 뒤에 reusable lesson을 다루는 supporting layer로 남는다

이 요소들은 저장소 안에 계속 남아야 하지만, 첫 public product story의 전면에는 오지 않아야 한다.

## Transition Rule

v0.1에서 v1로 넘어가는 전환기에는:

- public docs는 user-facing workflow output을 설명해야 한다
- internal skill은 현재 implementation-oriented 이름을 유지해도 된다
- 새로운 user-facing skill은 현재 internal 요소를 즉시 대체하기보다, 그 위에 추가될 수 있다

목표는 현재 internal engine을 버리지 않으면서 adoption을 단순하게 만드는 것이다.
