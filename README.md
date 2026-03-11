English | [한국어](README.ko.md)

# decision-skills

Open skills and reference docs for making AI-agent engineering decisions traceable, reusable, and reviewable.

## Why This Exists

AI coding agents can already edit code, run tests, inspect CI, and prepare pull requests.
What teams still lose is the decision context around that work:

- why a path was chosen
- which alternatives were considered
- what evidence supported the choice
- what remains risky or uncertain
- what the next agent should know before continuing

`decision-skills` focuses on that gap.

## Core Principles

- Decision traceability first
- AI-readable canonical records first
- Human-readable summaries derived from the same source
- Long-term memory as a derived, validated layer
- Skills-style repository structure for open reuse

## Safety Note

`decision-skills` is primarily a decision-recording tool. It may include limited automation such as scripts or hooks where they improve consistency and safety, but automation should stay bounded, reviewable, and secondary to explicit evidence-based records.

## Current Status

This repository is in a documentation-first public v0.1 phase.

What is available now:

- a public project one-pager
- a shared glossary
- v0.1 specs for triggers, decision records, and memory promotion
- starter skill templates plus `decision-core` and `decision-capture`
- public-safe end-to-end examples for CI and dependency/config triggers
- evaluation prompts for replay and reviewer comprehension
- minimal CI for example validation and derived-summary drift checks
- bilingual manuals and development docs for English and Korean readers

What comes next:

- contribution guidance for outside collaborators
- narrower hook or guardrail decisions after more usage feedback
- workflow-specific skill expansions
- future evaluation automation and memory-promotion examples

## Documentation

- [Project One-Pager](docs/project-one-pager.md)
- [Glossary](docs/glossary.md)
- [Trigger Taxonomy v0.1](spec/trigger-taxonomy.md)
- [Decision Record Schema v0.1](spec/decision-record-schema.md)
- [Memory Promotion Policy v0.1](spec/memory-promotion-policy.md)
- [Security Policy](SECURITY.md)
- [Contributing Guide](CONTRIBUTING.md)

## Repository Layout

```text
decision-skills/
  README.md
  README.ko.md
  docs/
  spec/
  template/
  skills/
  examples/
  evaluations/
```

The intended runtime artifact layout inside a user repository is:

```text
.ai/
  records/
    decisions/
    memories/
      candidates/
      validated/
    plans/
    reports/
```

## Language Policy

- `README.md` is the default GitHub entry point.
- English files are the source of truth for meaning.
- Korean files are maintained only for public manuals and development docs, alongside the English source as `*.ko.md`.
- JSON keys, schema names, and file paths stay in English across both languages.

## Starter Assets

- [Skill Template](template/SKILL.md)
- [Skills Directory Notes](skills/README.md)
- [Examples Directory Notes](examples/README.md)
- [Evaluations Directory Notes](evaluations/README.md)
- [Contributing Guide](CONTRIBUTING.md)
- GitHub Actions CI in `.github/workflows/ci.yml`

## Near-Term Goal

Ship a small but credible public v0.1 that lets contributors understand the problem, inspect the schema, and build the first skills and examples on a stable documentation base.
