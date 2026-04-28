# Envoy (Outreach) Quick Reference

For full flag tables see `commands.md` (Envoy section).

## Sequences

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
ac envoy sequences duplicate <sequence-id>
ac envoy sequences archive <sequence-id>
ac envoy sequences restore <sequence-id>
ac envoy sequences impact-preview <sequence-id> --step-id <id> [--step-id <id> ...]
ac envoy sequences bulk-remove-recipients <sequence-id> --recipient-id <id> [--recipient-id <id> ...]
ac envoy sequences classify-step-subtype "Send a manual follow-up email"
ac envoy sequences outputs <sequence-id> [--limit 50] [--offset 0]
ac envoy sequences generate-drafts <sequence-id> <step-id> --workflow-id <id>
```

## Campaigns

```bash
ac envoy campaigns list [--archived] [--query "..."] [--limit 50]
ac envoy campaigns get <campaign-id>
ac envoy campaigns create --name "Q2 Outreach" [--description "..."] \
  [--goal "10 demos"] [--source-app envoy] [--started-at 2026-04-01] [--ended-at 2026-06-30]
ac envoy campaigns update <campaign-id> --name "Q2 Renamed"
ac envoy campaigns delete <campaign-id> [--yes]
ac envoy campaigns archive <campaign-id>
ac envoy campaigns unarchive <campaign-id>
```

## Steps

```bash
ac envoy steps create <sequence-id> --type message [--step-order 1] \
  [--message-template "Hi {{name}}..."] [--prompt "Write a cold intro"]
ac envoy steps update <sequence-id> <step-id> [--message-template "..."]
ac envoy steps delete <sequence-id> <step-id> [--yes]
ac envoy steps reorder <sequence-id> --step-ids id1,id2,id3
ac envoy steps stats <sequence-id>
```

Step types: `message` (email, template or AI prompt) · `delay` (value + unit: days/hours/minutes) · `task` (manual reminder)

## Recipients

```bash
ac envoy recipients list <sequence-id> [--status pending] [--step-id <id>]
ac envoy recipients add <sequence-id> --prospect-ids id1,id2,id3
ac envoy recipients add <sequence-id> --crm-list-id <list-id>
ac envoy recipients add <sequence-id> --source '{"type":"explicit","prospect_ids":["..."]}' # Advanced
ac envoy recipients remove <sequence-id> <recipient-id> [--yes]
```

## Outbox (Draft Approval)

```bash
ac envoy outbox pending [--sequence-id <id>] [--limit 50]
ac envoy outbox sent [--sequence-id <id>] [--status delivered] [--limit 50]
ac envoy outbox step-drafts --sequence-id <id> --step-id <id> [--limit 50]
ac envoy outbox update-draft <draft-id> [--subject "New subject"] [--body "..."]
ac envoy outbox approve <draft-id> [--subject "Override"] [--body "Override"]
ac envoy outbox reject <draft-id> --action regenerate_draft [--reason "Too formal"]
ac envoy outbox regenerate <draft-id> [--instruction "Make it shorter"]
```

Reject `--action` values: `regenerate_draft` (AI rewrites) · `remove_recipient` (drop from sequence).

## Inbox (Replies)

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

**Standard "read first thread + reply" recipe** — when the user asks to read messages then reply, chain all three steps in one call:

```bash
ac envoy inbox list --status open --json && \
ac envoy inbox messages <thread-id> && \
ac envoy inbox reply <thread-id> --body "..."
```

## Battlecards

```bash
ac envoy battlecards list [--query "competitor"] [--limit 50]
ac envoy battlecards get <battlecard-id>
ac envoy battlecards create --name "vs Competitor X" [--competitor-name "X"]
ac envoy battlecards update <battlecard-id> --description "Updated positioning"
ac envoy battlecards delete <battlecard-id> [--yes]
ac envoy battlecards duplicate <battlecard-id>
```

## Playbooks

```bash
ac envoy playbooks list [--query "enterprise"] [--limit 50]
ac envoy playbooks get <playbook-id>
ac envoy playbooks create --name "Enterprise Outreach" [--description "..."]
ac envoy playbooks update <playbook-id> --name "Updated Playbook"
ac envoy playbooks delete <playbook-id> [--yes]
ac envoy playbooks duplicate <playbook-id>
```

## Dashboard, Signals & Inbox Count

```bash
ac envoy dashboard                          # Outreach stats overview
ac envoy signals <recipient-id>             # Sales signals for a recipient
ac envoy inbox-count                        # Total inbox thread count
```
