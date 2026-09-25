# Agentic Capabilities and Runs

These commands require the CLI and API from `agentic-platform` until cutover.

## Start a capability

Use a stable product ID: `company.search`, `company.enrich`, `people.search`,
`people.enrich`, `people.signals` or `signals.search`. The capability must be installed and active
for the current organization. Its published schema defines the input fields.

```bash
ac agentic capabilities start company.search \
  --input '{"sources":["supplied"],"companies":[{"kind":"domain","value":"example.com"}]}' \
  --idempotency-key company-search-request-42 --json
```

Both flags are required. Use a JSON input object and a nonblank delivery key
with 1–255 header-safe ASCII characters.

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
ac agentic capabilities start signals.search \
  --input '{"source":"company_set","brief":{"icp":"Leadership changes"},"people":[{"full_name":"Ada Lovelace","email":"ada@acme.com","title":"CTO"}]}' \
  --idempotency-key signals-people-42 --json
```

Input is limited to 32 KiB. The server applies the published schema and preserves
omitted fields; it does not insert schema defaults.

Reuse the same key and request after a timeout. A matching replay returns the
original Run, even after a binding change. A changed capability or input
with that key returns `idempotency_conflict` (409). Use a new key for a new request.
Keys are isolated by organization, caller and start source.

The response is the existing Run detail. Read `status` as well as `outcome`:
`started` can mean queued, waiting for approval, or failed on policy admission.
A duplicate does not start another execution. Read the Run with the commands below.

Errors preserve the API code in JSON output: unknown ID (404), unavailable binding
(409), missing scope (403), invalid input (422), oversized input
(413), and invalid key (400). The CLI uses its existing semantic exit codes.

## Start a run

The command starts one Run of one definition. The definition is an agent or a
workflow. Read the IDs with `ac agentic definitions list`.

```bash
ac agentic runs start --definition <definition-id> \
  --input '{"query":"series B fintech"}' --json
```

Only `--definition` is required. An absent or empty `--input` sends an empty
object. Any other value must be a JSON object of at most 32 KiB.

The CLI mints a fresh key for each start when `--idempotency-key` is absent, so
two identical commands start two Runs. Pass a key only when a retry must not
start a second Run, and use 1–255 header-safe ASCII characters. The CLI refuses
an empty flag before it calls the API. A repeat with the same key returns the
first Run and starts no second execution; human output marks it `Duplicate`.

The definition must be published, and it must be an agent or a workflow.
`ac agentic definitions list` also returns drafts, disabled definitions and
skills. Each of those returns 409. `ac agentic capabilities start` above starts
a published product capability and selects the active contract automatically.

## Read Runs

```bash
ac agentic runs list --json
ac agentic runs get <run-id>
ac agentic runs get <run-id> --json
ac agentic runs list --parent <run-id> --json
ac agentic runs list --capability signals.search --source trigger --json
ac agentic runs list --capability signals.search --capability people.signals --json
ac agentic runs spans <run-id> --scope tree --json
ac agentic runs span-detail <owning-run-id> <span-id> --json
```

`--capability` repeats. The Sonar history lists the `signals.search` and
the `people.signals` Runs in one page, and the title of each.

`--source` lists the Runs one entry point started: `front_door`, `trigger`,
`api` or `workflow_step`. A schedule starts `trigger` Runs. On a list that
names only `signals.search` and `people.signals`, each Run also
carries a `title`: the saved-search name, else the first sales-signal criterion,
the ICP, or the target-company text. Every other list answers `title: null`.

Run start, list and detail JSON include `capability_id` and `contract_version`.
The values come from the published executor binding at admission. A later
rename or binding change does not change a Run. Both fields are null on old
Runs and custom executors. Null does not mean contract version zero.

`get` shows both fields in human output. Tree usage is the whole Run tree;
do not add parent and child usage totals. Capability cost metrics use separate
usage deltas and can be incomplete. Use durable usage records for billing.

`list` returns one page. Use `next_cursor` with `--cursor` to read the next
page. The default lists root Runs. Use `--all` to include child Runs.
To read another page, pass `next_cursor` to `--cursor` even when you use `--all`.

The spans list omits tool arguments and results. `span-detail` reads the bounded,
redacted input and output for one span. Use the span's `run_id` from the tree
response as `<owning-run-id>`; a span from another run returns 404.

When `list` is filtered with `--capability company.search`, `people.search` or
`signals.search`, its rows include `search_query`, normalized from the
capability's input contract. The human table shows it in the
`Definition / Search` column. It is null for unfiltered lists, non-search Runs
and older Runs whose input did not retain the submitted query.

`list` JSON and the human `Prospects` column carry `prospect_count`: how many
prospects the Run last wrote. It is null on every list but a
`--capability signals.search` or `--capability people.signals` one, because only
those lists pay for the count.
Zero is a Run that wrote no prospect, so do not read null as zero. A later Run
that returns a company again claims the row, so the count of an older Run falls.
Run detail always carries null.


### Product progress

`ac agentic runs progress <run-id> --json` reads a bounded summary of observed
product milestones across a root run and its child agents. It supports Signals,
Company and People Search. Pass a root run ID; a child ID returns 422.

The response contains `run_id`, `status` and `stages`. Each stage has a stable
`id`, readable `name` and `description`, `status`, `started_at`, `updated_at`
and `incomplete`. An incomplete stage does not establish completion. An empty
stage list does not mean the run has stopped; read the run status.

The progress response includes up to six agent and tool activity entries per active stage. Each entry has a name, kind and status. `activity_incomplete` marks a limited view; tool arguments and outputs are omitted.
