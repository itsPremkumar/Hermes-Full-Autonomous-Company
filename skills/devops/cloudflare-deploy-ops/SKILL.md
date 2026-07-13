---
name: cloudflare-deploy-ops
description: Deploy, build, verify, and operate a Next.js site on Cloudflare Workers via the OpenNext adapter (@opennextjs/cloudflare), and set up the Cloudflare MCP server. Covers the build pipeline, multi-worker split configs, auth (wrangler login OAuth token OR CLOUDFLARE_API_TOKEN), headless-deploy pitfalls (stdin is not a tty, IPv6 DNS), the diff-based resumable asset upload, the Cloudflare MCP server (run <accountId> + OAuth token reuse), and how to verify a project is "completely working". Use when deploying/building/verifying for Cloudflare, wiring up the Cloudflare MCP, or hitting Cloudflare auth/deploy errors.
---

# cloudflare-deploy-ops

Deploy, configure, and operate a Next.js site on Cloudflare Workers using the OpenNext
adapter (`@opennextjs/cloudflare`). Symmetric to `vercel-deploy-ops` but for Cloudflare's
Workers + Wrangler flow.

## Trigger conditions
- "deploy this to Cloudflare" / "build for Cloudflare Workers" / "is it connected to the Cloudflare MCP?"
- Repo contains `wrangler.jsonc` / `wrangler.toml`, `open-next.config.ts`, or `@opennextjs/cloudflare` in `package.json`.
- Verifying a Next.js project that targets Cloudflare as a "completely working" check.

## Prerequisites
- Node 18+ and the package manager the repo declares (check the `packageManager` field; many use `yarn@1.22.x`).
- Dependencies installed (see Pitfall — large installs fail intermittently, this is the usual blocker).
- A Cloudflare account. Auth is the crux — see Auth section.

## Build pipeline (typical for OpenNext-based Next.js)
`npm run build:cloudflare` (or a custom script) usually chains:
1. `next build --webpack` (often with extra env like `NEXT_PUBLIC_CLOUDFLARE_FREE_ROUTES=1`, `NEXT_PRIVATE_STANDALONE=true`).
2. `opennextjs-cloudflare build --skipNextBuild` → produces `.open-next/` (`worker.js`, `assets/`, `server-functions/`).
3. Extra steps wired in the repo: route-group generation, static-feed generation, placeholder handlers.

Multi-worker setups split routes into separate Workers via `open-next.config.ts` `functions`
plus multiple `wrangler.*.jsonc` configs (e.g. public / blog / tools / games / companies / misc).
The deploy script loops `wrangler deploy --config <each>`. A public worker binds to the
sub-workers (`BLOG_WORKER` → `sproutern-server-blog`, etc.).

## How to verify "completely working"
Run in order; each must pass before the next:
1. Install deps (resiliently — see Pitfall). You cannot verify anything without `node_modules`.
2. `npm run typecheck` (`tsc --noEmit`). **Pitfall:** `next.config.ts` often sets
   `typescript.ignoreBuildErrors: true`, so a green `next build` does NOT mean types pass.
   Run typecheck separately to catch type errors.
3. `npm run lint` (eslint).
4. `npm run test` (jest unit tests).
5. `npm run build` (plain `next build`) — proves the app compiles.
6. `npm run build:cloudflare` — proves it compiles to a valid Worker (`.open-next/` output).

## Cloudflare auth for deploy — TWO options
**Option A — API token (headless; preferred for agents):**
```
export CLOUDFLARE_API_TOKEN=<token with Workers Edit + Account-level perms>
export CLOUDFLARE_ACCOUNT_ID=<account_id>
npm run deploy          # build + wrangler deploy loop
```
Create the token at Cloudflare dashboard → My Profile → API Tokens → "Edit Cloudflare Workers" template.

**Option B — Interactive `wrangler login` (browser OAuth):**
```
npx wrangler login      # opens browser, user approves
npm run deploy
```
Persists a token in `~/.wrangler/config.json`. Requires a human at a browser.

## Cloudflare MCP server (✅ WORKS — verified)
The Cloudflare MCP server **is available and works** — `@cloudflare/mcp-server-cloudflare`
(reuses the `wrangler login` OAuth token, no separate API token needed). This corrected an
earlier (wrong) note claiming "no Cloudflare MCP is available." Setup:

1. Add a `.mcp.json` (shape in `templates/mcp-json.json`) with the `run <accountId>` subcommand.
2. `npx wrangler login` once (browser OAuth). The MCP server reads the cached token from
   `%APPDATA%\xdg.config\.wrangler\config\default.toml`, so it is already authenticated.
3. Open the project in an MCP-aware client → it picks up `.mcp.json`.

Verified live: startup logs `Config loaded: {"accountId":"✓","apiToken":"✓"}`; `tools/list`
returns ~89 tools (`worker_list`, `worker_get`, `worker_deploy`, `kv_*`, `r2_*`, `d1_*`,
`queue_*`, `ai_*`, `analytics_*`); `worker_list` returns the actual deployed Workers.
Full setup + auth detail: `references/cloudflare-mcp-setup.md`.

### Pitfall — MCP server needs `run <accountId>`, not bare package name
`npx @cloudflare/mcp-server-cloudflare` (no subcommand) throws
`Unknown command: undefined. Expected 'init' or 'run'.`
Correct invocation: `npx @cloudflare/mcp-server-cloudflare run <accountId>`.
(The `run` branch reads `CLOUDFLARE_API_TOKEN`/`CLOUDFLARE_ACCOUNT_ID` from env, else falls
back to the local wrangler OAuth token via `getAuthTokens()`.

### Pitfall — Cloudflare MCP tools have a NON-STANDARD argument envelope
When you drive the MCP server programmatically (stdio JSON-RPC), the "list/config" tools
read `request.params.input`, NOT the standard `request.params.arguments`. If you pass only
`arguments`, you get a confusing error:
```
Error: Cannot destructure property 'scriptName' of 'request.params.input' as it is undefined.
```
But the SDK's `CallToolRequestSchema` VALIDATES `params.name` + `params.arguments` — so you
must supply BOTH. The working call shape for `version_list` / `service_binding_list` /
`env_var_list` / `secret_list` is:
```json
{ "jsonrpc":"2.0", "id":11, "method":"tools/call",
  "params": {
    "name": "service_binding_list",
    "arguments": { "scriptName": "sproutern" },
    "input": { "scriptName": "sproutern" }
  }
}
```
Whereas `worker_*` tools (`worker_get`, `worker_list`) read `request.params.arguments` normally
and do NOT need `input`. Detect which style a tool wants by reading its `inputSchema.properties`
from `tools/list` — if the property is `scriptName`/`name` and the handler errors on `.input`,
add the `input` mirror.

### Pitfall — `env_var_list` is broken server-side in @cloudflare/mcp-server-cloudflare@0.2.0
It returns `Error: No number after minus sign in JSON at position 1` from the handler itself
(not your call). Non-blocking: the deployed worker uses BUILD-TIME `NEXT_PUBLIC_*` vars baked
in, not runtime env vars, so there is nothing meaningful to list. `secret_list` correctly
returns `[]`. Don't waste time debugging `env_var_list` — it's a server bug.

### Verifying the MCP connection / calling tools over stdio
A Node probe that spawns `cmd.exe /c npx …` (NOT bare `npx` — child spawn can't resolve it on
MSYS) is the reliable way to prove the connection and exercise tools. A reusable, parameterized
version lives at `scripts/mcp-ops-probe.cjs` (run with `ACCOUNT_ID=… WORKER=… ZONE_ID=… node scripts/mcp-ops-probe.cjs [workers|versions|bindings|secrets|routes]`).

### Custom domain routing via MCP (`route_create` / `route_list` / `route_delete`)
Attach a real domain (e.g. `app.example.com`) to a Worker WITHOUT migrating DNS — only if the
zone already exists in the account (often true; the domain may already resolve to Cloudflare
IPs with no worker routed yet). Verified live: `app.sproutern.com/*` → `sproutern` worker.
Full recipe, the `zones_list`-is-broken workaround (get Zone ID via the wrangler OAuth token +
REST `/zones?name=` API), and the rollback path in `references/cloudflare-custom-domain-routing.md`.
Key points:
- `route_*` tools read `request.params.input` → send the `arguments`+`input` mirror like other list tools.
- `zones_list` MCP is ALSO broken server-side in `@0.2.0` (`"[object Object]" is not valid JSON`); use the REST API with the cached OAuth token to get the Zone ID.
- A route is fully reversible (`route_delete` with `{zoneId, routeId}`) and does NOT touch DNS records.
- After routing, BOTH the custom domain and `*.workers.dev` serve the site. Wait ~30s for propagation, then `curl -I`.


- Hermes **cannot** perform interactive `wrangler login` itself (needs a browser + the user's
  Cloudflare creds). But once the user runs `wrangler login` once, the MCP server AND headless
  `wrangler deploy` both work (they reuse the cached OAuth token). So Hermes CAN deploy after
  the user authenticates, without a separate API token.
- If the user says "it was connected with the MCP" — **verify before assuming.** Grep for
  `.mcp.json` / `mcpServers` blocks in repo configs AND in `~/.claude.json` (global Claude Code
  MCP servers). Don't take "connected to MCP" at face value, but DO know the Cloudflare MCP
  server exists and is the right tool when present.
- To actually deploy from Hermes headlessly: set `CI=1` + `NODE_OPTIONS=--dns-result-order=ipv4first`
  and run `wrangler deploy --config …` directly (see headless pitfall). Optionally ask the user
  for a `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` env instead of `wrangler login`.

## Pitfall — file-writing tools double the Windows path (`C:\c\one\...`)
On this Windows/MSYS host, `write_file`/`patch` with a `/c/one/...` path silently
resolve to `C:\c\one\...` (doubled), writing the file where neither you nor the
project can find it. Symptom: a write "succeeds" but `ls`/`read_file` at the
intended path shows the file missing, and later steps read a stale file.
**Fix:** write any file under `C:\one\...` via the `terminal` heredoc
(`cat > path <<'EOF' ... EOF`) or `python - <<'PYEOF' ... PYEOF`, never via
`write_file`/`patch`. ALWAYS `ls -la` after a write to confirm it landed at the
right path; if it's at `C:\c\...`, `mv` it to `C:\one\...`. Full detail in
`references/msys-path-doubling.md`.

## Pitfall — large `yarn install` fails with ENETUNREACH
On slow/flaky networks, `yarn install --frozen-lockfile` for big trees (Next 16, React 19,
Firebase, Monaco, Lighthouse, Playwright, sharp) intermittently dies with
`AggregateError [ENETUNREACH]` while fetching platform binaries (`@next/swc-*`, `@img/sharp-*`).
The registry is reachable (curl returns 200) — it's transient parallel-connect drops.
Fix: retry with lower concurrency + long timeout:
```
yarn install --frozen-lockfile --network-concurrency 4 --network-timeout 600000
```
Progress monitoring when `| tail` buffers all output and `node_modules` stays ABSENT for many minutes:
- Cache growth = downloading: `du -sh "$(yarn cache dir)"` (e.g. `~/.yarn/cache/v6`). 1.5–2.3 GB is normal for this size.
- `node_modules` appears ONLY at the linking/extract phase — it stays ABSENT for 10–30 min even when healthy. Don't treat absence as failure.
- Confirm alive: `ps -ef | grep "yarn install"`.
Full recipe + monitoring in `references/large-yarn-install.md`.

## Pitfall — headless `wrangler deploy` dies with "stdin is not a tty" (Windows)
The repo's `scripts/deploy-cloudflare-free.mjs` (and any `spawnSync(cmd, args, {shell: isWindows})`
wrapper) launches wrangler with a non-TTY stdin under `cmd.exe`. Wrangler v4 detects the
non-TTY stdin and exits immediately with:
```
stdin is not a tty
DEPLOY_EXIT=1
```
even though `CI=1` is set and the network is fine. **The documented `npm run deploy` /
`node scripts/deploy-cloudflare-free.mjs` path therefore FAILS when run headless from the
agent terminal** — it only works in a true interactive shell (where the user ran `npm run deploy`).

Fix — bypass the spawnSync script and invoke wrangler directly per config (this is what works
headlessly). `CI=1` is the correct non-interactive switch; do NOT use `wrangler deploy --yes`
(illegal in v4.81 → `yargs validation error: Unknown argument: yes`):
```bash
export CI=1 NODE_OPTIONS="--dns-result-order=ipv4first"   # see IPv6 pitfall below
for c in cloudflare/wrangler.server-blog.jsonc \
         cloudflare/wrangler.server-tools.jsonc \
         cloudflare/wrangler.server-games.jsonc \
         cloudflare/wrangler.server-companies.jsonc \
         cloudflare/wrangler.server-misc.jsonc \
         cloudflare/wrangler.public.jsonc; do
  node_modules/.bin/wrangler deploy --config "$c"
done
```
For a single worker: `CI=1 NODE_OPTIONS="--dns-result-order=ipv4first" node_modules/.bin/wrangler deploy --config cloudflare/wrangler.public.jsonc`.
Run it via `terminal(background=true)` so it survives (the public worker uploads 600+ static
assets and takes several minutes). The 5 split workers are tiny; the public worker is the heavy one.

## Pitfall — "Unable to resolve Cloudflare's API hostname" (IPv6-only DNS in sandbox)
`wrangler` (Node `undici`) intermittently fails with `fetch failed` /
`Unable to resolve Cloudflare's API hostname (api.cloudflare.com or dash.cloudflare.com)`
even though `curl https://api.cloudflare.com` returns HTTP 403 (host reachable). Root cause:
the sandbox DNS returns **only AAAA (IPv6) records** for `api.cloudflare.com`, and Node's
fetch can't connect over IPv6 here.
Fix: force IPv4-first resolution for Node:
```bash
export NODE_OPTIONS="--dns-result-order=ipv4first"
```
Always pair this with `CI=1` (non-interactive) when deploying headlessly.

## Pitfall — full build OOMs on low-RAM machines → durable-objects corruption cycle
This is the sneakiest failure on small dev boxes (observed on a 6 GB RAM / 18 GB pagefile
Windows host). Symptom chain:

1. `npm run build:cloudflare` dies with `Fatal process out of memory: Zone` (exit 3) or
   `Next.js build worker exited with code: 2147483651`. Root cause: the app's `.next` is
   ~3 GB; the build needs a big heap (`--max-old-space-size=8192`) that exceeds PHYSICAL RAM.
   It only works if the OS pagefile can back the commit (18 GB pagefile → fine).
2. **CRITICAL:** a crashed build leaves `.open-next/.build/durable-objects/{queue,sharded-tag-cache,bucket-cache-purge}.js`
   MISSING (they're generated near the end of the OpenNext step). `public-worker.ts` imports
   them, so the NEXT `wrangler deploy` fails with:
   `X [ERROR] Could not resolve "../.open-next/.build/durable-objects/queue.js"` (3 errors).
   The site is then undeployable until a clean build regenerates those files.
3. **The `--skipNextBuild` rescue does NOT work here.** `opennextjs-cloudflare build --skipNextBuild`
   needs `.next/standalone/.next/server/pages-manifest.json`, which the OOM'd builds never
   produced. It fails with `ENOENT … pages-manifest.json`. So a partial build cannot be
   "finished" cheaply — you must get ONE complete full build.

Fix / prevention (in order):
- **NEVER run more than one `npm run build:cloudflare` at a time.** Stacked builds each grab
  8 GB and exceed commit → guaranteed OOM. Before building, kill orphans:
  `tasklist | grep node.exe` then `taskkill /F /PID <pid>`; also `rm -f .next/lock`.
- Set the heap AND keep it under what pagefile can back:
  `export NODE_OPTIONS="--dns-result-order=ipv4first --max-old-space-size=8192"` (pair with `CI=1`).
- **Verify the pagefile can actually back an 8 GB heap BEFORE building** (don't guess):
  `wmic pagefile get AllocatedBaseSize,CurrentUsage /Value` → `AllocatedBaseSize` is in MB.
  If it's ≥ ~12000 MB, an 8192 MB heap is safe (commit = RAM + pagefile). If it's small,
  the build WILL OOM even with the flag set — free RAM first or add pagefile. On the
  6 GB / 18 GB-pagefile host this was the difference between repeat OOM and a green build.
- Before building, free every non-essential `node.exe` (each stale build can hold GBs):
  `tasklist | grep -i node.exe` → `taskkill /F /PID <pid>`; also `rm -f .next/lock`.
- After a clean build, VERIFY before deploying: `ls .open-next/.build/durable-objects/` must
  list `queue.js`, `sharded-tag-cache.js`, `bucket-cache-purge.js`. If empty, the build did
  not finish — do not deploy.
- Build stages to watch in the log: `✓ Compiled successfully` → `Generating static pages (N/997)`
  → `OpenNext — Generating bundle` (this is where durable-objects are written) → `BUILD_EXIT=0`.
- If you only changed a PUBLIC ASSET (e.g. swapped `public/foo.jpg`), you still need a full
  rebuild + redeploy — Cloudflare serves assets from `.open-next/assets` uploaded at deploy
  time, and the deploy can't run while durable-objects are missing. The asset does get copied
  into `.open-next/assets` during the build's asset-population phase, but you can't ship it
  without a green full build first.

## Pitfall — public-worker asset upload is slow, diff-based, and resumable
`wrangler deploy` of the public worker uploads 600+ prerendered `.cache` files under
`.open-next/assets/cdn-cgi/_next_cache/`. On flaky networks it drops mid-upload with
`Asset upload failed. Retrying... TypeError: fetch failed` and may ultimately exit non-zero.
Key facts:
- The asset upload is **diff-based**: it only uploads NEW or MODIFIED files. A failed run leaves
  the site LIVE (worker code deployed + whatever assets made it up). Re-running the SAME
  `wrangler deploy --config cloudflare/wrangler.public.jsonc` just tops up the remaining assets
  (e.g. "Found 232 new or modified static assets to upload" → "Uploaded 162 of 162 assets").
- Wrangler auto-retries dropped uploads; a stuck pass at e.g. "105 of 622" often breaks through
  on retry, but if it loops/fails, KILL it and re-run — each re-run converges toward 100%.
- The site serves HTTP 200 even before the full asset bundle is up; verify with curl after each pass.
- Watch for the success line: `Uploaded sproutern (NNN sec)` → `Deployed sproutern triggers` →
  `https://<name>.<subdomain>.workers.dev` → `Current Version ID: <uuid>`.

## Verification checklist (after deploy)
- `npm run preview` (or `opennextjs-cloudflare preview`) to test the Worker locally.
- After `wrangler deploy`, hit the assigned `*.workers.dev` URL or custom domain.
- `wrangler tail` to stream live Worker logs/errors.

## References
- `references/msys-path-doubling.md` — on this Windows/MSYS host, `write_file`/`patch` silently write to a DOUBLED path (`C:\c\one\...`); write files via `terminal` heredoc instead, and verify every write with `ls`.
- `references/dummy-image-swap.md` — remove a real image (personal photo/logo) and replace with a PIL-generated placeholder, keep the filename so no code changes, then verify the swap is live via a PIL dimension check (not just HTTP 200).
- `references/opennext-deploy-checklist.md` — exact command sequence, required env vars, wrangler config shape.
- `references/large-yarn-install.md` — resilient install recipe + progress monitoring for huge Node projects (generic, not Cloudflare-specific).
- `references/headless-wrangler-deploy.md` — the two headless-deploy killers ("stdin is not a tty" from `shell:true` spawn wrappers; IPv6-only DNS → `NODE_OPTIONS=--dns-result-order=ipv4first`) plus the working `CI=1` per-config recipe and the diff-based resumable asset-upload pattern.
- `references/cloudflare-mcp-setup.md` — Cloudflare MCP server install, `.mcp.json` shape, OAuth-token reuse, and a stdio probe to verify the connection.
- `references/cloudflare-mcp-tool-calls.md` — the non-standard JSON-RPC argument envelope (input vs arguments), the broken env_var_list, and a working stdio probe that calls MCP tools.
- `references/cloudflare-custom-domain-routing.md` — attach a real domain to a Worker via MCP `route_create` (no DNS migration), the broken `zones_list` workaround (Zone ID via REST + wrangler OAuth token), and rollback.
- `scripts/cloudflare-mcp-ops.cjs` — KNOWN-GOOD reusable parameterized stdio probe (validated against @0.2.0). `ACCOUNT_ID=… WORKER=… ZONE_ID=… node scripts/cloudflare-mcp-ops.cjs [workers|versions|bindings|secrets|routes]`. Encodes the input/arguments envelope quirk and excludes the broken `env_var_list`.
- `templates/mcp-json.json` — copy to the project's `.mcp.json` (replace `<accountId>`).
- `references/msys-path-doubling.md` — on this Windows/MSYS host, `write_file`/`patch` silently write to a DOUBLED path (`C:\c\one\...`); write files via `terminal` heredoc instead, and verify every write with `ls`.
