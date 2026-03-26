---
name: ac-cli-admin
description: >
  Guide for using the AgencyCore CLI (`ac`) admin commands -- user management,
  organization management, app usage analytics, AI usage monitoring, platform
  activity monitoring, legal document management, queue management, demo
  accounts, and onboarding. Use this skill when someone asks about admin
  operations, user analytics, AI costs, token usage, app usage metrics, queue
  health, super-admin tasks, platform activity, user activity tracking, legal
  documents, terms of service, or privacy policy management. Also trigger when
  users mention "ac admin", "admin dashboard", "usage stats", "AI costs",
  "platform activity", "legal documents", "user activity".
allowed-tools:
  - Bash
argument-hint: "[command or question]"
---

# AgencyCore CLI -- Admin Operations

The `ac` CLI lets super admins manage users, organizations, queues, demo
accounts, onboarding, and monitor app/AI usage from the terminal. This guide
covers setup, authentication, every admin command, and common workflows.

---

## Step 0: Ensure CLI Is Installed (Always Do This First)

Before running any admin command, check if the `ac` CLI is available and install
it automatically if missing. **Do NOT ask the user where the code is -- the
package is public on PyPI.**

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

## Step 1: Authentication Check (Must Be Super Admin)

Admin commands require super admin privileges. Verify:

```bash
ac whoami
```

- **If authenticated**: Check for `superadmin` role in the output. If the user
  is not a super admin, inform them that admin commands require elevated
  privileges.
- **If not authenticated** (error or "not logged in"): Ask the user for their
  email and password, then log them in:

```bash
ac login --email "user@example.com" --password "their-password"
```

After login, verify with `ac whoami` and confirm super admin role.

---

## Output Modes

Every admin command supports two output styles:

- **Rich output** (default) -- formatted tables and panels, good for reading
- **JSON output** (`--json`) -- raw JSON, good for piping into other tools like `jq`

```bash
ac admin users list              # Pretty table
ac admin users list --json       # Raw JSON for scripting
```

## Quick Reference

Read `references/commands.md` for the full command reference with all flags and
options. Below is an overview of what's available.

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

---

## App Usage Commands

Track how users interact with the AgencyCore application.

### Summary

Get an overview of app usage across the platform:

```bash
ac admin app-usage summary --json
```

Filter by date range and/or organization:

```bash
ac admin app-usage summary --start-date 2026-03-01 --end-date 2026-03-23 --org-id <id> --json
```

### Top Users by Activity

```bash
ac admin app-usage users --sort total_actions --order desc --limit 10 --json
```

Search for a specific user:

```bash
ac admin app-usage users --search "jane@example.com" --json
```

### Individual User Detail

```bash
ac admin app-usage user <user-id> --start-date 2026-03-01 --json
```

---

## AI Usage Commands

Monitor AI token consumption, costs, and usage patterns.

### Summary

Get a high-level overview of AI usage (tokens, cost, request count):

```bash
ac admin ai-usage summary --json
```

### Top AI Users

Find who's using the most AI resources:

```bash
ac admin ai-usage users --sort total_tokens --order desc --limit 10 --json
```

### Usage by Model

See which AI models are consuming the most tokens:

```bash
ac admin ai-usage by-model --start-date 2026-03-01 --json
```

### Usage by Workflow

See which AI workflows are consuming the most tokens:

```bash
ac admin ai-usage by-workflow --start-date 2026-03-01 --json
```

### Detailed Usage Logs

Drill into individual AI usage records:

```bash
ac admin ai-usage details --user-id <id> --limit 20 --json
```

Filter by model or workflow run:

```bash
ac admin ai-usage details --model-id <id> --workflow-run-id <id> --json
```

---

## Platform Activity Commands

Monitor how users interact with the platform.

### Summary

Get an overview of platform activity:

```bash
ac admin platform-activity summary --json
```

Filter by date range:

```bash
ac admin platform-activity summary --start-date 2026-03-01 --end-date 2026-03-23 --json
```

### Most Active Users

```bash
ac admin platform-activity users --sort total_events --order desc --page-size 10 --json
```

### Individual User Activity

```bash
ac admin platform-activity user <user-id> --start-date 2026-03-01 --json
```

---

## Legal Document Commands

Manage terms of service, privacy policies, and other legal documents.

### List Documents

```bash
ac admin legal-docs list --json
ac admin legal-docs list --document-type terms_of_service --json
```

### Create a New Version

```bash
ac admin legal-docs create --document-type terms_of_service \
  --version "2.0" --title "Terms of Service v2" \
  --content-html "<p>Updated terms...</p>" --json
```

### Set as Current

```bash
ac admin legal-docs set-current <document-id>
```

### Delete a Document

```bash
AC_YES=1 ac admin legal-docs delete <document-id>
```

---

## Common Workflows

### Check who's using the most AI tokens this month

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

### Check queue health

```bash
# 1. Quick health check
ac admin queues health --json

# 2. Detailed stats per queue
ac admin queues stats --json

# 3. Check for failed jobs
ac admin queues failed <queue-name> --limit 20 --json

# 4. Retry all failed jobs in a specific queue
AC_YES=1 ac admin queues retry-all <queue-name>

# 5. Clear failed jobs if they can't be recovered
AC_YES=1 ac admin queues clear-failed <queue-name>
```

### Manage demo accounts

```bash
# 1. Scrape a real website for demo data
ac admin demo scrape-website --url "https://example.com" --json

# 2. Generate an org profile for a demo
ac admin demo generate-org --industry "Technology" --size "medium" --json

# 3. Prepare a full demo account
ac admin demo prepare-account --org-name "Demo Corp" --json

# 4. List existing demo accounts
ac admin demo list-accounts --json

# 5. Clean up old demo accounts
AC_YES=1 ac admin demo cleanup --max-age-days 30
```

### Onboard a new customer

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

### Investigate a user's app and AI usage

```bash
# 1. Search for the user
ac admin users search --email "jane@example.com" --json

# 2. Check their app usage
ac admin app-usage user <user-id> --start-date 2026-03-01 --json

# 3. Check their AI usage
ac admin ai-usage user <user-id> --start-date 2026-03-01 --json
```

### Monitor platform activity

```bash
# 1. Get activity summary for this month
ac admin platform-activity summary --start-date 2026-03-01 --json

# 2. Get most active users
ac admin platform-activity users --sort total_events --order desc --page-size 10 --json

# 3. Drill into a specific user
ac admin platform-activity user <user-id> --start-date 2026-03-01 --json
```

### Manage legal documents

```bash
# 1. List current documents
ac admin legal-docs list --json

# 2. Create a new version
ac admin legal-docs create --document-type terms_of_service \
  --version "2.0" --title "Terms of Service v2" --json

# 3. Set it as the current version
ac admin legal-docs set-current <document-id>
```

---

## Agent-Friendly Features

### JSON Output

All admin command groups support `--json` for structured output. Always prefer
JSON mode when you need to parse results or chain commands:

```bash
ac admin users list --json | jq '.[].id'
ac admin ai-usage summary --json | jq '.total_cost'
```

### Structured JSON Errors

When using `--json`, errors return a structured object instead of rich text:

```json
{"error": true, "status_code": 404, "detail": "User not found"}
```

This makes it easy to detect and handle errors programmatically.

### Non-Interactive Mode

Set `AC_YES=1` to skip all confirmation prompts (useful for scripting and
automation):

```bash
AC_YES=1 ac admin users delete <user-id>
AC_YES=1 ac admin queues retry-all <queue-name>
AC_YES=1 ac admin demo cleanup --max-age-days 30
```

### Semantic Exit Codes

The CLI uses semantic exit codes for programmatic error handling:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Validation error (422) |
| 3 | Not found (404) |
| 4 | Auth/permission error (401/403) |
| 5 | Conflict (409) |

Example usage in scripts:

```bash
ac admin users get <user-id> --json
case $? in
  0) echo "Found user" ;;
  3) echo "User not found" ;;
  4) echo "Not authorized -- are you a super admin?" ;;
  *) echo "Unexpected error" ;;
esac
```

---

## Auth Commands Reference

| Command | What it does |
|---------|-------------|
| `ac login` | Sign in (stores credentials locally) |
| `ac logout` | Clear stored credentials |
| `ac whoami` | Show your user info, organization, and role |
| `ac health check` | Verify the API is reachable (no auth needed) |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Not authenticated" error | Run `ac login` with super admin credentials |
| "Forbidden" or 403 error | Your account is not a super admin. Contact an existing admin to grant access |
| Connection refused | Check network access and that the API is reachable: `ac health check` |
| 401 after long idle | The CLI auto-refreshes tokens, but if it fails, run `ac login` again |
| Command not found: `ac` | Run `pip install --upgrade agencycore-cli` -- the package is public on PyPI. Do not ask the user for source code |
| Cloud VM can't reach API | Enable **Full network access** in Claude Code on the web project settings |
| Queue commands return empty | Queues may not be running. Check `ac admin queues health` first |
| AI usage shows no data | Verify the date range covers a period with actual AI activity |
| Demo cleanup fails | Ensure you have super admin privileges and the accounts are not in use |
