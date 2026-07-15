# Zero-Investment AI Company — Free Stack Setup

> **Purpose:** a complete, fully-documented blueprint for running an **autonomous AI "money-earning
> machine" company at $0 cash investment**. Covers (1) free AI model providers (no paid API key),
> (2) a free domain, (3) free compute / deploy / DB / email / payments, and (4) how the automation
> stack (Hermes → Paperclip → OpenClaw + OmniRoute) wires it all together.
>
> Companion to `Hermes-Full-Autonomous-Company` (OS source of truth) and
> [OmniRoute](https://github.com/diegosouzapw/OmniRoute) (free AI gateway).

---

## 🎯 Why this document exists (zero-budget money machine)

We are building a fully autonomous company under a **$0 budget** — no paid API keys, no subscriptions,
no upfront cash. The largest recurring cost for any AI company is **LLM inference**; the second is
**hosting/domain/payments plumbing**. This document proves every one of those has a **free option**,
so the company runs end-to-end at net-zero cash outlay.

Canonical stack (per the company CONSTITUTION):

```
Hermes  (first boss — self-improving orchestrator, commands Paperclip + OpenClaw)
  └─ Paperclip  (ops company: budgets, agents, heartbeats)
       └─ OpenClaw  (channel: phone/Telegram, draft-only, no file persistence)
  └─ OmniRoute  (free AI gateway — one endpoint, 250+ providers, free pools)
```

---

## 🔑 Golden rule — ALWAYS verify against the latest docs

Free tiers, domains, rate limits, and provider Terms of Service **change constantly**. Before relying
on anything below, re-check the live sources of truth:

1. **OmniRoute latest free catalog** (canonical, machine-readable):
   `open-sse/config/freeModelCatalog.data.ts` on
   [github.com/diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) →
   `open-sse/config/freeModelCatalog.data.ts`, plus `docs/reference/FREE_TIERS.md`.
2. **That specific provider's latest official docs** (base URL, auth method, current limits, ToS).
3. **FreeDomain latest** — [github.com/DigitalPlatDev/FreeDomain](https://github.com/DigitalPlatDev/FreeDomain)
   and the dashboard at <https://dash.domain.digitalplat.org/> (TLDs and rules change).

> Treat every ID, URL, and limit here as a **snapshot** (OmniRoute refresh 2026-06-17, shipped
> v3.8.40+). Re-verify before production use.

---

# 1️⃣ Free AI model providers (no paid API key)

Full model-by-model catalog lives in **[`docs/free-ai-providers.md`](./free-ai-providers.md)** (also in
the standalone repo `omniroute-free-ai-providers`). Summary:

## 🟢 Tier A — truly no sign-up, no API key (anonymous)

Works with **zero account**. ~80+ models across 12 provider families.

| Provider | `tos` | Models | Notes |
| --- | --- | --- | --- |
| **Pollinations** | caution | ~24 | Multimodal, anonymous, rate-limited (~1 req/6–15s) |
| **Puter** | caution | 33 | GPT-5.x, Claude Opus/Sonnet, Gemini, Grok, Perplexity, Llama, Mistral, Qwen |
| **Z.AI / GLM-CN** | **ok** | 3 | GLM-4/4.5/4.7-Flash — cleanest free-forever terms |
| **OpenCode Zen** | caution | 6 | Best free *coding* models (DeepSeek V4 Flash, Nemotron 3, MiMo V2.5) |
| **Kilo-gateway free** | caution | 7 | Rotating auto free set (Nemotron, StepFun, Poolside, Nex) |
| **SiliconFlow** | caution | 10 | DeepSeek R1/V3, Qwen3, Kimi K2.5 (free account, no paid key) |
| **Tencent Hunyuan** | caution | 1 | `hunyuan-pro` (free since 2024) |
| **Baidu ERNIE** | caution | 1 | `ernie-4.0-8k` |
| **UncloseAI / Liquid / Reka / StepFun / SenseNova** | caution/ok | ~8 | Smaller free model sets |

## 🟡 Tier B — keyless but REQUIRES a host login/cookie (not "no sign-in")

Marked `keyless` by OmniRoute but needs a signed-in session. **Avoid in the production pipeline**
(host ToS bans proxy use): Antigravity (`agy`), Qwen-web, Muse/Meta, DuckDuckGo, Blackbox, OpenCode
(GitHub login), Friendliai, iFlytek, Coze, NLPCloud, etc.

**Two usage paths (both documented in the catalog):**
- **With OmniRoute** — single `http://localhost:20128/v1` endpoint, `model: auto`. Recommended.
- **Without OmniRoute** — call each provider's free endpoint directly (e.g. Pollinations
  `https://text.pollinations.ai/v1/chat/completions`, anonymous). Verify current URLs in provider docs.

---

# 2️⃣ Free domain

## DigitalPlat FreeDomain 🌐

> Repo: **[github.com/DigitalPlatDev/FreeDomain](https://github.com/DigitalPlatDev/FreeDomain)**
> (AGPL-3.0, 185k+ stars, 500k+ domains registered)
> Dashboard: <https://dash.domain.digitalplat.org/>

A free, no-strings-attached domain platform — "free domain for everyone." Register a unique domain and
host it on your favorite DNS provider (Cloudflare, FreeDNS/Afraid.org, Hostry).

**Available free extensions (verify current list in the repo — more coming):**

- `.dpdns.org`
- `.us.kg`
- `.qzz.io`
- `.xx.kg`
- `.qd.je`

These replace the paid `$8–15/yr` domain purchase entirely. For a zero-investment company, use one of
these instead of buying a domain. (Your existing `www.sproutern.com` is a paid domain; the company can
use a free `.us.kg` / `.dpdns.org` while keeping paid branding optional later.)

### Other free-domain options (no purchase)

| Option | Free? | Notes |
| --- | --- | --- |
| **DigitalPlat FreeDomain** | ✅ | `.dpdns.org`, `.us.kg`, `.qzz.io`, `.xx.kg`, `.qd.je` |
| **Free subdomains** | ✅ | `*.vercel.app`, `*.pages.dev`, `*.github.io`, `*.onrender.com`, `*.fly.dev` |
| **Paid domain** | ❌ ($8–15/yr) | Only if branding/email requires it — skip-able |

DNS hosting for the free domain is free via **Cloudflare** (also gives free SSL/TLS + proxy).

---

# 3️⃣ Full zero-cost setup map (paid → free)

Every normally-paid line item and its free replacement:

| # | Normally costs | Free option | How it applies |
| --- | --- | --- | --- |
| 1 | **24/7 compute / VPS ($4–10/mo)** | **Oracle Always-Free ARM** — 4 ARM cores + **24GB RAM** + 200GB disk, permanent free (no expiry). Also fly.io / Render free tier, or your own PC (electricity only). | ⚠️ **Key constraint:** your Windows box is ~6GB RAM with ~100MB free and 565+ procs; Paperclip + OmniRoute each ~100MB and Node CLIs already hang/fork-fail there. Not viable for 24/7. **Oracle ARM (24GB, $0)** is the practical free host. Needs a card for identity check but never charges. |
| 2 | **Domain ($8–15/yr)** | **DigitalPlat FreeDomain** (`.us.kg`/`.dpdns.org`/etc.) or free subdomains | See §2. |
| 3 | **Payment processor (Stripe 2.9%+$0.30, Gumroad 10%)** | **Gumroad free plan** (10% only on sales, no monthly) · **Stripe** (per-txn, no monthly) · Ko-fi/Patreon free | Fee taken **from revenue, not your pocket**. Gumroad = lowest friction for a solo maker. |
| 4 | **Outbound proxy/VPN ($0–10/mo)** | Free until it breaks — your own IP first; Cloudflare WARP (free) | Only if a free provider geo-blocks. Start $0. |
| 5 | **Anti-bot / scraping (Browserbase $10+/mo)** | Local/stealth browser automation (OmniRoute TPROXY MITM, headless on free ARM) | Only for heavy web automation; light use = $0. |
| 6 | **Transactional email ($0–20/mo)** | **Skip** → **Telegram bot** for alerts (free). Or Brevo/Resend free tier. | Your stack already uses Telegram/OpenClaw. No paid email needed. |
| 7 | **Hosted DB upgrade (Supabase/Neon paid)** | **SQLite** (local, $0) or Neon/Supabase free tier | OmniRoute + Paperclip use SQLite/local DB. Free tier enough early. |
| 8 | **Business registration / legal ($0–100)** | **Skip until earning** — earn as individual via Gumroad/Stripe to personal payout | LLC/trademark optional later, not an upfront investment. |
| 9 | **Ads / marketing ($)** | **100% free organic** — X/Twitter, Moltbook, Reddit, Product Hunt, LinkedIn, GitHub README | You're already on X and announce to Moltbook. Organic = $0. |
| 10 | **Your time** | Replaced by **automation** (the company itself) | The point: Hermes/Paperclip automate the work. |

### The only money that ever leaves your pocket
1. **Electricity** if you run it on your own PC (unreliable there) **or** a small VPS if you want
   reliability — but **Oracle ARM removes even that**.
2. **Payment processor fees** — taken from revenue, not savings.

➡️ **A complete $0-cash AI company is real**, provided you host on a free-tier machine (Oracle ARM)
instead of the RAM-starved laptop.

---

# 4️⃣ Money-earning automation stack (zero cost)

How the pieces fit into an autonomous, self-funding loop:

```
                 ┌─────────────────────────────────────────────┐
                 │  FREE HOST: Oracle Always-Free ARM (24GB)     │
                 │  FREE DOMAIN: <company>.us.kg (DigitalPlat)  │
                 │  FREE DNS+SSL: Cloudflare                     │
                 └─────────────────────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▼                         ▼                         ▼
   Hermes (boss)            Paperclip (ops)          OmniRoute (AI gateway)
   - planning               - agents/budgets         - one endpoint
   - documentation          - heartbeats             - Tier-A free models
   - coordination           - money tracking         - model: auto routing
        │                         │                         │
        └─────────────────────────┴─────────────────────────┘
                                  │
                                  ▼
                     OpenClaw (channel: Telegram/X)
                                  │
                                  ▼
                     EARN → Gumroad/Stripe (fee on revenue only)
                                  │
                                  ▼
                     Reinvest $0 (already free) — profit = net
```

### Routing rule (from `docs/model-registry.md`)
1. Start local / free. 2. If code-heavy/vision/reasoning → escalate to Tier-A free model via OmniRoute.
3. Log chosen actor + token cost (should be $0) so routing improves. 4. Never hardcode a single paid
model — the OS is model-agnostic.

### What actually earns (zero upfront)
- **Digital products** on Gumroad (templates, ebooks, AI tools, skill packs) — list free, sell, pay 10% only on sales.
- **ClawHub skills/products** you already ship (30+), published free, monetized via Gumroad/Stripe.
- **Content/announcements** on X + Moltbook (organic, free) driving traffic to the free-domain landing page.
- **Automation services** (the company builds & sells automations) using free models end-to-end.

---

# 5️⃣ Quick-start (free, end-to-end)

```bash
# 1) Get a FREE domain (no purchase):
#    https://dash.domain.digitalplat.org/  → register <yourco>.us.kg
#    Point DNS to Cloudflare (free SSL + proxy).

# 2) Get FREE compute:
#    Oracle Cloud Always-Free → create ARM VM (4 cores / 24GB / 200GB).
#    (Card only for identity check; never billed.)

# 3) Install OmniRoute (free AI gateway, one endpoint):
#    https://github.com/diegosouzapw/OmniRoute
#    Endpoint: http://localhost:20128/v1   → expose via the free domain + Cloudflare.

# 4) Connect Tier-A free providers (see docs/free-ai-providers.md):
#    Pollinations, Puter, GLM-CN, OpenCode Zen, Kilo-gateway, SiliconFlow...

# 5) Run the autonomous company (Hermes + Paperclip + OpenClaw) on the free ARM box.

# 6) Monetize with ZERO upfront: list a product on Gumroad → pay 10% only when it sells.
```

Example free-model call (anonymous, no gateway):

```bash
curl https://text.pollinations.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"openai","messages":[{"role":"user","content":"Hello from a $0 model!"}]}'
```

---

## Source & license

- **Free AI models:** OmniRoute `open-sse/config/freeModelCatalog.data.ts` (refresh 2026-06-17,
  v3.8.40+). OmniRoute is MIT: <https://github.com/diegosouzapw/OmniRoute>
- **Free domain:** DigitalPlat FreeDomain <https://github.com/DigitalPlatDev/FreeDomain> (AGPL-3.0).
- **Company stack:** `Hermes-Full-Autonomous-Company` (OS source of truth).
- This document is a component of the zero-budget autonomous company stack. Provided for reference
  only; model/domain/limit/ToS details change frequently — always verify against the live catalogs and
  each provider's official terms before building. Not legal/financial advice.
- This document is MIT licensed.
