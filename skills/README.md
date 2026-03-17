# Skills Directory

This directory holds the primary public skill packages for the repository.

## Outward-Facing Workflows

- `prepare-handoff` — user-facing workflow skill built from `_internal/handoff-context`, `_internal/decision-capture`, and `_internal/decision-core`
- `write-pr-rationale` — user-facing workflow skill built from `_internal/pr-rationale`, `_internal/decision-capture`, and `_internal/decision-core`
- `capture-ci-investigation` — skill-first workflow skill, wrapper-only by design, built from `_internal/ci-rationale`, `_internal/decision-capture`, and `_internal/decision-core`

If routing is unclear before loading one of those skills, start with `docs/workflow-trigger-table.md`.

## Internal Building Blocks (`_internal/`)

- `_internal/decision-core`
- `_internal/decision-capture`
- `_internal/dependency-upgrade-decision`
- `_internal/ci-rationale`
- `_internal/handoff-context`
- `_internal/pr-rationale`
- `_internal/memory-promote`

These skills are instruction-first by design.
They include bounded local automation only where deterministic behavior still adds value: schema validation in `decision-core`, draft record scaffolding and summary rendering in `decision-capture`, memory artifact validation in `memory-promote`, and a small number of optional local workflow helpers.

The public story is now centered on the skills themselves.
Internal packages still matter, but they are building blocks rather than the final outward-facing surface.
Helper code under `mimir_skills/`, `skills/*/scripts/`, and `adapters/` remains secondary: useful for local collection, validation, or proof points, but no longer the intended source of workflow judgment.
