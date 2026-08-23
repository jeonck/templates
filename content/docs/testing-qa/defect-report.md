---
weight: 5030
title: "Defect Report"
description: "Enough information for someone else to reproduce the problem without asking you a single question."
icon: "bug_report"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

The measure of a defect report is whether a developer who has never seen the system can reproduce it from the report alone. Everything else — severity debates, assignment, status — is administration around that one requirement.

## When to use it

- Any behaviour that differs from a specified or reasonably expected result.
- Also for defects found in production, where it becomes the input to an [Incident Report](/docs/operations-incident/incident-report/) if user impact is ongoing.

## What it must answer

- What did you do, what happened, and what should have happened?
- Where and when — build, environment, time, correlation ID?
- How often does it happen, and does a workaround exist?
- Who does it affect and how badly?

## Template

{{< tabs tabTotal="2" >}}
{{% tab tabName="Rendered" %}}

| Field | Value |
|---|---|
| ID | DEF-yyyy-nnnn |
| Title | Observable symptom, not a guess at the cause |
| Reported by / date | |
| Environment | env, build/commit, client version |
| Severity | Sev-1..4 (impact) |
| Priority | (scheduling) |
| Reproducibility | Always / Intermittent (x of y) / Once |
| Related case | TC-nnn |

**Steps to reproduce**

1.  
2.  

**Expected result**

**Actual result**

**Evidence**

Logs with correlation ID, screenshots, request/response, timestamps in UTC.  

**Impact**

Who is affected, how many, and what it costs them.  

**Workaround**

**Scope of damage**

Any data already affected, and how it will be identified and corrected.  

**Notes**

Investigation so far — clearly separated from observed facts.

{{% /tab %}}
{{% tab tabName="Markdown" %}}

```markdown
| Field | Value |
|---|---|
| ID | DEF-yyyy-nnnn |
| Title | Observable symptom, not a guess at the cause |
| Reported by / date | |
| Environment | env, build/commit, client version |
| Severity | Sev-1..4 (impact) |
| Priority | (scheduling) |
| Reproducibility | Always / Intermittent (x of y) / Once |
| Related case | TC-nnn |

## Steps to reproduce
1.
2.

## Expected result
## Actual result
## Evidence
Logs with correlation ID, screenshots, request/response, timestamps in UTC.

## Impact
Who is affected, how many, and what it costs them.

## Workaround
## Scope of damage
Any data already affected, and how it will be identified and corrected.

## Notes
Investigation so far — clearly separated from observed facts.
```

{{% /tab %}}
{{< /tabs >}}

## Worked example

{{< tabs tabTotal="2" >}}
{{% tab tabName="Rendered" %}}

| Field | Value |
|---|---|
| ID | DEF-2026-0311 |
| Title | Grant applied using the latest bundle version instead of the version pinned on the request |
| Reported by / date | H. Ito, 2026-11-04 |
| Environment | production, v1.13.2, observed via audit log review |
| Severity | Sev-1 — wrong access can be granted and the audit trail is misleading |
| Priority | Immediate |
| Reproducibility | Always, when the pinned bundle version row is absent |
| Related case | TC-112 (did not cover the missing-row case) |

**Steps to reproduce**

1. Create a provisioning request for job code ENG-3 while bundle version  
&nbsp;&nbsp;&nbsp;eng-3@17 is current. Request records `bundle_version = eng-3@17`.  
2. Delete or archive the eng-3@17 row (this happens when People Ops uses the  
&nbsp;&nbsp;&nbsp;"clean up old versions" admin action).  
3. Publish eng-3@18, which adds `repo:payments:write` to the bundle.  
4. Wait for the request to reach APPLYING (start date minus one day).  

**Expected result**

Application fails with an error, because the pinned rule version no longer  
exists and no grant can be attributed to it. ADR-0012 requires that every grant  
trace to exactly one immutable bundle version.  

**Actual result**

`resolveBundle` falls back to the latest version (bundles.go:88) and applies  
eng-3@18, granting `repo:payments:write`. The audit record states the bundle  
version as eng-3@17, which no longer exists — so the audit trail asserts a rule  
that cannot be inspected.  

**Evidence**

Correlation IDs c-8f21a4, c-8f2210, c-8f2266 (2026-10-28 06:04 UTC,  
2026-11-01 06:03 UTC, 2026-11-04 06:03 UTC). For each, the audit record's  
bundle_version has no matching row in `bundle_version`, and the applied  
entitlement set matches eng-3@18. Query and output attached to the ticket.  

**Impact**

Three joiners received `repo:payments:write` without an approval step, because  
that entitlement was in eng-3@18 as a bundle entitlement rather than an  
additional one. All three are engineers who would plausibly have been approved,  
but no approval was recorded. Internal Audit considers an unattributable grant  
a reportable control failure regardless of whether the access was appropriate.  

**Workaround**

Disable the "clean up old versions" admin action (done 2026-11-04 14:20 UTC).  
Without deletion of pinned rows the fallback path is unreachable.  

**Scope of damage**

Query identifies every grant whose audit record references a non-existent  
bundle version: 3 grants, all listed above. Correction: revoke and re-issue  
each through the normal approval path, and notify Internal Audit. Completed  
2026-11-05.  

**Notes**

Investigation, not fact: the fallback looks like it was added to make an old  
migration test pass (commit 4a1c9de, 2026-05-02). Worth checking whether other  
resolvers have a similar "fall back to latest" path.

{{% /tab %}}
{{% tab tabName="Markdown" %}}

```markdown
| Field | Value |
|---|---|
| ID | DEF-2026-0311 |
| Title | Grant applied using the latest bundle version instead of the version pinned on the request |
| Reported by / date | H. Ito, 2026-11-04 |
| Environment | production, v1.13.2, observed via audit log review |
| Severity | Sev-1 — wrong access can be granted and the audit trail is misleading |
| Priority | Immediate |
| Reproducibility | Always, when the pinned bundle version row is absent |
| Related case | TC-112 (did not cover the missing-row case) |

## Steps to reproduce
1. Create a provisioning request for job code ENG-3 while bundle version
   eng-3@17 is current. Request records `bundle_version = eng-3@17`.
2. Delete or archive the eng-3@17 row (this happens when People Ops uses the
   "clean up old versions" admin action).
3. Publish eng-3@18, which adds `repo:payments:write` to the bundle.
4. Wait for the request to reach APPLYING (start date minus one day).

## Expected result
Application fails with an error, because the pinned rule version no longer
exists and no grant can be attributed to it. ADR-0012 requires that every grant
trace to exactly one immutable bundle version.

## Actual result
`resolveBundle` falls back to the latest version (bundles.go:88) and applies
eng-3@18, granting `repo:payments:write`. The audit record states the bundle
version as eng-3@17, which no longer exists — so the audit trail asserts a rule
that cannot be inspected.

## Evidence
Correlation IDs c-8f21a4, c-8f2210, c-8f2266 (2026-10-28 06:04 UTC,
2026-11-01 06:03 UTC, 2026-11-04 06:03 UTC). For each, the audit record's
bundle_version has no matching row in `bundle_version`, and the applied
entitlement set matches eng-3@18. Query and output attached to the ticket.

## Impact
Three joiners received `repo:payments:write` without an approval step, because
that entitlement was in eng-3@18 as a bundle entitlement rather than an
additional one. All three are engineers who would plausibly have been approved,
but no approval was recorded. Internal Audit considers an unattributable grant
a reportable control failure regardless of whether the access was appropriate.

## Workaround
Disable the "clean up old versions" admin action (done 2026-11-04 14:20 UTC).
Without deletion of pinned rows the fallback path is unreachable.

## Scope of damage
Query identifies every grant whose audit record references a non-existent
bundle version: 3 grants, all listed above. Correction: revoke and re-issue
each through the normal approval path, and notify Internal Audit. Completed
2026-11-05.

## Notes
Investigation, not fact: the fallback looks like it was added to make an old
migration test pass (commit 4a1c9de, 2026-05-02). Worth checking whether other
resolvers have a similar "fall back to latest" path.
```

{{% /tab %}}
{{< /tabs >}}

## Common mistakes

- **A title that guesses the cause.** "Caching bug in bundle resolver" sends everyone to the wrong file. Describe the symptom.
- **Missing environment and build.** Half of "cannot reproduce" outcomes are version mismatches.
- **Severity argued instead of impact stated.** Write who is affected and how badly; severity then follows from the definitions in the [Test Plan](/docs/testing-qa/test-plan/).
- **Speculation mixed with observation.** Keep the notes section separate, and label it. A wrong hypothesis stated as fact costs hours.
- **No scope-of-damage section for data-affecting defects.** Fixing the code is half the work; identifying and correcting the records already affected is the other half.

## Related templates

- [Test Case Specification](/docs/testing-qa/test-case-specification/) — the case that should have caught it.
- [Incident Report](/docs/operations-incident/incident-report/) — when the defect is live and hurting users.
- [Release Notes](/docs/development-release/release-notes/) — where the fix and its blast radius are announced.
- [Postmortem](/docs/operations-incident/postmortem/) — for defects worth a systemic look.
- [Testing & QA](/docs/testing-qa/) — the other four testing and QA templates.
