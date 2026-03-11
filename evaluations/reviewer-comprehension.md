English | [한국어](reviewer-comprehension.ko.md)

# Reviewer Comprehension Evaluation

## Purpose

Use this evaluation to check whether a reviewer can understand the reason for a change quickly from the rendered summary and canonical record.

## Example Under Test

Choose one public-safe synthetic example pair:

- `../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`
- `../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json`
- `../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`
- `../examples/cache-client-pin/.ai/records/decisions/dec-20260312-cache-client-pin-001.json`

## Review Questions

Ask the reviewer or evaluator to answer:

1. What changed?
2. Why did it change?
3. What evidence supports the change?
4. What was tested?
5. What still needs attention?

## Pass Criteria

The evaluation passes if the reviewer can answer all five questions without needing the original task transcript.

## Failure Signals

The evaluation should be considered weak or failed if:

- the summary hides the actual reason for the decision
- the evidence is too vague to support the claim
- the validation result is missing or unclear
- remaining risk or follow-up is absent from both the summary and the record

## Notes

- Use the Markdown summary first, then confirm details in the JSON record.
- The goal is not perfect verbosity; the goal is fast, reliable comprehension.
