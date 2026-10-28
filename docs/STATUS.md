# Status (update at the end of every session)

## Verified done
- main is in sync with origin, CI green: cc13cdf
- Local tests: 13 passing
- uv uses Python 3.12 in .venv
- VS Code interpreter set to .venv (3.12)

## Open
- Local secrets (dev DB user, root password, SECRET_KEY)
- V2-001: ResourceMetadata models + tests

## Next action
- ___

## Parked (time-sensitive)
- Domain/hosting lapsed: first step is back up DB + media

## Gotchas
- VS Code must use .venv (3.12)
- Never use PowerShell > to write config files (UTF-16)
- .env lives beside settings.py (merouni/merouni/)