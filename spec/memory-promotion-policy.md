# Memory Promotion Policy v0.1

## Purpose

This policy defines how reusable lessons move from decision records into bounded project memory.
Memory is a derived layer. It should never be treated as raw truth without validation.

Machine-readable companion schema:

- `memory-artifact-schema.json`

## Artifact Flow

```text
decision record(s) -> memory candidate -> validated memory
```

- Decision records are the only allowed source for shared project memory.
- Promotion is explicit in v0.1. It is not automatic.
- If a lesson does not pass the gates below, it stays a candidate or is discarded.

## Storage Locations

- Candidates: `.ai/records/memories/candidates/`
- Validated memory: `.ai/records/memories/validated/`

## Candidate Minimum Contract

Each candidate should include:

- `id`
- `statement`
- `scope`
- `source_decision_ids`
- `evidence_refs`
- `confidence`
- `created_at`
- `status` set to `candidate`

## Validated Memory Minimum Contract

Each validated memory entry should include everything from the candidate plus:

- `validated_at`
- `validation_basis`
- `last_validated_at`
- `freshness`
- `status` set to `validated`

`freshness` may include an expiry date or a revalidation interval for volatile knowledge.

## Promotion Gates

Promote a candidate only when all gates pass:

1. Provenance: the lesson cites one or more decision records through `source_decision_ids`.
2. Evidence: the lesson has supporting `evidence_refs`, not summary-only claims.
3. Reuse value: the lesson is likely to help beyond one isolated task.
4. Current validity: the lesson has been checked against the current repository or branch state.
5. Safety: the lesson does not expose secrets, unsafe private reasoning, or unnecessary sensitive details.
6. Freshness: the lesson has a revalidation or expiry strategy if it can become stale.

## Demotion and Archival

A validated memory should be demoted back to candidate or archived when:

- the referenced decision has been superseded
- the underlying code, workflow, or environment changed materially
- the lesson no longer saves time or reduces risk
- the safety classification changes

## Allowed Memory Shapes

v0.1 supports memory statements that look like:

- stable project rules
- durable workflow facts
- repeatedly verified environment constraints

v0.1 should avoid promoting:

- one-off task notes
- branch-local temporary workarounds with no future value
- unverified personal preferences

## Review Questions

Before promoting, ask:

1. Can a new agent follow the memory back to the original decision record?
2. Is the claim backed by evidence that still matches the current repo state?
3. Would the memory help on a future task without restating a whole decision log?
4. Is the memory safe to expose to future agents?

If any answer is no, do not promote.
