English | [한국어](README.ko.md)

# decision-skills

Draft handoffs, PR rationale, and CI investigation context from local project state.

`decision-skills` is shifting toward an output-first workflow skill pack for AI coding agents.
The product direction is simple: stop reconstructing engineering context by hand when a skill can read local signals and draft the first useful version for you.

## Who This Is For

- small software teams, roughly 2 to 8 engineers
- working in a GitHub pull-request-based flow
- already using AI coding agents in regular engineering work

It is also being shaped to help individual developers who use AI coding agents daily and want better continuity across sessions, branches, and review cycles.

## What v1 Is Being Built To Do

- `prepare-handoff`: read the current branch context and draft a handoff that explains what changed, what remains, and where to continue
- `write-pr-rationale`: read the branch diff and validation context and draft a reviewer-facing explanation of why the change happened
- `capture-ci-investigation`: draft a bounded CI investigation summary from the available failure context, without promising perfect root-cause analysis

## Why This Exists

AI coding agents can already edit code, run tests, inspect CI, and prepare pull requests.
What teams still lose is the context around that work:

- why a path was chosen
- what was actually changed
- what evidence supported the choice
- what remains risky or uncertain
- what the next agent or reviewer should know before continuing

`decision-skills` exists to lower the cost of preserving that context.

## Quality Boundary

This repository should help generate strong drafts, not pretend to replace engineering judgment.

- outputs are drafts, not final truth
- human review is still required before external sharing
- CI help is best-effort and depends on the available logs and context
- automation should stay bounded, reviewable, and secondary to explicit evidence-based records

## Current Status

The repository is still in a documentation-first public v0.1 phase today.
The output-first direction above is the next layer being built on top of the current internal engine.

What is available now:

- a public project one-pager
- a shared CLI-friendly surface under `decision_skills/`, including `python -m decision_skills list`, `python -m decision_skills prepare-handoff`, and `python -m decision_skills write-pr-rationale`
- a first Codex-local install path under `adapters/codex/scripts/install_codex_skills.py`, documented in `docs/codex-local-install.md`
- a public support-level definition for Claude Code, OpenAI / Codex and GPT-facing coding-agent surfaces, Gemini CLI, and Qwen Code under `shared CLI support`, `documented support`, and `thin adapter support`
- a compact always-loaded rules baseline for shared CLI runs and future adapters
- a shared glossary
- v0.1 specs for triggers, decision records, and memory promotion, plus machine-readable companion schemas for decision records and memory artifacts
- starter skill templates plus `decision-core`, `decision-capture`, `dependency-upgrade-decision`, `ci-rationale`, `handoff-context`, `pr-rationale`, `memory-promote`, and the public workflow wrappers `prepare-handoff`, `write-pr-rationale`, and the narrower beta `capture-ci-investigation`
- public-safe end-to-end examples for CI, dependency/config, and memory-promotion flows
- evaluation prompts for replay, reviewer comprehension, and memory promotion
- minimal CI for schema-helper consistency checks, example validation, public memory artifact validation, and derived-summary drift checks
- Korean companion docs for the root README and `docs/`, plus mirrored local workspace notes outside the published repository surface

What comes next:

- use the published support-level policy to decide whether future agent work should stop at shared CLI support, documented support, or thin adapter support
- treat `prepare-handoff` as the stronger current workflow and confirm it once more on an in-progress, non-clean task state before freezing it as stable public guidance
- keep `write-pr-rationale` in active output shaping until it can capture stronger `why` context for clean-state runs without depending on generic placeholders or heavy manual rewrite
- keep `capture-ci-investigation` narrower and best-effort until stronger examples and reliability boundaries justify any direct-use script layer

## Documentation

- [Project One-Pager](docs/project-one-pager.md)
- [Glossary](docs/glossary.md)
- [Always-Loaded Rules](docs/always-loaded-rules.md)
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
decision-skills/
  README.md
  README.ko.md
  adapters/
  decision_skills/
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
- Korean files are maintained only for the root README and files under `docs/`, alongside the English source as `*.ko.md`.
- Local `.workspace/` notes may also be mirrored in Korean, but they are gitignored and not part of the public repository surface.
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

Ship a credible public v1 direction that lets teams see immediate workflow value, while keeping the current documentation, schema, and validation base intact underneath.
