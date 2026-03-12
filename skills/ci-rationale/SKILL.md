---
name: ci-rationale
description: Capture CI triage decisions when failing jobs, flaky tests, build regressions, or workflow config changes cross a trigger boundary. Use when the agent must record the root-cause hypothesis, compared remediation options, validating reruns, affected workflow files, and remaining CI risk in a canonical decision record.
---

# ci-rationale

Use this skill when CI, build, or test-workflow incidents need a canonical decision record with concrete operational evidence.

## Workflow

1. Confirm that the task qualifies under `../../spec/trigger-taxonomy.md`, especially the CI, build, or test strategy trigger.
2. Read `../decision-capture/SKILL.md` if a new decision record must be created or updated from scratch.
3. Gather only the CI-specific evidence needed for the decision: failing job links, workflow or config files, reruns, local reproduction, and timing or environment notes.
4. Compare the real options, such as fix the root cause, tune timeout or retry policy, revert a workflow change, quarantine the failure, or defer with follow-up.
5. Record the selected option, rationale, affected paths, validation, remaining risks, and follow-up in the public schema.
6. Validate the JSON record with `../decision-core/scripts/validate_decision_record.py <path>`.
7. Render Markdown only when another human or agent needs a short handoff or review summary.

## Capture Focus

- Distinguish the root cause from the symptom. Record whether the issue was a timeout, flake, misconfiguration, regression, or infra-related variance.
- Keep evidence tied to concrete CI artifacts such as job IDs, workflow files, commands, reruns, and timing observations.
- Make it explicit whether the chosen action fixes, mitigates, hides, or defers the CI problem.
- Record follow-up monitoring when the CI decision changes retries, timeouts, or other shared workflow settings.

## Guardrails

- Do not reduce the record to "reran and passed" without explaining why that evidence matters.
- Do not hide flaky behavior by increasing retries or timeouts without rationale and validation.
- Do not mark a CI issue as fixed without a validating rerun, reproduction, or equivalent evidence.
- Do not persist full raw logs, secrets, or private infrastructure details in the canonical record.
- Do not treat shared workflow changes as trivial when they affect other jobs, platforms, or future debugging.

## Load References As Needed

- Read [`references/ci-playbook.md`](references/ci-playbook.md) when capturing CI triage, timeout, retry, rollback, or quarantine decisions.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when creating or updating a canonical record.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) when checking shared validation and safety rules.
- Read [`../../spec/decision-record-schema.md`](../../spec/decision-record-schema.md) when filling or reviewing fields.
- Read [`../../spec/trigger-taxonomy.md`](../../spec/trigger-taxonomy.md) when deciding whether the CI work crosses a capture trigger.
- Inspect the public example under [`../../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json`](../../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json) when you need a concrete CI decision-record shape.
