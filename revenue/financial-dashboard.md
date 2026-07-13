# PREM AUTONOMOUS CO — REVENUE TRACKING DASHBOARD

**Owner:** Hermes CMO / Hermes Engineer · **Status:** live (tracking artifact)
**Cadence:** updated weekly (every Monday) · **Last updated:** 2026-07-13 (Week 0 / M2 plan set)
**Window tracked:** Month 1 (30-day) projection, from launch 2026-07-12 — **+ Month-2 projection, burn analysis & runway (this section: PRE-73)**
**Source of truth for targets:** `revenue/30-day-zero-cost-launch-plan.md` + `revenue/monetization-brief-revenue-engine-v1.md`
**Burn/runway source of truth:** live Paperclip API telemetry (`/companies/{id}/budgets/overview`, `/costs/summary`) pulled 2026-07-13

> This is a manual tracking doc. Each metric below has a **Target** (from strategy docs) and an
> **Actual** (entered weekly from real dashboards). Do NOT estimate — pull real numbers from the
> sources listed in "Where the numbers come from" and append a row to the Weekly Log.

---

## 1. Month 1 Projection (headline KPIs)

Targets are straight from the launch plan's 30-day KPIs and the monetization brief.

| Metric | Month-1 Target | Actual (Week 0) | Source |
|--------|---------------:|----------------:|--------|
| Calculator / landing visitors | 500 | 0 (not launched) | site analytics |
| Leads captured | 40 | 0 | email/CRM capture |
| Fit calls booked | 12 | 0 | calendar |
| Paid subscribers (starter/team) | 5 | 0 | Gumroad/Stripe |
| Build proposals sent | 3 | 0 | CRM |
| **MRR (month-end)** | **$245** | **$0** | billing |
| Burn / ad spend | $0 | $0 | finance |
| Articles published | 3+ | 3 | see §4 |
| Fiverr gigs live | TBD | 0 | see §5 |

> Note: the monetization brief's conservative month-1 line is **5 starter subscribers = $245/mo**.
> The launch plan's 30-day KPI block matches this. These are the same target stated two ways.

---

## 1b. Month-2 Projection, Burn Analysis & Runway (PRE-73)

> Added 2026-07-13. Targets come straight from `monetization-brief-revenue-engine-v1.md` §6
> (the published 90-day conservative plan). Actuals are pulled from **live Paperclip telemetry**
> (`/companies/3056c999-.../budgets/overview`, `/costs/summary`) as of 2026-07-13T04:39Z.
> Burn reflects the autonomous-company operating cost (model inference via OpenRouter), which is
> the only spend the system tracks today. Human-owned ad/tooling spend stays $0 by policy.

### 1b.1 Month-2 revenue projection (target vs. actual, to be filled weekly)

Month 2 window: 2026-08-12 → 2026-09-12 (30 days after the 2026-07-12 launch).
The strategy doc's conservative month-2 line is **15 subscribers + 1 build = ~$1,240/mo**.

| Metric | Month-1 target | Month-2 target | Month-2 actual (W0 baseline) | Source |
|--------|---------------:|---------------:|-----------------------------:|--------|
| Paid subscribers (starter/team) | 5 | 15 | 0 | Gumroad/Stripe |
| Build proposals closed | 0 | 1 | 0 | CRM |
| **MRR (month-2 end)** | **$245** | **~$1,240** | **$0** | billing |
| One-time build revenue | $0 | ~$990–$4,900 | $0 | billing |
| Affiliate/recurring add-ons | — | (reseller later) | $0 | dashboards |

> At the $49 starter price, 15 subscribers = $735/mo; the brief's ~$1,240/mo assumes a mix of
> starter/team tiers plus the one build. Track the blended figure weekly and reconcile to the brief.

### 1b.2 Burn analysis (live)

Pulled 2026-07-13T04:39Z from the Paperclip budgets/costs endpoints (company scope, calendar-month UTC window 2026-07-01 → 2026-08-01).

| Burn metric | Value | Notes |
|-------------|------:|-------|
| Recognized revenue (M-T-D) | **$0.00** | No revenue events recorded; pre-revenue stage |
| Gross burn (M-T-D) | **$70.00** (7,000¢) | 100% OpenRouter model inference (tencent/hy3:free), attributed to Hermes CMO |
| Monthly budget cap | **$500.00** (50,000¢) | hard-stop policy, calendar-month UTC |
| Budget remaining | **$430.00** (43,000¢) | 14% of cap used; 0 active incidents |
| Net burn (M-T-D) | **$70.00 / mo** | = gross burn (revenue is $0) |
| Burn rate (month-to-date run-rate) | **$6.02 / day** (~$183 / mo) | principled figure: $70 ÷ 11.6 days elapsed — **use this for planning** |
| Burn rate (process-uptime burst) | **$35.53 / hr** (~$852 / day) | artifact of a fresh process started 2026-07-12T13:10Z; **do NOT use for runway** |

> Two rates are shown deliberately. The month-to-date run-rate ($6.02/day) reflects real elapsed
> calendar time and is the planning figure. The process-uptime rate is a burst artifact (all spend
> landed in a ~2h window after the process booted) and overstates burn ~14x.

### 1b.3 Runway update

Runway has two valid definitions; only one is computable from system data today.

- **Runway to budget cap (computable): ~71 days** at the M-T-D pace of $6.02/day against the
  $430 remaining. Comfortably covers the 19.4 days left in the current billing window, so the
  $500 cap will **not** be breached this month. Even at the burst rate it would take ~0.5 day to
  hit the cap — but that rate is not expected to persist.
- **Runway to insolvency (NOT yet computable): undefined.** True runway = cash balance ÷ net burn.
  The company record has `cashBalanceCents: null` and no funding figure is stored anywhere in the
  system. **Gap to close (owner: founder/Prem):** supply a single `cash_balance` input (and any
  committed funding) before "runway in months" can be stated. Until then, runway is reported only
  relative to the budget cap.

### 1b.4 Net position & 2-month picture

| Snapshot | Value |
|----------|------:|
| Cumulative burn (launch → 2026-07-13) | $70.00 |
| Cumulative revenue (launch → 2026-07-13) | $0.00 |
| Net cash impact (launch → now) | **–$70.00** |
| Month-2 revenue target (added MRR) | +$1,240/mo |
| Projected burn if M-T-D pace holds | ~$183/mo |
| Projected net for Month 2 (if targets hit) | **≈ +$1,057** (first net-positive month) |

> Note: the only tracked cost is autonomous agent inference. Human-owned acquisition spend stays $0
> by policy (organic/product-led). If Prem later funds paid acquisition, that must be added to gross
> burn and the budget cap revisited.

---

## 2. Products Published

Real inventory as of 2026-07-13 (from `digital-products/product-catalog.json` and
`income-engine/gumroad/.used_products.json`).

**Cataloged & ready:** 10 digital products.
**Gumroad published (live):** 2.
**Gumroad listings drafted (not yet published):** 5 more.

| # | Product | Price (USD) | Catalog status | Gumroad status |
|---|---------|------------:|----------------|----------------|
| 1 | 50 Viral Short-Form Video Scripts | 12 | ready | drafted |
| 2 | Autonomous AI Agent Operations Playbook | 29 | ready | drafted |
| 3 | Remotion Short-Form Video Template Pack | 19 | ready | drafted |
| 4 | AI-Powered Business Monetization Kit | 29 | ready | drafted |
| 5 | Cold Outreach & Lead Generation Pack | 15 | ready | drafted |
| 6 | Free Job Board Outreach Mastery Guide | 12 | ready | drafted |
| 7 | AI Agent Service Catalog + Pricing Templates | 19 | ready | drafted |
| 8 | 30-Day Zero-Cost Business Launch Plan | 9 | ready | drafted |
| 9 | AI Agent Capability Manifest Toolkit | 14 | ready | drafted |
| 10 | 150 Developer Productivity Prompts | 14 | ready | drafted |
| — | ai-agent-roi-calculator (lead magnet / product) | 0/free | — | **published** |
| — | n8n-starter-workflow-pack | — | — | **published** |

**Total published products:** 2 · **Total cataloged:** 10 · **Bundle price:** $109 (35% saving vs $167 separately).

---

## 3. Sales by Product (revenue)

Baseline = 0. Fill in weekly from Gumroad + Stripe dashboards.

| Product | Units sold | Revenue (USD) | Notes |
|---------|-----------:|--------------:|-------|
| 50 Viral Short-Form Video Scripts | 0 | 0 | not live |
| Autonomous AI Agent Operations Playbook | 0 | 0 | not live |
| Remotion Short-Form Video Template Pack | 0 | 0 | not live |
| AI-Powered Business Monetization Kit | 0 | 0 | not live |
| Cold Outreach & Lead Generation Pack | 0 | 0 | not live |
| Free Job Board Outreach Mastery Guide | 0 | 0 | not live |
| AI Agent Service Catalog + Pricing Templates | 0 | 0 | not live |
| 30-Day Zero-Cost Business Launch Plan | 0 | 0 | not live |
| AI Agent Capability Manifest Toolkit | 0 | 0 | not live |
| n8n-starter-workflow-pack | 0 | 0 | live, no sales yet |
| ai-agent-roi-calculator | 0 | 0 | live, free lead magnet |
| **Total** | **0** | **$0** | — |

**Subscription MRR (service catalog plans):** $0 (no subscribers yet — see §1 paid-subscriber target).

---

## 4. Articles Published & Views

Real articles on disk as of 2026-07-13:

| # | Article | Location | Views | Source |
|---|---------|----------|------:|--------|
| 1 | Best AI Agents for Small Business Automation | `income-engine/content/` | 0 (untracked) | blog |
| 2 | No-Code Automation Tools: n8n, Make, Zapier | `income-engine/content/` | 0 (untracked) | blog |
| 3 | How to Run an AI Company at Zero Budget | `revenue/blog/` | 0 (untracked) | blog |

**Articles published:** 3 · **Total views:** not yet tracked (no analytics connected to the site).
> Action: connect site analytics (GitHub Pages / Vercel / Plausible) and record weekly view counts here.

---

## 5. Fiverr Gigs Live

**Gigs live:** 0 — no Fiverr assets exist anywhere in the repo (no `fiverr` references found).
**Plan:** this is a future channel. Create gigs once the first 2–3 digital products have proof of sale.
Track the count here each week once gigs go live.

| Gig title | Price (USD) | Status | Orders |
|-----------|------------:|--------|-------:|

---

## 6. Leads Generated

**Leads captured:** 0 — the ROI calculator lead magnet exists (`income-engine/gumroad/products/ai-agent-roi-calculator`)
but is not yet wired to an email-capture + CRM, so no leads are recorded.

| Week | Leads (calculator) | Outreach replies | Fit calls booked | Converted to paid |
|------|-------------------:|-----------------:|-----------------:|------------------:|
| W0   | 0 | 0 | 0 | 0 |

---

## 7. Where the numbers come from (pull weekly)

- **Product publish status:** `digital-products/product-catalog.json` + `income-engine/gumroad/.used_products.json`.
- **Sales / revenue / MRR:** Gumroad dashboard + Stripe/Razorpay (founder-managed accounts).
- **Article views:** site analytics (connect if missing).
- **Fiverr gigs / orders:** Fiverr seller dashboard.
- **Leads:** email-capture backend + CRM behind the ROI calculator.

---

## 8. Weekly Log

Append a row every Monday. Keep the latest on top.

| Week of | Products live | MRR | Units sold | Articles | Views | Fiverr gigs | Leads | Notes |
|---------|--------------:|----:|-----------:|---------:|------:|------------:|------:|-------|
| 2026-07-13 (W0) | 2 | $0 | 0 | 3 | untracked | 0 | 0 | baseline; launch 2026-07-12 |
| 2026-07-13 (W1) | 0 | $0 | 0 | 0 | untracked | 0 | 0 | cataloged 11 products incl. agent-sentinel bundle (#11) |

---

*This dashboard is the single source of truth for PRE-59 (Month-1) and PRE-73 (Month-2 projection,
burn analysis & runway). Edit it directly each week; no code changes needed.
Do not auto-publish founder-owned pricing/payment pages — that remains a Prem (founder) decision.*
