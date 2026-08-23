---
weight: 2040
title: "Use Case Specification"
description: "Step-by-step actor–system interaction, including every way it can go wrong."
icon: "account_tree"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

A use case documents a complete interaction from trigger to outcome. Its distinctive value is the alternate and exception flows: the numbered branches where things deviate. Those branches are where most defects and most missing requirements live.

## When to use it

- Interactions with many decision points, states or error paths — payments, claims, onboarding, regulated workflows.
- When several actors, including systems and timers, participate in one flow.
- When a [User Story](/docs/requirements/user-story/)'s Given/When/Then set has grown past about eight scenarios and lost its shape.

## What it must answer

- What triggers this, and what must already be true?
- What is the sequence of steps in the normal case?
- At each step, what else can happen, and what does the system do then?
- What is guaranteed to be true when it finishes, in success and in failure?

## Template

```markdown
# UC-<id>: <Use case name>

| Field | Value |
|---|---|
| Primary actor | |
| Secondary actors | |
| Trigger | |
| Preconditions | |
| Success guarantee | |
| Minimal guarantee | What holds even when the case fails |
| Frequency | |

## Main success scenario
1. Actor does X.
2. System validates Y.
3. System records Z.
4. System notifies ...

## Extensions
2a. <Condition at step 2>
    2a1. System does ...
    2a2. Use case ends / resumes at step 3.

3a. <Condition at step 3>
    3a1. ...

## Special requirements
Performance, security, localisation, accessibility specific to this case.

## Open questions
```

## Worked example

```markdown
# UC-07: Provision access for a new joiner

| Field | Value |
|---|---|
| Primary actor | Provisioning Service (triggered by HR event) |
| Secondary actors | Line manager, target systems, service desk |
| Trigger | New employee record appears in the HR feed |
| Preconditions | Employee record has employee ID, job code, start date and manager ID |
| Success guarantee | All entitlements for the resolved bundle are active before the start date, and every grant is recorded in the audit log |
| Minimal guarantee | No entitlement is granted without a recorded justification, and any partial state is visible as an open service desk ticket |
| Frequency | ~380 per year, peaking at 90 in the September graduate intake |

## Main success scenario
1. HR feed emits a joiner event.
2. System validates the record has all mandatory fields.
3. System resolves the job code to an access bundle.
4. System creates a provisioning request in state APPROVED.
5. System applies each entitlement to its target system in dependency order.
6. System writes a grant record to the audit log for each entitlement.
7. System notifies the joiner's manager that provisioning is complete.
8. Use case ends with the request in state COMPLETE.

## Extensions

2a. Mandatory field missing.
    2a1. System raises a data-quality ticket naming the field and employee ID.
    2a2. System does not create a provisioning request.
    2a3. Use case ends.

2b. Duplicate event for an employee ID already provisioned.
    2b1. System deduplicates on event ID and records the duplicate.
    2b2. Use case ends without side effects.

3a. Job code does not map to any bundle.
    3a1. System routes the request to the People Ops queue in state
         AWAITING_BUNDLE.
    3a2. People Ops assigns a bundle or creates one.
    3a3. Resume at step 4.

4a. Request contains an entitlement outside the bundle (added by People Ops).
    4a1. System sets state AWAITING_APPROVAL and notifies the line manager.
    4a2. Manager approves -> resume at step 5.
    4a3. Manager rejects -> system applies only bundle entitlements, records
         the rejection, resumes at step 6.
    4a4. No decision within 72 hours -> system escalates to the manager's
         manager and applies the standard bundle; resume at step 5 for
         bundle entitlements only.

5a. A target system rejects the call.
    5a1. System retries 5 times with exponential backoff.
    5a2. If still failing, system marks that entitlement FAILED, leaves the
         others applied, and raises a service desk ticket with the
         correlation ID.
    5a3. Request ends in state PARTIAL. Resume at step 6 for successful
         entitlements.

5b. Start date is more than 14 days in the future.
    5b1. System schedules application for start date minus 1 working day.
    5b2. Use case suspends until then, then resumes at step 5.

7a. Manager notification fails.
    7a1. System retries for 24 hours, then logs and continues. Notification
         failure never blocks provisioning.

## Special requirements
- Steps 5 and 6 must be idempotent; a replayed event must not double-grant.
- The audit log write (step 6) must succeed or the grant is treated as FAILED —
  an unlogged grant is worse than a missing one.
- Correlation ID from step 1 propagates to every downstream call.

## Open questions
- Does the legacy ERP support scheduling (5b), or must we hold the request?
```

## Common mistakes

- **Only the happy path.** A use case without extensions is a paragraph with numbers. The extensions are the deliverable.
- **UI detail in the steps.** "User clicks the blue Submit button" pins the design and dates the document. Say what the actor accomplishes.
- **No minimal guarantee.** What holds when things fail is exactly what operations and audit need to know.
- **Extensions that do not say where the flow resumes.** "System shows an error" leaves the state undefined; every extension must end, resume at a numbered step, or transition to another use case.
- **One giant use case.** If the main scenario is longer than about ten steps, there are probably two use cases.

## Related templates

- [User Story](/docs/requirements/user-story/) — the lighter-weight alternative.
- [Software Requirements Specification](/docs/requirements/software-requirements-specification/) — where these cases are referenced as sources.
- [Test Case Specification](/docs/testing-qa/test-case-specification/) — each extension becomes at least one test case.
- [Technical Design Document](/docs/architecture-design/technical-design-document/) — states and transitions above become the design's state machine.
