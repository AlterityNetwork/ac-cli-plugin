# Admin Quick Reference

Admin commands require super admin privileges. Verify with `ac whoami` (look for `superadmin` role). For full flag tables see `commands.md` (Admin section).

## Users

```bash
ac admin users list [--query "jane"] [--sort created_at] [--order desc] [--page 1] [--page-size 50]
ac admin users get <user-id>
ac admin users create --email jane@example.com --password "secret123" [--full-name "Jane Smith"]
ac admin users update <user-id> [--full-name "Jane Doe"] [--is-superadmin]
ac admin users delete <user-id> [--yes]
ac admin users auth-search --email jane@example.com
ac admin users search --email jane@example.com
ac admin users reset-password <user-id> [--yes]
ac admin users impersonate <user-id>
ac admin users exit-impersonation
ac admin users generate-link <user-id> [--send-email]
```

## Organizations

```bash
ac admin orgs list [--query "acme"] [--sort created_at] [--order desc] [--page 1] [--page-size 50]
ac admin orgs get <org-id>
ac admin orgs create --name "Acme Corp" [--slug acme-corp] [--plan pro]
ac admin orgs update <org-id> [--name "New Name"] [--slug new-slug] [--plan enterprise]
ac admin orgs delete <org-id> [--yes]
ac admin orgs members <org-id> [--page 1] [--page-size 50]
ac admin orgs add-member <org-id> --user-id <user-id> [--role member]
ac admin orgs update-member <org-id> <user-id> --role admin
ac admin orgs remove-member <org-id> <user-id> [--yes]
ac admin orgs transfer-ownership <org-id> --new-owner-id <user-id> [--yes]
```

## Queues

```bash
ac admin queues health
ac admin queues stats
ac admin queues queue-stats <queue-name>
ac admin queues metrics
ac admin queues send-to-sentry
ac admin queues job-performance <job-id>
ac admin queues failed <queue-name> [--limit 50]
ac admin queues retry-all <queue-name> [--yes]
ac admin queues retry-job <job-id>
ac admin queues clear-failed <queue-name> [--yes]
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
  [--sort total_actions] [--order desc] [--page 1] [--page-size 50] [--search "jane"]
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

```bash
ac admin platform-activity summary [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>]
ac admin platform-activity users [--start-date 2026-01-01] [--end-date 2026-03-23] [--org-id <id>] \
  [--sort total_events] [--order desc] [--page 1] [--page-size 50] [--query "jane"]
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
  [-q "VPs of Eng"] [--page 1] [--page-size 25] [--all]

ac admin searches run <run-id>

ac admin searches companies [--source sonar|headhunter|both] \
  [--org-id <id>...] [--user-id <id>...] [-q "acme"] \
  [--page 1] [--page-size 25] [--all]

ac admin searches people [--source headhunter] \
  [--org-id <id>...] [--user-id <id>...] [--page 1] [--page-size 25] [--all]
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
ac admin subscriptions get <subscription-id>
ac admin subscriptions create --org-id <id> --plan-id <id> --billing-period monthly \
  --started-at 2026-04-01 [--status active] [--ended-at 2026-12-31] \
  [--trial-ends-at 2026-04-15] [--stripe-customer-id cus_x] [--stripe-subscription-id sub_x]
ac admin subscriptions update <subscription-id> [--plan-id <id>] [--status cancelled]
ac admin subscriptions delete <subscription-id> [--yes]
```

## Subscription Plans

```bash
ac admin subscription-plans list
ac admin subscription-plans get <plan-id>
ac admin subscription-plans create --slug pro --name "Pro" \
  --monthly-price-cents 4900 --annual-price-cents 49000 \
  [--description "..."] [--features '{"seats":10}'] [--active/--inactive]
ac admin subscription-plans update <plan-id> [--name "Pro Plus"] [--features '{"seats":25}']
ac admin subscription-plans delete <plan-id> [--yes]
```
