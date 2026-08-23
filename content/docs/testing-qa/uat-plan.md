---
weight: 5040
title: "UAT Plan"
description: "How business users will decide whether to accept the system — and what happens when they do not."
icon: "how_to_reg"
date: "2026-08-23"
draft: false
---

User acceptance testing answers a different question from system testing: not "does it meet the specification" but "can these people do their job with it". That means real users, real tasks and real data shapes, and an acceptance decision that is defined before testing starts.

## When to use it

- Before go-live for anything with a business user population.
- Before accepting a supplier's delivery under contract.
- When a process, not just a system, is changing — UAT is where process gaps surface.

## What it must answer

- Who accepts, on what basis, and what does "accepted with conditions" mean?
- Which real business scenarios must be completable, by whom?
- What environment and data do participants get?
- How do participants raise problems, and how fast do they get answers?

## Template

{{< doctabs >}}
# UAT Plan: <System>

| Field | Value |
|---|---|
| Business owner (accepts) | |
| UAT coordinator | |
| Window | |
| Environment | |
| Related | Test Plan v_, BRD v_ |


## 1. Objectives
What acceptance will and will not prove.

## 2. Participants
| Name | Role | Scenarios | Time committed |
|---|---|---|---|


## 3. Scenarios
| # | Business scenario | Participant | Data needed | Acceptance condition |
|---|---|---|---|---|


## 4. Environment and data
## 5. Entry criteria
## 6. Acceptance criteria
Including what "accept with conditions" requires.

## 7. Defect handling during UAT
Severity, response times, who decides.

## 8. Schedule
| Day | Activity | Who |
|---|---|---|


## 9. Sign-off
| Name | Role | Decision | Date | Conditions |
|---|---|---|---|---|
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# UAT Plan: Access Provisioning Service

| Field | Value |
|---|---|
| Business owner (accepts) | K. Ferreira, Head of People Operations |
| UAT coordinator | H. Ito |
| Window | 2026-11-17 to 2026-11-28 |
| Environment | uat, refreshed 2026-11-14 with anonymised production data |


## 1. Objectives
Prove that People Ops can run joiner, mover and leaver events without IT
involvement, that line managers can approve from a phone, and that Internal
Audit can answer an access question from the audit export unaided. It does not
prove performance or resilience — those are covered by the system test plan.

## 2. Participants
| Name | Role | Scenarios | Time committed |
|---|---|---|---|
| K. Ferreira | Head of People Ops | 1, 2, 6 | 4h |
| T. Blomqvist | People Ops administrator | 1–5 | 12h |
| Three line managers (rotating) | Approvers | 3 | 30 min each |
| L. Haddad | Internal Audit | 7 | 3h |
| D. Achebe | Service desk lead | 5, 8 | 4h |


## 3. Scenarios
| # | Business scenario | Participant | Data needed | Acceptance condition |
|---|---|---|---|---|
| 1 | Standard engineering joiner, start date in 10 days | T. Blomqvist | Anonymised joiner record | Access complete one working day before the start date, with no ticket raised |
| 2 | Joiner with an unmapped job code | T. Blomqvist | Job code with no bundle | Lands in the People Ops queue; administrator assigns a bundle and completes it without IT |
| 3 | Joiner needing extra access | Line manager | As scenario 1 plus an additional entitlement | Manager receives the request on a phone and approves it in under 3 minutes |
| 4 | Internal move between departments | T. Blomqvist | Mover record | Old entitlements removed, new applied, no manual cleanup |
| 5 | Leaver with immediate effect | D. Achebe | Leaver record dated today | All non-batch entitlements revoked within 1 hour; the ERP exception appears on the daily report |
| 6 | Bundle change | K. Ferreira | — | A bundle edit takes effect for new requests without an IT release, and does not alter pending requests |
| 7 | Audit question: who granted X to Y on date Z, and under which rule? | L. Haddad | Historical export | Answered from the export in under 5 minutes, without engineering help |
| 8 | Something goes wrong: a target system is down | D. Achebe | Simulated adapter outage | A ticket is raised with the correlation ID, and other entitlements still apply |


## 5. Entry criteria
System test exit criteria met; zero open Sev-1; uat refreshed within 7 days;
participants trained (one 90-minute session on 2026-11-14).

## 6. Acceptance criteria
- All eight scenarios completed with their acceptance condition met.
- No Sev-1 or Sev-2 defect open at the end of the window.
- Participants complete scenarios without IT intervention, except where the
  scenario explicitly involves the service desk.

**Accept with conditions** is permitted only where the condition is written
down with an owner and a date. "Accept with conditions" without a dated
remediation is a rejection.

## 7. Defect handling during UAT
Raised in the tracker with the UAT label; triaged twice daily at 10:00 and
15:00. Sev-1 gets a fix or a workaround within one working day, Sev-2 within
three. The business owner decides severity disputes, not engineering.

## 9. Sign-off
| Name | Role | Decision | Date | Conditions |
|---|---|---|---|---|
| K. Ferreira | Business owner | Accepted with conditions | 2026-11-28 | ERP revocation latency: daily exception report to run from go-live, reviewed by People Ops; ERP fix tracked on the FY2027 roadmap. Owner: K. Ferreira, review 2027-03-31 |
| L. Haddad | Internal Audit | Accepted | 2026-11-27 | — |
{{< /doctabs >}}

## Common mistakes

- **UAT run by the project team.** If a tester is the person who built or specified it, they will not find the process gaps — they will unconsciously avoid them.
- **Scripted click-through instead of business scenarios.** "Click new, enter name, click save" tests the software. "Onboard this engineer starting in ten days" tests the process.
- **Acceptance defined after testing.** The criteria must exist before, or the decision becomes a negotiation about how tired everyone is.
- **"Accepted with conditions" as a rubber stamp.** Every condition needs an owner and a date, otherwise it is an unrecorded defect.
- **Synthetic data only.** Real data shapes — long names, missing managers, historical anomalies — are exactly where UAT earns its cost.

## Related templates

- [Test Plan](/docs/testing-qa/test-plan/) — the system testing that must finish first.
- [Test Summary Report](/docs/testing-qa/test-summary-report/) — evidence supporting the acceptance decision.
- [Business Requirements Document](/docs/requirements/business-requirements-document/) — the scenarios trace back to these requirements.
- [Testing & QA](/docs/testing-qa/) — the other four testing and QA templates.
