# GCM Windows — full procedure + this-user rule

## Verified procedure (run on the PREM KUMAR Windows box)
1. `git config --global credential.helper` -> `manager` (GCM active)
2. `git-credential-manager github list` -> showed ONLY `x-access-token` (the bad one);
   `itsPremkumar` lived only in plaintext `~/.git-credentials`.
3. Extract real token (no echo):
   ```bash
   TOK=$(grep -oE 'https://[^:]+:[^@]+@github' "$HOME/.git-credentials" \
         | sed -E 's#https://[^:]+:([^@]+)@.*#\1#')
   ```
4. `printf 'protocol=https\nhost=github.com\nusername=itsPremkumar\npassword=%s\n' "$TOK" | git-credential-manager store --no-ui`
5. `printf 'protocol=https\nhost=github.com\nusername=x-access-token\n' | git-credential-manager erase --no-ui`
6. Cleared plaintext dup (kept `.bak`).
7. Verified: `git-credential-manager github list` -> `itsPremkumar` only; `git push`
   succeeded with NO modal. Same for `git ls-remote` on the second repo.

## THIS-USER OPERATIONAL RULE (explicit, from a correction)
The user said, repeatedly and with frustration: **"you keep asking me — just push to
itspremkumar automatically."** Encode it:
- On this machine, GitHub auth is ALREADY set up via cached creds. NEVER ask the user
  for approval, a token, or an account selection to push. Just run the git CLI
  (`git init` / `add` / `commit` / `push`) and it authenticates silently.
- If a push ever triggers the "Select an account" modal, that is a BUG to FIX via the
  GCM procedure above — not a reason to ask the user. Fix it, then push.
- User insists ALL code pushes go to the `itspremkumar` GitHub account.
- `gh` CLI is NOT installed here; use `git` CLI + `curl` with the cached token for API.

## Secrets in commits (GitHub secret scanning)
- Symptom: push rejected, `remote: Push cannot contain secrets`, names commit + path.
- The key was in a COMMITTED commit (`run-server.bat`/`watchdog.sh` had a hardcoded
  `OPENROUTER_API_KEY=sk-...`). Working-tree edit alone did NOT satisfy the scanner.
- Fix: redact file to read key from env (`%OPENROUTER_API_KEY%` / `${OPENROUTER_API_KEY:-}`),
  then `git reset --soft origin/master && git add -A && git commit && git push`.
- After, rotate the leaked token at github.com/settings/tokens.
- Rule: NEVER hardcode API keys in committed files. GitHub blocks it and that is correct.
