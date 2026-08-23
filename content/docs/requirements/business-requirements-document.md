---
weight: 2010
title: "Business Requirements Document"
description: "What the business needs and why, stated without prescribing a solution."
icon: "business_center"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

A BRD describes the problem in business terms. Its discipline is negative: it must not contain a solution. The moment it names a technology, the option space closes before anyone has costed the alternatives.

## When to use it

- Before a build-or-buy decision, or before an RFP goes out.
- When several departments have overlapping demands and someone must reconcile them.
- Not for small changes inside an existing product — a [User Story](/docs/requirements/user-story/) is enough.

## What it must answer

- What is happening today that costs money, time or risk, and how much?
- What must be true after the change for the sponsor to consider it worthwhile?
- Which constraints are real (regulation, contract, deadline) and which are preferences?
- Who is affected, including the people who will lose something?

## Template

{{< doctabs >}}
# Business Requirements Document: <Initiative>

| Field | Value |
|---|---|
| Version / date | |
| Author | |
| Business owner | |
| Status | Draft / In review / Approved |

## 1. Background and problem statement
What is happening now. Quantify it.

## 2. Objectives
| # | Objective | Measure | Baseline | Target |
|---|---|---|---|---|

## 3. Scope
In scope / out of scope / future phases.

## 4. Stakeholders
| Group | Interest | Impact of change | Who speaks for them |
|---|---|---|---|

## 5. Current state
Process, systems, volumes, pain points. A diagram beats a paragraph.

## 6. Business requirements
| ID | Requirement | Priority (MoSCoW) | Rationale | Acceptance |
|---|---|---|---|---|

## 7. Constraints
Regulatory, contractual, budgetary, timing.

## 8. Assumptions and dependencies

## 9. Options considered
| Option | Description | Cost | Benefit | Risk |
|---|---|---|---|---|

## 10. Approval
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Business Requirements Document: Employee Onboarding Automation

| Field | Value |
|---|---|
| Version / date | 1.2 / 2026-04-18 |
| Business owner | K. Ferreira, Head of People Operations |
| Status | Approved |

## 1. Background and problem statement
New joiners currently take an average of 4.6 working days to receive all
system access. HR raises 11 separate tickets per joiner, manually, from a
spreadsheet. At 380 hires per year this consumes roughly 1,900 hours of HR and
IT effort. In the last audit, 14 of 60 sampled leavers still held active
accounts more than 30 days after their end date.

## 2. Objectives
| # | Objective | Measure | Baseline | Target |
|---|---|---|---|---|
| 1 | Faster access provisioning | Working days from contract signed to full access | 4.6 | <= 1.0 |
| 2 | Reduce manual effort | HR+IT hours per joiner | 5.0 | <= 1.0 |
| 3 | Close the leaver gap | Accounts active >7 days after end date | 23% | 0% |

## 3. Scope
**In scope:** permanent and fixed-term employees; the 11 systems currently
provisioned by ticket; joiner, mover and leaver events.
**Out of scope:** contractors (different contractual identity), physical badge
issuance, payroll enrolment.
**Future phase:** contractor onboarding once the vendor identity model is agreed.

## 4. Stakeholders
| Group | Interest | Impact of change | Who speaks for them |
|---|---|---|---|
| People Ops | Fewer tickets, faster starts | Loses manual control over exceptions | K. Ferreira |
| IT Service Desk | Ticket volume drops ~4,200/yr | Two roles change substantially | D. Achebe |
| Line managers | Joiners productive on day one | Must approve access requests within 24h | Managers' forum |
| Internal Audit | Leaver revocation evidence | Gains an automated evidence trail | L. Haddad |

## 5. Current state
HR spreadsheet -> 11 manual tickets -> per-system admin action -> email to
manager. No single record of who approved what. Leaver process depends on HR
remembering to raise a closure ticket.

## 6. Business requirements
| ID | Requirement | Priority | Rationale | Acceptance |
|---|---|---|---|---|
| BR-01 | Access requests must be generated automatically from an authoritative HR record | Must | Removes the spreadsheet as the source of truth | No manual ticket is required for a standard joiner |
| BR-02 | A line manager must approve non-standard access before it is granted | Must | Audit finding 2025-11 | Every non-standard grant has a recorded approver and timestamp |
| BR-03 | Access must be revoked automatically on the recorded leave date | Must | Objective 3 | Sampling shows 0 active accounts >24h after end date |
| BR-04 | Role-based access bundles must be maintainable by People Ops without IT | Should | Bundles change monthly | A bundle change reaches production without a code release |
| BR-05 | Joiners should receive a status page showing provisioning progress | Could | Reduces "where is my laptop" tickets | — |

## 7. Constraints
- The HR system of record cannot be replaced; it exposes a read-only API.
- Works council consultation is required before any change to leaver monitoring;
  allow 6 weeks.
- No budget for additional identity licences before FY2027.

## 8. Assumptions and dependencies
- HR data quality is sufficient: start dates are correct in >95% of records.
  (To be validated by sampling before design — see [RAID Log](/docs/project-management/raid-log/).)
- The existing identity platform supports SCIM for 9 of the 11 systems.

## 9. Options considered
| Option | Description | Cost | Benefit | Risk |
|---|---|---|---|---|
| A | Extend existing identity platform | EUR 210k | Reuses licences and skills | Two systems still need custom connectors |
| B | Buy a dedicated onboarding SaaS | EUR 340k + 90k/yr | Fastest to first value | New vendor, new data processing agreement, works council review |
| C | Do nothing, add HR headcount | EUR 120k/yr | No project risk | Audit finding remains open |

Recommendation: Option A.

## 10. Approval
K. Ferreira (business owner) 2026-04-18; D. Achebe (IT) 2026-04-22.
{{< /doctabs >}}

## Common mistakes

- **Solutions disguised as requirements.** "The system shall use SAML" is a design decision. The requirement is "employees must not maintain a separate password for this system".
- **Unquantified problems.** "Onboarding is slow" cannot be closed. "4.6 days, target 1.0" can.
- **Every requirement is a Must.** If nothing can be dropped, the first budget cut will be made by someone who has not read the document.
- **Stakeholders listed without their losses.** The group that loses discretion is the group that will resist; naming it early is cheaper than discovering it at UAT.
- **No options section.** Approving a BRD with one option is approving a decision already made elsewhere.

## Related templates

- [Software Requirements Specification](/docs/requirements/software-requirements-specification/) — the systems-level successor to this document.
- [Requirements Traceability Matrix](/docs/requirements/requirements-traceability-matrix/) — proves each BR survives into design and test.
- [Project Charter](/docs/project-management/project-charter/) — the funding decision this feeds.
- [Vendor Security Assessment](/docs/security-compliance/vendor-security-assessment/) — if option B wins, vendor due diligence starts here.
- [Requirements & Analysis](/docs/requirements/) — the other four requirements templates.
