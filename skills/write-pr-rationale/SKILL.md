---
name: write-pr-rationale
description: Draft reviewer-facing pull request rationale from the current branch when a change needs a concise explanation of what changed, why it changed, what was validated, and what still needs attention. Use when the user wants a bounded PR-ready draft from local repository context plus optional validation or reviewer notes.
---

# write-pr-rationale

Use this skill to draft a reviewer-facing PR rationale from the current local project state.

## Workflow

1. Start with this skill and the reviewer-facing references before relying on helper commands.
2. Read [`../_internal/pr-rationale/SKILL.md`](../_internal/pr-rationale/SKILL.md) for canonical PR-summary framing and [`../_internal/decision-capture/SKILL.md`](../_internal/decision-capture/SKILL.md) when a canonical record is missing but should exist.
3. Read [`references/decision-rules.md`](references/decision-rules.md) for epistemic guardrails, evidence-source rules, output template sections, and signal usage policy.
4. Prefer the smallest evidence set that still explains what changed, why it changed, what was validated, and what reviewers should watch.
5. Link back to canonical decision records or derived summaries when they exist instead of copying raw logs into the PR rationale.
6. Use helper commands only when they save time:
   - `scripts/collect_pr_context.py --repo <path> --output <context.json>` when the branch snapshot should be inspected or reused before drafting
   - `python -m mimir_skills write-pr-rationale --repo <path>` only when you need the deprecated shared helper note from an older workflow
   - `scripts/generate_pr_rationale.py --repo <path>` only when you need the deprecated direct-helper note from an older workflow
7. Treat the generated Markdown as a first draft to review and tighten before sharing in a pull request.

## Output Focus

- what changed in the current branch
- why the change happened
- what the local branch evidence tentatively suggests when explicit rationale is missing
- what validation ran or is still missing
- what reviewers should pay attention to
- what risks or follow-up remain
- what committed branch work still matters when there are no uncommitted files

## Guardrails

- Do not present the PR rationale as canonical truth; the canonical decision records remain the source of truth.
- Do not claim rationale, validation, or confidence that cannot be tied to local evidence or existing records.
- Do not let inferred rationale, reviewer focus, or follow-up risk sound more certain than the evidence source allows.
- Do not assume branch-only context is enough to explain why a change happened; add explicit rationale notes when intent is not recoverable from local state.
- Do not treat inferred rationale from file paths or commit subjects as stronger than an explicit user-provided `--why` note.
- Do not paste raw logs, hidden reasoning, or sensitive output into reviewer-facing text.
- Do not hide incomplete validation, uncertainty, or remaining risks to make the PR sound cleaner.
- Do not let reviewer-facing text drift away from the branch state or the canonical records behind it.
- Do not let a clean working tree collapse the rationale into generic filler when committed branch context is still available.

## Load References As Needed

- Read [`references/decision-rules.md`](references/decision-rules.md) for decision rules and the output template.
- Read [`../_internal/pr-rationale/SKILL.md`](../_internal/pr-rationale/SKILL.md) for the reviewer-facing summary shape and PR-specific guardrails.
- Read [`../_internal/pr-rationale/references/pr-playbook.md`](../_internal/pr-rationale/references/pr-playbook.md) for the local signal map, default section patterns, and compact fallback examples.
- Read [`../_internal/decision-capture/SKILL.md`](../_internal/decision-capture/SKILL.md) only when a missing canonical record should be created before drafting the rationale.
- Read [`../_internal/decision-core/SKILL.md`](../_internal/decision-core/SKILL.md) only when shared validation, evidence, and safety constraints need to be checked.
- Optionally run [`scripts/collect_pr_context.py`](scripts/collect_pr_context.py) when you need a reusable JSON snapshot of branch, diff, changed files, and recent-commit context.
- Inspect the public summaries under [`../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`](../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md) and [`../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`](../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md) only when you need concrete reviewer-facing rationale shapes.
- Read [`../../evaluations/reviewer-comprehension.md`](../../evaluations/reviewer-comprehension.md) only when checking whether the generated rationale is likely to answer a reviewer's core questions quickly.
