English | [한국어](replay-evaluation.ko.md)

# Replay Evaluation

## Purpose

Use this evaluation to check whether a fresh agent can continue work from stored decision artifacts without re-discovering the original context.

## Example Under Test

Choose one public-safe synthetic example pair:

- `../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json`
- `../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`
- `../examples/cache-client-pin/.ai/records/decisions/dec-20260312-cache-client-pin-001.json`
- `../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`

## Evaluator Instructions

Give a fresh agent only the chosen example record and rendered summary.
Do not provide the original conversation or hidden implementation notes.

Ask the agent to answer:

1. What decision was made?
2. Why was that option selected over alternatives?
3. Which file or workflow area was affected?
4. What validation happened?
5. What risk remains?
6. What should happen next?

## Pass Criteria

The evaluation passes if the agent can correctly recover:

- the chosen change
- the supporting evidence
- the affected path
- the validation result
- the remaining risk
- the follow-up task

## Failure Signals

The evaluation should be considered weak or failed if the agent:

- invents evidence not present in the record
- cannot identify the affected path
- misses the remaining risk or follow-up
- confuses the chosen option with a rejected alternative

## Notes

- This evaluation is designed for public-safe synthetic examples.
- Run the validator first if the canonical JSON changed.
