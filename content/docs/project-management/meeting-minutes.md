---
weight: 1050
title: "Meeting Minutes"
description: "Decisions and actions, captured in a form that survives the disagreement three months later."
icon: "groups"
date: "2026-08-23"
draft: false
---

Minutes are not a transcript. Their value is in two things a recording cannot give you: what was *decided*, and what someone committed to do by when. Everything else is optional context.

## When to use it

- Any meeting where a decision is made, money is committed, or scope changes.
- Governance meetings — steering, change advisory board, design review — where an audit trail is expected.
- Not for standups or informal syncs; a shared task board is cheaper.

## What it must answer

- Who was there, and who was invited but absent (absence matters when a decision binds them).
- What was decided, by whom, and on what basis.
- Which actions were accepted, by which named person, by which date.
- What was explicitly deferred, so it does not silently disappear.

## Template

{{< doctabs >}}
# <Meeting name> — YYYY-MM-DD

| Field | Value |
|---|---|
| Chair | |
| Minutes by | |
| Attendees | |
| Apologies | |
| Distribution | |

## Decisions
| # | Decision | Rationale | Decided by | Reversible? |
|---|---|---|---|---|

## Actions
| # | Action | Owner | Due | Status |
|---|---|---|---|---|

## Discussion notes
Brief, per agenda item. Record positions where people disagreed — not who
"lost", but what the competing arguments were.

## Deferred
| Item | Deferred until | Why |
|---|---|---|

## Next meeting
Date, and what must be ready beforehand.
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Payment Migration Steering — 2026-08-19

| Field | Value |
|---|---|
| Chair | R. Okafor (Sponsor) |
| Minutes by | S. Lindqvist |
| Attendees | R. Okafor, M. Duarte, A. Berg, S. Lindqvist, J. Marek |
| Apologies | P. Nowak (data) — represented by M. Duarte |
| Distribution | Attendees + programme mailbox |

## Decisions
| # | Decision | Rationale | Decided by | Reversible? |
|---|---|---|---|---|
| D-14 | Ramp starts at 5%, not the originally planned 10% | Auth-rate signal is statistically usable at 5% within 48h, and halves revenue exposure if the rate drops | R. Okafor | Yes — step size can be raised at the next gate |
| D-15 | Automatic rollback threshold set at 95.5% rolling auth rate over 30 minutes | 0.9pp below current baseline; below this the revenue loss exceeds the cost of a rollback | R. Okafor, on Finance's numbers | Yes, by steering only |
| D-16 | Dual-running extended to 8 weeks from 4 | Finance needs two full month-end cycles to trust the new reconciliation feed | M. Duarte | No — provider contract dates now assume it |

## Actions
| # | Action | Owner | Due | Status |
|---|---|---|---|---|
| A-31 | Confirm P. Nowak's allocation through September in writing | M. Duarte | 2026-08-28 | Open |
| A-32 | Implement 95.5% rollback trigger and prove it in a game day | J. Marek | 2026-09-11 | Open |
| A-33 | Re-forecast provider costs with 8-week dual-run | S. Lindqvist | 2026-09-02 | Open |

## Discussion notes
**Ramp size.** Engineering argued for 10% to reach statistical significance in
24h; Finance argued for 5% to cap exposure. Both accepted that 5% reaches
significance in 48h, which does not move M3. Decision D-14 taken on that basis.

**PCI scope.** Security has not completed the scope review (dependency D-01,
now 4 days late). A. Berg confirmed no new scope is expected but would not
sign before review completion. No decision taken.

## Deferred
| Item | Deferred until | Why |
|---|---|---|
| Bank transfer migration | FY2027 planning | Out of scope in the current charter; needs its own business case |
| Merchant fee repricing | After M4 | Depends on realised provider costs |

## Next meeting
2026-09-16. Required beforehand: PCI scope sign-off (D-01), rollback game day
result (A-32), revised cost forecast (A-33).
{{< /doctabs >}}

## Common mistakes

- **Actions without a named person.** "The team will investigate" is an action nobody has.
- **Recording only the outcome of a contested discussion.** Six months later, someone will re-open it. Two lines on the competing arguments prevent re-litigating from zero.
- **No "reversible?" marker on decisions.** Reversible decisions can be made quickly by one person; irreversible ones deserve the meeting's full attention. Marking them changes how the next one is handled.
- **Publishing days later.** Minutes lose most of their value after 48 hours; people have already acted on their own recollection.
- **Minuting everything.** If a meeting produces no decision and no action, the minutes should say exactly that — in one line.

## Related templates

- [Status Report](/docs/project-management/status-report/) — carries open decisions forward between meetings.
- [Architecture Decision Record](/docs/architecture-design/architecture-decision-record/) — for technical decisions that need a durable home outside minutes.
- [Change Request](/docs/operations-incident/change-request/) — the CAB equivalent of these minutes.
- [Project Management](/docs/project-management/) — the other four project-management templates.
