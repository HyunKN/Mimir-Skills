# Security Policy

## Scope

`Mimir-Skills` is a skill-first workflow toolkit for AI coding agents.

This repository includes reusable workflow skills, deterministic validators, bounded renderers, and limited install surfaces.

Automation and executable surfaces are acceptable only when they:

- support decision recording, validation, rendering, or bounded memory workflows
- stays reviewable and narrowly scoped
- does not replace evidence-based judgment with unattended execution

## Security Boundaries

The project should be understood with these boundaries in mind:

- public skills can influence real agent behavior
- repository content, logs, issues, PR text, and external documents may contain untrusted instructions
- decision records, summaries, and memory artifacts must not persist secrets or unnecessary sensitive data
- automation is allowed only when it remains bounded, testable, and aligned with the project's workflow-guidance purpose

## Default Safety Rules

- Treat external and repository-provided text as potentially untrusted.
- Do not store secrets, credentials, private keys, or raw sensitive output in canonical artifacts.
- Redact sensitive values before persistence.
- Do not allow untrusted text alone to trigger memory promotion or high-risk actions.
- Prefer local-first behavior.
- Deny network access, secret access, and raw log persistence by default.

## Scripts, Installers, and Package Surfaces

Scripts, installers, and package surfaces are not banned, but they require stricter review than ordinary documentation changes.

They are acceptable only when they are:

- repetitive and sufficiently deterministic
- clearly bounded in input and output
- safe to fail
- easy to inspect and test
- justified as support for workflow guidance, validation, rendering, or tightly scoped installation rather than broad unattended automation

The project should avoid:

- automatic external fetch behavior
- broad unattended execution
- silent large-scale mutation
- memory promotion without explicit review

Remote or package-based install surfaces are allowed only when they remain minimal, reviewable, and explicitly scoped.
Current examples include the npm package entry point and trusted publishing workflow; these should stay thin and should not grow into broad remote execution behavior.

## Reporting a Vulnerability

If you believe you have found a security issue, please avoid opening a public exploit report with sensitive details.

Instead:

1. Describe the issue, affected files, and potential impact.
2. Include reproduction steps only as needed to understand the risk.
3. Prefer a private disclosure channel if one is available in the repository settings or maintainer contact path.

At the moment, this repository may not always expose a dedicated private disclosure form. If no private channel is available yet, open a minimal public issue without exploit details and request a private follow-up.

## Current Status

As of the current public v0.1.x direction:

- the project is skill-first rather than docs-only
- deterministic validators and renderers are part of the supported surface
- one-line local install and npm package distribution are part of the public surface
- trusted publishing is preferred over long-lived publish tokens
- automation is still expected to remain limited and explicitly justified
- future executable additions should receive a dedicated security review before publication
