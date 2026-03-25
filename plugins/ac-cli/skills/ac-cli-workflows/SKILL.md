---
name: ac-cli-workflows
description: >
  Guide for using the AgencyCore CLI (`ac`) to manage workflow automation --
  runs, schedules, and presets. Use this skill when someone asks about workflow
  runs, cron schedules, workflow presets, run logs, or automating recurring
  tasks. Also trigger when users mention "ac workflows", "workflow runs",
  "cron schedule", "workflow presets", or "run logs".
allowed-tools:
  - Bash
argument-hint: "[command or question]"
---

# AgencyCore CLI -- Workflow Automation

The `ac workflows` commands let you manage workflow runs, cron schedules, and
presets from the terminal.

---

## Step 0: Ensure CLI Is Installed (Always Do This First)

Before running any workflow command, check if the `ac` CLI is available and
install it automatically if missing. **Do NOT ask the user where the code is --
the package is public on PyPI.**

```bash
pip install --upgrade agencycore-cli
```

If `pip` is not available, try `uv pip install --upgrade agencycore-cli` or `pipx upgrade agencycore-cli`.

Then verify it works:
```bash
ac --help
```

---

## Step 1: Authentication Check

Verify the user is authenticated:

```bash
ac whoami
```

- **If authenticated**: Proceed to the command the user needs.
- **If not authenticated**: Ask for email and password, then run:
  ```bash
  ac login --email "user@example.com" --password "their-password"
  ```

---

## Quick Reference

Read `references/commands.md` for the full command reference with all flags.

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

---

## Common Workflows

### Schedule a recurring workflow

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

### Trigger and monitor a workflow run

```bash
# 1. Create a new run
ac workflows runs create <workflow-id> --input '{"param":"value"}' --json

# 2. Check run status
ac workflows runs get <workflow-id> <run-id> --json

# 3. View run logs
ac workflows runs logs <workflow-id> <run-id> --json
```

### Manage workflow presets

```bash
# 1. Create a preset with saved configuration
ac workflows presets create <workflow-id> --name "Enterprise Sync" \
  --config '{"batch_size": 100, "mode": "full"}' --json

# 2. List available presets
ac workflows presets list <workflow-id> --json
```

---

## Important Patterns

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

### JSON Input
Pass structured data to workflow runs and presets as JSON strings:
```bash
--input '{"company_id": "abc123", "mode": "incremental"}'
--config '{"batch_size": 50}'
```

### Toggle Schedules
Enable or disable a schedule without deleting it:
```bash
ac workflows schedules toggle <workflow-id> <schedule-id> --enabled
ac workflows schedules toggle <workflow-id> <schedule-id> --disabled
```

### JSON Output
All workflow commands support `--json` for structured output:
```bash
ac workflows runs list <workflow-id> --json | jq '.[].status'
```

### Non-Interactive Mode
```bash
AC_YES=1 ac workflows schedules delete <workflow-id> <schedule-id>
```

### Semantic Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Validation error (422) |
| 3 | Not found (404) |
| 4 | Auth/permission (401/403) |
| 5 | Conflict (409) |

---

## Auth Commands Reference

| Command | What it does |
|---------|-------------|
| `ac login` | Sign in (stores credentials locally) |
| `ac logout` | Clear stored credentials |
| `ac whoami` | Show your user info and organization |
| `ac health check` | Verify the API is reachable (no auth needed) |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Not authenticated" error | Run `ac login` with credentials |
| Connection refused | Check `ac health check` |
| Command not found: `ac` | Run `pip install --upgrade agencycore-cli` |
| Run stuck in pending | Check workflow service health and queue status |
| Schedule not triggering | Verify timezone and cron expression with `schedules preview` |
| Invalid cron expression | Use standard 5-field format (minute hour dom month dow) |
