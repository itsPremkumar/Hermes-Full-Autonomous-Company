# Revenue Strategy — Automated & Semi-Auto Channels ($0 stack)

Research date: 2026-07-13. Sources: parmen.net (autonomous affiliate agents 2026),
bizfina.org (AI micro-SaaS zero-funding), easyauthor.ai (affiliate SEO 2026),
realincomelab.com (Fiverr AI 2026), grizzlypeaksoftware (free AI APIs 2026).

## Scoring rubric
- **Automatable %**: how much an agent (Hermes/OpenClaw) can do WITHOUT human action.
- **Human gate**: what still needs the principal (Charter §0).
- **$0-cost**: fits no-cash, low-RAM box.
- **Fit**: works with our existing stack/products.

## Channel scorecard

| # | Channel | Automatable | Human gate | $0 | Fit | Verdict |
|---|---------|-------------|-----------|----|-----|---------|
| 1 | **Affiliate content engine** (SEO blog + affiliate links) | 85% | apply for affiliate programs (approval); disclose links | Yes | High (reuses our blog + products) | **DO NOW** |
| 2 | **Gumroad product sales** (7 packages ready) | 70% | create acct + link payout + publish | Yes | High | **YOU PUBLISH** (PRE-52) |
| 3 | **Micro-SaaS: resell free-tier AI APIs** (wrap + charge) | 60% | hosting (free tier ok), payments = Gumroad/PayPal | Yes | Med (agent-caps shows we can build tools) | **PILOT** |
| 4 | **Fiverr/Upwork gigs (AI services)** | 40% | account + gig approval + deliverables may need review | Yes | Med | Later (low automation) |
| 5 | **Ad revenue (Mediavine/Ezoic)** | 20% | need traffic threshold (10k+ visits/mo) + account | Yes | Low (traffic takes months) | Defer |
| 6 | **Newsletter sponsorship** | 30% | need list size | Yes | Low | Defer |

## Decision
Build in this order (all agent-safe parts now; human gates flagged):
1. **Affiliate content engine** — fully automatable writing pipeline; only affiliate-program
   APPLICATION + link disclosure need the human. Highest ROI per effort on a $0 stack.
2. **Micro-SaaS pilot** — wrap a free-tier AI API (e.g. our agent-caps concept, or a
   free LLM) behind a simple paid access page on Gumroad (no server needed: deliver via
   file + hosted README). Reuses product #9.
3. Keep Gumroad publish as the human step (PRE-52).

## Compliance (non-negotiable, Charter §0.3/§0.4)
- Every affiliate link MUST be disclosed ("I may earn a commission").
- No fake reviews, no income guarantees, no cloaking.
- Only promote tools we actually use / have verified (our §4 tool gate).
- Affiliate IDs are the human's — agent never stores the principal's payout creds.

## Next actions (agent-safe, this turn)
- Scaffold `revenue/affiliate/` engine: topic list + draft generator + disclosure template.
- Add micro-SaaS pilot plan to `revenue/microsaas/`.
- Both committed + pushed; human approves affiliate applications + Gumroad publish.
