English | [한국어](glossary.ko.md)

# Glossary

## decision traceability

The ability to recover why an important engineering choice was made, what evidence supported it, and what should happen next.

## decision record

The canonical machine-readable artifact for one high-impact decision. In v0.1 this is one JSON file per decision.

## evidence reference

A structured pointer to supporting material such as a file path, test run, CI log, diff, issue, command output, or document.

## rendered summary

A human-readable Markdown view derived from one or more canonical records. It is not the source of truth.

## trigger

A workflow event or decision boundary that qualifies for record creation, such as a CI fix, architecture change, dependency update, or handoff.

## memory candidate

A reusable lesson extracted from one or more decision records that has not yet been validated for durable reuse.

## validated memory

A promoted memory entry that has passed provenance, evidence, safety, and freshness checks.

## promotion

The explicit act of moving a reusable lesson from candidate status into validated memory.

## supersedes

A relationship showing that a newer decision record replaces or updates an earlier one.

## runtime artifact root

The project-local directory where generated artifacts are stored. In this repository the target path is `.ai/records/`.

## confidence

A bounded estimate of how reliable a record or conclusion is at the time it was written. In the schema it is represented as a numeric value from `0.0` to `1.0`.
