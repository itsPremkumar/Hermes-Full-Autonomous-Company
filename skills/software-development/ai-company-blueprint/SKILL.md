---
name: ai-company-blueprint
description: Research and assemble a fully open-source, AI-agent-operated company stack. Use when the user wants to build an autonomous or one-person AI company, map business departments to free self-hostable tools, compare agent frameworks (CrewAI, OpenHands, MetaGPT, AutoGen, LangGraph, OpenClaw), or produce a department-to-tool blueprint folder. Triggers include "AI company", "autonomous company", "agent-operated business", "open-source stack for a department", "which tool for this team", "map every department to a project".
---

# AI-Company Blueprint (open-source agent stack)

## When to use
- User wants to build or plan an AI-operated / one-person company using open-source tools.
- User gives a department/team list and asks to map each to a free, self-hostable project.
- User asks to compare agent frameworks (OpenClaw, CrewAI, OpenHands, Paperclip, MetaGPT, AutoGen, LangGraph).
- User wants a blueprint folder with one file per department and verified project links.

## Core method
1. Discover + verify, never assert from memory. For each tool, hit the GitHub repo API for live star count + license, and confirm the URL returns HTTP 200. See references/open-source-stack-map.md for the curated, already-verified map (update it as you verify new repos).
2. Department-to-tool blueprint. For each department write a file with: Role, Recommended projects (name, stars, license, link), Why this tool, Integration. Use templates/department-blueprint.md.
3. Verify all links in the folder with scripts/verify_links.py — it scans .md for github.com/owner/repo, checks 200 + prints current stars. Run it; do not hand-type curls.
4. Tier the org. Do not build 60 departments. Lead with a 7-agent MVP (CEO/COO/Research/SWE/Marketing/Sales/CFO) then expand. See the map.

## Agent frameworks (the "hands") — verified this session
| Framework | stars | License | Role |
|---|---|---|---|
| CrewAI | 55.3k | MIT | Role-based company (CEO/CFO/CMO agents) |
| OpenHands | 80.3k | Open | Autonomous software engineering |
| MetaGPT | 69.3k | MIT | Whole AI Software Company in a box |
| Microsoft AutoGen | 59.6k | CC-BY-4.0 | Multi-agent conversation / research |
| LangGraph | 37k | MIT | Resilient production workflows |
| OpenClaw (Hermes 212k) | MIT | Agent templates + runtime (swarmclaw, mission-control) |
| claw-empire | 1.3k | Apache-2.0 | CEO Desk orchestration |
| **Paperclip** (`paperclipai/paperclip`) | ~73.4k | MIT | **Production** agent-company orchestrator — org chart, budgets, goals, heartbeats, ticket system. Ships the Hermes adapter in `main` (`hermes_local` + `hermes_gateway`). The real "run an AI company" engine. See references/paperclip-hermes-runtime.md. |
| Paperclip Maximus | none | concept | WARNING self-improving-agent idea, NOT a production tool. R&D only. |

## Self-evolving core (the user's #1 emphasis — "self-improving company")
A company that *improves itself* needs a 4-layer brain, NOT just an orchestrator:
- **Layer 1 (brain, self-improving):** **Hermes** (this agent — "grows with you", only purpose-built self-improving agent = the MAIN POST) + `mem0ai/mem0` (60.5k★, memory evolution) + `getzep/graphiti` (28.6k★, knowledge-graph evolution).
- **Layer 2 (autonomy):** `Viku-AI/agent-zero` (spawns/modifies its own sub-agents & tools at runtime).
- **Layer 3 (orchestration):** claw-empire (CEO desk) + CrewAI (roles) + LangGraph (resilient flows).
- **Layer 4 (domain):** Agent-Reach (research), OpenHands (coding), your Video-Gen (product).
- **Reality check:** true self-evolution (agent rewrites own source → verifies → redeploys) is still research-grade. Hermes+Mem0 is the practical start; AgentZero adds autonomy. Combine, don't bet on one. **Paperclip Maximus = concept only**, never production.
- **How Hermes is controllable:** expose Hermes as a callable tool (MCP server, like your Video-Gen's MCP) so orchestrators (CrewAI/claw-empire) can command it.

## Compulsory baseline (the "default 20-project set every company must have")
User wants a STANDARD set present in EVERY company deployment, industry-agnostic, domain tools added ON TOP. The 20:
Keycloak, Infisical, PostgreSQL, MinIO, Docker+Coolify, Prometheus+Grafana+Loki, NATS, ERPNext, Postal+Listmonk, Outline+OpenWebUI, Mem0+pgvector, n8n, Hermes+CrewAI+LangGraph, Agent-Reach+SearXNG, Chatwoot, Matomo, Gitea+Forgejo, Plane, Wazuh.
- **For a NON-AI company:** drop the 3 AI-only (Mem0/pgvector, orchestration, research) → 17 universal.
- **For an AI company:** keep all 20.
- This is the "operating system of the company" — always present; domain tools (e.g. your Video-Gen, Medusa) layer on top.

## OpenClaw / ClawHub ecosystem (verified this session)
- `openclaw/openclaw` — **382.5k★** — "Your own personal AI assistant. Any OS. Any Platform." The main assistant.
- `openclaw/clawhub` — **9.1k★** (TypeScript) — **Skill + Plugin Registry** → clawhub.ai. The "app store for agents."
- ClawHub trending skills are exactly self-improving/memory/security-vetting (self-improving agent, Skill Vetter, ontology, SkillScan) — plug directly into the self-evolving core above.
- Adjacent: `NousResearch/hermes-agent` (212k★, same philosophy), `nanoclaw` (30k★), `zeroclaw` (32k★), `garrytan/gbrain` (25.8k★, "OpenClaw/Hermes Brain").
- Cautions: huge/fast-moving (382k★); some org repos tiny/experimental (crabhelm 2★) — vet before prod. ClawHub skills community-contributed → **always vet via SkillScan/Skill Vetter** before install.

## Product angle (what the coding/product dept BUILDS & SELLS)
The blueprint isn't just tools — it's products to sell. Tiered catalog:
- **Tier A digital:** faceless videos (your Video-Gen), prompt packs, eBooks, stock assets (ComfyUI), browser extensions, mobile utilities.
- **Tier B SaaS:** micro-SaaS, AI chat/RAG (OpenWebUI+Mem0), niche CRM, automation bots, lead-gen.
- **Tier C client work:** custom dev, websites, mobile apps, MCP servers (cash flow while SaaS ramps).
- **Tier D OSS:** dev tools, agent templates, self-hosted SaaS alternatives (stars → sponsors/Pro).
- Recommended first product = your `Automated-Video-Generator` (already built, MCP-ready); prove the loop before building new.

### Agent-artifact → digital product pipeline (package what agents already built)
When the company's agent has produced artifacts (playbooks, scripts, pricing docs, outreach sequences), convert them into sellable digital products rather than generating from scratch. Workflow:

1. **Audit existing artifacts** — scan the agent's output directories, Paperclip attached work-products, and completed issues for well-structured content. Each standalone deliverable (playbook, script set, pricing table, launch plan) is a candidate product.
2. **Define product line** — group into a coherent catalog. Each product needs: title (descriptive + search-friendly), tagline (one-liner value prop), price ($9–$29 impulse-buy range), category (Content, Business, Marketing, Templates), and file formats (.md, .pdf, .csv, .json).
3. **Write product description** — create a README.md per product with: what it is, what's inside, sample excerpt, format specs, pricing. Use the company's existing proof ("Used to launch an autonomous AI company") as social proof.
4. **Package deliverables** — create downloadable ZIP files per product (Python zipfile since `zip` may not be on the host). Also create a master bundle ZIP with all products at ~40% discount.
5. **Build a store landing page** — static HTML page (GitHub Pages /docs) listing all products with prices, badges, grid layout, and bundle CTA. Dark-themed, responsive, links to Gumroad or Ko-fi.
6. **List on marketplace** — Gumroad or Ko-fi (both free, worldwide payments + VAT + delivery). Signup may be bot-detected; provide user with per-product ZIP + description text + price. They can paste into Gumroad's create-product form in ~2 min per product.
7. **Set catalog pricing** — $9 (lowest friction) to $29 (premium single). Bundle all at $99 (35–40% discount). 5+ products across multiple niches makes the bundle feel like a complete toolkit.

**Key differences from `automated-income-systems`'s Gumroad factory (Stream B):**
- Stream B generates NEW templated products from a `generate.py` script (Notion templates, prompt packs).
- This pipeline repackages EXISTING real agent-produced artifacts — they already have proven value.
- Use BOTH: Stream B for automated bulk generation; this pipeline for premium assets from actual operations.

**Pitfalls:**
- Free stock media (AVG Openverse fallback) is unreliable for video products. Pexels/Pixabay API keys needed for polished renders (free registration).
- Bot detection on Gumroad/Ko-fi signup pages makes automated listing infeasible. Provide files/instructions for manual paste.
- Don't overload product ZIPs — 1-3 files max per product plus README.
- Price anchor: all $9–$29 with $99 bundle (40% savings) feels real; avoid individual prices close to bundle price.

## Web intelligence / crawling layer (verified this session)
For internet research + lead discovery the winning combo is AI-native crawlers (clean Markdown/JSON, LLM-ready), NOT legacy scrapers:
| Tool | stars | License | Role |
|---|---|---|---|
| Firecrawl | 148.8k | AGPL-3.0 | AI web search/scrape/extract, JS sites, MCP, Docker — TOP pick |
| Browser Use | 104.1k | MIT | AI browser control, logins, form-filling |
| Crawl4AI | 72.2k | Apache-2.0 | Local-first crawling, LLM-ready Markdown, RAG |
| Agent-Reach | 54.3k | MIT | Internet + social intelligence, zero API fee |
| SearXNG | 33.7k | AGPL-3.0 | Private metasearch engine |
| Scrapy | 63.1k | BSD-3 | Large-scale structured crawling |
| Playwright | — | Apache-2.0 | Reliable browser automation |
Recommended stack: Agent-Reach (research) + Crawl4AI (local) + Firecrawl (AI extraction) + Browser Use (interactive) + Playwright + SearXNG. See references/web-crawlers.md.

## Pitfalls
- Paperclip Maximus is a concept, not a tool. No canonical high-star repo. Never put it in core ops; flag as experimental/R&D.
- License "NOASSERTION" (OpenHands, mautic, nocobase, automatisch, grafana) = open-source but NOT an OSI-approved license. Still free/self-hostable; note it is not MIT/Apache.
- Star counts drift. Re-verify via API before publishing a blueprint; the map is a snapshot.
- **GitHub unauthenticated API rate-limit is HARD, not gentle.** This session proved: after ~20-30 calls the API returns HTTP 403 for ALL subsequent /repos/* and /search/* calls for the rest of the session — `sleep` + a `User-Agent` header did NOT clear it. When you hit 403:
  1. Stop hammering (more calls just extend the block).
  2. Use the repo's **canonical path** you already know (owner/repo) and label it `(canonical)` in the deliverable — do NOT fake a star count.
  3. Be explicit: "✅ verified live this session" vs "(canonical) not re-verified due to rate limit." The user values honesty over completeness here.
  4. Optionally retry the unverified ones in a LATER session once the limit resets.
  `scripts/github_verify.py` encodes this: it catches 403, prints "RATELIMITED" for that repo, and never invents numbers.
- Prefer repo-API (`/repos/owner/name`) over `/search/repositories` — search is more aggressively rate-limited and returns fewer fields.
- HTTP-200 means the repo exists, not that it is healthy. Check stars/license/last-push.
- **Mature > experimental.** User explicitly prefers production-ready OSS (Agent-Reach, ERPNext, n8n, Mautic, OpenHands, CrewAI, LangGraph, **Paperclip**) over small/experimental repos. Keep a separate "Treat cautiously" list (ringback, AIReceptionist, auto-company, swarmclaw, markus-small, **Paperclip Maximus**) — fine for R&D, never core ops.
  - **Correction (2026-07-12):** `paperclipai/paperclip` is a REAL, production orchestrator (~73.4k★, MIT), NOT a concept. Only "Paperclip Maximus" (no canonical repo) is the concept/R&D idea. Do not confuse the two. Paperclip is the recommended way to actually *run* an agent company and ships a Hermes adapter in `main`. See references/paperclip-hermes-runtime.md for the install/run recipe.
- Exhaustive detail is wanted for THIS artifact. The user explicitly asks for "every department, every relevant project link, every detail." For blueprint/research deliverables be thorough (full tables, all links, stars, licenses) — this OVERRIDES the usual concise-chat preference for this artifact class. Chat replies stay concise; the blueprint files are exhaustive.

## Support files
- references/open-source-stack-map.md — full department-to-tool map with verified stars/license/links (condensed knowledge bank).
- references/web-crawlers.md — verified web-intel/crawler picks (Firecrawl/Crawl4AI/Browser Use/etc.) + recommended combo.
- references/paperclip-hermes-runtime.md — CONCRETE install/run recipe for a Paperclip company that employs Hermes (`hermes_local` vs `hermes_gateway`, native run w/ embedded Postgres, pnpm + Docker pitfalls, API seed).
- references/digital-product-catalog.md — template for packaging agent artifacts into sellable digital products (product line structure, catalog JSON schema, ZIP packager code, store page HTML recipe, pricing guidelines).
- templates/department-blueprint.md — copy-modify starter for one department file.
- scripts/github_verify.py — scan a folder's .md for github.com/owner/repo, call /repos API, print stars+license, mark 403 as RATELIMITED (never invents numbers). Run it; do not hand-type curls.

## Related
- automated-income-systems overlaps on the GitHub repo-discovery recipe + income angle — reuse its references/github-repo-discovery.md for the curl recipe. (Note to curator: these two skills share repo-discovery; consider consolidating the recipe.)
