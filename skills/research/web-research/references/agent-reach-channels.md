# Agent Reach — 15-Platform Routing Cheat-Sheet

Source: https://github.com/Panniantong/agent-reach (MIT, Python 3.10+, ~8.4k LOC).
Capability layer, NOT a wrapper: it selects/installs/health-checks/routes; the
agent calls upstream tools directly. `agent-reach doctor --json` reports the live
`active_backend` per platform.

## Zero-config (live now)
| Platform | Command |
|----------|---------|
| Web page (Jina Reader) | `curl -s "https://r.jina.ai/URL"`  (some domains rate-limited → browser fallback) |
| YouTube subtitles/info | `yt-dlp --write-sub --skip-download -o "/tmp/%(id)s" "URL"` |
| V2EX hot/topics | `curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"` |
| RSS/Atom | `python -c "import feedparser,sys; e=feedparser.parse(sys.argv[1]).entries; print(e[0].title, e[0].link)" URL` |
| Bilibili search (no login) | `curl -s "https://api.bilibili.com/x/web-interface/search/all/v2?keyword=K" -H "User-Agent: Mozilla/5.0"` (full feat: `pipx install bilibili-cli`) |
| Full-web semantic search (Exa, free, no key) | `mcporter call 'exa.web_search_exa(query: "q", numResults: 5)'` |

## Login-gated (activate on request; use ALT accounts — ban risk)
Ordered-backend lists (first usable wins):
- Twitter/X: `twitter-cli` ▸ OpenCLI ▸ bird
  - `twitter search "q" -n 10`  (set TWITTER_AUTH_TOKEN / TWITTER_CT0 or log in to x.com in browser)
- Reddit: OpenCLI (desktop) ▸ rdt-cli (`rdt search "q" --limit 10`)  — no zero-config path
- 小红书 Xiaohongshu: OpenCLI (`opencli xiaohongshu search "q" -f yaml`) ▸ xiaohongshu-mcp ▸ xhs-cli
- Facebook: OpenCLI (`opencli facebook search "q" -f yaml`, `opencli facebook groups -f yaml`)
- Instagram: OpenCLI (`opencli instagram search "q" -f yaml`, `opencli instagram user USER -f yaml`)
- LinkedIn: linkedin-scraper-mcp ▸ Jina Reader
- 雪球 Xueqiu (stocks): login-gated; 小宇宙 Xiaoyuzhou (podcasts → Whisper transcript): login-gated

## GitHub
- Needs `gh` CLI (NOT installed on this host) → fallback to native browser / web_extract.
- Install: https://cli.github.com ; then `gh repo view owner/repo`, `gh search repos "q"`.

## Retry chain (on failure)
1. Run `agent-reach doctor --json` → read `active_backend` for the platform.
2. Try the next backend in that channel's ordered list (e.g. twitter-cli fails → OpenCLI).
3. If all fail: tell user to "configure XXX" (login session / cookies). Never guess commands.

## Notes
- doctor may FALSE-NEGATIVE on mcporter/Exa even when `mcporter call exa.web_search_exa`
  works — trust a real call.
- yt-dlp on Windows needs `%APPDATA%/yt-dlp/config` with `--js-runtimes node`.
- Uninstall: `agent-reach uninstall` (wipes ~/.agent-reach tokens) + `pip uninstall agent-reach`.
