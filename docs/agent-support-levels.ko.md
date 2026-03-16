[English](agent-support-levels.md) | 한국어

# Agent Support Levels

## 목적

이 문서는 가까운 범위의 target agent family에 대해 `shared CLI support`, `documented support`, `thin adapter support`가 각각 무엇을 뜻하는지 정의한다.

목표는 저장소가 모든 target에 대해 같은 수준의 install, discovery, native integration 품질을 제공하는 것처럼 보이지 않게 하는 것이다. 현재 제공 수준은 target마다 다르다.

## 지원 수준 정의

### `shared CLI support`

- 기대 경로: 저장소 루트에서 `python -m decision_skills ...`를 실행한다
- 약속 범위: shared workflow entry point가 dedicated install 또는 discovery layer 없이도 project-root CLI agent에서 계속 usable해야 한다
- 약속하지 않는 것: native discovery, agent-local registration, target-specific install path

### `documented support`

- `shared CLI support`의 내용을 모두 포함한다
- 오늘 시점에 특정 target agent family가 shared CLI surface를 어떻게 써야 하는지에 대한 공개 guidance를 추가한다
- known friction, current limits, recommended invocation path를 포함할 수 있다
- dedicated adapter나 native install/discovery flow를 약속하지는 않는다

### `thin adapter support`

- `documented support`의 내용을 모두 포함한다
- shared CLI와 shared workflow core 위에 작은 agent-specific install, discovery, invocation layer를 추가한다
- workflow logic, schema, example, evaluation rule을 복제하지 않으면서 UX를 개선해야 한다
- adapter는 반드시 얇아야 한다. adapter 코드는 glue이지, 두 번째 core 구현이 아니다

## 현재 가까운 범위의 할당

| Agent family | 현재 수준 | 현재 경로 | 지금 이 수준에서 멈추는 이유 |
| --- | --- | --- | --- |
| Anthropic / Claude Code | `documented support` | shared CLI + 공개 support guidance | shared CLI 형태와 workflow 표현은 이미 Claude 관점에서 한 차례 검토되었지만, dedicated Claude adapter나 install path는 아직 없다. |
| OpenAI / Codex 및 GPT-facing coding-agent surface | `thin adapter support` | shared CLI + 로컬 Codex installer | 실제 로컬 Codex adapter는 이미 존재하지만, 아직 broader hosted 또는 registry-backed packaging story까지는 아니다. |
| Google / Gemini CLI | `shared CLI support` | shared CLI only | dedicated evaluation pass, install path, target-specific public guidance가 아직 없다. |
| Qwen / Qwen Code | `shared CLI support` | shared CLI only | dedicated evaluation pass, install path, target-specific public guidance가 아직 없다. |

## 승격 규칙

- 어떤 target을 `shared CLI support`에서 `documented support`로 올리려면, 최소 한 번 이상의 concrete usage pass, review, 또는 재현 가능한 invocation pattern이 문서화 가능해야 한다.
- 어떤 target을 `documented support`에서 `thin adapter support`로 올리려면, UX 이득이 지속적인 유지 비용을 정당화할 만큼 분명해야 한다.
- support level을 올린다는 이유로 workflow logic을 agent-specific path에 복제하면 안 된다. adapter는 얇게 유지하고, shared CLI와 shared workflow module을 그대로 사용해야 한다.

## 현재 해석

- 이 수준들은 target agent family 사이의 UX 품질이 모두 같다고 주장하지 않는다.
- 이 문서는 각 family에 대해 저장소가 현재 공개적으로 어디까지 지원한다고 말할 수 있는지를 정의한다.
- 현재 실 adapter가 있는 가까운 범위 target은 Codex뿐이지만, 그렇다고 미래 adapter 순서가 영구적으로 고정되는 것은 아니다.
