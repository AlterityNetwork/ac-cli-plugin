# Common Workflow Recipes

Multi-step recipes for non-core flows. Core recipes (CRM company+contact+deal, bulk import, sequence launch, draft approval, schedule, env switch) are in the main `SKILL.md`.

## CRM: Check engagement

```bash
# Engagement metrics for the last 30 days
ac crm engagement-dashboard

# Custom period (60 days)
ac crm engagement-dashboard --period 60

# Raw data for analysis
ac crm engagement-dashboard --json | jq '{open_rate, click_rate, reply_rate}'
```

## Envoy: Manage inbox

```bash
ac envoy inbox list --status open --json
ac envoy inbox messages <thread-id>
ac envoy inbox reply <thread-id> --body "Thanks for your interest!"
ac envoy inbox complete <thread-id>
```

## Workflows: Trigger and monitor a run

```bash
ac workflows runs create <workflow-id> --input '{"param":"value"}' --json
ac workflows runs get <workflow-id> <run-id> --json
ac workflows runs logs <workflow-id> <run-id> --json
```

## Workflows: Parse CSV and review discovered companies

```bash
# 1. Parse the CSV
ac workflows csv-parse leads.csv --json

# 2. Trigger a run that discovers companies
ac workflows runs create <workflow-id> --input '{"source":"csv"}' --json

# 3. List discovered companies
ac workflows run-companies list <workflow-id> --json

# 4. Add promising ones to CRM
ac workflows run-companies add-to-crm <workflow-id> --company-ids id1,id2
```

## Workflows: Review and import discovered people

```bash
# 1. List discovered people
ac workflows run-people list <workflow-id> --json

# 2. Preview company matches BEFORE importing
ac workflows run-people company-match-preview <workflow-id> --person-ids id1,id2

# 3. (optional) Search for a specific company match
ac workflows run-people company-search <workflow-id> --query "acme"

# 4. Add to CRM (optionally with overrides)
ac workflows run-people add-to-crm <workflow-id> --person-ids id1,id2

# 5. Verify count
ac workflows run-people crm-count <workflow-id>
```

## Admin: Check AI token usage

```bash
ac admin ai-usage summary --start-date 2026-03-01 --json
ac admin ai-usage users --start-date 2026-03-01 --sort total_tokens --order desc --limit 10 --json
ac admin ai-usage user <user-id> --start-date 2026-03-01 --json
ac admin ai-usage by-model --start-date 2026-03-01 --json
```

## Admin: Onboard a customer

```bash
# 1. Create the onboarding record
ac admin onboarding create --email "newcustomer@example.com" \
  --first-name "Jane" --last-name "Smith" \
  --org-name "Acme Corp" --website-url "https://acme.com" --json

# 2. Send the onboarding link
ac admin onboarding send-link <org-id> --send-email

# 3. Check status
ac admin onboarding get <org-id> --json

# 4. Activate when ready
ac admin onboarding activate <org-id> --send-password-reset
```

## Admin: Check queue health

```bash
ac admin queues health --json
ac admin queues stats --json
ac admin queues failed <queue-name> --limit 20 --json
AC_YES=1 ac admin queues retry-all <queue-name>
```

## Platform: Upload image, install app, train writing style

```bash
# Upload an organization logo
ac files images upload ./logo.png --category organization_logos --json

# Install and configure an app
ac apps install my-app --json
ac apps configs my-app --json
ac apps update-config my-app api_key --value "sk-..." --json

# Train a writing style
ac styles create --name "Sales Outreach" --tone professional --formality medium --json
ac styles train <style-id> --sample-text "Hi Jane, I noticed your team..."
ac styles feedback <session-id> --rating 3 --comments "Good but too formal"
ac styles iterate <session-id> --feedback "Make it more conversational"
```
