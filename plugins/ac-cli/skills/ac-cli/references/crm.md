# CRM Quick Reference

For full flag tables see `commands.md` (CRM section).

## Companies

```bash
ac crm companies list [--limit 100] [--offset 0] \
  [--approved | --unapproved] [--added-by-type user|agent] [--added-by-user <user-id>]
ac crm companies get <company-id>
ac crm companies create --name "Acme Corp" [--website https://acme.com] \
  [--industry Technology] [--lifecycle-stage lead] [--tags "hot,enterprise"]
ac crm companies update <company-id> --industry "SaaS"
ac crm companies approve --ids id1,id2,id3        # mark human-approved (ENG-819)
ac crm companies unapprove --ids id1,id2,id3      # clear approval
ac crm companies delete <company-id> [--yes]
ac crm companies bulk-delete --ids id1,id2,id3 [--yes]
```

## People (Contacts)

```bash
ac crm people list [--company-id <id>] [--limit 100] \
  [--approved | --unapproved] [--added-by-type user|agent] [--added-by-user <user-id>]
ac crm people get <person-id>
ac crm people create [--email jane@acme.com] --full-name "Jane Smith" \
  [--current-title "VP Sales"] [--company-id <id>] [--tags "decision-maker"]
ac crm people update <person-id> --current-title "CRO"
ac crm people approve --ids id1,id2,id3           # mark human-approved (ENG-819)
ac crm people unapprove --ids id1,id2,id3         # clear approval
ac crm people delete <person-id> [--yes]
ac crm people bulk-upsert --file people.json
ac crm people bulk-delete --ids id1,id2,id3 [--yes]
```

> **Bulk vs single rule**: when the user names **more than one** id for delete or upsert, ALWAYS use `bulk-delete --ids id1,id2,id3` or `bulk-upsert --file <path>`. Do not loop single `delete` calls — slower and breaks atomicity.

> **Provenance & approval (ENG-819)**: every company/person carries `created_by_user_id` (who added it manually or via CSV), `discovered_via_agent` (which agent surfaced it, e.g. `sonar`/`headhunter`), and `approved_by`/`approved_at` (human vetting). Manual + CSV adds are auto-approved; agent-discovered rows start unapproved. Filter the lists with `--approved`/`--unapproved`, `--added-by-type user|agent`, and `--added-by-user <user-id>`. Mark agent finds as vetted with `ac crm companies approve --ids ...` / `ac crm people approve --ids ...` (bulk-friendly; use `unapprove` to reverse).

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
ac crm lists lists-for-member --person-id <id>
ac crm lists lists-for-member --company-id <id>
ac crm lists bulk-remove-members <list-id> --member-type person --ids id1,id2,id3 [--yes]
ac crm lists bulk-remove-members <list-id> --member-type company --ids id1,id2,id3 [--yes]
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

## Signals (buying signals)

```bash
ac crm signals list [--signal-type funding] [--company-id <id>] [--person-id <id>] \
  [--company-ids id1,id2] [--limit 50] [--offset 0]
ac crm signals get <signal-id>
ac crm signals create --signal-type funding --description "Series B raised" \
  --company-id <id> [--signal-date 2026-05-01] [--source-url <url>] [--snippet "..."] \
  [--workflow-run-id <id>] [--source-agent manual] [--attach-score 80]
ac crm signals create --signal-type hiring --description "..." --person-id <id>
ac crm signals attach <signal-id> --company-id <id> [--score 80]
ac crm signals attach <signal-id> --person-id <id> [--score 80]
ac crm signals delete <signal-id> [--yes]
```

`signal_type` enum: `hiring`, `tech_stack`, `funding`, `content`, `leadership`, `growth`, `competitor`, `compliance`, `event`, `news`, `product`, `expansion`, `partnership`.

> **`crm signals` vs `envoy signals`**: `ac crm signals` is the CRM signals store (CRUD on standalone signal records attached to companies/people). `ac envoy signals <recipient-id>` returns sales signals for a sequence recipient. Different APIs — do not conflate.
