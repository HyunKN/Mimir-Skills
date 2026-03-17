# Workflow Surface

## Purpose

This document defines the outward-facing skill surface being built for `Mimir-Skills` v1.

The repository already contains internal building blocks, workflow-specific skills, and optional local helper code.
This document explains how those pieces map to the simpler public skill story and which surfaces are now primary versus secondary.

## Public Workflow Surface

The first public skill surface centers on three user-facing workflows:

- `prepare-handoff`
- `write-pr-rationale`
- `capture-ci-investigation`

These names describe the visible output a user wants, not the current internal package names.
The primary source of truth should move toward `SKILL.md` and companion references, with runtime helpers treated as optional local utilities.
Use [`workflow-trigger-table.md`](workflow-trigger-table.md) when the first question is which public workflow should be loaded at all.

## Workflow Mapping

### `prepare-handoff`

User-facing goal:

- draft a handoff from the current branch state
- explain what changed, what remains, where to continue, and what risks or blockers remain

Current internal building blocks:

- `handoff-context`
- `decision-capture`
- `decision-core`

Current status:

- public workflow name is defined
- the primary user-facing skill now exists under `skills/prepare-handoff/`
- the skill and handoff playbook now carry the main dirty-tree, clean branch-range, and recent-commit fallback rules directly
- docs-only reproduction now succeeds for the three representative branch-state cases above, so the runtime is no longer the only source of truth for this workflow's decision rules
- the first runtime-reduction pass now keeps only git-context collection in the helper runtime
- local helper commands still exist, but `python -m mimir_skills prepare-handoff` and `skills/prepare-handoff/scripts/generate_handoff.py` now emit deprecation guidance instead of handoff Markdown
- the remaining live helper path is `skills/prepare-handoff/scripts/collect_git_context.py`
- the Codex-local install path under `adapters/codex/scripts/install_codex_skills.py` remains only an optional thin-adapter proof point
- this workflow now follows the same skill-first plus thin-collector pattern as `write-pr-rationale`
- broader multi-agent packaging is still not implemented and is no longer the main short-term story

### `write-pr-rationale`

User-facing goal:

- draft reviewer-facing rationale from the current branch diff and validation context
- explain what changed, why it changed, what was validated, and what reviewers should watch

Current internal building blocks:

- `pr-rationale`
- `decision-capture`
- `decision-core`

Current status:

- public workflow name is defined
- an initial user-facing skill now exists under `skills/write-pr-rationale/`
- the user-facing skill and PR playbook now carry the main inference guardrails, signal patterns, and reviewer-facing output template
- the first runtime-reduction pass now keeps only git-context collection in the helper runtime
- local helper commands still exist, but `python -m mimir_skills write-pr-rationale` and `skills/write-pr-rationale/scripts/generate_pr_rationale.py` now emit deprecation guidance instead of reviewer-facing Markdown
- the remaining live helper path is `skills/write-pr-rationale/scripts/collect_pr_context.py`
- the Codex-local install path under `adapters/codex/scripts/install_codex_skills.py` remains only an optional thin-adapter proof point
- the current clean-state rationale still needs heavier rewrite than `prepare-handoff`, especially when explicit `why` context is missing
- the first skill-first codification pass now exists, with the epistemic guardrail placed ahead of the local signal map so inferred intent is treated as tentative by default
- the first local agent-validation gate also passed across dirty-tree, clean branch-range, recent-commit fallback, and explicit-`why` override cases without needing extra runtime-only rules
- this workflow can now move toward thin-collector status, but should still not yet be treated as stable public guidance for clean-state runs, because explicit product or tradeoff intent still needs a user-supplied `why` note more often than `prepare-handoff` needs extra context
- broader multi-agent packaging is still not implemented and is no longer the main short-term story

### `capture-ci-investigation`

User-facing goal:

- draft a bounded CI investigation summary from available failure context
- explain what failed, what evidence exists, what the current best explanation is, and what temporary next step was taken

Current internal building blocks:

- `ci-rationale`
- `decision-capture`
- `decision-core`

Current status:

- public workflow name is defined
- an initial beta user-facing skill now exists under `skills/capture-ci-investigation/`
- the beta skill, examples, and boundary notes are the primary public surface today
- the beta skill now carries explicit evidence-tier wording rules, shared-workflow blast-radius checks, and monitor-first output guidance directly in the skill plus boundary note
- a dedicated beta review anchor now exists at `evaluations/capture-ci-investigation-beta-review.md` so uncertainty separation and anti-overclaiming can be re-checked later
- the workflow still appears in `python -m mimir_skills list` as a beta wrapper, but it does not yet expose a direct shared CLI generation command
- the first Codex-local install path can still include this workflow through `adapters/codex/scripts/install_codex_skills.py`, but that remains optional and secondary
- the beta guidance now points at both a stronger config-backed CI example and a weaker rerun-only monitoring example, so the overclaim boundary is more explicit
- dedicated direct-use scripts are intentionally not implemented yet
- this remains a narrower best-effort direction until stronger examples and reliability boundaries exist

Beta graduation note:

- keep it beta until it has multiple public-safe examples across different CI failure shapes
- keep it beta until either a direct-use path exists or wrapper-only remains an explicit product decision
- keep it beta until repeated observations show it can separate evidence, explanation, uncertainty, and next step without repeated overclaiming

## Supporting Internal Skills

Some current skills stay important but are not part of the first outward-facing product promise:

- `dependency-upgrade-decision` remains a specialized support workflow for dependency and config changes
- `memory-promote` remains a supporting layer for validated reusable lessons after repeated evidence and review

These should stay in the repository, but they should not lead the first public product story.

## Helper Surface Note

Secondary helper surfaces still exist and remain useful for local experimentation:

- `mimir_skills/` shared CLI commands
- `skills/*/scripts/` direct collectors or generators
- `adapters/codex/scripts/install_codex_skills.py` as an optional thin-adapter proof point

These helper surfaces should support the skills, not define them. The intended direction is for workflow judgment to live in `SKILL.md` and references first, with runtime code shrinking toward thin collectors or deterministic helpers.

## Routing Note

The public routing order is now:

1. choose the visible workflow through [`workflow-trigger-table.md`](workflow-trigger-table.md)
2. load that workflow's `SKILL.md`
3. load the companion reference only when the draft needs more detailed output or boundary guidance
4. use thin collectors or validators only when deterministic local evidence still adds value

## Transition Rule

During the v0.1 to v1 transition:

- public docs should describe user-facing workflow outputs through the skill documents first
- internal skills may keep their current implementation-oriented names while the public story moves toward skill-first naming
- local helper code may remain temporarily, but it should become secondary to the skill docs rather than the main product surface
- new user-facing skills can still be added on top of the current internals instead of replacing them immediately

The goal is to simplify adoption without losing the current validation and collection utilities that still add deterministic value.
