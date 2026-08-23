---
weight: 4020
title: "Code Review Checklist"
description: "What a human should look for once linters, tests and scanners have had their turn."
icon: "reviews"
date: "2026-08-23"
draft: false
---

Automation catches formatting, obvious bugs and known vulnerabilities. A human reviewer's scarce attention should go to correctness under conditions the tests do not cover, to blast radius, and to whether the change matches the problem it claims to solve.

## When to use it

- As a reference for reviewers, especially new ones — it makes review quality less dependent on who is available.
- As the basis for a repository's review guidance in `CONTRIBUTING.md`.
- Not as a form to complete on every change. A three-line config fix does not need eleven checks.

## What it must answer

- Does this change do what its description says, and only that?
- What happens when it fails, retries, runs twice, or runs with production data volumes?
- Can it be deployed and rolled back safely?
- Will someone understand it in a year?

## Template

{{< doctabs >}}
# Code Review Checklist

## Before reviewing
- [ ] CI is green — do not review red pull requests
- [ ] The description explains the *why*, and links a story or issue
- [ ] The change is small enough to review properly (target < 400 lines)

## Correctness
- [ ] The change does what the description claims — no unrelated changes
- [ ] Edge cases: empty, one, many, maximum, null, duplicate
- [ ] Error paths return or propagate; nothing is silently swallowed
- [ ] Idempotent where it can be retried or replayed
- [ ] Concurrency: shared state, ordering assumptions, transaction boundaries

## Data
- [ ] Migrations are backwards compatible for the deploy window
- [ ] Migration is reversible, or the irreversibility is called out
- [ ] Query plans checked for anything touching a large table
- [ ] No unbounded result set or unbounded memory growth

## Security
- [ ] Authorisation checked at the right layer, for every new path
- [ ] Input validated at the trust boundary
- [ ] No secrets, tokens or personal data in code, logs or tests
- [ ] New dependency justified and licence-compatible

## Operability
- [ ] Metric or alert for the new failure mode
- [ ] Log lines carry correlation identifiers, and nothing sensitive
- [ ] Feature flag or another way to disable it without a deploy
- [ ] Runbook updated if operational behaviour changed

## Tests
- [ ] A failing test existed first, for a bug fix
- [ ] Tests assert behaviour, not implementation detail
- [ ] Failure modes are tested, not only the happy path

## Readability
- [ ] Names say what the thing is; comments say why, not what
- [ ] The next person can follow the control flow without a diagram

## Reviewer conduct
- [ ] Distinguish blocking from non-blocking: prefix "nit:" for preference
- [ ] Ask rather than assert when you might be missing context
- [ ] Approve when it is better than what is there, not when it is perfect
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
## Review comments produced by working through the checklist
PR #482 — "Pin bundle version at request creation"

**Blocking**

1. `resolveBundle` returns the latest version when the pinned version row is
   missing (bundles.go:88). That silently defeats ADR-0012 — the grant would
   trace to the wrong rule. Should be an error; a missing pinned version is a
   data-integrity problem, not something to paper over.

2. The migration adds `bundle_version NOT NULL` with no default, while the
   previous release still writes rows without it. During the rolling deploy the
   old pods will fail every insert. Two-step it: nullable now, backfill,
   NOT NULL next release.

**Non-blocking**

3. nit: `bv` reads as "bundle version" only if you already know. `bundleVer`
   costs nothing.

4. The table test covers 6 of the 8 transitions; APPROVED -> APPLYING and
   REJECTED -> APPLYING are missing. Not blocking since integration tests hit
   both, but they belong in the unit table.

**Question**

5. If People Ops re-resolves a pending request, does the audit record show both
   the original and the new pinned version? I could not tell from
   `reResolve()`. If not, an auditor cannot reconstruct the change — that would
   be blocking.

**Good**

6. The idempotency key on adapter calls is exactly right and was not asked for.
{{< /doctabs >}}

## Common mistakes

- **Reviewing style that a linter should catch.** It trains authors to expect trivial feedback and to skim the substantive kind.
- **Not distinguishing blocking from preference.** Authors cannot tell what actually stops the merge, so everything becomes negotiable — or nothing does.
- **Approving huge pull requests.** Above roughly 400 lines, review quality collapses. Ask for a split; that is a legitimate review outcome.
- **Only reading the diff.** Some defects are only visible in the surrounding function, or in the caller that the diff does not touch.
- **No positive comments.** Reviews that only ever list defects make people avoid review, which is the opposite of the goal.

## Related templates

- [Coding Standards](/docs/development-release/coding-standards/) — the automated rules that keep this checklist short.
- [Pull Request Template](/docs/development-release/pull-request-template/) — gives the reviewer the context this checklist assumes.
- [Defect Report](/docs/testing-qa/defect-report/) — for issues found that are too large to fix in this change.
- [Development & Release](/docs/development-release/) — the other four development and release templates.
