# Install & Verify Agent Reach (this host)

## Install (NOT on PyPI — clone + editable)
```bash
# repo already cloned at /tmp/agent-reach during analysis; otherwise:
git clone --depth 1 https://github.com/Panniantong/agent-reach.git
cd agent-reach
pip install -e .          # installs agent-reach 1.5.0 + feedparser + yt-dlp
```
Verify: `agent-reach doctor` (prints per-platform channel status + active backend).

## Unlock cheap backends
```bash
# yt-dlp JS runtime (Windows) — REQUIRED or subtitle extraction fails
mkdir -p "$APPDATA/yt-dlp" && printf -- '--js-runtimes node\n' > "$APPDATA/yt-dlp/config"

# Exa full-web search (free, no API key)
npm install -g mcporter
mcporter config add exa https://mcp.exa.ai/mcp
mcporter call 'exa.web_search_exa(query: "test", numResults: 3)'   # should return results
```
Note: `mcporter config add` writes to a project-local `config/mcporter.json` if
cwd is inside a project. Run from `~` so it lands in the home config. doctor may
still flag Exa "broken" — trust the real `mcporter call` (verified working).

## GitHub (optional)
`gh` CLI not installed on this host. Install from https://cli.github.com ; then
`gh auth login` for private repos/issues/PRs.

## Login-gated platforms (per request only)
Tell the agent "帮我配 XXX" (configure XXX). These reuse the user's browser login
state via OpenCLI, or need cookies. Recommend dedicated ALT accounts (ban risk).
Channels: Twitter/X, Reddit, 小红书, Facebook, Instagram, LinkedIn, 雪球, 小宇宙.

## Verified live this session (2026-07-10)
- Web (Jina): 403 on github.com transient (Jina domain rate-limit), fine elsewhere
- YouTube: ✅ (after node runtime fix)
- V2EX: ✅ public API
- RSS: ✅ feedparser
- Bilibili: ✅ search API (curl)
- Exa: ✅ mcporter free search
- GitHub: ⚠️ needs gh
- 8 login-gated: 🔒 not activated
