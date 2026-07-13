# Fix: GitHub account-picker modal on every push

## Symptom
Every `git push`/fetch pops a "Select an account" modal listing `itsPremkumar` AND
`x-access-token`. Push cannot complete silently.

## Root cause
Git Credential Manager (helper `manager`) stored a bogus `x-access-token` identity for
github.com alongside the real `itsPremkumar` credential (which lived only in the plaintext
`~/.git-credentials`). Two identities → picker every time.

## Fix (no UI prompts)
```bash
# 1. Read the real token from the plaintext file (do NOT print it)
TOK=$(grep -oE 'https://[^:]+:[^@]+@github' "$HOME/.git-credentials" | sed -E 's#https://[^:]+:([^@]+)@.*#\1#')
echo "len: ${#TOK}"

# 2. Store itsPremkumar into GCM (suppress any GUI)
printf 'protocol=https\nhost=github.com\nusername=itsPremkumar\npassword=%s\n' "$TOK" \
  | git-credential-manager store --no-ui

# 3. Erase the bogus x-access-token entry
printf 'protocol=https\nhost=github.com\nusername=x-access-token\n' \
  | git-credential-manager erase --no-ui

# 4. Clear the plaintext duplicate so GCM is the sole store (keep a backup)
cp "$HOME/.git-credentials" "$HOME/.git-credentials.bak"
: > "$HOME/.git-credentials"

# 5. Verify only itsPremkumar remains, then test a real push
git-credential-manager github list   # -> itsPremkumar
GIT_TERMINAL_PROMPT=0 git push        # silent, no modal
```
## Notes
- `git-credential-manager` (not `git credential-manager`) is the CLI on this box.
- If a future tool re-adds `x-access-token`, the modal returns — just re-run step 3.
- The user explicitly insisted: NEVER ask for approval/token to push; just run git CLI.
