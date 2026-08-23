---
weight: 5020
title: "Test Case Specification"
description: "Cases precise enough that two testers get the same result, and a failure is unambiguous."
icon: "checklist"
date: "2026-08-23"
draft: false
---

A test case is a repeatable experiment. If the preconditions are vague or the expected result is "works correctly", the case cannot fail cleanly — and a case that cannot fail cleanly generates argument instead of information.

## When to use it

- Manual test execution, especially by people who did not write the software.
- Regulated environments where executed evidence must be retained.
- As the specification for automated cases, so intent survives when the code is refactored.

## What it must answer

- What state must exist before this case runs?
- What exactly does the tester do?
- What is the observable expected result, including in the system's data and logs?
- Which requirement does this case exist to verify?

## Template

{{< doctabs >}}
| Field | Value |
|---|---|
| Case ID | TC-nnn |
| Title | |
| Verifies | FR/NFR/BR IDs |
| Level | Unit / Integration / System / UAT |
| Type | Positive / Negative / Boundary / Security / Performance |
| Priority | |
| Automated | Yes / No / Planned |
| Preconditions | |
| Test data | |

## Steps
| # | Action | Expected result |
|---|---|---|

## Postconditions
State the system should be left in, including data and audit records.

## Cleanup
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
| Field | Value |
|---|---|
| Case ID | TC-124 |
| Title | Approval times out after 72 hours and escalates to the manager's manager |
| Verifies | FR-03, UC-07 extension 4a4 |
| Level | Integration |
| Type | Boundary / negative |
| Priority | High — this is the path that silently blocks a joiner's start date |
| Automated | Yes (int suite, clock injected) |
| Preconditions | Service running with `approval_state_machine` enabled; employee E-TEST-01 exists with manager E-TEST-02, whose manager is E-TEST-03; notification service reachable |
| Test data | Job code ENG-3 (bundle eng-3@17); additional entitlement `repo:payments:write` |

## Steps
| # | Action | Expected result |
|---|---|---|
| 1 | Create a request for E-TEST-01 with the additional entitlement | 201; state AWAITING_APPROVAL; bundle_version = eng-3@17 |
| 2 | Confirm no entitlement has been applied | All entitlements in state PENDING or AWAITING_APPROVAL; no adapter call recorded |
| 3 | Confirm notification to E-TEST-02 | Notification record exists within 5 minutes, addressed to E-TEST-02 |
| 4 | Advance the injected clock to T+71h59m | State unchanged; no escalation notification |
| 5 | Advance the injected clock to T+72h01m | Within one poll interval (60s): notification sent to E-TEST-03; audit record `approval_escalated` written with both employee IDs |
| 6 | Confirm bundle entitlements applied | The 9 bundle entitlements move to APPLIED; `repo:payments:write` remains AWAITING_APPROVAL |
| 7 | Approve as E-TEST-03 with justification "Covering approver, joiner starts Monday" | 200; `repo:payments:write` moves to APPLIED; audit record shows approver E-TEST-03 and the justification |
| 8 | Query the audit log for the request | Exactly one record per grant, one for the escalation, one for the approval; no duplicates |

## Postconditions
Request in state COMPLETE with 10 applied entitlements. Audit log contains 12
records for this request. No open service desk ticket.

## Cleanup
Revoke all entitlements for E-TEST-01 via the deprovisioning flow (not by
direct database edit — the audit log must reflect the revocation). Reset the
injected clock.
{{< /doctabs >}}

## Common mistakes

- **"Verify the system works correctly."** Not a result. Say what is observably true afterwards.
- **Preconditions that assume yesterday's leftovers.** Cases that only pass in a particular order are worthless in parallel execution and in CI.
- **Checking the UI only.** Step 8 above — checking the audit records — is what catches double-writes that the screen hides.
- **No cleanup, or cleanup by direct database edit.** Editing data behind the application's back leaves a state the application can never produce, and later failures get blamed on the wrong thing.
- **One case covering six requirements.** When it fails, nobody knows which requirement is broken. Keep it to one intent per case.

## Related templates

- [Test Plan](/docs/testing-qa/test-plan/) — the scope these cases sit inside.
- [User Story](/docs/requirements/user-story/) — acceptance criteria convert almost directly into cases.
- [Use Case Specification](/docs/requirements/use-case-specification/) — each extension deserves at least one case.
- [Defect Report](/docs/testing-qa/defect-report/) — what to raise when a case fails.
- [Testing & QA](/docs/testing-qa/) — the other four testing and QA templates.
