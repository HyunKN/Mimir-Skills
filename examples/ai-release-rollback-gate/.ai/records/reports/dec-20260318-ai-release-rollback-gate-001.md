# Gate AI-assisted checkout cache rollout behind canary approval

- Decision ID: `dec-20260318-ai-release-rollback-gate-001`

## Source of Truth

- Canonical JSON: `.ai/records/decisions/dec-20260318-ai-release-rollback-gate-001.json`

## Summary

Reject the AI-suggested full checkout-cache rollout based on stale rollout guidance, deploy the change to a 5% canary only, and require explicit platform approval plus post-deploy monitoring before any wider promotion.

## Follow-Up

- Update the stale checkout-cache cutover runbook so future agents see the current canary-and-approval requirement first.
- Re-open approval review before increasing production traffic beyond the initial 5% canary.
- Record the final post-deploy outcome in a follow-up decision record if the rollout later reaches full production.
