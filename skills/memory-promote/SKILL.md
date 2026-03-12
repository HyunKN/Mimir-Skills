---
name: memory-promote
description: Review and promote reusable lessons from validated decision records into bounded project memory. Use when one or more decisions seem useful beyond a single task and the agent must decide whether to keep the lesson as a candidate, validate it, defer promotion, or demote stale memory based on provenance, evidence, current-state checks, safety, and freshness.
---

# memory-promote

Use this skill when reusable lessons should be evaluated for candidate or validated project memory.

## Workflow

1. Confirm that the lesson starts from one or more concrete decision records rather than free-form notes.
2. Read `../../spec/memory-promotion-policy.md` before creating, promoting, demoting, or discarding any memory artifact.
3. Gather the minimum promotion evidence: `source_decision_ids`, `evidence_refs`, current-state validation, safety review, and freshness or revalidation guidance.
4. Decide whether the lesson should stay a candidate, be promoted to validated memory, or be rejected or demoted.
5. Write only the minimal candidate or validated artifact needed for the chosen state.
6. Run `scripts/validate_memory_artifact.py <path>` when a concrete candidate or validated memory JSON file needs contract validation.
7. Re-check the lesson against the current repository or branch state before promotion.
8. Keep promotion explicit and conservative; do not infer long-term memory by default.

## Promotion Focus

- Promote only lessons that reduce repeated work or repeated risk beyond one task.
- Keep provenance and evidence obvious enough that a future agent can trace the lesson back to the underlying decision.
- Treat freshness as a first-class part of the memory contract, especially for volatile workflow or environment facts.
- Prefer candidate status when reuse value is plausible but current-state validation is still thin.

## Guardrails

- Do not promote memory from summaries or notes alone; require decision-record provenance.
- Do not promote one-off workarounds, branch-local quirks, or unverified preferences as durable memory.
- Do not store secrets, raw logs, or hidden reasoning in candidate or validated memory artifacts.
- Do not validate a lesson without checking whether the current repository state still supports it.
- Do not leave volatile memory without freshness or revalidation guidance.

## Load References As Needed

- Read [`references/promotion-playbook.md`](references/promotion-playbook.md) when deciding whether a lesson should stay a candidate, be promoted, or be demoted.
- Run [`scripts/validate_memory_artifact.py`](scripts/validate_memory_artifact.py) when validating one or more candidate or validated memory JSON files.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) when checking shared validation, safety, and redaction constraints.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when the source decision record is missing or incomplete.
- Read [`../../spec/memory-promotion-policy.md`](../../spec/memory-promotion-policy.md) when checking candidate and validated memory requirements.
- Read [`../../spec/memory-artifact-schema.json`](../../spec/memory-artifact-schema.json) when a tool or editor needs the machine-readable companion contract for candidate or validated memory artifacts.
- Read [`../../spec/decision-record-schema.md`](../../spec/decision-record-schema.md) when tracing the lesson back to the source decision records.
- Inspect the public example under [`../../examples/cache-client-tls-memory/`](../../examples/cache-client-tls-memory/) when you need a concrete candidate-to-validated memory flow.
