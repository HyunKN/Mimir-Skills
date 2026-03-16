# Skill-First Staleness Review

## Purpose

Use this review to check whether the public docs, examples, and helper surfaces still describe the same current behavior after workflow-surface changes.

The goal is not to catch every typo.
The goal is to catch product-level drift: stale instructions, outdated examples, mismatched helper guidance, or phase language that can mislead a fresh agent.

## Review Scope

Review at least these surfaces when a workflow or public helper surface changes:

- `../README.md`
- `../docs/project-one-pager.md`
- `../docs/workflow-surface.md`
- `../docs/quick-start.md`
- `../skills/prepare-handoff/SKILL.md`
- `../skills/write-pr-rationale/SKILL.md`
- `../mimir_skills/manifest.json`
- `python -m mimir_skills list`
- the changed workflow help text under `python -m mimir_skills <workflow> --help`
- `python scripts/verify_examples.py`

## Review Questions

1. Do the public docs lead with the current primary surface (`SKILL.md` plus references) instead of an outdated generator path?
2. Are deprecated generator or helper paths described as secondary compatibility stubs rather than the main workflow?
3. Do the documented collector commands still exist and produce structured output?
4. Do public-safe examples and rendered summaries still match the current schemas and intended workflow story?
5. If phase language appears in active local notes, is it clear whether it refers to the historical `v0.1 Deliverables` phases or the newer operating roadmap?

## Pass Criteria

The review passes if:

- public docs agree that the repository is skill-first
- helper stubs are described truthfully as deprecated or secondary
- collector commands, manifest summaries, and help text match the docs
- example verification passes without schema or rendered-summary drift
- actively maintained local notes do not use ambiguous unlabeled phase shorthand

## Failure Signals

Treat the review as weak or failed if:

- a doc still presents shared CLI or adapter generation as the primary workflow path
- a public doc, skill doc, or example points at removed or renamed files
- rendered summaries or examples drift from the canonical records or schemas
- helper help text or manifest summaries contradict the docs
- phase shorthand in active notes can be read as either the old v0.1 phases or the newer operating roadmap

## Notes

- Fix one-off wording mistakes directly.
- If the same drift pattern repeats, record it in `../.workspace/failure-modes.md`.
- This review is intentionally lightweight and should be run after meaningful workflow-surface changes, not after every typo fix.
