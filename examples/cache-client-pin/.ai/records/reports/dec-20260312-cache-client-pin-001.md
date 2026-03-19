# Stabilize cache client dependency before release cut

- Decision ID: `dec-20260312-cache-client-pin-001`

## Source of Truth

- Canonical JSON: `.ai/records/decisions/dec-20260312-cache-client-pin-001.json`

## Summary

Pin the synthetic acme-cache-client dependency to 4.2.7 and defer the v4.3 config migration.

## Follow-Up

- Add the new TLS config fields in a later change and retry the v4.3 upgrade in staging.
