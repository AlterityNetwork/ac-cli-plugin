# Sequences (`ac sequences`) Quick Reference

For full flag tables see `commands.md` (Sequences section).

## Sequences

```bash
ac sequences sequences list [--status active]
ac sequences sequences get <sequence-id>
ac sequences sequences create --name "Q2 Outreach" [--description "..."] \
  [--writing-style-id <id>] [--playbook-id <id>] [--crm-list-id <id>]
ac sequences sequences update <sequence-id> --name "Updated Name"
ac sequences sequences update <sequence-id> --draft-feedback "Write in British English."
ac sequences sequences update <sequence-id> --no-auto-enrich   # skip a recipient with no email, phone or LinkedIn URL at once
ac sequences sequences delete <sequence-id> [--yes]
ac sequences sequences launch <sequence-id> --workflow-id <id>
ac sequences sequences pause <sequence-id>
ac sequences sequences resume <sequence-id> --workflow-id <id>
ac sequences sequences duplicate <sequence-id>
ac sequences sequences archive <sequence-id>
ac sequences sequences restore <sequence-id>
ac sequences sequences impact-preview <sequence-id> --step-id <id> [--step-id <id> ...]
ac sequences sequences bulk-remove-recipients <sequence-id> --recipient-id <id> [--recipient-id <id> ...]
ac sequences sequences classify-step-subtype "Send a manual follow-up email"
ac sequences sequences outputs <sequence-id> [--limit 50] [--offset 0]
ac sequences sequences generate-drafts <sequence-id> <step-id> --workflow-id <id>
ac sequences sequences for-prospect <prospect-id>          # Sequences containing a given person
```

## Steps

```bash
ac sequences steps create <sequence-id> --type message [--step-order 1] \
  [--message-template "Hi {{name}}..."] [--prompt "Write a cold intro"]
ac sequences steps update <sequence-id> <step-id> [--message-template "..."]
ac sequences steps delete <sequence-id> <step-id> [--yes]
ac sequences steps reorder <sequence-id> --step-ids id1,id2,id3
ac sequences steps stats <sequence-id>
```

Step types: `message` (email, template or AI prompt) · `delay` (value + unit: days/hours/minutes) · `task` (manual reminder)

## Recipients

```bash
ac sequences recipients list <sequence-id> [--status pending] [--step-id <id>]
ac sequences recipients add <sequence-id> --prospect-ids id1,id2,id3
ac sequences recipients add <sequence-id> --crm-list-id <list-id>
ac sequences recipients add <sequence-id> --prospect-ids id1 --reenroll   # re-add previously-removed
ac sequences recipients add <sequence-id> --source '{"type":"explicit","prospect_ids":["..."]}' # Advanced
ac sequences recipients remove <sequence-id> <recipient-id> [--yes]
ac sequences recipients history <sequence-id> <recipient-id>   # every step, the email thread + the completed tasks
```

`add` returns `{added, already_active, requires_confirmation}`. Re-adding an
already-active prospect is a safe silent skip. Re-adding someone previously
removed (or whose enrolment completed/errored) is NOT silent — it lands in
`requires_confirmation` and is only reactivated with `--reenroll` / `--force`
(or by confirming the interactive prompt; set `AC_YES=1` to auto-confirm).
Re-adding may send them outreach again, so confirm intentionally.

## Outbox (Draft Approval)

```bash
ac sequences outbox pending [--sequence-id <id>] [--limit 50]
ac sequences outbox sent [--sequence-id <id>] [--status delivered] [--limit 50]
ac sequences outbox step-drafts --sequence-id <id> --step-id <id> [--limit 50]
ac sequences outbox update-draft <draft-id> [--subject "New subject"] [--body "..."]
ac sequences outbox approve <draft-id> [--subject "Override"] [--body "Override"]
ac sequences outbox reject <draft-id> --action regenerate [--reason "Too formal"]
ac sequences outbox regenerate <draft-id> [--instruction "Make it shorter"] \
  [--apply-to-sequence] [--apply-to-writing-style] [--scope draft|step]
```

`--apply-to-sequence` saves the instruction as draft feedback on the sequence. Every later draft of the sequence applies it, together with the writing style. `--apply-to-writing-style` rewrites your writing style for the sequence with the instruction first, so the new drafts follow it. `--scope step` also regenerates every other waiting draft of the same step, and discards any edits on those drafts.

Reject `--action` values: `regenerate` (AI rewrites) · `remove_recipient` (drop from sequence) · `skip_send` (skip this draft, keep the recipient) · `manual_edit` (edit and resend later).

## Inbox (Replies)

```bash
ac sequences inbox list [--status open] [--sentiment positive] [--limit 50]
ac sequences inbox messages <thread-id>
ac sequences inbox archive <thread-id>
ac sequences inbox unarchive <thread-id>
ac sequences inbox assign <thread-id> --user-id <id>
ac sequences inbox snooze <thread-id> --until "2026-04-01T09:00:00"
ac sequences inbox complete <thread-id>
ac sequences inbox mark-read <thread-id>
ac sequences inbox update-status <thread-id> --status resolved
ac sequences inbox add-tags <thread-id> --tags "hot-lead,priority"
ac sequences inbox remove-tags <thread-id> --tags "stale"
ac sequences inbox reply <thread-id> --body "Thanks for your reply!"
```

The list holds only threads with at least one reply from the prospect, by email or LinkedIn. A thread of sent emails only is not listed; read sent emails with `ac sequences sequences outputs <sequence-id>`. The Channel column is `email` or `linkedin`. Each item in `--json` carries `unread_count`: the received messages you have not read. `mark-read` clears it for you only. `reply` sends an email, so it refuses a LinkedIn thread: answer that person on LinkedIn.

**Standard "read first thread + reply" recipe** — when the user asks to read messages then reply, chain all three steps in one call:

```bash
ac sequences inbox list --status open --json && \
ac sequences inbox messages <thread-id> && \
ac sequences inbox reply <thread-id> --body "..."
```

## Battlecards

```bash
ac sequences battlecards list [--query "competitor"] [--limit 50]
ac sequences battlecards get <battlecard-id>
ac sequences battlecards create --name "vs Competitor X" [--competitor-name "X"]
ac sequences battlecards update <battlecard-id> --description "Updated positioning"
ac sequences battlecards delete <battlecard-id> [--yes]
ac sequences battlecards duplicate <battlecard-id>
```

## Playbooks

```bash
ac sequences playbooks list [--query "enterprise"] [--limit 50]
ac sequences playbooks get <playbook-id>
ac sequences playbooks create --name "Enterprise Outreach" [--description "..."] [--icp-id <profile-id>]
ac sequences playbooks update <playbook-id> --name "Updated Playbook" [--icp-id <profile-id>]
ac sequences playbooks delete <playbook-id> [--yes]
ac sequences playbooks duplicate <playbook-id>
```

Repeat `--icp-id` to target several ideal customer profiles on an offer. Omitting it on update preserves the existing selection.

## Dashboard, Signals & Inbox Count

```bash
ac sequences dashboard                          # Sequences stats overview
ac sequences signals <recipient-id>             # Sales signals for a recipient (positional, NOT --recipient-id)
ac sequences inbox-count                        # Total inbox thread count
```

> "Signals for recipient X" → `ac sequences signals X` (positional). Do not use `ac sequences signals list --recipient-id` or `ac sequences signals for X` — those subcommands do not exist.

> "How many threads in my inbox" → `ac sequences inbox-count` (single dedicated command). Do not pipe `inbox list --json | jq length` when a count command exists.
