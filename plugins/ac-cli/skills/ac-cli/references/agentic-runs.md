# Agentic Runs

These commands require the CLI and API from `agentic-platform` until cutover.

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
page. For these commands, `--all` includes child Runs; it does not read all
pages. The default lists root Runs.
