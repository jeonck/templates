---
weight: 3010
title: "Solution Architecture Document"
description: "The structure of a system, the constraints that shaped it, and the trade-offs accepted."
icon: "schema"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

A solution architecture document (SAD) describes a system at the level where changing your mind is still cheap: components, boundaries, data flows, and the quality attributes that drove them. If it reads like a description of the code, it will be obsolete in a month and nobody will update it.

## When to use it

- New systems, or significant re-platforming of existing ones.
- When more than one team must build against the same structure.
- Before a procurement or security review that needs a system-level view.

## What it must answer

- What are the components, and what is each one responsible for?
- Where are the trust and ownership boundaries?
- How does data flow, and where does it rest?
- Which quality attributes drove the structure, and what did we trade away?

## Template

```markdown
# Solution Architecture: <System>

| Field | Value |
|---|---|
| Version / date | |
| Architect | |
| Status | Draft / Reviewed / Approved |
| Related | Charter, SRS, ADRs |

## 1. Context
Business purpose in five sentences. Who uses it, what it replaces.

## 2. Drivers and constraints
| # | Driver / constraint | Type | Source | Architectural consequence |
|---|---|---|---|---|

## 3. Quality attribute scenarios
| Attribute | Stimulus | Response | Measure |
|---|---|---|---|

## 4. Logical view
Components and responsibilities. One diagram plus a table — the table is what
people actually read.

| Component | Responsibility | Owner | Technology | Notes |
|---|---|---|---|---|

## 5. Data view
Entities, stores, classification, retention, residency.

## 6. Integration and interfaces
Inbound and outbound, protocols, contracts, failure behaviour.

## 7. Deployment view
Environments, regions, network zones, scaling model.

## 8. Cross-cutting concerns
Identity and access, secrets, observability, error handling, tenancy,
configuration.

## 9. Availability and recovery
SLO, failure modes, RPO/RTO, degraded operation.

## 10. Security
Trust boundaries, threat summary, controls, residual risk.

## 11. Alternatives considered
| Option | Why rejected |
|---|---|

## 12. Risks and open decisions
| # | Item | Owner | Needed by |
|---|---|---|---|
```

## Worked example

```markdown
# Solution Architecture: Access Provisioning Service (extract)

## 2. Drivers and constraints
| # | Driver / constraint | Type | Source | Consequence |
|---|---|---|---|---|
| D1 | Every entitlement change must be attributable for 7 years | Compliance | Audit finding 2025-11 | Append-only audit store, separate from the operational database, written before the grant is considered successful |
| D2 | HR system is read-only and cannot be replaced | Constraint | BRD §7 | Event-driven ingest with local projection; no writes back to HR |
| D3 | Two of eleven targets have no modern API | Constraint | Discovery | Adapter layer with a batch adapter for the legacy ERP; provisioning latency for those targets is inherently nightly |
| D4 | People Ops must change bundles without a release | Business | BR-04 | Bundle definitions are data, versioned in the database, not code |
| D5 | No new identity licences before FY2027 | Budget | BRD §7 | Reuse existing identity platform for SCIM; no third-party IGA product |

## 3. Quality attribute scenarios
| Attribute | Stimulus | Response | Measure |
|---|---|---|---|
| Latency | Joiner event arrives | Entitlements applied and audited | p95 <= 30 min, excluding batch targets |
| Availability | One target system unavailable | Other entitlements still applied; failed one queued and ticketed | No cascading failure; partial state visible |
| Auditability | Auditor asks who granted X to Y on date Z | Answer from the audit store | < 5 minutes, without engineer involvement |
| Elasticity | 500 joiners in one day (graduate intake) | Processed within the working day | No manual intervention |

## 4. Logical view
| Component | Responsibility | Owner | Technology | Notes |
|---|---|---|---|---|
| Ingest | Receive, deduplicate and validate HR events | Platform | Go service | Idempotent on HR event ID |
| Bundle resolver | Map job code to entitlement set | Platform | Go + Postgres | Bundles are versioned rows; resolution pins a bundle version onto the request |
| Approval | State machine for non-standard entitlements | Platform | Go | States: DRAFT, AWAITING_BUNDLE, AWAITING_APPROVAL, APPROVED, APPLYING, COMPLETE, PARTIAL, REJECTED |
| Adapters (11) | Talk to each target system | Platform | SCIM client; SFTP batch for ERP | One adapter per target, uniform interface, per-adapter retry policy |
| Audit sink | Append-only record of grants and revocations | Security | Object storage, daily signed export | Write precedes success; failure to write fails the grant |
| Admin UI | Bundle maintenance for People Ops | Platform | Server-rendered | Changes are reviewed by a second People Ops user before taking effect |

## 8. Cross-cutting concerns
- **Identity:** the service authenticates to targets with per-target service
  credentials from the secrets manager, rotated every 90 days. It never holds
  end-user credentials.
- **Observability:** correlation ID minted at ingest, propagated to every
  adapter call and written to the audit record. Golden signals per adapter.
- **Error handling:** adapters are the only place that retries; the core state
  machine treats every adapter outcome as final for that attempt.

## 9. Availability and recovery
SLO 99.5% monthly during business hours. Degraded mode: events queue for up to
4 hours without loss. RPO 15 min (Postgres PITR), RTO 4 hours. A queued event
is never dropped; the queue is the durability boundary.

## 11. Alternatives considered
| Option | Why rejected |
|---|---|
| Commercial IGA product | EUR 90k/yr recurring, exceeds FY2027 budget constraint D5; also requires works council review, adding ~6 weeks |
| Direct HR-to-target integrations, no service | No central audit point, which is the whole reason for the project (D1) |
| Synchronous provisioning at HR event time | Couples availability to eleven targets; one target's outage would fail the joiner entirely |

## 12. Risks and open decisions
| # | Item | Owner | Needed by |
|---|---|---|---|
| 1 | Legacy ERP revocation latency is 26h worst case, against a 1h requirement | A. Vogel | Before UAT — see RTM accepted gaps |
| 2 | Bundle version pinning: do in-flight requests follow bundle edits? Decided no — see ADR-0012 | A. Vogel | Closed |
```

## Common mistakes

- **Diagrams without a component table.** Boxes and arrows do not say who owns a component or what it is responsible for; the table does, and it survives being pasted into a review document.
- **No drivers section.** A structure with no stated drivers is indefensible and unmaintainable — the next person cannot tell which parts are load-bearing.
- **Missing alternatives.** "Why not the obvious cheaper thing?" will be asked in every review. Answer it once, in writing.
- **Cross-cutting concerns left implicit.** Identity, secrets, observability and error handling are where most production surprises come from.
- **Document versioned separately from the system.** Keep it in the repository so a change to structure and a change to the document arrive in the same pull request.

## Related templates

- [Architecture Decision Record](/docs/architecture-design/architecture-decision-record/) — one decision each, referenced from section 11.
- [Technical Design Document](/docs/architecture-design/technical-design-document/) — the level below this one.
- [Data Model Document](/docs/architecture-design/data-model-document/) — expands section 5.
- [API Specification](/docs/architecture-design/api-specification/) — expands section 6.
- [Software Requirements Specification](/docs/requirements/software-requirements-specification/) — the requirements this structure satisfies.
- [Architecture & Design](/docs/architecture-design/) — the other four architecture and design templates.
