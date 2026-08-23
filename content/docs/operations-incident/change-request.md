---
weight: 6040
title: "Change Request"
description: "The approval record for a production change: what, when, risk, backout, and who said yes."
icon: "change_circle"
date: "2026-08-23"
draft: false
---

A change request exists so that someone other than the implementer assesses risk before a production change, and so there is a record afterwards. It becomes bureaucracy when every change gets the same scrutiny — the useful version has clear categories with genuinely different paths.

## When to use it

- Production changes affecting shared services, data, or anything under a regulatory or contractual obligation.
- Standard, pre-approved changes still need a record — but not a meeting.
- Emergency changes get retrospective approval, on a defined deadline.

## What it must answer

- What is changing, when, and who is doing it?
- What is the risk, and what happens if it goes wrong?
- How do we back it out, and how long does that take?
- Who approved it, and on what basis?

## Template

{{< doctabs >}}
# Change Request CR-<id>

| Field | Value |
|---|---|
| Title | |
| Type | Standard (pre-approved) / Normal / Emergency |
| Risk | Low / Medium / High |
| Requested by / team | |
| Implementer | |
| Window | start–end, timezone |
| Services affected | |
| Customer impact | None / Degraded / Outage — with duration |
| Related | Release notes, runbook, incident |


## 1. Description
What changes, in one paragraph a non-specialist can follow.

## 2. Justification
Why now, and what happens if we do not.

## 3. Risk assessment
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|


## 4. Implementation plan
Link the deployment runbook; do not duplicate it.

## 5. Verification
How we will know it worked.

## 6. Backout plan
Trigger, procedure, duration, and the point after which backout is not possible.

## 7. Communications
Who is told, when.

## 8. Approvals
| Role | Name | Decision | Date | Conditions |
|---|---|---|---|---|


## 9. Post-implementation review
Completed as planned? Issues? Actual duration?
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Change Request CR-2026-0884

| Field | Value |
|---|---|
| Title | Deploy Provisioning API v1.14.0 (bundle version pinning fix) |
| Type | Normal |
| Risk | Medium |
| Requested by | Platform Identity |
| Implementer | J. Marek |
| Window | 2026-11-12 07:00–08:00 UTC |
| Services affected | Access Provisioning Service; bulk import unavailable ~10 min |
| Customer impact | Degraded — bulk import paused; no impact on individual provisioning |
| Related | Release notes v1.14.0; deployment runbook; DEF-2026-0311 |


## 1. Description
Deploys the fix for DEF-2026-0311, where a provisioning request could apply a
different bundle version from the one recorded against it, producing a grant
that cannot be traced to a rule. The change makes that condition an error and
adds an alert. Also adds the re-resolve endpoint and rate-limit headers.

## 2. Justification
DEF-2026-0311 is a Sev-1 control failure already reported to Internal Audit.
The current mitigation (disabling the bundle clean-up action) is manual and
easily undone by anyone with admin access. Delay keeps an audit finding open.

## 3. Risk assessment
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Migration fails mid-deploy | Low | Requests cannot be created until rolled back | Additive nullable column; rehearsed in staging 2026-11-07; snapshot taken at step 4 |
| Old pods reject inserts during the rolling window | Low | Transient errors; events queue and retry | Column is nullable in this release; NOT NULL deferred to the next |
| New error path fires on legitimate requests | Medium | Requests fail instead of applying the wrong bundle | Intended behaviour — failing safe is preferred. Alert routes to the platform on-call; volume expected to be zero |
| Window overlaps the HR feed burst | Low | Backlog | Window is before the 09:00 burst; ingest paused during deploy |


## 4. Implementation plan
See the deployment runbook for v1.14.0. Eight steps, ~25 minutes, point of no
return at step 5.

## 5. Verification
Health checks on all pods, read-only contract tests against production, one
end-to-end test request for job code TEST-1 reaching COMPLETE with an audit
record, 5xx rate within baseline + 0.1pp over 15 minutes, and the new metric
present and reading zero.

## 6. Backout plan
Trigger: 5xx above baseline + 1pp for 5 minutes, contract test failure, or any
unexpected PARTIAL request. Procedure: pause ingest, deploy v1.13.4, resume;
approximately 12 minutes. The down-migration is only needed if v1.13.4 fails to
start, since it ignores the new column. Backout remains possible throughout;
after step 5 it requires the down-migration rather than a simple redeploy.

## 7. Communications
#platform-deploys at start and completion. Service desk lead notified 24h ahead
about the bulk import pause, and directly on any rollback.

## 8. Approvals
| Role | Name | Decision | Date | Conditions |
|---|---|---|---|---|
| Service owner | A. Vogel | Approved | 2026-11-10 | — |
| CAB chair | D. Achebe | Approved | 2026-11-10 | Approver present in the window |
| Security | A. Berg | Approved | 2026-11-10 | Internal Audit notified when the fix is live |


## 9. Post-implementation review
Completed 2026-11-12 07:52 UTC, 8 minutes ahead of the window. All verification
passed. One deviation: the ingest backlog took 7 minutes to drain rather than
the expected 5, because an overnight HR batch had queued more events than
usual. No impact. CR closed 2026-11-12 11:40 after the 09:00 burst processed
cleanly.
{{< /doctabs >}}

## Common mistakes

- **One process for every change.** If a config toggle needs the same paperwork as a database migration, people will route around the process entirely.
- **Backout plan as "roll back the deployment".** For anything touching data that is a hypothesis, not a plan. Say what happens to records written under the new version.
- **Approvers who cannot assess the risk.** A signature from someone with no basis to judge adds delay and no safety. Pick approvers who can actually say no.
- **No post-implementation review.** Without it, the estimates in every future change request stay unexamined.
- **Emergency changes never regularised.** Define the retrospective approval deadline, and measure how many changes take the emergency path — a rising number means the normal path is broken.

## Related templates

- [Deployment Runbook](/docs/development-release/deployment-runbook/) — the plan this approves.
- [Release Notes](/docs/development-release/release-notes/) — what the change delivers.
- [Incident Report](/docs/operations-incident/incident-report/) — when a change causes one.
- [Meeting Minutes](/docs/project-management/meeting-minutes/) — the CAB's own record.
- [Operations & Incident](/docs/operations-incident/) — the other four operations and incident templates.
