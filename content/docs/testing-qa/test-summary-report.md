---
weight: 5050
title: "Test Summary Report"
description: "What was tested, what was found, and what is being shipped with known problems."
icon: "assessment"
date: "2026-08-23"
draft: false
---

The test summary report is the evidence behind a release decision. It is not a recommendation to ship — that decision belongs to the business owner. Keeping those separate is what lets a tester state uncomfortable facts without appearing to block the release.

## When to use it

- At the end of every formal test cycle, before a go/no-go decision.
- As the retained evidence for audit and for contractual acceptance.
- As the input to the release decision meeting, circulated beforehand.

## What it must answer

- Was the plan executed, and where did execution deviate from it?
- What are the results against the stated exit criteria?
- What is still open, and what is the risk of shipping with it open?
- What could we not test, and what does that leave unknown?

## Template

{{< doctabs >}}
# Test Summary Report: <Release>

| Field | Value |
|---|---|
| Cycle / dates | |
| Test lead | |
| Build tested | commit / version |
| Related | Test Plan v_, RTM v_ |


## 1. Summary
Three sentences: what was tested, headline result, what remains open.

## 2. Execution
| Suite | Planned | Executed | Passed | Failed | Blocked | Not run |
|---|---|---|---|---|---|---|


Explain every deviation from plan.

## 3. Exit criteria status
| Criterion | Target | Actual | Met? |
|---|---|---|---|


## 4. Defects
| Severity | Found | Fixed | Open | Deferred |
|---|---|---|---|---|


Open defects listed individually with impact and workaround.

## 5. Coverage
By requirement priority; reference the RTM.

## 6. Non-functional results
Performance, resilience, security, accessibility — numbers, not verdicts.

## 7. Untested areas and residual risk
| Area | Why not tested | Residual risk | Accepted by |
|---|---|---|---|


## 8. Environment and data notes
Anything that limits confidence in the results.

## 9. Conclusion
State the facts against the criteria. The release decision belongs to the
business owner and is recorded separately.
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Test Summary Report: Access Provisioning Service 1.0

| Field | Value |
|---|---|
| Cycle / dates | System test 2026-10-05 to 2026-11-14; UAT 2026-11-17 to 2026-11-28 |
| Test lead | H. Ito |
| Build tested | v1.0.0-rc4, commit 9f3c1ab |


## 1. Summary
All Must requirements are covered and passing except FR-04 for the legacy ERP,
where revocation is nightly rather than hourly. One Sev-1 defect was found late
(DEF-2026-0311) and fixed. Two Sev-3 defects remain open with workarounds, and
one accepted gap is carried into production with a compensating control.

## 2. Execution
| Suite | Planned | Executed | Passed | Failed | Blocked | Not run |
|---|---|---|---|---|---|---|
| Integration | 186 | 186 | 184 | 2 | 0 | 0 |
| Contract | 44 | 44 | 44 | 0 | 0 | 0 |
| Performance | 9 | 9 | 9 | 0 | 0 | 0 |
| Security (pen test) | — | 1 engagement | — | — | — | — |
| DR exercise | 1 | 1 | 1 | 0 | 0 | 0 |
| UAT scenarios | 8 | 8 | 7 | 1 | 0 | 0 |


Deviation: integration testing was suspended 2026-10-21 to 2026-10-23 when the
vendor sandbox changed its 3DS response shape without notice. The affected 26
cases were re-run from a clean state after contract recordings were refreshed.

## 3. Exit criteria status
| Criterion | Target | Actual | Met? |
|---|---|---|---|
| Must requirements with a passing test | 100% | 11 of 12 | No — see accepted gap |
| Should requirements passing | >= 95% | 100% (3 of 3) | Yes |
| Open Sev-1 | 0 | 0 | Yes |
| Open Sev-2 without approved deferral | 0 | 0 | Yes |
| p95 provisioning latency at 40 events/h | <= 30 min | 11 min | Yes |
| 500-event intake within one working day | Yes | 3h 12m | Yes |
| DR: RTO / RPO | 4h / 15 min | 2h 51m / 4 min | Yes |
| Pen test High/Critical unresolved | 0 | 0 (2 Medium open, scheduled) | Yes |
| Audit log completeness on 1,000-grant sample | 100% | 100% | Yes |


## 4. Defects
| Severity | Found | Fixed | Open | Deferred |
|---|---|---|---|---|
| Sev-1 | 1 | 1 | 0 | 0 |
| Sev-2 | 6 | 6 | 0 | 0 |
| Sev-3 | 19 | 17 | 2 | 0 |
| Sev-4 | 31 | 12 | 19 | 19 |


Open Sev-3:
- DEF-2026-0327: bundle admin screen paginates incorrectly beyond 200 bundles.
  Impact: People Ops cannot see bundles past page 4. Workaround: search by job
  code. Fix scheduled 1.0.1.
- DEF-2026-0333: the daily exception report lists leavers in a non-obvious
  order. Impact: cosmetic but slows the review. Workaround: sort in the
  spreadsheet. Fix scheduled 1.0.1.

## 6. Non-functional results
- Performance: p95 11 min, p99 19 min at 40 events/hour. Bottleneck is adapter
  latency, not the service.
- Resilience: with one adapter fully down, other entitlements continued to
  apply; requests ended PARTIAL with tickets raised, as designed.
- Security: pen test found 2 Medium (verbose error message on the admin login;
  missing `Cache-Control: no-store` on an authenticated response). Both fixed
  in rc4 and retested; no High or Critical.
- Accessibility: admin UI at WCAG 2.1 AA except two contrast failures on the
  status badges — DEF-2026-0339, fix scheduled 1.0.1.

## 7. Untested areas and residual risk
| Area | Why not tested | Residual risk | Accepted by |
|---|---|---|---|
| Contractor identities | Not built | None for this release | K. Ferreira |
| Sustained load beyond 500 events/day | No business case for higher volumes | Unknown behaviour above ~2x peak; would need a load test before any acquisition-driven intake | A. Vogel |
| ERP behaviour under simultaneous joiner and leaver for the same person | Cannot be produced in the vendor sandbox | Ordering ambiguity in a rare case; mitigated by the daily exception report | A. Vogel, L. Haddad |


## 8. Environment and data notes
UAT ran on anonymised production data refreshed 2026-11-14. Two UAT scenarios
used manually constructed records because the anonymised set contained no
employee without a manager — the very case that scenario 2 needed. That case is
therefore less well evidenced than the others.

## 9. Conclusion
Exit criteria are met except "100% of Must requirements passing", which stands
at 11 of 12 due to the legacy ERP nightly revocation window (FR-04). That gap
is documented in the RTM with a compensating control accepted by Internal Audit
and the business owner. All other criteria are met with margin.
{{< /doctabs >}}

## Common mistakes

- **A recommendation instead of evidence.** "QA recommends release" transfers a business decision to the wrong person and discourages honest reporting.
- **Pass rates without the denominator's story.** 184 of 186 looks fine until you learn 26 cases were re-run after a mid-cycle environment change.
- **No untested-areas section.** What was not tested is the part a release decision most needs and least often gets.
- **Open defects summarised only as counts.** List them individually with impact and workaround; a count tells the reader nothing about risk.
- **Written after the go-live decision.** Then it is a record of a decision, not an input to one.

## Related templates

- [Test Plan](/docs/testing-qa/test-plan/) — the criteria reported against here.
- [UAT Plan](/docs/testing-qa/uat-plan/) — the acceptance side of the evidence.
- [Requirements Traceability Matrix](/docs/requirements/requirements-traceability-matrix/) — the coverage source.
- [Release Notes](/docs/development-release/release-notes/) — where open defects become known issues.
- [Testing & QA](/docs/testing-qa/) — the other four testing and QA templates.
