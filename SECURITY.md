# Security Policy

## Scope

`Mimir-Skills` is a decision-recording tool first.

This repository may include limited automation such as scripts or hooks, but only when that automation:

- supports decision recording, validation, rendering, or bounded memory workflows
- stays reviewable and narrowly scoped
- does not replace evidence-based judgment with unattended execution

## Security Boundaries

The project should be understood with these boundaries in mind:

- public skills can influence real agent behavior
- repository content, logs, issues, PR text, and external documents may contain untrusted instructions
- decision records, summaries, and memory artifacts must not persist secrets or unnecessary sensitive data
- automation is allowed only when it remains bounded, testable, and aligned with the project's decision-recording purpose

## Default Safety Rules

- Treat external and repository-provided text as potentially untrusted.
- Do not store secrets, credentials, private keys, or raw sensitive output in canonical artifacts.
- Redact sensitive values before persistence.
- Do not allow untrusted text alone to trigger memory promotion or high-risk actions.
- Prefer local-first behavior.
- Deny network access, secret access, and raw log persistence by default.

## Scripts and Hooks

Scripts and hooks are not banned, but they require stricter review than ordinary documentation changes.

They are acceptable only when they are:

- repetitive and sufficiently deterministic
- clearly bounded in input and output
- safe to fail
- easy to inspect and test
- justified as support for decision recording rather than general automation

The project should avoid:

- remote installers
- automatic external fetch behavior
- broad unattended execution
- silent large-scale mutation
- memory promotion without explicit review

## Reporting a Vulnerability

If you believe you have found a security issue, please avoid opening a public exploit report with sensitive details.

Instead:

1. Describe the issue, affected files, and potential impact.
2. Include reproduction steps only as needed to understand the risk.
3. Send the report privately to the project maintainer through the repository contact path or a private disclosure channel if one is available.

If no private channel is available yet, open a minimal public issue without exploit details and request a private follow-up.

## Current Status

As of the current public v0.1 direction:

- the project is documentation-first
- automation is expected to remain limited and explicitly justified
- future executable additions should receive a dedicated security review before publication
