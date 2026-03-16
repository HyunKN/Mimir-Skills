English | [한국어](agent-support-levels.ko.md)

# Agent Support Levels

## Purpose

This document defines what `shared CLI support`, `documented support`, and `thin adapter support` mean for the near-term target agent families.

The goal is to avoid implying that every target has the same install, discovery, or native integration quality when the repository currently offers different levels of support.

## Level Definitions

### `shared CLI support`

- expected path: run `python -m decision_skills ...` from the repository root
- promise: the shared workflow entry points should remain usable from project-root CLI agents without a dedicated install or discovery layer
- does not promise native discovery, agent-local registration, or a target-specific install path

### `documented support`

- includes everything in `shared CLI support`
- adds public guidance for how a target agent family should use the shared CLI surface today
- can include known friction, current limits, and the recommended invocation path
- does not promise a dedicated adapter or native install/discovery flow

### `thin adapter support`

- includes everything in `documented support`
- adds a small agent-specific install, discovery, or invocation layer on top of the shared CLI and shared workflow core
- should improve UX without forking workflow logic, schemas, examples, or evaluation rules
- must stay thin: adapter code is glue, not a second core implementation

## Current Near-Term Assignments

| Agent family | Current level | Current path | Why it stops here today |
| --- | --- | --- | --- |
| Anthropic / Claude Code | `documented support` | shared CLI plus public support guidance | The shared CLI shape and workflow phrasing have already been reviewed from Claude's perspective, but there is still no dedicated Claude adapter or install path. |
| OpenAI / Codex and GPT-facing coding-agent surfaces | `thin adapter support` | shared CLI plus the local Codex installer | A real local Codex adapter exists today, but it is still a local install path rather than a broader hosted or registry-backed packaging story. |
| Google / Gemini CLI | `shared CLI support` | shared CLI only | No dedicated evaluation pass, install path, or target-specific public guidance exists yet. |
| Qwen / Qwen Code | `shared CLI support` | shared CLI only | No dedicated evaluation pass, install path, or target-specific public guidance exists yet. |

## Upgrade Rules

- Move a target from `shared CLI support` to `documented support` only after at least one concrete usage pass, review, or reproducible invocation pattern is available to document.
- Move a target from `documented support` to `thin adapter support` only when the UX gain is clear enough to justify ongoing maintenance.
- Do not raise a support level by copying workflow logic into agent-specific paths; adapters should stay thin and defer to the shared CLI and shared workflow modules.

## Current Interpretation

- These levels do not claim equal UX quality across the target agent families.
- They describe the highest public support layer that the repository currently stands behind for each family.
- Codex is the only near-term target with a real adapter today, and that does not fix the permanent order of future adapters.
