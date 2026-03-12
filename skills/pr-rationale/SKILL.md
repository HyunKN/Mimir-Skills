---
name: pr-rationale
description: Prepare or review reviewer-facing pull request rationale when a change needs a concise explanation of what changed, why it changed, what evidence supports it, what was validated, and what still needs attention. Use when validated decision records exist or must be created, and a PR description should stay tightly aligned with canonical records instead of raw chat or ad hoc summaries.
---

# pr-rationale

Use this skill when a pull request needs a concise, reviewable rationale derived from validated decision records.

## Workflow

1. Confirm that the underlying work has crossed a trigger boundary and that the relevant decision record exists or should be created first.
2. Read `../decision-capture/SKILL.md` if the canonical record is missing or incomplete.
3. Gather only the decision records, rendered summaries, and validation results needed for reviewer comprehension.
4. Distill what changed, why it changed, what evidence supports it, what was validated, and what still needs attention.
5. Use `../decision-capture/scripts/render_summary.py <record-path>` when a single validated record needs a derived Markdown starting point.
6. Keep the PR rationale short, reviewer-facing, and linked back to the canonical JSON records for deeper detail.
7. Update the rationale when the source decision record changes so the PR text does not drift.

## PR Focus

- Optimize for reviewer comprehension, not for full session replay.
- Make the selected option and the tradeoff against rejected alternatives clear.
- Surface validation, remaining risk, and follow-up work in a way that helps review and approval.
- Keep every claim traceable to a canonical record or a validated derived summary.

## Guardrails

- Do not paste raw chat history, hidden reasoning, or long logs into the PR rationale.
- Do not introduce claims that are missing from the source decision record.
- Do not omit remaining risks or incomplete validation just to make the PR sound cleaner.
- Do not treat the PR description as the source of truth; the canonical JSON record remains primary.
- Do not use reviewer-facing text to justify unsafe shortcuts that are absent from the underlying record.

## Load References As Needed

- Read [`references/pr-playbook.md`](references/pr-playbook.md) when preparing or reviewing PR descriptions from one or more decision records.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when creating a missing canonical record or rendering a summary from it.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) when checking shared validation, safety, and promotion constraints.
- Read [`../../spec/decision-record-schema.md`](../../spec/decision-record-schema.md) when reviewing which fields should be preserved in reviewer-facing rationale.
- Inspect the public summaries under [`../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`](../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md) and [`../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`](../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md) when you need concrete reviewer-facing rationale shapes.
- Read [`../../evaluations/reviewer-comprehension.md`](../../evaluations/reviewer-comprehension.md) when checking whether a PR rationale is likely to answer the reviewer’s core questions quickly.
