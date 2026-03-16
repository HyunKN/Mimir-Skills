---
name: capture-ci-investigation
description: Draft a bounded CI investigation summary when failing jobs, flaky tests, build regressions, or workflow config changes need a concise best-effort explanation and next step. Use when the user wants a narrow incident summary from available failure context without promising perfect root-cause analysis.
---

# capture-ci-investigation

Use this skill to draft a narrow, best-effort CI investigation summary from the available failure context.

## Workflow

1. Start from the concrete failure context that already exists: job links, workflow files, rerun results, local reproduction, timing notes, and recent config changes.
2. Read [`../ci-rationale/SKILL.md`](../ci-rationale/SKILL.md) for CI-specific evidence and action framing.
3. Read [`references/beta-boundaries.md`](references/beta-boundaries.md) when you need to decide how strong the current evidence really is or whether the summary should stay at a monitoring-only conclusion.
4. Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when a canonical decision record should be created before or alongside the summary.
5. Distill what failed, what evidence exists, what the current best explanation is, and what action was taken, deferred, or still needs review.
6. Keep uncertainty explicit whenever logs, reruns, or reproduction evidence are incomplete.
7. Prefer mitigation and next-step language over definitive root-cause language when the evidence is thin.
8. Treat this as a beta workflow and keep the output human-reviewed before it is shared beyond the immediate engineering loop.

## Output Focus

- what failed
- what evidence is available
- what the current best explanation is
- what action was taken or deferred
- what is still only being monitored rather than confirmed fixed
- what risk, uncertainty, or monitoring remains

## Guardrails

- Do not promise perfect root-cause analysis.
- Do not treat a rerun-only success as proof that the CI issue is fixed.
- Do not let the absence of a workflow diff stand in for evidence of root cause.
- Do not hide missing validation, incomplete logs, or remaining uncertainty.
- Do not paste raw logs, secrets, or private infrastructure details into the summary.
- Do not recommend shared workflow changes without calling out their blast radius and follow-up need.
- Do not treat the summary as canonical truth; decision records remain primary when one exists.

## Beta Status

Keep this workflow beta until all of the following are true:

- there are multiple public-safe examples covering more than one CI failure shape
- either a direct-use collection and generation path exists, or wrapper-only behavior remains an explicit written decision
- repeated observation shows the workflow can consistently separate observed evidence, current explanation, unknowns, and next action without overclaiming

## Load References As Needed

- Read [`../ci-rationale/SKILL.md`](../ci-rationale/SKILL.md) for CI-specific evidence handling, option framing, and safety constraints.
- Read [`references/beta-boundaries.md`](references/beta-boundaries.md) when the available evidence is thin, rerun-only, or still too weak for root-cause language.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when the CI issue should be captured in a canonical record.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) when shared validation, evidence, and safety constraints need to be checked.
- Inspect the public examples under [`../../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json`](../../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json) and [`../../examples/linux-ci-rerun-watch/.ai/records/decisions/dec-20260316-linux-ci-rerun-watch-001.json`](../../examples/linux-ci-rerun-watch/.ai/records/decisions/dec-20260316-linux-ci-rerun-watch-001.json) when you need concrete CI investigation shapes for both validated-change and monitor-only cases.
- Keep this workflow script-light for now; add direct-use collectors or generators only after stronger examples and reliability boundaries exist.
