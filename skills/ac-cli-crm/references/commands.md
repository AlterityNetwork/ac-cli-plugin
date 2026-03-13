# AC CLI — CRM Command Reference

Complete flag reference for every CRM command. All commands require authentication
(`ac login`) unless noted otherwise.

## Table of Contents

1. [Companies](#companies)
2. [People](#people)
3. [Deals](#deals)
4. [Activities](#activities)
5. [Communications](#communications)
6. [Lists](#lists)
7. [Import](#import)
8. [Search & Dashboard](#search--dashboard)

---

## Companies

### `ac crm companies list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 20 | Max results to return |
| `--offset` | int | 0 | Skip this many results |
| `--json` | flag | off | Output raw JSON |

### `ac crm companies get <company-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

### `ac crm companies create`
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

### `ac crm companies update <company-id>`
Same optional flags as `create`. Only provided fields are updated.

### `ac crm companies delete <company-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Output raw JSON |

---

## People

### `ac crm people list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--company-id` | str | — | Filter by company |
| `--limit` | int | 20 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

### `ac crm people get <person-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

### `ac crm people create`
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

### `ac crm people update <person-id>`
Same optional flags as `create`. Only provided fields are updated.

### `ac crm people delete <person-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Output raw JSON |

---

## Deals

### `ac crm deals list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--stage` | str | — | Filter by pipeline stage |
| `--company-id` | str | — | Filter by company |
| `--owner-id` | str | — | Filter by deal owner |
| `--limit` | int | 20 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

### `ac crm deals get <deal-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

### `ac crm deals create`
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

### `ac crm deals update <deal-id>`
Same optional flags as `create`. Only provided fields are updated.

### `ac crm deals move <deal-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--stage` | str | yes | Target pipeline stage |
| `--json` | flag | no | Output raw JSON |

### `ac crm deals order`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--stage` | str | yes | Pipeline stage to reorder |
| `--deal-ids` | str | yes | Comma-separated deal IDs in desired order |
| `--json` | flag | no | Output raw JSON |

### `ac crm deals delete <deal-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Output raw JSON |

---

## Activities

### `ac crm activities list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--deal-id` | str | — | Filter by deal |
| `--company-id` | str | — | Filter by company |
| `--contact-id` | str | — | Filter by contact |
| `--type` | str | — | Filter by type (call, email, meeting, task) |
| `--status` | str | — | Filter by status (pending, completed) |
| `--sort-by` | str | — | Sort field |
| `--limit` | int | 20 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

### `ac crm activities get <activity-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

### `ac crm activities create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--type` | str | yes | Activity type (call, email, meeting, task) |
| `--title` | str | yes | Activity title |
| `--due-date` | str | no | ISO date |
| `--priority` | str | no | Priority level (low, medium, high, urgent) |
| `--deal-id` | str | no | Link to deal |
| `--company-id` | str | no | Link to company |
| `--contact-id` | str | no | Link to contact |
| `--description` | str | no | Free-text description |
| `--json` | flag | no | Output raw JSON |

### `ac crm activities update <activity-id>`
All flags from `create` are optional. Only provided fields are updated.

### `ac crm activities complete <activity-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

### `ac crm activities delete <activity-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Output raw JSON |

---

## Communications

### `ac crm comms list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--company-id` | str | — | Filter by company |
| `--contact-id` | str | — | Filter by contact |
| `--deal-id` | str | — | Filter by deal |
| `--type` | str | — | Filter by type (email, etc.) |
| `--direction` | str | — | Filter by direction (inbound, outbound) |
| `--status` | str | — | Filter by status |
| `--limit` | int | 20 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

### `ac crm comms get <communication-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

### `ac crm comms thread <thread-id>`
Shows all messages in a conversation thread.

### `ac crm comms unread`
Shows unread thread counts. No flags required.

### `ac crm comms unread-thread-ids`
Returns list of unread thread IDs (useful for scripting).

### `ac crm comms mark-read <thread-id>`
Marks all messages in a thread as read.

### `ac crm comms contact-by-email <email>`
Look up a CRM contact by their email address.

### `ac crm comms resolve-contact <email>`
| Flag | Type | Description |
|------|------|-------------|
| `--name` | str | Contact name (if creating new) |
| `--job-title` | str | Job title |
| `--company-id` | str | Link to company |

Finds or creates a contact record for the given email.

### `ac crm comms draft-email`
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

### `ac crm comms generate-draft`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--mode` | str | yes | Draft mode (cold_outreach, follow_up, reply) |
| `--recipient-name` | str | yes | Recipient's name |
| `--recipient-email` | str | no | Recipient's email |
| `--company-name` | str | no | Recipient's company |
| `--sender-name` | str | no | Your name |
| `--original-subject` | str | no | Subject of email being replied to |
| `--original-content` | str | no | Content of email being replied to |
| `--context` | str | no | Additional context for draft generation |
| `--json` | flag | no | Output raw JSON |

### `ac crm comms update <communication-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--subject` | str | Update subject |
| `--content` | str | Update content |
| `--status` | str | Update status |
| `--tags` | str | Comma-separated tags |
| `--json` | flag | Output raw JSON |

### `ac crm comms archive`
| Flag | Type | Description |
|------|------|-------------|
| `--thread-id` | str | Archive entire thread |
| `--comm-id` | str | Archive single message |

One of `--thread-id` or `--comm-id` is required.

### `ac crm comms unarchive`
Same flags as `archive`.

### `ac crm comms delete <communication-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation |
| `--json` | flag | Output raw JSON |

### `ac crm comms delete-thread <thread-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation |
| `--json` | flag | Output raw JSON |

---

## Lists

### `ac crm lists list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 20 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

### `ac crm lists get <list-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

### `ac crm lists create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | List name |
| `--member-type` | str | no | person, company, or mixed |
| `--type` | str | no | static or dynamic |
| `--description` | str | no | List description |
| `--json` | flag | no | Output raw JSON |

### `ac crm lists update <list-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--name` | str | New name |
| `--description` | str | New description |
| `--type` | str | static or dynamic |
| `--member-type` | str | person, company, or mixed |
| `--json` | flag | Output raw JSON |

### `ac crm lists members <list-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 20 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Output raw JSON |

### `ac crm lists add-member <list-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--person-id` | str | Add a person |
| `--company-id` | str | Add a company |
| `--json` | flag | Output raw JSON |

One of `--person-id` or `--company-id` is required.

### `ac crm lists remove-member <list-id>`
Same flags as `add-member`.

### `ac crm lists delete <list-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation |
| `--json` | flag | Output raw JSON |

---

## Import

### `ac crm import preview`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--file` | path | yes | Path to JSON file to import |
| `--json` | flag | no | Output raw JSON |

Shows a summary of what will be imported (new records, duplicates, errors)
before committing.

### `ac crm import commit`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--preview-id` | str | yes | ID from the preview step |
| `--auto-accept` | flag | no | Skip confirmation |
| `--json` | flag | no | Output raw JSON |

---

## Search & Dashboard

### `ac crm search <query>`
Searches across companies, contacts, and deals. Returns matching records
from all three domains.

| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Output raw JSON |

### `ac crm dashboard`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--period` | int | 30 | Number of days to report on |
| `--json` | flag | off | Output raw JSON |

Shows pipeline metrics: total deals, total value, leads created, messages
sent, and activities completed for the given period.
