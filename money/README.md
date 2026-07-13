# 💰 Money Pipelines — Autonomous Income System

Part of the autonomous money system. Each pipeline turns free OSS tools from the
`ai-company` blueprint into a sellable, automated income stream.

## Pipeline #1 — Fiverr Gig Factory ✅
`pipeline1_fiverr_gig_factory.py` → generates 8 ready-to-publish Fiverr gigs
(title, description, 3 tiers, SEO tags) + n8n delivery stub.
- **Gigs generated:** `gigs/*.json` (8 files, paste-ready)
- Validated 2026 pricing: $120–$1500/gig, 95–99% margin

## Pipeline #2 — Cold-Email Agency ✅
`pipeline2_cold_email_agency.py` → generates a done-for-you cold-outreach package
(3-touch sequence, subject lines, n8n workflow, onboarding brief, report template).
- **Packages generated:** `email_packs/*.json` (5 niches)
- Validated 2026 pricing: $450–$700 setup + $99–$149/mo management, 95% margin
- Tools: n8n + Listmonk + Postal + Stirling-PDF (all free/self-hosted)

## Pipeline #3 — Video Generation Service ✅ (YOUR EDGE)
`pipeline3_video_service.py` → turns your `Automated-Video-Generator` into a service.
Generates per-format packages (gig copy, render manifest, delivery steps, pricing).
- **Packages generated:** `video_packs/*.json` (5 formats)
- Validated 2026 pricing: $150–$500/video, **99% margin ($0 API cost, self-hosted)**
- Tools: Remotion + Edge-TTS + free stock (Pexels/Pixabay)
- Formats: product-promo, faceless-short, explainer, social-batch, real-estate

## Pipeline #4 — AI Support Bot Deployer ✅
`pipeline4_support_bot.py` → done-for-you AI support bots on Chatwoot.
- **Packages generated:** `bot_packs/*.json` (5 verticals)
- Validated 2026 pricing: $500–$1200 setup + $99–$299/mo, 90% margin
- Tools: Chatwoot + Hermes/OpenClaw + agent-sentinel (all self-hosted)
- Verticals: ecommerce, saas, clinic, agency, local

## Pipeline #5 — SEO/Audit Reporter ✅
`pipeline5_seo_reporter.py` → recurring website/code audit reports (subscription).
- **Packages generated:** `audit_packs/*.json` (3 plans)
- Validated 2026 pricing: $49–$399/mo, **97% margin, pure recurring**
- Tools: codebase-inspection + secret-scanner + skill-lint + Stirling-PDF
- Plans: starter, pro, agency (white-label)

## Master orchestrator
`run_all.py` regenerates ALL packages + writes `INCOME_DASHBOARD.md`.
```bash
python run_all.py            # regenerate 26 packages + dashboard
python run_all.py --dry-run  # income totals only
python run_all.py self-test  # verify 5 pipelines, 26 packages
```
Current: **50 packages, 12 pipelines, $26,000+ combined one-time value.** Run `python money/run_all.py` to regenerate everything.

## Helper scripts
- `generate_listings.py` → turns all 50 packages into Fiverr/Upwork-ready `.md` copy under `listings/`
- `generate_moltbook_drafts.py` → seeds 12 promo drafts into `revenue/moltbook/` for the acquisition funnel
- `../GO_LIVE_CHECKLIST.md` → the 3 human gates, step-by-step, to go live in ~15 min

## Usage
```bash
python pipeline1_fiverr_gig_factory.py --list
python pipeline1_fiverr_gig_factory.py --service email-automation --out gigs/email.json
python pipeline1_fiverr_gig_factory.py self-test

python pipeline2_cold_email_agency.py --list
python pipeline2_cold_email_agency.py --niche saas --out email_packs/saas.json
python pipeline2_cold_email_agency.py self-test
```

## Idea bank
See `MONEY_AUTOMATION_IDEAS.md` (12 validated pipelines ranked by speed-to-first-dollar).

> Zero dependencies (stdlib only). Part of `Hermes-Full-Autonomous-Company/money/`.
