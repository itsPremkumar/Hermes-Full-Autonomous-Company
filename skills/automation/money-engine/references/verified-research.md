# Verified research bank — money-engine (as of 2026-07)

## Agent frameworks (GitHub API verified, stars / license / last push)
- microsoft/autogen 59.6k CC-BY-4.0 2026-04
- crewAIInc/crewAI 55.2k MIT 2026-07
- langchain-ai/langgraph 36.9k MIT 2026-07
- assafelovic/gpt-researcher 28.2k Apache-2.0 2026-07
- OpenClaw/OpenClaw 382k (NOASSERTION) 2026-07-09 — HUGE, very active
- All-Hands-AI/OpenHands active MIT
- OpenManus/OpenManus active MIT
- browser-use/browser-use 103.8k MIT 2026-07
- n8n-io/n8n 195.7k fair-code 2026-07
- ollama/ollama 175.7k MIT 2026-07
- mudler/LocalAI 47.4k MIT 2026-07
- flowiseai/flowise 54.5k fair-code 2026-07
- langgenius/dify 148.3k fair-code 2026-07
- letta-ai/letta 23.7k Apache-2.0 2026-07
- e2b-dev/e2b 12.9k Apache-2.0 2026-07 (code-exec sandbox)
- Shubhamsaboo/awesome-llm-apps 116.9k Apache-2.0 2026-07
- awesome-selfhosted/awesome-selfhosted 304k 2026-07
- OpenBMB/ChatDev 33.7k Apache-2.0 2026-06
- Significant-Gravitas/AutoGPT 185.4k 2026-07
- vanna-ai/vanna 23.7k MIT — ARCHIVED (avoid)

## India payment providers (live HTTP check)
- Gumroad 200 (MoR, payout PayPal/IN bank, no GST till threshold)
- Polar.sh 200 (MoR, dev-focused, handles GST/VAT)
- Paddle 200 (MoR)
- Lemon Squeezy 301->live (MoR)
- Creem 200 (cards+crypto, dev-friendly)
- Razorpay 200 (INR/UPI, needs KYC+GST — you file)
- Cashfree 301->live, Instamojo 301->live (INR)
- Stripe stripe.com/in 200 (Atlas for IN entities)
Recommendation: Gumroad/Polar (MoR) for products to minimize tax work; Razorpay
only when adding INR SaaS.

## Free deploy platforms (live HTTP 200 unless noted)
GitHub Pages 200, Cloudflare Pages 200, Vercel 200, Netlify 301->live, Render 200,
Fly.io 200, Hugging Face Spaces 200, Supabase 200, Neon 308->live,
Oracle Cloud Free 301->live, Firebase 200, Koyeb 200.

## Scam filtering (always reject)
crypto/DEX-arbitrage, "automatic money" bots, "investment bot", airdrop scam,
ponzi/doubler. GitHub search surfaces many (e.g. Cryptoaj-hack/DFDTOKEN) — keyword-drop.

## Research technique notes
- GitHub search API unauthenticated = 60 req/hr; throttle to ~20/hr, 1 call/90s.
- Raw file fetches (raw.githubusercontent) get 429 — use direct curl HTTP-code
  checks on official pages instead of scraping search captchas.
- `git archive HEAD | tarfile` = clean committed-state verification (strongest proof
  that committed code is green, not just the live working tree).

## CashClaw analysis (user asked to analyze both repos, 2026-07)
- moltlaunch/cashclaw — 1086 stars, TypeScript, MIT. Real autonomous agent on the
  Moltlaunch on-chain marketplace; DEFAULT pays via mltl token. README explicitly says
  "fork it, wire it to Fiverr". -> USE the safe loop pattern, route to Fiverr.
  Implemented as Stream L (service/generate.py, de-crypto'd).
- ertugrulakben/cashclaw — 291 stars, JS, MIT. "OpenClaw skills" on HYRVE AI
  marketplace; pays MPP stablecoin; README uses anonymous "$847 by Monday" /
  "Guard saved $4,700" testimonials. -> REJECT crypto payout for India (taxable,
  volatile, unproven liquidity). Do not route income through it.
- Lesson: harvest agent-loop architecture from crypto-adjacent OSS, but ALWAYS strip
  the token/stablecoin payment layer and replace with free/legal/INR channels.
- Stream L (service/generate.py) = de-crypto'd CashClaw loop -> Fiverr gig drafts.
- Stream M (fiverr/lister.py) = consumes L's gigs, emits one-action Fiverr publish
  packages (service/<slug>.fiverr.md) + content/_fiverr_queue.md (QUEUED/PUBLISHED).
  User pastes each into free Fiverr; Fiverr collects payment. No crypto, no API key.
