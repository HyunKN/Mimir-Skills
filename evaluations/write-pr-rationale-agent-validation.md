# Write-PR-Rationale Agent Validation

## Purpose

Use this evaluation before shrinking the `write-pr-rationale` runtime.

The goal is to confirm that a local-file agent can follow:

- `../skills/write-pr-rationale/SKILL.md`
- `../skills/pr-rationale/references/pr-playbook.md`

and produce a reviewer-facing PR rationale that stays aligned with the current runtime behavior without treating inferred intent as fact.

## Inputs Under Test

Primary references:

- `../skills/write-pr-rationale/SKILL.md`
- `../skills/pr-rationale/references/pr-playbook.md`

Optional supporting references:

- `../skills/pr-rationale/SKILL.md`
- `reviewer-comprehension.md`

Do not require the evaluator to read the runtime code first. The point is to test whether the skill-first documents stand on their own.

## Representative Cases

### Case A: Dirty Working Tree, Mixed Docs and Runtime Changes

Use a local branch state with:

- uncommitted file changes present
- at least one workflow or runtime path touched
- at least one docs or skill path touched
- no explicit `why` note

### Case B: Clean Branch Range, Docs-Only or Guidance-Only Change

Use a local branch state with:

- no current working-tree diff
- a committed branch-range diff against the detected base
- docs, README, or skill-guidance files as the main touched area
- no explicit `why` note

### Case C: Recent-Commit Fallback Only

Use a local branch state with:

- no current working-tree diff
- no committed branch-range diff against the detected base
- recent committed work available as fallback context
- no explicit `why` note

### Case D: Explicit Rationale Override

Repeat one of the cases above, but add an explicit rationale note from the user, issue, incident, or helper-command input.

## Evaluation Questions

For each case, ask:

1. Did the agent choose the correct evidence layer?
2. Did the agent keep inferred `why` language tentative instead of definitive?
3. Did the agent preserve the expected section structure:
   - `PR Snapshot`
   - `What Changed`
   - `Evidence`
   - `Why This Changed`
   - `Validation`
   - `Reviewer Notes`
   - `Risks and Follow-Up`
4. Did the agent keep reviewer notes and risks tied to the observed signal set?
5. Did the agent avoid empty or filler-only sections when evidence was thin?
6. In the explicit-rationale case, did the explicit `why` replace inferred-intent filler?

## Pass Criteria

The evaluation passes if, across the representative cases:

- the agent chooses the same evidence priority the runtime uses
- inferred rationale is always framed as tentative when explicit intent is missing
- explicit rationale overrides local inference cleanly
- reviewer notes and risks stay consistent with the local signal map
- no section collapses into obviously generic filler
- no section is left empty without explanation

## Failure Signals

Treat the result as weak or failed if:

- inferred intent is written as confirmed fact
- the agent uses recent commits when a live diff or branch-range diff was available
- explicit rationale is ignored because the agent treats `--why` as CLI-only
- reviewer notes or risks drift away from the detected signal set
- the output contains empty headings or filler-only sections
- the agent must read runtime code to complete the draft correctly

## Notes

- This evaluation is a guardrail gate, not a final “stable public guidance” declaration.
- Passing this evaluation means the skill-first documents are strong enough to support the next runtime-reduction step.
- Failing this evaluation means the missing rule should be added to the skill documents or playbook before runtime logic is removed.
