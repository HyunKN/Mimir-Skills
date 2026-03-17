# Local Install

## Purpose

This is the local install path for `Mimir-Skills`.

It provides a real local install path for Claude Code, Codex, and other AI agent environments without requiring a remote registry, hosted installer, or full multi-agent packaging story.

See [Agent Support Levels](agent-support-levels.md) for how this install path fits relative to Claude Code, Codex, Gemini CLI, Qwen Code, and the current skill-first plus helper baseline.
See [Always-Loaded Rules](always-loaded-rules.md) for the compact rule layer that future adapters and repository-root helper runs should keep visible.

## What It Installs

The installer copies the current outward-facing workflows and their internal dependencies into the target skills directory:

- `prepare-handoff`
- `write-pr-rationale`
- `capture-ci-investigation`
- `handoff-context`
- `pr-rationale`
- `ci-rationale`
- `decision-capture`
- `decision-core`

It also copies publishable support assets into a `mimir-skills-support/` directory so example and evaluation references still resolve after install, and so the installed helper scripts can still import the shared `mimir_skills` runtime package.

## Install Targets

| Target | Skills Directory | When to Use |
|--------|-----------------|-------------|
| `claude` | `<project>/.claude/skills/` | Claude Code projects |
| `codex` | `$CODEX_HOME/skills/` (or `~/.codex/skills/`) | OpenAI Codex projects |
| `generic` | `<project>/.skills/` | Other agents or custom setups |

## One-Line Install (No Repo Clone)

```bash
npx mimir-skills install --target claude
npx mimir-skills install --target codex
npx mimir-skills install --target generic
```

## Install From Repository

Install all current outward-facing workflows:

```bash
python -m mimir_skills install --target claude
python -m mimir_skills install --target codex
python -m mimir_skills install --target generic
```

Install only selected workflows:

```bash
python -m mimir_skills install --target claude --workflows prepare-handoff write-pr-rationale
```

Install into a specific project directory:

```bash
python -m mimir_skills install --target claude --project-dir /path/to/project
```

Install into a specific Codex home and replace existing installed copies:

```bash
python -m mimir_skills install --target codex --codex-home ~/.codex --force
```

## Auto-Detection

When `--target` is not specified, the installer detects the target from the project directory:

- `.claude/` exists → `claude`
- `.codex/` exists → `codex`
- `$CODEX_HOME` env var set → `codex`
- Neither → `generic`

If both `.claude/` and `.codex/` exist, `--target` is required.

## Force Replace

With `--force`, the installer replaces only paths that already look like a previous `Mimir-Skills` install. If a destination does not look managed by this installer, it will refuse the overwrite and ask you to remove it manually.

## Quick Start

See [Quick Start](quick-start.md) for the broader side-by-side guidance between the current skill-first baseline and the install paths.

After install, ask your agent with direct workflow language such as:

- `Prepare a handoff from my current changes.`
- `Write PR rationale for this branch.`
- `Summarize this CI failure as a bounded investigation note.`

If routing is weak or inconsistent, use the explicit workflow form instead:

- `Use the prepare-handoff workflow. Prepare a handoff from my current changes.`
- `Use the write-pr-rationale workflow. Write PR rationale for this branch.`
- `Use the capture-ci-investigation workflow. Summarize this CI failure as a bounded investigation note.`

See [Prompt Macros](prompt-macros.md) for the portable copy-paste prompt pack.

## Feedback Loop

Use the lightweight review loop in [Adapter Feedback Loop](adapter-feedback-loop.md) after real usage.

The current goal is to learn whether the installed workflows produce useful drafts quickly enough to justify broader adapter work, not to claim that the install path is already final.

## Current Limits

- This is a local install path only.
- It does not publish to a remote skill registry.
- It does not install every internal workflow in the repository.
- `--force` is intentionally conservative and refuses to replace unrelated-looking directories.
- Outputs remain drafts and still require human review.
- the installed `prepare-handoff` and `write-pr-rationale` helper entrypoints now mirror the repository-root baseline: collectors remain live, while old generate paths are compatibility/deprecation stubs
- `capture-ci-investigation` is a skill-first workflow, wrapper-only by design, and does not include direct-use collector or generator scripts.
