English | [한국어](README.ko.md)

# Mimir-Skills

Skill-first workflow guidance, playbooks, and validators for AI coding agents working from local files.

`Mimir-Skills` is shifting toward a skill-first repository for local-file AI coding agents.
The direction is simple: put workflow judgment rules, safety constraints, and output patterns into `SKILL.md` and companion references so agents can read them directly, while keeping only deterministic validation and thin local collection helpers in Python.

## Who This Is For

- small software teams, roughly 2 to 8 engineers
- working in a GitHub pull-request-based flow
- already using AI coding agents in regular engineering work

It is also being shaped to help individual developers who use AI coding agents daily and want better continuity across sessions, branches, and review cycles.

## What v1 Is Being Built To Do

- `prepare-handoff`: give local-file agents a repeatable handoff pattern that explains what changed, what remains, and where to continue
- `write-pr-rationale`: give local-file agents a reviewer-facing pattern for explaining what changed, why it changed, what was validated, and what reviewers should watch
- `capture-ci-investigation`: give local-file agents a bounded CI investigation pattern that stays explicit about uncertainty and avoids overclaiming root cause

## Why This Exists

AI coding agents can already edit code, run tests, inspect CI, and prepare pull requests.
What teams still lose is the context around that work:

- why a path was chosen
- what was actually changed
- what evidence supported the choice
- what remains risky or uncertain
- what the next agent or reviewer should know before continuing

`Mimir-Skills` exists to lower the cost of preserving that context.

## Quality Boundary

This repository should help generate strong drafts, not pretend to replace engineering judgment.

- outputs are drafts, not final truth
- human review is still required before external sharing
- CI help is best-effort and depends on the available logs and context
- automation should stay bounded, reviewable, and secondary to explicit evidence-based records

## Current Status

The repository is now in a skill-first direction reset.
The public value centers on `SKILL.md`, references, examples, schemas, and deterministic validators first; local Python helpers remain available, but they are now secondary to the skill documents rather than the main product story.

What is available now:

- a public project one-pager
- user-facing workflow skills under `skills/prepare-handoff/`, `skills/write-pr-rationale/`, and the narrower beta `skills/capture-ci-investigation/`
- internal support skills such as `decision-core`, `decision-capture`, `handoff-context`, `pr-rationale`, `ci-rationale`, `dependency-upgrade-decision`, and `memory-promote`
- local helper surfaces under `mimir_skills/` and `skills/*/scripts/` for repository-root collection or draft generation when you explicitly want command-driven help
- a first Codex-local install path under `adapters/codex/scripts/install_codex_skills.py`, now treated as an optional thin-adapter proof point rather than the main public path
- a public support-level definition for Claude Code, OpenAI / Codex and GPT-facing coding-agent surfaces, Gemini CLI, and Qwen Code under `shared CLI support`, `documented support`, and `thin adapter support`
- a compact always-loaded rules baseline for shared CLI runs and any future adapters that remain worth supporting
- a shared glossary
- v0.1 specs for triggers, decision records, and memory promotion, plus machine-readable companion schemas for decision records and memory artifacts
- public-safe end-to-end examples for CI, dependency/config, and memory-promotion flows
- evaluation prompts for replay, reviewer comprehension, and memory promotion
- minimal CI for schema-helper consistency checks, example validation, public memory artifact validation, and derived-summary drift checks
- Korean companion docs for the root README plus a small overview subset under `docs/` (`project-one-pager`, `quick-start`, and `glossary`)

What comes next:

- keep the repository on the current skill-first baseline and rerun lightweight staleness reviews after meaningful workflow-surface changes
- keep workflow routing on the public trigger table until the workflow count or ambiguity justifies anything machine-readable
- keep deterministic validators and example verification stable while avoiding a return to a larger workflow runtime
- do not add another agent-specific adapter yet; only revisit adapter growth if repeated usage shows a clear UX gain beyond the current skill-first baseline
- keep `write-pr-rationale` honest about missing explicit `why` context, and keep `capture-ci-investigation` narrow and wrapper-only until repeated real usage justifies anything broader

## Documentation

- [Project One-Pager](docs/project-one-pager.md)
- [Glossary](docs/glossary.md)
- [Always-Loaded Rules](docs/always-loaded-rules.md)
- [Workflow Trigger Table](docs/workflow-trigger-table.md)
- [Quick Start](docs/quick-start.md)
- [Codex Local Install](docs/codex-local-install.md)
- [Agent Support Levels](docs/agent-support-levels.md)
- [Adapter Feedback Loop](docs/adapter-feedback-loop.md)
- [Workflow Surface](docs/workflow-surface.md)
- [Trigger Taxonomy v0.1](spec/trigger-taxonomy.md)
- [Decision Record Schema v0.1](spec/decision-record-schema.md)
- [Memory Promotion Policy v0.1](spec/memory-promotion-policy.md)
- [Security Policy](SECURITY.md)
- [Contributing Guide](CONTRIBUTING.md)
- [License](LICENSE)

## Repository Layout

```text
Mimir-Skills/
  README.md
  README.ko.md
  docs/
  skills/
  spec/
  examples/
  evaluations/
  scripts/
  template/
  mimir_skills/
  adapters/
```

Primary public surface:

- `skills/`
- `docs/`
- `spec/`
- `examples/`

Secondary helper surface:

- `scripts/`
- `mimir_skills/`
- `adapters/`

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
- Korean files are maintained only for the root README and a small entry or overview subset under `docs/`, currently `project-one-pager`, `quick-start`, and `glossary`.
- Detailed workflow docs, helper docs, skills, references, evaluations, contributor workflow files, and local planning notes stay English-first.
- Public technical specs, skills, examples, evaluations, and contributor workflow files stay English-only.
- JSON keys, schema names, and file paths stay in English across both languages.

## Starter Assets

- [Skill Template](template/SKILL.md)
- [Skills Directory Notes](skills/README.md)
- [Workflow Surface](docs/workflow-surface.md)
- [Examples Directory Notes](examples/README.md)
- [Evaluations Directory Notes](evaluations/README.md)
- [Contributing Guide](CONTRIBUTING.md)
- GitHub Actions CI in `.github/workflows/ci.yml`

## Near-Term Goal

Ship a credible public v1 direction where local-file agents can use the skills directly, while deterministic validators and thin local helpers remain available without becoming the main product.
