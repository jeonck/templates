---
weight: 7010
title: "Information Security Policy"
description: "Mandatory rules with named owners, written so people can actually comply with them."
icon: "policy"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

A security policy states what must be true. It is not a standard (how), a procedure (steps), or a guideline (advice) — mixing those is why most policies are long, unread and unenforceable. Keep the policy short and put the detail in documents that can change without a board approval cycle.

## When to use it

- When certification (ISO 27001, SOC 2) or a customer contract requires documented policy.
- When a control needs to be mandatory and auditable rather than a team preference.
- Not for anything you are unwilling to enforce. An unenforced policy is worse than none: it is a documented control failure.

## What it must answer

- Who does this apply to, and what must they do?
- Who owns each rule, and how is compliance measured?
- What happens when someone cannot comply?
- When is it reviewed, and by whom?

## Template

{{< doctabs >}}
# <Organisation> Information Security Policy

| Field | Value |
|---|---|
| Version / effective date | |
| Owner | |
| Approved by | |
| Review cycle | |
| Applies to | |

## 1. Purpose and scope
Who and what is covered, including contractors and third parties.

## 2. Roles and responsibilities
| Role | Responsibility |
|---|---|

## 3. Policy statements
Each statement: mandatory, testable, owned.

### 3.1 <Domain>
| ID | Statement | Owner | Evidence of compliance |
|---|---|---|---|

Domains to cover: access control, authentication, data classification and
handling, cryptography, secure development, change management, logging and
monitoring, vulnerability management, third parties, incident response,
business continuity, physical, acceptable use.

## 4. Exceptions
Request, approve, time-limit, review.

## 5. Non-compliance
Consequences, stated plainly.

## 6. Related documents
Standards and procedures that implement this policy.

## 7. Review history
| Version | Date | Change | Approver |
|---|---|---|---|
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Information Security Policy (extract)

| Field | Value |
|---|---|
| Version / effective date | 4.1 / 2026-07-01 |
| Owner | CISO |
| Approved by | Executive Committee, 2026-06-24 |
| Review cycle | Annual, or on material change |
| Applies to | All employees, contractors and third parties with access to company systems or data |

## 3.1 Access control
| ID | Statement | Owner | Evidence |
|---|---|---|---|
| AC-01 | Access is granted on the principle of least privilege, based on a documented role | Head of IT | Bundle definitions in the provisioning service; quarterly access review records |
| AC-02 | Access outside a documented role requires approval by the individual's line manager before it is granted | Head of IT | Audit log entries showing approver, timestamp and justification |
| AC-03 | Access is revoked within 24 hours of an individual's leave date | Head of IT | Daily exception report; quarterly sampling by Internal Audit |
| AC-04 | Privileged accounts are individually attributable; shared administrative credentials are prohibited | Head of IT | Account inventory; no accounts of type "shared" |
| AC-05 | Access rights are reviewed at least quarterly by the system owner | System owners | Signed review records retained 3 years |

## 3.2 Authentication
| ID | Statement | Owner | Evidence |
|---|---|---|---|
| AU-01 | Multi-factor authentication is required for all remote access and all administrative access | Head of IT | Identity platform configuration report |
| AU-02 | Service credentials are stored in the approved secrets manager and rotated at least every 90 days | Platform lead | Secrets manager age report; alert on any credential over 90 days |
| AU-03 | Credentials must not appear in source code, configuration files, logs, or ticketing systems | Engineering leads | Secret scanning in CI; findings tracked to closure |

## 3.6 Logging and monitoring
| ID | Statement | Owner | Evidence |
|---|---|---|---|
| LM-01 | Security-relevant events are logged with actor, timestamp, action and outcome | System owners | Log schema review per system |
| LM-02 | Security logs are retained for at least 12 months and are tamper-evident | Platform lead | Retention configuration; append-only storage settings |
| LM-03 | Personal data must not be written to operational logs | Engineering leads | Log sampling each quarter; findings tracked |

## 4. Exceptions
Exceptions are requested through the risk register, approved by the CISO for
Medium risk and by the Executive Committee for High. Every exception is
time-limited to a maximum of 12 months, names a compensating control, and is
reviewed at expiry. An expired exception is a policy violation.

Current example: legacy ERP cannot revoke access within 24 hours (AC-03) and
runs a nightly batch, giving a worst case of 26 hours. Exception EX-2026-014,
approved by the CISO 2026-10-30, expires 2027-06-30, compensating control is
a daily exception report reviewed by People Operations.

## 5. Non-compliance
Deliberate circumvention is a disciplinary matter. Inability to comply is not:
raise an exception. Teams that raise exceptions are not penalised — hidden
non-compliance is the failure mode this policy is designed to prevent.

## 6. Related documents
Access Control Standard; Secure Development Standard; Cryptographic Standard;
Incident Response Procedure; Data Classification Standard. Standards may be
updated by their owner without Executive Committee approval, provided they do
not weaken a policy statement.
{{< /doctabs >}}

## Common mistakes

- **Policy, standard and procedure in one document.** Then every implementation detail needs executive re-approval, so nothing gets updated.
- **Statements nobody can test.** "Systems shall be appropriately secured" cannot be audited and cannot be complied with. Every statement needs an evidence column.
- **No exception process.** Teams that cannot comply and cannot get an exception will simply not comply, invisibly.
- **Rules without owners.** An unowned control is an unimplemented control, and the auditor will find it before you do.
- **Copied from a template without adaptation.** A policy referencing systems you do not have signals to an auditor that nothing here reflects reality.

## Related templates

- [Risk Register](/docs/security-compliance/risk-register/) — where exceptions and accepted risks are recorded.
- [Access Review](/docs/security-compliance/access-review/) — evidence for AC-05.
- [Vendor Security Assessment](/docs/security-compliance/vendor-security-assessment/) — how third-party scope is assessed.
- [Data Protection Impact Assessment](/docs/security-compliance/data-protection-impact-assessment/) — for processing that carries privacy risk.
- [Security & Compliance](/docs/security-compliance/) — the other four security and compliance templates.
