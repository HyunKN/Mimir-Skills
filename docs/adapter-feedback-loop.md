English | [한국어](adapter-feedback-loop.ko.md)

# Adapter Feedback Loop

## Purpose

This document defines how `decision-skills` should evaluate the first real adapter experiences.

The goal is not to add heavy telemetry.
The goal is to keep a small, repeatable feedback loop so the project can tell whether a workflow draft is actually saving time.

## Current Scope

This feedback loop is defined for the currently implemented local adapter path and can later be reused for additional agent adapters.

Right now, the primary workflows to watch are:

- `prepare-handoff`
- `write-pr-rationale`
- `capture-ci-investigation`

## Core Success Metrics

Use a small set of outcome-oriented metrics:

### Time to First Useful Draft

Measure how long it takes from invoking the workflow to seeing the first draft that is good enough to continue editing instead of starting from scratch.

Target direction:

- fast enough to feel lower-friction than writing manually

### Draft Usefulness Rate

Classify each generated draft into one of four buckets:

- usable as-is
- usable with light edits
- usable only after heavy rewrite
- discarded

Target direction:

- most drafts should land in the first two buckets

### Manual Edit Time

Measure how long it takes to make the draft ready for actual sharing or handoff.

Target direction:

- editing the draft should clearly take less time than writing the same artifact manually

### Repeat Usage

Track whether the same user or team chooses the workflow again after trying it once.

Target direction:

- the workflow should be reused because it is actually helpful, not just because it was novel once

## Lightweight Review Questions

After using a workflow, answer these questions:

1. Did the draft reduce reconstruction work?
2. What important context was still missing?
3. What parts felt too generic or overstated?
4. What evidence or local signal should be collected next time?
5. Would the same user choose this workflow again for a similar task?

## Recommended Review Record

Use a short manual note with:

- date
- workflow used
- repository or task context
- time to first useful draft
- usefulness bucket
- manual edit time
- top missing detail
- top unnecessary detail
- whether the user would reuse it

This can live in local team notes, a private evaluation log, or later public-safe examples if the case becomes reusable.

## Structured Observation Checklist

Before running a comparison pass, prepare a small checklist that captures at least:

- date of the run
- workflow under test
- execution surface under test:
  - shared CLI
  - current adapter path
  - or both
- repository and task context
- repository state:
  - dirty or clean
  - external clone or active local workspace
  - synthetic sample or real local work
- exact command used
- output mode:
  - stdout
  - file write
  - or both
- time to first useful draft
- usefulness bucket
- estimated manual edit time
- whether the same user would reuse the workflow again
- path, import, discovery, or stdout-surface friction
- any stale-doc or stale-example mismatch discovered during the run

The checklist should stay lightweight.
It exists so the next observation pass is comparable to later ones instead of becoming another one-off note.

## What To Improve First

If the metrics are weak, improve in this order:

1. output shape and section ordering
2. missing local context collection
3. domain knowledge inside the workflow skill
4. clearer uncertainty handling
5. adapter install or invocation friction

## What Not To Do Yet

- do not add heavy analytics or background telemetry
- do not optimize every agent surface at once
- do not expand workflow count just to collect more metrics
- do not treat a single success case as proof that the adapter design is stable

## Relationship to Failure Modes

This feedback loop should feed later failure-mode tracking.

If the same weak output pattern, stale reference problem, or missing context problem repeats, record it as a failure mode and consider whether the workflow, docs, or adapter rules should change.
