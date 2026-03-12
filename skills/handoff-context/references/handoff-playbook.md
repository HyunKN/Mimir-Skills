# Handoff Playbook

## Use This Reference For

- agent-to-agent continuation
- agent-to-human status transfer
- pause-and-resume workflows
- reviewer or maintainer context that should stay tied to canonical records

## Capture Sequence

1. Identify who needs the handoff and what they need to do next.
2. Gather only the decision records and derived summaries that matter for that continuation.
3. Separate completed work from remaining work.
4. Call out validation state, blockers, and remaining risks.
5. Make the next actions explicit.
6. Link back to the canonical JSON records and render Markdown only when it helps the next reader.

## Handoff Checklist

- selected decision or decisions
- affected paths
- validation state
- remaining risks
- follow-up or next actions
- blockers or open questions
- links to the canonical records and any derived summaries

## Summary Patterns

### Single-Record Handoff

- use when one decision record explains the state clearly
- prefer the derived Markdown summary and keep it tightly aligned with the JSON source

### Multi-Record Handoff

- use when several decisions affect the same continuation path
- summarize only the records that matter to the next owner instead of replaying the whole session

### Pause-and-Resume Handoff

- use when the same agent or a future agent will resume later
- make the next command, validation target, or decision checkpoint explicit

## Risk Patterns

- handoffs that retell the whole transcript instead of the actionable state
- missing blockers or hidden incomplete validation
- stale summaries that drift from the canonical JSON
- follow-up ownership omitted from the continuation note

## Example Mapping

- `../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md` shows a compact CI handoff derived from one canonical record.
- `../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md` shows the same pattern for a dependency and config decision.
