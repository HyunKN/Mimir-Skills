---
name: dependency-upgrade-decision
description: Capture dependency-change decisions when a package upgrade, pin, rollback, or deferral crosses a trigger boundary. Use when a library version, lockfile, config contract, or release-note change requires explicit evidence about compatibility, validation, risk, and why one dependency path was chosen over alternatives.
---

# dependency-upgrade-decision

Use this skill when dependency or config changes need a canonical decision record with concrete engineering evidence.

## Workflow

1. Confirm that the task qualifies under `../../spec/trigger-taxonomy.md`, especially the dependency or config change trigger.
2. Read `../decision-capture/SKILL.md` if a new decision record must be created or updated from scratch.
3. Gather only the dependency-specific evidence needed for the choice: manifest diff, lockfile or config changes, release notes, validation runs, and risk notes.
4. Compare the real options, such as upgrade now, pin the current version, roll back, defer, or add a compatibility change.
5. Record the selected option, rationale, affected paths, validation, remaining risks, and follow-up in the public schema.
6. Validate the JSON record with `../decision-core/scripts/validate_decision_record.py <path>`.
7. Render Markdown only when another human or agent needs a short summary.

## Capture Focus

- Treat upgrade, pin, rollback, and defer decisions as record-worthy when they change behavior, delivery risk, or future work.
- Make the tradeoff explicit: compatibility, security, maintenance cost, and release timing.
- Keep evidence tied to concrete artifacts such as `package.json`, lockfiles, config files, release notes, and test or CI results.
- Record why rejected options lost when the dependency decision was non-trivial.

## Guardrails

- Do not reduce the record to "package updated" without the reason and impact.
- Do not claim compatibility without validation or cited release-note evidence.
- Do not hide security or migration risk just to justify a faster upgrade path.
- Do not treat dependency churn as trivial when it changes config contracts, generated artifacts, or operational behavior.
- Do not persist raw logs, secrets, or private registry details in the canonical record.

## Load References As Needed

- Read [`references/upgrade-playbook.md`](references/upgrade-playbook.md) when capturing upgrade, pin, rollback, or defer decisions.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when creating or updating a canonical record.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) when checking shared validation and safety rules.
- Read [`../../spec/decision-record-schema.md`](../../spec/decision-record-schema.md) when filling or reviewing fields.
- Read [`../../spec/trigger-taxonomy.md`](../../spec/trigger-taxonomy.md) when deciding whether a dependency change crosses a capture trigger.
- Inspect the public example under [`../../examples/cache-client-pin/.ai/records/decisions/dec-20260312-cache-client-pin-001.json`](../../examples/cache-client-pin/.ai/records/decisions/dec-20260312-cache-client-pin-001.json) when you need a concrete dependency/config record shape.
