# Complete synthetic cache client v4.3 migration Decision Summary

> Derived from canonical decision record `dec-20260320-cache-client-v43-migration-003`.

## Decision

Add tls.ca_bundle configuration and upgrade the synthetic acme-cache-client dependency to 4.3.0 in staging.

## Context

The release branch had previously pinned acme-cache-client to 4.2.7 because v4.3 required tls.ca_bundle. The follow-up task adds the missing config so the upgrade can proceed safely.

## Selected Option

- Add tls.ca_bundle and upgrade to 4.3.0
- Update the synthetic cache TLS config with ca_bundle and remove the temporary version pin.

## Why

The earlier pin isolated the missing config contract clearly, and the follow-up change validates that the upgrade is safe once tls.ca_bundle is present.

## Alternatives Considered

- Keep the 4.2.7 pin (rejected): Would leave the migration debt in place and postpone the verified TLS contract update again.
- Disable TLS verification temporarily (rejected): Would weaken transport safety and conflict with the repository security baseline.
- Add tls.ca_bundle and upgrade to 4.3.0 (selected): Restores forward progress while preserving verified TLS behavior.

## Evidence

- [doc] `docs/upgrade-notes/acme-cache-client-v4.3.md`: Synthetic upgrade note states that verified TLS connections require tls.ca_bundle in v4.3+. (captured 2026-03-20T07:18:00Z)
- [file] `config/cache.yaml`: Synthetic cache config now includes tls.ca_bundle alongside the existing verified TLS settings. (captured 2026-03-20T07:24:00Z)
- [test] `tests/cache/client-config.test.ts`: Synthetic compatibility test passed on acme-cache-client 4.3.0 after the TLS config update. (captured 2026-03-20T07:35:00Z)

## Affected Paths

- `config/cache.yaml`
- `package.json`
- `pnpm-lock.yaml`

## Validation

- [test] `pnpm test:cache-client` -> passed: Synthetic cache client compatibility tests passed with acme-cache-client 4.3.0 and the new TLS config.
- [build] `pnpm build` -> passed: The service build and synthetic staging boot check completed with the migrated config.

## Remaining Risks

- Future minor releases may still change the TLS bootstrap contract and should be checked against release notes.

## Follow-Up

- Promote the repeated TLS contract lesson into validated memory for future cache client upgrades.

## Supersedes

- `dec-20260312-cache-client-pin-001`

## Confidence

- 0.86
