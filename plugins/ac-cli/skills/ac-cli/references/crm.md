# CRM Quick Reference

For full flag tables see `commands.md` (CRM section).

## Companies

```bash
ac crm companies list [--limit 100] [--offset 0]
ac crm companies get <company-id>
ac crm companies create --name "Acme Corp" [--website https://acme.com] \
  [--industry Technology] [--lifecycle-stage lead] [--tags "hot,enterprise"]
ac crm companies update <company-id> --industry "SaaS"
ac crm companies delete <company-id> [--yes]
```

## People (Contacts)

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

> **Bulk vs single rule**: when the user names **more than one** id for delete or upsert, ALWAYS use `bulk-delete --ids id1,id2,id3` or `bulk-upsert --file <path>`. Do not loop single `delete` calls — slower and breaks atomicity.

## Deals

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

## Activities (Tasks)

```bash
ac crm activities list [--deal-id <id>] [--type call] [--status pending]
ac crm activities get <activity-id>
ac crm activities create --type call --title "Follow up with Jane" \
  [--due-date 2026-03-20] [--priority high] [--deal-id <id>] [--contact-id <id>]
ac crm activities update <activity-id> --priority urgent
ac crm activities complete <activity-id>
ac crm activities delete <activity-id> [--yes]
```

## Communications (Email & Messages)

```bash
ac crm comms list [--company-id <id>] [--contact-id <id>] [--type email]
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

# Approval workflow (awaiting_approval status)
ac crm comms pending-approvals [--sequence-id <id>] [--step-id <id>]
ac crm comms approve <communication-id>
ac crm comms reject <communication-id> --action skip_send [--reason "..."]
ac crm comms regenerate <communication-id>
```

## Lists

```bash
ac crm lists list
ac crm lists get <list-id>
ac crm lists create --name "Q2 Targets" [--member-type person] [--type static]
ac crm lists add-member <list-id> --person-id <id>
ac crm lists remove-member <list-id> --person-id <id>
ac crm lists members <list-id>
ac crm lists delete <list-id> [--yes]
```

## Import

```bash
ac crm import preview --file contacts.json    # Preview what will be imported
ac crm import commit --preview-id <id>        # Apply the import
```

Always `preview` first; `commit` is irreversible.

## Search & Dashboard

```bash
ac crm search "acme"                    # Search across companies, contacts, deals
ac crm dashboard [--period 30]          # Pipeline metrics for the last N days
```

## Engagement Dashboard

```bash
ac crm engagement-dashboard [--period 30]    # Email engagement metrics
```

Returns: emails sent (current/previous/change), open rate, click rate, reply rate, bounce rate, email health score, top clicked links.
