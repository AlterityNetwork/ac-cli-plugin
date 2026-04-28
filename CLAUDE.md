# AgencyCore CLI Plugin

Claude Code marketplace plugin providing AgencyCore management skills (CRM, admin, envoy, platform, workflows) powered by the AgencyCore CLI (`ac`). Configuration-driven — no compiled code, just JSON metadata + Markdown skill definitions.

## Critical Rules (Always Apply)

1. **No application code**: This repo is JSON config + Markdown docs only — one unified skill covering CRM, admin, envoy, platform, and workflows. No TypeScript, no build step.
2. **Version sync**: `plugin.json` and `marketplace.json` must always have the same version. The pre-commit hook handles this automatically.
3. **Kebab-case names**: Plugin names must use kebab-case (e.g., `agencycore-cli`) to pass Cowork validation.
4. **SKILL.md is the product**: The skill file is what Claude reads at runtime — keep it accurate, complete, and tested against the latest CLI.
5. **`SKILL.md` ≤ 500 lines**: per-domain detail belongs in `plugins/ac-cli/skills/ac-cli/references/<domain>.md`; exhaustive flag tables in `references/commands.md`. References stay one level deep from SKILL.md.
6. **Scoped `allowed-tools`**: only the binaries actually used (`Bash(ac *)`, `Bash(pip *)`, `Bash(uv *)`, `Bash(pipx *)`, `Bash(jq *)`). No open `Bash`.
7. **Push directly to `main`**: This repo is not Heroku-deployed. Use `ALLOW_MAIN_PUSH=1 git push` to bypass the inherited pre-push hook.

## Project Layout

```
.claude-plugin/
  marketplace.json       → Marketplace registry (namespace, plugin list, versions)
plugins/ac-cli/
  .claude-plugin/
    plugin.json          → Plugin manifest (name, version, metadata)
  skills/
    ac-cli/              → Unified skill (CRM, admin, envoy, platform, workflows)
      SKILL.md           → Quick reference guide (≤ 500 lines)
      references/
        commands.md           → Full flag tables for every command
        crm.md                → CRM quick reference
        envoy.md              → Outreach quick reference
        workflows.md          → Workflows quick reference
        admin.md              → Admin quick reference (superadmin)
        platform.md           → Platform quick reference
        auth-env.md           → Auth & environment quick reference
        workflows-recipes.md  → Multi-step recipes beyond the SKILL.md core 6
      evals/
        evals.json       → Skill evaluation test cases (~70 scenarios)
        run.py           → Eval runner (claude -p, grades assertions)
        README.md        → Eval vocab + runner usage
scripts/
  bump-version.sh        → Auto-bumps patch version on commit (pre-commit hook)
```

## How It Works

- **Marketplace registration**: `.claude-plugin/marketplace.json` defines the `agencycore-plugins` namespace and lists available plugins
- **Plugin manifest**: `plugins/ac-cli/.claude-plugin/plugin.json` provides metadata for marketplace display
- **Skill execution**: `SKILL.md` frontmatter defines trigger conditions and allowed tools (Bash only). The body is Claude's runtime guide for executing CRM, admin, envoy, platform, and workflow commands
- **CLI dependency**: All operations delegate to the `agencycore-cli` Python package (installed from PyPI at runtime)

## Versioning

Patch version auto-bumps on every commit via the pre-commit hook (`scripts/bump-version.sh`). The hook updates both `plugin.json` and `marketplace.json` and stages the changes.

For minor/major bumps, edit both files manually before committing (the hook will not double-bump if versions already differ from what it reads).

## Installation (for users)

```bash
# From marketplace
/plugin marketplace add AlterityNetwork/ac-cli-plugin
/plugin install ac-cli@agencycore-plugins

# For local development
claude --plugin-dir ./ac-cli-plugin
```

## Testing Changes

### Local edits do NOT auto-reach Claude

When `ac-cli@agencycore-plugins` is installed via the marketplace (the normal path), Claude reads the skill from the cached copy at `~/.claude/plugins/cache/agencycore-plugins/ac-cli/<version>/`, NOT from this working tree. Editing `plugins/ac-cli/skills/ac-cli/SKILL.md` here has zero effect on triggering until you publish.

The publish path:

```bash
# 1. Edit, commit, push (parent CLAUDE.md says ALLOW_MAIN_PUSH=1 since this repo lacks staging)
ALLOW_MAIN_PUSH=1 git push origin main

# 2. In any session that has the plugin installed, refresh the marketplace cache
/plugin update ac-cli@agencycore-plugins
```

`/plugin marketplace update agencycore-plugins` followed by `/plugin install ac-cli@agencycore-plugins` is the equivalent two-step.

### Local-only test BEFORE publishing

Use the eval runner — it spawns `claude -p` with `--plugin-dir` pointing at the working tree, bypassing marketplace cache:

```bash
python plugins/ac-cli/skills/ac-cli/evals/run.py --runs 2 --model haiku
```

For interactive checks, drop into a session loading the local working tree:

```bash
claude --plugin-dir ./
```

Then ask "list my deals", "draft a cold email to Jane at Acme", "schedule workflow wf-99 every Monday at 9am ET", etc. and verify Claude triggers the skill rather than falling back to direct `Bash("ac --help")` exploration.

### Trigger pitfalls observed in the field

- If `ac-cli/` source code is on Claude's `--add-dir` path or in cwd, Claude may grep the source instead of loading the skill — keep tests in a clean cwd.
- `--plugin-dir` alone does NOT enable a plugin; it only makes it discoverable. Activation still goes through `enabledPlugins` in `.claude/settings.json` (the agencycore parent repo's settings does this for us).
- Description trigger keywords matter — generic verbs like "schedule a workflow" or "upload a PDF" without "ac"/"AgencyCore" need explicit object-noun matches in the skill description (e.g. "knowledge base PDF resources", "schedule workflow cron preset").

## Detailed Rules

See `.claude/rules/` for focused guides:
- `01-plugin-structure` — Marketplace, manifests, and file layout
- `02-skill-authoring` — Writing and updating SKILL.md and command references
