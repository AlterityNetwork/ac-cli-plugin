# Auth & Environment Quick Reference

`ac health check` and `ac env` commands do NOT require authentication. Everything else does.

## Authentication

```bash
ac login --email "user@example.com" --password "their-password"
ac login --dev --email "user@example.com" --password "their-password"   # Local dev
ac logout
ac whoami
ac health check [--api-url https://custom-api.example.com]
```

## Environment

```bash
ac env list                    # Show all environments and login status
ac env show                    # Show active environment details
ac env use <name>              # Switch environment (local | staging | production)
```

Valid names: `local`, `staging`, `production`. After switching, you must `ac login` again — credentials are per-environment.

## Recovering from auth errors

| Symptom | Fix |
|---------|-----|
| `not authenticated` | `ac login --email ... --password ...` |
| 401 after long idle | Token refresh failed — re-run `ac login` |
| 403 / "forbidden" | Account lacks role; admin commands need `superadmin` (check `ac whoami`) |
| `ac env use <x>` "no effect" | Expected: env is switched but you must `ac login` again on the new env |
