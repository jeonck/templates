---
weight: 6010
title: "Operational Runbook"
description: "What to do when the alert fires, written for someone half asleep who did not build the system."
icon: "menu_book"
date: "2026-08-23"
draft: false
---

A runbook is read in the worst conditions a document ever faces: at night, under stress, by someone unfamiliar with the system. Optimise for that reader. Commands to copy, one alert per section, and an explicit "if this does not work, escalate to" line.

## When to use it

- Before any service goes live — an on-call rotation without runbooks is an on-call rotation that pages the author every time.
- After every incident that revealed a missing procedure.
- Alongside each alert: if an alert has no runbook section, either write one or delete the alert.

## What it must answer

- What does this service do, and what does it depend on?
- For each alert: what does it mean, how do I check, what do I do?
- What am I allowed to do without waking someone up?
- Who do I escalate to, and when?

## Template

{{< doctabs >}}
# Runbook: <Service>

| Field | Value |
|---|---|
| Owning team | |
| On-call rotation | |
| Escalation | L1 -> L2 -> owner |
| Dashboards | |
| Logs | |
| Source | repo link |
| Last reviewed | |


## 1. What this service does
Three sentences. Business impact if it is down.

## 2. Dependencies
| Depends on | Impact if unavailable | Their on-call |
|---|---|---|


## 3. Health checks
How to tell in 60 seconds whether it is healthy.

## 4. Alerts
### <ALERT_NAME>
- **Means:**
- **Impact:**
- **Check:** commands
- **Fix:** steps
- **If that fails:** escalation
- **Do not:** actions that make it worse

## 5. Common procedures
Restart, scale, drain, replay, pause, backfill.

## 6. Safe / unsafe actions
| Action | Safe? | Notes |
|---|---|---|


## 7. Maintenance
Certificates, credential rotation, log volume, capacity headroom.

## 8. Recovery
Backup locations, restore procedure, RPO/RTO, last exercise date.

## 9. Known issues
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Runbook: Access Provisioning Service

| Field | Value |
|---|---|
| Owning team | Platform Identity |
| On-call | #platform-oncall, PagerDuty schedule "platform-primary" |
| Escalation | Primary -> secondary (15 min) -> A. Vogel (30 min) |
| Dashboards | "Provisioning — pipeline", "Provisioning — adapters" |
| Last reviewed | 2026-11-30 |


## 1. What this service does
Grants and revokes system access for employees, driven by HR events. If it is
down, new joiners do not get access and leavers are not revoked on time. It is
not customer-facing: a four-hour outage during the working day is a
significant problem; a four-hour outage overnight usually is not.

## 2. Dependencies
| Depends on | Impact if unavailable | Their on-call |
|---|---|---|
| HR feed (webhook) | No new events; existing queue still drains | #hr-platform |
| Postgres (primary) | Service is down; requests queue at ingest | #dba-oncall |
| Secrets manager | Adapters fail auth after the current lease expires (max 1h) | #security-oncall |
| Target systems (11) | Only those entitlements fail; requests end PARTIAL | Varies — see adapter table |


## 3. Health checks
Sixty-second triage, in this order:

`provctl status` — one line per component.
`provctl poller status` — is a leader elected, and how old is the lease?
`provctl adapter status --all` — per-target error rate and retry backlog.

Healthy is: a leader elected with a lease under 30 seconds old, zero overdue
due-actions, every adapter under a 5% error rate, and nothing stuck in
APPLYING for more than a few minutes on the pipeline dashboard. If all four
hold, this service is fine and the problem is somewhere else.

## 4. Alerts

### PROV_DUE_ACTIONS_OVERDUE
- **Means:** the poller has not processed scheduled actions for over 10 minutes.
  Approval escalations and start-date applications are stalled.
- **Impact:** joiners may not have access on their start date. Silent — nobody
  will report it until someone cannot log in.
- **Check:**
  `provctl poller status` — is a leader elected?
  `SELECT count(*), min(due_at) FROM due_action WHERE state='PENDING' AND due_at < now();`
- **Fix:**
  1. If no leader: `provctl poller elect --force` and confirm within 60s.
  2. If a leader exists but is stuck, restart it: `provctl restart poller`.
     Safe at any time — due actions are idempotent.
  3. Confirm the overdue count returns to 0 within 5 minutes.
- **If that fails:** escalate to secondary. Do not delete rows from
  `due_action` to clear the alert — that silently drops joiner provisioning.
- **Do not:** run the poller in two places manually. Two leaders double-apply
  entitlements, which is a security-relevant event requiring an incident.

### PROV_ADAPTER_ERROR_RATE
- **Means:** one adapter is failing more than 20% of calls over 5 minutes.
- **Impact:** entitlements for that target are not applied; requests end
  PARTIAL and tickets accumulate. Everything else continues.
- **Check:** dashboard "Provisioning — adapters", identify which target.
  `provctl adapter status <target>` shows last error and retry state.
- **Fix:**
  1. If the target is in a known maintenance window (see #change-calendar),
     pause the adapter: `provctl adapter pause <target>`. Queued work resumes
     when unpaused. Note it in the incident channel.
  2. If auth errors: check credential lease age with
     `provctl secrets status <target>`. Rotate with
     `provctl secrets rotate <target>` — safe, takes ~30 seconds.
  3. Otherwise contact the target system's on-call from the adapter table.
- **If that fails:** if more than 3 adapters are affected, this is likely
  network or secrets, not the targets. Escalate to secondary immediately.
- **Do not:** raise retry limits to push work through. That was the cause of
  INC-2026-0142, where nested retries turned a 30-second blip into 40 minutes.

### PROV_MISSING_BUNDLE_VERSION
- **Means:** a grant referenced a bundle version that does not exist.
- **Impact:** security-relevant. A grant may be unattributable.
- **Check:** `provctl audit orphan-grants --since 24h`
- **Fix:** none at 3am. Page the owner (A. Vogel) regardless of hour, and open
  a Sev-1 incident. Do not attempt to reconstruct the bundle version.

## 5. Common procedures
**Pause and resume ingest** — `provctl ingest pause` / `resume`. Events queue
at the webhook for up to 24 hours with no loss. Do this before any deploy.

**Pause one adapter** — `provctl adapter pause <target>` / `resume <target>`.
Other targets keep working, but requests needing the paused target end PARTIAL
and raise tickets, so prefer this only for a known maintenance window.

**Rotate a target's credentials** — `provctl secrets rotate <target>`. About
30 seconds of auth failures during the swap, absorbed by adapter retries.

**Replay a stuck request** — `provctl request replay <id>`. Idempotent:
already-applied entitlements are not re-applied. Never edit `request.state`
directly to achieve the same thing.

**Drain before maintenance** — pause ingest, then wait for
`requests_by_state{state="APPLYING"}` to reach zero. Under two minutes outside
the 09:00 burst.

## 6. Safe / unsafe actions
| Action | Safe? | Notes |
|---|---|---|
| Restart any service pod | Yes | Stateless; in-flight work resumes from the database |
| Pause ingest | Yes | Events queue at the webhook; no loss for up to 24h |
| Pause an adapter | Yes | Other targets unaffected |
| Rotate adapter credentials | Yes | ~30s of failures during rotation |
| Delete rows from `due_action` | **No** | Silently drops provisioning; no recovery path |
| Edit `request.state` directly | **No** | Bypasses the audit log; creates states the application cannot produce |
| Re-run a completed request | **No** | Use the re-resolve action, which is audited |


## 7. Maintenance
| Task | Cadence | Owner | Notes |
|---|---|---|---|
| Target credential rotation | 90 days, automated | Platform | Alerts if any credential passes 90 days; rotate with the command in section 5 |
| Admin ingress certificate | 90 days, automated at 02:00 | Platform | Manual fallback `provctl cert renew --ingress admin` |
| Audit export to cold storage | Monthly, automated | Security | Failure alerts within 2h; a missed month is a reportable control gap, not a nuisance |
| Bundle version pruning | Never | — | Deliberately disabled: deleting a pinned bundle version breaks grant attribution, which caused DEF-2026-0311 |
| Postgres disk headroom | Weekly glance | Platform | Alert at 85%; growth ~1.5pp/week, dominated by the audit table |
| DR exercise | Every 6 months | Platform | Last 2026-10-22, next due 2027-04 |


## 8. Recovery
Postgres PITR, 15-minute RPO, snapshots retained 35 days. Restore procedure is
in the DBA runbook, section 4. Last DR exercise 2026-10-22: RTO 2h51m against
a 4h target. Next exercise due 2027-04.

## 9. Known issues
- Legacy ERP revokes on the nightly batch only; worst case 26h latency against
  a 1h target. The daily exception report (delivered 07:00 to People Ops) is
  the compensating control. Do not raise an incident for this — it is expected.
{{< /doctabs >}}

## Common mistakes

- **Alerts with no runbook section.** The on-call engineer then improvises, and improvisation at 3am is how small incidents become large ones.
- **No "do not" list.** The dangerous action is usually the one that appears to clear the alert fastest.
- **Describing commands instead of giving them.** "Check the poller's leadership status" versus a command that can be pasted — the difference is minutes and mistakes.
- **Never reviewed.** Commands rot. A runbook not reviewed in a year is a set of confident-sounding wrong instructions.
- **Missing the "expected, do not escalate" section.** Known issues that page people erode trust in every other alert.

## Related templates

- [Incident Report](/docs/operations-incident/incident-report/) — what to open when the runbook does not resolve it.
- [On-call Handover](/docs/operations-incident/on-call-handover/) — carries live context between shifts.
- [Technical Design Document](/docs/architecture-design/technical-design-document/) — the failure modes table feeds section 4.
- [Deployment Runbook](/docs/development-release/deployment-runbook/) — the change-time counterpart.
- [Operations & Incident](/docs/operations-incident/) — the other four operations and incident templates.
