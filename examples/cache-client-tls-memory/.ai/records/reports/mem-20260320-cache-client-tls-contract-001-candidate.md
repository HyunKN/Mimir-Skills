# mem-20260320-cache-client-tls-contract-001 (candidate)

- Memory ID: `mem-20260320-cache-client-tls-contract-001`
- Status: `candidate`

## Source of Truth

- Canonical JSON: `.ai/records/memories/candidates/mem-20260320-cache-client-tls-contract-001.json`

## Statement

Synthetic services using acme-cache-client v4.3+ with verified TLS should add tls.ca_bundle before the upgrade is considered safe.

## Scope

Synthetic cache client upgrades in services that keep TLS verification enabled.

## Related Artifacts

- Source decisions: [[dec-20260312-cache-client-pin-001]], [[dec-20260320-cache-client-v43-migration-003]]
- Counterpart memory note: [[mem-20260320-cache-client-tls-contract-001-validated]]
