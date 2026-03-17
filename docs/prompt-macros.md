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
