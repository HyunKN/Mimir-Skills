---
name: capture-ci-investigation
description: Draft a bounded CI investigation summary when failing jobs, flaky tests, build regressions, or workflow config changes need a concise best-effort explanation and next step. Use when the user wants a narrow incident summary from available failure context without promising perfect root-cause analysis.
---

# capture-ci-investigation

Use this skill to draft a narrow, best-effort CI investigation summary from the available failure context.

## Workflow

1. Start from the concrete failure context that already exists: job links, workflow files, rerun results, local reproduction, timing notes, and recent config changes.
2. Read [`../ci-rationale/SKILL.md`](../ci-rationale/SKILL.md) for CI-specific evidence and action framing.
3. Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when a canonical decision record should be created before or alongside the summary.
4. Distill what failed, what evidence exists, what the current best explanation is, and what action was taken, deferred, or still needs review.
5. Keep uncertainty explicit whenever logs, reruns, or reproduction evidence are incomplete.
6. Prefer mitigation and next-step language over definitive root-cause language when the evidence is thin.
7. Treat this as a beta workflow and keep the output human-reviewed before it is shared beyond the immediate engineering loop.

## Output Focus

- what failed
- what evidence is available
- what the current best explanation is
- what action was taken or deferred
- what risk, uncertainty, or monitoring remains

## Guardrails

- Do not promise perfect root-cause analysis.
- Do not treat a rerun-only success as proof that the CI issue is fixed.
- Do not hide missing validation, incomplete logs, or remaining uncertainty.
- Do not paste raw logs, secrets, or private infrastructure details into the summary.
- Do not recommend shared workflow changes without calling out their blast radius and follow-up need.
- Do not treat the summary as canonical truth; decision records remain primary when one exists.

## Load References As Needed

- Read [`../ci-rationale/SKILL.md`](../ci-rationale/SKILL.md) for CI-specific evidence handling, option framing, and safety constraints.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when the CI issue should be captured in a canonical record.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) when shared validation, evidence, and safety constraints need to be checked.
- Inspect the public example under [`../../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json`](../../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json) and its rendered summary under [`../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`](../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md) when you need a concrete CI investigation shape.
- Keep this workflow script-light for now; add direct-use collectors or generators only after stronger examples and reliability boundaries exist.
