# Platform Quick Reference

For full flag tables see `commands.md` (Platform section).

## Agentic Saved Searches

```bash
ac agentic saved-searches create --name "UK fintech" --brief '{"icp":"UK fintech firms"}'
ac agentic saved-searches list [--cursor <cursor>] [--limit 50]
ac agentic saved-searches get <saved-search-id>
ac agentic saved-searches patch <saved-search-id> --expected-updated-at <token> [--name "New name"] [--brief '{...}']
ac agentic saved-searches delete <saved-search-id> [--yes]
ac agentic saved-searches start <saved-search-id> --definition <definition-id> [--idempotency-key <key>]
ac agentic saved-searches diff <saved-search-id> [--cursor <cursor>] [--limit 50]
```

The brief must be a JSON object. It must contain a non-empty `icp` string or a
non-empty `company_criteria` array. `list` omits the brief. Use `get` when you
need the full brief or the current `updated_at` write token.

`patch` requires that token and at least one replacement field. A stale token
returns exit code 5. `start` freezes the stored brief and current baseline in a
normal Run. It does not create a schedule. `diff` reads only the latest
published successful Run. Start a new page walk if the published Run changes.
Deleting a saved search does not cancel a Run that already started.

## Agentic Prospect Review

```bash
ac agentic prospects list [--review-state new] [--cursor <cursor>] [--limit 50]
ac agentic prospects get <prospect-id>
ac agentic prospects people <prospect-id> [--cursor <cursor>] [--limit 50]
ac agentic prospects signals <prospect-id> [--cursor <cursor>] [--limit 50]
ac agentic prospects watch <prospect-id>
ac agentic prospects dismiss <prospect-id>
ac agentic prospects promote <prospect-id> [--person <id>]... [--list <list-id>] [--yes]
```

Use `--json` when a later command needs an ID or the full nested company,
person, or signal data. `watch` and `dismiss` are repeatable intents. Neither
can change a promoted prospect.

`promote` is the one command that writes CRM. It resolves or creates the CRM
company and each selected person, then sets the prospect to `promoted`. Repeat
`--person` for each prospect person id, taken from `ac agentic prospects people`.
It asks before it writes; pass `--yes` to skip the question. A second promotion
writes nothing and answers the same references.

## Organization Analytics

```bash
ac analytics overview [--period-days 30] [--json]
```

Shows cross-product output for the active organization. The reporting window
must be between 1 and 365 days.

## Launchpad

```bash
ac launchpad signal-preferences get
ac launchpad signal-preferences set --sort-mode recent --score-threshold 5 --score-direction above
ac launchpad signal-preferences set --group
ac launchpad signal-preferences set --clear-threshold
```

Lead scores use a 0-10 scale. `set` preserves unspecified preferences; use
`--clear-threshold` to remove the score filter.

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
ac styles create --name "Professional" [--prompt "..."] [--sample-email "..."] [--default]
ac styles update <style-id> [--name "Updated"] [--prompt "..."] [--default|--no-default] [--active|--inactive]
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

## Agentic Conversations

```bash
ac agentic conversations list [--cursor <cursor>] [--limit 50]
ac agentic conversations create [--title "Project Discussion"]
ac agentic conversations messages <conversation-id> [--cursor <cursor>] [--limit 50]
ac agentic conversations send <conversation-id> "What's on my plate today?" \
  [--idempotency-key <key>]
```

The CLI sends one message and returns immediately. Read the answer with
`ac agentic conversations messages`; the browser owns the live event stream.
`send` takes the message text as a positional argument. There is no `--message`
flag and no single-conversation `get` command.

## Resources (Knowledge Base)

```bash
ac resources list [--limit 50] [--offset 0]
ac resources upload <file-path> --name "Source Name" [--description "..."] [--tags "tag1,tag2"]
ac resources delete <resource-id> [--yes]
ac resources status <resource-id>
```

Formats: .pdf, .txt, .md, .docx (max 10 MB). `--name` is required.

## Notifications

```bash
ac notifications list [--unread-only] [--limit 50] [--offset 0]
ac notifications unread-count
ac notifications read <notification-id>
ac notifications read-all
ac notifications preferences                       # List type/channel preferences
ac notifications set-preference --type mention --channel email --enabled
ac notifications set-preference --type mention --channel in_app --disabled
```

Channel enum: `in_app`, `email`.

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
