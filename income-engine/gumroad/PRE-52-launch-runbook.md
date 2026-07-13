# PRE-52 — Gumroad Launch Runbook (HUMAN ACTION REQUIRED)

> ⚠️ This is the ONLY money-moving step. An AI agent cannot do it: Gumroad requires
> your logged-in identity, email verification, and tax/payout linkage. The agent has
> prepared everything up to the publish click. You do the publish + payout linking.

## Agent-complete portion (verified, ready)
7 upload-ready product packages exist under `income-engine/gumroad/products/`, each with
`PRODUCT.md` (deliverable) + `LISTING.txt` (copy-paste Title/Price/Description + steps):

| # | Package | Price | Category |
|---|---------|-------|----------|
| 1 | sales-prompts-pack | $19 | Sales & Marketing Templates |
| 2 | ai-content-machine-blueprint | $47 | Business & Productivity |
| 3 | zero-to-10k-ai-agents | $19 | Technology & Business |
| 4 | ai-agent-roi-calculator | (see LISTING) | Developer Tools |
| 5 | n8n-starter-workflow-pack | (see LISTING) | Automation |
| 6 | dev-prompts-pack | $14 | Developer Tools / Prompts |
| 7 | agent-caps-pack | $14 | Developer Tools / AI Agents |

(Plus 2 more catalog products without separate Gumroad packages yet: product-2-playbook,
product-3-remotion... — package them on demand; the 7 above are the launch set.)

## Your steps (est. 45–60 min for all 7)
1. **Create account** — https://gumroad.com → sign up with business email → verify email.
2. **Link payouts** — Settings > Payouts → connect bank or PayPal. REQUIRED to receive money.
3. For EACH of the 7 packages:
   - Products > New product
   - Copy Name / Price / Category / Description from that package's `LISTING.txt`
   - Add file: upload the `PRODUCT.md` (access = "Software / File")
   - Publish
4. **Verify** — open each public URL; confirm price + download works.
5. Paste the 7 product URLs back here (or in the Hermes chat) so the agent records them
   as `preview_url` work products and closes PRE-52.

## Notes
- Gumroad fee ≈ 10% per sale; no listing cost. You keep the rest.
- No secrets, no API keys, no agent auth needed — this is purely your account action.
- After publish, the autonomy loop can begin driving traffic (SEO blog, social drafts)
  which are agent-safe and already partially in `revenue/`.
