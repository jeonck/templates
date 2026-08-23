---
weight: 5010
title: "Test Plan"
description: "What will be tested, how, by whom, and what we are consciously not testing."
icon: "science"
date: "2026-08-23"
draft: false
---

A test plan is a scoping document, not a list of tests. Its most valuable sections are the ones that say what will *not* be covered and what conditions stop testing — those are the statements that get renegotiated under deadline pressure, and having them written down is what makes that renegotiation visible.

## When to use it

- Releases with an acceptance gate, external users, or regulatory exposure.
- Any test effort involving more than one team or a shared environment.
- Not for a single story; its acceptance criteria are its test plan.

## What it must answer

- What is in scope, and at which level is each thing tested?
- What environments and data are needed, and who provides them?
- What are the entry and exit criteria, in numbers?
- What risks are we accepting by not testing something?

## Template

{{< doctabs >}}
# Test Plan: <Release or system>

| Field | Value |
|---|---|
| Version / date | |
| Test lead | |
| Approvers | |
| Related | SRS v_, RTM v_ |


## 1. Scope
In scope / out of scope, by feature and by quality attribute.

## 2. Test levels and responsibility
| Level | What it proves | Owner | Automation |
|---|---|---|---|


## 3. Approach per quality attribute
Functional, performance, security, resilience, accessibility, data migration.

## 4. Environments
| Environment | Purpose | Data | Refresh | Owner |
|---|---|---|---|---|


## 5. Test data
Source, anonymisation, volume, and how personal data is handled.

## 6. Entry criteria
## 7. Exit criteria
Numbers, not adjectives.

## 8. Suspension and resumption criteria
When testing stops, and what must happen before it restarts.

## 9. Defect management
Severity definitions, triage cadence, who decides on deferral.

## 10. Risks to the test effort
| Risk | Impact | Mitigation |
|---|---|---|


## 11. Schedule and resources
## 12. Deliverables
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Test Plan: Access Provisioning Service, release 1.0

| Field | Value |
|---|---|
| Version / date | 2.0 / 2026-09-08 |
| Test lead | H. Ito |
| Approvers | A. Vogel (engineering), K. Ferreira (business), L. Haddad (audit) |


## 1. Scope
**In scope:** all Must and Should requirements in SRS v2.0; the eleven target
system adapters; the joiner, mover and leaver flows; audit log completeness;
performance at graduate-intake volume; DR recovery.
**Out of scope:** the admin UI's visual design (accessibility is in scope, look
and feel is not); the HR system itself; contractor identities (not built).

## 2. Test levels and responsibility
| Level | What it proves | Owner | Automation |
|---|---|---|---|
| Unit | State transitions, bundle resolution, validation | Developers | 100% automated, runs per commit |
| Contract | Adapter behaviour against recorded provider responses | Developers | Automated, nightly refresh check |
| Integration | End-to-end through real sandbox targets | QA | Automated, nightly |
| UAT | People Ops and managers can complete real tasks | Business | Manual, scripted |
| Performance | Intake volumes, p95 latency | QA | Automated, per release candidate |
| Security | Authorisation, secrets handling, injection | External pen test | Manual, once per release |
| DR | RPO/RTO under a simulated region loss | Platform | Manual exercise, once |


## 4. Environments
| Environment | Purpose | Data | Refresh | Owner |
|---|---|---|---|---|
| dev | Developer testing | Synthetic, 50 employees | On demand | Platform |
| int | Automated integration | Synthetic, 4,000 employees | Nightly rebuild | QA |
| uat | Business acceptance | Anonymised production copy | Weekly | QA |
| perf | Load and soak | Synthetic, 6,000 employees | Per test | QA |


Only int and uat are connected to real vendor sandboxes. There is one uat
environment shared with the Finance reconciliation project — a scheduling
conflict risk, see section 10.

## 5. Test data
UAT data is a production copy with names, emails and free-text justifications
replaced by generated values; employee IDs are pseudonymised consistently so
relationships survive. No production personal data reaches dev, int or perf.
The anonymisation script is itself tested (TC-240) because a failure there
would be a personal data breach, not a test failure.

## 6. Entry criteria
- All Must requirements implemented and unit tested.
- Contract tests green against current sandbox recordings.
- Zero open Sev-1 defects; no more than 3 open Sev-2.
- uat refreshed within the last 7 days.

## 7. Exit criteria
- 100% of Must requirements have at least one passing test (per the RTM).
- >= 95% of Should requirements passing.
- Zero open Sev-1; zero open Sev-2 without a written, approved deferral.
- p95 provisioning latency <= 30 minutes at 40 events/hour, and the 500-event
  intake completes within one working day.
- DR exercise achieves RTO <= 4h and RPO <= 15 min.
- Pen test has no unresolved High or Critical finding.
- Audit log completeness check: 100% of grants in a 1,000-grant sample have a
  matching audit record.

## 8. Suspension and resumption criteria
Testing is suspended if the int environment is unavailable for more than four
hours, if a Sev-1 defect blocks more than 30% of planned cases, or if a
sandbox provider changes behaviour mid-cycle. Resumption requires the blocking
condition cleared and a re-run of the affected suite from a clean state.

## 9. Defect management
| Severity | Definition | Response |
|---|---|---|
| Sev-1 | Wrong access granted or revocation fails; data loss; audit record missing | Stop the line, fix immediately |
| Sev-2 | Core flow blocked, no workaround | Fix before release |
| Sev-3 | Workaround exists | Fix or defer with approval |
| Sev-4 | Cosmetic | Backlog |


Triage daily at 09:30 during the cycle. Only the test lead plus the business
approver may defer a Sev-2, and only in writing.

## 10. Risks to the test effort
| Risk | Impact | Mitigation |
|---|---|---|
| uat shared with the Finance project | Cycle delayed by contention | Booked slots agreed 2026-09-01; escalation to M. Duarte |
| Vendor sandbox behaviour diverges from production | False confidence — assumption A-03 | 5% live ramp before full cutover; treat the ramp as a test phase |
| Anonymisation script defect | Personal data in a lower environment | TC-240 verifies it; uat refresh blocked if it fails |


## 12. Deliverables
Test plan (this), test cases in the tracker, defect reports, weekly progress
summary, RTM coverage extract, and the test summary report at exit.
{{< /doctabs >}}

## Common mistakes

- **Exit criteria written as adjectives.** "Quality is acceptable" cannot be argued with data. Numbers can.
- **No suspension criteria.** Teams grind on against a broken environment, producing results nobody trusts.
- **Out-of-scope section missing.** Everyone then assumes their concern is covered, and discovers otherwise after release.
- **Test data handling unstated.** Copying production data into a test environment is one of the most common sources of real breaches.
- **A plan that duplicates the test cases.** Keep cases in the tracker; the plan says what kinds exist and why.

## Related templates

- [Test Case Specification](/docs/testing-qa/test-case-specification/) — the level of detail this plan deliberately omits.
- [UAT Plan](/docs/testing-qa/uat-plan/) — the business acceptance slice.
- [Test Summary Report](/docs/testing-qa/test-summary-report/) — reports against these exit criteria.
- [Requirements Traceability Matrix](/docs/requirements/requirements-traceability-matrix/) — where coverage is proven.
- [Testing & QA](/docs/testing-qa/) — the other four testing and QA templates.
