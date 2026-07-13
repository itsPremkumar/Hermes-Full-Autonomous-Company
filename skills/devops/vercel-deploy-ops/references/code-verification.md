# Code-verification recipes (Vercel-deployed Next.js)

Copy-paste patterns for proving a code change is correct before/after a Vercel deploy.

## 1. Full project typecheck (background — never foreground)
`tsc --noEmit` on a large app runs 3–6 min; the `terminal()` foreground is clamped at
~60s and kills it. Background it and read the log:

```bash
cd /c/one/<project> && rm -f /tmp/tsc.log
# launch with terminal(background=true, notify_on_complete=true):
./node_modules/.bin/tsc --noEmit > /tmp/tsc.log 2>&1; echo "TSC_DONE exit=$?" >> /tmp/tsc.log
# then: cat /tmp/tsc.log   (expect: "TSC_DONE exit=0", empty above = no errors)
```
- Use `./node_modules/.bin/tsc` — `npx tsc` is intercepted by a stub.
- If `./node_modules/.bin/tsc` is missing, `node_modules` isn't installed → `yarn install` first.

## 2. ESLint on the touched files (fast pre-commit gate)
```bash
cd /c/one/<project> && ./node_modules/.bin/eslint src/app/api/embed/route.ts src/app/tools/gpa-converter/page.tsx
# exit 0 = clean
```

## 3. Live CORS verification (the real test of a header fix)
A CORS change is only proven by what production returns. Vercel/CDN CACHES the CORS
header, so a single request returns a stale value for every origin — always cache-bust:

```bash
# before fix you'd see: Access-Control-Allow-Origin: *
# after fix (reflect origin) you should see the EXACT origin sent:
curl -sI -H "Origin: https://partner-blog.com" \
  "https://www.<site>.com/api/embed?type=salary&cb=2" \
  | grep -i "access-control-allow-origin"
# expect: Access-Control-Allow-Origin: https://partner-blog.com   (NOT *)
```
Confirm with 2–3 different origins + `?cb=N` each to defeat cache. A reflected origin
that matches the request = correct; `*` = still wildcard (broken).

## 4. Deploy-status without fragile grep
`vercel ls <project>` columns don't grep cleanly. Use inspect on the deploy URL:
```bash
vercel inspect <deploy-url> 2>&1 | grep -iE "status|building|ready|error"
# reliable: "status   ● Building"  |  "status   ● Ready"
```

## 5. Fresh-evidence rule
When a verification hook re-fires "unverified" after a prior turn already verified,
re-run #1 + #2 + #3 in the current turn and paste the new output. Stale evidence
from a prior turn does not satisfy a fresh gate.
