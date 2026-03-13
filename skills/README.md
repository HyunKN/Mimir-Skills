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

- `prepare-handoff` -> thin user-facing wrapper built from `handoff-context`, `decision-capture`, and `decision-core`

Planned next outward-facing workflow entries:

- `write-pr-rationale` -> built from `pr-rationale`, `decision-capture`, and `decision-core`
- `capture-ci-investigation` -> built from `ci-rationale`, `decision-capture`, and `decision-core`

Specialized supporting workflows:

- `dependency-upgrade-decision`
- `memory-promote`

These current skills remain instruction-first and mostly non-executable by design.
They include bounded local automation where needed: schema validation in `decision-core`, draft record scaffolding and summary rendering in `decision-capture`, memory artifact validation in `memory-promote`, and workflow-specific guidance in the specialized skills above.

The public product story is being simplified around user-facing workflow outputs.
The current internal packages stay important, but they are now treated as building blocks rather than as the final outward-facing surface.
`prepare-handoff` is the first thin public wrapper on top of that internal engine; dedicated local collectors and output scripts are still the next layer to build.
