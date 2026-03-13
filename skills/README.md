# Skills Directory

This directory will hold installable or reference skill packages built on top of the public specs.

Current internal entries:

- `decision-core`
- `decision-capture`
- `dependency-upgrade-decision`
- `ci-rationale`
- `handoff-context`
- `pr-rationale`
- `memory-promote`

Current outward-facing workflow entry:

- `prepare-handoff` -> user-facing wrapper built from `handoff-context`, `decision-capture`, and `decision-core`, now with local git-context collection and Markdown handoff draft scripts
- `write-pr-rationale` -> user-facing wrapper built from `pr-rationale`, `decision-capture`, and `decision-core`, now with local PR-context collection and Markdown rationale draft scripts
- `capture-ci-investigation` -> narrow beta wrapper built from `ci-rationale`, `decision-capture`, and `decision-core`, intentionally kept best-effort and script-light for now

Specialized supporting workflows:

- `dependency-upgrade-decision`
- `memory-promote`

These current skills remain instruction-first and mostly non-executable by design.
They include bounded local automation where needed: schema validation in `decision-core`, draft record scaffolding and summary rendering in `decision-capture`, memory artifact validation in `memory-promote`, and workflow-specific guidance in the specialized skills above.

The public product story is being simplified around user-facing workflow outputs.
The current internal packages stay important, but they are now treated as building blocks rather than as the final outward-facing surface.
`prepare-handoff` and `write-pr-rationale` are now the first direct-use public wrappers on top of that internal engine.
`capture-ci-investigation` is intentionally narrower: a beta wrapper that stays best-effort until stronger examples justify a direct-use script layer.
