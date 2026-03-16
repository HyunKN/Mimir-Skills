English | [한국어](project-one-pager.ko.md)

# Project One-Pager

## What `Mimir-Skills` Is

`Mimir-Skills` is a skill-first repository for AI-agent decision traceability.

It helps teams preserve why meaningful engineering changes were made, not just what changed, by giving local-file agents reusable workflow skills, playbooks, examples, and deterministic validators.

## The Problem

Modern coding agents can leave behind logs, diffs, and test output.
Those artifacts are useful, but they rarely capture the full operating context:

- the decision being made
- the rejected alternatives
- the evidence consulted
- the validation performed
- the remaining risk
- the handoff context for the next agent or engineer

This creates a gap between activity logging and reusable decision context.

## Product Thesis

The project is built on six claims:

1. Logs alone are not enough.
2. High-impact decisions should be captured in a structured form.
3. The canonical record should be AI-readable first.
4. Human-readable summaries should be rendered from the same source.
5. Long-term memory should be promoted from validated records, not written directly as truth.
6. Workflow judgment rules should live in `SKILL.md` and references whenever local-file agents can read them directly; code should be reserved for deterministic validation or thin collection helpers.

## What Ships in Public v0.1

- English-first public docs, plus Korean companions for the root README and a small overview subset under `docs/`
- skill-first workflow packages under `skills/`
- a glossary for shared terminology
- a trigger taxonomy for deciding what to record
- a canonical decision record schema
- a memory promotion policy
- public-safe examples and evaluations
- deterministic validation helpers for schemas, examples, and memory artifacts
- optional local helper surfaces under `mimir_skills/` and `skills/*/scripts/`

## What Does Not Ship Yet

- hosted services or central coordination
- automatic memory promotion from every observation
- adapter coverage for every agent platform
- storage of hidden reasoning or unsafe private details
- a large workflow runtime that tries to own judgment instead of the skill docs

## Initial Use Cases

- CI failure triage with explicit rationale and validation
- multi-file refactors that need durable handoff context
- PR-ready summaries rendered from machine-readable records
- project memory created only after repeated validation

## Why the Repository Is Bilingual

- GitHub needs a clear default entry point for global readers.
- Korean companions are kept only for the root README and a small entry or overview subset under `docs/`, currently `project-one-pager`, `quick-start`, and `glossary`.
- English remains the source of truth so detailed docs, specs, schemas, skills, evaluations, and future packaging can stay consistent.

## Near-Term Roadmap

1. Finish the skill-first direction reset in the public docs.
2. Continue moving the remaining workflow judgment rules out of runtime code and into `SKILL.md` plus references, with `write-pr-rationale` now on its first skill-first pass and runtime reduction still ahead.
3. Keep deterministic validators and example verification stable while runtime code shrinks toward thin collectors.
4. Treat adapter paths as optional proof points, not as the main product story.
5. Expand workflow-specific skills only when the skill docs and examples stay stronger than the runtime they replace.

## What Success Looks Like

A new contributor or agent should be able to open this repository, read a small set of docs, and immediately understand:

- what should be recorded
- how it should be stored
- how summaries are derived
- how memory is promoted safely
- where the first skills and examples should be added
- which parts are primary skill guidance and which parts are only optional local helpers
