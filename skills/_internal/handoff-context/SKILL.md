---
name: handoff-context
description: Prepare or review agent-to-agent handoff context when another human or agent needs a short, evidence-backed continuation summary. Use when a validated decision record exists or must be created, and the next reader needs the selected option, rationale, affected paths, validation status, remaining risks, and next actions without rereading raw logs or full chat history.
---

# handoff-context

Use this skill when work needs to be handed off with a concise continuation summary derived from validated decision records.

## Workflow

1. Confirm that the task has crossed a trigger boundary or reached a pause point where another human or agent must continue the work.
2. Read `../decision-capture/SKILL.md` if a required decision record does not exist yet.
3. Gather only the canonical decision records and derived summaries needed for the next owner to continue safely.
4. Distill the selected option, rationale, affected paths, validation state, remaining risks, and next actions into a short handoff view.
5. Use `../decision-capture/scripts/render_summary.py <record-path>` when a single validated record needs a derived Markdown summary.
6. Keep the handoff concise and link back to the canonical JSON records for deeper detail.
7. Leave memory promotion to a separate review step unless the promotion policy is explicitly being evaluated.

## Handoff Focus

- Optimize for continuation, not for retelling the entire session.
- Surface what changed, what is still uncertain, and what should happen next.
- Keep every claim traceable to a canonical record or a validated derived summary.
- Make blockers, pending validation, and follow-up ownership obvious to the next reader.

## Guardrails

- Do not copy raw logs, long transcripts, or hidden reasoning into the handoff.
- Do not introduce claims in Markdown that are missing from the source decision record.
- Do not hide incomplete validation or remaining risks for the sake of brevity.
- Do not treat the handoff summary as a new canonical source; the JSON record remains the source of truth.
- Do not include secrets, credentials, or private infrastructure details beyond already-redacted record content.

## Load References As Needed

- Read [`references/handoff-playbook.md`](references/handoff-playbook.md) when preparing agent-to-agent or agent-to-human continuation context.
- Read [`../decision-capture/SKILL.md`](../decision-capture/SKILL.md) when creating a missing canonical record or rendering a summary from it.
- Read [`../decision-core/SKILL.md`](../decision-core/SKILL.md) when checking shared validation, safety, and promotion constraints.
- Read [`../../../spec/decision-record-schema.md`](../../../spec/decision-record-schema.md) when reviewing which fields must be preserved in the handoff.
- Inspect the public summaries under [`../../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`](../../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md) and [`../../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`](../../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md) when you need concrete single-record handoff shapes.
