---
weight: 3040
title: "Data Model Document"
description: "Entities, relationships, classification and retention — the parts of the schema that outlive the code."
icon: "database"
date: "2026-08-23"
lastmod: "2026-08-23"
draft: false
---

Code gets rewritten; data outlives it. A data model document records what each entity means, what makes it unique, how long it is kept, and how sensitive it is — facts that a schema dump does not carry and that privacy and audit reviews always ask for.

## When to use it

- New systems that own data, especially anything containing personal data.
- Before a migration, so the target model is agreed before anyone writes DDL.
- When preparing for a [DPIA](/docs/security-compliance/data-protection-impact-assessment/) or an audit — the data inventory is derived from this.

## What it must answer

- What entities exist, and what does each one mean in business terms?
- What identifies a record uniquely, and what are the real cardinalities?
- Which fields are personal, special-category, or otherwise classified?
- How long is each entity kept, on what legal or operational basis, and who deletes it?

## Template

{{< doctabs >}}
# Data Model: <System>

| Field | Value |
|---|---|
| Version / date | |
| Owner | |
| Data steward | |
| Classification | |

## 1. Scope
Which stores this covers, and which it deliberately does not.

## 2. Entity overview
One diagram, plus:

| Entity | Business meaning | Natural key | Volume | Growth |
|---|---|---|---|---|

## 3. Entity detail
### <Entity>
| Field | Type | Required | Classification | Meaning / valid values |
|---|---|---|---|---|

Relationships, with cardinality and what enforces it.

## 4. Reference data
Code lists, who maintains them, how changes are released.

## 5. Classification and privacy
| Entity.field | Data category | Lawful basis | Subject rights impact |
|---|---|---|---|

## 6. Retention and deletion
| Entity | Retention | Trigger | Method | Owner |
|---|---|---|---|---|

## 7. Residency and replication
Where data lives, where copies exist, cross-border transfers.

## 8. Integrity rules
Constraints, invariants, and what happens when they are violated.

## 9. Migration notes
Source of each field on initial load, and the reconciliation method.
{{< /doctabs >}}

## Worked example

{{< doctabs >}}
# Data Model: Access Provisioning Service (extract)

## 2. Entity overview
| Entity | Business meaning | Natural key | Volume | Growth |
|---|---|---|---|---|
| Employee projection | Local read-only copy of the HR record needed to provision | employee_id | ~4,100 | +380/yr |
| Bundle | Immutable version of the entitlement set for a job code | (job_code, version) | ~180 rows | ~25 versions/yr |
| Request | One provisioning or deprovisioning workflow instance | request_id | ~800/yr | flat |
| Entitlement grant | One entitlement applied to one person at one time | grant_id | ~9,000/yr | flat |
| Audit record | Append-only fact about a grant, revocation or approval | audit_id | ~30,000/yr | flat |

## 3. Entity detail

### Request
| Field | Type | Required | Classification | Meaning / valid values |
|---|---|---|---|---|
| request_id | ULID | yes | Internal | Immutable |
| employee_id | string(12) | yes | Personal (identifier) | FK to employee projection |
| bundle_version | string | yes | Internal | Pinned at creation — see ADR-0012 |
| state | enum | yes | Internal | DRAFT, AWAITING_BUNDLE, AWAITING_APPROVAL, APPROVED, APPLYING, COMPLETE, PARTIAL, REJECTED |
| approver_employee_id | string(12) | no | Personal (identifier) | Set only when an approval occurred |
| justification | text | no | Personal (free text — may contain anything) | Minimum 20 chars when present |
| created_at / updated_at | timestamptz | yes | Internal | UTC |

Relationships: Request 1—N Entitlement grant (enforced by FK, cascade
forbidden — grants are never deleted with their request). Request N—1 Bundle,
pointing at an immutable version row.

## 5. Classification and privacy
| Entity.field | Data category | Lawful basis | Subject rights impact |
|---|---|---|---|
| employee_projection.full_name | Personal | Legitimate interest (access administration) | Rectification flows from HR, never edited here |
| employee_projection.job_code | Personal | Legitimate interest | — |
| request.justification | Personal, free text | Legal obligation (audit trail) | Erasure refused for the audit retention period; documented in the DPIA |
| audit_record.* | Personal | Legal obligation | Retained 7 years; not erasable |

No special-category data is held. Free-text justification is the one field
where a user could enter something sensitive; the UI warns against it and the
field is excluded from operational log export.

## 6. Retention and deletion
| Entity | Retention | Trigger | Method | Owner |
|---|---|---|---|---|
| Employee projection | 90 days after leave date | Nightly job | Hard delete | Platform |
| Request | 7 years | Creation date | Partition drop | Platform |
| Entitlement grant | 7 years | Grant date | Partition drop | Platform |
| Audit record | 7 years, then legal review | Record date | Export to cold storage, then delete | Security |
| Operational logs | 90 days | Ingest | Retention policy on log platform | Platform |

## 8. Integrity rules
- A grant must reference an audit record; the grant is only marked applied
  after the audit write returns. An orphan grant is a P2 incident.
- Bundle rows are immutable: `UPDATE` is revoked at the database role level and
  a nightly check verifies no row's content hash has changed.
- A request in state COMPLETE must have zero entitlements in PENDING. Violations
  are alerted, not silently corrected.

## 9. Migration notes
The initial load reconstructed 14 months of historical grants from service desk
tickets. Those rows carry `source = 'backfill'` and a lower confidence flag:
approver is unknown for 61 of them, which is recorded as an accepted gap rather
than filled with a guess.
{{< /doctabs >}}

## Common mistakes

- **A schema dump presented as a data model.** Column names and types are already in the database. Business meaning, classification and retention are not.
- **No retention column.** Retention is where privacy, storage cost and audit all meet. A model without it will not survive its first privacy review.
- **Cardinalities from the diagram tool's defaults.** State whether the relationship is enforced by a constraint or merely intended; "intended" relationships are where data quality dies.
- **Free-text fields ignored in classification.** Any free-text field can hold personal or sensitive data. Say what you do about that.
- **Backfilled data indistinguishable from real data.** Flag it. Every later analysis will need to exclude it.

## Related templates

- [Solution Architecture Document](/docs/architecture-design/solution-architecture-document/) — section 5 of that document points here.
- [Data Protection Impact Assessment](/docs/security-compliance/data-protection-impact-assessment/) — takes its inventory from this.
- [Software Requirements Specification](/docs/requirements/software-requirements-specification/) — data requirements are stated there and modelled here.
- [Architecture & Design](/docs/architecture-design/) — the other four architecture and design templates.
