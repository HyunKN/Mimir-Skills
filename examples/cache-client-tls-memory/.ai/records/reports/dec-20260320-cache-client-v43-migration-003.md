# Complete synthetic cache client v4.3 migration

- Decision ID: `dec-20260320-cache-client-v43-migration-003`

## Source of Truth

- Canonical JSON: `.ai/records/decisions/dec-20260320-cache-client-v43-migration-003.json`

## Summary

Add tls.ca_bundle configuration and upgrade the synthetic acme-cache-client dependency to 4.3.0 in staging.

## Related Artifacts

- Supersedes: [[dec-20260312-cache-client-pin-001]]

## Follow-Up

- Promote the repeated TLS contract lesson into validated memory for future cache client upgrades.
