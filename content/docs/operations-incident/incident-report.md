---
weight: 6020
title: "Incident Report"
description: "The factual record of an outage: timeline, impact, actions — written during and immediately after, not weeks later."
icon: "report"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

An incident report records what happened. It is deliberately separate from the [Postmortem](/docs/operations-incident/postmortem/), which asks why. Keeping them apart lets the report be published within a day, while memories and logs are fresh, without waiting for analysis to conclude.

## When to use it

- Any incident meeting the declaration threshold: customer impact, data risk, security event, or an SLO breach.
- Also for near misses where only luck prevented impact — those are the cheapest lessons available.

## What it must answer

- What was the impact, on whom, and for how long?
- What is the timeline, in UTC, with sources?
- What did we do, and what actually helped?
- What is still outstanding?

## Template

```markdown
# Incident <ID>: <Short factual title>

| Field | Value |
|---|---|
| Severity | |
| Status | Active / Mitigated / Resolved |
| Detected | UTC, and by what |
| Mitigated | UTC |
| Resolved | UTC |
| Duration of impact | |
| Incident commander | |
| Services affected | |

## Impact
Who, how many, what they could not do, and any financial or regulatory effect.

## Timeline (UTC)
| Time | Event | Source |
|---|---|---|

Facts only. Analysis goes in the postmortem.

## Detection
How we found out, and whether monitoring or a human found it first.

## Actions taken
| Time | Action | By | Effect |
|---|---|---|---|

## Current state
What is fixed, what is on a workaround, what is still degraded.

## Follow-up items
| # | Item | Owner | Due | Tracker |
|---|---|---|---|---|

## Communications
| Time | Audience | Channel | Message summary |
|---|---|---|---|

## Data and security impact
Any data loss, exposure or integrity issue. State "none identified" explicitly.
```

## Worked example

```markdown
# Incident INC-2026-0207: Joiner provisioning stalled for 9 hours

| Field | Value |
|---|---|
| Severity | Sev-2 |
| Status | Resolved |
| Detected | 2026-12-03 07:12 UTC, by a People Ops report — not by monitoring |
| Mitigated | 2026-12-03 07:58 UTC |
| Resolved | 2026-12-03 11:40 UTC |
| Duration of impact | 2026-12-02 22:31 to 2026-12-03 07:58 UTC (9h 27m) |
| Incident commander | J. Marek |
| Services affected | Access Provisioning Service (scheduled actions only) |

## Impact
Fourteen joiners due to start on 2026-12-03 did not have access at 08:00 local
time. Eleven were provisioned by 08:30 after mitigation; three required manual
intervention because their start-date action had already been skipped. Six
approval escalations did not fire, delaying two additional joiners by one day.
No access was granted incorrectly. No data loss. Estimated cost: roughly 20
person-hours of lost productivity plus 3 hours of People Ops effort.

## Timeline (UTC)
| Time | Event | Source |
|---|---|---|
| 2026-12-02 22:29 | Routine node pool upgrade drains the node running the poller leader | Cluster audit log |
| 2026-12-02 22:31 | Poller leader lease expires; no new leader elected | Service logs |
| 2026-12-02 22:41 | `PROV_DUE_ACTIONS_OVERDUE` condition first true | Metrics (retrospective) |
| 2026-12-02 22:41 | Alert not delivered — routed to a Slack channel deleted on 2026-11-19 | PagerDuty routing config |
| 2026-12-03 07:12 | People Ops reports that four joiners have no access | #platform-support |
| 2026-12-03 07:19 | Incident declared, Sev-2, J. Marek commanding | Incident channel |
| 2026-12-03 07:31 | `due_action` backlog identified: 1,204 pending, oldest 8h51m | Investigation |
| 2026-12-03 07:44 | `provctl poller elect --force` executed | Command log |
| 2026-12-03 07:58 | Backlog drained to 0; provisioning resumed | Metrics |
| 2026-12-03 08:30 | 11 of 14 affected joiners confirmed provisioned | People Ops |
| 2026-12-03 09:50 | 3 remaining joiners provisioned manually via re-resolve | Audit log |
| 2026-12-03 11:40 | Alert routing corrected and verified with a test alert; resolved | PagerDuty |

## Detection
Monitoring detected the condition at 22:41 but the alert was never delivered:
its notification target was a Slack channel deleted two weeks earlier, and
PagerDuty had no fallback route. The incident was found by a human 8h31m later.
This detection gap is the most significant finding and is the primary subject
of the postmortem.

## Actions taken
| Time | Action | By | Effect |
|---|---|---|---|
| 07:44 | Forced leader election | J. Marek | Poller resumed; backlog drained in 14 min |
| 08:05 | Paused the node pool upgrade for the remaining nodes | J. Marek | Prevented recurrence during the incident |
| 09:50 | Manually re-resolved 3 requests whose start-date action was skipped | T. Blomqvist | Joiners provisioned; both actions audited |
| 11:20 | Added a fallback route on the PagerDuty service | J. Marek | Undelivered alerts now escalate to the primary |

## Current state
Resolved. Poller is running with a leader; backlog is zero. Alert routing has a
fallback and was verified with a test alert at 11:38. The underlying fragility —
a single-leader poller with no liveness alert of its own — is unchanged and is
the subject of follow-up item 2.

## Follow-up items
| # | Item | Owner | Due | Tracker |
|---|---|---|---|---|
| 1 | Audit every alert route for deleted or invalid targets | J. Marek | 2026-12-10 | OPS-881 |
| 2 | Poller emits a heartbeat; alert on heartbeat absence rather than only on backlog | A. Vogel | 2026-12-19 | OPS-882 |
| 3 | Node pool upgrades drain leader-holding pods gracefully with lease handover | Platform | 2027-01-16 | OPS-884 |
| 4 | Add a synthetic joiner every hour and alert if it is not provisioned | H. Ito | 2027-01-16 | OPS-885 |

## Communications
| Time | Audience | Channel | Message summary |
|---|---|---|---|
| 07:25 | People Ops, service desk | #platform-support | Incident declared, investigating, manual workaround available |
| 08:05 | Same | #platform-support | Mitigated; confirming affected joiners |
| 12:00 | Engineering leadership | Email | Summary, impact, follow-ups, postmortem scheduled 2026-12-05 |

## Data and security impact
None identified. No entitlement was granted without approval; the audit log
shows a complete record for all 14 affected requests, including the three
manual re-resolves. Delayed revocation was not in scope — no leaver event fell
in the affected window (verified against the HR feed).
```

## Common mistakes

- **Analysis mixed into the timeline.** "The poller failed because leases are fragile" is a hypothesis. The timeline holds observations with sources; the reasoning belongs in the postmortem.
- **Impact described in system terms.** "The poller was down" is not impact. "Fourteen joiners had no access on their first morning" is.
- **Timeline without sources.** Six weeks later nobody can distinguish a logged fact from a recollection.
- **Follow-up items without owners and dates.** They will not happen, and the next incident will be the same one.
- **Omitting "no data impact identified".** Saying nothing leaves the reader to assume the worst, and gives audit nothing to rely on.

## Related templates

- [Postmortem](/docs/operations-incident/postmortem/) — the analysis that follows this report.
- [Operational Runbook](/docs/operations-incident/operational-runbook/) — where the fix procedure should have lived.
- [Defect Report](/docs/testing-qa/defect-report/) — for the underlying code defect, if there is one.
- [On-call Handover](/docs/operations-incident/on-call-handover/) — how an active incident crosses a shift boundary.
