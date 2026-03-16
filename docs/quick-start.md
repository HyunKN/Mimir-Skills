English | [한국어](quick-start.ko.md)

# Quick Start

## Purpose

This guide gives the shortest practical path to try `Mimir-Skills` today.

There are two supported entry paths:

1. `shared CLI` for the lowest-friction project-root workflow
2. `Codex local install` when you specifically want Codex to load installed workflow skills

See [Agent Support Levels](agent-support-levels.md) for how these paths map to the current target agent families.

## Path 1: Shared CLI

This is the default recommendation today.

Use it when you want the lowest-friction way to try the workflow outputs directly from the repository root.

![Shared CLI command snapshot](assets/shared-cli-quick-start.svg)

### Commands

List the available shared workflows:

```bash
python -m mimir_skills list
```

Draft a handoff from the current repository state:

```bash
python -m mimir_skills prepare-handoff --repo .
```

Draft reviewer-facing PR rationale from the current branch:

```bash
python -m mimir_skills write-pr-rationale --repo .
```

Persist the Markdown draft to disk only when you actually want a file:

```bash
python -m mimir_skills prepare-handoff --repo . --output handoff.md
python -m mimir_skills write-pr-rationale --repo . --output pr-rationale.md
```

### What to Expect

- `prepare-handoff` is currently the stronger clean-state workflow.
- `write-pr-rationale` is usable, but still needs stronger `why` capture when local branch context is thin.
- outputs are drafts and still require human review before external sharing.

## Path 2: Codex Local Install

Use this when you want Codex to load the outward-facing workflows as installed local skills.

![Codex local install snapshot](assets/codex-local-install.svg)

### Commands

Install the current outward-facing workflows into the default Codex home:

```bash
python adapters/codex/scripts/install_codex_skills.py
```

Install only the main direct-use workflows:

```bash
python adapters/codex/scripts/install_codex_skills.py --workflows prepare-handoff write-pr-rationale
```

Then ask Codex with direct workflow language such as:

- `Prepare a handoff from my current changes.`
- `Write PR rationale for this branch.`
- `Summarize this CI failure as a bounded investigation note.`

### What to Expect

- this is a real local install path, not a hosted registry flow
- the installed wrappers use the same shared workflow core as the shared CLI path
- the shared CLI path is still the lower-friction baseline when you do not specifically need installed Codex skills

## Choosing Between the Two

Choose `shared CLI` when:

- you want the fastest way to try the workflows
- you are using a project-root CLI agent
- you do not need agent-specific install or discovery behavior

Choose `Codex local install` when:

- you specifically want Codex to load the workflows as installed local skills
- you want a proof point for thin adapter support

## Current Limits

- `capture-ci-investigation` is still a narrower beta wrapper
- there is no hosted multi-agent install story yet
- support levels differ by agent family, and not every target has a thin adapter
- deeper behavior and safety constraints still live in [Always-Loaded Rules](always-loaded-rules.md), [Workflow Surface](workflow-surface.md), and the workflow `SKILL.md` files
