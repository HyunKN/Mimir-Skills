# PR Playbook

## Use This Reference For

- reviewer-facing pull request summaries
- rationale derived from one or more decision records
- update notes that should stay aligned with canonical JSON
- review preparation focused on validation, risk, and follow-up

## Capture Sequence

1. Identify which decision records matter to the PR.
2. Gather only the evidence and validation details that a reviewer needs.
3. Separate what changed from why it changed.
4. Call out validation status, remaining risks, and follow-up work.
5. Link back to the canonical JSON records and use rendered Markdown only as a reviewer-facing derivative.
6. Refresh the PR rationale when the underlying records change.

## Reviewer Checklist

- what changed
- why it changed
- what evidence supports it
- what was validated
- what still needs attention
- which canonical record or records back the rationale

## Summary Patterns

### Single-Record PR Rationale

- use when one decision record explains the PR clearly
- start from the derived Markdown summary and tighten it for reviewer needs

### Multi-Record PR Rationale

- use when several decision records contribute to the same PR
- keep the explanation organized by review-relevant themes rather than by session chronology

### Risk-Forward PR Rationale

- use when the remaining risks or deferred follow-up are central to approval
- make the risks explicit instead of burying them in the middle of the text

## Risk Patterns

- PR descriptions that hide the real tradeoff
- reviewer summaries that omit failed or deferred alternatives
- stale PR text drifting away from canonical records
- missing validation or follow-up details that block confident review

## Example Mapping

- `../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md` shows a concise reviewer-facing explanation for a CI workflow adjustment.
- `../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md` shows the same pattern for a dependency and config decision.
- `../../evaluations/reviewer-comprehension.md` provides the five core questions a reviewer should be able to answer from the rationale.
