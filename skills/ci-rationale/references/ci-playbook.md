# CI Playbook

## Use This Reference For

- failing CI jobs and test triage
- flaky or timing-sensitive pipeline behavior
- workflow config changes involving retries, timeouts, or job sequencing
- temporary mitigations that need explicit follow-up

## Capture Sequence

1. Identify the failing surface, affected platform, and trigger category.
2. Gather only the evidence needed to compare the available remediation options.
3. List the real options: fix the root cause, tune timeout or retry settings, revert, quarantine, or defer.
4. Record the selected action and why it won.
5. Record validation, remaining risks, and follow-up monitoring.
6. Validate the JSON record and render Markdown only if another human or agent needs a short summary.

## Evidence Checklist

- failing job or build identifiers
- relevant workflow, config, or test files
- rerun results or local reproduction notes
- timing, infrastructure, or environment observations tied to the failure
- targeted diffs that changed the workflow or test behavior
- explicit notes when the chosen action is a temporary mitigation

## Decision Patterns

### Fix the Root Cause

- use when the underlying CI or test behavior can be corrected directly
- cite the change and the validating rerun or reproduction

### Tune Timeout or Retry

- use when the failure is caused by known timing characteristics and the mitigation preserves failure visibility
- explain why the change does not simply hide flakiness

### Roll Back a Workflow or Config Change

- use when a recent workflow edit introduced the failure and stability must be restored first
- record the rollback path and the evidence that the failing job recovered

### Quarantine or Defer

- use when the issue cannot be safely fixed now without blocking other work
- record the scope of the quarantine or deferral and the follow-up needed to remove it

## Risk Patterns

- flakiness masked as stability
- environment-specific failures misread as product regressions
- retries or timeouts that delay future debugging
- shared workflow edits that affect platforms outside the current incident
- temporary mitigations that become permanent without review

## Example Mapping

- The public synthetic example under `../../examples/windows-ci-timeout/` shows a CI timeout decision where increasing the threshold was chosen over increasing retries.
- Use that example when you need a compact reference for `decision`, `alternatives_considered`, `validation_run`, `remaining_risks`, and `follow_up` in this workflow.
