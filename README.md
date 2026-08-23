# IT Template Library

Copy-paste document templates for IT work — charters, requirement specs,
decision records, runbooks, incident reports and access reviews. Each template
ships with a worked example and the mistakes that usually spoil it.

**Live site:** https://templates.metacog.co.kr/

## Contents

| Category | Templates |
|---|---|
| Project Management | Charter, plan, status report, RAID log, meeting minutes |
| Requirements & Analysis | BRD, SRS, user story, use case spec, traceability matrix |
| Architecture & Design | Solution architecture, ADR, API spec, data model, technical design |
| Development & Release | Coding standards, review checklist, PR template, release notes, deployment runbook |
| Testing & QA | Test plan, case spec, defect report, UAT plan, test summary |
| Operations & Incident | Runbook, incident report, postmortem, change request, on-call handover |
| Security & Compliance | Security policy, risk register, access review, vendor assessment, DPIA |

## Local development

Requires Hugo Extended and a Go toolchain (the theme is a Hugo Module).

```bash
hugo mod get -u
hugo server
```

## Structure

- `content/docs/<category>/` — one markdown file per template.
  Page `weight` is `1000 * <category index> + 10 * <page index>`, unique
  site-wide, so Lotus Docs' Prev/Next navigation walks categories in order.
- `data/landing.yaml` — the home page (Lotus Docs renders it from data, not
  from `content/_index.md`).
- `layouts/partials/backlinks.html` — "Linked from" section, wired into
  `layouts/docs/single.html` and `layouts/_default/single.html`.
- `static/CNAME` — custom domain, copied to `public/` on every build.

Built with [Hugo](https://gohugo.io) and [Lotus Docs](https://github.com/colinwilson/lotusdocs).
