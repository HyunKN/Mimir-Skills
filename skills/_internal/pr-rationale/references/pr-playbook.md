# PR Playbook

## Use This Reference For

- reviewer-facing pull request summaries
- rationale derived from one or more decision records
- update notes that should stay aligned with canonical JSON
- review preparation focused on validation, risk, and follow-up

## Capture Sequence

1. Identify which decision records matter to the PR.
2. Gather only the evidence and validation details that a reviewer needs.
3. Separate what changed from why it changed.
4. Call out validation status, remaining risks, and follow-up work.
5. Link back to the canonical JSON records and use rendered Markdown only as a reviewer-facing derivative.
6. Refresh the PR rationale when the underlying records change.

## Reviewer Checklist

- what changed
- why it changed
- what evidence supports it
- what was validated
- what still needs attention
- which canonical record or records back the rationale

## Inference Boundary

- This boundary mirrors [`../../../write-pr-rationale/SKILL.md`](../../../write-pr-rationale/SKILL.md) Decision Rule #1 and should stay aligned with it.
- When explicit rationale is missing, inferred goals are temporary substitutes, not confirmed author intent.
- Prefer wording such as `this branch appears to...`, `local evidence suggests...`, and `review should check...`.
- Avoid wording such as `this branch does...`, `the author intended...`, or `reviewers can assume...` unless that claim is backed by explicit rationale input or canonical records.
- Keep the missing `why` visible when branch evidence shows what changed more clearly than why it mattered.

## Evidence Priority

1. Current working-tree diff
2. Committed branch-range diff against the detected base
3. Recent committed work when both diff layers are clean

Always name which layer you used so reviewers know whether they are reading live diff evidence or fallback history.

## Local Signal Map

### `docs`

- touched areas often include `README*`, `docs/`, and `skills/`
- validation prompt: confirm commands, paths, and examples still match the current implementation
- reviewer focus: published guidance should describe the same behavior the code now implements
- risk: stale docs or examples will mislead both reviewers and future agents

### `workflow`, `runtime`, `adapter`

- touched areas often include `mimir_skills/`, `skills/*/scripts/`, or adapter/install glue
- validation prompt: add shared-helper, direct-script, or installed-path smoke evidence
- reviewer focus: documented entry points should still match runtime behavior and helper paths
- risk: path or wrapper changes can break other execution surfaces even when repository-root runs look fine

### `ci`

- touched areas often include `.github/workflows/` or workflow-run investigation notes
- validation prompt: attach the relevant rerun, workflow result, or investigation note
- reviewer focus: preserve failure visibility rather than only making the pipeline look greener
- risk: CI-facing changes can mask the underlying failure mode if evidence is too thin

### `dependency/config`

- touched areas often include dependency manifests, config files, or compatibility notes
- validation prompt: add the build, compatibility, migration, or config check that justified the change
- reviewer focus: compatibility assumptions, rollback safety, and migration cost
- risk: config or dependency drift can look small in diff form but carry rollout risk

### `examples`, `evaluation`, `spec`

- touched areas often include `examples/`, `evaluations/`, or `spec/`
- validation prompt: confirm examples, evaluations, schemas, and rendered outputs still align
- reviewer focus: published artifacts should continue to match the actual workflow shape
- risk: example or schema drift weakens trust even when the local code path is correct

### `rename`

- touched areas often include commands, package paths, install locations, and published docs together
- validation prompt: smoke-test the renamed surfaces across both docs and runnable entry points
- reviewer focus: keep path-sensitive surfaces aligned, not just the main code path
- risk: partial rename drift leaves old commands or support paths behind

## Section Defaults

### `Why This Changed`

- explicit `--why` wins over all local inference
- if explicit rationale is missing, infer a tentative goal from the strongest signals and touched areas
- end the section with a prompt to replace or tighten the inferred rationale when reviewer approval depends on product or incident context

### `Validation`

- `workflow`, `runtime`, `adapter`: ask for a shared-helper, direct-script, or installed-path smoke result
- `ci`: ask for the relevant workflow rerun or CI result
- `docs`: ask for command/path/example verification when the change is guidance-only
- `dependency/config`: ask for the compatibility or configuration check that justified the change
- `examples`, `evaluation`, `spec`: ask for schema/output/example consistency verification

### `Reviewer Notes`

- clean branch-range fallback: tell reviewers to anchor on committed branch-range changes, not on expected uncommitted diff
- recent-commit fallback: tell reviewers to anchor on recent commit history plus explicit rationale notes
- `docs`: focus on docs and examples matching current behavior
- `workflow`, `runtime`, `adapter`: focus on runtime behavior matching documented entry points
- `ci`: focus on preserving failure visibility
- `rename`: focus on path and install-surface alignment

### `Risks and Follow-Up`

- when explicit `--why` is missing, keep the missing tradeoff or motivation risk visible
- `docs`: stale docs or examples can mislead reviewers and future agents
- `workflow`, `runtime`, `adapter`: wrapper or path changes can still break other surfaces
- `ci`: evidence can be too thin and hide the real failure mode
- `rename`: old names, commands, or install locations can remain partially behind

## Compact Fallback Examples

### Example A: Dirty Working Tree With Runtime and Docs Changes

- `What Changed`: current diff summary, changed files, and untracked files
- `Evidence`: current working-tree diff is primary evidence
- `Why This Changed`: `Inferred from the current working-tree diff: this branch appears to tighten the workflow runtime and the published guidance around it.`
- `Validation`: ask for shared-helper and direct-script smoke evidence if not already supplied
- `Reviewer Notes`: confirm docs and helper entry points still match

### Example B: Clean Docs-Only Branch Range

- `What Changed`: explicitly say the tree is clean and the draft is using committed branch-range context
- `Evidence`: branch-range diff is the primary evidence source
- `Why This Changed`: `Inferred from committed branch-range context: this branch appears to tighten the published guidance around the current behavior or product direction.`
- `Validation`: confirm commands, paths, and examples still match the implementation
- `Reviewer Notes`: review the committed branch-range changes rather than expecting uncommitted diff

### Example C: Recent-Commit Fallback Only

- `What Changed`: explicitly say both the working tree and branch-range diff are clean, then list recent committed work
- `Evidence`: recent committed work is the fallback evidence source
- `Why This Changed`: keep the rationale tentative and mention that local evidence is thin
- `Reviewer Notes`: tell reviewers to anchor on recent commit history and any explicit rationale notes
- `Risks and Follow-Up`: ask for explicit `--why` or risk notes before external sharing when approval depends on more than recent commit history

## Summary Patterns

### Single-Record PR Rationale

- use when one decision record explains the PR clearly
- start from the derived Markdown summary and tighten it for reviewer needs

### Multi-Record PR Rationale

- use when several decision records contribute to the same PR
- keep the explanation organized by review-relevant themes rather than by session chronology

### Risk-Forward PR Rationale

- use when the remaining risks or deferred follow-up are central to approval
- make the risks explicit instead of burying them in the middle of the text

## Risk Patterns

- PR descriptions that hide the real tradeoff
- reviewer summaries that omit failed or deferred alternatives
- stale PR text drifting away from canonical records
- missing validation or follow-up details that block confident review

## Example Mapping

- `../../../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md` shows a concise reviewer-facing explanation for a CI workflow adjustment.
- `../../../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md` shows the same pattern for a dependency and config decision.
- `../../../evaluations/reviewer-comprehension.md` provides the five core questions a reviewer should be able to answer from the rationale.
