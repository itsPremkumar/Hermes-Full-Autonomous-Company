# Continuous development loop (Prem Autonomous Co session)

## Issue lifecycle timeline

Each agent heartbeat cycle follows this pattern (verified across 6+ runs):

```
Heartbeat fires (30s interval)
  → hermes chat -q "<prompt>" -m <model> --quiet
  → Agent loads AGENTS.md instructions (3589 chars)
  → Agent reads the assigned issue via $PAPERCLIP_TASK_ID
  → Agent writes Python scripts to Paperclip scratch dir
  → Agent executes scripts (API calls, terminal commands)
  → Agent uploads artifacts, creates work products
  → Agent posts comments updating issue status
  → Agent patches issue to done/in_review
  → [hermes] Exit code: 0 ✓
```

Typical duration: **3–4 minutes** per issue cycle (including 2+ min of model think time).

## Agent model resolution chain (why PATCH doesn't stick)

The Paperclip server's `normalizeMediatedAdapterConfigForPersistence` function overrides
whatever `model` and `provider` you set in the agent's `adapterConfig`. Here's the chain:

1. You PATCH agent: `{"adapterConfig": {"model": "deepseek-v4-flash-free", "provider": "auto"}}`
2. Server's PATCH handler merges into existing adapterConfig
3. `normalizeMediatedAdapterConfigForPersistence()` reads Hermes config → resolves model
4. The **stored value** ends up as whatever Hermes auto-detects (e.g., `tencent/hy3:free`)
5. PATCH response shows your values but they're silently overwritten

**Workaround:** set `replaceAdapterConfig: true` in the PATCH body to bypass merge logic:
```json
PATCH /api/agents/<ID>
{"adapterConfig": {"model": "tencent/hy3:free", "provider": "openrouter", ...}, "replaceAdapterConfig": true}
```

**Better:** set the model in Hermes's own `config.yaml` and leave the Paperclip adapter
model empty — Hermes uses its configured default.

## Known working free model: tencent/hy3:free

| Setting | Value |
|---|---|
| model | `tencent/hy3:free` |
| provider | `openrouter` |
| Env needed | `OPENROUTER_API_KEY` (passthrough via Paperclip's `ADAPTER_ENV_PASSTHROUGH`) |
| Rate limit | 20 req/min on OpenRouter free pool |
| Tool support | Full (terminal, file, web, vision) |
| Issues | Slight tendency to verbose output, but completes autonomously |

## Auto-assign-on-create and maxConcurrentRuns

Paperclip has two distinct behaviors around issue assignment:

1. **Agent-created child issues**: The Hermes Engineer creates child issues (e.g., PRE-3 → PRE-5 through PRE-8) but leaves `assigneeAgentId` blank. They sit as `todo`/`in_review` until someone assigns them.

2. **API-created issues with assignee**: If YOU create an issue via REST API with `assigneeAgentId` set, Paperclip **immediately starts a heartbeat run** — no 30s tick wait. Verified: creating PRE-11 and PRE-12 with `assigneeAgentId` populated caused instant run creation (timestamps show runs starting <1s after issue creation).

3. **maxConcurrentRuns limit**: The agent has `maxConcurrentRuns: 3`. When all 3 slots are occupied:
   - PRE-7 (3 sample videos) → active run
   - PRE-11 (monitor outreach) → active run
   - PRE-12 (implement revenue assets) → active run
   Any new issue with an assigned agent queues until a slot opens. No error, no rejection — just deferred execution.

**Practical implication for cron pipeline management**: Creating a child issue with `assigneeAgentId` is the fastest way to get work started. The agent doesn't self-assign, so the cron/founder must either: (a) create the issue with assignee pre-set (triggers auto-run), or (b) create without assignee, then PATCH the assignee (also triggers a run).

## Run timeout and retry cycle

The agent runs are bounded by `timeoutSec` (default 1800s = 30 min). What happens when a run times out:

```
1. Agent works on the issue (e.g., PRE-7: producing 3 sample videos)
2. Agent edits files, runs commands, generates content
3. Run reaches 1800s timeout
4. [hermes] Exit code: null, timed out: true   ← clean timeout exit
5. Paperclip detects the run ended (or keeps it in "running" state)
6. A new heartbeat is triggered (by the 30s tick or by issue creation)
7. Agent picks up the same issue and continues
```

This was verified with PRE-7: the first run (`fcb142a9...`) worked on editing `input-scripts.json`, adding 3 video scripts, then timed out at 30 min. A new run (`86935249...`) was auto-triggered and started the same issue again. The agent makes durable progress each cycle — file edits, artifacts uploaded, work products created — so retries resume from where the previous run left off.

**Key insight:** runs are idempotent progress cycles, not transactions. Each cycle advances the issue toward completion. Multiple retries on the same issue are normal and expected, especially for long-running tasks (video rendering, batch publishing).

## Revenue engine output (PRE-9)

Agent `1ca47b10-b2c7-4bb9-b73e-d2428f1c6fd8` completed PRE-9 "Revenue engine: build zero-cost, publishable monetization assets" with **8 artifact work products**:

| # | Artifact | Description |
|---|---|---|
| 1 | 30-Day Zero-Cost Launch Plan | Week-by-week launch with KPIs, risks, and definition of done |
| 2 | Lead Magnet: AI Agent ROI Calculator | Zero-cost gated calculator offer + copy block + email hook |
| 3 | Company One-Pager | Shareable Prem Autonomous Co one-pager for prospects/communities |
| 4 | Monetization Brief (Revenue Engine v1) | CMO strategy: ICP, revenue streams, pricing posture, funnel, 90-day target |
| 5 | Cold Outreach Pack | Ready-to-send email + LinkedIn sequences and objection handlers |
| 6 | Service Catalog (6 agent teams) | Six packaged autonomous-agent offers + bundle |
| 7 | Reseller & Affiliate Program | 25-30% recurring partner tracks, onboarding, guardrails |
| 8 | Public Pricing Sheet | Transparent USD price table, add-ons, annual discount, reseller terms |

These are all uploaded as attachments to PRE-9. The follow-up issue PRE-12 was created for the Hermes Engineer to review and start implementing these assets at zero cost (GitHub Pages / LinkedIn / free hosting).

## Full AGENTS.md execution contract summary

The agent loads `AGENTS.md` (3589 chars) at the start of every run. Key directives relevant to pipeline management and issue creation:

- **Start actionable work immediately** — do not stop at a plan unless the issue explicitly asks for one
- **Leave durable progress** — task comments, documents, work products
- **Upload artifacts via `paperclip-upload-artifact.sh`** — don't rely on local filesystem paths
- **Create work products** — use correct type: `artifact` for deliverables, `pull_request` for PRs, `preview_url` for previews
- **Use child issues for parallel work** — instead of polling agents or processes
- **Use interactions for decisions** — `suggest_tasks` (propose follow-ups), `ask_user_questions` (structured questions), `request_confirmation` (yes/no decisions with idempotency key)
- **Final disposition checklist**: `done` when complete/verified, `in_review` only with a real reviewer path, `blocked` with named unblock owner, `in_progress` only with a live continuation path
- **Assign/unblock routing** — assign or comment naming the unblock owner and action when someone needs to unblock

## Revenue pipeline (PRE-3 monetization plan → execution)

The agent designed and partially executed this zero-investment revenue pipeline:

```
PRE-3: Product analysis + monetization plan
  → Created artifact: artifacts/PRE-3-monetization-plan.md (84 lines)
  → 4 revenue paths: Service / Templates / Channel / Lead-gen
  → Created child issues PRE-5 through PRE-8
  ↓
PRE-6: Pricing tiers (completed, in_review)
  → Artifact: artifacts/PRE-6-agent-labor-service-pricing.md (106 lines)
  → Tiers: Free ($0, 1/mo) / Starter ($15-40/task) / Pro ($99/mo, 8/mo) / Scale ($299/mo, 30/mo)
  → ~100% gross margin (agent compute only)
  ↓
PRE-7: 3 sample videos (in_progress)
  → 3 scripts written to AVG input-scripts.json:
    1. "3 Mind Blowing Facts About Space" (portrait, en-US-GuyNeural)
    2. "The Ocean Is Deeper Than You Imagine" (portrait, en-US-AriaNeural)
    3. "One Simple Trick To Beat Procrastination" (portrait, en-US-JennyNeural)
  → AVG render started via npm run generate
PRE-5: Showcase repo/LinkedIn page (in_progress)
PRE-8: Direct outreach on free job boards (in_progress)
```

## Founder gates

The agent cannot finalize these decisions — they block go-to-market:

1. **Target niche** — job-seekers / tech creators / local businesses / edu?
2. **Price floor** — ₹499/video ($6) or higher?
3. **Public demo** — Can AVG be shown publicly as the company's demo product?
4. **Lead offer** — Pay-per-task (Starter) or $99 Pro retainer first?
5. **Catalog scope** — All 5 deliverable types or focused 2 (e.g. code + media)?

## Server zombie detection and recovery

The Paperclip Node process can appear alive in the process list while the HTTP server
is not serving requests. This happened after a crash — `ps -W | grep node` showed
node.exe alive (PID 15956) but `curl localhost:3100/api/health` returned connection
refused (exit code 7). The process was a zombie: alive in the process table but the
port was unbound.

**Detection sequence (cron-safe):**
```bash
# Step 1: Try health endpoint first (fast, no side effects)
curl -s --max-time 5 "http://localhost:3100/api/health"
# If this returns {"status":"ok"} → server is healthy, proceed.
# If this returns connection refused (exit code 7) → check process list.

# Step 2: Check process list
ps -W | grep node
# If node.exe is running but health endpoint is down → zombie.

# Step 3: Check port binding
netstat -ano | grep 3100
# If nothing on 3100 but node.exe is running → confirmed zombie.
```

**Recovery sequence:**
1. Kill the stale Node process: `kill -9 <PID>` (git-bash) or `taskkill /F /PID <PID>` (cmd)
2. Verify port is free: `netstat -ano | grep 3100` returns nothing
3. Restart the server: `cd /c/one/paperclip-company && cmd.exe /c run-server.bat`
4. Wait for health endpoint to return `{"status":"ok"}`
5. **Must reset agent runtime session** (stale after crash):
   ```bash
   curl -s -b cj.txt -H "Origin: http://localhost:3100" -H "Content-Type: application/json" \
     -X POST "http://localhost:3100/api/agents/<AGENT_ID>/runtime-state/reset-session" -d '{}'
   ```
6. Invoke heartbeat:
   ```bash
   curl -s -b cj.txt -H "Origin: http://localhost:3100" -H "Content-Type: application/json" \
     -H "X-Requested-By: paperclip" \
     -X POST "http://localhost:3100/api/agents/<AGENT_ID>/heartbeat/invoke"
   ```
7. Verify dispatch: check run-logs directory for new `.ndjson` files within 60 seconds.

**Key insight:** The server restart reaps orphaned heartbeat runs automatically (seen in
startup logs: "reaped orphaned heartbeat runs"). But the agent's Hermes session is
stale and must be explicitly reset. Without the reset, subsequent heartbeat runs
may fail with adapter initialization errors.

## Heartbeat invoke queue vs. scheduler tick

When you call `POST /api/agents/<ID>/heartbeat/invoke`, the response status is
`"queued"` — not immediately `"running"`. This is normal. However, the Paperclip
scheduler has its own 30-second tick that independently dispatches the highest-priority
issues. The two mechanisms interact:

**Important behavior observed:**
- Calling `/heartbeat/invoke` returns a queued run that may sit in `queued` status
  indefinitely if `maxConcurrentRuns` (default 3) is saturated.
- Meanwhile, the 30-second tick scheduler continues dispatching runs as slots free up.
- The agent was actively processing and completing issues (PRE-63, PRE-64, PRE-65, PRE-13
  all got done during/after a server restart) even though the manually-invoked run
  stayed `queued`.

**How to verify the agent is actually working:**
```bash
# Don't poll the run status endpoint — check for new log files instead:
ls -lt /c/one/paperclip-company/data/paperclip/instances/default/data/run-logs/<COMPANY_ID>/<AGENT_ID>/*.ndjson | head -5
```
If new `.ndjson` files appear with recent modification timestamps (within the last
60 seconds), the scheduler is dispatching the agent and it is doing real work.
Each log file with >50 lines of content = a successful run with tool calls, code
changes, API interactions, and issue updates.

**Practical rules for cron jobs:**
1. After invoking heartbeat, do not poll the run status. Check run-logs instead.
2. If the agent shows `activeRun: none` but run-logs have recent files, the agent is
   working on short-lived runs that complete quickly between checks.
3. A `queued` invoke status is not an error. The queue drains when scheduler capacity
   opens. The invoke is a safety-net trigger, not the primary dispatch mechanism.
4. If no new run-logs appear for >2 minutes after the invoke, the scheduler may be
   stuck — try the session reset + re-invoke sequence.

## Cookie recovery after server restart

```bash
# Re-authenticate
curl -s -X POST "http://localhost:3100/api/auth/sign-in/email" \
  -H "Content-Type: application/json" \
  -d '{"email":"prem@local.dev","password":"LocalDevPass123!"}' \
  -c cj.txt -H "Origin: http://localhost:3100"
# Verify
curl -s -b cj.txt "http://localhost:3100/api/companies" \
  -H "Origin: http://localhost:3100"
```

## AVG (Automated-Video-Generator) render pipeline

The revenue product is at `C:\one\Automated-Video-Generator` (MIT, TS/Node, Remotion + Edge-TTS).

```bash
# Install deps (one-time)
cd /c/one/Automated-Video-Generator && npm install

# Generate a single video
npm run generate -- --id <script-id>
# e.g. npm run generate -- --id pre7-space-facts

# Scripts live in input/input-scripts.json
# Each entry: {id, title, script, orientation, language, voice, showText}

# Render via Remotion studio (for preview)
npm run remotion:studio

# Direct Remotion render
npm run remotion:render -- --props '{"id":"pre7-space-facts"}'
```

Stock media fetching uses free sources (Openverse, CC0) — quality varies. Portrait (9:16) oriented
for YouTube Shorts/Instagram Reels. Voices: en-US-GuyNeural, en-US-AriaNeural, en-US-JennyNeural.

## Cron job for pipeline management

```bash
hermes cron create --name "company-revenue-pulse" --schedule "every 15m" \
  --prompt "Check the Prem Autonomous Co Paperclip company and advance revenue work.
Company ID: 3056c999-62ba-4321-ae69-799a61286bad
Agent ID: 9eed5712-96c2-4f3c-9fea-1cef0e6b7f2f
Tasks:
1. GET /api/companies/{companyId}/issues (use cookie auth — extract token inline, see below)
2. For 'done' issues, create follow-up child issues if appropriate
3. For unassigned 'todo' issues, assign to agent + set in_progress
4. If agent is idle and work exists, POST /api/agents/{agentId}/heartbeat/invoke

Auth pattern (curl in git-bash):
- Cookie file at C:/one/paperclip-company/cj.txt may NOT load with -b flag (MSYS path issue).
  Extract the token inline instead:
  TOKEN=\$(grep 'paperclip-default.session_token' /c/one/paperclip-company/cj.txt | awk '{print \$NF}')
- GET reads: curl -s --cookie \"paperclip-default.session_token=\$TOKEN\" ...
- POST/PATCH mutations: add -H 'Origin: http://localhost:3100' -H 'X-Requested-By: paperclip'
- Also add -H 'Referer: http://localhost:3100/' if Origin+X-Requested-By still returns 403.
- Always pair with -H 'Content-Type: application/json' for POST bodies." \
  --deliver local \
  --enabled-toolsets terminal,file,web
```
