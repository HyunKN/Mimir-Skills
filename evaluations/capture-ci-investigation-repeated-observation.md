# capture-ci-investigation Repeated Observation Review

## Purpose

Use this review after real local use of the `capture-ci-investigation` skill.

The goal is to decide whether repeated usage continues to keep evidence, explanation, uncertainty, and next action clearly separated without overclaiming or hidden runtime dependence.

This is not a one-off example review.
Use it as the running gate for quality assurance: whether repeated real usage maintains consistent four-lane separation, or whether the workflow needs tightening.

## When To Run

Run this review when one of the following happens:

- a real local CI investigation draft was produced from the skill-first path
- the workflow surface, beta boundary note, or public examples changed in a way that could affect wording or routing
- repeated confusion appears around wrapper-only behavior, monitor-first language, or shared-workflow mitigation wording

## Observation Checklist

Capture at least the following for each observed run:

1. What CI shape was involved?
   - config-backed failure
   - rerun-only monitoring case
   - shared-workflow mitigation case
   - another shape not yet represented in the public examples
2. Did the draft clearly separate:
   - observed evidence
   - current explanation
   - unknowns or remaining risk
   - current action or next check
3. Did the wording match the available evidence strength?
   - strong evidence did not skip validation
   - weak evidence did not sound like a confirmed fix
   - rerun-only success did not become root-cause language
4. If the action touched shared workflow behavior, did the draft call out:
   - blast radius
   - failure-visibility risk
   - follow-up owner or window
   - the signal that would justify reverting or tightening the change
5. Did the operator need hidden runtime-only rules to complete the draft correctly?
6. Did wrapper-only behavior remain acceptable for the run, or did the operator hit repeated friction that a dedicated direct-use helper would clearly reduce?

## Pass Criteria

The repeated-observation gate stays healthy if:

- multiple observed runs keep the four lanes separate without repeated overclaiming
- weak or monitor-first cases remain explicit about uncertainty
- shared-workflow mitigations keep blast radius and follow-up visible
- the skill-first path remains usable without needing hidden runtime-only rules
- wrapper-only behavior does not show repeated, concrete UX friction strong enough to justify a new direct-use helper surface

## Failure Signals

Treat the gate as weak or regressing if:

- the same overclaiming or filler pattern appears across more than one observed run
- operators repeatedly need to invent missing rules that are not in `SKILL.md` or `beta-boundaries.md`
- wrapper-only usage causes repeated friction that is more than minor path or reading overhead
- shared-workflow mitigation drafts repeatedly omit blast radius, follow-up, or visibility tradeoffs
- public examples no longer feel representative of the observed CI shapes

## Notes

- Use this review together with `capture-ci-investigation-beta-review.md`.
- If a repeated issue shows up here, record it in `../.workspace/failure-modes.md`.
- If a new CI shape appears repeatedly, consider whether the public examples need another anchor before changing the product surface.

## Graduation Assessment (2026-03-17)

Summary: Three public CI examples reviewed against the observation checklist.

- `windows-ci-timeout`
  - CI shape type: config-backed
  - 4-lane separation verdict: pass - observed evidence, current explanation, unknowns, and current action stay explicitly separated.
  - Evidence-strength wording correctness: strong-evidence wording remains likely/validated and avoids certainty overreach.
  - Shared workflow blast-radius coverage: not applicable for this case.

- `linux-ci-rerun-watch`
  - CI shape type: rerun-only monitoring
  - 4-lane separation verdict: pass - rerun success is kept as urgency reduction while uncertainty and monitoring remain explicit.
  - Evidence-strength wording correctness: weak-evidence wording avoids fixed/root-cause claims.
  - Shared workflow blast-radius coverage: not applicable because no shared-workflow change was made.

- `macos-flaky-quarantine`
  - CI shape type: shared-workflow mitigation
  - 4-lane separation verdict: pass - repeated evidence, leading explanation, residual uncertainty, and mitigation/follow-up are clearly split.
  - Evidence-strength wording correctness: medium-to-strong framing stays bounded and ties claims to available checks.
  - Shared workflow blast-radius coverage: covered with affected scope, failure-visibility risk, and follow-up/revert signals.

Conclusion: All three examples pass the repeated-observation checklist. The four-lane separation is consistent across strong, medium, and weak evidence tiers. No overclaiming detected. Gate: PASS.
