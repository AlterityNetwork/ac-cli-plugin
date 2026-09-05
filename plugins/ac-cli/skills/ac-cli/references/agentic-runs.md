# Agentic Capabilities and Runs

These commands require the CLI and API from `agentic-platform` until cutover.

## Start a capability

Use a stable product ID: `company.search`, `company.enrich`, `people.search`,
`people.enrich` or `signals.search`. The capability must be installed and active
for the current organization. Its published schema defines the input fields.

```bash
ac agentic capabilities start company.search --contract-version 1 \
  --input '{"sources":["supplied"],"companies":[{"kind":"domain","value":"example.com"}]}' \
  --idempotency-key company-search-request-42 --json
```

All three flags are required. Use a positive integer contract version, a JSON
input object, and a nonblank delivery key with 1–200 header-safe ASCII characters.
Input is limited to 32 KiB. The server applies the published schema and preserves
omitted fields; it does not insert schema defaults.

Reuse the same key and request after a timeout. A matching replay returns the
original Run, even after a binding change. A changed capability, version or input
with that key returns `idempotency_conflict` (409). Use a new key for a new request.
Keys are isolated by organization, caller and start source.

The response is the existing Run detail. Read `status` as well as `outcome`:
`started` can mean queued, waiting for approval, or failed on policy admission.
A duplicate does not start another execution. Read the Run with the commands below.

Errors preserve the API code in JSON output: unknown ID (404), unavailable binding
or stale version (409), missing scope (403), invalid input (422), oversized input
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
start a second Run, and use 1–200 header-safe ASCII characters. The CLI refuses
an empty flag before it calls the API. A repeat with the same key returns the
first Run and starts no second execution; human output marks it `Duplicate`.

The definition must be published, and it must be an agent or a workflow.
`ac agentic definitions list` also returns drafts, disabled definitions and
skills. Each of those returns 409. `ac agentic capabilities start` above starts
a published product capability, and it takes a contract version.

## Read Runs

```bash
ac agentic runs list --json
ac agentic runs get <run-id>
ac agentic runs get <run-id> --json
ac agentic runs list --parent <run-id> --json
```

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
