# Skills Directory

This directory holds the primary public skill packages for the repository.

Current internal entries:

- `decision-core`
- `decision-capture`
- `dependency-upgrade-decision`
- `ci-rationale`
- `handoff-context`
- `pr-rationale`
- `memory-promote`

Current outward-facing workflow entries:

- `prepare-handoff` -> user-facing workflow skill built from `handoff-context`, `decision-capture`, and `decision-core`, now with its main decision rules living in the skill and playbook docs
- `write-pr-rationale` -> user-facing workflow skill built from `pr-rationale`, `decision-capture`, and `decision-core`, now carrying a first-pass skill-first rule set while clean-state rationale capture still needs stronger explicit `why` support
- `capture-ci-investigation` -> narrow beta workflow skill built from `ci-rationale`, `decision-capture`, and `decision-core`, intentionally kept best-effort and script-light for now

Specialized supporting workflows:

- `dependency-upgrade-decision`
- `memory-promote`

These skills are instruction-first by design.
They include bounded local automation only where deterministic behavior still adds value: schema validation in `decision-core`, draft record scaffolding and summary rendering in `decision-capture`, memory artifact validation in `memory-promote`, and a small number of optional local workflow helpers.

The public story is now centered on the skills themselves.
Internal packages still matter, but they are building blocks rather than the final outward-facing surface.
Helper code under `mimir_skills/`, `skills/*/scripts/`, and `adapters/` remains secondary: useful for local collection, validation, or proof points, but no longer the intended source of workflow judgment.
