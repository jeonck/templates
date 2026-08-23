---
weight: 2050
title: "Requirements Traceability Matrix"
description: "One table proving every requirement reached design, code and test — and that nothing untraceable was built."
icon: "table_chart"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

The RTM answers two questions that nothing else answers cheaply: is every requirement covered by a test, and does every piece of built functionality trace back to a requirement? The second direction catches gold-plating and scope creep.

## When to use it

- Regulated delivery (medical, financial, safety, public sector) where coverage evidence is mandatory.
- Fixed-price contracts, where acceptance depends on demonstrable coverage.
- Any project large enough that "did we test that?" cannot be answered from memory.
- Skip it for small internal product work where the [Test Plan](/docs/testing-qa/test-plan/) already references stories directly.

## What it must answer

- For each business requirement: which system requirement implements it, which design element realises it, which tests verify it, and what the current result is.
- For each test: which requirement justifies its existence.
- What is deliberately untested, and who accepted that.

## Template

{{< doctabs >}}
# Requirements Traceability Matrix: <Project>

| Field | Value |
|---|---|
| Version / date | |
| Maintained by | |
| Sources | BRD v_, SRS v_, Test Plan v_ |

## Forward trace
| BR ID | SRS ID | Design ref | Code ref | Test case IDs | Test result | Status |
|---|---|---|---|---|---|---|

## Backward trace (orphans)
| Built element | Traces to | Justification if none |
|---|---|---|

## Coverage summary
| Priority | Requirements | With >=1 test | Passed | Deferred |
|---|---|---|---|---|

## Accepted gaps
| Requirement | Gap | Accepted by | Date | Compensating control |
|---|---|---|---|---|
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Requirements Traceability Matrix: Access Provisioning Service
Version 3 / 2026-11-04. Maintained by H. Ito.
Sources: BRD v1.2, SRS v2.0, Test Plan v2.

## Forward trace
| BR ID | SRS ID | Design ref | Code ref | Test case IDs | Result | Status |
|---|---|---|---|---|---|---|
| BR-01 | FR-01 | SAD §4.2 event ingest | ingest/handler.go | TC-101, TC-102, TC-118 | Pass | Verified |
| BR-01 | FR-02 | SAD §4.3 bundle resolver | bundles/resolve.go | TC-110, TC-111 | Pass | Verified |
| BR-02 | FR-03 | TDD §3 approval state machine | approval/*.go | TC-120…TC-127 | Pass | Verified |
| BR-02 | FR-05 | SAD §6 audit sink | audit/writer.go | TC-140, TC-141, TC-142 | Pass | Verified |
| BR-03 | FR-04 | TDD §5 leaver scheduler | leaver/schedule.go | TC-150, TC-151 | 1 fail (TC-151, legacy ERP nightly only) | Gap accepted |
| BR-04 | FR-06 | SAD §4.4 bundle admin UI | admin/ | TC-160, TC-161 | Pass | Verified |
| BR-05 | — | — | — | — | — | Deferred to phase 2 |
| — | NFR-01 | SAD §7 | — | TC-200 (load) | Pass — p95 = 11 min vs 30 target | Verified |
| — | NFR-03 | SAD §7 | — | TC-210 (chaos) | Pass | Verified |
| — | NFR-04 | Runbook §9 | — | DR-01 (exercise 2026-10-22) | Pass — RTO 2h51m | Verified |
| — | NFR-06 | Data inventory v4 | — | TC-230 (retention) | Pass | Verified |

## Backward trace (orphans)
| Built element | Traces to | Justification if none |
|---|---|---|
| /admin/bulk-import | — | Built for the September intake load; no requirement. Retained — approved by K. Ferreira 2026-09-08, documented as FR-08 in SRS v2.1 |
| Slack notification channel | — | Removed before release. No requirement, no owner |

## Coverage summary
| Priority | Requirements | With >=1 test | Passed | Deferred |
|---|---|---|---|---|
| Must | 12 | 12 | 11 | 0 |
| Should | 3 | 3 | 3 | 0 |
| Could | 2 | 0 | 0 | 2 |

## Accepted gaps
| Requirement | Gap | Accepted by | Date | Compensating control |
|---|---|---|---|---|
| BR-03 / FR-04 | Legacy ERP revokes on the nightly batch, so worst case is 26h not 1h | L. Haddad (Internal Audit), K. Ferreira | 2026-10-30 | Daily exception report of accounts active past their leave date, reviewed by People Ops; ERP replacement on the FY2027 roadmap |
{{< /doctabs >}}

## Common mistakes

- **Only the forward trace.** Without the backward trace you never discover the feature nobody asked for — which still has to be maintained and secured.
- **Maintained by hand at the end.** An RTM written the week before acceptance is a fiction. Generate it from IDs already present in commits and test names.
- **Test IDs with no results.** Coverage means a test that ran and passed, not a test that exists.
- **Gaps hidden as "partially verified".** Name the gap, name who accepted it, name the compensating control. That row is the most valuable one in the document.
- **Requirement IDs that change.** Once published, an ID is permanent; supersede rather than renumber, or every trace breaks.

## Related templates

- [Business Requirements Document](/docs/requirements/business-requirements-document/) — the BR column.
- [Software Requirements Specification](/docs/requirements/software-requirements-specification/) — the SRS column.
- [Test Plan](/docs/testing-qa/test-plan/) — defines what "verified" means here.
- [Test Summary Report](/docs/testing-qa/test-summary-report/) — the results column comes from there.
- [Requirements & Analysis](/docs/requirements/) — the other four requirements templates.
