# Investigate intermittent Linux unit-test timeout Decision Summary

> Derived from canonical decision record `dec-20260316-linux-ci-rerun-watch-001`.

## Decision

Keep the Linux unit-test workflow unchanged, rerun the failed job once, and monitor the next three CI runs before changing timeout or retry settings.

## Context

The Linux unit-test job timed out once during dependency install after a base image refresh. A single rerun passed, and no branch-local workflow or test-command change explains the failure yet.

## Selected Option

- Rerun once and monitor subsequent runs
- Leave timeout and retry settings unchanged, record the rerun result, and collect the next three Linux job durations before deciding whether a workflow change is justified.

## Why

The current evidence is too weak to justify a shared workflow change. A rerun-only success suggests the failure may be transient, but it does not confirm root cause or prove the issue is fixed.

## Alternatives Considered

- Increase the workflow timeout (deferred): Would weaken the current signal before confirming that the timeout threshold is actually too low.
- Increase the retry count (rejected): Would make future failures harder to interpret while the evidence is still thin.
- Rerun once and monitor subsequent runs (selected): Preserves the current workflow signal while acknowledging that the rerun reduces urgency without proving a fix.

## Evidence

- [ci] `build-1846/linux-unit`: The initial job timed out during dependency install at 14m58s, two seconds before the current 15-minute threshold. (captured 2026-03-16T07:02:00Z)
- [ci] `build-1846-rerun/linux-unit`: A single rerun passed without code or workflow changes, which lowered urgency but did not identify a cause. (captured 2026-03-16T07:18:00Z)
- [diff] `origin/main...HEAD`: The branch diff does not include Linux workflow, dependency-install, or unit-test command changes related to this job. (captured 2026-03-16T07:24:00Z)
- [file] `.github/workflows/test.yml`: The Linux unit-test job already uses a 15-minute timeout, so changing the limit would affect a shared workflow path rather than a branch-local fix. (captured 2026-03-16T07:29:00Z)

## Validation

- [manual] `Re-run linux-unit job in CI` -> partial: One rerun passed, but the run did not reproduce the timeout or validate a concrete fix.

## Remaining Risks

- The timeout may recur if the image-refresh slowdown or package-registry variance continues.
- A future workflow change made on this evidence alone could hide the real source of the instability.

## Follow-Up

- Collect the next three Linux unit-test job durations and failure stages before changing timeout or retry policy.
- Re-open deeper CI triage if another timeout occurs with the same base image.

## Confidence

- 0.41
