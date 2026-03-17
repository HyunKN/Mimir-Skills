# prepare-handoff Decision Rules

## 1. Snapshot Mode

- If the working tree has staged, unstaged, or untracked entries, treat the handoff as a dirty-tree handoff.
- If the working tree is clean and the branch still differs from its base, treat the handoff as a clean-state checkpoint backed by committed branch context.
- If both the working tree and committed branch-range diff are clean, treat the handoff as a recent-commit fallback rather than implying that no useful context exists.

## 2. What Changed Priority

- Dirty-tree handoff:
  - show the working-tree count first
  - list raw status entries before summarizing touched files
  - call out untracked files in a dedicated subsection when they exist
  - include staged and unstaged diff summaries when they exist
- Clean-state branch-range handoff:
  - say explicitly that no working-tree changes were detected
  - use committed branch-range files as the primary "what changed" evidence
  - include committed diff-stat lines when they exist
- Recent-commit fallback handoff:
  - say explicitly that both the working tree and branch-range diff are clean
  - summarize the most recent committed work that still matters for continuation

## 3. Evidence Priority

Use this order when you need to explain what the handoff is based on:

1. working-tree status and diff
2. committed branch-range context
3. recent committed work
4. explicit user-supplied evidence notes
5. generic "no extra local evidence" fallback only when nothing above exists

If the user already supplied evidence notes, use them as the section content instead of the default bullets.

## 4. Default Risk Rules

- Dirty tree:
  - warn that the final intended state still needs confirmation before external sharing
- Fully clean tree:
  - warn that missing continuation context may already live in commits or decision records and should be checked
- User-supplied risk notes:
  - prefer them over the default bullets, but keep uncertainty explicit if the branch state is still ambiguous

## 5. Default Next-Step Rules

- Dirty tree:
  - tell the next owner to review changed files and confirm what still needs committing
- Clean tree:
  - tell the next owner to decide whether a clean-state checkpoint is enough or whether a richer committed-work summary is needed
- Any changed files:
  - tell the next owner to replace placeholder validation text with concrete results before wider sharing
- Always:
  - remind the author to add blockers, risks, and owner notes when another person or agent will resume

## 6. Override Contract

- Explicit title input overrides the default repository-name title.
- Explicit evidence, validation, blocker, risk, and next-step notes override the default section bullets for those sections.
- Do not let override notes erase important uncertainty that the next owner still needs to know.

## Output Template

Use this structure unless the user asks for a different handoff shape:

```md
# Handoff: <title or repo name>

> Generated from local repository context for branch `<branch>` at `<timestamp>`.

## Current Snapshot

- Repository: `<repo name>`
- Branch: `<branch>`
- HEAD: `<short hash>`
- Branch context base: `<base ref>`
- Working tree: clean | not clean (`<staged>` staged, `<unstaged>` unstaged, `<untracked>` untracked)

## What Changed

- Follow the dirty-tree, clean-state branch-range, or recent-commit fallback rules above.

## Relevant Evidence

- Use explicit evidence notes if present.
- Otherwise use the evidence-priority decision tree above.

## Recent Commits

- List recent commits when available.
- If none are available, say that no recent commit history was available.

## Validation

- Use explicit validation notes if present.
- Otherwise say that no explicit validation notes were provided.

## Blockers and Risks

- Use explicit blocker and risk notes if present.
- Otherwise apply the default risk rules above.

## Next Steps

- Use explicit next-step notes if present.
- Otherwise apply the default next-step rules above.
```
