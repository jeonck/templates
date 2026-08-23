---
weight: 7020
title: "Risk Register"
description: "Standing organisational risks with owners, treatment decisions, and dated reviews."
icon: "crisis_alert"
date: "2026-08-23"
draft: false
---

A risk register differs from a project [RAID Log](/docs/project-management/raid-log/) in lifespan and audience: these risks outlive projects, and the entries are decisions by named accountable people, not a team's working notes. The register's value comes entirely from being reviewed — an unreviewed register is a list of old opinions.

## When to use it

- As the standing record for security, privacy, operational and compliance risk.
- As the home for policy exceptions and accepted risks, with expiry dates.
- Wherever an auditor will ask "who accepted this, when, and on what basis?"

## What it must answer

- What is the risk, in cause-and-effect terms?
- What is the current exposure, after existing controls?
- What are we doing about it, by when, and who owns that?
- Who accepted the residual risk, and when is it re-examined?

## Template

{{< doctabs >}}
# Risk Register: <Organisation or domain>

| Field | Value |
|---|---|
| Owner | |
| Review cycle | |
| Last reviewed | |


## Scoring
State the likelihood and impact scales, and the tolerance thresholds. Do not
assume they are obvious.

## Register
| ID | Risk (cause -> event -> consequence) | Category | Inherent L/I | Existing controls | Residual L/I | Treatment | Owner | Action / due | Accepted by | Review date | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|


Treatment: mitigate, transfer, avoid, accept.

## Accepted risks and policy exceptions
| ID | Exception to | Compensating control | Accepted by | Expires |
|---|---|---|---|---|


## Movement since last review
New, escalated, de-escalated, closed.
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Risk Register: Identity and Access (extract)

Owner: CISO. Review cycle: quarterly, next 2027-01-20. Last reviewed 2026-10-21.

## Scoring
Likelihood: 1 rare (< once in 5 years), 2 unlikely, 3 possible (once a year),
4 likely (quarterly), 5 almost certain (monthly).
Impact: 1 negligible, 2 minor, 3 moderate (reportable internally), 4 major
(regulatory notification or > EUR 250k), 5 severe (material to the business).
Score = L x I. Tolerance: score >= 12 requires Executive Committee acceptance;
9–11 requires CISO acceptance; <= 8 may be accepted by the system owner.

## Register
| ID | Risk | Category | Inherent | Controls | Residual | Treatment | Owner | Action / due | Accepted by | Review | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R-2026-011 | Legacy ERP revokes access only on a nightly batch, so a dismissed employee retains ERP access for up to 26 hours, during which they could export customer data | Access | 3 x 4 = 12 | Daily exception report; ERP access is read-only for 90% of roles; termination-day physical and VPN revocation is immediate | 2 x 4 = 8 | Mitigate, then avoid | Head of IT | ERP replacement in FY2027 (BUD-2027-04); until then the exception report is reviewed by 09:00 daily | CISO (EX-2026-014) | 2027-06-30 | Open |
| R-2026-018 | Alert routing configuration can reference deleted destinations, so a security-relevant alert may never be delivered | Detection | 4 x 3 = 12 | CI check that every alert route resolves (added 2026-12-10); fallback route on every PagerDuty service | 2 x 3 = 6 | Mitigate | Platform lead | Complete. Quarterly verification added to the ops calendar | CISO | 2027-01-20 | Closed 2026-12-19 |
| R-2026-022 | Free-text justification fields let a user enter personal or special-category data that then falls under a 7-year audit retention with no erasure path | Privacy | 3 x 3 = 9 | UI warning; field excluded from log export; DPIA documents the retention basis | 2 x 3 = 6 | Accept | DPO | Quarterly sampling of 50 justification entries for sensitive content | DPO | 2027-01-20 | Open |
| R-2026-027 | A single-leader poller with no liveness signal can stall silently, delaying provisioning and (in a leaver window) delaying revocation beyond policy | Availability / Access | 3 x 3 = 9 | Heartbeat alert (OPS-882); hourly synthetic provisioning check (OPS-885); backlog alert | 2 x 3 = 6 | Mitigate | Platform lead | OPS-885 due 2027-01-16 | CISO | 2027-01-20 | Open, on track |
| R-2026-031 | Growth in direct third-party dependencies raises the chance of a compromised package reaching production | Supply chain | 4 x 4 = 16 | Dependency scanning gating CI on High/Critical; new dependencies require maintainer approval; lockfiles pinned | 3 x 4 = 12 | Mitigate | Engineering director | Build provenance attestation and artefact signing, due 2027-03-31 | Executive Committee | 2027-01-20 | Open, above tolerance |


## Accepted risks and policy exceptions
| ID | Exception to | Compensating control | Accepted by | Expires |
|---|---|---|---|---|
| EX-2026-014 | AC-03 (revocation within 24h) for the legacy ERP | Daily exception report reviewed by People Ops by 09:00 | CISO | 2027-06-30 |
| EX-2026-019 | LM-03 (no personal data in operational logs) for the legacy ERP's own logs, which we do not control | Log access restricted to 4 named administrators; 30-day retention | CISO | 2027-06-30 |


## Movement since last review
- New: R-2026-031 (supply chain) raised after an industry incident; above
  tolerance and therefore accepted at Executive Committee, not by the CISO.
- De-escalated: R-2026-018 residual from 12 to 6 after the CI check landed;
  closed on verification.
- Unchanged: R-2026-011. The FY2027 budget line is approved but the project has
  not started; if it slips past Q3 the exception must be re-approved rather
  than extended silently.
{{< /doctabs >}}

## Common mistakes

- **No scoring scale.** "High" means different things to different people, and scores stop being comparable across entries.
- **Risks as one-word topics.** "Supply chain" is a category. The cause-event-consequence sentence is what makes exposure assessable.
- **Inherent score only.** What matters for a decision is the residual risk after existing controls — and stating both shows what the controls are actually buying.
- **Acceptance by the wrong level.** A risk above tolerance accepted by a team lead is an audit finding waiting to happen. Match the acceptor to the score.
- **Exceptions that get extended rather than re-approved.** Silent extension is how a temporary compensating control becomes permanent and unexamined.
- **Reviewed annually.** Anything reviewed less often than quarterly drifts out of date and stops informing decisions.

## Related templates

- [Information Security Policy](/docs/security-compliance/information-security-policy/) — the statements exceptions are granted against.
- [RAID Log](/docs/project-management/raid-log/) — the project-level equivalent.
- [Postmortem](/docs/operations-incident/postmortem/) — a common source of new entries.
- [Vendor Security Assessment](/docs/security-compliance/vendor-security-assessment/) — third-party risks land here.
- [Security & Compliance](/docs/security-compliance/) — the other four security and compliance templates.
