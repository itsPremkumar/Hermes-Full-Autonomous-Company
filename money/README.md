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
