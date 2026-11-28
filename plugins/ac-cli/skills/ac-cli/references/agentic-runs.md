# Agentic Definitions and Runs

These commands require the CLI and API from `agentic-platform` until cutover.

## Start a definition by key

Use a definition key: `company.search`, `company.enrich`, `people.search`,
`people.enrich`, `people.signals` or `signals.search`. The definition must be installed and active
for the current organization. `ac agentic definitions startable` lists the keys you can start;
`ac agentic definitions startable-show <key> --json` reads one input schema.

```bash
ac agentic runs start --key company.search \
  --input '{"natural_language_query":"UK fintech companies"}' \
  --idempotency-key company-search-request-42 --json
```

`--input` is a JSON object. `--idempotency-key` is optional: the CLI mints a fresh one when it is
absent. Pass one only when a retry must not start a second Run (1–255 header-safe ASCII characters).

### Company Enrich (contract version 2)

`company.enrich` takes one field, `subjects`, a list of 1 to 100 company
references. The input is closed: `preset`, `fields` and `refresh` are refused.

```bash
ac agentic runs start --key company.enrich \
  --input '{"subjects":[{"kind":"domain","value":"acme.com"},{"kind":"name","value":"Globex"}]}' \
  --idempotency-key company-enrich-request-42 --json
```

A reference is one of `{"kind":"domain","value":"acme.com"}`,
`{"kind":"company_linkedin","value":"<company URL>"}`, `{"kind":"name","value":"Acme GmbH"}`,
`{"kind":"intel_company","id":"<uuid>"}` or
`{"kind":"search_result","run_id":"<uuid>","result_id":"<uuid>"}`. Only Company
Enrich accepts a `name` reference.

The result is under `result.company_enrich`. It holds `items`, one per input
position in input order, then `outcome` (`complete`, `partial` or `empty`),
`diagnostics` and `usage` (`cost_cents`, `cost_kind`, `provider_calls`). Each item has:

- `input_index` and `ref`: the position and the reference as sent.
- `status`: `enriched`, `not_found` (the Run tried the row and saved nothing) or
  `failed` (the Run stopped before it tried the row).
- `match`: `name`, `domain`, `linkedin_url` and `how` (`domain`, `linkedin`, `name`
  or `agent`). All four are null unless the status is `enriched`.
- `values`: only the fields the source stated, from `name`, `website`, `linkedin_url`,
  `industry`, `sub_industry`, `country_code`, `location`, `description`, `founding_year`,
  `employee_count_exact`, `employee_count_band`, `logo_url`, `annual_revenue`,
  `revenue_band`, `revenue_currency`, `funding_round`, `funding_amount` and
  `funding_currency`. A missing key means the source did not state it.

`outcome` is `partial` when any row is `failed`, else `empty` when nothing is enriched,
else `complete`.

A name that matches more than one company returns the best match with
`match.how` set to `agent`. The result lists no candidates.

A `signals.search` bounded set (`"source":"company_set"`) names companies, people
or both. A company reference carries one of `intel_company_id`, `prospect_id`,
`domain` or `linkedin_url`, with an optional `name`, or a `name` alone that the
Run researches. A person carries `linkedin_url`, or `full_name` with `email`,
`domain` or `company_name`, plus an optional `title`. The Run seeds each
person's company from the domain, the work email host or the company name, and
the result carries `skipped_companies`, `skipped_people` and one
`supplied_people` outcome per person (`signal_recorded`, `no_signal`,
`no_profile` or `employer_mismatch`).

```bash
ac agentic runs start --key signals.search \
  --input '{"source":"company_set","brief":{"icp":"Leadership changes"},"people":[{"full_name":"Ada Lovelace","email":"ada@acme.com","title":"CTO"}]}' \
  --idempotency-key signals-people-42 --json
```

For a person event, start `people.signals`. Discovery is the default. To
research a known people list, use `"source":"people_set"` with 1–10 people;
the Run excludes people outside that list. `brief.employer_criteria` optionally
describes the person's current employer, `brief.persona` refines the person's
role and location, and `brief.persona_description` describes the people.
Optional `signal_recency` accepts `"1w"`, `"1m"`,
`"3m"`, `"6m"`, `"12m"`, or `"24m"` (default `"3m"`). The person with the
signal is the resulting contact.

```bash
ac agentic runs start --key people.signals \
  --input '{"source":"people_set","people":[{"full_name":"Ada Lovelace","email":"ada@example.com"}],"brief":{"icp":"Started a marketing leadership role","employer_criteria":"B2B SaaS companies"},"signal_recency":"1m"}' \
  --idempotency-key people-signals-42 --json
```

Input is limited to 32 KiB. The server applies the published schema and preserves
omitted fields; it does not insert schema defaults.

`--title` names the search, up to 200 characters. `--saved-search-id` names the
saved search the request came from: the Run then lists under that saved search,
and a list or a detail names it. The link is for display only. The saved search
keeps its last Run and its diff. A link to a saved search that no longer exists
is dropped, and a link to a saved search of another key returns 422.
Neither flag is part of the request identity.

```bash
ac agentic runs start --key signals.search \
  --input '{"source":"discovery","brief":{"icp":"Raised a seed round"}}' \
  --title "Joyvie lookalikes" --saved-search-id <saved-search-id> \
  --idempotency-key signals-named-42 --json
```

Reuse the same key and request after a timeout. A matching replay returns the
original Run, even after a binding change. A changed key or input
with that key returns `idempotency_conflict` (409). Use a new key for a new request.
Keys are isolated by organization, caller and start source.

The response is the existing Run detail. Read `status` as well as `outcome`:
`started` can mean queued, waiting for approval, or failed on policy admission.
A duplicate does not start another execution. Read the Run with the commands below.

Errors preserve the API code in JSON output: unknown ID (404), unavailable binding
(409), missing scope (403), invalid input (422), oversized input
(413), and invalid key (400). The CLI uses its existing semantic exit codes.

A spent limit refuses the start with a `detail` object `{code, message, remedy}`.
`ac agentic runs start --key` and `ac agentic runs start --definition` answer the same two:

| Code | Status | Exit | What to do |
|------|--------|------|------------|
| `day_cap_exhausted` | 429, with `Retry-After` | 1 | Try again after midnight UTC, or ask an owner or admin to raise the daily cap |
| `credits_exhausted` | 402 | 6 | Ask an owner or admin to add credits, or wait for the next billing period. `ac profiles usage` shows the balance |

Text mode prints `Error {status}: {message} {remedy} ({code})`. `--json` keeps the
`detail` object. A Run that is already in flight is not refused at the start: it
ends `partial` at its next checkpoint, with `partial_reason` `budget_exhausted`.

## Estimate the credits of a run

A `signals.search` run pays one price for each company or person it checks,
and one price for a discovery run. Tokens and enrichment inside the run are
free. The prices can change, so read them from the estimate
(`credits_per_unit`, `credits_per_run`), not from this page:

```bash
ac agentic definitions startable-estimate signals.search --units 48 --json
ac agentic definitions startable-estimate signals.search --input '{"source":"discovery","brief":{"icp":"Raised a seed round"}}'
ac agentic definitions startable-estimate signals.search --saved-search-id <saved-search-id> \
  --cron "0 9 * * 1" --timezone Europe/London
```

Name one of `--units`, `--input` or `--saved-search-id`. A saved search is
priced with the members its list holds now. `--cron` adds the runs and the
credits of 30 days on that schedule.

`credits_per_run` is the most the run charges. The start uses the same number,
so a start that the credits left do not cover returns `credits_exhausted`
(402). `units_covered` is how many companies the credits left pay for, when
the organisation has a credit limit. A definition without a price per unit
answers `"priced": false`.

## Start a run

The command starts one Run of one definition. The definition is an agent or a
workflow. Read the IDs with `ac agentic definitions list`, or start by key as above.

```bash
ac agentic runs start --definition <definition-id> \
  --input '{"query":"series B fintech"}' --json
```

Name exactly one of `--definition` and `--key`. An absent or empty `--input` sends an empty
object. Any other value must be a JSON object of at most 32 KiB.

The CLI mints a fresh key for each start when `--idempotency-key` is absent, so
two identical commands start two Runs. Pass a key only when a retry must not
start a second Run, and use 1–255 header-safe ASCII characters. The CLI refuses
an empty flag before it calls the API. A repeat with the same key returns the
first Run and starts no second execution; human output marks it `Duplicate`.

The definition must be published, and it must be an agent or a workflow.
`ac agentic definitions list` also returns drafts, disabled definitions and
skills. Each of those returns 409. An archived definition is hidden from the
list unless you pass `--include-archived`; `ac agentic definitions archive <id>`
hides one and disables it, and `ac agentic definitions unarchive <id>` brings it
back, still disabled. `ac agentic runs start --key` above starts
a startable definition by its key and selects the active contract automatically.

## Read Runs

```bash
ac agentic runs list --json
ac agentic runs get <run-id>
ac agentic runs get <run-id> --json
ac agentic runs list --parent <run-id> --json
ac agentic runs list --key signals.search --source trigger --json
ac agentic runs list --saved-search-id <saved-search-id> --json
ac agentic runs list --key signals.search --key people.signals --json
ac agentic runs list --key company.search --status succeeded --include-result --json
ac agentic runs spans <run-id> --scope tree --json
ac agentic runs span-detail <owning-run-id> <span-id> --json
```

`--include-result` puts the frozen `result` of each Run on its row, so one
list request answers the results of many Runs. Without it, `result` is null.

`--key` repeats. The Signals history lists the `signals.search` and
the `people.signals` Runs in one page, and the title of each.

`--source` lists the Runs one entry point started: `front_door`, `trigger`,
`api` or `workflow_step`. A schedule starts `trigger` Runs.

Each Run carries a `title`: the name a person gave the Run (`custom_title`).
On a list that names `signals.search`, `people.signals`, or both, a Run with no
name takes the name of its saved search, else the first sales-signal
criterion, the ICP, or the target-company text. Every other Run with no name
answers `title: null`. `saved_search_id` is null for a manual
search. `saved_search_name` is null for a manual search and for a saved search
that was deleted.

Rename a Run with `ac agentic runs rename <run-id> --title "New name"`, or
remove the name with `--clear`. A rename does not rename the saved search.

`--saved-search-id` lists the Runs one saved search started, from Run now, from
its schedule, or from the form after Load search, for every key. Runs a saved search started before the
filter existed list only for Signals, because only a Signals Run input named
its saved search.

Run start, list and detail JSON include `definition_key` and `contract_version`.
The values come from the published executor binding at admission. A later
rename or binding change does not change a Run. Both fields are null on old
Runs and custom executors. Null does not mean contract version zero.

`get` shows both fields in human output. Tree usage is the whole Run tree;
do not add parent and child usage totals. Key cost metrics use separate
usage deltas and can be incomplete. Use durable usage records for billing.

`list` returns one page. Use `next_cursor` with `--cursor` to read the next
page. The default lists root Runs. Use `--all` to include child Runs.
To read another page, pass `next_cursor` to `--cursor` even when you use `--all`.

The spans list omits tool arguments and results. `span-detail` reads the bounded,
redacted input and output for one span. Use the span's `run_id` from the tree
response as `<owning-run-id>`; a span from another run returns 404.

When `list` is filtered with `--key company.search`, `people.search` or
`signals.search`, its rows include `search_query`, normalized from the
definition's input contract. The human table shows it in the
`Definition / Search` column. It is null for unfiltered lists, non-search Runs
and older Runs whose input did not retain the submitted query.

`ac agentic prospects find-people <prospect-id>` starts one `people.search` Run
for the company of a prospect. The prospect holds the link in
`people_search_run_id` while the Run is live. When the Run ends, the platform
attaches the people it found to the prospect and clears the link. Read the Run
with `ac agentic runs get <run-id>`, and the people with
`ac agentic prospects people <prospect-id>`.

`list` JSON and the human `Results` column carry `result_count`: the number of
results the run page lists. The API counts it on any list, for a succeeded
`signals.search`, `people.signals`, `company.search` or `people.search` Run. A
Company Search or People Search Run counts the items of its result. A Signals
or People Signals Run counts the prospects its result names that still exist
and are not dismissed, so the count falls when a person dismisses or deletes
one. Every other Run carries null.
Zero is a search that found nothing, so do not read null as zero. Run detail
always carries null. `prospect_count` is always null and will go away.


### Product progress

`ac agentic runs progress <run-id> --json` reads a bounded summary of observed
product milestones across a root run and its child agents. It supports Signals,
Company and People Search. Pass a root run ID; a child ID returns 422.

The response contains `run_id`, `status` and `stages`. Each stage has a stable
`id`, readable `name` and `description`, `status`, `started_at`, `updated_at`
and `incomplete`. An incomplete stage does not establish completion. An empty
stage list does not mean the run has stopped; read the run status.

The progress response includes up to six agent and tool activity entries per active stage. Each entry has a name, kind and status. `activity_incomplete` marks a limited view; tool arguments and outputs are omitted.

## People profile and affiliations

`ac agentic people profile` reads what the global people cache holds for one
person. The read is free and starts no Run.

```bash
ac agentic people profile --linkedin-url https://www.linkedin.com/in/<handle> --json
```

The response carries `linkedin_url`, `experience_history`, `affiliations` and
`affiliations_checked_at`. A key inside an entry is absent when its value is null.

- `experience_history` holds up to 50 entries, current first. Each entry has
  `title`, `company`, `location`, `start_date`, `end_date` and `kind`.
- `affiliations` holds up to 20 roles outside the main job: boards, advisory
  roles, trusteeships, investments, founded projects, fellowships, books,
  podcasts, columns and talks. Each entry has `kind`, `name`, `role`,
  `current`, `source_url` and optional `start_date` and `end_date`.
- `kind` is one of `employment`, `board`, `advisory`, `trustee`, `investor`,
  `founder`, `fellowship`, `author`, `podcast`, `column`, `speaking`, `other`.
- `affiliations_checked_at` is the time of the last deep dive. Null means no
  deep dive ran. An empty `affiliations` list with a time means the deep dive
  found nothing.

A URL with no cache row returns 404 (exit 3). A URL that is not a LinkedIn
profile URL returns 422 (exit 2). A plan without the People apps returns 402
(exit 6). Each user can read 60 profiles a minute and 1,000 a day; a read over
either budget returns 429 (exit 1). A person reaches the cache through People
Search or People Enrich.

### Run a deep dive for one person

`affiliations` is a People Enrich field that a caller must name. The `standard`
preset is required, and a bare preset request never fills it. The deep dive
costs one `people` entity credit when it finds at least one affiliation, and
nothing when it finds none. A second start inside 90 days reuses the stored
answer.

```bash
ac agentic runs start --key people.enrich \
  --input '{"subjects":[{"kind":"person_linkedin","value":"https://www.linkedin.com/in/<handle>"}],"preset":"standard","fields":["full_name","current_company_text","affiliations"],"refresh":"stale"}' \
  --idempotency-key affiliations-<handle>-1 --json
```

When the Run ends, read the result with `ac agentic people profile`. When the
deep dive cannot run, for example because the Run knows no usable name, the
`affiliations` field state is `failed` and nothing is stored.
