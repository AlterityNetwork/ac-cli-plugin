---
name: ac-cli
description: >
  AgencyCore platform via `ac` CLI: CRM (companies, contacts, deals, pipelines,
  activities, follow-ups, communications, lists, imports, engagement); outreach
  automation (Envoy sequences, campaigns, recipients, outbox drafts, inbox
  replies, signals, battlecards, playbooks, cold emails); workflows (runs,
  schedules, cron, presets, CSV, discovered companies/people); admin (users,
  organizations, queues, failed jobs, demo, customer onboarding, AI/app/platform
  usage, cross-org Sonar/Headhunter searches, legal docs, subscriptions, chat
  escalations); platform (file/image upload, knowledge base PDF resources, apps,
  writing styles, Nylas email, hooks, messaging sessions, chat threads, profiles,
  environment switching). Use when user mentions "ac"/"AgencyCore", any record
  (deal, contact, sequence, draft, queue), wants to draft a cold email, schedule
  a workflow, upload a PDF to the knowledge base, install an app, switch envs,
  check queue health, onboard a customer, or script AgencyCore with JSON+jq.
when_to_use: >
  Fires on: "ac"/"AgencyCore"; CRM verbs on companies/contacts/deals/activities;
  "draft/approve/reject email", "cold email"; "sequence", "Envoy", "playbook",
  "battlecard", "signal"; "schedule workflow", "cron", "preset", "discovered",
  "csv parse"; admin ops on users/orgs/queues/onboarding/usage/searches/legal/
  subscriptions; "knowledge base", "upload PDF", "writing style", "messaging",
  "chat thread", "Nylas", "install app", "switch env"; ids like wf-*/seq-*.
  Run install+auth first if not done.
allowed-tools:
  - Bash(ac *)
  - Bash(pip *)
  - Bash(uv *)
  - Bash(pipx *)
  - Bash(jq *)
  - Bash(echo *)
argument-hint: "[command or question about the AgencyCore CLI]"
---

# AgencyCore CLI

The `ac` CLI manages CRM, outreach, workflows, admin, and platform from the terminal. This file is the entrypoint guide. Domain command lists live in `references/<domain>.md`; the full flag reference is `references/commands.md`.

---

## Step 0 -- Ensure CLI Is Installed (always run first)

The package is public on PyPI. **Do NOT ask the user where the source is.**

```bash
pip install --upgrade agencycore-cli
```

If `pip` is unavailable, fall back to `uv pip install --upgrade agencycore-cli` or `pipx upgrade agencycore-cli`. Verify:

```bash
ac --help
```

If the user is inside the `agencycore` monorepo and prefers source, `cd ac-cli && uv sync` then prefix every command with `uv run`. PyPI install is the default.

---

## Step 1 -- Authenticate

```bash
ac whoami
```

- Authenticated → user/org info appears. Proceed.
- Not authenticated → ask the user for their email and password, then run login for them. Do NOT instruct the user to run it themselves.

```bash
ac login --email "user@example.com" --password "their-password"
```

The CLI defaults to **staging**. Server URLs are built in. For local dev only:

```bash
ac login --dev --email "user@example.com" --password "their-password"
```

Verify with `ac whoami`.

### Claude Code on the web (cloud VM)

The CLI is not pre-installed on cloud VMs — install from PyPI as above. If `ac login` fails with a connection error, the VM may need network access. Tell the user to enable **Full network access** in their project settings, or at minimum allowlist:
- `api.agencycore.dev`
- `tjzxfwiqommgrzxaflar.supabase.co`

---

## Output Modes

Every command supports two styles:

- Default — Rich tables/panels for humans
- `--json` — Raw JSON for piping into `jq`

```bash
ac crm companies list             # Pretty table
ac crm companies list --json      # Raw JSON
```

`--json` also makes errors structured: `{"error": true, "status_code": 404, "detail": "..."}`.

---

## Domain Map -- Find the Right Commands

For the command list of a domain, **read the matching reference file** before composing commands.

| Domain | Covers | Reference |
|--------|--------|-----------|
| CRM | companies, people, deals, activities, communications, lists, import, search, dashboards | [`references/crm.md`](references/crm.md) |
| Envoy (Outreach) | sequences, campaigns, steps, recipients, outbox (drafts), inbox (replies), battlecards, playbooks, signals | [`references/envoy.md`](references/envoy.md) |
| Workflows | runs, schedules, presets, CSV, discovered companies/people | [`references/workflows.md`](references/workflows.md) |
| Admin | users, orgs, queues, demo, onboarding, app/AI/platform usage, cross-org searches, legal docs, subscriptions, plans (requires `superadmin`) | [`references/admin.md`](references/admin.md) |
| Platform | files/images, apps, writing styles, Nylas email, hooks, messaging, chat threads, resources, profiles | [`references/platform.md`](references/platform.md) |
| Auth & Env | login, logout, whoami, health, env list/show/use | [`references/auth-env.md`](references/auth-env.md) |

For exhaustive flag tables see [`references/commands.md`](references/commands.md). For multi-step recipes beyond the 6 in this file, see [`references/workflows-recipes.md`](references/workflows-recipes.md).

---

## Important Patterns

### Tags
Comma-separated string; the CLI splits automatically:
```bash
--tags "enterprise,hot-lead,q2"
```

### Dates
ISO format always:
```bash
--due-date 2026-03-20
--expected-close-date 2026-04-15
```

### Pagination
List commands accept `--limit` and `--offset`:
```bash
ac crm people list --limit 50 --offset 100
```

### Period flag (dashboards / usage / engagement)
Dashboards default to a 30-day window. **Always pass `--period N`** when the user names a different timeframe ("last 60 days", "this quarter", "the past two weeks"). Translate weeks/quarters to days (60, 90, 180):

```bash
ac crm engagement-dashboard --period 60
ac crm dashboard --period 14
```

### Cron expressions
Standard 5-field (`minute hour dom month dow`):
- `0 9 * * 1` — every Monday 9 AM
- `0 9 * * 1-5` — every weekday 9 AM
- `0 */6 * * *` — every 6 hours
- `30 8 1 * *` — 1st of each month 8:30 AM

**Always pass `--timezone`** (e.g. `America/New_York`, `Europe/London`, `UTC`) when creating or previewing schedules — without it the server defaults may surprise you. Mention timezone explicitly even when the user says "ET" / "Eastern" / "PT".

```bash
ac workflows schedules create wf-77 --cron "0 9 * * 1-5" --timezone America/New_York
```

### JSON input for workflows
```bash
--input '{"company_id": "abc123", "mode": "incremental"}'
--config '{"batch_size": 50}'
```

### Workflow ID is positional
All `ac workflows ...` subcommands take `<workflow-id>` as their first positional arg.

### Org auto-resolution
`ac apps ...` resolves `--org-id` from your session. Only pass `--org-id` to operate on a different org.

### Upload constraints
- Images (`ac files images upload`): max 1 MB; .jpg/.jpeg/.png/.gif/.webp/.svg/.avif
- Resources (`ac resources upload`): max 10 MB; .pdf/.txt/.md/.docx; `--name` required

---

## Dry-Run / Preview Patterns

Before any irreversible mutation, prefer the preview/list command first.

| Mutation | Preview first |
|----------|---------------|
| `ac crm import commit --preview-id <id>` | `ac crm import preview --file <path>` |
| `ac workflows schedules create ... --cron "..."` | `ac workflows schedules preview ... --cron "..." --count 5` |
| `ac envoy sequences launch <id>` | `ac envoy sequences impact-preview <id> --step-id <id>` |
| `ac workflows run-people add-to-crm` | `ac workflows run-people company-match-preview` |
| Any `delete` | `get` / `list` to confirm target id |

### Skipping confirmations (scripts/agents)

`delete` commands ask for confirmation. Either:
- Pass `--yes` per-command, or
- Set `AC_YES=1` once for the session/script:

```bash
AC_YES=1 ac crm companies delete abc123
AC_YES=1 ac admin queues retry-all default
```

---

## Exit Codes

The CLI uses semantic exit codes so agents can branch on failure type:

| Code | Meaning | HTTP |
|------|---------|------|
| 0 | Success | 2xx |
| 1 | General/unknown error | 500, connection errors |
| 2 | Validation error | 422 |
| 3 | Not found | 404 |
| 4 | Auth / permission denied | 401, 403 |
| 5 | Conflict | 409 |

```bash
ac crm companies get bad-id
echo $?    # 3
```

Pair `--json` (structured error body) with `$?` (typed code) for robust scripting.

---

## JSON-First Scripting

Canonical pattern for agents:

```bash
# IDs only
ac crm deals list --stage qualified --json | jq -r '.[].id'

# Counts
ac crm people list --company-id abc123 --json | jq length

# Aggregations
ac admin searches runs --status failed --all \
  | jq 'group_by(.organization_id) | map({org: .[0].organization_id, count: length})'

# Subset of fields
ac crm engagement-dashboard --json | jq '{open_rate, click_rate, reply_rate}'
```

`--all` walks every page (page-size 100) and emits a single JSON array; capped at 50,000 items — narrow filters if you hit the cap.

---

## Common Workflows (Core 6)

The other 9 multi-step recipes live in [`references/workflows-recipes.md`](references/workflows-recipes.md).

> **Multi-step execution rule**: when a user request maps to a recipe with N steps, run **all N steps in one response** (chain them in a single bash invocation with `&&` if outputs feed forward, or run sequentially). Do not stop after the first step and ask the user "ready for the next step?" — chain the whole flow, then summarize results.

### CRM: Company + contact + deal in one go

```bash
ac crm companies create --name "Acme Corp" --website https://acme.com \
  --industry Technology --lifecycle-stage lead

# Note the company id from output, then:
ac crm people create --email jane@acme.com --full-name "Jane Smith" \
  --current-title "VP Sales" --company-id <company-id>

ac crm deals create --name "Acme Enterprise" --stage discovery \
  --amount 50000 --company-id <company-id> --contact-id <person-id>
```

### CRM: Bulk import (preview → commit)

```bash
ac crm import preview --file contacts.json
# If preview looks right:
ac crm import commit --preview-id <id-from-preview>
```

### Envoy: Launch a sequence

```bash
# 1. Create
ac envoy sequences create --name "Q2 Enterprise" \
  --writing-style-id <style-id> --playbook-id <playbook-id> --json

# 2. Steps
ac envoy steps create <sequence-id> --type message \
  --prompt "Write a cold intro email" --step-order 1
ac envoy steps create <sequence-id> --type delay \
  --delay-value 3 --delay-unit days --step-order 2
ac envoy steps create <sequence-id> --type message \
  --prompt "Write a follow-up" --step-order 3

# 3. Recipients
ac envoy recipients add <sequence-id> --prospect-ids id1,id2,id3

# 4. Launch
ac envoy sequences launch <sequence-id> --workflow-id <workflow-id>
```

### Envoy: Review and approve drafts

```bash
ac envoy outbox pending --json
ac envoy outbox approve <draft-id>
# OR
ac envoy outbox reject <draft-id> --action regenerate_draft --reason "Too formal"
ac envoy outbox sent --json
```

### Workflows: Schedule a recurring run

```bash
# Always preview the cron interpretation first
ac workflows schedules preview <workflow-id> \
  --cron "0 9 * * 1" --timezone "America/New_York" --count 10

ac workflows schedules create <workflow-id> \
  --cron "0 9 * * 1" --timezone "America/New_York" --json

ac workflows schedules list <workflow-id> --json
```

### Platform: Switch environments

```bash
ac env list                           # See available envs + login status
ac env use staging                    # Switch
ac env show                           # Confirm
ac login --email "..." --password "..."   # Re-auth on the new env
```

---

## Agent-Friendly Features

- **Structured JSON errors** — `--json` returns `{"error": true, "status_code": ..., "detail": "..."}` instead of pretty text
- **Non-interactive mode** — `AC_YES=1` skips every confirmation prompt
- **Semantic exit codes** — see Exit Codes table above
- **Pagination + `--all`** — page through then aggregate; respects the 50k cap

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Command not found: ac` | `pip install --upgrade agencycore-cli` (PyPI is public — never ask the user for source) |
| `Not authenticated` | `ac login --email ... --password ...` |
| 401 after long idle | Token refresh failed — re-run `ac login` |
| 403 / Forbidden | Account lacks role; admin commands need `superadmin` (verify via `ac whoami`) |
| `ac env use <x>` "no effect" | Expected — env switched but you must `ac login` again on the new env |
| Connection refused | `ac health check`; if cloud VM, enable **Full network access** in project settings |
| Cloud VM blocks API | Allowlist `api.agencycore.dev` and `tjzxfwiqommgrzxaflar.supabase.co` |
| `ac --json` parse error in jq | Confirm exit code; on non-zero the body is `{"error": true, ...}` not your expected shape |
| Image upload fails | File >1 MB or unsupported format (.jpg/.jpeg/.png/.gif/.webp/.svg/.avif) |
| Resource upload fails | File >10 MB or unsupported format (.pdf/.txt/.md/.docx); `--name` is required |
| App install returns 409 | Already installed for this org |
| Nylas OAuth fails | Browser must reach the redirect; ensure network allows OAuth flows |
| No drafts in outbox | Sequence must be launched and steps must have generated drafts |
| Reject fails | `--action` must be `regenerate_draft` or `remove_recipient` |
| Queue commands return empty | Queues may not be running — start with `ac admin queues health` |
| AI usage shows no data | Date range covers no AI activity — widen `--start-date` |
| Run stuck in pending | Check workflow service health and queue status |
| Schedule not triggering | Verify timezone + cron with `ac workflows schedules preview` |
| Invalid cron expression | Use 5-field format (`minute hour dom month dow`) |
| Demo cleanup fails | Need superadmin; accounts must not be in use |
| Wrong env results | `ac env show` to confirm; `ac env use <env>` then re-login |
