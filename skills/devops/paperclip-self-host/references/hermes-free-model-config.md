# Hermes model config for Paperclip hermes_local agents (free-LLM gotchas)

When you hire a `hermes_local` agent, its `adapterConfig.model` / `provider` drive which
LLM Hermes shells out to. Getting this wrong produces runs that "succeed" (Hermes exits 0)
but never actually do the work. These are the failure modes observed end-to-end.

## Provider prefix rule (most common 400)
When `provider` is set, the `model` string must NOT repeat the provider prefix.
- `provider: "openrouter"` + `model: "openrouter/tencent/hy3:free"` -> HTTP 400
  `openrouter/tencent/hy3:free is not a valid model ID`.
- CORRECT: `provider: "openrouter"` + `model: "tencent/hy3:free"`.
- For Nous: `provider: "nous"` + `model: "RefinedNeuro/vibethinker-3b-hermes"` (no `nous/` prefix).

## persistSession must be false (stale-session trap)
With `persistSession: true`, each heartbeat RESUMES the previous Hermes session. After any
failed/empty run, the next run boots into the dead session and prints "I'm ready to execute,
please provide the task" instead of pulling the assigned issue. Set `persistSession: false`
so every run starts fresh with the issue injected. (Session resume is for interactive
continuations, not scheduled agent work.)

## Free models: rate limits + capability
OpenRouter's SHARED free pool (`is_byok:false`) is heavily rate-limited (HTTP 429) on the
larger models (gemma-4-26b, qwen-80b, etc.) and the small ones that return content
(nemotron-nano-9b-v2:free) are too weak to follow the execution contract. Observed working
free models reachable from this host:
- `tencent/hy3:free` (via OpenRouter) — **RECOMMENDED ZERO-COST DEFAULT.** VERIFIED
  2026-07-12: with a real `OPENROUTER_API_KEY` exported to the Paperclip server it
  returns valid `tool_calls` (OpenRouter routes it to a capable upstream). The stale
  note claiming it "returns EMPTY on tool calls" is WRONG — retest before switching
  away. Ship agents with this model.
- `nvidia/nemotron-nano-9b-v2:free` — returns content but is TOO SMALL to follow the
  execution contract; it churns through iterations without completing work. Do NOT use
  for autonomous agents.
- Other capable free+tool models (from the 19-model list): `qwen/qwen3-coder:free`,
  `openai/gpt-oss-120b:free`, `meta-llama/llama-3.3-70b-instruct:free`,
  `google/gemma-4-26b-a4b-it:free`. These work but are MORE rate-limited (HTTP 429) on
  OpenRouter's shared pool than hy3:free — prefer them only with a personal OpenRouter
  key. Probe any candidate with `scripts/verify-openrouter-model.sh` before wiring it in.
- 19 free + tool-capable models exist on OpenRouter (query `GET https://openrouter.ai/api/v1/models`
  and filter pricing.prompt=="0" and supported_parameters includes "tools").
Reliable autonomous execution needs EITHER a dedicated free tier (Groq / Cerebras / NVIDIA NIM
— own API key, not OpenRouter's shared pool) OR a multi-provider fallback gateway.

## Why OmniRoute was the intended fix (and how to install it)

`diegosouzapw/OmniRoute` is a free AI gateway: one OpenAI-compatible endpoint
(`http://localhost:20128/v1`, `Model: auto`) that aggregates 90+ free providers with
auto-fallback across 237 providers. That directly solves the free-model rate-limit problem.

**Install** on Windows with the same hoisted-linker trick as Paperclip:
```bash
mkdir omniroute && cd omniroute
echo '{"name":"omniroute-local","private":true,"dependencies":{"omniroute":"*"}}' > package.json
pnpm install --config.node-linker=hoisted
```
This avoids the MSYS symlink stall. On a flaky network, add `.npmrc`:
```
fetch-retries=20
fetch-retry-factor=2
fetch-retry-mintimeout=1000
fetch-retry-maxtimeout=60000
fetch-timeout=120000
network-concurrency=4
```

Start via: `node node_modules\\omniroute\\bin\\omniroute.mjs` (port 20128).

### Hoisted-linker startup fix

The hoisted linker has two side-effects that crash the first start:

1. **Missing `package.json`** — `bin/omniroute.mjs` line ~174 reads `join(ROOT, "package.json")`
   (for update-notifier). Create the file:
   ```json
   {"name":"omniroute","version":"3.8.46"}
   ```
   at `node_modules/omniroute/package.json`.

2. **Node 22 blocks `.ts` under `node_modules`** — The binary imports
   `open-sse/utils/setupPolyfill.ts` which throws `ERR_UNSUPPORTED_NODE_MODULES_TYPE_STRIPPING`.
   Fix: convert to `.mjs` (strip TypeScript `as` casts), save as
   `open-sse/utils/setupPolyfill.mjs`, then patch `bin/omniroute.mjs` line 27:
   `await import("../open-sse/utils/setupPolyfill.ts")` → `.mjs`.

Docker alternative: `docker run -d --name omniroute -p 20128:20128 diegosouzapw/omniroute:latest`
(requires Docker Desktop Engine to be running — open the GUI, not just `net start`).

Once running, point Hermes at `http://localhost:20128/v1` for multi-provider fallback.
OpenRouter API keys (`OPENROUTER_API_KEY`) are auto-discovered from the env by Omniroute's
provider key system, or can be added through the dashboard at `http://localhost:20128`.

## Hermes config.yaml is security-sensitive
`hermes config` / `~/.hermes/config.yaml` edits are BLOCKED by the agent sandbox
("Agent cannot modify security-sensitive configuration"). Do NOT try to patch it via the
file tool — set the per-agent model via the Paperclip `PATCH /api/agents/:id` adapterConfig
instead. A global `fallback_model:` in config.yaml is the resilient pattern but must be set
by the user, not the agent.

## Debug loop that actually works
1. `PATCH /api/agents/:id` adapterConfig with `provider`+`model` (correct prefix), `persistSession:false`.
2. `POST /api/agents/:id/heartbeat/invoke` -> get RUN_ID.
3. `GET /api/heartbeat-runs/<RUN_ID>` and read `stdoutExcerpt` — it shows the Hermes transcript
   (model errors, empty responses, "provide the task" = stale session, etc.). Iterate on the model.
4. To test a model directly without Paperclip: `curl -X POST https://openrouter.ai/api/v1/chat/completions`
   with `Authorization: Bearer $OPENROUTER_API_KEY` (key lives in `~/.hermes/.env`) and a
   `tools:` array to confirm tool-call support before wiring it into the agent.
