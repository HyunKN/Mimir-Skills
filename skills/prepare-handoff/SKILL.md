---
name: prepare-handoff
description: Draft a handoff from the current branch or working tree when another human or agent needs to continue the task without reconstructing the whole session by hand. Use when the user wants a concise continuation summary from local repository context, changed files, recent validation, blockers, and next actions.
---

# prepare-handoff

Use this skill to draft a user-facing handoff from the current local project state.

## Workflow

1. Start with `scripts/generate_handoff.py --repo <path>` when a quick handoff draft from the local repository state is enough.
2. Use `scripts/collect_git_context.py --repo <path> --output <context.json>` first when the repository snapshot should be inspected or reused before rendering the handoff.
3. Read [`../handoff-context/SKILL.md`](../handoff-context/SKILL.md) for the continuation-summary shape and [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when a canonical decision record is missing but should exist.
4. Prefer the minimum evidence set that still explains what changed, what remains, where to continue, what was validated, and what is still risky.
5. Link back to canonical decision records or derived summaries when they exist instead of copying raw logs into the handoff.
6. When the working tree is already clean, fall back to committed branch context or recent committed work instead of implying that nothing happened.
7. Accept optional evidence notes when the local git snapshot alone would be too thin for the next owner.
8. State uncertainty plainly when the branch context is incomplete or validation evidence is missing.
9. Treat the generated Markdown as a first draft to review and tighten before handing it to another human or agent.

## Output Focus

- what changed in the current branch or working tree
- what work is complete
- what work remains unfinished
- where the next owner should continue
- what validation has or has not run
- what blockers, risks, or follow-ups remain
- what recent committed work matters when the working tree is already clean

## Guardrails

- Do not present the handoff as canonical truth; the canonical decision records remain the source of truth.
- Do not claim rationale, validation, or confidence that cannot be tied to local evidence or existing records.
- Do not copy secrets, credentials, or raw sensitive logs into the handoff.
- Do not retell the whole session when a shorter continuation summary is enough.
- Do not hide incomplete validation, uncertainty, or remaining risks to make the handoff look cleaner.
- Do not let a clean working tree erase important recently committed context when that context still matters for the handoff.

## Load References As Needed

- Read [`../handoff-context/SKILL.md`](../handoff-context/SKILL.md) for the current continuation-summary structure and summary-specific guardrails.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when a missing canonical record should be created before drafting the handoff.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) when shared validation, evidence, and safety constraints need to be checked.
- Run [`scripts/collect_git_context.py`](scripts/collect_git_context.py) when you need a reusable JSON snapshot of branch, status, diff, and recent-commit context.
- Run [`scripts/generate_handoff.py`](scripts/generate_handoff.py) when you need a directly usable `handoff.md` draft from the current repository state, including clean-state fallback from committed work when needed.
- Inspect the public summaries under [`../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`](../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md) and [`../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`](../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md) when you need concrete published handoff shapes.
