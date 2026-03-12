# Memory Promotion Evaluation

## Purpose

Use this evaluation to check whether a fresh agent or reviewer can understand why a reusable lesson stayed a candidate or became validated memory, and whether the validation and freshness boundaries are still clear.

## Example Under Test

Use the public-safe synthetic memory-promotion example under:

- `../examples/cache-client-tls-memory/.ai/records/decisions/dec-20260320-cache-client-v43-migration-003.json`
- `../examples/cache-client-tls-memory/.ai/records/reports/cache-client-tls-memory-summary.md`
- `../examples/cache-client-tls-memory/.ai/records/memories/candidates/mem-20260320-cache-client-tls-contract-001.json`
- `../examples/cache-client-tls-memory/.ai/records/memories/validated/mem-20260320-cache-client-tls-contract-001.json`

## Evaluator Instructions

Give the evaluator the source decision record, the rendered summary, and both the candidate and validated memory artifacts.
Do not provide the original implementation transcript or hidden local notes.

Ask the evaluator to answer:

1. What reusable lesson was extracted from the source decisions?
2. Which decision records support that lesson?
3. Why is the lesson strong enough to become validated memory instead of remaining only a candidate?
4. What current-state validation supports the validated artifact?
5. What freshness or revalidation boundary limits reuse of the lesson?
6. What should trigger another review, demotion, or removal?

## Pass Criteria

The evaluation passes if the evaluator can correctly recover:

- the reusable lesson being promoted
- the provenance trail back to the source decision records
- the current-state validation basis for the validated artifact
- the freshness or revalidation rule that bounds reuse
- the condition under which the memory should be revisited, demoted, or removed

## Failure Signals

The evaluation should be considered weak or failed if the evaluator:

- cannot trace the memory back to the source decision records
- treats the candidate and validated artifacts as equivalent without noticing the added validation basis
- ignores freshness or revalidation guidance
- invents evidence, guarantees, or long-term rules not present in the artifacts

## Notes

- Use this evaluation after running `python scripts/verify_examples.py` if the example artifacts changed.
- The goal is conservative reuse: the evaluator should understand both why the memory is useful and why it is still bounded.
