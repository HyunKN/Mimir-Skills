---
name: prepare-handoff
description: Draft a handoff from the current branch or working tree when another human or agent needs to continue the task without reconstructing the whole session by hand. Use when the user wants a concise continuation summary from local repository context, changed files, recent validation, blockers, and next actions.
---

# prepare-handoff

Use this skill to draft a user-facing handoff from the current local project state.

## Workflow

1. Read the smallest useful slice of local context before writing: current branch, `git status`, changed files, `git diff --stat`, and a short recent commit window when available.
2. Read [`../handoff-context/SKILL.md`](../handoff-context/SKILL.md) for the continuation-summary shape and [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when a canonical decision record is missing but should exist.
3. Prefer the minimum evidence set that still explains what changed, what remains, where to continue, what was validated, and what is still risky.
4. Draft a concise Markdown handoff for the next human or agent.
5. Link back to canonical decision records or derived summaries when they exist instead of copying raw logs into the handoff.
6. State uncertainty plainly when the branch context is incomplete or validation evidence is missing.

## Output Focus

- what changed in the current branch or working tree
- what work is complete
- what work remains unfinished
- where the next owner should continue
- what validation has or has not run
- what blockers, risks, or follow-ups remain

## Guardrails

- Do not present the handoff as canonical truth; the canonical decision records remain the source of truth.
- Do not claim rationale, validation, or confidence that cannot be tied to local evidence or existing records.
- Do not copy secrets, credentials, or raw sensitive logs into the handoff.
- Do not retell the whole session when a shorter continuation summary is enough.
- Do not hide incomplete validation, uncertainty, or remaining risks to make the handoff look cleaner.

## Load References As Needed

- Read [`../handoff-context/SKILL.md`](../handoff-context/SKILL.md) for the current continuation-summary structure and summary-specific guardrails.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when a missing canonical record should be created before drafting the handoff.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) when shared validation, evidence, and safety constraints need to be checked.
- Inspect the public summaries under [`../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`](../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md) and [`../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`](../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md) when you need concrete published handoff shapes.
