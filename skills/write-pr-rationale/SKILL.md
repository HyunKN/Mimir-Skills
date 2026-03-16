---
name: write-pr-rationale
description: Draft reviewer-facing pull request rationale from the current branch when a change needs a concise explanation of what changed, why it changed, what was validated, and what still needs attention. Use when the user wants a bounded PR-ready draft from local repository context plus optional validation or reviewer notes.
---

# write-pr-rationale

Use this skill to draft a reviewer-facing PR rationale from the current local project state.

## Workflow

1. Start with `python -m mimir_skills write-pr-rationale --repo <path>` when a quick reviewer-facing first draft from local repository context plus optional rationale notes is enough.
2. Use `scripts/collect_pr_context.py --repo <path> --output <context.json>` first when the branch snapshot should be inspected or reused before rendering the PR rationale, or when you want to call the collector directly without the shared CLI entry point.
3. Read [`../pr-rationale/SKILL.md`](../pr-rationale/SKILL.md) for reviewer-facing framing and [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when a canonical decision record is missing but should exist.
4. Prefer the smallest evidence set that still explains what changed, why it changed, what was validated, and what reviewers should watch.
5. Link back to canonical decision records or derived summaries when they exist instead of copying raw logs into the PR rationale.
6. When the working tree is already clean, surface committed branch-range context or recent committed work instead of defaulting to a nearly empty reviewer draft.
7. Provide `--why`, `--validation`, `--reviewer-note`, or `--evidence` whenever local branch data alone would underspecify why the change matters to reviewers.
8. State uncertainty plainly when the branch context is incomplete or validation evidence is missing.
9. Treat the generated Markdown as a first draft to review and tighten before sharing in a pull request.

## Output Focus

- what changed in the current branch
- why the change happened
- what validation ran or is still missing
- what reviewers should pay attention to
- what risks or follow-up remain
- what committed branch work still matters when there are no uncommitted files

## Guardrails

- Do not present the PR rationale as canonical truth; the canonical decision records remain the source of truth.
- Do not claim rationale, validation, or confidence that cannot be tied to local evidence or existing records.
- Do not assume branch-only context is enough to explain why a change happened; add explicit rationale notes when intent is not recoverable from local state.
- Do not paste raw logs, hidden reasoning, or sensitive output into reviewer-facing text.
- Do not hide incomplete validation, uncertainty, or remaining risks to make the PR sound cleaner.
- Do not let reviewer-facing text drift away from the branch state or the canonical records behind it.
- Do not let a clean working tree collapse the rationale into generic filler when committed branch context is still available.

## Load References As Needed

- Read [`../pr-rationale/SKILL.md`](../pr-rationale/SKILL.md) for the reviewer-facing summary shape and PR-specific guardrails.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when a missing canonical record should be created before drafting the rationale.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) when shared validation, evidence, and safety constraints need to be checked.
- Run `python -m mimir_skills list` from the repository root when you need a quick view of the current shared CLI workflows.
- Run `python -m mimir_skills write-pr-rationale --repo <path>` when you need a reviewer-facing first draft from the current repository state, and add explicit rationale notes when the branch-only view is too thin to explain why the change happened.
- Run [`scripts/collect_pr_context.py`](scripts/collect_pr_context.py) when you need a reusable JSON snapshot of branch, diff, changed files, and recent-commit context.
- Run [`scripts/generate_pr_rationale.py`](scripts/generate_pr_rationale.py) when you want the same shared generator through the direct script path, and add `--output <path>` when you want to persist the Markdown draft to disk.
- Inspect the public summaries under [`../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`](../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md) and [`../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`](../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md) when you need concrete reviewer-facing rationale shapes.
- Read [`../../evaluations/reviewer-comprehension.md`](../../evaluations/reviewer-comprehension.md) when checking whether the generated rationale is likely to answer a reviewer’s core questions quickly.
