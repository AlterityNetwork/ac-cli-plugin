# Platform Quick Reference

For full flag tables see `commands.md` (Platform section).

## Agentic Saved Searches

```bash
ac agentic saved-searches create --capability signals.search --name "UK fintech" --brief '{"icp":"UK fintech firms","persona":{"titles":["CTO"],"country_codes":["GB"]}}'
ac agentic saved-searches create --capability people.signals --name "New marketing leaders" --brief '{"signal_recency":"1m","brief":{"icp":"New marketing leaders"}}'
ac agentic saved-searches create --capability company.search --name "UK mid-market" --brief '{"sources":["provider_discovery"],"filters":{"country_codes":["GB"]}}'
ac agentic saved-searches create --capability signals.search --name "Watched accounts" --brief '{"icp":"Any recent sales signal at the company"}' --watch-list-id <crm-list-id>
ac agentic saved-searches list --capability signals.search [--cursor <cursor>] [--limit 50]
ac agentic saved-searches list --capability signals.search --capability people.signals
ac agentic saved-searches get <saved-search-id>
ac agentic saved-searches patch <saved-search-id> --expected-updated-at <token> [--name "New name"] [--brief '{...}'] [--watch-list-id <crm-list-id> | --clear-watch-list-id]
ac agentic saved-searches delete <saved-search-id> [--yes]
ac agentic saved-searches start <saved-search-id> --idempotency-key <key>
ac agentic saved-searches diff <saved-search-id> [--cursor <cursor>] [--limit 50]
ac agentic saved-searches schedule get <saved-search-id>
ac agentic saved-searches schedule set <saved-search-id> --cron "0 9 * * 1" [--timezone Europe/London]
ac agentic saved-searches schedule clear <saved-search-id> [--yes]
```

The brief must be a JSON object in the selected capability's input shape.
For `people.signals`, save the complete input with a nested `brief.icp` and
optional `signal_recency` (`"1w"`, `"1m"`, `"3m"`, `"6m"`, `"12m"`, or `"24m"`),
`brief.persona`, `brief.persona_description`, and `brief.employer_criteria`.
For a known people list, include `"source":"people_set"` and 1–10 `people`
references. For `signals.search`, the
saved brief must contain a non-empty `icp` string or a non-empty
`company_criteria` array. It also requires a `persona` object.
Use `titles`, `departments`, `seniority` and `country_codes` lists. Supply at least one list.
Each list contains 1 to 20 unique values. Omit unused lists; do not send null or empty lists.
Text values contain 1 to 1,000 characters. Country codes use uppercase ISO alpha-2 values.
Values use OR within each list and AND between fields. The complete execution input must also fit the byte limits.
Do not infer a country from free-text location or convert a title family into exact titles.
`list` omits the brief. Use `get` when you
need the full brief or the current `updated_at` write token.

`schedule set` starts a Signals saved search on a five-field cron, read in the
IANA zone you give (default `UTC`). Only a `signals.search` saved search takes a
schedule. Any member who can start Signals may set one, and becomes its author.
A search keeps one schedule, so `set` replaces the one it has. `list` shows each
schedule. Deleting a saved search also stops its schedule.

`patch` requires that token and at least one replacement field. A stale token
returns exit code 5. `start` freezes the stored brief and current baseline in a
normal Run. Reuse its key only for the same saved search.
It does not create a schedule. `diff` reads only the latest
published successful Run. Start a new page walk if the published Run changes.
Deleting a saved search does not cancel a Run that already started.

To correct a legacy persona, first use `get --json` and preserve the original brief.
Obtain explicit criteria for ambiguous legacy values. Replace only `brief.persona` in a copy of the full brief.
Send that full copy with `patch --brief` and the current `--expected-updated-at` token.
Keep unrelated brief fields. If the token changes, read the search again before correcting it.
An incompatible search remains readable and permits a name-only edit, but cannot start until corrected.
Read the returned field errors with `--json`. Do not recreate the search or change its ID, watches or schedule.

## Agentic Prospect Review

```bash
ac agentic prospects list [--review-state <state>] [--last-seen-run-id <run>] [--id <prospect> ...] [--people-state <state>] [--signal-type <type>] [--search <text>] [--saved-search-id <id>] [--min-score <0-100>] [--max-score <0-100>] [--sort <order>] [--cursor <cursor>] [--limit 50]
ac agentic prospects act <prospect-id>
ac agentic prospects counts
ac agentic prospects signal-types [--review-state new]
ac agentic prospects get <prospect-id>
ac agentic prospects people <prospect-id> [--cursor <cursor>] [--limit 50]
ac agentic prospects signals <prospect-id> [--cursor <cursor>] [--limit 50]
ac agentic prospects add-person <prospect-id> --name <name> [--linkedin-url <url>] [--title <title>] [--email <email>]
ac agentic prospects search-persona <prospect-id>
ac agentic prospects find-people <prospect-id> [--title <title>]... [--department <department>]... [--seniority <level>]... [--country <code>]...
ac agentic prospects find-people <prospect-id> --describe "<the people to find>"
ac agentic prospects watch <prospect-id>
ac agentic prospects dismiss <prospect-id>
ac agentic prospects restore <prospect-id>
ac agentic prospects dismiss-action <prospect-id>
ac agentic prospects promote <prospect-id> [--person <id>]... [--signal <signal-id>]... [--list <list-id>] [--yes]
ac agentic prospects delete <prospect-id> [--yes]
```

Use `--json` when a later command needs an ID or the full nested company,
person, or signal data. `watch` and `dismiss` are repeatable intents. Neither
can change a promoted prospect.

`--sort` takes `score`, `signal_strength` or `discovered`. The default is
`discovered`, the date this organization first saw the company. `score` reads
`opportunity_score` and `signal_strength` reads the score of the most recently
attached signal. Both put an ungraded prospect last. A cursor belongs to one
sort, so keep `--sort` on every page of a walk. A cursor another sort wrote
is refused with a 400, which is exit code 1.

`--people-state`, `--signal-type`, `--search`, `--saved-search-id`,
`--min-score` and `--max-score` filter on the server. A signal type matches
any attached signal, and `signal-types` lists the types one review state
holds, with a count each. This includes current intel types and older stored
types such as `tech_stack` and `agency_review`. Use those names: another name
is refused with a 422. `--min-score` and `--max-score` read `opportunity_score`, 0 to 100, and a
prospect with no score drops out when either bound is set.

`dismiss-action` closes the suggested action card and stamps
`suggested_action_dismissed_at`. It changes no review state, and a repeat call
keeps the first stamp.

`add-person` and `find-people` give a company prospect more people. Neither
works on a person prospect or a promoted prospect: both return exit code 5.
`add-person` attaches one person you name. Only the name is required. The
title and the email stay on the prospect, and each fills only a value the
LinkedIn profile does not have. With no profile, the person stays on the
prospect.
`find-people` starts one `people.search` Run for the company. With no option
it looks for the decision makers that `search-persona` shows. The `--title`,
`--department`, `--seniority` and `--country` options replace that persona.
`--describe` takes free text instead, and the Run plans the lists from it.
Use it when the request names people in words rather than exact fields.
The people attach to the prospect when the Run ends. Read them with
`people`. While the Run is live, `get` shows `people_search_run_id` and a
second `find-people` returns exit code 5.

`restore` undoes `watch` and `dismiss`: it returns the prospect to `new`. A
prospect already at `new` writes nothing, and a promoted prospect is refused.

`delete` removes the prospect with its people and its signals, and asks first
unless `--yes` is set. It keeps no record of the company, so a later run that
finds the company writes a new prospect. Use `dismiss` to keep a company out.

`counts` reads how many prospects each review state holds. Every state carries
a number, and a state with no prospect reads 0.

`get` prints a Company block for a company prospect and a Person block for a
person prospect, which a `people.signals` Run writes. The person is the subject:
a creator or a public figure with no company target. `list` shows the subject
kind in `Subject` and the person's name in `Person`.

`promote` is the one command that writes CRM. For a company prospect it
resolves or creates the CRM company and each selected person, then sets the
prospect to `promoted`. Repeat `--person` for each prospect person id, taken
from `ac agentic prospects people`. For a person prospect, with no `--person`
it promotes the subject person alone, and `--list` adds the person to a person
list. When the person is linked to an employer, the promotion resolves or
creates the CRM company of that employer, links the CRM person to it, and
answers it as `crm_company_id`. A CRM person that already holds a company link
keeps it. An employer the CRM cannot resolve to one company links no company,
and `crm_company_id` is null. `get` and `people` print the linked employer as
`Company`, and fall back to the employer text. The CRM holds a person by an
email or a LinkedIn URL; a person with neither is refused before any write,
and the refusal names the missing identifier. It asks before it writes; pass
`--yes` to skip the question. A second promotion writes nothing and answers the
same references.

A promotion also sets the `lifecycle_stage` of the company and of each promoted
person to `prospect`. It moves a row at the `identified` stage, and a person
that holds no stage. A qualified lead or a customer keeps the stage it holds.
A company always holds a stage, so only a person can hold none.

## Agentic Outreach Campaigns

```bash
ac agentic outreach campaigns list [--status draft|active|paused|archived] [--limit 50] [--offset 0]
ac agentic outreach campaigns get <campaign-id>
ac agentic outreach campaigns create --name "Q4 intro" [--description "Heads of growth at Series A SaaS companies"]
ac agentic outreach campaigns update <campaign-id> [--name "..."] [--description "..."]
ac agentic outreach campaigns activate|pause|resume <campaign-id>
ac agentic outreach campaigns archive <campaign-id> [--yes]
ac agentic outreach campaigns enroll <campaign-id> --person-kind crm.person|prospect.person --person-id <id>
ac agentic outreach enrollments list --campaign-id <campaign-id> [--state active|awaiting_approval|needs_contact_data|ended] [--search "jane"] [--limit 100] [--offset 0]
ac agentic outreach enrollments get <enrollment-id>
ac agentic outreach enrollments timeline <enrollment-id> [--limit 50] [--order desc|asc]
ac agentic outreach enrollments evaluate <enrollment-id> [--request-id <id>]
ac agentic outreach enrollments exit <enrollment-id> [--yes]
ac agentic outreach organization status|resume
ac agentic outreach organization stop [--yes]
```

These commands run the agentic Outreach campaigns. They are not the legacy
`ac envoy campaigns` or `ac envoy sequences`.

A new campaign is a `draft`, and the caller owns it: the owner's mailbox sends
its emails. A campaign has a name and an optional description, nothing more.
The campaign has no fixed goal and no email limits. For each Run, the planner
selects the next step from the latest context of the person. The description
is context for the planner, not an instruction. The planner prompt holds the
email cadence: with no reply, at most 4 emails, with gaps of about 3, then 5,
then 7 days. `activate` and `resume` both set the campaign `active`; `pause`
sets it `paused`. While a campaign is paused, no new Run starts and no email is
sent. A Run that started before the pause still finishes its decision, and its
send is refused. `archive` is final and asks first. It ends every live
enrollment in the background, so for a few seconds a person can still read as
live.

`enroll` adds one person and starts the first Run. A person can be live in
one campaign only. Enrolling a person who is live in another campaign returns
exit code 5 (`already_enrolled`), and the message names that campaign. A
campaign holds at most 200 live enrollments (`campaign_full`). A prospect
person that is already in the CRM enrolls as the CRM person.

`campaigns list` and `campaigns get` show the live enrollments against the cap
(`People 140/200`) and the count per state: active, awaiting a draft review,
needing an email, and ended.

`enrollments list` shows one page of a campaign, newest first. Each row names
the person, the email of the person row, the state and the last decision
(action and outcome). `--search` keeps the people whose name holds the text,
in any case. The title shows the rows and the total, for example `2-2 of 3`.
When more rows wait, the command prints the `--offset` of the next page.

`enrollments timeline` lists what happened to one enrollment: the start, each
decision with its outcome and reviewer note, the thread emails (a reply shows
as an `inbound` email), the CRM activities, and the end. It is newest first by
default, the left column of the review card. `--order asc` lists it oldest
first, as the enrollment drawer shows it.

`enrollments evaluate` asks for a Run now. Use it to re-evaluate, to retry an
enrollment in `needs_contact_data`, and after you add an email to the CRM
person, because a CRM edit starts no Run. It returns exit code 5 when the
enrollment waits for a draft review (`awaiting_approval`), a Run decides now
(`run_in_progress`), the campaign is not active, the organization stopped, or
the enrollment ended. `enrollments exit` ends the enrollment as `manual`,
records the caller in `ended_by` and rejects a draft that waits for review.

`organization stop` stops Outreach for every campaign of the organization,
and `resume` clears it. Only an organization admin may run them; another
member gets exit code 4.

## Agentic Outreach Drafts

```bash
ac agentic outreach drafts list [--campaign-id <campaign-id>] [--limit 50] [--offset 0]
ac agentic outreach drafts get <draft-id>
ac agentic outreach drafts save <draft-id> [--subject "New subject"] [--body "Text" | --body-file body.txt]
ac agentic outreach drafts approve <draft-id> --version <n> --content-hash <hash>
ac agentic outreach drafts reject <draft-id> --mode regenerate|skip|exit [--note "Feedback"] [--yes]
```

These commands review the emails that an agentic Outreach campaign drafted.
They are not the legacy `ac envoy outbox` drafts. The draft ID is the decision
ID that `list` prints.

`list` prints one page: each draft names the person, the campaign and when its
approval expires. The title shows the rows against the total, and a last line
prints the next `--offset` while more drafts wait. Only the table output has
that line: with `--json`, compute the next offset as `offset + length(data)`
while `has_more` is true.

`get` prints the draft text, the enrollment `version` and the `content_hash`.
`approve` must send both values back. Save your edits first, then approve with
the `version` and `content_hash` that `save` or a new `get` printed. The Run
then sends that exact text once. A save after the approval returns exit code 5.

`approve` returns exit code 5 with a `code` in `--json` output when the
version or the text changed (`version_changed`, `content_changed`), another
person approved first (`already_approved`), the campaign is not active
(`campaign_not_active`), the organization stopped Outreach
(`organization_stopped`), or the Run does not wait yet (`approval_not_ready`;
retry in a few seconds). Read the draft again before you retry.

`reject --mode regenerate` plans a new email at once. `--mode skip` sends
nothing and looks again later. `--mode exit` ends the person's enrollment and
asks first; pass `--yes` to skip the question. `--note` is feedback that later
Runs read. Do not approve an Outreach email with `ac agentic approvals`; that
inbox refuses it with exit code 5.

## Organization Analytics

```bash
ac analytics overview [--period-days 30] [--json]
```

Shows cross-product output for the active organization. The reporting window
must be between 1 and 365 days.

## Settings

The copilot approval framework and Memory of the active organization.

```bash
ac settings framework get
ac settings framework get --json
ac settings framework set --content-file ./framework.md
ac settings framework publish
ac settings framework publish --content-file ./framework.md
```

`set` saves the draft and leaves the published copy. `publish` without content
publishes the stored draft. Run `ac whoami` first: the commands act on the
selected organization.

Memory is what the apps know about the organization and about you. The company
part holds the Company profile, the services, the ideal customer profiles, the
offers, and the title and summary of each active document. The personal part
holds your profile, email signature and default writing style.

```bash
ac settings dossier get                  # Markdown to stdout, empty fields to stderr
ac settings dossier get --user           # add your profile, signature and writing style
ac settings dossier get --json           # the full record, with gaps and totals
ac settings dossier get > ./dossier.md
ac settings dossier pdf --user -o ./memory.pdf   # Memory as a PDF file
```

Memory lines are your own standing instructions for the apps, for example
"Sign off as Marc". Each line belongs to you in the active organization. No
other user reads or changes it. The email writer reads the `all` and `email`
lines. The chat reads the `all` lines. One user keeps at most 50 lines; a
51st `add` gets exit code 1 (HTTP 400).

```bash
ac settings memory list                                       # table, oldest first
ac settings memory list --json                                # {data, total, max_lines}
ac settings memory add --text "Sign off as Marc"              # --applies-to defaults to all
ac settings memory add --text "Use UK spelling" --applies-to email
ac settings memory edit <line-id> --text "Sign off as Marc C" # --text, --applies-to or both
ac settings memory remove <line-id> --yes
```

Memory suggestions are lines that the app learns from your edits to email
drafts. A suggestion shows how many emails and how many people the edit came
from. Accept one to add it as an `email` memory line; the 50-line cap applies,
so an accept at the cap gets exit code 1 (HTTP 400). A dismissed suggestion
does not come back. A suggestion that is no longer proposed gets exit code 5
(HTTP 409).

```bash
ac settings memory suggestions list                       # id, text, "N emails / M people"
ac settings memory suggestions list --json                # {data, total}; each has examples [{before, after}]
ac settings memory suggestions refresh                    # "Read N emails. M new suggestions."
ac settings memory suggestions accept <id>                # keep the suggested text
ac settings memory suggestions accept <id> --text "Sign off as Marc"
ac settings memory suggestions dismiss <id> --yes
```

## Launchpad

```bash
ac launchpad signal-preferences get
ac launchpad signal-preferences set --sort-mode recent --score-threshold 5 --score-direction above
ac launchpad signal-preferences set --group
ac launchpad signal-preferences set --clear-threshold
```

The threshold reads the 0-10 prospect score the launchpad rows show.
`set` preserves unspecified preferences; use `--clear-threshold` to remove
the score filter.

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
ac agentic conversations list [--cursor <cursor>] [--limit 50] \
  [--draft-capability <capability-id>]
ac agentic conversations create [--title "Project Discussion"] \
  [--draft-capability <capability-id>]...
ac agentic conversations messages <conversation-id> [--cursor <cursor>] [--limit 50]
ac agentic conversations send <conversation-id> "What's on my plate today?" \
  [--entity-ref <kind>:<id>] [--idempotency-key <key>] [--draft '<json>']
```

The CLI sends one message and returns immediately. Read the answer with
`ac agentic conversations messages`; the browser owns the live event stream.
`send` takes the message text as a positional argument. There is no `--message`
flag and no single-conversation `get` command.

`--entity-ref` names a row the message is about, as `kind:id`. Repeat it for
each row. Each one enters the conversation entity scope before the turn runs,
so the turn resolves "this company" and a capability input can carry the id.
The scope survives the turn, so a later message needs no ref for the same row.

```bash
ac agentic conversations send <conversation-id> "Enrich this company." \
  --entity-ref crm.company:2f57d848-34df-4593-b144-c8815027db87
```

Name one row when you mean one row. Two rows of one kind make "this company"
ambiguous, and the platform asks which one instead of guessing.

### Draft conversations

A draft conversation writes a search for a form and starts no run. The Signals
search page opens one for `signals.search` and `people.signals`, the only two
capabilities a draft takes. `list` without `--draft-capability` reads ordinary
chats only, so a draft conversation never appears in the chat list.

```bash
ac agentic conversations create --title Signals \
  --draft-capability signals.search --draft-capability people.signals
ac agentic conversations send <conversation-id> "UK fintechs that raised a Series B" \
  --draft '{"capability_id": "signals.search", "input": {"source": "discovery"}}'
ac agentic conversations messages <conversation-id> --json
```

`--draft` is the form state at send time, and it may be incomplete. The reply
carries the drafted search in `draft`: a `capability_id` and the product
`input`. Start it with `ac agentic capabilities start`. The draft keeps the
companies and people the form already lists, and the chat never adds a row.

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
ac profiles usage                                 # Period usage per action (calls, tokens)
```

> **"Switch active organization" → `ac profiles set-organization <org-id>`**, NOT `ac env use` (env is local/staging/production) and NOT `ac admin orgs` (which manages org records, not user's active org).


### Targeting settings

Owners, admins and assigned copilots can replace the active organization's ICPs:

```bash
ac settings targeting set --profiles-file ./icps.json --json
```

The file is a JSON array of profiles with `id`, `name`, `description` and
`country_codes` (ISO-2 codes). Keep existing IDs when editing profiles so offers
retain their selections. Omit `id` only for a new profile. An empty array clears
all profiles. This command does not grant access to general organization settings.
