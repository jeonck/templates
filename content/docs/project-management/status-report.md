---
weight: 1030
title: "Status Report"
description: "A weekly one-pager that reports the delta, the decisions needed, and the truth about the date."
icon: "summarize"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

Most status reports are written to reassure. A useful one is written to surface the two or three things a reader can act on, and to report schedule confidence honestly enough that bad news arrives early rather than at the deadline.

## When to use it

- On a fixed weekly or fortnightly cadence for any project with a sponsor.
- Ad hoc when a milestone date changes — do not wait for the next scheduled report.

## What it must answer

- Is the end date still credible, and has that answer changed since last time?
- What did we finish, and what did we say we would finish and did not?
- What decision or unblocking do I need from the reader, by when?

## Template

{{< doctabs >}}
# Status Report: <Project> — week ending YYYY-MM-DD

**Overall:** Green / Amber / Red (last period: X)
**Next milestone:** <name>, due YYYY-MM-DD, confidence High / Medium / Low

## Decisions needed
| # | Decision | Owner | Needed by | Impact if late |
|---|---|---|---|---|

## Progress this period
- Completed: ...
- Slipped: ... (planned <date>, now <date>, cause)

## Plan for next period
- ...

## Risks and issues (changes only)
| ID | Item | Change since last report |
|---|---|---|

## Metrics
| Metric | Last | Now | Target |
|---|---|---|---|

## Budget
Spent to date / forecast at completion / approved.
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Status Report: Payment Gateway Migration — week ending 2026-08-21

**Overall:** Amber (last period: Green)
**Next milestone:** M3 — 5% live traffic, due 2026-09-30, confidence Medium

## Decisions needed
| # | Decision | Owner | Needed by | Impact if late |
|---|---|---|---|---|
| 1 | Confirm P. Nowak stays at 50% through September | M. Duarte | 2026-08-28 | Reconciliation feed slips 3 weeks and consumes all float |
| 2 | Accept 3DS challenge rate rising to 8% during ramp | R. Okafor | 2026-09-04 | Ramp cannot start; M3 slips |

## Progress this period
- Completed: sandbox test suite green on 5 consecutive nightly runs — M2 met,
  one week late.
- Completed: routing flag service deployed to production, disabled.
- Slipped: reconciliation feed UAT (planned 2026-08-19, now 2026-09-02).
  Cause: Finance systems team unavailable during month-end close. Known
  dependency, not a new one.

## Plan for next period
- Dry-run the ramp procedure against 0% traffic in production.
- Reconciliation feed UAT with Finance, 2026-09-01.
- Close out the PCI scope review with Security.

## Risks and issues (changes only)
| ID | Item | Change since last report |
|---|---|---|
| R-04 | Auth rate drop after cutover | Unchanged. Mitigation (automatic rollback below 95.5%) implemented this week. |
| R-07 | Shared data engineer | Escalated to Amber — this is decision 1 above. |
| I-02 | Sandbox rate limits | Closed. Provider raised the limit on 2026-08-18. |

## Metrics
| Metric | Last | Now | Target |
|---|---|---|---|
| Sandbox suite pass rate | 92% | 100% | 100% |
| Live volume on new provider | 0% | 0% | 5% by 2026-09-30 |
| Open defects (sev 1–2) | 3 | 1 | 0 before ramp |

## Budget
Spent EUR 402k of EUR 785k approved. Forecast at completion EUR 760k,
including EUR 45k of the EUR 100k contingency. No new budget request.
{{< /doctabs >}}

## Common mistakes

- **Green until the week it is Red.** A status that never goes Amber is not being measured; it is being performed. State milestone confidence separately from overall status so the trend is visible.
- **A list of activity instead of outcomes.** "Held three workshops" is not progress. "Integration spec signed by Finance" is.
- **Decisions buried in prose.** Put them in a table at the top with a date. A decision needed "soon" will not be made.
- **Restating the whole risk register every week.** Report the *changes*; the full list lives in the [RAID Log](/docs/project-management/raid-log/).
- **Silent re-baselining.** If the milestone date moved, say the old date, the new date, and the cause in the same line.

## Related templates

- [Project Plan](/docs/project-management/project-plan/) — the baseline this reports against.
- [RAID Log](/docs/project-management/raid-log/) — the source of the risks and issues section.
- [Meeting Minutes](/docs/project-management/meeting-minutes/) — where decisions get recorded once made.
- [Project Management](/docs/project-management/) — the other four project-management templates.
