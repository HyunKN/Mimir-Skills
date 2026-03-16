# capture-ci-investigation Beta Boundaries

Use this note to keep the beta CI-investigation workflow narrow, truthful, and reviewable.

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
  - repeated failures, concrete job links, affected workflow or config files, and a validating rerun or local reproduction
- Medium evidence:
  - one failure plus partial corroboration such as workflow inspection, timing notes, or a single rerun
- Weak evidence:
  - rerun-only success, incomplete logs, or unexplained variance without a confirmed config or code cause

## Output Rules By Evidence Strength

- Strong evidence:
  - explain the likely cause, the selected action, and the validation that supports it
- Medium evidence:
  - explain the best current hypothesis and what would strengthen or falsify it
- Weak evidence:
  - say explicitly that the issue is not confirmed fixed, avoid root-cause language, and bias toward monitoring or evidence collection

## Public Example Anchors

- `examples/windows-ci-timeout/` shows a stronger config-backed CI decision with a validating rerun.
- `examples/linux-ci-rerun-watch/` shows a weaker rerun-only signal where monitoring is the selected action and the issue is not described as fixed.
