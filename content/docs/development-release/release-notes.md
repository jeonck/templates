---
weight: 4040
title: "Release Notes"
description: "What changed, what breaks, and what the reader has to do about it."
icon: "new_releases"
date: "2026-08-23"
draft: false
---

Release notes are written for someone deciding whether to upgrade and what it will cost them. That makes "Action required" the most important section and the changelog the least — a generated list of commits is not release notes.

## When to use it

- Every release of anything another team or customer consumes.
- Especially when a release contains a breaking change, a deprecation, or a security fix.
- Internal-only services still need them; the audience is the on-call engineer trying to correlate a behaviour change with a deploy.

## What it must answer

- Do I need to do anything, and by when?
- What changed that could affect me?
- What is being removed, and what replaces it?
- If something goes wrong, how do I go back?

## Template

{{< doctabs >}}
# <Product> v<version> — YYYY-MM-DD

## Summary
Two sentences. Who should care about this release.

## Action required
| Action | Who | By when | Consequence if skipped |
|---|---|---|---|


If none: "None."

## Breaking changes
Each with: what changed, why, and the migration path.

## New
## Improved
## Fixed
Reference the issue or defect ID.

## Security
Advisory IDs, severity, and whether exploitation was observed.

## Deprecated
| Item | Deprecated in | Removed in | Replacement |
|---|---|---|---|


## Known issues
| Issue | Impact | Workaround | Fix expected |
|---|---|---|---|


## Upgrade notes
Order of operations, downtime, compatibility window, rollback.
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Provisioning API v1.14.0 — 2026-11-12

## Summary
Adds re-resolution of pending requests and tightens bundle version handling.
Callers who read `bundle_version` should note it is now always present.
One security fix, no exploitation observed.

## Action required
| Action | Who | By when | Consequence if skipped |
|---|---|---|---|
| Stop relying on `GET /requests?state=PENDING` — it is removed in v2 | Service desk tooling team | 2027-02-28 | Tooling breaks at the v2 cutover |
| Upgrade the Go client to >= 1.9.0 if you parse `bundle_version` | All API consumers | Before v1.15.0 | Older clients reject the now-always-present field |


## Breaking changes
None in v1. See Deprecated for what changes in v2.

## New
- `POST /requests/{id}/re-resolve` re-evaluates a pending request against the
  current bundle. Requires `provisioning.write` and a justification of at least
  20 characters. Both the old and new bundle version appear in the audit record.
  (AP-131)
- `RateLimit-*` response headers on all endpoints. (AP-140)

## Improved
- Bundle resolution p95 down from 240 ms to 55 ms by caching immutable bundle
  versions. No behaviour change. (AP-138)
- Clearer error when a job code has no bundle: `bundle_not_found` now includes
  the job code in `details`. (AP-142)

## Fixed
- DEF-2026-0311: a request whose pinned bundle version was missing silently fell
  back to the latest version, so a grant could trace to the wrong rule. It now
  fails with `bundle_version_missing` and alerts. Affected 3 requests between
  2026-10-28 and 2026-11-04; all three were reviewed and re-issued, and
  Internal Audit was notified on 2026-11-05.
- DEF-2026-0318: the 72-hour approval escalation did not fire if the service
  restarted within the window. Timers are now persisted.

## Security
- GHSA-xxxx-yyyy-zzzz (High) in a transitive JSON dependency, allowing
  excessive memory allocation on malformed input. Dependency updated. Our
  ingress limits request bodies to 256 KB, so exploitation was not possible
  through the public path; no exploitation observed in logs.

## Deprecated
| Item | Deprecated in | Removed in | Replacement |
|---|---|---|---|
| `GET /requests?state=PENDING` (the PENDING pseudo-state) | v1.14.0 | v2.0.0 (no earlier than 2027-03-01) | `?state=AWAITING_APPROVAL` or `?state=AWAITING_BUNDLE` |
| `X-Request-Trace` header | v1.12.0 | v2.0.0 | `X-Correlation-Id` |


Deprecated endpoints return `Deprecation` and `Sunset` headers from this
release onwards.

## Known issues
| Issue | Impact | Workaround | Fix expected |
|---|---|---|---|
| Legacy ERP revocation runs on the nightly batch | Worst-case 26h revocation latency vs the 1h target | Daily exception report reviewed by People Ops | Blocked on the ERP replacement, FY2027 |


## Upgrade notes
Rolling deploy, no downtime. The database migration is additive and reversible.
Rollback to v1.13.x is safe: `bundle_version` is ignored by that release.
{{< /doctabs >}}

## Common mistakes

- **A generated commit list.** Nobody upgrades because of "Merge pull request #482". Write for the reader's decision, not the tool's convenience.
- **Burying the required action.** If a reader must do something, it goes at the top with a date.
- **Vague security entries.** "Fixed a security issue" invites everyone to assume the worst. Give the advisory ID, severity, and whether exploitation was possible in your configuration.
- **Deprecation without a removal date.** Consumers will not act, and you will be unable to remove the thing.
- **Silent fixes of data-affecting bugs.** The DEF-2026-0311 entry above names the blast radius and the notification. Omitting that is how a defect becomes an audit finding.

## Related templates

- [Deployment Runbook](/docs/development-release/deployment-runbook/) — how this release actually reaches production.
- [API Specification](/docs/architecture-design/api-specification/) — the versioning policy these notes follow.
- [Defect Report](/docs/testing-qa/defect-report/) — the source of the Fixed section.
- [Change Request](/docs/operations-incident/change-request/) — the approval record for the deployment.
- [Development & Release](/docs/development-release/) — the other four development and release templates.
