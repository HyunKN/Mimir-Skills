---
name: capture-ci-investigation
description: Draft a bounded CI investigation summary when failing jobs, flaky tests, build regressions, or workflow config changes need a concise best-effort explanation and next step. Use when CI failure context is available and a concise investigation summary with clear evidence separation is needed.
---

# capture-ci-investigation

Use this skill to draft a bounded CI investigation summary from the available failure context.

## Workflow

1. Start from the concrete failure context that already exists: job links, workflow files, rerun results, local reproduction, timing notes, and recent config changes.
2. Read [`../_internal/ci-rationale/SKILL.md`](../_internal/ci-rationale/SKILL.md) first for CI-specific evidence and option framing.
3. Read [`references/beta-boundaries.md`](references/beta-boundaries.md) when you need the wording ladder, blast-radius checklist, or a stronger rule for monitor-only conclusions.
4. Read [`../_internal/decision-capture/SKILL.md`](../_internal/decision-capture/SKILL.md) when a canonical decision record should be created before or alongside the summary.
5. Read [`references/decision-rules.md`](references/decision-rules.md) for the four-lane separation rules, evidence-strength wording, and the output template.
6. Call out stale guidance, AI-assisted suggestions, approval scope, or rollout posture when they materially explain why the incident path was risky.
7. Keep uncertainty explicit whenever logs, reruns, or reproduction evidence are incomplete.
8. Prefer mitigation and next-step language over definitive root-cause language when the evidence is thin.
9. Keep the output human-reviewed before sharing beyond the immediate engineering loop.

## Output Focus

- what failed
- what evidence is available
- what the current best explanation is
- what action was taken or deferred
- what governance constraints shaped the response when they matter
- what is still only being monitored rather than confirmed fixed
- what risk, uncertainty, or monitoring remains

## Guardrails

- Do not promise perfect root-cause analysis.
- Do not treat a rerun-only success as proof that the CI issue is fixed.
- Do not let the absence of a workflow diff stand in for evidence of root cause.
- Do not reduce a risky AI-assisted change to a generic failure note when approval scope, stale guidance, or rollout posture mattered.
- Do not hide missing validation, incomplete logs, or remaining uncertainty.
- Do not paste raw logs, secrets, or private infrastructure details into the summary.
- Do not recommend shared workflow changes without calling out their blast radius and follow-up need.
- Do not treat the summary as canonical truth; decision records remain primary when one exists.

## Load References As Needed

- Read [`references/decision-rules.md`](references/decision-rules.md) for decision rules and output template.
- Read [`../_internal/ci-rationale/SKILL.md`](../_internal/ci-rationale/SKILL.md) first for CI-specific evidence handling, option framing, and safety constraints.
- Read [`references/beta-boundaries.md`](references/beta-boundaries.md) for wording ladder, blast-radius checklist, or monitor-only rules.
- Read [`../_internal/decision-capture/SKILL.md`](../_internal/decision-capture/SKILL.md) only when the CI issue should be captured in a canonical record.
- Read [`../../spec/trigger-taxonomy.md`](../../spec/trigger-taxonomy.md) when the summary may need governance context or a canonical record with optional governance fields.
- Read [`../_internal/decision-core/SKILL.md`](../_internal/decision-core/SKILL.md) only when shared validation, evidence, and safety constraints need to be checked.
- Inspect the public examples under [`../../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json`](../../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json), [`../../examples/linux-ci-rerun-watch/.ai/records/decisions/dec-20260316-linux-ci-rerun-watch-001.json`](../../examples/linux-ci-rerun-watch/.ai/records/decisions/dec-20260316-linux-ci-rerun-watch-001.json), and [`../../examples/macos-flaky-quarantine/.ai/records/decisions/dec-20260317-macos-flaky-quarantine-001.json`](../../examples/macos-flaky-quarantine/.ai/records/decisions/dec-20260317-macos-flaky-quarantine-001.json) when you need concrete CI investigation shapes.
- Read [`../../evaluations/capture-ci-investigation-beta-review.md`](../../evaluations/capture-ci-investigation-beta-review.md) when checking whether the draft keeps evidence, explanation, uncertainty, and temporary action clearly separated.
- Read [`../../evaluations/capture-ci-investigation-repeated-observation.md`](../../evaluations/capture-ci-investigation-repeated-observation.md) when deciding whether repeated real usage still supports the current wrapper-only posture.
