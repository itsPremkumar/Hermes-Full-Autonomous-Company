# Paperclip first-run bootstrap via API (no browser needed)

The UI ("Sign in / Create account") is the documented path, but every step is also a
REST call. Use this when you want to script company + agent creation, or when driving
the flow from a headless shell. Base URL: `http://localhost:3100`. All mutation calls
need an `Origin: http://localhost:3100` header (Paperclip enforces a "trusted browser
origin" check — without it you get `Board mutation requires trusted browser origin`).

Save the session cookie once: `curl -c cj.txt ...` then reuse with `-b cj.txt`.

### 1) Create the first user (Better Auth sign-up)
```
curl -s -c cj.txt -X POST http://localhost:3100/api/auth/sign-up/email \
  -H "Content-Type: application/json" \
  -d '{"email":"prem@local.dev","password":"LocalDevPass123!","name":"Prem"}'
# -> {"token": "...", "user": {"id":"..."}}
```

### 2) Claim the instance as first admin (only once; bootstrapStatus must be pending)
```
curl -s -b cj.txt -X POST http://localhost:3100/api/bootstrap/claim \
  -H "Origin: http://localhost:3100"
# -> {"claimed":true,"userId":"..."}
# Requires the session cookie from step 1 — the claim reads req.actor.userId.
```

### 3) Create a company (requires instance admin — you now are one)
```
curl -s -b cj.txt -X POST http://localhost:3100/api/companies \
  -H "Origin: http://localhost:3100" -H "Content-Type: application/json" \
  -d '{"name":"Prem Autonomous Co","mission":"...","budgetMonthlyCents":50000}'
# -> {"id":"3056c999-...","issuePrefix":"PRE", ...}
```

### 4) Hire a Hermes agent
```
curl -s -b cj.txt -X POST http://localhost:3100/api/companies/<COMPANY_ID>/agents \
  -H "Origin: http://localhost:3100" -H "Content-Type: application/json" \
  -d '{"name":"Hermes Engineer","adapterType":"hermes_local","role":"cto",
       "adapterConfig":{...see hermes-free-model-config.md...}}'
# role is a LOWERCASE enum: ceo|cto|cmo|cfo|security|engineer|designer|pm|qa|devops|researcher|general
# "CTO" (uppercase) -> 400 invalid_enum_value.
```

### 5) Create + assign an issue, then trigger a heartbeat run
```
# Create (mounted under /companies/:id):
curl -s -b cj.txt -X POST http://localhost:3100/api/companies/<COMPANY_ID>/issues \
  -H "Origin: http://localhost:3100" -H "Content-Type: application/json" \
  -d '{"title":"...","body":"...","assignedAgentId":"<AGENT_ID>"}'
# NOTE: assigneeAgentId is the field; "assignedAgentId" works at create time,
#       but the issue may still come back with assigneeAgentId:null — PATCH it after.

# Assign via PATCH — GOTCHA: the issues router is mounted at the API ROOT, NOT under
# /companies/:id. Use /api/issues/:id (not /api/companies/:id/issues/:id).
curl -s -b cj.txt -X PATCH http://localhost:3100/api/issues/<ISSUE_ID> \
  -H "Origin: http://localhost:3100" -H "Content-Type: application/json" \
  -d '{"assigneeAgentId":"<AGENT_ID>","status":"todo"}'

# Trigger the agent heartbeat (manual dispatch):
curl -s -b cj.txt -X POST http://localhost:3100/api/agents/<AGENT_ID>/heartbeat/invoke \
  -H "Origin: http://localhost:3100"
# -> {"id":"<RUN_ID>","status":"queued"}

# Inspect the run (stdoutExcerpt shows the Hermes session transcript):
curl -s -b cj.txt http://localhost:3100/api/heartbeat-runs/<RUN_ID> -H "Origin: http://localhost:3100"
```

### 6) Reset a stale agent session (if persistSession left a dead session)
```
curl -s -b cj.txt -X POST http://localhost:3100/api/agents/<AGENT_ID>/runtime-state/reset-session \
  -H "Origin: http://localhost:3100" -H "Content-Type: application/json" -d '{}'
# Body required (validate() expects an object) or you get "Validation error ... Required".
```

### 7) Autonomy wiring: the task-bridge key (REQUIRED for hands-off execution)
### 7) Autonomy wiring: the task-bridge key (REQUIRED for hands-off execution)
The `hermes_local` adapter delivers the assigned issue to Hermes via the
`paperclip-task-bridge` Hermes skill, which calls Paperclip's REST API. That needs a
**task_bridge-scoped agent API key**. GOTCHA: the key body MUST include a boundary —
`scope.projectId` (use the COMPANY_ID) — or you get:
`Validation error ... task_bridge keys require at least one project or parent issue boundary`.
```curl -s -b cj.txt -X POST http://localhost:3100/api/agents/<AGENT_ID>/keys \
  -H "Origin: http://localhost:3100" -H "Content-Type: application/json" \
  -d '{"scope":{"kind":"task_bridge","projectId":"<COMPANY_ID>"},"name":"bridge"}'
# The returned key is injected as PAPERCLIP_BRIDGE_API_KEY for the agent's Hermes runs.
# Without it Hermes boots, prints the Execution Contract, then waits for a task ID
# instead of pulling PRE-1 itself.
# Idempotent: if a key already exists for the agent, just reuse/list it (GET .../keys).
```

### Issue assignment + status-transition gotchas (cost real debugging time)
- **`assignedAgentId` is silently dropped at issue creation** unless you ALSO pass
  `"status":"todo"` in the same create call. If you create with `assignedAgentId` but
  default status, the assignee comes back `null` and the agent never picks it up.
  SAFE pattern: create with BOTH `{"assignedAgentId":"<AID>","status":"todo",...}`.
- **PATCH `/api/issues/:id` is root-mounted** (NOT under `/companies/:id`).
- **`in_progress` requires an assignee.** PATCHing `status:"in_progress"` with
  `assigneeAgentId:null` returns **422** `in_progress issues require an assignee`.
  Fix: first PATCH `{"assigneeAgentId":"<AID>","status":"todo"}`, THEN a second PATCH
  `{"status":"in_progress"}`.
- **Project-scoped issues** created via `POST /api/companies/:id/issues` with a
  `projectId` start in `backlog`; they won't be heartbeat-dispatched until moved to
  `todo`/`in_progress`. Use the two-step assign+activate above.
- Agents sometimes **re-create duplicate epics** if the same mandate lives in both the
  COMPANY_PLAN.md and a standalone issue. Keep one canonical issue per epic; if duplicates
  appear, cancel the later ones (status `cancelled`) so the board stays clean.
- Shell note: MSYS `/tmp` is not shared between separate `terminal` calls on this host;
  write scratch files into the project dir (e.g. `C:/one/paperclip-company/`) instead.

- List an agent's issues with `GET /api/companies/<COMPANY_ID>/issues?assigneeId=<AGENT_ID>`
  — the bare `/api/issues?assigneeId=...` route returns 400.
- **Once `runtimeConfig.heartbeat.enabled=true`, the agent self-dispatches on a timer —
  do NOT keep manually calling `heartbeat/invoke`.** Repeated manual invokes while
  auto-heartbeat is on cause runs to be `cancelled`/`skipped` by the periodic recovery
  loop. Invoke manually only when heartbeat is disabled or for a one-off test.
