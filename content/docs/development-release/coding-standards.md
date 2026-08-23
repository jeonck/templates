---
weight: 4010
title: "Coding Standards"
description: "The rules a team agrees to enforce — and, more importantly, which ones a machine enforces instead of a human."
icon: "rule"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

A coding standard is only worth writing for rules that are contested and consequential. Formatting is not contested once a formatter is configured; error handling, logging, dependency policy and test expectations are. Write down the second kind.

## When to use it

- When a team grows past the point where conventions spread by osmosis.
- When several teams contribute to one repository and disagree in review.
- When onboarding time is dominated by "how do we do X here?" questions.

## What it must answer

- Which rules are automated, and which require human judgement?
- What is the escape hatch when a rule does not fit, and who approves it?
- What are the rules that exist for safety rather than taste?

## Template

{{< tabs tabTotal="2" >}}
{{% tab tabName="Rendered" %}}

**Coding Standards: &lt;Team or repository&gt;**

| Field | Value |
|---|---|
| Applies to | |
| Owner | |
| Last reviewed | |

**1. Automated rules**

Everything here is enforced in CI; reviewers must not spend time on it.  

| Rule | Tool | Config location | Failing behaviour |
|---|---|---|---|

**2. Language conventions**

Naming, file layout, package structure, public surface.  

**3. Error handling**

When to wrap, when to return, what must never be swallowed.  

**4. Logging and observability**

Levels, structure, required fields, what must never be logged.  

**5. Testing expectations**

What must have a test, what kind, and what coverage means here.  

**6. Dependencies**

Adding, pinning, updating, licence policy, and who approves a new one.  

**7. Security rules**

Input handling, secrets, crypto, authorisation checks.  

**8. Exceptions**

How to deviate: marker, justification, approver, review date.  

**9. Changing this document**

{{% /tab %}}
{{% tab tabName="Markdown" %}}

```markdown
# Coding Standards: <Team or repository>

| Field | Value |
|---|---|
| Applies to | |
| Owner | |
| Last reviewed | |

## 1. Automated rules
Everything here is enforced in CI; reviewers must not spend time on it.

| Rule | Tool | Config location | Failing behaviour |
|---|---|---|---|

## 2. Language conventions
Naming, file layout, package structure, public surface.

## 3. Error handling
When to wrap, when to return, what must never be swallowed.

## 4. Logging and observability
Levels, structure, required fields, what must never be logged.

## 5. Testing expectations
What must have a test, what kind, and what coverage means here.

## 6. Dependencies
Adding, pinning, updating, licence policy, and who approves a new one.

## 7. Security rules
Input handling, secrets, crypto, authorisation checks.

## 8. Exceptions
How to deviate: marker, justification, approver, review date.

## 9. Changing this document
```

{{% /tab %}}
{{< /tabs >}}

## Worked example

{{< tabs tabTotal="2" >}}
{{% tab tabName="Rendered" %}}

**Coding Standards: Platform Identity (Go services)**

**1. Automated rules**

| Rule | Tool | Config | Failing behaviour |
|---|---|---|---|
| Formatting | gofumpt | Makefile `fmt` | CI fails |
| Static analysis | golangci-lint (errcheck, ineffassign, gosec) | .golangci.yml | CI fails |
| Dependency vulnerabilities | govulncheck | CI workflow | CI fails on High/Critical |
| Licence policy | go-licenses | CI workflow | CI fails on GPL family |
| Test coverage on changed lines | CI script | ci/coverage.sh | Warning below 70%, fail below 50% |

Reviewers must not comment on anything in this table. If a rule is wrong,  
change the config, not the review comment.  

**3. Error handling**

- Wrap with context at boundaries: `fmt.Errorf("resolve bundle %s: %w", code, err)`.  
&nbsp;&nbsp;Do not wrap the same error twice in one call chain.  
- Never discard an error with `_` except in deferred `Close()` on a read-only  
&nbsp;&nbsp;handle, and then with a comment saying why.  
- Adapters are the only layer that retries. Everything else treats an error as  
&nbsp;&nbsp;final for that attempt. This is a safety rule: nested retries multiply and  
&nbsp;&nbsp;turned a 30-second outage into 40 minutes in incident INC-2026-0142.  
- Errors crossing the API boundary map to a stable `code` (see the API  
&nbsp;&nbsp;specification); a new code is an API change and needs the same review.  

**4. Logging and observability**

- Structured logs only (slog), never `fmt.Println`.  
- Every log line inside a request must carry `correlation_id` and, where it  
&nbsp;&nbsp;exists, `request_id`. Get them from the context; do not pass them explicitly.  
- Levels: `error` means someone should look; `warn` means it self-healed;  
&nbsp;&nbsp;`info` is a business event; `debug` is off in production.  
- Never log: tokens, entitlement justification text (personal free text),  
&nbsp;&nbsp;full HR records. Log the employee ID, not the name.  
- New code paths need a metric before they need a log line — logs are for  
&nbsp;&nbsp;detail, metrics are for detection.  

**5. Testing expectations**

- Every bug fix starts with a failing test that reproduces it. No exceptions;  
&nbsp;&nbsp;this is the one rule reviewers do block on.  
- State machines and adapters need table-driven tests covering every  
&nbsp;&nbsp;transition or error branch.  
- Contract tests against recorded provider responses, refreshed quarterly.  
- Coverage is a signal, not a target. 100% coverage of trivial getters is not  
&nbsp;&nbsp;worth a reviewer's attention; an untested error branch is.  

**6. Dependencies**

- A new direct dependency needs a one-paragraph justification in the pull  
&nbsp;&nbsp;request and an approval from a maintainer. Volume, not any single choice, is  
&nbsp;&nbsp;the risk.  
- Prefer the standard library. `time`, `net/http` and `database/sql` cover most  
&nbsp;&nbsp;of what small helper libraries offer.  
- Pin exact versions; renovate proposes updates weekly, and security updates  
&nbsp;&nbsp;merge without discussion once CI is green.  

**7. Security rules**

- Authorisation is checked in the handler, never in the adapter. One place.  
- Secrets come from the secrets manager at startup or on rotation; never from  
&nbsp;&nbsp;environment variables baked into an image, never from a file in the repo.  
- SQL through parameterised queries only. String-built SQL fails review even  
&nbsp;&nbsp;if the input is "obviously" safe.  

**8. Exceptions**

Deviate with a comment: `// standards-exception(&lt;rule&gt;): &lt;why&gt;. approved:  
&lt;name&gt; &lt;date&gt;. review: &lt;date&gt;`. CI lists all exceptions in a weekly report so  
they do not accumulate silently.  

**9. Changing this document**

Open a pull request against it. Two maintainer approvals. A rule that cannot be  
justified in two sentences gets deleted rather than debated.

{{% /tab %}}
{{% tab tabName="Markdown" %}}

```markdown
# Coding Standards: Platform Identity (Go services)

## 1. Automated rules
| Rule | Tool | Config | Failing behaviour |
|---|---|---|---|
| Formatting | gofumpt | Makefile `fmt` | CI fails |
| Static analysis | golangci-lint (errcheck, ineffassign, gosec) | .golangci.yml | CI fails |
| Dependency vulnerabilities | govulncheck | CI workflow | CI fails on High/Critical |
| Licence policy | go-licenses | CI workflow | CI fails on GPL family |
| Test coverage on changed lines | CI script | ci/coverage.sh | Warning below 70%, fail below 50% |

Reviewers must not comment on anything in this table. If a rule is wrong,
change the config, not the review comment.

## 3. Error handling
- Wrap with context at boundaries: `fmt.Errorf("resolve bundle %s: %w", code, err)`.
  Do not wrap the same error twice in one call chain.
- Never discard an error with `_` except in deferred `Close()` on a read-only
  handle, and then with a comment saying why.
- Adapters are the only layer that retries. Everything else treats an error as
  final for that attempt. This is a safety rule: nested retries multiply and
  turned a 30-second outage into 40 minutes in incident INC-2026-0142.
- Errors crossing the API boundary map to a stable `code` (see the API
  specification); a new code is an API change and needs the same review.

## 4. Logging and observability
- Structured logs only (slog), never `fmt.Println`.
- Every log line inside a request must carry `correlation_id` and, where it
  exists, `request_id`. Get them from the context; do not pass them explicitly.
- Levels: `error` means someone should look; `warn` means it self-healed;
  `info` is a business event; `debug` is off in production.
- Never log: tokens, entitlement justification text (personal free text),
  full HR records. Log the employee ID, not the name.
- New code paths need a metric before they need a log line — logs are for
  detail, metrics are for detection.

## 5. Testing expectations
- Every bug fix starts with a failing test that reproduces it. No exceptions;
  this is the one rule reviewers do block on.
- State machines and adapters need table-driven tests covering every
  transition or error branch.
- Contract tests against recorded provider responses, refreshed quarterly.
- Coverage is a signal, not a target. 100% coverage of trivial getters is not
  worth a reviewer's attention; an untested error branch is.

## 6. Dependencies
- A new direct dependency needs a one-paragraph justification in the pull
  request and an approval from a maintainer. Volume, not any single choice, is
  the risk.
- Prefer the standard library. `time`, `net/http` and `database/sql` cover most
  of what small helper libraries offer.
- Pin exact versions; renovate proposes updates weekly, and security updates
  merge without discussion once CI is green.

## 7. Security rules
- Authorisation is checked in the handler, never in the adapter. One place.
- Secrets come from the secrets manager at startup or on rotation; never from
  environment variables baked into an image, never from a file in the repo.
- SQL through parameterised queries only. String-built SQL fails review even
  if the input is "obviously" safe.

## 8. Exceptions
Deviate with a comment: `// standards-exception(<rule>): <why>. approved:
<name> <date>. review: <date>`. CI lists all exceptions in a weekly report so
they do not accumulate silently.

## 9. Changing this document
Open a pull request against it. Two maintainer approvals. A rule that cannot be
justified in two sentences gets deleted rather than debated.
```

{{% /tab %}}
{{< /tabs >}}

## Common mistakes

- **Documenting what the formatter already enforces.** It wastes the reader's attention on the one section that never mattered.
- **Rules with no rationale.** "Do not nest retries" is followed inconsistently; "do not nest retries — it turned a 30s outage into 40 minutes in INC-2026-0142" is followed.
- **No exception mechanism.** Teams then either violate the rule silently or contort the code to obey it. Both are worse than a recorded exception.
- **A standard nobody owns.** Without an owner and a review date, it fossilises and then gets ignored wholesale.
- **Coverage percentage as a gate.** It reliably produces tests for trivial code and leaves the error branches untested.

## Related templates

- [Code Review Checklist](/docs/development-release/code-review-checklist/) — what a human checks once the machine has checked the rest.
- [Pull Request Template](/docs/development-release/pull-request-template/) — where the standard is applied per change.
- [Technical Design Document](/docs/architecture-design/technical-design-document/) — where deviations get argued before code exists.
- [Development & Release](/docs/development-release/) — the other four development and release templates.
