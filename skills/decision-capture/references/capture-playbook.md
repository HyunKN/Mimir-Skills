# Capture Playbook

## Use This Reference For

- CI failure triage
- architecture or interface changes
- dependency, config, or security-sensitive updates
- handoff preparation

## Capture Sequence

1. Identify the trigger category.
2. Create a bounded draft with `../scripts/create_decision_record.py <slug>` if starting from scratch.
3. Gather only the evidence needed to justify the decision.
4. Write the decision statement in one sentence.
5. Record the chosen option and why it won over alternatives.
6. List affected paths.
7. Record validation, remaining risks, and follow-up if they exist.
8. Validate the completed JSON record.
9. Save the JSON record.
10. Render Markdown with `../scripts/render_summary.py <record-path>` only if another human or agent needs a summary.

## Draft Workflow

- The scaffolding script creates an intentionally incomplete draft.
- Required fields remain empty until a human or agent fills real evidence and rationale.
- A fresh scaffold should fail validation until it is completed.
- The renderer should run only after the JSON record passes validation.

## Rendered Summary Expectations

- Treat JSON as the canonical source and Markdown as a derived view.
- Do not introduce claims in Markdown that are missing from the JSON record.
- Keep summaries short enough for handoff or reviewer context, not as a second canonical record.

## Scenario Notes

### CI Triage

- Link the failing job, relevant file or config, and the validating rerun.
- Focus on the root cause and chosen remediation.

### Multi-File Refactor

- Focus on the changed contract, the selected approach, and continuation risks.
- Avoid narrating every edit when one decision explains them.

### Handoff

- Keep the record concise.
- Make the remaining risks and next actions explicit.
