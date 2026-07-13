---
name: openclaw-setup
description: Install, configure, and run OpenClaw (openclaw/openclaw) — a self-hosted multi-channel AI assistant gateway — on a Windows dev box, wired to a FREE OpenRouter model (tencent/hy3:free). Covers the exact config schema (env.OPENROUTER_API_KEY + agents.defaults.model.primary), the reasoning-model token gotcha, where the existing OpenRouter key lives, and the low-RAM boot-failure debugging path (wmic vs /proc, timeout-bounded commands). Use when the user says "install openclaw", "set up the openclaw agent", "run openclaw with my openrouter key", or references openclaw.ai.
---

# OpenClaw setup (Windows, self-hosted, free OpenRouter model)

OpenClaw (`openclaw/openclaw`, npm package `openclaw`, MIT) is a personal AI
assistant gateway you run on your own machine. It speaks to channels
(Telegram/WhatsApp/Discord/Slack/…) and routes agent requests to an LLM. It is
OpenAI-compatible and has **OpenRouter built in**, so a free model
(`tencent/hy3:free`) works with zero paid keys.

This skill was written for a host that already had `openclaw@2026.6.11` installed
globally via npm. Adjust paths if your install differs.

## Environment facts (verified on the build host)

- Node **≥ 22.19 required**. The host had v22.23.1 — fine.
- Global install: `npm install -g openclaw@latest` (or pnpm/bun). Binary:
  `openclaw` → `openclaw.mjs`.
- Config lives at `C:\Users\PREM KUMAR\.openclaw\openclaw.json`
  (`$HOME/.openclaw/openclaw.json` in git-bash).
- Gateway default port **18789**, `bind: loopback`, `auth.mode: token`.
- Telegram channel may already be wired (`channels.telegram`, `dmPolicy: pairing`).
- The user's OpenRouter key is NOT in the shell env — it lives in
  `C:\one\omniroute\start-omniroute.bat` as `OPENROUTER_API_KEY=sk-or-...`.

## Procedure (fresh install on this host)

1. **Install** (if missing):
   ```bash
   npm install -g openclaw@latest
   openclaw --version   # prints e.g. "OpenClaw 2026.6.11 (e085fa1)"
   ```
   Note: `openclaw --help` is heavy (loads every plugin) and may **hang** on a
   memory-starved box — don't use it as a health check. `--version` is light.

2. **Extract the OpenRouter key WITHOUT printing it** (see Pitfalls — never echo
   the secret):
   ```bash
   KEY=$(grep -oP 'OPENROUTER_API_KEY=\K\S+' /c/one/omniroute/start-omniroute.bat | head -1)
   printf '%s' "$KEY" > ~/.openrouter_key
   chmod 600 ~/.openrouter_key
   ```
   Then patch the config with `scripts/setup-openclaw.sh`
   (reads `~/.openrouter_key`, writes `env.OPENROUTER_API_KEY` + sets the primary
   model). Or hand-edit per the schema below.

3. **Config schema** — add/merge into `openclaw.json`:
   ```json5
   {
     "env": { "OPENROUTER_API_KEY": "sk-or-..." },
     "agents": {
       "defaults": {
         "model": { "primary": "openrouter/tencent/hy3:free" },
         "models": { "openrouter/tencent/hy3:free": {} }   // allowlist entry
       }
     }
   }
   ```
   - Model ref is `openrouter/<provider>/<model>` — e.g.
     `openrouter/tencent/hy3:free`. Onboarding default is `openrouter/auto`.
   - Switch later without editing JSON: `openclaw models set openrouter/tencent/hy3:free`.
   - OpenRouter is OpenAI-compatible, so OpenClaw talks to it over the same
     `openai-completions`-style transport.

4. **Boot the gateway** (see Pitfalls for the low-RAM trap):
   ```bash
   openclaw gateway --port 18789
   ```
   Onboarding (`openclaw onboard --install-daemon`) installs a launchd/systemd
   user service so it stays running — preferred if you want 24/7.

5. **Verify the model is reachable** (lightweight, no gateway needed):
   ```bash
   curl -sS -X POST "https://openrouter.ai/api/v1/chat/completions" \
     -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
     -d '{"model":"tencent/hy3:free","messages":[{"role":"user","content":"Reply with exactly: OK"}],"max_tokens":200}' \
     | python -c "import sys,json;print(json.load(sys.stdin)['choices'][0]['message']['content'])"
   ```
   Expect `OK`. This call also confirms the key is valid independent of OpenClaw.

## ⚠️ Reasoning-model gotcha (important)

`tencent/hy3:free` is a **reasoning model**. At low `max_tokens` (e.g. 20) it
spends all tokens on its internal "thinking" (`reasoning` field) and returns
**empty `content`** (`finish_reason: length`). Give it `max_tokens: ~200` so it
actually emits a reply. The OpenRouter API resolves the alias to
`tencent/hy3-20260706:free` (provider: Novita). Within OpenClaw this matters for
agent tasks: very short tool-call expectations may come back empty.

## Pitfalls

### 1. NEVER echo the OpenRouter key
The key is a 73-char `sk-or-...` secret. Extract it to a file with `grep -oP`,
store in `~/.openrouter_key`, and pass it to curl via `$(cat ~/.openrouter_key)`.
Verify success by printing only `len` + 4-char prefix, never the full value.

### 2. Low-RAM boot failure (this host is the poster child)
The box had **~70–150 MB free RAM of 6 GB** with 565 processes (a Paperclip/
Omniroute cluster eats ~100 MB each). Symptoms:
- `openclaw gateway` node.exe **is alive** (via `wmic`) but never binds the port —
  stuck loading plugins.
- `openclaw --help` times out (60s).
- Shell gets `fork: Resource temporarily unavailable` (EAGAIN).

**Debugging path that works on Windows git-bash:**
- Confirm the process is real with **`wmic.exe process where "name='node.exe'"
  get ProcessId,CommandLine`** — `/proc/<pid>/cmdline` does NOT see Windows-native
  node.exe from git-bash, and `tasklist | grep node` is unreliable for cmdlines.
- Check RAM: `grep MemFree /proc/meminfo`. < 200 MB free ⇒ expect hangs.
- **Bound every command with `timeout`** (e.g. `timeout 8 curl ...`) so a hung
  call fails fast instead of eating the 60s tool budget.
- **Avoid deep recursive greps** (`grep -r` over `$HOME`) — they trigger the
  EAGAIN fork failures. Target specific files/dirs instead.
- **Free RAM first**: kill stale `openclaw gateway` procs (`taskkill /PID <n> /F`)
  and any unneeded Paperclip/Omniroute node processes before restarting.
- After freeing RAM, a fresh `openclaw gateway` boots and binds within ~30s.

### 3. Port already in use by a stale gateway
If `netstat -ano | grep :18789` shows LISTENING but it's an OLD config (wrong
model), kill that PID and relaunch — the new process can't bind a taken port and
will silently hang.

### 4. Config not re-read until restart
OpenClaw loads `openclaw.json` at gateway startup. Editing the file does nothing
until you restart the gateway.

## References / templates / scripts

- `references/openrouter-config.md` — full OpenRouter schema, model-ref rules,
  and the key-extraction + config-patch recipe.
- `references/windows-low-ram-debugging.md` — the EAGAIN / wmic / timeout
  debugging path in detail, for any heavy Node CLI on this box.
- `scripts/setup-openclaw.sh` — extracts the key (no echo), patches
  `openclaw.json` (env key + primary model + allowlist), verifies without
  printing the secret.
- `scripts/verify-openrouter.sh` — lightweight probe: confirms the key works and
  `tencent/hy3:free` returns non-empty content at max_tokens=200.
- `templates/openclaw.openrouter.json` — known-good config fragment to merge into
  `openclaw.json`.
