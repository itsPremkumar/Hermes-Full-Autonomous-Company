# Web Intelligence / Crawler Layer (verified)

For an AI-agent company, internet research + lead discovery needs AI-native crawlers that output
clean Markdown/JSON and plug into LLM/RAG pipelines — NOT legacy HTML scrapers.

## Verified picks (live stars, this session)
| Tool | stars | License | Best for |
|---|---|---|---|
| firecrawl/firecrawl | 148.8k | AGPL-3.0 | AI search/scrape/extract, JS sites, MCP, Docker — TOP pick |
| browser-use/browser-use | 104.1k | MIT | AI browser control, login flows, form-filling |
| scrapy/scrapy | 63.1k | BSD-3 | Large-scale structured crawling |
| unclecode/crawl4ai | 72.2k | Apache-2.0 | Local-first crawling, LLM-ready Markdown, RAG |
| Panniantong/Agent-Reach | 54.3k | MIT | Internet + social intelligence, zero API fee |
| searxng/searxng | 33.7k | AGPL-3.0 | Private metasearch engine |
| apify/crawlee | 24.6k | Apache-2.0 | Modern JS crawler, Playwright |
| microsoft/playwright | — | Apache-2.0 | Reliable browser automation, auth, testing |

## Recommended stack for THIS company
| Purpose | Project |
|---|---|
| Internet/social research | Agent-Reach |
| Local crawling | Crawl4AI |
| AI web extraction | Firecrawl |
| Interactive browser | Browser Use |
| Reliable browser | Playwright |
| Private search | SearXNG |

## Notes
- Firecrawl is AGPL-3.0 — fine for self-hosting; if you redistribute a modified version you must
  publish changes. For a purely internal autonomous company this is a non-issue.
- Crawl4AI (Apache-2.0) is the best fully-local option (no external API).
- Agent-Reach covers social/listening + zero API cost — pair with Firecrawl for deep extraction.
- Tier 3 (ScrapeGraphAI, Apache Nutch, Colly, Katana) for specialized/high-scale crawling.
