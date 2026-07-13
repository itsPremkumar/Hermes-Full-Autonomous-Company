# Diagnosing a CI failure with NO `gh` and NO token (public repos)

Used when a CI email/notification reports a red run but the machine has neither
`gh` CLI nor a GitHub PAT. You can still find out WHICH jobs failed via the
unauthenticated REST API, then fix the likely cause or ask the user to paste
the real error.

## Step-by-step
```bash
OWNER_REPO="itsPremkumar/Automated-Video-Generator"   # or extract from git remote

# 1. List recent runs; spot the CI run id + head sha
curl -s "https://api.github.com/repos/$OWNER_REPO/actions/runs?per_page=10" \
  | python -c "import sys,json; [print(r['id'], r['name'],'|',r['head_sha'][:8],'|',r['conclusion']) for r in json.load(sys.stdin)['workflow_runs'] if r['name']=='CI']"

# 2. Job conclusions for that run (tells you which job is red)
RUN_ID=<ci_run_id>
curl -s "https://api.github.com/repos/$OWNER_REPO/actions/runs/$RUN_ID/jobs?per_page=100" \
  | python -c "import sys,json; [print(j['name'],'->',j['conclusion']) for j in json.load(sys.stdin)['jobs']]"

# 3. Cross-check via check-runs on the commit
SHA=<commit_sha>
curl -s "https://api.github.com/repos/$OWNER_REPO/commits/$SHA/check-runs?per_page=100" \
  | python -c "import sys,json; [print(c['name'],'=>',c['conclusion']) for c in json.load(sys.stdin).get('check_runs',[])]"
```

## What you CAN and CANNOT get
- CAN: job names + pass/fail conclusions (enough to know e.g. "Lint & Format" and "Unit Tests" failed while typecheck/audit passed).
- CANNOT: the raw error TEXT. The `jobs`/`check-runs` `annotations` are usually empty without a token, and the log-download zip (`/actions/runs/{id}/logs`) returns an error JSON without auth. So you cannot read the exact stack trace.

## Common failure patterns to fix blind
- "Lint" job red but `eslint` is clean locally -> it also runs `prettier --check` (`format:check`). Fix: `npm run format` then verify `npm run format:check` is green. This breaks the repo on EVERY push until fixed, independent of your edits.
- "Unit Tests" red locally-green -> usually a clean `npm ci` env difference (dep version, missing committed fixture, OS path). Reproduce with the exact `npm run test:unit` command; if it passes locally you need the real log.
- If you must see the error: ask the user to paste the red text from the Actions page, or give you a PAT with `actions:read` to download the log zip.

## Gotcha
The `jobs` list endpoint sometimes returns only 1 job (e.g. a CodeQL run) when you query the wrong run id - re-confirm you grabbed the `CI` (not `pages` / `CodeQL`) run from step 1.
