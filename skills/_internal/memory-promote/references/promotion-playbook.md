# Promotion Playbook

## Use This Reference For

- deciding whether a lesson should remain a candidate
- promoting a candidate into validated memory
- demoting or archiving stale memory
- turning one or more decision records into one reusable lesson

## Promotion Sequence

1. Select the source decision records.
2. Write the candidate statement and scope in the narrowest useful form.
3. Check the evidence quality and reuse value.
4. Validate the lesson against the current repository or branch state.
5. Review safety and freshness requirements.
6. Choose the final state: candidate, validated, rejected, demoted, or archived.

## Candidate Checklist

- `statement`
- `scope`
- `source_decision_ids`
- `evidence_refs`
- `confidence`
- `created_at`
- `status` set to `candidate`

## Validated Checklist

- everything in the candidate checklist
- `validated_at`
- `validation_basis`
- `last_validated_at`
- `freshness`
- `status` set to `validated`

## Decision Patterns

### Keep as Candidate

- use when the lesson looks reusable but still needs stronger current-state validation
- prefer this state when the rule might still change soon

### Promote to Validated

- use when provenance, evidence, reuse value, safety, and freshness all pass
- make the validation basis explicit so a future agent can trust the promotion

### Reject or Discard

- use when the lesson is too narrow, too stale, unsafe, or not actually reusable
- avoid keeping low-value memory artifacts just because a candidate was drafted

### Demote or Archive

- use when a once-valid lesson has been superseded, invalidated, or made obsolete
- preserve traceability without letting stale memory remain authoritative

## Risk Patterns

- a one-off workaround presented as a durable rule
- evidence tied to superseded code or workflow behavior
- memory promoted without freshness guidance
- secret-bearing or overly detailed lessons
- promotion without an actual current-state check

## Example Gap

- No public candidate-to-validated example is published yet.
- Treat promotion conservatively until the first example shows the full artifact flow.
