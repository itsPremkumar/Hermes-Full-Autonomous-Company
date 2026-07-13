# Micro-SaaS Pilot Plan ($0, no server)

Pilot idea: **resell access to a free-tier AI API** wrapped with our own tooling —
starting with `agent-caps` (product #9) as the "productized" version, then a hosted
free-LLM proxy concept.

## Why this fits
- bizfina.org (2026): vertical AI micro-SaaS with near-zero marginal cost is the
  ramen-profitable play. We already build tools (agent-caps proves it).
- grizzlypeaksoftware (2026): many AI APIs have free tiers — we can wrap, not host.

## Two zero-infra models (no server, no card)
1. **File-deliverable micro-SaaS**: bundle a tool + setup guide as a Gumroad product
   (already done: agent-caps $14). "Micro-SaaS" without a running server.
2. **API-resale via free tier**: run a thin wrapper on a free-tier host (e.g. a
   serverless free quota) that forwards to a free LLM API. Charge via Gumroad one-time
   or a small monthly. Risk: free tiers have rate limits — scope to low volume.

## Human gates (Charter S0)
- Hosting account (if model 2) = human.
- Payments = Gumroad/PayPal (human, PRE-52).
- No agent stores the principal's payout creds.

## Agent-safe work we can do now
- Write the wrapper code (model 2) as a stdlib-only Python proof-of-concept.
- Document the free-tier limits per provider (research).
- Package as a product when ready.

## Status: PLANNED — not built yet. Next: prototype the free-LLM proxy PoC (agent-safe).
