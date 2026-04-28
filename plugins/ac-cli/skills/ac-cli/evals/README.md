# Skill Evals -- Conventions

Each entry in `evals.json` is a scenario the `ac-cli` skill must handle. `run.py` loads the skill, spawns `claude -p` per scenario, records the actions (Bash invocations + Read tool calls + Skill invocations), and grades them against `assertions`.

## Running

```bash
# All evals against local working tree (default — auto-detects plugin dir)
python evals/run.py

# Subset
python evals/run.py --ids 1,5,12

# Use a specific plugin dir (e.g. force testing local edits, not marketplace cache)
python evals/run.py --plugin-dir /Users/me/code/ac-cli-plugin

# Cheap model + multiple runs for stability
python evals/run.py --model haiku --runs 3 --workers 8

# Save results JSON
python evals/run.py --output /tmp/eval-results.json
```

Exit code: 0 if every scenario passes, 1 otherwise.

## Assertion Types

| `type` | Meaning | Pattern |
|--------|---------|---------|
| `command_matches` | At least one Bash command Claude ran matches the regex in `text`. | regex over the executed command line |
| `command_sequence` | Multiple commands ran **in the listed order** (extra commands between them are allowed). | comma- or sentence-separated regexes inside `text` |
| `reads_file` | Claude invoked the Read tool on one of the listed reference paths before the related command. | absolute or `references/`-relative path |
| `auth_check_first` | `ac whoami` (or `ac login`) appears before the first mutating command. | implicit — no extra args needed |

## Why not `output_contains`?

The previous suite asserted on the description Claude wrote in chat. That is fragile: the same correct sequence of `ac` invocations can be described many ways. Asserting on the **commands actually executed** (and on which reference files were consulted) tests the behavior we care about.

## Adding a new scenario

1. Append a new object to the `evals` array. Pick the next id.
2. Choose assertion types from the table above. Prefer `command_sequence` for multi-step flows; reserve `command_matches` for single-flag correctness checks.
3. For dry-run / preview-first flows, always use `command_sequence` to enforce ordering.
4. For "skill must look up the docs" scenarios, use `reads_file` pointing at the correct domain reference (`references/<domain>.md`).
5. Run the eval suite locally before committing: `claude eval ./evals/evals.json`.

## Coverage targets

The suite should hit:
- Every domain (CRM, Envoy, Workflows, Admin, Platform, Auth/Env)
- Both setup steps (install + auth) at least once
- Every dry-run pattern listed in `SKILL.md` (cron preview, import preview, company-match preview)
- Auth recovery (401 → re-login)
- Env switching (must re-auth)
- References-file lookup (skill consults `references/*.md` instead of guessing)
- Exit-code branching ($? = 3, 4, 5)

## Anti-patterns

- Do NOT assert on chat text wording.
- Do NOT hard-code generated IDs or timestamps; use placeholders the runner substitutes.
- Do NOT add scenarios that require credentials. Use stub envs.
