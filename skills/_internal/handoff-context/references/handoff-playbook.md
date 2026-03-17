# Handoff Playbook

## Use This Reference For

- agent-to-agent continuation
- agent-to-human status transfer
- pause-and-resume workflows
- reviewer or maintainer context that should stay tied to canonical records

## Capture Sequence

1. Identify who needs the handoff and what they need to do next.
2. Gather only the decision records and derived summaries that matter for that continuation.
3. Separate completed work from remaining work.
4. Call out validation state, blockers, and remaining risks.
5. Make the next actions explicit.
6. Link back to the canonical JSON records and render Markdown only when it helps the next reader.

## Handoff Checklist

- selected decision or decisions
- affected paths
- validation state
- remaining risks
- follow-up or next actions
- blockers or open questions
- links to the canonical records and any derived summaries

## Branch-State Patterns

### Dirty-Tree Pattern

Use when the repository still has staged, unstaged, or untracked changes.

- make the branch state explicit in the snapshot
- list raw status entries before summarizing anything else
- break untracked files into their own short subsection when they exist
- include staged and unstaged diff summaries when they help the next owner see the shape of in-progress work
- default risk should mention that the final intended state still needs confirmation
- default next steps should mention commit review and validation follow-up

### Clean Branch-Range Pattern

Use when the working tree is clean but the branch still differs from its base.

- say plainly that no working-tree changes were detected
- explain that committed branch context is the primary fallback evidence
- list committed branch files and diff-stat lines instead of pretending the task is empty
- default risk should remind the next owner to check whether important context already lives in commits or decision records
- default next steps should ask whether a clean-state checkpoint is enough or whether a richer continuation note is needed

### Recent-Commit Fallback Pattern

Use when both the working tree and committed branch-range diff are clean, but recent committed work still matters.

- say explicitly that the handoff is falling back to recent committed work
- summarize the most relevant recent commits instead of inventing new narrative
- keep the tone checkpoint-oriented rather than implying unfinished local edits
- treat this as the weakest local-evidence mode and keep uncertainty plain

## Summary Patterns

### Single-Record Handoff

- use when one decision record explains the state clearly
- prefer the derived Markdown summary and keep it tightly aligned with the JSON source

### Multi-Record Handoff

- use when several decisions affect the same continuation path
- summarize only the records that matter to the next owner instead of replaying the whole session

### Pause-and-Resume Handoff

- use when the same agent or a future agent will resume later
- make the next command, validation target, or decision checkpoint explicit

## Section Defaults

### Evidence Section

Use this priority order when explicit evidence notes are missing:

1. working-tree status and diff
2. committed branch-range context
3. recent committed work
4. generic fallback only when the local snapshot is otherwise thin

### Risk Section

- dirty tree -> mention unfinished local state and the need to confirm final intended changes
- fully clean tree -> mention that missing context may live in commits or decision records
- explicit user risk notes should replace the defaults, but should not erase obvious uncertainty

### Next-Step Section

- dirty tree -> review changed files and confirm commit intent
- clean tree -> decide whether a checkpoint is enough or whether a richer continuation note is needed
- changed files present -> ask for concrete validation results before wider sharing
- always -> add blockers, owner notes, and follow-up responsibility when another person or agent will continue

## Compact Fallback Examples

### Example A: Dirty Tree

- Working tree: not clean (`1` staged, `2` unstaged, `1` untracked)
- What changed:
  - raw status entries
  - untracked subsection
  - staged / unstaged diff summaries
- Evidence:
  - "Use the current working-tree status and diff summary above as the primary local evidence for this draft."
- Risk:
  - "The branch still contains uncommitted changes, so the next owner should verify the final intended state before sharing externally."

### Example B: Clean Branch-Range

- Working tree: clean
- What changed:
  - "No working-tree changes were detected, so this draft is using committed branch context."
  - committed branch-range file list
  - committed diff summary
- Evidence:
  - "The working tree is clean, so this draft is using committed branch-range context as the primary local evidence."

### Example C: Recent-Commit Fallback

- Working tree: clean
- What changed:
  - "No committed branch-range diff was detected either, so this draft is falling back to recent committed work."
  - recent committed work summary
- Evidence:
  - "The working tree and branch-range diff are both clean, so this draft is using recent committed work as fallback evidence."

## Risk Patterns

- handoffs that retell the whole transcript instead of the actionable state
- missing blockers or hidden incomplete validation
- stale summaries that drift from the canonical JSON
- follow-up ownership omitted from the continuation note

## Example Mapping

- `../../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md` shows a compact CI handoff derived from one canonical record.
- `../../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md` shows the same pattern for a dependency and config decision.
