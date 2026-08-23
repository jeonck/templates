---
weight: 6030
title: "Postmortem"
description: "Blameless analysis of why an incident was possible, and what change would prevent the class of it."
icon: "history_edu"
date: "2026-08-23"
draft: false
---

A postmortem asks why the system allowed the incident, not who made a mistake. Blameless is not politeness — it is the only way to get the honest account of what people actually believed at the time, which is where the real causes live.

## When to use it

- After any Sev-1 or Sev-2 incident, and after significant near misses.
- After any incident where detection was slow, regardless of how small the impact was.
- Within a week of resolution — later than that, the reconstructed reasoning is less reliable than the logs.

## What it must answer

- What did people believe at each decision point, and why was that reasonable?
- Which contributing factors combined to make this possible?
- Why did detection take as long as it did?
- What change removes the whole class of problem, not just this instance?

## Template

{{< doctabs >}}
# Postmortem: <Incident ID> — <title>

| Field | Value |
|---|---|
| Incident | link to the incident report |
| Severity / impact | |
| Facilitator | |
| Participants | |
| Date of review | |
| Status | Draft / Reviewed / Actions tracked |

## 1. Summary
Five sentences a newcomer can understand.

## 2. Contributing factors
Not "the root cause". List the conditions that had to hold simultaneously.

| Factor | Why it existed | Why it was reasonable at the time |
|---|---|---|

## 3. What went well
Genuinely — the things worth keeping.

## 4. Detection analysis
Time to detect, why, and what would have detected it sooner.

## 5. Response analysis
Decision points, what was known at each, and what would have helped.

## 6. Where we got lucky
The things that could have made this much worse and did not.

## 7. Actions
| # | Action | Type (prevent/detect/mitigate) | Owner | Due | Tracker |
|---|---|---|---|---|---|

## 8. Actions we are deliberately not taking
With reasons.

## 9. Lessons for other teams
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Postmortem: INC-2026-0207 — Joiner provisioning stalled for 9 hours

| Field | Value |
|---|---|
| Incident | INC-2026-0207 |
| Severity / impact | Sev-2; 14 joiners without access on their first morning |
| Facilitator | H. Ito (not on the responding team, by design) |
| Participants | J. Marek, A. Vogel, T. Blomqvist, platform on-call rotation |
| Date of review | 2026-12-05 |

## 1. Summary
A routine node pool upgrade drained the node holding the provisioning poller's
leader lease. No new leader was elected because the lease-renewal path had no
handover on graceful shutdown, and the service had no liveness signal of its
own. Monitoring did notice within ten minutes, but the alert was routed to a
Slack channel that had been deleted two weeks earlier, and there was no
fallback route. The failure was therefore invisible for nine hours until a
human noticed missing access.

## 2. Contributing factors
| Factor | Why it existed | Why it was reasonable at the time |
|---|---|---|
| Single-leader poller with no heartbeat | The design (TDD, section 3) chose persisted timers over in-process ones, correctly, but only alerted on the *symptom* (backlog) rather than on leader liveness | Backlog was thought to be a sufficient proxy; in normal operation it is |
| Alert routed to a deleted Slack channel | The channel was deleted during a workspace tidy-up on 2026-11-19; nothing linked channels to alert routes | Nobody deleting a channel had any way to know an alert depended on it |
| No fallback route in PagerDuty | The service was configured with one notification target | Consistent with every other service we own — this was a fleet-wide gap, not a local oversight |
| Node pool upgrades do not consider leases | Cluster upgrades are automated and treat all pods as stateless | True for every other workload we run |
| Overnight window | The failure began at 22:31; nobody was looking | Expected — the service has no overnight SLO |

Note that four of these five had to hold at once. Fixing any single one would
have reduced impact from nine hours to under one.

## 3. What went well
- Once detected, mitigation took 46 minutes, most of it diagnosis; the actual
  fix was one documented command from the runbook.
- The runbook's explicit "do not delete rows from due_action" warning stopped a
  responder from taking exactly the action that would have permanently dropped
  fourteen joiners' provisioning. This warning was added after a near miss in
  September and paid for itself here.
- The audit log was complete and made the impact assessment straightforward:
  we could state with confidence that no access was granted incorrectly.
- People Ops had a workable manual path and used it without waiting for us.

## 4. Detection analysis
Time to detect: 8h 31m (condition true 22:41, human report 07:12). Monitoring
evaluated correctly; delivery failed silently. PagerDuty does not alert on an
undeliverable notification target, and we had no test that alerts actually
arrive. A synthetic end-to-end check — provision a test joiner hourly and alert
on failure — would have detected this within an hour regardless of which
component broke, and independently of alert routing.

## 5. Response analysis
At 07:19 the responder's first hypothesis was a database problem, because the
backlog query was slow. Three minutes were spent there. The dashboard shows
backlog size but not leader identity, so leadership was not the obvious first
check. Adding leader identity and lease age to the top of the pipeline
dashboard would have made the cause visible immediately.

## 6. Where we got lucky
- No leaver event fell in the window. A delayed revocation would have made this
  a security incident with an audit obligation, not a productivity one.
- 2026-12-03 was a Wednesday. The same failure on a Friday night would have run
  until Monday: roughly 60 hours, spanning weekend leaver events.
- The 500-joiner graduate intake was three months earlier. The same failure
  during intake would have affected hundreds of people.

## 7. Actions
| # | Action | Type | Owner | Due | Tracker |
|---|---|---|---|---|---|
| 1 | Audit all alert routes for invalid targets; add a CI check that every route resolves | Detect | J. Marek | 2026-12-10 | OPS-881 |
| 2 | Poller emits a heartbeat; alert on its absence within 5 minutes | Detect | A. Vogel | 2026-12-19 | OPS-882 |
| 3 | Hourly synthetic joiner, alerting on failure | Detect | H. Ito | 2027-01-16 | OPS-885 |
| 4 | Graceful lease handover on SIGTERM; verify with a chaos test | Prevent | J. Marek | 2027-01-16 | OPS-884 |
| 5 | Leader identity and lease age on the pipeline dashboard | Mitigate | J. Marek | 2026-12-12 | OPS-886 |
| 6 | Share the alert-route audit pattern at the platform guild — likely fleet-wide | Prevent | H. Ito | 2026-12-19 | OPS-887 |

## 8. Actions we are deliberately not taking
- **Running the poller in multiple instances.** Two leaders double-apply
  entitlements, which is a security-relevant failure far worse than a delay.
  The single-leader design stays; we improve handover and detection instead.
- **Overnight on-call for this service.** The business impact of an overnight
  outage is low provided it is fixed before 08:00. Actions 2 and 3 give us that
  without a rotation change; we will revisit if the synthetic check shows more
  than two overnight failures in a quarter.
- **Blocking node pool upgrades.** They are a security control. Action 4 makes
  the service tolerate them instead.

## 9. Lessons for other teams
Alert routes are configuration that can rot silently, and nothing tells you.
Every team should verify that its alerts are deliverable, and should have at
least one synthetic end-to-end check that does not depend on the same alerting
path as everything else.
{{< /doctabs >}}

## Common mistakes

- **Hunting for "the root cause".** Real incidents need several conditions to hold at once. Naming one cause guarantees you fix the least important of them.
- **Blame disguised as analysis.** "The engineer failed to check X" ends the inquiry. "Nothing in the tooling made X visible" continues it, and produces a fix.
- **No detection analysis.** Time to detect is usually the largest and cheapest lever on impact.
- **Only prevention actions.** You cannot prevent every failure. Detection and mitigation actions are often more valuable per hour spent.
- **No "not doing" section.** Every postmortem generates proposals that would cost more than the incident. Recording the rejection stops them being re-raised, and shows the analysis was a decision rather than a wish list.
- **Actions untracked.** If they are not in the same backlog as feature work, they will lose to feature work.

## Related templates

- [Incident Report](/docs/operations-incident/incident-report/) — the factual record this analyses.
- [Operational Runbook](/docs/operations-incident/operational-runbook/) — where response improvements land.
- [RAID Log](/docs/project-management/raid-log/) — for risks the postmortem reveals but cannot fix now.
- [Risk Register](/docs/security-compliance/risk-register/) — when the finding is a standing organisational risk.
- [Operations & Incident](/docs/operations-incident/) — the other four operations and incident templates.
