# 🚀 Go-Live Checklist — Clear the 3 Human Gates

The autonomous system is **built, verified, and deploy-ready**. It cannot cross
these 3 gates itself (legal/UI gated to a human). Your total manual effort: ~15 min.

---

## Gate 1 — Marketplace accounts (~5 min)
- [ ] Create Fiverr account → https://www.fiverr.com → "Join"
- [ ] Verify email + phone (ID check if prompted)
- [ ] Create Upwork account → https://www.upwork.com → "Sign Up"
- [ ] Complete profile (use `money/listings/` copy as bio)

## Gate 2 — Payment linkage (~5 min)
- [ ] **Direct Indian payments (UPI):** your receiving address is
      **`premkumar016555@oksbi`** (Google Pay / any UPI app). Share this with
      Indian clients who pay directly instead of through a marketplace.
- [ ] Fiverr: Profile → Earnings → Payout method → link PayPal or bank
- [ ] Upwork: Settings → Get Paid → add PayPal/bank + tax form (W-8BEN for non-US)
- [ ] Confirm a test payout method is "Active"

> Payment destinations are documented centrally in `money/PAYMENT.md`.
> Do NOT paste your UPI ID into the 50 `listings/*.md` files — those are
> marketplace gigs (Fiverr/Upwork handle payment internally).

## Gate 3 — First gig live (~5 min)
Pick the highest-margin, fastest-deliverable package:
**SEO/Audit Reporter — starter ($49/mo)** or **Invoice Automation — starter ($49/mo)**.

1. Open `money/listings/audit_packs/starter.md` (or `invoice_packs/starter.md`)
2. Copy the **title + "What you get" + FAQ** into the Fiverr gig creator
3. Set price = the price in the listing
4. Add the tags listed
5. Click **Publish**
6. Repeat on Upwork as a "Fixed-Price" job

→ System is now earning. The Moltbook scheduler (3-min cadence) keeps the
acquisition funnel full via the 12 drafts in `revenue/moltbook/post-*.json`.

---

## After go-live — optional scaling
- [ ] Deploy `infra/docker-compose.yml` on a $5-20/mo VPS → `docker compose up -d`
- [ ] Import each package's `n8n_workflow` into n8n (localhost:5678)
- [ ] Set env vars (`$env.MAPS_KEY`, etc.) in n8n Credentials
- [ ] Activate workflows → delivery runs automatically
- [ ] Add more gigs from `money/listings/` (all 50 are ready)

## Verification you can run anytime
```
cd money
python run_all.py self-test    # 12 pipelines, 50 packages
python generate_listings.py   # refresh 50 listings
python generate_moltbook_drafts.py  # refresh 12 promo drafts
```
