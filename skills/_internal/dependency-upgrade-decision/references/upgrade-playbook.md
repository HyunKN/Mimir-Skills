# Upgrade Playbook

## Use This Reference For

- package or library upgrades
- version pinning or hold decisions
- rollback decisions after an incompatible change
- deferrals caused by timing, migration cost, or validation gaps

## Capture Sequence

1. Identify the dependency or config contract that changed.
2. List the real options: upgrade, pin, roll back, defer, or add compatibility work.
3. Gather only the evidence needed to compare those options.
4. Record the selected path and why it won.
5. Record affected paths, validation, remaining risks, and follow-up.
6. Validate the JSON record and render Markdown only if a human or another agent needs a short summary.

## Evidence Checklist

- manifest diff such as `package.json`, `pyproject.toml`, or equivalent
- lockfile diff or generated-artifact impact
- config, schema, or interface changes tied to the dependency decision
- release notes, changelog entries, or migration guidance
- validation runs such as tests, CI reruns, smoke checks, or build output
- explicit risk notes when the change is deferred, pinned, or rolled back

## Decision Patterns

### Upgrade Now

- use when validation passes and the compatibility cost is acceptable
- cite the validating evidence, not only the version bump

### Pin or Hold

- use when the newer version breaks compatibility, needs migration work, or adds release risk
- explain the unblock value of the pin and the follow-up needed to revisit it

### Roll Back

- use when a new version or config path has already landed and must be reversed to restore stability
- record the restoring action and the evidence that it fixed the regression

### Defer

- use when the upgrade is desirable but cannot be safely completed now
- record the reason for delay and the condition that should trigger a revisit

## Risk Patterns

- hidden config contract changes
- transitive dependency drift
- test coverage that misses runtime or deploy behavior
- security fixes postponed by a pin or defer decision
- migration work split across multiple follow-up tasks

## Example Mapping

- The public synthetic example under `../../../examples/cache-client-pin/` shows a dependency-and-config trigger where pinning was chosen over immediate adoption.
- Use that example when you need a compact reference for `decision`, `selected_option`, `evidence_refs`, `validation_run`, and `remaining_risks` in this workflow.
