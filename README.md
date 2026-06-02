# AgencyCore CLI Plugin for Claude Code & Cowork

A Claude Code plugin that adds CRM management skills powered by the [AgencyCore CLI](https://pypi.org/project/agencycore-cli/).

## What it does

The `ac-cli-crm` skill lets Claude manage your AgencyCore CRM data from the terminal — companies, people, deals, activities, communications, lists, imports, and more.

## Prerequisites

Install the AgencyCore CLI before using this plugin:

```bash
pip install agencycore-cli
```

Then authenticate:

```bash
ac login
```

## Installation

### From the marketplace

```bash
/plugin marketplace add AlterityNetwork/ac-cli-plugin
/plugin install ac-cli@agencycore-plugins
```

### For development/testing

```bash
claude --plugin-dir ./ac-cli-plugin
```

## Usage

Once installed, the skill is automatically triggered when you ask Claude to:

- Look up, create, update, or delete CRM records
- Search CRM data or check your pipeline
- Draft emails or manage communications
- Import contacts from a file
- Anything CRM-related via the command line

You can also invoke it directly:

```
/ac-cli:ac-cli-crm
```

## What's included

| Skill | Description |
|-------|-------------|
| `ac-cli-crm` | Full CRM operations — companies, people, deals, activities, communications, lists, imports, search, and dashboard |

## Adding to your team's project

To auto-prompt teammates to install this plugin, add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "agencycore-plugins": {
      "source": {
        "source": "github",
        "repo": "AlterityNetwork/ac-cli-plugin"
      }
    }
  },
  "enabledPlugins": {
    "ac-cli@agencycore-plugins": true
  }
}
```
