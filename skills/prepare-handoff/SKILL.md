---
name: prepare-handoff
description: Draft a handoff from the current branch or working tree when another human or agent needs to continue the task without reconstructing the whole session by hand. Use when the user wants a concise continuation summary from local repository context, changed files, recent validation, blockers, and next actions.
---

# prepare-handoff

Use this skill to draft a user-facing handoff from the current local project state.

## Workflow

1. Start with `python -m mimir_skills prepare-handoff --repo <path>` when a quick handoff draft from the local repository state is enough.
2. Use `scripts/collect_git_context.py --repo <path> --output <context.json>` first when the repository snapshot should be inspected or reused before rendering the handoff, or when you want to call the collector directly without the shared CLI entry point.
3. Read [`../handoff-context/SKILL.md`](../handoff-context/SKILL.md) for the continuation-summary shape and [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when a canonical decision record is missing but should exist.
4. Prefer the minimum evidence set that still explains what changed, what remains, where to continue, what was validated, and what is still risky.
5. Link back to canonical decision records or derived summaries when they exist instead of copying raw logs into the handoff.
6. When the working tree is already clean, fall back to committed branch context or recent committed work instead of implying that nothing happened.
7. Accept optional evidence notes when the local git snapshot alone would be too thin for the next owner.
8. State uncertainty plainly when the branch context is incomplete or validation evidence is missing.
9. Treat the generated Markdown as a first draft to review and tighten before handing it to another human or agent.

## Decision Rules

### 1. Snapshot Mode

- If the working tree has staged, unstaged, or untracked entries, treat the handoff as a dirty-tree handoff.
- If the working tree is clean and the branch still differs from its base, treat the handoff as a clean-state checkpoint backed by committed branch context.
- If both the working tree and committed branch-range diff are clean, treat the handoff as a recent-commit fallback rather than implying that no useful context exists.

### 2. What Changed Priority

- Dirty-tree handoff:
  - show the working-tree count first
  - list raw status entries before summarizing touched files
  - call out untracked files in a dedicated subsection when they exist
  - include staged and unstaged diff summaries when they exist
- Clean-state branch-range handoff:
  - say explicitly that no working-tree changes were detected
  - use committed branch-range files as the primary "what changed" evidence
  - include committed diff-stat lines when they exist
- Recent-commit fallback handoff:
  - say explicitly that both the working tree and branch-range diff are clean
  - summarize the most recent committed work that still matters for continuation

### 3. Evidence Priority

Use this order when you need to explain what the handoff is based on:

1. working-tree status and diff
2. committed branch-range context
3. recent committed work
4. explicit user-supplied evidence notes
5. generic "no extra local evidence" fallback only when nothing above exists

If the user already supplied evidence notes, use them as the section content instead of the default bullets.

### 4. Default Risk Rules

- Dirty tree:
  - warn that the final intended state still needs confirmation before external sharing
- Fully clean tree:
  - warn that missing continuation context may already live in commits or decision records and should be checked
- User-supplied risk notes:
  - prefer them over the default bullets, but keep uncertainty explicit if the branch state is still ambiguous

### 5. Default Next-Step Rules

- Dirty tree:
  - tell the next owner to review changed files and confirm what still needs committing
- Clean tree:
  - tell the next owner to decide whether a clean-state checkpoint is enough or whether a richer committed-work summary is needed
- Any changed files:
  - tell the next owner to replace placeholder validation text with concrete results before wider sharing
- Always:
  - remind the author to add blockers, risks, and owner notes when another person or agent will resume

### 6. Override Contract

- Explicit title input overrides the default repository-name title.
- Explicit evidence, validation, blocker, risk, and next-step notes override the default section bullets for those sections.
- Do not let override notes erase important uncertainty that the next owner still needs to know.

## Output Template

Use this structure unless the user asks for a different handoff shape:

```md
# Handoff: <title or repo name>

> Generated from local repository context for branch `<branch>` at `<timestamp>`.

## Current Snapshot

- Repository: `<repo name>`
- Branch: `<branch>`
- HEAD: `<short hash>`
- Branch context base: `<base ref>`
- Working tree: clean | not clean (`<staged>` staged, `<unstaged>` unstaged, `<untracked>` untracked)

## What Changed

- Follow the dirty-tree, clean-state branch-range, or recent-commit fallback rules above.

## Relevant Evidence

- Use explicit evidence notes if present.
- Otherwise use the evidence-priority decision tree above.

## Recent Commits

- List recent commits when available.
- If none are available, say that no recent commit history was available.

## Validation

- Use explicit validation notes if present.
- Otherwise say that no explicit validation notes were provided.

## Blockers and Risks

- Use explicit blocker and risk notes if present.
- Otherwise apply the default risk rules above.

## Next Steps

- Use explicit next-step notes if present.
- Otherwise apply the default next-step rules above.
```

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
- Read [`../handoff-context/references/handoff-playbook.md`](../handoff-context/references/handoff-playbook.md) for dirty-tree, clean-state branch-range, and recent-commit fallback output patterns.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when a missing canonical record should be created before drafting the handoff.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) when shared validation, evidence, and safety constraints need to be checked.
- Run `python -m mimir_skills list` from the repository root when you need a quick view of the current shared CLI workflows.
- Run `python -m mimir_skills prepare-handoff --repo <path>` when you need a directly usable handoff draft from the current repository state, including clean-state fallback from committed work when needed.
- Run [`scripts/collect_git_context.py`](scripts/collect_git_context.py) when you need a reusable JSON snapshot of branch, status, diff, and recent-commit context.
- Run [`scripts/generate_handoff.py`](scripts/generate_handoff.py) when you want the same shared generator through the direct script path, and add `--output <path>` when you want to persist the Markdown draft to disk.
- Inspect the public summaries under [`../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`](../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md) and [`../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`](../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md) when you need concrete published handoff shapes.
