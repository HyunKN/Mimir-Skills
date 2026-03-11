English | [한국어](project-one-pager.ko.md)

# Project One-Pager

## What `decision-skills` Is

`decision-skills` is an open documentation and skill-design project for AI-agent decision traceability.

It helps teams preserve why meaningful engineering changes were made, not just what changed.

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

The project is built on five claims:

1. Logs alone are not enough.
2. High-impact decisions should be captured in a structured form.
3. The canonical record should be AI-readable first.
4. Human-readable summaries should be rendered from the same source.
5. Long-term memory should be promoted from validated records, not written directly as truth.

## What Ships in Public v0.1

- bilingual README and project docs
- a glossary for shared terminology
- a trigger taxonomy for deciding what to record
- a canonical decision record schema
- a memory promotion policy
- starter template and directory structure for future skills and examples

## What Does Not Ship Yet

- hosted services or central coordination
- automatic memory promotion from every observation
- support for every agent platform
- storage of hidden reasoning or unsafe private details

## Initial Use Cases

- CI failure triage with explicit rationale and validation
- multi-file refactors that need durable handoff context
- PR-ready summaries rendered from machine-readable records
- project memory created only after repeated validation

## Why the Repository Is Bilingual

- GitHub needs a clear default entry point for global readers.
- Korean documentation is a first-class companion, not an afterthought.
- English remains the source of truth so specs, schemas, and future packaging can stay consistent.

## Near-Term Roadmap

1. Stabilize the core docs and terms.
2. Publish `decision-core` and `decision-capture` scaffolding.
3. Add one end-to-end example using canonical JSON and rendered Markdown.
4. Add replay-style evaluations for handoff quality.
5. Expand into workflow-specific skills only after the core record model proves useful.

## What Success Looks Like

A new contributor or agent should be able to open this repository, read a small set of docs, and immediately understand:

- what should be recorded
- how it should be stored
- how summaries are derived
- how memory is promoted safely
- where the first skills and examples should be added
