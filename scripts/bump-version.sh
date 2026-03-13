#!/usr/bin/env bash
# Auto-bump patch version in plugin.json and marketplace.json
# Called by the pre-commit hook

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_JSON="$REPO_ROOT/plugins/ac-cli/.claude-plugin/plugin.json"
MARKETPLACE_JSON="$REPO_ROOT/.claude-plugin/marketplace.json"

# Extract current version from plugin.json
CURRENT=$(grep '"version"' "$PLUGIN_JSON" | head -1 | sed 's/.*"version": *"\([^"]*\)".*/\1/')

if [ -z "$CURRENT" ]; then
  echo "bump-version: could not read version from plugin.json" >&2
  exit 0
fi

# Split into major.minor.patch and bump patch
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"
PATCH=$((PATCH + 1))
NEW="$MAJOR.$MINOR.$PATCH"

# Update both files
sed -i '' "s/\"version\": *\"$CURRENT\"/\"version\": \"$NEW\"/" "$PLUGIN_JSON"
sed -i '' "s/\"version\": *\"$CURRENT\"/\"version\": \"$NEW\"/" "$MARKETPLACE_JSON"

# Stage the version changes so they're included in the commit
git add "$PLUGIN_JSON" "$MARKETPLACE_JSON"

echo "bump-version: $CURRENT → $NEW"
