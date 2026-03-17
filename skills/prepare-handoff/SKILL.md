---
name: prepare-handoff
description: Draft a handoff from the current branch or working tree when another human or agent needs to continue the task without reconstructing the whole session by hand. Use when the user wants a concise continuation summary from local repository context, changed files, recent validation, blockers, and next actions.
---

# prepare-handoff

Use this skill to draft a user-facing handoff from the current local project state.

## Workflow

1. Start with this skill and the continuation-summary references before relying on helper commands.
2. Read [`../_internal/handoff-context/SKILL.md`](../_internal/handoff-context/SKILL.md) for the continuation-summary shape and [`../_internal/decision-capture/SKILL.md`](../_internal/decision-capture/SKILL.md) when a canonical decision record is missing but should exist.
3. Read [`references/decision-rules.md`](references/decision-rules.md) for snapshot-mode rules, evidence priority, risk defaults, next-step defaults, override contracts, and the output template.
4. Prefer the minimum evidence set that still explains what changed, what remains, where to continue, what was validated, and what is still risky.
5. Link back to canonical decision records or derived summaries when they exist instead of copying raw logs into the handoff.
6. Use helper commands only when they save time:
   - `scripts/collect_git_context.py --repo <path> --output <context.json>` when the repository snapshot should be inspected or reused before drafting
   - `python -m mimir_skills prepare-handoff --repo <path>` only when you need the deprecated shared helper note from an older workflow
   - `scripts/generate_handoff.py --repo <path>` only when you need the deprecated direct-helper note from an older workflow
7. State uncertainty plainly when the branch context is incomplete or validation evidence is missing.
8. Treat the generated Markdown as a first draft to review and tighten before handing it to another human or agent.

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

- Read [`references/decision-rules.md`](references/decision-rules.md) for decision rules, override contracts, and the output template.
- Read [`references/invocation-prompts.md`](references/invocation-prompts.md) when you want copy-paste prompt macros for installed-agent use.
- Read [`../_internal/handoff-context/SKILL.md`](../_internal/handoff-context/SKILL.md) for the current continuation-summary structure and summary-specific guardrails.
- Read [`../_internal/handoff-context/references/handoff-playbook.md`](../_internal/handoff-context/references/handoff-playbook.md) for dirty-tree, clean-state branch-range, and recent-commit fallback output patterns.
- Read [`../_internal/decision-capture/SKILL.md`](../_internal/decision-capture/SKILL.md) when a missing canonical record should be created before drafting the handoff.
- Read [`../_internal/decision-core/SKILL.md`](../_internal/decision-core/SKILL.md) when shared validation, evidence, and safety constraints need to be checked.
- Run `python -m mimir_skills list` from the repository root when you need a quick view of the current shared CLI workflows.
- Run [`scripts/collect_git_context.py`](scripts/collect_git_context.py) when you need a reusable JSON snapshot of branch, status, diff, and recent-commit context.
- Inspect the public summaries under [`../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`](../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md) and [`../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`](../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md) when you need concrete published handoff shapes.
