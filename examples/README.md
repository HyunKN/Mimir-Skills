English | [한국어](README.ko.md)

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

- `windows-ci-timeout/` shows a runtime-style `.ai/records/` layout with one canonical decision record and one rendered Markdown summary.
- `cache-client-pin/` shows a dependency-and-config trigger with one canonical decision record and one rendered Markdown summary derived from the JSON source.
