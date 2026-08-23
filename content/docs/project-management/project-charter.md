---
weight: 1010
title: "Project Charter"
description: "The one-page authorisation that says a project exists, who runs it, and what 'done' means."
icon: "flag"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

A charter is the document that turns an idea into a funded project. Its real job is not description — it is authorisation and boundary setting. It names the sponsor who can say yes, the manager who can spend, and the things this project is explicitly *not* going to do.

## When to use it

- At project initiation, before any team member is assigned.
- When a piece of work that started informally has grown enough that people are arguing about its scope.
- When the sponsor changes and the mandate needs re-confirming.

## What it must answer

| Question | Why it belongs in the charter |
|---|---|
| Why now? | Separates a real trigger (contract expiry, audit finding, capacity ceiling) from a preference. |
| Who is accountable? | One sponsor, one manager. Two of either means neither. |
| What is out of scope? | The only section that reliably prevents a fight in month four. |
| What does success look like? | Measurable, with a baseline. "Improve performance" is not a success criterion. |
| What is the budget and deadline? | An order of magnitude is fine; a blank is not. |

## Template

```markdown
# Project Charter: <Project Name>

| Field | Value |
|---|---|
| Charter version | 1.0 |
| Date | YYYY-MM-DD |
| Sponsor | Name, role |
| Project manager | Name, role |
| Status | Draft / Approved |

## 1. Business case
Two or three sentences. What changes in the business if this succeeds, and what
happens if we do nothing.

## 2. Objectives and success criteria
| # | Objective | Measure | Baseline | Target | Measured by |
|---|---|---|---|---|---|
| 1 | | | | | |

## 3. Scope
**In scope**
- ...

**Out of scope**
- ...

**Assumptions**
- ...

## 4. Deliverables and milestones
| Milestone | Deliverable | Target date |
|---|---|---|

## 5. Budget
| Category | Amount | Notes |
|---|---|---|
| People | | |
| Licences / cloud | | |
| Contingency | | |

## 6. Key risks
Top three only; the full list lives in the RAID log.

## 7. Stakeholders and governance
| Name | Role | Decision rights | Cadence |
|---|---|---|---|

## 8. Approval
| Name | Role | Date | Signature |
|---|---|---|---|
```

## Worked example

```markdown
# Project Charter: Payment Gateway Migration

| Field | Value |
|---|---|
| Charter version | 1.0 |
| Date | 2026-03-02 |
| Sponsor | R. Okafor, VP Engineering |
| Project manager | S. Lindqvist |
| Status | Approved |

## 1. Business case
Our contract with the incumbent payment provider ends 2027-01-31 and renewal
pricing is 40% higher. Migrating to the new provider saves roughly EUR 380k
per year and removes the single-region dependency that caused the outage in
January. Doing nothing means auto-renewal at the higher rate.

## 2. Objectives and success criteria
| # | Objective | Measure | Baseline | Target | Measured by |
|---|---|---|---|---|---|
| 1 | Migrate all card traffic | % of volume on new provider | 0% | 100% | 2026-12-15 |
| 2 | Hold authorisation rate | Weekly auth success rate | 96.4% | >= 96.4% | 2027-01-15 |
| 3 | Reduce annual cost | Provider fees per year | EUR 950k | <= EUR 570k | FY2027 close |

## 3. Scope
**In scope**
- Card payments (credit, debit) on web and mobile.
- Refunds, chargeback handling, reconciliation feeds to Finance.
- Dual-running both providers during cutover.

**Out of scope**
- Bank transfers and direct debit — remain with the incumbent until 2028.
- Repricing of merchant fees to customers.
- Replacing the internal ledger service.

**Assumptions**
- The new provider's sandbox is available from 2026-04-01.
- Finance can accept two reconciliation feeds during dual-running.

## 4. Deliverables and milestones
| Milestone | Deliverable | Target date |
|---|---|---|
| M1 | Integration spec signed off | 2026-05-15 |
| M2 | Sandbox integration passing test suite | 2026-07-31 |
| M3 | 5% live traffic on new provider | 2026-09-30 |
| M4 | 100% traffic migrated | 2026-12-15 |
| M5 | Incumbent card contract terminated | 2027-01-31 |

## 5. Budget
| Category | Amount | Notes |
|---|---|---|
| People | EUR 640k | 4 engineers, 1 QA, 0.5 PM for 9 months |
| Licences / cloud | EUR 45k | Sandbox, additional egress during dual-run |
| Contingency | EUR 100k | 15% |

## 6. Key risks
1. Authorisation rate drops after cutover and revenue falls before we can react.
2. The provider's PSD2 flow differs enough to require checkout redesign.
3. Finance reconciliation cannot handle dual feeds, delaying month-end close.

## 7. Stakeholders and governance
| Name | Role | Decision rights | Cadence |
|---|---|---|---|
| R. Okafor | Sponsor | Budget, go/no-go on cutover | Monthly steering |
| M. Duarte | Head of Finance | Accepts reconciliation design | Monthly steering |
| S. Lindqvist | PM | Day-to-day scope within charter | Weekly |
| A. Berg | Security lead | Accepts PCI scope changes | Gate reviews |

## 8. Approval
| Name | Role | Date | Signature |
|---|---|---|---|
| R. Okafor | Sponsor | 2026-03-02 | signed |
| M. Duarte | Head of Finance | 2026-03-04 | signed |
```

## Common mistakes

- **No out-of-scope section.** This is the single most common defect. Without it, every adjacent idea is arguably in scope.
- **Objectives without a baseline.** "Reduce latency by 30%" is meaningless if nobody wrote down today's number before the work started.
- **Two sponsors.** Shared accountability produces deadlock at exactly the moment a decision is needed.
- **Charter as a design document.** Architecture belongs in the [Solution Architecture Document](/docs/architecture-design/solution-architecture-document/), not here. A charter that specifies technology has already made decisions the team has not yet earned.
- **Never revisited.** If scope formally changes, reissue the charter at version 1.1 rather than burying the change in a status report.

## Related templates

- [Project Plan](/docs/project-management/project-plan/) — turns the milestones above into a schedule.
- [RAID Log](/docs/project-management/raid-log/) — where the full risk list lives.
- [Business Requirements Document](/docs/requirements/business-requirements-document/) — expands the business case into requirements.
- [Status Report](/docs/project-management/status-report/) — reports progress against the charter's milestones.
