---
name: ac-cli-crm
description: >
  Guide for using the AgencyCore CLI (`ac`) to manage CRM data — companies, people,
  deals, activities, communications, lists, and imports. Use this skill whenever
  someone asks to look up, create, update, or delete CRM records via the command line,
  manage contacts or deals, search CRM data, check their pipeline, draft emails,
  import data, or do anything CRM-related outside the web UI. Also trigger when
  users mention "ac crm", "ac cli", or ask how to interact with AgencyCore data
  from a terminal.
allowed-tools:
  - Bash
argument-hint: "[command or question]"
---

# AgencyCore CLI — CRM Operations

The `ac` CLI lets you manage your AgencyCore CRM from the terminal. This guide
covers setup, authentication, every CRM command, and common workflows so you can
work with your data without opening the web app.

---

## Step 0: Ensure CLI Is Installed (Always Do This First)

Before running any CRM command, check if the `ac` CLI is available and install it
automatically if missing. **Do NOT ask the user where the code is — the package is
public on PyPI.**

```bash
pip install --upgrade agencycore-cli
```

If `pip` is not available, try `uv pip install --upgrade agencycore-cli` or `pipx upgrade agencycore-cli`.

This always installs or upgrades to the latest version. Then verify it works:
```bash
ac --help
```

**Note**: If you are inside the `agencycore` monorepo and the `ac-cli/` directory
exists, you may alternatively install from source with `cd ac-cli && uv sync` (then
prefix commands with `uv run`, e.g., `uv run ac whoami`). But PyPI install is the
default — never ask the user for the source code location.

---

## Step 1: Authentication Check

Verify the user is authenticated:

```bash
ac whoami
```

- **If authenticated**: You'll see user info and org details. Proceed to the command the user needs.
- **If not authenticated** (error or "not logged in"): Ask the user for their email and password, then log them in (see below).

---

## Login

When the user is not authenticated, **always ask for their email and password
directly, then run the login command for them**. Do NOT tell the user to run the
command themselves or offer it as an alternative. The user experience should be:

1. Ask: "What's your AgencyCore email and password?"
2. Once they provide credentials, run:
   ```bash
   ac login --email "user@example.com" --password "their-password"
   ```
3. Verify with `ac whoami`

The CLI defaults to the **staging** environment. All server URLs are built in —
no need to pass them manually.

**For local dev** (if the user explicitly asks for it):
```bash
ac login --dev --email "user@example.com" --password "their-password"
```

### Verify login

```bash
ac whoami
```

You should see the user's email, org, and role.

### Claude Code on the Web (Cloud VM)

When running on a cloud VM (e.g., Claude Code on the web), the CLI won't be
pre-installed. **Just install it from PyPI** — don't ask the user for source code:

```bash
pip install --upgrade agencycore-cli
```

If install succeeds but `ac login` or API calls fail with connection errors, the
cloud VM may need network access enabled. Tell the user to enable **Full network
access** in their Claude Code on the web project settings, or at minimum allowlist:
- `api.agencycore.dev`
- `tjzxfwiqommgrzxaflar.supabase.co`

---

## Output Modes

Every CRM command supports two output styles:

- **Rich output** (default) — formatted tables and panels, good for reading
- **JSON output** (`--json`) — raw JSON, good for piping into other tools like `jq`

```bash
uv run ac crm companies list              # Pretty table
uv run ac crm companies list --json       # Raw JSON for scripting
```

## Quick Reference

Read `references/commands.md` for the full command reference with all flags and
options. Below is an overview of what's available.

### Companies

```bash
ac crm companies list [--limit 20] [--offset 0]
ac crm companies get <company-id>
ac crm companies create --name "Acme Corp" [--website https://acme.com] \
  [--industry Technology] [--lifecycle-stage lead] [--tags "hot,enterprise"]
ac crm companies update <company-id> --industry "SaaS"
ac crm companies delete <company-id> [--yes]
```

### People (Contacts)

```bash
ac crm people list [--company-id <id>] [--limit 20]
ac crm people get <person-id>
ac crm people create --email jane@acme.com --full-name "Jane Smith" \
  [--current-title "VP Sales"] [--company-id <id>] [--tags "decision-maker"]
ac crm people update <person-id> --current-title "CRO"
ac crm people delete <person-id> [--yes]
```

### Deals

```bash
ac crm deals list [--stage qualified] [--company-id <id>] [--owner-id <id>]
ac crm deals get <deal-id>
ac crm deals create --name "Acme Enterprise" --stage qualified \
  [--amount 50000] [--currency USD] [--company-id <id>] \
  [--expected-close-date 2026-04-15] [--tags "q2,enterprise"]
ac crm deals update <deal-id> --amount 75000
ac crm deals move <deal-id> --stage negotiation
ac crm deals order --stage qualified --deal-ids id1,id2,id3
ac crm deals delete <deal-id> [--yes]
```

### Activities (Tasks)

```bash
ac crm activities list [--deal-id <id>] [--type call] [--status pending]
ac crm activities get <activity-id>
ac crm activities create --type call --title "Follow up with Jane" \
  [--due-date 2026-03-20] [--priority high] [--deal-id <id>] [--contact-id <id>]
ac crm activities update <activity-id> --priority urgent
ac crm activities complete <activity-id>
ac crm activities delete <activity-id> [--yes]
```

### Communications (Email & Messages)

```bash
ac crm comms list [--company-id <id>] [--contact-id <id>] [--type email]
ac crm comms get <communication-id>
ac crm comms thread <thread-id>
ac crm comms unread
ac crm comms mark-read <thread-id>
ac crm comms draft-email --contact-id <id> --subject "Intro" --content "Hi..."
ac crm comms generate-draft --mode cold_outreach --recipient-name "Jane" \
  [--company-name "Acme"] [--context "Met at conference"]
ac crm comms contact-by-email jane@acme.com
ac crm comms archive --thread-id <id>
ac crm comms delete <communication-id> [--yes]
```

### Lists

```bash
ac crm lists list
ac crm lists get <list-id>
ac crm lists create --name "Q2 Targets" [--member-type person] [--type static]
ac crm lists add-member <list-id> --person-id <id>
ac crm lists remove-member <list-id> --person-id <id>
ac crm lists members <list-id>
ac crm lists delete <list-id> [--yes]
```

### Import

```bash
ac crm import preview --file contacts.json    # Preview what will be imported
ac crm import commit --preview-id <id>        # Apply the import
```

### Search & Dashboard

```bash
ac crm search "acme"                    # Search across companies, contacts, deals
ac crm dashboard [--period 30]          # Pipeline metrics for the last N days
```

## Important Patterns

### Tags
Pass tags as a comma-separated string. The CLI splits them automatically:
```bash
--tags "enterprise,hot-lead,q2"
```

### Dates
Use ISO format for all dates:
```bash
--due-date 2026-03-20
--expected-close-date 2026-04-15
```

### Deleting Records
Delete commands ask for confirmation by default. Add `--yes` to skip the prompt
(useful in scripts):
```bash
ac crm companies delete abc123 --yes
```

### Pagination
List commands accept `--limit` and `--offset` for pagination:
```bash
ac crm people list --limit 50 --offset 100
```

### Scripting with JSON
Combine `--json` with `jq` for powerful one-liners:
```bash
# Get all deal IDs in the "qualified" stage
ac crm deals list --stage qualified --json | jq -r '.[].id'

# Count contacts at a company
ac crm people list --company-id abc123 --json | jq length
```

## Common Workflows

### Add a new company with a contact and deal
```bash
# 1. Create the company
ac crm companies create --name "Acme Corp" --website https://acme.com \
  --industry Technology --lifecycle-stage lead

# 2. Note the company ID from the output, then add a contact
ac crm people create --email jane@acme.com --full-name "Jane Smith" \
  --current-title "VP Sales" --company-id <company-id>

# 3. Create a deal linked to both
ac crm deals create --name "Acme Enterprise" --stage discovery \
  --amount 50000 --company-id <company-id> --contact-id <person-id>
```

### Review your pipeline
```bash
ac crm dashboard                         # Overview metrics
ac crm deals list --stage negotiation    # Deals in negotiation
ac crm activities list --status pending  # Overdue tasks
ac crm comms unread                      # Unread messages
```

### Bulk import contacts
```bash
# Preview first to check for issues
ac crm import preview --file contacts.json

# If the preview looks good, commit it
ac crm import commit --preview-id <id-from-preview>
```

## Auth Commands Reference

| Command | What it does |
|---------|-------------|
| `ac login` | Sign in (stores credentials locally) |
| `ac logout` | Clear stored credentials |
| `ac whoami` | Show your user info and organization |
| `ac health check` | Verify the API is reachable (no auth needed) |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Not authenticated" error | Run `ac login` with staging credentials (see First-Time Setup) |
| Connection refused | Check network access and that the API is reachable: `ac health check` |
| 401 after long idle | The CLI auto-refreshes tokens, but if it fails, run `ac login` again |
| Command not found: `ac` | Run `pip install --upgrade agencycore-cli` — the package is public on PyPI. Do not ask the user for source code. |
| Cloud VM can't reach API | Enable **Full network access** in Claude Code on the web project settings |
