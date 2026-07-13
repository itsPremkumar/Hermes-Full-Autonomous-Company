# Verify loop — exact commands to prove green (local + remote)

## Local gate (run ALL before commit)
```bash
cd /c/one/<repo>
npx prettier --check "src/**/*.ts"   && echo FORMAT_OK   || echo FORMAT_FAIL
npx eslint .                          && echo LINT_OK     || echo LINT_FAIL
npx tsc --noEmit -p tsconfig.json    && echo TS_OK       || echo TS_FAIL
npx tsx --test "src/**/*.test.ts" 2>&1 | grep -E "^# (tests|pass|fail)"
git status --short ; echo "gs_exit=$?"
```

## End-to-end functional proof
```bash
rm -rf data
npx tsx src/demo.ts 2>&1 | head -16          # ingest->score->draft, senior excluded
npx tsx src/cli.ts --import jobs.sample.json 2>&1 | head -10
```

## Remote CI is actually green (after push)
```bash
curl -s "https://api.github.com/repos/<you>/<repo>/actions/runs?per_page=2" | \
  python -c "import sys,json; d=json.load(sys.stdin); [print(r['status'], r['conclusion'], r.get('head_branch'), r.get('created_at')) for r in d.get('workflow_runs',[])]"
```
- Look for `completed success` on the MOST RECENT run. An older `failure` line is the
  previous (superseded) push — ignore it if a newer `success` exists.

## Stale "unverified" reminder
The system reminder may list changed paths even after commit+push+green CI. It is stale.
A fresh green gate + clean `git status` + `completed success` from the API is sufficient
proof. Do NOT re-edit code blindly in response to it.
