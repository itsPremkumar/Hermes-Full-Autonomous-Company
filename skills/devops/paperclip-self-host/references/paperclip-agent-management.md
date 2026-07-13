# Paperclip Agent Management (post-setup operations)

Operations for managing a running Paperclip company and its Hermes agents —
fixing config after server restart, enabling heartbeat, creating task-bridge keys,
resolving model/provider mismatches, and reading run output.

## Re-authentication after server restart

When the Paperclip server restarts, Better Auth session cookies are invalidated.
Re-login via the sign-in endpoint:

```bash
BASE=http://localhost:3100/api
curl -s -c cj.txt -X POST "$BASE/auth/sign-in/email" \
  -H "Content-Type: application/json" \
  -d '{"email":"prem@local.dev","password":"LocalDevPass123!"}'
# -> {"token":"...","user":{"id":"..."}}
```

Then use `-b cj.txt` for subsequent calls. All mutation calls also need
`-H "Origin: http://localhost:3100"` (Paperclip's trusted-origin check).

## Checking agent state after restart

```bash
# List all agents for a company
curl -s -b cj.txt "$BASE/companies/<COMPANY_ID>/agents" \
  -H "Origin: http://localhost:3100"

# Key fields to check per agent:
#   status: "idle" | "running" | "paused" | "error"
#   adapterConfig.model, adapterConfig.provider
#   runtimeConfig.heartbeat.enabled          <- often false after initial create
#   lastHeartbeatAt                         <- null if never ran
```

## Enabling heartbeat (agent won't run without it)

New agents and agents created via the API boot with heartbeat **disabled**.
You must explicitly enable it:

```bash
curl -s -b cj.txt -X PATCH "$BASE/agents/<AGENT_ID>" \
  -H "Origin: http://localhost:3100" -H "Content-Type: application/json" \
  -d '{
    "runtimeConfig": {
      "heartbeat": { "enabled": true, "maxConcurrentRuns": 3 }
    }
  }'
```

Default heartbeat interval is 30 seconds. The agent will auto-queue work for
any `in_progress` or `todo` issue assigned to it.

## Resetting agent session after config changes

After changing model/provider/instructions, always reset the runtime session
to clear stale state. The body MUST be `{}` (empty JSON object) — Paperclip's
validate() rejects a bare POST without it:

```bash
curl -s -b cj.txt -X POST "$BASE/agents/<AGENT_ID>/runtime-state/reset-session" \
  -H "Origin: http://localhost:3100" -H "Content-Type: application/json" \
  -d '{}'
```

## hermes_local adapter: valid providers

From `packages/adapters/hermes/src/shared/constants.ts`:

```
auto, openrouter, nous, openai-codex, copilot, copilot-acp,
anthropic, huggingface, zai, kimi-coding, minimax, minimax-cn, kilocode
```

**`opencode` is NOT a valid provider.** If the adapter receives an invalid
provider string, `resolveProvider()` falls through to model-prefix inference
(step 4) or `auto` (step 5), so the agent may still run but will ignore your
explicit provider choice. Use `"auto"` to let Hermes use its own config.

## Model resolution chain

The adapter in `execute.ts` resolves the model and provider in this priority:

1. **Explicit model in adapterConfig** — if non-empty, passed as `-m <model>`.
2. **Empty model** → falls back to `DEFAULT_MODEL = "auto"` → also passed as `-m auto`.
3. **Explicit provider in adapterConfig** — if set AND in VALID_PROVIDERS, passed as `--provider <provider>`.
4. **Provider `"auto"`** → `--provider` is NOT passed → Hermes CLI uses its own config.yaml default.
5. **No explicit model AND no explicit provider** → `-m auto`, no `--provider` → Hermes uses its own config.

When BOTH model and provider are auto/resolved-to-auto, the adapter runs:
```
hermes chat -q "<prompt>" -Q --source tool --yolo
```
(no `-m` or `--provider` flags) — Hermes CLI reads its own `~/.hermes/config.yaml` entirely.

When model is explicitly set (e.g. `deepseek-v4-flash-free`) and provider is `auto`:
```
hermes chat -m deepseek-v4-flash-free -q "..." -Q --source tool --yolo
```
Hermes resolves the provider from the model-name prefix first (`deepseek` → model-prefix hint → `auto`),
then falls back to its config.yaml. If `OPENROUTER_API_KEY` is present in the environment AND the
model name is recognized by OpenRouter, Hermes may route through OpenRouter instead of the
configured provider — see "OpenRouter key env conflict" below.

## Prefix-based provider hints

From `MODEL_PREFIX_PROVIDER_HINTS` in the adapter's `constants.ts`:

| Model prefix | Inferred provider |
|---|---|
| `gpt-4` | `openai-codex` |
| `gpt-5` | `copilot` |
| `o1-`, `o3-`, `o4-` | `openai-codex` |
| `claude` | `anthropic` |
| `gemini` | `auto` |
| `hermes-` | `nous` |
| `glm-` | `zai` |
| `moonshot`, `kimi` | `kimi-coding` |
| `minimax` | `minimax` |
| `deepseek` | `auto` |
| `llama`, `qwen`, `mistral` | `auto` |
| `huggingface/` | `huggingface` |

## Working free model: deepseek-v4-flash-free via OpenCode Zen

This model worked reliably where OpenRouter's free pool was rate-limited (429s):

```json
{
  "model": "deepseek-v4-flash-free",
  "provider": "auto",
  "maxIterations": 50,
  "timeoutSec": 1800,
  "persistSession": false
}
```

Requires `OPENCODE_ZEN_API_KEY` in `~/.hermes/.env` (already present on this host).

## OpenRouter key env conflict

When `OPENROUTER_API_KEY` is set in the Paperclip server's environment (e.g. in
`run-server.bat`), the Hermes child process inherits it. If Hermes detects an
OpenRouter key AND the model name is not explicitly one that maps to a different
provider, Hermes may route through OpenRouter's (rate-limited) free pool instead
of the intended provider.

**To force Hermes to use its own config**: set an explicit model name that
maps to a non-OpenRouter provider via prefix hints (e.g. `deepseek-v4-flash-free`
maps to `auto`), OR remove `OPENROUTER_API_KEY` from the server env and rely on
Hermes's own `~/.hermes/.env`.

## Task-bridge key (autonomous execution)

The task-bridge key is **required** for the Hermes agent to autonomously pull
and work on issues. Without it, Hermes boots, prints the Execution Contract,
and waits for a task ID instead of self-dispatcing the assigned issue.

**IMPORTANT:** The `projectId` field is **required** — Paperclip validates
"task_bridge keys require at least one project or parent issue boundary":

```bash
curl -s -b cj.txt -X POST "$BASE/agents/<AGENT_ID>/keys" \
  -H "Origin: http://localhost:3100" -H "Content-Type: application/json" \
  -d '{
    "scope": { "kind": "task_bridge", "projectId": "<COMPANY_ID>" },
    "name": "bridge"
  }'
# -> {"id":"...","token":"pcp_..."}
```

The returned token is automatically injected as `PAPERCLIP_BRIDGE_API_KEY` into
the Hermes subprocess environment by the Paperclip server.

## Triggering a heartbeat manually

```bash
curl -s -b cj.txt -X POST "$BASE/agents/<AGENT_ID>/heartbeat/invoke" \
  -H "Origin: http://localhost:3100"
# -> {"id":"<RUN_ID>","status":"queued"}
```

## Reading run output

```bash
curl -s -b cj.txt "$BASE/heartbeat-runs/<RUN_ID>" \
  -H "Origin: http://localhost:3100"
```

Key fields:
- `status`: `queued` → `running` → `succeeded` | `failed` | `cancelled`
- `stdoutExcerpt`: Hermes session transcript (includes model, provider, errors,
  tool calls, and the execution contract)
- `stderrExcerpt`: stderr from the Hermes process
- `exitCode`: 0 even when the API call failed (Hermes exits 0 after logging errors)
  — check `stdoutExcerpt` for 429/rate-limit messages
- `error`: top-level error message from Paperclip's perspective
- `issueCommentStatus`: whether the run posted an issue comment

**Run succeeded but agent did nothing?** Check `stdoutExcerpt` for:
- `"HTTP 429"` → rate-limited model, switch provider or add a dedicated API key
- `"Rate limit exceeded"` → same
- `"waiting for a task ID"` → task-bridge key missing or not wired
- `"persistSession"` → agent resumed a stale session instead of executing the issue

## Issue lifecycle: the autonomy gap

A critical behavioral pattern of `hermes_local` agents that stalls continuous
development if unhandled:

```
Assigned issue → agent completes it → creates child issues
                                     → child issues are UNASSIGNED ❌
                                     → pipeline stops at next heartbeat
```

The agent reliably:
- Reads its assigned issue and writes Python/curl scripts to execute work
- Uploads artifacts as Paperclip attachments + work-products
- Posts detailed completion comments
- Sets the issue to `done`
- Creates follow-on / child issues with descriptive titles

What it does **not** do:
- Assign itself to the child issues it creates (`assigneeAgentId` stays null)
- Respond to `ask_user_questions` or `request_confirmation` interactions
  (the agent POSTs them but the API schema often rejects them with 400)

### Bridging the gap

**1. Hermes cron auto-assigner (preferred for continuous operation)**

Create a cron job that runs every 15m — it finds unassigned `todo` issues and
assigns them to the agent so the next heartbeat picks them up:

```python
# Pseudocode — implement with curl + jq or Python
GET /api/companies/<COMPANY_ID>/issues
# Filter: status == "todo" AND assigneeAgentId == null
# For each: PATCH /api/issues/<ID> with {"assigneeAgentId": "<AGENT_ID>"}
```

The cron job uses the Paperclip API with the stored cookie + Origin header.
This makes the pipeline fully hands-off: the agent creates issues, the cron
assigns them, the heartbeat dispatches them.

**2. Manual batch assign**

PATCH all child issues to the agent in one batch call, then trigger
`POST /api/agents/<AGENT_ID>/heartbeat/invoke`. The agent works through them
sequentially — each heartbeat picks up the next `in_progress` or `todo` issue.

## Multi-agent revenue pipeline (CTO + CMO)

Hire a second `hermes_local` agent with `role: "cmo"` (same free model,
heartbeat enabled, task-bridge key). Create revenue issues with concrete,
**free-only** acceptance criteria. Both agents then self-dispatch in parallel.

Caveats:
- Both share the same free model (`tencent/hy3:free`) — concurrent runs
  compound OpenRouter rate limits; stagger or assign different models.
- Agents build the assets; the human must still publish and do outreach
  (the agent cannot post to LinkedIn/Naukri without your credentials).
- The autonomy gap applies to both agents — the cron auto-assigner or
  manual assignment step is needed for each.

**Agent stays "running" for minutes with no stdout**: Hermes CLI is starting,
connecting to the model, or the model is slow on first inference. Wait 60-90s
before investigating. If still running after 5 min, the model may be hung —
cancel the run and try a different model.

**401 on API calls**: cookie expired (server restart resets Better Auth sessions).
Re-login via sign-in/email.

**"Board mutation requires trusted browser origin"**: missing `Origin` header.
Add `-H "Origin: http://localhost:3100"`.

**400 "Unsupported query parameter"**: Some Paperclip endpoints use `limit`
instead of `pageSize`. Try without the query param, or use `limit=50`.

**422 "Validation error" on PATCH**: The endpoint expects specific fields.
For `/api/issues/:id`, use `assigneeAgentId` (not `assignedAgentId` or `assigneeId`).
For `/api/agents/:id/runtime-state/reset-session`, body MUST be `{}`.
