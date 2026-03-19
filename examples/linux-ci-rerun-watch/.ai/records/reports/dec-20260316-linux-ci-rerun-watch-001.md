# Investigate intermittent Linux unit-test timeout

- Decision ID: `dec-20260316-linux-ci-rerun-watch-001`

## Source of Truth

- Canonical JSON: `.ai/records/decisions/dec-20260316-linux-ci-rerun-watch-001.json`

## Summary

Keep the Linux unit-test workflow unchanged, rerun the failed job once, and monitor the next three CI runs before changing timeout or retry settings.

## Follow-Up

- Collect the next three Linux unit-test job durations and failure stages before changing timeout or retry policy.
- Re-open deeper CI triage if another timeout occurs with the same base image.
