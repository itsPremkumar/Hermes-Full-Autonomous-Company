# Paperclip + Hermes quickstart (copy-paste)

Assumes: Node 22, pnpm 9, Hermes Agent installed (`hermes` on PATH), a Postgres service on :5432.

## 1. Clone + install + build
```bash
git clone --depth 1 https://github.com/paperclipai/paperclip
cd paperclip
pnpm install --ignore-scripts --config.node-linker=hoisted
pnpm build
```

## 2. Start server (native, external Postgres)
Set env then run tsx on the source (see templates/run-server.bat for a one-file version):
```bash
cd server
export PORT=3100 HOST=0.0.0.0 SERVE_UI=true
export BETTER_AUTH_SECRET=paperclip-dev-secret-change-me
export PAPERCLIP_DEPLOYMENT_MODE=authenticated
export PAPERCLIP_DEPLOYMENT_EXPOSURE=private
export PAPERCLIP_PUBLIC_URL=http://localhost:3100
export PAPERCLIP_HOME=/c/one/paperclip-company/data/paperclip
export PAPERCLIP_MIGRATION_AUTO_APPLY=true
export DATABASE_URL=postgres://postgres:PASSWORD@localhost:5432/paperclip
../node_modules/.bin/tsx src/index.ts
```
Server listens on :3100. (If you don't set DATABASE_URL and you're a Windows admin, embedded Postgres
will refuse to start — use the external URL above.)

## 3. First-run onboarding
Open http://localhost:3100 → create owner account → create a company → add agent:
- adapterType: `hermes_local`
- role: CTO
- adapterConfig: `{ "model": "", "maxIterations": 50, "timeoutSec": 1800, "persistSession": true,
  "enabledToolsets": ["terminal","file","web","git"] }`
Leave `model` blank to use Hermes's already-configured default (e.g. Nous Portal model).

## 4. Seed a company + Hermes employee via API (optional)
```bash
# after logging in, grab a session token from the browser DevTools
export PAPERCLIP_TOKEN=xxxx
BASE=http://localhost:3100/api
COMPANY=$(curl -s -X POST $BASE/companies -H "Authorization: Bearer $PAPERCLIP_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name":"My Co","mission":"Ship AI products that earn."}')
CID=$(echo "$COMPANY" | python -c "import sys,json;print(json.load(sys.stdin)['id'])")
curl -s -X POST $BASE/companies/$CID/agents -H "Authorization: Bearer $PAPERCLIP_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Hermes Engineer","adapterType":"hermes_local","role":"CTO",
       "adapterConfig":{"model":"","maxIterations":50,"timeoutSec":1800,
       "persistSession":true,"enabledToolsets":["terminal","file","web","git"]}}'
```
Then assign a task in the UI and the Hermes agent executes it on the next heartbeat.

## Verify the adapter is wired
```bash
ls server/node_modules/@paperclipai/hermes-paperclip-adapter   # symlink to packages/adapters/hermes
grep -l hermes server/src/adapters/registry.ts                  # imports createHermesLocalServerAdapter
```
