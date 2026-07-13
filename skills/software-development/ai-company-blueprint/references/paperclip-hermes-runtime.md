# Paperclip + Hermes runtime (production path)

Verified live 2026-07-12 on Windows 11 (Node 22.23.1, pnpm 9.15.9, Python 3.11.15,
Docker 28.3.0 installed but daemon OFF). This is the concrete "build a Paperclip
company that employs Hermes Agent" recipe.

## Key fact (corrects an old pitfall)
Paperclip is NOT a concept/research project. `paperclipai/paperclip` is ~73.4k stars, MIT,
actively developed (3k+ commits, daily). Critically: **Paperclip's `main` branch
already bundles the Hermes adapter** — `packages/adapters/hermes` (local CLI) and
`packages/adapters/hermes-gateway` (HTTP/SSE). `server/src/adapters/registry.ts`
imports `createHermesLocalServerAdapter` / `createHermesGatewayServerAdapter` directly.
The repo the user links (`NousResearch/hermes-paperclip-adapter`) is the UPSTREAM of the
published `@paperclipai/hermes-paperclip-adapter` — it compiles standalone
(`npm install && npm run build` -> produces `dist/`), but you normally do NOT need to
build it yourself; a plain Paperclip install already gives you `hermes_local` +
`hermes_gateway` employees.

Links:
- Paperclip: https://github.com/paperclipai/paperclip  (site https://paperclip.ing, docs https://docs.paperclip.ing)
- Hermes adapter upstream: https://github.com/NousResearch/hermes-paperclip-adapter
- Hermes Agent (the employee runtime): https://github.com/NousResearch/hermes-agent

## hermes_local vs hermes_gateway
- `hermes_local`: Paperclip and Hermes on the SAME host; Paperclip shells out to the
  `hermes` CLI per heartbeat (`hermes chat -q "<task>"`). Simplest; needs Hermes on PATH.
- `hermes_gateway`: Hermes already running as an API server
  (`API_SERVER_ENABLED=true API_SERVER_KEY=... hermes gateway run --replace --accept-hooks`);
  Paperclip calls it over HTTP/SSE. Use when Hermes is remote/in Docker/behind TLS.

## Install + run (NATIVE — no Docker needed)
Paperclip uses embedded Postgres when DATABASE_URL is unset, so you can skip external DB.
```
git clone --depth 1 https://github.com/paperclipai/paperclip.git
cd paperclip
corepack enable                       # if pnpm missing; else: npm i -g pnpm@9
pnpm install                          # BIG monorepo (~1248 pkgs). Slow on weak net.
pnpm build                            # builds ui + server + plugin-sdk
cd server && pnpm start               # serves :3100, embedded Postgres
# in another terminal: cd ui && pnpm dev   (if you want the dev UI)
```
Open http://localhost:3100 -> create owner account (authenticated mode) -> New Company ->
add agent `adapterType: hermes_local`.

## Install pitfalls (learned the hard way)
- **pnpm not on corepack here** -> `npm install -g pnpm@9` (the repo pins
  `packageManager: pnpm@9.15.4`; the binary works despite the "project uses yarn" warning).
- **Monorepo install is network-bound and LONG** (10-15+ min, 1248 store packages, ~891M
  node_modules). It looks frozen (node_modules size stable, 90+ ESTABLISHED conns) during
  the resolution/download phase before linking — it is NOT hung. Be patient; do not kill
  prematurely. If it does hang in the linking/postinstall phase, retry with
  `--ignore-scripts` (the postinstall `scripts/link-plugin-dev-sdk.mjs` only symlinks the
  in-repo plugin-sdk and is safe to skip).
- **Docker daemon is OFF by default on this machine.** `docker compose up --build` cannot
  run until the user starts Docker Desktop (GUI). Prefer the NATIVE run above. The
  published image does NOT exist — it builds locally from the repo Dockerfile.

## Seed a Hermes employee via API (after server is up)
Create owner account in the UI first, copy session token, then:
```
POST /api/companies            -> {name, mission}
POST /api/companies/:id/agents -> {
  name: "Hermes Engineer", adapterType: "hermes_local", role: "CTO",
  adapterConfig: { model: "", maxIterations: 50, timeoutSec: 1800,
                   persistSession: true,
                   enabledToolsets: ["terminal","file","web","git"] } }
```
Leave `model: ""` to use Hermes's already-configured default (e.g. Nous Portal
`tencent/hy3:free`) — no separate API key needed for the agent to run.

## Reality check to carry forward
Paperclip + Hermes automates the WORK of a company (coding, research, content, QA). It
does not generate revenue by itself — still needs a product people pay for + an API budget.
Treat it as a self-running engineering/marketing team the user owns and steers, not a
money printer.