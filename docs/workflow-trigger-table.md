# Workflow Trigger Table

## Purpose

Use this table when you need to decide which top-level workflow fits the current user request or local evidence.

These routing rules are intentionally public, lightweight, and skill-first.
They do not replace the deeper workflow-specific `SKILL.md` files.
They help an agent choose the right public workflow before loading the detailed playbook.

## Primary Routing Table

| User need | Typical ask or local cue | Choose this workflow | Read first | Optional helper now | Escalate or switch when |
| --- | --- | --- | --- | --- | --- |
| Continue work on the current branch | `handoff`, `checkpoint`, `what changed`, `where do I continue`, dirty tree, clean branch checkpoint | `prepare-handoff` | `skills/prepare-handoff/SKILL.md` | `skills/prepare-handoff/scripts/collect_git_context.py` | the work needs a canonical decision record rather than a continuation summary |
| Explain a change to reviewers | `PR rationale`, `why this changed`, `review notes`, `what was validated`, reviewer-facing explanation of a diff | `write-pr-rationale` | `skills/write-pr-rationale/SKILL.md` | `skills/write-pr-rationale/scripts/collect_pr_context.py` | explicit product or tradeoff intent is missing and the user must supply that `why` directly |
| Summarize a CI or workflow incident without overclaiming | failing job, flaky test, timeout, rerun note, workflow config change, request for an incident summary | `capture-ci-investigation` | `skills/capture-ci-investigation/SKILL.md` | none; skill-first and wrapper-only by design | the incident changes shared retry, timeout, quarantine, or workflow policy, or needs a durable canonical record |

## Routing Notes

- `prepare-handoff` is for continuation context, not reviewer persuasion.
- `write-pr-rationale` is for reviewer-facing explanation, not canonical truth. If explicit `why` context is thin, keep the rationale tentative.
- `capture-ci-investigation` is for bounded incident summaries. Keep observed evidence, current explanation, unknowns, and temporary action separate.

## Local Signal Hints

- Prefer `prepare-handoff` when the strongest signal is branch state:
  - staged, unstaged, or untracked work
  - a clean branch that still needs a continuation checkpoint
  - a request for blockers, risks, or next steps
- Prefer `write-pr-rationale` when the strongest signal is reviewer communication:
  - changed files or commits already exist
  - the user wants validation, reviewer focus, or PR-facing wording
  - explicit `why`, `validation`, `risk`, or reviewer-note context exists or can be supplied
- Prefer `capture-ci-investigation` when the strongest signal is incident evidence:
  - job links or failing workflow names
  - rerun notes, reproduction attempts, or timing observations
  - workflow, retry, timeout, or runner changes that may affect more than one job

## If More Than One Workflow Fits

- `prepare-handoff` + `write-pr-rationale`:
  - use both when the user needs a continuation summary and a reviewer-facing explanation from the same branch
  - default to `prepare-handoff` first if the work is still in motion and the next agent needs a truthful checkpoint before a PR story
- `capture-ci-investigation` + canonical decision capture:
  - use both when the CI issue changes shared workflow policy or needs durable auditability
  - keep the CI summary bounded, and let the canonical decision record hold the durable truth
- no top-level workflow:
  - do not force one of these workflows when the user really needs a raw validator, a schema decision record, or a specialized support skill instead

## Boundary

- This table routes the top-level workflow choice only.
- Detailed output structure, guardrails, and fallback behavior still belong in each workflow's `SKILL.md` and references.
- If routing ambiguity starts to grow, revisit whether a machine-readable companion is justified.
