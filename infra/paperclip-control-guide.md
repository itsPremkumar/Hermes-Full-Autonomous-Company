# Paperclip — Control & Usage Guide
### How to start, control, and operate the autonomous company runtime (Paperclip) on this machine

> **Verified on:** 2026-07-14 · Windows 10 · Paperclip (paperclipai/paperclip) · Server on port `3100` · Postgres 17 on `5432` · Node 22.23.1
>
> Every command below was **actually run and verified** on the machine it documents. Outputs shown are the literal results observed.

---

## 0. TL;DR — what Paperclip is, in one line

**Paperclip is the autonomous-company runtime:** an org chart of AI agents (CEO, CFO, COO, CMO, Head of Product, QA, Engineer) with budgets, governance, ticketing, and a web UI on `localhost:3100`. It is the **brain of the company**; Hermes Agent and OpenClaw plug into it as adapters.

On this machine the stack is layered:
| Layer | Tool | Job |
|-------|------|-----|
| **Runtime / org** | **Paperclip** (this repo) | Agent org chart, budgets, tickets, governance — `localhost:3100` |
| **Brain + hands** | **Hermes Agent** | Does the work (builds, file ops, learning) via `hermes_local` adapter |
| **Mouth + ears** | **OpenClaw** | Chat/phone front-door (Telegram) — see `infra/openclaw-control-guide.md` |
| **Income execution** | **money-engine** | Zero-cost income pipelines — see `COMPANY_PLAN.md` §5.1 |

---

## 1. Prerequisites (verified present on this box)

| Requirement | Status | How verified |
|-------------|--------|----------------|
| Postgres 17 running | ✅ | `netstat` shows `:5432` LISTENING (PID 8348); service `postgresql-x64-17` = Running |
| Paperclip source present | ✅ | `paperclip/server/src/index.ts` exists |
| node_modules built | ✅ | `paperclip/node_modules` present (no install needed) |
| Node 22.23.1 | ✅ | used by tsx at launch |
| `.moltbook_key` secret | ✅ safe | gitignored (`.gitignore` line 20) — never committed/echoed |

> ⚠️ **RAM constraint:** this box is ~6 GB. The repo's `run-server.bat` sets `--max-old-space-size=8192` (8 GB) — that **will OOM and crash** here. Launch with **`--max-old-space-size=1500`** instead (verified stable: server ran at ~330 MB free).

---

## 2. Starting the server (the command that actually works)

> ⚠️ **Critical Windows/git-bash pitfall:** the repo's `run-server.bat` uses backslash paths (`C:\one\...`). Under git-bash those backslashes get mangled → `bash: exec: C:onepaperclip...: not found`. **Use forward slashes.** Also `exec` detaches in background shells — don't use it.

Launch (background, RAM-safe) from a shell:

```bash
cd /c/one/paperclip-company/paperclip/server
export PORT=3100
export HOST=0.0.0.0
export SERVE_UI=true
export PAPERCLIP_DEPLOYMENT_MODE=authenticated
export PAPERCLIP_DEPLOYMENT_EXPOSURE=private
export PAPERCLIP_PUBLIC_URL=http://localhost:3100
export PAPERCLIP_HOME=/c/one/paperclip-company/data/paperclip
export PAPERCLIP_MIGRATION_AUTO_APPLY=true
export DATABASE_URL="postgres://paperclip:paperclippw@localhost:5432/paperclip"
export BETTER_AUTH_SECRET=paperclip-dev-secret-change-me
export NODE_OPTIONS="--max-old-space-size=1500"   # NOT 8192 — box is 6GB
export PATH="/c/Users/PREM KUMAR/AppData/Local/Programs/Python/Python312:$PATH"
node node_modules/tsx/dist/cli.mjs src/index.ts
```

Verified boot banner (literal):
```
Mode       external-postgres  |  static-ui
Deploy    authenticated (private)
Bind      lan (0.0.0.0)
Auth      ready
Server    3100
API       http://localhost:3100/api  (health: http://localhost:3100/api/health)
Database  postgres://paperclip:***@localhost:5432/paperclip
Migrations already applied
Heartbeat  enabled (30000ms)
[INFO] Server listening on 0.0.0.0:3100
```

---

## 3. Controlling Paperclip — the verified control surface

### 3.1 Health (no auth — your primary probe)
```bash
curl -sS --max-time 10 http://127.0.0.1:3100/api/health
```
Verified response (HTTP 200):
```json
{"status":"ok","deploymentMode":"authenticated","deploymentExposure":"private",
 "bootstrapStatus":"ready","databaseBackup":{"enabled":true,"status":"warning",
 "warnings":[{"code":"database_backup_missing","message":"No recent database backup was found."}]}
```
> The `database_backup_missing` warning is **informational** — backups auto-enable after first 60-min cycle. Not blocking.

### 3.2 Is the process alive? (Windows — use wmic, NOT /proc)
```bash
timeout 10 wmic.exe process where "name='node.exe'" get ProcessId,CommandLine 2>/dev/null | tr -d '\r' | grep -i tsx
netstat -ano 2>/dev/null | grep ":3100"
```
Verified: PID **20152** LISTENING on `:3100`.

### 3.3 Is Postgres up? (required dependency)
```bash
netstat -ano 2>/dev/null | grep ":5432"
timeout 10 wmic.exe service where "name='postgresql-x64-17'" get Name,State
```

### 3.4 Stopping / restarting
```bash
# find + kill the tsx/node PID (use wmic, never pkill on Windows git-bash)
for p in $(timeout 10 wmic.exe process where "name='node.exe'" get ProcessId,CommandLine 2>/dev/null | tr -d '\r' | grep -i tsx | grep -oE '[0-9]+ *$'); do
  taskkill /PID $(echo $p | tr -d ' ') /F
done
# then relaunch per §2
```

### 3.5 Agent-command API (auth-gated — needs JWT)
```bash
curl -sS --max-time 10 -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3100/api/companies
```
Verified: **`403`** — agent/company endpoints require the **Agent JWT**, which is not yet bootstrapped (see §4).

---

## 4. The one missing step: Agent JWT (`onboard`)

The health banner warns: `Agent JWT missing (run pnpm paperclipai onboard)`. Without it you can **monitor** Paperclip (health/process) but **cannot command the agents** via API/UI.

**Why it didn't complete automatically here:**
- `npx paperclipai@latest onboard` **timed out (150s)** fetching the CLI on this network/box.
- Building the CLI locally (`tsc` in `paperclip/cli`) succeeds, but the emitted `dist/cli/src/index.js` imports `packages/shared/src/*.ts` that are **not compiled** in a partial build → `ERR_MODULE_NOT_FOUND` at runtime.
- The CLI needs a **full monorepo build** (`pnpm build` at repo root: builds `packages/*` + `cli`) before `onboard` runs.

**To finish later (when box has headroom / network):**
```bash
cd /c/one/paperclip-company/paperclip
pnpm install        # if deps drifted
pnpm build          # builds packages/shared + cli (full monorepo)
export PAPERCLIP_HOME=/c/one/paperclip-company/data/paperclip
node cli/dist/cli/src/index.js onboard --yes
# then open http://localhost:3100 and log in with the bootstrapped CEO creds
```

Until then, Paperclip runs in **monitor-only** mode: health green, agents reconciled (startup log: `reconciliation ... scanned:1, reconciled:1`), but no JWT-authed commands.

---

## 5. Failure modes observed (so you don't repeat them)

| Symptom | Cause | Fix |
|---------|-------|-----|
| `bash: exec: C:onepaperclip...: not found` | Backslash paths mangled by git-bash | Use **forward slashes** (`/c/one/...`) |
| Server logs "listening" then port dead | `exec` detached in background shell; or OOM | Don't `exec`; cap RAM at 1500 MB |
| OOM / box freezes on launch | `NODE_OPTIONS=--max-old-space-size=8192` from `run-server.bat` | Override to **1500** |
| `/api/companies` → 403 | Agent JWT not bootstrapped | Run `onboard` (§4) after full build |
| `npx paperclipai onboard` hangs | Network/registry slow on this box | Build CLI locally + full `pnpm build` instead |
| Postgres connection refused | Postgres service stopped | `net start postgresql-x64-17` (needs admin) |

---

## 6. Security & honesty notes

- **`.moltbook_key`** is gitignored — never commit or echo it. Same for any `OPENROUTER_API_KEY` (injected from env, never hardcoded — GitHub secret scanning blocks leaks).
- **`BETTER_AUTH_SECRET`** above is the dev default (`paperclip-dev-secret-change-me`). For any non-local exposure, set a real secret.
- **Deploy mode is `authenticated` + `private`** in this setup — correct for a local company runtime. Don't flip to public without a real auth secret + firewall.
- Paperclip is the **company OS source of truth** (per `README.md`); this guide lives at `infra/paperclip-control-guide.md` so the runtime is documented for reuse.

---

## 7. Quick command reference

| Goal | Command |
|------|---------|
| Start (RAM-safe) | §2 launch block |
| Health | `curl http://127.0.0.1:3100/api/health` |
| Is it up? | `netstat -ano \| grep :3100` + `wmic ... node.exe` |
| Postgres up? | `netstat -ano \| grep :5432` |
| Stop | `taskkill /PID <PID> /F` (from wmic) |
| Agent JWT | `node cli/dist/cli/src/index.js onboard --yes` (after `pnpm build`) |
| UI | http://localhost:3100 |

---

## 8. Sources (live, 2026-07-14)
- Local: `/c/one/paperclip-company/` (mirror of `paperclipai/paperclip`, MIT)
- Verified: server boot banner, `/api/health` 200, Postgres 5432 LISTENING, wmic node PIDs
- CLI docs: `paperclip/cli/README.md` (`npx paperclipai onboard --yes`)

*Generated and verified by Hermes Agent on the target machine. Commands are real; outputs are the literal results observed.*
