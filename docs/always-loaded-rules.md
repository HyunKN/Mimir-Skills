# Always-Loaded Rules

## Purpose

This document is the compact always-loaded baseline for `Mimir-Skills`.

It is intentionally short.
It is not a large constitution or a replacement for the deeper workflow, spec, example, or evaluation documents.

Use it as the minimum rule layer that should stay visible when a shared CLI run, future adapter, or future entry surface invokes the repository workflows.

## Baseline Rules

1. Treat outputs as drafts, not final truth.
2. Prefer the skill-first surface first:
   - choose the workflow through `docs/workflow-trigger-table.md`
   - read the selected workflow `SKILL.md` before reaching for helper code
3. Use `prepare-handoff` when the user needs a continuation summary from local branch or working-tree context.
4. Use `write-pr-rationale` when the user needs a reviewer-facing explanation of what changed, why it changed, what was validated, and what still needs attention. Keep inferred rationale tentative unless explicit `why` context exists.
5. Use `capture-ci-investigation` as a bounded best-effort investigation summary. Keep evidence and uncertainty separate, and do not promise root-cause certainty.
6. Canonical decision records outrank rendered summaries and workflow drafts.
7. Do not claim rationale, validation, or confidence that cannot be tied to local evidence.
8. If local branch context is too thin, add explicit rationale or evidence notes instead of filling the gap with generic prose.
9. Do not persist secrets, credentials, raw sensitive logs, or unnecessary private output.
10. Say when validation is missing, incomplete, or still uncertain.
11. Use thin collectors or validators only when deterministic local evidence adds value; do not treat deprecated generator stubs as the primary workflow path.

## Boundary

- This rules layer should stay map-like.
- Detailed workflow behavior belongs in `SKILL.md`, `docs/`, `spec/`, `examples/`, and `evaluations/`.
- Future adapters may mirror or embed this baseline, but they should not fork it silently.
