---
weight: 3020
title: "Architecture Decision Record"
description: "One decision, its context, the options rejected, and what it costs — in under a page."
icon: "gavel"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

An ADR captures a single significant decision at the moment it is made, while the alternatives are still fresh and nobody yet knows how it turns out. Its purpose is to stop the same argument being had every eighteen months by people who lack the original context.

## When to use it

- Any decision that is expensive to reverse: a datastore, a protocol, a boundary, a vendor, an auth model.
- Any decision where a reasonable engineer would choose differently — that is exactly what needs recording.
- Not for reversible, local choices. If undoing it is an afternoon's work, skip it.

## What it must answer

- What forces were in play at the time, including the non-technical ones?
- What was chosen, stated in one sentence?
- What was rejected, and why — specifically enough that it is not re-proposed unchanged?
- What does this cost us, now and later?

## Template

```markdown
# ADR-<NNNN>: <Decision, phrased as a statement>

- **Status:** Proposed / Accepted / Superseded by ADR-XXXX / Deprecated
- **Date:** YYYY-MM-DD
- **Deciders:** names
- **Consulted:** names
- **Supersedes:** ADR-XXXX (if any)

## Context
The forces at play: requirements, constraints, deadlines, team skills, existing
commitments. Write what was true *then*; do not update this section later.

## Decision
One sentence in the active voice: "We will ...".
Then the detail needed to act on it.

## Options considered
### Option A — <name>
Pros / cons / why not chosen.

### Option B — <name>
...

## Consequences
**Positive:** ...
**Negative:** ...
**Neutral / follow-up work:** ...

## Compliance
How we will notice if this decision is being violated in practice.

## Notes
Links to spikes, benchmarks, discussions.
```

## Worked example

```markdown
# ADR-0012: In-flight provisioning requests keep the bundle version pinned at creation

- **Status:** Accepted
- **Date:** 2026-06-24
- **Deciders:** A. Vogel (architect), J. Marek (lead), K. Ferreira (People Ops)
- **Consulted:** L. Haddad (Internal Audit)

## Context
Access bundles map a job code to a set of entitlements, and People Ops edits
them directly (BR-04) — roughly twice a month, sometimes reactively after an
audit query. A provisioning request can live for weeks: requests are created
when the HR record appears, but entitlements are applied one working day before
the start date.

That means a bundle can change between request creation and application. Audit
requires that we can state, for any grant, which rule produced it (D1). Two
readings of "the correct entitlements" were in conflict: the bundle as it was
when the request was made, or as it is when access is granted.

Postgres row versioning was already in place for bundles; neither option
required new infrastructure.

## Decision
We will pin the bundle version onto the provisioning request at creation time,
and apply that pinned version even if the bundle has since changed.

A People Ops user may explicitly re-resolve a pending request against the
current bundle; this is an auditable action requiring a justification.

## Options considered

### Option A — Pin at creation (chosen)
Every grant traces to exactly one immutable bundle version. The audit answer is
a single row lookup. Cost: a bundle fix does not automatically reach the 30-odd
requests already pending, so a genuine correction needs an explicit re-resolve.

### Option B — Resolve at application time
Always applies the latest thinking, and corrections propagate automatically.
Rejected because the audit trail becomes ambiguous: a grant made at 06:00 and
one at 06:10 could differ with no visible cause, and reconstructing the reason
requires joining against bundle history by timestamp. Internal Audit stated
this would not satisfy the finding.

### Option C — Pin, but auto-re-resolve when the bundle changes
Rejected as the worst of both: the pin exists but is silently broken, so the
recorded version is not necessarily the one applied. Any implementation bug
here produces exactly the class of untraceable grant we are trying to remove.

## Consequences
**Positive**
- One row answers "which rule granted this?" — meets D1 directly.
- Bundle edits are safe to make at any time; they cannot retroactively alter
  what a pending request will do.

**Negative**
- Removing a wrongly-included entitlement requires re-resolving pending
  requests. Worst case observed in the September intake: 90 requests.
- People Ops needs a UI affordance to find and re-resolve pending requests,
  which is extra work (story AP-131).

**Neutral / follow-up**
- Bundle rows become immutable; edits create a new version. Storage growth is
  negligible (tens of rows per year).
- The re-resolve action must appear in the audit log with a justification.

## Compliance
A weekly check asserts that every grant record references a bundle version that
exists and is marked immutable. Any grant referencing a mutable or missing
bundle version alerts to the platform team.

## Notes
Spike results and the audit conversation are in the 2026-06-19 design review
minutes. This decision drove the state machine change recorded in the
technical design.
```

## Common mistakes

- **Editing the context after the fact.** An ADR is a historical record. If the situation changes, write a new ADR that supersedes it; never rewrite the old one.
- **Options listed without reasons.** "We considered X" adds nothing. Why X was worse *given the context of the time* is the entire value.
- **No negative consequences.** Every real decision costs something. An ADR with only benefits is marketing, and readers discount the whole document.
- **ADRs for everything.** Twenty ADRs a month means nobody reads any of them. Reserve them for decisions that are expensive to reverse.
- **Stored outside the repository.** ADRs in a wiki drift away from the code. Keep them in `docs/adr/` next to what they govern.

## Related templates

- [Solution Architecture Document](/docs/architecture-design/solution-architecture-document/) — references ADRs instead of restating decisions.
- [Technical Design Document](/docs/architecture-design/technical-design-document/) — where an accepted ADR gets implemented.
- [Meeting Minutes](/docs/project-management/meeting-minutes/) — decisions made in governance meetings that deserve an ADR.
