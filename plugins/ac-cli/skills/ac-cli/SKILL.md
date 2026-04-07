---
name: ac-cli
description: >
  Guide for using the AgencyCore CLI (`ac`) -- CRM (companies, people, deals,
  activities, communications, lists, imports), outreach/Envoy (sequences, steps,
  recipients, inbox, outbox, battlecards, playbooks), workflows (runs, schedules,
  presets, discovered companies/people, CSV parsing), admin (users, orgs, queues,
  onboarding, analytics, demo), platform (files, apps, writing styles, Nylas email,
  messaging, chat, resources, profiles, environment, health). Use when someone asks
  about any AgencyCore CLI operations, mentions "ac" commands, CRM management,
  outreach sequences, workflow automation, admin tasks, file uploads, email
  integration, environment switching, or anything AgencyCore-related from a terminal.
allowed-tools:
  - Bash
argument-hint: "[command or question about the AgencyCore CLI]"
---

# AgencyCore CLI

The `ac` CLI lets you manage your entire AgencyCore platform from the terminal --
CRM, outreach, workflows, admin, and platform utilities. This guide covers setup,
authentication, every command group, and common workflows.

---

## Step 0: Ensure CLI Is Installed (Always Do This First)

Before running any command, check if the `ac` CLI is available and install it
automatically if missing. **Do NOT ask the user where the code is -- the package is
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
default -- never ask the user for the source code location.

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

The CLI defaults to the **staging** environment. All server URLs are built in --
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
pre-installed. **Just install it from PyPI** -- don't ask the user for source code:

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

Every command supports two output styles:

- **Rich output** (default) -- formatted tables and panels, good for reading
- **JSON output** (`--json`) -- raw JSON, good for piping into other tools like `jq`

```bash
ac crm companies list              # Pretty table
ac crm companies list --json       # Raw JSON for scripting
```

---

## Quick Reference -- CRM

Read `references/commands.md` for the full command reference with all flags and
options. Below is an overview of what's available.

### Companies

```bash
ac crm companies list [--limit 100] [--offset 0]
ac crm companies get <company-id>
ac crm companies create --name "Acme Corp" [--website https://acme.com] \
  [--industry Technology] [--lifecycle-stage lead] [--tags "hot,enterprise"]
ac crm companies update <company-id> --industry "SaaS"
ac crm companies delete <company-id> [--yes]
```

### People (Contacts)

```bash
ac crm people list [--company-id <id>] [--limit 100]
ac crm people get <person-id>
ac crm people create [--email jane@acme.com] --full-name "Jane Smith" \
  [--current-title "VP Sales"] [--company-id <id>] [--tags "decision-maker"]
ac crm people update <person-id> --current-title "CRO"
ac crm people delete <person-id> [--yes]
ac crm people bulk-upsert --file people.json
ac crm people bulk-delete --ids id1,id2,id3 [--yes]
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
ac crm comms generate-draft --mode compose --recipient-name "Jane" \
  [--company-name "Acme"] [--recipient-title "VP Sales"] \
  [--sender-signature "Best, John"] [--user-draft-subject "Intro"] \
  [--user-draft-body "Draft to refine..."]
ac crm comms contact-by-email jane@acme.com
ac crm comms resolve-contact <email> [--name "Jane"] [--company-id <id>]
ac crm comms unread-thread-ids
ac crm comms archive --thread-id <id>
ac crm comms unarchive --thread-id <id>
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

### Engagement Dashboard

```bash
ac crm engagement-dashboard [--period 30]    # Email engagement metrics
```

Shows: emails sent (current/previous/change), open rate, click rate, reply rate, bounce rate, email health score, and top clicked links.

---

## Quick Reference -- Envoy (Outreach)

### Sequences

```bash
ac envoy sequences list [--status active]
ac envoy sequences get <sequence-id>
ac envoy sequences create --name "Q2 Outreach" [--description "..."] \
  [--writing-style-id <id>] [--playbook-id <id>] [--crm-list-id <id>]
ac envoy sequences update <sequence-id> --name "Updated Name"
ac envoy sequences delete <sequence-id> [--yes]
ac envoy sequences launch <sequence-id> --workflow-id <id>
ac envoy sequences pause <sequence-id>
ac envoy sequences resume <sequence-id> --workflow-id <id>
```

### Steps

```bash
ac envoy steps create <sequence-id> --type message [--step-order 1] \
  [--message-template "Hi {{name}}..."] [--prompt "Write a cold intro"]
ac envoy steps update <sequence-id> <step-id> [--message-template "..."]
ac envoy steps delete <sequence-id> <step-id> [--yes]
ac envoy steps reorder <sequence-id> --step-ids id1,id2,id3
ac envoy steps stats <sequence-id>
```

### Recipients

```bash
ac envoy recipients list <sequence-id> [--status pending] [--step-id <id>]
ac envoy recipients add <sequence-id> --prospect-ids id1,id2,id3
ac envoy recipients add <sequence-id> --crm-list-id <list-id>
ac envoy recipients add <sequence-id> --source '{"type":"explicit","prospect_ids":["..."]}' # Advanced
ac envoy recipients remove <sequence-id> <recipient-id> [--yes]
```

### Outbox (Draft Approval)

```bash
ac envoy outbox pending [--sequence-id <id>] [--limit 50]
ac envoy outbox sent [--sequence-id <id>] [--status delivered] [--limit 50]
ac envoy outbox step-drafts --sequence-id <id> --step-id <id> [--limit 50]
ac envoy outbox update-draft <draft-id> [--subject "New subject"] [--body "..."]
ac envoy outbox approve <draft-id> [--subject "Override"] [--body "Override"]
ac envoy outbox reject <draft-id> --action regenerate_draft [--reason "Too formal"]
ac envoy outbox regenerate <draft-id> [--instruction "Make it shorter"]
```

### Inbox (Replies)

```bash
ac envoy inbox list [--status open] [--sentiment positive] [--limit 50]
ac envoy inbox messages <thread-id>
ac envoy inbox archive <thread-id>
ac envoy inbox unarchive <thread-id>
ac envoy inbox assign <thread-id> --user-id <id>
ac envoy inbox snooze <thread-id> --until "2026-04-01T09:00:00"
ac envoy inbox complete <thread-id>
ac envoy inbox update-status <thread-id> --status resolved
ac envoy inbox add-tags <thread-id> --tags "hot-lead,priority"
ac envoy inbox remove-tags <thread-id> --tags "stale"
ac envoy inbox reply <thread-id> --body "Thanks for your reply!"
```

### Battlecards

```bash
ac envoy battlecards list [--query "competitor"] [--limit 50]
ac envoy battlecards get <battlecard-id>
ac envoy battlecards create --name "vs Competitor X" [--competitor-name "X"]
ac envoy battlecards update <battlecard-id> --description "Updated positioning"
ac envoy battlecards delete <battlecard-id> [--yes]
ac envoy battlecards duplicate <battlecard-id>
```

### Playbooks

```bash
ac envoy playbooks list [--query "enterprise"] [--limit 50]
ac envoy playbooks get <playbook-id>
ac envoy playbooks create --name "Enterprise Outreach" [--description "..."]
ac envoy playbooks update <playbook-id> --name "Updated Playbook"
ac envoy playbooks delete <playbook-id> [--yes]
ac envoy playbooks duplicate <playbook-id>
```

### Dashboard, Signals & Inbox Count

```bash
ac envoy dashboard                          # Outreach stats overview
ac envoy signals <recipient-id>             # Sales signals for a recipient
ac envoy inbox-count                        # Total inbox thread count
```

---

## Quick Reference -- Workflows

### Runs

```bash
ac workflows runs create <workflow-id> [--input '{"key":"value"}'] [--idempotency-key <key>]
ac workflows runs list <workflow-id> [--limit 50] [--offset 0]
ac workflows runs get <workflow-id> <run-id>
ac workflows runs logs <workflow-id> <run-id> [--limit 50] [--offset 0]
```

### Schedules

```bash
ac workflows schedules list <workflow-id>
ac workflows schedules get <workflow-id>
ac workflows schedules create <workflow-id> --cron "0 9 * * 1" \
  [--timezone "America/New_York"] [--input '{"key":"value"}']
ac workflows schedules update <workflow-id> <schedule-id> \
  [--cron "0 10 * * 1"] [--timezone UTC]
ac workflows schedules delete <workflow-id> <schedule-id> [--yes]
ac workflows schedules preview <workflow-id> --cron "0 9 * * 1" \
  [--timezone UTC] [--count 5]
ac workflows schedules toggle <workflow-id> <schedule-id> --enabled/--disabled
```

### Presets

```bash
ac workflows presets list <workflow-id>
ac workflows presets get <workflow-id> <preset-id>
ac workflows presets create <workflow-id> --name "Daily Sync" \
  [--description "..."] [--config '{"key":"value"}']
ac workflows presets update <workflow-id> <preset-id> --name "Updated Preset"
ac workflows presets delete <workflow-id> <preset-id> [--yes]
```

### CSV Parsing

```bash
ac workflows csv-parse <file.csv>
```

### Discovered Companies (from workflow runs)

```bash
ac workflows run-companies list <workflow-id> [--limit 50] [--offset 0] [--include-in-crm]
ac workflows run-companies list-by-run <workflow-id> <run-id>
ac workflows run-companies add-to-crm <workflow-id> --company-ids id1,id2
ac workflows run-companies crm-count <workflow-id>
ac workflows run-companies delete <workflow-id> --company-ids id1,id2 [--yes]
```

### Discovered People (from workflow runs)

```bash
ac workflows run-people list <workflow-id> [--limit 50] [--offset 0] [--include-in-crm]
ac workflows run-people list-by-run <workflow-id> <run-id>
ac workflows run-people company-match-preview <workflow-id> --person-ids id1,id2
ac workflows run-people company-search <workflow-id> --query "acme"
ac workflows run-people add-to-crm <workflow-id> --person-ids id1,id2 [--overrides-file overrides.json]
ac workflows run-people crm-count <workflow-id>
ac workflows run-people delete <workflow-id> --person-ids id1,id2 [--yes]
```

---

## Quick Reference -- Admin

Admin commands require super admin privileges. Check `ac whoami` for `superadmin` role.

### Users

```bash
ac admin users list [--query "jane"] [--sort created_at] [--order desc] [--page 1] [--page-size 50]
ac admin users get <user-id>
ac admin users create --email jane@example.com --password "secret123" [--full-name "Jane Smith"]
ac admin users update <user-id> [--full-name "Jane Doe"] [--is-superadmin]
ac admin users delete <user-id> [--yes]
ac admin users auth-search --email jane@example.com
ac admin users search --email jane@example.com
ac admin users reset-password <user-id> [--yes]
ac admin users impersonate <user-id>
ac admin users exit-impersonation
ac admin users generate-link <user-id> [--send-email]
```

### Organizations

```bash
ac admin orgs list [--query "acme"] [--sort created_at] [--order desc] [--page 1] [--page-size 50]
ac admin orgs get <org-id>
ac admin orgs create --name "Acme Corp" [--slug acme-corp] [--plan pro]
ac admin orgs update <org-id> [--name "New Name"] [--slug new-slug] [--plan enterprise]
ac admin orgs delete <org-id> [--yes]
ac admin orgs members <org-id> [--page 1] [--page-size 50]
ac admin orgs add-member <org-id> --user-id <user-id> [--role member]
ac admin orgs update-member <org-id> <user-id> --role admin
ac admin orgs remove-member <org-id> <user-id> [--yes]
ac admin orgs transfer-ownership <org-id> --new-owner-id <user-id> [--yes]
```

### Queues

```bash
ac admin queues health
ac admin queues stats
ac admin queues queue-stats <queue-name>
ac admin queues metrics
ac admin queues send-to-sentry
ac admin queues job-performance <job-id>
ac admin queues failed <queue-name> [--limit 50]
ac admin queues retry-all <queue-name> [--yes]
ac admin queues retry-job <job-id>
ac admin queues clear-failed <queue-name> [--yes]
```

### Demo

```bash
ac admin demo scrape-website --url "https://example.com"
ac admin demo generate-org [--industry "Technology"] [--size "medium"]
ac admin demo generate-profile [--industry "Technology"]
ac admin demo prepare-account --org-name "Demo Corp" [--template default]
ac admin demo list-accounts [--page 1] [--page-size 50] [--sort created_at] [--order desc]
ac admin demo get-account <org-id>
ac admin demo update-account <org-id> [--status active] [--notes "Updated demo"]
ac admin demo delete-account <org-id> [--yes]
ac admin demo cleanup [--max-age-days 30] [--yes]
ac admin demo stats
```

### Onboarding

```bash
ac admin onboarding create --email user@example.com --first-name "Jane" \
  --last-name "Smith" --org-name "Acme Corp" [--website-url "https://acme.com"] \
  [--country US] [--timezone "America/New_York"] [--locale en] [--currency USD] \
  [--job-title "CEO"] [--bio "..."] [--linkedin "https://..."] \
  [--contact-email "alt@example.com"] [--calendly-url "https://..."]
ac admin onboarding list [--status pending] [--query "acme"] [--page 1] [--page-size 25]
ac admin onboarding get <org-id>
ac admin onboarding delete <org-id>
ac admin onboarding send-link <org-id> [--send-email]
ac admin onboarding impersonate <org-id>
ac admin onboarding end-impersonation <org-id>
ac admin onboarding activate <org-id> [--send-password-reset] (default: sends reset email)
ac admin onboarding deactivate <org-id>
ac admin onboarding update-config <org-id> [--show-calendly] [--calendly-url "https://..."]
ac admin onboarding get-settings
ac admin onboarding update-settings [--terms-html "<p>...</p>"] \
  [--calendly-url "https://..."] [--calendly-enabled/--no-calendly-enabled]
```

### App Usage

```bash
ac admin app-usage summary [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin app-usage users [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>] \
  [--sort total_actions] [--order desc] [--page 1] [--page-size 50] [--search "jane"]
ac admin app-usage user <user-id> [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
```

### AI Usage

```bash
ac admin ai-usage summary [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin ai-usage users [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>] \
  [--sort total_tokens] [--order desc] [--page 1] [--page-size 50] [--search "jane"]
ac admin ai-usage user <user-id> [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin ai-usage by-model [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin ai-usage by-workflow [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin ai-usage details [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>] \
  [--limit 50] [--offset 0] [--model-id <id>] [--user-id <id>] [--workflow-run-id <id>]
```

### Platform Activity

```bash
ac admin platform-activity summary [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin platform-activity users [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>] \
  [--sort total_events] [--order desc] [--page 1] [--page-size 50] [--query "jane"]
ac admin platform-activity user <user-id> [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
```

### Legal Documents

```bash
ac admin legal-docs list [--document-type terms_of_service]
ac admin legal-docs get <document-id>
ac admin legal-docs create --document-type terms_of_service --version "1.0" --title "Terms of Service" \
  [--content-html "<p>...</p>"]
ac admin legal-docs update <document-id> [--title "Updated Title"] [--content-html "<p>...</p>"]
ac admin legal-docs delete <document-id> [--yes]
ac admin legal-docs set-current <document-id>
```

### Analytics Overview (unified summary)

```bash
ac admin analytics-overview [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
```

### Cache Stats

```bash
ac admin cache-stats
```

---

## Quick Reference -- Platform

### Files (Images)

```bash
ac files images upload <file-path> --category avatars
ac files images delete <r2-object-key> [--yes]
```

Supported categories: `avatars`, `organization_logos`, `crm_company_logos`, `general_images`, `apps_assets`
Supported formats: .jpg, .jpeg, .png, .gif, .webp, .svg, .avif (max 1 MB)

### Apps

```bash
ac apps list [--org-id <id>] [--include-inactive] [--limit 100]
ac apps install <app-slug> [--org-id <id>]
ac apps uninstall <app-slug> [--org-id <id>] [--yes]
ac apps usage <app-slug> [--org-id <id>]
ac apps usage-event <app-slug> --event-type "page_view" [--metadata '{"page":"dashboard"}']
ac apps configs <app-slug> [--org-id <id>] [--no-mask-secrets]
ac apps update-config <app-slug> <config-key> --value "new-value" [--org-id <id>]
ac apps delete-config <app-slug> <config-key> [--org-id <id>] [--yes]
```

### Writing Styles

```bash
ac styles list [--include-inactive]
ac styles get <style-id>
ac styles create --name "Professional" [--description "..."] [--tone formal] [--formality high]
ac styles update <style-id> [--name "Updated"] [--tone casual]
ac styles delete <style-id> [--yes]
ac styles train <style-id> --sample-text "Example email text..."
ac styles feedback <session-id> --rating 4 [--comments "Good but too formal"]
ac styles iterate <session-id> --feedback "Make it more casual"
ac styles analyze --text "Analyze this text for style..."
```

### Nylas (Email Integration)

```bash
ac nylas oauth-start [--provider google] [--return-path "/settings"]
ac nylas account
ac nylas org-accounts
ac nylas disconnect [--yes]
ac nylas send --to "jane@example.com" --subject "Hello" --body "Hi Jane..." \
  [--reply-to-message-id <id>]
ac nylas update-signature --signature "<p>Best regards</p>"
ac nylas validate-signature --signature "<p>Best regards</p>"
```

### Hooks

```bash
ac hooks list <capability>     # List available hooks for a capability
```

### Messaging

```bash
ac messaging sessions                          # List active messaging sessions
ac messaging link --token <link-token>         # Link external messaging sender
```

### Chat (AI Threads)

```bash
ac chat threads list
ac chat threads create --title "Project Discussion"
ac chat threads update <thread-id> [--title "New Title"] [--archived/--no-archived]
ac chat threads delete <thread-id> [--yes]
ac chat threads messages <thread-id>
ac chat threads generate-title <thread-id>
```

### Resources (Knowledge Base)

```bash
ac resources list [--limit 50] [--offset 0]
ac resources upload <file-path> --name "Source Name" [--description "..."] [--tags "tag1,tag2"]
ac resources delete <resource-id> [--yes]
ac resources status <resource-id>
```

Supported formats: .pdf, .txt, .md, .docx (max 10 MB)

### Profiles

```bash
ac profiles me                                    # View your profile
ac profiles update [--first-name "Jane"] [--last-name "Smith"] [--bio "..."] \
  [--job-title "Developer"] [--avatar-url "..."] [--email "jane@example.com"]
ac profiles members [--limit 50] [--offset 0]     # List org members
```

---

## Quick Reference -- Auth & Environment

### Authentication

```bash
ac login --email "user@example.com" --password "their-password"
ac login --dev --email "user@example.com" --password "their-password"  # Local dev
ac logout
ac whoami
ac health check [--api-url https://custom-api.example.com]
```

### Environment

```bash
ac env list                    # Show all environments and login status
ac env show                    # Show active environment details
ac env use <name>              # Switch environment (local, staging, production)
```

Valid environment names: `local`, `staging`, `production`

**Note**: `ac health check` and `ac env` commands do not require authentication.

---

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

### Workflow ID as First Argument
All workflow subcommands take `<workflow-id>` as their first positional argument.
The workflow ID identifies which workflow definition to operate on.

### Cron Expressions
Schedule cron expressions use standard 5-field format:
```
minute hour day-of-month month day-of-week
```
Examples:
- `0 9 * * 1` -- Every Monday at 9 AM
- `0 */6 * * *` -- Every 6 hours
- `30 8 1 * *` -- 1st of each month at 8:30 AM

### JSON Input for Workflows
Pass structured data to workflow runs and presets as JSON strings:
```bash
--input '{"company_id": "abc123", "mode": "incremental"}'
--config '{"batch_size": 50}'
```

### Reject Actions (Envoy)
When rejecting a draft, specify what should happen next:
- `regenerate_draft` -- AI generates a new draft
- `remove_recipient` -- Remove the recipient from the sequence

```bash
ac envoy outbox reject <draft-id> --action regenerate_draft --reason "Wrong tone"
```

### Step Types (Envoy)
- `message` -- Email step (uses template or AI prompt)
- `delay` -- Wait step (value + unit: days, hours, minutes)
- `task` -- Manual task reminder

### Organization ID Auto-Resolution
For `ac apps` commands, `--org-id` is auto-resolved from your login session
(`/whoami`). You only need to specify it when operating on a different organization.

### Image Upload Constraints
- Max file size: 1 MB
- Allowed formats: .jpg, .jpeg, .png, .gif, .webp, .svg, .avif
- Category is required and determines the storage path

### Resource Upload Constraints
- Max file size: 10 MB
- Allowed formats: .pdf, .txt, .md, .docx
- `--name` is required and sets the source name

---

## Common Workflows

### CRM: Add a company with a contact and deal

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

### CRM: Bulk import contacts

```bash
# Preview first to check for issues
ac crm import preview --file contacts.json

# If the preview looks good, commit it
ac crm import commit --preview-id <id-from-preview>
```

### CRM: Check engagement

```bash
# View engagement metrics for the last 30 days
ac crm engagement-dashboard

# View engagement for a custom period (60 days)
ac crm engagement-dashboard --period 60

# Get raw data for analysis
ac crm engagement-dashboard --json | jq '{open_rate, click_rate, reply_rate}'
```

### Envoy: Launch a sequence

```bash
# 1. Create the sequence
ac envoy sequences create --name "Q2 Enterprise" \
  --writing-style-id <style-id> --playbook-id <playbook-id> --json

# 2. Add steps (message, delay, task)
ac envoy steps create <sequence-id> --type message \
  --prompt "Write a cold intro email" --step-order 1
ac envoy steps create <sequence-id> --type delay \
  --delay-value 3 --delay-unit days --step-order 2
ac envoy steps create <sequence-id> --type message \
  --prompt "Write a follow-up" --step-order 3

# 3. Add recipients
ac envoy recipients add <sequence-id> --prospect-ids id1,id2,id3

# 4. Launch with a workflow
ac envoy sequences launch <sequence-id> --workflow-id <workflow-id>
```

### Envoy: Review and approve drafts

```bash
# 1. Check pending drafts
ac envoy outbox pending --json

# 2. Review a specific draft, then approve or reject
ac envoy outbox approve <draft-id>
# OR
ac envoy outbox reject <draft-id> --action regenerate_draft --reason "Too formal"

# 3. Check sent emails
ac envoy outbox sent --json
```

### Envoy: Manage inbox

```bash
# 1. Check inbox
ac envoy inbox list --status open --json

# 2. Read thread messages
ac envoy inbox messages <thread-id>

# 3. Reply to a thread
ac envoy inbox reply <thread-id> --body "Thanks for your interest!"

# 4. Complete the thread
ac envoy inbox complete <thread-id>
```

### Workflows: Schedule a recurring workflow

```bash
# 1. Create a cron schedule (every Monday at 9 AM ET)
ac workflows schedules create <workflow-id> \
  --cron "0 9 * * 1" --timezone "America/New_York" --json

# 2. Preview upcoming run times
ac workflows schedules preview <workflow-id> \
  --cron "0 9 * * 1" --timezone "America/New_York" --count 10

# 3. Check the schedule was created
ac workflows schedules list <workflow-id> --json
```

### Workflows: Trigger and monitor a run

```bash
# 1. Create a new run
ac workflows runs create <workflow-id> --input '{"param":"value"}' --json

# 2. Check run status
ac workflows runs get <workflow-id> <run-id> --json

# 3. View run logs
ac workflows runs logs <workflow-id> <run-id> --json
```

### Workflows: Parse CSV and review discovered companies

```bash
# 1. Parse a CSV file
ac workflows csv-parse leads.csv --json

# 2. Trigger a workflow run to discover companies
ac workflows runs create <workflow-id> --input '{"source":"csv"}' --json

# 3. List discovered companies from the workflow
ac workflows run-companies list <workflow-id> --json

# 4. Add promising companies to CRM
ac workflows run-companies add-to-crm <workflow-id> --company-ids id1,id2
```

### Workflows: Review and import discovered people to CRM

```bash
# 1. List discovered people from a workflow
ac workflows run-people list <workflow-id> --json

# 2. Preview company matches before importing
ac workflows run-people company-match-preview <workflow-id> --person-ids id1,id2

# 3. Search for a specific company to match
ac workflows run-people company-search <workflow-id> --query "acme"

# 4. Add people to CRM (with optional overrides file)
ac workflows run-people add-to-crm <workflow-id> --person-ids id1,id2

# 5. Verify the count of people added
ac workflows run-people crm-count <workflow-id>
```

### Admin: Check AI token usage

```bash
# 1. Get AI usage summary for this month
ac admin ai-usage summary --start-date 2026-03-01 --json

# 2. Get top users sorted by token usage
ac admin ai-usage users --start-date 2026-03-01 --sort total_tokens --order desc --limit 10 --json

# 3. Drill into a specific user's usage
ac admin ai-usage user <user-id> --start-date 2026-03-01 --json

# 4. See which models are costing the most
ac admin ai-usage by-model --start-date 2026-03-01 --json
```

### Admin: Onboard a customer

```bash
# 1. Create the onboarding record
ac admin onboarding create --email "newcustomer@example.com" \
  --first-name "Jane" --last-name "Smith" \
  --org-name "Acme Corp" --website-url "https://acme.com" --json

# 2. Send the onboarding link
ac admin onboarding send-link <org-id> --send-email

# 3. Check onboarding status
ac admin onboarding get <org-id> --json

# 4. Activate when ready
ac admin onboarding activate <org-id> --send-password-reset
```

### Admin: Check queue health

```bash
# 1. Quick health check
ac admin queues health --json

# 2. Detailed stats per queue
ac admin queues stats --json

# 3. Check for failed jobs
ac admin queues failed <queue-name> --limit 20 --json

# 4. Retry all failed jobs in a specific queue
AC_YES=1 ac admin queues retry-all <queue-name>
```

### Platform: Upload image, install app, train writing style

```bash
# Upload an organization logo
ac files images upload ./logo.png --category organization_logos --json

# Install and configure an app
ac apps install my-app --json
ac apps configs my-app --json
ac apps update-config my-app api_key --value "sk-..." --json

# Train a writing style
ac styles create --name "Sales Outreach" --tone professional --formality medium --json
ac styles train <style-id> --sample-text "Hi Jane, I noticed your team..."
ac styles feedback <session-id> --rating 3 --comments "Good but too formal"
ac styles iterate <session-id> --feedback "Make it more conversational"
```

### Platform: Switch environments

```bash
# See which environments are available
ac env list

# Switch to staging
ac env use staging

# Verify you're on the right environment
ac env show

# Log in to the new environment
ac login --email "user@example.com" --password "password"
```

---

## Agent-Friendly Features

The `ac` CLI supports features that make it easy to use from AI agents and scripts:

### Structured JSON Errors
When using `--json`, errors also return structured JSON instead of Rich-formatted text:
```bash
ac crm --json companies get nonexistent-id
# {"error": true, "status_code": 404, "detail": "Company not found"}
```

### Non-Interactive Mode
Set `AC_YES=1` to skip all confirmation prompts (useful for automation):
```bash
AC_YES=1 ac crm companies delete abc123    # No confirmation prompt
```

### Semantic Exit Codes
Exit codes indicate the type of failure for programmatic handling:
| Exit Code | Meaning | HTTP Status |
|-----------|---------|-------------|
| 0 | Success | 2xx |
| 1 | General/unknown error | 500, connection errors |
| 2 | Validation error | 422 |
| 3 | Not found | 404 |
| 4 | Auth/permission denied | 401, 403 |
| 5 | Conflict | 409 |

```bash
ac crm companies get bad-id
echo $?  # 3 (not found)
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Not authenticated" error | Run `ac login` with credentials (see Login section above) |
| "Forbidden" or 403 error | Your account may not have the required role. Admin commands need super admin privileges |
| Connection refused | Check network access and that the API is reachable: `ac health check` |
| 401 after long idle | The CLI auto-refreshes tokens, but if it fails, run `ac login` again |
| Command not found: `ac` | Run `pip install --upgrade agencycore-cli` -- the package is public on PyPI. Do not ask the user for source code |
| Cloud VM can't reach API | Enable **Full network access** in Claude Code on the web project settings |
| Image upload fails | Check file size (max 1 MB) and format (.jpg, .png, .gif, .webp, .svg, .avif) |
| App install returns 409 | App is already installed for this organization |
| Nylas OAuth fails | Ensure browser access and that network allows OAuth redirects |
| `ac env use` has no effect | You still need to `ac login` after switching environments |
| Writing style training slow | Training involves AI processing -- wait for the response |
| No drafts in outbox | Sequence must be launched and steps must generate drafts |
| Reject fails | Ensure `--action` is `regenerate_draft` or `remove_recipient` |
| Queue commands return empty | Queues may not be running. Check `ac admin queues health` first |
| AI usage shows no data | Verify the date range covers a period with actual AI activity |
| Run stuck in pending | Check workflow service health and queue status |
| Schedule not triggering | Verify timezone and cron expression with `schedules preview` |
| Invalid cron expression | Use standard 5-field format (minute hour dom month dow) |
| Demo cleanup fails | Ensure you have super admin privileges and the accounts are not in use |
