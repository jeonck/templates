---
weight: 3050
title: "Technical Design Document"
description: "How one component will actually be built — enough detail to review the idea before the code exists."
icon: "draft"
date: "2026-08-23"
draft: false
---

A TDD (design document, not the testing acronym) sits below architecture and above code. It exists so that a reviewer can find the flaw in an approach in an hour of reading rather than a week of reviewing pull requests.

## When to use it

- Work larger than roughly two weeks, or touching a boundary other teams depend on.
- Anything with tricky state, concurrency, migration or failure semantics.
- Not for routine feature work whose shape is obvious from the [user story](/docs/requirements/user-story/).

## What it must answer

- What problem is being solved, and what is explicitly not being solved?
- What is the proposed approach, in enough detail to disagree with?
- What are the failure modes, and what happens in each?
- How does this get rolled out and rolled back?

## Template

{{< doctabs >}}
# Technical Design: <Feature or component>

| Field | Value |
|---|---|
| Author | |
| Reviewers | |
| Status | Draft / In review / Approved / Implemented |
| Related | Story / SRS / ADRs |


## 1. Problem
## 2. Goals and non-goals
## 3. Proposed design
Data structures, state transitions, algorithms, interfaces. Diagrams where
they earn their space.

## 4. Alternatives considered
## 5. Data changes
Schema changes, migration and backfill plan, reversibility.

## 6. Failure modes
| Failure | Detection | Behaviour | Blast radius |
|---|---|---|---|


## 7. Performance and capacity
Expected load, hot paths, and the number that would make this design wrong.

## 8. Security and privacy
New data, new trust boundaries, new secrets, authorisation changes.

## 9. Observability
Metrics, logs, traces, alerts, and the dashboard someone opens at 3am.

## 10. Testing strategy
What is proven by unit, integration, contract and load tests respectively.

## 11. Rollout and rollback
Flags, migration order, backwards compatibility window, kill switch.

## 12. Open questions
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Technical Design: Approval state machine

| Field | Value |
|---|---|
| Author | J. Marek |
| Reviewers | A. Vogel, H. Ito |
| Status | Approved 2026-07-02 |
| Related | FR-03, UC-07 ext. 4a, ADR-0012 |


## 1. Problem
Provisioning requests are created when an HR joiner event arrives, but
entitlements are applied one working day before the start date — often weeks
later. Some entitlements need a line manager's approval first, and nothing in
the current design holds a request in a waiting state or chases the approver.
Today a request applies everything or nothing, so People Operations handles
every non-standard case by hand and the approval ends up in a ticket rather
than the audit log — which is what audit finding 2025-11 objects to.

## 2. Goals and non-goals
**Goals:** a single authoritative state per request; no entitlement applied
before approval where approval is required; every transition auditable;
idempotent under event replay.
**Non-goals:** approval delegation (AP-118), bulk approval, approval of
deprovisioning — leaver revocation is never approved, it is mandatory.

## 3. Proposed design
States and permitted transitions:

DRAFT -> AWAITING_BUNDLE -> AWAITING_APPROVAL -> APPROVED -> APPLYING ->
COMPLETE | PARTIAL
AWAITING_APPROVAL -> REJECTED -> APPLYING (bundle entitlements only)
Any state -> CANCELLED (People Ops, with justification)

Transitions are rows in `request_transition`, not an UPDATE on the request.
The request's current state is a materialised column maintained in the same
transaction as the transition insert, with a check that the previous state
matches. Concurrent approval attempts therefore collide on the version column
and the loser gets 412 rather than a lost update.

Timers (the 72-hour escalation, UC-07 4a4) are rows in a `due_action` table
polled every minute, not in-process timers — the service is deployed with
rolling restarts and in-process timers would be lost.

Entitlement application (APPLYING) iterates adapters. Each adapter call is
keyed by (request_id, entitlement) so a replay is a no-op. The request moves to
COMPLETE only when every entitlement is APPLIED; if any is FAILED after
retries, it moves to PARTIAL and a ticket is raised. PARTIAL is a terminal
state — resolution is a new request, not a mutation of this one.

## 4. Alternatives considered
A workflow engine (Temporal) was considered. Rejected: one state machine with
eight states does not justify a new runtime dependency, an operational burden
and a second place where state lives. Revisit if a second workflow of this
complexity appears.

## 5. Data changes
New tables: `request_transition`, `due_action`. `request.state` becomes a
materialised column with a check constraint. No backfill needed — no requests
exist in production yet. Reversible by dropping the two tables; the column has
a default.

## 6. Failure modes
| Failure | Detection | Behaviour | Blast radius |
|---|---|---|---|
| Audit write fails | Error from audit sink | Transition aborts, transaction rolls back, retried by the poller | One request |
| Adapter times out | Adapter deadline 30s | Retry per policy, then FAILED for that entitlement, request PARTIAL | One entitlement of one request |
| due_action poller stops | `due_actions_overdue` gauge > 0 for 10 min | Escalations delayed; alert pages platform on-call | All pending approvals |
| Two managers approve simultaneously | Version conflict | Second gets 412; first approval stands and is the audited one | One request |
| HR event replayed | Idempotency on event ID | No new request created | None |


## 7. Performance and capacity
Peak is the graduate intake: 500 requests in a day, each with ~9 entitlements,
so ~4,500 adapter calls. Adapters are the bottleneck, not the state machine —
the legacy ERP accepts one batch per night regardless. The design would be
wrong if a single request needed more than ~50 entitlements, since application
is sequential per request; at 9 this is not worth parallelising.

## 8. Security and privacy
Approval is the security-relevant step, so it gets the attention. Approving
requires a user-delegated token; a service token holding
`provisioning.approve` is rejected, because an approval that cannot be
attributed to a person does not satisfy the control. The approver's identity
comes from the token, never from the request body — otherwise a caller could
name any approver it liked.

The justification field is free text typed by a manager and is treated as
potentially personal: written to the audit store, excluded from operational
logs and from the log export, retained seven years, not erasable. The DPIA
records that refusal.

No new secrets are introduced. The state machine holds no credentials; only
adapters talk to targets, using existing per-target service credentials.

## 9. Observability
- `requests_by_state` gauge, `transition_total{from,to}` counter.
- `approvals_pending` gauge, alert at >20 for 2 hours.
- `due_actions_overdue` gauge, page at >0 for 10 minutes.
- Every log line carries request_id and correlation_id.
- Dashboard "Provisioning — pipeline" shows state counts, adapter error rates
  and the overdue gauge on one screen.

## 10. Testing strategy
- **Unit:** table-driven over every permitted *and* forbidden transition. The
  forbidden half is the one that matters — a state machine that allows too
  much is the failure mode here.
- **Integration:** the four extension paths from UC-07 against sandbox
  targets, plus the 72-hour escalation with an injected clock (TC-124).
- **Contract:** unchanged; the adapter interface does not move.
- **Concurrency:** two simultaneous approvals must yield one applied approval
  and one 412 — asserted in a test, not reasoned about.
- **Replay:** the same HR event delivered twice must produce one request and
  one set of grants, tested by replaying a recorded event stream.
- **Load:** no separate suite. The intake load test covers this path; the
  bottleneck is adapters, not the state machine.

## 11. Rollout and rollback
Behind flag `approval_state_machine`. Enabled first for a single job code
(ENG-3), then all. Rollback is disabling the flag; requests already in flight
under the flag are completed manually by People Ops — at most a handful, since
the first cohort is one job code.

## 12. Open questions
- Should CANCELLED be permitted from APPLYING? Currently yes, which can leave
  entitlements applied. Proposal: forbid it, require a deprovisioning request
  instead. Decision needed before general enablement.
{{< /doctabs >}}

## Common mistakes

- **Design that stops at the happy path.** The failure-modes table is what reviewers should spend their time on.
- **No non-goals.** Reviewers will otherwise raise every adjacent concern, and the review will not converge.
- **Alternatives omitted because the author already decided.** The reviewer cannot tell whether an option was rejected or never considered.
- **Observability as an afterthought.** If you cannot name the alert and the dashboard, the design is not finished.
- **No rollback story.** "We would fix forward" is a plan only if the change is backwards compatible; say why it is.

## Related templates

- [Solution Architecture Document](/docs/architecture-design/solution-architecture-document/) — the level above.
- [Architecture Decision Record](/docs/architecture-design/architecture-decision-record/) — for decisions inside this design that outlive it.
- [Code Review Checklist](/docs/development-release/code-review-checklist/) — what reviewers check once this is built.
- [Operational Runbook](/docs/operations-incident/operational-runbook/) — the failure modes table feeds it directly.
- [Architecture & Design](/docs/architecture-design/) — the other four architecture and design templates.
