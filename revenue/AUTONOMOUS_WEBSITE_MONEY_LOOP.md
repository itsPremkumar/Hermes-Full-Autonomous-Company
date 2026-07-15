# Autonomous Website Money Loop — Improved, Legitimate Workflow

**Reference implementation:** `itsPremkumar/sproutern-open-source` (public) and `itsPremkumar/sproutern-hermes` (Hermes-wired copy).
**Status:** the *operation* loop is real and already coded. The *money* path is real but **human-gated** (see §0.7 of the v4.0 master prompt).
**Last verified:** 2026-07-15 against live GitHub API + the `vercel-deploy-ops` / `cloudflare-deploy-ops` skills.

---

## 0. Honest framing (read this first)

This is a **legitimate, repeatable content+SEO+monetization engine** — NOT a "money printer." Truths the operator must accept:

1. **The loop runs itself daily. The money does not.** Content, SEO, deploy, and improvement can be 100% agent-driven. Revenue requires (a) real human traffic and (b) platform approvals that only you can complete.
2. **AdSense was REJECTED for sproutern** ("low-value content" — caused by auto-generated, future-dated blog posts). It stays rejected on any clone until content is cleaned + 20–40+ original pages added. Monetag/Ezoic are easier-entry alternatives but still pay per impression, so they earn ~nothing without traffic.
3. **"Immediate approval" ad networks** (Monetag etc.) lower the *approval* bar, not the *earning* bar. Earnings scale with audience, not with automation.
4. **Free hosting is real and sufficient** to validate the model. You do not need to buy a domain to start; free subdomains work. Buy a domain only when traffic justifies it.
5. Every public claim about income must be true (Charter §0.3). Do not publish "passive income" / "guaranteed" framing — it is both false and a policy violation.

---

## 1. Architecture (what actually gets wired)

```
        YOU (principal) — crosses the 3 money-gates (§6), buys domain if wanted
                 │
        HERMES (1st boss) — schedules + supervises the loop; persists all artifacts
              │
              ├─ WEBSITE REPO (Next.js)  e.g. sproutern-open-source
              │     ├─ daily-hermes-automation/  (measure→decide→improve→verify)
              │     ├─ scripts/daily_content_writer.py  (≥800-word guard, no future-dates)
              │     ├─ src/config/monetization.ts  (AdSense/affiliate/UPI — OFF by default)
              │     └─ docs/  (SEO / GEO / AEO / ADSENSE_* plans)
              │
              ├─ HOSTING (pick ONE per site; all free tiers exist)
              │     ├─ Vercel Hobby  (auto-deploy on git push; *.vercel.app)
              │     ├─ Cloudflare Pages/Workers  (free 100k req/day; *.workers.dev)
              │     ├─ GitHub Pages  (static; *.github.io)
              │     └─ Netlify Free
              │
              ├─ DATA COLLECTION (MCP / CLI)
              │     ├─ Vercel: `vercel` CLI + REST (the repo `.mcp.json` is EDITOR-SIDE only)
              │     └─ Cloudflare: `@cloudflare/mcp-server-cloudflare` (works; ~89 tools)
              │
              └─ MONETIZATION (all OFF until approved + traffic)
                    ├─ AdSense (re-apply after content fix)
                    ├─ Monetag / Ezoic (lower approval bar)
                    └─ Affiliate (Amazon ?tag=) + UPI (premkumar016555@oksbi) — zero approval
```

**Key correction to the original idea:** "MCP connects and collects data daily" → the agent collects data daily via the **Vercel CLI / Cloudflare MCP + a cron loop**, not via a magic always-on MCP. The `website-improvement-loop` cron (job `596366de8767`, `0 3 * * *`) already does this for sproutern.

---

## 2. Phase A — One-time HUMAN setup (you do this once per site)

| # | Step | Who | Notes |
|---|---|---|---|
| 1 | Create the site repo (fork `sproutern-open-source` as template) | You / Hermes drafts | `git clone` + rename |
| 2 | Connect hosting (Vercel `vercel link` / Cloudflare `wrangler login`) | You authenticate once | Hermes deploys afterward headlessly |
| 3 | Enable Vercel Web Analytics + Speed Insights | Hermes via CLI | free on Hobby |
| 4 | Install + authenticate the loop cron | Hermes | `website-improvement-loop` |
| 5 | **Buy domain OR use free subdomain** | You (if buying) | `yourname.vercel.app` is free; a real domain helps SEO/GEO trust |
| 6 | **Ad network account + approval** | You (KYC/approval) | AdSense/Monetag need your account; agent cannot complete KYC |
| 7 | **Payment linkage** | You | PayPal/bank/UPI — agent never holds credentials |

Steps 5–7 are the **money-gates** (Charter §0.7). They are NOT one-time-then-forgotten for *every* new site/payout — each new site and each payout threshold may re-trigger a check.

---

## 3. Phase B — Autonomous DAILY operation (Hermes runs this)

The closed loop (verified live on sproutern, Hobby plan):

```
CRON 0 3 * * *  →  daily-hermes-automation/loop.sh
 1. MEASURE : vercel metrics pageview(30d) + LCP/FCP/CLS/TTFB/INP(7d) + vercel ls + vercel logs (grep 4xx/5xx)
 2. DIAGNOSE: rank signals; pick the 1 worst issue
 3. IMPROVE : ONE scoped, git-committed edit (never a rewrite)
 4. BUILD   : npm run build (keyless: ignoreBuildErrors, --max-old-space-size=8192, timeout 540)
 5. DEPLOY  : git push → Vercel auto-deploys (or `vercel deploy --prod`)
 6. VERIFY  : re-pull LCP + pageviews + logs; if LCP regresses >20% or build fails → vercel rollback
 7. REPORT  : append IMPROVEMENT_LOG.md (before→after numbers); else backlog item
```

**Loop invariants (never violate):**
- Exactly ONE change per day — reversible, git-committed. No big-bang rewrites.
- Build always keyless (ignoreBuildErrors, 8192 MB heap, timeout 540s).
- Auto-rollback on LCP regression >20% or build failure.
- FREE plan only — never call gated metrics; never suggest Pro/paid.
- Report real before→after numbers; never claim "improved" without them.

**Two footguns already fixed in sproutern (do not repeat):**
1. Loop scripts must end with `sys.exit(main())`, not `sys.exit(0)` — otherwise `decide.py` silently produces no `next_action.json`.
2. The cron relay has **no `/bin/bash`** — verify with `sh -n`, not `bash -n`.

---

## 4. SEO / GEO / AEO (already documented in sproutern)

`sproutern-open-source/docs/` already contains the full playbook — reuse, don't reinvent:
- `SEO_IMPLEMENTATION*.md`, `SEO_PART2_ONPAGE.md`, `SEO_PART3_GEO.md`, `GEO_SEO_IMPLEMENTATION.md`
- `SEO_GEO_AEO_AUDIT_2026.md` — the AEO (Answer Engine Optimization) audit
- `HOW_TO_APPLY_SEO.md`, `KEYWORD_RESEARCH_CONTENT_SUMMARY.md`, `SEO-Outreach-Templates.md`

**How Hermes improves SEO/GEO/AEO daily:** the loop's `decide.py` ranks the worst signal; one daily edit targets it — e.g. add an original 800+ word page (kills the "low-value content" AdSense rejection), add structured data / FAQ schema (AEO), add local/entity markup (GEO). `scripts/daily_content_writer.py` enforces the 800-word guard and refuses future-dated posts.

---

## 5. Monetization (honest path)

All switches live in `src/config/monetization.ts` + `src/components/monetization/*` — **OFF by default** so the site stays AdSense-safe while building traffic.

| Stream | Approval | Barrier | Realistic timing |
|---|---|---|---|
| **Affiliate (Amazon `?tag=`)** | none | low | works immediately; pays on sales |
| **UPI / donate (`premkumar016555@oksbi`)** | none | low | immediate; depends on audience goodwill |
| **Monetag / Ezoic** | easy/fast | low | live in days; pays per impression (tiny without traffic) |
| **AdSense** | strict | high | re-apply ONLY after cleaning low-value content + 20–40+ original pages |

**Order to switch on (per Charter §10):** affiliate + UPI first (zero approval) → Monetag once traffic exists → AdSense re-apply last, after the content upgrade documented in `docs/ADSENSE_CONTENT_UPGRADE_GUIDE.md`.

---

## 6. The 3 money-gates (permanent human checkpoints — Charter §0.7)

1. **Marketplace / ad-network identity** — AdSense/Monetag KYC needs your ID. Agent prepares the application; cannot complete it.
2. **Payment linkage** — PayPal / bank / UPI needs your credentials. Agent never enters them.
3. **First publish / payout** — pasting the listing, clicking "Publish", or first withdrawal needs your click.

The agent builds the entire machine, then **STOPS at the gate**. ~15 min of your action per site = go-live.

---

## 7. Multi-site scaling (free)

The sproutern loop is **templatable**. For each new site:
1. Fork `sproutern-open-source` → new repo.
2. `vercel link` / `wrangler login` once (human).
3. Copy `daily-hermes-automation/` + point `measure.py` at the new project name.
4. Same cron pattern, different project slug.

Free limits per provider (2026): Vercel Hobby = unlimited projects, 1 prod deploy/concurrent, 100 GB bandwidth/mo; Cloudflare Workers = 100k requests/day; GitHub Pages = 100 GB/mo. You can run **several sites in parallel at $0**.

---

## 8. Concrete sproutern example (real files)

- Loop: `daily-hermes-automation/{measure,decide,improve,verify}.py` + `loop.sh`
- Content quality: `scripts/daily_content_writer.py` (≥800-word guard, no future-dates)
- Monetization (off): `src/config/monetization.ts`, `src/components/monetization/{AffiliateStrip,SponsorCTA,UpiDonate}.tsx`
- SEO/GEO/AEO: `docs/SEO_GEO_AEO_AUDIT_2026.md` + the `SEO_PART*` series
- AdSense recovery: `docs/ADSENSE_CONTENT_UPGRADE_GUIDE.md`, `docs/ADSENSE_COMPLIANCE_PLAN.md`
- Logs: `IMPROVEMENT_LOG.md` (before→after table), `DAILY_LOOP.md` (setup)

Live baseline (sproutern, 2026-07-14): 4,653 pageviews/30d; LCP 1,925 ms (target <1,200 ms). The loop's daily job is to push LCP down and pages up.

---

## 9. What will NOT happen automatically (set expectations)

- No revenue without traffic. Automation grows traffic slowly via SEO; it is not instant.
- No approval without you. AdSense/Monetag/payment = your accounts.
- No "guaranteed income." Any framing claiming otherwise is a Charter violation.
- AdSense rejection does not auto-clear. It needs the content upgrade in §5/§8.
- Free tiers have limits (bandwidth/requests). Scale = more free projects, not paid upgrades (per "FREE Hobby ONLY" rule).

---

## 10. End-Goal Loop (filled per v4.0 §11)

```
Objective: Run N free-hosted websites that earn via affiliate+ads after human approval.
Inputs needed: site repo (fork), hosting account (you auth), ad account (you approve), traffic.
Outputs / definition of done: site live, daily loop running, monetization switched on post-approval.
Success metric: real measured pageviews (Vercel CLI) + real payout recorded in finance/revenue-ledger.csv.
Failure condition: 90 days, <500 pageviews/mo, zero payout → pivot niche or kill.
Recovery strategy: improve on-page SEO + add 20 original pages; re-apply AdSense; try Monetag.
Automation triggers: cron 0 3 * * * (daily loop); on-demand for new-site scaffolding.
Human checkpoints: domain buy, ad-network approval, payment linkage, first publish (§0.7).
Self-optimization note: after 30 runs, keep the 1-change/day invariant; promote winning niche templates.
```

*Legitimate autonomous-website engine — operation is agent-driven, money is human-gated. Truth over narrative (Charter §0.8).*
