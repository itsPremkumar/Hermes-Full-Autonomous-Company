---
name: git-credential-manager-windows
description: "Windows Git Credential Manager (GCM) operations: fix the 'Select an account' x-access-token modal, store/erase github.com identities, and recover from GitHub secret-scanning push rejections. Use when git push/fetch pops an account picker, or a push is blocked for containing a secret."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [GitHub, Git, Windows, Credential-Manager, GCM, Authentication]
    related_skills: [github-auth]
---

# Git Credential Manager (Windows)

When `git config --global credential.helper` is `manager`, git uses **Git Credential
Manager (GCM)**, which stores credentials in the **Windows Credential Manager** vault —
separate from the plaintext `~/.git-credentials` file. This has two classic failure
modes the generic `github-auth` skill does NOT cover:

1. The **"Select an account" modal** on every push (dual-identity conflict).
2. **Push rejected: "Push cannot contain secrets"** (GitHub secret scanning).

## Trigger / When to use
- `git push` opens a GitHub "Select an account" dialog listing e.g. `itsPremkumar` AND
  `x-access-token`.
- A push fails with `remote: Push cannot contain secrets` and names a file/commit.
- You need to add/remove/inspect a stored GitHub credential on Windows without a GUI.

## THIS-USER rule (load-bearing — stated by the user MORE THAN ONCE, repeated across sessions)
For this user, **never ask for an approval prompt or a token to push to GitHub.** Git uses
**cached Windows Credential Manager creds** for `itspremkumar`; just run `git init/add/commit/push`
and it authenticates silently. The "Select an account" modal is a BUG (stale `x-access-token`
identity), NOT a reason to ask the user — ERASE the `x-access-token` identity (Fix A) and re-push.
Every push goes to `itspremkumar/*`. Treat any account-picker modal as a failure to fix, never as
something to surface for approval.

**This rule fired repeatedly in one session** (the modal resurfaced; the user re-iterated
"just push to my itspremkumar account, stop asking me every time"). So: if you ever start to
type a clarification like "may I push?" or "which account?" — DON'T. Push silently to
`itspremkumar`. If the modal appears, FIX IT (Fix A) and re-push; never surface it for approval.

## Diagnosis (no secrets printed)
```bash
git config --global credential.helper            # expect: manager
git-credential-manager github list               # identities GCM currently knows
grep -oE 'https://[^:]+:' "$HOME/.git-credentials"   # plaintext usernames only
```

## Fix A — the account-picker modal (dual identity)
Root cause: two github.com identities in play (a real username + a stale
`x-access-token`). GCM can't pick, so it asks every time.

Verified fix:
1. Read the real token from the plaintext file into a var (never echo it):
   ```bash
   TOK=$(grep -oE 'https://[^:]+:[^@]+@github' "$HOME/.git-credentials" \
         | sed -E 's#https://[^:]+:([^@]+)@.*#\1#')
   ```
2. Store it in GCM under the REAL username (no GUI):
   ```bash
   printf 'protocol=https\nhost=github.com\nusername=itsPremkumar\npassword=%s\n' "$TOK" \
     | git-credential-manager store --no-ui
   ```
3. Erase the bogus `x-access-token` entry:
   ```bash
   printf 'protocol=https\nhost=github.com\nusername=x-access-token\n' \
     | git-credential-manager erase --no-ui
   ```
4. Optional: clear the plaintext duplicate so GCM is the sole store (keep `.bak`):
   `cp ~/.git-credentials ~/.git-credentials.bak && : > ~/.git-credentials`
5. Verify: `git-credential-manager github list` shows ONLY `itsPremkumar`, then a real
   `git push` succeeds with NO modal. Use `GIT_TERMINAL_PROMPT=0` to fail-fast if a
   prompt would appear.

Re-occurrence: if `gh`/CI re-adds an `x-access-token`, the modal returns — re-run
step 3. `git-credential-manager github list` is the fast check.

## Fix B — "Push cannot contain secrets" rejection
GitHub secret scanning blocks the push and names the commit + path (e.g.
`run-server.bat:14` with `OPENROUTER_API_KEY=sk-...`). The key is already in a
COMMITTED commit, so a working-tree edit alone won't satisfy the scanner.

1. Scan the whole tree (exclude `.git`/`node_modules`):
   `grep -rIon "sk-[A-Za-z0-9_-]{20,}" . --exclude-dir=.git --exclude-dir=node_modules`
2. Redact the file so the key is read from env only:
   - Windows `.bat`: `set OPENROUTER_API_KEY=%OPENROUTER_API_KEY%`
   - Shell: `export OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-}"`
   - NEVER hardcode the key.
3. Rewrite history so the bad blob never reaches GitHub. **Do NOT `git reset --soft
   origin/master` naively — that drops the real local worktree.** Safe path used in
   practice (local is a git repo already tracking origin/master):
   - Back up untracked real files first (the live folder may hold actual products):
     `mkdir -p ../_live_backup && cp -rn . ../_live_backup/  # skip dirs already on disk`
   - Soft-reset local to origin (keeps working tree + index), then recommit cleanly:
     `git reset --soft origin/master && git add -A && git commit -q -m "redact secret; read key from env"` — this DROPS only the bad commits, not your files, because the tree is preserved.
   - If the repo is NOT yet tracking origin, first `git fetch origin` and point at the
     remote ref. Then `git push` (no `--force`; the reset produced a linear rewrite
     only if you had no divergent work — if you did, prefer `git rebase` or `filter-repo`).
   - **Safer alternative for a single bad commit:** `git commit --amend` the redaction
     into the existing commit, then `git push --force-with-lease`. `force-with-lease`
     refuses if the remote moved, preventing an accidental overwrite.
4. Verify the committed file is clean: fetch it via API and assert no `sk-...` present.

## Pre-push secret guard (prevent Fix B entirely)
Before `git add`, scan the working tree for secret-shaped strings so they never get
committed (and never trip Push Protection):
```bash
grep -rniE 'sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]+|github_pat_[A-Za-z0-9_]+' . \
  --exclude-dir=.git --exclude-dir=node_modules
# also catch literal key assignments in launch scripts:
grep -rniE 'OPENROUTER_API_KEY=|OPENAI_API_KEY=|ANTHROPIC_API_KEY=' . \
  --exclude-dir=.git --exclude-dir=node_modules
```
If this prints anything, redact BEFORE staging (read from env; keep the real key only in
`~/.openrouter_key` / a local env file that is gitignored). Also add the patterns to
`.gitignore` (`*.key`, `.env`, `secrets/`).

**Exact Push Protection error string** (what Fix B's rejection looks like):
`remote: error: GH013: Repository rule violations found for refs/heads/master`
`remote: secret scanning ... (e.g. OPENROUTER_API_KEY in run-server.bat)` — followed by
a GitHub bypass link. Do NOT click the bypass link for a real key; redact + rewrite
history + rotate the token instead.

## Pitfalls
- `git-credential-manager store` (not `credential store`) is the correct subcommand;
  `credential list`/`credential reject` are also under `git-credential-manager`, not
  `git-credential-manager credential ...`.
- `git-credential-manager github list` (plural `list`), NOT `accounts list`.
- The embedded `x-access-token` identity is invisible in `~/.git-credentials` — it lives
  only in the Windows vault, so always check with `git-credential-manager github list`.
- After rewriting history for a secret, also rotate the leaked token at
  github.com/settings/tokens (GitHub marks it compromised).
- **Recurrence across sessions:** the `x-access-token` modal can return if `gh` or a CI
  job re-stores that identity. When it does, the user gets annoyed at being asked again —
  re-run Fix A step 3 (`git-credential-manager erase` for `x-access-token`) without
  surfacing the modal for approval. This is the single most repeated GitHub friction for
  this user; fixing it silently is the expected behavior, not a favor.
- **Pushing is the default, not a question.** For this user, `git push` to `itspremkumar/*`
  is always authorized via cached creds. Asking "shall I push?" or "which account?" is a
  workflow error. Just push.

See `references/gcm-windows-dual-identity.md` for the full annotated procedure, the
verified run on this machine, and the THIS-USER rule: never prompt for approval/token
to push — cached creds authenticate silently, and any account-picker modal is a bug to
FIX (erase the `x-access-token` identity), not a reason to ask the user.
