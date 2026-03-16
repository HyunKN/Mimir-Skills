---
name: write-pr-rationale
description: Draft reviewer-facing pull request rationale from the current branch when a change needs a concise explanation of what changed, why it changed, what was validated, and what still needs attention. Use when the user wants a bounded PR-ready draft from local repository context plus optional validation or reviewer notes.
---

# write-pr-rationale

Use this skill to draft a reviewer-facing PR rationale from the current local project state.

## Decision Rules

1. Start with an epistemic guardrail, not with a signal table.
   Treat all inferred goals, signal-based reviewer notes, and signal-based risks as temporary substitutes when explicit `--why` notes are missing.
   Write `this branch appears to...`, `local branch evidence suggests...`, or `review should check...`, not `this branch does...` or `the author intended...`.
2. Let explicit rationale inputs win.
   Explicit rationale can arrive as user notes, helper-command flags such as `--why`, issue or incident context, editor context, or linked decision records.
   When that explicit rationale exists, treat it as higher-confidence input than any local inference.
3. Use the narrowest truthful evidence source and name it.
   Prefer the current working-tree diff first, then committed branch-range context when the tree is clean, then recent committed work only when both diff layers are clean.
4. Keep the draft reviewer-shaped.
   Separate what changed, why it changed, what was validated, what reviewers should watch, and what still needs follow-up instead of blending them into one branch summary.
5. Use local signals only as cautious prompts.
   File paths and commit subjects can suggest `docs`, `workflow`, `runtime`, `adapter`, `ci`, `dependency/config`, `examples/evaluation`, `spec`, or `rename`, but those signals are reviewer-orientation hints, not proof of author intent.
6. Surface clean-state context instead of filler.
   When the working tree is already clean, show committed branch-range or recent committed work explicitly instead of pretending there is no meaningful context.
7. End in uncertainty rather than overclaim.
   If explicit intent or validation is still missing after local inspection, say so plainly and ask for the missing rationale note before external sharing.

## Output Template

Use this shape and keep every section truthful to the evidence source you actually used:

### `PR Snapshot`

- repository, branch, base reference, and HEAD

### `What Changed`

- if the working tree is dirty: summarize changed files, notable name-status entries, untracked files, and diff stats
- if the working tree is clean: explicitly say the draft is using committed branch-range or recent-commit fallback context

### `Evidence`

- name the primary evidence source
- add nearby commit or branch signals only when they help the reviewer orient quickly

### `Why This Changed`

- if explicit `--why` notes exist: use them directly and do not add inferred-intent filler
- otherwise: state a tentative inferred goal, mention the strongest local signals and touched areas, and end with a prompt to replace or tighten the rationale with explicit `--why`

### `Validation`

- include explicit validation notes when they exist
- otherwise: keep missing validation visible and add the smallest reviewer-relevant validation prompt for the detected signal set

### `Reviewer Notes`

- point reviewers to the main watch areas implied by the evidence source and the local signals
- clean-state runs should explicitly tell reviewers when to anchor on committed branch-range or recent commits instead of uncommitted diff

### `Risks and Follow-Up`

- if explicit risks exist: use them directly
- otherwise: keep the missing-intent risk visible when `--why` is absent, then add only the highest-signal follow-up risks

## Workflow

1. Start with this skill and the reviewer-facing references before relying on helper commands.
2. Read [`../pr-rationale/SKILL.md`](../pr-rationale/SKILL.md) for canonical PR-summary framing and [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when a canonical record is missing but should exist.
3. Read [`../pr-rationale/references/pr-playbook.md`](../pr-rationale/references/pr-playbook.md) first when you need the signal map, section defaults, and compact fallback examples.
4. Prefer the smallest evidence set that still explains what changed, why it changed, what was validated, and what reviewers should watch.
5. Link back to canonical decision records or derived summaries when they exist instead of copying raw logs into the PR rationale.
6. Use helper commands only when they save time:
   - `python -m mimir_skills write-pr-rationale --repo <path>` for the optional shared helper path
   - `scripts/collect_pr_context.py --repo <path> --output <context.json>` when the branch snapshot should be inspected or reused before rendering
   - `scripts/generate_pr_rationale.py --repo <path>` when you want the direct helper-script path
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

- Read [`../pr-rationale/SKILL.md`](../pr-rationale/SKILL.md) for the reviewer-facing summary shape and PR-specific guardrails.
- Read [`../pr-rationale/references/pr-playbook.md`](../pr-rationale/references/pr-playbook.md) first for the local signal map, default section patterns, and compact fallback examples behind this skill.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) only when a missing canonical record should be created before drafting the rationale.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) only when shared validation, evidence, and safety constraints need to be checked.
- Optionally run `python -m mimir_skills write-pr-rationale --repo <path>` when the shared helper path is faster than assembling the draft manually from the skill.
- Optionally run [`scripts/collect_pr_context.py`](scripts/collect_pr_context.py) when you need a reusable JSON snapshot of branch, diff, changed files, and recent-commit context.
- Optionally run [`scripts/generate_pr_rationale.py`](scripts/generate_pr_rationale.py) when you want the direct helper-script path, and add `--output <path>` when you want to persist the Markdown draft to disk.
- Inspect the public summaries under [`../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`](../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md) and [`../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`](../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md) only when you need concrete reviewer-facing rationale shapes.
- Read [`../../evaluations/reviewer-comprehension.md`](../../evaluations/reviewer-comprehension.md) only when checking whether the generated rationale is likely to answer a reviewer’s core questions quickly.
