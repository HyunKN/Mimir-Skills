English | [한국어](quick-start.ko.md)

# Quick Start

## Purpose

This guide gives the shortest practical path to try `Mimir-Skills` today.

If your agent can read local files and run shell commands, the primary path is now to read the relevant `SKILL.md` directly.
The command paths below are optional local helpers for when you explicitly want repo-driven collection, discovery, or compatibility notes.

There are four practical entry paths:

1. `skill-first reading` for agents that can open local files directly
2. `one-line install` for installing skills into your project from any directory
3. `local helpers` for collectors, discovery, and deprecation-note compatibility paths
4. `Codex local install` when you specifically want Codex to load installed workflow skills (backward compat)

See [Agent Support Levels](agent-support-levels.md) for how these paths map to the current target agent families.

## Path 1: Skill-First Reading

This is the primary recommendation for local-file agents.

Use it when your agent can open repository files and run shell commands directly.

Start from:

- `skills/prepare-handoff/SKILL.md`
- `skills/write-pr-rationale/SKILL.md`
- `skills/capture-ci-investigation/SKILL.md`

Then load only the references you need and use the optional local scripts only when collection or validation help is useful.

## Path 2: One-Line Install

Use this when you want to install Mimir-Skills workflows into your project with a single command.

This works from any project directory — no repository clone needed:

```bash
npx mimir-skills install --target claude
npx mimir-skills install --target codex
npx mimir-skills install --target generic
```

If you have the repository cloned:

```bash
python -m mimir_skills install --target claude
python -m mimir_skills install --target codex --codex-home ~/.codex
python -m mimir_skills install --target generic --project-dir /path/to/project
```

Install only specific workflows:

```bash
npx mimir-skills install --target claude --workflows prepare-handoff write-pr-rationale
```

The installer auto-detects the target when `.claude/` or `.codex/` exists in the project directory. If both exist, `--target` is required.

### Target Directories

| Target | Install Path |
|--------|-------------|
| `claude` | `<project>/.claude/skills/` |
| `codex` | `$CODEX_HOME/skills/` (or `~/.codex/skills/`) |
| `generic` | `<project>/.skills/` |

### What to Expect

- installed skills are copies, not symlinks
- example and evaluation references are rewritten to point to a local `mimir-skills-support/` directory
- re-run with `--force` to replace existing installations

## Path 3: Local Helpers

This is now a secondary helper path, not the main product story.

Use it when you want repository-root discovery, structured context collection, or compatibility notes for older helper-based flows.

![Shared CLI command snapshot](assets/shared-cli-quick-start.svg)

### Commands

List the available shared workflows:

```bash
python -m mimir_skills list
```

Collect structured handoff context for the skill-first `prepare-handoff` path:

```bash
python skills/prepare-handoff/scripts/collect_git_context.py --repo . --output handoff-context.json
```

Collect structured PR context for the skill-first `write-pr-rationale` path:

```bash
python skills/write-pr-rationale/scripts/collect_pr_context.py --repo . --output pr-context.json
```

Persist generated artifacts to disk only when you actually want a file:

```bash
python skills/prepare-handoff/scripts/collect_git_context.py --repo . --output handoff-context.json
python skills/write-pr-rationale/scripts/collect_pr_context.py --repo . --output pr-context.json
```

### What to Expect

- `prepare-handoff` is now a skill-first workflow. Use its `SKILL.md` plus playbook to draft the handoff, and use the collector only when you want structured git context first.
- `write-pr-rationale` is now a skill-first workflow. Use its `SKILL.md` plus playbook to draft the rationale, and use the collector only when you want structured git context first.
- `python -m mimir_skills prepare-handoff --repo .` still exists, but now prints a deprecation note instead of generating handoff Markdown.
- `python -m mimir_skills write-pr-rationale --repo .` still exists, but now prints a deprecation note instead of generating reviewer-facing Markdown.
- outputs are drafts and still require human review before external sharing.

## Path 4: Codex Local Install (Legacy)

Use this when you specifically want the older Codex-specific install path.

![Codex local install snapshot](assets/codex-local-install.svg)

### Commands

Install the current outward-facing workflows into the default Codex home:

```bash
python -m mimir_skills install
```

Install only the main direct-use workflows:

```bash
python -m mimir_skills install --workflows prepare-handoff write-pr-rationale
```

The older direct script path still works when you explicitly want it:

```bash
python adapters/codex/scripts/install_codex_skills.py
```

Then ask Codex with direct workflow language such as:

- `Prepare a handoff from my current changes.`
- `Write PR rationale for this branch.`
- `Summarize this CI failure as a bounded investigation note.`

### What to Expect

- this is a real local install path, not a hosted registry flow
- the installed wrappers point to the same skill-first workflow packages and local helper runtime used from the repository root
- skill-first reading is still the lower-friction baseline when you do not specifically need installed Codex skills

## Choosing Between the Paths

Choose `skill-first reading` when:

- your agent can read local files directly
- you want the skill rules and playbooks, not just generated helper output
- you want the repository to stay adapter-light

Choose `one-line install` when:

- you want skills installed locally without cloning the repository
- you are using Claude Code, Codex, or another agent that reads from a local skills directory
- you want a single command to set up everything

Choose `local helpers` when:

- you want the fastest discovery or collection path from the repository root
- you want structured context JSON before drafting from the skill
- you need compatibility guidance for older helper-based invocations

Choose `Codex local install (legacy)` when:

- you specifically want the older Codex-specific install flow
- you need backward compatibility with existing scripts

## Current Limits

- `capture-ci-investigation` is a skill-first workflow, wrapper-only by design
- there is no hosted multi-agent install story yet, but `npx mimir-skills install` provides a one-line install from any directory
- support levels differ by agent family, and not every target has a thin adapter
- deeper behavior and safety constraints still live in [Always-Loaded Rules](always-loaded-rules.md), [Workflow Surface](workflow-surface.md), and the workflow `SKILL.md` files
- helper commands are secondary; the skills and references are the primary workflow source of truth
