# Public-repo sanitization — purge personal data from git history

When the user requires no sensitive/personal detail in a PUBLIC repo AND its history
(e.g. Vercel username, team slug, production domain, real email committed in docs or
as the git commit author). Verified recipe from the Sproutern session (2026-07).

## 1. Prevent: use placeholders in committed docs
Never write real values into files that get pushed to a public GitHub repo. Use:
- `<your-vercel-username>`  (not `premkumar016555`)
- `<your-team-slug>`        (not `prems-projects-27978e99`)
- `https://<project>-<team-slug>.vercel.app`  (not the real deployment URL)
- `name@bank`               (not a real UPI handle)
- If the user pastes a setup guide containing their real identifiers, scrub to
  placeholders BEFORE writing the file. Don't copy verbatim.

## 2. Cure: already-committed personal data
### a) Rewrite author/committer email across ALL commits
```bash
git filter-branch -f --env-filter '
export GIT_AUTHOR_NAME="Sproutern"
export GIT_AUTHOR_EMAIL="prem@users.noreply.github.com"
export GIT_COMMITTER_NAME="Sproutern"
export GIT_COMMITTER_EMAIL="prem@users.noreply.github.com"
' -- --all
```
(`--all` rewrites every ref. The noreply GitHub address is not personally identifying.)

### b) Expunge the old objects locally
`filter-branch` keeps a backup under `refs/original/` that still contains the old email.
Delete it and garbage-collect so the old objects can't be re-pushed:
```bash
git for-each-ref --format="%(refname)" refs/original/ | while read ref; do git update-ref -d "$ref"; done
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### c) Force-push the rewritten history
```bash
git push --force origin master
```
Force-push rewrites remote history → approval-gated. After force-push, GitHub's active
branch shows only the new HEAD; old objects are no longer reachable (GitHub purges
dangling objects within days).

## 3. Verify it's actually gone (from the REMOTE, not stale local refs)
```bash
git fetch origin
git fetch origin master:refs/remotes/origin/master   # force-refresh stale origin/master
git ls-remote origin                                  # must show only new HEAD + refs/heads/master
git log origin/master -p -S "premkumar016555@gmail.com" --oneline   # must return NOTHING
git log --all --format="%ae" | grep -c "premkumar016555@gmail.com"   # must be 0
git for-each-ref --format="%(refname) %(authoremail)" # only noreply addresses remain
```
A stale `origin/master` ref (not yet refreshed) can make `-S` searches falsely "FOUND"
— always re-fetch / force-refresh the remote ref before concluding.

## 4. Vercel env vars (server-side, NOT in repo — safe)
Real values like `NEXT_PUBLIC_SITE_URL`, `NEXT_PUBLIC_UPI_ID` live in Vercel's Dashboard
(env vars), never in committed files. Set them via `vercel env add` (see vercel-deploy-ops
skill for the per-env, no-`--scope` gotcha). `.env.local` created by `vercel link` is
gitignored — confirm with `git check-ignore .env.local`.
