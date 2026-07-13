---
name: paperclip-local-company
description: Stand up a local autonomous "agent company" — Paperclip (the orchestrator) + Hermes Agent employees (via the hermes_local adapter) — on Windows via the Hermes terminal. Covers the verified pnpm/tsx build, the embedded-Postgres-vs-admin trap, and how the Hermes adapter is already bundled in Paperclip main (so you do NOT hand-wire it). Use when the user wants to "run a Paperclip company", "hire a Hermes agent in Paperclip", "build the agent-company stack", or references paperclipai/paperclip + NousResearch/hermes-paperclip-adapter.
---

# Paperclip + Hermes local "agent company"

Paperclip (`paperclipai/paperclip`) is an open-source orchestration platform for running teams of
AI agents as a "company": companies, org chart, goals, budgets, tickets, heartbeats. Hermes Agent
(`NousResearch/hermes-agent`) is a 30+ tool agent. The **hermes_local** adapter lets Paperclip shell
out to the `hermes` CLI as a managed employee.

## Mental model (how the pieces connect)
```
Paperclip (company/orchestrator, Node server + React UI)
   └─ on each heartbeat, calls the hermes_local adapter's execute()
        └─ runs:  hermes chat -q "<task>"   (Hermes uses its 30+ tools)
   └─ results + cost flow back; sessions persist across heartbeats
```
"OpenClaw is an employee, Paperclip is the company." Any agent that can receive a heartbeat can be
hired. Paperclip also supports Claude, Codex, Cursor, Gemini, Grok, OpenCode, Pi, and HTTP adapters.

## KEY FACT — the Hermes adapter is ALREADY bundled
Paperclip's `main` branch **ships** the Hermes adapter:
- `packages/adapters/hermes` + `packages/adapters/hermes-gateway` in the monorepo
- `server/src/adapters/registry.ts` imports `createHermesLocalServerAdapter` / `createHermesGatewayServerAdapter`
  from `@paperclipai/hermes-paperclip-adapter`
- The standalone `NousResearch/hermes-paperclip-adapter` repo is the **upstream source** (published as
  `@paperclipai/hermes-paperclip-adapter`). A normal `pnpm install` of Paperclip already gives you
  `hermes_local` + `hermes_gateway` adapters. **Do NOT hand-patch the registries** — just add a
  `hermes_local` agent after first run.

Two adapter modes:
- `hermes_local` — Paperclip starts `hermes chat` as a child process (same trusted host). Needs `hermes` on PATH.
- `hermes_gateway` — Paperclip calls an already-running Hermes API server over HTTP/SSE.
  Start Hermes gateway first: `API_SERVER_ENABLED=true API_SERVER_KEY=<secret> hermes gateway run --replace --accept-hooks`

## Prerequisites (this machine had all of these)
- Node 22+, pnpm (install via `npm i -g pnpm@9` if missing; corepack is flaky here)
- Hermes Agent installed (`hermes` on PATH). Windows native install:
  `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`
- At least one LLM key for Hermes (in `~/.hermes/.env`, or via Nous Portal).
- **Model auto-detect trap**: leaving the agent `model` blank defaults to `"auto"`,
  which passes `-m auto` — Hermes then auto-detects a model instead of using its
  configured default. Always set `model` explicitly.

## Verified Windows build + run (native, no Docker needed)
Docker path exists (docker-compose.yml in repo) but the **Docker daemon is often OFF** on this host —
prefer the native run below. Paperclip uses embedded Postgres by default, but embedded Postgres
**refuses to run under a Windows admin account** (see Pitfalls). Use an external Postgres via
`DATABASE_URL` (a full PostgreSQL is frequently already installed as a Windows service on :5432 — point
Paperclip at it).

Step-by-step:
1. Clone: `git clone https://github.com/paperclipai/paperclip` (depth 1 is fine).
2. Install deps. The default pnpm linker **stalls on the MSYS git-bash shell** during linking — use
   hoisted linker (see Pitfalls). From the repo root:
   `pnpm install --ignore-scripts --config.node-linker=hoisted`
3. Build all workspace packages: `pnpm build` (tsc passes with 0 errors on a clean tree).
4. Start the server with **tsx on the source** (NOT `node dist/index.js` — see Pitfalls):
   `../node_modules/.bin/tsx src/index.ts`  (run from `server/`)
   Pass env (see env block / templates/run-server.bat). With `DATABASE_URL` set to your external
   Postgres, it migrates and listens on PORT (default 3100).
5. Open `http://localhost:3100` → create owner account → create company → add agent `hermes_local`.
   Or script it via the REST API (see references/quickstart.md).

## Server env (set before launch)
```
PORT=3100
HOST=0.0.0.0
SERVE_UI=true
BETTER_AUTH_SECRET=<any-string, dev-only>
PAPERCLIP_DEPLOYMENT_MODE=authenticated      # first run creates an owner account
PAPERCLIP_DEPLOYMENT_EXPOSURE=private
PAPERCLIP_PUBLIC_URL=http://localhost:3100
PAPERCLIP_HOME=<writable dir>
PAPERCLIP_MIGRATION_AUTO_APPLY=true
DATABASE_URL=postgres://<user>:<pass>@localhost:5432/paperclip   # REQUIRED on Windows admin accounts
```

## Creating a Hermes employee (agent payload)
```json
POST /api/companies/:companyId/agents
{
  "name": "Hermes Engineer",
  "adapterType": "hermes_local",
  "role": "cto",
  "adapterConfig": {
    "model": "tencent/hy3:free",
    "provider": "openrouter",
    "maxIterations": 50,
    "timeoutSec": 1800,
    "persistSession": false,
    "enabledToolsets": ["terminal","file","web"],
    "checkpoints": false,
    "quiet": true
  }
}
```

### Post-creation steps (agent won't work without these)
1. **Enable heartbeat** — new agents boot with heartbeat **disabled**:
   ```bash
   PATCH /api/agents/<AGENT_ID>
   {"runtimeConfig": {"heartbeat": {"enabled": true, "maxConcurrentRuns": 3}}}
   ```
2. **Create task-bridge key** — required for autonomous issue execution:
   ```bash
   POST /api/agents/<AGENT_ID>/keys
   {"scope": {"kind": "task_bridge", "projectId": "<COMPANY_ID>"}, "name": "bridge"}
   ```
   The `projectId` field is mandatory. Returns a `pcp_...` token auto-injected as
   `PAPERCLIP_BRIDGE_API_KEY` into the Hermes subprocess.
3. **Reset session** after any config change:
   ```bash
   POST /api/agents/<AGENT_ID>/runtime-state/reset-session
   {}  # empty body is required
   ```

### Model & provider notes
- Valid `hermes_local` providers: `auto`, `openrouter`, `nous`, `openai-codex`,
  `copilot`, `copilot-acp`, `anthropic`, `huggingface`, `zai`, `kimi-coding`,
  `minimax`, `minimax-cn`, `kilocode`. **`opencode` is NOT valid.**
- Empty model → defaults to `"auto"` → passed as `-m auto` (Hermes ignores its
  configured default and auto-detects). Always set model explicitly.
- Known working free models: `tencent/hy3:free` (via openrouter, needs
  `OPENROUTER_API_KEY` in server env), `deepseek-v4-flash-free` (via auto,
  needs `OPENCODE_ZEN_API_KEY` in `~/.hermes/.env`).

## Continuous autonomous operation (the lifecycle after setup)

Once the Hermes agent is hired and the heartbeat is enabled, the company runs itself — but
with specific handoff patterns the founder/board must understand.

### Issue lifecycle
1. **Create an issue** (via UI or API) with a clear description.
2. If you set `assigneeAgentId` on creation, Paperclip **immediately starts a heartbeat
   run** for that agent — no wait for the next tick. If you leave assignee blank, the
   issue sits in `todo` until assigned.
3. **Agent picks it up** on the next available heartbeat. It reads the issue, creates
   Python scripts, executes work (terminal commands, file edits, API calls to Paperclip).
4. **Agent produces deliverables** — artifacts uploaded as issue attachments, work products
   created, issue status updated.
5. **Agent creates child issues** for follow-up work (e.g., PRE-3 → PRE-5 through PRE-8).
6. **Agent sets issue to `done` or `in_review`** and exits cleanly.

### Critical pattern: agent does NOT self-assign, but the SERVER auto-triggers
The Hermes CTO agent creates child issues but **never assigns itself to them** — it leaves
them as `todo` with no assignee, expecting the board/founder to confirm. This is an agent
behavior, NOT a server limitation.

**However**, if YOU (the cron/founder) create an issue via API with `assigneeAgentId` set,
Paperclip **immediately auto-starts a heartbeat run** for it. The server respects
`maxConcurrentRuns` (default 3) — if the agent is at capacity, new runs queue until a slot
opens.

To keep the pipeline moving:
- **Via cron:** set up a 15-minute cron job that assigns unassigned `todo` issues to the
  agent AND creates follow-up child issues for `done` items (see "Cron job for continuous
  development" below).
- **Via API:** when creating child issues for completed work, set `assigneeAgentId` to
  the agent's UUID and Paperclip auto-starts execution.
- **Manually:** after each completed cycle, assign new issues via UI or API.

### Heartbeat reliability
Each agent run starts a `hermes chat` subprocess. The model response time determines run
duration (~3–4 min for a full issue cycle). If the subprocess is lost (killed/crashes), the
run stays in "running" state in Paperclip. **Fix:**
```bash
# Extract cookie value (curl -b cj.txt fails on git-bash — MSYS path issue)
TOKEN=$(grep 'paperclip-default.session_token' /c/one/paperclip-company/cj.txt | awk '{print $NF}')

# Cancel the stale run (needs Cookie + Origin + Referer)
curl -s -X POST "http://localhost:3100/api/heartbeat-runs/<RUN_ID>/cancel" \
  -H "Cookie: paperclip-default.session_token=$TOKEN" \
  -H "Origin: http://localhost:3100" \
  -H "Referer: http://localhost:3100/"

# Reset session and re-trigger
curl -s -X POST "http://localhost:3100/api/agents/<AGENT_ID>/runtime-state/reset-session" \
  -H "Cookie: paperclip-default.session_token=$TOKEN" \
  -H "Origin: http://localhost:3100" \
  -H "Content-Type: application/json" -d '{}'

curl -s -X POST "http://localhost:3100/api/agents/<AGENT_ID>/heartbeat/invoke" \
  -H "Cookie: paperclip-default.session_token=$TOKEN" \
  -H "Origin: http://localhost:3100" \
  -H "Referer: http://localhost:3100/"
```
**Heartbeat invoke header note:** the `/heartbeat/invoke` endpoint checks for a trusted
browser origin and returns `"Board mutation requires trusted browser origin"` without
browser-emulating headers. You need `Cookie` + `Origin` + `Referer` (or
`X-Requested-By: paperclip` instead of `Referer`). The 3-header set (Cookie + Origin +
Referer) is the simplest reliable combination. Using `-b cj.txt` alone fails on git-bash
because MSYS path rewriting interferes with curl's `-b` flag — always prefer the cookie-header
approach shown above.

### Diagnosing a stuck heartbeat (before cancelling)
Before cancelling a stale run, check whether the agent actually produced output or just
went silent. Each run's stdout/stderr is persisted as a per-run ndjson log:

```bash
# Find the most recent run logs by modification time
ls -lt /c/one/paperclip-company/data/paperclip/instances/default/data/run-logs/<COMPANY_ID>/<AGENT_ID>/*.ndjson

# Check the last 20 lines — was the agent making progress?
tail -20 <latest-run>.ndjson

# Each line: {"ts":"...","stream":"stdout|stderr","chunk":"...","seq":N}
# Key signals the agent is still alive:
#   - Recent timestamps (within the last few minutes)
#   - Tool call output (code changes, API responses, file diffs)
#   - `[hermes]` lifecycle messages
# Key signals the agent stalled:
#   - Last timestamp hours ago with no new lines added
#   - `RateLimitError [HTTP 429]` or similar API errors
#   - `[hermes] Exit code: 0` or `[hermes] Exit code: 1` — process exited cleanly but Paperclip didn't notice
```

If the run log shows a clean exit code (`Exit code: 0`), the agent finished the work but
Paperclip didn't update the run status — cancel + reset + retrigger. If it shows rate-limit
errors or a last-output timestamp hours ago, the subprocess died and needs the same fix.

**Corrective/handoff run silently dying (PRE-7 pattern).** When a prior run times out or
exits, the system may auto-create a *corrective* or *handoff* run (`correctiveRunId` in the
issue's `successfulRunHandoff` points to the new run). These corrective runs sometimes die
before producing any meaningful output. Diagnostic:

- The new run's `.ndjson` log has only 3–4 startup lines (workspace fallback warning,
  `Warning: could not read agent instructions file`, `Starting Hermes Agent`,
  `Resuming session: ...`) — nothing more, even after several minutes.
- The log file is ~700–800 bytes (startup noise only).
- The API may briefly show `activeRun: { status: "running" }` but later reflect
  `activeRun: null` as the server cleans up the ghost.
- The agent's own endpoint (`GET /api/agents/:id`) shows `status: "idle"` because the
  dead run was never formally cancelled.

**Fix:** invoke a fresh heartbeat (see the `heartbeat/invoke` call above). No need to cancel
the dead run — it was never truly alive. The fresh invoke creates a new run that picks up the
issue from scratch. Use the cookie-header approach (not `-b cj.txt`) to sidestep the MSYS
path issue on git-bash.

### Zombie server process (Node alive, port not serving)
Paperclip's Node process can appear in the process list while the HTTP server is not serving
requests. This happens when the process hangs internally without fully terminating:
- `ps -W | grep node` shows node.exe alive with a PID
- `curl -s --max-time 5 http://localhost:3100/api/health` returns connection refused (exit code 7)
- `netstat -ano | grep 3100` returns nothing — port is unbound
- The process is a zombie: occupies memory and a PID slot but does no work

**Detection:** Always test the health endpoint, not just the process list. A running Node
process with a health endpoint that doesn't respond IS a zombie.

**Recovery sequence when the server is a zombie:**
1. Kill the stale Node process by PID: `kill -9 <PID>` (git-bash) or `taskkill /F /PID <PID>` (cmd)
2. Verify port is free: `netstat -ano | grep 3100` returns nothing, curl still fails
3. Start the server (run-server.bat or tsx command)
4. Wait for health endpoint to return `{"status":"ok"}`
5. Reset the agent's runtime session (stale after crash):
   `POST /api/agents/<ID>/runtime-state/reset-session`
6. Invoke heartbeat: `POST /api/agents/<ID>/heartbeat/invoke`
7. Verify dispatch: check run-logs directory for new `.ndjson` files within 60 seconds

**Cron-safe approach:** Before any agent-state operations, probe `/api/health`. If it fails
but the process is alive, recover the server first — don't attempt heartbeat operations on
a zombie instance.

### Heartbeat invoke queue vs. scheduler tick
Calling `POST /api/agents/<ID>/heartbeat/invoke` returns a run with status `"queued"`. However,
the agent's 30-second heartbeat tick scheduler is independent — it dispatches runs for the
highest-priority issues automatically. When `maxConcurrentRuns` (default 3) is saturated, the
queued invoke stays `queued` until a slot opens, while the tick continues dispatching new runs.

**Immediate agent status transition.** Calling `/heartbeat/invoke` changes the agent's `status`
from `"idle"` to `"running"` instantly, even though no actual run has started yet
(`activeRunId` remains `null`). This `"running"` status means "nudged / has accepted work" —
the agent is in a transitional state between idle and executing. Do NOT treat `status: "running"`
as proof that a run is actively executing; cross-reference with `activeRunId` and the
run-logs directory.

**Don't rely on the queued run status to determine if the agent is working.**
Instead, check the run-logs directory for new files:
```bash
ls -lt /c/one/paperclip-company/data/paperclip/instances/default/data/run-logs/<COMPANY_ID>/<AGENT_ID>/*.ndjson | head -5
```
If new log files appear with recent modification timestamps, the scheduler is healthy and
the agent is being dispatched. The queued invoke is a safety-net trigger, not the primary
dispatch mechanism.

**Practical implication for cron jobs:** After invoking heartbeat, don't poll the run status
endpoint — check for new run-log files instead. If new logs appear within 60 seconds, the
scheduler is working and the agent is active. The agent's `status` field will already be
`"running"` from the invoke nudge, so use `lastHeartbeatAt` + run-log presence (not just
`status`) to determine whether the agent is truly executing work.

**Pro tip:** run logs use UUID filenames (not issue IDs). Cross-reference by checking the
`PAPERCLIP_TASK_ID` or `issueId` in the context snapshot within the log's first JSON line
to identify which issue a run was serving.

### Board mutations need Cookie + Origin (and sometimes Referer/X-Requested-By) headers
PATCH/DELETE endpoints on issues and agents require `Origin: http://localhost:3100` AND a valid
session cookie — otherwise you get `"Board mutation requires trusted browser origin"`. Always
pass the cookie via the `Cookie` header (not `-b`, which fails on git-bash):
```bash
TOKEN=$(grep 'paperclip-default.session_token' /c/one/paperclip-company/cj.txt | awk '{print $NF}')
curl -s -X PATCH "http://localhost:3100/api/issues/<ID>" \
  -H "Cookie: paperclip-default.session_token=$TOKEN" \
  -H "Origin: http://localhost:3100" \
  -H "Content-Type: application/json" \
  -H "X-Requested-By: paperclip" \
  -d '{"status":"done"}'
```
**Important:** `Origin` alone may still return 403 in some setups. Always include
`X-Requested-By: paperclip` (or `Referer: http://localhost:3100/`) alongside `Origin` for
reliable mutations. This was verified: `Origin` alone → 403, adding `X-Requested-By: paperclip`
→ 200.

### Session cookie survival depends on database engine
With **external PostgreSQL** (`DATABASE_URL` set, the recommended setup for Windows admin
accounts), Better Auth sessions are stored in the database and **survive server restarts**.
The same cookie works before and after restart — no re-authentication needed. Verified:
server stopped at 07:37, restarted at 07:54, same cookie accepted immediately.

With **embedded Postgres** (no `DATABASE_URL`, default), the ephemeral DB is created fresh on
each server start, so session data is lost. Re-authentication is required:
```bash
TOKEN=$(grep 'paperclip-default.session_token' /c/one/paperclip-company/cj.txt | awk '{print $NF}')
curl -s -X POST "http://localhost:3100/api/auth/sign-in/email" \
  -H "Content-Type: application/json" \
  -d '{"email":"prem@local.dev","password":"LocalDevPass123!"}' \
  -H "Cookie: paperclip-default.session_token=$TOKEN" -H "Origin: http://localhost:3100"
```
(Use `-c cj.txt` on the first sign-in to save the cookie to the file, then extract the token
for subsequent requests with the `grep | awk` pattern.)

### PATCH adapterConfig normalization trap
When you PATCH an agent's `adapterConfig`, the `normalizeMediatedAdapterConfigForPersistence`
function overwrites `model` and `provider` with values from the Hermes config detection.
PATCH response may **show** your values but they are **not persisted**. The server always
resolves model/provider from the actual Hermes config.yaml. Fix: set these in Hermes
config directly, or set `replaceAdapterConfig: true` on the PATCH to bypass the merge logic.

## Cron job for continuous development

Set up a periodic cron job that monitors the issue pipeline and advances work so the
founder doesn't need to assign issues manually:

```bash
hermes cron create --name "company-revenue-pulse" --schedule "every 15m" \
  --prompt "Check the Paperclip company and advance revenue work.
- Fetch issues via GET /api/companies/{companyId}/issues
- For 'done' issues, create follow-up child issues if appropriate
- For unassigned 'todo'/'backlog' issues, assign to the agent and set in_progress.
- If agent is idle and work exists, invoke heartbeat: POST /api/agents/{id}/heartbeat/invoke" \
  --enabled-toolsets terminal,file,web
```

The long-running agent heartbeat loop (30s) processes issues one at a time, while the
15-minute cron handles pipeline management (assigning, creating follow-ups, triggering).

The full operational checklist for each cron execution — stale-run detection, session
reset, follow-up creation, timeout unblocking, and dispatch verification — is documented
in `references/cron-pipeline-workflow.md`. Load this file before writing or modifying
the cron prompt. The "Data Processing Mechanics for Cron Jobs" section in that file details the
JSON pipe-breakage workaround (multi-line descriptions), PATCH 400 diagnosis, and run-log summary
scanning for next-step recommendations — essential implementation patterns for cron execution.

## Maintaining the knowledge base (GitHub as single source of truth)

The company is built locally at `/c/one/paperclip-company`, but a local-only company drifts and is
fragile. Establish GitHub as the canonical store and treat every document/prompt/tool as versioned
knowledge. Full verified commands + pitfalls: `references/github-knowledge-base.md`.

### Triggering principle
"If it isn't committed, it isn't done." Push the real, running company (products, income engine,
finance ledger, `hermes-paperclip-adapter` source, COMPANY_PLAN, status snapshot) — not just a
constitution doc. Create two repos: `Hermes-Full-Autonomous-Company` (the OS) and
`Hermes-Prompt-Library` (versioned prompts).

### Prompt-consolidation discipline (this is a class of work, not a one-off)
Users will hand you several overlapping "master prompt / constitution" drafts. Do NOT push them all
as-is. Instead:
1. **Adopt the draft whose structure matches the REAL stack** as the spine. Here that was
   `hermes-master-operating-prompt.md` (Paperclip + OpenClaw + budget caps + human-in-the-loop).
2. **Drop fictional-stack assumptions.** Drafts routinely list tools you do NOT run (n8n, Mem0,
   CrewAI, AutoGen, standalone "OmniRouter", OpenHands). The actual stack is Paperclip + Hermes +
   OpenClaw + `hermes-paperclip-adapter` + OmniRoute→OpenRouter + Automated-Video-Generator.
3. **Consolidate into ONE versioned constitution** (`CONSTITUTION.md` = master operating prompt v2.0).
   Archive superseded drafts in `prompts/archive/` — never delete (they ARE the version history).
4. **Never build on unverified "leaked system prompts"** (e.g. "Claude Fable 5"). Prefer
   officially-published guidance.
5. **Embed the low-RAM memory-discipline rule** explicitly (this box runs at ~70–150 MB free):
   close tools after use, exclude `node_modules` from pushes, clean up staging dirs.

### Governance contract to preserve (Section 0 of the constitution)
Money has a human in the loop (budget caps + approval gates), no binding commitments without
sign-off, no deceptive claims, compliance is mandatory, self-improvement = better skills/docs not
unsupervised self-editing of the charter. Any change to Section 0 is a human-reviewed decision.

### THIS-USER auto-push rule (load-bearing — corrected by the user more than once)
The user stated explicitly and repeatedly: **push ALL code automatically to his `itspremkumar`
GitHub account via git CLI — never ask for approval and never ask for a token.** Git uses
**cached Windows Credential Manager creds** for `itspremkumar`, so just run `git init/add/commit/push`
and it authenticates silently. If a "Select an account" modal appears, that is a BUG (a stale
`x-access-token` identity in GCM) — FIX it per `git-credential-manager-windows`, do NOT ask the
user. `gh` CLI is not installed; use git CLI + `curl` with the cached token for any GitHub API call.
Treat every push as going to `itspremkumar/*`.

### OS-spec implementation pattern (reviewer/architecture-suggestion → repo artifacts)
When the user (or a reviewer) hands a list of architecture improvements for the company, do NOT
paste them into the constitution as prose. Implement them as **concrete, auditable repo artifacts**
— this is the "repository = operating system" principle: the constitution defines agent *behavior*;
the repo defines the *system*. Verified recipe (the v2.0 → v3.0 bump):
1. For each suggestion, create a real file: `docs/<subsystem>.md` (spec),
   `knowledge-base/<x>.md` (state/metrics), `agents/registry.md` (agent interface),
   `tools/repo-index.md` (catalog).
2. Wire the *behavioral* ones into `autonomy-loop.py` (the 24/7 cron brain) — e.g. a **confidence
   gate** (≥75 proceed+validate, 50–74 consult second model, <50 escalate to human) and a **benchmark
   logger** that appends a row to `knowledge-base/benchmarks.md` every tick (RAM, success/failure
   rate, revenue, automation coverage).
3. Add a `CONSTITUTION.md` Section 17 table mapping each subsystem → its real file, so the spec is auditable. Bump the version (v2.0→v3.0).
4. Reject "invent a new service" suggestions (n8n/Mem0/CrewAI event-bus) — map the subsystem onto
   what ACTUALLY runs (Paperclip + cron + GitHub + Hermes memory). Don't bloat a low-RAM box.
5. Run an ad-hoc verifier (`hermes-verify-*.py`) against the changed loop; fix any bug it finds;
   then commit + push (auto, per the THIS-USER rule above).

## PITFALLS (all hit and solved this session)
- **pnpm install "hangs" on MSYS/git-bash**: node_modules size freezes, no `@paperclipai` symlinks
  appear, yet network is active. Cause: the default `isolated` linker does slow/hung hardlink+symlink
  resolution under MSYS. **Fix: `pnpm install --ignore-scripts --config.node-linker=hoisted`.** Hoisted
  links in seconds. (The `--ignore-scripts` skips the harmless `link-plugin-dev-sdk` postinstall; you
  then `pnpm build` explicitly.)
- **`node dist/index.js` fails** with `ERR_MODULE_NOT_FOUND` (e.g. can't find
  `packages/db/src/client.js`). Cause: workspace packages declare `exports: { ".": "./src/index.ts" }`
  — they resolve to **source .ts**, not built `dist`. **Fix: run via tsx** —
  `../node_modules/.bin/tsx src/index.ts` from `server/`. tsx loads `.ts` exports fine.
- **Do NOT call tsx by its absolute `.pnpm` path.** The MSYS shell rewrites `C:\one\...` → `C:\c\one\...`
  and node then reports `Cannot find module 'C:\c\one\...'`. Use the **relative shim**
  `../node_modules/.bin/tsx` (works) or a `.bat` that uses the native `C:\one\...` `.bin\tsx` path.
- **Embedded Postgres refuses admin accounts on Windows**: error
  *"Execution of PostgreSQL by a user with administrative permissions is not permitted."* Cause: the
  interactive user is an admin. **Fix: set `DATABASE_URL` to an external PostgreSQL.** A full PostgreSQL
  17 is often already installed as a Windows service on :5432 (runs under a service account, not the
  admin user) — just `createdb paperclip` (or let Paperclip migrate) and point `DATABASE_URL` at it.
- **Adapter already bundled** — don't edit `server/src/adapters/registry.ts` or `ui/src/adapters/*`.
  Adding a `hermes_local` agent via UI/API is all that's needed.
- **Docker daemon off** — skip compose; use the native tsx run above.
- **Heartbeat disabled by default** — agent stays "idle" and never executes work.
  Must set `runtimeConfig.heartbeat.enabled: true` explicitly after creation.
- **Empty model → `-m auto`** — blank model field defaults to `"auto"` which passes
  `-m auto`. Hermes with `-m auto` ignores its configured `config.yaml` default and
  auto-selects a model (often falls back to OpenRouter free pool → 429 rate limits).
  Always set model explicitly.
- **Task-bridge key needs `projectId`** — `scope.kind: "task_bridge"` without
  `scope.projectId` returns `"task_bridge keys require at least one project or parent
  issue boundary"`. Pass the company UUID as `projectId`.
- **`opencode` is not a valid `hermes_local` provider** — the adapter's
  `VALID_PROVIDERS` list (from `constants.ts`) does not include it. Setting it causes
  fallthrough to model-prefix inference or `"auto"`. Valid providers: `auto`, `openrouter`,
  `nous`, `openai-codex`, `copilot`, `copilot-acp`, `anthropic`, `huggingface`, `zai`,
  `kimi-coding`, `minimax`, `minimax-cn`, `kilocode`.
- **Session cookie expires on server restart** — Better Auth invalidates sessions.
  Re-login via `POST /api/auth/sign-in/email` after each restart. Use
  `-H "Origin: http://localhost:3100"` for mutation endpoints.
- **PATCH adapterConfig normalization overwrites model/provider** — the
  `normalizeMediatedAdapterConfigForPersistence` function reads Hermes config and
  overwrites `model` and `provider`. PATCH response may show your values but they
  are not persisted. Set values in Hermes `config.yaml` directly, or pass
  `replaceAdapterConfig: true` in the PATCH body.
- **Agent does NOT self-assign child issues** — the CTO agent creates follow-up
  issues but leaves them unassigned. Founder must assign them manually or via cron.
- **Board mutations need `Origin: http://localhost:3100`** — PATCH/DELETE on issues
  and agents return `"Board mutation requires trusted browser origin"` without it.
  Always pass the cookie via the `Cookie` header (not `-b`, which fails on git-bash)
  plus `Origin` and `Referer` or `X-Requested-By` headers.
- **Heartbeat runs can get stuck** — if the Hermes subprocess is killed/crashes,
  Paperclip keeps the run in "running" state. Cancel the stale run and reset the
  agent session before re-triggering.
- **Done issue auto-dispatches a fresh run (PRE-18 pattern)** — an issue marked
  `status: done` can still receive a new heartbeat run if Paperclip's scheduler
  dispatches it after the issue was already completed. The run's `startedAt`
  timestamp is *after* the issue's `completedAt`. The agent loads the issue,
  sees it's done, and exits immediately — producing a run log with only 2–3
  lines (startup warnings + "Starting Hermes Agent") and no tool output. This
  run occupies a `maxConcurrentRuns` slot indefinitely until cancelled.
  **Diagnostic:** issue has `activeRun` with `status:running` AND the run log
  is ~700–800 bytes (only startup messages). **Fix:** cancel the stale run
  and reset the agent session.
- **Zombie server process (Node alive, port not serving)** — the Paperclip Node
  process can appear in the process list but the HTTP server is not actually bound
  to port 3100. `ps -W | grep node` shows it alive but `curl localhost:3100/api/health`
  returns connection refused (exit code 7). The process is hung internally — a zombie.
  **Fix:** kill the stale Node PID (`kill -9 <PID>`), verify the port is free
  (`netstat -ano | grep 3100` returns nothing), restart the server, then reset agent
  runtime session and re-trigger heartbeat. Always test the health endpoint before
  acting on agent state — process-list presence alone is misleading.
- **AGENTS.md instructions file missing** — the heartbeat run log starts with
  `Warning: could not read agent instructions file "C:\\...\\AGENTS.md": ENOENT`.
  The agent runs without company-specific context, producing generic output that
  does not reference the company playbook, budget caps, or operating principles.
  **Fix:** create the instructions directory and a `templates/AGENTS.md`-style
  instructions file at the expected path:
  `<PAPERCLIP_HOME>/instances/default/companies/<CID>/agents/<AGENT_ID>/instructions/AGENTS.md`.
  Load the `templates/AGENTS.md` template from this skill, fill placeholders,
  and write it. After creating the file, reset the agent session:
  `POST /api/agents/<ID>/runtime-state/reset-session`.
- **Agent "soft error" state (status: error, reasons null)** — after repeated run
  failures, the agent status changes to `"error"` but `errorReason` and
  `pauseReason` remain null. This is the stuck state: the agent is not working,
  not paused, and not healthy. The recovery action system may still auto-wake
  the agent (via `wake_owner` policy), but each wake fails until the root cause
  (model provider, API key, connection) is fixed. **Diagnosis:** check the
  recovery action `attemptCount` — if climbing rapidly (>3), the agent is in a
  failure loop. **Fix:** resolve the provider issue, then reset session.
  Do NOT invoke heartbeats on a soft-error agent — they fail and contribute to
  the loop. See `references/agent-run-patterns.md` for detailed diagnosis.
- **Heartbeat invoke can stay "queued" indefinitely** — calling
  `POST /api/agents/<ID>/heartbeat/invoke` returns a `queued` run, but if the
  scheduler's 30-second tick is already at `maxConcurrentRuns` capacity, the
  queue does not drain until a slot opens. The agent may still be working via the
  tick scheduler. Verify agent activity by checking the run-logs directory for
  new `.ndjson` files, not by polling the queued run's status endpoint.
- **MSYS rewrites `-b /c/...` paths for curl** — in git-bash, `curl -b /c/one/.../cj.txt`
  fails with `failed to open cookie file` because MSYS rewrites `/c/` but curl's `-b`
  flag doesn't go through the same path expansion as file arguments. **Fix options** (try
  in order of reliability):
  1. Use the native Windows path with quotes: `--cookie C:/one/paperclip-company/cj.txt`
  2. Keep cookie files in the current directory and use the relative `-b cj.txt`.
  3. **Fallback (always works):** pass the raw cookie value via the `Cookie` header, which
     bypasses both MSYS path rewriting and Netscape cookie-file format issues:
     ```bash
     TOKEN=$(grep 'paperclip-default.session_token' /c/one/paperclip-company/cj.txt | awk '{print $NF}')
     curl -s -H "Cookie: paperclip-default.session_token=$TOKEN" "http://localhost:3100/api/..."
     ```
     The token is the last whitespace-delimited field on the cookie-file line. This approach
     works for both GET reads and POST mutations (pair with `Origin` header for writes) and
     sidesteps all filesystem-path and cookie-format pitfalls at once.
- **Cookie file domain format matters** — `curl -b file.txt` parses Netscape cookie files.
  If the domain line has `HttpOnly_localhost` (written by some auth flows), curl skips it
  because the domain `HttpOnly_localhost` doesn't match the request to `localhost`. **Fix:**
  the domain in the cookie file must be just `localhost` (no prefix). The `watchdog-cj.txt`
  has the correct format (`localhost`); `cj.txt` from a fresh sign-in may have the wrong
  format (`#HttpOnly_localhost`). Regenerate with `-c` flag, or edit the file to remove
  `#HttpOnly_` from the domain.
- **Issue creation auto-starts heartbeat runs** — POST a new issue with `assigneeAgentId`
  set, and Paperclip IMMEDIATELY fans out a heartbeat run. No 30s wait. This is distinct
  from the "agent doesn't self-assign" behavior: the AGENT doesn't assign, but the SYSTEM
  auto-triggers when you set assignee on creation. At `maxConcurrentRuns` capacity (default 3),
  new issues queue. Monitor active runs via the `activeRun` field in issue responses.
- **Issue creation needs Origin + Content-Type headers** — even though GET reads work with
  just the cookie, POSTing a new issue requires BOTH headers:
  ```bash
  TOKEN=$(grep 'paperclip-default.session_token' /c/one/paperclip-company/cj.txt | awk '{print $NF}')
  curl -s -H "Cookie: paperclip-default.session_token=$TOKEN" -H "Origin: http://localhost:3100" \
    -H "Content-Type: application/json" \
    -X POST -d '{"title":"...","assigneeAgentId":"<AGENT_ID>"}' \
    http://localhost:3100/api/companies/<CID>/issues
  ```
  Without `Origin`, you get `Board mutation requires trusted browser origin`.
- **Local JSON snapshots go stale** — `iss.json`, `company-status.json`, and other files
  written to the repo by previous agent runs are snapshots from when they were generated,
  not live state. This session found `company-status.json` was ~19 hours stale (generated
  2026-07-12T14:51Z vs actual-time 2026-07-13T03:35Z). The API at
  `GET /api/companies/<CID>/issues` is the authoritative live source. Always prefer the
  API over local JSON files for current issue status. Use local files only for historical
  comparison or when the server is down.

## Reality check to set with the user
Paperclip automates the *work* of a company; it does not generate revenue by itself. You still need a
product people pay for and an API budget. Treat it as a self-running engineering/marketing team you own
and steer. Agents won't run until a model key is present for Hermes.

## References & templates
- `references/agent-activity-detection.md` — Multi-signal decision tree for determining whether the Hermes Engineer is actually working, idle, or stuck. Cross-references agent endpoint, per-issue activeRun fields, run-log directory, and ndjson parsing to avoid false negatives from the agent-level activeRunId being null. Load before running the pipeline cron job or deciding whether to invoke a heartbeat.
- `references/agent-run-patterns.md` — Run lifecycle states, failure mode diagnosis (connection error vs timeout vs success), recovery action loop detection, agent status values ("error" with null errorReason = soft error), when to invoke heartbeat vs not, run-log-to-issue cross-referencing, and the "done issue still dispatched" pattern. Load when diagnosing agent non-responsiveness or deciding whether to intervene in a recovery loop.
- `references/cron-pipeline-workflow.md` — Cron job operational checklist: stale-run detection, session reset, follow-up creation for done items, timeout unblocking, dispatch verification, AND data-processing mechanics (JSON pipe-breakage workaround, PATCH 400 diagnosis, run-log summary scanning for next-step recommendations, run-ID cross-referencing). Load before writing or modifying the cron prompt for the revenue pulse job.
- `references/issue-automation-workflow.md` — Programmatic issue automation API: exact curl commands for creating issues, assigning to agents (triggering autonomous execution), batch-sprint launches, and troubleshooting. Shows how to bypass the "agent doesn't self-assign" limitation. Verified on a 7-agent Paperclip instance. Load before automating Paperclip work pipelines.
- `references/windows-build-pitfalls.md` — deeper repro recipes for each pitfall above.
- `references/quickstart.md` — copy-paste command sequence + REST seed script.
- `references/continuous-development-loop.md` — keeping the agent company running: issue lifecycle, cron setup for pipeline management, revenue model sequencing (PRE-3 → PRE-5–PRE-8 pattern), founder handoff gates, cookie expiry recovery, board mutation Origin header.
- `references/github-knowledge-base.md` — pushing the local company to GitHub as single source of truth: repo creation via cached creds, curated copy (exclude node_modules), `master` default branch, write_file native-path bug, prompt-consolidation + reality-match rules.
- `templates/run-server.bat` — known-good Windows launcher (native paths, tsx shim, env block).
- `templates/AGENTS.md` — Standard agent instructions template with mission, priorities, active issues, work rules, and retry discipline. Fill in the placeholders ({AGENT_NAME}, {COMPANY_NAME}, {MISSION}, etc.) and write to `<PAPERCLIP_HOME>/instances/default/companies/<CID>/agents/<AGENT_ID>/instructions/AGENTS.md`. Load before creating or updating agent instructions for a company.
