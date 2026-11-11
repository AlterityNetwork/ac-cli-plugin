# Inbox (`ac inbox`)

One inbox for every inbound email and LinkedIn item from a CRM person, in a
sequence or not. One row is one person. A person's email and LinkedIn
conversations share the row, and `show` merges them into one timeline.

Every `<thread-id>` is an inbox thread id. A command on a person takes any
thread of the person.

## Read

```bash
ac inbox list                                   # Mine, open, newest activity first
ac inbox list --owner all --needs-reply --unread
ac inbox list --channel linkedin --intent interested --intent none
ac inbox list --kind connection --sequence any --since 2026-11-01 --q acme
ac inbox list --view done --limit 20 --offset 20
ac inbox show <thread-id>                       # timeline + who can reply on each channel
ac inbox messages --view sent|drafts|scheduled [--channel email|linkedin] [--owner all]
ac inbox counts                                 # badge: unread messages + waiting connection requests
ac inbox resolve --message-id thread_<id> | --comm-id <id> | --contact-id <person-id>
```

- `--owner` is `me` (the default), `all` or a user id.
- `--kind` is `message`, `connection` (accepted and received requests) or
  `engagement` (comments and reactions).
- `--sequence` is `any`, `none` or a sequence id.
- `--intent none` keeps people with no intent.

## Shared state

Done, open and snoozed apply to every conversation of the person, for everyone
in the organization. Read and unread are per user.

```bash
ac inbox status <thread-id> --status done
ac inbox status <thread-id> --status snoozed --until 2026-11-09T09:00:00Z
ac inbox status <thread-id> --status open
ac inbox read <thread-id>
ac inbox unread <thread-id>
ac inbox intent <thread-id> --intent interested|not_interested|out_of_office|none
ac inbox bulk --ids <id>,<id> --action done|read|unread
```

## Reply and new message

Only the owner of the connected account replies (exit 4 otherwise). A
disconnected account exits 5. Check `ac inbox show <thread-id>` first: each
channel says `can_reply` and the reason.

```bash
ac inbox reply <thread-id> --channel email --body "..." [--subject "..."] [--cc a@x.test] [--send-at 2026-11-09T09:00:00Z]
ac inbox reply <thread-id> --channel linkedin --body "..."     # at most 1000 characters
ac inbox send --contact-id <person-id> --channel email --subject "..." --body "..."
ac inbox send --contact-id <person-id> --channel linkedin --body "..."
ac inbox ask-to-reply <thread-id>                               # notify the owner
```

A LinkedIn message counts against the account's daily message budget and waits
for its send window. Outside the window the answer is `scheduled` with
`sends_at`, and the message appears in `ac inbox messages --view scheduled`.
With LinkedIn off for the organization, a LinkedIn reply exits 3.

## AI draft

The Email or LinkedIn writer drafts a reply from the conversations and the CRM
record. The draft never sends.

```bash
ac inbox ai-draft <thread-id> --channel email --wait
ac inbox ai-draft <thread-id> --channel linkedin --regenerate --wait
```

Without `--wait` the command prints the draft id. The API answers the draft at
`GET /api/v1/inbox/ai-drafts/<draft-id>`.

## Inbox or Sequences inbox

`ac sequences inbox` is the Sequences inbox: sequence replies only. `ac inbox` holds
every conversation with a CRM person. Use `ac inbox` unless the user names the
Sequences inbox.
