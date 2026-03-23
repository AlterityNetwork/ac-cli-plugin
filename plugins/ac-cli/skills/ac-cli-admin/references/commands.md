# AC CLI -- Admin Command Reference

Complete flag reference for all admin commands. All commands require super admin
authentication.

## Table of Contents

1. [Users](#users)
2. [Organizations](#organizations)
3. [Queues](#queues)
4. [Demo](#demo)
5. [Onboarding](#onboarding)
6. [App Usage](#app-usage)
7. [AI Usage](#ai-usage)

---

## Users

### `ac admin users list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--query` | str | None | Filter by name or email |
| `--sort` | str | "created_at" | Sort field |
| `--order` | str | "desc" | Sort order (asc/desc) |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Offset for pagination |
| `--json` | flag | off | Raw JSON output |

### `ac admin users get <user-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac admin users create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--email` | str | yes | User email |
| `--password` | str | yes | User password |
| `--full-name` | str | no | Full name |
| `--json` | flag | no | Raw JSON output |

### `ac admin users update <user-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--full-name` | str | no | Update full name |
| `--is-superadmin` | flag | no | Grant super admin privileges |
| `--json` | flag | no | Raw JSON output |

### `ac admin users delete <user-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac admin users auth-search`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--email` | str | yes | Email to search in auth provider |
| `--json` | flag | no | Raw JSON output |

### `ac admin users search`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--email` | str | yes | Email to search in application database |
| `--json` | flag | no | Raw JSON output |

### `ac admin users reset-password <user-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac admin users impersonate <user-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Switches to the specified user's session. All subsequent commands run as that user.

### `ac admin users exit-impersonation`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns to the original super admin session.

### `ac admin users generate-link <user-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--send-email` | flag | Send the link via email to the user |
| `--json` | flag | Raw JSON output |

---

## Organizations

### `ac admin orgs list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--query` | str | None | Filter by name or slug |
| `--sort` | str | "created_at" | Sort field |
| `--order` | str | "desc" | Sort order (asc/desc) |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Offset for pagination |
| `--json` | flag | off | Raw JSON output |

### `ac admin orgs get <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac admin orgs create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Organization name |
| `--slug` | str | no | URL-friendly slug (auto-generated from name if omitted) |
| `--plan` | str | no | Subscription plan |
| `--json` | flag | no | Raw JSON output |

### `ac admin orgs update <org-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | no | Update organization name |
| `--slug` | str | no | Update slug |
| `--plan` | str | no | Update subscription plan |
| `--json` | flag | no | Raw JSON output |

### `ac admin orgs delete <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac admin orgs members <org-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Offset for pagination |
| `--json` | flag | off | Raw JSON output |

### `ac admin orgs add-member <org-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--user-id` | str | yes | User ID to add |
| `--role` | str | no | Member role (e.g. admin, member) |
| `--json` | flag | no | Raw JSON output |

### `ac admin orgs update-member <org-id> <user-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--role` | str | yes | New role for the member |
| `--json` | flag | no | Raw JSON output |

### `ac admin orgs remove-member <org-id> <user-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac admin orgs transfer-ownership <org-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--new-owner-id` | str | yes | User ID of the new owner |
| `--yes` | flag | no | Skip confirmation prompt |
| `--json` | flag | no | Raw JSON output |

---

## Queues

### `ac admin queues health`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns overall health status of all queues.

### `ac admin queues stats`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns aggregate statistics across all queues.

### `ac admin queues queue-stats <queue-name>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns statistics for a specific queue.

### `ac admin queues metrics`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns performance metrics for all queues.

### `ac admin queues send-to-sentry`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Sends current queue errors to Sentry for monitoring.

### `ac admin queues job-performance`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns job execution performance statistics.

### `ac admin queues failed`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max failed jobs to return |
| `--queue` | str | None | Filter by queue name |
| `--json` | flag | off | Raw JSON output |

### `ac admin queues retry-all <queue-name>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

Retries all failed jobs in the specified queue.

### `ac admin queues retry-job <job-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Retries a single failed job by its ID.

### `ac admin queues clear-failed <queue-name>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

Permanently removes all failed jobs from the specified queue.

---

## Demo

### `ac admin demo scrape-website`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--url` | str | yes | Website URL to scrape for demo data |
| `--json` | flag | no | Raw JSON output |

### `ac admin demo generate-org`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--industry` | str | no | Industry for the generated organization |
| `--size` | str | no | Company size (e.g. small, medium, large) |
| `--json` | flag | no | Raw JSON output |

### `ac admin demo generate-profile`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--industry` | str | no | Industry for the generated profile |
| `--json` | flag | no | Raw JSON output |

### `ac admin demo prepare-account`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--org-name` | str | yes | Name for the demo organization |
| `--template` | str | no | Account template to use |
| `--json` | flag | no | Raw JSON output |

### `ac admin demo list-accounts`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Offset for pagination |
| `--sort` | str | "created_at" | Sort field |
| `--order` | str | "desc" | Sort order (asc/desc) |
| `--json` | flag | off | Raw JSON output |

### `ac admin demo get-account <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac admin demo update-account <org-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--status` | str | no | Update account status |
| `--notes` | str | no | Update account notes |
| `--json` | flag | no | Raw JSON output |

### `ac admin demo delete-account <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac admin demo cleanup`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--max-age-days` | int | 30 | Delete demo accounts older than this many days |
| `--yes` | flag | off | Skip confirmation prompt |
| `--json` | flag | off | Raw JSON output |

### `ac admin demo stats`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns aggregate statistics about demo accounts.

---

## Onboarding

### `ac admin onboarding create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--email` | str | yes | User email |
| `--first-name` | str | yes | First name |
| `--last-name` | str | yes | Last name |
| `--org-name` | str | yes | Organization name |
| `--website-url` | str | yes | Organization website URL |
| `--json` | flag | no | Raw JSON output |

Additional optional flags may be available for extended onboarding configuration.

### `ac admin onboarding list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--status` | str | None | Filter by onboarding status |
| `--query` | str | None | Search by name or email |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Offset for pagination |
| `--json` | flag | off | Raw JSON output |

### `ac admin onboarding get <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac admin onboarding delete <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac admin onboarding send-link <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--send-email` | flag | Send the onboarding link via email |
| `--json` | flag | Raw JSON output |

### `ac admin onboarding impersonate <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Switches to the onboarding organization's context for testing.

### `ac admin onboarding end-impersonation <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns to the original super admin session.

### `ac admin onboarding activate <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--send-password-reset/--no-send-password-reset` | flag | Send (or don't send) a password reset email on activation |
| `--json` | flag | Raw JSON output |

### `ac admin onboarding deactivate <org-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac admin onboarding update-config`
| Flag | Type | Description |
|------|------|-------------|
| `--show-calendly` | flag | Show Calendly widget in onboarding |
| `--calendly-url` | str | Calendly scheduling URL |
| `--json` | flag | Raw JSON output |

### `ac admin onboarding get-settings`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns current onboarding settings.

### `ac admin onboarding update-settings`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--terms-html` | str | no | HTML content for terms and conditions |
| `--calendly-url` | str | no | Calendly scheduling URL |
| `--calendly-enabled` | flag | no | Enable/disable Calendly integration |
| `--json` | flag | no | Raw JSON output |

---

## App Usage

### `ac admin app-usage summary`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format, e.g. 2026-01-01) |
| `--end-date` | str | None | End date (ISO format, e.g. 2026-03-23) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

### `ac admin app-usage users`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--sort` | str | None | Sort field (e.g. total_actions) |
| `--order` | str | None | Sort order (asc/desc) |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Offset for pagination |
| `--search` | str | None | Search by user name or email |
| `--json` | flag | off | Raw JSON output |

### `ac admin app-usage user <user-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

---

## AI Usage

### `ac admin ai-usage summary`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format, e.g. 2026-01-01) |
| `--end-date` | str | None | End date (ISO format, e.g. 2026-03-23) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

### `ac admin ai-usage users`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--sort` | str | None | Sort field (e.g. total_tokens, total_cost) |
| `--order` | str | None | Sort order (asc/desc) |
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Offset for pagination |
| `--search` | str | None | Search by user name or email |
| `--json` | flag | off | Raw JSON output |

### `ac admin ai-usage user <user-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

### `ac admin ai-usage by-model`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

### `ac admin ai-usage by-workflow`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--start-date` | str | None | Start date (ISO format) |
| `--end-date` | str | None | End date (ISO format) |
| `--org-id` | str | None | Filter by organization |
| `--json` | flag | off | Raw JSON output |

### `ac admin ai-usage details`
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
