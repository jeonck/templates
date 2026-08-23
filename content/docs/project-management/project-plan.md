---
weight: 1020
title: "Project Plan"
description: "Schedule, dependencies, resourcing and the critical path, in a form a delivery team will actually maintain."
icon: "calendar_month"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

The project plan converts the charter's milestones into dated, owned, sequenced work. The mistake is treating it as a Gantt chart to be admired; the useful version is a small table plus an explicit statement of what is on the critical path and what the plan assumes.

## When to use it

- Immediately after the [Project Charter](/docs/project-management/project-charter/) is approved.
- Before committing to an external date (a contract, a regulatory deadline, a marketing launch).
- Whenever a dependency changes enough that the finish date moves.

## What it must answer

- What are the work packages, and who owns each one?
- What must finish before what — and which of those chains determines the end date?
- Where does the plan depend on people or systems outside the team's control?
- How much buffer exists, and where is it held?

## Template

```markdown
# Project Plan: <Project Name>

| Field | Value |
|---|---|
| Plan version | |
| Baseline date | |
| Owner | |
| Related charter | link |

## 1. Approach
One paragraph: delivery method (iterative / phased), why it suits this work,
and how progress will be measured.

## 2. Work breakdown
| ID | Work package | Owner | Effort (days) | Depends on | Start | Finish |
|---|---|---|---|---|---|---|
| 1.1 | | | | — | | |

## 3. Milestones
| Milestone | Definition of done | Date | Owner |
|---|---|---|---|

## 4. Critical path
List the chain of work packages that determines the end date, and the total
float on the next-nearest chain.

## 5. Resourcing
| Role | Person | Allocation | Period | Confirmed? |
|---|---|---|---|---|

## 6. External dependencies
| Dependency | Provider | Needed by | Status | Escalation route |
|---|---|---|---|---|

## 7. Assumptions and buffer
- Assumptions this plan rests on.
- Where contingency is held and who may release it.

## 8. Change control
How a date change gets approved, and by whom.
```

## Worked example

```markdown
# Project Plan: Payment Gateway Migration

| Field | Value |
|---|---|
| Plan version | 2.1 (rebaselined after M2 slip) |
| Baseline date | 2026-08-04 |
| Owner | S. Lindqvist |

## 1. Approach
Incremental migration behind a routing flag, with traffic moved in steps
(5% / 25% / 100%). Progress is measured by percentage of live card volume on
the new provider, not by code completeness, because the integration is only
proven under real traffic.

## 2. Work breakdown
| ID | Work package | Owner | Effort (days) | Depends on | Start | Finish |
|---|---|---|---|---|---|---|
| 1.1 | Integration spec | A. Vogel | 15 | — | 2026-04-06 | 2026-05-15 |
| 1.2 | Sandbox client library | J. Marek | 25 | 1.1 | 2026-05-18 | 2026-06-26 |
| 1.3 | Routing flag service | J. Marek | 10 | — | 2026-05-18 | 2026-06-01 |
| 1.4 | Reconciliation feed | P. Nowak | 20 | 1.1 | 2026-06-01 | 2026-07-10 |
| 1.5 | Test suite against sandbox | H. Ito | 20 | 1.2 | 2026-06-29 | 2026-07-31 |
| 1.6 | 5% traffic ramp | J. Marek | 10 | 1.3, 1.5 | 2026-09-01 | 2026-09-30 |
| 1.7 | Full ramp | J. Marek | 30 | 1.6 | 2026-10-05 | 2026-12-15 |

## 3. Milestones
| Milestone | Definition of done | Date | Owner |
|---|---|---|---|
| M2 | Full sandbox suite green for 5 consecutive nightly runs | 2026-07-31 | H. Ito |
| M3 | 5% of card volume settled and reconciled through new provider | 2026-09-30 | S. Lindqvist |
| M4 | 100% volume, incumbent in standby only | 2026-12-15 | S. Lindqvist |

## 4. Critical path
1.1 -> 1.2 -> 1.5 -> 1.6 -> 1.7. Total float on the reconciliation chain
(1.1 -> 1.4) is 15 working days, so a two-week slip there does not move M4;
a two-week slip in 1.5 does.

## 5. Resourcing
| Role | Person | Allocation | Period | Confirmed? |
|---|---|---|---|---|
| Backend | J. Marek | 100% | Apr–Dec | Yes |
| Backend | A. Vogel | 50% | Apr–Jul | Yes |
| Data | P. Nowak | 50% | Jun–Jul | No — shared with Reporting |
| QA | H. Ito | 100% | Jun–Dec | Yes |

## 6. External dependencies
| Dependency | Provider | Needed by | Status | Escalation route |
|---|---|---|---|---|
| Sandbox credentials | Payment provider | 2026-04-01 | Received 2026-04-03 | Account manager |
| PCI scope sign-off | Internal security | 2026-08-15 | In review | A. Berg -> CISO |
| Finance dual-feed capacity | Finance systems | 2026-08-31 | Not started | M. Duarte |

## 7. Assumptions and buffer
- P. Nowak's 50% allocation holds; if Reporting reclaims it, 1.4 slips 3 weeks
  and consumes all its float.
- 15 working days of contingency sit before M4, released only by the sponsor.

## 8. Change control
Any change to M4 requires sponsor approval at monthly steering. Changes inside
the plan that do not move a milestone are the PM's to make.
```

## Common mistakes

- **A schedule with no critical path.** If everything looks equally urgent, the team optimises the wrong task.
- **Unconfirmed resources shown as confirmed.** Mark them honestly; an unconfirmed 50% allocation is a risk, and belongs in the [RAID Log](/docs/project-management/raid-log/) too.
- **Buffer spread thinly across every task.** Padding each estimate hides the buffer and guarantees it gets consumed. Hold it in one visible block.
- **Task-level detail beyond two weeks out.** Plan the near term in days and the far term in milestones; anything else is fiction that must be maintained.
- **No definition of done per milestone.** "Integration complete" gets declared complete under pressure. "Suite green five nights running" does not.

## Related templates

- [Project Charter](/docs/project-management/project-charter/) — the authority this plan executes.
- [Status Report](/docs/project-management/status-report/) — the weekly delta against this plan.
- [RAID Log](/docs/project-management/raid-log/) — dependencies and risks from sections 6 and 7.
- [Deployment Runbook](/docs/development-release/deployment-runbook/) — the detail behind the ramp work packages.
- [Project Management](/docs/project-management/) — the other four project-management templates.
