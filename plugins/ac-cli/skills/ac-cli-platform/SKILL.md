---
name: ac-cli-platform
description: >
  Guide for using the AgencyCore CLI (`ac`) platform utilities -- file/image
  management, app installation, writing styles, Nylas email integration,
  environment switching, health checks, platform hooks, AI chat threads,
  knowledge base resources, and user profiles. Use this skill when someone asks
  about uploading images, installing apps, managing writing styles, connecting
  email accounts, switching environments, checking API health, listing hooks,
  chat threads, AI conversations, resources, knowledge base, uploading documents,
  user profile, or org members. Also trigger when users mention "ac files",
  "ac apps", "ac styles", "ac nylas", "ac env", "ac health", "image upload",
  "app install", "writing style", "email integration", "environment switching",
  "ac chat", "ac resources", "ac profiles", "my profile", "upload document",
  "knowledge base".
allowed-tools:
  - Bash
argument-hint: "[command or question]"
---

# AgencyCore CLI -- Platform Utilities

The `ac` CLI includes several platform utility commands: file management, app
installation, writing styles, Nylas email integration, environment switching,
health checks, and platform hooks.

---

## Step 0: Ensure CLI Is Installed (Always Do This First)

Before running any command, check if the `ac` CLI is available and install it
automatically if missing. **Do NOT ask the user where the code is -- the
package is public on PyPI.**

```bash
pip install --upgrade agencycore-cli
```

If `pip` is not available, try `uv pip install --upgrade agencycore-cli` or `pipx upgrade agencycore-cli`.

Then verify it works:
```bash
ac --help
```

---

## Step 1: Authentication Check

Most platform commands require authentication. Verify:

```bash
ac whoami
```

- **If authenticated**: Proceed to the command the user needs.
- **If not authenticated**: Ask for email and password, then run:
  ```bash
  ac login --email "user@example.com" --password "their-password"
  ```

**Exceptions**: `ac health check` and `ac env` commands do not require authentication.

---

## Quick Reference

Read `references/commands.md` for the full command reference with all flags.

### Files (Images)

```bash
ac files images upload <file-path> --category avatars
ac files images delete <r2-object-key> [--yes]
```

Supported categories: `avatars`, `organization_logos`, `crm_company_logos`, `general_images`, `apps_assets`
Supported formats: .jpg, .jpeg, .png, .gif, .webp, .svg, .avif (max 1 MB)

### Apps

```bash
ac apps list [--org-id <id>] [--include-inactive] [--limit 100]
ac apps install <app-slug> [--org-id <id>]
ac apps uninstall <app-slug> [--org-id <id>] [--yes]
ac apps usage <app-slug> [--org-id <id>]
ac apps usage-event <app-slug> --event-type "page_view" [--metadata '{"page":"dashboard"}']
ac apps configs <app-slug> [--org-id <id>] [--no-mask-secrets]
ac apps update-config <app-slug> <config-key> --value "new-value" [--org-id <id>]
ac apps delete-config <app-slug> <config-key> [--org-id <id>] [--yes]
```

### Writing Styles

```bash
ac styles list [--include-inactive]
ac styles get <style-id>
ac styles create --name "Professional" [--description "..."] [--tone formal] [--formality high]
ac styles update <style-id> [--name "Updated"] [--tone casual]
ac styles delete <style-id> [--yes]
ac styles train <style-id> --sample-text "Example email text..."
ac styles feedback <session-id> --rating 4 [--comments "Good but too formal"]
ac styles iterate <session-id> --feedback "Make it more casual"
ac styles analyze --text "Analyze this text for style..."
```

### Nylas (Email Integration)

```bash
ac nylas oauth-start [--provider google] [--return-path "/settings"]
ac nylas account
ac nylas org-accounts
ac nylas disconnect [--yes]
ac nylas send --to "jane@example.com" --subject "Hello" --body "Hi Jane..." \
  [--reply-to-message-id <id>]
ac nylas update-signature --signature "<p>Best regards</p>"
ac nylas validate-signature --signature "<p>Best regards</p>"
```

### Environment

```bash
ac env list                    # Show all environments and login status
ac env show                    # Show active environment details
ac env use <name>              # Switch environment (local, staging, production)
```

### Health

```bash
ac health check [--api-url https://custom-api.example.com]
```

No authentication required. Checks if the API is reachable.

### Hooks

```bash
ac hooks list <capability>     # List available hooks for a capability
```

### Chat (AI Threads)

```bash
ac chat threads list
ac chat threads create --title "Project Discussion"
ac chat threads update <thread-id> [--title "New Title"] [--archived/--no-archived]
ac chat threads delete <thread-id> [--yes]
ac chat threads messages <thread-id>
ac chat threads generate-title <thread-id>
```

### Resources (Knowledge Base)

```bash
ac resources list [--limit 50] [--offset 0]
ac resources upload <file-path> --name "Source Name" [--description "..."] [--tags "tag1,tag2"]
ac resources delete <resource-id> [--yes]
ac resources status <resource-id>
```

Supported formats: .pdf, .txt, .md, .docx (max 10 MB)

### Profiles

```bash
ac profiles me                                    # View your profile
ac profiles update [--first-name "Jane"] [--last-name "Smith"] [--bio "..."] \
  [--job-title "Developer"] [--avatar-url "..."] [--email "jane@example.com"]
ac profiles members [--limit 50] [--offset 0]     # List org members
```

---

## Common Workflows

### Upload an organization logo

```bash
# Upload the image
ac files images upload ./logo.png --category organization_logos --json

# The response includes the R2 object key and public URL
```

### Install and configure an app

```bash
# 1. Install the app
ac apps install my-app --json

# 2. Check current configuration
ac apps configs my-app --json

# 3. Update a config value
ac apps update-config my-app api_key --value "sk-..." --json
```

### Set up email integration

```bash
# 1. Start OAuth flow (opens browser for Google/Microsoft auth)
ac nylas oauth-start --provider google

# 2. After completing OAuth, verify the account is connected
ac nylas account --json

# 3. Update your email signature
ac nylas update-signature --signature "<p>Best regards,<br>Jane Smith</p>"
```

### Train a writing style

```bash
# 1. Create a new style
ac styles create --name "Sales Outreach" --tone professional --formality medium --json

# 2. Start training with a sample
ac styles train <style-id> --sample-text "Hi Jane, I noticed your team..."

# 3. Submit feedback on the training
ac styles feedback <session-id> --rating 3 --comments "Good but too formal"

# 4. Iterate to refine
ac styles iterate <session-id> --feedback "Make it more conversational"
```

### Switch between environments

```bash
# See which environments are available
ac env list

# Switch to staging
ac env use staging

# Verify you're on the right environment
ac env show

# Log in to the new environment
ac login --email "user@example.com" --password "password"
```

### Chat with AI

```bash
# 1. Create a new thread
ac chat threads create --title "Q2 Planning" --json

# 2. View messages in a thread
ac chat threads messages <thread-id>

# 3. Generate a title from conversation content
ac chat threads generate-title <thread-id>

# 4. Archive when done
ac chat threads update <thread-id> --archived
```

### Upload a knowledge base resource

```bash
# 1. Upload a document
ac resources upload ./product-guide.pdf --name "Product Guide" \
  --description "Main product documentation" --tags "docs,product" --json

# 2. Check processing status
ac resources status <resource-id>

# 3. List all resources
ac resources list --json
```

---

## Important Patterns

### Organization ID Auto-Resolution
For `ac apps` commands, `--org-id` is auto-resolved from your login session
(`/whoami`). You only need to specify it when operating on a different
organization.

### Image Upload Constraints
- Max file size: 1 MB
- Allowed formats: .jpg, .jpeg, .png, .gif, .webp, .svg, .avif
- Category is required and determines the storage path

### Environment Names
Valid environment names: `local`, `staging`, `production`

### Resource Upload Constraints
- Max file size: 10 MB
- Allowed formats: .pdf, .txt, .md, .docx
- `--name` is required and sets the source name

### JSON Output
All commands support `--json` for structured output:
```bash
ac apps list --json | jq '.[].slug'
ac styles list --json | jq '.[] | {name, id}'
```

### Non-Interactive Mode
```bash
AC_YES=1 ac apps uninstall my-app
AC_YES=1 ac files images delete <key>
```

### Semantic Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Validation error (422) |
| 3 | Not found (404) |
| 4 | Auth/permission (401/403) |
| 5 | Conflict (409) |

---

## Auth Commands Reference

| Command | What it does |
|---------|-------------|
| `ac login` | Sign in (stores credentials locally) |
| `ac logout` | Clear stored credentials |
| `ac whoami` | Show your user info and organization |
| `ac health check` | Verify the API is reachable (no auth needed) |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Not authenticated" error | Run `ac login` with credentials |
| Connection refused | Check `ac health check` |
| Command not found: `ac` | Run `pip install --upgrade agencycore-cli` |
| Image upload fails | Check file size (max 1 MB) and format (.jpg, .png, .gif, .webp, .svg, .avif) |
| App install returns 409 | App is already installed for this organization |
| Nylas OAuth fails | Ensure browser access and that network allows OAuth redirects |
| `ac env use` has no effect | You still need to `ac login` after switching environments |
| Writing style training slow | Training involves AI processing -- wait for the response |
