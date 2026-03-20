# Plugin Structure

## File Roles

| File | Purpose | When to Edit |
|------|---------|-------------|
| `.claude-plugin/marketplace.json` | Marketplace namespace registry — lists all plugins, versions, tags | Adding a new plugin, changing metadata/tags |
| `plugins/ac-cli/.claude-plugin/plugin.json` | Plugin manifest — name, version, author, license | Changing plugin metadata (version auto-bumped) |
| `plugins/ac-cli/skills/ac-cli-crm/SKILL.md` | Skill definition — Claude's runtime guide | CLI commands change, new CRM features, UX improvements |
| `plugins/ac-cli/skills/ac-cli-crm/references/commands.md` | Full command reference with flags | CLI adds/removes/changes flags or commands |
| `scripts/bump-version.sh` | Pre-commit hook for auto version bump | Changing version bump logic |

## Marketplace Registration

The marketplace uses a two-level structure:

1. **Namespace** (`.claude-plugin/marketplace.json`): Groups plugins under `agencycore-plugins`
2. **Plugin** (`plugins/<name>/.claude-plugin/plugin.json`): Individual plugin metadata

Consumers reference plugins as `<plugin-name>@<namespace>`, e.g., `ac-cli@agencycore-plugins`.

## Adding a New Plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json` with name, description, version, author, license
2. Create `plugins/<name>/skills/<skill-name>/SKILL.md` with frontmatter and guide
3. Add the plugin entry to `.claude-plugin/marketplace.json` plugins array
4. Update `scripts/bump-version.sh` to include the new plugin's `plugin.json` path

## Naming Rules

- Plugin directory names: kebab-case (`ac-cli`)
- Plugin `name` field in `plugin.json`: kebab-case (`agencycore-cli`) — required for Cowork validation
- Skill directory names: kebab-case (`ac-cli-crm`)
- Namespace: kebab-case (`agencycore-plugins`)

## Version Management

- **Patch**: Auto-bumped on every commit by pre-commit hook
- **Minor/Major**: Edit `plugin.json` and `marketplace.json` manually, then commit
- Both files must always have the same version string
