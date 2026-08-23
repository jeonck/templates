---
weight: 1040
title: "RAID Log"
description: "One table for Risks, Assumptions, Issues and Dependencies — the project's short-term memory."
icon: "warning"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

RAID stands for Risks, Assumptions, Issues, Dependencies. Keeping all four in one place works because they convert into each other: an assumption that fails becomes an issue, a dependency that slips becomes a risk. A log that only tracks risks loses those transitions.

## When to use it

- From project kickoff to closure, reviewed at every status cycle.
- As the standing input to the risk section of the [Status Report](/docs/project-management/status-report/).
- At closure, to hand open items to the operational owner rather than deleting them.

## What it must answer

| Type | The question it answers |
|---|---|
| Risk | What might happen, how likely, how bad, and what are we doing about it *now*? |
| Assumption | What are we treating as true without proof, and when will we know? |
| Issue | What has already gone wrong, who owns it, by when? |
| Dependency | What do we need from outside the team, by when, and who do we escalate to? |

## Template

{{< tabs tabTotal="2" >}}
{{% tab tabName="Rendered" %}}

**RAID Log: &lt;Project&gt;**

Last reviewed: YYYY-MM-DD by &lt;name&gt;  

**Risks**

| ID | Risk (if X then Y) | Prob (H/M/L) | Impact (H/M/L) | Score | Response | Mitigation / owner | Review date | Status |
|---|---|---|---|---|---|---|---|---|

Response is one of: avoid, reduce, transfer, accept.  

**Assumptions**

| ID | Assumption | Made by | Validate by | Consequence if false | Status |
|---|---|---|---|---|---|

**Issues**

| ID | Issue | Raised | Severity | Owner | Action | Due | Status |
|---|---|---|---|---|---|---|---|

**Dependencies**

| ID | We need | From | By when | Escalation | Status |
|---|---|---|---|---|---|

**Closed items**

Keep them; do not delete. Closure date and outcome.

{{% /tab %}}
{{% tab tabName="Markdown" %}}

```markdown
# RAID Log: <Project>

Last reviewed: YYYY-MM-DD by <name>

## Risks
| ID | Risk (if X then Y) | Prob (H/M/L) | Impact (H/M/L) | Score | Response | Mitigation / owner | Review date | Status |
|---|---|---|---|---|---|---|---|---|

Response is one of: avoid, reduce, transfer, accept.

## Assumptions
| ID | Assumption | Made by | Validate by | Consequence if false | Status |
|---|---|---|---|---|---|

## Issues
| ID | Issue | Raised | Severity | Owner | Action | Due | Status |
|---|---|---|---|---|---|---|---|

## Dependencies
| ID | We need | From | By when | Escalation | Status |
|---|---|---|---|---|---|

## Closed items
Keep them; do not delete. Closure date and outcome.
```

{{% /tab %}}
{{< /tabs >}}

## Worked example

{{< tabs tabTotal="2" >}}
{{% tab tabName="Rendered" %}}

**RAID Log: Payment Gateway Migration**

Last reviewed: 2026-08-21 by S. Lindqvist  

**Risks**

| ID | Risk | Prob | Impact | Score | Response | Mitigation / owner | Review | Status |
|---|---|---|---|---|---|---|---|---|
| R-04 | If the new provider's auth rate is lower than the incumbent's, then card revenue drops during the ramp | M | H | 6 | Reduce | Automatic rollback if rolling auth rate < 95.5% over 30 min — J. Marek, implemented 2026-08-19 | 2026-09-04 | Open |
| R-07 | If Reporting reclaims P. Nowak, then the reconciliation feed slips 3 weeks and M4 moves | H | M | 6 | Avoid | Sponsor to confirm allocation through Sept — S. Lindqvist | 2026-08-28 | Open, escalated |
| R-11 | If PSD2 challenge flows differ, then checkout needs redesign mid-project | L | H | 3 | Reduce | Spike completed 2026-06-12; flows are compatible for 97% of cases | 2026-09-30 | Open, downgraded |

**Assumptions**

| ID | Assumption | Made by | Validate by | Consequence if false | Status |
|---|---|---|---|---|---|
| A-01 | Finance can process two reconciliation feeds during dual-running | S. Lindqvist | 2026-09-02 (UAT) | Dual-running impossible; big-bang cutover with far higher risk | Open |
| A-03 | Sandbox behaviour matches production for 3DS | A. Vogel | 2026-09-30 (5% ramp) | Test coverage is illusory; defects appear in live traffic | Open |
| A-05 | Incumbent will not charge early-termination fees | M. Duarte | 2026-09-15 | Business case loses EUR 120k of benefit | Validated 2026-08-11 — no fee. Closed |

**Issues**

| ID | Issue | Raised | Severity | Owner | Action | Due | Status |
|---|---|---|---|---|---|---|---|
| I-05 | Reconciliation UAT cannot run during Finance month-end close | 2026-08-14 | Medium | P. Nowak | Move UAT to 2026-09-02; confirm no knock-on to M3 | 2026-08-25 | Open |
| I-02 | Sandbox rate limits block full-suite nightly runs | 2026-07-22 | Medium | H. Ito | Provider raised limit to 50 rps | 2026-08-18 | Closed |

**Dependencies**

| ID | We need | From | By when | Escalation | Status |
|---|---|---|---|---|---|
| D-01 | PCI scope sign-off | Internal security | 2026-08-15 | A. Berg -> CISO | Late — in review, chased 2026-08-20 |
| D-03 | Dual-feed capacity confirmation | Finance systems | 2026-08-31 | M. Duarte | On track |

{{% /tab %}}
{{% tab tabName="Markdown" %}}

```markdown
# RAID Log: Payment Gateway Migration
Last reviewed: 2026-08-21 by S. Lindqvist

## Risks
| ID | Risk | Prob | Impact | Score | Response | Mitigation / owner | Review | Status |
|---|---|---|---|---|---|---|---|---|
| R-04 | If the new provider's auth rate is lower than the incumbent's, then card revenue drops during the ramp | M | H | 6 | Reduce | Automatic rollback if rolling auth rate < 95.5% over 30 min — J. Marek, implemented 2026-08-19 | 2026-09-04 | Open |
| R-07 | If Reporting reclaims P. Nowak, then the reconciliation feed slips 3 weeks and M4 moves | H | M | 6 | Avoid | Sponsor to confirm allocation through Sept — S. Lindqvist | 2026-08-28 | Open, escalated |
| R-11 | If PSD2 challenge flows differ, then checkout needs redesign mid-project | L | H | 3 | Reduce | Spike completed 2026-06-12; flows are compatible for 97% of cases | 2026-09-30 | Open, downgraded |

## Assumptions
| ID | Assumption | Made by | Validate by | Consequence if false | Status |
|---|---|---|---|---|---|
| A-01 | Finance can process two reconciliation feeds during dual-running | S. Lindqvist | 2026-09-02 (UAT) | Dual-running impossible; big-bang cutover with far higher risk | Open |
| A-03 | Sandbox behaviour matches production for 3DS | A. Vogel | 2026-09-30 (5% ramp) | Test coverage is illusory; defects appear in live traffic | Open |
| A-05 | Incumbent will not charge early-termination fees | M. Duarte | 2026-09-15 | Business case loses EUR 120k of benefit | Validated 2026-08-11 — no fee. Closed |

## Issues
| ID | Issue | Raised | Severity | Owner | Action | Due | Status |
|---|---|---|---|---|---|---|---|
| I-05 | Reconciliation UAT cannot run during Finance month-end close | 2026-08-14 | Medium | P. Nowak | Move UAT to 2026-09-02; confirm no knock-on to M3 | 2026-08-25 | Open |
| I-02 | Sandbox rate limits block full-suite nightly runs | 2026-07-22 | Medium | H. Ito | Provider raised limit to 50 rps | 2026-08-18 | Closed |

## Dependencies
| ID | We need | From | By when | Escalation | Status |
|---|---|---|---|---|---|
| D-01 | PCI scope sign-off | Internal security | 2026-08-15 | A. Berg -> CISO | Late — in review, chased 2026-08-20 |
| D-03 | Dual-feed capacity confirmation | Finance systems | 2026-08-31 | M. Duarte | On track |
```

{{% /tab %}}
{{< /tabs >}}

## Common mistakes

- **Risks written as topics, not sentences.** "Security" is not a risk. "If the PCI review finds the ramp expands scope, then cutover is blocked for 6 weeks" is — it names cause, effect and magnitude.
- **Mitigations that are plans to plan.** "Monitor closely" is not a mitigation. A mitigation has an owner and a completion date.
- **No review date.** Risks that are never re-scored drift into fiction; a stale log gets ignored wholesale.
- **Assumptions never validated.** Every assumption needs a date by which it becomes a fact or an issue.
- **Deleting closed items.** The closed section is the evidence trail for the [Postmortem](/docs/operations-incident/postmortem/) and for audit.

## Related templates

- [Status Report](/docs/project-management/status-report/) — reports the deltas in this log.
- [Project Plan](/docs/project-management/project-plan/) — dependencies here should match section 6 there.
- [Risk Register](/docs/security-compliance/risk-register/) — the organisation-level equivalent for security risk.
- [Project Management](/docs/project-management/) — the other four project-management templates.
