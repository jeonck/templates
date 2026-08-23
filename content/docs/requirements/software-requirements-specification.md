---
weight: 2020
title: "Software Requirements Specification"
description: "System-level functional and non-functional requirements, each one testable."
icon: "description"
date: "2026-08-23"
draft: false
---

An SRS states what the system must do, precisely enough that two independent teams would build something equivalent and a tester could write cases without asking questions. It is the bridge between the business intent in a [BRD](/docs/requirements/business-requirements-document/) and the design in an architecture document.

## When to use it

- For systems built under contract, or where a formal acceptance gate exists.
- In regulated environments where evidence of specification is required.
- For anything with meaningful non-functional demands — throughput, latency, retention, availability.
- A backlog of [user stories](/docs/requirements/user-story/) can replace an SRS for product work with a stable team; it cannot replace one for a fixed-price contract.

## What it must answer

- What does the system do, for whom, under what conditions?
- What are the measurable quality attributes, with numbers and measurement points?
- What are the interfaces, and who owns each side of them?
- What is explicitly excluded?

## Template

{{< doctabs >}}
# Software Requirements Specification: <System>

| Field | Value |
|---|---|
| Version / date | |
| Author / owner | |
| Status | |
| Supersedes | |


## 1. Purpose and scope
## 2. Definitions and abbreviations
## 3. System context
Actors, external systems, trust boundaries. One diagram.

## 4. Functional requirements
| ID | Requirement | Priority | Source | Verification |
|---|---|---|---|---|


Write each as: "The system shall <observable behaviour> when <condition>."
Verification is one of: test, demonstration, inspection, analysis.

## 5. Non-functional requirements
| ID | Attribute | Requirement | Measured at | Verification |
|---|---|---|---|---|


Cover at least: performance, capacity, availability, recovery, security,
privacy/retention, accessibility, observability, portability.

## 6. External interfaces
| Interface | Direction | Protocol / format | Owner | Failure behaviour |
|---|---|---|---|---|


## 7. Data requirements
Entities, retention, residency, classification.

## 8. Constraints
## 9. Out of scope
## 10. Open issues
| # | Question | Owner | Needed by |
|---|---|---|---|
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Software Requirements Specification: Access Provisioning Service

| Field | Value |
|---|---|
| Version / date | 2.0 / 2026-06-30 |
| Owner | A. Vogel |
| Status | Approved for build |


## 1. Purpose and scope
Specifies the Access Provisioning Service, which grants and revokes employee
access to eleven internal systems in response to HR events. It covers the
joiner, mover and leaver flows for permanent and fixed-term employees.
Contractors are out of scope for this release (see section 9). This document
is the acceptance baseline for the build; it supersedes the requirements
section of BRD v1.2 where the two disagree.

## 2. Definitions and abbreviations
| Term | Meaning |
|---|---|
| Bundle | The set of entitlements a job code grants, versioned and immutable |
| Entitlement | One permission in one target system, e.g. `repo:payments:write` |
| Joiner / mover / leaver | HR events for starting, changing role, and leaving |
| Standard access | Entitlements resolved from the bundle, needing no approval |
| Target system | Any of the eleven systems this service provisions into |
| SCIM | System for Cross-domain Identity Management, RFC 7644 |


## 3. System context
Actors: HR system (source of record), line manager (approver), target systems
(11), service desk agent (exception handling), auditor (read-only). The service
is inside the corporate trust boundary; target system credentials live in the
existing secrets manager.

## 4. Functional requirements
| ID | Requirement | Priority | Source | Verification |
|---|---|---|---|---|
| FR-01 | The system shall create a provisioning request within 5 minutes of a new employee record appearing in the HR feed | Must | BR-01 | Test |
| FR-02 | The system shall resolve the employee's job code to an access bundle, and shall reject the request if no bundle matches | Must | BR-01 | Test |
| FR-03 | The system shall require line-manager approval for any entitlement not present in the resolved bundle | Must | BR-02 | Test |
| FR-04 | The system shall revoke all entitlements within 1 hour of the recorded leave date passing | Must | BR-03 | Test |
| FR-05 | The system shall record, for every grant and revocation, the actor, timestamp, entitlement and justification, in an append-only log | Must | BR-02, audit | Inspection |
| FR-06 | The system shall allow a People Ops administrator to modify bundle contents without a code deployment | Should | BR-04 | Demonstration |
| FR-07 | The system shall retry a failed target-system call 5 times with exponential backoff before raising a service desk ticket | Must | Ops | Test |


## 5. Non-functional requirements
| ID | Attribute | Requirement | Measured at | Verification |
|---|---|---|---|---|
| NFR-01 | Performance | 95th percentile end-to-end provisioning completes within 30 minutes of the HR event | Service metrics, weekly | Test |
| NFR-02 | Capacity | Sustains 40 joiner events per hour and a bulk load of 500 events (annual graduate intake) | Load test | Test |
| NFR-03 | Availability | 99.5% monthly, business hours; degraded mode may queue events for up to 4 hours | Synthetic probe | Analysis |
| NFR-04 | Recovery | RPO 15 minutes, RTO 4 hours | DR exercise | Demonstration |
| NFR-05 | Security | No entitlement change may be made by the service without a corresponding approved request; service credentials rotate every 90 days | Pen test, secrets audit | Test |
| NFR-06 | Privacy | Personal data limited to name, employee ID, job code, dates; audit log retained 7 years, operational logs 90 days | Data inventory | Inspection |
| NFR-07 | Observability | Every request exposes a correlation ID present in all downstream calls and in the audit log | Log sampling | Inspection |


## 6. External interfaces
| Interface | Direction | Protocol / format | Owner | Failure behaviour |
|---|---|---|---|---|
| HR feed | In | Webhook, JSON, at-least-once | HR platform team | Deduplicate on event ID; alert if no event in 24h |
| Target systems (9) | Out | SCIM 2.0 | Identity platform | Retry per FR-07, then ticket |
| Legacy ERP | Out | SFTP batch, fixed-width, nightly | ERP team | File rejected -> ticket + no partial apply |
| Audit export | Out | Signed NDJSON to object storage, daily | Internal Audit | Missing file alerts within 2h |


## 7. Data requirements
| Entity | Purpose | Retention | Classification | Residency |
|---|---|---|---|---|
| Employee projection | Fields needed to resolve a bundle and route approval | 90 days after leave date | Personal | EEA only |
| Bundle version | Immutable rule a grant is attributed to | 7 years | Internal | EEA only |
| Request | One provisioning workflow instance | 7 years | Personal | EEA only |
| Entitlement grant | One entitlement applied to one person | 7 years | Personal | EEA only |
| Audit record | Append-only fact about a grant, revocation or approval | 7 years | Personal | EEA only |


The HR system remains the system of record; the projection is read-only and is
never edited in this service. Corrections flow from HR. The full model is in
the data model document.

## 8. Constraints
- The HR system cannot be modified and exposes a read-only feed; no write-back.
- Two of the eleven targets have no modern API. The legacy ERP accepts one
  SFTP batch per night, which bounds FR-04 for that target.
- No budget for additional identity licences before FY2027, so the existing
  identity platform must carry the nine SCIM targets.
- Works council agreement limits use of the last-authentication timestamp to
  dormant-account detection; it must not be exposed to line managers.
- Bundle definitions must be editable by People Operations without a release.


## 9. Out of scope
Contractor identities, badge provisioning, payroll enrolment, mobile device
enrolment.

## 10. Open issues
| # | Question | Owner | Needed by |
|---|---|---|---|
| 1 | Does the legacy ERP support same-day revocation, or only nightly? | ERP team | 2026-07-15 — affects FR-04 |
{{< /doctabs >}}

## Common mistakes

- **Unverifiable requirements.** "The system shall be user-friendly" cannot be tested, so it will not be. If you cannot name a verification method, it is not a requirement.
- **Non-functional requirements without a measurement point.** "99.9% available" measured where — the load balancer, or the user's browser? The difference is often an order of magnitude of work.
- **Mixing design into the specification.** "The system shall store requests in PostgreSQL" belongs in the [Technical Design Document](/docs/architecture-design/technical-design-document/) unless the database is genuinely a contractual constraint.
- **No source column.** Without traceability back to a business requirement, nobody can tell which requirements can be cut.
- **Open issues hidden in prose.** An explicit open-issues table with dates is what keeps a specification honest during review.

## Related templates

- [Business Requirements Document](/docs/requirements/business-requirements-document/) — the source of the requirements here.
- [Requirements Traceability Matrix](/docs/requirements/requirements-traceability-matrix/) — links each FR/NFR to a test.
- [API Specification](/docs/architecture-design/api-specification/) — expands section 6.
- [Test Plan](/docs/testing-qa/test-plan/) — consumes the verification column.
- [Requirements & Analysis](/docs/requirements/) — the other four requirements templates.
