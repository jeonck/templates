---
weight: 2030
title: "User Story"
description: "A small unit of value with acceptance criteria you can argue about before the work starts."
icon: "person"
date: "2026-08-23"
draft: false
---

A user story is a placeholder for a conversation, plus a written record of how that conversation ended. The story text matters much less than the acceptance criteria — those are what a developer builds against and a tester verifies.

## When to use it

- Iterative product delivery with a stable team and a product owner available for questions.
- Any change small enough to finish inside one iteration.
- Not for cross-team contracts or fixed-price scope; use an [SRS](/docs/requirements/software-requirements-specification/) there.

## What it must answer

- Who wants this, and what do they get that they cannot get today?
- How will we know it works — in specific, observable terms?
- What is deliberately not included in this story?
- What has to be true before it can start?

## Template

{{< doctabs >}}
## <Short title>

**As a** <role>
**I want** <capability>
**So that** <outcome the role values>

### Acceptance criteria
Given <context>
When <action>
Then <observable result>

(Repeat per scenario. Cover the unhappy paths and the boundaries, not just
the golden path.)

### Out of scope
- ...

### Preconditions / dependencies
- ...

### Non-functional notes
Performance, security, accessibility or data constraints that apply to
this story specifically.

### Definition of done
- [ ] Acceptance criteria demonstrated
- [ ] Automated tests added at the appropriate level
- [ ] Observability: metric or log line for the new path
- [ ] Documentation updated
- [ ] No new high or critical vulnerability introduced
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
## Manager approves a non-standard entitlement

**As a** line manager
**I want** to approve or reject access that falls outside a joiner's standard role bundle
**So that** unusual access is granted deliberately and there is a record of who allowed it

### Acceptance criteria

Given a provisioning request contains an entitlement not present in the resolved bundle
When the request is created
Then the request enters state AWAITING_APPROVAL
And the line manager named on the HR record receives a notification within 5 minutes
And no entitlement in the request is applied to any target system

Given a request is AWAITING_APPROVAL
When the line manager approves it with a justification of at least 20 characters
Then all entitlements in the request are applied
And the audit log records approver, timestamp, entitlement list and justification

Given a request is AWAITING_APPROVAL
When the line manager rejects it
Then only the standard bundle entitlements are applied
And the non-standard entitlements are recorded as REJECTED with the reason

Given a request is AWAITING_APPROVAL
When 72 hours pass with no decision
Then the request escalates to the manager's manager
And the joiner's standard bundle is applied in the meantime

Given the HR record has no line manager
When a request requiring approval is created
Then the request is routed to the People Ops queue
And an alert is raised, because this indicates an HR data defect

### Out of scope
- Bulk approval of multiple joiners in one action (separate story).
- Delegation of approval rights during absence (backlog item AP-118).

### Preconditions / dependencies
- HR feed exposes the manager's employee ID (delivered in story AP-104).
- Notification service supports the approval deep link.

### Non-functional notes
- The approval link must be usable on mobile; managers approve from phones.
- Justification text is personal data adjacent — retained with the audit log
  for 7 years, not in operational logs.

### Definition of done
- [x] Acceptance criteria demonstrated to product owner 2026-07-09
- [x] Contract tests for the four states, plus the no-manager case
- [x] Metric: approvals_pending gauge, alert at >20 for 2h
- [x] Runbook section added for the People Ops queue
- [x] Dependency scan clean
{{< /doctabs >}}

## Common mistakes

- **"As a user, I want..."** — if the role is "user", nobody has thought about who this is for. The role should change the design.
- **Acceptance criteria that only cover the happy path.** The timeout case and the missing-data case above are where the real design decisions were made.
- **The "so that" clause restating the "I want" clause.** "So that I can approve access" adds nothing; "so that unusual access is deliberate and attributable" explains why it is worth building.
- **Stories sized to a sprint boundary rather than to a coherent slice.** Splitting by layer ("build the API", "build the UI") produces stories that deliver nothing on their own.
- **Definition of done as a ritual.** If observability and docs are never actually checked, remove them from the list rather than pretending.

## Related templates

- [Use Case Specification](/docs/requirements/use-case-specification/) — when interaction flows are too complex for Given/When/Then.
- [Test Case Specification](/docs/testing-qa/test-case-specification/) — acceptance criteria become test cases directly.
- [Pull Request Template](/docs/development-release/pull-request-template/) — where the definition of done is enforced.
- [Software Requirements Specification](/docs/requirements/software-requirements-specification/) — the formal alternative.
- [Requirements & Analysis](/docs/requirements/) — the other four requirements templates.
