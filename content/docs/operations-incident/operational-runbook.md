---
weight: 6010
title: "Operational Runbook"
description: "What to do when the alert fires, written for someone half asleep who did not build the system."
icon: "menu_book"
date: "2026-08-23"
lastmod: "2026-08-23"
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

{{< tabs tabTotal="2" >}}
{{% tab tabName="Rendered" %}}

**Runbook: &lt;Service&gt;**

| Field | Value |
|---|---|
| Owning team | |
| On-call rotation | |
| Escalation | L1 -> L2 -> owner |
| Dashboards | |
| Logs | |
| Source | repo link |
| Last reviewed | |

**1. What this service does**

Three sentences. Business impact if it is down.  

**2. Dependencies**

| Depends on | Impact if unavailable | Their on-call |
|---|---|---|

**3. Health checks**

How to tell in 60 seconds whether it is healthy.  

**4. Alerts**

**&lt;ALERT_NAME&gt;**

- **Means:**  
- **Impact:**  
- **Check:** commands  
- **Fix:** steps  
- **If that fails:** escalation  
- **Do not:** actions that make it worse  

**5. Common procedures**

Restart, scale, drain, replay, pause, backfill.  

**6. Safe / unsafe actions**

| Action | Safe? | Notes |
|---|---|---|

**7. Maintenance**

Certificates, credential rotation, log volume, capacity headroom.  

**8. Recovery**

Backup locations, restore procedure, RPO/RTO, last exercise date.  

**9. Known issues**

{{% /tab %}}
{{% tab tabName="Markdown" %}}

```markdown
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
```

{{% /tab %}}
{{< /tabs >}}

## Worked example

{{< tabs tabTotal="2" >}}
{{% tab tabName="Rendered" %}}

**Runbook: Access Provisioning Service**

| Field | Value |
|---|---|
| Owning team | Platform Identity |
| On-call | #platform-oncall, PagerDuty schedule "platform-primary" |
| Escalation | Primary -> secondary (15 min) -> A. Vogel (30 min) |
| Dashboards | "Provisioning — pipeline", "Provisioning — adapters" |
| Last reviewed | 2026-11-30 |

**1. What this service does**

Grants and revokes system access for employees, driven by HR events. If it is  
down, new joiners do not get access and leavers are not revoked on time. It is  
not customer-facing: a four-hour outage during the working day is a  
significant problem; a four-hour outage overnight usually is not.  

**2. Dependencies**

| Depends on | Impact if unavailable | Their on-call |
|---|---|---|
| HR feed (webhook) | No new events; existing queue still drains | #hr-platform |
| Postgres (primary) | Service is down; requests queue at ingest | #dba-oncall |
| Secrets manager | Adapters fail auth after the current lease expires (max 1h) | #security-oncall |
| Target systems (11) | Only those entitlements fail; requests end PARTIAL | Varies — see adapter table |

**4. Alerts**

**PROV_DUE_ACTIONS_OVERDUE**

- **Means:** the poller has not processed scheduled actions for over 10 minutes.  
&nbsp;&nbsp;Approval escalations and start-date applications are stalled.  
- **Impact:** joiners may not have access on their start date. Silent — nobody  
&nbsp;&nbsp;will report it until someone cannot log in.  
- **Check:**  
&nbsp;&nbsp;`provctl poller status` — is a leader elected?  
&nbsp;&nbsp;`SELECT count(*), min(due_at) FROM due_action WHERE state='PENDING' AND due_at &lt; now();`  
- **Fix:**  
&nbsp;&nbsp;1. If no leader: `provctl poller elect --force` and confirm within 60s.  
&nbsp;&nbsp;2. If a leader exists but is stuck, restart it: `provctl restart poller`.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Safe at any time — due actions are idempotent.  
&nbsp;&nbsp;3. Confirm the overdue count returns to 0 within 5 minutes.  
- **If that fails:** escalate to secondary. Do not delete rows from  
&nbsp;&nbsp;`due_action` to clear the alert — that silently drops joiner provisioning.  
- **Do not:** run the poller in two places manually. Two leaders double-apply  
&nbsp;&nbsp;entitlements, which is a security-relevant event requiring an incident.  

**PROV_ADAPTER_ERROR_RATE**

- **Means:** one adapter is failing more than 20% of calls over 5 minutes.  
- **Impact:** entitlements for that target are not applied; requests end  
&nbsp;&nbsp;PARTIAL and tickets accumulate. Everything else continues.  
- **Check:** dashboard "Provisioning — adapters", identify which target.  
&nbsp;&nbsp;`provctl adapter status &lt;target&gt;` shows last error and retry state.  
- **Fix:**  
&nbsp;&nbsp;1. If the target is in a known maintenance window (see #change-calendar),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pause the adapter: `provctl adapter pause &lt;target&gt;`. Queued work resumes  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;when unpaused. Note it in the incident channel.  
&nbsp;&nbsp;2. If auth errors: check credential lease age with  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`provctl secrets status &lt;target&gt;`. Rotate with  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`provctl secrets rotate &lt;target&gt;` — safe, takes ~30 seconds.  
&nbsp;&nbsp;3. Otherwise contact the target system's on-call from the adapter table.  
- **If that fails:** if more than 3 adapters are affected, this is likely  
&nbsp;&nbsp;network or secrets, not the targets. Escalate to secondary immediately.  
- **Do not:** raise retry limits to push work through. That was the cause of  
&nbsp;&nbsp;INC-2026-0142, where nested retries turned a 30-second blip into 40 minutes.  

**PROV_MISSING_BUNDLE_VERSION**

- **Means:** a grant referenced a bundle version that does not exist.  
- **Impact:** security-relevant. A grant may be unattributable.  
- **Check:** `provctl audit orphan-grants --since 24h`  
- **Fix:** none at 3am. Page the owner (A. Vogel) regardless of hour, and open  
&nbsp;&nbsp;a Sev-1 incident. Do not attempt to reconstruct the bundle version.  

**6. Safe / unsafe actions**

| Action | Safe? | Notes |
|---|---|---|
| Restart any service pod | Yes | Stateless; in-flight work resumes from the database |
| Pause ingest | Yes | Events queue at the webhook; no loss for up to 24h |
| Pause an adapter | Yes | Other targets unaffected |
| Rotate adapter credentials | Yes | ~30s of failures during rotation |
| Delete rows from `due_action` | **No** | Silently drops provisioning; no recovery path |
| Edit `request.state` directly | **No** | Bypasses the audit log; creates states the application cannot produce |
| Re-run a completed request | **No** | Use the re-resolve action, which is audited |

**8. Recovery**

Postgres PITR, 15-minute RPO, snapshots retained 35 days. Restore procedure is  
in the DBA runbook, section 4. Last DR exercise 2026-10-22: RTO 2h51m against  
a 4h target. Next exercise due 2027-04.  

**9. Known issues**

- Legacy ERP revokes on the nightly batch only; worst case 26h latency against  
&nbsp;&nbsp;a 1h target. The daily exception report (delivered 07:00 to People Ops) is  
&nbsp;&nbsp;the compensating control. Do not raise an incident for this — it is expected.

{{% /tab %}}
{{% tab tabName="Markdown" %}}

```markdown
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

## 8. Recovery
Postgres PITR, 15-minute RPO, snapshots retained 35 days. Restore procedure is
in the DBA runbook, section 4. Last DR exercise 2026-10-22: RTO 2h51m against
a 4h target. Next exercise due 2027-04.

## 9. Known issues
- Legacy ERP revokes on the nightly batch only; worst case 26h latency against
  a 1h target. The daily exception report (delivered 07:00 to People Ops) is
  the compensating control. Do not raise an incident for this — it is expected.
```

{{% /tab %}}
{{< /tabs >}}

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
