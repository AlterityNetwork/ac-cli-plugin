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

> **MANDATORY**: `--cron` AND `--timezone` are co-required for `schedules create` and `schedules preview`. Never omit `--timezone`. Translate any user-mentioned region: "ET"/"Eastern"/"EST" → `America/New_York`, "PT"/"Pacific" → `America/Los_Angeles`, "UTC"/"GMT" → `UTC`, "London" → `Europe/London`. Translate "weekday"/"weekdays" → cron `1-5` in the dow field.

```bash
ac workflows schedules list <workflow-id>
ac workflows schedules get <workflow-id>

# create — --cron and --timezone are BOTH required
ac workflows schedules create <workflow-id> --cron "0 9 * * 1" --timezone "America/New_York" \
  [--input '{"key":"value"}']

# update — pass any combination of --cron / --timezone / --input
ac workflows schedules update <workflow-id> <schedule-id> \
  [--cron "0 10 * * 1"] [--timezone UTC]

ac workflows schedules delete <workflow-id> <schedule-id> [--yes]

# preview — always pass all three to see the next N fire times
ac workflows schedules preview <workflow-id> --cron "0 9 * * 1" --timezone "America/New_York" --count 5

ac workflows schedules toggle <workflow-id> <schedule-id> --enabled/--disabled
```

Cron format: standard 5-field (`minute hour dom month dow`). Common patterns:

| User says | Cron | Timezone |
|-----------|------|----------|
| Every weekday 9am ET | `0 9 * * 1-5` | `America/New_York` |
| Every Monday 9am ET | `0 9 * * 1` | `America/New_York` |
| Every 6 hours UTC | `0 */6 * * *` | `UTC` |
| 1st of month 8:30am | `30 8 1 * *` | (user's tz) |

**Always run `schedules preview` before `create`** to confirm the next 5 fire times look right.

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
