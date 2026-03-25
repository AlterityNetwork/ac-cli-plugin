# AC CLI -- Envoy Command Reference

Complete flag reference for all envoy (outreach automation) commands. All
commands require authentication (`ac login`).

## Table of Contents

1. [Sequences](#sequences)
2. [Steps](#steps)
3. [Recipients](#recipients)
4. [Outbox](#outbox)
5. [Inbox](#inbox)
6. [Battlecards](#battlecards)
7. [Playbooks](#playbooks)
8. [Dashboard, Signals & Inbox Count](#dashboard-signals--inbox-count)

---

## Sequences

### `ac envoy sequences list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--status` | str | None | Filter by sequence status |
| `--json` | flag | off | Raw JSON output |

### `ac envoy sequences get <sequence-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac envoy sequences create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Sequence name |
| `--description` | str | no | Sequence description |
| `--writing-style-id` | str | no | Writing style to use for AI drafts |
| `--playbook-id` | str | no | Playbook to guide messaging |
| `--crm-list-id` | str | no | CRM list to source recipients from |
| `--execution-mode` | str | no | Execution mode |
| `--json` | flag | no | Raw JSON output |

### `ac envoy sequences update <sequence-id>`
Same optional flags as `create`. Only provided fields are updated.

### `ac envoy sequences delete <sequence-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac envoy sequences launch <sequence-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--workflow-id` | str | yes | Workflow to use for execution |
| `--json` | flag | no | Raw JSON output |

### `ac envoy sequences pause <sequence-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Pauses a running sequence. No new steps will execute until resumed.

### `ac envoy sequences resume <sequence-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--workflow-id` | str | yes | Workflow to use for resumed execution |
| `--json` | flag | no | Raw JSON output |

---

## Steps

### `ac envoy steps create <sequence-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--type` | str | yes | Step type (message, delay, task) |
| `--step-order` | int | no | Position in sequence |
| `--message-template` | str | no | Email template text |
| `--prompt` | str | no | AI prompt for draft generation |
| `--delay-value` | int | no | Delay duration (for delay steps) |
| `--delay-unit` | str | no | Delay unit (days, hours, minutes) |
| `--json` | flag | no | Raw JSON output |

### `ac envoy steps update <sequence-id> <step-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--message-template` | str | Update email template |
| `--prompt` | str | Update AI prompt |
| `--delay-value` | int | Update delay duration |
| `--delay-unit` | str | Update delay unit |
| `--json` | flag | Raw JSON output |

### `ac envoy steps delete <sequence-id> <step-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac envoy steps reorder <sequence-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--step-ids` | str | yes | Comma-separated step IDs in desired order |
| `--json` | flag | no | Raw JSON output |

### `ac envoy steps stats <sequence-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Shows execution statistics for each step in the sequence.

---

## Recipients

### `ac envoy recipients list <sequence-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--status` | str | None | Filter by recipient status |
| `--step-id` | str | None | Filter by current step |
| `--json` | flag | off | Raw JSON output |

### `ac envoy recipients add <sequence-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--source` | str | yes | JSON array of recipients (e.g. `[{"email":"...","name":"..."}]`) |
| `--json` | flag | no | Raw JSON output |

### `ac envoy recipients remove <sequence-id> <recipient-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

---

## Outbox

### `ac envoy outbox pending`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--sequence-id` | str | None | Filter by sequence |
| `--step-id` | str | None | Filter by step |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

Lists drafts awaiting approval.

### `ac envoy outbox sent`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--sequence-id` | str | None | Filter by sequence |
| `--status` | str | None | Filter by delivery status |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

### `ac envoy outbox step-drafts`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--sequence-id` | str | yes | Sequence ID |
| `--step-id` | str | yes | Step ID |
| `--limit` | int | no | Max results (default: 50) |
| `--offset` | int | no | Skip results (default: 0) |
| `--json` | flag | no | Raw JSON output |

Lists all drafts for a specific step.

### `ac envoy outbox update-draft <draft-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--subject` | str | New subject line |
| `--body` | str | New email body |
| `--json` | flag | Raw JSON output |

### `ac envoy outbox approve <draft-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--subject` | str | Override subject before sending |
| `--body` | str | Override body before sending |
| `--json` | flag | Raw JSON output |

Approves and sends the draft.

### `ac envoy outbox reject <draft-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--action` | str | yes | What to do next: `regenerate_draft` or `remove_recipient` |
| `--reason` | str | no | Reason for rejection (used as AI context for regeneration) |
| `--json` | flag | no | Raw JSON output |

### `ac envoy outbox regenerate <draft-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--instruction` | str | Additional instruction for AI regeneration |
| `--json` | flag | Raw JSON output |

---

## Inbox

### `ac envoy inbox list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--status` | str | None | Filter by thread status |
| `--sentiment` | str | None | Filter by sentiment (positive, negative, neutral) |
| `--sequence-id` | str | None | Filter by source sequence |
| `--assigned-to` | str | None | Filter by assigned user ID |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

### `ac envoy inbox messages <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns all messages in a thread.

### `ac envoy inbox archive <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac envoy inbox unarchive <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac envoy inbox assign <thread-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--user-id` | str | yes | User ID to assign the thread to |
| `--json` | flag | no | Raw JSON output |

### `ac envoy inbox snooze <thread-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--until` | str | yes | ISO datetime to snooze until (e.g. 2026-04-01T09:00:00) |
| `--json` | flag | no | Raw JSON output |

### `ac envoy inbox complete <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Marks the thread as complete.

### `ac envoy inbox update-status <thread-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--status` | str | yes | New thread status |
| `--json` | flag | no | Raw JSON output |

### `ac envoy inbox add-tags <thread-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--tags` | str | yes | Comma-separated tags to add |
| `--json` | flag | no | Raw JSON output |

### `ac envoy inbox remove-tags <thread-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--tags` | str | yes | Comma-separated tags to remove |
| `--json` | flag | no | Raw JSON output |

### `ac envoy inbox reply <thread-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--body` | str | yes | Reply message body |
| `--subject` | str | no | Override subject line |
| `--json` | flag | no | Raw JSON output |

---

## Battlecards

### `ac envoy battlecards list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--query` / `-q` | str | None | Search by name or content |
| `--limit` | int | None | Max results |
| `--json` | flag | off | Raw JSON output |

### `ac envoy battlecards get <battlecard-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac envoy battlecards create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Battlecard name |
| `--description` | str | no | Battlecard description |
| `--competitor-name` | str | no | Competitor name |
| `--status` | str | no | Battlecard status |
| `--json` | flag | no | Raw JSON output |

### `ac envoy battlecards update <battlecard-id>`
Same optional flags as `create`. Only provided fields are updated.

### `ac envoy battlecards delete <battlecard-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac envoy battlecards duplicate <battlecard-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Creates a copy of the battlecard.

---

## Playbooks

### `ac envoy playbooks list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--query` / `-q` | str | None | Search by name or content |
| `--limit` | int | None | Max results |
| `--json` | flag | off | Raw JSON output |

### `ac envoy playbooks get <playbook-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac envoy playbooks create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Playbook name |
| `--description` | str | no | Playbook description |
| `--status` | str | no | Playbook status |
| `--competitor-name` | str | no | Competitor name |
| `--json` | flag | no | Raw JSON output |

### `ac envoy playbooks update <playbook-id>`
Same optional flags as `create`. Only provided fields are updated.

### `ac envoy playbooks delete <playbook-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac envoy playbooks duplicate <playbook-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Creates a copy of the playbook.

---

## Dashboard, Signals & Inbox Count

### `ac envoy dashboard`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Shows outreach dashboard statistics (sequences active, emails sent, replies, etc.).

### `ac envoy signals <recipient-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns sales signals for a specific recipient.

### `ac envoy inbox-count`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns total inbox thread count.
