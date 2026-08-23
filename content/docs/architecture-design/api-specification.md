---
weight: 3030
title: "API Specification"
description: "The contract between two teams: resources, errors, versioning and what happens when it breaks."
icon: "api"
date: "2026-08-23"
draft: false
---

An API specification is a contract, so it must be precise about the parts people argue over later: error semantics, idempotency, pagination, versioning and deprecation. The schema itself belongs in OpenAPI; this document holds the decisions the schema cannot express.

## When to use it

- Before another team, or an external partner, writes code against your service.
- When a public or partner-facing interface needs a support and deprecation commitment.
- Alongside — not instead of — a machine-readable OpenAPI or protobuf definition.

## What it must answer

- What resources exist, and what operations are allowed on each?
- How does a caller authenticate, and what is it authorised to do?
- What errors can occur, how are they shaped, and which are retryable?
- What are the rate limits, the pagination rules, and the versioning policy?

## Template

{{< doctabs >}}
# API Specification: <Service> v<major>

| Field | Value |
|---|---|
| Base URL | |
| Machine-readable spec | link to openapi.yaml |
| Owner team | |
| Support channel | |
| Stability | Experimental / Stable / Deprecated |


## 1. Purpose and audience
Who calls this, for what.

## 2. Authentication and authorisation
Scheme, token lifetime, scopes, and what each scope permits.

## 3. Conventions
Media types, date and money formats, casing, null vs absent, time zones,
correlation header.

## 4. Resources
### <Resource>
| Method | Path | Purpose | Idempotent? | Required scope |
|---|---|---|---|---|


Request and response examples for each non-trivial operation.

## 5. Errors
| HTTP | Code | Meaning | Retryable? | Caller action |
|---|---|---|---|---|


Error body shape, and the rule for machine-readable codes.

## 6. Idempotency and concurrency
Idempotency keys, optimistic concurrency (ETag / version), replay window.

## 7. Pagination, filtering, sorting
## 8. Rate limits and quotas
Limits, headers returned, behaviour at the limit.

## 9. Versioning and deprecation
How breaking changes are made, notice period, sunset headers.

## 10. Non-functional commitments
Latency targets, availability, and where they are measured.

## 11. Changelog
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# API Specification: Provisioning API v1

| Field | Value |
|---|---|
| Base URL | https://provisioning.internal.example.com/v1 |
| Machine-readable spec | /openapi.yaml |
| Owner team | Platform Identity |
| Stability | Stable since 2026-09-01 |


## 2. Authentication and authorisation
OAuth 2.0 client credentials. Tokens live 15 minutes. Scopes:

| Scope | Permits |
|---|---|
| provisioning.read | Read requests and their status |
| provisioning.write | Create requests, re-resolve pending requests |
| provisioning.approve | Approve or reject non-standard entitlements |


Approval requires a user-delegated token; a service token with
provisioning.approve is rejected, because approval must be attributable to a
person (audit driver D1).

## 3. Conventions
JSON only (`application/json`). Timestamps are RFC 3339 in UTC with a trailing
`Z`. Field names are `snake_case`. Absent means "not supplied"; `null` means
"explicitly cleared" — the two are not interchangeable on PATCH. Every request
should carry `X-Correlation-Id`; if absent, the service mints one and returns
it in the response.

## 4. Resources

### Provisioning requests
| Method | Path | Purpose | Idempotent? | Scope |
|---|---|---|---|---|
| POST | /requests | Create a provisioning request | Yes, with Idempotency-Key | provisioning.write |
| GET | /requests/{id} | Fetch one request | Yes | provisioning.read |
| GET | /requests | List, filtered | Yes | provisioning.read |
| POST | /requests/{id}/approve | Approve pending entitlements | Yes, with If-Match | provisioning.approve |
| POST | /requests/{id}/reject | Reject pending entitlements | Yes, with If-Match | provisioning.approve |
| POST | /requests/{id}/re-resolve | Re-resolve against the current bundle | No | provisioning.write |


POST /requests

```json
{
  "employee_id": "E-40219",
  "job_code": "ENG-3",
  "start_date": "2026-10-05",
  "manager_employee_id": "E-11804",
  "additional_entitlements": ["repo:payments:write"]
}
```

201 Created

```json
{
  "id": "req_01J9F3K2",
  "state": "AWAITING_APPROVAL",
  "bundle_version": "eng-3@17",
  "entitlements": [
    {"name": "sso:default", "source": "bundle", "state": "PENDING"},
    {"name": "repo:payments:write", "source": "additional", "state": "AWAITING_APPROVAL"}
  ],
  "created_at": "2026-09-18T09:12:44Z"
}
```

## 5. Errors
Body shape:

```json
{"code": "bundle_not_found", "message": "...", "correlation_id": "...", "details": {}}
```

| HTTP | Code | Meaning | Retryable? | Caller action |
|---|---|---|---|---|
| 400 | invalid_request | Schema or field validation failed | No | Fix the request |
| 401 | unauthenticated | Missing or expired token | After refresh | Get a new token |
| 403 | insufficient_scope | Token lacks the scope, or is a service token on /approve | No | Use a delegated token |
| 404 | not_found | Request ID unknown | No | — |
| 409 | state_conflict | Request is not in a state that allows this action | No | Re-read and decide |
| 412 | precondition_failed | If-Match did not match current version | No | Re-read, re-apply |
| 422 | bundle_not_found | Job code has no bundle | No | Route to People Ops |
| 429 | rate_limited | Quota exceeded | Yes, after Retry-After | Back off |
| 503 | target_unavailable | A downstream target system is down | Yes | Retry with backoff; request is queued regardless |


`code` values are stable and part of the contract; `message` is human-readable
and may change without notice. Never branch on `message`.

## 6. Idempotency and concurrency
POST /requests accepts `Idempotency-Key`; the same key with the same body
returns the original 201 for 24 hours. The same key with a *different* body
returns 409 `idempotency_key_reuse`. Approve and reject require `If-Match` with
the request's ETag, so two managers cannot decide simultaneously.

## 8. Rate limits and quotas
600 requests per minute per client. Responses carry `RateLimit-Limit`,
`RateLimit-Remaining` and `RateLimit-Reset`. Bulk import is exempt but capped
at one concurrent job per client.

## 9. Versioning and deprecation
The major version is in the path. Additive changes (new optional fields, new
enum values on output) ship within v1 — clients must ignore unknown fields and
tolerate unknown enum values. Breaking changes require v2, with both versions
served for at least 6 months. Deprecated endpoints return `Deprecation` and
`Sunset` headers for the whole notice period.

## 10. Non-functional commitments
p95 < 300 ms for reads and < 800 ms for writes, measured at the service's
ingress. 99.5% monthly availability. These are the numbers the owning team is
paged against.
{{< /doctabs >}}

## Common mistakes

- **Documenting only the happy path.** Consumers spend most of their integration effort on errors. The error table is the most-read section of any API document.
- **No retryability guidance.** Without it, callers either retry nothing (and drop work) or retry everything (and duplicate it).
- **`message` used as a machine-readable code.** State explicitly which field is stable, or clients will parse the prose and break on a typo fix.
- **Versioning policy left unstated.** "We will not break you" is not a policy. Notice period and sunset mechanics are.
- **Two sources of truth.** If this document and the OpenAPI file disagree, generate what you can from the schema and keep only the decisions here.

## Related templates

- [Solution Architecture Document](/docs/architecture-design/solution-architecture-document/) — the integration section this expands.
- [Technical Design Document](/docs/architecture-design/technical-design-document/) — the internals behind the contract.
- [Release Notes](/docs/development-release/release-notes/) — where deprecations are announced.
- [Test Plan](/docs/testing-qa/test-plan/) — contract tests are derived from this document.
- [Architecture & Design](/docs/architecture-design/) — the other four architecture and design templates.
