# write-pr-rationale Decision Rules

1. Start with an epistemic guardrail, not with a signal table.
   Treat all inferred goals, signal-based reviewer notes, and signal-based risks as temporary substitutes when explicit `--why` notes are missing.
   Write `this branch appears to...`, `local branch evidence suggests...`, or `review should check...`, not `this branch does...` or `the author intended...`.
2. Let explicit rationale inputs win.
   Explicit rationale can arrive as user notes, helper-command flags such as `--why`, issue or incident context, editor context, or linked decision records.
   When that explicit rationale exists, treat it as higher-confidence input than any local inference.
3. Use the narrowest truthful evidence source and name it.
   Prefer the current working-tree diff first, then committed branch-range context when the tree is clean, then recent committed work only when both diff layers are clean.
4. Keep the draft reviewer-shaped.
   Separate what changed, why it changed, what was validated, what reviewers should watch, and what still needs follow-up instead of blending them into one branch summary.
5. Use local signals only as cautious prompts.
   File paths and commit subjects can suggest `docs`, `workflow`, `runtime`, `adapter`, `ci`, `dependency/config`, `examples/evaluation`, `spec`, or `rename`, but those signals are reviewer-orientation hints, not proof of author intent.
6. Surface clean-state context instead of filler.
   When the working tree is already clean, show committed branch-range or recent committed work explicitly instead of pretending there is no meaningful context.
7. End in uncertainty rather than overclaim.
   If explicit intent or validation is still missing after local inspection, say so plainly and ask for the missing rationale note before external sharing.

## Output Template

Use this shape and keep every section truthful to the evidence source you actually used:

### `PR Snapshot`

- repository, branch, base reference, and HEAD

### `What Changed`

- if the working tree is dirty: summarize changed files, notable name-status entries, untracked files, and diff stats
- if the working tree is clean: explicitly say the draft is using committed branch-range or recent-commit fallback context

### `Evidence`

- name the primary evidence source
- add nearby commit or branch signals only when they help the reviewer orient quickly

### `Why This Changed`

- if explicit `--why` notes exist: use them directly and do not add inferred-intent filler
- otherwise: state a tentative inferred goal, mention the strongest local signals and touched areas, and end with a prompt to replace or tighten the rationale with explicit `--why`

### `Validation`

- include explicit validation notes when they exist
- otherwise: keep missing validation visible and add the smallest reviewer-relevant validation prompt for the detected signal set

### `Reviewer Notes`

- point reviewers to the main watch areas implied by the evidence source and the local signals
- clean-state runs should explicitly tell reviewers when to anchor on committed branch-range or recent commits instead of uncommitted diff

### `Risks and Follow-Up`

- if explicit risks exist: use them directly
- otherwise: keep the missing-intent risk visible when `--why` is absent, then add only the highest-signal follow-up risks
