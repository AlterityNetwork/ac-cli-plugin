# Platform Quick Reference

For full flag tables see `commands.md` (Platform section).

## Files (Images)

```bash
ac files images upload <file-path> --category avatars
ac files images delete <r2-object-key> [--yes]
```

Categories: `avatars`, `organization_logos`, `crm_company_logos`, `general_images`, `apps_assets`
Formats: .jpg, .jpeg, .png, .gif, .webp, .svg, .avif (max 1 MB)

## Apps

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

`--org-id` auto-resolves from your login session — only specify it when operating on a different org.

## Writing Styles

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

## Nylas (Email Integration)

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

## Hooks

```bash
ac hooks list <capability>     # List available hooks for a capability
```

## Messaging

```bash
ac messaging sessions                          # List active messaging sessions
ac messaging link --token <link-token>         # Link external messaging sender
```

## Chat (AI Threads)

```bash
ac chat threads list
ac chat threads create --title "Project Discussion"
ac chat threads update <thread-id> [--title "New Title"] [--archived/--no-archived]
ac chat threads delete <thread-id> [--yes]
ac chat threads messages <thread-id>
ac chat threads generate-title <thread-id>
ac chat threads send <thread-id> "What's on my plate today?" [--context "..."] \
  [--document-id <id>...]                       # Non-streaming send
ac chat threads escalate <thread-id> [--note "..."] [--message-id <id>]
ac chat messages update-data <message-id> --data '{"key":"value"}'
```

## Resources (Knowledge Base)

```bash
ac resources list [--limit 50] [--offset 0]
ac resources upload <file-path> --name "Source Name" [--description "..."] [--tags "tag1,tag2"]
ac resources delete <resource-id> [--yes]
ac resources status <resource-id>
```

Formats: .pdf, .txt, .md, .docx (max 10 MB). `--name` is required.

## Profiles

```bash
ac profiles me                                    # View your profile
ac profiles update [--first-name "Jane"] [--last-name "Smith"] [--bio "..."] \
  [--job-title "Developer"] [--avatar-url "..."] [--email "jane@example.com"]
ac profiles members [--limit 50] [--offset 0]     # List org members
ac profiles set-organization <org-id>             # Switch active org (per-user)
ac profiles set-password                          # Mark password as set (post-magic-link)
ac profiles subscription                          # View current org subscription
```

> **"Switch active organization" → `ac profiles set-organization <org-id>`**, NOT `ac env use` (env is local/staging/production) and NOT `ac admin orgs` (which manages org records, not user's active org).
