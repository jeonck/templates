---
weight: 6050
title: "On-call Handover"
description: "Live context passed between shifts, so the next engineer does not start from zero."
icon: "swap_horiz"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

Everything a handover needs is already somewhere — in dashboards, tickets, incident channels. The point of writing it down is that the incoming engineer should not have to reconstruct it from six places at the start of a shift, and definitely not at 02:00.

## When to use it

- Every rotation change, even a quiet one — "nothing outstanding" is useful information.
- At the start and end of a shift spanning an active incident.
- Before planned absence, when a service's only informed person will be unavailable.

## What it must answer

- What is currently broken or degraded?
- What is expected to happen during your shift?
- What is fragile right now, and what do I do if it moves?
- What did I try that did not work, so you do not repeat it?

## Template

{{< doctabs >}}
# On-call handover: <rotation> — YYYY-MM-DD HH:MM UTC

**Outgoing:** name    **Incoming:** name

## Active incidents
| ID | Sev | State | What is needed next | Channel |
|---|---|---|---|---|

## Degraded or on a workaround
| Service | State | Workaround in place | Expires / needs attention |
|---|---|---|---|

## Expected during your shift
| When | What | Whose | What to do if it goes wrong |
|---|---|---|---|

## Watch list
Things not yet broken but trending badly, with the threshold that matters.

## Known noise
Alerts that will fire and are expected — with the reason and the ticket.

## Tried and did not work
So the next person does not repeat it.

## Access and escalation notes
Anything unusual about who is reachable.
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# On-call handover: platform-primary — 2026-12-03 18:00 UTC

**Outgoing:** J. Marek    **Incoming:** P. Nowak

## Active incidents
| ID | Sev | State | What is needed next | Channel |
|---|---|---|---|---|
| INC-2026-0207 | Sev-2 | Resolved 11:40, monitoring | Nothing unless the poller backlog rises again. Postmortem is Friday; do not start analysis in the channel | #inc-2026-0207 |

## Degraded or on a workaround
| Service | State | Workaround | Expires / needs attention |
|---|---|---|---|
| Provisioning | Bundle clean-up admin action disabled since 2026-11-04 | Manual, by config flag | Stays until v1.14.0 ships (2026-11-12 — already shipped; flag can now be re-enabled, ticket OPS-878 open, not urgent) |
| Provisioning poller | Running normally, but no heartbeat alert yet (OPS-882 in progress) | Backlog alert only, now routed correctly | If the backlog alert fires, check leader identity first — it is on the pipeline dashboard as of today |
| Node pool upgrades | Paused on 3 remaining nodes since 08:05 | Manual pause | Security wants them completed by 2026-12-06. Do not resume during your shift; A. Vogel is coordinating with the lease handover fix |

## Expected during your shift
| When | What | Whose | What to do if it goes wrong |
|---|---|---|---|
| 22:00 UTC | HR nightly batch, ~40 events | HR platform | Expect a brief backlog; it should clear within 15 min. If not, check adapters before assuming the poller |
| 23:30 UTC | Legacy ERP nightly provisioning batch | ERP team | Failures show as PARTIAL requests plus tickets. Not a page — the daily exception report catches it. ERP on-call is #erp-oncall but they do not staff overnight |
| 02:00 UTC | Certificate renewal on the admin ingress (automated) | Platform | Runbook section 7. Manual renewal command is there; takes 4 minutes |

## Watch list
- Postgres primary disk at 71%, rising ~1.5pp/week. Alert threshold 85%. Not
  your problem this shift, but if it jumps more than 3pp overnight, something
  is writing more than it should — check the audit table partition size first.
- One adapter (the HR-adjacent directory) has been at a 3–4% error rate all
  week, well below the 20% alert. Retries absorb it. Ticket OPS-879.

## Known noise
- `PROV_ADAPTER_ERROR_RATE` for the ERP target will fire around 23:35 and clear
  by 23:50. Expected — the batch closes its connection abruptly. Ticket
  OPS-860, fix scheduled but not started. Do not escalate.

## Tried and did not work
- During INC-2026-0207 I tried `provctl poller restart` before forcing an
  election. It did not help, because the stale lease had not expired; the pod
  restarted and waited. `provctl poller elect --force` is the command that
  works. The runbook now says so.

## Access and escalation notes
A. Vogel is on a flight 20:00–23:30 UTC and unreachable. Secondary escalation
for anything provisioning-related is H. Ito, who ran the test cycle and knows
the system well. DBA on-call rotation changed on Monday: it is now
#dba-oncall-eu, not the old channel, which still exists and is unmonitored.
{{< /doctabs >}}

## Common mistakes

- **"All quiet" when it is not.** The watch list is exactly what the incoming engineer cannot see for themselves.
- **Omitting known noise.** An engineer paged by an expected alert wastes twenty minutes and loses trust in the alert set.
- **No "tried and did not work".** This is the highest-value section per line and is almost always left out.
- **Handover only in chat.** A written artefact survives the shift; a chat thread scrolls away and cannot be read at the start of the next handover.
- **Escalation contacts assumed current.** Rotations and channels change. The one time it matters is at 02:00.

## Related templates

- [Operational Runbook](/docs/operations-incident/operational-runbook/) — the standing procedures this assumes.
- [Incident Report](/docs/operations-incident/incident-report/) — for incidents crossing a shift boundary.
- [Change Request](/docs/operations-incident/change-request/) — the source of "expected during your shift".
- [Operations & Incident](/docs/operations-incident/) — the other four operations and incident templates.
