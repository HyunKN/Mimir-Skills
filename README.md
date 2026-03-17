English | [한국어](README.ko.md)

# Mimir-Skills

Skill-first workflow guidance, playbooks, and validators for AI coding agents working from local files.

`Mimir-Skills` now operates on a skill-first baseline for local-file AI coding agents.
The core idea is simple: put workflow judgment rules, safety constraints, and output patterns into `SKILL.md` and companion references so agents can read them directly, while keeping only deterministic validation and thin local collection helpers in Python.

## Why Mimir-Skills?

AI coding agents can already edit code, run tests, inspect CI, and prepare pull requests.
What teams still lose is the context around that work:

- why a path was chosen
- what actually changed
- what evidence supported the choice
- what remains risky or uncertain
- what the next agent or reviewer should know before continuing

`Mimir-Skills` helps preserve that context with reusable workflow skills such as:

- `prepare-handoff`
- `write-pr-rationale`
- `capture-ci-investigation`

Best fit for:

- small software teams, roughly 2 to 8 engineers
- GitHub pull-request-based workflows
- developers already using local-file AI coding agents in regular engineering work

Quality boundary:

- outputs are drafts, not final truth
- human review is still required before external sharing
- CI help is best-effort and depends on the available logs and context
- automation should stay bounded, reviewable, and secondary to explicit evidence-based records

## Getting Started

There are three practical ways to use `Mimir-Skills` today.
See [Quick Start](docs/quick-start.md) for step-by-step commands and path details.

### 1. Skill-First Reading (Recommended)

Start from the workflow `SKILL.md` files directly:

- `skills/prepare-handoff/SKILL.md`
- `skills/write-pr-rationale/SKILL.md`
- `skills/capture-ci-investigation/SKILL.md`

This is the primary path for local-file agents that can open repository files directly.

### 2. One-Line Install

Install skills into your project with a single command. No repo clone needed:

```bash
npx mimir-skills install --target claude
npx mimir-skills install --target codex
npx mimir-skills install --target generic
```

Or from the repository:

```bash
python -m mimir_skills install --target claude
python -m mimir_skills install --target codex
```

The installer auto-detects the target when `.claude/` or `.codex/` exists in the project directory. Use `--target` to be explicit.

See [Local Install](docs/codex-local-install.md) for full options and details.

### 3. Local Helpers

Use repository-root helpers when you want discovery or structured context collection before drafting from the skill.

- `python -m mimir_skills list`
- `python skills/prepare-handoff/scripts/collect_git_context.py --repo . --output handoff-context.json`
- `python skills/write-pr-rationale/scripts/collect_pr_context.py --repo . --output pr-context.json`

The old `prepare-handoff` and `write-pr-rationale` generate commands now exist as compatibility or deprecation stubs rather than the primary workflow path.

## Documentation

Start here:

- [Project One-Pager](docs/project-one-pager.md)
- [Quick Start](docs/quick-start.md)
- [Workflow Trigger Table](docs/workflow-trigger-table.md)
- [Workflow Surface](docs/workflow-surface.md)
- [Agent Support Levels](docs/agent-support-levels.md)

Reference:

- [Always-Loaded Rules](docs/always-loaded-rules.md)
- [Local Install](docs/codex-local-install.md)
- [Adapter Feedback Loop](docs/adapter-feedback-loop.md)
- [Skills Directory Notes](skills/README.md)
- [Examples Directory Notes](examples/README.md)
- [Evaluations Directory Notes](evaluations/README.md)
- [Trigger Taxonomy v0.1](spec/trigger-taxonomy.md)
- [Decision Record Schema v0.1](spec/decision-record-schema.md)
- [Memory Promotion Policy v0.1](spec/memory-promotion-policy.md)
- [Security Policy](SECURITY.md)
- [Contributing Guide](CONTRIBUTING.md)

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

## Current Status

The repository now runs on a skill-first baseline.

- `prepare-handoff` and `write-pr-rationale` are skill-first workflows with live collectors and deprecated generate stubs
- `capture-ci-investigation` is a skill-first workflow, wrapper-only by design
- workflow routing stays on the public trigger table until scale or ambiguity justifies anything machine-readable
- deterministic validators and example verification remain stable and should not grow back into a larger workflow runtime
- new agent-specific adapters stay deferred unless repeated usage shows a clear UX gain beyond the current baseline

## Language Policy

- `README.md` is the default GitHub entry point.
- English files are the source of truth for meaning.
- Korean files are maintained only for the root README and a small entry or overview subset under `docs/`, currently `project-one-pager`, `quick-start`, and `glossary`.
- Detailed workflow docs, helper docs, skills, references, evaluations, contributor workflow files, and local planning notes stay English-first.
- Public technical specs, skills, examples, evaluations, and contributor workflow files stay English-only.
- JSON keys, schema names, and file paths stay in English across both languages.

## License

Apache 2.0. See [LICENSE](LICENSE).
