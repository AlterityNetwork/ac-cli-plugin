# Admin Quick Reference

Admin commands require super admin privileges. Verify with `ac whoami` (look for `superadmin` role). For full flag tables see `commands.md` (Admin section).

## Users

```bash
ac admin users list [--query "jane"] [--sort created_at] [--order desc] [--limit 50] [--offset 0]
ac admin users get <user-id>
ac admin users create --email jane@example.com --password "secret123" [--full-name "Jane Smith"]
ac admin users update <user-id> [--full-name "Jane Doe"] [--is-superadmin]
ac admin users delete <user-id> [--yes]
ac admin users auth-search --email jane@example.com
ac admin users search --email jane@example.com
ac admin users reset-password <user-id> [--yes]
ac admin users require-tos-resign <user-id> [--yes] [--json]
ac admin users impersonate <user-id>
ac admin users exit-impersonation
ac admin users impersonation-status --session-id <session-id>     # Check active session
ac admin users impersonation-end    --session-id <session-id>     # End session by ID
ac admin users generate-link <user-id> [--send-email]
```

## CRM Hard-Delete (super admin, destructive)

Bypasses soft-delete. Unrecoverable. Pair with `--yes` to skip the confirm; refuse without explicit instruction.

```bash
ac admin crm hard-delete-company <company-id> [--yes]
ac admin crm hard-delete-person  <person-id>  [--yes]
```

## Organizations

```bash
ac admin orgs list [--query "acme"] [--sort created_at] [--order desc] [--limit 50] [--offset 0]
ac admin orgs get <org-id>
ac admin orgs create --name "Acme Corp" [--slug acme-corp] [--plan pro]
ac admin orgs update <org-id> [--name "New Name"] [--slug new-slug] [--plan enterprise]
ac admin orgs delete <org-id> [--yes]
ac admin orgs members <org-id> [--page 1] [--page-size 50]
ac admin orgs add-member <org-id> --user-id <user-id> [--role member]
ac admin orgs update-member <org-id> <user-id> --role admin
ac admin orgs remove-member <org-id> <user-id> [--yes]
ac admin orgs transfer-ownership <org-id> --new-owner-id <user-id> [--yes]
ac admin orgs suspend    <org-id> --reason <trial_expired|non_payment|misconduct> [--yes]   # blocks all members except billing
ac admin orgs unsuspend  <org-id>                                                          # restores member access
```

## Queues

```bash
ac admin queues health
ac admin queues stats
ac admin queues queue-stats <queue-name>
ac admin queues metrics
ac admin queues send-to-sentry
ac admin queues job-performance <job-id>
```

**Standard "queue health" recipe** — when the user reports unhealthy queues, chain the diagnostic steps in one call:

```bash
ac admin queues health --json && \
ac admin queues stats --json && \
ac admin queues metrics --json
```

## Demo

```bash
ac admin demo scrape-website --url "https://example.com"
ac admin demo generate-org [--industry "Technology"] [--size "medium"]
ac admin demo generate-profile [--industry "Technology"]
ac admin demo prepare-account --org-name "Demo Corp" [--template default]
ac admin demo list-accounts [--page 1] [--page-size 50] [--sort created_at] [--order desc]
ac admin demo get-account <org-id>
ac admin demo update-account <org-id> [--status active] [--notes "Updated demo"]
ac admin demo delete-account <org-id> [--yes]
ac admin demo cleanup [--max-age-days 30] [--yes]
ac admin demo stats
```

## Onboarding

```bash
ac admin onboarding create --email user@example.com --first-name "Jane" \
  --last-name "Smith" --org-name "Acme Corp" [--website-url "https://acme.com"] \
  [--country US] [--timezone "America/New_York"] [--locale en] [--currency USD] \
  [--job-title "CEO"] [--bio "..."] [--linkedin "https://..."] \
  [--contact-email "alt@example.com"] [--calendly-url "https://..."]
ac admin onboarding list [--status pending] [--query "acme"] [--page 1] [--page-size 25]
ac admin onboarding get <org-id>
ac admin onboarding delete <org-id>
ac admin onboarding send-link <org-id> [--send-email]
ac admin onboarding impersonate <org-id>
ac admin onboarding end-impersonation <org-id>
ac admin onboarding activate <org-id> [--send-password-reset] (default: sends reset email)
ac admin onboarding deactivate <org-id>
ac admin onboarding update-config <org-id> [--show-calendly] [--calendly-url "https://..."]
ac admin onboarding get-settings
ac admin onboarding update-settings [--terms-html "<p>...</p>"] \
  [--calendly-url "https://..."] [--calendly-enabled/--no-calendly-enabled]
```

## App Usage

```bash
ac admin app-usage summary [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin app-usage users [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>] \
  [--sort total_events] [--order desc] [--limit 50] [--offset 0] [--search "jane"]
ac admin app-usage user <user-id> [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
```

## AI Usage

```bash
ac admin ai-usage summary [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin ai-usage users [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>] \
  [--sort total_tokens] [--order desc] [--page 1] [--page-size 50] [--search "jane"]
ac admin ai-usage user <user-id> [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin ai-usage by-model [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin ai-usage by-workflow [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin ai-usage details [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>] \
  [--limit 50] [--offset 0] [--model-id <id>] [--user-id <id>] [--workflow-run-id <id>]
```

## Platform Activity

> Sort key for `users` is **`total_events`** (NOT `event_count` / `events` / `activity`). Use the exact string `total_events`.

```bash
ac admin platform-activity summary [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin platform-activity users [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>] \
  [--sort total_events] [--order desc] [--limit 50] [--offset 0] [--query "jane"]
ac admin platform-activity user <user-id> [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
```

## Searches (Sonar + Headhunter)

Cross-org analytics. Responses are PII-scrubbed: people rows omit names, emails, LinkedIn URLs, avatars, free-text summaries; only role, country, quality scores remain. `trigger_data` on runs is sanitized the same way.

```bash
ac admin searches summary [--source sonar|headhunter|both] \
  [--start-date 2026-04-01] [--end-date 2026-04-27] \
  [--org-id <id>...] [--user-id <id>...]

ac admin searches runs [--source sonar|headhunter|both] \
  [--org-id <id>...] [--user-id <id>...] [--status completed|failed|running|pending] \
  [-q "VPs of Eng"] [--limit 25] [--offset 0] [--all]

ac admin searches run <run-id>

ac admin searches companies [--source sonar|headhunter|both] \
  [--org-id <id>...] [--user-id <id>...] [-q "acme"] \
  [--limit 25] [--offset 0] [--all]

ac admin searches people [--source headhunter] \
  [--org-id <id>...] [--user-id <id>...] [--limit 25] [--offset 0] [--all]
```

Notes:
- `--org-id` and `--user-id` are repeatable for multi-value filters.
- `--all` walks every page (page-size 100) and emits a single JSON array. Capped at 50,000 items — narrow filters if you hit the cap.
- Pipe with `--json | jq` for ad-hoc analysis. Examples:
  - `ac admin searches summary --source headhunter --json | jq '.success_rate'`
  - `ac admin searches runs --status failed --all | jq 'group_by(.organization_id) | map({org: .[0].organization_id, count: length})'`

## Legal Documents

```bash
ac admin legal-docs list [--document-type terms_of_service]
ac admin legal-docs get <document-id>
ac admin legal-docs create --document-type terms_of_service --version "1.0" --title "Terms of Service" \
  [--content-html "<p>...</p>"]
ac admin legal-docs update <document-id> [--title "Updated Title"] [--content-html "<p>...</p>"]
ac admin legal-docs delete <document-id> [--yes]
ac admin legal-docs set-current <document-id>
```

## Analytics Overview (unified summary)

```bash
ac admin analytics-overview [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
```

## Cache Stats

```bash
ac admin cache-stats
```

## Chat Escalations

```bash
ac admin chat-escalations list [--status open|triaged|resolved]
ac admin chat-escalations update <escalation-id> --status resolved [--note "..."]
```

## Subscriptions

```bash
ac admin subscriptions list [--org-id <id>] [--status active] [--limit 50] [--offset 0]
ac admin subscriptions get <subscription-id>   # includes dunning detail: decline/advice codes, attempt count, next retry, live Stripe amount

# `create` requires ALL FOUR: --org-id, --plan-id, --billing-period, --started-at.
# --billing-mode is stripe (default) or manual. A manual subscription is comped/
# offline/legacy: admin-set status, no Stripe object, no Activate, never reconciled.
# Per-org custom pricing (kept off the shared catalogue): --custom-price-cents is
# the NET price in cents; Stripe adds VAT on top at invoice time.
ac admin subscriptions create --org-id <id> --plan-id <id> --billing-period monthly \
  --started-at 2026-04-01 [--billing-mode manual] [--status active] [--ended-at 2026-12-31] [--trial-ends-at 2026-04-15] \
  [--custom-price-cents 25000] [--currency gbp] [--coupon FOUNDER50]

# `status` is webhook-authoritative and the stripe ids are system-managed, so
# neither is settable on update (and the stripe ids are not settable on create).
ac admin subscriptions update <subscription-id> [--plan-id <id>] [--billing-period annual] \
  [--billing-mode manual] [--started-at 2026-04-01] [--ended-at 2026-12-31] [--trial-ends-at 2026-04-15] \
  [--custom-price-cents 25000] [--currency gbp] [--coupon FOUNDER50]
ac admin subscriptions delete <subscription-id> [--yes]

# Activate: ONE action grants the org account access AND starts billing
# off-session (charges the first period now). If the charge needs authentication
# it stays incomplete and the customer is emailed the hosted payment link; the
# org then appears under `worklists` stuck.
ac admin subscriptions activate-billing <subscription-id> [--yes]

# Link an EXISTING Stripe subscription to this local row. Distinct from
# activate-billing: linking never creates a Stripe object and never charges. It
# adopts the live Stripe status and stamps our ids into the Stripe metadata.
# Safeguards: refuses a manual subscription, blocks a Stripe sub already linked
# elsewhere or one owned by a different customer, and is idempotent (re-linking
# the same pair is a no-op). Use `ac admin billing stripe-subscriptions` to find
ac admin billing refund <charge-id> [--amount-cents N] [--reason duplicate|fraudulent|requested_by_customer] [--yes]
# orphaned Stripe subscription ids.
ac admin subscriptions link <subscription-id> --stripe-subscription-id <sub_id> [--yes]

# Clear the Stripe link (leaves the Stripe subscription itself running).
ac admin subscriptions unlink <subscription-id> [--yes]

# Pause / resume billing. Pause stops Stripe collection (held invoices are
# voided, the customer is not billed) and the status reads paused; resume
# returns to the normal cycle. Only active subs pause; only paused subs resume.
ac admin subscriptions pause <subscription-id> [--yes]
ac admin subscriptions resume <subscription-id> [--yes]

# Downgrade to free/comped: cancels the Stripe subscription immediately, flags
# the org comped (kept out of billing worklists and auto-suspend), and converts
# the local row to a manual active subscription.
ac admin subscriptions switch-comped <subscription-id> [--yes]

# Email the account owner the hosted invoice link for an overdue payment and
# record the send (visible as Manual Reminders / Last Reminder on `get`).
# Requires status past_due/unpaid/incomplete and a hosted invoice link.
ac admin subscriptions send-reminder <subscription-id> [--yes]

# Revenue-leakage guard: the awaiting-activation queue + the stuck / needs-
# attention bucket (activation_stuck, no_plan_assigned, unbilled_access).
ac admin subscriptions worklists   # buckets: payment overdue, awaiting activation, stuck [--json]
```

## Billing

```bash
# List live Stripe subscriptions cross-referenced with local rows. Each Stripe
# sub shows its plan name (from the catalogue), billing interval, next bill date
# (current period end), lifetime total paid, its linked local subscription id (or
# that it is an orphan); `broken_links` flags local rows whose Stripe subscription
# no longer exists. Use this to find the Stripe subscription id to pass to
# `subscriptions link`. The Stripe list is paginated; broken-links is complete.
ac admin billing stripe-subscriptions [--limit 50] [--offset 0] [--json]

# Import active Stripe products + recurring prices into the plan catalogue.
# Idempotent: each active product with a recurring price is matched to a plan by
# stripe_product_id (prices / name updated) or created as a new plan; products
# with no recurring price are skipped. Reports imported / updated / skipped counts
# plus notes (e.g. a product missing a monthly or annual price). Requires --yes to
# skip the confirmation prompt. Use when plans were set up in the Stripe dashboard
# rather than via `subscription-plans create`.
ac admin billing import-stripe-products [--yes] [--json]
```

## Subscription Plans

> Subcommand is **`subscription-plans`** (full word), NOT `plans`. `ac admin plans` does not exist.

> **Pricing in cents.** When user says "$9/mo" → `--monthly-price-cents 900`. "$99/yr" → `--annual-price-cents 9900`. "$49.99/mo" → `--monthly-price-cents 4999`. Always multiply dollars × 100. The `--slug` is lowercase kebab of the user's plan name (e.g. "Starter" → `--slug starter`).

```bash
ac admin subscription-plans list
ac admin subscription-plans get <plan-id>

# Required flags: --slug, --name, --monthly-price-cents, --annual-price-cents
ac admin subscription-plans create --slug pro --name "Pro" \
  --monthly-price-cents 4900 --annual-price-cents 49000 \
  [--description "..."] [--features '{"seats":10}'] [--active/--inactive]

# Example: "Starter $9/mo $99/yr"
ac admin subscription-plans create --slug starter --name "Starter" \
  --monthly-price-cents 900 --annual-price-cents 9900

ac admin subscription-plans update <plan-id> [--name "Pro Plus"] [--features '{"seats":25}']
ac admin subscription-plans delete <plan-id> [--yes]
```
