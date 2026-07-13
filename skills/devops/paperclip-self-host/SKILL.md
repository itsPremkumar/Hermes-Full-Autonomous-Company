---
name: paperclip-self-host
description: Run Paperclip (paperclipai/paperclip) with the Hermes Agent adapter on a Windows dev machine NATIVELY (no Docker) — install the pnpm monorepo, build, create the Postgres DB, and start the server via tsx. Documents the Windows/MSYS/pnpm pitfalls that otherwise silently stall the install or crash startup with confusing errors.
---

# Paperclip self-hosting (Windows, native, with Hermes)

Paperclip (`paperclipai/paperclip`, MIT, ~73k stars) is an open-source orchestration
platform for teams of AI agents — "if OpenClaw is an employee, Paperclip is the company."
This skill covers running it on a Windows dev box **without Docker**, with the Hermes
Agent adapter wired in so you can hire a Hermes "employee" (CTO/engineer).

## Key fact: Hermes is already bundled — do NOT hand-wire it

Paperclip's `main` branch **ships** the Hermes adapter:
- `packages/adapters/hermes` (local CLI) and `packages/adapters/hermes-gateway` (HTTP/SSE)
- `server/src/adapters/registry.ts` imports `createHermesLocalServerAdapter()` and
  `createHermesGatewayServerAdapter()` from `@paperclipai/hermes-paperclip-adapter`.

The upstream source is `NousResearch/hermes-paperclip-adapter` (published as
`@paperclipai/hermes-paperclip-adapter`, v0.3.x). A normal Paperclip install already
gives you the `hermes_local` and `hermes_gateway` adapter types. You do **not** manually
wire the adapter. Cloning the NousResearch repo builds standalone (`npm install && npm run build`
→ `dist/`) but is only needed if you want to patch the adapter itself.

- `hermes_local`: Paperclip shells out to the `hermes` CLI as a child process each heartbeat.
  Requires `hermes` on PATH for the user running Paperclip.
- `hermes_gateway`: Paperclip calls an already-running Hermes API server over HTTP/SSE
  (start Hermes with `API_SERVER_ENABLED=true API_SERVER_KEY=<secret> hermes gateway run --replace`).

## Environment (verified on the build host)

Node 22.x, pnpm 9.x (install via `npm install -g pnpm@9`; `corepack enable` failed on that
host), Python 3.11, git. Hermes Agent installed natively (Windows). PostgreSQL 17 present as
a Windows service on `:5432` — **embedded Postgres will NOT run under an admin Windows account**
(see Pitfalls), so use the external one.

## Procedure

1. **Clone + install**
   ```
   git clone https://github.com/paperclipai/paperclip && cd paperclip
   pnpm install --ignore-scripts --config.node-linker=hoisted
   ```
   (The `--ignore-scripts` + `hoisted` flags avoid the MSYS link stall — see Pitfalls.)

2. **Build**
   ```
   pnpm build
   ```
   Runs `tsc` across all workspace packages; expect **0 errors**. The default `server` build
   script is `tsc && mkdir -p dist/onboarding-assets dist/built-ins && cp -R src/onboarding-assets/. dist/onboarding-assets/ && cp -R src/built-ins/. dist/built-ins/`.
   If tsc passed but those two dirs are missing under `server/dist/`, create them:
   `mkdir -p server/dist/onboarding-assets server/dist/built-ins && cp -R server/src/onboarding-assets/. server/dist/onboarding-assets/ && cp -R server/src/built-ins/. server/dist/built-ins/`.

3. **Create the Postgres role + database** (see `scripts/setup-pg-db.bat` and
   `references/windows-pnpm-pitfalls.md`). Then set:
   ```
   DATABASE_URL=postgres://<role>:<pw>@localhost:5432/<db>
   ```

4. **Start the server via `tsx`** — NOT `node dist/index.js` (see Pitfall). Use the launcher
   bat (`templates/run-server.bat`) invoked as:
   ```
   cmd.exe /c "C:/abs/path/run-server.bat"
   ```
   Do NOT invoke node/tsx with absolute Windows paths through the git-bash shell (MSYS path
   mangling — Pitfall). Inside the bat, native `C:\` paths are correct, and the
   `../node_modules/.bin/tsx` shim works.

5. **Bootstrap the instance + company + agent.** The UI path is documented below, but
   **every step is also a REST call** — see `references/paperclip-api-bootstrap.md` for the
   full scriptable flow (sign-up → `POST /api/bootstrap/claim` with an `Origin` header →
   `POST /api/companies` → `POST /api/companies/:id/agents` → heartbeat invoke). Gotchas
   captured there: mutation endpoints need `Origin: http://localhost:3100` (else
   "trusted browser origin" error); `role` is a **lowercase** enum (`cto` not `CTO`);
   `PATCH /api/issues/:id` is root-mounted (not under `/companies/:id`); the task-bridge key
   (`POST /api/agents/:id/keys` with `scope.kind=task_bridge`) is **required for autonomous
   execution** — without it Hermes boots and waits for a task ID instead of pulling the issue.

   Browser path: `GET /api/health` → `{"status":"ok"}`; open `http://localhost:3100` →
   create owner account (first run) → create Company → add agent with `adapterType=hermes_local`.

6. **Post-setup agent management.** After bootstrap, agents need manual post-setup:
   `references/paperclip-agent-management.md` covers re-authentication after server restart,
   enabling heartbeat (disabled by default), creating the task-bridge key with its required
   `projectId` field, resetting stale agent sessions after config changes, and the valid
   `hermes_local` provider list. Without these steps the agent stays idle or fails with
   confusing errors.

## OpenRouter API key: env passthrough to the adapter

Paperclip passes `OPENROUTER_API_KEY` to the Hermes adapter via the
`ADAPTER_ENV_PASSTHROUGH` mechanism in `server/src/services/plugin-loader.ts`:

```typescript
const ADAPTER_ENV_PASSTHROUGH = [
  "ANTHROPIC_API_KEY",
  "OPENAI_API_KEY",
  "GOOGLE_API_KEY",
  "GEMINI_API_KEY",
  "OPENROUTER_API_KEY",
];
```

These keys are injected into the worker env when the Hermes adapter runs. To make
them available:

- **Persistent (survives reboots):** `setx OPENROUTER_API_KEY "sk-or-v1-..."` in
  a terminal (takes effect in new shells only).
- **Per-launcher:** add `set OPENROUTER_API_KEY=sk-or-v1-...` to the
  `run-server.bat` before the `tsx` line.
- **Current shell (bash):** `export OPENROUTER_API_KEY="sk-or-v1-..."` before
  starting the server.

If a free OpenRouter model (`tencent/hy3:free`, etc.) previously returned empty
responses on the shared pool, adding a personal key gives it a dedicated rate
limit and it starts returning real content. The key is read by the
`@paperclipai/hermes-paperclip-adapter` → Hermes CLI → OpenRouter SDK chain.

## 24/7 Operation (Hermes cron watchdog)

To keep Paperclip running 24/7 without a dedicated terminal, set up a no_agent
Hermes cron job that polls the health endpoint and restarts the server if it goes
down. This survives terminal closes, reboots (if Hermes Desktop is running), and
transient crashes.

### Setup

1. Place `templates/watchdog.sh` into `~/.hermes/scripts/watchdog.sh`.
2. Customize `PAPERCLIP_HEALTH_URL` and `PAPERCLIP_SERVER_BAT` at the top of
   the script, or rely on defaults.
3. Create the cron job (set `no_agent=true` so no LLM token is burned per tick):
   ```bash
   # From Hermes CLI or via cronjob tool:
   cronjob(action='create',
     name='paperclip-watchdog',
     schedule='5m',
     script='watchdog.sh',
     no_agent=true)
   ```

The cron job runs every 5 minutes, does a single `curl` check, and only
restarts when the server is unresponsive. No tokens consumed, no LLM overhead.

### Windows-native alternative (more robust on a dev box)

If Hermes Desktop is not guaranteed to be running, use **Windows Task Scheduler**
instead — `scripts/watchdog.py` is a stdlib-only, zero-LLM watchdog that does the
same health-check + auto-restart + idle-nudge, plus it re-authenticates each
cycle (so the session never expires) and writes `company-status.json` /
`company-report.md`. Register it with two `schtasks /Create` calls (every 5 min
**and** `/SC ONSTART`) and a `PaperclipServer` `/SC ONSTART` task with
`/DELAY 0001:00`. Full recipe + auth/run-output gotchas in
`references/continuous-operation.md`. Prefer this when you want the company to
survive a reboot without a logged-in Hermes session.

### What the watchdog covers

- **Server crash recovery:** if Paperclip exits for any reason, it's back
  within 5 minutes.
- **Agent heartbeat continuity:** Paperclip's own agent loop runs on a timer;
  as long as the server is up, agents self-dispatch on their heartbeat.
- **Zero maintenance:** the cron output is saved locally; errors surface
  through Hermes cron list.

### Autonomous agent execution checklist

For an agent to work hands-off:
1. **Heartbeat enabled** — `PATCH /api/agents/:id` with
   `runtimeConfig: { heartbeat: { enabled: true } }`.
2. **Task-bridge key exists** — `POST /api/agents/:id/keys` with
   `{ scope: { kind: "task_bridge", projectId: "<COMPANY_ID>" } }`.
3. **An issue is assigned** to the agent (`PATCH /api/issues/:id` with
   `assigneeAgentId`).
4. **Server stays up** — covered by the watchdog above.

### Known agent behavior limits

**The agent autonomy gap.** A Hermes agent with a task-bridge key can:
- Complete an assigned issue ✅
- Create child / follow-on issues ✅
- Upload artifacts and post comments ✅
- Set its own issue to `done` ✅

What it **cannot** do autonomously:
- **Self-assign child issues it creates** ❌ — child issues are always left
  with `assigneeAgentId: null`, stalling the pipeline until a bridge mechanism
  fills the gap.
- **Set issue status via board-mutation endpoints from a non-browser origin**
  (needs `Origin: http://localhost:3100` + valid session cookie).
- **Interact with `ask_user_questions` / `request_confirmation`** — the
  interaction endpoint has strict schema requirements that the agent's POST
  attempts often violate (4xx).

**Bridging the autonomy gap.** To keep the company developing without manual
stepping between issues:

1. **Cron-based auto-assigner** — create a Hermes cron job (every 15m) that
   queries unassigned `todo` issues and PATCHes them to the agent. The agent's
   heartbeat then picks them up on the next cycle.
2. **Parent-issue pattern** — attach "after completing this, create child issues
   AND leave them `in_progress` assigned to yourself" in the AC. The agent
   follows this some of the time, but unreliably — the cron fallback is the
   safety net.
3. **Manual batch** — PATCH all child issues to the agent in one call, then
   trigger `heartbeat/invoke`. The agent works through them sequentially.

**PATCH persistence quirk for model/provider.** `PATCH /api/agents/:id` values
for `adapterConfig.model` and `adapterConfig.provider` are silently overwritten
by `normalizeMediatedAdapterConfigForPersistence` in the server route handler.
The stored config always reflects what was set at agent creation. Workarounds:
- Create a new agent with the desired config if you must change it.
- Accept the creation-time config if it works — the PATCH failure is cosmetic.
- Alternatively, modify the normalize function in the server source and restart.

### Building a full autonomous company (C-suite pattern, verified end-to-end)

Beyond one agent, you can stand up a complete org. Verified working layout for a
zero-cost company (all `hermes_local`, model `tencent/hy3:free` via OpenRouter, heartbeat on):

| Agent | role enum | Mandate |
|-------|-----------|---------|
| Hermes CEO | `ceo` | Strategy, roadmap, cross-agent coordination |
| Hermes CTO | `cto` | Product engineering, infra |
| Hermes CMO | `cmo` | Brand, GTM, pricing, outreach |
| Hermes COO | `devops` | Delivery ops, SLAs, client workflows |
| Hermes CFO | `cfo` | Unit economics, burn=$0 guard, revenue ledger |
| Hermes Head of Product | `pm` | Roadmap specs, feedback loop |
| Hermes QA | `qa` | Test plans, release gates |

Steps that actually worked (one session):
1. Create each agent via `POST /api/companies/:id/agents` with `runtimeConfig.heartbeat.enabled:true`
   and the `adapterConfig` block above. Do them ONE AT A TIME — batching 5 in one shell
   loop hit transient errors; the loop also scrambled the `agentId`→epic mapping (bash
   associative-array ordering), so assign epics from an authoritative `identifier→id` map
   written to a JSON file, not inline shell vars.
2. Create a **project** (`POST /api/companies/:id/projects`) for the product build.
3. Create **epic issues** (`POST .../issues` with `projectId`, `assignedAgentId`, AND
   `status:"todo"` together — see assignment gotchas in `references/paperclip-api-bootstrap.md`).
4. Two-step activate each epic: PATCH `assigneeAgentId`+`status:"todo"`, then PATCH
   `status:"in_progress"` (in_progress requires an assignee or it 422s).
5. Each agent self-dispatches its epic via heartbeat. Agents produce **artifact work-products**
   (Paperclip attachments) — retrieve them: `GET /api/issues/:id/work-products` → each item's
   `metadata.attachmentId` → `GET /api/attachments/<id>/content`. Download these to local files
   so the human has deliverables (see `scripts/fetch_assets.py` pattern in `references/continuous-operation.md`).

**Detecting "is the agent running" without a runs-list endpoint.** This build's
`/api/agents/:id/heartbeat-runs?page=1&limit=3` route returns 404 (not exposed). Use the
agent's own `status` field instead: `status=="running"` means a heartbeat is active; combine
with `lastHeartbeatAt` to decide whether to nudge. The watchdog nudge guard: nudge only when
`status != "running"` AND `(now - lastHeartbeatAt) > IDLE_NUDGE_SECS` AND pending work exists.
This prevents the double-nudge problem (manual invoke while auto-heartbeat is on cancels runs).

See `references/continuous-operation.md` for the Task Scheduler recipe, Set-Cookie auth
gotcha, artifact retrieval, and the revenue-asset pattern.

## Cron-tick decision checklist (exact order of operations for scheduled checks)

When executing a periodic check (every 5–30 min) to advance the company pipeline,
run these steps in order. This is the cron-friendly concise sequence; for full
diagnostics (stale runs, timeout analysis, zombie server) see the sections below.

1. **Fetch all issues** — `GET /api/companies/:companyId/issues`. This is the
   authoritative live source. Ignore stale local JSON snapshots.

2. **Audit done issues** — For each issue with `status: "done"`:
   - Read its completion note (run log's last ~10 lines) for stated next steps.
   - Check for existing child issues (same `parentId`).
   - If agent mentioned unfinished follow-up work but no child issue tracks it →
     `POST` a new child issue with `assigneeAgentId` + `status: "todo"` so the
     server auto-triggers a heartbeat on creation.
   - If follow-up is already captured and in_progress/done → skip.

3. **Adopt orphan todo/backlog issues** — For each issue with `status: "todo"`
   or `"backlog"` AND `assigneeAgentId: null`:
   - Assign to the appropriate agent via `PATCH /api/issues/:id` with
     `assigneeAgentId` + `status: "todo"`. The heartbeat system auto-advances
     to `in_progress` on the next tick — no second PATCH needed.

4. **Check agent liveness** — `GET /api/agents/:agentId`:
   - If `status: "running"` AND issues assigned to it have `activeRun` objects
     with recent `startedAt` → agent is actively working; **skip heartbeat**.
   - If `status: "idle"` AND pending work exists → invoke heartbeat
     (`POST /api/agents/:id/heartbeat/invoke` with `Origin: http://localhost:3100`).
   - If `status: "running"` but NO issue has an active run and the run-log
     directory has no new files in the last hour → the agent has a stale
     "running" marker. Cancel the ghost run, reset session, re-trigger.

5. **Cross-check run logs for genuine execution** — `ls -lt` the agent's
   run-log directory. If the most recent `.ndjson` has a modification timestamp
   within the last heartbeat interval and >3 lines of output, the agent is
   genuinely executing work regardless of API status.

6. **Report** — Summarize what was done, what was already running, and what
   needs human attention (founder-gated steps: npm publish, domain registration,
   LinkedIn account creation, Gumroad publish — none an agent can do).

## Operations monitoring — issue lifecycle tracking & agent progress

Beyond basic agent liveness (`status` + `lastHeartbeatAt`), you need to track whether
agents are actually making progress on assigned work. This section covers inspecting
issue state transitions, reading run logs to confirm real work, and auditing done
issues for required follow-up.

### Why API-based liveness is not enough

`agent.status == "running"` only means a heartbeat process is active — it does NOT
mean the agent is making progress. An agent can be "running" while its run is
rate-limited, timed out, or stuck producing no output. Use the file-system run logs
and issue lifecycle data to determine actual work.

### Run log analysis (real-time, file-system approach)

The `stdoutExcerpt` returned by `GET /api/heartbeat-runs/<id>` stays `""` until the
run exits. For real-time progress, read the raw `.ndjson` log files:

```
RUN_LOGS = <PAPERCLIP_HOME>/data/paperclip/instances/default/data/run-logs/<COMPANY_ID>/<AGENT_ID>/
```

Each `.ndjson` file is a run's streaming output — **one JSON object per line** with keys
`ts` (ISO timestamp), `stream` (`stdout`/`stderr`), and `chunk` (the text payload).
`tail`/`head` on the raw file show JSON, not clean prose. To extract readable lines:
```bash
python -c "import sys,json; [print(json.loads(l).get('chunk','').rstrip()) for l in sys.stdin if l.strip()]" < <run_id>.ndjson
```
Some runs end with `"Exit code: 0"` / `"timed out: true"` inside the `chunk`; others
end with agent-init lines like `[hermes] Session: ...`. Check them with:
- `ls -lt $RUN_LOGS | head -5` — most recent runs first
- parse `head -3 <run_id>.ndjson` — init lines name the workspace/issue the run targets
- parse `tail -5 <run_id>.ndjson` — last activity (exit code, timeout, or agent init)
- `wc -l <run_id>.ndjson` — more lines = more work done; a 4-line file with just init + timeout
  means the agent produced nothing useful (PRE-7 pattern)

### Issue lifecycle states

| State | Meaning for operations |
|-------|----------------------|
| `todo` | Assigned but never started. Heartbeat auto-advances to in_progress on next cycle. |
| `in_progress` | Has (or had) an active run. Check the run log to confirm actual work was done. |
| `in_review` | Agent completed work, awaiting review. May or may not have a current run. |
| `done` | Completion timestamp tells recency. Check if follow-up child issues exist. |
| `blocked` | Run failed/timed out without auto-retry. Needs triage. PRE-7 hit this: video production timed out with zero output → status set to `blocked`. |
| `backlog` | Not yet assigned. Will NOT auto-advance until moved to `todo`. |

Key auto-advancement behaviors (observed in production):
- **Auto-`in_progress`**: Issues with `status: "todo"` and an assignee get
  auto-advanced to `in_progress` on the next heartbeat cycle. PRE-34 transitioned
  from `todo` to `in_progress` between two API polls without manual PATCH.
- **Auto-respawn after timeout**: When a run times out at 1800s (the default
  `timeoutSec`), a new run is automatically created for the same issue.
  Run e978e29a timed out → run bc5e04ff spawned for the same issue (PRE-34).
  One timeout is not permanent failure; repeated timeouts suggest the task needs
  smaller decomposition or a longer timeout.
- **No auto-spawn for `done`**: The agent creates child issues but leaves them
  unassigned (see "Bridging the autonomy gap" above). Done issues require a
  manual audit (see below).

### Done-issue follow-up audit

1. `GET /api/companies/:id/issues` → filter `status == "done"`
2. For each done issue:
   - Read the completion note (last ~10 lines of the issue's most recent run log)
     for stated next steps
   - Check if child issues exist via `parentId` linking back
   - If follow-up exists AND is assigned/in_progress → no action needed
   - If follow-up exists but is unassigned → assign via cron bridge or manual PATCH
   - If follow-up is mentioned but NOT tracked as an issue → create a child issue
3. Example from this session: PRE-12 (monetization site) noted "register domain,
   LinkedIn page" as next steps. Checked PRE-5 (showcase repo) — already captured
   LinkedIn scope. No new child needed.

### Cron-based auto-assigner for unassigned todos

The autonomy gap (child issues left unassigned) can be bridged with a Hermes cron
job (every 5-15 minutes) that queries unassigned `todo` issues and PATCHes them
to the appropriate agent. Without this, each completed issue creates orphans that
stall the pipeline.

Full operational patterns and session-specific observations in
`references/operations-monitoring.md`.

## Omniroute install (DEFAULT linker, NOT hoisted — hoisted misses pre-built dist/)

**CRITICAL: do NOT use `--config.node-linker=hoisted` for omniroot.** The
hoisted linker skips extraction of the pre-built `dist/server.js` (tarball
entries under `dist/` are pruned), producing a package that can only boot to
`✖ Server not found at: ...dist/server.js`. Use the default isolated linker so
the published bundle files land in the right place.

Omniroute (`omniroute` npm package v3.8.46, by diegosouzapw) is a free AI
gateway with 160+ providers, auto-fallback, and an OpenAI-compatible endpoint.
Install it into a throwaway project:

```bash
mkdir omniroute && cd omniroute
echo '{"name":"omniroute-local","private":true,"dependencies":{"omniroute":"*"}}' > package.json
pnpm install --ignore-scripts
```

The `--ignore-scripts` flag avoids the postinstall step that stalls on MSYS
(paperclip-style) and saves time. The pre-built bundle including
`dist/server.js` is extracted correctly with the default linker.

On a slow network, add a `.npmrc`:
```
fetch-retries=20
fetch-retry-factor=2
fetch-retry-mintimeout=1000
fetch-retry-maxtimeout=60000
fetch-timeout=120000
network-concurrency=4
```

Start via:
```bat
node node_modules\\omniroute\\bin\\omniroute.mjs
```
(port 20128 by default, configurable via `PORT` or `OMNIROUTE_PORT` env vars.)

### Hoisted-linker startup fix (Windows — only if you used the wrong linker)

If you used `--config.node-linker=hoisted` for omniroute (the wrong linker —
see above), two issues appear:

1. **`package.json` missing from the package root** — hoisted linker strips
   it. Create a stub: `{"name":"omniroute","version":"3.8.46"}`
2. **`dist/server.js` missing** — the entire pre-built bundle was never
   extracted. The only fix is to reinstall with the default linker
   (`pnpm install --ignore-scripts`, no hoisted flag).

## Set env vars permanently (Windows)

For env vars that must survive reboots (API keys, etc.), use `setx`:
```cmd
setx OPENROUTER_API_KEY "sk-or-v1-..."
```
This writes to the user-level registry — new terminal shells pick it up, but the
current shell doesn't. Combine with `export` in bash or `set` in a `.bat` for the
current session.

Paperclip's `run-server.bat` or Omniroute's `start-omniroute.bat` are the right
places to set per-launcher env vars (add `set VAR=value` before the node command).

## Hiring a Hermes agent (adapterConfig)

```json
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
    "enabledToolsets": ["terminal","file","web"]
  }
}
```
Gotchas (full detail in `references/hermes-free-model-config.md` and
`references/paperclip-agent-management.md`):
- **Provider prefix is NOT repeated in `model`**: `provider:"openrouter"` + `model:"openrouter/tencent/hy3:free"` → HTTP 400. Use `model:"tencent/hy3:free"`. Same for `nous`.
- **`persistSession` must be `false`** for scheduled agent work. `true` resumes a stale
  session and Hermes prints "provide the task" instead of executing the issue.
- **`role` is a fixed lowercase enum** — invalid values are rejected with `invalid_enum_value`.
  Valid: `ceo|cto|cmo|cfo|security|engineer|designer|pm|qa|devops|researcher|general`.
  There is **no `coo` and no `product`** — map them: COO → `devops` (ops/delivery fits),
  Head of Product → `pm`. An invalid role returns a `None` agent (creation looks like it
  failed) — re-create with a valid enum value.
- **Free models are rate-limited / capability-limited.** OpenRouter's shared free pool 429s
  the large models and the small ones that return content are too weak to follow the
  execution contract. For reliable autonomy use a dedicated free key (Groq/Cerebras/NVIDIA NIM)
  or a fallback gateway (OmniRoute). A working free alternative is `deepseek-v4-flash-free`
  via OpenCode Zen (`provider: "auto"`). Debug via `GET /api/heartbeat-runs/<RUN_ID>` → `stdoutExcerpt`.
- **`git` is not a valid Hermes toolset** (it's part of terminal/file) — invalid entries just warn.
- **Autonomous execution needs a task-bridge key** (`POST /api/agents/:id/keys`,
  `scope.kind=task_bridge` with `projectId` = company ID). Without it the agent
  never self-dispatches the issue. The `projectId` field is **required**.
- **Heartbeat is disabled by default** on new agents. Enable it via
  `PATCH /api/agents/:id` with `runtimeConfig: { heartbeat: { enabled: true } }`.
- **`opencode` is NOT a valid `hermes_local` provider.** Valid providers are:
  `auto`, `openrouter`, `nous`, `openai-codex`, `copilot`, `copilot-acp`,
  `anthropic`, `huggingface`, `zai`, `kimi-coding`, `minimax`, `minimax-cn`,
  `kilocode`. Use `"auto"` to let Hermes use its own config.yaml.

## Pitfalls (Windows / MSYS / pnpm)

Full failure modes + exact commands in `references/windows-pnpm-pitfalls.md`. Summary:

- **Auth via `-b cj.txt` (Netscape cookie file) returns `Unauthorized`** even on plain
  `GET` calls. This build's `/api/.../issues` (and other GETs) rejected the Netscape
  cookie file but accepted a raw header: `curl -H "Cookie: <name>=<value>" ...`.
  Workaround when `-b file` fails: extract the `session_token` value from `cj.txt` and
  pass it as a literal `Cookie:` header. (Mutating endpoints additionally require
  `Origin: http://localhost:3100`, per below.)
- **Job/cron briefs assert STALE issue state — re-fetch before mutating.** A scheduled
  task brief may claim e.g. "all 4 issues are `in_progress`" while the live API shows
  `in_review` / `blocked` / `done`. Never PATCH status/assignee to match the brief.
  Always `GET /api/companies/:id/issues` first, read each target's true
  `status` + `assigneeAgentId`, and act on *actual* state. If a brief's premise is
  wrong, report the divergence and proceed from real state (no destructive changes).

- **pnpm install stalls during linking on git-bash** — Symptom: 1248 packages resolved/reused,
  `added 0` frozen for minutes, no `.modules.yaml`. Fix: `pnpm install --ignore-scripts
  --config.node-linker=hoisted`.
- **MSYS path mangling** — passing `C:\one\...` to `node` through bash becomes `C:\c\one\...`
  (extra `c`) → MODULE_NOT_FOUND. Fix: run everything via `cmd.exe /c "C:/path/bat.bat"`;
  inside bats use native `C:\` paths. The `.bin/tsx` shim works; direct
  `node node_modules/.pnpm/tsx@.../cli.mjs` fails.
- **`node dist/index.js` crashes** with `ERR_MODULE_NOT_FOUND` for `packages/db/src/client.js`
  because workspace `exports` point at `./src/index.ts`. Fix: run `tsx src/index.ts`.
- **Embedded PostgreSQL refuses a Windows admin account** ("Execution of PostgreSQL by a user
  with administrative permissions is not permitted"). Fix: external Postgres via `DATABASE_URL`.
- **Creating the PG role/db without the postgres password** — pg_hba is `scram-sha-256`. On
  Windows psql uses TCP `host`, so change the `host 127.0.0.1/32 scram-sha-256` line to `trust`
  (NOT the `local` line — no Unix socket on Windows), `net stop/start` the service, create with
  `psql -U postgres -h 127.0.0.1 -w`, then restore pg_hba. Use `ping -n 4 127.0.0.1 >nul`
  instead of `timeout /t` (MSYS intercepts `timeout`).

## Verification checklist

- `GET /api/health` → `{"status":"ok","deploymentMode":"authenticated"}`.
- Server log: `Server listening on 0.0.0.0:3100` and `Migrations applied` / `applied`.
- `/api/adapters` returns `{"error":"Board access required"}` until you log in — expected, not a failure.
- After login, the agent-creation form lists `hermes_local` (and `hermes_gateway`).

## References / templates / scripts

- `references/windows-pnpm-pitfalls.md` — full Windows/pnpm/MSYS failure modes + exact commands.
- `references/paperclip-api-bootstrap.md` — scriptable first-run: sign-up, claim, company, agent, issue, heartbeat, task-bridge key, and the non-obvious route paths/headers.
- `references/paperclip-agent-management.md` — post-setup operations: re-authentication after restart, enabling heartbeat, task-bridge key gotchas, valid providers list, model resolution chain, reading run output, troubleshooting.
- `references/hermes-free-model-config.md` — Hermes model/provider gotchas for hermes_local agents (prefix doubling, persistSession trap, free-model rate limits, OmniRoute install wall, config.yaml sandbox block).
- `references/continuous-operation.md` — keep-alive beyond install: Task Scheduler recipe for watchdog+server, Set-Cookie auth gotcha, reading run output / why stdoutExcerpt is empty until exit, task-bridge `projectId` requirement, artifact work-products retrieval, CTO+CMO revenue pattern.
- `references/omniroute-windows-startup.md` — Windows-specific Omniroute polyfill fix (Node.js 22 .ts import), serve subcommand requirement, hoisted linker recovery, first-run 500 diagnostic.
- `scripts/verify-openrouter-model.sh` — probe a free OpenRouter model for tool-call support before wiring it into an agent (exit 0 = usable for autonomy).
- `scripts/watchdog.py` — Windows-native, zero-LLM watchdog: re-auth, health check, auto-restart server, nudge idle worker agent; pair with Task Scheduler (see `references/continuous-operation.md`).
- `scripts/setup-pg-db.bat` — idempotent: temporarily trusts local PG, creates role+db, restores secure pg_hba.
- `templates/run-server.bat` — parameterized server launcher (sets env, runs tsx, logs to file).
- `templates/watchdog.sh` — no_agent Hermes cron script for 24/7 uptime (pings health endpoint, restarts on failure).

## Reality check

This automates the *work* of a company; it does not generate revenue by itself. You still need
a product people pay for and an API budget. Treat it as a self-running engineering/marketing
team you own and steer.
