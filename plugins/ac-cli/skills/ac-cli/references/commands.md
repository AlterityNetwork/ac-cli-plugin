# AgencyCore CLI -- Command Reference

Complete flag reference for all `ac` CLI commands. All commands require
authentication (`ac login`) unless noted otherwise.

For domain-scoped quick references (just the common commands per domain), see:
- [`crm.md`](./crm.md) · [`envoy.md`](./envoy.md) · [`workflows.md`](./workflows.md) · [`admin.md`](./admin.md) · [`platform.md`](./platform.md) · [`auth-env.md`](./auth-env.md) · [`workflows-recipes.md`](./workflows-recipes.md)

## Table of Contents

1. [CRM](#crm)
   - [Companies](#companies)
   - [People](#people)
   - [Deals](#deals)
   - [Activities](#activities)
   - [Communications](#communications)
   - [Lists](#lists)
   - [Import](#import)
   - [Search & Dashboard](#search--dashboard)
   - [Engagement Dashboard](#engagement-dashboard)
2. [Envoy (Outreach)](#envoy-outreach)
   - [Sequences](#sequences)
   - [Campaigns](#campaigns)
   - [Steps](#steps)
   - [Recipients](#recipients)
   - [Outbox](#outbox)
   - [Inbox](#inbox)
   - [Battlecards](#battlecards)
   - [Playbooks](#playbooks)
   - [Dashboard, Signals & Inbox Count](#dashboard-signals--inbox-count)
3. [Workflows](#workflows)
   - [Runs](#runs)
   - [Schedules](#schedules)
   - [Presets](#presets)
   - [CSV Parse](#csv-parse)
   - [Run Companies](#run-companies)
   - [Run People](#run-people)
4. [Admin](#admin)
   - [Users](#users)
   - [Organizations](#organizations)
   - [Queues](#queues)
   - [Demo](#demo)
   - [Onboarding](#onboarding)
   - [App Usage](#app-usage)
   - [AI Usage](#ai-usage)
   - [Platform Activity](#platform-activity)
   - [Legal Documents](#legal-documents)
   - [Analytics Overview](#analytics-overview)
   - [Cache Stats](#cache-stats)
   - [Chat Escalations](#chat-escalations)
   - [Subscriptions](#subscriptions)
   - [Subscription Plans](#subscription-plans)
5. [Platform](#platform)
   - [Files (Images)](#files-images)
   - [Apps](#apps)
   - [Writing Styles](#writing-styles)
   - [Nylas (Email Integration)](#nylas-email-integration)
   - [Hooks](#hooks)
   - [Messaging](#messaging)
   - [Chat (AI Threads)](#chat-ai-threads)
   - [Resources (Knowledge Base)](#resources-knowledge-base)
   - [Profiles](#profiles)
6. [Auth & Environment](#auth--environment)
   - [Auth](#auth)
   - [Environment](#environment)
   - [Health](#health)

---

## CRM

### Companies

#### `ac crm companies list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 100 | Max results to return |
| `--offset` | int | 0 | Skip this many results |
| `--json` | flag | off | Output raw JSON |

#### `ac crm companies get <company-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

#### `ac crm companies create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Company name |
| `--website` | str | no | Company website URL |
| `--industry` | str | no | Industry category |
| `--lifecycle-stage` | str | no | e.g. lead, customer, churned |
| `--tags` | str | no | Comma-separated tags |
| `--location` | str | no | City/region |
| `--country` | str | no | Country |
| `--description` | str | no | Free-text description |
| `--json` | flag | no | Output raw JSON |

#### `ac crm companies update <company-id>`
Same optional flags as `create`. Only provided fields are updated.

#### `ac crm companies delete <company-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Output raw JSON |

---

### People

#### `ac crm people list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--company-id` | str | -- | Filter by company |
| `--limit` | int | 100 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

#### `ac crm people get <person-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

#### `ac crm people create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--email` | str | no | Contact email |
| `--full-name` | str | no | Full name |
| `--current-title` | str | no | Job title |
| `--company-id` | str | no | Link to company |
| `--lifecycle-stage` | str | no | e.g. lead, customer |
| `--tags` | str | no | Comma-separated tags |
| `--linkedin-url` | str | no | LinkedIn profile URL |
| `--location` | str | no | City/region |
| `--country` | str | no | Country |
| `--json` | flag | no | Output raw JSON |

#### `ac crm people update <person-id>`
Same optional flags as `create`. Only provided fields are updated.

#### `ac crm people delete <person-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Output raw JSON |

#### `ac crm people bulk-upsert`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--file` / `-f` | str | yes | Path to JSON file containing people array |
| `--json` | flag | no | Raw JSON output |

Bulk upserts people from a JSON file. The file must contain a JSON array of person objects.

#### `ac crm people bulk-delete`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--ids` | str | yes | Comma-separated people IDs to delete |
| `--yes` | flag | no | Skip confirmation prompt |

---

### Deals

#### `ac crm deals list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--stage` | str | -- | Filter by pipeline stage |
| `--company-id` | str | -- | Filter by company |
| `--owner-id` | str | -- | Filter by deal owner |
| `--limit` | int | 100 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

#### `ac crm deals get <deal-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

#### `ac crm deals create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Deal name |
| `--stage` | str | no | Pipeline stage |
| `--amount` | float | no | Deal value |
| `--currency` | str | no | Currency code (e.g. USD) |
| `--company-id` | str | no | Link to company |
| `--contact-id` | str | no | Link to primary contact |
| `--expected-close-date` | str | no | ISO date (e.g. 2026-04-15) |
| `--tags` | str | no | Comma-separated tags |
| `--next-steps` | str | no | Free-text next steps |
| `--json` | flag | no | Output raw JSON |

#### `ac crm deals update <deal-id>`
Same optional flags as `create`. Only provided fields are updated.

#### `ac crm deals move <deal-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--stage` | str | yes | Target pipeline stage |
| `--json` | flag | no | Output raw JSON |

#### `ac crm deals order`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--stage` | str | yes | Pipeline stage to reorder |
| `--deal-ids` | str | yes | Comma-separated deal IDs in desired order |
| `--json` | flag | no | Output raw JSON |

#### `ac crm deals delete <deal-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Output raw JSON |

---

### Activities

#### `ac crm activities list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--deal-id` | str | -- | Filter by deal |
| `--company-id` | str | -- | Filter by company |
| `--contact-id` | str | -- | Filter by contact |
| `--type` | str | -- | Filter by type (call, meeting, email, task, note) |
| `--status` | str | -- | Filter by status (pending, completed) |
| `--sort-by` | str | -- | Sort field (due_date, created_at) |
| `--limit` | int | 100 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

#### `ac crm activities get <activity-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

#### `ac crm activities create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--type` | str | yes | Activity type (call, meeting, email, task, note) |
| `--title` | str | yes | Activity title |
| `--due-date` | str | no | ISO date |
| `--priority` | str | no | Priority level (low, medium, high, urgent) |
| `--deal-id` | str | no | Link to deal |
| `--company-id` | str | no | Link to company |
| `--contact-id` | str | no | Link to contact |
| `--description` | str | no | Free-text description |
| `--json` | flag | no | Output raw JSON |

#### `ac crm activities update <activity-id>`
All flags from `create` are optional. Only provided fields are updated.

#### `ac crm activities complete <activity-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

#### `ac crm activities delete <activity-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Output raw JSON |

---

### Communications

#### `ac crm comms list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--company-id` | str | -- | Filter by company |
| `--contact-id` | str | -- | Filter by contact |
| `--deal-id` | str | -- | Filter by deal |
| `--type` | str | -- | Filter by type (email, etc.) |
| `--direction` | str | -- | Filter by direction (inbound, outbound) |
| `--status` | str | -- | Filter by status |
| `--limit` | int | 20 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

#### `ac crm comms thread <thread-id>`
Shows all messages in a conversation thread.

#### `ac crm comms unread`
Shows unread thread counts. No flags required.

#### `ac crm comms unread-thread-ids`
Returns list of unread thread IDs (useful for scripting).

#### `ac crm comms mark-read <thread-id>`
Marks all messages in a thread as read.

#### `ac crm comms contact-by-email <email>`
Look up a CRM contact by their email address.

#### `ac crm comms resolve-contact <email>`
| Flag | Type | Description |
|------|------|-------------|
| `--name` | str | Contact name (if creating new) |
| `--job-title` | str | Job title |
| `--company-id` | str | Link to company |

Finds or creates a contact record for the given email.

#### `ac crm comms draft-email`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--contact-id` | str | yes | Recipient contact |
| `--subject` | str | yes | Email subject |
| `--content` | str | yes | Email body |
| `--company-id` | str | no | Related company |
| `--deal-id` | str | no | Related deal |
| `--to-emails` | str | no | Comma-separated recipient emails |
| `--from-email` | str | no | Sender email override |
| `--json` | flag | no | Output raw JSON |

#### `ac crm comms generate-draft`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--mode` | str | yes | Draft mode (compose, reply) |
| `--recipient-name` | str | yes | Recipient's name |
| `--recipient-email` | str | no | Recipient's email |
| `--company-name` | str | no | Recipient's company |
| `--sender-name` | str | no | Your name |
| `--original-subject` | str | no | Subject of email being replied to |
| `--recipient-title` | str | no | Recipient's job title |
| `--sender-signature` | str | no | Sender's email signature |
| `--user-draft-subject` | str | no | Draft subject to refine |
| `--user-draft-body` | str | no | Draft body to refine |
| `--json` | flag | no | Output raw JSON |

#### `ac crm comms update <communication-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--subject` | str | Update subject |
| `--content` | str | Update content |
| `--status` | str | Update status |
| `--tags` | str | Comma-separated tags |
| `--json` | flag | Output raw JSON |

#### `ac crm comms archive`
| Flag | Type | Description |
|------|------|-------------|
| `--thread-id` | str | Archive entire thread |
| `--comm-id` | str | Archive single message |

One of `--thread-id` or `--comm-id` is required.

#### `ac crm comms unarchive`
Same flags as `archive`.

#### `ac crm comms delete <communication-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation |
| `--json` | flag | Output raw JSON |

#### `ac crm comms delete-thread <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation |
| `--json` | flag | Output raw JSON |

#### `ac crm comms pending-approvals`
List communications in `awaiting_approval` status.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--sequence-id` | str | — | Filter by sequence |
| `--step-id` | str | — | Filter by step |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

#### `ac crm comms approve <communication-id>`
Approve a pending communication so it sends.

#### `ac crm comms reject <communication-id>`
Reject a pending communication.

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--action` | str | yes | One of: `regenerate`, `remove_recipient`, `skip_send`, `manual_edit` |
| `--reason` | str | no | Optional free-text reason |
| `--json` | flag | no | Output raw JSON |

#### `ac crm comms regenerate <communication-id>`
Regenerate a pending communication's draft.

---

### Lists

#### `ac crm lists list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 100 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

#### `ac crm lists get <list-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

#### `ac crm lists create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | List name |
| `--member-type` | str | no | person, company, or mixed |
| `--type` | str | no | static or dynamic |
| `--description` | str | no | List description |
| `--json` | flag | no | Output raw JSON |

#### `ac crm lists update <list-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--name` | str | New name |
| `--description` | str | New description |
| `--type` | str | static or dynamic |
| `--member-type` | str | person, company, or mixed |
| `--json` | flag | Output raw JSON |

#### `ac crm lists members <list-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 100 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

#### `ac crm lists add-member <list-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--person-id` | str | Add a person |
| `--company-id` | str | Add a company |
| `--json` | flag | Output raw JSON |

One of `--person-id` or `--company-id` is required.

#### `ac crm lists remove-member <list-id>`
Same flags as `add-member`.

#### `ac crm lists delete <list-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation |
| `--json` | flag | Output raw JSON |

---

### Import

#### `ac crm import preview`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--file` | path | yes | Path to JSON file to import |
| `--json` | flag | no | Output raw JSON |

Shows a summary of what will be imported (new records, duplicates, errors)
before committing.

#### `ac crm import commit`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--preview-id` | str | yes | ID from the preview step |
| `--auto-accept` | flag | no | Skip confirmation |
| `--json` | flag | no | Output raw JSON |

---

### Search & Dashboard

#### `ac crm search <query>`
Searches across companies, contacts, and deals. Returns matching records
from all three domains.

| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

#### `ac crm dashboard`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--period` | int | 30 | Number of days to report on |
| `--json` | flag | off | Output raw JSON |

Shows pipeline metrics: total deals, total value, leads created, messages
sent, and activities completed for the given period.

---

### Engagement Dashboard

#### `ac crm engagement-dashboard`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--period` | int | 30 | Period in days (1-365) |
| `--json` | flag | off | Output raw JSON |

Shows email engagement metrics including emails sent (current and previous period
with change), open rate, click rate, reply rate, bounce rate, email health score
and status, and top clicked links.

---

## Envoy (Outreach)

### Sequences

#### `ac envoy sequences list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--status` | str | None | Filter by sequence status |
| `--json` | flag | off | Raw JSON output |

#### `ac envoy sequences get <sequence-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac envoy sequences create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Sequence name |
| `--description` | str | no | Sequence description |
| `--writing-style-id` | str | no | Writing style to use for AI drafts |
| `--playbook-id` | str | no | Playbook to guide messaging |
| `--crm-list-id` | str | no | CRM list to source recipients from |
| `--execution-mode` | str | no | Execution mode |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy sequences update <sequence-id>`
Same optional flags as `create`. Only provided fields are updated.

#### `ac envoy sequences delete <sequence-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac envoy sequences launch <sequence-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--workflow-id` | str | yes | Workflow to use for execution |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy sequences pause <sequence-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Pauses a running sequence. No new steps will execute until resumed.

#### `ac envoy sequences resume <sequence-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--workflow-id` | str | yes | Workflow to use for resumed execution |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy sequences duplicate <sequence-id>`
Duplicate a sequence (copies steps + recipients).

#### `ac envoy sequences archive <sequence-id>` / `restore <sequence-id>`
Soft-archive or restore. Archived sequences won't run.

#### `ac envoy sequences impact-preview <sequence-id>`
Preview affected recipients/drafts before deleting steps.

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--step-id` | str (repeatable) | yes | Step IDs about to delete |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy sequences bulk-remove-recipients <sequence-id>`
Soft-delete a batch of recipients.

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--recipient-id` | str (repeatable) | yes | Recipient IDs to remove |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy sequences classify-step-subtype <instruction>`
Classify a step subtype from instruction text. Returns `{subtype}`.

#### `ac envoy sequences outputs <sequence-id>`
List sequence outputs (generated drafts/results).

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

#### `ac envoy sequences generate-drafts <sequence-id> <step-id>`
Trigger draft generation for a step.

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--workflow-id` | str | yes | Workflow under which drafts run |
| `--json` | flag | no | Raw JSON output |

---

### Campaigns

#### `ac envoy campaigns list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--archived` | flag | off | Show archived campaigns instead of active |
| `--query` / `-q` | str | — | Search by name |
| `--cursor` | str | — | Pagination cursor |
| `--limit` | int | — | Max results |
| `--json` | flag | off | Raw JSON output |

#### `ac envoy campaigns get <campaign-id>` / `delete <campaign-id> [--yes]`
Standard get/delete.

#### `ac envoy campaigns create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Campaign name |
| `--description` | str | no | Description |
| `--goal` | str | no | Campaign goal |
| `--source-app` | str | no | Source app slug |
| `--started-at` | ISO date | no | Start date |
| `--ended-at` | ISO date | no | End date |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy campaigns update <campaign-id>`
Same flags as `create` (all optional).

#### `ac envoy campaigns archive <campaign-id>` / `unarchive <campaign-id>`
Toggle archive state.

---

### Steps

#### `ac envoy steps create <sequence-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--type` | str | yes | Step type (message, delay, task) |
| `--step-order` | int | no | Position in sequence |
| `--message-template` | str | no | Email template text |
| `--prompt` | str | no | AI prompt for draft generation |
| `--delay-value` | int | no | Delay duration (for delay steps) |
| `--delay-unit` | str | no | Delay unit (days, hours, minutes) |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy steps update <sequence-id> <step-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--message-template` | str | Update email template |
| `--prompt` | str | Update AI prompt |
| `--delay-value` | int | Update delay duration |
| `--delay-unit` | str | Update delay unit |
| `--json` | flag | Raw JSON output |

#### `ac envoy steps delete <sequence-id> <step-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac envoy steps reorder <sequence-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--step-ids` | str | yes | Comma-separated step IDs in desired order |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy steps stats <sequence-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Shows execution statistics for each step in the sequence.

---

### Recipients

#### `ac envoy recipients list <sequence-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--status` | str | None | Filter by recipient status |
| `--step-id` | str | None | Filter by current step |
| `--json` | flag | off | Raw JSON output |

#### `ac envoy recipients add <sequence-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--prospect-ids` / `-p` | str | no | Comma-separated prospect IDs (mutually exclusive with --crm-list-id and --source) |
| `--crm-list-id` | str | no | CRM list ID to source recipients from (mutually exclusive with --prospect-ids and --source) |
| `--source` | str | no | Raw JSON source object (advanced, overrides other options) |
| `--json` | flag | no | Raw JSON output |

One of `--prospect-ids`, `--crm-list-id`, or `--source` is required.

#### `ac envoy recipients remove <sequence-id> <recipient-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

---

### Outbox

#### `ac envoy outbox pending`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--sequence-id` | str | None | Filter by sequence |
| `--step-id` | str | None | Filter by step |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

Lists drafts awaiting approval.

#### `ac envoy outbox sent`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--sequence-id` | str | None | Filter by sequence |
| `--status` | str | None | Filter by delivery status |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

#### `ac envoy outbox step-drafts`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--sequence-id` | str | yes | Sequence ID |
| `--step-id` | str | yes | Step ID |
| `--limit` | int | no | Max results (default: 50) |
| `--offset` | int | no | Skip results (default: 0) |
| `--json` | flag | no | Raw JSON output |

Lists all drafts for a specific step.

#### `ac envoy outbox update-draft <draft-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--subject` | str | New subject line |
| `--body` | str | New email body |
| `--json` | flag | Raw JSON output |

#### `ac envoy outbox approve <draft-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--subject` | str | Override subject before sending |
| `--body` | str | Override body before sending |
| `--json` | flag | Raw JSON output |

Approves and sends the draft.

#### `ac envoy outbox reject <draft-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--action` | str | yes | What to do next: `regenerate_draft` or `remove_recipient` |
| `--reason` | str | no | Reason for rejection (used as AI context for regeneration) |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy outbox regenerate <draft-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--instruction` | str | Additional instruction for AI regeneration |
| `--json` | flag | Raw JSON output |

---

### Inbox

#### `ac envoy inbox list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--status` | str | None | Filter by thread status |
| `--sentiment` | str | None | Filter by sentiment (positive, negative, neutral) |
| `--sequence-id` | str | None | Filter by source sequence |
| `--assigned-to` | str | None | Filter by assigned user ID |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

#### `ac envoy inbox messages <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns all messages in a thread.

#### `ac envoy inbox archive <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac envoy inbox unarchive <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac envoy inbox assign <thread-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--user-id` | str | yes | User ID to assign the thread to |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy inbox snooze <thread-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--until` | str | yes | ISO datetime to snooze until (e.g. 2026-04-01T09:00:00) |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy inbox complete <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Marks the thread as complete.

#### `ac envoy inbox update-status <thread-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--status` | str | yes | New thread status |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy inbox add-tags <thread-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--tags` | str | yes | Comma-separated tags to add |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy inbox remove-tags <thread-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--tags` | str | yes | Comma-separated tags to remove |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy inbox reply <thread-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--body` | str | yes | Reply message body |
| `--subject` | str | no | Override subject line |
| `--json` | flag | no | Raw JSON output |

---

### Battlecards

#### `ac envoy battlecards list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--query` / `-q` | str | None | Search by name or content |
| `--limit` | int | None | Max results |
| `--json` | flag | off | Raw JSON output |

#### `ac envoy battlecards get <battlecard-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac envoy battlecards create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Battlecard name |
| `--description` | str | no | Battlecard description |
| `--competitor-name` | str | no | Competitor name |
| `--status` | str | no | Battlecard status |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy battlecards update <battlecard-id>`
Same optional flags as `create`. Only provided fields are updated.

#### `ac envoy battlecards delete <battlecard-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac envoy battlecards duplicate <battlecard-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Creates a copy of the battlecard.

---

### Playbooks

#### `ac envoy playbooks list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--query` / `-q` | str | None | Search by name or content |
| `--limit` | int | None | Max results |
| `--json` | flag | off | Raw JSON output |

#### `ac envoy playbooks get <playbook-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac envoy playbooks create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Playbook name |
| `--description` | str | no | Playbook description |
| `--status` | str | no | Playbook status |
| `--competitor-name` | str | no | Competitor name |
| `--json` | flag | no | Raw JSON output |

#### `ac envoy playbooks update <playbook-id>`
Same optional flags as `create`. Only provided fields are updated.

#### `ac envoy playbooks delete <playbook-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac envoy playbooks duplicate <playbook-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Creates a copy of the playbook.

---

### Dashboard, Signals & Inbox Count

#### `ac envoy dashboard`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Shows outreach dashboard statistics (sequences active, emails sent, replies, etc.).

#### `ac envoy signals <recipient-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns sales signals for a specific recipient.

#### `ac envoy inbox-count`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns total inbox thread count.

---

## Workflows

### Runs

#### `ac workflows runs create <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--input` | str | no | JSON string of input parameters |
| `--idempotency-key` | str | no | Idempotency key to prevent duplicate runs |
| `--json` | flag | no | Raw JSON output |

Creates a new workflow run. Returns 202 (accepted) with run ID and status.

#### `ac workflows runs list <workflow-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

#### `ac workflows runs get <workflow-id> <run-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns run details including status, input, output, and timing.

#### `ac workflows runs logs <workflow-id> <run-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max log entries |
| `--offset` | int | 0 | Skip entries |
| `--json` | flag | off | Raw JSON output |

---

### Schedules

#### `ac workflows schedules list <workflow-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Lists all schedules for the workflow.

#### `ac workflows schedules get <workflow-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Gets the schedule details for the workflow.

#### `ac workflows schedules create <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--cron` | str | yes | Cron expression (5-field: minute hour dom month dow) |
| `--timezone` | str | no | Timezone (default: UTC) |
| `--input` | str | no | JSON string of input parameters for each run |
| `--json` | flag | no | Raw JSON output |

#### `ac workflows schedules update <workflow-id> <schedule-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--cron` | str | Updated cron expression |
| `--timezone` | str | Updated timezone |
| `--input` | str | Updated JSON input parameters |
| `--json` | flag | Raw JSON output |

#### `ac workflows schedules delete <workflow-id> <schedule-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac workflows schedules preview <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--cron` | str | yes | Cron expression to preview |
| `--timezone` | str | no | Timezone (default: UTC) |
| `--count` | int | no | Number of upcoming times to show (default: 5) |
| `--json` | flag | no | Raw JSON output |

Shows the next N upcoming run times for a cron expression without creating a schedule.

#### `ac workflows schedules toggle <workflow-id> <schedule-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--enabled/--disabled` | flag | yes | Enable or disable the schedule |
| `--json` | flag | no | Raw JSON output |

---

### Presets

#### `ac workflows presets list <workflow-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac workflows presets get <workflow-id> <preset-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac workflows presets create <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Preset name |
| `--description` | str | no | Preset description |
| `--config` | str | no | JSON string of preset configuration |
| `--json` | flag | no | Raw JSON output |

#### `ac workflows presets update <workflow-id> <preset-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--name` | str | Update preset name |
| `--description` | str | Update description |
| `--config` | str | Update JSON configuration |
| `--json` | flag | Raw JSON output |

#### `ac workflows presets delete <workflow-id> <preset-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

---

### CSV Parse

#### `ac workflows csv-parse <file>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `<file>` | str | yes | Path to CSV file (positional argument) |
| `--json` | flag | no | Raw JSON output |

Parses a CSV file into structured company data via multipart upload. File must have .csv extension.

---

### Run Companies

Manage companies discovered by workflow runs.

#### `ac workflows run-companies list <workflow-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--include-in-crm` | flag | off | Include companies already added to CRM |
| `--json` | flag | off | Raw JSON output |

Lists deduplicated companies discovered across all runs of a workflow.

#### `ac workflows run-companies list-by-run <workflow-id> <run-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Lists companies from a specific run (no deduplication).

#### `ac workflows run-companies add-to-crm <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--company-ids` | str | yes | Comma-separated workflow company IDs |
| `--json` | flag | no | Raw JSON output |

Adds workflow-discovered companies to CRM.

#### `ac workflows run-companies crm-count <workflow-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns count of companies added to CRM for this workflow.

#### `ac workflows run-companies delete <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--company-ids` | str | yes | Comma-separated workflow company IDs |
| `--yes` | flag | no | Skip confirmation prompt |
| `--json` | flag | no | Raw JSON output |

---

### Run People

Manage people discovered by workflow runs.

#### `ac workflows run-people list <workflow-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--include-in-crm` | flag | off | Include people already added to CRM |
| `--json` | flag | off | Raw JSON output |

Lists deduplicated people discovered across all runs of a workflow.

#### `ac workflows run-people list-by-run <workflow-id> <run-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Lists people from a specific run (no deduplication).

#### `ac workflows run-people company-match-preview <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--person-ids` | str | yes | Comma-separated workflow person IDs |
| `--json` | flag | no | Raw JSON output |

Previews company matches for the specified people. Shows match source, type, and people without company info.

#### `ac workflows run-people company-search <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--query` / `-q` | str | no | Search query (default: empty) |
| `--json` | flag | no | Raw JSON output |

Searches CRM and Sonar companies by name.

#### `ac workflows run-people add-to-crm <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--person-ids` | str | yes | Comma-separated workflow person IDs |
| `--overrides-file` | str | no | Path to JSON file with company overrides |
| `--json` | flag | no | Raw JSON output |

Adds workflow-discovered people to CRM. Optionally provide company overrides for matching.

#### `ac workflows run-people crm-count <workflow-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns count of people added to CRM for this workflow.

#### `ac workflows run-people delete <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--person-ids` | str | yes | Comma-separated workflow person IDs |
| `--yes` | flag | no | Skip confirmation prompt |
| `--json` | flag | no | Raw JSON output |

---

## Admin

All admin commands require super admin authentication.

### Users

#### `ac admin users list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--query` | str | None | Filter by name or email |
| `--sort` | str | "created_at" | Sort field |
| `--order` | str | "desc" | Sort order (asc/desc) |
| `--page` | int | 1 | Page number |
| `--page-size` | int | 50 | Results per page |
| `--json` | flag | off | Raw JSON output |

#### `ac admin users get <user-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac admin users create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--email` | str | yes | User email |
| `--password` | str | yes | User password |
| `--full-name` | str | no | Full name |
| `--json` | flag | no | Raw JSON output |

#### `ac admin users update <user-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--full-name` | str | no | Update full name |
| `--is-superadmin` | flag | no | Grant super admin privileges |
| `--json` | flag | no | Raw JSON output |

#### `ac admin users delete <user-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac admin users auth-search`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--email` | str | yes | Email to search in auth provider |
| `--json` | flag | no | Raw JSON output |

#### `ac admin users search`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--email` | str | yes | Email to search in application database |
| `--json` | flag | no | Raw JSON output |

#### `ac admin users reset-password <user-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac admin users impersonate <user-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Switches to the specified user's session. All subsequent commands run as that user.

#### `ac admin users exit-impersonation`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns to the original super admin session.

#### `ac admin users generate-link <user-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--send-email` | flag | Send the link via email to the user |
| `--json` | flag | Raw JSON output |

---

### Organizations

#### `ac admin orgs list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--query` | str | None | Filter by name or slug |
| `--sort` | str | "created_at" | Sort field |
| `--order` | str | "desc" | Sort order (asc/desc) |
| `--page` | int | 1 | Page number |
| `--page-size` | int | 50 | Results per page |
| `--json` | flag | off | Raw JSON output |

#### `ac admin orgs get <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac admin orgs create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Organization name |
| `--slug` | str | no | URL-friendly slug (auto-generated from name if omitted) |
| `--plan` | str | no | Subscription plan |
| `--json` | flag | no | Raw JSON output |

#### `ac admin orgs update <org-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | no | Update organization name |
| `--slug` | str | no | Update slug |
| `--plan` | str | no | Update subscription plan |
| `--json` | flag | no | Raw JSON output |

#### `ac admin orgs delete <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac admin orgs members <org-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--page` | int | 1 | Page number |
| `--page-size` | int | 50 | Results per page |
| `--json` | flag | off | Raw JSON output |

#### `ac admin orgs add-member <org-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--user-id` | str | yes | User ID to add |
| `--role` | str | no | Member role (e.g. admin, member) |
| `--json` | flag | no | Raw JSON output |

#### `ac admin orgs update-member <org-id> <user-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--role` | str | yes | New role for the member |
| `--json` | flag | no | Raw JSON output |

#### `ac admin orgs remove-member <org-id> <user-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac admin orgs transfer-ownership <org-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--new-owner-id` | str | yes | User ID of the new owner |
| `--yes` | flag | no | Skip confirmation prompt |
| `--json` | flag | no | Raw JSON output |

---

### Queues

#### `ac admin queues health`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns overall health status of all queues.

#### `ac admin queues stats`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns aggregate statistics across all queues.

#### `ac admin queues queue-stats <queue-name>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns statistics for a specific queue.

#### `ac admin queues metrics`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns performance metrics for all queues.

#### `ac admin queues send-to-sentry`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Sends current queue errors to Sentry for monitoring.

#### `ac admin queues job-performance <job-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns performance metrics for a specific job.

#### `ac admin queues failed <queue-name>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max failed jobs to return |
| `--json` | flag | off | Raw JSON output |

#### `ac admin queues retry-all <queue-name>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

Retries all failed jobs in the specified queue.

#### `ac admin queues retry-job <job-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Retries a single failed job by its ID.

#### `ac admin queues clear-failed <queue-name>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

Permanently removes all failed jobs from the specified queue.

---

### Demo

#### `ac admin demo scrape-website`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--url` | str | yes | Website URL to scrape for demo data |
| `--json` | flag | no | Raw JSON output |

#### `ac admin demo generate-org`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--industry` | str | no | Industry for the generated organization |
| `--size` | str | no | Company size (e.g. small, medium, large) |
| `--json` | flag | no | Raw JSON output |

#### `ac admin demo generate-profile`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--industry` | str | no | Industry for the generated profile |
| `--json` | flag | no | Raw JSON output |

#### `ac admin demo prepare-account`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--org-name` | str | yes | Name for the demo organization |
| `--template` | str | no | Account template to use |
| `--json` | flag | no | Raw JSON output |

#### `ac admin demo list-accounts`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--page` | int | 1 | Page number |
| `--page-size` | int | 50 | Results per page |
| `--sort` | str | "created_at" | Sort field |
| `--order` | str | "desc" | Sort order (asc/desc) |
| `--json` | flag | off | Raw JSON output |

#### `ac admin demo get-account <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac admin demo update-account <org-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--status` | str | no | Update account status |
| `--notes` | str | no | Update account notes |
| `--json` | flag | no | Raw JSON output |

#### `ac admin demo delete-account <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac admin demo cleanup`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--max-age-days` | int | 30 | Delete demo accounts older than this many days |
| `--yes` | flag | off | Skip confirmation prompt |
| `--json` | flag | off | Raw JSON output |

#### `ac admin demo stats`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns aggregate statistics about demo accounts.

---

### Onboarding

#### `ac admin onboarding create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--email` | str | yes | User email |
| `--first-name` | str | yes | First name |
| `--last-name` | str | yes | Last name |
| `--org-name` | str | yes | Organization name |
| `--website-url` | str | no | Organization website URL |
| `--country` | str | no | Country code (e.g. US) |
| `--timezone` | str | no | Timezone (e.g. America/New_York) |
| `--locale` | str | no | Locale (e.g. en) |
| `--currency` | str | no | Currency code (e.g. USD) |
| `--job-title` | str | no | Job title |
| `--bio` | str | no | Short biography |
| `--user-website` | str | no | Personal website URL |
| `--logo-url` | str | no | Organization logo URL |
| `--linkedin` | str | no | LinkedIn profile URL |
| `--contact-number` | str | no | Phone number |
| `--contact-email` | str | no | Alternative contact email |
| `--description` | str | no | Organization description |
| `--products-services` | str | no | Products and services offered |
| `--calendly-url` | str | no | Calendly scheduling URL |
| `--show-calendly/--no-show-calendly` | flag | no | Show Calendly widget |
| `--json` | flag | no | Raw JSON output |

#### `ac admin onboarding list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--status` | str | None | Filter by onboarding status (setup/pending/active) |
| `--query` | str | None | Search by name or email |
| `--page` | int | 1 | Page number |
| `--page-size` | int | 25 | Results per page |
| `--json` | flag | off | Raw JSON output |

#### `ac admin onboarding get <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac admin onboarding delete <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac admin onboarding send-link <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--send-email` | flag | Send the onboarding link via email |
| `--json` | flag | Raw JSON output |

#### `ac admin onboarding impersonate <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Switches to the onboarding organization's context for testing.

#### `ac admin onboarding end-impersonation <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns to the original super admin session.

#### `ac admin onboarding activate <org-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--send-password-reset/--no-send-password-reset` | flag | True | Send (or don't send) a password reset email on activation |
| `--json` | flag | off | Raw JSON output |

#### `ac admin onboarding deactivate <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac admin onboarding update-config <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--show-calendly/--no-show-calendly` | flag | Show/hide Calendly widget in onboarding |
| `--calendly-url` | str | Calendly scheduling URL |
| `--json` | flag | Raw JSON output |

#### `ac admin onboarding get-settings`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns current onboarding settings.

#### `ac admin onboarding update-settings`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--terms-html` | str | no | HTML content for terms and conditions |
| `--calendly-url` | str | no | Calendly scheduling URL |
| `--calendly-enabled/--no-calendly-enabled` | flag | no | Enable/disable Calendly integration |
| `--json` | flag | no | Raw JSON output |

---

### App Usage

#### `ac admin app-usage summary`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format, e.g. 2026-01-01) |
| `--end-date` | str | None | End date (ISO format, e.g. 2026-03-23) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

#### `ac admin app-usage users`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--sort` | str | None | Sort field (e.g. total_actions) |
| `--order` | str | None | Sort order (asc/desc) |
| `--page` | int | 1 | Page number |
| `--page-size` | int | 50 | Results per page |
| `--search` | str | None | Search by user name or email |
| `--json` | flag | off | Raw JSON output |

#### `ac admin app-usage user <user-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

---

### AI Usage

#### `ac admin ai-usage summary`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format, e.g. 2026-01-01) |
| `--end-date` | str | None | End date (ISO format, e.g. 2026-03-23) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

#### `ac admin ai-usage users`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--sort` | str | None | Sort field (e.g. total_tokens, total_cost) |
| `--order` | str | None | Sort order (asc/desc) |
| `--page` | int | 1 | Page number |
| `--page-size` | int | 50 | Results per page |
| `--search` | str | None | Search by user name or email |
| `--json` | flag | off | Raw JSON output |

#### `ac admin ai-usage user <user-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

#### `ac admin ai-usage by-model`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

#### `ac admin ai-usage by-workflow`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

#### `ac admin ai-usage details`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Offset for pagination |
| `--model-id` | str | None | Filter by AI model ID |
| `--user-id` | str | None | Filter by user ID |
| `--workflow-run-id` | str | None | Filter by workflow run ID |
| `--json` | flag | off | Raw JSON output |

---

### Platform Activity

#### `ac admin platform-activity summary`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

#### `ac admin platform-activity users`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--sort` | str | None | Sort field (e.g. total_events) |
| `--order` | str | None | Sort order (asc/desc) |
| `--page` | int | 1 | Page number |
| `--page-size` | int | 50 | Results per page |
| `--query` | str | None | Search by user name or email |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

#### `ac admin platform-activity user <user-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

---

### Searches (Sonar + Headhunter)

Cross-org search analytics for super admins. **PII is stripped from every response**: people rows omit `full_name`, `email`, `linkedin_url`, `avatar_url`, `summary`, `experience_history`, and city-level location; only role, country, skills, and quality scores remain. `trigger_data` on runs is recursively sanitized to drop any keys matching name/email/phone/linkedin patterns. The raw `output_data` blob is never returned.

#### `ac admin searches summary`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | 30d ago | Start date (ISO format) |
| `--end-date` | str | today | End date (ISO format) |
| `--source` | str | both | Filter by `sonar`, `headhunter`, or `both` |
| `--org-id` | list[str] | None | Filter by org ID (repeatable for multi-value) |
| `--user-id` | list[str] | None | Filter by user ID (repeatable for multi-value) |
| `--json` | flag | off | Raw JSON output |

Returns total runs, completed/failed counts, success rate, total companies/people discovered, average lead/relevance scores, daily breakdown, and per-source totals with previous-period change percentages.

#### `ac admin searches runs`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | 30d ago | Start date (ISO format) |
| `--end-date` | str | today | End date (ISO format) |
| `--source` | str | both | `sonar`, `headhunter`, or `both` |
| `--org-id` | list[str] | None | Org filter (repeatable) |
| `--user-id` | list[str] | None | User filter (repeatable) |
| `--status` | str | None | `pending`, `running`, `completed`, `failed` |
| `-q`, `--query` | str | None | Substring match against sanitized trigger_data |
| `--page` | int | 1 | Page number |
| `--page-size` | int | 25 | Results per page (max 100) |
| `--all` | flag | off | Walk every page (page-size 100). Implies `--json`. Capped at 50,000 items. |
| `--json` | flag | off | Raw JSON output |

#### `ac admin searches run <run-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output (includes `snapshot_definition`) |

Returns one workflow run with org/user/source context, sanitized trigger_data, status, duration, and discovered company/people counts. Raises `404` (exit 3) if the run does not exist or is not a Sonar/Headhunter run.

#### `ac admin searches companies`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | 30d ago | Start date (ISO format) |
| `--end-date` | str | today | End date (ISO format) |
| `--source` | str | both | `sonar`, `headhunter`, or `both` |
| `--org-id` | list[str] | None | Org filter (repeatable) |
| `--user-id` | list[str] | None | User filter (repeatable) |
| `-q`, `--query` | str | None | ILIKE match on `name` or `website` |
| `--page` | int | 1 | Page number |
| `--page-size` | int | 25 | Results per page (max 100) |
| `--all` | flag | off | Walk every page. Capped at 50,000 items. |
| `--json` | flag | off | Raw JSON output |

Returns firmographics, lead score, sales signals, country, and discovery timing. Omits `linkedin_url` and `crm_company_id` (cross-tenant linkage).

#### `ac admin searches people`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | 30d ago | Start date (ISO format) |
| `--end-date` | str | today | End date (ISO format) |
| `--source` | str | headhunter | Sonar produces no people, so the default is `headhunter`. Pass `both` to include sonar (returns headhunter rows only). `sonar` returns empty. |
| `--org-id` | list[str] | None | Org filter (repeatable) |
| `--user-id` | list[str] | None | User filter (repeatable) |
| `--page` | int | 1 | Page number |
| `--page-size` | int | 25 | Results per page (max 100) |
| `--all` | flag | off | Walk every page. Capped at 50,000 items. |
| `--json` | flag | off | Raw JSON output |

De-identified rows: `current_title`, `current_company_text`, `country`, `skills`, `languages`, `relevance_score`, `email_score` (the integer 0–100, not the email address), `email_source` (provider name only). Use this endpoint for cohort and distribution analysis, not per-record review.

---

### Legal Documents

#### `ac admin legal-docs list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--document-type` | str | None | Filter by document type (e.g. terms_of_service, privacy_policy) |
| `--json` | flag | off | Raw JSON output |

#### `ac admin legal-docs get <document-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns all fields including content_html.

#### `ac admin legal-docs create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--document-type` | str | yes | Document type (e.g. terms_of_service, privacy_policy) |
| `--version` | str | yes | Document version (e.g. "1.0") |
| `--title` | str | yes | Document title |
| `--content-html` | str | no | HTML content of the document |
| `--json` | flag | no | Raw JSON output |

#### `ac admin legal-docs update <document-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--title` | str | Update document title |
| `--content-html` | str | Update HTML content |
| `--json` | flag | Raw JSON output |

At least one of `--title` or `--content-html` is required.

#### `ac admin legal-docs delete <document-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac admin legal-docs set-current <document-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Sets this document as the current version for its document type.

---

### Analytics Overview

#### `ac admin analytics-overview`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (YYYY-MM-DD) |
| `--end-date` | str | None | End date (YYYY-MM-DD) |
| `--org-id` | str | None | Filter by organization ID |
| `--json` | flag | off | Raw JSON output |

Shows unified analytics summary: daily averages (AI requests, app runs, platform events), active user rate, AI cost with change, app usage with change, and platform activity with change.

---

### Cache Stats

#### `ac admin cache-stats`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Shows application cache hit/miss statistics.

---

### Chat Escalations

#### `ac admin chat-escalations list`
| Flag | Type | Description |
|------|------|-------------|
| `--status` | str | Filter: `open`, `triaged`, `resolved` |
| `--json` | flag | Raw JSON output |

#### `ac admin chat-escalations update <escalation-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--status` | str | yes | `open`, `triaged`, or `resolved` |
| `--note` | str | no | Optional triage note (max 2000 chars) |
| `--json` | flag | no | Raw JSON output |

---

### Subscriptions

#### `ac admin subscriptions list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--org-id` | str | — | Filter by organization |
| `--status` | str | — | Filter by status |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

#### `ac admin subscriptions get <subscription-id>` / `delete <subscription-id> [--yes]`
Standard get/delete.

#### `ac admin subscriptions create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--org-id` | str | yes | Organization ID |
| `--plan-id` | str | yes | Plan ID |
| `--billing-period` | str | yes | `monthly` or `annual` |
| `--started-at` | ISO date | yes | Start date |
| `--status` | str | no | Initial status |
| `--ended-at` | ISO date | no | End date |
| `--trial-ends-at` | ISO date | no | Trial end date |
| `--stripe-customer-id` | str | no | Stripe customer ID |
| `--stripe-subscription-id` | str | no | Stripe subscription ID |
| `--json` | flag | no | Raw JSON output |

#### `ac admin subscriptions update <subscription-id>`
Same flags as `create` (all optional).

---

### Subscription Plans

#### `ac admin subscription-plans list`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac admin subscription-plans get <plan-id>` / `delete <plan-id> [--yes]`
Standard get/delete.

#### `ac admin subscription-plans create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--slug` | str | yes | Plan slug |
| `--name` | str | yes | Plan display name |
| `--monthly-price-cents` | int | yes | Monthly price in cents |
| `--annual-price-cents` | int | yes | Annual price in cents |
| `--description` | str | no | Plan description |
| `--features` | JSON object | no | Feature flags (e.g. `'{"seats":10}'`) |
| `--active/--inactive` | flag | no | Active state |
| `--json` | flag | no | Raw JSON output |

#### `ac admin subscription-plans update <plan-id>`
Same flags as `create` (all optional).

---

## Platform

### Files (Images)

#### `ac files images upload <file-path>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--category` / `-c` | str | yes | Storage category: `avatars`, `organization_logos`, `crm_company_logos`, `general_images`, `apps_assets` |
| `--json` | flag | no | Raw JSON output |

Uploads an image file. Allowed formats: .jpg, .jpeg, .png, .gif, .webp, .svg, .avif. Max size: 1 MB.

#### `ac files images delete <key>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

Deletes an image by its R2 object key.

---

### Apps

#### `ac apps list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--org-id` | str | auto | Organization ID (auto-resolved from /whoami) |
| `--include-inactive` | flag | off | Include inactive/uninstalled apps |
| `--limit` | int | 100 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

#### `ac apps install <app-slug>`
| Flag | Type | Description |
|------|------|-------------|
| `--org-id` | str | Organization ID (auto-resolved from /whoami) |
| `--json` | flag | Raw JSON output |

#### `ac apps uninstall <app-slug>`
| Flag | Type | Description |
|------|------|-------------|
| `--org-id` | str | Organization ID (auto-resolved from /whoami) |
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac apps usage-event <app-slug>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--org-id` | str | no | Organization ID (auto-resolved) |
| `--event-type` | str | yes | Event type to record |
| `--metadata` | str | no | JSON metadata for the event |
| `--json` | flag | no | Raw JSON output |

#### `ac apps usage <app-slug>`
| Flag | Type | Description |
|------|------|-------------|
| `--org-id` | str | Organization ID (auto-resolved) |
| `--json` | flag | Raw JSON output |

Returns usage summary for the app.

#### `ac apps configs <app-slug>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--org-id` | str | auto | Organization ID (auto-resolved) |
| `--mask-secrets/--no-mask-secrets` | flag | True | Mask secret values in output |
| `--json` | flag | off | Raw JSON output |

#### `ac apps update-config <app-slug> <config-key>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--value` | str | yes | New value for the config key |
| `--org-id` | str | no | Organization ID (auto-resolved) |
| `--json` | flag | no | Raw JSON output |

#### `ac apps delete-config <app-slug> <config-key>`
| Flag | Type | Description |
|------|------|-------------|
| `--org-id` | str | Organization ID (auto-resolved) |
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

---

### Writing Styles

#### `ac styles list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--include-inactive` | flag | off | Include inactive styles |
| `--json` | flag | off | Raw JSON output |

#### `ac styles get <style-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

#### `ac styles create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Style name |
| `--description` | str | no | Style description |
| `--tone` | str | no | Tone (e.g. formal, casual, professional) |
| `--formality` | str | no | Formality level (e.g. high, medium, low) |
| `--json` | flag | no | Raw JSON output |

#### `ac styles update <style-id>`
Same optional flags as `create`. Only provided fields are updated.

#### `ac styles delete <style-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac styles train <style-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--sample-text` | str | yes | Sample text to train the style on |
| `--json` | flag | no | Raw JSON output |

Starts a training session using the provided sample text.

#### `ac styles feedback <session-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--rating` | int | yes | Rating for the training output |
| `--comments` | str | no | Additional feedback comments |
| `--json` | flag | no | Raw JSON output |

#### `ac styles iterate <session-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--feedback` | str | yes | Feedback to refine the style |
| `--json` | flag | no | Raw JSON output |

#### `ac styles analyze`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--text` | str | yes | Text to analyze for writing style characteristics |
| `--json` | flag | no | Raw JSON output |

---

### Nylas (Email Integration)

#### `ac nylas oauth-start`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--provider` | str | google | OAuth provider (google, microsoft) |
| `--return-path` | str | None | Path to redirect after OAuth |
| `--json` | flag | off | Raw JSON output |

Starts the OAuth flow and returns the authorization URL.

#### `ac nylas account`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns connected Nylas account details.

#### `ac nylas org-accounts`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Lists all connected accounts in the organization.

#### `ac nylas disconnect`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac nylas send`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--to` | str | yes | Recipient email address |
| `--subject` | str | yes | Email subject |
| `--body` | str | yes | Email body |
| `--reply-to-message-id` | str | no | Message ID to reply to |
| `--json` | flag | no | Raw JSON output |

#### `ac nylas update-signature`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--signature` | str | yes | Email signature (HTML or plain text) |
| `--json` | flag | no | Raw JSON output |

#### `ac nylas validate-signature`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--signature` | str | yes | Signature to validate |
| `--json` | flag | no | Raw JSON output |

---

### Hooks

#### `ac hooks list <capability>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Lists available hooks for the specified capability.

---

### Messaging

#### `ac messaging sessions`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Lists active messaging sessions for the organization. Shows platform, display name, sender ID, and last activity.

#### `ac messaging link`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--token` | str | yes | Link token from the bot's login URL |
| `--json` | flag | no | Raw JSON output |

Links an external messaging sender to the user's AgencyCore account.

---

### Chat (AI Threads)

#### `ac chat threads list`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Lists all chat threads with id, title, archived status, and creation date.

#### `ac chat threads create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--title` | str | yes | Thread title |
| `--json` | flag | no | Raw JSON output |

#### `ac chat threads update <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--title` | str | New thread title |
| `--archived/--no-archived` | flag | Archive or unarchive the thread |
| `--json` | flag | Raw JSON output |

At least one of `--title` or `--archived/--no-archived` is required.

#### `ac chat threads delete <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac chat threads messages <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Lists messages in a thread with id, role, content (truncated), and creation date.

#### `ac chat threads generate-title <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Generates an AI-suggested title for the thread based on its conversation content.

#### `ac chat threads send <thread-id> <content>`
Non-streaming send of a message to a chat thread.

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--context` | str | no | Surrounding context for the model (max 20000 chars) |
| `--document-id` | str (repeatable) | no | Restrict knowledge retrieval to these resource_hub IDs (max 10) |
| `--json` | flag | no | Raw JSON output |

#### `ac chat threads escalate <thread-id>`
Escalate a thread to a human.

| Flag | Type | Description |
|------|------|-------------|
| `--note` | str | Optional escalation note (max 2000 chars) |
| `--message-id` | str | Specific message to escalate |
| `--json` | flag | Raw JSON output |

#### `ac chat messages update-data <message-id>`
Update structured data attached to a chat message.

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--data` | JSON object | yes | JSON object to merge into the message's data field |
| `--json` | flag | no | Raw JSON output |

---

### Resources (Knowledge Base)

#### `ac resources list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

#### `ac resources upload <file-path>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Source name for the resource |
| `--description` | str | no | Resource description |
| `--tags` | str | no | Comma-separated tags |
| `--json` | flag | no | Raw JSON output |

Uploads a knowledge base resource file. Allowed formats: .pdf, .txt, .md, .docx. Max size: 10 MB.

#### `ac resources delete <resource-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

#### `ac resources status <resource-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns processing status including chunk count and any error messages.

---

### Profiles

#### `ac profiles me`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns the current user's profile details (name, email, job title, bio, superadmin status, organization).

#### `ac profiles update`
| Flag | Type | Description |
|------|------|-------------|
| `--first-name` | str | First name |
| `--last-name` | str | Last name |
| `--bio` | str | Bio |
| `--job-title` | str | Job title |
| `--avatar-url` | str | Avatar URL |
| `--email` | str | Email address |
| `--json` | flag | Raw JSON output |

At least one field is required.

#### `ac profiles members`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

Lists all members of the current organization.

#### `ac profiles set-organization <organization-id>`
Switch the current user's selected organization.

#### `ac profiles set-password`
Mark the current user's password as set (post Supabase magic-link signup). No flags.

#### `ac profiles subscription`
Show the current organization's subscription. Calls `GET /api/v1/subscriptions/me`.

| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

---

## Auth & Environment

### Auth

#### `ac login`
| Flag | Type | Description |
|------|------|-------------|
| `--email` | str | User email |
| `--password` | str | User password |
| `--env` | str | Target environment (local, staging, production) |

#### `ac logout`
No flags.

#### `ac whoami`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

---

### Environment

*No authentication required for environment commands.*

#### `ac env list`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Shows all environments (local, staging, production) and login status for each.

#### `ac env show`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Shows active environment details.

#### `ac env use <name>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Switches the active environment. Valid names: `local`, `staging`, `production`.

---

### Health

*No authentication required.*

#### `ac health check`
| Flag | Type | Description |
|------|------|-------------|
| `--api-url` | str | Override the default API URL |
| `--json` | flag | Raw JSON output |

Checks if the API is reachable and returns health status.
