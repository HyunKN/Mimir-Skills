# Fix failing Windows test job Decision Summary

> Derived from canonical decision record `dec-20260311-ci-timeout-001`.

## Decision

Increase the Windows integration test timeout and keep the retry count unchanged.

## Context

The Windows integration suite started failing after asset extraction time increased by about 40 seconds.

## Selected Option

- Increase timeout threshold
- Extend the timeout from 120s to 180s without changing retry behavior.

## Why

The failures were caused by slower setup time rather than flakiness in the tests themselves.

## Alternatives Considered

- Raise retries (rejected): Would hide the timeout root cause and lengthen successful runs.
- Increase timeout threshold (selected): Matches observed extraction time and preserves failure visibility.

## Evidence

- [ci] `build-1824/windows-integration`: Three consecutive failures timed out during the setup stage. (captured 2026-03-11T10:08:00Z)
- [file] `.github/workflows/test.yml`: Timeout was configured at 120 seconds for the integration step. (captured 2026-03-11T10:12:00Z)

## Affected Paths

- `.github/workflows/test.yml`

## Validation

- [test] `pnpm test:integration:windows` -> passed: The workflow completed once with the new timeout.

## Remaining Risks

- If setup time continues to grow, the timeout may need to be revisited.

## Follow-Up

- Track setup duration for the next five CI runs.

## Confidence

- 0.82
