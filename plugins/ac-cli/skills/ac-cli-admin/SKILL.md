---
name: ac-cli-admin
description: >
  Guide for using the AgencyCore CLI (`ac`) admin commands -- user management,
  organization management, app usage analytics, AI usage monitoring, queue
  management, demo accounts, and onboarding. Use this skill when someone asks
  about admin operations, user analytics, AI costs, token usage, app usage
  metrics, queue health, or super-admin tasks. Also trigger when users mention
  "ac admin", "admin dashboard", "usage stats", or "AI costs".
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
ac admin users list [--query "jane"] [--sort created_at] [--order desc] [--limit 50] [--offset 0]
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
ac admin orgs list [--query "acme"] [--sort created_at] [--order desc] [--limit 50] [--offset 0]
ac admin orgs get <org-id>
ac admin orgs create --name "Acme Corp" [--slug acme-corp] [--plan pro]
ac admin orgs update <org-id> [--name "New Name"] [--slug new-slug] [--plan enterprise]
ac admin orgs delete <org-id> [--yes]
ac admin orgs members <org-id> [--limit 50] [--offset 0]
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
ac admin queues job-performance
ac admin queues failed [--limit 50] [--queue <queue-name>]
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
ac admin demo list-accounts [--limit 50] [--offset 0] [--sort created_at] [--order desc]
ac admin demo get-account <org-id>
ac admin demo update-account <org-id> [--status active] [--notes "Updated demo"]
ac admin demo delete-account <org-id> [--yes]
ac admin demo cleanup [--max-age-days 30] [--yes]
ac admin demo stats
```

### Onboarding

```bash
ac admin onboarding create --email user@example.com --first-name "Jane" \
  --last-name "Smith" --org-name "Acme Corp" --website-url "https://acme.com"
ac admin onboarding list [--status pending] [--query "acme"] [--limit 50] [--offset 0]
ac admin onboarding get <org-id>
ac admin onboarding delete <org-id>
ac admin onboarding send-link <org-id> [--send-email]
ac admin onboarding impersonate <org-id>
ac admin onboarding end-impersonation <org-id>
ac admin onboarding activate <org-id> [--send-password-reset/--no-send-password-reset]
ac admin onboarding deactivate <org-id>
ac admin onboarding update-config [--show-calendly] [--calendly-url "https://..."]
ac admin onboarding get-settings
ac admin onboarding update-settings [--terms-html "<p>...</p>"] \
  [--calendly-url "https://..."] [--calendly-enabled]
```

### App Usage

```bash
ac admin app-usage summary [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin app-usage users [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>] \
  [--sort total_actions] [--order desc] [--limit 50] [--offset 0] [--search "jane"]
ac admin app-usage user <user-id> [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
```

### AI Usage

```bash
ac admin ai-usage summary [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin ai-usage users [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>] \
  [--sort total_tokens] [--order desc] [--limit 50] [--offset 0] [--search "jane"]
ac admin ai-usage user <user-id> [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin ai-usage by-model [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin ai-usage by-workflow [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin ai-usage details [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>] \
  [--limit 50] [--offset 0] [--model-id <id>] [--user-id <id>] [--workflow-run-id <id>]
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
ac admin queues failed --limit 20 --json

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
