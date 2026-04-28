# Skill Authoring

## SKILL.md Structure

Every skill file has two parts: a YAML frontmatter block and a Markdown body. Both load only when the skill is triggered — the frontmatter `description` is what Claude sees during auto-discovery, so it carries most of the trigger weight.

### Frontmatter (YAML)
```yaml
---
name: ac-cli
description: >
  Short, third-person, trigger-rich. Front-load the use case in the first
  sentence. Include the natural phrases users say (e.g. "ac commands", "CRM",
  "draft an email"). Max 1024 chars when rendered.
when_to_use: >
  Optional refinement of when to fire. Use to disambiguate from overlapping
  skills.
allowed-tools:
  - Bash(ac *)
  - Bash(pip *)
  - Bash(uv *)
  - Bash(pipx *)
  - Bash(jq *)
argument-hint: "[command or question]"
---
```

- `description` drives auto-trigger matching — write in third person, include keywords users naturally say, keep under 1024 chars
- `when_to_use` (optional) refines the trigger; treat it as an extension of the description
- `allowed-tools` MUST be scoped to specific binaries with glob patterns. Open `Bash` is forbidden — it bypasses permission prompts for unrelated commands and grows the skill's effective surface area
- `argument-hint` shows in help text

### Body (Markdown)

The body is Claude's runtime guide. Target structure:

1. **Step 0 — Install** — Always run `pip install --upgrade agencycore-cli` first; never assume the CLI is present
2. **Step 1 — Authenticate** — `ac whoami`; if not logged in, ask the user for credentials and run `ac login` for them
3. **Output Modes** — `--json` semantics
4. **Domain Map** — pointer table to `references/<domain>.md`
5. **Important Patterns** — tags, dates, pagination, cron, JSON input, upload constraints (cross-cutting only)
6. **Dry-Run / Preview Patterns** — every irreversible mutation paired with its preview command
7. **Exit Codes** — semantic table (0 success, 1 generic, 2 validation, 3 not found, 4 auth, 5 conflict)
8. **JSON-First Scripting** — canonical `ac … --json | jq …` recipes
9. **Common Workflows** — 6 highest-signal multi-step recipes (others go in `references/workflows-recipes.md`)
10. **Agent-Friendly Features** — JSON errors, `AC_YES=1`, exit codes
11. **Troubleshooting** — error → fix table

## Size Budget

- **`SKILL.md` ≤ 500 lines.** Anthropic's guidance is to keep the always-loaded skill body small; per-domain detail belongs in `references/`. Current target: ~350 lines.
- **References ≤ 1 level deep from `SKILL.md`.** Do NOT chain references (SKILL → A → B). Reference files may link to each other for cross-reference, but the skill must not require multi-hop traversal.
- One reference file per domain (`crm.md`, `envoy.md`, `workflows.md`, `admin.md`, `platform.md`, `auth-env.md`). The exhaustive flag table stays in `references/commands.md`.

## Rules for Editing SKILL.md

- **Install first, always**: Step 0 must run `pip install --upgrade agencycore-cli`
- **Never expose credentials in examples**: use `<company-id>`, `user@example.com`
- **Ask the user for creds, then run `ac login` for them**: do not tell the user to run login themselves
- **Keep commands tested** against the current `ac` version
- **Push detail to references**: the skill body is for orientation, patterns, and the 6 most common cross-domain recipes; flag tables and per-domain command lists live in `references/`
- **Scope `allowed-tools`**: only the binaries actually used (`ac`, `pip`, `uv`, `pipx`, `jq`). Adding new tool families requires a justification

## references/

Layout and roles:

| File | Role | Update trigger |
|------|------|---------------|
| `commands.md` | Exhaustive flag tables, all 220+ commands | CLI adds/removes/renames a flag |
| `crm.md` | Quick reference for CRM commands (companies, people, deals, activities, comms, lists, import, search, dashboards) | CRM CLI surface changes |
| `envoy.md` | Quick reference for outreach commands | Envoy CLI surface changes |
| `workflows.md` | Quick reference for workflow commands | Workflows CLI surface changes |
| `admin.md` | Quick reference for admin commands (requires `superadmin`) | Admin CLI surface changes |
| `platform.md` | Quick reference for files, apps, styles, Nylas, hooks, messaging, chat, resources, profiles | Platform CLI surface changes |
| `auth-env.md` | Auth + environment commands and recovery patterns | Auth/env behavior changes |
| `workflows-recipes.md` | Multi-step recipes that don't make the SKILL.md core 6 | New common multi-step pattern emerges |

The source of truth for flags is `ac-cli`'s Typer command definitions in `ac-cli/src/agencycore_cli/commands/`.

## Evals

`evals/evals.json` is the regression suite. `evals/run.py` is the runner — spawns `claude -p --plugin-dir <local>` per scenario, captures Bash/Read/Skill tool calls, grades against assertions. `evals/README.md` documents the assertion vocabulary (`command_matches`, `command_sequence`, `reads_file`, `auth_check_first`).

```bash
python evals/run.py --runs 2 --workers 8 --model haiku
```

Prefer behavior assertions (commands actually executed, files actually read) over chat-text matching.

## Testing Changes

1. `claude --plugin-dir ./ac-cli-plugin` — load locally
2. Trigger prompts that should auto-discover the skill (e.g. "list my deals", "draft an email to Jane", "switch to staging")
3. Verify the skill installs the CLI, authenticates, reads the right `references/<domain>.md`, and runs the documented commands
4. Run `wc -l plugins/ac-cli/skills/ac-cli/SKILL.md` — must be ≤ 500
5. Run the eval suite
