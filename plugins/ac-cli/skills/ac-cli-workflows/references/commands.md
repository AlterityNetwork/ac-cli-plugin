# AC CLI -- Workflows Command Reference

Complete flag reference for all workflow automation commands. All commands
require authentication (`ac login`).

## Table of Contents

1. [Runs](#runs)
2. [Schedules](#schedules)
3. [Presets](#presets)

---

## Runs

### `ac workflows runs create <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--input` | str | no | JSON string of input parameters |
| `--idempotency-key` | str | no | Idempotency key to prevent duplicate runs |
| `--json` | flag | no | Raw JSON output |

Creates a new workflow run. Returns 202 (accepted) with run ID and status.

### `ac workflows runs list <workflow-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

### `ac workflows runs get <workflow-id> <run-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns run details including status, input, output, and timing.

### `ac workflows runs logs <workflow-id> <run-id>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--limit` | int | 50 | Max log entries |
| `--offset` | int | 0 | Skip entries |
| `--json` | flag | off | Raw JSON output |

---

## Schedules

### `ac workflows schedules list <workflow-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Lists all schedules for the workflow.

### `ac workflows schedules get <workflow-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Gets the schedule details for the workflow.

### `ac workflows schedules create <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--cron` | str | yes | Cron expression (5-field: minute hour dom month dow) |
| `--timezone` | str | no | Timezone (default: UTC) |
| `--input` | str | no | JSON string of input parameters for each run |
| `--json` | flag | no | Raw JSON output |

### `ac workflows schedules update <workflow-id> <schedule-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--cron` | str | Updated cron expression |
| `--timezone` | str | Updated timezone |
| `--input` | str | Updated JSON input parameters |
| `--json` | flag | Raw JSON output |

### `ac workflows schedules delete <workflow-id> <schedule-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac workflows schedules preview <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--cron` | str | yes | Cron expression to preview |
| `--timezone` | str | no | Timezone (default: UTC) |
| `--count` | int | no | Number of upcoming times to show (default: 5) |
| `--json` | flag | no | Raw JSON output |

Shows the next N upcoming run times for a cron expression without creating a schedule.

### `ac workflows schedules toggle <workflow-id> <schedule-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--enabled/--disabled` | flag | yes | Enable or disable the schedule |
| `--json` | flag | no | Raw JSON output |

---

## Presets

### `ac workflows presets list <workflow-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac workflows presets get <workflow-id> <preset-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac workflows presets create <workflow-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Preset name |
| `--description` | str | no | Preset description |
| `--config` | str | no | JSON string of preset configuration |
| `--json` | flag | no | Raw JSON output |

### `ac workflows presets update <workflow-id> <preset-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--name` | str | Update preset name |
| `--description` | str | Update description |
| `--config` | str | Update JSON configuration |
| `--json` | flag | Raw JSON output |

### `ac workflows presets delete <workflow-id> <preset-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |
