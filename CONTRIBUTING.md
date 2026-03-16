# Contributing

Thanks for helping build `Mimir-Skills`.

This repository is documentation-first. Contributions should make decision records, examples, skills, and evaluation assets easier to understand, validate, and reuse.

## Good First Contribution Types

- improve public docs or clarify terminology
- extend a spec without breaking existing examples
- add a public-safe synthetic example
- improve validator or renderer behavior without widening the security surface
- add evaluation prompts or reviewer guidance
- refine skill instructions or references

## Before You Change Anything

1. Read [README.md](README.md), [SECURITY.md](SECURITY.md), and [docs/project-one-pager.md](docs/project-one-pager.md).
2. Check the relevant spec before changing examples, skills, or scripts.
3. Prefer small, reviewable changes over broad repository rewrites.

## Repository Rules

- Keep canonical decision records in JSON.
- Treat Markdown summaries as derived outputs, not the source of truth.
- Keep examples public-safe and synthetic.
- Do not add secrets, internal URLs, private incident details, or raw sensitive logs.
- Keep `.workspace/` local and out of GitHub publication.
- Keep JSON keys, schema field names, and file paths in English.

## Language Rules

- English files are the source of truth for meaning.
- Public manuals and development docs should have Korean companions when that document class is already bilingual.
- Update the Korean companion as a direct translation when the English source changes.
- Keep section order and link structure aligned across both languages.

## Scripts And Hooks

- Prefer bounded scripts before hooks.
- New automation should be local-first, reviewable, and safe by default.
- Do not add network-dependent automation, remote installers, or secret-dependent behavior by default.
- Do not add a blocking pre-save hook for draft decision records in v0.1.
- If a future hook is proposed, keep it narrow, explicit, and preferably warning-only or tied to finalization steps.

## Examples And Evaluations

- New examples should include a canonical JSON decision record under `.ai/records/decisions/`.
- If a summary is included, render it from the JSON record or keep it clearly derived from the JSON source.
- Update evaluation docs when a new example materially expands the workflow coverage.

## Validation Checklist

Before opening a contribution, run the checks relevant to your change.

- Verify public examples end to end with `python scripts/verify_examples.py`
- Validate canonical records with `python skills/decision-core/scripts/validate_decision_record.py <path>`
- Render summaries with `python skills/decision-capture/scripts/render_summary.py <record-path> --output <summary-path>`
- Re-read the touched bilingual doc pair to make sure the Korean file still mirrors the English source

When new functionality lands, extend CI with the smallest check that proves that feature works. Do not widen CI with unrelated checks by default.

## Security Reporting

If your contribution uncovers a security problem, follow [SECURITY.md](SECURITY.md) instead of opening a public issue with sensitive details.
