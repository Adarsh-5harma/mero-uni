# Status (update at the end of every session)

## Verified done
- main is in sync with origin, CI green: cc13cdf
- Local tests: 13 passing
- uv uses Python 3.12 in .venv
- VS Code interpreter set to .venv (3.12)
- ENVIRONMENT/DEBUG parse correctly: 'development' 'True' True
- Local secrets: app connects as `merouni_dev`; old root password rejected; grants scoped to `csai_resources` and `test_csai_resources`
- New SECRET_KEY in use (67 chars)

## Open
- V2-001: write 4 failing tests for ResourceMetadata, then the model

## Next action
- Check what the agent left in the repo (git status), then write the 4 tests

## Parked (time-sensitive)
- Domain/hosting lapsed: first step is back up DB + media

## Gotchas
- VS Code must use .venv (3.12)
- Never use PowerShell > to write config files (UTF-16)
- .env lives beside settings.py (merouni/merouni/)