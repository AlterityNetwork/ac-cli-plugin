# AgencyCore CLI Plugin

Claude Code marketplace plugin providing AgencyCore management skills (CRM, admin, envoy, platform, workflows) powered by the AgencyCore CLI (`ac`). Configuration-driven — no compiled code, just JSON metadata + Markdown skill definitions.

## Critical Rules (Always Apply)

1. **No application code**: This repo is JSON config + Markdown docs only — 5 skills (CRM, admin, envoy, platform, workflows). No TypeScript, no build step.
2. **Version sync**: `plugin.json` and `marketplace.json` must always have the same version. The pre-commit hook handles this automatically.
3. **Kebab-case names**: Plugin names must use kebab-case (e.g., `agencycore-cli`) to pass Cowork validation.
4. **SKILL.md is the product**: The skill file is what Claude reads at runtime — keep it accurate, complete, and tested against the latest CLI.
5. **Push directly to `main`**: This repo is not Heroku-deployed. Use `ALLOW_MAIN_PUSH=1 git push` to bypass the inherited pre-push hook.

## Project Layout

```
.claude-plugin/
  marketplace.json       → Marketplace registry (namespace, plugin list, versions)
plugins/ac-cli/
  .claude-plugin/
    plugin.json          → Plugin manifest (name, version, metadata)
  skills/
    ac-cli-crm/          → CRM operations skill
    ac-cli-admin/        → Admin operations skill
    ac-cli-envoy/        → Envoy outreach skill
    ac-cli-platform/     → Platform operations skill
    ac-cli-workflows/    → Workflow management skill
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

## Detailed Rules

See `.claude/rules/` for focused guides:
- `01-plugin-structure` — Marketplace, manifests, and file layout
- `02-skill-authoring` — Writing and updating SKILL.md and command references
