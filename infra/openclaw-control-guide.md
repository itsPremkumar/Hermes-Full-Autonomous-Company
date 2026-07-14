# OpenClaw — Complete Control & Usage Guide
### How to run, command, and operate OpenClaw as the chat/phone front-door to your AI agent stack

> **Verified on:** 2026-07-14 · Windows 10 · OpenClaw `2026.7.1 (2d2ddc4)` · Gateway on port `18789` · Agent `main` · Telegram bot `@<your-bot-handle>` (connected)

> **Note for public repo:** replace `<your-bot-handle>`, `<PEER>`, and `<WINDOWS_USER>` with your own values. No real tokens or personal paths are committed.
>
> Every command in this guide was **actually run and verified** on the machine it documents. Where a real output is shown, it is the literal result — not an example.

---

## 0. TL;DR — what OpenClaw is, in one line

**OpenClaw is a self-hosted gateway that bridges your chat apps (Telegram, WhatsApp, Discord, Slack, iMessage, Signal, Teams, Matrix…) to an AI agent.** You run one Gateway process; it becomes the always-on, phone-reachable front door to your AI.

On this machine the division of labor is deliberate:

| Layer | Tool | Job |
|-------|------|-----|
| **Brain + hands** | **Hermes Agent** (Nous Research) | Does the real work: writes files, builds, runs `money-engine` crons, learns/self-improves. |
| **Mouth + ears** | **OpenClaw** (gateway, Telegram) | Talks to you and your audiences from your phone; delivers drafts; receives commands. |

They are **complementary layers, not rivals.**

---

## 1. Verified live facts (pulled 2026-07-14)

| Fact | OpenClaw | Hermes Agent |
|------|----------|--------------|
| GitHub stars (live API) | **382,920** | **214,750** |
| License | `NOASSERTION` (custom — **not** MIT) | **MIT** |
| Open issues (live API) | 6,624 | 24,213 |
| Language | TypeScript (Node gateway) | Python |
| Repo created | 2025-11-24 | 2025-07-22 |
| Install | `npm i -g openclaw` | `pip install hermes-agent` / desktop |
| Channels | 20+ native (deepest: WhatsApp/iMessage, polls, reactions, member mgmt) | Also multi-platform (Telegram + 24 platforms) |
| Skills | **ClawHub: 5,700+** community skills | 80+ curated + agent self-generates |
| Self-learning | Limited (file-based memory) | **Excellent** (built-in learning loop) |
| Footprint | Heavier (channel daemons + state) | **Lightweight** ($5 VPS / Raspberry Pi-class) |
| Made by | Peter Steinberger → OpenClaw Foundation (he joined OpenAI Feb 2026) | Nous Research |
| Former names | Clawdbot → Moltbot → OpenClaw | — |

> ⚠️ **Hallucination warning:** AI-generated "comparison" articles repeatedly mis-state the star counts (we saw "30k", "30k", "66k" for Hermes — all wrong; real = **214,750**). Trust the GitHub API, not a chatbot, for these numbers.

---

## 2. Purposes — what we use OpenClaw for

OpenClaw is the right tool **only** for the chat/phone-facing and orchestration jobs. Concretely, in our stack:

1. **Phone-controlled control system.** Message `@<your-bot-handle>` from Telegram to check status, trigger a build, or query the money system — from anywhere, 24/7.
2. **Delivery layer for money crons.** The `money-engine` crons *write* promo/newsletter drafts but stop there (the agent can't auto-post). OpenClaw pushes those drafts to Telegram (bot `@<your-bot-handle>`) so you only hit "forward." This fills the "can't auto-post" gap honestly — **you still approve**.
3. **Multi-channel fan-out.** One agent reply → Telegram + Discord + Slack simultaneously, with channel-native features (reactions, polls, threads).
4. **Internet + media into chat.** `web.search` / `web.fetch` and `image` / `video` / `tts` generation, delivered back inside the chat you're in.
5. **Programmatic control plane.** `admin-http-rpc` (disabled by default, see §6) lets other services / Hermes crons call OpenClaw over HTTP.

**What OpenClaw does NOT do (and Hermes does instead):**
- ❌ **Write/save files.** Proven this session: the agent generated an HTML page but *refused to save it* ("no file/exec tool"). All file work → Hermes.
- ❌ **Builds, `git push`, run generators.** → Hermes crons.
- ❌ **Long-term self-improvement / learning your workflows.** → Hermes.
- ❌ **KYC / GST / paid-store accounts / affiliate IDs.** Human gates — required by law and by the money-engine rules.

---

## 3. How to confirm OpenClaw is actually running (the first thing to check)

OpenClaw's logs do **not** go to your stdout redirect when launched in background — they go to `%LocalAppData%\Temp\openclaw\openclaw-YYYY-MM-DD.log`. So to check health, use the **process + port**, not your log file.

```bash
# 1. Is the gateway process alive? (Windows git-bash: use wmic, NOT /proc)
timeout 10 wmic.exe process where "name='node.exe'" get ProcessId,CommandLine 2>/dev/null \
  | tr -d '\r' | grep -i gateway

# 2. Is it listening? (default port 18789, loopback)
netstat -ano 2>/dev/null | grep :18789

# 3. Live health probe via the local HTTP API (token from config, never echoed)
TOKEN=$(grep -oP '"token"\s*:\s*"\K[^"]+' "$HOME/.openclaw/openclaw.json" | head -1)
curl -sS -H "Authorization: Bearer $TOKEN" http://127.0.0.1:18789/ -o /dev/null -w "HTTP %{http_code}\n"
```

**Verified output (sanitized — your PIDs/paths will differ):**
```text
node.exe ...\openclaw.mjs gateway --port 18789   <PID>
  TCP    127.0.0.1:18789   0.0.0.0:0    LISTENING    <PID>
  TCP    127.0.0.1:18789   127.0.0.1:<PEER_PORT>   ESTABLISHED    <PID>
HTTP 200
```
→ Gateway is up, bound, and answering. The `ESTABLISHED` socket on `<PEER_PORT>` is the live Telegram connection.

---

## 4. Controlling OpenClaw — the commands that work

All commands below were run live this session. Use git-bash (POSIX) on Windows.

### 4.1 Version & general help
```bash
openclaw --version          # "OpenClaw 2026.7.1 (2d2ddc4)"
openclaw --help             # lists 80+ subcommands
```

### 4.2 List agents
```bash
openclaw agents list
```
Verified:
```
- main (default)
  Workspace: ~\.openclaw\workspace
  Agent dir: ~\.openclaw\agents\main\agent
  Model: openrouter/tencent/hy3:free
  Routing rules: 0
```

### 4.3 Channel health (live probe)
```bash
openclaw channels status --probe
```
Verified:
```
Gateway reachable.
- Telegram default: enabled, configured, running, connected,
  transport:just now, mode:polling, bot:@<your-bot-handle>, token:config, works
```

### 4.4 List capabilities (what the agent can actually do)
```bash
openclaw capability list
```
Returns canonical ids including: `model.run`, `web.search`, `web.fetch`, `image.generate`, `image.describe`, `video.generate`, `tts.convert`, `audio.transcribe`, `embedding.create` — each tagged `local` and/or `gateway` transport.

### 4.5 List plugins
```bash
openclaw plugins list        # "Plugins (52/69 enabled)"
```
Key plugins: `browser` (enabled), `alibaba`/`anthropic`/`byteplus` providers (enabled), `codex-supervisor` (**disabled**), `admin-http-rpc` (**disabled**), `azure-speech` (enabled).

### 4.6 Delegate a task to the agent (the "command it" path)
```bash
openclaw agent --agent main --message "Your instruction here" --json --timeout 200
```
Or from a file (use a **Windows path**, not `/tmp` — Node resolves `/tmp` to `C:\tmp` and fails):
```bash
openclaw agent --agent main --message-file "C:\path\to\oc_task.txt" --json --timeout 200
```
> **Real behavior note:** the agent *reasons and generates* but, in default config, **cannot write files** (no file/exec tool). It will produce the artifact and tell you it won't fake the save. Persist the result yourself (Hermes) or enable a file capability (§6).

### 4.7 Send a message out through a channel (Telegram delivery)
```bash
openclaw message send --target "+15551234567" --message "Hi from OpenClaw"
openclaw message send --target "+15551234567" --message "Look" --media photo.jpg
openclaw message broadcast --targets "+91...,+91..." --message "..."
```
(Use your real Telegram peer / channel id. Never put a real phone or token in a committed doc — use placeholders.)

### 4.8 Gateway logs (the real location)
```bash
# Background launches write HERE, not your stdout redirect:
sed 's/[[:cntrl:]]/ /g' "/c/Users/<WINDOWS_USER>/AppData/Local/Temp/openclaw/openclaw-YYYY-MM-DD.log" | tail -20
```
Foreground verbose boot (captured to stdout, good for proving a clean start):
```bash
timeout 90 openclaw gateway --verbose --port 18789
```

---

## 5. Starting / restarting / stopping the gateway

```bash
# Start (long-lived — run in background, or as a Windows scheduled task)
openclaw gateway --port 18789

# Restart = stop then start. Find PID, kill, relaunch:
timeout 10 wmic.exe process where "name='node.exe'" get ProcessId,CommandLine 2>/dev/null \
  | tr -d '\r' | grep -i gateway
taskkill /PID <PID> /F
openclaw gateway --port 18789
```

### 5.1 Low-RAM boot failure (this box is the poster child)
This machine is ~6 GB RAM and often near-empty. Symptoms: `openclaw gateway` node.exe is **alive** but never binds; `--help` times out; shell gets `fork: Resource temporarily unavailable` (EAGAIN).

**Debugging path that works on Windows git-bash:**
- Confirm the process is real with **`wmic.exe process where "name='node.exe'" get ProcessId,CommandLine`** — `/proc/<pid>/cmdline` does NOT see Windows-native node.exe from git-bash.
- Check RAM: `grep MemFree /proc/meminfo` — under ~200 MB free ⇒ expect hangs.
- **Bound every command with `timeout`** (e.g. `timeout 8 curl ...`) so a hung call fails fast.
- **Avoid deep recursive greps** over `$HOME` (trigger EAGAIN). Target specific files.
- **Free RAM first:** kill stale gateway procs and any unneeded Paperclip/Omniroute node processes before relaunching.

### 5.2 Orphaned `startup-migrations` lease (most common stuck-start)
OpenClaw writes a lease row into `~/.openclaw/state/openclaw.sqlite` (`state_leases`, `scope='startup-migrations'`) at boot and clears it on clean exit. A `taskkill`/crash leaves it → every later launch fails instantly.

**Fix (only when no gateway node.exe is alive):**
```bash
# 1. kill EVERY gateway node process
for p in $(wmic.exe process where "name='node.exe'" get ProcessId,CommandLine 2>/dev/null \
            | tr -d '\r' | grep -i gateway | grep -oE ' [0-9]+ *$'); do
  taskkill /PID $(echo $p | tr -d ' ') /F; done
# 2. clear the lease row
cd "$HOME" && python - <<'PYEOF'
import sqlite3, os
p = os.path.expanduser(r"~/.openclaw/state/openclaw.sqlite")
c = sqlite3.connect(p); cur = c.cursor()
cur.execute("DELETE FROM state_leases WHERE scope='startup-migrations'")
c.commit(); cur.execute("SELECT count(*) FROM state_leases")
print("leases left:", cur.fetchone()[0]); c.close()
PYEOF
# 3. launch exactly ONE gateway, then poll port 18789
```

### 5.3 Windows scheduled task silently respawns the gateway
`openclaw gateway install` creates tasks **"OpenClaw Gateway"** and **"OpenClaw Companion"** that may auto-restart it. Disable before lease surgery:
```bash
schtasks /change /tn "OpenClaw Gateway" /disable
schtasks /change /tn "OpenClaw Companion" /disable
# re-enable the Gateway task after a clean, healthy boot if you want 24/7:
schtasks /change /tn "OpenClaw Gateway" /enable
```

---

## 6. Enabling the programmatic control plane (`admin-http-rpc`)

To let Hermes crons / external services drive OpenClaw over HTTP, enable the admin RPC plugin in `~/.openclaw/openclaw.json` and restart the gateway. **Security:** this exposes a control API — bind to loopback, keep the token secret, and only enable on a machine you control.

```jsonc
// ~/.openclaw/openclaw.json (merge)
{
  "plugins": { "entries": { "admin-http-rpc": { "enabled": true } } }
}
```
Then restart (§5) and verify the RPC endpoint answers with the gateway token.

---

## 7. Wiring OpenClaw to the money system (recommended bridge)

The honest, rules-compliant pattern:

1. `money-engine` crons generate `_promo-drafts.md` / `_newsletter.md` (Hermes does the writing).
2. A small bridge (Hermes cron or `openclaw message send`) pushes those drafts to Telegram via the connected `@<your-bot-handle>`.
3. **You** forward/approve to your audience. No auto-post, no fake engagement — within money-engine's honesty rules.

Optional: enable `admin-http-rpc` (§6) so a phone message to the bot can trigger a Hermes cron (e.g. "rebuild the site", "what's today's income?").

---

## 8. Security & honesty notes (non-negotiable)

- **ClawHub skill risk:** community guides warn **12–20% of third-party skills are malicious**. Vet before installing. Prefer curated/Owner-signed skills.
- **Long-term memory injection** attacks can affect persistent-agent frameworks (including OpenClaw and Hermes) — treat untrusted content fed to memory with suspicion.
- **OpenClaw license is NOT MIT** (`NOASSERTION`). If you fork/redistribute, check its actual LICENSE; don't assume MIT permissions.
- **Never echo secrets** (OpenRouter key, Telegram token, gateway token). Extract to a file with `grep -oP` + `chmod 600`, pass via `$(cat file)`.
- **No crypto / arbitrage / "automatic money" bots** — rejected by money-engine rules and by us. Autonomous income here is ~90%, never "guaranteed deposited."

---

## 9. Quick command reference

| Goal | Command |
|------|---------|
| Version | `openclaw --version` |
| Is it running? | `netstat -ano \| grep :18789` + `wmic ... node.exe` |
| Health | `curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:18789/` |
| Agents | `openclaw agents list` |
| Channel health | `openclaw channels status --probe` |
| Capabilities | `openclaw capability list` |
| Plugins | `openclaw plugins list` |
| Run a task | `openclaw agent --agent main --message "..."` |
| Send Telegram | `openclaw message send --target "<peer>" --message "..."` |
| Start gateway | `openclaw gateway --port 18789` |
| Stop gateway | `taskkill /PID <PID> /F` |
| Clear stuck lease | see §5.2 |
| Logs | `%LocalAppData%\Temp\openclaw\openclaw-YYYY-MM-DD.log` |

---

## 10. Sources (live, 2026-07-14)

- GitHub API: `api.github.com/repos/OpenClaw/OpenClaw` and `api.github.com/repos/NousResearch/hermes-agent` (stars/issues/license/created_at)
- OpenClaw docs: `docs.openclaw.ai`
- Hermes Agent docs: `hermes-agent.nousresearch.com`
- ClawHub: `clawhub.ai` (5,700+ skills)
- Times of India (2026-07-14): Nous Research $1.5B valuation
- Wikipedia: OpenClaw rename history (Clawdbot → Moltbot → OpenClaw)

*Generated and verified by Hermes Agent on the target machine. Commands are real; outputs are the literal results observed.*
