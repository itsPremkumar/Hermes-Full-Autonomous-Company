# Fix: push rejected by GitHub secret scanning

## Symptom
`git push` fails with "remote: error: GH013: Repository rule violations found ...
Push cannot contain secrets." The secret is a real API key (e.g. OpenRouter
`sk-or-v1-...`) committed in a `.bat`/`.sh`/`.env`.

## Why
GitHub secret scanning blocks any push that contains a detected credential, even in
history. Reverting the working tree is NOT enough — the key is already in the commit.

## Fix
1. **Redact the secret in the working files** to read from env only:
   - `run-server.bat`: `set OPENROUTER_API_KEY=%OPENROUTER_API_KEY%` (was a hardcoded key)
   - `watchdog.sh`: `export OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-}"`
2. **Rewrite the commits so the key is never in history.** Simplest when only one local
   commit is ahead of origin:
   ```bash
   git reset --soft origin/master          # uncommit, keep files staged
   git commit -q -m "..."                   # recommit with redacted files
   GIT_TERMINAL_PROMPT=0 git push           # now accepted
   ```
   If the key is deeper in history, use `git filter-repo` or an interactive rebase to
   purge it, then force-push (force-push only to your own repo).
3. **Verify** the key is gone: `grep -rn 'sk-or-v1-' .` returns nothing; re-push succeeds.

## Prevention
- Never hardcode keys. The OpenRouter key lives in `~/.openrouter_key` and is injected by
  the launcher into the env; it is NEVER written to a committed file.
- Add `*.key`, `.env`, `secrets/` to `.gitignore` (already done in this repo).
- Scan before pushing: `git diff --cached -U0 | grep -iE 'sk-|ghp_|pat_'` → must be empty.
