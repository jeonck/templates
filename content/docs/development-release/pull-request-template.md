---
weight: 4030
title: "Pull Request Template"
description: "The context a reviewer needs, collected before they start rather than asked for afterwards."
icon: "merge"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

A pull request description is written once and read by every reviewer, every future archaeologist, and whoever is bisecting an incident at 2am. The template's job is to make the author supply context they already have and would otherwise omit.

## When to use it

- Commit it as `.github/pull_request_template.md` (or the equivalent) in any repository with more than one contributor.
- Keep separate short templates for chores and docs if the full one causes people to delete it wholesale.

## What it must answer

- What changed, and why is that the right change?
- How do I know it works?
- What is the risk, and how do we back it out?
- What does the reviewer need to look at hardest?

## Template

```markdown
## What
One or two sentences. What behaviour changes for a user or a caller.

## Why
Link the story, incident or ADR. If there is no link, explain the trigger.

## How
The approach, and anything non-obvious about it. Skip if the diff is
self-explanatory.

## Testing
- [ ] Unit tests added or updated
- [ ] Integration/contract tests
- [ ] Manually verified: <what, in which environment>

## Risk and rollback
- Blast radius if this is wrong:
- Feature flag:
- Rollback procedure:
- Migration reversible? yes / no / n/a

## Checklist
- [ ] No secrets, tokens or personal data added
- [ ] Observability: metric/alert for any new failure mode
- [ ] Docs, runbook or API spec updated
- [ ] Breaking change? If yes, note it here and in the release notes

## Reviewer notes
Where to look first, and anything you are unsure about.

## Screenshots / output
For UI or CLI changes.
```

## Worked example

```markdown
## What
Provisioning requests now pin the bundle version at creation time. A bundle
edited after a request is created no longer changes what that request applies.

## Why
ADR-0012, driven by audit finding 2025-11: every grant must trace to exactly
one rule version. Story AP-127.

## How
`request.bundle_version` is written at creation and read at application time.
Bundle rows become immutable — `UPDATE` is revoked at the database role level
and edits create a new version row. `reResolve()` is the only way to change a
pending request's pinned version, and it writes an audit record with the old
and new version plus the operator's justification.

## Testing
- [x] Unit tests: table-driven over all 8 state transitions, plus the
      missing-pinned-version error case
- [x] Contract tests unchanged and green
- [x] Manually verified in staging: created a request, edited the bundle,
      confirmed the applied entitlements matched the pinned version and that
      the audit record showed `eng-3@17` not `eng-3@18`

## Risk and rollback
- Blast radius: all provisioning requests. Wrong behaviour means wrong access
  granted, which is a security-relevant defect, not a cosmetic one.
- Feature flag: none — the pin is a data property, not a code path. Flagging it
  would create two grant semantics simultaneously, which is worse.
- Rollback: revert the code. The `bundle_version` column stays and is ignored
  by the previous release.
- Migration reversible? Yes. Step 1 of 2 — column added nullable here, made
  NOT NULL in the next release after backfill.

## Checklist
- [x] No secrets or personal data added
- [x] Metric `grants_with_missing_bundle_version` added, alerts at > 0
- [x] Data model document and ADR-0012 updated
- [ ] Breaking change? No — additive for API consumers

## Reviewer notes
Look hardest at `bundles.go:80-110`. An earlier draft fell back to the latest
version when the pinned row was missing, which quietly defeats the whole point;
it now errors. I would like a second opinion on whether `re-resolve` should be
allowed while a request is APPLYING — currently it is not, and I think that is
right, but it is a judgement call.
```

## Common mistakes

- **A description that repeats the diff.** "Added a function to resolve bundles" is visible in the diff. Why, and what could go wrong, are not.
- **No link to a story, incident or decision.** In eighteen months, the link is the only way back to the reasoning.
- **A checklist that is always fully ticked.** If nobody ever leaves a box unticked, the checklist has stopped carrying information.
- **Rollback left blank.** For anything touching data or shared state, this is the section the on-call engineer will need.
- **A template so long that people delete it.** Aim for something an author can complete honestly in five minutes.

## Related templates

- [Code Review Checklist](/docs/development-release/code-review-checklist/) — the reviewer's side of the same conversation.
- [Coding Standards](/docs/development-release/coding-standards/) — what CI enforces so this stays short.
- [Release Notes](/docs/development-release/release-notes/) — breaking changes flagged here end up there.
- [Development & Release](/docs/development-release/) — the other four development and release templates.
