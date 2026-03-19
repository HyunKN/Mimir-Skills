# Quarantine flaky macOS visual snapshot test Decision Summary

> Derived from canonical decision record [[dec-20260317-macos-flaky-quarantine-001]].

## Decision

Quarantine the flaky macOS avatar snapshot spec from the required visual workflow, keep it running in a nightly-only lane, and reopen full triage before re-enabling it.

## Context

The release-required macOS visual job started failing on the same avatar snapshot assertion across multiple reruns and two branches after a browser patch. Linux and Windows visual lanes stayed green.

## Selected Option

- Quarantine the failing spec and keep nightly coverage
- Exclude the single flaky avatar snapshot spec from the required macOS visual lane, keep it in a nightly quarantine lane, and review re-enable criteria after five nightly runs.

## Why

Repeated failures on the same macOS-only snapshot plus stable Linux and Windows results point to a narrow flaky rendering path, not a suite-wide regression. Quarantining one spec preserves most release gating while keeping the failing test visible in a separate lane.

## Alternatives Considered

- Increase retries for the macOS visual workflow (rejected): Would blur whether the macOS-only snapshot failure is stable and make the required lane harder to interpret.
- Disable the full macOS visual job (deferred): Would unblock merges faster but would remove broader visual coverage for unrelated macOS cases.
- Quarantine the failing spec and keep nightly coverage (selected): Narrows the blast radius while preserving a visible signal for the flaky test in a separate lane.

## Evidence

- [ci] `build-1852/macos-visual`: The required macOS visual job failed three times on the same account-avatar snapshot diff across two PR reruns. (captured 2026-03-17T04:11:00Z)
- [ci] `build-1855/macos-visual`: A fresh rerun on the latest commit failed on the same spec again, which reduced the chance of a one-off CI interruption. (captured 2026-03-17T04:28:00Z)
- [file] `.github/workflows/e2e-visual.yml`: The macOS visual lane is part of the required merge gate, so any quarantine changes affect a shared workflow path. (captured 2026-03-17T04:34:00Z)
- [file] `tests/visual/account-avatar.spec.ts`: The failing assertion is isolated to the macOS avatar snapshot spec; adjacent visual specs in the same suite continued to pass. (captured 2026-03-17T04:39:00Z)
- [command] `pnpm test:visual --project=macos --grep "account avatar"`: A targeted local macOS rerun reproduced the same snapshot diff while the Linux baseline remained unchanged. (captured 2026-03-17T04:47:00Z)

## Related Artifacts

- Canonical decision note: [[dec-20260317-macos-flaky-quarantine-001]]

## Affected Paths

- `.github/workflows/e2e-visual.yml`
- `tests/visual/account-avatar.spec.ts`

## Validation

- [build] `Run required macOS visual workflow with avatar spec quarantined` -> passed: The required macOS visual lane passed once after excluding the flaky spec from the merge-gating job.
- [manual] `Nightly quarantined avatar snapshot lane` -> partial: The isolated nightly lane still failed on the same snapshot diff, preserving the signal while the required lane recovered.

## Remaining Risks

- The quarantine could linger and normalize reduced macOS coverage if re-enable criteria are not enforced.
- The flaky avatar snapshot may reflect a broader rendering issue that could spread to other visual specs after future browser updates.

## Follow-Up

- Collect five nightly quarantine runs before deciding whether to rewrite the snapshot, pin the browser version, or re-enable the spec in the required lane.
- Re-open broader CI triage immediately if another macOS visual spec starts failing on the same browser patch line.

## Confidence

- 0.74
