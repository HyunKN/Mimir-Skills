# Examples Directory

This directory will hold end-to-end examples that show:

- a trigger event
- a canonical JSON decision record
- a rendered Markdown summary
- optional memory candidate promotion

All examples in this directory should be public-safe synthetic samples.

- Do not copy real secrets, internal URLs, credentials, private incident details, or raw sensitive logs.
- Use examples to demonstrate repository structure, schemas, and workflows.
- Treat `examples/**/.ai/` as publishable sample data only, not as real runtime output from a live project.
- Checked-in Markdown summaries are derived artifacts. Re-render them from the canonical JSON when the source record changes.

Each example should focus on a high-impact change with clear evidence and validation.

Current examples:

- `windows-ci-timeout/` shows a runtime-style `.ai/records/` layout with one canonical decision record and one rendered Markdown summary. It is the anchor example for the `ci-rationale` workflow-specific skill.
- `linux-ci-rerun-watch/` shows a lower-confidence CI investigation where a single rerun passed, no shared workflow change was made, and monitoring remained the selected action. It is the boundary example for the `capture-ci-investigation` skill-first workflow.
- `macos-flaky-quarantine/` shows a repeated flaky macOS visual failure where quarantining one spec in a shared workflow was chosen over retries or disabling the full job. It is the shared-workflow-change example for the `capture-ci-investigation` skill-first workflow.
- `cache-client-pin/` shows a dependency-and-config trigger with one canonical decision record and one rendered Markdown summary derived from the JSON source. It is the anchor example for the `dependency-upgrade-decision` workflow-specific skill.
- `cache-client-tls-memory/` shows a dependency follow-up decision plus a public-safe `candidate -> validated` memory flow derived from decision records. It is the anchor example for the `memory-promote` workflow-specific skill.

The rendered summaries in the published examples also serve as reference shapes for the `handoff-context` and `pr-rationale` workflow-specific skills.
