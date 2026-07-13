# Dependency security audit recipe (Phase 2 — after clone)

## Node.js projects
```bash
cd /path/to/repo
# Production-only audit (transitive dev deps usually irrelevant to runtime risk)
npm audit --omit=dev --json > audit.json   # no install needed if lockfile present; else `npm install` first

# Parse to a severity table
python -c "
import json
d=json.load(open('audit.json'))
print('Summary:', d.get('metadata',{}).get('vulnerabilities'))
for name,info in d.get('vulnerabilities',{}).items():
    sev=info.get('severity')
    via=info.get('via') or []
    titles=[x.get('title') for x in via if isinstance(x,dict)]
    print(f\"{sev.upper():>8}  {name}  -> {'; '.join(t for t in titles if t)[:90]}\")
"
```

## Python projects
```bash
pip install pip-audit
pip-audit -r requirements.txt      # or: pip-audit -f json .
```

## What to report
- Group by severity (critical / high / moderate / low).
- Distinguish **direct** vs **transitive** (pulled in by a framework like Remotion/webpack).
- Note whether the app's **threat exposure** makes the vuln reachable:
  - SSRF / ReDoS / RCE matter most if the server binds `0.0.0.0` or accepts untrusted input.
  - If server binds `127.0.0.1` + sensitive routes gated by local-only middleware, runtime risk is low even if audit is red.
- Always recommend `npm audit fix` + re-pin frameworks, then **re-run typecheck/build** before declaring fixed.

## Cross-cutting security checks (read the code)
- Bind address in config (search `HOST`, `0.0.0.0`, `127.0.0.1`).
- Sensitive route middleware (search `requireLocalAccess`, `isLocalRequest`, `local-only`).
- Shell-out allowlists (search `exec(`, `spawn`, `ALLOWED_COMMANDS`, `whitelist`).
- Secrets: `git ls-files | grep -E '^\.env$'` should return nothing; `.env.example` is fine.
