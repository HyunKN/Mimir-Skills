---
name: capture-ci-investigation
description: Draft a bounded CI investigation summary when failing jobs, flaky tests, build regressions, or workflow config changes need a concise best-effort explanation and next step. Use when the user wants a narrow incident summary from available failure context without promising perfect root-cause analysis.
---

# capture-ci-investigation

Use this skill to draft a narrow, best-effort CI investigation summary from the available failure context.

## Decision Rules

1. Keep four lanes separate in the draft:
   - observed evidence
   - the current best explanation
   - unknowns or remaining uncertainty
   - the temporary decision, mitigation, or next check
2. Let evidence strength control the wording:
   - strong evidence can support likely-cause language when the failure shape, relevant change, and validating check all line up
   - medium evidence should stay hypothesis-shaped and say what would confirm or falsify the explanation
   - weak evidence should stay monitor-first, avoid root-cause or fixed language, and say explicitly that the issue is not yet explained
3. Treat rerun-only success or partial validation as a signal reducer, not proof of root cause or proof that the issue is fixed.
4. If the current best action would touch shared workflow behavior such as retries, timeouts, quarantines, cache policy, base image, or job sequencing, call out the blast radius and the follow-up needed before describing the change as safe.
5. If there is no concrete code, workflow, or environment cause yet, prefer monitoring, evidence collection, rollback, or escalation language over speculative tuning.
6. Escalate to a canonical decision record or deeper CI investigation when the issue changes shared policy, repeats across platforms, blocks release or deploy gates, or still lacks enough evidence for a bounded summary.
7. Keep human review in the loop. This workflow drafts a bounded incident summary; it does not replace canonical approval or final root-cause analysis.

## Workflow

1. Start from the concrete failure context that already exists: job links, workflow files, rerun results, local reproduction, timing notes, and recent config changes.
2. Read [`../ci-rationale/SKILL.md`](../ci-rationale/SKILL.md) first for CI-specific evidence and option framing.
3. Read [`references/beta-boundaries.md`](references/beta-boundaries.md) when you need the wording ladder, blast-radius checklist, or a stronger rule for monitor-only conclusions.
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

## Output Template

Use a compact summary with these sections when the incident needs a written draft:

1. `Failure Summary`
   - state the failing job, stage, and immediate symptom
   - if the signal is weak, say so here rather than implying a confirmed break
2. `Observed Evidence`
   - list the concrete CI artifacts, reruns, workflow files, timing notes, or reproduction checks that actually exist
3. `Current Explanation`
   - strong evidence: explain the likely cause and why the evidence supports it
   - medium evidence: explain the leading hypothesis and what would confirm or falsify it
   - weak evidence: say that the issue is not yet explained and keep the explanation tentative
4. `Current Action`
   - state whether the team changed something, chose monitoring, reverted, quarantined, or deferred
   - if a shared workflow change is involved, mention the blast radius and follow-up window
5. `Unknowns / Risks`
   - name what is still uncertain, what could recur, or what this mitigation might hide
6. `Next Check`
   - say what evidence, rerun, duration sample, owner, or trigger would reopen deeper investigation

Omit filler. If a section has no real content, compress it into a shorter sentence rather than padding the draft.

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

- Read [`../ci-rationale/SKILL.md`](../ci-rationale/SKILL.md) first for CI-specific evidence handling, option framing, and safety constraints.
- Read [`references/beta-boundaries.md`](references/beta-boundaries.md) next when the available evidence is thin, rerun-only, or still too weak for root-cause language, or when a shared workflow change would affect more than the current failing job.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) only when the CI issue should be captured in a canonical record.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) only when shared validation, evidence, and safety constraints need to be checked.
- Inspect the public examples under [`../../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json`](../../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json), [`../../examples/linux-ci-rerun-watch/.ai/records/decisions/dec-20260316-linux-ci-rerun-watch-001.json`](../../examples/linux-ci-rerun-watch/.ai/records/decisions/dec-20260316-linux-ci-rerun-watch-001.json), and [`../../examples/macos-flaky-quarantine/.ai/records/decisions/dec-20260317-macos-flaky-quarantine-001.json`](../../examples/macos-flaky-quarantine/.ai/records/decisions/dec-20260317-macos-flaky-quarantine-001.json) when you need concrete CI investigation shapes for validated-change, monitor-only, and shared-workflow-quarantine cases.
- Read [`../../evaluations/capture-ci-investigation-beta-review.md`](../../evaluations/capture-ci-investigation-beta-review.md) when checking whether the draft keeps evidence, explanation, uncertainty, and temporary action clearly separated.
- Keep this workflow script-light for now; add direct-use collectors or generators only after stronger examples and reliability boundaries exist.
