# Skill Authoring

## SKILL.md Structure

Every skill file has two parts:

### Frontmatter (YAML)
```yaml
---
name: ac-cli-crm
description: >
  One-paragraph description used for trigger matching.
  Include keywords users might say.
allowed-tools:
  - Bash
argument-hint: "[command or question]"
---
```

- `description` drives when Claude auto-triggers the skill — include all relevant keywords and phrases
- `allowed-tools` restricts what tools the skill can use (currently Bash only)
- `argument-hint` shows in help text

### Body (Markdown)

The body is Claude's runtime instruction manual. Structure:

1. **Setup** — Install/upgrade CLI, check auth
2. **Command reference** — Quick reference with examples
3. **Patterns** — Tags, dates, pagination, JSON output
4. **Workflows** — Multi-step recipes for common tasks
5. **Troubleshooting** — Error → fix table

## Rules for Editing SKILL.md

- **Always install first**: Step 0 must always run `pip install --upgrade agencycore-cli` — never assume it's installed
- **Never expose credentials in examples**: Use placeholders like `<company-id>`, `user@example.com`
- **Ask for credentials interactively**: The skill tells Claude to ask the user for email/password, then run `ac login` for them
- **Keep commands tested**: Every command example should work against the current CLI version
- **Reference file for details**: Keep `SKILL.md` as a usable quick guide; put exhaustive flag documentation in `references/commands.md`

## references/commands.md

Complete flag-level documentation for every CLI command. Structured by entity (Companies, People, Deals, etc.) with tables showing flag name, type, default, and description.

Update this file whenever `ac-cli` adds, removes, or changes command flags. The source of truth is `ac-cli`'s Typer command definitions in `ac-cli/src/agencycore_cli/commands/crm/`.

## Testing Changes

1. Run `claude --plugin-dir ./ac-cli-plugin` to load the plugin locally
2. Ask Claude a CRM question (e.g., "list my deals") to trigger the skill
3. Verify the skill installs the CLI, authenticates, and runs the correct commands
4. Check that `references/commands.md` flags match `ac <command> --help` output
