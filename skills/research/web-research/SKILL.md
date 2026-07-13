---
name: web-research
description: >-
  Route ALL internet search / research / lookup tasks through Agent Reach
  (agent-reach CLI) — the capability layer that installs, health-checks, and
  routes 15 platforms (Twitter, Reddit, YouTube, Bilibili, Xiaohongshu, GitHub,
  Exa full-web search, V2EX, LinkedIn, Xueqiu, Xiaoyuzhou, Facebook, Instagram,
  RSS, any web page). Use whenever the user asks to research / look up / search
  anything online, shares any platform URL, or wants web intelligence gathered.
  This is the DEFAULT research path for this user (explicit instruction:
  "use agent-reach for all search/research").
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [research, web-search, agent-reach, internet, social-platforms, chinese-platforms]
---

# Web Research via Agent Reach

The user instructed: **for any search or research task, use the Agent Reach
project** (https://github.com/Panniantong/agent-reach) as the primary capability
layer. It is installed locally (recipe in references/install-verify.md).

## Why Agent Reach (not ad-hoc fetching)
Agent Reach is a **capability layer**, NOT a wrapper. It selects, installs,
health-checks, and routes to the most reliable upstream tool per platform
(Jina Reader, Exa, yt-dlp, bili-cli, gh CLI, OpenCLI, ...). It gives curated,
self-healing coverage of platforms Hermes reaches poorly on its own — especially
**Chinese / social platforms** (小红书, Bilibili, 雪球, 小宇宙, Twitter, Reddit,
Facebook, Instagram, LinkedIn). When a platform blocks one method (e.g. Bilibili
banned yt-dlp → switched to bili-cli), the author updates the routing list and
the user does nothing.

Use Agent Reach for **breadth / reading / search** across platforms. Fall back to
Hermes native `browser_*` / `web_extract` for **interactive** work (clicking,
form-filling, logged-in write actions) that Agent Reach explicitly delegates to
BrowserAct.

## When to use
- "research X", "search for X", "what does everyone say about X", "look up X"
- Any platform / URL mentioned: Twitter/X, Reddit, YouTube, Bilibili, 小红书,
  Facebook, Instagram, V2EX, LinkedIn, 雪球, 小宇宙, GitHub, RSS, any web URL
- Multi-platform research → combine Exa + Twitter/Reddit + 小红书/B站, gather in
  parallel, then synthesize

## Workflow
1. **Doctor first for multi-platform tasks**: `agent-reach doctor --json` → read
   each platform's `active_backend`; choose that command group. (Single
   zero-config lookups can skip this.)
2. **Declare the backend**: tell the user "using Agent Reach → X platform / Y
   backend" before acting.
3. **Run the platform command** from the cheat-sheet / references/agent-reach-channels.md.
4. **On failure**: follow the retry chain in references; don't guess commands.

## Verified commands (this environment)
```bash
# Read any web page (Jina Reader; some domains rate-limited → browser fallback)
curl -s "https://r.jina.ai/URL"
# LIVE web SEARCH that actually works here: DuckDuckGo HTML via Jina Reader
Q="fresher AI ML engineer remote India"
ENC=$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$Q")
curl -s "https://r.jina.ai/https://html.duckduckgo.com/html/?q=$ENC" \
  | grep -oE '\[[^]]+\]\(https://duckduckgo.com/l/\?uddg=[^)]+\)' | head -10
# YouTube subtitles / info
yt-dlp --write-sub --skip-download -o "/tmp/%(id)s" "URL"
# V2EX hot
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"
# Bilibili search (no login)
curl -s "https://api.bilibili.com/x/web-interface/search/all/v2?keyword=KEYWORD" -H "User-Agent: Mozilla/5.0"
# RSS
python -c "import feedparser,sys; e=feedparser.parse(sys.argv[1]).entries; print(e[0].title, e[0].link)" URL
```

## Activation state (verified this session)
- **Zero-config, LIVE:** Web page reading (Jina Reader), YouTube (yt-dlp), V2EX, RSS,
  Bilibili search, **DuckDuckGo HTML search via Jina** (this is the working web-SEARCH path).
- **BROKEN here (do NOT rely on):** Exa / mcporter semantic search. `mcporter call
  exa.web_search_exa(...)` fails with "Unknown MCP server 'exa'" and `agent-reach doctor`
  lists Exa as `[X] 未安装` (node runtime broken). The skill's old claim that Exa is
  "zero-config, live" is WRONG in this environment.
- **Needs gh CLI (not installed):** GitHub → fallback to native browser/web_extract.
- **Login-gated (activate on request only):** Twitter/X, Reddit, 小红书, Facebook,
  Instagram, LinkedIn, 小宇宙, 雪球. Activate via "帮我配 XXX" pattern — needs the
  user's browser session or cookies; use **dedicated alt accounts** (ban risk).

## Web search that works (no API key, no Exa)
```bash
q="remote AI ML engineer India work from home salary"
enc=$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")
curl -s "https://r.jina.ai/https://html.duckduckgo.com/html/?q=$enc" \
  | grep -oE '\[[^]]+\]\(https://duckduckgo.com/l/\?uddg=[^)]+\)'
```
Google via Jina is blocked (JS redirect); DuckDuckGo HTML is the reliable free search.
For job boards, append `site:linkedin.com/jobs`, `site:naukri.com`, `site:wellfound.com`,
`site:weworkremotely.com`, `site:remoteok.com` to the query. See references/job-search.md.

## Pitfalls
- **Exa/mcporter is BROKEN in this environment** (`mcporter call exa...` → "Unknown MCP
  server 'exa'"; doctor shows `[X] 未安装`). The old guidance to "trust a real call over the
  probe" is wrong here — trust the probe. Use DuckDuckGo HTML via Jina for live search.
- **yt-dlp needs node JS runtime** on this host: ensure `%APPDATA%/yt-dlp/config`
  contains `--js-runtimes node` or subtitle extraction fails.
- **Jina rate-limits some domains** (e.g. github.com) with a time-boxed 403
  ("AbuseAlleviationError"). Not Agent Reach's fault; retry later or use browser/web_extract.
- **Login-gated platforms carry ban risk** — always recommend alt accounts; never
  the user's main account.
- **Agent Reach is NOT on PyPI** — install from the git clone (`pip install -e .`);
  `pip install agent-reach` fails. Verify with `agent-reach doctor`.
- **Job searching vs job APPLYING (important policy):** Searching the web for openings is
  fine and encouraged. But NEVER build/run a bot that auto-submits applications — LinkedIn,
  Naukri, Indeed ToS forbid it (account ban), CAPTCHAs block scripts, and mass generic applying
  hurts a strong candidate via ATS filtering. For a fresher with real projects, targeted
  apply >> blast. See references/job-search.md for the supported semi-auto workflow.
- **HEADLESS BROWSER REALITY (state up front):** the `browser_*` tools drive a backend
  headless Chromium the USER CANNOT SEE OR TYPE INTO. Never say "log in in my browser" — the
  user can't. Any login-gated flow needs the user to PASTE creds into chat (risky) or be done
  on a no-login board. For job apply, prefer no-login sources (RemoteOK index, RemoteAI) over
  LinkedIn headless login. Details in references/job-search.md.

## References
- references/agent-reach-channels.md — full 15-platform routing table + per-backend
  commands + retry chain
- references/install-verify.md — install from clone, unlock backends (mcporter/Exa,
  yt-dlp node), doctor verification, known pitfalls
- references/job-search.md — live remote/fresher job-search recipe (India) + apply policy
