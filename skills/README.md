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

Emerging public workflow surface:

- `prepare-handoff` -> built from `handoff-context`, `decision-capture`, and `decision-core`
- `write-pr-rationale` -> built from `pr-rationale`, `decision-capture`, and `decision-core`
- `capture-ci-investigation` -> built from `ci-rationale`, `decision-capture`, and `decision-core`

Specialized supporting workflows:

- `dependency-upgrade-decision`
- `memory-promote`

These current skills remain instruction-first and mostly non-executable by design.
They include bounded local automation where needed: schema validation in `decision-core`, draft record scaffolding and summary rendering in `decision-capture`, memory artifact validation in `memory-promote`, and workflow-specific guidance in the specialized skills above.

The public product story is being simplified around user-facing workflow outputs.
The current internal packages stay important, but they are now treated as building blocks rather than as the final outward-facing surface.
