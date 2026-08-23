---
weight: 7040
title: "Vendor Security Assessment"
description: "Due diligence on a third party, scaled to what they will actually hold and do."
icon: "handshake"
date: "2026-08-23"
draft: false
---

Vendor assessment goes wrong in two directions: a 300-question form sent to a vendor selling a static website, or a rubber stamp for one processing customer records. Tier the assessment by data and access, and spend the effort where the exposure is.

## When to use it

- Before contracting any supplier that will hold company or customer data, connect to internal systems, or provide a service whose failure would be an incident.
- On renewal, and whenever the vendor's scope changes materially.
- After a publicly disclosed breach at the vendor.

## What it must answer

- What data and access will this vendor have, and what happens if they are breached?
- What assurance do they provide, and what did we actually verify rather than accept?
- What do we require contractually?
- What residual risk are we accepting, and who accepted it?

## Template

{{< doctabs >}}
# Vendor Security Assessment: <Vendor> — <service>

| Field | Value |
|---|---|
| Assessment date | |
| Assessor | |
| Business owner | |
| Tier | 1 (critical) / 2 / 3 (low) |
| Decision | Approve / Approve with conditions / Reject |


## 1. Service description
What they do for us, and what we could not do without them.

## 2. Data and access scope
| Data category | Volume | Classification | Personal data? | Purpose |
|---|---|---|---|---|


| Access granted | Type | Justification |
|---|---|---|


## 3. Tiering
The criteria that put this vendor in its tier.

## 4. Assurance reviewed
| Evidence | Provided? | Date | Reviewed by | Notes |
|---|---|---|---|---|


## 5. Control assessment
| Domain | Finding | Rating | Evidence |
|---|---|---|---|


## 6. Concentration and exit
Dependency, lock-in, exit plan, data return and deletion.

## 7. Contractual requirements
| Requirement | In contract? | Clause |
|---|---|---|


## 8. Findings and conditions
| # | Finding | Severity | Required action | Owner | Due |
|---|---|---|---|---|---|


## 9. Residual risk and decision
| Risk | Rating | Accepted by | Date | Review date |
|---|---|---|---|---|
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Vendor Security Assessment: NorthPay — card payment processing

| Field | Value |
|---|---|
| Assessment date | 2026-04-28 |
| Assessor | A. Berg (Security) |
| Business owner | M. Duarte (Finance) |
| Tier | 1 — critical |
| Decision | Approve with conditions |


## 1. Service description
Processes all card payments for web and mobile. An outage stops revenue
immediately; a breach exposes cardholder data and triggers regulatory
notification. There is no manual fallback.

## 2. Data and access scope
| Data category | Volume | Classification | Personal data? | Purpose |
|---|---|---|---|---|
| Cardholder data (PAN, expiry) | ~2.1M transactions/yr | Restricted | Yes | Payment authorisation |
| Customer name and billing address | ~2.1M/yr | Confidential | Yes | Fraud screening, AVS |
| Transaction metadata | ~2.1M/yr | Internal | Indirectly | Reconciliation |


Access granted: outbound API calls from our systems to theirs; a webhook
endpoint they call, restricted by mutual TLS and IP allow-list; no access to
our internal networks or data stores.

## 3. Tiering
Tier 1 on three independent criteria: processes restricted data at scale,
outage is immediately revenue-affecting, and there is no rapid alternative
provider.

## 4. Assurance reviewed
| Evidence | Provided? | Date | Reviewed by | Notes |
|---|---|---|---|---|
| PCI DSS Attestation of Compliance (Level 1) | Yes | 2026-02-14 | A. Berg | Valid; scope covers the services we use. Verified against the card scheme's public registry rather than accepting the PDF |
| SOC 2 Type II | Yes | 2026-01-31 | A. Berg | Two exceptions noted by the auditor: delayed access revocation and one incomplete change record. Both remediated per management response |
| Penetration test summary | Yes | 2025-11 | A. Berg | Summary only, no findings detail. Requested full report — refused; standard for this vendor |
| ISO 27001 certificate | Yes | 2026-03 | A. Berg | Verified with the certification body |
| Business continuity plan | Partial | 2026-04 | A. Berg | Summary only. RTO stated as 4 hours; last exercise date not disclosed |
| Sub-processor list | Yes | 2026-04 | DPO | 7 sub-processors, 2 outside the EEA with standard contractual clauses in place |


## 5. Control assessment
| Domain | Finding | Rating | Evidence |
|---|---|---|---|
| Access control | MFA enforced; privileged access reviewed quarterly | Satisfactory | SOC 2 |
| Encryption | TLS 1.2+ in transit, AES-256 at rest, HSM-backed keys | Satisfactory | PCI AoC |
| Incident response | 24/7 team; contractual notification within 24h of confirmed breach | Satisfactory | Contract + SOC 2 |
| Change management | One incomplete change record in the SOC 2 period | Minor concern | SOC 2 exception 2 |
| Business continuity | RTO 4h claimed; no exercise evidence provided | Concern | Gap |
| Sub-processor management | Notification of new sub-processors, but only 30 days' notice with no right to object | Concern | Contract review |


## 6. Concentration and exit
Single provider for all card traffic. Exit would take an estimated 6–9 months
based on the incoming migration, which is itself a 9-month project. Contract
requires data return in a documented format within 30 days of termination and
deletion within 90, with certification of deletion. Mitigation: we retain our
own transaction ledger independently, so exit does not depend on their export.

## 7. Contractual requirements
| Requirement | In contract? | Clause |
|---|---|---|
| Breach notification within 24h | Yes | 11.3 |
| Right to audit or receive annual SOC 2 | Yes (report, not audit right) | 12.1 |
| Sub-processor notification | Yes, 30 days | 8.4 |
| Right to object to a sub-processor | No | — |
| Data return and certified deletion | Yes | 15.2 |
| Liability cap | 12 months' fees | 18.1 — below our EUR 5M standard for Tier 1 |


## 8. Findings and conditions
| # | Finding | Severity | Required action | Owner | Due |
|---|---|---|---|---|---|
| 1 | No right to object to new sub-processors | Medium | Negotiate an objection right with termination for cause | M. Duarte | Before signature |
| 2 | Liability cap below policy for Tier 1 | Medium | Escalate to Legal; accept or negotiate | M. Duarte | Before signature |
| 3 | No BCP exercise evidence | Medium | Request the most recent exercise report annually; treat non-provision as a finding at renewal | A. Berg | Annually |
| 4 | Pen test detail not disclosed | Low | Accept — consistent with the market; the PCI AoC provides independent coverage | A. Berg | — |


## 9. Residual risk and decision
| Risk | Rating | Accepted by | Date | Review date |
|---|---|---|---|---|
| Concentration: no rapid alternative provider | High | Executive Committee | 2026-05-06 | 2027-05 |
| Liability cap below policy | Medium | CFO | 2026-05-06 | At renewal |
| Unverified BCP capability | Medium | CISO | 2026-05-06 | 2027-04 |


Approved with conditions 1 and 2 resolved before signature. Condition 1 was
agreed by the vendor on 2026-05-02 (60 days' notice with an objection right);
condition 2 was accepted as-is by the CFO, with the concentration risk recorded
in the register as R-2026-008.
{{< /doctabs >}}

## Common mistakes

- **The same questionnaire for every vendor.** Tier by data and access. Effort spent on a low-tier vendor is effort not spent on the one holding cardholder data.
- **Accepting certificates without verification.** A PDF is not evidence. Check the certification body's or scheme's registry, and check that the scope covers the service you are buying.
- **Ignoring the auditor's exceptions in a SOC 2.** The exceptions section is the most informative part of the report and is routinely skipped.
- **No exit assessment.** Concentration risk is usually the largest exposure, and it is invisible if you only assess controls.
- **Findings without contract dates.** A finding that is not resolved before signature will not be resolved after it.
- **Assessed once, never again.** Vendors change scope, get acquired and get breached. Reassess at renewal and on material change.

## Related templates

- [Risk Register](/docs/security-compliance/risk-register/) — where residual vendor risk is recorded.
- [Information Security Policy](/docs/security-compliance/information-security-policy/) — the third-party requirements this assesses against.
- [Data Protection Impact Assessment](/docs/security-compliance/data-protection-impact-assessment/) — needed when the vendor processes personal data at scale.
- [Business Requirements Document](/docs/requirements/business-requirements-document/) — the build-or-buy decision this informs.
- [Access Review](/docs/security-compliance/access-review/) — recertifying the accounts a supplier holds, once they are onboarded.
- [Security & Compliance](/docs/security-compliance/) — the other four security and compliance templates.
