# Workflows Quick Reference

All workflow subcommands take `<workflow-id>` as their first positional argument. For full flag tables see `commands.md` (Workflows section).

## Runs

```bash
ac workflows runs create <workflow-id> [--input '{"key":"value"}'] [--idempotency-key <key>]
ac workflows runs list <workflow-id> [--limit 50] [--offset 0]
ac workflows runs get <workflow-id> <run-id>
ac workflows runs logs <workflow-id> <run-id> [--limit 50] [--offset 0]
```

## Schedules

```bash
ac workflows schedules list <workflow-id>
ac workflows schedules get <workflow-id>
ac workflows schedules create <workflow-id> --cron "0 9 * * 1" \
  [--timezone "America/New_York"] [--input '{"key":"value"}']
ac workflows schedules update <workflow-id> <schedule-id> \
  [--cron "0 10 * * 1"] [--timezone UTC]
ac workflows schedules delete <workflow-id> <schedule-id> [--yes]
ac workflows schedules preview <workflow-id> --cron "0 9 * * 1" \
  [--timezone UTC] [--count 5]
ac workflows schedules toggle <workflow-id> <schedule-id> --enabled/--disabled
```

Cron format: standard 5-field (`minute hour dom month dow`). Always run `schedules preview` before `create` to confirm interpretation.

## Presets

```bash
ac workflows presets list <workflow-id>
ac workflows presets get <workflow-id> <preset-id>
ac workflows presets create <workflow-id> --name "Daily Sync" \
  [--description "..."] [--config '{"key":"value"}']
ac workflows presets update <workflow-id> <preset-id> --name "Updated Preset"
ac workflows presets delete <workflow-id> <preset-id> [--yes]
```

## CSV Parsing

```bash
ac workflows csv-parse <file.csv>
```

## Discovered Companies (from workflow runs)

```bash
ac workflows run-companies list <workflow-id> [--limit 50] [--offset 0] [--include-in-crm]
ac workflows run-companies list-by-run <workflow-id> <run-id>
ac workflows run-companies add-to-crm <workflow-id> --company-ids id1,id2
ac workflows run-companies crm-count <workflow-id>
ac workflows run-companies delete <workflow-id> --company-ids id1,id2 [--yes]
```

## Discovered People (from workflow runs)

```bash
ac workflows run-people list <workflow-id> [--limit 50] [--offset 0] [--include-in-crm]
ac workflows run-people list-by-run <workflow-id> <run-id>
ac workflows run-people company-match-preview <workflow-id> --person-ids id1,id2
ac workflows run-people company-search <workflow-id> --query "acme"
ac workflows run-people add-to-crm <workflow-id> --person-ids id1,id2 [--overrides-file overrides.json]
ac workflows run-people crm-count <workflow-id>
ac workflows run-people delete <workflow-id> --person-ids id1,id2 [--yes]
```
