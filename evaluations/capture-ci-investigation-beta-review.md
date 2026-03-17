# capture-ci-investigation Beta Review

## Purpose

Use this review to check whether the beta `capture-ci-investigation` skill can produce a bounded CI summary without overclaiming.

The goal is not polished prose.
The goal is to confirm that the draft keeps observed evidence, current explanation, unknowns, and temporary action clearly separated.

## Suggested Cases

Review at least these public-safe CI shapes:

- `../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json`
- `../examples/linux-ci-rerun-watch/.ai/records/decisions/dec-20260316-linux-ci-rerun-watch-001.json`
- `../examples/macos-flaky-quarantine/.ai/records/decisions/dec-20260317-macos-flaky-quarantine-001.json`

## Review Questions

1. Does the summary clearly separate observed evidence from the current best explanation?
2. Does the summary keep weak or rerun-only evidence from sounding like a confirmed fix?
3. If the action changes shared workflow behavior, does the summary call out blast radius and follow-up?
4. Does the summary name the unknowns, remaining risk, or monitoring window instead of collapsing them into filler?
5. Does the summary say what would reopen deeper investigation or justify a stronger workflow change?

## Pass Criteria

The review passes if:

- strong-evidence cases can describe a likely cause without hiding the validating check
- weak-evidence cases stay monitor-first and do not claim root-cause certainty
- rerun-only success is described as urgency reduction, not proof of a fix
- shared workflow changes are described with blast radius and follow-up, not as isolated local edits
- the draft stays compact and does not pad empty sections with generic filler

## Failure Signals

Treat the review as weak or failed if:

- the draft says `fixed`, `confirmed`, or equivalent language without strong evidence
- evidence, explanation, uncertainty, and next action collapse into one undifferentiated paragraph
- the summary recommends timeout, retry, or quarantine changes without calling out what signal they could hide
- the summary leaves monitoring or next-check language vague when the evidence is still thin
- the draft cannot be completed correctly without relying on hidden runtime-only rules

## Notes

- Use this review alongside `skills/capture-ci-investigation/SKILL.md` and `skills/capture-ci-investigation/references/beta-boundaries.md`.
- If the same overclaim or filler pattern repeats, record it in `../.workspace/failure-modes.md`.
