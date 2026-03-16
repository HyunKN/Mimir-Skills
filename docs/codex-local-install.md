English | [한국어](codex-local-install.ko.md)

# Codex Local Install

## Purpose

This is the first runtime adapter for `Mimir-Skills`.

It provides a real local install path for Codex without claiming a remote registry, hosted installer, or full multi-agent packaging story.

See [Agent Support Levels](agent-support-levels.md) for how this Codex path fits relative to Claude Code, Gemini CLI, Qwen Code, and the shared CLI baseline.
See [Always-Loaded Rules](always-loaded-rules.md) for the compact rule layer that future adapters and shared CLI runs should keep visible.

## What It Installs

The installer copies the current outward-facing workflows and their internal dependencies into `$CODEX_HOME/skills/`:

- `prepare-handoff`
- `write-pr-rationale`
- `capture-ci-investigation`
- `handoff-context`
- `pr-rationale`
- `ci-rationale`
- `decision-capture`
- `decision-core`

It also copies publishable support assets into `$CODEX_HOME/skills/mimir-skills-support/` so example and evaluation references still resolve after install, and so the installed direct-use scripts can still import the shared `mimir_skills` runtime package.

## Install

Install all current outward-facing workflows into the default Codex home:

```bash
python adapters/codex/scripts/install_codex_skills.py
```

Install only selected workflows:

```bash
python adapters/codex/scripts/install_codex_skills.py --workflows prepare-handoff write-pr-rationale
```

Install into a specific Codex home and replace existing installed copies:

```bash
python adapters/codex/scripts/install_codex_skills.py --codex-home ~/.codex --force
```

With `--force`, the installer now replaces only paths that already look like a previous `Mimir-Skills` install. If a destination does not look managed by this installer, it will refuse the overwrite and ask you to remove it manually.

## Quick Start

See [Quick Start](quick-start.md) for the broader side-by-side guidance between the shared CLI baseline and this Codex-local install path.

![Codex local install snapshot](assets/codex-local-install.svg)

After install, ask Codex with direct workflow language such as:

- `Prepare a handoff from my current changes.`
- `Write PR rationale for this branch.`
- `Summarize this CI failure as a bounded investigation note.`

Codex can then trigger the installed workflow skills from those prompts and use the bundled scripts where the wrapper already supports direct draft generation.

## Feedback Loop

Use the lightweight review loop in [Adapter Feedback Loop](adapter-feedback-loop.md) after real usage.

The current goal is to learn whether the installed workflows produce useful drafts quickly enough to justify broader adapter work, not to claim that the first adapter path is already final.

## Current Limits

- This is a local Codex install path only.
- It does not publish to a remote skill registry.
- It does not install every internal workflow in the repository.
- `--force` is intentionally conservative and refuses to replace unrelated-looking directories.
- Outputs remain drafts and still require human review.
- `capture-ci-investigation` remains a narrower beta wrapper and does not yet include direct-use collector or generator scripts.
