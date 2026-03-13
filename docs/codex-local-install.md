English | [한국어](codex-local-install.ko.md)

# Codex Local Install

## Purpose

This is the first runtime adapter for `decision-skills`.

It provides a real local install path for Codex without claiming a remote registry, hosted installer, or full multi-agent packaging story.

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

It also copies publishable support assets into `$CODEX_HOME/skills/decision-skills-support/` so example and evaluation references still resolve after install.

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

## Quick Start

After install, ask Codex with direct workflow language such as:

- `Prepare a handoff from my current changes.`
- `Write PR rationale for this branch.`
- `Summarize this CI failure as a bounded investigation note.`

Codex can then trigger the installed workflow skills from those prompts and use the bundled scripts where the wrapper already supports direct draft generation.

## Current Limits

- This is a local Codex install path only.
- It does not publish to a remote skill registry.
- It does not install every internal workflow in the repository.
- Outputs remain drafts and still require human review.
- `capture-ci-investigation` remains a narrower beta wrapper and does not yet include direct-use collector or generator scripts.
