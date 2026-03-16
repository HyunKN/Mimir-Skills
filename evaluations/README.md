# Evaluations Directory

This directory will hold evaluation prompts and scenarios for checking whether the documentation and records are actually useful.

Initial evaluation themes:

- can a new agent continue from the stored records alone
- can a reviewer understand the decision quickly
- do promoted memories remain valid against current repository state

Current public evaluation docs:

- `replay-evaluation.md`
- `reviewer-comprehension.md`
- `memory-promotion-evaluation.md`
- `write-pr-rationale-agent-validation.md`
- `staleness-review.md`

These evaluations currently use the public-safe synthetic examples under:

- `../examples/windows-ci-timeout/`
- `../examples/cache-client-pin/`
- `../examples/cache-client-tls-memory/`

`reviewer-comprehension.md` also serves as the evaluation anchor for the `pr-rationale` workflow-specific skill.
`memory-promotion-evaluation.md` serves as the evaluation anchor for the `memory-promote` workflow-specific skill.
`write-pr-rationale-agent-validation.md` serves as the runtime-reduction gate for the `write-pr-rationale` wrapper skill.
`staleness-review.md` serves as the Phase 2 maintenance anchor for checking doc/example drift against the current skill-first baseline.
