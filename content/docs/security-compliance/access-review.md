---
weight: 7030
title: "Access Review"
description: "Periodic recertification of who has access to what — and the evidence that someone actually looked."
icon: "key"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

An access review is a control that fails quietly. Reviewers approve everything to clear the queue, and the record looks identical to a review that found nothing. The template's job is to make genuine review visible: exceptions found, revocations made, and how long they took.

## When to use it

- Quarterly for privileged access and systems in scope for certification; annually for lower-risk systems.
- On organisational change — a reorganisation or an acquisition invalidates role assumptions wholesale.
- After any incident involving inappropriate access.

## What it must answer

- What was reviewed, over what population, as of what date?
- Who reviewed it, and were they the right person to judge?
- What was found, and what happened as a result?
- What could not be reviewed, and why?

## Template

```markdown
# Access Review: <System or scope> — <period>

| Field | Value |
|---|---|
| Scope | |
| Population as at | date and how the snapshot was taken |
| Review period | |
| Coordinator | |
| Reviewers | |
| Policy reference | |

## 1. Population
| Category | Count |
|---|---|
| Total accounts | |
| Privileged | |
| Service accounts | |
| External / third party | |
| Dormant (> 90 days) | |

## 2. Method
How reviewers were given the data, what they were asked, and how long they had.

## 3. Results
| Reviewer | Accounts | Certified | Revoked | Modified | No response |
|---|---|---|---|---|---|

## 4. Findings
| # | Finding | Accounts affected | Action | Owner | Due | Status |
|---|---|---|---|---|---|---|

## 5. Revocations performed
| Account | Access removed | Reason | Date | Verified by |
|---|---|---|---|---|

## 6. Exclusions
What was not reviewed, and why.

## 7. Comparison with the previous review
Trend, and whether previous findings recurred.

## 8. Attestation
| Name | Role | Statement | Date |
|---|---|---|---|
```

## Worked example

```markdown
# Access Review: Provisioning-managed systems — Q4 2026

| Field | Value |
|---|---|
| Scope | 11 systems provisioned through the Access Provisioning Service |
| Population as at | 2026-12-01, exported by `provctl audit entitlements --as-of 2026-12-01` |
| Review period | 2026-12-01 to 2026-12-19 |
| Coordinator | T. Blomqvist (People Operations) |
| Policy reference | AC-05 |

## 1. Population
| Category | Count |
|---|---|
| Total accounts | 4,118 |
| Total entitlements | 37,402 |
| Privileged | 214 |
| Service accounts | 63 |
| External / third party | 89 |
| Dormant (> 90 days, no authentication) | 147 |

## 2. Method
Each system owner received a list of their system's entitlement holders with
job title, department, manager, grant date, the bundle that granted it, and
last authentication date. Reviewers were asked to mark each as certify, revoke
or modify, with a reason required for anything other than certify. Ten working
days were allowed, with reminders on days 5 and 8. Privileged and dormant
accounts were listed first so that queue fatigue hit the lowest-risk entries.

## 3. Results
| Reviewer | Accounts | Certified | Revoked | Modified | No response |
|---|---|---|---|---|---|
| Platform (A. Vogel) | 640 | 601 | 31 | 8 | 0 |
| Finance systems (M. Duarte) | 812 | 780 | 22 | 10 | 0 |
| ERP (external supplier) | 1,204 | 1,204 | 0 | 0 | 0 |
| Collaboration (D. Achebe) | 1,462 | 1,401 | 54 | 7 | 0 |

The ERP result — 1,204 of 1,204 certified with zero exceptions in under two
hours — is not credible and is treated as a review failure, not a clean result.
See finding 3.

## 4. Findings
| # | Finding | Accounts | Action | Owner | Due | Status |
|---|---|---|---|---|---|---|
| 1 | 147 accounts had not authenticated in over 90 days, including 12 privileged | 147 | Disable after manager confirmation; delete after 30 days | T. Blomqvist | 2027-01-15 | 89 disabled, 58 confirmed still needed (seasonal roles) |
| 2 | 19 employees retained entitlements from a previous role after an internal move | 19 | Revoked; mover flow investigated | A. Vogel | 2026-12-19 | Closed — the mover flow only removes bundle entitlements, not manually added ones. Defect DEF-2026-0361 raised |
| 3 | ERP review completed in 1h 50m with no exceptions across 1,204 accounts | 1,204 | Review rejected; re-run with the supplier's named security officer and a sampled verification by Internal Audit | L. Haddad | 2027-01-31 | Open |
| 4 | 8 service accounts had no named human owner | 8 | Owner assigned or account removed | A. Vogel | 2027-01-15 | 5 assigned, 3 removed |
| 5 | 4 third-party accounts belonged to individuals whose contract ended | 4 | Revoked same day; supplier notified | T. Blomqvist | 2026-12-08 | Closed |

## 6. Exclusions
Two systems (the archived reporting warehouse and the decommissioned intranet)
were excluded: both are read-only, offline, and scheduled for deletion in
Q1 2027. Excluded with CISO approval; if deletion slips past 2027-03-31 they
re-enter scope.

## 7. Comparison with the previous review
| Metric | Q3 2026 | Q4 2026 |
|---|---|---|
| Entitlements revoked | 78 | 107 |
| Dormant accounts | 203 | 147 |
| Findings repeated from the previous review | — | 1 (the ERP rubber-stamp, also seen in Q3) |

Dormant accounts are down 28% following the automated leaver flow. The residual
entitlements from internal moves (finding 2) are new — the mover flow was not
live during the Q3 review.

## 8. Attestation
| Name | Role | Statement | Date |
|---|---|---|---|
| A. Vogel | Platform system owner | I have reviewed all entitlements for my systems and certify the remaining access is appropriate | 2026-12-16 |
| M. Duarte | Finance system owner | As above | 2026-12-17 |
| D. Achebe | Collaboration system owner | As above | 2026-12-18 |
| L. Haddad | Internal Audit | The review was performed as documented, except for the ERP scope, which is rejected and being re-run | 2026-12-19 |
```

## Common mistakes

- **100% certification treated as a good result.** Across a large population it means nobody looked. Track review duration and exception rate as quality signals, and challenge outliers.
- **Reviewers who cannot judge.** A manager three levels up does not know whether an engineer needs a specific database role. Route to whoever knows the work.
- **Access lists without context.** Certifying a list of usernames is impossible. Job title, department, grant reason and last-authentication date make it a real decision.
- **Findings without revocation evidence.** "Should be revoked" is not a control; the revocation date and who verified it is.
- **No comparison with the previous review.** Repeat findings are the strongest signal that the underlying process, not the access, is what needs fixing.

## Related templates

- [Information Security Policy](/docs/security-compliance/information-security-policy/) — statement AC-05 that this evidences.
- [Risk Register](/docs/security-compliance/risk-register/) — where unresolved findings go.
- [Vendor Security Assessment](/docs/security-compliance/vendor-security-assessment/) — for third-party access populations.
