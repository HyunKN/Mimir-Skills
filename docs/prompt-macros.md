# Prompt Macros

## Purpose

This document gives portable prompt macros for the current outward-facing workflows.

Use these after install when you want the simplest user-facing invocation story:

- ask for the result you want first
- fall back to the explicit workflow name when routing is weak or inconsistent

These are plain prompt patterns, not native slash commands.
That keeps them portable across Claude Code, Codex, and other local-file agents that can read installed skills.

## Recommended Pattern

Try the shortest outcome-first prompt first:

```text
<ask for the output you want>
```

If the agent does not reliably pick the installed workflow, switch to the explicit fallback:

```text
Use the <workflow-name> workflow. <ask for the output you want>
```

## `prepare-handoff`

Minimal prompt:

```text
Prepare a handoff from my current changes.
```

Explicit fallback:

```text
Use the prepare-handoff workflow. Prepare a handoff from my current changes.
```

Stronger output-bound prompt:

```text
Use the prepare-handoff workflow. Draft a concise handoff covering what changed, what is done, what remains, what was validated, and what risks or blockers remain.
```

## `write-pr-rationale`

Minimal prompt:

```text
Write PR rationale for this branch.
```

Explicit fallback:

```text
Use the write-pr-rationale workflow. Write PR rationale for this branch.
```

Stronger output-bound prompt:

```text
Use the write-pr-rationale workflow. Draft reviewer-facing PR rationale that explains what changed, why it changed, what was validated, and what reviewers should watch.
```

## `capture-ci-investigation`

Minimal prompt:

```text
Summarize this CI failure as a bounded investigation note.
```

Explicit fallback:

```text
Use the capture-ci-investigation workflow. Summarize this CI failure as a bounded investigation note.
```

Stronger output-bound prompt:

```text
Use the capture-ci-investigation workflow. Draft a bounded CI investigation summary with observed evidence, current explanation, unknowns, current action, and next check.
```

## Support-Level Note

- Codex is the strongest fit today because it has thin adapter support.
- Claude Code has documented support, so the same prompts are still useful, but explicit workflow wording may be needed more often.
- Other agent families may still need more explicit workflow wording because install, discovery, and routing quality can differ.

See [`agent-support-levels.md`](agent-support-levels.md) for the current support matrix.

## Collector-Assisted Prompts

Use these when you already collected structured context JSON and want the agent to draft from that material explicitly.

### `prepare-handoff` with Collected Context

```text
Use the prepare-handoff workflow. Use the collected git context in `handoff-context.json` and draft a handoff covering what changed, what is done, what remains, what was validated, and any blockers or risks.
```

### `write-pr-rationale` with Collected Context

```text
Use the write-pr-rationale workflow. Use the collected PR context in `pr-context.json` and draft reviewer-facing rationale that explains what changed, why it changed, what was validated, and what reviewers should watch.
```

## Optional Validation Prompts

These are useful for repo maintainers or users who want explicit contract checks.

### Validate a Decision Record

```text
Validate this decision record against the repository contract and tell me what fields fail: `.ai/records/decisions/<id>.json`
```

### Validate a Memory Artifact

```text
Validate this memory artifact against the repository contract and tell me what fields fail: `.ai/records/memories/<candidate|validated>/<id>.json`
```

### Run the Full Example Verification Stack

```text
Run the repository example verification stack and summarize any failures.
```

## Optional Obsidian Prompts

Use these only when you want graph-friendly Markdown notes for local human browsing.

### Render a Decision Record as an Obsidian Note

```text
Render this decision record as an Obsidian-friendly note under the default project output location: `.ai/records/decisions/<id>.json`
```

### Render a Memory Artifact as an Obsidian Note

```text
Render this memory artifact as an Obsidian-friendly note under the default project output location: `.ai/records/memories/<candidate|validated>/<id>.json`
```

### Render Existing Records for Obsidian Review

```text
Render the existing decision and memory records in this project as Obsidian-friendly notes under the default project output location so I can browse them in Obsidian.
```

### Change the Obsidian Output Location

```text
Change the default Obsidian output location for this project to my Obsidian vault path.
```

```text
Switch the default Obsidian output location for this project back to `.ai/records/reports/`.
```

If you prefer direct local commands instead of an agent request:

```bash
python -m mimir_skills obsidian-config show
python -m mimir_skills obsidian-config set-vault "C:\\path\\to\\your\\Obsidian Vault\\Mimir-Skills"
python -m mimir_skills obsidian-config set-reports
python -m mimir_skills obsidian-config clear
```

Obsidian note rendering is manual opt-in.
If you do not use Obsidian, skip these prompts entirely.
