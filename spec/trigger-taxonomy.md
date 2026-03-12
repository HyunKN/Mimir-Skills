# Trigger Taxonomy v0.1

## Purpose

This taxonomy defines when a workflow should create a decision record and when it should stay silent.
The goal is to capture high-value decisions without turning the repository into a noisy activity log.

## Default Rule

Create a decision record when all of the following are true:

- the choice affects behavior, risk, shared interfaces, operations, or future work
- the choice required reasoning between meaningful alternatives
- the choice can be supported with evidence references

If those conditions are not met, do not create a standalone record.

## Capture Categories

| Category | Record when | Typical examples |
| --- | --- | --- |
| Architecture and interfaces | A shared design or contract changes | API shape changes, schema version changes, module boundary refactors |
| Dependencies, config, and security | A dependency, permission, secret-handling rule, or deployment config changes risk or behavior | package add/remove, CI permission change, runtime config change |
| CI, build, and test strategy | A workflow changes how the project validates or ships | test strategy shift, build pipeline fix, flake workaround with rationale |
| Root cause and remediation | A failure is diagnosed and a fix path is chosen | CI failure triage, production bug analysis, rollback decision |
| Workflow boundary and handoff | A task boundary needs durable continuation context | handoff note, paused migration, partial rollout summary |
| Memory promotion signals | A repeated lesson appears reusable beyond one task | project rule candidate, recurring environment constraint |

## Usually Do Not Capture

Do not create standalone decision records for:

- formatting-only edits
- trivial local refactors with no shared impact
- raw command output without interpretation
- speculative notes with no evidence
- duplicated notes already covered by a current record

## Required Minimum Output for Triggered Records

When a trigger does qualify, the record should include at least:

- `decision`
- `selected_option`
- `rationale`
- `evidence_refs`
- `affected_paths`
- `confidence`

## Escalation Heuristics

Prefer recording even small decisions when one of these is true:

- the change touches authentication, authorization, secrets, or permissions
- the change modifies shared contracts or generated artifacts
- a failure diagnosis is likely to be revisited later
- the work will be handed off across people, sessions, or agents

## Review Guidance

When in doubt, ask:

1. Would a future agent lose time or make a mistake without this rationale?
2. Is the decision likely to be questioned in review?
3. Can the claim be backed by a file, test, log, diff, or issue?

If the answer is yes to at least two questions, create the record.
