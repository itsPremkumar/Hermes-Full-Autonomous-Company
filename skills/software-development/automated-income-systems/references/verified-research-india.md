# Verified research — India, free-first AI income (condensed)

Collected 2026-07 via GitHub API + live HTTP checks during the money-engine build.
Star counts / "live" status are VERIFIED, not invented. Re-confirm fees/KYC at signup.

## Autonomous agent frameworks (GitHub API, verified)
| Repo | Stars | License | Pushed | Local LLM |
|---|---|---|---|---|
| microsoft/autogen | 59.6k | CC-BY-4.0 | 2026-04 | yes |
| crewAIInc/crewAI | 55.2k | MIT | 2026-07 | yes |
| langchain-ai/langgraph | 36.9k | MIT | 2026-07 | yes |
| assafelovic/gpt-researcher | 28.2k | Apache-2.0 | 2026-07 | yes |
| All-Hands-AI/OpenHands | active | MIT | 2026 | yes |
| OpenManus/OpenManus | active | MIT | 2026 | yes |
| browser-use/browser-use | 103.8k | MIT | 2026-07 | yes |
| n8n-io/n8n | 195.7k | fair-code | 2026-07 | self-host |
| ollama/ollama | 175.7k | MIT | 2026-07 | yes (engine) |
| mudler/LocalAI | 47.4k | MIT | 2026-07 | yes (engine) |
| flowiseai/flowise | 54.5k | fair-code | 2026-07 | yes |
| langgenius/dify | 148.3k | fair-code | 2026-07 | yes |
| AUTOMATIC1111/stable-diffusion-webui | 164.0k | AGPL-3.0 | 2026-03 | yes |

Recommended KISS stack for an 8GB laptop: Hermes (orchestrator) + Ollama (local LLM)
+ n8n (glue) + gpt-researcher (research) + browser-use (posting) + Gumroad/Polar (sales).

## Payment providers (India) — live HTTP check
| Provider | HTTP | Best for solo IN dev | Notes |
|---|---|---|---|
| Gumroad | 200 | digital products, payout to PayPal/IN bank | no GST till threshold |
| Polar.sh | 200 | dev-focused Merchant of Record (handles GST/VAT) | best low-friction |
| Paddle | 200 | MoR, handles IN tax | |
| Lemon Squeezy | 301->live | MoR | |
| Creem | 200 | crypto+card, dev-friendly | |
| Razorpay | 200 | INR/UPI, full KYC+GST | you file returns |
| Cashfree | 301->live | INR | KYC |
| Instamojo | 301->live | INR, low friction | KYC |
| Stripe (stripe.com/in) | 200 | Atlas for IN entities; direct IN limited | |
| Paytm/PhonePe/UPI | - | via Razorpay/Cashfree gateway | |

Recommendation: use Gumroad/Polar (Merchant of Record) for digital products - they
collect tax and pay YOU, so you avoid GST filings until you cross the threshold. Use
Razorpay only when adding INR SaaS billing (then you handle GST). Minimizes the human
tax work - the key to "mostly autonomous."

## Free deploy platforms (live HTTP, all 200 unless noted)
GitHub Pages (200), Cloudflare Pages (200), Vercel (200), Netlify (301->live),
Render (200), Fly.io (200), Hugging Face Spaces (200), Supabase (200), Neon (308->live),
Oracle Cloud Free Tier (301->live), Firebase (200), Koyeb (200).
Static+content: GitHub Pages/Cloudflare. App demo: HF Spaces (free CPU).
DB+auth: Supabase free. One API: Render free tier.

## Scam exclusion rule (hard)
Crypto/DEX "arbitrage bots", "automatic money" bots, token-airdrop schemes found on
GitHub are scams or illegal. Deliberately exclude. Build only legal, value-providing
streams. The honest ceiling: a system that collects payments into an Indian bank with
ZERO human intervention is NOT legally possible - KYC, GST, chargebacks, tax require a
human of record. Target ~90% autonomous: agents do research->build->deploy->market->
support->analytics; the user does one-time KYC + monthly GST-if-over-threshold + ~1hr/mo oversight.
