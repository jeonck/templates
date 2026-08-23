---
weight: 7050
title: "Data Protection Impact Assessment"
description: "Structured analysis of privacy risk before processing starts — necessity, proportionality, and what you will do about the risks."
icon: "privacy_tip"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

A DPIA is required under the GDPR (Article 35) where processing is likely to result in a high risk to individuals, and equivalent obligations exist in other regimes. Done at the right time it is a design tool: it forces the necessity and proportionality questions while the design can still change.

## When to use it

- Systematic and extensive automated evaluation of people, including profiling with legal or similarly significant effects.
- Large-scale processing of special-category data, or systematic monitoring of a publicly accessible area.
- New technologies, or any processing your supervisory authority lists as requiring one.
- When in doubt, do a short screening assessment and record why a full DPIA was or was not required.

## What it must answer

- What processing, of whose data, for what purpose, on what lawful basis?
- Is it necessary and proportionate — could the purpose be achieved with less data?
- What are the risks to individuals, not to the organisation?
- What measures reduce those risks, and what remains?

## Template

```markdown
# DPIA: <Processing activity>

| Field | Value |
|---|---|
| Version / date | |
| Controller | |
| DPO consulted | date |
| Status | Draft / Approved / Under review |
| Review date | |

## 1. Screening
Why a DPIA is required (or why not, if this is a screening record).

## 2. Description of processing
Nature, scope, context and purposes. Data flows, including transfers.

| Data category | Subjects | Volume | Source | Retention | Special category? |
|---|---|---|---|---|---|

Recipients, sub-processors, transfers outside the jurisdiction.

## 3. Lawful basis
Per purpose. For legitimate interests, include the balancing test.

## 4. Necessity and proportionality
Could the purpose be met with less data, less granularity, or shorter
retention? Answer honestly, per data category.

## 5. Consultation
Who was consulted — DPO, data subjects or their representatives, processors —
and what they said.

## 6. Risks to individuals
| # | Risk to the individual | Likelihood | Severity | Overall |
|---|---|---|---|---|

## 7. Measures
| Risk | Measure | Effect | Residual | Owner |
|---|---|---|---|---|

## 8. Data subject rights
How access, rectification, erasure, restriction, portability and objection are
handled — including where a right is limited and why.

## 9. Outcome
Sign-off, residual risk accepted, whether prior consultation with the
supervisory authority is required.
```

## Worked example

```markdown
# DPIA: Automated access provisioning and deprovisioning

| Field | Value |
|---|---|
| Version / date | 1.3 / 2026-09-22 |
| Controller | Example Group GmbH |
| DPO consulted | 2026-05-14, 2026-08-30 |
| Status | Approved |
| Review date | 2027-09-22, or on material change |

## 1. Screening
The processing concerns employees, is systematic, and determines access to
systems required to perform their job. It is not automated decision-making with
legal effect under Article 22 — no employment decision is made — but it is
systematic monitoring-adjacent processing of employee data at organisational
scale, and the works council requested a full assessment. A DPIA was therefore
completed.

## 2. Description of processing
Employee records flow from the HR system into a local projection, which drives
the creation and revocation of system access. Grants, revocations and approvals
are recorded in an append-only audit log.

| Data category | Subjects | Volume | Source | Retention | Special category? |
|---|---|---|---|---|---|
| Name, employee ID | Employees, ~4,100 | 4,100 | HR system | 90 days after leave date | No |
| Job code, department, manager ID | Employees | 4,100 | HR system | 90 days after leave date | No |
| Start and leave dates | Employees | 4,100 | HR system | 90 days after leave date | No |
| Entitlement grants and revocations | Employees | ~9,000/yr | Generated | 7 years | No |
| Approval justification (free text) | Employees + approving managers | ~800/yr | Manager input | 7 years | Potentially — free text |
| Last authentication timestamp | Employees | 4,100 | Target systems | 12 months | No |

Recipients: eleven internal target systems; Internal Audit (read-only export).
No transfers outside the EEA. One processor: the cloud infrastructure provider,
under an existing data processing agreement.

## 3. Lawful basis
- Provisioning and revocation: legitimate interests (Art. 6(1)(f)) — securing
  systems and enabling employees to work. Balancing test in section 4.
- Audit log retention for 7 years: legal obligation (Art. 6(1)(c)) under
  financial-reporting record-keeping requirements, and legitimate interests for
  the remainder.
- Last authentication timestamp: legitimate interests, for detecting dormant
  accounts. Explicitly *not* used for performance management, and this
  limitation is stated in the works council agreement and enforced by
  restricting the field to the access review export.

## 4. Necessity and proportionality
- **Could we use less data?** The projection holds only fields needed to resolve
  a bundle and route an approval. Salary, contract type, absence and
  performance data were available in the HR feed and are deliberately not
  ingested. The feed is filtered at the source, not after ingestion.
- **Could retention be shorter?** The 90-day operational retention is set by the
  need to investigate provisioning disputes. The 7-year audit retention follows
  the statutory record-keeping period; shorter would not satisfy the audit
  finding that prompted the system.
- **Is the free-text justification necessary?** Yes — an approval without a
  reason does not satisfy the control. But it is the highest-risk field, since
  a manager could type anything. Mitigated in section 7.
- **Is the last-authentication timestamp proportionate?** It is the only
  practical way to find dormant accounts. Its use is contractually and
  technically limited to that purpose.

## 5. Consultation
DPO consulted twice; requested the free-text mitigation and the explicit
purpose limitation on the authentication timestamp, both adopted. The works
council was consulted over six weeks (2026-05-20 to 2026-07-01) and agreed,
conditional on the timestamp not being available to line managers and on
employees receiving a written explanation of the processing. Both conditions
are implemented.

## 6. Risks to individuals
| # | Risk to the individual | Likelihood | Severity | Overall |
|---|---|---|---|---|
| 1 | A manager records sensitive information (health, union membership) in a justification field, which is then retained 7 years with no erasure path | Possible | High | High |
| 2 | An employee is denied access they need because of an HR data error, and cannot get it corrected quickly | Possible | Medium | Medium |
| 3 | The authentication timestamp is repurposed for performance monitoring | Unlikely | High | Medium |
| 4 | Excess personal data reaches lower environments through a test data copy | Unlikely | High | Medium |
| 5 | An individual cannot find out what access they hold or why | Possible | Low | Low |

## 7. Measures
| Risk | Measure | Effect | Residual | Owner |
|---|---|---|---|---|
| 1 | Field labelled with a warning; guidance in manager training; excluded from operational logs and from the audit export sent to third parties; quarterly sampling of 50 entries by the DPO with deletion of any sensitive content found | Reduced, not eliminated — the field is free text by necessity | Low–Medium, accepted, reviewed quarterly | DPO |
| 2 | Errors are corrected in the HR system, which propagates within 5 minutes; People Ops can apply access immediately while the correction flows through; the process is documented in the employee-facing explanation | Reduced | Low | People Ops |
| 3 | Field exposed only in the access review export; not in any manager-facing view; works council agreement records the purpose limitation; access to the export is logged | Reduced | Low | Platform |
| 4 | Only anonymised copies reach lower environments; the anonymisation script is itself tested (TC-240) and a refresh is blocked if that test fails | Reduced | Low | QA |
| 5 | Self-service page showing an employee their current entitlements, the bundle that granted each, and the date | Reduced | Low | Platform |

## 8. Data subject rights
- **Access:** the self-service page covers current entitlements; a full audit
  history is available on request through the DPO.
- **Rectification:** flows from the HR system; the provisioning service is never
  edited directly, so there is one place to correct.
- **Erasure:** operational data is deleted 90 days after the leave date. Audit
  records are retained for 7 years on a legal-obligation basis, and erasure is
  refused for that period — this refusal is explained in the employee-facing
  notice rather than left to be discovered on request.
- **Objection:** legitimate-interests processing carries a right to object; an
  objection would in practice mean no system access, so it is handled as an
  HR conversation, not a technical setting.

## 9. Outcome
Residual risk is Low, except risk 1 at Low–Medium, accepted by the DPO on
2026-09-22 with quarterly sampling. Prior consultation with the supervisory
authority is not required, as no high residual risk remains after measures.
Review on material change or by 2027-09-22.
```

## Common mistakes

- **Written after the system is built.** A DPIA is a design input. Afterwards it can only document risk, not reduce it.
- **Risks to the organisation instead of to individuals.** "Reputational damage" is not the subject of a DPIA. What happens to the person is.
- **Necessity treated as a formality.** The question "could we do this with less data?" is the one that most often improves the design — the filtered HR feed above is a direct result of asking it.
- **Free-text fields not analysed.** They are the most common route for special-category data to enter a system that was designed not to hold any.
- **No review date.** Processing evolves; a DPIA describing a system from two years ago provides no protection.
- **Measures without owners.** An unowned measure is not implemented, and the assessment overstates how safe the processing is.

## Related templates

- [Data Model Document](/docs/architecture-design/data-model-document/) — the inventory this assessment draws on.
- [Risk Register](/docs/security-compliance/risk-register/) — where accepted privacy risk is tracked.
- [Vendor Security Assessment](/docs/security-compliance/vendor-security-assessment/) — needed when a processor is involved.
- [Information Security Policy](/docs/security-compliance/information-security-policy/) — the controls this assessment relies on.
