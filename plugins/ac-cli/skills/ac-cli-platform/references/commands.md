# AC CLI -- Platform Command Reference

Complete flag reference for platform utility commands. Most commands require
authentication (`ac login`) unless noted otherwise.

## Table of Contents

1. [Files (Images)](#files-images)
2. [Apps](#apps)
3. [Writing Styles](#writing-styles)
4. [Nylas (Email Integration)](#nylas-email-integration)
5. [Environment](#environment)
6. [Health](#health)
7. [Hooks](#hooks)

---

## Files (Images)

### `ac files images upload <file-path>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--category` / `-c` | str | yes | Storage category: `avatars`, `organization_logos`, `crm_company_logos`, `general_images`, `apps_assets` |
| `--json` | flag | no | Raw JSON output |

Uploads an image file. Allowed formats: .jpg, .jpeg, .png, .gif, .webp, .svg, .avif. Max size: 1 MB.

### `ac files images delete <key>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

Deletes an image by its R2 object key.

---

## Apps

### `ac apps list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--org-id` | str | auto | Organization ID (auto-resolved from /whoami) |
| `--include-inactive` | flag | off | Include inactive/uninstalled apps |
| `--limit` | int | 100 | Max results |
| `--offset` | int | 0 | Skip results |
| `--json` | flag | off | Raw JSON output |

### `ac apps install <app-slug>`
| Flag | Type | Description |
|------|------|-------------|
| `--org-id` | str | Organization ID (auto-resolved from /whoami) |
| `--json` | flag | Raw JSON output |

### `ac apps uninstall <app-slug>`
| Flag | Type | Description |
|------|------|-------------|
| `--org-id` | str | Organization ID (auto-resolved from /whoami) |
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac apps usage-event <app-slug>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--org-id` | str | no | Organization ID (auto-resolved) |
| `--event-type` | str | yes | Event type to record |
| `--metadata` | str | no | JSON metadata for the event |
| `--json` | flag | no | Raw JSON output |

### `ac apps usage <app-slug>`
| Flag | Type | Description |
|------|------|-------------|
| `--org-id` | str | Organization ID (auto-resolved) |
| `--json` | flag | Raw JSON output |

Returns usage summary for the app.

### `ac apps configs <app-slug>`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--org-id` | str | auto | Organization ID (auto-resolved) |
| `--mask-secrets/--no-mask-secrets` | flag | True | Mask secret values in output |
| `--json` | flag | off | Raw JSON output |

### `ac apps update-config <app-slug> <config-key>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--value` | str | yes | New value for the config key |
| `--org-id` | str | no | Organization ID (auto-resolved) |
| `--json` | flag | no | Raw JSON output |

### `ac apps delete-config <app-slug> <config-key>`
| Flag | Type | Description |
|------|------|-------------|
| `--org-id` | str | Organization ID (auto-resolved) |
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

---

## Writing Styles

### `ac styles list`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--include-inactive` | flag | off | Include inactive styles |
| `--json` | flag | off | Raw JSON output |

### `ac styles get <style-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

### `ac styles create`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | str | yes | Style name |
| `--description` | str | no | Style description |
| `--tone` | str | no | Tone (e.g. formal, casual, professional) |
| `--formality` | str | no | Formality level (e.g. high, medium, low) |
| `--json` | flag | no | Raw JSON output |

### `ac styles update <style-id>`
Same optional flags as `create`. Only provided fields are updated.

### `ac styles delete <style-id>`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac styles train <style-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--sample-text` | str | yes | Sample text to train the style on |
| `--json` | flag | no | Raw JSON output |

Starts a training session using the provided sample text.

### `ac styles feedback <session-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--rating` | int | yes | Rating for the training output |
| `--comments` | str | no | Additional feedback comments |
| `--json` | flag | no | Raw JSON output |

### `ac styles iterate <session-id>`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--feedback` | str | yes | Feedback to refine the style |
| `--json` | flag | no | Raw JSON output |

### `ac styles analyze`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--text` | str | yes | Text to analyze for writing style characteristics |
| `--json` | flag | no | Raw JSON output |

---

## Nylas (Email Integration)

### `ac nylas oauth-start`
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--provider` | str | google | OAuth provider (google, microsoft) |
| `--return-path` | str | None | Path to redirect after OAuth |
| `--json` | flag | off | Raw JSON output |

Starts the OAuth flow and returns the authorization URL.

### `ac nylas account`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Returns connected Nylas account details.

### `ac nylas org-accounts`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Lists all connected accounts in the organization.

### `ac nylas disconnect`
| Flag | Type | Description |
|------|------|-------------|
| `--yes` | flag | Skip confirmation prompt |
| `--json` | flag | Raw JSON output |

### `ac nylas send`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--to` | str | yes | Recipient email address |
| `--subject` | str | yes | Email subject |
| `--body` | str | yes | Email body |
| `--reply-to-message-id` | str | no | Message ID to reply to |
| `--json` | flag | no | Raw JSON output |

### `ac nylas update-signature`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--signature` | str | yes | Email signature (HTML or plain text) |
| `--json` | flag | no | Raw JSON output |

### `ac nylas validate-signature`
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--signature` | str | yes | Signature to validate |
| `--json` | flag | no | Raw JSON output |

---

## Environment

*No authentication required for environment commands.*

### `ac env list`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Shows all environments (local, staging, production) and login status for each.

### `ac env show`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Shows active environment details.

### `ac env use <name>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Switches the active environment. Valid names: `local`, `staging`, `production`.

---

## Health

*No authentication required.*

### `ac health check`
| Flag | Type | Description |
|------|------|-------------|
| `--api-url` | str | Override the default API URL |
| `--json` | flag | Raw JSON output |

Checks if the API is reachable and returns health status.

---

## Hooks

### `ac hooks list <capability>`
| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Raw JSON output |

Lists available hooks for the specified capability.
