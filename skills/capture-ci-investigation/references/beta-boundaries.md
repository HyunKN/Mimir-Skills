# capture-ci-investigation Beta Boundaries

Use this note to keep the beta CI-investigation workflow narrow, truthful, and reviewable.

This boundary note mirrors and extends the core decision rules in `skills/capture-ci-investigation/SKILL.md`.
If the top-level wording changes there, update the framing here too.

## When This Workflow Fits

- There is already concrete CI failure context such as job IDs, rerun notes, workflow files, or local reproduction output.
- The immediate need is a bounded summary for teammates, not a claim of final root-cause certainty.
- The current best action may be mitigation, monitoring, rollback, or deferred follow-up rather than a confirmed fix.

## When To Escalate Or Switch

- Create or update a canonical decision record when the work changes shared retry, timeout, quarantine, or workflow policy.
- Escalate to deeper CI or incident investigation when logs are missing, failures are repeated across platforms, or the blast radius reaches release, security, or deploy gates.
- Do not use this workflow as the only artifact when someone needs canonical approval, durable auditability, or a stable record of a shared workflow change.

## Evidence Tiers

- Strong evidence:
  - repeated failures or a reproducible failure shape
  - concrete job links and affected workflow, config, or test files
  - a validating rerun, reproduction, or equivalent check that supports the selected action
- Medium evidence:
  - one failure plus partial corroboration such as workflow inspection, timing notes, environment observations, or a single rerun
  - a plausible explanation exists, but the validating check is incomplete or indirect
- Weak evidence:
  - rerun-only success
  - incomplete logs
  - unexplained variance without a confirmed config, code, or environment cause
  - a workflow or timeout change would be made mainly to quiet the signal rather than to match a known cause

## Wording Ladder

- Strong evidence:
  - acceptable: `The failure was likely caused by ...`
  - acceptable: `The current evidence supports changing ... because ...`
- Medium evidence:
  - acceptable: `The current evidence points to ...`
  - acceptable: `The leading hypothesis is ...`
  - required: say what would confirm or falsify the hypothesis
- Weak evidence:
  - acceptable: `The issue may reflect ...`
  - acceptable: `The current evidence is too thin to justify ...`
  - acceptable: `A rerun lowered urgency but did not confirm a fix.`

Avoid these phrases when the evidence is not strong:

- `fixed`
- `root cause confirmed`
- `the incident was caused by`
- `safe to increase retries or timeout now`

Prefer explicit uncertainty language over filler such as `further investigation may be needed` when you already know what evidence is missing.

## Output Rules By Evidence Strength

- Strong evidence:
  - explain the likely cause, the selected action, and the validation that supports it
- Medium evidence:
  - explain the best current hypothesis and what would strengthen or falsify it
- Weak evidence:
  - say explicitly that the issue is not confirmed fixed, avoid root-cause language, and bias toward monitoring or evidence collection

## Shared Workflow Change Checklist

When the summary would tune timeout, retry, quarantine, cache, runner, base image, or job sequencing behavior, also state:

- what jobs, platforms, or future debugging paths the change could affect
- whether the change preserves or weakens failure visibility
- what follow-up window or owner will decide whether the mitigation should stay
- what evidence would justify reverting or tightening the temporary change

If that blast radius cannot be described yet, the safer beta outcome is usually to monitor, collect evidence, or escalate rather than tune the shared workflow immediately.

## Monitoring-First Outcomes

Choose a monitor-first summary when:

- the failure occurred once and only a rerun passed
- there is no relevant branch-local workflow or code diff
- the suspected cause is infra or environment variance, but the logs are incomplete
- a shared workflow change would hide future failures more than it would explain the current one

In those cases, the summary should still say:

- what failed
- what evidence exists now
- why the evidence is still too weak
- what exact future signal would reopen deeper investigation or justify a workflow change

## Public Example Anchors

- `examples/windows-ci-timeout/` shows a stronger config-backed CI decision with a validating rerun.
- `examples/linux-ci-rerun-watch/` shows a weaker rerun-only signal where monitoring is the selected action and the issue is not described as fixed.
