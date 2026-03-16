English | [한국어](quick-start.ko.md)

# Quick Start

## Purpose

This guide gives the shortest practical path to try `Mimir-Skills` today.

If your agent can read local files and run shell commands, the primary path is now to read the relevant `SKILL.md` directly.
The command paths below are optional local helpers for when you explicitly want repo-driven collection or draft generation.

There are three practical entry paths:

1. `skill-first reading` for agents that can open local files directly
2. `shared CLI` for repo-root helper commands
3. `Codex local install` when you specifically want Codex to load installed workflow skills

See [Agent Support Levels](agent-support-levels.md) for how these paths map to the current target agent families.

## Path 1: Skill-First Reading

This is the primary recommendation for local-file agents.

Use it when your agent can open repository files and run shell commands directly.

Start from:

- `skills/prepare-handoff/SKILL.md`
- `skills/write-pr-rationale/SKILL.md`
- `skills/capture-ci-investigation/SKILL.md`

Then load only the references you need and use the optional local scripts only when collection or validation help is useful.

## Path 2: Shared CLI

This is now the default helper path, not the main product story.

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

Collect structured PR context for the skill-first `write-pr-rationale` path:

```bash
python skills/write-pr-rationale/scripts/collect_pr_context.py --repo . --output pr-context.json
```

Persist generated artifacts to disk only when you actually want a file:

```bash
python -m mimir_skills prepare-handoff --repo . --output handoff.md
python skills/write-pr-rationale/scripts/collect_pr_context.py --repo . --output pr-context.json
```

### What to Expect

- `prepare-handoff` is currently the stronger clean-state workflow.
- `write-pr-rationale` is now a skill-first workflow. Use its `SKILL.md` plus playbook to draft the rationale, and use the collector only when you want structured git context first.
- `python -m mimir_skills write-pr-rationale --repo .` still exists, but now prints a deprecation note instead of generating reviewer-facing Markdown.
- outputs are drafts and still require human review before external sharing.

## Path 3: Codex Local Install

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

## Choosing Between the Paths

Choose `skill-first reading` when:

- your agent can read local files directly
- you want the skill rules and playbooks, not just generated helper output
- you want the repository to stay adapter-light

Choose `shared CLI` when:

- you want the fastest command-driven helper path from the repository root
- you are using a project-root CLI agent
- you do not need agent-specific install or discovery behavior beyond normal file access

Choose `Codex local install` when:

- you specifically want Codex to load the workflows as installed local skills
- you want a proof point for thin adapter support

## Current Limits

- `capture-ci-investigation` is still a narrower beta wrapper
- there is no hosted multi-agent install story yet
- support levels differ by agent family, and not every target has a thin adapter
- deeper behavior and safety constraints still live in [Always-Loaded Rules](always-loaded-rules.md), [Workflow Surface](workflow-surface.md), and the workflow `SKILL.md` files
- helper commands are secondary; the skills and references are the primary workflow source of truth
