# CI Failure Forensics (GitHub Actions, no token / no gh)

When a CI run fails but you can't open the GitHub UI and have no `gh` CLI or
auth token (so workflow log downloads 403), recover the root cause from the
**unauthenticated REST API**. The annotations endpoint is often empty, but the
run/jobs/check-runs graph plus local reproduction is enough.

## 1. Find the failing run
```bash
curl -s "https://api.github.com/repos/<owner>/<repo>/actions/runs?per_page=10" \
 | python -c "import sys,json;[print(r['id'],r['name'],'|',r['head_sha'][:8],'|',r['conclusion']) for r in json.load(sys.stdin)['workflow_runs']]"
```
Pick the `CI` run with `conclusion: failure`. Note its `id` and `head_sha`.

## 2. Which jobs failed (and which passed)
```bash
curl -s "https://api.github.com/repos/<owner>/<repo>/actions/runs/<RUN_ID>/jobs?per_page=100" \
 | python -c "import sys,json;[print(j['name'],'->',j['conclusion']) for j in json.load(sys.stdin)['jobs']]"
```
This alone localizes the failure (e.g. `Lint & Format -> failure`,
`Unit Tests -> failure`, typecheck on node 18/20/22 all `success`).

## 3. check-runs annotations (sometimes populated)
```bash
curl -s "https://api.github.com/repos/<owner>/<repo>/commits/<HEAD_SHA>/check-runs?per_page=100" \
 | python -c "import sys,json
for c in json.load(sys.stdin).get('check_runs',[]):
    print(c['name'],'=>',c['conclusion'])
    for a in c.get('output',{}).get('annotations',[])[:8]:
        print('  ANN:',a.get('message','')[:200])"
```
If annotations are empty (common), fall back to local reproduction.

## 4. Reproduce locally — read the actual job steps
The workflow YAML tells you the exact commands. For a `Lint & Format` job that
runs `npm run lint` then `npm run format:check`, the failure is almost always
**prettier** (the `format:check` step), not eslint — eslint with only warnings
exits 0. Verify:
```bash
npm run lint          # warnings-only => exit 0
npm run format:check  # prettier => fails if ANY file unformatted
```
Fix with `npm run format` (prettier --write), then re-confirm `format:check`.

For `Unit Tests` failing while passing locally: the difference is CI's clean
`npm ci` environment. Common causes — (a) a file the tests read that is NOT
committed (check `git ls-files <path>`), (b) a test that spawns an external
binary absent in CI (grep tests for `execSync`/`spawn`/`ffmpeg`/`python`),
(c) an unclean working tree (confirm `git status --short` is empty before
trusting "passes locally").

## 5. Get the raw log when you DO have a token
```bash
curl -sL -H "Authorization: Bearer <TOKEN>" \
  "https://api.github.com/repos/<owner>/<repo>/actions/runs/<RUN_ID>/logs" -o ci.zip
# unzip, then grep the "<Job Name>.txt" for the stack trace
```
Without a token this returns a 180-byte JSON error, not a zip.

## Key lessons
- `Lint & Format` jobs that chain `eslint` + `prettier --check`: prettier is the
  usual failure, even when eslint is green. Don't assume the linter is the culprit.
- Three consecutive pushes all failing CI = pre-existing break, not your change.
- Local "passes" is not proof when `git status` is dirty or assets are uncommitted.
