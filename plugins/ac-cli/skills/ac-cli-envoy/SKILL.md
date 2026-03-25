---
name: ac-cli-envoy
description: >
  Guide for using the AgencyCore CLI (`ac`) to manage outreach automation --
  sequences, steps, recipients, outbox (draft approval), inbox (replies),
  battlecards, and playbooks. Use this skill when someone asks about outreach
  campaigns, email sequences, draft approval workflows, inbox management,
  battlecards, playbooks, or sales signals via the command line. Also trigger
  when users mention "ac envoy", "outreach", "sequences", "drafts", "outbox",
  "inbox replies", "battlecards", or "playbooks".
allowed-tools:
  - Bash
argument-hint: "[command or question]"
---

# AgencyCore CLI -- Envoy (Outreach Automation)

The `ac envoy` commands let you manage outreach automation from the terminal --
sequences, steps, recipients, draft approval, inbox replies, battlecards, and
playbooks.

---

## Step 0: Ensure CLI Is Installed (Always Do This First)

Before running any envoy command, check if the `ac` CLI is available and install
it automatically if missing. **Do NOT ask the user where the code is -- the
package is public on PyPI.**

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
ac envoy recipients add <sequence-id> --source '[{"email":"...","name":"..."}]'
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

## Common Workflows

### Launch a new outreach sequence

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
ac envoy recipients add <sequence-id> \
  --source '[{"email":"jane@acme.com","name":"Jane Smith"}]'

# 4. Launch with a workflow
ac envoy sequences launch <sequence-id> --workflow-id <workflow-id>
```

### Review and approve drafts

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

### Manage inbox replies

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

---

## Important Patterns

### Reject Actions
When rejecting a draft, specify what should happen next:
- `regenerate_draft` -- AI generates a new draft
- `remove_recipient` -- Remove the recipient from the sequence

```bash
ac envoy outbox reject <draft-id> --action regenerate_draft --reason "Wrong tone"
```

### Step Types
- `message` -- Email step (uses template or AI prompt)
- `delay` -- Wait step (value + unit: days, hours, minutes)
- `task` -- Manual task reminder

### JSON Output
All envoy commands support `--json` for structured output:
```bash
ac envoy outbox pending --json | jq '.[].id'
```

### Non-Interactive Mode
```bash
AC_YES=1 ac envoy sequences delete <id>    # Skip confirmation
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
| Cloud VM can't reach API | Enable **Full network access** in Claude Code on the web project settings |
| No drafts in outbox | Sequence must be launched and steps must generate drafts |
| Reject fails | Ensure `--action` is `regenerate_draft` or `remove_recipient` |
