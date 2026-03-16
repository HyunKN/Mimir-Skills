English | [한국어](always-loaded-rules.ko.md)

# Always-Loaded Rules

## Purpose

This document is the compact always-loaded baseline for `decision-skills`.

It is intentionally short.
It is not a large constitution or a replacement for the deeper workflow, spec, example, or evaluation documents.

Use it as the minimum rule layer that should stay visible when a shared CLI run, future adapter, or future entry surface invokes the repository workflows.

## Baseline Rules

1. Treat outputs as drafts, not final truth.
2. Prefer the shared CLI surface first:
   - `python -m decision_skills prepare-handoff`
   - `python -m decision_skills write-pr-rationale`
3. Use `prepare-handoff` when the user needs a continuation summary from local branch or working-tree context.
4. Use `write-pr-rationale` when the user needs a reviewer-facing explanation of what changed, why it changed, what was validated, and what still needs attention.
5. Use `capture-ci-investigation` only as a narrower best-effort investigation summary. It is still beta and does not promise root-cause certainty.
6. Canonical decision records outrank rendered summaries and workflow drafts.
7. Do not claim rationale, validation, or confidence that cannot be tied to local evidence.
8. If local branch context is too thin, add explicit rationale or evidence notes instead of filling the gap with generic prose.
9. Do not persist secrets, credentials, raw sensitive logs, or unnecessary private output.
10. Say when validation is missing, incomplete, or still uncertain.

## Boundary

- This rules layer should stay map-like.
- Detailed workflow behavior belongs in `SKILL.md`, `docs/`, `spec/`, `examples/`, and `evaluations/`.
- Future adapters may mirror or embed this baseline, but they should not fork it silently.
