# Gate AI-assisted checkout cache rollout behind canary approval Decision Summary

> Derived from canonical decision record [[dec-20260318-ai-release-rollback-gate-001]].

## Decision

Reject the AI-suggested full checkout-cache rollout based on stale rollout guidance, deploy the change to a 5% canary only, and require explicit platform approval plus post-deploy monitoring before any wider promotion.

## Context

A local AI coding assistant proposed a direct production rollout for a checkout-cache invalidation change after reading an outdated internal-style runbook snapshot that predated the current staged-rollout policy. The change touches a shared commerce path, so a broad rollout would carry customer-visible blast radius if the cache warmup assumptions are wrong.

## Selected Option

- Approve a 5% canary with rollback-ready monitoring
- Keep the rollout at 5% production traffic, require platform approval for that limited scope, and hold wider promotion until canary telemetry stays clean for four hours.

## Why

The stale guidance made the original AI-assisted rollout plan unsafe to follow directly. A narrow canary plus explicit approval captures the real operating policy, gives reviewers a durable record of why the full rollout was rejected, and keeps rollback posture visible while the change is observed in production.

## Alternatives Considered

- Ship the AI-suggested 100% rollout immediately (rejected): Relied on stale rollout guidance and skipped the current canary requirement for a shared production path.
- Pause the release entirely (deferred): Would remove near-term risk but would also delay the verified cache-fix path even though a bounded canary is available.
- Approve a 5% canary with rollback-ready monitoring (selected): Preserves forward progress while keeping the blast radius bounded, the approval scope explicit, and the rollback path ready.

## Evidence

- [doc] `docs/runbooks/checkout-cache-cutover.md`: The older runbook snapshot still described a full-rollout path and did not include the newer staged-rollout approval note. (captured 2026-03-18T13:42:00Z)
- [doc] `docs/policies/production-rollout-safety.md`: The current policy requires canary rollout plus explicit platform approval for high-blast-radius checkout changes. (captured 2026-03-18T13:48:00Z)
- [diff] `origin/main...HEAD`: The branch diff shows the cache invalidation change plus a rollout manifest update that would move all production traffic at once without further gating. (captured 2026-03-18T13:55:00Z)
- [command] `python scripts/check_rollout_policy.py --service checkout-cache --stage production`: The synthetic policy check failed for a full rollout and passed once the plan was reduced to a 5% canary with explicit approval metadata. (captured 2026-03-18T14:08:00Z)
- [discussion] `platform-review-2026-03-18`: Platform review confirmed that checkout-cache invalidation is a shared customer path and must stay rollback-ready during the first production segment. (captured 2026-03-18T14:18:00Z)

## AI Assistance

- Used: yes
- Summary: A local AI assistant proposed the initial rollout plan after reading stale rollout guidance that no longer matched the current production policy.
- Tools: Local coding assistant, Repository runbook snapshot
- Human verification: A platform engineer compared the stale runbook against the current rollout policy and replaced the full rollout with a canary-only plan.

## Approval

- Required: yes
- Status: approved
- Approver: platform-oncall
- Scope: 5% canary only for the checkout-cache production path; wider rollout requires a new review after four hours of clean telemetry.
- Timestamp: 2026-03-18T14:22:00Z

## Change Governance

- Risk tier: high
- Blast radius: A bad checkout-cache rollout could surface stale prices or availability across the shared customer purchase path if promoted broadly.
- Deployment stage: canary
- Rollback plan: Revert the rollout manifest to 0% and restore the previous cache invalidation behavior immediately if error rate, stale-read alerts, or checkout latency regress during the canary window.
- Post-deploy status: monitoring
- Post-deploy summary: The first 30 minutes of 5% canary telemetry stayed within error-budget thresholds, but wider promotion remains blocked until four hours of clean production signals are recorded.

## Related Artifacts

- Canonical decision note: [[dec-20260318-ai-release-rollback-gate-001]]

## Affected Paths

- `deploy/checkout-cache-rollout.yaml`
- `docs/runbooks/checkout-cache-cutover.md`
- `docs/policies/production-rollout-safety.md`

## Validation

- [build] `python scripts/check_rollout_policy.py --service checkout-cache --stage production` -> passed: The synthetic rollout policy check passed once the manifest was reduced to a 5% canary and approval metadata was attached.
- [manual] `Review first 30 minutes of canary telemetry for checkout-cache` -> partial: Initial canary telemetry stayed clean, but the policy still requires four hours of monitoring before any wider production promotion.

## Remaining Risks

- If the stale runbook remains easy for agents to find, similar unsafe rollout suggestions may recur on future shared production changes.
- A wider rollout could still surface cache-warmup regressions that do not appear during the smaller canary slice.

## Follow-Up

- Update the stale checkout-cache cutover runbook so future agents see the current canary-and-approval requirement first.
- Re-open approval review before increasing production traffic beyond the initial 5% canary.
- Record the final post-deploy outcome in a follow-up decision record if the rollout later reaches full production.

## Confidence

- 0.81
