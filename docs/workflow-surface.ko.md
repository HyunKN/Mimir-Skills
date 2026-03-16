[English](workflow-surface.md) | 한국어

# Workflow Surface

## Purpose

이 문서는 `Mimir-Skills` v1을 위해 만들고 있는 outward-facing skill surface를 정의한다.

이 저장소에는 이미 internal building block, workflow-specific skill, optional local helper code가 들어 있다.
이 문서는 그 요소들이 어떻게 더 단순한 public skill story로 매핑되는지, 그리고 어떤 surface가 이제 primary이고 어떤 것이 secondary인지 설명한다.

## Public Workflow Surface

첫 번째 public skill surface는 다음 세 user-facing workflow를 중심으로 한다:

- `prepare-handoff`
- `write-pr-rationale`
- `capture-ci-investigation`

이 이름들은 현재 internal package 이름이 아니라, 사용자가 원하는 눈에 보이는 output을 설명한다.
앞으로의 primary source of truth는 runtime helper보다 `SKILL.md`와 companion reference 쪽으로 이동해야 한다.

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
- 이제 primary user-facing skill이 `skills/prepare-handoff/` 아래에 존재한다
- skill과 handoff playbook이 이제 dirty-tree, clean branch-range, recent-commit fallback 규칙의 중심을 직접 담고 있다
- 위 세 representative branch-state 케이스에 대한 docs-only 재현도 통과했으므로, 이 workflow의 판단 규칙은 더 이상 runtime만의 source of truth가 아니다
- 첫 runtime-reduction pass는 이제 helper runtime에 git-context collection만 남긴다
- local helper command는 여전히 존재하지만, `python -m mimir_skills prepare-handoff`와 `skills/prepare-handoff/scripts/generate_handoff.py`는 이제 handoff Markdown 대신 deprecation guidance를 출력한다
- 남아 있는 live helper path는 `skills/prepare-handoff/scripts/collect_git_context.py`다
- `adapters/codex/scripts/install_codex_skills.py` 아래의 Codex-local install path는 optional thin-adapter proof point로만 유지된다
- 이 workflow도 이제 `write-pr-rationale`와 같은 skill-first + thin-collector 패턴을 따른다
- 더 넓은 multi-agent packaging은 아직 구현되지 않았고, 더 이상 main short-term story도 아니다

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
- 초기 user-facing skill이 이제 `skills/write-pr-rationale/` 아래에 존재한다
- user-facing skill과 PR playbook이 이제 주요 inference guardrail, signal pattern, reviewer-facing output template를 담고 있다
- 첫 runtime-reduction pass는 이제 helper runtime에 git-context collection만 남긴다
- local helper command는 여전히 존재하지만, `python -m mimir_skills write-pr-rationale`와 `skills/write-pr-rationale/scripts/generate_pr_rationale.py`는 이제 reviewer-facing Markdown 대신 deprecation guidance를 출력한다
- 남아 있는 live helper path는 `skills/write-pr-rationale/scripts/collect_pr_context.py`다
- `adapters/codex/scripts/install_codex_skills.py` 아래의 Codex-local install path는 optional thin-adapter proof point로만 유지된다
- 현재 clean-state rationale은 `prepare-handoff`보다 더 큰 재작성이 필요하며, 특히 명시적 `why` context가 없을 때 그 차이가 더 크다
- 첫 skill-first codification pass는 이제 존재하며, inferred intent를 기본적으로 tentative하게 다루도록 epistemic guardrail을 local signal map보다 앞에 두었다
- dirty tree, clean branch-range, recent-commit fallback, explicit `why` override 케이스를 포함한 첫 local agent-validation gate도 extra runtime-only rule 없이 통과했다
- 이 workflow는 이제 thin-collector 상태를 향해 갈 수 있지만, 그래도 clean-state run에 대해서는 아직 stable public guidance로 취급하면 안 되며, `prepare-handoff`보다 explicit product/tradeoff `why` note가 더 자주 필요하다
- 더 넓은 multi-agent packaging은 아직 구현되지 않았고, 더 이상 main short-term story도 아니다

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
- 초기 beta user-facing skill이 이제 `skills/capture-ci-investigation/` 아래에 존재한다
- beta skill, example, boundary note가 현재의 primary public surface다
- 이 workflow는 이제 `python -m mimir_skills list`에 beta wrapper로 보이지만, direct shared CLI generation command는 아직 없다
- 첫 Codex 전용 로컬 install path는 여전히 `adapters/codex/scripts/install_codex_skills.py`를 통해 이 workflow도 포함할 수 있지만, 그 경로는 optional하고 secondary다
- beta guidance가 이제 더 강한 config-backed CI example과 더 약한 rerun-only monitoring example을 함께 가리키도록 되어, overclaim boundary가 더 명확해졌다
- 전용 direct-use script는 의도적으로 아직 구현하지 않았다
- 더 강한 example과 reliability boundary가 생길 때까지 더 좁고 best-effort인 방향으로 유지된다

Beta graduation 메모:

- 서로 다른 CI failure shape를 아우르는 public-safe example이 여러 개 생기기 전까지는 beta로 유지한다
- direct-use path가 생기거나, wrapper-only 유지가 명시적 product decision으로 남기 전까지는 beta로 유지한다
- 반복 관찰에서 evidence, explanation, uncertainty, next step을 과장 없이 안정적으로 분리한다는 신호가 쌓이기 전까지는 beta로 유지한다

## Supporting Internal Skills

현재의 몇몇 skill은 여전히 중요하지만, 첫 outward-facing product promise의 일부는 아니다:

- `dependency-upgrade-decision`은 dependency 및 config change를 위한 specialized support workflow로 남는다
- `memory-promote`는 반복된 evidence와 review 뒤에 reusable lesson을 다루는 supporting layer로 남는다

이 요소들은 저장소 안에 계속 남아야 하지만, 첫 public product story의 전면에는 오지 않아야 한다.

## Helper Surface Note

로컬 실험을 위한 secondary helper surface는 여전히 존재하고 유용하다:

- `mimir_skills/` shared CLI command
- `skills/*/scripts/` 아래의 direct collector / generator
- optional thin-adapter proof point로서의 `adapters/codex/scripts/install_codex_skills.py`

다만 이 helper surface는 skill을 보조해야지 정의하면 안 된다. 의도하는 방향은 workflow 판단이 먼저 `SKILL.md`와 reference에 살고, runtime code는 점점 thin collector나 deterministic helper 쪽으로 줄어드는 것이다.

## Transition Rule

v0.1에서 v1로 넘어가는 전환기에는:

- public docs는 user-facing workflow output을 먼저 skill 문서 기준으로 설명해야 한다
- internal skill은 public story가 skill-first naming으로 옮겨가는 동안에도 현재 implementation-oriented 이름을 유지해도 된다
- local helper code는 당분간 남아 있어도 되지만, skill 문서보다 앞서는 main product surface가 되면 안 된다
- 새로운 user-facing skill은 현재 internal 요소를 즉시 대체하기보다, 그 위에 추가될 수 있다

목표는 현재의 validation 및 collection utility를 버리지 않으면서도 adoption을 단순하게 만드는 것이다.
