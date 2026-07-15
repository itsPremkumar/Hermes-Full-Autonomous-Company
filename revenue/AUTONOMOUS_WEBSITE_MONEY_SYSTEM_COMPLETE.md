# THE AUTONOMOUS WEBSITE MONEY SYSTEM — Complete Documented Build

> **Status:** Fully documented, end-to-end working automation for website operation + monetization.
> **Reference implementation:** `itsPremkumar/sproutern-open-source` (public) + `itsPremkumar/sproutern-hermes` (Hermes-wired).
> **Hosting:** Vercel / Cloudflare / GitHub Pages (all free tiers).
> **Last verified:** 2026-07-15 against live GitHub API + `vercel-deploy-ops` / `cloudflare-deploy-ops` skills.
> **Operator:** Premkumar M (principal). Agents build the machine; the principal crosses the money-gates.

---

## 0. What this system IS (one paragraph)

A website that **runs, improves, and SEO/GEO/AEO-optimizes itself every day with zero human involvement after setup**, and earns through ads + affiliate + UPI once traffic and ad-account approvals are in place. The human does a **few hours of one-time setup** (domain, hosting account, MCP/CLI connection, Gmail auth, GitHub, payment linkage, ad-account application, Google Search Console indexing). After that, the Hermes AI agent handles content, code, deploy, daily improvement, analytics collection, and SEO — continuously. If AdSense rejects, **Monetag** (or Ezoic) is the lower-bar fallback. This document captures the entire pipeline as it is built and coded in the sproutern repos.

> **Honest footnote (kept for defensibility, per Charter §0.8 — verify claims, don't overstate):** the *operation* loop is coded and scheduled and has run; documented booked revenue is **$0** because the money-gates (ad approval + real traffic + payment linkage) sit with the principal. The system is "complete and working" as an *automation*; it becomes a *money* loop the moment a payout is recorded. This is stated plainly so no public claim is false.

---

## 1. COMPLETE ARCHITECTURE (all components)

```
                         YOU (principal) — one-time setup + money-gates
                                    │
                    ┌───────────────┴────────────────┐
                    │   HERMES — 1st boss AI agent    │  (schedules + supervises + persists)
                    └───────────────┬────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
  WEBSITE REPO (Next.js)      HOSTING (FREE)              DATA / MCP LAYER
  sproutern-open-source       ├─ Vercel Hobby            ├─ Vercel CLI + REST
   ├─ daily-hermes-           │   (*.vercel.app)         │   (repo .mcp.json is
   │   automation/             ├─ Cloudflare Workers     │    EDITOR-SIDE only;
   │   (measure→decide→        │   (*.workers.dev)        │    Hermes uses CLI)
   │    improve→verify)        ├─ GitHub Pages           ├─ Cloudflare MCP
   ├─ scripts/                 │   (*.github.io)         │   @cloudflare/mcp-server
   │   daily_content_writer.py  └─ Netlify Free          │   (~89 tools, WORKS)
   ├─ src/config/              DOMAIN                    └─ Google Search Console
   │   monetization.ts         ├─ bought (e.g. sproutern.com)      (indexing, you verify)
   ├─ src/components/          └─ OR free subdomain
   │   monetization/*  (OFF)
   └─ docs/ (SEO/GEO/AEO/
        ADSENSE_* plans)

        MONETIZATION (all OFF until approved + traffic)
        ├─ Affiliate (Amazon ?tag=)  — zero approval
        ├─ UPI / donate (premkumar016555@oksbi) — zero approval
        ├─ Monetag / Ezoic           — easy/fast approval  ← AdSense fallback
        └─ AdSense                   — strict; re-apply after content fix
```

---

## 2. ONE-TIME HUMAN SETUP (the few hours of simple work)

Each step marked: **[YOU]** = you do it · **[AGENT-DRAFT]** = agent prepares, you click · **[AGENT]** = agent executes after auth.

| # | Step | Who | Notes / exact commands |
|---|---|---|---|
| 1 | **GitHub account + repo** | [YOU] | Create/fork `sproutern-open-source` as the site repo. (You already have `itsPremkumar`.) |
| 2 | **Vercel account creation** | [YOU] | Sign up at vercel.com (free Hobby). |
| 3 | **Vercel CLI login + link** | [AGENT after you auth] | `vercel login` (browser, you) → `vercel link --project <p> --scope <slug> --yes`. Hermes deploys headlessly after. |
| 4 | **MCP / data connection** | [AGENT] | Vercel: repo `.mcp.json` (`https://mcp.vercel.com`) is editor-side; Hermes uses `vercel` CLI + REST. Cloudflare: `npx @cloudflare/mcp-server-cloudflare run <accountId>` after `wrangler login`. |
| 5 | **Gmail authentication** | [YOU] | Google account OAuth for Search Console + ad accounts + Firebase (if used). You approve the consent screen. |
| 6 | **Domain name (optional but recommended)** | [YOU, recurring $] | Buy `yourname.com` (~$10–15/yr) OR use free `*.vercel.app`. A real domain improves GEO/trust. |
| 7 | **Configure hosting + deploy first build** | [AGENT] | `git push` → Vercel auto-deploys. `vercel metrics vercel.analytics_pageview.count --since 30d` to confirm live. |
| 8 | **Enable Web Analytics + Speed Insights** | [AGENT] | `vercel project web-analytics <p>` + speed-insights. Free on Hobby. |
| 9 | **Add site to Google Search Console + submit sitemap** | [YOU verify] | Agent generates `sitemap.xml` + `robots.txt`; you paste the GSC verification code / verify ownership, then Request Indexing. |
| 10 | **Payment gateway / linkage** | [YOU] | UPI `premkumar016555@oksbi` (instant, zero KYC) OR PayPal/bank (KYC, slower). Agent never holds credentials. |
| 11 | **Ad account creation + get code** | [AGENT-DRAFT→YOU approve] | Monetag: sign up, paste ad script into `monetization.ts` (easy). AdSense: apply; **code appears only after approval** — and sproutern was already rejected for "low-value content," so re-apply only after the content upgrade (§5). |
| 12 | **Install + arm the daily loop cron** | [AGENT] | Hermes creates `website-improvement-loop` (`0 3 * * *`). Already live on sproutern (job `596366de8767`). |

> Steps 6, 10, 11 (payment + ad approval + domain renewals) are the **money-gates** (Charter §0.7). Steps 1–5, 7–9, 12 can be agent-executed after your one-time auth. Total hands-on time for a new site: **a few hours**, mostly waiting on OAuth screens and ad approval.

---

## 3. AUTONOMOUS AGENT LOOP (runs daily, zero human input)

Verified closed loop (DAILY_LOOP.md, run on sproutern Hobby):

```
CRON 0 3 * * *  →  daily-hermes-automation/loop.sh
 1. MEASURE : vercel metrics pageview(30d) + LCP/FCP/CLS/TTFB/INP(7d) + vercel ls + vercel logs (grep 4xx/5xx)
 2. DIAGNOSE: rank free signals; pick the 1 weakest (7-day rotation guarantees coverage)
 3. IMPROVE : ONE scoped, git-committed edit (content / SEO / speed / reliability / monetization)
 4. BUILD   : npm run build (keyless: ignoreBuildErrors, --max-old-space-size=8192, timeout 540s)
 5. DEPLOY  : git push origin main → Vercel auto-deploys (or `vercel deploy --prod`)
 6. VERIFY  : re-pull LCP + pageviews + logs; if LCP regresses >20% or build fails → vercel rollback
 7. REPORT  : append IMPROVEMENT_LOG.md (before→after numbers); else backlog item
```

**Loop invariants (hard rules):**
- Exactly **ONE change per day** — reversible, git-committed. No big-bang rewrites.
- Build always **keyless** (ignoreBuildErrors, 8192 MB heap, timeout 540s) — the 8 GB host OOM-crashes full Next 16 tsc.
- **Auto-rollback** on LCP regression >20% or build failure.
- **FREE plan only** — never call gated metrics; never suggest Pro/paid upgrades.
- Report **real before→after numbers**; never claim "improved" without them.
- Private/source repo — never force-push.

**Two footguns already fixed in sproutern (do not repeat):**
1. Loop scripts end with `sys.exit(main())`, NOT `sys.exit(0)` — otherwise `decide.py` silently produces no `next_action.json`.
2. The cron relay has **no `/bin/bash`** — verify scripts with `sh -n`, not `bash -n`.

---

## 4. SEO / GEO / AEO (agent-driven, documented in sproutern)

All playbooks already exist in `sproutern-open-source/docs/` — the agent reuses them, doesn't reinvent:
- `SEO_IMPLEMENTATION*.md`, `SEO_PART2_ONPAGE.md`, `SEO_PART3_GEO.md`, `GEO_SEO_IMPLEMENTATION.md`
- `SEO_GEO_AEO_AUDIT_2026.md` — the AEO (Answer Engine Optimization) audit (current scores: Technical 85, On-Page 80, GEO 75, AEO 70)
- `HOW_TO_APPLY_SEO.md`, `KEYWORD_RESEARCH_CONTENT_SUMMARY.md`, `SEO-Outreach-Templates.md`

**What the agent does daily for SEO/GEO/AEO:**
- Adds original 800+ word pages (`daily_content_writer.py` enforces the guard, refuses future-dated posts) — this also attacks the AdSense "low-value content" rejection.
- Adds structured data / FAQ schema (AEO) and local/entity markup (GEO).
- Submits `sitemap.xml` + `IndexNow` (already integrated for 6 search engines) so new pages get indexed.
- Uses the daily `decide.py` weakest-signal pick to target the next SEO gap.

---

## 5. MONETIZATION (the realistic ladder)

All switches live in `src/config/monetization.ts` + `src/components/monetization/*` — **OFF by default** so the site stays AdSense-safe while traffic builds.

| Stream | Approval | Barrier | When to switch on |
|---|---|---|---|
| **Affiliate (Amazon `?tag=`)** | none | low | immediately |
| **UPI / donate (`premkumar016555@oksbi`)** | none | low | immediately |
| **Monetag / Ezoic** | easy / fast | low | once any traffic exists — **this is the AdSense fallback** |
| **AdSense** | strict | high | **re-apply ONLY after** the content upgrade below |

**AdSense rejection → recovery (already planned in repo):**
- `docs/ADSENSE_COMPLIANCE_PLAN.md`: add Terms of Service, refresh Privacy/Contact, fix blog architecture (not per-folder posts).
- `docs/ADSENSE_CONTENT_UPGRADE_GUIDE.md`: 1200–1800+ word pages, H1/H2/H3, author bio, last-updated, 5–8 FAQs with schema.
- **Decision rule:** if AdSense rejects → **use Monetag** (lower bar, live in days) and keep building original content; re-apply AdSense once 20–40+ quality pages exist.

---

## 6. MULTI-SITE SCALING (free, templated)

The sproutern loop is **templatable** — each new site reuses the same engine:
1. Fork `sproutern-open-source` → new repo.
2. `vercel link` / `wrangler login` once (human auth).
3. Copy `daily-hermes-automation/`; point `measure.py` at the new project slug.
4. Same cron (`0 3 * * *`), different project.

**Free limits (2026):** Vercel Hobby = unlimited projects, 100 GB bandwidth/mo; Cloudflare Workers = 100k req/day; GitHub Pages = 100 GB/mo. You can run **several sites in parallel at $0**.

---

## 7. END-TO-END EXAMPLE (sproutern, real files)

- **Loop:** `daily-hermes-automation/{measure,decide,improve,verify}.py` + `loop.sh`
- **Content quality:** `scripts/daily_content_writer.py` (≥800-word guard, no future-dates)
- **Monetization (off):** `src/config/monetization.ts`, `src/components/monetization/{AffiliateStrip,SponsorCTA,UpiDonate}.tsx`
- **SEO/GEO/AEO:** `docs/SEO_GEO_AEO_AUDIT_2026.md` + `SEO_PART*` series
- **AdSense recovery:** `docs/ADSENSE_CONTENT_UPGRADE_GUIDE.md`, `docs/ADSENSE_COMPLIANCE_PLAN.md`
- **Logs:** `IMPROVEMENT_LOG.md` (before→after), `DAILY_LOOP.md` (setup)
- **Live baseline (2026-07-14):** 4,653 pageviews/30d; LCP 1,925 ms (target <1,200 ms) — the loop's daily job is to push LCP down and pages up.

---

## 8. WHAT THE HUMAN NEVER HAS TO DO AGAIN (post-setup)

After §2 steps 1–12:
- ❌ write content → agent does (800+ word quality-guarded)
- ❌ do SEO/GEO/AEO coding → agent does daily
- ❌ deploy → auto on git push
- ❌ check analytics → agent collects + acts on it
- ❌ improve speed/SEO → agent's daily loop
- ✅ only: approve ad account (once), link payment (once), buy/renew domain (annual), verify GSC (once), and **cross the money-gates** when a payout is due.

---

## 9. REALISTIC EXPECTATIONS (truthful, not hype)

- The **automation is complete and works** (operation loop coded + scheduled + running).
- **Earning requires two things the agent cannot supply:** (1) real traffic (grows via SEO over *weeks–months*, not hours) and (2) ad-account approval + payment linkage (you).
- **Monetag** removes the AdSense approval bottleneck but still pays per impression — near-zero without audience.
- Documented booked revenue to date: **$0** (blocked at the gates). The system becomes a *money* loop when the first payout is recorded in `finance/revenue-ledger.csv`.
- No "guaranteed/passive income" claim is made or permitted (Charter §0.3).

---

## 10. END-GOAL LOOP (v4.0 §11 template, filled)

```
Objective: Run N free-hosted websites that earn via affiliate + ads after human approval.
Inputs: site repo (fork), hosting account (you auth), ad account (you approve), traffic.
Outputs / done: site live, daily loop running, monetization ON post-approval.
Success metric: real measured pageviews (Vercel CLI) + real payout in revenue-ledger.csv.
Failure condition: 90 days, <500 pageviews/mo, zero payout → pivot niche or kill.
Recovery: improve on-page SEO + add 20 original pages; re-apply AdSense; use Monetag.
Automation triggers: cron 0 3 * * * (daily loop); on-demand for new-site scaffolding.
Human checkpoints: domain buy, ad approval, payment linkage, first publish (§0.7).
Self-optimization: after 30 runs, keep 1-change/day invariant; promote winning templates.
```

*Complete autonomous-website system — operation is agent-driven and documented end-to-end;
money is human-gated and honest. Truth over narrative (Charter §0.8).*
