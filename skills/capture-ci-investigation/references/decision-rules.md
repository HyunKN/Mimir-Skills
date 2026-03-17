# capture-ci-investigation Decision Rules

## Four-Lane Separation

Keep four lanes separate in the draft:
- observed evidence
- the current best explanation
- unknowns or remaining uncertainty
- the temporary decision, mitigation, or next check

## Evidence-Strength Wording

- strong evidence can support likely-cause language when the failure shape, relevant change, and validating check all line up
- medium evidence should stay hypothesis-shaped and say what would confirm or falsify the explanation
- weak evidence should stay monitor-first, avoid root-cause or fixed language, and say explicitly that the issue is not yet explained

Treat rerun-only success or partial validation as a signal reducer, not proof of root cause or proof that the issue is fixed.

## Shared Workflow Impact

If the current best action would touch shared workflow behavior such as retries, timeouts, quarantines, cache policy, base image, or job sequencing, call out the blast radius and the follow-up needed before describing the change as safe.

## Governance Context

If stale guidance, AI-assisted suggestions, approval scope, or rollout stage materially affected the incident path, mention that context explicitly instead of collapsing it into a generic fix note.

- Say whether the risky path was AI-assisted only when that provenance changes how the event should be reviewed later.
- Say what approval or deployment boundary limited the response when it affected the chosen action.
- Prefer bounded wording such as canary, rollback-ready, monitor-first, or escalation-required over vague safety language.
- When a canonical record is needed, use the governance-field threshold matrix in `../../../spec/trigger-taxonomy.md` to decide which optional governance fields are worth filling.

## Escalation

Escalate to a canonical decision record or deeper CI investigation when the issue changes shared policy, repeats across platforms, blocks release or deploy gates, or still lacks enough evidence for a bounded summary.

## Default Stance

If there is no concrete code, workflow, or environment cause yet, prefer monitoring, evidence collection, rollback, or escalation language over speculative tuning.

## Output Template

Use a compact summary with these sections when the incident needs a written draft:

1. `Failure Summary`
   - state the failing job, stage, and immediate symptom
   - if the signal is weak, say so here rather than implying a confirmed break
2. `Observed Evidence`
   - list the concrete CI artifacts, reruns, workflow files, timing notes, or reproduction checks that actually exist
3. `Current Explanation`
   - strong evidence: explain the likely cause and why the evidence supports it
   - medium evidence: explain the leading hypothesis and what would confirm or falsify it
   - weak evidence: say that the issue is not yet explained and keep the explanation tentative
4. `Current Action`
   - state whether the team changed something, chose monitoring, reverted, quarantined, or deferred
   - if a shared workflow change is involved, mention the blast radius and follow-up window
5. `Unknowns / Risks`
   - name what is still uncertain, what could recur, or what this mitigation might hide
6. `Next Check`
   - say what evidence, rerun, duration sample, owner, or trigger would reopen deeper investigation

Omit filler. If a section has no real content, compress it into a shorter sentence rather than padding the draft.
