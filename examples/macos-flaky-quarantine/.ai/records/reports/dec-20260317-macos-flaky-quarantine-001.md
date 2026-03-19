# Quarantine flaky macOS visual snapshot test

- Decision ID: `dec-20260317-macos-flaky-quarantine-001`

## Source of Truth

- Canonical JSON: `.ai/records/decisions/dec-20260317-macos-flaky-quarantine-001.json`

## Summary

Quarantine the flaky macOS avatar snapshot spec from the required visual workflow, keep it running in a nightly-only lane, and reopen full triage before re-enabling it.

## Follow-Up

- Collect five nightly quarantine runs before deciding whether to rewrite the snapshot, pin the browser version, or re-enable the spec in the required lane.
- Re-open broader CI triage immediately if another macOS visual spec starts failing on the same browser patch line.
