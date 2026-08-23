---
weight: 4050
title: "Deployment Runbook"
description: "The exact sequence to ship a release, verify it, and back it out — written before the deployment starts."
icon: "rocket_launch"
date: "2026-08-23"
draft: false
---

A deployment runbook is executed under time pressure by someone who may not have written the change. Every step should be a command that can be copied, and every step should have a way to tell whether it worked. The rollback section is written first, not last.

## When to use it

- Any deployment involving a migration, a cutover, a coordinated multi-service change, or an out-of-hours window.
- Not for routine continuous deployment where the pipeline is the runbook — in that case document the pipeline's abort and rollback behaviour instead.

## What it must answer

- What must be true before we start, and who says go?
- What exactly do we run, in what order, and how do we know each step worked?
- At what point does rollback become impossible, and what is the plan after that?
- Who is watching what, for how long, afterwards?

## Template

{{< doctabs >}}
# Deployment Runbook: <Release / change>

| Field | Value |
|---|---|
| Change reference | CR-xxxx |
| Scheduled window | |
| Deployer | |
| Approver present | |
| Comms channel | |
| Expected duration | |
| Point of no return | Step N |

## 1. Pre-checks (T-24h)
- [ ] Change approved
- [ ] CI green on the exact commit: <sha>
- [ ] Backup verified, restore tested: <evidence>
- [ ] Dependent teams notified
- [ ] Rollback rehearsed in staging on <date>

## 2. Go/no-go (T-0)
| Condition | Check | Go? |
|---|---|---|

## 3. Steps
| # | Action | Command | Expected result | Verify | Owner |
|---|---|---|---|---|---|

Mark the point of no return explicitly.

## 4. Verification
| Check | How | Pass criteria | Owner |
|---|---|---|---|

## 5. Rollback
Trigger conditions, procedure, expected duration, data implications.

## 6. Post-deployment
Monitoring period, who watches what, when the change is declared stable.

## 7. Comms
Who is told at start, at completion, and on rollback.
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Deployment Runbook: Provisioning API v1.14.0

| Field | Value |
|---|---|
| Change reference | CR-2026-0884 |
| Scheduled window | 2026-11-12, 07:00–08:00 UTC (before the HR feed's 09:00 burst) |
| Deployer | J. Marek |
| Approver present | A. Vogel |
| Comms channel | #platform-deploys |
| Expected duration | 25 minutes |
| Point of no return | Step 5 (migration applied) |

## 1. Pre-checks (T-24h)
- [x] CR-2026-0884 approved at CAB 2026-11-10
- [x] CI green on commit 9f3c1ab
- [x] Postgres PITR verified; restore of a 2026-11-09 snapshot into staging
      completed in 41 minutes
- [x] Service desk notified — bulk import unavailable for ~10 minutes
- [x] Rollback rehearsed in staging 2026-11-07

## 2. Go/no-go (T-0)
| Condition | Check | Go? |
|---|---|---|
| No open Sev-1/2 incident | Incident board | |
| Error rate at baseline | Dashboard "Provisioning — pipeline" | |
| No HR bulk load running | `SELECT count(*) FROM due_action WHERE state='RUNNING'` returns 0 | |
| Approver present | — | |

## 3. Steps
| # | Action | Command | Expected result | Verify | Owner |
|---|---|---|---|---|---|
| 1 | Announce start | post in #platform-deploys | — | — | J. Marek |
| 2 | Pause the HR ingest consumer | `provctl ingest pause` | "paused" | `provctl ingest status` shows paused | J. Marek |
| 3 | Confirm the pipeline has drained | — | 0 requests in APPLYING | `requests_by_state{state="APPLYING"}` = 0 on dashboard | J. Marek |
| 4 | Snapshot the database | `provctl db snapshot --tag pre-1.14.0` | Snapshot ID printed | Snapshot listed and marked complete | J. Marek |
| 5 | **Apply migration (point of no return for schema)** | `provctl migrate up --to 0042` | "applied 1 migration" | `provctl migrate status` shows 0042 current | J. Marek |
| 6 | Deploy v1.14.0 | `provctl deploy --version 1.14.0` | Rolling update completes | All pods Ready, version endpoint reports 1.14.0 | J. Marek |
| 7 | Resume ingest | `provctl ingest resume` | "running" | Backlog drains within 5 minutes | J. Marek |
| 8 | Announce completion | post in #platform-deploys | — | — | J. Marek |

Migration 0042 is additive (adds a nullable column and an index) and is
reversible with `migrate down --to 0041`; "point of no return" here means any
rollback after step 5 must go through the documented down-migration rather than
a simple redeploy.

## 4. Verification
| Check | How | Pass criteria | Owner |
|---|---|---|---|
| Service healthy | `/healthz` on each pod | All 200 | J. Marek |
| Contract tests | `make contract-test ENV=prod-readonly` | All pass | H. Ito |
| Real request end to end | Create a test request for job code TEST-1 | Reaches COMPLETE, audit record written | H. Ito |
| Error rate | Dashboard, 15 minutes | 5xx rate <= baseline + 0.1pp | A. Vogel |
| New metric present | `grants_with_missing_bundle_version` | Exists and is 0 | J. Marek |

## 5. Rollback
**Trigger any of:** 5xx rate above baseline + 1pp for 5 minutes; any request
reaching PARTIAL that would not have before; contract tests failing;
`grants_with_missing_bundle_version` > 0.

**Procedure (approx. 12 minutes):**
1. `provctl ingest pause`
2. `provctl deploy --version 1.13.4`
3. `provctl migrate down --to 0041` — only if v1.13.4 fails to start; the
   column is otherwise ignored and can stay.
4. `provctl ingest resume`
5. Verify with the same checks in section 4.

**Data implications:** requests created under v1.14.0 have a populated
`bundle_version`, which v1.13.4 ignores. No data loss on rollback. Any
re-resolve actions performed under v1.14.0 remain in the audit log and cannot
be undone — this is intentional.

## 6. Post-deployment
Deployer watches the dashboard for 60 minutes. On-call is briefed at handover.
The change is declared stable after the next HR bulk event (09:00) processes
cleanly. If stable, close CR-2026-0884 by 12:00.

## 7. Comms
Start and completion in #platform-deploys. On rollback: #platform-deploys plus
a direct message to the service desk lead, since bulk import stays paused
during rollback.
{{< /doctabs >}}

## Common mistakes

- **Steps described rather than given.** "Apply the migration" leaves the deployer guessing at flags at 07:00. Paste the command.
- **No verification per step.** Without it, a half-failed step is discovered three steps later, with unclear state.
- **Rollback written after the deployment section.** Writing it first often changes the deployment design — a rollback you cannot describe is a deployment you should not do.
- **The point of no return left implicit.** People need to know when the cheap option expires.
- **Written once, never re-run.** A runbook that has not been executed in staging is a hypothesis.

## Related templates

- [Release Notes](/docs/development-release/release-notes/) — what this deployment delivers.
- [Change Request](/docs/operations-incident/change-request/) — the approval this runbook executes.
- [Operational Runbook](/docs/operations-incident/operational-runbook/) — the steady-state equivalent.
- [Incident Report](/docs/operations-incident/incident-report/) — what to open if rollback triggers.
- [Development & Release](/docs/development-release/) — the other four development and release templates.
