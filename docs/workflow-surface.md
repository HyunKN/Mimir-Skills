English | [한국어](workflow-surface.ko.md)

# Workflow Surface

## Purpose

This document defines the outward-facing workflow surface being built for `decision-skills` v1.

The repository already contains internal building blocks and workflow-specific skills.
This document explains how those current internals map to the simpler public workflow story.

## Public Workflow Surface

The first public workflow surface centers on three user-facing workflows:

- `prepare-handoff`
- `write-pr-rationale`
- `capture-ci-investigation`

These names describe the visible output a user wants, not the current internal package names.

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
- an initial user-facing skill skeleton now exists under `skills/prepare-handoff/`
- a shared CLI entry now exists under `python -m decision_skills prepare-handoff`
- the first local context collectors and direct Markdown output scripts now exist under `skills/prepare-handoff/scripts/`
- a first Codex-local install path now exists under `adapters/codex/scripts/install_codex_skills.py`
- the second observation pass showed that the shared CLI path is lower-friction than the current Codex-local path for this workflow
- the current clean-state checkpoint shape is approaching guidance-ready status, but one more non-clean task-state confirmation is still planned before calling it stable public guidance
- broader multi-agent packaging is still not implemented

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
- a shared CLI entry now exists under `python -m decision_skills write-pr-rationale`
- the first local PR-context collectors and direct Markdown output scripts now exist under `skills/write-pr-rationale/scripts/`
- a first Codex-local install path now exists under `adapters/codex/scripts/install_codex_skills.py`
- the second observation pass showed that the shared CLI path is lower-friction than the current Codex-local path for this workflow
- the current clean-state rationale still needs heavier rewrite than `prepare-handoff`, especially when explicit `why` context is missing
- this workflow remains in active output shaping and should not yet be treated as stable public guidance for clean-state runs
- broader multi-agent packaging is still not implemented

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
- the workflow now appears in `python -m decision_skills list` as a beta wrapper, but it does not yet expose a direct shared CLI generation command
- the first Codex-local install path can now include this workflow through `adapters/codex/scripts/install_codex_skills.py`
- dedicated direct-use scripts are intentionally not implemented yet
- this remains a narrower best-effort direction until stronger examples and reliability boundaries exist

## Supporting Internal Skills

Some current skills stay important but are not part of the first outward-facing product promise:

- `dependency-upgrade-decision` remains a specialized support workflow for dependency and config changes
- `memory-promote` remains a supporting layer for validated reusable lessons after repeated evidence and review

These should stay in the repository, but they should not lead the first public product story.

## Transition Rule

During the v0.1 to v1 transition:

- public docs should describe the user-facing workflow outputs
- internal skills may keep their current implementation-oriented names
- new user-facing skills can be added on top of the current internals instead of replacing them immediately

The goal is to simplify adoption without throwing away the current internal engine.
