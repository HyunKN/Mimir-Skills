# Stabilize cache client dependency before release cut Decision Summary

> Derived from canonical decision record `dec-20260312-cache-client-pin-001`.

## Decision

Pin the synthetic acme-cache-client dependency to 4.2.7 and defer the v4.3 config migration.

## Context

A minor upgrade to the synthetic acme-cache-client dependency introduced a required tls.ca_bundle setting. The current service config does not provide it, which caused startup failure in staging and blocked the release branch.

## Selected Option

- Pin acme-cache-client to 4.2.7
- Replace the caret dependency range with an exact pin and keep the current cache TLS configuration unchanged for this release.

## Why

Pinning the dependency removes the immediate regression with the smallest bounded change, while keeping the eventual config migration visible as explicit follow-up work.

## Alternatives Considered

- Complete the v4.3 config migration immediately (deferred): Would require a wider deployment and secret-distribution change late in the release window.
- Pin acme-cache-client to 4.2.7 (selected): Restores the previous config contract with the smallest safe patch.
- Disable TLS verification temporarily (rejected): Would weaken transport safety and conflict with the repository security baseline.

## Evidence

- [doc] `docs/upgrade-notes/acme-cache-client-v4.3.md`: Synthetic upgrade note states that verified TLS connections now require tls.ca_bundle. (captured 2026-03-12T08:40:00Z)
- [file] `config/cache.yaml`: Current synthetic cache config defines tls.enabled and server_name but not ca_bundle. (captured 2026-03-12T08:44:00Z)
- [test] `tests/cache/client-config.test.ts`: The compatibility test failed on v4.3 and passed again after pinning 4.2.7. (captured 2026-03-12T09:05:00Z)

## Affected Paths

- `package.json`
- `pnpm-lock.yaml`

## Validation

- [test] `pnpm test:cache-client` -> passed: Synthetic cache client compatibility tests passed with the pinned dependency.
- [build] `pnpm build` -> passed: The service build completed without requiring additional config changes.

## Remaining Risks

- The eventual v4.3 migration is still pending and must add explicit tls.ca_bundle handling.

## Follow-Up

- Add the new TLS config fields in a later change and retry the v4.3 upgrade in staging.

## Confidence

- 0.79
